#!/usr/bin/env python3
"""CogniRouter installer.

Installs a provider-neutral skill-routing policy plus a skill library into the
AI coding hosts found on this machine (Claude Code, Codex, Gemini CLI,
Qwen Code, opencode, ...) or into a single project (AGENTS.md / CLAUDE.md).

Standard library only. Python 3.8+. Git is needed only to fetch upstream skills.

Commands:
  install    install core + skills + host instruction blocks
  status     show what is installed
  uninstall  remove everything this tool installed (instruction blocks, skills, agents)
  export     write a single-file prompt for web chats (ChatGPT, GLM, Gemini, Claude Projects)
  index      rebuild SKILLS_INDEX.md
  lock       show or refresh upstream pins (--refresh queries the remote HEAD)
  hosts      list supported hosts and whether they are detected
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

VERSION = "1.1.0"
NAME = "cognirouter"
MARK_START = "<!-- COGNIROUTER:START -->"
MARK_END = "<!-- COGNIROUTER:END -->"
MANAGED_MARKER = ".cognirouter.json"
REPO = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# --------------------------------------------------------------------------- hosts

def host_table(home: Path, use_env: bool = True) -> dict:
    """Instruction file, skills dir and agents dir for every supported host."""
    codex_home = Path(os.environ["CODEX_HOME"]) if use_env and os.environ.get("CODEX_HOME") else home / ".codex"
    xdg = home / ".config"
    return {
        "claude": {
            "label": "Claude Code (also GLM / Kimi / DeepSeek via an Anthropic-compatible endpoint)",
            "detect": [home / ".claude"], "cli": "claude",
            "instructions": home / ".claude" / "CLAUDE.md",
            "skills": home / ".claude" / "skills",
            "agents": home / ".claude" / "agents",
        },
        "codex": {
            "label": "OpenAI Codex CLI / app",
            "detect": [codex_home], "cli": "codex",
            "instructions": codex_home / "AGENTS.md",
            "skills": home / ".agents" / "skills",
        },
        "gemini": {
            "label": "Google Gemini CLI",
            "detect": [home / ".gemini"], "cli": "gemini",
            "instructions": home / ".gemini" / "GEMINI.md",
            "skills": home / ".agents" / "skills",
        },
        "qwen": {
            "label": "Qwen Code",
            "detect": [home / ".qwen"], "cli": "qwen",
            "instructions": home / ".qwen" / "QWEN.md",
            "skills": home / ".qwen" / "skills",
        },
        "opencode": {
            "label": "opencode (any provider: GLM, DeepSeek, Kimi, OpenRouter, local models)",
            "detect": [xdg / "opencode"], "cli": "opencode",
            "instructions": xdg / "opencode" / "AGENTS.md",
            "skills": xdg / "opencode" / "skills",
        },
    }


ALIASES = {
    "glm": "claude", "zai": "claude", "zhipu": "claude",
    "kimi": "claude", "deepseek": "claude",
    "openai": "codex", "chatgpt": "codex", "google": "gemini",
}


def resolve_hosts(spec: str, table: dict) -> list:
    if spec in ("auto", ""):
        found = []
        for name, h in table.items():
            if any(p.exists() for p in h["detect"]) or shutil.which(h["cli"]):
                found.append(name)
        return found
    if spec == "all":
        return list(table)
    out = []
    for raw in spec.split(","):
        n = ALIASES.get(raw.strip().lower(), raw.strip().lower())
        if n not in table:
            raise SystemExit(f"Unknown host '{raw}'. Supported: {', '.join(table)} (aliases: {', '.join(ALIASES)})")
        if n not in out:
            out.append(n)
    return out


# --------------------------------------------------------------------------- utils

class Ctx:
    def __init__(self, args):
        self.home = Path(args.home).expanduser().resolve() if getattr(args, "home", None) else Path.home()
        self.root = self.home / f".{NAME}"
        self.dry = getattr(args, "dry_run", False)
        self.force = getattr(args, "force", False)
        self.stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.backup_dir = self.root / "backups" / self.stamp
        self.state_path = self.root / "state.json"
        self.use_env = not getattr(args, "home", None)

    def log(self, msg):
        print(("[dry-run] " if self.dry else "") + msg)

    def load_state(self) -> dict:
        if self.state_path.exists():
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        return {"version": VERSION, "hosts": {}, "projects": {}, "upstream": {}}

    def save_state(self, st):
        if self.dry:
            return
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        st["version"] = VERSION
        st["updated_at"] = _dt.datetime.now().isoformat(timespec="seconds")
        self.state_path.write_text(json.dumps(st, indent=2), encoding="utf-8")

    def backup(self, path: Path, label: str):
        if self.dry or not path.exists():
            return
        dest = self.backup_dir / label
        dest.parent.mkdir(parents=True, exist_ok=True)
        if path.is_dir():
            shutil.copytree(path, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(path, dest)


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _write_lf(p: Path, text: str):
    # Path.write_text(newline=) needs Python 3.10; open() keeps 3.8 support.
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_text(ctx: Ctx, p: Path, text: str):
    if ctx.dry:
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    _write_lf(p, text)


def rmtree(path: Path):
    """shutil.rmtree that also removes read-only files (Git pack files on Windows)."""
    import stat

    def _retry(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)

    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=_retry)
    else:
        shutil.rmtree(path, onerror=_retry)


def posix(p: Path) -> str:
    return str(p).replace("\\", "/")


def tree_hash(path: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(path.rglob("*")):
        if f.is_file() and f.name != MANAGED_MARKER and "__pycache__" not in f.parts:
            h.update(posix(f.relative_to(path)).encode())
            h.update(f.read_bytes())
    return h.hexdigest()


def parse_frontmatter(skill_md: Path) -> dict:
    text = read_text(skill_md)
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    meta = {}
    if not m:
        return meta
    key = None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            meta[key] = val.strip("'\"")
        elif key and line.startswith((" ", "\t")):
            meta[key] = (meta[key] + " " + line.strip()).strip()
    return meta


def replace_block(text: str, block: str) -> str:
    body = f"{MARK_START}\n{block.strip()}\n{MARK_END}"
    pat = re.compile(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), re.S)
    if pat.search(text):
        return pat.sub(lambda _m: body, text, count=1)
    sep = "" if not text.strip() else ("\n" if text.endswith("\n") else "\n\n")
    return f"{text}{sep}\n{body}\n" if text.strip() else body + "\n"


def remove_block(text: str) -> str:
    pat = re.compile(r"\n*" + re.escape(MARK_START) + r".*?" + re.escape(MARK_END) + r"\n?", re.S)
    return pat.sub("\n", text).strip() + ("\n" if text.strip() else "")


# --------------------------------------------------------------------------- upstream

def load_lock() -> dict:
    return json.loads((REPO / "upstream.lock.json").read_text(encoding="utf-8"))


def git(*args, cwd=None, check=True):
    return subprocess.run(["git", *args], cwd=cwd, check=check, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def fetch_upstream(ctx: Ctx, up: dict) -> Path:
    store = ctx.root / "store" / up["id"]
    if ctx.dry:
        ctx.log(f"fetch {up['repo']} @ {up['commit'][:10]}")
        return store
    if not shutil.which("git"):
        raise RuntimeError("git is required to fetch upstream skills (or pass --no-upstream)")
    if not (store / ".git").exists():
        store.parent.mkdir(parents=True, exist_ok=True)
        git("-c", "core.symlinks=false", "clone", "--filter=blob:none", "--no-checkout", up["repo"], str(store))
    have = git("cat-file", "-e", up["commit"] + "^{commit}", cwd=store, check=False).returncode == 0
    if not have:
        git("fetch", "origin", up["commit"], cwd=store, check=False)
        git("fetch", "origin", cwd=store)
    git("-c", "core.symlinks=false", "checkout", "--force", "--detach", up["commit"], cwd=store)
    return store


def _symlinks(store: Path, commit: str, path: str) -> dict:
    """Git symlinks (mode 120000) under path -> target, resolved manually so Windows works."""
    out = git("ls-tree", "-r", commit, "--", path, cwd=store).stdout
    links = {}
    for line in out.splitlines():
        meta, _, rel = line.partition("\t")
        mode, _, sha = meta.split()
        if mode == "120000":
            links[rel] = git("cat-file", "-p", sha, cwd=store).stdout.strip()
    return links


def materialize_upstream_skill(ctx: Ctx, store: Path, up: dict, spec: dict, dest: Path):
    src = store if spec["path"] == "." else store / spec["path"]
    if ctx.dry:
        ctx.log(f"  skill {spec['name']} <- {up['id']}:{spec['path']}")
        return
    if not (src / "SKILL.md").exists():
        raise RuntimeError(f"{up['id']}: {spec['path']}/SKILL.md not found at {up['commit'][:10]}; update upstream.lock.json")
    excludes = set(spec.get("exclude", [])) | {".git"}
    if dest.exists():
        rmtree(dest)
    shutil.copytree(src, dest, ignore=lambda d, names: [n for n in names if n in excludes and Path(d) == src])
    for rel, target in _symlinks(store, up["commit"], spec["path"]).items():
        link_path = store / rel
        resolved = (link_path.parent / target).resolve()
        local = dest / (rel if spec["path"] == "." else os.path.relpath(rel, spec["path"]))
        if local.exists() and local.is_file():
            local.unlink()
        if resolved.is_dir():
            shutil.copytree(resolved, local, dirs_exist_ok=True)
        elif resolved.is_file():
            local.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(resolved, local)
    (dest / MANAGED_MARKER).write_text(json.dumps({
        "tool": NAME, "source": up["repo"], "commit": up["commit"], "path": spec["path"]}, indent=2), encoding="utf-8")


def selected_upstreams(args) -> list:
    lock = load_lock()["upstreams"]
    if args.no_upstream:
        return []
    if args.upstream in (None, "", "default"):
        return [u for u in lock if u.get("default", True)]
    if args.upstream == "all":
        return lock
    want = {x.strip() for x in args.upstream.split(",")}
    unknown = want - {u["id"] for u in lock}
    if unknown:
        raise SystemExit(f"Unknown upstream id(s): {', '.join(sorted(unknown))}")
    return [u for u in lock if u["id"] in want]


# --------------------------------------------------------------------------- library

def build_library(ctx: Ctx, args, state: dict) -> Path:
    """Copy core + own skills + upstream skills into ~/.cognirouter (the canonical library)."""
    lib = ctx.root / "skills"
    ctx.log(f"library -> {ctx.root}")
    if not ctx.dry:
        for sub in ("core", "scripts"):
            if (ctx.root / sub).exists():
                rmtree(ctx.root / sub)
            shutil.copytree(REPO / sub, ctx.root / sub)
        (ctx.root / "local").mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / "local" / "MCP_DESTINATIONS.example.md", ctx.root / "local" / "MCP_DESTINATIONS.example.md")
        lib.mkdir(parents=True, exist_ok=True)
    for skill in sorted((REPO / "skills").iterdir()):
        if not (skill / "SKILL.md").exists():
            continue
        dest = lib / skill.name
        if not ctx.dry:
            if dest.exists():
                rmtree(dest)
            shutil.copytree(skill, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (dest / MANAGED_MARKER).write_text(json.dumps({"tool": NAME, "source": "cognirouter", "version": VERSION}, indent=2), encoding="utf-8")
    ups = selected_upstreams(args)
    state.setdefault("upstream", {})
    for up in ups:
        try:
            store = fetch_upstream(ctx, up)
            for spec in up["skills"]:
                materialize_upstream_skill(ctx, store, up, spec, lib / spec["name"])
            state["upstream"][up["id"]] = up["commit"]
        except (RuntimeError, subprocess.CalledProcessError) as e:
            err = getattr(e, "stderr", "") or str(e)
            print(f"WARNING: upstream '{up['id']}' skipped: {err.strip()[:300]}")
    write_index(ctx, lib, ctx.root / "SKILLS_INDEX.md")
    return lib


def skill_rows(lib: Path) -> list:
    rows = []
    for d in sorted(lib.iterdir(), key=lambda p: p.name.lower()) if lib.exists() else []:
        if not (d / "SKILL.md").exists():
            continue
        meta = parse_frontmatter(d / "SKILL.md")
        src = "cognirouter"
        mk = d / MANAGED_MARKER
        if mk.exists():
            try:
                src = json.loads(read_text(mk)).get("source", src)
            except ValueError:
                pass
        src = re.sub(r"^https://github.com/|\.git$", "", src)
        desc = re.sub(r"\s+", " ", meta.get("description", "")).replace("|", "/")
        if len(desc) > 260:
            desc = desc[:257].rsplit(" ", 1)[0] + "..."
        rows.append((meta.get("name", d.name), desc, src))
    return rows


def write_index(ctx: Ctx, lib: Path, out: Path):
    rows = skill_rows(lib) if not ctx.dry else skill_rows(REPO / "skills")
    lines = ["# Skills index", "",
             "Generated by CogniRouter. Pick by intent; load only what the task needs.",
             "Path: `<skills dir>/<name>/SKILL.md` (the skills dir is named in your host instruction block).", "",
             "| Skill | Use when | Source |", "|---|---|---|"]
    lines += [f"| `{n}` | {d} | {s} |" for n, d, s in rows]
    write_text(ctx, out, "\n".join(lines) + "\n")
    ctx.log(f"index: {len(rows)} skills -> {out}")


def render_block(ctx: Ctx, host: str, skills_dir: Path) -> str:
    tpl = read_text(REPO / "core" / "ROUTER.md")
    return (tpl.replace("{{HOST}}", host)
               .replace("{{ROUTER_HOME}}", posix(ctx.root))
               .replace("{{SKILLS_DIR}}", posix(skills_dir)))


# --------------------------------------------------------------------------- install

def sync_skills(ctx: Ctx, lib: Path, dest_dir: Path, host: str, prev: list) -> list:
    """Copy library skills into a host skills dir. Never overwrites an unmanaged skill unless --force."""
    installed = []
    names = [d.name for d in sorted(lib.iterdir())] if lib.exists() else [d.name for d in sorted((REPO / "skills").iterdir())]
    for name in names:
        src, dest = lib / name, dest_dir / name
        if dest.resolve() == src.resolve():
            installed.append(name)
            continue
        if dest.exists() or dest.is_symlink():
            managed = (dest / MANAGED_MARKER).exists() or name in prev
            if not managed:
                if not ctx.force:
                    if not ctx.dry and src.exists() and dest.is_dir() and tree_hash(dest) == tree_hash(src):
                        installed.append(name)
                        continue
                    print(f"  skip {host}:{name} (an unmanaged skill with this name exists; --force backs it up and replaces it)")
                    continue
                ctx.log(f"  backup {dest}")
                ctx.backup(dest, f"{host}/skills/{name}")
            if not ctx.dry:
                if dest.is_symlink() or dest.is_file():
                    dest.unlink()
                else:
                    rmtree(dest)
        if not ctx.dry:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dest)
        installed.append(name)
    ctx.log(f"  {host}: {len(installed)} skills -> {dest_dir}")
    return installed


def sync_agents(ctx: Ctx, dest_dir: Path, prev: list) -> list:
    out = []
    for f in sorted((REPO / "agents" / "claude").glob("*.md")):
        dest = dest_dir / f.name
        if dest.exists() and f.name not in prev and read_text(dest) != read_text(f):
            if not ctx.force:
                print(f"  skip agent {f.name} (exists, unmanaged; --force replaces it)")
                continue
            ctx.backup(dest, f"claude/agents/{f.name}")
        if not ctx.dry:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
        out.append(f.name)
    ctx.log(f"  claude: {len(out)} subagents -> {dest_dir}")
    return out


def write_instruction_block(ctx: Ctx, path: Path, block: str, label: str):
    old = read_text(path)
    new = replace_block(old, block)
    if new == old:
        ctx.log(f"  {label}: instruction block unchanged ({path})")
        return
    if old and MARK_START not in old:
        ctx.backup(path, f"{label}/{path.name}")
    write_text(ctx, path, new)
    ctx.log(f"  {label}: instruction block -> {path}")


def cmd_install(args):
    ctx = Ctx(args)
    table = host_table(ctx.home, ctx.use_env)
    state = ctx.load_state()
    lib = build_library(ctx, args, state)

    if args.project:
        proj = Path(args.project).expanduser().resolve()
        block = render_block(ctx, "project", lib)
        write_instruction_block(ctx, proj / "AGENTS.md", block, "project")
        claude_md = proj / "CLAUDE.md"
        write_instruction_block(ctx, claude_md, "Follow the shared agent instructions in @AGENTS.md (CogniRouter block).", "project-claude")
        state.setdefault("projects", {})[posix(proj)] = {"files": ["AGENTS.md", "CLAUDE.md"]}
        ctx.save_state(state)
        print(f"Project ready: {proj} (AGENTS.md is read by Codex, Cursor, opencode, Copilot, Windsurf, Zed, Amp, Jules...; CLAUDE.md imports it)")
        return

    hosts = resolve_hosts(args.hosts, table)
    if not hosts:
        print("No supported host detected. Use --hosts claude,codex,gemini,qwen,opencode (or 'all'), or --project DIR.")
    for name in hosts:
        h = table[name]
        prev = state["hosts"].get(name, {})
        ctx.log(f"host {name}: {h['label']}")
        entry = {"instructions": posix(h["instructions"]), "skills_dir": posix(h["skills"])}
        if not args.no_skills:
            entry["skills"] = sync_skills(ctx, lib, h["skills"], name, prev.get("skills", []))
        else:
            entry["skills"] = []
        skills_dir = h["skills"] if not args.no_skills else lib
        if "agents" in h:
            entry["agents_dir"] = posix(h["agents"])
            entry["agents"] = sync_agents(ctx, h["agents"], prev.get("agents", []))
        write_instruction_block(ctx, h["instructions"], render_block(ctx, name, skills_dir), name)
        state["hosts"][name] = entry
    ctx.save_state(state)
    if not ctx.dry and ctx.backup_dir.exists():
        print(f"Backups: {ctx.backup_dir}")
    print("Done. Restart the AI tool (new session) so it loads the new instructions.")


# --------------------------------------------------------------------------- other commands

def cmd_status(args):
    ctx = Ctx(args)
    st = ctx.load_state()
    if not ctx.state_path.exists():
        print(f"CogniRouter is not installed under {ctx.root}")
        return
    print(f"CogniRouter {st.get('version')} at {ctx.root} (updated {st.get('updated_at')})")
    print(f"Library: {len(skill_rows(ctx.root / 'skills'))} skills; upstream pins: " +
          (", ".join(f"{k}@{v[:8]}" for k, v in st.get("upstream", {}).items()) or "none"))
    for name, e in st.get("hosts", {}).items():
        block = MARK_START in read_text(Path(e["instructions"]))
        print(f"- {name}: block {'OK' if block else 'MISSING'} in {e['instructions']}; "
              f"{len(e.get('skills', []))} skills in {e['skills_dir']}"
              + (f"; {len(e.get('agents', []))} agents" if "agents" in e else ""))
    for p in st.get("projects", {}):
        print(f"- project: {p}")


def cmd_uninstall(args):
    ctx = Ctx(args)
    st = ctx.load_state()
    table = host_table(ctx.home, ctx.use_env)
    targets = list(st.get("hosts", {})) if args.hosts in ("auto", "all", "") else resolve_hosts(args.hosts, table)
    for name in targets:
        e = st["hosts"].get(name)
        if not e:
            continue
        p = Path(e["instructions"])
        if MARK_START in read_text(p):
            ctx.log(f"{name}: remove block from {p}")
            write_text(ctx, p, remove_block(read_text(p)))
        shared = {s for other, oe in st["hosts"].items() if other != name and oe["skills_dir"] == e["skills_dir"] for s in oe.get("skills", [])}
        for s in e.get("skills", []):
            d = Path(e["skills_dir"]) / s
            if s in shared or not (d / MANAGED_MARKER).exists():
                continue
            ctx.log(f"{name}: remove skill {d}")
            if not ctx.dry:
                rmtree(d)
        for a in e.get("agents", []):
            f = Path(e["agents_dir"]) / a
            if f.exists():
                ctx.log(f"{name}: remove agent {f}")
                if not ctx.dry:
                    f.unlink()
        del st["hosts"][name]
    if args.project:
        proj = Path(args.project).expanduser().resolve()
        for fn in ("AGENTS.md", "CLAUDE.md"):
            p = proj / fn
            if MARK_START in read_text(p):
                ctx.log(f"project: remove block from {p}")
                write_text(ctx, p, remove_block(read_text(p)))
        st.get("projects", {}).pop(posix(proj), None)
    if args.purge and not st.get("hosts") and not st.get("projects"):
        ctx.log(f"purge {ctx.root}")
        if not ctx.dry and ctx.root.exists():
            rmtree(ctx.root)
        return
    ctx.save_state(st)
    print("Uninstalled. Backups (if any) remain under " + posix(ctx.root / "backups"))


def cmd_export(args):
    ctx = Ctx(args)
    lib = ctx.root / "skills" if (ctx.root / "skills").exists() else REPO / "skills"
    block = render_block(ctx, "web-chat", Path("<skills>"))
    block = block.replace(posix(ctx.root) + "/core/", "the policy section below: ")
    block = block.replace(posix(ctx.root) + "/SKILLS_INDEX.md", "the skills index below")
    parts = [block,
             "\n---\n\n" + read_text(REPO / "core" / "NATURAL_LANGUAGE_ROUTING.md"),
             "\n---\n\n" + read_text(REPO / "core" / "SAFETY_POLICY.md"),
             "\n---\n\n## Skills index\n\nNo file access in a web chat: when a skill is needed, use the ones pasted below; for any other, ask the user to paste its SKILL.md.\n\n"
             + "\n".join(f"- `{n}`: {d}" for n, d, _ in skill_rows(lib))]
    for name in [s for s in (args.with_skills or "").split(",") if s.strip()]:
        f = lib / name.strip() / "SKILL.md"
        if not f.exists():
            raise SystemExit(f"Skill not found: {name}")
        parts.append(f"\n---\n\n<!-- skill: {name.strip()} -->\n" + read_text(f))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    _write_lf(out, "".join(parts))
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB). Paste it into the system prompt / custom instructions / project knowledge.")


def cmd_index(args):
    ctx = Ctx(args)
    out = Path(args.out) if args.out else REPO / "docs" / "SKILLS.md"
    lib = Path(args.lib) if args.lib else REPO / "skills"
    write_index(ctx, lib, out)


def cmd_lock(args):
    lock = load_lock()
    for up in lock["upstreams"]:
        line = f"{up['id']:<22} {up['commit'][:12]}  {'default' if up.get('default', True) else 'opt-in '}  {up['repo']}"
        if args.refresh:
            r = git("ls-remote", up["repo"], "HEAD", check=False)
            head = r.stdout.split()[0] if r.returncode == 0 and r.stdout else None
            if head and head != up["commit"]:
                line += f"  -> {head[:12]}"
                up["commit"] = head
        print(line)
    if args.refresh:
        (REPO / "upstream.lock.json").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
        print("upstream.lock.json updated. Re-run install and review upstream changes before committing.")


def cmd_hosts(args):
    ctx = Ctx(args)
    table = host_table(ctx.home, ctx.use_env)
    detected = set(resolve_hosts("auto", table))
    for n, h in table.items():
        print(f"{'*' if n in detected else ' '} {n:<9} {h['label']}\n            instructions: {h['instructions']}\n            skills:       {h['skills']}")
    print("\nAliases: " + ", ".join(f"{a}->{t}" for a, t in ALIASES.items()))
    print("Any other tool that reads AGENTS.md: use  install --project <repo>")


def main(argv=None):
    p = argparse.ArgumentParser(prog="cognirouter", description="CogniRouter: provider-neutral skill routing for AI coding agents.")
    p.add_argument("--version", action="version", version=f"cognirouter {VERSION}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--home", help="override the home directory (testing / portable installs)")
        sp.add_argument("--dry-run", action="store_true", help="print actions without writing")

    sp = sub.add_parser("install", help="install core, skills, and instruction blocks")
    common(sp)
    sp.add_argument("--hosts", default="auto", help="auto | all | comma list: claude,codex,gemini,qwen,opencode (aliases: glm, kimi, deepseek...)")
    sp.add_argument("--project", help="install into one repository (AGENTS.md + CLAUDE.md) instead of global hosts")
    sp.add_argument("--upstream", default="default", help="default | all | comma list of upstream ids")
    sp.add_argument("--no-upstream", action="store_true", help="skip third-party skills (no git/network needed)")
    sp.add_argument("--no-skills", action="store_true", help="only write instruction blocks; skills stay in ~/.cognirouter/skills")
    sp.add_argument("--force", action="store_true", help="back up and replace unmanaged skills/agents with the same name")
    sp.set_defaults(func=cmd_install)

    sp = sub.add_parser("status", help="show installation status"); common(sp); sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("uninstall", help="remove what CogniRouter installed")
    common(sp)
    sp.add_argument("--hosts", default="all")
    sp.add_argument("--project")
    sp.add_argument("--purge", action="store_true", help="also delete ~/.cognirouter when nothing is left")
    sp.set_defaults(func=cmd_uninstall)

    sp = sub.add_parser("export", help="single-file prompt for web chats")
    common(sp)
    sp.add_argument("--out", default="dist/cognirouter-prompt.md")
    sp.add_argument("--with-skills", help="comma list of skills to inline, e.g. senior-backend-engineer,senior-test-engineer")
    sp.set_defaults(func=cmd_export)

    sp = sub.add_parser("index", help="rebuild a skills index")
    common(sp)
    sp.add_argument("--lib"); sp.add_argument("--out")
    sp.set_defaults(func=cmd_index)

    sp = sub.add_parser("lock", help="show or refresh upstream pins")
    sp.add_argument("--refresh", action="store_true")
    sp.set_defaults(func=cmd_lock)

    sp = sub.add_parser("hosts", help="list supported hosts"); common(sp); sp.set_defaults(func=cmd_hosts)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

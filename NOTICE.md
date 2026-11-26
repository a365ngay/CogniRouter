# Third-party notice

Everything in `core/`, `skills/`, `agents/`, `installer/`, `scripts/` and `tests/` is part of Skill Compass and licensed under the MIT License (see `LICENSE`).

The skills listed in `upstream.lock.json` are **not redistributed** in this repository. The installer downloads them from their original repositories at a pinned commit, on your machine, when you run `install`. Each remains under its own license and copyright:

| Upstream | Repository | Skills |
|---|---|---|
| taste-skill | https://github.com/Leonxlnx/taste-skill | design-taste-frontend, redesign-existing-projects, minimalist-ui, industrial-brutalist-ui, stitch-design-taste, brandkit, imagegen-frontend-web, imagegen-frontend-mobile |
| typeui | https://github.com/bergside/typeui | typeui-fundamentals |
| awesome-design-skills | https://github.com/bergside/awesome-design-skills | enterprise |
| anthropics/skills | https://github.com/anthropics/skills | frontend-design |
| ui-ux-pro-max-skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | ui-ux-pro-max |
| interface-design | https://github.com/Dammyjay93/interface-design | interface-design |
| Uncodixfy | https://github.com/cyxzdev/Uncodixfy | Uncodixfy |
| Understand-Anything (opt-in) | https://github.com/Egonex-AI/Understand-Anything | understand, understand-chat, understand-diff, understand-explain, understand-onboard |

Check each upstream license before redistributing those skills yourself. Skip all of them with `--no-upstream`.

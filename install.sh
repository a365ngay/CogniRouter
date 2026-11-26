#!/usr/bin/env sh
# Skill Compass - macOS / Linux wrapper. Usage: ./install.sh [install|status|uninstall|export|hosts] [options]
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
PY="$(command -v python3 || command -v python || true)"
[ -n "$PY" ] || { echo "Python 3.8+ is required." >&2; exit 1; }
[ "$#" -eq 0 ] && set -- install
exec "$PY" "$DIR/installer/compass.py" "$@"

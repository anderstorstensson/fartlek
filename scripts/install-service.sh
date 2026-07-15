#!/usr/bin/env bash
# Install Fartlek as a systemd user service, autostarted at login.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
UNIT_SRC="$REPO_DIR/systemd/fartlek.service"
UNIT_DIR="$HOME/.config/systemd/user"

# Venv resolution mirrors the Makefile: in-repo .venv if present,
# otherwise ~/.venvs/fartlek; override with VENV=/path/to/venv.
if [ -z "${VENV:-}" ]; then
  if [ -d "$REPO_DIR/.venv" ]; then
    VENV="$REPO_DIR/.venv"
  else
    VENV="$HOME/.venvs/fartlek"
  fi
fi

if [ ! -x "$VENV/bin/uvicorn" ]; then
  echo "Error: no uvicorn found at $VENV/bin/uvicorn — set up the venv first (see README)." >&2
  exit 1
fi

# Clean up the pre-rename unit if it exists.
if systemctl --user list-unit-files runapp.service >/dev/null 2>&1 \
   && [ -f "$UNIT_DIR/runapp.service" ]; then
  systemctl --user disable --now runapp.service 2>/dev/null || true
  rm -f "$UNIT_DIR/runapp.service"
fi

mkdir -p "$UNIT_DIR"
sed -e "s|@WORKDIR@|$REPO_DIR|g" -e "s|@VENV@|$VENV|g" \
  "$UNIT_SRC" > "$UNIT_DIR/fartlek.service"
systemctl --user daemon-reload
systemctl --user enable --now fartlek.service

echo "Fartlek service installed and started."
echo "  Status:  systemctl --user status fartlek"
echo "  Logs:    journalctl --user -u fartlek -f"
echo "  Web UI:  http://127.0.0.1:8077"
echo
echo "Optional: keep it running even when not logged in:"
echo "  sudo loginctl enable-linger $USER"

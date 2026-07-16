#!/usr/bin/env bash
# Install Fartlek as a macOS launchd user agent, autostarted at login.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LABEL="com.fartlek.app"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

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

mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$VENV/bin/uvicorn</string>
    <string>backend.main:app</string>
    <string>--host</string><string>127.0.0.1</string>
    <string>--port</string><string>8077</string>
  </array>
  <key>WorkingDirectory</key><string>$REPO_DIR</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key>
  <dict><key>SuccessfulExit</key><false/></dict>
  <key>StandardOutPath</key><string>$HOME/Library/Logs/fartlek.log</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/fartlek.log</string>
  <!-- Optional overrides, e.g. nightly cloud backups:
  <key>EnvironmentVariables</key>
  <dict><key>FARTLEK_RCLONE_REMOTE</key><string>gdrive:fartlek</string></dict>
  -->
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "Installed and started $LABEL (logs: ~/Library/Logs/fartlek.log)"
echo "App: http://127.0.0.1:8077"

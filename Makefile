# Uses the in-repo .venv when present (uv sync default), otherwise
# ~/.venvs/fartlek (for repos on filesystems that can't hold symlinks,
# e.g. exFAT). Override with: make VENV=/path/to/venv <target>
VENV ?= $(if $(wildcard .venv),.venv,$(HOME)/.venvs/fartlek)
PY = $(VENV)/bin/python
NODE_BIN = node

.PHONY: help login sync backfill recompute serve dev test typecheck build-frontend install-service

help:
	@echo "Fartlek targets:"
	@echo "  make login            One-time Garmin Connect authentication"
	@echo "  make sync             Incremental sync from Garmin"
	@echo "  make backfill         Full sync of all Garmin history"
	@echo "  make recompute        Recompute load metrics (after settings change)"
	@echo "  make serve            Run the web app (http://127.0.0.1:8077)"
	@echo "  make dev              Frontend dev server with hot reload"
	@echo "  make test             Run backend test suite"
	@echo "  make typecheck        Typecheck the frontend"
	@echo "  make build-frontend   Production frontend build"
	@echo "  make install-service  Install + enable systemd user service (autostart)"

login:
	$(PY) -m backend.cli login

sync:
	$(PY) -m backend.cli sync

backfill:
	$(PY) -m backend.cli sync --full

recompute:
	$(PY) -m backend.cli recompute

rescan:
	$(PY) -m backend.cli rescan

serve:
	$(PY) -m backend.cli serve

dev:
	cd frontend && $(NODE_BIN) node_modules/vite/bin/vite.js

test:
	$(PY) -m pytest -q

typecheck:
	cd frontend && $(NODE_BIN) node_modules/typescript/bin/tsc --noEmit

build-frontend:
	cd frontend && $(NODE_BIN) node_modules/vite/bin/vite.js build

install-service:
	./scripts/install-service.sh

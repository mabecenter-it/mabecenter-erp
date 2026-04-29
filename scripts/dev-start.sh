#!/usr/bin/env bash
set -euo pipefail

BENCH_ROOT="${BENCH_ROOT:-$HOME/frappe-dev}"
BENCH_NAME="${BENCH_NAME:-mabecenter-bench}"
BENCH_DIR="${BENCH_ROOT}/${BENCH_NAME}"
SITE_NAME="${SITE_NAME:-dev.localhost}"

export PATH="$HOME/.local/bin:$PATH"

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This script is intended for WSL/Linux." >&2
  exit 1
fi

if ! command -v bench >/dev/null 2>&1; then
  echo "bench was not found. Run scripts/dev-prereqs.sh first, then retry." >&2
  echo 'If bench was just installed, run: source ~/.bashrc && export PATH="$HOME/.local/bin:$PATH"' >&2
  exit 1
fi

if [[ ! -d "$BENCH_DIR" ]]; then
  echo "Bench not found at $BENCH_DIR. Run scripts/dev-up.sh first." >&2
  exit 1
fi

if command -v sudo >/dev/null 2>&1; then
  sudo service mariadb start || true
  sudo service redis-server start || true
fi

cd "$BENCH_DIR"
bench use "$SITE_NAME" >/dev/null 2>&1 || true
exec bench start

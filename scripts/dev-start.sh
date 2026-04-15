#!/usr/bin/env bash
set -euo pipefail

BENCH_ROOT="${BENCH_ROOT:-$HOME/frappe-dev}"
BENCH_NAME="${BENCH_NAME:-mabecenter-bench}"
BENCH_DIR="${BENCH_ROOT}/${BENCH_NAME}"
SITE_NAME="${SITE_NAME:-dev.localhost}"

if [[ ! -d "$BENCH_DIR" ]]; then
  echo "Bench not found at $BENCH_DIR. Run scripts/dev-up.sh first." >&2
  exit 1
fi

cd "$BENCH_DIR"
bench use "$SITE_NAME" >/dev/null 2>&1 || true
exec bench start

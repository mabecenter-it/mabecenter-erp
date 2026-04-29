#!/usr/bin/env bash
set -euo pipefail

BENCH_ROOT="${BENCH_ROOT:-$HOME/frappe-dev}"
BENCH_NAME="${BENCH_NAME:-mabecenter-bench}"
BENCH_DIR="${BENCH_ROOT}/${BENCH_NAME}"
SITE_NAME="${SITE_NAME:-dev.localhost}"

export PATH="$HOME/.local/bin:$PATH"

print_command() {
  local command_name="$1"

  if command -v "$command_name" >/dev/null 2>&1; then
    printf 'OK   %-14s %s\n' "$command_name" "$(command -v "$command_name")"
  else
    printf 'MISS %-14s not found\n' "$command_name"
  fi
}

print_version() {
  local label="$1"
  shift

  printf '%-16s ' "$label"
  "$@" 2>/dev/null || echo "not available"
}

echo "Mabecenter ERP development doctor"
echo
echo "System"
echo "  OS:      $(uname -a)"
echo "  Shell:   ${SHELL:-unknown}"
echo "  PATH:    $PATH"
echo
echo "Commands"
print_command sudo
print_command apt-get
print_command git
print_command python3.11
print_command python3.10
print_command python3
print_command pipx
print_command bench
print_command mysql
print_command redis-server
print_command node
print_command yarn
echo
echo "Versions"
print_version "python3" python3 --version
print_version "bench" bench --version
print_version "node" node --version
print_version "yarn" yarn --version
echo
echo "Bench"
echo "  Expected bench directory: $BENCH_DIR"
echo "  Expected site:            $SITE_NAME"
if [[ -d "$BENCH_DIR" ]]; then
  echo "  Bench directory exists:   yes"
else
  echo "  Bench directory exists:   no"
fi
echo
echo "Next step"
echo "  If anything says MISS, run: ./scripts/dev-prereqs.sh"
echo "  If prereqs are OK, run:    ./scripts/dev-up.sh"

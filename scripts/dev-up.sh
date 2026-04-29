#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PREREQS_SCRIPT="${SCRIPT_DIR}/dev-prereqs.sh"

BENCH_ROOT="${BENCH_ROOT:-$HOME/frappe-dev}"
BENCH_NAME="${BENCH_NAME:-mabecenter-bench}"
BENCH_DIR="${BENCH_ROOT}/${BENCH_NAME}"
SITE_NAME="${SITE_NAME:-dev.localhost}"
FRAPPE_BRANCH="${FRAPPE_BRANCH:-version-15}"
PYTHON_BIN="${PYTHON_BIN:-}"
MARIADB_ROOT_PASSWORD="${MARIADB_ROOT_PASSWORD:-root}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-Admin1234.}"

export PATH="$HOME/.local/bin:$PATH"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

have_command() {
  command -v "$1" >/dev/null 2>&1
}

choose_python() {
  if [[ -n "$PYTHON_BIN" ]]; then
    command -v "$PYTHON_BIN" >/dev/null 2>&1 && {
      echo "$PYTHON_BIN"
      return 0
    }
    return 1
  fi

  for candidate in python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      echo "$candidate"
      return 0
    fi
  done

  return 1
}

app_installed() {
  bench --site "$SITE_NAME" list-apps 2>/dev/null | awk '{print $1}' | grep -qx "$1"
}

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This script is intended for WSL/Linux." >&2
  exit 1
fi

require_command git

if ! choose_python >/dev/null || ! have_command bench || ! have_command mysql || ! have_command redis-server || ! have_command node || ! have_command yarn; then
  if [[ -f "$PREREQS_SCRIPT" ]]; then
    echo "Installing missing development prerequisites"
    bash "$PREREQS_SCRIPT"
    export PATH="$HOME/.local/bin:$PATH"
  else
    echo "Missing prerequisites and ${PREREQS_SCRIPT} was not found." >&2
    exit 1
  fi
fi

PYTHON_BIN="$(choose_python || true)"

require_command bench
require_command "$PYTHON_BIN"
require_command mysql
require_command redis-server
require_command node
require_command yarn

if command -v sudo >/dev/null 2>&1; then
  sudo service mariadb start || true
  sudo service redis-server start || true
fi

echo "Using Python: $PYTHON_BIN ($(command -v "$PYTHON_BIN"))"
echo "Using Bench:  $(command -v bench)"

git config --global --add safe.directory "$REPO_DIR" || true
git config --global --add safe.directory "$REPO_DIR/.git" || true

mkdir -p "$BENCH_ROOT"

if [[ ! -d "$BENCH_DIR" ]]; then
  echo "Creating bench at $BENCH_DIR"
  (
    cd "$BENCH_ROOT"
    bench init "$BENCH_NAME" --frappe-branch "$FRAPPE_BRANCH" --python "$PYTHON_BIN"
  )
fi

cd "$BENCH_DIR"

if [[ ! -d "sites/$SITE_NAME" ]]; then
  echo "Creating site $SITE_NAME"
  bench new-site "$SITE_NAME" \
    --mariadb-root-password "$MARIADB_ROOT_PASSWORD" \
    --admin-password "$ADMIN_PASSWORD"
fi

if [[ ! -d "apps/erpnext" ]]; then
  echo "Fetching ERPNext"
  bench get-app --branch "$FRAPPE_BRANCH" erpnext
fi

if ! app_installed "erpnext"; then
  echo "Installing ERPNext on $SITE_NAME"
  bench --site "$SITE_NAME" install-app erpnext
fi

if [[ ! -d "apps/mabecenter" ]]; then
  echo "Fetching mabecenter from local repo"
  bench get-app mabecenter "$REPO_DIR"
fi

if ! app_installed "mabecenter"; then
  echo "Installing mabecenter on $SITE_NAME"
  bench --site "$SITE_NAME" install-app mabecenter
fi

echo "Running migrations"
bench --site "$SITE_NAME" migrate
bench --site "$SITE_NAME" clear-cache

cat <<EOF

Development environment is ready.

Bench: $BENCH_DIR
Site:  $SITE_NAME

Next:
  1. Add '127.0.0.1 $SITE_NAME' to your Windows hosts file if needed.
  2. Start the stack with:
     $REPO_DIR/scripts/dev-start.sh
  3. Open:
     http://$SITE_NAME:8000/app

Default Administrator password for dev: $ADMIN_PASSWORD
Override it by exporting ADMIN_PASSWORD before running this script.
EOF

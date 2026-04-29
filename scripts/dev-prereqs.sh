#!/usr/bin/env bash
set -euo pipefail

log() {
  printf '\n==> %s\n' "$1"
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command after install: $1" >&2
    exit 1
  fi
}

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This script is intended for WSL/Linux." >&2
  exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This script currently supports Ubuntu/Debian systems with apt-get." >&2
  exit 1
fi

if ! command -v sudo >/dev/null 2>&1; then
  echo "sudo is required to install system packages." >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
export PATH="$HOME/.local/bin:$PATH"

log "Installing system packages"
sudo apt-get update
sudo apt-get install -y \
  build-essential \
  curl \
  git \
  libmysqlclient-dev \
  mariadb-server \
  pkg-config \
  python3 \
  python3-dev \
  python3-pip \
  python3-venv \
  redis-server \
  pipx

if ! command -v node >/dev/null 2>&1; then
  log "Installing Node.js 18"
  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
  sudo apt-get install -y nodejs
  sudo apt-get install -y npm
fi

if ! command -v yarn >/dev/null 2>&1; then
  log "Installing Yarn"
  sudo npm install -g yarn
fi


if ! command -v pip3 >/dev/null 2>&1; then
  sudo apt-get install -y python3-pip
fi

python3.11 -m pip install --user --upgrade pip --break-system-packages
python3.11 -m pip install --user frappe-bench --break-system-packages



mkdir -p "$HOME/.local/bin"

if ! grep -Fq 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

log "Installing Frappe Bench CLI"
if command -v bench >/dev/null 2>&1; then
  echo "bench is already installed at $(command -v bench)"
else
  pipx install frappe-bench
fi

log "Starting local services"
sudo service mariadb start || true
sudo service redis-server start || true

require_command git
require_command mysql
require_command redis-server
require_command node
require_command yarn
require_command bench

echo
echo "Development prerequisites installed."
echo "bench: $(command -v bench)"
echo "node:  $(node --version)"
echo "yarn:  $(yarn --version)"
echo
echo "If this is a new shell later, run:"
echo '  source ~/.bashrc'
echo '  export PATH="$HOME/.local/bin:$PATH"'

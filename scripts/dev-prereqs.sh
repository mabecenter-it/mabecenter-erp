#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This script is intended for WSL/Linux." >&2
  exit 1
fi

if ! command -v sudo >/dev/null 2>&1; then
  echo "sudo is required to install system packages." >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

sudo apt-get update
sudo apt-get install -y curl git redis-server mariadb-server pkg-config libmysqlclient-dev

if ! command -v python3.11 >/dev/null 2>&1; then
  sudo apt-get install -y python3.11 python3.11-venv python3.11-dev
fi

if ! command -v node >/dev/null 2>&1; then
  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi

if ! command -v yarn >/dev/null 2>&1; then
  sudo npm install -g yarn
fi

if ! command -v pip3 >/dev/null 2>&1; then
  sudo apt-get install -y python3-pip
fi

python3.11 -m pip install --user --upgrade pip
python3.11 -m pip install --user frappe-bench

mkdir -p "$HOME/.local/bin"

if ! grep -Fq 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

export PATH="$HOME/.local/bin:$PATH"

sudo service mariadb start || true
sudo service redis-server start || true

echo
echo "Development prerequisites installed."
echo "If this is a new shell later, run: source ~/.bashrc"

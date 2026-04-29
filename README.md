# Mabecenter ERP App

Custom Frappe app that extends ERPNext with Mabecenter-specific customizations and a VTiger sync flow.

## Dev Setup

This repo is a Frappe app, not a full bench. For local development in WSL/Linux, use the scripts in `scripts/`.

### Quick Start

If your machine already has the required system dependencies installed, the shortest path is:

```bash
git clone https://github.com/mabecenter-it/mabecenter-erp.git
cd mabecenter-erp
chmod +x scripts/dev-up.sh scripts/dev-start.sh
./scripts/dev-up.sh
./scripts/dev-start.sh
```

If the machine is fresh, `scripts/dev-up.sh` will first call `scripts/dev-prereqs.sh` to install the required WSL packages and the `bench` CLI.

Then open:

```text
http://dev.localhost:8000/app
```

Default login:

- user: `Administrator`
- password: `Admin1234.`

Change the password after first login if you are sharing the environment.

### Prerequisites

- WSL/Linux
- `sudo` access (the scripts use `sudo` non‑interactive; provide your sudo password in the scripts or modify them to prompt for it)

Installed automatically by `scripts/dev-prereqs.sh`:

- `bench`
- `python3.11`
- MariaDB
- Redis
- Node.js 18
- Yarn

### One-command bootstrap

From the repo root inside WSL:

```bash
./scripts/dev-up.sh
```

This script will:

- install missing WSL development prerequisites if needed
- create a bench if needed
- create a site if needed
- install `erpnext`
- install this app as `mabecenter`
- run migrations

Defaults:

- bench: `~/frappe-dev/mabecenter-bench`
- site: `dev.localhost`
- admin password: `Admin1234.`
- MariaDB root password: `root`

You can override them:

```bash
BENCH_NAME=lab-bench SITE_NAME=lab.localhost ADMIN_PASSWORD=MyStrongPass. ./scripts/dev-up.sh
```

Optional overrides:

- `BENCH_ROOT`: where the bench folder will be created
- `BENCH_NAME`: bench name
- `SITE_NAME`: Frappe site name
- `FRAPPE_BRANCH`: Frappe and ERPNext branch, defaults to `version-15`
- `PYTHON_BIN`: Python binary, defaults to `python3.11`
- `MARIADB_ROOT_PASSWORD`: MariaDB root password
- `ADMIN_PASSWORD`: Administrator password for the site

### Install Only Prerequisites

If you want to prepare the machine first and bootstrap later:

```bash
./scripts/dev-prereqs.sh
```

### Start the stack

```bash
./scripts/dev-start.sh
```

If Windows cannot resolve the hostname, add this to `C:\Windows\System32\drivers\etc\hosts`:

```text
127.0.0.1 dev.localhost
```

## What This App Adds

- VTiger sync DocTypes and logic
- customizations for `Customer`, `Contact`, `Sales Order`, `Packed Item`, and `Address`
- Mabecenter-specific supporting DocTypes such as `bank_card`, `broker_item`, and `company_item`

## License

mit

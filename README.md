# Mabecenter ERP App

Custom Frappe app that extends ERPNext with Mabecenter-specific customizations and a VTiger sync flow.

## Dev Setup

This repo is a Frappe app, not a full bench. You do not run it directly from this
folder like a normal Python or Node project. For local development, create a
Frappe bench in WSL/Linux and install this app into that bench.

The scripts in `scripts/` automate that setup for Ubuntu/WSL.

### Quick Start

From a fresh Windows machine:

1. Install WSL with Ubuntu.
2. Open the Ubuntu/WSL terminal.
3. Clone and bootstrap the project:

```bash
git clone https://github.com/mabecenter-it/mabecenter-erp.git
cd mabecenter-erp
chmod +x scripts/*.sh
./scripts/dev-doctor.sh
./scripts/dev-up.sh
./scripts/dev-start.sh
```

If the machine is fresh, `scripts/dev-up.sh` will first call
`scripts/dev-prereqs.sh` to install the required WSL packages and the `bench`
CLI.

Then open:

```text
http://dev.localhost:8000/app
```

Default login:

- user: `Administrator`
- password: `Admin1234.`

Change the password after first login if you are sharing the environment.

### Prerequisites

- Windows with WSL/Ubuntu, or native Linux
- `sudo` access in WSL/Linux
- internet access to download Frappe, ERPNext, Node packages, and Python packages
- ports `8000`, `9000`, `6787`, and the usual Redis/MariaDB ports available

Installed automatically by `scripts/dev-prereqs.sh`:

- `bench`
- Python 3
- `pipx`
- MariaDB
- Redis
- Node.js 18
- Yarn

The scripts are written for Linux. Run them inside WSL/Ubuntu, not PowerShell or
CMD.

### One-command bootstrap

From the repo root inside WSL:

```bash
chmod +x scripts/*.sh
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
- `PYTHON_BIN`: Python binary, defaults to the first available `python3.11`, `python3.10`, or `python3`
- `MARIADB_ROOT_PASSWORD`: MariaDB root password
- `ADMIN_PASSWORD`: Administrator password for the site

### Start After Setup

After `dev-up.sh` has completed once, start the dev server with:

```bash
./scripts/dev-start.sh
```

Open:

```text
http://dev.localhost:8000/app
```

If Windows cannot resolve the hostname, add this line to
`C:\Windows\System32\drivers\etc\hosts` as Administrator:

```text
127.0.0.1 dev.localhost
```

If port `8000` is already busy, Frappe may fail to start. Stop the process using
that port or change the bench/web port in your local bench configuration.

### Install Only Prerequisites

If you want to prepare the machine first and bootstrap later:

```bash
chmod +x scripts/*.sh
./scripts/dev-prereqs.sh
```

### Diagnose a Machine

If setup fails on another machine, run:

```bash
./scripts/dev-doctor.sh
```

This prints the detected system, required commands, versions, and expected bench
folder. Share that output when debugging setup problems.

### Start the stack

```bash
./scripts/dev-start.sh
```

### Dashboard Assets

The Angular dashboard is in `dashboard/`. The Frappe app build uses:

```bash
yarn install
yarn build
```

The root `yarn build` command builds the Angular dashboard and copies the built
files into the Frappe app under `mabecenter/public/dashboard` and
`mabecenter/www/dashboard.html`.

### Common Problems

`This script is intended for WSL/Linux.`

You are running the setup from PowerShell/CMD instead of WSL/Ubuntu.

`bench: command not found`

Open a new WSL terminal or run:

```bash
source ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
```

`dev.localhost` does not open from Windows.

Add this line to the Windows hosts file:

```text
127.0.0.1 dev.localhost
```

MariaDB password errors during `bench new-site`.

The scripts assume the MariaDB root password is `root` by default. If your local
MariaDB uses a different password, run:

```bash
MARIADB_ROOT_PASSWORD=your-password ./scripts/dev-up.sh
```

## What This App Adds

- VTiger sync DocTypes and logic
- customizations for `Customer`, `Contact`, `Sales Order`, `Packed Item`, and `Address`
- Mabecenter-specific supporting DocTypes such as `bank_card`, `broker_item`, and `company_item`

## License

mit

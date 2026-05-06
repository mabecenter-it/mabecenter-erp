# Mabecenter ERP

Mabecenter ERP is a custom Frappe/ERPNext app for Mabecenter-specific insurance brokerage workflows, including ERPNext customizations and VTiger sync logic.

This project targets **Frappe/ERPNext v16**.

## 1. Idea Principal

This repo is a Frappe app, not a full bench and not a standalone Node/Python app. You do not run it directly from the repo folder.

Keep these three concepts separate:

```text
Repo Git = code shared with the team
Bench    = local Frappe runtime
Site     = database/configuration where changes are tested
```

Recommended local structure:

```text
~/mabecenter-workspace/
  repo/
    mabecenter-erp/     -> real Git repo
  bench-v16/            -> Frappe/ERPNext v16 bench
```

## 2. Requirements

Use WSL/Ubuntu or Linux. Run the commands inside WSL, not PowerShell/CMD.

For Frappe/ERPNext v16, use:

```text
Python 3.14
Node.js 24
Yarn 1.22+
MariaDB 11.8
Redis 6+
bench 5+
```

Check your versions:

```bash
python --version
node --version
yarn --version
mysql --version
redis-server --version
bench --version
```

If you use `uv` for Python/bench:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv python install 3.14 --default
uv tool install frappe-bench --force
```

If you use `nvm` for Node:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
npm install -g yarn
```

## 3. Crear Workspace Limpio

```bash
cd ~
mkdir -p ~/mabecenter-workspace
cd ~/mabecenter-workspace
```

Create the repo folder:

```bash
mkdir -p repo
cd repo
```

Clone the project:

```bash
git clone https://github.com/mabecenter-it/mabecenter-erp.git
cd mabecenter-erp
git checkout develop
```

The real repo is:

```text
~/mabecenter-workspace/repo/mabecenter-erp
```

Open this folder in VS Code:

```bash
code ~/mabecenter-workspace/repo/mabecenter-erp
```

## 4. Crear Bench v16

Return to the workspace:

```bash
cd ~/mabecenter-workspace
```

Create the v16 bench:

```bash
bench init bench-v16 --frappe-branch version-16
cd ~/mabecenter-workspace/bench-v16
```

Install ERPNext v16:

```bash
bench get-app erpnext --branch version-16
```

Install Mabecenter as a soft link to the real Git repo:

```bash
bench get-app --soft-link ~/mabecenter-workspace/repo/mabecenter-erp
```

Verify that the bench uses the real repo:

```bash
readlink -f apps/mabecenter
readlink -f ~/mabecenter-workspace/repo/mabecenter-erp
```

Both commands should print:

```text
~/mabecenter-workspace/repo/mabecenter-erp
```

That means the bench is not using a second copy of the app.

## 5. Crear Site

Create the local site:

```bash
bench new-site mabe16.localhost --mariadb-root-password root --admin-password Admin1234.
```

If your MariaDB root password is not `root`, use the correct password.

Install the apps:

```bash
bench --site mabe16.localhost install-app erpnext
bench --site mabe16.localhost install-app mabecenter
bench --site mabe16.localhost migrate
bench use mabe16.localhost
```

If `install-app erpnext` fails with a Redis queue connection error, start the bench in another terminal:

```bash
cd ~/mabecenter-workspace/bench-v16
bench start
```

Then repeat the failed install command.

## 6. Arrancar el Proyecto

From the v16 bench:

```bash
cd ~/mabecenter-workspace/bench-v16
bench start
```

Open:

```text
http://mabe16.localhost:8001/app
```

If your bench uses port `8000`, open:

```text
http://mabe16.localhost:8000/app
```

Login:

```text
User: Administrator
Password: Admin1234.
```

If Windows does not resolve `mabe16.localhost`, add this line to `C:\Windows\System32\drivers\etc\hosts` as Administrator:

```text
127.0.0.1 mabe16.localhost
```

## 7. Flujo Diario de Trabajo

Terminal for running Frappe:

```bash
cd ~/mabecenter-workspace/bench-v16
bench start
```

Terminal for coding:

```bash
cd ~/mabecenter-workspace/repo/mabecenter-erp
code .
```

Rule:

```text
Code in repo/
Run from bench-v16/
Test in mabe16.localhost
```

## 8. Customizaciones Desde la UI

If you customize an ERPNext form from the Frappe UI, for example:

```text
Customize Form > Sales Order
```

changes such as these are saved first in the site database, not in Git:

- adding a field
- changing a label
- hiding a field
- making a field required
- moving fields
- changing field properties

The local site database is:

```text
mabe16.localhost
```

To move UI customizations into Git, export fixtures.

## 9. Configurar Fixtures en hooks.py

File:

```text
~/mabecenter-workspace/repo/mabecenter-erp/mabecenter/hooks.py
```

Use filtered fixtures:

```python
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["dt", "in", [
                "Sales Order",
                "Customer",
                "Contact",
                "Address",
                "Packed Item",
            ]]
        ],
    },
    {
        "dt": "Property Setter",
        "filters": [
            ["doc_type", "in", [
                "Sales Order",
                "Customer",
                "Contact",
                "Address",
                "Packed Item",
            ]]
        ],
    },
    "Client Script",
    "Server Script",
]
```

This belongs in Git. It tells Frappe to export:

- Custom Fields for the selected DocTypes
- Property Setters for the selected DocTypes
- Client Scripts
- Server Scripts

## 10. Exportar Cambios de la UI al Repo

After customizing from the UI:

```bash
cd ~/mabecenter-workspace/bench-v16
bench --site mabe16.localhost export-fixtures
```

This creates or updates files like:

```text
~/mabecenter-workspace/repo/mabecenter-erp/mabecenter/fixtures/custom_field.json
~/mabecenter-workspace/repo/mabecenter-erp/mabecenter/fixtures/property_setter.json
```

Review before committing:

```bash
cd ~/mabecenter-workspace/repo/mabecenter-erp
git status
git diff -- mabecenter/hooks.py mabecenter/fixtures
```

If the diff is correct:

```bash
git add mabecenter/hooks.py mabecenter/fixtures
git commit -m "Export ERPNext customizations"
git push
```

## 11. Si Te Arrepientes de un Cambio en la UI

Clean both places:

```text
1. Database/UI
2. Repo/fixtures
```

First revert the change in Frappe:

```text
Customize Form > Sales Order
```

Then export fixtures again:

```bash
cd ~/mabecenter-workspace/bench-v16
bench --site mabe16.localhost export-fixtures
```

Review Git:

```bash
cd ~/mabecenter-workspace/repo/mabecenter-erp
git status
git diff
```

If you do not want to keep any pending fixture change:

```bash
git restore mabecenter/hooks.py
git restore mabecenter/fixtures/custom_field.json mabecenter/fixtures/property_setter.json
```

If the fixture files are new/untracked:

```bash
rm mabecenter/fixtures/custom_field.json mabecenter/fixtures/property_setter.json
```

Important rule:

```text
git restore does not revert the UI/database.
The UI is reverted from Frappe.
Git is reverted from Git.
```

## 12. Cuando un Compañero Sube Cambios

Pull the repo:

```bash
cd ~/mabecenter-workspace/repo/mabecenter-erp
git pull
```

Apply changes to the local site:

```bash
cd ~/mabecenter-workspace/bench-v16
bench --site mabe16.localhost migrate
bench --site mabe16.localhost clear-cache
```

If frontend/assets changed:

```bash
bench build --app mabecenter
```

If running with `bench start`, stop it with `Ctrl + C` and start it again:

```bash
bench start
```

## 13. Trabajo en Equipo con Fixtures

Fixture files are regenerated completely. Two developers can work on the same DocType, but it requires discipline.

Before customizing from UI:

```bash
cd ~/mabecenter-workspace/repo/mabecenter-erp
git pull
cd ~/mabecenter-workspace/bench-v16
bench --site mabe16.localhost migrate
```

Then customize, export, and review:

```bash
bench --site mabe16.localhost export-fixtures
cd ~/mabecenter-workspace/repo/mabecenter-erp
git diff -- mabecenter/fixtures
```

Do not commit if your diff removes fields or property setters you did not touch.

Best practice:

```text
One developer per heavily customized DocType at a time.
Always pull + migrate before UI customization.
Always review fixture diff before commit.
```

## 14. Qué No Debemos Hacer

Do not modify ERPNext directly:

```text
~/mabecenter-workspace/bench-v16/apps/erpnext
```

ERPNext is an external dependency. Extend it from `mabecenter` using:

```text
Custom Fields
Property Setters
Client Scripts
Server Scripts
hooks.py
fixtures
patches
overrides
```

Senior rule:

```text
ERPNext is extended.
ERPNext is not edited directly unless there is an exceptional reason.
```

## 15. Flujo Mental Completo

When customizing from UI:

```text
Frappe UI
-> site database
-> bench export-fixtures
-> JSON in mabecenter repo
-> git commit/push
-> teammate git pull
-> bench migrate
-> change appears in teammate site
```

When changing code:

```text
Edit mabecenter-erp repo
-> git commit/push
-> teammate git pull
-> bench migrate/build/clear-cache
```

## 16. Resumen Final

```text
Git/repo
= shared team truth
= where commits are made
= ~/mabecenter-workspace/repo/mabecenter-erp
```

```text
Bench
= Frappe runtime
= contains apps, sites, env, config and logs
= ~/mabecenter-workspace/bench-v16
```

```text
Site
= local database/configuration
= where the UI saves changes first
= mabe16.localhost
```

```text
Fixtures
= bridge between DB and Git
= convert UI customizations into versioned JSON
```

Core lesson:

```text
Frappe UI does not write to Git.
Frappe UI writes to the database.
export-fixtures moves DB -> repo.
migrate moves repo -> DB.
```

## 17. Dashboard Assets

The Angular dashboard is in `dashboard/`. The Frappe app build uses:

```bash
yarn install
yarn build
```

The root `yarn build` command builds the Angular dashboard and copies the built files into:

```text
mabecenter/public/dashboard
mabecenter/www/dashboard.html
```

## 18. What This App Adds

- VTiger sync DocTypes and logic
- customizations for `Customer`, `Contact`, `Sales Order`, `Packed Item`, and `Address`
- supporting DocTypes such as `Bank Card`, `Broker Item`, `Company Item`, `Dependent Item`, and `Document Item`

## License

mit

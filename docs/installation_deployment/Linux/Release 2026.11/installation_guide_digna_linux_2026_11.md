---
title: Linux Installation Guide – digna Release 2026.11 | digna Documentation
description: Step-by-step guide to installing digna Release 2026.11 on Linux — system requirements, PostgreSQL setup, nginx or Apache configuration, backend and dashboard configuration, running digna as a systemd service, and upgrading from Release 2026.06.
keywords: digna linux installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql linux, nginx linux, digna systemd service, digna upgrade guide
image: /assets/logo_square.png
---

# Linux Installation Guide for digna Release 2026.11

**Release:** 2026.11

**Last Updated:** November 7, 2026


---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Setup](#pre-installation-setup)
4. [PostgreSQL Server Setup](#postgresql-server-setup)
5. [Web Server Configuration](#web-server-configuration)
6. [Initial Installation](#initial-installation)
7. [Backend Configuration](#backend-configuration)
8. [Dashboard Configuration](#dashboard-configuration)
9. [Running digna as a systemd Service](#running-digna-as-a-systemd-service)
10. [Upgrading to a New Release](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### About digna

digna is a comprehensive AI-driven platform designed to optimize data quality management across various data environments such as warehouses, lakes, and lakehouses. Built to be highly scalable and adaptable, digna addresses modern data challenges through automation, real-time monitoring, and anomaly detection.

digna consists of two main components:

- **digna**: The core engine of the application, responsible for processing data and performing quality checks. It combines the backend and the command line interface in a single executable, replacing the separate `dignabackend` and `dignacli` of earlier releases.
- **dignadashboard**: A web-based interface hosted on a web server, providing a user-friendly way to interact with the digna platform and visualize data quality metrics.

### What's New in Release 2026.11

This release adds digna Data Reconciliation, digna Agentic with the digna MCP Server, and the digna Engine, which can profile data inside digna and check referential integrity between different database technologies. See the [release notes](../../../changelog/Release_202611.md) for complete details.

For an installation, the release brings a new repository migration mechanism, an optional `[duckdb]` section in `config.toml` for the digna Engine, and a new license file. The [upgrade section](#upgrading-to-a-new-release) covers each of them.

### Looking for Windows or macOS?

This guide covers Linux. For other platforms, see the [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) or the [macOS Installation Guide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Which Distribution Does This Guide Cover?

The instructions are written for the two most common server families. Where the two differ, both commands are given:

- **Debian family** — Debian, Ubuntu. Package manager: `apt`.
- **RHEL family** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Package manager: `dnf`.

Any modern distribution with `systemd` will work; only the package names and a few configuration paths change.

---

## System Requirements {: #system-requirements }

Before you begin the installation, ensure that your system meets the following minimum requirements:

| Requirement | Specification |
|---|---|
| **Operating System** | Ubuntu 22.04 LTS or later, Debian 12 or later, RHEL 9 / Rocky 9 / AlmaLinux 9 or later |
| **Architecture** | x86_64 (amd64) or arm64 |
| **Init System** | systemd |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB available storage |
| **Database** | PostgreSQL Server 12 or higher |
| **Web Server** | nginx, Apache httpd, or equivalent |

!!! info "digna Engine"

    Database connections that use the digna Engine as their profiling location are profiled on the
    digna host itself. Plan additional memory and disk space for them, see the
    [\[duckdb\] section](#duckdb-section).

### Database Installation Options

**If PostgreSQL is already installed:**
You can add a new database for digna to your existing PostgreSQL Server.

**If installing PostgreSQL on the same machine as digna:**

!!! info "Recommended Specifications"

    - **Memory**: 32 GB RAM (instead of 16 GB)
    - **Disk Space**: 50 GB available storage (instead of 10 GB)

    These higher specifications accommodate both digna and the PostgreSQL database running simultaneously.

### Checking Your Distribution and Architecture

Several commands in this guide differ between the Debian and RHEL families. To check which you are on, run:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` or `ID=debian` — use the `apt` commands.
- `ID=rhel`, `rocky`, `almalinux` or `fedora` — use the `dnf` commands.
- `x86_64` or `aarch64` — the architecture of the installation package you need.

---

## Pre-Installation Setup {: #pre-installation-setup }

Before installing digna, ensure that two key prerequisites are in place:

1. **PostgreSQL Server** – for storing calculated metrics and performance data
2. **Web Server** – for hosting the digna Dashboard

If these components are not already set up, follow the sections below to install and configure them.

### Refreshing the Package Index

Update your package lists before installing anything:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Note"

    Throughout this guide, the first command in a pair is for the **Debian family** and the second for the **RHEL family**. Run only the one that matches your system.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### If You Already Have PostgreSQL

If PostgreSQL is already installed and running on your local machine or if you are using a managed remote PostgreSQL server, you can skip to the [next section](#web-server-configuration).

### Installing PostgreSQL

#### Step 1: Install the Server Package

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Tip"

    Distribution packages may lag behind the current PostgreSQL release. If you need a specific newer version, use the official [PostgreSQL apt or yum repository](https://www.postgresql.org/download/linux/) instead.

#### Step 2: Initialize the Database Cluster

On the **Debian family**, the package creates and starts a cluster automatically — skip to the next step.

On the **RHEL family**, the cluster must be created explicitly:

```bash
sudo postgresql-setup --initdb
```

#### Step 3: Start and Enable the Service

```bash
sudo systemctl enable --now postgresql
```

This starts PostgreSQL immediately and configures it to start again automatically at boot.

#### Step 4: Verify the Installation

```bash
psql --version
sudo systemctl status postgresql
```

You should see the PostgreSQL version and an `active (running)` service.

#### Step 5: Connect to the Server

A Linux PostgreSQL package creates a `postgres` system account that owns the cluster. Connect through it:

```bash
sudo -u postgres psql
```

!!! note "Note — Linux Differs From Windows Here"

    The Windows installer prompts you to set a password for the `postgres` superuser during setup. Linux packages do not. Instead, local connections are authenticated by **peer authentication**: the `postgres` operating-system user is allowed to connect as the `postgres` database user without a password.

    This is why the command above uses `sudo -u postgres`. The digna backend connects over TCP with a username and password, so you will create an explicit digna user in [Initial Installation](#initial-installation).

#### Step 6: Confirm the Port

The default PostgreSQL port is `5432`. To confirm the port your server is listening on:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Note the value — you will need it when configuring the digna backend.

#### Step 7: Enable Password Authentication for the digna User

digna connects to PostgreSQL over TCP as `digna_user`, which requires password authentication rather than peer authentication. Check that your `pg_hba.conf` permits it.

Locate the file:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Open it in an editor and confirm that the local TCP lines use `scram-sha-256` (or `md5` on older servers) rather than `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Reload PostgreSQL after any change:

```bash
sudo systemctl reload postgresql
```

!!! warning "Important"

    If digna reports `FATAL: Ident authentication failed for user "digna_user"`, this setting is the cause.

#### Step 8: If PostgreSQL Runs on Another Machine

To accept connections from a different host, set `listen_addresses` in `postgresql.conf` and add a matching `host` line for your network in `pg_hba.conf`:

```
listen_addresses = '*'
```

Then open the port in the firewall and restart the service:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Web Server Configuration {: #web-server-configuration }

digna requires a web server to host the dashboard. Choose one of the following options:

- [nginx](#nginx-setup) — lightweight and recommended
- [Apache httpd](#apache-setup) — widely deployed alternative

You only need to install and configure **one** of these servers.

Both sections configure two things the dashboard depends on:

- **A single-page-application fallback**, so that refreshing a dashboard URL does not return a 404
- **A `.md` MIME type**, so that Markdown files are served correctly

### nginx Setup {: #nginx-setup }

#### Overview

nginx is a lightweight, high-performance web server well suited to serving the static digna dashboard.

#### Installation

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Starting nginx

```bash
sudo systemctl enable --now nginx
```

#### Verify the Installation

1. Open your browser
2. Navigate to `http://localhost`
3. You should see the nginx welcome page

#### Opening the Firewall

If the server is reached from other machines, allow HTTP traffic:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Configuring a Site for the Dashboard

nginx includes every file in its `conf.d` directory on both distribution families. Create a dedicated configuration file for digna there:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Paste the following, replacing `/opt/digna/dashboard` with the actual path to your extracted `dashboard` folder:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Important"

    Without the `try_files` directive, reloading any dashboard page other than the root URL returns a 404. This is the nginx equivalent of the URL Rewrite module required by IIS on Windows.

#### Disable the Default Site

Only one server block may be the `default_server` for a port. On the **Debian family**, remove the packaged default so it does not conflict:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

On the **RHEL family**, comment out or delete the `server { ... }` block inside `/etc/nginx/nginx.conf`.

#### Apply the Configuration

Test the configuration for syntax errors, then reload nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd Setup {: #apache-setup }

#### Overview

Apache httpd is available in the default repositories of every supported distribution. The package is named `apache2` on the Debian family and `httpd` on the RHEL family.

#### Installation

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Starting Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Verify the Installation

1. Open your browser
2. Navigate to `http://localhost`
3. You should see the distribution's default Apache page

#### Required: Enable mod_rewrite

The dashboard requires URL rewriting.

On the **Debian family**, enable the module and restart:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

On the **RHEL family**, `mod_rewrite` is loaded by default. Confirm it:

```bash
httpd -M | grep rewrite
```

#### Required: Allow .htaccess Overrides

Open the configuration file for your document root:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Locate the `<Directory>` block covering your document root (`/var/www/html` on both families) and change:

```apache
AllowOverride None
```

to:

```apache
AllowOverride All
```

#### Required: MIME Type for Markdown Files

In the same file, add the following line so that Markdown files are served correctly:

```apache
AddType text/markdown .md
```

!!! warning "Important"

    Without this setting, `.md` files may not be served properly.

#### Apply the Configuration

Check the configuration for syntax errors, then restart Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Initial Installation {: #initial-installation }

### Step 1: Set Up the digna Repository

The digna repository stores all metrics calculated by digna. It acts as the central database for analytical and performance data.

#### Create Repository Schema and User

Open your PostgreSQL client (psql, pgAdmin, or similar) and execute the following SQL commands:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Replace the following placeholders:**

- `<digna_repo_schema>` — Your desired schema name (e.g., `dignarepo`)
- `<digna_repo_user>` — Your desired username (e.g., `digna_user`)
- `<digna_repo_password>` — A secure password for this user

**Example:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

To run these from the shell in a single step:

```bash
sudo -u postgres psql
```

Then paste the statements at the `postgres=#` prompt and type `\q` to exit.

!!! tip "Best Practice"

    Use strong, complex passwords for database users. Avoid easily guessable credentials.

---

### Step 2: Extract the digna Installation Package

1. Locate the digna installation ZIP file provided to you
2. Extract it to your desired installation location — for example `/opt/digna`
3. After extraction, you should see the following items:
   - `dashboard/` — Web dashboard interface
   - `digna` — Main executable (backend + CLI combined)

!!! info "The configuration and licence files are not in the package"

    Neither `config.toml` nor `dashboard/dashboard_config.toml` ships with the installation — you
    create both yourself, in [Backend Configuration](#backend-configuration) and
    [Dashboard Configuration](#dashboard-configuration). `license.toml` does not ship either;
    digna supplies it separately, as Step 3 describes.

To extract from the shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Note"

    If `unzip` is not installed, add it with `sudo apt install -y unzip` or `sudo dnf install -y unzip`.

#### Make the Executable Runnable

Depending on how the archive was transferred, the executable bit may not survive extraction. Set it explicitly:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Create a Service Account

Running the backend as a dedicated unprivileged user is recommended for production deployments:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Note"

    On the RHEL family the equivalent shell path is `/sbin/nologin`.

### Step 3: Install the License File

!!! warning "Important"

    The license file is **not** included in the installation package and will be provided separately by digna.

1. Locate the `license.toml` file provided to you
2. Copy it into the root digna installation directory (where `config.toml` and the `digna` executable are located)

**Why this matters:**
The license file contains your customer information, license expiration date, and digital signature. **Do not modify this file** — any changes will invalidate it.

**Directory structure after setup:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend Configuration {: #backend-configuration }

### Step 1: Create and Edit the Configuration File

The `config_template.toml` file is provided in your digna installation directory. You only need to rename it to `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Location:** `/opt/digna/config.toml`

Open `config.toml` in a text editor and configure each section below.

#### [app] Section

This section configures cross-origin resource sharing (CORS) between the dashboard and the backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard URLs | The URLs the dashboard is served from. Browser requests from any other origin are rejected |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Required, so that the browser sends the session cookie with each request |

!!! note "Note"

    If you serve the dashboard from nginx or Apache on the default HTTP port, the origin to allow is `http://localhost` — or the server's public URL when the dashboard is reached from other machines.

!!! info "The [app] section is optional"

    From Release 2026.11, both keys, and the whole `[app]` section, may be left out. This is the
    right setup when a reverse proxy serves the dashboard and the backend under one origin: the
    browser then makes no cross-origin requests, and none is allowed by default.

#### [repo] Section

This section configures the connection to the PostgreSQL database:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` or IP | PostgreSQL server hostname/IP |
| `DIGNA_REPO_PORT` | `5432` (default) | PostgreSQL port |
| `DIGNA_REPO_DB` | `postgres` | Database name |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema created earlier |
| `DIGNA_REPO_USER` | `digna_user` | User created in PostgreSQL setup |
| `DIGNA_REPO_PASSWORD` | Your password | Password set during schema creation |
| `DIGNA_REPO_SSLMODE` | `prefer` (default) | Optional. PostgreSQL SSL mode: `disable`, `allow`, `prefer`, `require`, `verify-ca` or `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (default) | Optional. Number of connections digna keeps open to the repository |

!!! tip "Best Practice"

    `config.toml` contains a database password in plain text. Restrict its permissions so that only the service account can read it:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] Section

This section contains security, cookie and inspection settings:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_FERNET_KEY` | Value shown above | Key of the encryption used by earlier releases. It must be present; keep the value shown |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host the dashboard is reached under. `""` sets no domain, which is right behind a proxy that serves the dashboard and the backend under one origin |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Must be `true` whenever digna is served over HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Keeps the session cookie out of reach of scripts |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 hours) | Session timeout in seconds |
| `DIGNA_MAX_WORKERS` | Number of CPU cores - 1 | Number of inspections that may run at the same time |
| `DIGNA_FRONTEND_BASEURL` | Dashboard URL | Required. Used for the links in notification messages, so it must be a URL the recipients can open |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (default) | Optional. Seconds a single query against a source database may run before it is aborted; `0` disables the timeout |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (default) | Optional. Seconds to wait for a connection to a source database; `0` waits indefinitely |

!!! tip "Tip"

    To find the number of CPU cores available on your server, run `nproc`.

#### [encryption] Section

This section holds the key used to encrypt sensitive values stored in the repository. It is **required** — `config check` reports the `[encryption]` section as FAILED if the key is missing.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-encoded key | Encrypts sensitive values stored in the digna repository |

!!! warning "Protect config.toml"

    This key is a fixed value, identical across all digna installations, and it is what decrypts
    the sensitive values in your repository. Restrict `config.toml` to the account that runs
    digna, keep it out of source control and off shared drives, and exclude it from any backup
    that is stored less securely than the repository itself.

#### [logging] Section

This section configures logging behavior:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` or `DEBUG` | `INFO` for production, `DEBUG` for troubleshooting. `TRACE`, `WARN` and `ERROR` are accepted as well |
| `DIGNA_LOGGING_DIR` | `logs` (default) | Optional. Directory for the rotating log files, relative to the working directory |
| `DIGNA_LOGGING_MAX_FILES` | `30` (default) | Optional. Number of rotated log files to keep |

#### [duckdb] Section (Optional) {: #duckdb-section }

New in Release 2026.11. This section sets the resources of the **digna Engine**, which profiles
data inside digna for database connections whose profiling location is **digna Engine**, and
runs referential integrity checks between data sources on different database connections. See
[Profiling Location](../../../platform/profiling/profiling_location.md).

The section is optional. Without it, the defaults below apply.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (default) | Memory, in MB, that one digna Engine run may use. Up to `DIGNA_MAX_WORKERS` runs can be active at the same time |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Default: the system's temporary directory (`$TMPDIR`, or `/tmp` when it is not set) | Directory for temporary files when the data does not fit into memory |

!!! tip "Sizing the digna Engine"

    Plan for up to `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` of memory on the digna
    host, on top of what digna itself uses, and for enough free disk space in the temporary
    directory to hold the largest inspected date of the data sources that use the digna Engine.
    Point `DIGNA_DUCKDB_TEMP_DIRECTORY` at a disk with that space, writable by the account that
    runs digna:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
    ```

    You only need this section if at least one database connection uses the digna Engine, or a
    referential integrity check compares data sources on different connections.

---

### Step 2: Validate the Configuration

Before initializing the repository, check that `config.toml` is complete and well formed. In your digna installation directory, run:

```bash
./digna config check
```

Every section is validated on its own, so a single mistake does not hide the state of the rest:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Fix anything reported as FAILED and run the command again before continuing. A WARNING under **Unknown keys** lists keys in `config.toml` that digna does not read; they have no effect, so remove them or correct their spelling. See the [CLI reference](../../../cli/Command_Line_Interface_202611.md) for the full list of options.

### Step 3: Initialize the Repository

1. Open a terminal
2. Navigate to your digna installation directory (where `config.toml` and the `digna` executable are located)
3. Run the connection test:

```bash
cd /opt/digna
./digna repo check
```

On a new schema, the command connects and then reports that no repository is installed yet:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

At this point that is the expected result: it confirms that digna reaches PostgreSQL and the schema. A connection or authentication error instead points at the `[repo]` section or at the PostgreSQL setup.

!!! note "Note"

    On Linux, the current directory is not on your PATH, so the executable is invoked as `./digna` rather than `digna`. To use the shorter form everywhere, add a symbolic link:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Step 4: Install the Repository Schema

In the same directory, run:

```bash
./digna repo upgrade
```

This command installs the necessary tables in the repository schema and finishes with:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installs and upgrades"

    From Release 2026.11, `repo upgrade` installs a new repository and upgrades an existing one.
    `repo install` still works as another name for the same command.

### Step 5: Create an Admin User

The admin user is created directly against the repository schema, so the server does not need to be running yet. In the digna installation directory, run:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Example:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

This creates a user with email `admin@example.com` and full administrative privileges.

!!! tip "Tip"

    Wrap the password in single quotes. `bash` and `zsh` treat characters such as `!`, `$` and `*` specially, and an unquoted password containing them will not be passed through as typed.

!!! tip "Best Practice"

    Use a strong password with a mix of uppercase, lowercase, numbers, and special characters.

### Step 6: Start the digna Server

In the digna installation directory, start the server with:

```bash
./digna serve --address <host> --port <port>
```

**Parameters:**
- `--address` — Server hostname/IP (default `127.0.0.1`)
- `--port` — Server port (default `8000`)

When the server is up, it prints the address it listens on:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tip"

    If the dashboard is served from a different machine than the backend, open the API port in the firewall as well:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "The server holds the terminal"

    `serve` runs in the foreground and keeps running until you stop it with ++ctrl+c++. Leave it running while you finish the setup, and see [Running digna as a systemd Service](#running-digna-as-a-systemd-service) to start it automatically at boot instead.

---

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

The digna dashboard reads its own configuration from `dashboard/dashboard_config.toml`. That file does not ship with the installation — you create it in the `dashboard/` directory alongside the dashboard files.

Its contents are described under [Single Sign-On](../../../sso/overview.md), which is also where the file is needed: it carries the login options the dashboard offers and, for multi-instance deployments, the backend connection.

Choose your web server and follow the corresponding deployment steps.

#### Deploying to nginx

If you followed the [nginx Setup](#nginx-setup) section, the server block already points at your `dashboard` folder and no copying is required.

1. **Confirm the path**
   - Open `/etc/nginx/conf.d/digna.conf`
   - Verify that `root` points at your extracted `dashboard` folder

2. **Ensure the folder is readable**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Reload nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Test the Installation**
   - Open your browser
   - Navigate to `http://localhost` (or your configured URL)
   - You should see the digna dashboard login page

#### Deploying to Apache httpd

1. **Copy the Dashboard to the Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Add the Rewrite Rules**

   Create an `.htaccess` file inside the deployed folder so that dashboard routes survive a browser refresh:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Paste the following:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Restart Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Access the Dashboard**
   - Open your browser
   - Navigate to `http://localhost/digna`
   - You should see the digna dashboard login page

### Step 2: SELinux (RHEL Family Only)

On RHEL, Rocky, AlmaLinux and Fedora, SELinux is enforcing by default and will block the web server from reading files outside its expected locations. Check whether it is active:

```bash
getenforce
```

If the result is `Enforcing` and you are serving the dashboard from `/opt/digna/dashboard`, label the directory so the web server may read it:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Note"

    If `semanage` is not found, install it with `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Important"

    A dashboard that returns **403 Forbidden** on a freshly configured RHEL server is almost always an SELinux labelling problem rather than a file-permission one. Confirm with `sudo ausearch -m avc -ts recent`.

---

## Running digna as a systemd Service {: #running-digna-as-a-systemd-service }

### Why Run digna as a Service?

Running the digna backend as a systemd service ensures it:

- Starts automatically when the machine boots
- Runs in the background without an open terminal window
- Restarts automatically if it crashes
- Can be managed through `systemctl`, the standard Linux service manager

### Service Management Files

All necessary files are located in the digna installation directory under: `bin/`

The following shell scripts are available:

- `install_service.sh` — Registers digna with systemd
- `uninstall_service.sh` — Unregisters the service
- `start_service.sh` — Starts the registered service
- `stop_service.sh` — Stops the running service

!!! warning "Root Privileges Required"

    All scripts must be executed with `sudo`, because registering a service that starts at boot writes a unit file to `/etc/systemd/system`.

### Making the Scripts Executable

Extraction may not preserve the executable bit. Before first use:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Installing the Service

1. **Open a terminal**

2. **Navigate to the bin Folder**
   ```bash
   cd /opt/digna/bin
   ```

3. **Run the Installation Script**
   ```bash
   sudo ./install_service.sh
   ```

The digna server is now registered with systemd with **automatic startup** enabled. The service does not start immediately — see the next section to start it.

### Starting and Stopping the Service

#### To Start the Service

1. Open a terminal
2. Navigate to `/opt/digna/bin`
3. Run:
   ```bash
   sudo ./start_service.sh
   ```

#### To Stop the Service

1. Open a terminal
2. Navigate to `/opt/digna/bin`
3. Run:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tip"

    Always stop the service before updating application files.

### Managing the Service with systemctl

Once registered, the service can also be controlled with the standard systemd commands from any directory:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Verifying the Service

To confirm that the service is registered and running:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` means the service starts at boot; `active` means it is running now.

### Viewing the Service Logs

systemd captures everything the backend writes to the console. To read it:

```bash
sudo journalctl -u digna -n 100
```

To follow the log live while reproducing a problem:

```bash
sudo journalctl -u digna -f
```

!!! tip "Tip"

    This is the fastest way to diagnose a service that starts and immediately stops. A repository connection failure or a missing `license.toml` is reported here.

### Moving the Service to a New Directory

The unit file stores the absolute path to the executable, so relocating the installation requires re-registering the service:

1. **Uninstall the Current Service**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Move the Application Files**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Reinstall the Service**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Start the Service**
   ```bash
   sudo ./start_service.sh
   ```

### Uninstalling the Service

1. **Stop the Running Service**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Uninstall the Service**
   ```bash
   sudo ./uninstall_service.sh
   ```

The digna server is now unregistered from systemd.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

This section upgrades an installation of Release 2026.06 to Release 2026.11.

!!! warning "Upgrading from a release before 2026.06"

    First carry out the upgrade steps of Release 2026.06: [Upgrading to a New Release](../Release%202026.06/installation_guide_digna_linux_2026_06.md#upgrading-to-a-new-release). Then continue with the steps below.

### Before You Upgrade

**Creating a digna Repository Backup is Mandatory**

Before upgrading digna, back up your repository (PostgreSQL) to protect against data loss.
A backup ensures you can recover if the upgrade encounters unexpected issues.

To create a backup from the shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Requesting the License File for Release 2026.11**

Release 2026.11 needs a new `license.toml`. Request it from the digna team before you start, and
have it ready for [Step 7](#step-7-replace-the-license-file).

### Upgrade Process

#### Step 1: Stop the digna Service {: #step-1-stop-the-digna-service }

If digna is running as a systemd service, stop it first:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

If digna is running in the foreground, press ++ctrl+c++ in its terminal window.

#### Step 2: Backup Current Installation {: #step-2-backup-current-installation }

In your digna installation directory, rename the executable and the dashboard folder of your
current installation, so that the new release can be deployed alongside them:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Keep `digna_old` until you have verified the upgrade, and `dashboard_old` until you have restored
your configuration files from it (see Step 4). Afterwards you can delete both.

#### Step 3: Extract and Deploy New Version {: #step-3-extract-and-deploy-new-version }

1. Extract the new digna installation ZIP file
2. Copy the new `digna` executable and `dashboard` folder to your installation directory
3. Restore the executable bit and the ownership of the service account:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Important"

    Neither `config.toml` nor `dashboard/dashboard_config.toml` is ever included in the
    installation ZIP — the digna team never ships either file. Your existing configuration is
    therefore untouched by the upgrade, and the copies in the renamed `*_old` folders are the
    only ones you have.

#### Step 4: Restore Your Configuration Files {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 needs no change to `config.toml`: a file that works with Release 2026.06 keeps
working. Two changes are optional:

- Add a [`[duckdb]` section](#duckdb-section) if database connections are to use the digna Engine
  and its defaults don't suit your host.
- Leave out the `[app]` section if a reverse proxy serves the dashboard and the backend under one
  origin.

!!! warning "Settings that digna does not read"

    Earlier versions of this guide showed some settings that digna does not read. They have no
    effect, and `config check` lists them under **Unknown keys** in Step 6. Remove or correct
    them:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` and
      `digna_LOGGING_BACKUP_COUNT` don't exist. Remove them.
    - Setting names are case-sensitive. digna reads `DIGNA_REPO_HOST`, not `digna_REPO_HOST`.
      Write every name in upper case, as in [Backend Configuration](#backend-configuration).

!!! warning "Single sign-on: keep [[oidc_clients]]"

    digna reads single sign-on providers as a list of `[[oidc_clients]]` entries, each with its own
    `DIGNA_OIDC_KEY`. If you changed your providers to `[oidc_clients.<key>]` sections, as an
    earlier version of this guide showed, change them back. `config check` reports
    `OIDC config(s)` as FAILED while that form is in place:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Repeat the entry for every provider, and keep each `DIGNA_OIDC_KEY` matching the `key` in
    `dashboard_config.toml`. Only installations that use single sign-on are affected.

#### Step 5: Reload the Web Server {: #step-5-reload-the-web-server }

The dashboard is a set of static files, so your web server — and the browser — may still be
serving the previous version. Reload or restart whichever web server hosts the `dashboard`
folder, then reload the page with a hard refresh (++ctrl+f5++).

#### Step 6: Validate the Configuration {: #step-6-validate-the-configuration }

Confirm that `config.toml` is complete before touching the repository:

```bash
./digna config check
```

Every section must report OK. Fix anything reported as FAILED, remove the keys listed under
**Unknown keys**, and run the command again before continuing.

#### Step 7: Replace the License File {: #step-7-replace-the-license-file }

A license file issued for an earlier release does not work with Release 2026.11. Copy the
`license.toml` that the digna team provided for Release 2026.11 into the installation directory,
replacing the old one:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Do not keep the previous license"

    With the previous license, every command that checks the license — `serve`, `user`,
    `inspection`, `repo` — fails, so digna does not start and the repository cannot be upgraded.
    Verify the new license before going further:

    ```bash
    ./digna license check
    ```

#### Step 8: Upgrade the Repository Schema {: #step-8-upgrade-the-repository-schema }

In your digna installation directory, run:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 manages the repository schema with versioned migrations. The first upgrade from
an earlier release brings the schema to the last version of the previous scheme, records that as
its starting point, and then applies the migrations of Release 2026.11. It finishes with:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

All existing data is preserved. To see the state of the repository at any time, run
`./digna repo check`: it lists the latest applied migration and any pending ones.

!!! warning "digna does not start on an outdated repository"

    From Release 2026.11, the server refuses to start while the repository needs an upgrade, and
    says so, for example:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Run `repo upgrade` before you start the server or the service.

#### Step 9: Restart Services {: #step-9-restart-services }

If running as a systemd service:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

If running manually, restart the server:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

If using nginx or Apache, reload the respective web server:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

On the RHEL family, re-apply the SELinux labelling if the `dashboard` directory was replaced:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Step 10: Verify the Upgrade {: #step-10-verify-the-upgrade }

1. Confirm the release of the new executable:

    ```bash
    ./digna version
    ```

    The first line must read `Release: 2026.11`.

2. Access the digna dashboard and verify that the interface loads correctly.
3. Check the server logs for errors:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Test your database connections — see
   [Testing a Connection](../../../databases/overview.md#testing-a-connection).

To start with the new modules, see [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Connect an AI Agent](../../../platform/agentic/connect_ai_agent.md) for the digna MCP Server, and
[Profiling Location](../../../platform/profiling/profiling_location.md) for the digna Engine.

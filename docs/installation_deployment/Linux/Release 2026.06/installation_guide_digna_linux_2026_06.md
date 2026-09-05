---
title: Linux Installation Guide – digna Release 2026.06 | digna Documentation
description: Step-by-step guide to installing digna Release 2026.06 on Linux — system requirements, PostgreSQL setup, nginx or Apache configuration, backend and dashboard configuration, running digna as a systemd service, and upgrading to a new release.
keywords: digna linux installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql linux, nginx linux, digna systemd service, digna upgrade guide
image: /assets/logo_square.png
---

# Linux Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** September 5, 2026


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

- **dignabackend**: The core engine of the application, responsible for processing data and performing quality checks.
- **dignadashboard**: A web-based interface hosted on a web server, providing a user-friendly way to interact with the digna platform and visualize data quality metrics.

### What's New in Release 2026.06

This release brings data observability capabilities directly into your code, enabling developers to monitor data quality at the source. See the [release notes](http://docs.digna.ai/changelog/Release_202606/) for complete details.

### Looking for Windows or macOS?

This guide covers Linux. For other platforms, see the [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) or the [macOS Installation Guide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

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
   - `config.toml` — Configuration file
   - `license.toml` — License file (copy yours here)

To extract from the shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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

This section configures the digna backend application settings:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` or IP address | Hostname or IP where dignabackend is hosted |
| `digna_APP_PORT` | `8082` (default) | Port for REST API endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | If dashboard is on different server, include its URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Required for CORS with credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Allow all HTTP methods |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Allow all headers |

!!! note "Note"

    If you serve the dashboard from nginx or Apache on the default HTTP port, the origin to allow is `http://localhost` — or the server's public URL when the dashboard is reached from other machines.

#### [repo] Section

This section configures the connection to the PostgreSQL database:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` or IP | PostgreSQL server hostname/IP |
| `digna_REPO_PORT` | `5432` (default) | PostgreSQL port |
| `digna_REPO_DB` | `postgres` | Database name |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema created earlier |
| `digna_REPO_USER` | `digna_user` | User created in PostgreSQL setup |
| `digna_REPO_PASSWORD` | Your password | Password set during schema creation |

!!! tip "Best Practice"

    `config.toml` contains a database password in plain text. Restrict its permissions so that only the service account can read it:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] Section

This section contains security and cookie settings:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | Encryption key | Used to encrypt tokens and cookies (default provided) |
| `digna_COOKIE_DOMAIN` | `localhost` | Match your frontend domain |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (production) | Use `true` for HTTPS connections |
| `digna_COOKIE_HTTPONLY` | `true` | Always enabled for security |
| `digna_COOKIE_SAME_SITE` | `lax` | Prevents CSRF attacks |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 hours) | Session timeout in seconds |
| `digna_MAX_WORKERS` | Number of CPU cores - 1 | Number of parallel inspection tasks |

!!! tip "Tip"

    To find the number of CPU cores available on your server, run `nproc`.

#### [logging] Section

This section configures logging behavior:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` or `DEBUG` | `INFO` for production, `DEBUG` for troubleshooting |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Number of daily log backups to retain |

---

### Step 2: Initialize the Repository

1. Open a terminal
2. Navigate to your digna installation directory (where `config.toml` and the `digna` executable are located)
3. Run the connection test:

```bash
cd /opt/digna
./digna repo check
```

You should see a confirmation that the connection is established (the repository itself hasn't been initialized yet).

!!! note "Note"

    On Linux, the current directory is not on your PATH, so the executable is invoked as `./digna` rather than `digna`. To use the shorter form everywhere, add a symbolic link:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Step 3: Install the Repository Schema

In the same directory, run:

```bash
./digna repo install
```

This command installs the necessary tables and schema in your PostgreSQL database.

### Step 4: Start the digna Server

In the digna installation directory, start the server with:

```bash
./digna serve --address <host> --port <port>
```

**Parameters:**
- `--address` — Server hostname/IP
- `--port` — Server port

You should see startup messages confirming the server is running:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Tip"

    If the dashboard is served from a different machine than the backend, open the API port in the firewall as well:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Step 5: Create an Admin User

1. Open a **new** terminal window
2. Navigate to your digna installation directory
3. Run the following command to create an admin user:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Example:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

This creates a user with username `admin` and full administrative privileges.

!!! tip "Tip"

    Wrap the password in single quotes. `bash` and `zsh` treat characters such as `!`, `$` and `*` specially, and an unquoted password containing them will not be passed through as typed.

!!! tip "Best Practice"

    Use a strong password with a mix of uppercase, lowercase, numbers, and special characters.

---

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

The digna dashboard has its own separate `config.toml` file located in the `dashboard/` directory. This configuration is already provided and does not require changes during initial setup. You only need to configure it if you need to customize the backend connection.

If you need to modify the dashboard configuration (e.g., for multi-instance deployments), refer to the dashboard's documentation.

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

### Before You Upgrade

**Creating a digna Repository Backup is Mandatory**

Before upgrading digna, back up your repository (PostgreSQL) to protect against data loss.
A backup ensures you can recover if the upgrade encounters unexpected issues.

To create a backup from the shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Upgrade Process

#### Step 1: Stop the digna Service

If digna is running as a systemd service, stop it first:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

If digna is running in the foreground, press `Ctrl + C` in its terminal window.

#### Step 2: Backup Current Backend Installation

In your digna installation directory:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Step 3: Extract and Deploy New Version

1. Extract the new digna installation ZIP file
2. Copy the new `digna` executable and `dashboard` folder to your installation directory
3. Restore the executable bit and the ownership of the service account:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Important"

    The `config.toml` file is **never** included in the installation ZIP. Your existing configuration remains safe.

### Step 4: Restore Your Configuration Files

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Step 5: Upgrade the Repository Schema

Navigate to your digna installation directory and run:

```bash
cd /opt/digna
./digna repo upgrade
```

This updates the PostgreSQL schema to the latest version while preserving all existing data.

### Step 6: Restart Services

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

#### Step 7: Verify the Upgrade

1. Access the digna dashboard
2. Verify that the interface loads correctly
3. Check the server logs for any errors:

```bash
sudo journalctl -u digna -n 100
```

# macOS Installation Guide for digna Release 2026.06

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
9. [Running digna as a Background Service](#running-digna-as-a-background-service)
10. [Upgrading to a New Release](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### About digna

digna is a comprehensive AI-driven platform designed to optimize data quality management across various data environments such as warehouses, lakes, and lakehouses. Built to be highly scalable and adaptable, digna addresses modern data challenges through automation, real-time monitoring, and anomaly detection.

digna consists of two main components:

- **digna**: The core engine of the application, responsible for processing data and performing quality checks. It combines the backend and the command line interface in a single executable, replacing the separate `dignabackend` and `dignacli` of earlier releases.
- **dignadashboard**: A web-based interface hosted on a web server, providing a user-friendly way to interact with the digna platform and visualize data quality metrics.

### What's New in Release 2026.06

This release brings data observability capabilities directly into your code, enabling developers to monitor data quality at the source. See the [release notes](http://docs.digna.ai/changelog/Release_202606/) for complete details.

### Looking for Windows or Linux?

This guide covers macOS. For other platforms, see the [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) or the [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## System Requirements {: #system-requirements }

Before you begin the installation, ensure that your system meets the following minimum requirements:

| Requirement | Specification |
|---|---|
| **Operating System** | macOS 13 (Ventura) or later |
| **Architecture** | Apple Silicon (arm64) or Intel (x86_64) |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB available storage |
| **Database** | PostgreSQL Server 12 or higher |
| **Web Server** | nginx, Apache httpd, or equivalent |
| **Command Line Tools** | Xcode Command Line Tools (required by Homebrew) |

### Database Installation Options

**If PostgreSQL is already installed:**
You can add a new database for digna to your existing PostgreSQL Server.

**If installing PostgreSQL on the same machine as digna:**

!!! info "Recommended Specifications"

    - **Memory**: 32 GB RAM (instead of 16 GB)
    - **Disk Space**: 50 GB available storage (instead of 10 GB)

    These higher specifications accommodate both digna and the PostgreSQL database running simultaneously.

### Checking Your Architecture

Several paths in this guide differ between Apple Silicon and Intel Macs. To check which you have, open **Terminal** and run:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew installs to `/opt/homebrew`.
- `x86_64` — Intel. Homebrew installs to `/usr/local`.

!!! tip "Tip"

    Rather than hard-coding either path, this guide uses `$(brew --prefix)`, which expands to the correct location on both architectures. You can copy the commands verbatim.

---

## Pre-Installation Setup {: #pre-installation-setup }

Before installing digna, ensure that three key prerequisites are in place:

1. **Homebrew** – the package manager used to install the components below
2. **PostgreSQL Server** – for storing calculated metrics and performance data
3. **Web Server** – for hosting the digna Dashboard

If these components are not already set up, follow the sections below to install and configure them.

### Installing Homebrew

Homebrew is the standard package manager for macOS and is used throughout this guide to install PostgreSQL and nginx.

#### Step 1: Check Whether Homebrew Is Already Installed

Open **Terminal** (press `Cmd + Space`, type `Terminal`, press Enter) and run:

```bash
brew --version
```

If a version number is returned, skip to the [PostgreSQL Server Setup](#postgresql-server-setup) section.

#### Step 2: Install Homebrew

If the command was not found, install Homebrew by following the instructions on the [official Homebrew site](https://brew.sh). The installer also installs the Xcode Command Line Tools if they are not already present.

#### Step 3: Add Homebrew to Your PATH

On Apple Silicon, the installer prints two commands to add Homebrew to your shell environment. Run them as instructed, then confirm:

```bash
brew --prefix
```

This should print `/opt/homebrew` on Apple Silicon or `/usr/local` on Intel.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### If You Already Have PostgreSQL

If PostgreSQL is already installed and running on your local machine or if you are using a managed remote PostgreSQL server, you can skip to the [next section](#web-server-configuration).

### Installation Options

macOS offers two straightforward ways to install PostgreSQL. Choose **one**:

- [Homebrew](#postgresql-homebrew) — command-line installation, recommended for server deployments
- [Postgres.app](#postgresql-app) — graphical installation, convenient for local evaluation

### Installing PostgreSQL with Homebrew {: #postgresql-homebrew }

#### Step 1: Install the PostgreSQL Formula

```bash
brew install postgresql@16
```

#### Step 2: Add PostgreSQL to Your PATH

Versioned PostgreSQL formulas are *keg-only*, which means Homebrew does not link their commands into your PATH automatically. Add them yourself:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Note"

    This assumes the default `zsh` shell used by macOS. If you use `bash`, append the same line to `~/.bash_profile` instead.

#### Step 3: Start the PostgreSQL Service

```bash
brew services start postgresql@16
```

This starts PostgreSQL immediately and configures it to start again automatically when you log in.

#### Step 4: Verify the Installation

```bash
psql --version
```

You should see the PostgreSQL version if the installation was successful.

#### Step 5: Connect to the Server

```bash
psql postgres
```

!!! warning "Important — macOS Differs From Windows Here"

    The Windows installer prompts you to create a `postgres` superuser and password. Homebrew does not. Instead it creates a superuser named after your **macOS account**, with no password, reachable only from the local machine.

    This means there is no `postgres` role on a fresh Homebrew installation. Use your own account name when you need a superuser, and create an explicit digna user as described in [Initial Installation](#initial-installation).

#### Step 6: Confirm the Port

The default PostgreSQL port is `5432`. To confirm the port your server is listening on:

```bash
psql postgres -c "SHOW port;"
```

Note the value — you will need it when configuring the digna backend.

### Installing PostgreSQL with Postgres.app {: #postgresql-app }

If you prefer a graphical installation:

1. Download [Postgres.app](https://postgresapp.com) and drag it into your **Applications** folder
2. Open the app and click **Initialize** to create a new server
3. Follow the app's instructions to add its command-line tools to your PATH
4. Verify the installation:

```bash
psql --version
```

Postgres.app also creates a superuser named after your macOS account.

---

## Web Server Configuration {: #web-server-configuration }

digna requires a web server to host the dashboard. Choose one of the following options:

- [nginx](#nginx-setup) — installed via Homebrew, recommended
- [Apache httpd](#apache-setup) — included with macOS

You only need to install and configure **one** of these servers.

Both sections configure two things the dashboard depends on:

- **A single-page-application fallback**, so that refreshing a dashboard URL does not return a 404
- **A `.md` MIME type**, so that Markdown files are served correctly

### nginx Setup {: #nginx-setup }

#### Overview

nginx is a lightweight, high-performance web server well suited to serving the static digna dashboard.

#### Installation

```bash
brew install nginx
```

#### Starting nginx

```bash
brew services start nginx
```

#### Verify the Installation

1. Open your browser
2. Navigate to `http://localhost:8080`
3. You should see the nginx welcome page

!!! note "Note — Default Port Is 8080, Not 80"

    Homebrew configures nginx to listen on port `8080` so that it can run without administrator privileges. On macOS, binding to port `80` or any other port below 1024 requires root.

    To serve the dashboard on port 80, change `listen 8080;` to `listen 80;` in the configuration below and start nginx with `sudo brew services start nginx` instead.

#### Configuring a Site for the Dashboard

Homebrew's nginx configuration includes every file in its `servers` directory. Create a dedicated configuration file for digna there:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Paste the following, replacing `/path/to/digna/dashboard` with the actual path to your extracted `dashboard` folder:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
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

#### Apply the Configuration

Test the configuration for syntax errors, then reload nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd Setup {: #apache-setup }

#### Overview

macOS includes Apache httpd, so no installation is required. It is disabled by default.

#### Starting Apache

```bash
sudo apachectl start
```

#### Verify the Installation

1. Open your browser
2. Navigate to `http://localhost`
3. You should see the message "It works!"

#### Required: Enable mod_rewrite

The dashboard requires URL rewriting. Open the Apache configuration:

```bash
sudo nano /etc/apache2/httpd.conf
```

Find the following line and remove the leading `#` to uncomment it:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Required: Allow .htaccess Overrides

In the same file, locate the `<Directory "/Library/WebServer/Documents">` block and change:

```apache
AllowOverride None
```

to:

```apache
AllowOverride All
```

#### Required: MIME Type for Markdown Files

Still in `httpd.conf`, add the following line so that Markdown files are served correctly:

```apache
AddType text/markdown .md
```

!!! warning "Important"

    Without this setting, `.md` files may not be served properly.

#### Apply the Configuration

Check the configuration for syntax errors, then restart Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
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

To run these from the Terminal in a single step:

```bash
psql postgres
```

Then paste the statements at the `postgres=#` prompt and type `\q` to exit.

!!! tip "Best Practice"

    Use strong, complex passwords for database users. Avoid easily guessable credentials.

---

### Step 2: Extract the digna Installation Package

1. Locate the digna installation ZIP file provided to you
2. Extract it to your desired installation location — for example `/opt/digna` or `~/digna`
3. After extraction, you should see the following items:
   - `dashboard/` — Web dashboard interface
   - `digna` — Main executable (backend + CLI combined)

!!! info "The configuration and licence files are not in the package"

    Neither `config.toml` nor `dashboard/dashboard_config.toml` ships with the installation — you
    create both yourself, in [Backend Configuration](#backend-configuration) and
    [Dashboard Configuration](#dashboard-configuration). `license.toml` does not ship either;
    digna supplies it separately, as Step 3 describes.

To extract from the Terminal:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Make the Executable Runnable

Depending on how the archive was transferred, the executable bit may not survive extraction. Set it explicitly:

```bash
cd /opt/digna
chmod +x digna
```

#### If macOS Blocks the Application

Files downloaded through a browser or mail client are tagged with a quarantine attribute. If macOS reports that the app *"cannot be opened because the developer cannot be verified"*, clear the attribute from the installation directory:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternatively, open **System Settings → Privacy & Security**, find the blocked item near the bottom of the page, and click **Open Anyway**.

!!! note "Note"

    This step is only needed if macOS actually blocks the executable. Packages transferred over SSH or from internal file shares are usually not quarantined.

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
mv config_template.toml config.toml
```

**Location:** `/opt/digna/config.toml`

Open `config.toml` in a text editor and configure each section below.

#### [app] Section

This section configures the digna backend application settings:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | If dashboard is on different server, include its URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Required for CORS with credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Allow all HTTP methods |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Allow all headers |

!!! note "Note"

    If you serve the dashboard from Homebrew's nginx on its default port, the origin to allow is `http://localhost:8080`.

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

#### [base] Section

This section contains security and cookie settings:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Match your frontend domain |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (production) | Use `true` for HTTPS connections |
| `digna_COOKIE_HTTPONLY` | `true` | Always enabled for security |
| `digna_COOKIE_SAME_SITE` | `lax` | Prevents CSRF attacks |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 hours) | Session timeout in seconds |
| `digna_MAX_WORKERS` | Number of CPU cores - 1 | Number of parallel inspection tasks |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Maximum delay, in seconds, that the scheduler may add before starting a due job |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Time of day (24-hour `HH:MM`) at which the daily cleanup run starts |

!!! tip "Tip"

    To find the number of CPU cores available on your Mac, run `sysctl -n hw.ncpu`.

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` or `DEBUG` | `INFO` for production, `DEBUG` for troubleshooting |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Number of daily log backups to retain |

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

Overall: OK
```

Fix anything reported as FAILED and run the command again before continuing. See the [CLI reference](../../../cli/Command_Line_Interface_202606.md) for the full list of options.

### Step 3: Initialize the Repository

1. Open **Terminal**
2. Navigate to your digna installation directory (where `config.toml` and the `digna` executable are located)
3. Run the connection test:

```bash
cd /opt/digna
./digna repo check
```

You should see a confirmation that the connection is established (the repository itself hasn't been initialized yet).

!!! note "Note"

    On macOS, commands in the current directory are not on your PATH, so the executable is invoked as `./digna` rather than `digna`. To use the shorter form everywhere, add the installation directory to your PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Step 4: Install the Repository Schema

In the same directory, run:

```bash
./digna repo install
```

This command installs the necessary tables and schema in your PostgreSQL database.

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

    Wrap the password in single quotes. `zsh` treats characters such as `!`, `$` and `*` specially, and an unquoted password containing them will not be passed through as typed.

!!! tip "Best Practice"

    Use a strong password with a mix of uppercase, lowercase, numbers, and special characters.

### Step 6: Start the digna Server

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

    The first time you start the server, macOS may ask whether you want the application to accept incoming network connections. Click **Allow**, otherwise the dashboard will not be able to reach the backend.

!!! note "The server holds the terminal"

    `serve` runs in the foreground and keeps running until you stop it with ++ctrl+c++. Leave it running while you finish the setup, and see [Running digna as a Background Service](#running-digna-as-a-background-service) to start it automatically at boot instead.

---

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

The digna dashboard reads its own configuration from `dashboard/dashboard_config.toml`. That file does not ship with the installation — you create it in the `dashboard/` directory alongside the dashboard files.

Its contents are described under [Single Sign-On](../../../sso/overview.md), which is also where the file is needed: it carries the login options the dashboard offers and, for multi-instance deployments, the backend connection.

Choose your web server and follow the corresponding deployment steps.

#### Deploying to nginx

If you followed the [nginx Setup](#nginx-setup) section, the server block already points at your `dashboard` folder and no copying is required.

1. **Confirm the path**
   - Open `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Verify that `root` points at your extracted `dashboard` folder

2. **Ensure the folder is readable**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Reload nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Test the Installation**
   - Open your browser
   - Navigate to `http://localhost:8080` (or your configured URL)
   - You should see the digna dashboard login page

#### Deploying to Apache httpd

1. **Copy the Dashboard to the Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Add the Rewrite Rules**

   Create an `.htaccess` file inside the deployed folder so that dashboard routes survive a browser refresh:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
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
   sudo apachectl restart
   ```

4. **Access the Dashboard**
   - Open your browser
   - Navigate to `http://localhost/digna`
   - You should see the digna dashboard login page

---

## Running digna as a Background Service {: #running-digna-as-a-background-service }

### Why Run digna as a Service?

Running the digna backend as a background service ensures it:

- Starts automatically when the machine boots
- Runs in the background without an open Terminal window
- Restarts automatically if it crashes
- Can be managed through `launchctl`, macOS's service manager

### Service Management Files

All necessary files are located in the digna installation directory under: `bin/`

The following shell scripts are available:

- `install_service.sh` — Registers digna with launchd
- `uninstall_service.sh` — Unregisters the service
- `start_service.sh` — Starts the registered service
- `stop_service.sh` — Stops the running service

!!! warning "Administrator Required"

    All scripts must be executed with `sudo`, because registering a service that starts at boot writes to `/Library/LaunchDaemons`.

### Making the Scripts Executable

Extraction may not preserve the executable bit. Before first use:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Installing the Service

1. **Open Terminal**

2. **Navigate to the bin Folder**
   ```bash
   cd /opt/digna/bin
   ```

3. **Run the Installation Script**
   ```bash
   sudo ./install_service.sh
   ```

The digna server is now registered with launchd with **automatic startup** enabled. The service does not start immediately — see the next section to start it.

### Starting and Stopping the Service

#### To Start the Service

1. Open Terminal
2. Navigate to `/opt/digna/bin`
3. Run:
   ```bash
   sudo ./start_service.sh
   ```

#### To Stop the Service

1. Open Terminal
2. Navigate to `/opt/digna/bin`
3. Run:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tip"

    Always stop the service before updating application files.

### Verifying the Service

To confirm that the service is registered and running:

```bash
sudo launchctl list | grep digna
```

A line beginning with a process ID indicates the service is running. A `-` in the first column means it is registered but stopped.

### Moving the Service to a New Directory

launchd stores the absolute path to the executable, so relocating the installation requires re-registering the service:

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

The digna server is now unregistered from launchd.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Before You Upgrade

**Verify All Database Connections First**

From Release 2026.06, digna reaches every source technology over **ODBC**. Earlier releases
offered a choice between a per-technology driver and ODBC, selected with a **Use ODBC** switch.
The digna team decided to build on ODBC alone, because a single, standard interface gives you
more than a set of bespoke drivers can:

- **Authentication** — authentication is part of ODBC, so a connection can use whatever its
  driver supports: passwords, tokens and PATs, Kerberos and Active Directory, MFA and browser-based
  single sign-on, cloud identity, client certificates and TLS. New methods arrive with a driver
  update, rather than waiting for a digna release.
- **Drivers maintained by the database vendors** — the vendor's own driver tracks new server
  versions and security fixes, and you can update it on your own schedule, independently of digna.
- **One way to configure everything** — every technology is a list of key/value properties, with
  the same interface, the same encryption of sensitive values and the same troubleshooting,
  instead of a different set of fields per source.
- **Tuning and reach** — driver-level options such as timeouts, TLS settings, proxies and fetch
  sizes are available for every source, and any technology with a compliant ODBC driver can be
  connected, including ones digna does not publish a dedicated guide for.

In practice this means the **Use ODBC** switch and the separate host, port, database, user and
password fields no longer exist. **Every connection that does not already use ODBC must be
changed to ODBC** — there is no automatic conversion, so plan for this before you upgrade:

1. Review every database connection defined in your installation and list the ones that are not
   yet using ODBC — each of these has to be reconfigured.
2. Install the matching ODBC driver on the digna host — connections are opened from the server
   that runs the digna backend, not from the browser. See
   [Install the ODBC Driver on the digna Host](../../../databases/overview.md#install-the-driver).
3. Have the ODBC properties ready for each affected connection. The
   [technology guides](../../../databases/overview.md#technology-guides) list a known-working
   property set per source.

After the upgrade, change each affected connection over to ODBC and test it from the dashboard —
see [Create a Database Connection](../../../databases/overview.md#create-a-database-connection)
and [Testing a Connection](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy connections"

    The Databricks Legacy connector has been removed in this release. Migrate those connections
    to the [Databricks](../../../databases/databricks_connector_guide.md) connector.

**Creating a digna Repository Backup is Mandatory**

Before upgrading digna, back up your repository (PostgreSQL) to protect against data loss.
A backup ensures you can recover if the upgrade encounters unexpected issues.

To create a backup from the Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Upgrade Process

#### Step 1: Stop the digna Service

If digna is running as a background service, stop it first:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

If digna is running in the foreground, press `Ctrl + C` in its Terminal window.

#### Step 2: Backup Current Installation

In your digna installation directory, rename the folders of your current installation so that the new release can be deployed alongside them:

```bash
cd /opt/digna
mv dignabackend dignabackend_old
```
```bash
mv dignacli dignacli_old
```
```bash
mv dashboard dashboard_old
```

!!! info "dignabackend and dignacli are no longer used"

    Starting with Release 2026.06, `dignabackend` and `dignacli` are replaced by the single `digna` executable, which combines the backend and the CLI. Keep `dignabackend_old` and `dignacli_old` only until you have verified the upgrade — afterwards you can delete both folders. Keep `dashboard_old` until you have restored your configuration files from it (see Step 4).

#### Step 3: Extract and Deploy New Version

1. Extract the new digna installation ZIP file
2. Copy the new `digna` executable and `dashboard` folder to your installation directory
3. Restore the executable bit and, if necessary, clear the quarantine attribute:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Important"

    Neither `config.toml` nor `dashboard/dashboard_config.toml` is ever included in the
    installation ZIP — the digna team never ships either file. Your existing configuration is
    therefore untouched by the upgrade, and the copies in the renamed `*_old` folders are the
    only ones you have.

#### Step 4: Restore Your Configuration Files

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

!!! warning "Release 2026.06 changes config.toml"

    Three settings are new and required, and three are no longer used. A `config.toml` carried over from an earlier release does not contain the new settings, and digna will not start until they are present. Add the following to your existing `config.toml`:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Add the two `[base]` keys to your existing `[base]` section, and add `[encryption]` as a new section. Then remove the settings that are no longer used: **`digna_FERNET_KEY`** from `[base]`, and **`digna_APP_HOST`** and **`digna_APP_PORT`** from `[app]` — the server now takes its address and port from `digna serve`.

    See [Backend Configuration](#backend-configuration) for what each setting does.

!!! warning "Single sign-on: the [oidc_clients] format has changed"

    Release 2026.06 replaces the array of tables with one table per provider, named after the
    provider key. `DIGNA_OIDC_KEY` is gone — the key is now part of the section header.

    Before:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    After:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Repeat the section for every provider, and keep each key matching the `key` in
    `dashboard_config.toml`. `digna config check` reports `oidc_clients` as FAILED while the
    old form is still in place. Only installations that use single sign-on are affected.

#### Step 5: Reload the Web Server

The dashboard is a set of static files, so your web server — and the browser — may still be
serving the previous version. Reload or restart whichever web server hosts the `dashboard`
folder, then reload the page with a hard refresh (++cmd+shift+r++).

#### Step 6: Validate the Configuration

Confirm that the updated `config.toml` is complete before touching the repository:

```bash
./digna config check
```

Every section must report OK. Fix anything reported as FAILED and run the command again before continuing.

#### Step 7: Replace the License File

Each release is licensed separately. Copy the `license.toml` that the digna team provided for
this release into the installation directory, replacing the old one:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Do not keep the previous license"

    A `license.toml` issued for an earlier release does not cover this one, and every command
    that checks the license — `user`, `inspection`, `repo` — aborts before touching the
    repository when the check fails. Verify it before going further:

    ```bash
    ./digna license check
    ```

#### Step 8: Upgrade the Repository Schema

Navigate to your digna installation directory and run:

```bash
cd /opt/digna
./digna repo upgrade
```

This updates the PostgreSQL schema to the latest version while preserving all existing data.

#### Step 9: Restart Services

If running as a background service:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

If running manually, restart the server:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

If using nginx or Apache, restart the respective web server:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Step 10: Verify the Upgrade

1. Access the digna dashboard
2. Verify that the interface loads correctly
3. Check the server logs for any errors
4. Change every connection that did not already use ODBC over to ODBC, then test all connections
   — see [Testing a Connection](../../../databases/overview.md#testing-a-connection)
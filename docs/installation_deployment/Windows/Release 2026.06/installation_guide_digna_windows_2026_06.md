---
title: Windows Installation Guide – digna Release 2026.06 | digna Documentation
description: Step-by-step guide to installing digna Release 2026.06 on Windows — system requirements, PostgreSQL setup, web server configuration, backend and dashboard configuration, running digna as a Windows service, and upgrading to a new release.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Windows Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** August 30, 2026


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
9. [Running digna as a Windows Service](#running-digna-as-a-windows-service)
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

### Looking for macOS or Linux?

This guide covers Windows. For other platforms, see the [macOS Installation Guide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) or the [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## System Requirements {: #system-requirements }

Before you begin the installation, ensure that your system meets the following minimum requirements:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server or Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB available storage |
| **Database** | PostgreSQL Server 12 or higher |
| **Web Server** | IIS, Apache Tomcat, or equivalent |

### Database Installation Options

**If PostgreSQL is already installed:**
You can add a new database for digna to your existing PostgreSQL Server.

**If installing PostgreSQL on the same machine as digna:**

!!! info "Recommended Specifications"

    - **Memory**: 32 GB RAM (instead of 16 GB)
    - **Disk Space**: 50 GB available storage (instead of 10 GB)

    These higher specifications accommodate both digna and the PostgreSQL database running simultaneously.

---

## Pre-Installation Setup {: #pre-installation-setup }

Before installing digna, ensure that two key prerequisites are in place:

1. **PostgreSQL Server** – for storing calculated metrics and performance data
2. **Web Server** – for hosting the digna Dashboard

If these components are not already set up, follow the sections below to install and configure them.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### If You Already Have PostgreSQL

If PostgreSQL is already installed and running on your local machine or if you are using a managed remote PostgreSQL server, you can skip to the [next section](#web-server-configuration).

### Installing PostgreSQL

Follow these steps to install PostgreSQL on Windows:

#### Step 1: Download PostgreSQL

1. Visit the [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Select **Windows**
3. Download the latest installer

#### Step 2: Run the Installer

1. Double-click the downloaded installer file
2. Follow the prompts in the setup wizard

#### Step 3: Choose Installation Directory

Select the directory where PostgreSQL will be installed. The default location is usually appropriate.

#### Step 4: Select Components

For a standard setup, keep the default component options selected.

#### Step 5: Set PostgreSQL Superuser Password

Enter and confirm a password for the PostgreSQL superuser (`postgres`). **Save this password securely** — you will need it later.

#### Step 6: Configure Port Number

The default PostgreSQL port is `5432`. You can use the default or specify a different port if needed.

!!! tip "Tip"

    If port 5432 is already in use, choose an alternative port and note it for later configuration.

#### Step 7: Choose Locale

Select the locale for your database. The default is usually suitable for most installations.

#### Step 8: Complete Installation

Click **Next** through the remaining steps, then click **Finish**.

#### Step 9: Verify Installation

Open Command Prompt and verify PostgreSQL is installed:

```bash
psql --version
```

You should see the PostgreSQL version if the installation was successful.

---

## Web Server Configuration {: #web-server-configuration }

digna requires a web server to host the dashboard. Choose one of the following options:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

You only need to install and configure **one** of these servers.

### IIS Setup {: #iis-setup }

#### Overview

Internet Information Services (IIS) is Microsoft's web server for hosting websites and web applications.

#### Enabling IIS

1. **Open Control Panel**
   - Press `Win + R`
   - Type `control` and press Enter

2. **Navigate to Windows Features**
   - Click **Programs**
   - Select **Turn Windows features on or off**

3. **Enable Internet Information Services**
   - Scroll down and find **Internet Information Services (IIS)**
   - Check the checkbox to enable it
   - Click the **+** to expand and verify these subcomponents are selected:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Click OK** to apply changes

5. **Verify IIS Installation**
   - Open your browser
   - Navigate to `http://localhost`
   - You should see the IIS Welcome page

#### Required: URL Rewrite Module

IIS requires the URL Rewrite component. Download and install it from the [official Microsoft page](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Required: MIME Type for Markdown Files

To ensure Markdown files (`.md`) are served correctly by IIS:

1. Open **IIS Manager** (press `Win + R`, type `inetmgr`, press Enter)
2. Navigate to **Your Site > MIME Types**
3. Click **Add...**
4. Configure:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Important"

    Without this setting, `.md` files may not be served properly.

---

### Apache Tomcat Setup {: #apache-tomcat-setup }

#### Overview

Apache Tomcat is an open-source Java servlet container and web server.

#### Installation

1. **Download Apache Tomcat**
   - Visit [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Download the Windows ZIP distribution

2. **Extract the Archive**
   - Extract the ZIP file to a directory on your system
   - Example: `C:\Program Files\Apache Tomcat`

3. **Verify Tomcat is Running**
   - Open your browser
   - Navigate to `http://localhost:8080`
   - You should see the Apache Tomcat welcome page

!!! tip "Tip"

    Apache Tomcat typically starts automatically after installation. If it doesn't, navigate to the `bin` folder and run `startup.bat`.

---

## Initial Installation {: #initial-installation }

### Step 1: Set Up the digna Repository

The digna repository stores all metrics calculated by digna. It acts as the central database for analytical and performance data.

#### Create Repository Schema and User

Open your PostgreSQL client (pgAdmin, psql, or similar) and execute the following SQL commands:

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

!!! tip "Best Practice"

    Use strong, complex passwords for database users. Avoid easily guessable credentials.

---

### Step 2: Extract the digna Installation Package

1. Locate the digna installation ZIP file provided to you
2. Extract it to your desired installation location
3. After extraction, you should see the following items:
   - `dashboard/` — Web dashboard interface
   - `digna` — Main executable (backend + CLI combined)

!!! info "The configuration and licence files are not in the package"

    Neither `config.toml` nor `dashboard/dashboard_config.toml` ships with the installation — you
    create both yourself, in [Backend Configuration](#backend-configuration) and
    [Dashboard Configuration](#dashboard-configuration). `license.toml` does not ship either;
    digna supplies it separately, as Step 3 describes.

### Step 3: Install the License File

!!! warning "Important"

    The license file is **not** included in the installation package and will be provided separately by digna.

1. Locate the `license.toml` file provided to you
2. Copy it into the root digna installation directory (where `config.toml` and the `digna` executable are located)

**Why this matters:**
The license file contains your customer information, license expiration date, and digital signature. **Do not modify this file** — any changes will invalidate it.

**Directory structure after setup:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend Configuration {: #backend-configuration }

### Step 1: Create and Edit the Configuration File

The `config_template.toml` file is provided in your digna installation directory. You only need to rename it to `config.toml`.

**Location:** `digna_installation/config.toml`

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
digna config check
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

1. Open Command Prompt
2. Navigate to your digna installation directory (where `config.toml` and the `digna` executable are located)
3. Run the connection test:

```bash
digna repo check
```

You should see a confirmation that the connection is established (the repository itself hasn't been initialized yet).

### Step 4: Install the Repository Schema

In the same directory, run:

```bash
digna repo install
```

This command installs the necessary tables and schema in your PostgreSQL database.

### Step 5: Create an Admin User

The admin user is created directly against the repository schema, so the server does not need to be running yet. In the digna installation directory, run:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Example:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

This creates a user with full administrative privileges.

!!! tip "Best Practice"

    Use a strong password with a mix of uppercase, lowercase, numbers, and special characters.

### Step 6: Start the digna Server

In the digna installation directory, start the server with:

```bash
digna serve --address <host> --port <port>
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

!!! note "The server holds the terminal"

    `serve` runs in the foreground and keeps running until you stop it with ++ctrl+c++. Leave it running while you finish the setup, and see [Running digna as a Windows Service](#running-digna-as-a-windows-service) to start it automatically at boot instead.

---

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

The digna dashboard reads its own configuration from `dashboard/dashboard_config.toml`. That file does not ship with the installation — you create it in the `dashboard/` directory alongside the dashboard files.

Its contents are described under [Single Sign-On](../../../sso/overview.md), which is also where the file is needed: it carries the login options the dashboard offers and, for multi-instance deployments, the backend connection.

Choose your web server and follow the corresponding deployment steps.

#### Deploying to IIS

1. **Open IIS Manager**
   - Press `Win + R`, type `inetmgr`, press Enter

2. **Create a New Website**
   - In the left panel, right-click **Sites**
   - Select **Add Website...**

3. **Configure the Website**
   - **Site Name**: Enter a name (e.g., "dignaDashboard")
   - **Physical Path**: Click Browse and select your `dashboard` folder
   - **Binding**: Set IP address and port (default port 80 for HTTP, 443 for HTTPS)

4. **Start the Website**
   - Click **OK** to create the site
   - Right-click the new site and select **Start**

5. **Test the Installation**
   - Open your browser
   - Navigate to `http://localhost` (or your configured URL)
   - You should see the digna dashboard login page

#### Deploying to Apache Tomcat

1. **Copy Dashboard to Tomcat**
   - Copy the `dashboard` folder to your Tomcat `webapps` directory
   - Rename it if needed (e.g., to `digna`)
   - Example: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verify Deployment**
   - Refresh or reload the Tomcat management page (http://localhost:8080)
   - You should see "digna" (or your chosen name) listed in the deployed applications

3. **Access the Dashboard**
   - Open your browser
   - Navigate to `http://localhost:8080/digna`
   - You should see the digna dashboard login page

---

## Running digna as a Windows Service {: #running-digna-as-a-windows-service }

### Why Use a Windows Service?

Running the digna backend as a Windows service ensures it:
- Starts automatically when the server boots
- Runs in the background without an open Command Prompt
- Restarts automatically if it crashes
- Can be managed through Windows Services

### The `windows` Commands

The service is managed by the `digna` executable itself, through the `digna windows`
subcommands. There are no batch files to run.

| Command | Purpose |
|---|---|
| `digna windows install` | Registers digna as a Windows service |
| `digna windows start` | Starts the registered service |
| `digna windows stop` | Stops the running service |
| `digna windows uninstall` | Unregisters the service |

!!! warning "Administrator Required"

    All four commands must be run from a Command Prompt opened as Administrator.

Every command takes `--name` to address a service registered under a non-default name. The full
option list is in the [CLI reference](../../../cli/Command_Line_Interface_202606.md).

### Installing the Service

1. **Open Command Prompt as Administrator**
   - Right-click Command Prompt
   - Select "Run as Administrator"

2. **Navigate to your digna installation directory**
   ```bash
   cd C:\path\to\digna
   ```

3. **Register the service**
   ```bash
   digna windows install
   ```

!!! important "Specify the address and port unless the defaults suit you"

    `install` records the address and port in the service registration, and the service binds to
    exactly what was recorded. The defaults are `127.0.0.1` and `8000`, which accept connections
    only from the machine itself. A dashboard on another host cannot reach that, so give the
    address the backend should listen on:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    These are not read from `config.toml`. To change them later, uninstall the service and
    install it again with the new values.

The service is registered with **automatic startup**, so it will start with Windows. It does not
start immediately — see the next section.

#### Install Options

| Option | Default | Purpose |
|---|---|---|
| `--name` | `digna` | Name to register the service under |
| `--display-name` | `digna` | Name shown in services.msc |
| `--description` | `digna data quality backend` | Description shown in services.msc |
| `--address` | `127.0.0.1` | Address the service binds its API to |
| `--port` | `8000` | Port the service binds its API to |
| `--working-dir` | the directory of the `digna` executable | Directory holding `config.toml` and `license.toml`, which the service makes its working directory |
| `--start-type` | `auto` | `auto` starts with Windows, `manual` starts only when asked, `disabled` registers the service but refuses to start it |
| `--account` | `LocalSystem` | Account to run as, e.g. `DOMAIN\user` or `.\user` |
| `--password` | | Password of `--account` |

!!! tip "Running under a domain account"

    `LocalSystem` has no network identity, so Windows Authentication against SQL Server and any
    access to a network share will fail. Install with `--account` and `--password` where the
    service needs to reach resources as a specific user.

### Starting and Stopping the Service

#### To Start the Service

```bash
digna windows start
```

#### To Stop the Service

```bash
digna windows stop
```

!!! tip "Tip"

    Always stop the service before updating application files.

### Moving the Service to a New Directory

If you need to relocate the digna installation:

1. **Stop and unregister the current service**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Move the Application Files**
   - Move the entire digna installation folder to the new location

3. **Register the service again from the new location**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Repeat any `--address`, `--port` or `--account` values you used the first time — the previous
   registration is gone.

4. **Start the Service**
   ```bash
   digna windows start
   ```

### Uninstalling the Service

1. **Stop the Running Service**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Unregister the Service**
   ```bash
   digna windows uninstall
   ```

The digna server is now unregistered as a Windows service.

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

### Upgrade Process

#### Step 1: Stop and Unregister the Old Service

If digna is running as a Windows service, stop it with the **batch files of your current
installation** — the `digna windows` commands belong to the new release and are not available
yet:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

Then unregister the service, again with the old batch file. The registration points at the old
executable and its scripts, both of which this upgrade replaces, so it cannot be reused:

```bash
uninstall_service.bat
```

!!! warning "Unregister before you rename anything"

    `uninstall_service.bat` lives in the `bin` folder you are about to rename, and it is the only
    thing that can remove the registration it created. Run it while the old installation is still
    in place. If the folder has already been renamed, rename it back, unregister, then continue.

    Note down the account the service ran under, and the address and port it served on — you will
    need them in Step 7.

#### Step 2: Backup Current Installation

In your digna installation directory, rename the folders of your current installation so that the new release can be deployed alongside them:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend and dignacli are no longer used"

    Starting with Release 2026.06, `dignabackend` and `dignacli` are replaced by the single `digna` executable, which combines the backend and the CLI. Keep `dignabackend_old` and `dignacli_old` only until you have verified the upgrade — afterwards you can delete both folders. Keep `dashboard_old` until you have restored your configuration files from it (see Step 4). The `bin` folder goes too: its batch files drove the old service and 2026.06 does not ship them, so once the service has been unregistered in Step 1 they do nothing but mislead.

#### Step 3: Extract and Deploy New Version

1. Extract the new digna installation ZIP file
2. Copy the new `digna` executable, `dashboard` folder to your installation directory


!!! warning "Important"

    The `config.toml` file is **never** included in the installation ZIP. Your existing configuration remains safe.

#### Step 4: Restore Your Configuration Files

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
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

#### Step 5: Validate the Configuration

Confirm that the updated `config.toml` is complete before touching the repository:

```bash
digna config check
```

Every section must report OK. Fix anything reported as FAILED and run the command again before continuing.

#### Step 6: Upgrade the Repository Schema

Navigate to your digna installation directory and run:

```bash
digna repo upgrade
```

This updates the PostgreSQL schema to the latest version while preserving all existing data.

#### Step 7: Register and Start the Service

The old registration was removed in Step 1, so the service is registered again — this time with
the `digna` executable, which has no batch files:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Give `--address` and `--port` the values the old service served on, unless you want the new
defaults of `127.0.0.1` and `8000`; they are recorded in the registration and are no longer read
from `config.toml`. Add `--account` and `--password` if the old service ran under a domain
account. See
[Running digna as a Windows Service](#running-digna-as-a-windows-service) for the full option
list.

If running manually, restart the server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

If using IIS or Tomcat, restart the respective web server.

#### Step 8: Verify the Upgrade

1. Access the digna dashboard
2. Verify that the interface loads correctly
3. Check the server logs for any errors
4. Change every connection that did not already use ODBC over to ODBC, then test all connections
   — see [Testing a Connection](../../../databases/overview.md#testing-a-connection)




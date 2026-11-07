---
title: Windows Installation Guide – digna Release 2026.11 | digna Documentation
description: Step-by-step guide to installing digna Release 2026.11 on Windows — system requirements, PostgreSQL setup, web server configuration, backend and dashboard configuration, running digna as a Windows service, and upgrading from Release 2026.06.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Windows Installation Guide for digna Release 2026.11

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
9. [Running digna as a Windows Service](#running-digna-as-a-windows-service)
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

### Looking for macOS or Linux?

This guide covers Windows. For other platforms, see the [macOS Installation Guide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) or the [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! warning "Keep the log directory when running as a service"

    A Windows service has no console, so the log files are the only record of what the service
    does. Do not set `DIGNA_LOGGING_DIR` to an empty string, which switches the log files off.

#### [duckdb] Section (Optional) {: #duckdb-section }

New in Release 2026.11. This section sets the resources of the **digna Engine**, which profiles
data inside digna for database connections whose profiling location is **digna Engine**, and
runs referential integrity checks between data sources on different database connections. See
[Profiling Location](../../../platform/profiling/profiling_location.md).

The section is optional. Without it, the defaults below apply.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (default) | Memory, in MB, that one digna Engine run may use. Up to `DIGNA_MAX_WORKERS` runs can be active at the same time |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Default: the temporary directory of the account that runs digna (`%TEMP%`) | Directory for temporary files when the data does not fit into memory |

!!! tip "Sizing the digna Engine"

    Plan for up to `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` of memory on the digna
    host, on top of what digna itself uses, and for enough free disk space in the temporary
    directory to hold the largest inspected date of the data sources that use the digna Engine.
    Point `DIGNA_DUCKDB_TEMP_DIRECTORY` at a disk with that space, writable by the account that
    runs digna:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    You only need this section if at least one database connection uses the digna Engine, or a
    referential integrity check compares data sources on different connections.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Fix anything reported as FAILED and run the command again before continuing. A WARNING under **Unknown keys** lists keys in `config.toml` that digna does not read; they have no effect, so remove them or correct their spelling. See the [CLI reference](../../../cli/Command_Line_Interface_202611.md) for the full list of options.

### Step 3: Initialize the Repository

1. Open Command Prompt
2. Navigate to your digna installation directory (where `config.toml` and the `digna` executable are located)
3. Run the connection test:

```bash
digna repo check
```

On a new schema, the command connects and then reports that no repository is installed yet:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

At this point that is the expected result: it confirms that digna reaches PostgreSQL and the schema. A connection or authentication error instead points at the `[repo]` section or at the PostgreSQL setup.

### Step 4: Install the Repository Schema

In the same directory, run:

```bash
digna repo upgrade
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
- `--address` — Server hostname/IP (default `127.0.0.1`)
- `--port` — Server port (default `8000`)

When the server is up, it prints the address it listens on:

```text
Server running on http://127.0.0.1:8082
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
option list is in the [CLI reference](../../../cli/Command_Line_Interface_202611.md).

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

This section upgrades an installation of Release 2026.06 to Release 2026.11. If your
installation is older, read [Upgrading From a Release Before 2026.06](#upgrading-from-a-release-before-2026-06)
first.

### Before You Upgrade

**Creating a digna Repository Backup is Mandatory**

Before upgrading digna, back up your repository (PostgreSQL) to protect against data loss.
A backup ensures you can recover if the upgrade encounters unexpected issues.

**Requesting the License File for Release 2026.11**

Release 2026.11 needs a new `license.toml`. Request it from the digna team before you start, and
have it ready for [Step 7](#step-7-replace-the-license-file).

### Upgrading From a Release Before 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 brought three changes that still apply when you upgrade an older installation
straight to 2026.11:

- **ODBC only.** digna reaches every source technology over ODBC. Every database connection that
  does not use ODBC yet must be changed to ODBC after the upgrade; there is no automatic
  conversion. Install the ODBC drivers on the digna host beforehand, see
  [Install the ODBC Driver on the digna Host](../../../databases/overview.md#install-the-driver),
  and have the properties of each connection ready from the
  [technology guides](../../../databases/overview.md#technology-guides). The Databricks Legacy
  connector no longer exists; move those connections to the
  [Databricks](../../../databases/databricks_connector_guide.md) connector.
- **One executable.** `dignabackend` and `dignacli` are replaced by the single `digna` executable,
  which combines the backend and the CLI.
- **config.toml.** The `[encryption]` section is required, and `DIGNA_APP_HOST` and
  `DIGNA_APP_PORT` are no longer read: the server takes its address and port from `digna serve`.
  Compare your file with [Backend Configuration](#backend-configuration).

The steps below point out where an older installation needs something different. The repository
upgrade in Step 8 brings a repository of any earlier release straight to 2026.11.

### Upgrade Process

#### Step 1: Stop the digna Service {: #step-1-stop-the-digna-service }

Open a Command Prompt as Administrator and stop the service with the `digna` executable of
your current installation:

```bash
cd C:\path\to\digna
digna windows stop
```

The service stays registered. The new executable takes the place of the old one in the same
directory, so the registration keeps pointing at the right file.

If digna is running in the foreground, press ++ctrl+c++ in its Command Prompt window.

!!! warning "Upgrading from a release before 2026.06"

    Releases before 2026.06 registered the service with batch files. Stop and unregister it with
    the batch files of your current installation, **before** you rename anything in Step 2:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    Note down the account the service ran under, and the address and port it served on. You will
    register the service again in Step 9.

#### Step 2: Backup Current Installation {: #step-2-backup-current-installation }

In your digna installation directory, rename the executable and the dashboard folder of your
current installation, so that the new release can be deployed alongside them:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Keep `digna_old` until you have verified the upgrade, and `dashboard_old` until you have restored
your configuration files from it (see Step 4). Afterwards you can delete both.

!!! info "Upgrading from a release before 2026.06"

    Rename the `dignabackend` and `dignacli` folders instead of the executable:
    `ren dignabackend dignabackend_old` and `ren dignacli dignacli_old`; the `bin` folder of batch files is no longer used either. Neither is used by Release 2026.11.

#### Step 3: Extract and Deploy New Version {: #step-3-extract-and-deploy-new-version }

1. Extract the new digna installation ZIP file
2. Copy the new `digna` executable and `dashboard` folder to your installation directory

!!! warning "Important"

    Neither `config.toml` nor `dashboard/dashboard_config.toml` is ever included in the
    installation ZIP — the digna team never ships either file. Your existing configuration is
    therefore untouched by the upgrade, and the copies in the renamed `*_old` folders are the
    only ones you have.

#### Step 4: Restore Your Configuration Files {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
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
digna config check
```

Every section must report OK. Fix anything reported as FAILED, remove the keys listed under
**Unknown keys**, and run the command again before continuing.

#### Step 7: Replace the License File {: #step-7-replace-the-license-file }

A license file normally carries over from one release to the next. Release 2026.11 is an
exception: it adds two licensed modules, digna Data Reconciliation and digna Agentic, and a
license issued before 2026.11 does not contain them. Copy the `license.toml` that the digna team
provided for Release 2026.11 into the installation directory, replacing the old one:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Do not keep the previous license"

    With the previous license, digna still starts, but digna Data Reconciliation and the digna
    MCP Server stay switched off. Every command that checks the license — `user`,
    `inspection`, `repo` — aborts before touching the repository when the check fails. Verify
    the new license before going further:

    ```bash
    digna license check
    ```

#### Step 8: Upgrade the Repository Schema {: #step-8-upgrade-the-repository-schema }

In your digna installation directory, run:

```bash
digna repo upgrade
```

Release 2026.11 manages the repository schema with versioned migrations. The first upgrade from
an earlier release brings the schema to the last version of the previous scheme, records that as
its starting point, and then applies the migrations of Release 2026.11. It finishes with:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

All existing data is preserved. To see the state of the repository at any time, run
`digna repo check`: it lists the latest applied migration and any pending ones.

!!! warning "digna does not start on an outdated repository"

    From Release 2026.11, the server refuses to start while the repository needs an upgrade, and
    says so, for example:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Run `repo upgrade` before you start the server or the service.

#### Step 9: Restart Services {: #step-9-restart-services }

If digna runs as a Windows service, start it again:

```bash
cd C:\path\to\digna
digna windows start
```

If you upgraded from a release before 2026.06 and unregistered the service in Step 1, register
it again with the `digna` executable first:

```bash
digna windows install --address <address> --port <port>
digna windows start
```

Give `--address` and `--port` the values the old service served on, unless you want the
defaults of `127.0.0.1` and `8000`. Add `--account` and `--password` if the old service ran
under a domain account. See
[Running digna as a Windows Service](#running-digna-as-a-windows-service) for the full option
list.

If running manually, restart the server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

If using IIS or Tomcat, restart the respective web server.

#### Step 10: Verify the Upgrade {: #step-10-verify-the-upgrade }

1. Confirm the release of the new executable:

    ```bash
    digna version
    ```

    The first line must read `Release: 2026.11`.

2. Access the digna dashboard and verify that the interface loads correctly.
3. Check the files in the `logs` directory of the installation for errors.
4. Test your database connections — see
   [Testing a Connection](../../../databases/overview.md#testing-a-connection). After an upgrade
   from a release before 2026.06, change every connection that did not already use ODBC over to
   ODBC first.

To start with the new modules, see [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Connect an AI Agent](../../../platform/agentic/connect_ai_agent.md) for the digna MCP Server, and
[Profiling Location](../../../platform/profiling/profiling_location.md) for the digna Engine.

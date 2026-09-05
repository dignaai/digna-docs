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

- **dignabackend**: The core engine of the application, responsible for processing data and performing quality checks.
- **dignadashboard**: A web-based interface hosted on a web server, providing a user-friendly way to interact with the digna platform and visualize data quality metrics.

### What's New in Release 2026.06

This release brings data observability capabilities directly into your code, enabling developers to monitor data quality at the source. See the [release notes](http://docs.digna.ai/changelog/Release_202606/) for complete details.

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
   - `config.toml` — Configuration file
   - `license.toml` — License file (copy yours here)

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

### Step 5: Start the digna Server

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

### Step 6: Create an Admin User

1. Open a **new** Command Prompt window
2. Navigate to your digna installation directory
3. Run the following command to create an admin user:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Example:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

This creates a user with full administrative privileges.

!!! tip "Best Practice"

    Use a strong password with a mix of uppercase, lowercase, numbers, and special characters.

---

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

The digna dashboard has its own separate `config.toml` file located in the `dashboard/` directory. This configuration is already provided and does not require changes during initial setup. You only need to configure it if you need to customize the backend connection.

If you need to modify the dashboard configuration (e.g., for multi-instance deployments), refer to the dashboard's documentation.

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

### Service Management Files

All necessary files are located in the digna installation directory under: `bin/`

The following batch files are available:
- `install_service.bat` — Registers digna as a Windows service
- `uninstall_service.bat` — Unregisters the service
- `start_service.bat` — Starts the running service
- `stop_service.bat` — Stops the running service

!!! warning "Administrator Required"

    All batch files must be executed with Administrator privileges.

### Installing the Service

1. **Open Command Prompt as Administrator**
   - Right-click Command Prompt
   - Select "Run as Administrator"

2. **Navigate to the bin Folder**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Run the Installation Script**
   ```bash
   install_service.bat
   ```

The digna server is now registered as a Windows service with **automatic startup** enabled. The service does not start immediately — see the next section to start it.

### Starting and Stopping the Service

#### To Start the Service

1. Open Command Prompt as Administrator
2. Navigate to `digna\bin`
3. Run:
   ```bash
   start_service.bat
   ```

#### To Stop the Service

1. Open Command Prompt as Administrator
2. Navigate to `digna\bin`
3. Run:
   ```bash
   stop_service.bat
   ```

!!! tip "Tip"

    Always stop the service before updating application files.

### Moving the Service to a New Directory

If you need to relocate the digna installation:

1. **Uninstall the Current Service**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Move the Application Files**
   - Move the entire digna installation folder to the new location

3. **Reinstall the Service**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Start the Service**
   ```bash
   start_service.bat
   ```

### Uninstalling the Service

1. **Stop the Running Service**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Uninstall the Service**
   ```bash
   uninstall_service.bat
   ```

The digna server is now unregistered as a Windows service.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Before You Upgrade

**Creating a digna Repository Backup is Mandatory**

Before upgrading digna, back up your repository (PostgreSQL) to protect against data loss.
A backup ensures you can recover if the upgrade encounters unexpected issues.

### Upgrade Process

#### Step 1: Stop digna Service

If digna is running as a Windows service, stop it first:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Step 2: Backup Current Backend Installation

In your digna installation directory:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Step 3: Extract and Deploy New Version

1. Extract the new digna installation ZIP file
2. Copy the new `digna` executable, `dashboard` folder to your installation directory


!!! warning "Important"

    The `config.toml` file is **never** included in the installation ZIP. Your existing configuration remains safe.

### Step 4: Restore Your Configuration Files

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Step 5: Upgrade the Repository Schema

Navigate to your digna installation directory and run:

```bash
digna repo upgrade
```

This updates the PostgreSQL schema to the latest version while preserving all existing data.

### Step 6: Restart Services

If running as a Windows service:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

If running manually, restart the server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

If using IIS or Tomcat, restart the respective web server.

#### Step 7: Verify the Upgrade

1. Access the digna dashboard
2. Verify that the interface loads correctly
3. Check the server logs for any errors




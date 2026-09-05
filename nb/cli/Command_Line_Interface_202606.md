# digna CLI Reference 2026.06
**2026-09-05**

This page documents the full set of commands available in ***digna*** CLI release **2026.06**, including usage examples and options.

---

## CLI Basics

---

### Overview & Syntax

The release **2026.06** CLI uses a structured, category-based command hierarchy:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

### Global Options

The following global options apply across all commands:

- `--help`, `-h`: Display help information for the CLI or specific subcommands.
- `--version`, `-V`: Print version information.
- `--stacktrace`: Display full stack trace on error.

### help
The `--help` option provides information about available command categories, subcommands, and options:

1. **Displaying General Help:**
   ```bash
   digna --help
   ```

2. **Getting Help for Specific Categories and Commands:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Output Includes:**
   - **Command Description:** Summary of the command purpose.
   - **Syntax:** Required and optional arguments.
   - **Options:** Flags and parameters specific to the command.

### version

To check the installed version of ***digna*** CLI:

#### Command Usage
```bash
digna --version
```

#### Example Output
```text
digna-rust 0.1.0 (Release 2026.06)
```

---

## Configuration Management

---

### config check

The `config check` command validates the configuration file (`config.toml`), verifying that all mandatory sections and settings (App, Repository, Base, Logging, Encryption, and OIDC) are present and properly formatted.

#### Command Usage
```bash
digna config check [OPTIONS]
```

#### Options
- `--configpath`, `-c`: Path to the configuration file or directory containing `config.toml` (defaults to `./config.toml`).
- `--json`: Output the validation report in JSON format.
- `--quiet`, `-q`: Suppress stdout output and rely solely on the exit code (0 for success, 1 for invalid config).

#### Example
```bash
digna config check
```

Validate a specific configuration file and format output as JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

---

## Repository Management

---

### repo check

The `repo check` command tests the database connection and verifies repository installation and version.

#### Command Usage
```bash
digna repo check
```

#### Example Output
```text
Repo version 2026.06 installed
```

### repo install

The `repo install` command initializes and installs a new ***digna*** repository schema, creating all required tables, sequences, and initial metadata.

#### Command Usage
```bash
digna repo install
```

### repo upgrade

The `repo upgrade` command applies database schema updates to migrate an existing repository to the latest version.

#### Command Usage
```bash
digna repo upgrade [OPTIONS]
```

#### Options
- `--simulation-mode`, `-s`: Run in simulation mode (dry-run). Prints SQL statements without executing them.

#### Example
```bash
digna repo upgrade
```

To preview pending SQL migrations without applying changes:
```bash
digna repo upgrade --simulation-mode
```

---

## Encryption Management

---

### crypt gen-key

The `crypt gen-key` command generates a new AES-GCM encryption key.

#### Command Usage
```bash
digna crypt gen-key
```

### crypt encrypt

The `crypt encrypt` command encrypts a string (such as a database password) using the AES-GCM key configured in `config.toml`.

#### Command Usage
```bash
digna crypt encrypt <VALUE>
```

#### Arguments
- **VALUE**: The plaintext string to encrypt (required).

#### Example
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

The `crypt decrypt` command decrypts an AES-GCM encrypted string using the key configured in `config.toml`.

#### Command Usage
```bash
digna crypt decrypt <VALUE>
```

#### Arguments
- **VALUE**: The encrypted ciphertext string to decrypt (required).

#### Example
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## User Management

---

### user add

The `user add` command creates a new user account in the ***digna*** repository.

#### Command Usage
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Arguments
- **EMAIL**: The email address for the user (required).
- **PASSWORD**: The initial password for the user (required).
- **DISPLAY_NAME**: The full display name of the user (required).

#### Options
- `--admin`, `-a`: Flag to designate the user as an administrator/superuser.

#### Example
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

To create an administrator account:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

### user list

The `user list` command lists all registered users in tabular format with ID, email, display name, and admin privileges.

#### Command Usage
```bash
digna user list
```

### user modify

The `user modify` command updates the display name or administrative privileges of an existing user account.

#### Command Usage
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Arguments
- **EMAIL**: The email of the user to modify (required).
- **DISPLAY_NAME**: The updated display name (required).

#### Options
- `--admin`, `-a`: Grant or revoke administrator privileges.
- `--valid_until`, `-v`: Set account validity expiration timestamp.

#### Example
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

### user modify-pwd

The `user modify-pwd` command updates the password for an existing user account.

#### Command Usage
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Arguments
- **EMAIL**: The email of the user whose password is to be updated (required).
- **PASSWORD**: The new password (required).

#### Example
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

The `user delete` command removes a user account from the system.

#### Command Usage
```bash
digna user delete <EMAIL>
```

#### Arguments
- **EMAIL**: The email of the user to delete (required).

#### Example
```bash
digna user delete jdoe@example.com
```

---

## Project & Data Source Management

---

### project list

The `project list` command lists all available projects in the repository, showing their ID, name, and description.

#### Command Usage
```bash
digna project list
```

### project list-ds

The `project list-ds` command lists all data sources associated with a given project, displaying their ID, name, kind, schema, and table name.

#### Command Usage
```bash
digna project list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME**: The name of the project whose data sources should be listed (required).

#### Example
```bash
digna project list-ds ProjectA
```

### project export-ds

The `project export-ds` command exports data sources from a project into a JSON document.

#### Command Usage
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME**: The name of the project to export data sources from (required).

#### Options
- `--table-name`, `-n`: Specific table names to export (multiple names can be provided separated by spaces).
- `--table-id`, `-i`: Specific table IDs to export (multiple IDs can be provided separated by spaces).
- `--exportfile`, `-f`: Path to save exported data sources (default: `data_sources_export.json`).

#### Example
To export all data sources from `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

To export specific tables:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

### project import-ds

The `project import-ds` command imports data sources from an export file into a target project.

#### Command Usage
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME**: Target project name to import into (required).
- **EXPORT_FILE**: Path to the JSON export file (required).

#### Options
- `--output-file`, `-o`: File to save the import report.
- `--output-format`, `-f`: Format of the import report (`table`, `json`, `csv`; default: `table`).

#### Example
```bash
digna project import-ds ProjectB my_export.json
```

### project plan-import-ds

The `project plan-import-ds` command previews a data source import into a target project, displaying which data sources would be imported and which would be skipped.

#### Command Usage
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME**: Target project name (required).
- **EXPORT_FILE**: Path to the export file (required).

#### Options
- `--output-file`, `-o`: File to save the import plan report.
- `--output-format`, `-f`: Format of the import report (`table`, `json`, `csv`; default: `table`).

#### Example
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Inspection Management

---

### inspection run

The `inspection run` command executes or schedules an inspection for a project and date range.

#### Command Usage
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME**: The target project name (required).
- **START_DATE**: Start date of the date range in `YYYY-MM-DD` format (required).
- **END_DATE**: End date of the date range in `YYYY-MM-DD` format (required).

#### Options
- `--table-name`: Limit inspection to a specific table.
- `--async-mode`: Submit inspection asynchronously and return the generated request ID immediately.
- `--bypass-backend`: Bypass backend scheduling and run inspection directly within the CLI.

#### Example
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

To submit an asynchronous inspection:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

To inspect a single table:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

### inspection status

The `inspection status` command queries the execution progress and state of an inspection request by its request ID.

#### Command Usage
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Arguments
- **INSPECTION_REQUEST_ID**: The numerical inspection request ID (required).

#### Example
```bash
digna inspection status 1024
```

### inspection abort

The `inspection abort` command cancels ongoing or pending inspection requests.

#### Command Usage
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Arguments
- **INSPECTION_REQUEST_ID**: The inspection request ID to abort (optional when `--killall` is specified).

#### Options
- `--killall`: Abort all currently running and pending inspection requests.

#### Example
To abort a specific request:
```bash
digna inspection abort 1024
```

To abort all active and queued inspections:
```bash
digna inspection abort --killall
```

---

## License Management

---

### license check

The `license check` command validates the current `license.toml` against the public key stored in the system.

#### Command Usage
```bash
digna license check
```

---

## Server & Background Services

---

### serve

The `serve` command launches the ***digna*** REST API server along with the background inspection scheduler and manager.

#### Command Usage
```bash
digna serve [OPTIONS]
```

#### Options
- `--address`: Network address to bind the API server to (default: `127.0.0.1`).
- `--port`: Port number to listen on (default: `8000`).

#### Example
```bash
digna serve --address 0.0.0.0 --port 8000
```
# digna CLI Reference 2026.06
**2026-09-05**

This page documents the full set of commands available in ***digna*** CLI release **2026.06**, including usage examples and options.

The executable is called `digna`.

---

## CLI Basics

---

### Overview & Syntax

The release **2026.06** CLI uses a structured, category-based command hierarchy:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` and `serve` are single commands without a subcommand:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Global Options

The following global options apply across all commands:

- `--help`, `-h`: Display help information for the CLI or a specific command category or subcommand.
- `--stacktrace`: Display the full error chain on failure instead of only the top-level message.

`--stacktrace` is a global option in the strict sense: it has to be given **before** the command
category, not after it.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

There is no `--version` flag. Use the [`version`](#version) command instead.

### Prerequisites

Most commands need a readable, valid `config.toml`; some additionally require a valid license.
The following table records what each command category loads before it does anything:

| Command category | Needs `config.toml` | Needs a valid license |
|---|---|---|
| `version` | no | no |
| `config check` | no (it is what the command reports on) | no |
| `license check` | no | it *is* the check |
| `crypt` | yes | no |
| `serve` | yes | no |
| `project` | yes | no |
| `user` | yes | yes |
| `inspection` | yes | yes |
| `repo` | yes | yes |

Where a license is required, both its signature and its expiry date are checked, and the command
aborts before touching the repository if either fails.

### Exit Codes

- `0`: the command succeeded.
- `1`: the command failed. The error message is written to stderr, prefixed with `Error: `.

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

The `version` command prints the installed ***digna*** release. It reads no configuration and
validates no license, so it also works on an installation whose `config.toml` or license is
missing or invalid.

The release version is independent of the repository schema version reported by
[`repo check`](#repo-check).

#### Command Usage
```bash
digna version
```

#### Example Output
```text
2026.06
```

---

## Configuration Management

---

### config check

The `config check` command validates the configuration file (`config.toml`), verifying that all
mandatory sections and settings are present and properly formatted. Each section is validated on
its own, so a broken `[app]` section does not hide the state of `[repo]`.

The sections reported are:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — optional; an absent key passes, a present but malformed list fails

The command deliberately does not load the application configuration the way the other commands
do, so it can diagnose a `config.toml` that would stop ***digna*** from starting at all.

#### Command Usage
```bash
digna config check [OPTIONS]
```

#### Options
- `--configpath`, `-c`: Path to the configuration file, or to a directory containing `config.toml` (defaults to `./config.toml`).
- `--json`: Output the validation report as JSON. Takes precedence over `--quiet`.
- `--quiet`, `-q`: Suppress the report and rely solely on the exit code.

#### Example
```bash
digna config check
```

Validate a specific configuration file and format output as JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Example Output
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

A missing file or a TOML syntax error leaves nothing to validate section by section and is
reported as a single error instead of a report, regardless of `--quiet` or `--json`.

---

## Repository Management

---

### repo check

The `repo check` command tests the database connection and verifies repository installation and
version. It fails if the configured schema does not exist, or if it exists but holds no ***digna***
repository.

The version reported is the version of the repository schema, which is versioned separately from
the ***digna*** release printed by [`version`](#version).

#### Command Usage
```bash
digna repo check
```

#### Example Output
```text
Repo version 3.0.0 installed
```

### repo install

The `repo install` command installs a new ***digna*** repository into the schema configured in
`config.toml`, creating all required sequences, tables, indices, constraints, and initial records.

The schema itself is **not** created by this command — it has to exist beforehand. The command also
refuses to run if a repository is already installed in that schema, and points at
[`repo upgrade`](#repo-upgrade) if the installed version is an older one.

#### Command Usage
```bash
digna repo install
```

#### Example Output
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

The `repo upgrade` command applies database schema migrations to bring an existing repository up to
the version expected by the installed release. Upgrades are applied one version hop at a time along
a fixed upgrade path, and each completed hop is recorded in the repository.

If the repository is already at the expected version, the command reports that no upgrade is needed
and makes no changes.

#### Command Usage
```bash
digna repo upgrade
```

#### Example Output
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Encryption Management

---

### crypt gen-key

The `crypt gen-key` command generates a new AES-GCM encryption key, for use as the encryption key
in `config.toml`. A loadable `config.toml` must already be present, even though the generated key
does not depend on it.

#### Command Usage
```bash
digna crypt gen-key
```

#### Example Output
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

The `crypt encrypt` command encrypts a string (such as a database password) using the AES-GCM key
configured in `config.toml`, and prints the ciphertext.

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

The `crypt decrypt` command decrypts an AES-GCM encrypted string using the key configured in
`config.toml`, and prints the plaintext.

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

The `user add` command creates a new user account in the ***digna*** repository. The command fails
if a user with the given email address already exists.

#### Command Usage
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Arguments
- **EMAIL**: The email address for the user (required).
- **PASSWORD**: The initial password for the user (required).
- **DISPLAY_NAME**: The full display name of the user (required).

#### Options
- `--admin`, `-a`: Create the user with administrator (superuser) privileges.

#### Example
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

To create an administrator account:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Example Output
```text
User created with ID: 42
```

### user list

The `user list` command lists all registered users in tabular format with ID, email, display name,
and administrator flag.

#### Command Usage
```bash
digna user list
```

#### Example Output
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

The `user modify` command updates the display name and administrator privileges of an existing user
account, identified by email address.

Both the display name and the administrator flag are always written. `--admin` is a switch, not a
value: **omitting it revokes administrator privileges**, so pass it whenever the user should keep
or gain them.

#### Command Usage
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Arguments
- **EMAIL**: The email of the user to modify (required).
- **DISPLAY_NAME**: The updated display name (required).

#### Options
- `--admin`, `-a`: Grant administrator privileges. Omit to revoke them.
- `--valid-until`, `-v`: Accepted for compatibility but **not currently applied**. Passing it prints a warning and changes nothing.

#### Example
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Example Output
```text
User jdoe@example.com modified successfully
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

The `project list` command lists all available projects in the repository, showing their ID, name,
and description.

#### Command Usage
```bash
digna project list
```

#### Example Output
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

The `project list-ds` command lists all data sources associated with a given project, displaying
their ID, name, kind, schema, and table name.

#### Command Usage
```bash
digna project list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME**: The name of the project whose data sources should be listed (required). The name must match exactly.

#### Example
```bash
digna project list-ds ProjectA
```

#### Example Output
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

The `project export-ds` command exports data sources from a project into a JSON document.

If neither `--table-name` nor `--table-id` is given, all data sources of the project are exported.

#### Command Usage
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME**: The name of the project to export data sources from (required).

#### Options
- `--table-name`, `-n`: Data source names to export. Multiple names can be given separated by spaces.
- `--table-id`, `-i`: Data source IDs to export. Multiple IDs can be given separated by spaces.
- `--exportfile`, `-f`: Path to save the exported data sources to (default: `data_sources_export.json`).

#### Example
To export all data sources from `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

To export specific tables:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Example Output
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

The `project import-ds` command imports data sources from an export file into a target project, and
reports per object what was created, updated, or skipped.

#### Command Usage
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME**: Target project name to import into (required).
- **EXPORT_FILE**: Path to the JSON export file (required).

#### Options
- `--output-file`, `-o`: File to write the import report to. Without it, the report goes to stdout.
- `--output-format`, `-f`: Format of the import report — `table`, `json`, or `csv` (default: `table`).

#### Example
```bash
digna project import-ds ProjectB my_export.json
```

To capture a machine-readable report:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

The report covers four object levels — data source, data set definition, attribute, and validation
rule — each with its import action, result, resulting object ID, and any additional information.

### project plan-import-ds

The `project plan-import-ds` command previews a data source import into a target project, showing
which objects would be created, updated, or skipped, without changing anything. It takes the same
export file and the same reporting options as [`project import-ds`](#project-import-ds), and adds a
step number per planned object.

#### Command Usage
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME**: Target project name (required).
- **EXPORT_FILE**: Path to the export file (required).

#### Options
- `--output-file`, `-o`: File to write the import plan to. Without it, the plan goes to stdout.
- `--output-format`, `-f`: Format of the import plan — `table`, `json`, or `csv` (default: `table`).

#### Example
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Inspection Management

---

### inspection run

The `inspection run` command creates an inspection request for a project and a date range, and then
— depending on the options given — either waits for it, returns immediately, or runs it in-process.

The three execution modes are:

- **Default (no flag)**: the request is queued for the backend, and the CLI polls it every two seconds, printing task progress until the inspection reaches a final state. A running `digna serve` is required, otherwise nothing picks the request up.
- **`--async-mode`**: the request is queued and its ID is printed immediately. Use [`inspection status`](#inspection-status) to follow it.
- **`--bypass-backend`**: the inspection is executed by the CLI process itself and is not queued, so no running server is needed.

`--async-mode` and `--bypass-backend` are mutually exclusive.

In every mode the command ends with a non-zero exit code if the inspection did not complete
successfully.

#### Command Usage
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME**: The target project name (required). The name must match exactly.
- **START_DATE**: Start date of the date range in `YYYY-MM-DD` format (required).
- **END_DATE**: End date of the date range in `YYYY-MM-DD` format (required).

#### Options
- `--table-name`: Restrict the inspection to a single data source of the project, given by its data source name. Without it, all data sources of the project are inspected.
- `--async-mode`: Queue the inspection and print the request ID instead of waiting for it. Cannot be combined with `--bypass-backend`.
- `--bypass-backend`: Run the inspection directly in the CLI process instead of queueing it for the backend. Cannot be combined with `--async-mode`.

#### Example
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

To submit an asynchronous inspection:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

To inspect a single data source:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Example Output
Default mode:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asynchronous mode:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

The `inspection status` command queries the state and task progress of an inspection request by its
request ID.

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

#### Example Output
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

The `inspection abort` command requests cancellation of running or pending inspection requests. It
records a stop event for each affected request; the backend acts on it, so an abort is a request to
stop rather than an immediate kill.

#### Command Usage
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Arguments
- **INSPECTION_REQUEST_ID**: The inspection request ID to abort. Required unless `--killall` is given.

#### Options
- `--killall`: Abort all currently running and pending inspection requests. Takes precedence over a request ID given alongside it.

#### Example
To abort a specific request:
```bash
digna inspection abort 1024
```

To abort all active and queued inspections:
```bash
digna inspection abort --killall
```

#### Example Output
`--killall` reports what it did; aborting a single request produces no output and reports success
through its exit code.
```text
All running and pending inspections have been aborted.
```

---

## License Management

---

### license check

The `license check` command validates `license.toml`, verifying its signature against the public
key shipped with the installation and checking that it has not expired. It reads no application
configuration, so it also works before `config.toml` is set up.

#### Command Usage
```bash
digna license check
```

#### Example Output
```text
License is valid
```

An invalid signature and an expired license are reported as distinct errors, both with exit code 1.

---

## Server & Background Services

---

### serve

The `serve` command launches the ***digna*** REST API server along with the background inspection
scheduler and inspection manager. At startup it also fails any inspection the repository still
records as running, since nothing can have survived from an earlier process.

The command runs in the foreground until it is stopped.

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

#### Example Output
```text
Server running on http://0.0.0.0:8000
```
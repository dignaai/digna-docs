---
title: digna CLI Reference 2026.04 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2026.04
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202604/
image: /assets/logo_square.png
---

# digna CLI Reference 2026.04
**2026-04-08**

This page documents the full set of commands available in ***digna*** CLI release **2026.01**, including usage examples and options.

---

## CLI Basics

---

### help
The `--help` option provides information about available commands and their usage. There are two main ways to use this option:

1. **Displaying General Help:**
   
    Use –help immediate after the keyword ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Getting Help for Specific Commands:**  
  
    For detailed information about a specific command, append `--help` to that command.
    For example, to obtain help with the `add-user` command, run:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Command Description:** Offers a detailed description of what the command does.  
     - **Syntax:** Shows the exact syntax, including required and optional arguments.  
     - **Options:** Lists any options specific to the command, along with their explanations.  
     - **Examples:** Provides examples of how to execute the command effectively.

### check-config

The check-config command is a utility within the ***digna*** CLI tool designed to test the configuration of ***digna***. This command ensures that the ***digna*** components can find the needed configuration elements in the config.toml.

#### Options

- `--configpath`, `-cp`: File or directory that contains the configuration. If omitted, ../config.toml will be used.
      
#### Command Usage
```bash
dignacli check-config
```

Upon successful execution, the command outputs a confirmation of completeness of the configration.  
  
If the configuration appears to be incomplete, the missing configuration elements will be listed.

  
### check-repo-connection

The check-repo-connection command is a utility within the ***digna*** CLI tool designed to test the connectivity and access to a specified ***digna*** repository. This command ensures that the CLI can interact with the repository.
      
#### Command Usage
```bash
dignacli check-repo-connection
```

Upon successful execution, the command outputs a confirmation of the connection, along with details about the repository: Repository version, Host, Database and Schema.  
  
If the repository connection is not successful, check the config.toml file for correct configuration settings.


### version

To check the installed version of *dignacli*, use the --version option.  
  
#### Command Usage
```bash
dignacli --version
```
  
#### Example Output
```bash
dignacli version 2026.01
```

### logging options
  
By default, the console output of the ***digna*** commands is designed to be minimalistic. Most commands offer the possibility of providing additional information, using the following options:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” and “debug” are defining the level of detail, whereas the “logfile” switch allows redirecting the output to be streamed to a file rather than the console window.

## User Management

### add-user
  
The add-user command in the ***digna*** CLI is used to add a new user to the ***digna*** system
  
#### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Arguments

- **USER_NAME**: The username for the new user (required).
- **USER_FULL_NAME**: The full name of the new user (required).
- **USER_PASSWORD**: The password for the new user (required).

#### Options

- `--is_superuser`, `-su`: Flag to designate the new user as an admin.
- `--valid_until`, `-vu`: Sets an expiration date for the user account in the format `YYYY-MM-DD HH:MI:SS`. If not set, the account does not have an expiration date.

#### Example

To add a new user with username `jdoe`, full name `John Doe`, and password `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
To add a new user and set an account expiration date:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
The `delete-user` command in the ***digna*** CLI is used to remove an existing user from the ***digna*** system.
  
#### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
#### Arguments
- **USER_NAME**: The username of the user to be deleted (required). This is the only argument required by the command.

#### Example
```bash
dignacli delete-user jdoe
```
  
Executing this command will remove the user `jdoe` from the ***digna*** system, revoking their access and deleting their associated data and permissions from the repository.

### modify-user

The `modify-user` command in the ***digna*** CLI is used to update the details of an existing user in the ***digna*** system.

#### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Arguments
  
- **USER_NAME**: The username of the user to be modified (required).
- **USER_FULL_NAME**: The new full name for the user (required).
  
#### Options  
  
- `--is_superuser`, `-su`: Sets the user as a superuser, granting elevated privileges. This flag does not require a value.  
- `--valid_until`, `-vu`: Sets an expiration date for the user account in the format YYYY-MM-DD HH:MI:SS. If not provided, the account remains valid indefinitely.  
  
#### Example
  
To modify the full name of the user `jdoe` to “Johnathan Doe” and set the user as a superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
The `modify-user-pwd` command in the ***digna*** CLI is used to change the password for an existing user in the ***digna*** system.
  
#### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Arguments
  
- **USER_NAME**: The username of the user whose password is to be changed (required).
- **USER_PWD**: The new password for the user (required).
  
#### Example
  
To change the password for the user `jdoe` to `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

The `list-users` command in the ***digna*** CLI displays a list of all users registered in the ***digna*** system.

#### Command Usage

```bash
dignacli list-users
```

Executing this command in the ***digna*** CLI will connect to the ***digna*** repository and list all users, showing their ID, username, full name, superuser status, and expiration timestamps.

## Repository Management

### upgrade-repo
  
The `upgrade-repo` command in the ***digna*** CLI is used to upgrade or initialize the ***digna*** repository. This command is essential for applying updates or setting up the repository infrastructure for the first time.
  
#### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: When enabled, this option runs the command in simulation mode, which prints the SQL statements that would be executed but does not actually execute them. This is useful for previewing changes without making any modifications to the repository.  

  
#### Example
  
To upgrade the ***digna*** repository, you can run the command without any options:
  
```bash
dignacli upgrade-repo
```  
To run the upgrade in simulation mode (to see the SQL statements without applying them):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
This command is crucial for maintaining the ***digna*** system, ensuring that the database schema and other repository components are up to date with the latest version of the software.

### encrypt
  
The `encrypt` command in the ***digna*** CLI is used to encrypt a password.
  
#### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Arguments
- **PASSWORD**: The password that needs to be encrypted (required).
  
#### Example
  
To encrypt a password, you need to provide the password as an argument.   
For instance, to encrypt the password `mypassword123`, you would use:
```bash
dignacli encrypt mypassword123
```
This command outputs the encrypted version of the provided password, which can then be used in secure contexts. If the password argument is not provided, the CLI will display an error indicating the missing argument.

### generate-key
  
The `generate-key` command is used to generate a Fernet key, which is essential for securing passwords stored in the ***digna*** repository.
  
#### Command Usage
```bash
dignacli generate-key
```
  
## Data Management

### clean-up

The `clean-up` command in the ***digna*** CLI is used to remove profiles, predictions, and traffic light system data for one or more data sources within a specified project. This command is essential for data lifecycle management, helping maintain an organized and efficient data environment by clearing outdated or unnecessary data.

#### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: The name of the project from which data is to be removed (required). Using the keyword all-projects in this argument instructs ***digna*** to iterate over all existing projects and apply this command.
- **FROM_DATE**: The start date and time for the data removal. Acceptable formats include %Y-%m-%d, %Y-%m-%dT%H:%M:%S, or %Y-%m-%d %H:%M:%S (required).
- **TO_DATE**: The end date and time for the data removal, following the same formats as FROM_DATE (required).
  
#### Options
  
- `--table-name`, `-tn`: Limits the clean-up operation to a specific table within the project.
- `--table-filter`, `-tf`: Filters to limit the clean-up to tables containing the specified substring in their names.
- `--timing`, `-tm`: Displays the time duration of the clean-up process after completion.
- `--help`: Displays help information for the clean-up command and exits.
  
#### Example
  
To remove data from the project ProjectA between January 1, 2023, and June 30, 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
To remove data only from a specific table named `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
This command helps in managing data storage and ensuring that the repository only contains relevant information.

### remove-orphans
  
The `remove-orphans` command in the ***digna*** CLI is used for house-keeping in the ***digna*** repository.  
When a user deletes projects or data sources, the profiles and predictions remain in the repository. With this command, such orphaned rows will be removed from the repository.
  
#### Command Usage
  
```bash
dignacli list-projects
```

### list-projects
  
The `list-projects` command in the ***digna*** CLI is used to display a list of all available projects within the ***digna*** system.
  
#### Command Usage
  
```bash
dignacli list-projects
```

This command is especially useful for administrators and users managing multiple projects, providing a quick overview of the available projects in the ***digna*** repository.

### list-ds

The `list-ds` command in the ***digna*** CLI is used to display a list of all available data sources within a specified project. This command is useful for understanding the data assets available for analysis and management in the ***digna*** system.

#### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME**: The name of the project for which the data sources are being listed (required).
  
#### Example
  
To list all data sources in the project named `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
This command provides users with an overview of the data sources available in a project, helping them to navigate and manage the data landscape more effectively.


### inspect

The `inspect` command in the ***digna*** CLI is used to create profiles, predictions, and traffic light system data for one or more data sources within a specified project. This command helps in analyzing and monitoring data over a defined period. After completion of the inspection, the value of the calculated traffic light system is returned:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: The name of the project for which data is to be inspected (required). Using the keyword all-projects in this argument instructs ***digna*** to iterate over all existing projects and apply this command.
- **FROM_DATE**: The starting date and time for the data inspection. Acceptable formats include %Y-%m-%d, %Y-%m-%dT%H:%M:%S, or %Y-%m-%d %H:%M:%S (required).
- **TO_DATE**: The ending date and time for the data inspection, following the same formats as FROM_DATE (required).
  
#### Options

- `--table-name`, `-tn`: Limits the inspection to a specific table within the project.
- `--table-filter`, `-tf`: Filters to inspect only tables containing the specified substring in their names.
- `--enable_notification`, `-en`: Enables the sending of notifications in case of alerts.
- `--bypass-backend`, `-bb`: Bypass backend and run inspection directly from CLI (for testing purposes only!).

  
#### Example
  
To inspect data for the project `ProjectA` from January 1, 2024, to January 31, 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
To inspect only a specific table and force recalculation of predictions:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
This command is useful for generating updated profiles and predictions, monitoring data integrity, and managing alert systems within a specified project timeframe.

### inspect-async

The `inspect-async` command in the ***digna*** CLI is used to create profiles, predictions, and traffic light system data for one or more data sources within a specified project. This command helps in analyzing and monitoring data over a defined period. In contrast to the `inspect-async` command, this does not wait for the completion of the inspection.
Instead, it returns the request id for the submitted inspection request. To query the progress of the inspection process, use the command `inspect-status`

#### Command Usage

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: The name of the project for which data is to be inspected (required). Using the keyword all-projects in this argument instructs ***digna*** to iterate over all existing projects and apply this command.
- **FROM_DATE**: The starting date and time for the data inspection. Acceptable formats include %Y-%m-%d, %Y-%m-%dT%H:%M:%S, or %Y-%m-%d %H:%M:%S (required).
- **TO_DATE**: The ending date and time for the data inspection, following the same formats as FROM_DATE (required).
  
#### Options

- `--table-name`, `-tn`: Limits the inspection to a specific table within the project.
- `--table-filter`, `-tf`: Filters to inspect only tables containing the specified substring in their names.
- `--enable_notification`, `-en`: Enables the sending of notifications in case of alerts.

  
#### Example
  
To inspect data for the project `ProjectA` from January 1, 2024, to January 31, 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

The `inspect-status` command in the ***digna*** CLI is used to check the progress of an asynchronous inspection based on the request ID.

#### Command Usage

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Arguments
  
- **REQUEST_ID**: The request id returned by the `inspect-async` command 
  
#### Example
  
To check the progress of an inspection with request ID 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

The `inspect-cancel` command in the ***digna*** CLI is used to cancel inspections based on the request ID or it can be used to cancel all current requests.

#### Command Usage

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Arguments
  
- **REQUEST_ID**: The request id returned by the `inspect-async` command 
  
#### Example
  
To cancel the inspection with request ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

To cancel all requests that are currently running or pending:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

The `export-ds` command in the ***digna*** CLI is used to create an export of data sources from the ***digna*** repository. By default, all data sources from a given project will be exported.

#### Command Usage
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Arguments
- **PROJECT_NAME**: The name of the project from which the data sources will be exported.

#### Options

- `--table_name`, `-tn`: Export a particular data source from a project.
- `--exportfile`, `-ef`: Specify the filename for the export.
    
#### Example
  
To export all data sources from the project named `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
This command exports all data sources from `ProjectA` as a JSON document that can be imported to another project or ***digna*** repository.


### import-ds

The `import-ds` command in the ***digna*** CLI is used to import data sources into a target project and create an import report.

#### Command Usage
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: The name of the project to which the data sources will be imported.
- **EXPORT_FILE**: The filename of the data sources export to be imported.

#### Options

- `--output-file`, `-o`: File to save the import report (if not specified, prints to terminal in tabular form).
- `--output-format`, `-f`: Format to save the import report (json, csv).
    
#### Example
  
To import all data sources from export file  `my_export.json` into `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
After the import, this command will also show a report of imported and skipped objects. Only new data sources will be imported into `ProjectB`. In order to find out which objects would be imported and skipped, you can use the command `plan-import-ds`

### plan-import-ds

The `plan-import-ds` command in the ***digna*** CLI is used to import data sources into a target project and create an import report.

#### Command Usage
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: The name of the project to which the data sources would be imported.
- **EXPORT_FILE**: The filename of the data sources export to be analyzed before the import.

#### Options

- `--output-file`, `-o`: File to save the import report (if not specified, prints to terminal in tabular form).
- `--output-format`, `-f`: Format to save the import report (json, csv).
    
#### Example
  
To check which data sources would be imported and which would be skipped from export file `my_export.json` when imported into `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
This command will only show an import plan of objects to be imported and skipped.



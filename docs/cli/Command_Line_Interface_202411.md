---
title: digna CLI Reference 2024.11 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.11. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

This page documents the full set of commands available in ***digna*** CLI release **2024.11**, including usage examples and options.


---
## CLI Basics

---

## Using `help` Option

The `--help` option provides information about available commands and their usage. There are two main ways to use this option:

1. **Displaying General Help:**
   
    Use –help immediate after the keyword ***digna***cl  
   ```bash
   dignacli --help

3.  **Getting Help for Specific Commands:**  
  
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

  
## Using `check-repo-connection` Command

The check-repo-connection command is a utility within the ***digna*** CLI tool designed to test the connectivity and access to a specified ***digna*** repository. This command ensures that the CLI can interact with the repository.
      
### Command Usage
```bash
dignacli check-repo-connection
```

Upon successful execution, the command outputs a confirmation of the connection, along with details about the repository: Repository version, Host, Database and Schema.  
  
If the repository connection is not successful, check the config.toml file for correct configuration settings.

## Using ‘version’ command

To check the installed version of *dignacli*, use the --version option.  
  
### Command Usage
```bash
dignacli --version
```
  
### Example Output
```bash
dignacli version 2024.11
```

## Using logging options
  
By default, the console output of the ***digna*** commands is designed to be minimalistic. Most commands offer the possibility of providing additional information, using the following options:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” and “debug” are defining the level of detail, whereas the “logfile” switch allows redirecting the output to be streamed to a file rather than the console window.

# User Management

## Using ‘add-user’ command
  
The add-user command in the ***digna*** CLI is used to add a new user to the ***digna*** system
  
### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Arguments

- **USER_NAME**: The username for the new user (required).
- **USER_FULL_NAME**: The full name of the new user (required).
- **USER_PASSWORD**: The password for the new user (required).

### Options

- `--is_superuser`, `-su`: Flag to designate the new user as an admin.
- `--valid_until`, `-vu`: Sets an expiration date for the user account in the format `YYYY-MM-DD HH:MI:SS`. If not set, the account does not have an expiration date.

### Example

To add a new user with username `jdoe`, full name `John Doe`, and password `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
To add a new user and set an account expiration date:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Using `delete-user` command
  
The `delete-user` command in the ***digna*** CLI is used to remove an existing user from the ***digna*** system.
  
### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
### Arguments
- **USER_NAME**: The username of the user to be deleted (required). This is the only argument required by the command.

### Example
```bash
dignacli delete-user jdoe
```
  
Executing this command will remove the user `jdoe` from the ***digna*** system, revoking their access and deleting their associated data and permissions from the repository.

## Using `modify-user` Command

The `modify-user` command in the ***digna*** CLI is used to update the details of an existing user in the ***digna*** system.

### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Arguments
  
- **USER_NAME**: The username of the user to be modified (required).
- **USER_FULL_NAME**: The new full name for the user (required).
  
### Options  
  
- `--is_superuser`, `-su`: Sets the user as a superuser, granting elevated privileges. This flag does not require a value.  
- `--valid_until`, `-vu`: Sets an expiration date for the user account in the format YYYY-MM-DD HH:MI:SS. If not provided, the account remains valid indefinitely.  
  
### Example
  
To modify the full name of the user `jdoe` to “Johnathan Doe” and set the user as a superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Using `modify-user-pwd` Command
  
The `modify-user-pwd` command in the ***digna*** CLI is used to change the password for an existing user in the ***digna*** system.
  
### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Arguments
  
- **USER_NAME**: The username of the user whose password is to be changed (required).
- **USER_PWD**: The new password for the user (required).
  
### Example
  
To change the password for the user `jdoe` to `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Using `list-users` Command

The `list-users` command in the ***digna*** CLI displays a list of all users registered in the ***digna*** system.

### Command Usage

```bash
dignacli list-users
```

Executing this command in the ***digna*** CLI will connect to the ***digna*** repository and list all users, showing their ID, username, full name, superuser status, and expiration timestamps.

# Repository Management

### Using `upgrade-repo` Command
  
The `upgrade-repo` command in the ***digna*** CLI is used to upgrade or initialize the ***digna*** repository. This command is essential for applying updates or setting up the repository infrastructure for the first time.
  
### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
### Options
  
- `--simulation-mode`, `-s`: When enabled, this option runs the command in simulation mode, which prints the SQL statements that would be executed but does not actually execute them. This is useful for previewing changes without making any modifications to the repository.  

  
### Example
  
To upgrade the ***digna*** repository, you can run the command without any options:
  
```bash
dignacli upgrade-repo
```  
To run the upgrade in simulation mode (to see the SQL statements without applying them):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
This command is crucial for maintaining the ***digna*** system, ensuring that the database schema and other repository components are up to date with the latest version of the software.

## Using `encrypt` Command
  
The `encrypt` command in the ***digna*** CLI is used to encrypt a password.
  
### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Arguments
- **PASSWORD**: The password that needs to be encrypted (required).
  
### Example
  
To encrypt a password, you need to provide the password as an argument.   
For instance, to encrypt the password `mypassword123`, you would use:
```bash
dignacli encrypt mypassword123
```
This command outputs the encrypted version of the provided password, which can then be used in secure contexts. If the password argument is not provided, the CLI will display an error indicating the missing argument.

## Using `generate-key` Command
  
The `generate-key` command is used to generate a Fernet key, which is essential for securing passwords stored in the ***digna*** repository.
  
### Command Usage
```bash
dignacli generate-key
```
  
# Data Management

## Using `clean-up` Command

The `clean-up` command in the ***digna*** CLI is used to remove profiles, predictions, and traffic light system data for one or more data sources within a specified project. This command is essential for data lifecycle management, helping maintain an organized and efficient data environment by clearing outdated or unnecessary data.

### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME**: The name of the project from which data is to be removed (required). Using the keyword all-projects in this argument instructs ***digna*** to iterate over all existing projects and apply this command.
- **FROM_DATE**: The start date and time for the data removal. Acceptable formats include %Y-%m-%d, %Y-%m-%dT%H:%M:%S, or %Y-%m-%d %H:%M:%S (required).
- **TO_DATE**: The end date and time for the data removal, following the same formats as FROM_DATE (required).
  
### Options
  
- `--table-name`, `-tn`: Limits the clean-up operation to a specific table within the project.
- `--table-filter`, `-tf`: Filters to limit the clean-up to tables containing the specified substring in their names.
- `--timing`, `-tm`: Displays the time duration of the clean-up process after completion.
- `--help`: Displays help information for the clean-up command and exits.
  
### Example
  
To remove data from the project ProjectA between January 1, 2023, and June 30, 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
To remove data only from a specific table named `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
This command helps in managing data storage and ensuring that the repository only contains relevant information.

## Using `inspect` Command

The `inspect` command in the ***digna*** CLI is used to create profiles, predictions, and traffic light system data for one or more data sources within a specified project. This command helps in analyzing and monitoring data over a defined period.

### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME**: The name of the project for which data is to be inspected (required). Using the keyword all-projects in this argument instructs ***digna*** to iterate over all existing projects and apply this command.
- **FROM_DATE**: The starting date and time for the data inspection. Acceptable formats include %Y-%m-%d, %Y-%m-%dT%H:%M:%S, or %Y-%m-%d %H:%M:%S (required).
- **TO_DATE**: The ending date and time for the data inspection, following the same formats as FROM_DATE (required).
  
### Options

- `--table-name`, `-tn`: Limits the inspection to a specific table within the project.
- `--table-filter`, `-tf`: Filters to inspect only tables containing the specified substring in their names.
- `--do-profile`: Triggers the recollection of profiles. The default is do-profile.
- `--no-do-profile`: Prevents the recollection of profiles.
- `--do-prediction`: Triggers the recalculation of predictions. The default is do-prediction.
- `--no-do-prediction`: Prevents the recalculation of predictions.
- `--do-alert-status`: Triggers the recalculation of alert statuses. The default is do-alert-status.
- `--no-do-alert-status`: Prevents the recalculation of alert statuses.
- `--timing`, `-tm`: Displays the duration of the inspection process after completion.
  
### Example
  
To inspect data for the project `ProjectA` from January 1, 2024, to January 31, 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
To inspect only a specific table and force recalculation of predictions:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
This command is useful for generating updated profiles and predictions, monitoring data integrity, and managing alert systems within a specified project timeframe.

## Using `tls-status` Command

The `tls-status` command in the ***digna*** CLI is used to query the status of the Traffic Light System (TLS) for a specific table within a project on a given date. The Traffic Light System provides insights into the data's health and quality, indicating any issues or alerts that may need attention.
  
### Command Usage
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Arguments
  
- **PROJECT_NAME**: The name of the project for which the TLS status is being queried (required).
- **TABLE_NAME**: The specific table within the project for which the TLS status is needed (required).
- **DATE**: The date for which the TLS status is being queried, typically in the format %Y-%m-%d (required).
  
### Example
  
To check the TLS status for a table named UserData in the project ProjectA on July 1, 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

This command helps users monitor and maintain data quality by providing a clear and actionable status report based on predefined criteria.

## Using `list-projects` Command
  
The `list-projects` command in the ***digna*** CLI is used to display a list of all available projects within the ***digna*** system.
  
### Command Usage
  
```bash
dignacli list-projects
```

This command is especially useful for administrators and users managing multiple projects, providing a quick overview of the available projects in the ***digna*** repository.

## Using `list-ds` Command

The `list-ds` command in the ***digna*** CLI is used to display a list of all available data sources within a specified project. This command is useful for understanding the data assets available for analysis and management in the ***digna*** system.

### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Arguments
- **PROJECT_NAME**: The name of the project for which the data sources are being listed (required).
  
### Example
  
To list all data sources in the project named `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
This command provides users with an overview of the data sources available in a project, helping them to navigate and manage the data landscape more effectively.

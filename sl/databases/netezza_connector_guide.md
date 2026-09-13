# Source Connector for Netezza

This guide describes how to configure *digna* to connect to Netezza over **ODBC**, using a
**DSN-less** connection string.

The *digna* side of the setup is the same for every technology — where connections are created,
how property values are encrypted, how a connection is tested and what the profiling modes
mean. It is described in [Database Connections Overview](overview.md). This page covers what is
specific to Netezza.

---

## 1. Install the ODBC Driver {: #1-install-the-odbc-driver }

Install the **NetezzaSQL** ODBC driver (part of the IBM Netezza client tools) on the machine
that runs the *digna* backend, following the vendor's official installation guide.

Read the exact registered driver name off your host as described in
[Install the ODBC Driver on the digna Host](overview.md#install-the-driver).

---

## 2. ODBC Properties {: #2-odbc-properties }

!!! important "An example, not a specification"

    The set below is one combination that is known to work. The properties belong to the
    NetezzaSQL driver, so their names, defaults and accepted values differ between client
    versions and platforms, and a TLS-secured appliance needs more than the properties shown
    here. Use this as a starting point and check the documentation of the client version you
    installed.

Add the following properties in the **Add DB Connection** screen:

| Key | Example value | Notes |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Must match the driver name registered on the *digna* host. The braces are the usual way to write this name |
| `SERVER` | `netezza.example.com` | Server name or IP address |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Database the session starts in |
| `UID` | `ADMIN` | Database user |
| `PWD` | `<password>` | Tick **Encrypted** |

The resulting connection string looks like this:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Depending on your driver version, setup and security requirements, further properties may be
needed — for example `SecurityLevel` and `CaCertFile` for a TLS-secured appliance. Every option
the driver's *Advanced*, *SSL* and *Driver* dialogs offer can be added as a property.

---

## 3. *digna* Configuration {: #3-digna-configuration }

In the **Add DB Connection** screen, provide the following:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Notes on Netezza {: #4-notes-on-netezza }

- **Catalogs and schemas both apply.** *digna* lists the databases the user may see (from
  `_V_DATABASE`) as catalogs and their schemas (from `_V_SCHEMA`) below them, so one connection
  can serve sources in more than one database. `DATABASE` only decides where the session
  starts.
- **Identifiers are upper case** unless they were created quoted, which is why the examples
  above use `TEST` and `ADMIN`.
- **Profiling modes.** *Permanent* creates the work tables in **Work Schema**, so the user needs
  `CREATE TABLE` there. *Session* uses `CREATE TEMPORARY TABLE` and does not touch
  **Work Schema**. *Standard* needs read access only.

---

## 5. Verifying the Driver (optional) {: #5-verifying-the-driver-optional }

Configuring an ODBC data source is not required for a DSN-less connection, but the driver's
own dialog is a convenient way to confirm that the driver and your credentials work before you
enter them in *digna*.

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

The fields in **DSN Options** correspond one-to-one to the properties in
[section 2](#2-odbc-properties). Depending on your Netezza driver, setup and security
requirements, you may also need data in the **Advanced DSN Options**, **SSL DSN Options** or
**Driver Options** tabs; for the simplest setup, **DSN Options** is sufficient.

Click the **Test Connection** button.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

When you receive the success screen, the driver is working and the values are correct.
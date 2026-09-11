---
title: Database Connections Overview – DSN-less ODBC Setup | digna Documentation
description: How database connections work in digna. Every source technology is reached over ODBC with a DSN-less connection string built from ODBC properties. Covers driver installation on the digna host, the Add DB Connection screen, property encryption, connection testing, troubleshooting and links to the per-technology guides.
image: /assets/logo_square.png
keywords:
  - digna database connection
  - dsn-less odbc
  - odbc connection string
  - odbc driver setup
  - unixodbc
  - odbc properties
  - data source configuration
lang: en
robots: index, follow
og_title: digna Database Connections – DSN-less ODBC Setup
og_description: Configure a digna source connection over ODBC without a DSN. Driver installation, ODBC properties, encryption, testing and troubleshooting.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Database Connections Overview

---

## Table of Contents

1. [How Connections Work](#how-connections-work)
2. [Technology Guides](#technology-guides)
3. [Prerequisite: Install the ODBC Driver on the digna Host](#install-the-driver)
4. [Create a Database Connection](#create-a-database-connection)
5. [ODBC Properties](#odbc-properties)
6. [Encrypting Property Values](#encrypting-property-values)
7. [Testing a Connection](#testing-a-connection)
8. [Which Database the Connection Sees](#which-database-the-connection-sees)
9. [Profiling Mode and Work Schema](#profiling-mode-and-work-schema)
10. [Using a DSN Instead](#using-a-dsn-instead)
11. [Troubleshooting](#troubleshooting)

---

## How Connections Work {: #how-connections-work }

*digna* reaches every source technology over **ODBC**. A connection is a list of ODBC
properties that you enter as key/value pairs. When *digna* opens the connection, it joins those
pairs into a connection string — `Key=Value`, separated by `;`, in the order you listed them —
and hands it to the ODBC driver manager on the *digna* host.

Entering the properties yourself is what makes the setup **DSN-less**: the connection carries
everything the driver needs, so no ODBC data source (DSN) has to be registered on the host.
This is the recommended way to configure *digna*, because the connection definition lives
entirely in *digna* and moves with it.

### Why ODBC {: #why-odbc }

Earlier releases offered a choice between a per-technology driver and ODBC, selected with a
**Use ODBC** switch. From Release 2026.06, *digna* builds on ODBC alone. A single, standard
interface gives you more than a set of bespoke drivers can:

- **Authentication** — authentication is part of ODBC, so a connection can use whatever its
  driver supports: passwords, tokens and PATs, Kerberos and Active Directory, MFA and
  browser-based single sign-on, cloud identity, client certificates and TLS. New methods arrive
  with a driver update, rather than waiting for a *digna* release.
- **Drivers maintained by the database vendors** — the vendor's own driver tracks new server
  versions and security fixes, and you can update it on your own schedule, independently of
  *digna*.
- **One way to configure everything** — every technology is a list of key/value properties, with
  the same interface, the same encryption of sensitive values and the same troubleshooting,
  instead of a different set of fields per source.
- **Tuning and reach** — driver-level options such as timeouts, TLS settings, proxies and fetch
  sizes are available for every source, and any technology with a compliant ODBC driver can be
  connected, including ones *digna* does not publish a dedicated guide for.

!!! note "What changed in the interface"

    The **Use ODBC** switch and the separate host, port, database, user and password fields no
    longer exist. A connection that does not already use ODBC needs its ODBC properties entered
    before it will work again — see
    [Create a Database Connection](#create-a-database-connection).

---

## Technology Guides {: #technology-guides }

The property names differ per driver, and each technology has one or two details that the
others do not have. The guides below cover that part; this page covers the *digna* side, which
is the same for all of them.

!!! important "The property sets in the guides are examples"

    Each guide shows one combination that is known to work — the one *digna* is tested against.
    It is a starting point, not a specification: the properties belong to the ODBC driver, and
    which ones exist, what they are called and which values they accept differs between driver
    versions and vendors, between Windows, Linux and macOS, and with how the source server is
    configured — authentication method, TLS, gateway, port. Expect to adjust a value or two,
    and treat the documentation of the driver version you installed as the authority.

| Technology | Guide | Worth knowing |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverless pools need `-ondemand` in the host name and support only *Standard* profiling |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Token authentication: `UID=token`, PAT in `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Catalogs come from the driver, not from a query |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Driver name is braced: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` takes either a full connect descriptor or a `tnsnames.ora` alias |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` must match what the server demands |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programmatic access token is the tested authentication path |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` decides which schemas *digna* can see |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Host goes into `DBCNAME`; databases act as schemas |

---

## Prerequisite: Install the ODBC Driver on the digna Host {: #install-the-driver }

*digna* opens source connections from the **server that runs the digna backend**, not from the
browser. The ODBC driver must therefore be installed on that machine, and its name must be
registered with the local driver manager.

=== "Windows"

    Install the vendor's 64-bit driver, then open **ODBC Data Source Administrator (64-bit)**
    and switch to the **Drivers** tab. The names listed there are exactly the values you may
    use for the `Driver` property.

=== "Linux"

    Install **unixODBC** and the vendor's driver, then list the registered driver names:

    ```bash
    odbcinst -q -d
    ```

    The names printed in brackets are the values you may use for the `Driver` property. They
    come from `/etc/odbcinst.ini` (or the file that `odbcinst -j` reports).

=== "macOS"

    Install **unixODBC** (for example with `brew install unixodbc`) and the vendor's driver,
    then list the registered driver names:

    ```bash
    odbcinst -q -d
    ```

!!! warning "The driver name must match character for character"

    `Driver` is passed to the driver manager unchanged. `Simba Spark ODBC Driver` and
    `Simba Spark ODBC Driver 64` are different drivers as far as the driver manager is
    concerned, and a name that is not registered produces a *data source name not found*
    error even though no DSN is involved.

Instead of a registered name, all common driver managers also accept the full path to the
driver library, for example `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. That is
useful when the driver is installed but not registered.

---

## Create a Database Connection {: #create-a-database-connection }

Open the **Admin Panel**, go to the **Database Connections** tab and click
**Add DB Connection**. The screen asks for five things:

| Field | Description |
|---|---|
| **Name** | Name of the connection. This is used for referencing the connection in other screens. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake or Hive. It selects the SQL dialect *digna* generates, so it must match the source — not the driver. Azure Synapse Analytics is a **SQL Server** connection. |
| **ODBC Properties** | The key/value pairs described in [ODBC Properties](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* or *Session* — see [Profiling Mode and Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schema that holds the work tables for *Permanent* profiling. |

A connection is administered centrally and then assigned to one or more projects, so the same
connection can serve several projects.

---

## ODBC Properties {: #odbc-properties }

Click **Add Property** for every property, and fill in **Key**, **Value** and, for secrets,
the **Encrypted** checkbox. Each technology guide lists an example set for that technology,
which you adapt to your driver version and server — see
[the note above](#technology-guides).

Whatever the driver, a property set covers the same four things:

- **`Driver`** — the registered driver name, as described [above](#install-the-driver).
- **The address of the server** — the key differs per driver: `SERVER`, `HOST`, `DBCNAME`,
  `Server`, or, for Oracle, the `DBQ` connect descriptor.
- **Credentials** — usually `UID` and `PWD`; Snowflake uses `UID` plus a `token`, and
  Databricks uses the literal user `token` plus the personal access token in `PWD`.
- **The database or catalog to work in**, where the technology has one — see
  [Which Database the Connection Sees](#which-database-the-connection-sees).

Anything else the driver documents can be added the same way — connection pooling, socket
timeouts, Kerberos settings, proxy settings. *digna* does not interpret the properties; it
only passes them on.

!!! warning "Values are not escaped — brace anything with a semicolon"

    Because the properties are joined with `;`, a value that itself contains `;` would split the
    connection string in the wrong place. Wrap such values in braces: `PWD={p@ss;word}`.
    The same applies to values with `=` or leading spaces. This is also why some drivers are
    conventionally written braced, as in `{NetezzaSQL}` or `{SnowflakeDSIIDriver}`.

---

## Encrypting Property Values {: #encrypting-property-values }

Tick **Encrypted** for every property that holds a secret — `PWD`, `token`, a client secret.
The value is then encrypted before it is stored in the *digna* repository, masked in the
screen, and decrypted only when the connection string is assembled.

!!! tip "Tip"

    An encrypted value cannot be read back, in the UI or through the API — it can only be
    replaced. Keep secrets in your own password manager as well.

Properties that are not secret — the driver name, host, port, database — are best left
unencrypted, so they stay readable for whoever maintains the connection later.

---

## Testing a Connection {: #testing-a-connection }

Click **Test** in the *Add DB Connection* dialog **before** saving. The test uses the values
currently in the form and performs a real connect, so it reports exactly what an inspection
would hit — a wrong driver name, a rejected password, an unreachable host. Nothing is stored:
the test connection is rolled back whether it succeeds or fails.

For a connection that already exists, hover its row in the **Database Connections** tab and
click the **plug** icon to re-test it. That is the quickest way to check whether a source is
reachable after a password rotation or a firewall change.

---

## Which Database the Connection Sees {: #which-database-the-connection-sees }

When you add a data source, *digna* offers the catalogs, schemas and tables that the
connection can reach. How far that reaches depends on the technology:

| Technology | Catalogs offered |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Only the connection's **current** database |
| **Teradata**, **Netezza**, **Databricks** | All databases or catalogs the user is allowed to see |
| **Hive**, **Impala** | Reported by the driver |

!!! important "One connection, one database"

    For PostgreSQL, SQL Server, Oracle and Snowflake, the properties must point at the database
    that holds the source schemas — `DATABASE=…`, `Database=…`, or the service name inside
    Oracle's `DBQ`. Tables in another database are not reachable through that connection; add a
    second connection for it.

---

## Profiling Mode and Work Schema {: #profiling-mode-and-work-schema }

The profiling mode determines how *digna* processes data and calculates metrics:

- **Standard:** Metrics are calculated directly on the source tables without copying the data.
- **Permanent:** Data for the inspected day is copied into a permanent table, and metrics are
  calculated on the copied data.
- **Session:** Data is copied into a session or temporary table, and metrics are calculated on
  this temporary data.

The mode decides what the connection user must be allowed to do:

| Mode | Writes | Rights the connection user needs |
|---|---|---|
| **Standard** | nothing | Read on the source tables |
| **Permanent** | a table per data source in **Work Schema** | Create and drop tables in **Work Schema** |
| **Session** | a temporary table that the database drops with the session | Create temporary tables — **Work Schema** is not used |

*Standard* reads only, which makes it the mode to choose when *digna* is granted read-only
access. **Work Schema** is only read for *Permanent*, but it is worth filling in anyway so the
connection keeps working if the mode is changed later.

---

## Using a DSN Instead {: #using-a-dsn-instead }

A DSN still works — `DSN` is just another property:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

The DSN must be registered on the *digna* host, for the same user account that runs the *digna*
backend, and as a **System DSN** when *digna* runs as a service. Everything that is configured
in the DSN can be overridden by adding it as a property as well.

DSN-less is the documented default because it avoids that host-side state: the connection is
fully described in *digna*, and a new *digna* host needs the driver installed but nothing
configured.

---

## Troubleshooting {: #troubleshooting }

### Data source name not found / no default driver specified

**Symptoms:**
- The **Test** button reports an error mentioning *data source name not found*, even though the
  setup is DSN-less

**Causes & Solutions:**
1. The `Driver` value does not match a registered driver name — compare it with the **Drivers**
   tab of *ODBC Data Source Administrator (64-bit)*, or with `odbcinst -q -d`
2. The driver is installed on your workstation but not on the *digna* host
3. The driver is 32-bit while *digna* is 64-bit — install the 64-bit driver
4. The `Driver` property is missing altogether, and no `DSN` was given either
5. On Linux and macOS, the driver is installed but not registered — give the full path to the
   driver library instead, or register it in `odbcinst.ini`

---

### The connection test times out

**Symptoms:**
- **Test** hangs and then fails after roughly half a minute

**Causes & Solutions:**
1. Host or port unreachable from the *digna* host — check the firewall and, for cloud sources,
   the IP allow list
2. The host name is right but the port belongs to a different service
3. The source needs longer than the default 30 seconds to accept a connection — raise
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` in the `[base]` section of `config.toml` (`0` waits
   indefinitely) and restart the backend
4. A serverless endpoint is resuming from idle — retry, and if it happens routinely, raise the
   login timeout as above

---

### Authentication fails although the credentials are correct

**Symptoms:**
- The driver reports invalid credentials, but the same user works in another SQL client

**Causes & Solutions:**
1. The password contains `;` — wrap the value in braces: `{p@ss;word}`
2. A trailing space was copied into the value
3. The driver expects a specific authentication mechanism — for example `AuthMech` for the
   Hive and Databricks drivers, or `authenticator` for Snowflake
4. The value was stored encrypted and then edited — encrypted values cannot be read back, so
   re-enter the secret in full
5. A token has expired — personal access tokens and programmatic access tokens are issued with
   an expiry date

---

### The data source screen does not offer the expected database or schema

**Symptoms:**
- Catalogs, schemas or tables are missing when a data source is added

**Causes & Solutions:**
1. The connection points at a different database — see
   [Which Database the Connection Sees](#which-database-the-connection-sees)
2. The connection user lacks read rights on the schema or on the data dictionary
3. **Technology** does not match the source, so *digna* queries the wrong data dictionary
4. For Snowflake, no default warehouse is assigned to the user and no `Warehouse` property was
   given, so metadata queries cannot run

---

### Profiling fails while the connection test succeeds

**Symptoms:**
- **Test** passes, but an inspection fails when work tables are created

**Causes & Solutions:**
1. *Permanent* profiling is selected and the connection user cannot create tables in
   **Work Schema** — grant the rights, or switch to *Session* or *Standard*
2. **Work Schema** is empty or names a schema that does not exist, while *Permanent* profiling
   is selected
3. *Session* profiling is selected and the connection user may not create temporary tables
4. A long-running profiling query hits the query timeout — raise
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` in the `[base]` section of `config.toml` (default 3600
   seconds, `0` disables the timeout)

---

## Best Practices

**DO:**

- Install and register the driver on the *digna* host before configuring the connection
- Tick **Encrypted** for every password and token
- Click **Test** before saving, and re-test after a password rotation
- Name connections after the source and environment, for example `sales_dwh_prod`
- Give *digna* a dedicated database user, read-only where *Standard* profiling is enough
- Keep one connection per source database, and add a second one rather than switching the first

**DON'T:**

- Store secrets unencrypted, or share one database user between *digna* and other tools
- Use a 32-bit driver with a 64-bit *digna* installation
- Rely on a User DSN when *digna* runs as a service — it will not be visible
- Put a value containing `;` into a property without braces
- Point **Work Schema** at a schema that holds source data

---

## Support

Need help with a database connection?

- **Email:** support@digna.ai
- **Documentation:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**

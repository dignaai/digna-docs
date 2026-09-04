---
title: Snowflake Connector – Database Integration | digna Documentation
description: Configure digna to connect to Snowflake using the Python connector or the Snowflake ODBC driver. Supports password-based authentication with DSN or DSN-less setups.
image: /assets/logo_square.png
---


# Zdrojový konektor pro Snowflake

Tento průvodce popisuje, jak nakonfigurovat *digna* pro připojení ke Snowflake buď pomocí nativního Python konektoru, nebo ODBC ovladače.

Odkazuje na obrazovku **„Vytvořit připojení k databázi“**.

![Vytvořit připojení k databázi](images/data_source_config_input_mask.png)

---

## Nativní Python ovladač

**Knihovna:** `snowflake-connector-python`  
**Podporovaná autentizace:** Pouze autentizace založená na hesle

> Pro jiné metody autentizace prosím použijte ODBC ovladač.

### *digna* konfigurace (nativní ovladač)

Do obrazovky **„Vytvořit připojení k databázi“** zadejte následující informace:

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Databáze, která obsahuje zdrojové schéma
Schema Name:     Schéma, které obsahuje zdrojová data
User Name:       Uživatelské jméno a warehouse ve formátu "user<@>warehouse"
User Password:   Heslo pro uživatele
Use ODBC:        Disabled (default)
```

---

## ODBC ovladač

ODBC ovladač může podporovat širší spektrum autentizačních a konektivních možností. Tato sekce se zaměřuje na autentizaci založenou na heslu pomocí **SnowflakeDSIIDriver**.

### 1. Instalace ODBC ovladače

Nainstalujte **SnowflakeDSIIDriver** podle oficiální instalační příručky dodavatele.

### 2. Konfigurace ODBC datového zdroje

Postupujte podle těchto kroků pro konfiguraci nového ODBC datového zdroje s autentizací založenou na heslu:

#### Krok 1
![Krok 1](images/snowflake/create_odbc_data_source_step1.png)

Poznámky:
- Pokud nezadáte hodnoty pro Database, Schema a Warehouse, budete je muset zadat jako ODBC vlastnosti během konfigurace datového zdroje v *digna*.
- Hodnota pro "Server" se skládá z názvu vašeho Snowflake účtu následovaného ".snowflakecomputing.com"

#### Krok 2 – Otestujte připojení

Klikněte na tlačítko **TEST**. Úspěšné připojení by mělo vypadat takto:

![Krok 2](images/snowflake/create_odbc_data_source_step2.png)

---

Nyní můžete nakonfigurovat *digna*, aby používalo ODBC připojení, buď pomocí **DSN (Data Source Name)**, nebo v **DSN-less** režimu.

---

### A. Konfigurace založená na DSN

#### *digna* konfigurace

V obrazovce **„Vytvořit připojení k databázi“** zadejte následující:

```
Technology:      Snowflake
Database Name:   Databáze, která obsahuje zdrojové schéma
Schema Name:     Schéma, které obsahuje zdrojová data
Use ODBC:        Enabled
```

#### ODBC vlastnosti

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

volitelně:
name: "Database",       value: "Databáze, která obsahuje zdrojové schéma"
name: "Schema",         value: "Schéma, které obsahuje zdrojová data"
name: "Warehouse",      value: "Warehouse použité pro vykonávání SQL příkazů"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less konfigurace

#### *digna* konfigurace

V obrazovce **„Vytvořit připojení k databázi“** zadejte následující:

```
Technology:      Snowflake
Database Name:   Schéma, které obsahuje zdrojová data (stejné jako Schema Name)
Schema Name:     Schéma, které obsahuje zdrojová data
Use ODBC:        Enabled
```

#### ODBC vlastnosti

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Databáze, která obsahuje zdrojové schéma"
name: "Schema",     value: "Schéma, které obsahuje zdrojová data"
name: "Warehouse",  value: "Warehouse použité pro vykonávání SQL příkazů"
```
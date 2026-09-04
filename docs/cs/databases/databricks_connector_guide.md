---
title: Konektor Databricks s Unity Catalog – integrace databáze | Dokumentace digna
description: Nakonfigurujte digna pro připojení k Databricks s Unity Catalog pomocí nativního Python konektoru nebo ODBC ovladače. Podporuje autentizaci založenou na tokenu a flexibilní konektivitu.
image: /assets/logo_square.png
---

# Zdrojový konektor pro Databricks - s Unity Catalog

Tento průvodce popisuje, jak nakonfigurovat *digna* pro připojení k Databricks buď pomocí nativního Python konektoru, nebo pomocí ODBC ovladače.

Vztahuje se na obrazovku **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativní Python driver

**Knihovna:** `databricks-sql-connector`  
**Podporovaná autentizace:** pouze osobní přístupový token (Personal Access Token, PAT)

> Pro jiné metody autentizace použijte prosím ovladač ODBC.

### Osobní přístupový token (PAT)

Pro autentizaci pomocí osobního přístupového tokenu odkažte na oficiální dokumentaci Databricks:  
[Jak získat PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### Konfigurace *digna* (nativní driver)

Ve obrazovce **"Create a Database Connection"** zadejte následující informace:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC ovladač

ODBC ovladač podporuje širší škálu možností autentizace a konektivity. Tato sekce se zaměřuje na autentizaci založenou na tokenu pomocí **Simba Spark ODBC Driver**.

### 1. Instalace ODBC ovladače

Nainstalujte **Simba Spark ODBC Driver** podle oficiálního instalačního návodu dodavatele.

### 2. Konfigurace ODBC datového zdroje

Postupujte podle těchto kroků pro konfiguraci nového ODBC datového zdroje pomocí osobního přístupového tokenu:

#### Krok 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Krok 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Krok 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Krok 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Krok 5 – Test připojení

Klikněte na tlačítko **TEST**. Úspěšné připojení vypadá takto:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nyní můžete nakonfigurovat *digna*, aby používalo ODBC připojení, buď pomocí **DSN (Data Source Name)**, nebo v **DSN-less** režimu.

---

### A. Konfigurace založená na DSN

#### Konfigurace *digna*

V obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> Hodnota `DSN` musí odpovídat názvu definovanému ve vaší konfiguraci ODBC ovladače.

---

### B. DSN-less konfigurace

#### Konfigurace *digna*

V obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
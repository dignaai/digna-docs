---
title: Databricks-anslutning (Legacy, utan Unity Catalog) | digna-dokumentation
description: Konfigurera digna för att ansluta till Databricks utan Unity Catalog med antingen den inbyggda Python-connectorn eller Simba Spark ODBC-drivrutinen. Stöd för token-baserad autentisering och flexibel uppkoppling.
image: /assets/logo_square.png
---

# Källanslutning för Databricks - utan Unity Catalog

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Databricks med antingen den inbyggda Python-connectorn eller ODBC-drivrutinen.

Den hänvisar till skärmen **"Skapa en databasanslutning"**.

![Skapa en databasanslutning](images/data_source_config_input_mask.png)

---

## Inbyggd Python-drivrutin

**Bibliotek:** `databricks-sql-connector`  
**Stödd autentisering:** Personligt åtkomsttoken (PAT) endast

> ⚠️ För andra autentiseringsmetoder, använd ODBC-drivrutinen.

### Personligt åtkomsttoken (PAT)

För att autentisera med ett personligt åtkomsttoken, se den officiella Databricks-dokumentationen:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna*-konfiguration (inbyggd drivrutin)

Ange följande information i skärmen **"Skapa en databasanslutning"**:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC-drivrutin

ODBC-drivrutinen stödjer ett bredare utbud av autentiserings- och anslutningsalternativ. Denna sektion fokuserar på token-baserad autentisering med **Simba Spark ODBC Driver**.

### 1. Installera ODBC-drivrutinen

Installera **Simba Spark ODBC Driver** genom att följa leverantörens officiella installationsanvisningar.

### 2. Konfigurera ODBC-datakällan

Följ dessa steg för att konfigurera en ny ODBC-datakälla med ett personligt åtkomsttoken:

#### Steg 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Steg 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Steg 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Steg 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Steg 5 – Testa anslutningen

Klicka på **TEST**-knappen. En lyckad anslutning bör se ut så här:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nu kan du konfigurera *digna* att använda ODBC-anslutningen, antingen med en **DSN (Data Source Name)** eller en **DSN-less** konfiguration.

---

### A. DSN-baserad konfiguration

#### *digna*-konfiguration

I skärmen **"Skapa en databasanslutning"** ange följande:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 `DSN` måste matcha namnet som är definierat i din ODBC-drivrutinskonfiguration.

---

### B. DSN-less konfiguration

#### *digna*-konfiguration

I skärmen **"Skapa en databasanslutning"** ange följande:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

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
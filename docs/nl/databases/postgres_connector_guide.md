---
title: PostgreSQL-connector – Database-integratie | digna-documentatie
description: Configureer *digna* om verbinding te maken met PostgreSQL met behulp van de Python-driver psycopg of de PostgreSQL ODBC-driver. Ondersteunt wachtwoordgebaseerde authenticatie met DSN- of DSN-loze configuraties.
image: /assets/logo_square.png
---


# Bronconnector voor PostgreSQL

Deze handleiding beschrijft hoe u *digna* configureert om verbinding te maken met Postgres met behulp van de native Python-connector of de ODBC-driver.

Deze handleiding verwijst naar het scherm **"Maak een databaseverbinding"**.

![Maak een databaseverbinding](images/data_source_config_input_mask.png)

---

## Native Python-driver

**Library:** `psycopg`  
**Ondersteunde authenticatie:** Alleen wachtwoordgebaseerde authenticatie

> ⚠️ Voor andere authenticatiemethoden gebruikt u de ODBC-driver.

### *digna*-configuratie (native driver)

Geef de volgende gegevens op in het scherm **"Maak een databaseverbinding"**:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-driver

De ODBC-driver kan een breder scala aan authenticatie- en connectiviteitsopties ondersteunen. Deze sectie richt zich op wachtwoordgebaseerde authenticatie met de driver **PostgreSQL Unicode(x64)**.

### 1. Installeer de ODBC-driver

Installeer **PostgreSQL Unicode(x64)** (of een vergelijkbare driver) door de officiële installatiehandleiding van de leverancier te volgen.

### 2. Configureer de ODBC-gegevensbron

Volg deze stappen om een nieuwe ODBC-gegevensbron te configureren met wachtwoordgebaseerde authenticatie:

#### Stap 1
![Stap 1](images/postgres/create_odbc_data_source_step1.png)

Opmerking: Als uw databaseconfiguratie vereist dat u een specifieke "SSLMode" kiest, zorg er dan voor dat u deze ook gebruikt bij het definiëren van een DSN-loze configuratie.

#### Stap 2 – Test de verbinding

Klik op de knop **Test Connection**.

![Stap 2](images/postgres/create_odbc_data_source_step2.png)

---

Nu kunt u *digna* configureren om de ODBC-verbinding te gebruiken, ofwel met een **DSN (Data Source Name)** of met een **DSN-loze** configuratie.

---

### A. DSN-gebaseerde configuratie

#### *digna*-configuratie

In het scherm **"Maak een databaseverbinding"** geeft u het volgende op:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-eigenschappen

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 De `DSN` moet overeenkomen met de naam die in uw ODBC-driverconfiguratie is gedefinieerd.

---

### B. DSN-loze configuratie

#### *digna*-configuratie

In het scherm **"Maak een databaseverbinding"** geeft u het volgende op:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-eigenschappen

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```
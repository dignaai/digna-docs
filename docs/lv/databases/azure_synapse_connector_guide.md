---
title: Azure Synapse savienotājs – datubāzu integrācija | digna dokumentācija
description: Konfigurējiet *digna*, lai izveidotu savienojumu ar Azure Synapse Analytics, izmantojot vai nu vietējo Python draiveri, vai ODBC draiveri. Atbalsta gan serverless, gan dedicated SQL poolus.
image: /assets/logo_square.png
---


# Avota savienotājs Azure Synapse Analytics

Šī rokasgrāmata apraksta, kā konfigurēt *digna*, lai savienotos ar Azure Synapse Analytics, izmantojot vai nu vietējo Python savienotāju, vai ODBC draiveri.
Tā atbalsta gan serverless, gan dedicated SQL poolus.

Tā atsaucas uz ekrānu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Vietējais Python draiveris

**Bibliotēka:** `pymssql`  
**Atbalstītā autentifikācija:** Tikai autentifikācija ar paroli

> ⚠️ Citu autentifikācijas metožu gadījumā, lūdzu, izmantojiet ODBC draiveri.

### *digna* konfigurācija (vietējais draiveris)

Norādiet sekojošo informāciju ekrānā **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC draiveris

ODBC draiveris var atbalstīt plašāku autentifikācijas un savienojamības iespēju klāstu. Šī sadaļa koncentrējas uz autentifikāciju ar paroli, izmantojot draiveri **ODBC Driver 18 for SQL Server**.

### 1. Instalējiet ODBC draiveri

Instalējiet draiveri **ODBC Driver 18 for SQL Server** (vai līdzīgu), sekojot piegādātāja oficiālajai instalācijas vadlīnijai.

### 2. Konfigurējiet ODBC datu avotu

Izpildiet šīs darbības, lai konfigurētu jaunu ODBC datu avotu, izmantojot autentifikāciju ar paroli:

#### Step 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Aizpildiet lauku "Server".
Izmantojiet Synapse workspace nosaukumu un papildiniet to ar ".sql.azuresynapse.net".  
**Uzmanību**, ja vēlaties savienoties, izmantojot serverless SQL pool, pārliecinieties, ka iekļaujat "-ondemand", kā parādīts zemāk redzamajā ekrānuzņēmumā.

Nospiediet pogu **Next >**.

#### Step 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Izvēlieties autentifikācijas metodi (piem., lietotājvārds un parole)
un ievadiet nepieciešamos datus.

Nospiediet pogu **Next >**.

#### Step 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Izvēlieties ANSI atbilstošos iestatījumus, pēc tam nospiediet pogu **Next >**.

#### Step 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Jūs varat atstāt noklusējuma iestatījumus vai izvēlēties opcijas pēc vajadzības 
un nospiest pogu **Finish**. 

#### Step 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Tagad noklikšķiniet uz pogas **Test datasource**.

#### Step 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Kad saņemat veiksmīga rezultāta ekrānu, ODBC ir pareizi konfigurēts.

---

Tagad varat konfigurēt *digna*, lai izmantotu ODBC savienojumu, vai nu ar **DSN (Data Source Name)**, vai ar konfigurāciju bez DSN.

---

### A. DSN bāzēta konfigurācija

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` jāatbilst nosaukumam, kas definēts jūsu ODBC draivera konfigurācijā.

---

### B. Konfigurācija bez DSN

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Piezīme** par SERVER īpašību:  
Izmantojiet Synapse workspace nosaukumu un papildiniet to ar ".sql.azuresynapse.net". Ja vēlaties savienoties, izmantojot serverless SQL pool, pārliecinieties, ka iekļaujat "-ondemand", kā parādīts zemāk redzamajā ekrānuzņēmumā.
---
title: Azure Synapse Connector – Integracija baze podatkov | digna dokumentacija
description: Konfigurirajte digna za povezavo z Azure Synapse Analytics z uporabo bodisi nativnega Python gonilnika ali ODBC gonilnika. Podprti so tako serverless kot dedicated SQL pooli.
image: /assets/logo_square.png
---


# Source Connector for Azure Synapse Analytics

Ta priročnik opisuje, kako nastaviti *digna* za povezavo z Azure Synapse Analytics z uporabo bodisi nativnega Python konnektorja ali ODBC gonilnika. Podprti so tako serverless kot dedicated SQL pooli.

Navaja zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Knjižnica:** `pymssql`  
**Podprta avtentikacija:** samo geselna avtentikacija

> ⚠️ Za druge metode avtentikacije uporabite ODBC gonilnik.

### *digna* konfiguracija (nativni gonilnik)

Navedite naslednje informacije na zaslonu **"Create a Database Connection"**:

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

## ODBC Driver

ODBC gonilnik lahko podpira širši nabor možnosti avtentikacije in povezovanja. Ta razdelek je osredotočen na geselno avtentikacijo z uporabo gonilnika **ODBC Driver 18 for SQL Server**.

### 1. Namestitev ODBC gonilnika

Namestite gonilnik **ODBC Driver 18 for SQL Server** (ali podoben), po uradnih navodilih dobavitelja.

### 2. Nastavitev vira podatkov ODBC

Izvedite te korake, da nastavite nov vir podatkov ODBC z uporabo geselne avtentikacije:

#### Korak 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Izpolnite polje "Server".  
Uporabite ime Synapse workspace in dodajte ".sql.azuresynapse.net".   
**Pozor**, če se želite povezati z serverless SQL poolom, se prepričajte, da vključite "-ondemand", kot je prikazano na naslednjem posnetku zaslona.

Kliknite gumb **Naprej >**.

#### Korak 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Izberite metodo avtentikacije (na primer uporabniško ime in geslo) in vnesite potrebne podatke.

Kliknite gumb **Naprej >**.

#### Korak 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Izberite možnosti, združljive z ANSI, nato kliknite gumb **Naprej >**.

#### Korak 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Lahko pustite privzete nastavitve ali izberete možnosti po potrebi in kliknete gumb **Končano**. 

#### Korak 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Zdaj kliknite gumb **Preveri vir podatkov**.

#### Korak 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Ko prejmete zaslon o uspehu, je ODBC pravilno nastavljen.

---

Zdaj lahko nastavite *digna*, da uporablja ODBC-povezavo, bodisi z **DSN (Data Source Name)** ali v **DSN-less** načinu.

---

### A. Konfiguracija na osnovi DSN

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** navedite naslednje:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Lastnosti ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` mora ustrezati imenu, določenemu v konfiguraciji vašega ODBC gonilnika.

---

### B. DSN-less konfiguracija

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** navedite naslednje:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Lastnosti ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Opomba** glede lastnosti SERVER:  
Uporabite ime Synapse workspace in dodajte ".sql.azuresynapse.net". Če se želite povezati z serverless SQL poolom, se prepričajte, da vključite "-ondemand", kot je prikazano na naslednjem posnetku zaslona.
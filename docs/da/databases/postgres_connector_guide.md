---
title: PostgreSQL Connector – Databaseintegration | digna-dokumentation
description: Konfigurer digna til at oprette forbindelse til PostgreSQL ved hjælp af psycopg Python-driveren eller PostgreSQL ODBC-driveren. Understøtter adgangskodebaseret autentificering med DSN- eller DSN-less-konfigurationer.
image: /assets/logo_square.png
---


# Source Connector for PostgreSQL

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til Postgres ved hjælp af enten den native Python-connector eller ODBC-driveren.

Det henviser til skærmen **"Create a Database Connection"**.

![Opret en databaseforbindelse](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Understøttet autentificering:** Kun adgangskodebaseret autentificering

> For andre autentificeringsmetoder, brug venligst ODBC-driveren.

### *digna* Konfiguration (Native Driver)

Angiv følgende oplysninger i skærmen **"Create a Database Connection"**:

```
Teknologi:        Postgres
Host-adresse:     Servernavn eller IP-adresse
Host-port:        Portnummer, f.eks. 5432
Databasenavn:     Navn på databasen
Schema-navn:      Schema, der indeholder kilde-data
Brugernavn:       Databasebrugernavn
Adgangskode:      Adgangskode for brugeren
Brug ODBC:        Deaktiveret (standard)
```

---

## ODBC Driver

ODBC-driveren kan understøtte et bredere udvalg af autentificerings- og forbindelsesmuligheder. Dette afsnit fokuserer på adgangskodebaseret autentificering ved brug af driveren **PostgreSQL Unicode(x64)**.

### 1. Installer ODBC-driveren

Installer **PostgreSQL Unicode(x64)** (eller lignende) ved at følge leverandørens officielle installationsvejledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trin for at konfigurere en ny ODBC-datakilde med adgangskodebaseret autentificering:

#### Trin 1
![Trin 1](images/postgres/create_odbc_data_source_step1.png)

Bemærk: Hvis din databasesætup kræver, at du vælger en specifik "SSLMode", så sørg også for at bruge denne, når du definerer en DSN-less-konfiguration.

#### Trin 2 – Test forbindelsen

Klik på **Test Connection**-knappen.

![Trin 2](images/postgres/create_odbc_data_source_step2.png)

---

Nu kan du konfigurere *digna* til at bruge ODBC-forbindelsen, enten med en **DSN (Data Source Name)** eller en **DSN-less** konfiguration.

---

### A. DSN-baseret konfiguration

#### *digna* Konfiguration

Angiv følgende i skærmen **"Create a Database Connection"**:

```
Teknologi:        PostgreSQL
Databasenavn:     Database, der indeholder kilde-schemaet
Schema-navn:      Schema, der indeholder kilde-data
Brug ODBC:        Aktiveret
```

#### ODBC-egenskaber

```
name: "DSN",    value: "PostgreSQL35W"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less konfiguration

#### *digna* Konfiguration

Angiv følgende i skærmen **"Create a Database Connection"**:

```
Teknologi:        PostgreSQL
Databasenavn:     Schema, der indeholder kilde-data (samme som Schema Name)
Schema-navn:      Schema, der indeholder kilde-data
Brug ODBC:        Aktiveret
```

#### ODBC-egenskaber

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```
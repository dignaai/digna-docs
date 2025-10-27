---
title: PostgreSQL savienotājs — Datubāzes integrācija | digna dokumentācija
description: Konfigurējiet digna, lai izveidotu savienojumu ar PostgreSQL, izmantojot psycopg Python draiveri vai PostgreSQL ODBC draiveri. Atbalsta autentifikāciju ar paroli gan ar DSN, gan bez DSN.
image: /assets/logo_square.png
---


# Avota savienotājs PostgreSQL

Šī rokasgrāmata apraksta, kā konfigurēt *digna*, lai izveidotu savienojumu ar Postgres, izmantojot vai nu vietējo Python savienotāju, vai ODBC draiveri.

Tiek atsauce uz ekrānu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Dabiskais Python draiveris

**Bibliotēka:** `psycopg`  
**Atbalstītā autentifikācija:** tikai autentifikācija ar paroli

> ⚠️ Citu autentifikācijas metožu gadījumā, lūdzu, izmantojiet ODBC draiveri.

### *digna* konfigurācija (dabiskais draiveris)

Norādiet šādu informāciju ekrānā **"Create a Database Connection"**:

```
Tehnoloģija:     Postgres
Saimniekdatora adrese: Servera nosaukums vai IP adrese
Saimniekdatora ports:  Porta numurs, piemēram, 5432
Datubāzes nosaukums:  Datubāzes nosaukums
Shēmas nosaukums:     Shēma, kurā atrodas avota dati
Lietotājvārds:        Datubāzes lietotāja vārds
Lietotāja parole:     Lietotāja parole
Izmantot ODBC:        Atspējots (noklusējums)
```

---

## ODBC draiveris

ODBC draiveris var atbalstīt plašāku autentifikācijas un savienojamības izvēļu klāstu. Šī sadaļa koncentrējas uz autentifikāciju ar paroli, izmantojot draiveri **PostgreSQL Unicode(x64)**.

### 1. Instalējiet ODBC draiveri

Instalējiet **PostgreSQL Unicode(x64)** (vai līdzīgu), sekojot piegādātāja oficiālajai instalācijas instrukcijai.

### 2. Konfigurējiet ODBC datu avotu

Veiciet šīs darbības, lai konfigurētu jaunu ODBC datu avotu, izmantojot autentifikāciju ar paroli:

#### 1. solis
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Piezīme: Ja jūsu datubāzes konfigurācija prasa izvēlēties konkrētu "SSLMode", pārliecinieties, ka to izmantojat arī definējot konfigurāciju bez DSN.

#### 2. solis – Savienojuma pārbaude

Nospiediet pogu **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Tagad varat konfigurēt *digna*, lai izmantotu ODBC savienojumu, vai nu ar **DSN (Data Source Name)**, vai ar konfigurāciju **bez DSN**.

---

### A. DSN bāzēta konfigurācija

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Tehnoloģija:      PostgreSQL
Datubāzes nosaukums:  Datubāze, kurā atrodas avota shēma
Shēmas nosaukums:     Shēma, kurā atrodas avota dati
Izmantot ODBC:        Ieslēgts
```

#### ODBC rekvizīti

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN` jāatbilst nosaukumam, kas definēts jūsu ODBC draivera konfigurācijā.

---

### B. Konfigurācija bez DSN

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Tehnoloģija:      PostgreSQL
Datubāzes nosaukums:  Shēma, kurā atrodas avota dati (tas pats, kas Shēmas nosaukums)
Shēmas nosaukums:     Shēma, kurā atrodas avota dati
Izmantot ODBC:        Ieslēgts
```

#### ODBC rekvizīti

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "jūsu servera nosaukums vai IP adrese"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres vai cita jūsu datubāzes nosaukums"
name: "UID",        value: "jūsu Postgres lietotājs"
name: "PWD",        value: "jūsu Postgres parole"
name: "SSLMode",    value: "require"
```
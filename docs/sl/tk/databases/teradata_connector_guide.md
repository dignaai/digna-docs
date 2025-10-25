---
title: Teradata Connector – Integracija baze podatkov | digna Dokumentacija
description: Konfigurirajte digna za povezavo s Teradata z uporabo teradatasql Python gonilnika ali Teradata ODBC gonilnika. Podpira overjanje z geslom z nastavitvami z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Povezovalnik virov za Teradata

Ta vodnik pojasnjuje, kako konfigurirati *digna*, da se poveže s Teradata bodisi z lokalno Python povezavo bodisi z uporabo ODBC gonilnika.

Spodaj se sklicuje na zaslon **"Ustvari povezavo do baze podatkov"**.

![Bir veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## Lokalni Python gonilnik

**Knjižnica:** `teradatasql`  
**Podprto overjanje:** Samo overjanje z geslom

> ⚠️ Za druge metode overjanja uporabite ODBC gonilnik.

### *digna* konfiguracija (lokalni gonilnik)

Na zaslonu **"Ustvari povezavo do baze podatkov"** vnesite naslednje podatke:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti overjanja in povezovanja. Ta razdelek se osredotoča na overjanje z geslom z uporabo gonilnika **Teradata Database ODBC Driver 20.00**.

### 1. Namestite ODBC gonilnik

Namestite gonilnik **Teradata Database ODBC Driver 20.00** (ali podoben), tako da sledite uradnemu namestitvenemu vodniku prodajalca.

### 2. Konfigurirajte ODBC vir podatkov

Za konfiguracijo novega ODBC vira podatkov z overjanjem z geslom sledite tem korakom:

#### Korak 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Kliknite gumb Test.

#### Korak 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Vnesite uporabniško ime in geslo.

Kliknite gumb OK.
Ko prejmete zaslon s sporočilom o uspehu, je ODBC pravilno konfiguriran.

---

Zdaj lahko *digna* konfigurirate za uporabo ODBC povezave bodisi z **DSN (Data Source Name)** bodisi z namestitvijo **brez DSN**.

---

### A. Konfiguracija z DSN

#### *digna* konfiguracija

Na zaslonu **"Ustvari povezavo do baze podatkov"** vnesite naslednje:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN` mora ustrezati imenu, definirano v konfiguraciji ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### *digna* konfiguracija

Na zaslonu **"Ustvari povezavo do baze podatkov"** vnesite naslednje:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
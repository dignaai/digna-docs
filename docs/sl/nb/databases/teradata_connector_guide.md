---
title: Povezava z Teradata – Integracija baze podatkov | digna-dokumentacija
description: Konfigurirajte digna za povezavo s Teradata z uporabo Python gonilnika teradatasql ali Teradata ODBC gonilnika. Podpira overjanje z geslom s konfiguracijo DSN ali brez DSN.
image: /assets/logo_square.png
---


# Vhodni konektor za Teradata

Ta vodič opisuje, kako konfigurirati *digna* za povezavo s Teradata z uporabo bodisi izvornega Python-connectorja ali ODBC gonilnika.

Prikazuje zaslon **"Ustvari povezavo z bazo podatkov"**.

![Ustvari povezavo z bazo podatkov](images/data_source_config_input_mask.png)

---

## Izvorni Python gonilnik

**Knjižnica:** `teradatasql`  
**Podprto preverjanje pristnosti:** Samo preverjanje pristnosti na osnovi gesla

> ⚠️ Za druge metode preverjanja pristnosti uporabite ODBC gonilnik.

### *digna* konfiguracija (izvorni gonilnik)

Vnesite naslednje informacije v zaslonu **"Ustvari povezavo z bazo podatkov"**:

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

ODBC gonilnik lahko podpira širši nabor možnosti overjanja in povezovanja. Ta razdelek se osredotoča na preverjanje pristnosti z geslom z uporabo gonilnika **Teradata Database ODBC Driver 20.00**.

### 1. Namestite ODBC gonilnik

Namestite gonilnik **Teradata Database ODBC Driver 20.00** (ali ustreznega) v skladu z uradnim navodilom za namestitev ponudnika.

### 2. Konfigurirajte ODBC podatkovni vir

Sledite tem korakom za konfiguracijo novega ODBC podatkovnega vira z uporabo overjanja na osnovi gesla:

#### Korak 1
![Korak 1](images/teradata/create_odbc_data_source_step1.png)

Kliknite gumb **Test**.

#### Korak 2
![Korak 2](images/teradata/create_odbc_data_source_step2.png)

Vnesite uporabniško ime in geslo.

Kliknite gumb **OK**.  
Ko se prikaže zaslon s potrditvijo uspeha, je ODBC pravilno konfiguriran.

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC-povezavo, bodisi z **DSN (Data Source Name)** ali kot **konfiguracijo brez DSN**.

---

### A. DSN-bazirana konfiguracija

#### *digna* konfiguracija

V zaslonu **"Ustvari povezavo z bazo podatkov"**, vnesite naslednje:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Lastnosti ODBC

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN` mora ustrezati imenu, ki je določeno v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### *digna* konfiguracija

V zaslonu **"Ustvari povezavo z bazo podatkov"**, vnesite naslednje:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Lastnosti ODBC

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
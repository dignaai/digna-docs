---
title: PostgreSQL Connector – Integracija z bazo podatkov | digna dokumentacija
description: Pojasnjuje, kako nastaviti *digna* za povezavo s PostgreSQL z lokalnim Python gonilnikom psycopg ali PostgreSQL ODBC gonilnikom. Podpira preverjanje pristnosti z geslom za namestitve z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Povezovalnik PostgreSQL

Ta vodnik pojasnjuje, kako nastaviti *digna* za povezavo s Postgresom z lokalnim Python gonilnikom ali ODBC gonilnikom.

To se nanaša na zaslon **"Ustvari povezavo z bazo podatkov"**.

![Ustvari povezavo z bazo podatkov](images/data_source_config_input_mask.png)

---

## Lokalni Python gonilnik

**Knjižnica:** `psycopg`  
**Podprto preverjanje pristnosti:** Samo preverjanje z geslom

> ⚠️ Za druge metode preverjanja pristnosti uporabite ODBC gonilnik.

### *digna* konfiguracija (lokalni gonilnik)

Na zaslonu **"Ustvari povezavo z bazo podatkov"** vnesite naslednje podatke:

```
Technology:      Postgres
Host Address:    Ime strežnika ali IP naslov
Host Port:       Številka vrat, npr. 5432
Database Name:   Ime baze podatkov
Schema Name:     Shema, ki vsebuje izvorne podatke
User Name:       Uporabniško ime baze podatkov
User Password:   Upornikovo geslo
Use ODBC:        Onemogočeno (privzeto)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti preverjanja pristnosti in povezav. Ta razdelek se osredotoča na preverjanje z geslom z uporabo gonilnika **PostgreSQL Unicode(x64)**.

### 1. Namestite ODBC gonilnik

Namestite gonilnik **PostgreSQL Unicode(x64)** (ali podoben) in sledite uradnemu namestitvenemu vodniku dobavitelja.

### 2. Konfigurirajte ODBC vir podatkov

Za nastavitev novega ODBC vira podatkov z uporabo preverjanja z geslom sledite tem korakom:

#### Korak 1
![Korak 1](images/postgres/create_odbc_data_source_step1.png)

Opomba: Če vaša konfiguracija baze podatkov zahteva določen "SSLMode", poskrbite, da ga vključite tudi pri konfiguraciji brez DSN.

#### Korak 2 – Preizkusi povezavo

Kliknite gumb **Preizkusi povezavo**.

![Korak 2](images/postgres/create_odbc_data_source_step2.png)

---

Zdaj lahko *digna* konfigurirate za uporabo ODBC povezave; bodisi z **DSN (ime vira podatkov)** ali z **namestitvijo brez DSN**.

---

### A. Konfiguracija s DSN

#### *digna* konfiguracija

Na zaslonu **"Ustvari povezavo z bazo podatkov"** zagotovite naslednje:

```
Technology:      PostgreSQL
Database Name:   Baza podatkov, ki vsebuje ciljno shemo
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN` se mora ujemati z imenom, določenim v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### *digna* konfiguracija

Na zaslonu **"Ustvari povezavo z bazo podatkov"** zagotovite naslednje:

```
Technology:      PostgreSQL
Database Name:   Shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "ime vašega strežnika ali IP naslov"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres ali drugo ime vaše baze podatkov"
name: "UID",        value: "vaše Postgres uporabniško ime"
name: "PWD",        value: "vaše Postgres geslo"
name: "SSLMode",    value: "require"
```
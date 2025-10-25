---
title: Povezovalnik PostgreSQL – integracija baze podatkov | dokumentacija digna
description: Konfigurirajte digna za povezavo s PostgreSQL z uporabo Python drajverja psycopg ali PostgreSQL ODBC drajverja. Podpira preverjanje pristnosti z geslom z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Source Connector for PostgreSQL

Ta vodič opisuje, kako konfigurirati *digna* za povezanost s Postgresom z uporabo bodisi nativnega Python konektorja bodisi ODBC drajverja.

Navaja zaslon **"Ustvari povezavo z bazo podatkov"**.

![Ustvarite povezavo z bazo podatkov](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Supported Authentication:** Samo preverjanje pristnosti z geslom

> ⚠️ Za druge metode preverjanja pristnosti uporabite ODBC drajver.

### Konfiguracija *digna* (nativni drajver)

Vnesite naslednje podatke v zaslon **"Ustvari povezavo z bazo podatkov"**:

```
Tehnologija:      Postgres
Naslov gostitelja:    Ime strežnika ali IP naslov
Vrata gostitelja:     Številka vrat, npr. 5432
Ime baze podatkov:    Ime baze podatkov
Ime sheme:            Shema, ki vsebuje izvorne podatke
Uporabniško ime:      Uporabniško ime za bazo podatkov
Geslo uporabnika:     Geslo za uporabnika
Uporabi ODBC:         Onemogočeno (privzeto)
```

---

## ODBC Driver

ODBC drajver lahko podpira širši nabor možnosti preverjanja pristnosti in povezljivosti. Ta razdelek se osredotoča na preverjanje pristnosti z geslom z uporabo drajverja **PostgreSQL Unicode(x64)**.

### 1. Namestite ODBC drajver

Namestite **PostgreSQL Unicode(x64)** (ali podoben) tako, da sledite uradnemu priročniku za namestitev ponudnika.

### 2. Konfigurirajte ODBC vir podatkov

Sledite tem korakom za konfiguracijo novega ODBC vira podatkov z uporabo preverjanja pristnosti z geslom:

#### Korak 1
![Korak 1](images/postgres/create_odbc_data_source_step1.png)

Opomba: Če vaša nastavitev baze zahteva izbiro specifičnega "SSLMode", poskrbite, da ga uporabite tudi pri definiranju konfiguracije brez DSN.

#### Korak 2 – Preizkusite povezavo

Kliknite gumb **Preizkusi povezavo**.

![Korak 2](images/postgres/create_odbc_data_source_step2.png)

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC povezavo, bodisi z **DSN (Data Source Name)** ali z **DSN-less** konfiguracijo.

---

### A. Konfiguracija z DSN

#### Konfiguracija *digna*

V zaslonu **"Ustvari povezavo z bazo podatkov"** vnesite naslednje:

```
Tehnologija:      PostgreSQL
Ime baze podatkov:   Baza podatkov, ki vsebuje izvorno shemo
Ime sheme:           Shema, ki vsebuje izvorne podatke
Uporabi ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN` mora ustrezati imenu, določenemu v konfiguraciji vašega ODBC drajverja.

---

### B. Konfiguracija brez DSN

#### Konfiguracija *digna*

V zaslonu **"Ustvari povezavo z bazo podatkov"** vnesite naslednje:

```
Tehnologija:      PostgreSQL
Ime baze podatkov:   Shema, ki vsebuje izvorne podatke (enako kot Ime sheme)
Ime sheme:           Shema, ki vsebuje izvorne podatke
Uporabi ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "ime vašega strežnika ali IP naslov"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres ali drugo ime vaše baze"
name: "UID",        value: "vaš postgres uporabnik"
name: "PWD",        value: "vaše postgres geslo"
name: "SSLMode",    value: "require"
```
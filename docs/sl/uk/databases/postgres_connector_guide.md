---
title: Povezovalnik PostgreSQL – integracija baze podatkov | Dokumentacija digna
description: Konfigurirajte digna za povezavo s PostgreSQL z uporabo Python gonilnika psycopg ali PostgreSQL ODBC gonilnika. Podpira overjanje z geslom z nastavitvami DSN ali brez DSN.
image: /assets/logo_square.png
---


# Povezovalnik vira za PostgreSQL

Ta vodnik opisuje, kako nastaviti *digna* za povezavo s Postgresom z uporabo nativenega Python gonilnika ali ODBC gonilnika.

Navaja zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativen Python-gonilnik

**Knjižnica:** `psycopg`  
**Podprto overjanje:** samo overjanje z geslom

> ⚠️ Za druge metode overjanja uporabite ODBC gonilnik.

### *digna* — konfiguracija (nativni gonilnik)

Na zaslonu **"Create a Database Connection"** vnesite naslednje informacije:

```
Technology:      Postgres
Host Address:    Ime strežnika ali IP-naslov
Host Port:       Številka vrat, npr. 5432
Database Name:   Ime baze podatkov
Schema Name:     Shema, ki vsebuje izvorne podatke
User Name:       Ime uporabnika baze podatkov
User Password:   Geslo uporabnika
Use ODBC:        Disabled (default)
```

---

## ODBC-gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti overjanja in povezav. Ta razdelek obravnava overjanje z geslom z uporabo gonilnika **PostgreSQL Unicode(x64)**.

### 1. Namestite ODBC-gonilnik

Namestite **PostgreSQL Unicode(x64)** (ali podoben) v skladu z uradnim navodilom dobavitelja.

### 2. Nastavite ODBC vir podatkov

Sledite tem korakom za nastavitev novega ODBC vira podatkov z overjanjem z geslom:

#### Korak 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Opomba: Če vaša konfiguracija baze zahteva izbiro določenega "SSLMode", obvezno uporabite isto nastavitev pri definiranju konfiguracije brez DSN.

#### Korak 2 – Preizkus povezave

Kliknite gumb **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Zdaj lahko nastavite *digna*, da uporablja ODBC-povezavo, bodisi z **DSN (Data Source Name)**, bodisi v **DSN-less** načinu.

---

### A. Konfiguracija na osnovi DSN

#### *digna* — konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      PostgreSQL
Database Name:   Baza podatkov, ki vsebuje shemo izvora
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Enabled
```

#### Lastnosti ODBC

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN` mora biti enak imenu, določenemu v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN (DSN-less)

#### *digna* — konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      PostgreSQL
Database Name:   Shema, ki vsebuje izvorne podatke (isto kot Schema Name)
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Enabled
```

#### Lastnosti ODBC

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "ime vašega strežnika ali IP-naslov"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres ali drugo ime vaše baze podatkov"
name: "UID",        value: "vaš postgres uporabnik"
name: "PWD",        value: "vaše postgres geslo"
name: "SSLMode",    value: "require"
```
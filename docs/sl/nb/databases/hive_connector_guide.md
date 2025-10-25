---
title: Apache Hive Connector – Integracija baze podatkov | digna-dokumentacija
description: Konfigurirajte *digna* za povezavo z Apache Hive z vgrajenim gonilnikom PyHive ali Cloudera ODBC gonilnikom. Podpira overjanje z geslom ter DSN- ali DSN-less nastavitev.
image: /assets/logo_square.png
---


# Povezava vira za Hive

Ta vodnik opisuje, kako konfigurirati *digna* za povezavo s Hive z uporabo bodisi domačega Python-connectorja bodisi ODBC-gonilnika.

Navedeno je na zaslonu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Domači (native) Python-gonilnik

**Library:** `PyHive`  
**Podprte metode overjanja:** Samo overjanje z geslom

> ⚠️ Za druge metode overjanja uporabite ODBC-gonilnik.

### Konfiguracija *digna* (domači gonilnik)

Vnesite naslednje podatke na zaslonu **"Create a Database Connection"**:

```
Technology:      Apache Hive
Host Address:    Ime gostitelja ali IP-naslov
Host Port:       Številka vrat, npr. 10000
Database Name:   Shema, ki vsebuje izvorne podatke
Schema Name:     Shema, ki vsebuje izvorne podatke
User Name:       Uporabniško ime
User Password:   Geslo uporabnika
Use ODBC:        Disabled (privzeto)
```

---

## ODBC-gonilnik

ODBC-gonilnik lahko podpira širši nabor možnosti overjanja in povezovanja. Ta del se osredotoča na overjanje z geslom z uporabo gonilnika **Cloudera ODBC Driver for Apache Hive**.

### 1. Namestite ODBC-gonilnik

Namestite **Cloudera ODBC Driver for Apache Hive** (ali ustreznega) v skladu z uradnim namestitvenim navodilom proizvajalca.

### 2. Konfigurirajte ODBC-vir podatkov

Sledite tem korakom za konfiguracijo novega ODBC-viri podatkov z overjanjem z geslom:

#### Korak 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Korak 2 – Preizkusite povezavo

Vnesite geslo in kliknite gumb **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Po uspešnem testu kliknite gumb **OK**.

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC-povezavo, bodisi z **DSN (Data Source Name)** ali z **DSN-less** nastavitvijo.

---

### A. DSN-bazirana konfiguracija

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Apache Hive
Database Name:   Shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Enabled
```

#### ODBC-lastnosti

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{vaše geslo v zavitih oklepajih}"
```

> 🔹 `DSN` mora ustrezati imenu, definiranemu v konfiguraciji vašega ODBC-gonilnika.

---

### B. DSN-less konfiguracija

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Apache Hive
Database Name:   Shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Enabled
```

#### ODBC-lastnosti

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "vaše ime strežnika ali IP-naslov"
name: "PORT",       value: "Številka vrat, npr. 10000"
name: "Schema",     value: "Shema, ki vsebuje izvorne podatke"
name: "UID",        value: "vaš hive uporabnik"
name: "PWD",        value: "vaše hive geslo"
name: "AuthMech",   value: "3"
```
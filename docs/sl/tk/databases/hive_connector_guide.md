---
title: Apache Hive Povezovalnik – Integracija baze podatkov | digna Dokumentacija
description: Konfiguracija digna za povezavo z Apache Hive z uporabo lokalnega PyHive gonilnika ali Cloudera ODBC gonilnika. Podpira preverjanje pristnosti z geslom in nastavitve z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Povezovalnik vira za Hive

Ta vodnik pojasnjuje, kako konfigurirati *digna*, da se poveže z Hive z uporabo lokalnega Python gonilnika ali ODBC gonilnika.

To se nanaša na zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Lokalni Python gonilnik

**Knjižnica:** `PyHive`  
**Podprto preverjanje pristnosti:** samo preverjanje pristnosti z geslom

> ⚠️ Za druge načine preverjanja pristnosti uporabite ODBC gonilnik.

### *digna* konfiguracija (lokalni gonilnik)

Vnesite naslednje podatke na zaslonu **"Create a Database Connection"**:

```
Technology:      Apache Hive
Host Address:    ime strežnika ali IP naslov
Host Port:       številka vrat, npr. 10000
Database Name:   shema, ki vsebuje izvorne podatke
Schema Name:     shema, ki vsebuje izvorne podatke
User Name:       uporabniško ime za bazo podatkov
User Password:   geslo za uporabnika
Use ODBC:        Izklopljeno (privzeto)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti preverjanja pristnosti in povezovanja. Ta razdelek se osredotoča na preverjanje pristnosti z geslom z uporabo gonilnika **Cloudera ODBC Driver for Apache Hive**.

### 1. Namestite ODBC gonilnik

Namestite **Cloudera ODBC Driver for Apache Hive** (ali podoben) v skladu z uradnim navodilom proizvajalca.

### 2. Konfigurirajte ODBC vir podatkov

Za konfiguracijo novega ODBC vira podatkov z uporabo preverjanja pristnosti z geslom sledite tem korakom:

#### Korak 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Korak 2 – Preizkusite povezavo

Vnesite geslo in kliknite gumb **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Po uspešnem preizkusu kliknite **OK**.

---

Zdaj lahko *digna* konfigurirate za uporabo ODBC povezave; bodisi z **DSN (Data Source Name)** ali z namestitvijo **brez DSN**.

---

### A. Konfiguracija z DSN

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Apache Hive
Database Name:   shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:     shema, ki vsebuje izvorne podatke
Use ODBC:        Vklopljeno
```

#### ODBC lastnosti

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{vaše geslo v zavitih oklepajih}"
```

> 🔹 `DSN` se mora ujemati z imenom, definiranim v vaši konfiguraciji ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Apache Hive
Database Name:   shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:     shema, ki vsebuje izvorne podatke
Use ODBC:        Vklopljeno
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "ime strežnika ali njegov IP naslov"
name: "PORT",       value: "številka vrat, npr. 10000"
name: "Schema",     value: "shema, ki vsebuje izvorne podatke"
name: "UID",        value: "your hive user"
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```
---
title: Povezava z Netezza – Integracija baze podatkov | digna-dokumentacija
description: Konfigurirajte digna za povezavo z Netezza z uporabo ODBC gonilnika NetezzaSQL. Podpira overjanje z geslom z uporabo DSN ali DSN-less nastavitve za prilagodljivo povezljivost.
image: /assets/logo_square.png
---


# Source Connector for Netezza

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Netezza z uporabo ODBC gonilnika.

Sklicuje se na zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC gonilnik

ODBC gonilnik lahko podpira več možnosti overjanja in povezovanja. Ta razdelek se osredotoča na overjanje z geslom z uporabo gonilnika **NetezzaSQL**.

### 1. Namestite ODBC gonilnik

Namestite gonilnik **NetezzaSQL** (ali ustreznega) v skladu z uradnim navodilom za namestitev dobavitelja.

### 2. Konfigurirajte ODBC podatkovni vir

Sledite tem korakom za konfiguracijo novega ODBC podatkovnega vira z overjanjem z geslom:

#### Korak 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Odvisno od vašega Netezza gonilnika, nastavitev in varnostnih zahtev, boste morda morali podatke vnesti tudi v zavihkih **Advanced DSN Options**, **SSL DSN Options** ali **Driver Options**. Za najpreprostejšo nastavitev zadostuje vnos podatkov v **DSN Options**.

Kliknite gumb **Test Connection**.

#### Korak 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Ko se prikaže zaslon o uspehu, je ODBC pravilno konfiguriran.

---

Zdaj lahko konfigurirate *digna*, da uporabi ODBC povezavo, bodisi z **DSN (Data Source Name)** ali z **DSN-less** nastavitvijo.

---

### A. Konfiguracija z DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"**, vnesite naslednje:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN` mora ustrezati imenu, ki je določeno v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN (DSN-less)

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"**, vnesite naslednje:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
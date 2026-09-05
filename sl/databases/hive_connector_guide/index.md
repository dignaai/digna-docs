# Povezovalnik vira za Hive

Ta vodnik opisuje, kako konfigurirati *digna*, da se poveže z Hive z uporabo izvornega Python konektorja ali ODBC gonilnika.

Sklicuje se na zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Izvorni Python gonilnik

**Knjižnica:** `PyHive`  
**Podprto overjanje:** Samo overjanje z geslom

> Za druge metode overjanja uporabite ODBC gonilnik.

### Konfiguracija *digna* (izvorni gonilnik)

Na zaslonu **"Create a Database Connection"** vnesite naslednje podatke:

```
Technology:      Apache Hive
Host Address:    Ime strežnika ali IP naslov
Host Port:       Številka vrat, npr. 10000
Database Name:   Shema, ki vsebuje izvorne podatke
Schema Name:     Shema, ki vsebuje izvorne podatke
User Name:       Uporabniško ime podatkovne baze
User Password:   Geslo za uporabnika
Use ODBC:        Onemogočeno (privzeto)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti overjanja in povezljivosti. Ta razdelek se osredotoča na overjanje z geslom z uporabo gonilnika **Cloudera ODBC Driver for Apache Hive**.

### 1. Namestite ODBC gonilnik

Namestite **Cloudera ODBC Driver for Apache Hive** (ali podoben) v skladu z uradnim navodilom proizvajalca za namestitev.

### 2. Konfigurirajte ODBC podatkovni vir

Sledite tem korakom za konfiguracijo novega ODBC podatkovnega vira z uporabo overjanja z geslom:

#### Korak 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Korak 2 – Preizkus povezave

Vnesite geslo in kliknite gumb **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Po uspešnem preizkusu kliknite gumb **OK**.

---

Zdaj lahko konfigurirate *digna*, da uporabi ODBC povezavo, bodisi z **DSN (Data Source Name)** ali z **brez-DSN** nastavitvijo.

---

### A. Konfiguracija z DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Apache Hive
Database Name:   Shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN` se mora ujemati z imenom, določenim v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Apache Hive
Database Name:   Shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "ime vašega strežnika ali IP naslov"
name: "PORT",       value: "Številka vrat, npr. 10000"
name: "Schema",     value: "Shema, ki vsebuje izvorne podatke"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```
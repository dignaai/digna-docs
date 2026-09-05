# Povezovalnik vira za Databricks - brez Unity Catalog

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Databricks z uporabo bodisi izvornega Python konektorja ali ODBC gonilnika.

Navaja se zaslon **"Create a Database Connection"**.

![Ustvarjanje povezave na bazo podatkov](images/data_source_config_input_mask.png)

---

## Izvorni Python gonilnik

**Knjižnica:** `databricks-sql-connector`  
**Podprta avtentikacija:** osebni dostopni žeton (PAT) samo

> Za druge metode avtentikacije uporabite ODBC gonilnik.

### Osebni dostopni žeton (PAT)

Za avtentikacijo z osebnim dostopnim žetonom se sklicujte na uradno dokumentacijo Databricks:  
[Kako pridobiti PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### Konfiguracija *digna* (izvorni gonilnik)

Vnesite naslednje podatke v zaslon **"Create a Database Connection"**:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, npr. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Ta parameter ni v uporabi za Databricks brez Unity Catalog
Schema Name:     Shema, ki vsebuje izvorne podatke
User Name:       HTTP Path, ki ga zagotavlja Databricks, npr. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Osebni dostopni žeton, npr. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Onemogočeno (privzeto)
```

---

## ODBC gonilnik

ODBC gonilnik podpira širši nabor možnosti avtentikacije in povezljivosti. Ta razdelek se osredotoča na avtentikacijo na podlagi žetona z uporabo **Simba Spark ODBC Driver**.

### 1. Namestite ODBC gonilnik

Namestite **Simba Spark ODBC Driver** po uradnem navodilu proizvajalca.

### 2. Konfigurirajte ODBC vir podatkov

Sledite tem korakom za konfiguracijo novega ODBC vira podatkov z uporabo osebnega dostopnega žetona:

#### Korak 1
![Korak 1](images/databricks/create_odbc_data_source_step1.png)

#### Korak 2
![Korak 2](images/databricks/create_odbc_data_source_step2.png)

#### Korak 3
![Korak 3](images/databricks/create_odbc_data_source_step3.png)

#### Korak 4
![Korak 4](images/databricks/create_odbc_data_source_step4.png)

#### Korak 5 – Testirajte povezavo

Kliknite gumb **TEST**. Uspešna povezava bi morala izgledati tako:

![Korak 5](images/databricks/create_odbc_data_source_step5.png)

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC povezavo, bodisi z **DSN (Data Source Name)** ali z **DSN-less** nastavitvijo.

---

### A. Konfiguracija na osnovi DSN

#### Konfiguracija *digna*

V zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Databricks (Legacy)
Database Name:   Ta parameter ni v uporabi za Databricks brez Unity Catalog
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DSN",    value: "*digna*data_databricks"
```

> Vrednost `DSN` se mora ujemati z imenom, definiranem v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### Konfiguracija *digna*

V zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Databricks (Legacy)
Database Name:   Ta parameter ni v uporabi za Databricks brez Unity Catalog
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
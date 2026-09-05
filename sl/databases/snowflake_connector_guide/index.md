# Vhodni konektor za Snowflake

Ta vodič opisuje, kako konfigurirati *digna*, da se poveže s Snowflake z uporabo bodisi nativnega Python connectorja bodisi ODBC gonilnika.

Navaja se zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativni Python gonilnik

**Library:** `snowflake-connector-python`  
**Podprta avtentikacija:** samo avtentikacija z geslom

> Za druge metode avtentikacije uporabite ODBC gonilnik.

### *digna* konfiguracija (nativni gonilnik)

Vnesite naslednje informacije na zaslonu **"Create a Database Connection"**:

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
User Name:       User name and warehouse in the format "user<@>warehouse"
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti za avtentikacijo in povezljivost. Ta razdelek se osredotoča na avtentikacijo z geslom z uporabo **SnowflakeDSIIDriver**.

### 1. Namestite ODBC gonilnik

Namestite **SnowflakeDSIIDriver** po uradnem vodiču ponudnika.

### 2. Konfigurirajte ODBC vir podatkov

Sledite tem korakom za konfiguracijo novega ODBC vira podatkov z avtentikacijo z geslom:

#### Korak 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Opombe: 
- Če ne vnesete vrednosti za Database, Schema in Warehouse, boste morali te podatke zagotoviti kot ODBC lastnosti med konfiguracijo vira podatkov v *digna*.
- Vrednost za "Server" je sestavljena iz imena vašega Snowflake računa, za njim pa sledi ".snowflakecomputing.com"

#### Korak 2 – Preizkusite povezavo

Kliknite gumb **TEST**. Uspešna povezava bi morala izgledati tako:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC povezavo, bodisi z **DSN (Data Source Name)** ali v **brez-DSN** konfiguraciji.

---

### A. Konfiguracija z DSN

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> `DSN` se mora ujemati z imenom, definiranim v vaši ODBC konfiguraciji.

---

### B. Konfiguracija brez DSN

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```
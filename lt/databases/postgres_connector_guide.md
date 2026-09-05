# Source Connector for PostgreSQL

Šiame vadove aprašoma, kaip sukonfigūruoti *digna* jungtį prie Postgres naudojant arba natyvų Python jungtį, arba ODBC draiverį.

Jame nurodoma ekrano dalis **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Supported Authentication:** Tik autentifikacija su slaptažodžiu

> Jei naudojate kitus autentifikacijos metodus, prašome naudoti ODBC draiverį.

### *digna* Configuration (Native Driver)

Pateikite šią informaciją ekrane **"Create a Database Connection"**:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC draiveris gali palaikyti platesnį autentifikacijos ir ryšio parinkčių spektrą. Šiame skyriuje aptariama autentifikacija su slaptažodžiu naudojant draiverį **PostgreSQL Unicode(x64)**.

### 1. Įdiekite ODBC draiverį

Įdiekite **PostgreSQL Unicode(x64)** (ar panašų) vadovaudamiesi tiekėjo oficialia instaliacijos instrukcija.

### 2. Konfigūruokite ODBC duomenų šaltinį

Atlikite šiuos veiksmus, kad sukonfigūruotumėte naują ODBC duomenų šaltinį, naudojant autentifikaciją su slaptažodžiu:

#### Step 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Pastaba: jei jūsų duomenų bazės konfigūracija reikalauja pasirinkti konkretų "SSLMode", įsitikinkite, kad jį taip pat nurodote apibrėždami DSN-less konfigūraciją.

#### Step 2 – Test the connection

Spustelėkite mygtuką **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Dabar galite sukonfigūruoti *digna* naudoti ODBC ryšį, arba su **DSN (Data Source Name)**, arba be DSN (DSN-less).

---

### A. DSN-Based Configuration

#### *digna* Configuration

Ekrane **"Create a Database Connection"** nurodykite:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "PostgreSQL35W"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

Ekrane **"Create a Database Connection"** nurodykite:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```
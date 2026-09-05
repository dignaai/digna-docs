# Avota savienotājs priekš Snowflake

Šajā ceļvedī aprakstīts, kā konfigurēt *digna*, lai izveidotu savienojumu ar Snowflake, izmantojot vai nu nativu Python connector, vai ODBC driver.

Tas attiecas uz ekrānu **"Create a Database Connection"**.

![Izveidot datubāzes savienojumu](images/data_source_config_input_mask.png)

---

## Nativais Python draiveris

**Bibliotēka:** `snowflake-connector-python`  
**Atbalstītā autentifikācija:** Tikai paroles autentifikācija

> Lai izmantotu citas autentifikācijas metodes, lūdzu izmantojiet ODBC driver.

### *digna* konfigurācija (nativais draiveris)

Norādiet sekojošo informāciju ekrānā **"Create a Database Connection"**:

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

## ODBC draiveris

ODBC draiveris var atbalstīt plašāku autentifikācijas un savienojamības iespēju spektru. Šī sadaļa fokusējas uz paroles autentifikāciju, izmantojot **SnowflakeDSIIDriver**.

### 1. Instalējiet ODBC draiveri

Instalējiet **SnowflakeDSIIDriver**, sekojot ražotāja oficiālajai instalācijas instrukcijai.

### 2. Konfigurējiet ODBC datu avotu

Izpildiet šīs darbības, lai konfigurētu jaunu ODBC datu avotu, izmantojot paroles autentifikāciju:

#### 1. solis
![1. solis](images/snowflake/create_odbc_data_source_step1.png)

Piezīmes:
- Ja nenorādīsiet vērtības laukiem Database, Schema un Warehouse, tad tās būs jānorāda kā ODBC rekvizīti *digna* datu avota konfigurācijas laikā.
- Vērtība lauka "Server" sastāv no jūsu Snowflake konta nosaukuma, kam seko ".snowflakecomputing.com"

#### 2. solis – Savienojuma pārbaude

Nospiediet pogu **TEST**. Veiksmīgs savienojums izskatīsies šādi:

![2. solis](images/snowflake/create_odbc_data_source_step2.png)

---

Tagad varat konfigurēt *digna*, lai izmantotu ODBC savienojumu, vai nu ar **DSN (Data Source Name)**, vai ar **bez-DSN** risinājumu.

---

### A. DSN pamatā balstīta konfigurācija

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC rekvizīti

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> `DSN` jāatbilst nosaukumam, kas definēts jūsu ODBC driver konfigurācijā.

---

### B. Bez-DSN konfigurācija

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC rekvizīti

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```
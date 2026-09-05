# Source Connector for Snowflake

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Snowflake antingen med den inbyggda Python-connectorn eller med ODBC-drivrutinen.

Den hänvisar till skärmen **"Skapa en databasanslutning"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `snowflake-connector-python`  
**Stödd autentisering:** Endast lösenordsbaserad autentisering

> För andra autentiseringsmetoder, använd ODBC-drivrutinen.

### *digna* Konfiguration (Native Driver)

Ange följande information i skärmen **"Skapa en databasanslutning"**:

```
Teknik:          Snowflake
Värdaddress:     Snowflake-kontots namn
Värdport:        Behövs inte
Databasnamn:     Databasen som innehåller källschemat
Schemnamn:       Schemat som innehåller källdata
Användarnamn:    Användarnamn och warehouse i formatet "user<@>warehouse"
Användarlösenord: Lösenord för användaren
Använd ODBC:     Inaktiverad (standard)
```

---

## ODBC Driver

ODBC-drivrutinen kan stödja ett bredare utbud av autentiserings- och anslutningsalternativ. Denna sektion fokuserar på lösenordsbaserad autentisering med **SnowflakeDSIIDriver**.

### 1. Installera ODBC-drivrutinen

Installera **SnowflakeDSIIDriver** genom att följa leverantörens officiella installationsguide.

### 2. Konfigurera ODBC-datakällan

Följ stegen nedan för att konfigurera en ny ODBC-datakälla med lösenordsbaserad autentisering:

#### Steg 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Noter:
- Om du inte anger värden för Database, Schema och Warehouse måste du ange dem som ODBC-egenskaper när du konfigurerar datakällan i *digna*.
- Värdet för "Server" består av ditt Snowflake-kontons namn följt av ".snowflakecomputing.com"

#### Steg 2 – Testa anslutningen

Klicka på **TEST**-knappen. En lyckad anslutning ser ut så här:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Nu kan du konfigurera *digna* att använda ODBC-anslutningen, antingen med en **DSN (Data Source Name)** eller en **DSN-less** konfiguration.

---

### A. DSN-baserad konfiguration

#### *digna* Konfiguration

I skärmen **"Skapa en databasanslutning"** ange följande:

```
Teknik:          Snowflake
Databasnamn:     Databasen som innehåller källschemat
Schemnamn:       Schemat som innehåller källdata
Använd ODBC:     Aktiverad
```

#### ODBC-egenskaper

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{ditt lösenord inom måsvingar}"

valfritt:
name: "Database",       value: "Databasen som innehåller källschemat"
name: "Schema",         value: "Schemat som innehåller källdata"
name: "Warehouse",      value: "Warehouse som ska användas för körning av SQL"
```

> `DSN` måste matcha det namn som definierats i din ODBC-drivrutinskonfiguration.

---

### B. DSN-less konfiguration

#### *digna* Konfiguration

I skärmen **"Skapa en databasanslutning"** ange följande:

```
Teknik:          Snowflake
Databasnamn:     Schemat som innehåller källdata (samma som Schemnamn)
Schemnamn:       Schemat som innehåller källdata
Använd ODBC:     Aktiverad
```

#### ODBC-egenskaper

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Databasen som innehåller källschemat"
name: "Schema",     value: "Schemat som innehåller källdata"
name: "Warehouse",  value: "Warehouse som ska användas för körning av SQL"
```
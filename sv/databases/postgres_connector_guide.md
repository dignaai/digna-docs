# Källanslutning för PostgreSQL

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Postgres med antingen den inbyggda Python-anslutningen eller ODBC-drivrutinen.

Det hänvisar till skärmen **"Create a Database Connection"**.

![Skapa en databasanslutning](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Supported Authentication:** Endast lösenordsbaserad autentisering

> För andra autentiseringsmetoder, använd ODBC-drivrutinen.

### *digna* Konfiguration (Native Driver)

Fyll i följande information på skärmen **"Create a Database Connection"**:

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

ODBC-drivrutinen kan stödja ett bredare utbud av autentiserings- och anslutningsalternativ. Detta avsnitt fokuserar på lösenordsbaserad autentisering med drivrutinen **PostgreSQL Unicode(x64)**.

### 1. Installera ODBC-drivrutinen

Installera **PostgreSQL Unicode(x64)** (eller motsvarande) genom att följa leverantörens officiella installationsguide.

### 2. Konfigurera ODBC-datakällan

Följ dessa steg för att konfigurera en ny ODBC-datakälla med lösenordsbaserad autentisering:

#### Steg 1
![Steg 1](images/postgres/create_odbc_data_source_step1.png)

Notera: Om din databaskonfiguration kräver att du väljer en specifik "SSLMode", se till att använda samma inställning när du definierar en DSN-lös konfiguration.

#### Steg 2 – Testa anslutningen

Klicka på knappen **Test Connection**.

![Steg 2](images/postgres/create_odbc_data_source_step2.png)

---

Nu kan du konfigurera *digna* att använda ODBC-anslutningen, antingen med en **DSN (Data Source Name)** eller en **DSN-less** konfiguration.

---

### A. DSN-baserad konfiguration

#### *digna* Konfiguration

På skärmen **"Create a Database Connection"** ange följande:

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

> `DSN` måste matcha namnet som definierats i din ODBC-drivrutinskonfiguration.

---

### B. DSN-less konfiguration

#### *digna* Konfiguration

På skärmen **"Create a Database Connection"** ange följande:

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
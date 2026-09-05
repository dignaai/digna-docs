# Källanslutare för Oracle

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Oracle DB med antingen den inbyggda Python-anslutningen eller ODBC-drivrutinen.

It refers to the screen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Inbyggd Python-drivrutin

**Library:** `python-oracledb`  
**Stödd autentisering:** Endast lösenordsbaserad autentisering

> För andra autentiseringsmetoder, använd ODBC-drivrutinen.

### *digna* konfiguration (inbyggd drivrutin)

Fyll i följande information i skärmen **"Create a Database Connection"**:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-drivrutin

ODBC-drivrutinen kan stödja ett bredare urval av autentiserings- och anslutningsalternativ. Den här sektionen fokuserar på lösenordsbaserad autentisering med drivrutinen **Oracle in OraDB21Home1**.

### 1. Installera ODBC-drivrutinen

Installera **Oracle in OraDB21Home1** (eller liknande) genom att följa leverantörens officiella installationsguide.

### 2. Konfigurera ODBC-datakällan

Följ dessa steg för att konfigurera en ny ODBC-datakälla med lösenordsbaserad autentisering:

#### Step 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Obs:
TNS Service Name måste konfigureras i tnsnames.ora-filen i din Oracle-klientinstallation. Det är här du anger anslutningsbeskrivningen (host, port, service name).

#### Step 2 – Test the connection

Klicka på knappen **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Ange lösenordet och klicka på **OK**-knappen.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Nu kan du konfigurera *digna* att använda ODBC-anslutningen, antingen med en **DSN (Data Source Name)** eller en **konfiguration utan DSN**.

---

### A. DSN-baserad konfiguration

#### *digna* konfiguration

I skärmen **"Create a Database Connection"**, ange följande:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. Konfiguration utan DSN

#### *digna* konfiguration

I skärmen **"Create a Database Connection"**, ange följande:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```
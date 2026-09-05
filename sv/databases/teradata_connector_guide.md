# Källaanslutning för Teradata

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Teradata med antingen den inbyggda Python-anslutaren eller ODBC-drivrutinen.

Den hänvisar till skärmen **"Create a Database Connection"**.

![Skapa en databasanslutning](images/data_source_config_input_mask.png)

---

## Inbyggd Python-drivrutin

**Library:** `teradatasql`  
**Stödd autentisering:** Endast lösenordsbaserad autentisering

> För andra autentiseringsmetoder, använd ODBC-drivrutinen.

### *digna*-konfiguration (inbyggd drivrutin)

Ange följande information i skärmen **"Create a Database Connection"**:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-drivrutin

ODBC-drivrutinen kan stödja ett bredare utbud av autentiserings- och anslutningsalternativ. Denna sektion fokuserar på lösenordsbaserad autentisering med drivrutinen **Teradata Database ODBC Driver 20.00**.

### 1. Installera ODBC-drivrutinen

Installera drivrutinen **Teradata Database ODBC Driver 20.00** (eller liknande) enligt leverantörens officiella installationsguide.

### 2. Konfigurera ODBC-datakällan

Följ dessa steg för att konfigurera en ny ODBC-datakälla med lösenordsbaserad autentisering:

#### Steg 1
![Steg 1](images/teradata/create_odbc_data_source_step1.png)

Klicka på knappen **Test**.

#### Steg 2
![Steg 2](images/teradata/create_odbc_data_source_step2.png)

Ange användarnamn och lösenord.

Klicka på knappen **OK**.
När du ser framgångsskärmen är ODBC korrekt konfigurerat.

---

Nu kan du konfigurera *digna* att använda ODBC-anslutningen, antingen med en **DSN (Data Source Name)** eller en **DSN-less** konfiguration.

---

### A. DSN-baserad konfiguration

#### Konfiguration för *digna*

I skärmen **"Create a Database Connection"** ange följande:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN` måste stämma överens med namnet som definierats i din ODBC-drivrutinskonfiguration.

---

### B. DSN-lös konfiguration

#### Konfiguration för *digna*

I skärmen **"Create a Database Connection"** ange följande:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
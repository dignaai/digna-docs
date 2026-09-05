# Source Connector for Netezza

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at forbinde til Netezza ved hjælp af ODBC-driveren.

Den henviser til skærmen **"Create a Database Connection"**.

![Opret en databaseforbindelse](images/data_source_config_input_mask.png)

---

## ODBC Driver

ODBC-driveren kan understøtte forskellige autentificerings- og forbindelsesmuligheder. Dette afsnit fokuserer på adgangskodebaseret autentificering ved brug af driveren **NetezzaSQL**.

### 1. Installér ODBC-driveren

Installer driveren **NetezzaSQL** (eller lignende) ved at følge leverandørens officielle installationsvejledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trin for at konfigurere en ny ODBC-datakilde ved brug af adgangskodebaseret autentificering:

#### Trin 1
![Trin 1](images/netezza/create_odbc_data_source_step1.png)

Afhængigt af din Netezza-driver, opsætning og sikkerhedskrav kan det være nødvendigt også at angive data i fanerne **Advanced DSN Options**, **SSL DSN Options** eller **Driver Options**. For den simpleste opsætning er det tilstrækkeligt at angive data i **DSN Options**.

Klik på knappen **Test Connection**.

#### Trin 2
![Trin 2](images/netezza/create_odbc_data_source_step2.png)

Når du modtager succesbeskeden, er ODBC konfigureret korrekt.

---

Nu kan du konfigurere *digna* til at bruge ODBC-forbindelsen, enten med en **DSN (Data Source Name)** eller en **DSN-less** opsætning.

---

### A. DSN-baseret konfiguration

#### *digna* Konfiguration

På skærmen **"Create a Database Connection"**, angiv følgende:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN` skal matche navnet defineret i din ODBC-driverkonfiguration.

---

### B. DSN-less konfiguration

#### *digna* Konfiguration

På skærmen **"Create a Database Connection"**, angiv følgende:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
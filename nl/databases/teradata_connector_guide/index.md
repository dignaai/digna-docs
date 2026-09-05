# Bronconnector voor Teradata

Deze gids beschrijft hoe u *digna* configureert om verbinding te maken met Teradata met behulp van de native Python-connector of de ODBC-driver.

Het verwijst naar het scherm **"Create a Database Connection"**.

![Maak een databaseverbinding](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `teradatasql`  
**Ondersteunde authenticatie:** Alleen wachtwoordgebaseerde authenticatie

> Voor andere authenticatiemethoden gebruikt u de ODBC-driver.

### *digna* configuratie (native driver)

Vul de volgende informatie in op het scherm **"Create a Database Connection"**:

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

## ODBC Driver

De ODBC-driver ondersteunt mogelijk een breder scala aan authenticatie- en verbindingsopties. Deze sectie richt zich op wachtwoordgebaseerde authenticatie met de driver **Teradata Database ODBC Driver 20.00**.

### 1. Installeer de ODBC-driver

Installeer de driver **Teradata Database ODBC Driver 20.00** (of vergelijkbaar) door de officiële installatiehandleiding van de leverancier te volgen.

### 2. Configureer de ODBC-datasource

Volg deze stappen om een nieuwe ODBC-datasource te configureren met wachtwoordgebaseerde authenticatie:

#### Stap 1
![Stap 1](images/teradata/create_odbc_data_source_step1.png)

Klik op de knop **Test**.

#### Stap 2
![Stap 2](images/teradata/create_odbc_data_source_step2.png)

Voer gebruikersnaam en wachtwoord in.

Klik op de knop **OK**.  
Wanneer u het succesvenster ziet, is ODBC correct geconfigureerd.

---

Nu kunt u *digna* configureren om de ODBC-verbinding te gebruiken, ofwel met een **DSN (Data Source Name)** of een **DSN-loze** configuratie.

---

### A. DSN-gebaseerde configuratie

#### *digna* configuratie

Vul op het scherm **"Create a Database Connection"** het volgende in:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-eigenschappen

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> De `DSN` moet overeenkomen met de naam die is gedefinieerd in uw ODBC-driverconfiguratie.

---

### B. DSN-loze configuratie

#### *digna* configuratie

Vul op het scherm **"Create a Database Connection"** het volgende in:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-eigenschappen

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
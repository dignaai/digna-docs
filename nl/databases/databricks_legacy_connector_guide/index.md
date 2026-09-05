# Bronconnector voor Databricks - zonder Unity Catalog

Deze gids beschrijft hoe je *digna* configureert om verbinding te maken met Databricks met behulp van de native Python-connector of de ODBC-driver.

Het verwijst naar het scherm **"Create a Database Connection"**.

![Maak een databaseverbinding](images/data_source_config_input_mask.png)

---

## Native Python-driver

**Library:** `databricks-sql-connector`  
**Ondersteunde authenticatie:** alleen Personal Access Token (PAT)

> Voor andere authenticatiemethoden, gebruik de ODBC-driver.

### Personal Access Token (PAT)

Om te authenticeren met een Personal Access Token, raadpleeg de officiële Databricks-documentatie:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* configuratie (native driver)

Geef de volgende informatie op in het scherm **"Create a Database Connection"**:

```
Technologie:      Databricks (Legacy)
Hostadres:        Databricks-hostnaam, bijv. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Hostpoort:        443
Databasenaam:     Deze parameter wordt niet gebruikt voor Databricks zonder Unity Catalog
Schemanaam:       Schema met de brongegevens
Gebruikersnaam:   HTTP-pad verstrekt door Databricks, bijv. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
Wachtwoord gebruiker: Personal Access Token, bijv. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Gebruik ODBC:     Uitgeschakeld (standaard)
```

---

## ODBC-driver

De ODBC-driver ondersteunt een breder scala aan authenticatie- en connectiviteitsopties. Deze sectie richt zich op token-gebaseerde authenticatie met de **Simba Spark ODBC Driver**.

### 1. Installeer de ODBC-driver

Installeer de **Simba Spark ODBC Driver** door de officiële installatiehandleiding van de leverancier te volgen.

### 2. Configureer de ODBC-gegevensbron

Volg deze stappen om een nieuwe ODBC-datasource te configureren met een Personal Access Token:

#### Stap 1
![Stap 1](images/databricks/create_odbc_data_source_step1.png)

#### Stap 2
![Stap 2](images/databricks/create_odbc_data_source_step2.png)

#### Stap 3
![Stap 3](images/databricks/create_odbc_data_source_step3.png)

#### Stap 4
![Stap 4](images/databricks/create_odbc_data_source_step4.png)

#### Stap 5 – Test de verbinding

Klik op de **TEST**-knop. Een succesvolle verbinding ziet er zo uit:

![Stap 5](images/databricks/create_odbc_data_source_step5.png)

---

Nu kun je *digna* configureren om de ODBC-verbinding te gebruiken, ofwel met een **DSN (Data Source Name)** of een **DSN-less** configuratie.

---

### A. DSN-gebaseerde configuratie

#### *digna* configuratie

Geef in het scherm **"Create a Database Connection"** het volgende op:

```
Technologie:      Databricks (Legacy)
Databasenaam:     Deze parameter wordt niet gebruikt voor Databricks zonder Unity Catalog
Schemanaam:       Schema met de brongegevens
Gebruik ODBC:     Ingeschakeld
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> De `DSN` moet overeenkomen met de naam die in je ODBC-driverconfiguratie is gedefinieerd.

---

### B. DSN-less configuratie

#### *digna* configuratie

Geef in het scherm **"Create a Database Connection"** het volgende op:

```
Technologie:      Databricks (Legacy)
Databasenaam:     Deze parameter wordt niet gebruikt voor Databricks zonder Unity Catalog
Schemanaam:       Schema met de brongegevens
Gebruik ODBC:     Ingeschakeld
```

#### ODBC Properties

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
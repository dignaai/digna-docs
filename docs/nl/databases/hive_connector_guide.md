---
title: Apache Hive-connector – Database-integratie | digna-documentatie
description: Configureer digna om verbinding te maken met Apache Hive met de native PyHive-driver of de Cloudera ODBC-driver. Ondersteunt wachtwoordgebaseerde authenticatie en DSN- of DSN-loze configuraties.
image: /assets/logo_square.png
---


# Source Connector voor Hive

Deze gids beschrijft hoe u *digna* configureert om verbinding te maken met Hive met behulp van de native Python-connector of de ODBC-driver.

It verwijst naar het scherm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `PyHive`  
**Ondersteunde authenticatie:** Alleen wachtwoordgebaseerde authenticatie

> Voor andere authenticatiemethoden gebruikt u de ODBC-driver.

### *digna* Configuratie (Native Driver)

Geef de volgende informatie op in het scherm **"Create a Database Connection"**:

```
Technologie:      Apache Hive
Hostadres:        Servernaam of IP-adres
Hostpoort:        Poortnummer, bijv. 10000
Databasenaam:     Schema dat de brongegevens bevat
Schemanaam:       Schema dat de brongegevens bevat
Gebruikersnaam:   Databasenaam gebruiker
Wachtwoord:       Wachtwoord voor de gebruiker
Gebruik ODBC:     Uitgeschakeld (standaard)
```

---

## ODBC Driver

De ODBC-driver kan een breder scala aan authenticatie- en connectiviteitsopties ondersteunen. Deze sectie richt zich op wachtwoordgebaseerde authenticatie met de driver **Cloudera ODBC Driver for Apache Hive**.

### 1. Installeer de ODBC-driver

Installeer de **Cloudera ODBC Driver for Apache Hive** (of een vergelijkbare driver) door de officiële installatiehandleiding van de leverancier te volgen.

### 2. Configureer de ODBC-datasource

Volg deze stappen om een nieuwe ODBC-datasource te configureren met wachtwoordgebaseerde authenticatie:

#### Stap 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Stap 2 – Test de verbinding

Voer het wachtwoord in en klik op de knop **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Na een succesvolle test klikt u op de knop **OK**.

---

Nu kunt u *digna* configureren om de ODBC-verbinding te gebruiken, ofwel met een **DSN (Data Source Name)** of een **DSN-loze** configuratie.

---

### A. DSN-gebaseerde configuratie

#### *digna* Configuratie

In het scherm **"Create a Database Connection"** geeft u het volgende op:

```
Technologie:      Apache Hive
Databasenaam:     Schema dat de brongegevens bevat (zelfde als Schemanaam)
Schemanaam:       Schema dat de brongegevens bevat
Gebruik ODBC:     Ingeschakeld
```

#### ODBC-eigenschappen

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{uw wachtwoord tussen accolades}"
```

> De `DSN` moet overeenkomen met de naam die is gedefinieerd in uw ODBC-driverconfiguratie.

---

### B. DSN-loze configuratie

#### *digna* Configuratie

In het scherm **"Create a Database Connection"** geeft u het volgende op:

```
Technologie:      Apache Hive
Databasenaam:     Schema dat de brongegevens bevat (zelfde als Schemanaam)
Schemanaam:       Schema dat de brongegevens bevat
Gebruik ODBC:     Ingeschakeld
```

#### ODBC-eigenschappen

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "uw servernaam of IP-adres"
name: "PORT",       value: "Poortnummer, bijv. 10000"
name: "Schema",     value: "Schema dat de brongegevens bevat"
name: "UID",        value: "uw hive-gebruiker"
name: "PWD",        value: "uw hive-wachtwoord"
name: "AuthMech",   value: "3"
```
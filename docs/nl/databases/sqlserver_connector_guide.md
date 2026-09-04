---
title: MS SQL Server-connector – Database-integratie | digna-documentatie
description: Configureer digna om verbinding te maken met Microsoft SQL Server met behulp van de pymssql Python-driver of de SQL Server ODBC-driver. Ondersteunt wachtwoordgebaseerde authenticatie met DSN- of DSN-less-configuraties.
image: /assets/logo_square.png
---


# Bronconnector voor MS SQL Server

Deze handleiding beschrijft hoe u *digna* configureert om verbinding te maken met SQL Server met behulp van de native Python-connector of de ODBC-driver.

Dit heeft betrekking op het scherm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python-driver

**Library:** `pymssql`  
**Ondersteunde authenticatie:** Alleen wachtwoordgebaseerde authenticatie

> Voor andere authenticatiemethoden, gebruik de ODBC-driver.

### *digna* configuratie (native driver)

Geef de volgende informatie op in het scherm **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    Servernaam of IP-adres
Host Port:       Poortnummer, bijv. 1433
Database Name:   Databasenaam
Schema Name:     Schema dat de brongegevens bevat
User Name:       Databasegebruikersnaam
User Password:   Wachtwoord voor de gebruiker
Use ODBC:        Disabled (default)
```

---

## ODBC-driver

De ODBC-driver kan een breder scala aan authenticatie- en verbindingsopties ondersteunen. Deze sectie richt zich op wachtwoordgebaseerde authenticatie met de driver **SQL Server**.

### 1. Installeer de ODBC-driver

Installeer de driver **SQL Server** (of een vergelijkbare) volgens de officiële installatiehandleiding van de leverancier.

### 2. Configureer de ODBC-datasource

Volg deze stappen om een nieuwe ODBC-datasource te configureren met wachtwoordgebaseerde authenticatie:

#### Stap 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Klik op de knop **Next >**.

#### Stap 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Kies de authenticatiemethode (bijv. gebruikersnaam en wachtwoord)
en geef de vereiste gegevens op.

Klik op de knop **Next >**.

#### Stap 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Kies de ANSI-conforme instellingen en klik vervolgens op de knop **Next >**.

#### Stap 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

U kunt de standaardinstellingen behouden of logopties kiezen indien nodig
en klik vervolgens op de knop **Finish**. 

#### Stap 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Klik nu op de knop ** Test datasource **.

#### Stap 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Wanneer u het succesvenster ontvangt, is ODBC correct geconfigureerd.

---

Nu kunt u *digna* configureren om de ODBC-verbinding te gebruiken, ofwel met een **DSN (Data Source Name)** of met een **DSN-less** configuratie.

---

### A. DSN-gebaseerde configuratie

#### *digna* configuratie

Geef in het scherm **"Create a Database Connection"** het volgende op:

```
Technology:      MS SQL Server
Database Name:   Database die het bronschema bevat
Schema Name:     Schema dat de brongegevens bevat
Use ODBC:        Enabled
```

#### ODBC-eigenschappen

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "uw databasegebruiker"
name: "PWD",        value: "uw databasewachtwoord"
name: "DATABASE",   value: "naam van de database die het bronschema bevat"
```

> De `DSN` moet overeenkomen met de naam die in uw ODBC-driverconfiguratie is ingesteld.

---

### B. DSN-less configuratie

#### *digna* configuratie

Geef in het scherm **"Create a Database Connection"** het volgende op:

```
Technology:      MS SQL Server
Database Name:   Schema dat de brongegevens bevat (zelfde als Schema Name)
Schema Name:     Schema dat de brongegevens bevat
Use ODBC:        Enabled
```

#### ODBC-eigenschappen

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "uw servernaam of IP-adres"
name: "UID",        value: "uw databasegebruiker"
name: "PWD",        value: "uw databasewachtwoord"
name: "DATABASE",   value: "naam van de database die het bronschema bevat"
```
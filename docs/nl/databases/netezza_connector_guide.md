---
title: Netezza Connector – Database-integratie | digna documentatie
description: Configureer digna om verbinding te maken met Netezza met de NetezzaSQL ODBC-driver. Ondersteunt wachtwoordgebaseerde authenticatie met DSN- of DSN-less configuraties voor flexibele connectiviteit.
image: /assets/logo_square.png
---


# Bronconnector voor Netezza

Deze gids beschrijft hoe je *digna* configureert om verbinding te maken met Netezza via de ODBC-driver.

Het verwijst naar het scherm **"Create a Database Connection"**.

![Maak een databaseverbinding](images/data_source_config_input_mask.png)

---

## ODBC-driver

De ODBC-driver kan een reeks authenticatie- en verbindingsopties ondersteunen. Deze sectie richt zich op wachtwoordgebaseerde authenticatie met de driver **NetezzaSQL**.

### 1. Installeer de ODBC-driver

Installeer de driver **NetezzaSQL** (of een vergelijkbare) door de officiële installatierichtlijnen van de leverancier te volgen.

### 2. Configureer de ODBC-databron

Volg deze stappen om een nieuwe ODBC-databron te configureren met wachtwoordgebaseerde authenticatie:

#### Stap 1
![Stap 1](images/netezza/create_odbc_data_source_step1.png)

Afhankelijk van je Netezza-driver, installatie- en beveiligingseisen, moet je mogelijk ook gegevens invullen in de tabbladen **Advanced DSN Options**, **SSL DSN Options** of **Driver Options**. Voor de meest eenvoudige setup volstaat het om gegevens in **DSN Options** in te vullen.

Klik op de **Test Connection**-knop.

#### Stap 2
![Stap 2](images/netezza/create_odbc_data_source_step2.png)

Wanneer je het succesvenster ziet, is ODBC correct geconfigureerd.

---

Nu kun je *digna* configureren om de ODBC-verbinding te gebruiken, ofwel met een **DSN (Data Source Name)** of met een **DSN-less** setup.

---

### A. DSN-gebaseerde configuratie

#### Configuratie in *digna*

In het scherm **"Create a Database Connection"** voer je het volgende in:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-eigenschappen

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 De `DSN` moet overeenkomen met de naam die is gedefinieerd in je ODBC-driverconfiguratie.

---

### B. DSN-less configuratie

#### Configuratie in *digna*

In het scherm **"Create a Database Connection"** voer je het volgende in:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-eigenschappen

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
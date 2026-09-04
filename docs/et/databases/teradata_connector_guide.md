---
title: Teradata Connector – Andmebaasi integratsioon | digna dokumentatsioon
description: Konfigureerige digna ühenduma Teradataga, kasutades teradatasql Pythoni draiverit või Teradata ODBC-draiverit. Toetab paroolipõhist autentimist DSN-iga või ilma DSN-ita seadistustes.
image: /assets/logo_square.png
---


# Source Connector for Teradata

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduse loomiseks Teradataga, kasutades kas natiivset Pythoni ühendajat või ODBC-draiverit.

See viitab ekraanile **"Loo andmebaasiühendus"**.

![Loo andmebaasiühendus](images/data_source_config_input_mask.png)

---

## Natiivne Pythoni draiver

**Library:** `teradatasql`  
**Toetatav autentimine:** Ainult paroolipõhine autentimine

> Muude autentimisviiside jaoks kasutage palun ODBC-draiverit.

### *digna* konfiguratsioon (natiivne draiver)

Sisestage järgmised andmed ekraanil **"Loo andmebaasiühendus"**:

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

## ODBC-draiver

ODBC-draiver võib toetada laiemat valikut autentimis- ja ühendusvõimalusi. See jaotis keskendub paroolipõhisele autentimisele, kasutades draiverit **Teradata Database ODBC Driver 20.00**.

### 1. Paigaldage ODBC-draiver

Paigaldage draiver **Teradata Database ODBC Driver 20.00** (või sarnane), järgides tarnija ametlikku paigaldusjuhendit.

### 2. Konfigureerige ODBC andmeallikas

Järgige neid samme, et konfigureerida uus ODBC andmeallikas, kasutades paroolipõhist autentimist:

#### Samm 1
![Samm 1](images/teradata/create_odbc_data_source_step1.png)

Klõpsake nuppu **Test**.

#### Samm 2
![Samm 2](images/teradata/create_odbc_data_source_step2.png)

Sisestage kasutajanimi ja parool.

Klõpsake nuppu **OK**.
Kui kuvatakse õnnestumise ekraan, on ODBC õigesti konfigureeritud.

---

Nüüd saate konfigureerida *digna* ODBC-ühenduse kasutamiseks kas **DSN (Data Source Name)**-iga või **ilma DSN-ita** seadistuses.

---

### A. DSN-põhine konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Loo andmebaasiühendus"** sisestage järgmised andmed:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC omadused

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN` peab vastama teie ODBC-draiveri konfiguratsioonis määratud nimele.

---

### B. DSN-vaba konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Loo andmebaasiühendus"** sisestage järgmised andmed:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC omadused

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
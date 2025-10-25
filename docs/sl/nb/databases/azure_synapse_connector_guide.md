---
title: Azure Synapse Connector – Integracija baze podatkov | digna dokumentacija
description: Konfigurirajte digna za povezavo z Azure Synapse Analytics z uporabo izvornega Python-gonilnika ali ODBC-gonilnika. Podpira tako serverless kot namenski SQL pool.
image: /assets/logo_square.png
---


# Povezovalnik vira za Azure Synapse Analytics

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Azure Synapse Analytics z uporabo bodisi izvorne Python-povezave ali ODBC-gonilnika.
Podpira tako serverless kot namenski SQL pool.

Navodila se nanašajo na zaslon **"Create a Database Connection"**.

![Ustvarjanje povezave z bazo podatkov](images/data_source_config_input_mask.png)

---

## Izvorni Python-gonilnik

**Knjiznica:** `pymssql`  
**Podprta avtentikacija:** Samo geselna avtentikacija

> ⚠️ Za druge metode avtentikacije uporabite ODBC-gonilnik.

### *digna* konfiguracija (izvorni gonilnik)

Vnesite naslednje podatke na zaslonu **"Create a Database Connection"**:

```
Tehnologija:     MS SQL Server
Naslov gostitelja: <synapse-workspace>[-ondemand].sql.azuresynapse.net
Vrata (port):    Številka vrat, npr. 1433
Ime baze podatkov:  Ime baze podatkov
Shema:           Shema, ki vsebuje izvorne podatke
Uporabniško ime: Uporabniško ime za bazo
Geslo uporabnika: Geslo za uporabnika
Uporabi ODBC:    Onemogočeno (privzeto)
```

---

## ODBC-gonilnik

ODBC-gonilnik lahko podpira širši nabor možnosti avtentikacije in povezovanja. Ta razdelek se osredotoča na geselno avtentikacijo z uporabo gonilnika **ODBC Driver 18 for SQL Server**.

### 1. Namestite ODBC-gonilnik

Namestite gonilnik **ODBC Driver 18 for SQL Server** (ali ustreznega) tako, da sledite uradnemu navodilu za namestitev ponudnika.

### 2. Konfigurirajte ODBC-datotečni vir

Sledite tem korakom, da konfigurirate nov ODBC-datotečni vir z geselno avtentikacijo:

#### Korak 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Izpolnite polje "Server".
Uporabite ime Synapse delovnega prostora in dodajte ".sql.azuresynapse.net".  
**Opomba**, če se želite povezati z uporabo serverless SQL-poola, poskrbite, da vključite "-ondemand", kot je prikazano na spodnjem posnetku zaslona.

Kliknite gumb **Next >**.

#### Korak 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Izberite metodo avtentikacije (npr. uporabniško ime in geslo)
in vnesite zahtevane podatke.

Kliknite gumb **Next >**.

#### Korak 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Izberite ANSI-kompatibilne nastavitve in nato kliknite gumb **Next >**.

#### Korak 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Lahko pustite privzete nastavitve ali izberete možnosti po potrebi 
in kliknete gumb **Finish**. 

#### Korak 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Kliknite zdaj gumb **Test datasource**.

#### Korak 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Ko prejmete zaslon s sporočilom o uspehu, je ODBC pravilno konfiguriran.

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC-povezavo, bodisi z **DSN (Data Source Name)** ali z **DSN-less** nastavitvijo.

---

### A. DSN-osnovana konfiguracija

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Tehnologija:       MS SQL Server
Ime baze podatkov: Baza, ki vsebuje izvorno shemo
Shema:             Shema, ki vsebuje izvorne podatke
Uporabi ODBC:      Omogočeno
```

#### Lastnosti ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` mora sovpadati z imenom, ki je določeno v vaši ODBC-konfiguraciji.

---

### B. Konfiguracija brez DSN

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Tehnologija:       MS SQL Server
Ime baze podatkov: Baza, ki vsebuje izvorne podatke (enako kot Shema)
Shema:             Shema, ki vsebuje izvorne podatke
Uporabi ODBC:      Omogočeno
```

#### Lastnosti ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Opomba** glede lastnosti SERVER:  
Uporabite ime Synapse delovnega prostora in dodajte ".sql.azuresynapse.net". Če se želite povezati z uporabo serverless SQL-poola, poskrbite, da vključite "-ondemand", kot je prikazano na zaslonih.
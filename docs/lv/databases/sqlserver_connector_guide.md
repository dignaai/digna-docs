---
title: MS SQL Server savienotājs – datubāžu integrācija | digna dokumentācija
description: Konfigurējiet digna, lai pievienotos Microsoft SQL Server, izmantojot Python draiveri pymssql vai SQL Server ODBC draiveri. Atbalsta paroli balstītu autentifikāciju ar DSN vai bez DSN.
image: /assets/logo_square.png
---


# Avota savienotājs MS SQL Server

Šī rokasgrāmata apraksta, kā konfigurēt *digna*, lai izveidotu savienojumu ar SQL Server, izmantojot vai nu vietējo Python konektoru, vai ODBC draiveri.

Tas attiecas uz ekrānu **"Create a Database Connection"**.

![Izveidot datubāzes savienojumu](images/data_source_config_input_mask.png)

---

## Vietējais Python draiveris

**Bibliotēka:** `pymssql`  
**Atbalstītā autentifikācija:** Tikai paroles autentifikācija

> Ja nepieciešamas citas autentifikācijas metodes, lūdzu, izmantojiet ODBC draiveri.

### *digna* konfigurācija (vietējais draiveris)

Norādiet sekojošo informāciju ekrānā **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    Server nosaukums vai IP adrese
Host Port:       Porta numurs, piem. 1433
Database Name:   Datubāzes nosaukums
Schema Name:     Šema, kurā atrodas avota dati
User Name:       Datubāzes lietotāja vārds
User Password:   Lietotāja parole
Use ODBC:        Disabled (default)
```

---

## ODBC draiveris

ODBC draiveris var atbalstīt plašāku autentifikācijas un savienojamības iespēju klāstu. Šī sadaļa koncentrējas uz paroli balstītu autentifikāciju, izmantojot draiveri **SQL Server**.

### 1. Instalējiet ODBC draiveri

Instalējiet draiveri **SQL Server** (vai līdzīgu), sekojot piegādātāja oficiālajai instalācijas instrukcijai.

### 2. Konfigurējiet ODBC datu avotu

Veiciet šīs darbības, lai konfigurētu jaunu ODBC datu avotu ar paroli balstītu autentifikāciju:

#### 1. solis
![1. solis](images/sqlserver/create_odbc_data_source_step1.png)

Nospiediet pogu **Next >**.

#### 2. solis
![2. solis](images/sqlserver/create_odbc_data_source_step2.png)

Izvēlieties autentifikācijas metodi (piem., lietotājvārds un parole) un ievadiet nepieciešamos datus.

Nospiediet pogu **Next >**.

#### 3. solis
![3. solis](images/sqlserver/create_odbc_data_source_step3.png)

Izvēlieties ANSI savietojamos iestatījumus, pēc tam nospiediet pogu **Next >**.

#### 4. solis
![4. solis](images/sqlserver/create_odbc_data_source_step4.png)

Jūs varat atstāt noklusējuma iestatījumus vai izvēlēties žurnāla opcijas pēc vajadzības un nospiest pogu **Finish**.

#### 5. solis
![5. solis](images/sqlserver/create_odbc_data_source_step5.png)

Tagad nospiediet pogu **Test datasource**.

#### 6. solis
![6. solis](images/sqlserver/create_odbc_data_source_step6.png)

Kad saņemat veiksmīgu paziņojumu, ODBC ir pareizi konfigurēts.

---

Tagad varat konfigurēt *digna*, lai izmantotu ODBC savienojumu, izmantojot gan **DSN (Data Source Name)**, gan **DSN-less** iestatījumu.

---

### A. DSN bāzēta konfigurācija

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      MS SQL Server
Database Name:   Datubāze, kurā atrodas avota šema
Schema Name:     Šema, kurā atrodas avota dati
Use ODBC:        Enabled
```

#### ODBC īpašības

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> `DSN` jāatbilst nosaukumam, kas definēts jūsu ODBC draivera konfigurācijā.

---

### B. DSN-less konfigurācija

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      MS SQL Server
Database Name:   Šema, kurā atrodas avota dati (tas pats, kas Schema Name)
Schema Name:     Šema, kurā atrodas avota dati
Use ODBC:        Enabled
```

#### ODBC īpašības

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```
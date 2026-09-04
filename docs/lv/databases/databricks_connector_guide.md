---
title: Databricks savienotājs ar Unity Catalog – datubāzu integrācija | digna dokumentācija
description: Konfigurējiet *digna*, lai izveidotu savienojumu ar Databricks, izmantojot Unity Catalog, izmantojot iebūvēto Python connector vai ODBC draiveri. Atbalsta token-pamata autentifikāciju un elastīgu savienojamību.
image: /assets/logo_square.png
---

# Avota savienotājs Databricks — ar Unity Catalog

Šī rokasgrāmata apraksta, kā konfigurēt *digna*, lai izveidotu savienojumu ar Databricks, izmantojot vai nu iebūvēto Python connector, vai ODBC draiveri.

Tā atsaucas uz ekrānu **"Create a Database Connection"**.

![Izveidot datubāzes savienojumu](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Bibliotēka:** `databricks-sql-connector`  
**Atbalstītā autentifikācija:** tikai Personal Access Token (PAT)

> Citu autentifikācijas metožu gadījumā izmantojiet ODBC draiveri.

### Personal Access Token (PAT)

Lai autentificētos, izmantojot personal access token, skatiet oficiālo Databricks dokumentāciju:  
[Kā iegūt PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfigurācija (Native Driver)

Norādiet sekojošo informāciju ekrānā **"Create a Database Connection"**:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC draiveris atbalsta plašāku autentifikācijas un savienojamības iespēju spektru. Šajā sadaļā galvenā uzmanība pievērsta token-pamata autentifikācijai, izmantojot **Simba Spark ODBC Driver**.

### 1. Instalējiet ODBC draiveri

Instalējiet **Simba Spark ODBC Driver**, sekojot piegādātāja oficiālajai instalācijas rokasgrāmatai.

### 2. Konfigurējiet ODBC datu avotu

Veiciet šīs darbības, lai konfigurētu jaunu ODBC datu avotu, izmantojot Personal Access Token:

#### 1. solis
![1. solis](images/databricks/create_odbc_data_source_step1.png)

#### 2. solis
![2. solis](images/databricks/create_odbc_data_source_step2.png)

#### 3. solis
![3. solis](images/databricks/create_odbc_data_source_step3.png)

#### 4. solis
![4. solis](images/databricks/create_odbc_data_source_step4.png)

#### 5. solis – Savienojuma pārbaude

Noklikšķiniet uz pogas **TEST**. Veiksmīgs savienojums izskatīsies šādi:

![5. solis](images/databricks/create_odbc_data_source_step5.png)

---

Tagad varat konfigurēt *digna*, lai izmantotu ODBC savienojumu, vai nu ar **DSN (Data Source Name)**, vai **bez DSN** risinājumu.

---

### A. DSN bāzēta konfigurācija

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC īpašības

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` jāatbilst nosaukumam, kas definēts jūsu ODBC draivera konfigurācijā.

---

### B. Bez DSN (DSN-less) konfigurācija

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC īpašības

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
---
title: Azure Synapse jungtis – Duomenų bazės integracija | digna dokumentacija
description: Konfigūruokite *digna* prisijungimui prie Azure Synapse Analytics naudodami arba natyvų Python tvarkyklę, arba ODBC tvarkyklę. Palaikomi tiek serverless, tiek dedicated SQL baseinai.
image: /assets/logo_square.png
canonical_url: https://docs.digna.ai/databases/azure_synapse_connector_guide/
---


# Source Connector for Azure Synapse Analytics

Šiame gide aprašoma, kaip konfigūruoti *digna* prisijungimui prie Azure Synapse Analytics naudojant arba natyvų Python jungtį, arba ODBC tvarkyklę.
Palaikomi tiek serverless, tiek dedicated SQL baseinai.

Tai nurodo ekraną **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Biblioteka:** `pymssql`  
**Palaikoma autentifikacija:** tik autentifikacija su slaptažodžiu

> Jei naudojate kitus autentifikacijos metodus, prašome naudoti ODBC tvarkyklę.

### *digna* konfigūracija (natyvus tvarkyklė)

Nurodykite šią informaciją ekrane **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC tvarkyklė gali palaikyti platesnį autentifikacijos ir ryšio parinkčių spektrą. Šiame skyriuje aptariama autentifikacija naudojant slaptažodį su tvarkykle **ODBC Driver 18 for SQL Server**.

### 1. Įdiekite ODBC tvarkyklę

Įdiekite tvarkyklę **ODBC Driver 18 for SQL Server** (ar panašią) vadovaudamiesi tiekėjo oficialia diegimo instrukcija.

### 2. Konfigūruokite ODBC duomenų šaltinį

Atlikite šiuos veiksmus, kad konfigūruotumėte naują ODBC duomenų šaltinį naudojant autentifikaciją su slaptažodžiu:

#### 1 žingsnis
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Užpildykite lauką "Server".
Naudokite Synapse darbo srities pavadinimą ir pridėkite ".sql.azuresynapse.net".  
**Dėmesio**, jei norite prisijungti naudojant serverless SQL pool, įsitikinkite, kad yra įtrauktas "-ondemand", kaip parodyta žemiau esančiame ekrane.

Spustelėkite mygtuką **Next >**.

#### 2 žingsnis
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Pasirinkite autentifikacijos metodą (pvz., vartotojo vardas ir slaptažodis)
ir nurodykite reikiamus duomenis.

Spustelėkite mygtuką **Next >**.

#### 3 žingsnis
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Pasirinkite ANSI atitinkančius nustatymus, tada spustelėkite mygtuką **Next >**.

#### 4 žingsnis
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Galite palikti numatytuosius nustatymus arba pasirinkti parinktis pagal poreikį 
ir spustelėti mygtuką **Finish**. 

#### 5 žingsnis
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Dabar spustelėkite mygtuką **Test datasource**.

#### 6 žingsnis
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Kai gausite sėkmės ekraną, ODBC yra tinkamai sukonfigūruotas.

---

Dabar galite konfigūruoti *digna*, kad naudotų ODBC ryšį, arba per **DSN (Data Source Name)**, arba per **DSN-less** nustatymą.

---

### A. Konfigūracija su DSN

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** nurodykite šiuos duomenis:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC savybės

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> `DSN` turi atitikti pavadinimą, apibrėžtą jūsų ODBC tvarkyklės konfiguracijoje.

---

### B. Konfigūracija be DSN (DSN-less)

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** nurodykite šiuos duomenis:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC savybės

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Pastaba** dėl SERVER savybės:  
Naudokite Synapse darbo srities pavadinimą ir pridėkite ".sql.azuresynapse.net". Jei norite prisijungti naudojant serverless SQL pool, įsitikinkite, kad yra įtrauktas "-ondemand", kaip parodyta žemiau esančiame ekrane.
# Šaltinio jungtis į Databricks – su Unity Catalog

Šis vadovas aprašo, kaip sukonfigūruoti *digna*, kad prisijungtų prie Databricks, naudojant arba natyvų Python jungiklį, arba ODBC tvarkyklę.

Jis nurodo ekraną **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natyvus Python tvarkyklė

**Biblioteka:** `databricks-sql-connector`  
**Palaikomas autentifikavimas:** tik Personal Access Token (PAT)

> Kitoms autentifikavimo metodikoms naudokite ODBC tvarkyklę.

### Personal Access Token (PAT)

Norėdami autentifikuotis naudodami asmeninį prieigos raktą, žiūrėkite oficialią Databricks dokumentaciją:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfigūracija (natyvus tvarkyklė)

Pateikite šią informaciją ekrane **"Create a Database Connection"**:

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

## ODBC tvarkyklė

ODBC tvarkyklė palaiko platesnį autentifikavimo ir prisijungimo variantų spektrą. Šiame skyriuje aptariamas tokenu pagrįstas autentifikavimas, naudojant **Simba Spark ODBC Driver**.

### 1. Įdiekite ODBC tvarkyklę

Įdiekite **Simba Spark ODBC Driver** vadovaudamiesi tiekėjo oficialiu diegimo gidu.

### 2. Konfigūruokite ODBC duomenų šaltinį

Atlikite šiuos veiksmus, kad sukurtumėte naują ODBC duomenų šaltinį, naudojant Personal Access Token:

#### 1 žingsnis
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### 2 žingsnis
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### 3 žingsnis
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### 4 žingsnis
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### 5 žingsnis – patikrinkite prisijungimą

Spustelėkite mygtuką **TEST**. Sėkmingas prisijungimas turėtų atrodyti taip:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Dabar galite sukonfigūruoti *digna* naudoti ODBC jungtį, arba per **DSN (Data Source Name)**, arba be DSN (DSN-less).

---

### A. DSN pagrindu atliekama konfigūracija

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** pateikite šią informaciją:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC savybės

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` turi atitikti vardą, nurodytą jūsų ODBC tvarkyklės konfigūracijoje.

---

### B. Be DSN (DSN-less) konfigūracija

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** pateikite šią informaciją:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC savybės

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
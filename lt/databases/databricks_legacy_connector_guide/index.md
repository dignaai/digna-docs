# Source Connector for Databricks - without Unity Catalog

Šiame vadove aprašoma, kaip sukonfigūruoti *digna* prisijungimui prie Databricks naudojant arba vietinį Python jungtį, arba ODBC driverį.

Jis nurodo ekraną **„Create a Database Connection“**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** tik asmeninis prieigos raktas (Personal Access Token, PAT)

> Jei norite naudoti kitus autentifikacijos metodus, prašome naudoti ODBC driverį.

### Personal Access Token (PAT)

Norėdami autentifikuotis naudojant asmeninį prieigos raktą, kreipkitės į oficialią Databricks dokumentaciją:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfigūracija (vietinis driveris)

Pateikite šią informaciją ekrane **„Create a Database Connection“**:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC driveris palaiko platesnį autentifikacijos ir jungties parinkčių spektrą. Ši dalis skirta tokenų pagrindu veikiančiai autentifikacijai naudojant **Simba Spark ODBC Driver**.

### 1. Įdiekite ODBC driverį

Įdiekite **Simba Spark ODBC Driver** vadovaudamiesi tiekėjo oficialia diegimo instrukcija.

### 2. Konfigūruokite ODBC duomenų šaltinį

Atlikite šiuos veiksmus, kad sukonfigūruotumėte naują ODBC duomenų šaltinį naudodami asmeninį prieigos raktą:

#### Žingsnis 1
![Žingsnis 1](images/databricks/create_odbc_data_source_step1.png)

#### Žingsnis 2
![Žingsnis 2](images/databricks/create_odbc_data_source_step2.png)

#### Žingsnis 3
![Žingsnis 3](images/databricks/create_odbc_data_source_step3.png)

#### Žingsnis 4
![Žingsnis 4](images/databricks/create_odbc_data_source_step4.png)

#### Žingsnis 5 – Išbandykite ryšį

Spustelėkite mygtuką **TEST**. Sėkmingas prisijungimas turėtų atrodyti taip:

![Žingsnis 5](images/databricks/create_odbc_data_source_step5.png)

---

Dabar galite sukonfigūruoti *digna*, kad jis naudotų ODBC prisijungimą, arba per **DSN (Data Source Name)**, arba be DSN.

---

### A. Konfigūracija su DSN

#### *digna* konfigūracija

Ekrane **„Create a Database Connection“** pateikite šią informaciją:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC savybės

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` turi atitikti vardą, nurodytą jūsų ODBC driverio konfigūracijoje.

---

### B. Konfigūracija be DSN

#### *digna* konfigūracija

Ekrane **„Create a Database Connection“** pateikite šią informaciją:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
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
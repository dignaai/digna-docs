# Source Connector for Databricks - with Unity Catalog

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Databricksiga, kasutades kas natiivset Pythoni draiverit või ODBC draiverit.

See viitab ekraanile **"Create a Database Connection"**.

![Loo andmebaasiühendus](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Muude autentimismeetodite jaoks kasutage palun ODBC draiverit.

### Personal Access Token (PAT)

Isikliku juurdepääsu tokeni kasutamiseks autentimiseks vaadake ametlikku Databricksi dokumentatsiooni:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Sisestage järgmine teave ekraanil **"Create a Database Connection"**:

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

ODBC draiver toetab laiemat valikut autentimis- ja ühendusvõimalusi. See jaotis keskendub token-põhisele autentimisele, kasutades **Simba Spark ODBC Driver**i.

### 1. Install the ODBC Driver

Installige **Simba Spark ODBC Driver** järgides tootja ametlikku paigaldusjuhendit.

### 2. Configure the ODBC Data Source

Järgige neid samme, et konfigureerida uus ODBC andmeallikas, kasutades Personal Access Tokenit:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Klõpsake nuppu **TEST**. Õnnestunud ühendus peaks välja nägema nii:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nüüd saate konfigureerida *digna* kasutama ODBC ühendust kas **DSN (Data Source Name)** või **DSN-less** seadistuse kaudu.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Ekraanil **"Create a Database Connection"** sisestage järgmine:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` peab vastama nimele, mis on määratud teie ODBC draiveri konfiguratsioonis.

---

### B. DSN-less Configuration

#### *digna* Configuration

Ekraanil **"Create a Database Connection"** sisestage järgmine:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

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
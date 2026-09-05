# Andmeallika ühendaja Databricksile — ilma Unity Catalogita

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Databricksiga, kasutades kas natiivset Python-ühendajat või ODBC-draiverit.

See viitab ekraanile **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natiivne Pythoni draiver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Muude autentimismeetodite puhul kasutage palun ODBC-draiverit.

### Personal Access Token (PAT)

Isikliku juurdepääsu tokeni autentimiseks vaadake ametlikku Databricks'i dokumentatsiooni:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfiguratsioon (natiivdraiver)

Esitage järgmine info ekraanil **"Create a Database Connection"**:

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

## ODBC-draiver

ODBC-draiver toetab laiemat valikut autentimis- ja ühenduvusvalikuid. See jaotis keskendub tokenipõhisele autentimisele, kasutades **Simba Spark ODBC Driver**it.

### 1. Paigaldage ODBC-draiver

Paigaldage **Simba Spark ODBC Driver** vastavalt tööandja ametlikule paigaldusjuhisele.

### 2. Konfigureerige ODBC andmeallikas

Järgige neid samme, et konfigureerida uus ODBC andmeallikas, kasutades Personal Access Tokenit:

#### 1. samm
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### 2. samm
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### 3. samm
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### 4. samm
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### 5. samm – Ühenduse testimine

Klõpsake nuppu **TEST**. Eduka ühenduse korral peaks see välja nägema umbes nii:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nüüd saate konfigureerida *digna* kasutama ODBC-ühendust kas **DSN (Data Source Name)**-i abil või **DSN-evaba** seadistusega.

---

### A. DSN-põhine konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Create a Database Connection"** esitage järgmine:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC omadused

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` peab vastama nimele, mis on määratud teie ODBC-draiveri konfiguratsioonis.

---

### B. DSN-evaba konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Create a Database Connection"** esitage järgmine:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC omadused

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
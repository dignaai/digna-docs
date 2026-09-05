# Zdrojový konektor pro Databricks – bez Unity Catalogu

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Databricks buď pomocí nativního Python konektoru, nebo pomocí ODBC driveru.

Odkazuje se na obrazovku **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Pro jiné metody autentizace použijte ODBC driver.

### Personal Access Token (PAT)

Pro autentizaci pomocí osobního přístupového tokenu postupujte podle oficiální dokumentace Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Provide the following information in the **"Create a Database Connection"** screen:

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

ODBC driver podporuje širší škálu možností autentizace a konektivity. Tato sekce se zaměřuje na autentizaci pomocí tokenu s použitím **Simba Spark ODBC Driveru**.

### 1. Instalace ODBC driveru

Nainstalujte **Simba Spark ODBC Driver** podle oficiální instalační příručky dodavatele.

### 2. Konfigurace ODBC Data Source

Postupujte podle těchto kroků pro konfiguraci nového ODBC datového zdroje pomocí Personal Access Tokenu:

#### Krok 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Krok 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Krok 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Krok 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Krok 5 – Test připojení

Klikněte na tlačítko **TEST**. Úspěšné připojení by mělo vypadat takto:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nyní můžete nakonfigurovat *digna*, aby používalo ODBC připojení, buď s **DSN (Data Source Name)**, nebo v **DSN-less** režimu.

---

### A. Konfigurace založená na DSN

#### *digna* Configuration

V obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` musí odpovídat názvu definovanému ve vaší konfiguraci ODBC driveru.

---

### B. DSN-less konfigurace

#### *digna* Configuration

V obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
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
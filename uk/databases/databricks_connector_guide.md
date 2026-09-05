# Source Connector for Databricks - with Unity Catalog

Цей посібник описує, як налаштувати *digna* для підключення до Databricks, використовуючи або рідний Python-конектор, або ODBC-драйвер.

Він посилається на екран **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> For other authentication methods, please use the ODBC driver.

### Personal Access Token (PAT)

Щоб автентифікуватися за допомогою personal access token, зверніться до офіційної документації Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Provide the following information in the **"Create a Database Connection"** screen:

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

ODBC-драйвер підтримує ширший спектр методів автентифікації та варіантів підключення. Цей розділ зосереджений на автентифікації на основі токена з використанням **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Встановіть **Simba Spark ODBC Driver**, дотримуючись офіційного керівництва постачальника.

### 2. Configure the ODBC Data Source

Виконайте ці кроки, щоб налаштувати нове джерело даних ODBC із використанням Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Натисніть кнопку **TEST**. Успішне підключення має виглядати так:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Тепер ви можете налаштувати *digna* для використання ODBC-з’єднання — або з **DSN (Data Source Name)**, або в **DSN-less** режимі.

---

### A. DSN-Based Configuration

#### *digna* Configuration

У вікні **"Create a Database Connection"** вкажіть наступне:

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

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

У вікні **"Create a Database Connection"** вкажіть наступне:

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
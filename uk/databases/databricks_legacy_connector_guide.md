# Джерельний конектор для Databricks — без Unity Catalog

Цей посібник описує, як налаштувати *digna* для підключення до Databricks за допомогою нативного Python-конектора або ODBC-драйвера.

Він посилається на екран **"Create a Database Connection"**.

![Створити підключення до бази даних](images/data_source_config_input_mask.png)

---

## Нативний Python-драйвер

**Бібліотека:** `databricks-sql-connector`  
**Підтримувана автентифікація:** лише Personal Access Token (PAT)

> Для інших методів автентифікації використовуйте ODBC-драйвер.

### Personal Access Token (PAT)

Щоб автентифікуватися за допомогою Personal Access Token, зверніться до офіційної документації Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### Конфігурація *digna* (нативний драйвер)

Надайте наступну інформацію на екрані **"Create a Database Connection"**:

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

## ODBC-драйвер

ODBC-драйвер підтримує ширший спектр методів автентифікації та варіантів підключення. У цьому розділі описано автентифікацію на основі токена з використанням **Simba Spark ODBC Driver**.

### 1. Встановіть ODBC-драйвер

Встановіть **Simba Spark ODBC Driver**, дотримуючись офіційного інструктажу постачальника.

### 2. Налаштуйте джерело даних ODBC

Виконайте ці кроки для налаштування нового джерела даних ODBC з використанням Personal Access Token:

#### Крок 1
![Крок 1](images/databricks/create_odbc_data_source_step1.png)

#### Крок 2
![Крок 2](images/databricks/create_odbc_data_source_step2.png)

#### Крок 3
![Крок 3](images/databricks/create_odbc_data_source_step3.png)

#### Крок 4
![Крок 4](images/databricks/create_odbc_data_source_step4.png)

#### Крок 5 – Тест підключення

Натисніть кнопку **TEST**. Успішне підключення виглядатиме так:

![Крок 5](images/databricks/create_odbc_data_source_step5.png)

---

Тепер ви можете налаштувати *digna* для використання ODBC-підключення — або через **DSN (Data Source Name)**, або у **DSN-less** конфігурації.

---

### A. Конфігурація на основі DSN

#### Конфігурація *digna*

На екрані **"Create a Database Connection"** вкажіть наступне:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` повинен відповідати імені, визначеному в налаштуваннях вашого ODBC-драйвера.

---

### B. DSN-less конфігурація

#### Конфігурація *digna*

На екрані **"Create a Database Connection"** вкажіть наступне:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Властивості ODBC

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
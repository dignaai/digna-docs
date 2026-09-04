---
title: Коннектор Databricks с Unity Catalog — интеграция базы данных | Документация digna
description: Настройка digna для подключения к Databricks с Unity Catalog с использованием нативного Python-коннектора или ODBC-драйвера. Поддерживается аутентификация по токену и гибкие варианты подключения.
image: /assets/logo_square.png
---

# Source Connector for Databricks - with Unity Catalog

Это руководство описывает, как настроить *digna* для подключения к Databricks с использованием либо нативного Python-коннектора, либо ODBC-драйвера.

Оно относится к экрану **"Create a Database Connection"**.

![Создать подключение к базе данных](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Для других методов аутентификации используйте ODBC-драйвер.

### Personal Access Token (PAT)

Для аутентификации с использованием персонального токена доступа обратитесь к официальной документации Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Укажите следующую информацию на экране **"Create a Database Connection"**:

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

ODBC-драйвер поддерживает более широкий набор вариантов аутентификации и подключений. В этом разделе рассматривается аутентификация по токену с использованием **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Установите **Simba Spark ODBC Driver**, следуя официальному руководству поставщика.

### 2. Configure the ODBC Data Source

Следуйте этим шагам, чтобы настроить новый ODBC-источник данных с использованием Personal Access Token:

#### Step 1
![Шаг 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Шаг 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Шаг 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Шаг 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Нажмите кнопку **TEST**. Успешное подключение должно выглядеть так:

![Шаг 5](images/databricks/create_odbc_data_source_step5.png)

---

Теперь вы можете настроить *digna* для использования ODBC-подключения — либо через **DSN (Data Source Name)**, либо в режиме **без DSN (DSN-less)**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

На экране **"Create a Database Connection"** укажите следующее:

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

> Значение `DSN` должно совпадать с именем, указанным в конфигурации вашего ODBC-драйвера.

---

### B. DSN-less Configuration

#### *digna* Configuration

На экране **"Create a Database Connection"** укажите следующее:

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
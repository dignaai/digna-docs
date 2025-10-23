---
title: Databricks Connector (Legacy, without Unity Catalog) | digna Documentation
description: Настройка digna для подключения к Databricks без Unity Catalog с помощью нативного Python-коннектора или драйвера Simba Spark ODBC. Поддерживается аутентификация по токену и гибкие варианты подключения.
image: /assets/logo_square.png
---

# Source Connector for Databricks - without Unity Catalog

Это руководство описывает, как настроить *digna* для подключения к Databricks с использованием либо нативного Python-коннектора, либо ODBC-драйвера.

Речь идёт о экране **"Create a Database Connection"**.

![Создать подключение к базе данных](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Поддерживаемая аутентификация:** только Personal Access Token (PAT)

> ⚠️ Для других методов аутентификации используйте ODBC-драйвер.

### Personal Access Token (PAT)

Чтобы аутентифицироваться с помощью персонального токена доступа, обратитесь к официальной документации Databricks:  
👉 [Как получить PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### Конфигурация *digna* (нативный драйвер)

Укажите следующую информацию на экране **"Create a Database Connection"**:

```
Technology:      Databricks (Legacy)
Host Address:    Доменное имя Databricks, напр. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Этот параметр не используется для databricks без unity catalog
Schema Name:     Схема, содержащая исходные данные
User Name:       HTTP Path, предоставляемый Databricks, напр. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, напр. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Отключено (по умолчанию)
```

---

## ODBC Driver

ODBC-драйвер поддерживает более широкий набор методов аутентификации и вариантов подключения. В этом разделе рассматривается аутентификация по токену с использованием **Simba Spark ODBC Driver**.

### 1. Установка ODBC-драйвера

Установите **Simba Spark ODBC Driver**, следуя официальному руководству поставщика.

### 2. Настройка источника данных ODBC

Выполните следующие шаги, чтобы настроить новый источник данных ODBC с использованием Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Тестирование подключения

Нажмите кнопку **TEST**. Успешное подключение выглядит так:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Теперь вы можете настроить *digna* для использования ODBC-подключения — либо через **DSN (Data Source Name)**, либо в режиме **DSN-less**.

---

### A. Конфигурация через DSN

#### Конфигурация *digna*

На экране **"Create a Database Connection"** укажите следующее:

```
Technology:      Databricks (Legacy)
Database Name:   Этот параметр не используется для databricks без unity catalog
Schema Name:     Схема, содержащая исходные данные
Use ODBC:        Включено
```

#### Свойства ODBC

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 Параметр `DSN` должен совпадать с именем, указанным в конфигурации вашего ODBC-драйвера.

---

### B. DSN-less конфигурация

#### Конфигурация *digna*

На экране **"Create a Database Connection"** укажите следующее:

```
Technology:      Databricks (Legacy)
Database Name:   Этот параметр не используется для databricks без unity catalog
Schema Name:     Схема, содержащая исходные данные
Use ODBC:        Включено
```

#### Свойства ODBC

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
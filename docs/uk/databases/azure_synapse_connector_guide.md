---
title: Azure Synapse Connector – Database Integration | digna Documentation
description: Configure digna to connect to Azure Synapse Analytics using either the native Python driver or the ODBC driver. Supports both serverless and dedicated SQL pools.
image: /assets/logo_square.png
canonical_url: https://docs.digna.ai/databases/azure_synapse_connector_guide/
---


# Source Connector for Azure Synapse Analytics

Цей посібник описує, як налаштувати *digna* для підключення до Azure Synapse Analytics, використовуючи або нативний Python-конектор, або ODBC-драйвер.
Підтримуються як serverless, так і dedicated SQL пулі.

Він посилається на екран **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Бібліотека:** `pymssql`  
**Підтримувана аутентифікація:** тільки парольна аутентифікація

> ⚠️ Для інших методів автентифікації використовуйте ODBC-драйвер.

### *digna* конфігурація (нативний драйвер)

Надайте наступну інформацію на екрані **"Create a Database Connection"**:

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

ODBC-драйвер може підтримувати ширший набір варіантів автентифікації та підключення. Цей розділ зосереджений на парольній аутентифікації з використанням драйвера **ODBC Driver 18 for SQL Server**.

### 1. Встановлення ODBC-драйвера

Встановіть драйвер **ODBC Driver 18 for SQL Server** (або подібний), дотримуючись офіційної інструкції постачальника.

### 2. Налаштування джерела даних ODBC

Виконайте ці кроки, щоб налаштувати нове джерело даних ODBC з використанням парольної автентифікації:

#### Крок 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Заповніть поле "Server".
Використовуйте ім'я Synapse workspace і додайте до нього ".sql.azuresynapse.net".   
**Увага**, якщо ви хочете підключитися до serverless SQL pool, переконайтеся, що включили "-ondemand", як показано на наступному знімку екрана.

Натисніть кнопку **Далі >**.

#### Крок 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Виберіть метод автентифікації (наприклад, ім'я користувача та пароль)
та введіть необхідні дані.

Натисніть кнопку **Далі >**.

#### Крок 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Виберіть параметри, сумісні з ANSI, потім натисніть кнопку **Далі >**.

#### Крок 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Можете залишити налаштування за замовчуванням або вибрати опції за потреби 
та натиснути кнопку **Готово**. 

#### Крок 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Тепер натисніть кнопку **Перевірити джерело даних**.

#### Крок 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Коли ви отримаєте екран успіху, ODBC налаштовано правильно.

---

Тепер ви можете налаштувати *digna* для використання ODBC-з'єднання, або з **DSN (Data Source Name)**, або в **DSN-less** режимі.

---

### A. Конфігурація на основі DSN

#### *digna* конфігурація

На екрані **"Create a Database Connection"** вкажіть наступне:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` має збігатися з іменем, визначеним у конфігурації вашого ODBC-драйвера.

---

### B. DSN-less конфігурація

#### *digna* конфігурація

На екрані **"Create a Database Connection"** вкажіть наступне:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Примітка** щодо властивості SERVER:  
Використовуйте ім'я Synapse workspace і додайте до нього ".sql.azuresynapse.net". Якщо ви хочете підключитися до serverless SQL pool, переконайтеся, що включили "-ondemand", як показано на наступному знімку екрана.
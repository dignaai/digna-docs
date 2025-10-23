---
title: Коннектор Azure Synapse — интеграция базы данных | digna Documentation
description: Настройте *digna* для подключения к Azure Synapse Analytics с помощью нативного Python-драйвера или ODBC-драйвера. Поддерживает как serverless, так и выделенные SQL-пулы.
image: /assets/logo_square.png
---


# Source Connector for Azure Synapse Analytics

В этом руководстве описано, как настроить *digna* для подключения к Azure Synapse Analytics с использованием нативного Python-коннектора или ODBC-драйвера.
Поддерживаются как serverless, так и выделенные SQL-пулы.

Руководство относится к экрану **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Только аутентификация по паролю

> ⚠️ Для других методов аутентификации используйте ODBC-драйвер.

### *digna* Configuration (Native Driver)

Укажите следующую информацию на экране **"Create a Database Connection"**:

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

ODBC-драйвер может поддерживать более широкий набор методов аутентификации и вариантов подключения. В этом разделе рассматривается аутентификация по паролю с использованием драйвера **ODBC Driver 18 for SQL Server**.

### 1. Установите ODBC-драйвер

Установите драйвер **ODBC Driver 18 for SQL Server** (или аналогичный), следуя официальному руководству по установке от поставщика.

### 2. Настройте источник данных ODBC

Выполните следующие шаги, чтобы настроить новый источник данных ODBC с аутентификацией по паролю:

#### Step 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Заполните поле "Server".
Используйте имя рабочей области Synapse и добавьте к нему ".sql.azuresynapse.net".  
**Внимание**, если вы хотите подключиться к serverless SQL pool, обязательно включите "-ondemand", как показано на скриншоте ниже.

Нажмите кнопку **Next >**.

#### Step 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Выберите метод аутентификации (например, имя пользователя и пароль)
и укажите необходимые данные.

Нажмите кнопку **Next >**.

#### Step 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Выберите настройки, совместимые с ANSI, затем нажмите кнопку **Next >**.

#### Step 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Вы можете оставить настройки по умолчанию или выбрать необходимые опции 
и нажать кнопку **Finish**. 

#### Step 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Теперь нажмите кнопку **Test datasource**.

#### Step 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Когда вы увидите экран с успешным результатом, ODBC настроен правильно.

---

Теперь вы можете настроить *digna* на использование ODBC-подключения, либо через **DSN (Data Source Name)**, либо в режиме **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

На экране **"Create a Database Connection"** укажите следующее:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 Значение `DSN` должно совпадать с именем, указанным в конфигурации вашего ODBC-драйвера.

---

### B. DSN-less Configuration

#### *digna* Configuration

На экране **"Create a Database Connection"** укажите следующее:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Примечание** относительно свойства SERVER:  
Используйте имя рабочей области Synapse и добавьте к нему ".sql.azuresynapse.net". Если вы хотите подключиться к serverless SQL pool, обязательно включите "-ondemand", как показано на скриншоте ниже.
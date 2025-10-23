---
title: Коннектор MS SQL Server — интеграция базы данных | документация digna
description: Настройка digna для подключения к Microsoft SQL Server с использованием Python-драйвера pymssql или ODBC-драйвера SQL Server. Поддерживается аутентификация по паролю с использованием DSN или без него.
image: /assets/logo_square.png
---


# Source Connector for MS SQL Server

Это руководство описывает, как настроить *digna* для подключения к SQLServer с использованием либо нативного Python-коннектора, либо ODBC-драйвера.

Речь идёт о экране **"Create a Database Connection"**.

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
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC-драйвер может поддерживать более широкий спектр вариантов аутентификации и подключения. В этом разделе рассматривается аутентификация по паролю с использованием драйвера **SQL Server**.

### 1. Install the ODBC Driver

Установите драйвер **SQL Server** (или аналогичный), следуя официальному руководству поставщика.

### 2. Configure the ODBC Data Source

Выполните следующие шаги, чтобы настроить новый ODBC-источник данных с аутентификацией по паролю:

#### Шаг 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Нажмите кнопку **Next >**.

#### Шаг 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Выберите метод аутентификации (например, имя пользователя и пароль)
и введите необходимые данные.

Нажмите кнопку **Next >**.

#### Шаг 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Выберите ANSI-совместимые настройки, затем нажмите кнопку **Next >**.

#### Шаг 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Вы можете оставить настройки по умолчанию или при необходимости выбрать параметры логирования 
и нажать кнопку **Finish**. 

#### Шаг 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Теперь нажмите кнопку **Test datasource**.

#### Шаг 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Когда вы увидите экран успеха, ODBC настроен правильно.

---

Теперь вы можете настроить *digna* на использование ODBC-подключения — либо с **DSN (Data Source Name)**, либо в **DSN-less** режиме.

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
name: "DSN",        value: "SQLServerDext"
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
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```
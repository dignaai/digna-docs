---
title: Конектор Oracle – Інтеграція баз даних | Документація digna
description: Налаштуйте digna для підключення до Oracle за допомогою драйвера python-oracledb або драйвера Oracle ODBC. Підтримується автентифікація на основі пароля з використанням DSN або без DSN.
image: /assets/logo_square.png
---


# Конектор джерела для Oracle

Цей посібник описує, як налаштувати *digna* для підключення до Oracle DB, використовуючи або рідний Python-конектор, або драйвер ODBC.

Він стосується екрана **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Рідний Python-драйвер

**Library:** `python-oracledb`  
**Підтримувана автентифікація:** лише автентифікація на основі пароля

> Для інших методів автентифікації використовуйте драйвер ODBC.

### Конфігурація *digna* (рідний драйвер)

Надайте таку інформацію на екрані **"Create a Database Connection"**:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## Драйвер ODBC

Драйвер ODBC може підтримувати ширший набір варіантів автентифікації та підключення. У цьому розділі зосереджено увагу на автентифікації на основі пароля з використанням драйвера **Oracle in OraDB21Home1**.

### 1. Встановіть драйвер ODBC

Встановіть **Oracle in OraDB21Home1** (або подібний) за офіційною інструкцією постачальника.

### 2. Налаштуйте джерело даних ODBC

Виконайте ці кроки, щоб налаштувати нове джерело даних ODBC з автентифікацією на основі пароля:

#### Крок 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Примітка:
TNS Service Name має бути налаштований у файлі tnsnames.ora вашої інсталяції Oracle-клієнта. Тут ви вказуєте дескриптор підключення (host, port, service name).

#### Крок 2 – Тестування підключення

Натисніть кнопку **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Введіть пароль і натисніть кнопку **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Тепер ви можете налаштувати *digna* для використання ODBC-підключення, або з **DSN (Data Source Name)**, або у конфігурації **без DSN**.

---

### A. Конфігурація на основі DSN

#### Конфігурація *digna*

На екрані **"Create a Database Connection"** вкажіть наступне:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> Значення `DSN` має співпадати з ім'ям, визначеним у конфігурації вашого ODBC-драйвера.

---

### B. Конфігурація без DSN

#### Конфігурація *digna*

На екрані **"Create a Database Connection"** вкажіть наступне:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```
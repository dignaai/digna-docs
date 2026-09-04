---
title: Teradata Connector – інтеграція бази даних | документація digna
description: Налаштуйте digna для підключення до Teradata за допомогою Python-драйвера teradatasql або драйвера ODBC Teradata. Підтримується автентифікація на основі пароля у конфігураціях з DSN або без DSN.
image: /assets/logo_square.png
---


# Конектор джерела для Teradata

У цьому посібнику описано, як налаштувати *digna* для підключення до Teradata за допомогою нативного Python-конектора або драйвера ODBC.

Він посилається на екран **«Create a Database Connection»**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Нативний Python-драйвер

**Library:** `teradatasql`  
**Підтримувана автентифікація:** лише автентифікація на основі пароля

> Для інших методів автентифікації використовуйте драйвер ODBC.

### Налаштування *digna* (нативний драйвер)

Надайте наступну інформацію на екрані **"Create a Database Connection"**:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## Драйвер ODBC

Драйвер ODBC може підтримувати ширший спектр варіантів автентифікації та підключення. У цьому розділі розглянуто автентифікацію на основі пароля за допомогою драйвера **Teradata Database ODBC Driver 20.00**.

### 1. Встановлення драйвера ODBC

Встановіть драйвер **Teradata Database ODBC Driver 20.00** (або подібний), дотримуючись офіційного посібника з установки від постачальника.

### 2. Налаштування джерела даних ODBC

Виконайте ці кроки, щоб налаштувати нове джерело ODBC з автентифікацією на основі пароля:

#### Крок 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Натисніть кнопку **Test**.

#### Крок 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Введіть ім'я користувача та пароль.

Натисніть кнопку **OK**. Коли з'явиться екран про успішне налаштування, ODBC налаштовано правильно.

---

Тепер ви можете налаштувати *digna* для використання з'єднання ODBC — або з використанням **DSN (Data Source Name)**, або в конфігурації без DSN (DSN-less).

---

### A. Конфігурація на основі DSN

#### Налаштування *digna*

На екрані **"Create a Database Connection"** надайте наступне:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> Значення `DSN` має збігатися з ім'ям, визначеним у конфігурації вашого ODBC-драйвера.

---

### B. Конфігурація без DSN (DSN-less)

#### Налаштування *digna*

На екрані **"Create a Database Connection"** надайте наступне:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
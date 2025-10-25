---
title: Netezza Connector – Інтеграція бази даних | digna Документація
description: Налаштуйте digna для підключення до Netezza за допомогою ODBC-драйвера NetezzaSQL. Підтримується автентифікація за паролем з використанням DSN або без DSN для гнучкого підключення.
image: /assets/logo_square.png
---


# Підключення джерела для Netezza

Цей посібник описує, як налаштувати *digna* для підключення до Netezza за допомогою ODBC-драйвера.

Він посилається на екран **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC-драйвер

ODBC-драйвер може підтримувати різні варіанти автентифікації та підключення. У цьому розділі йдеться про автентифікацію за паролем з використанням драйвера **NetezzaSQL**.

### 1. Встановіть ODBC-драйвер

Встановіть драйвер **NetezzaSQL** (або подібний) відповідно до офіційного посібника постачальника.

### 2. Налаштуйте джерело даних ODBC

Виконайте наведені кроки, щоб налаштувати нове джерело даних ODBC з автентифікацією за паролем:

#### Крок 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Залежно від вашого драйвера Netezza, вимог до налаштування та безпеки, можливо, доведеться також вказати дані на вкладках **Advanced DSN Options**, **SSL DSN Options** або **Driver Options**. Для найпростішого налаштування достатньо вказати дані у вкладці **DSN Options**.

Натисніть кнопку **Test Connection**.

#### Крок 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Коли ви побачите екран успіху, ODBC налаштовано правильно.

---

Тепер ви можете налаштувати *digna* для використання ODBC-зʼєднання — або з **DSN (Data Source Name)**, або в режимі **DSN-less**.

---

### A. Конфігурація на основі DSN

#### Конфігурація *digna*

На екрані **"Create a Database Connection"** вкажіть наступне:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN` має відповідати назві, визначеній у конфігурації вашого ODBC-драйвера.

---

### B. Конфігурація без DSN (DSN-less)

#### Конфігурація *digna*

На екрані **"Create a Database Connection"** вкажіть наступне:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
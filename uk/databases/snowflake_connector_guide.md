# Джерелo підключення для Snowflake

Цей посібник описує, як налаштувати *digna* для підключення до Snowflake з використанням або нативного Python-конектора, або ODBC-драйвера.

Він посилається на екран **«Створити підключення до бази даних»**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Нативний Python-драйвер

**Бібліотека:** `snowflake-connector-python`  
**Підтримувана автентифікація:** лише автентифікація за паролем

> Для інших методів автентифікації, будь ласка, використовуйте ODBC-драйвер.

### Конфігурація *digna* (нативний драйвер)

Надайте таку інформацію на екрані **«Створити підключення до бази даних»**:

```
Technology:      Snowflake
Host Address:    Назва облікового запису Snowflake
Host Port:       Не потрібно
Database Name:   База даних, що містить вихідну схему
Schema Name:     Схема, що містить вихідні дані
User Name:       Ім'я користувача та warehouse у форматі "user<@>warehouse"
User Password:   Пароль для користувача
Use ODBC:        Вимкнено (за замовчуванням)
```

---

## ODBC-драйвер

ODBC-драйвер може підтримувати ширший набір опцій автентифікації та підключення. Цей розділ зосереджений на автентифікації за паролем з використанням **SnowflakeDSIIDriver**.

### 1. Встановіть ODBC-драйвер

Встановіть **SnowflakeDSIIDriver**, дотримуючись офіційного посібника з встановлення від постачальника.

### 2. Налаштуйте джерело даних ODBC

Виконайте ці кроки, щоб налаштувати нове джерело даних ODBC з автентифікацією за паролем:

#### Крок 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Примітки:
- Якщо ви не вкажете значення для Database, Schema і Warehouse, то їх доведеться вказати як властивості ODBC під час конфігурації джерела даних у *digna*.
- Значення для "Server" складається з назви вашого облікового запису Snowflake з додаванням ".snowflakecomputing.com"

#### Крок 2 – Перевірка з’єднання

Натисніть кнопку **TEST**. Успішне підключення має виглядати так:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Тепер ви можете налаштувати *digna* для використання ODBC-з’єднання, або з **DSN (Data Source Name)**, або у **без-DSN** конфігурації.

---

### A. Конфігурація на основі DSN

#### Конфігурація *digna*

На екрані **«Створити підключення до бази даних»** вкажіть наступне:

```
Technology:      Snowflake
Database Name:   База даних, що містить вихідну схему
Schema Name:     Схема, що містить вихідні дані
Use ODBC:        Увімкнено
```

#### Властивості ODBC

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> Значення `DSN` має відповідати імені, визначеному у конфігурації вашого ODBC-драйвера.

---

### B. Конфігурація без DSN

#### Конфігурація *digna*

На екрані **«Створити підключення до бази даних»** вкажіть наступне:

```
Technology:      Snowflake
Database Name:   Схема, що містить вихідні дані (те саме, що Schema Name)
Schema Name:     Схема, що містить вихідні дані
Use ODBC:        Увімкнено
```

#### Властивості ODBC

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```
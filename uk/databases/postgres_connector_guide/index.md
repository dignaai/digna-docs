# Конектор джерела для PostgreSQL

Цей посібник описує, як налаштувати *digna* для підключення до Postgres за допомогою нативного Python-конектора або ODBC-драйвера.

Він посилається на екран **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Нативний Python-драйвер

**Бібліотека:** `psycopg`  
**Підтримувана автентифікація:** лише автентифікація на основі пароля

> Для інших методів автентифікації, будь ласка, використовуйте ODBC-драйвер.

### *digna* — конфігурація (нативний драйвер)

Вкажіть наступну інформацію на екрані **"Create a Database Connection"**:

```
Technology:      Postgres
Host Address:    Ім'я сервера або IP-адреса
Host Port:       Номер порту, наприклад 5432
Database Name:   Назва бази даних
Schema Name:     Схема, що містить вихідні дані
User Name:       Ім'я користувача бази даних
User Password:   Пароль користувача
Use ODBC:        Disabled (default)
```

---

## ODBC-драйвер

ODBC-драйвер може підтримувати ширший спектр варіантів автентифікації та підключення. У цьому розділі йдеться про автентифікацію на основі пароля з використанням драйвера **PostgreSQL Unicode(x64)**.

### 1. Встановіть ODBC-драйвер

Встановіть **PostgreSQL Unicode(x64)** (або подібний) згідно з офіційною інструкцією постачальника.

### 2. Налаштуйте джерело даних ODBC

Дотримуйтесь цих кроків, щоб налаштувати нове джерело даних ODBC з автентифікацією на основі пароля:

#### Крок 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Примітка: Якщо ваша конфігурація бази даних вимагає вибору конкретного "SSLMode", обов’язково використайте той самий параметр при визначенні конфігурації без DSN.

#### Крок 2 – Перевірка підключення

Натисніть кнопку **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Тепер ви можете налаштувати *digna* для використання ODBC-підключення, або з **DSN (Data Source Name)**, або у **DSN-less** режимі.

---

### A. Конфігурація на основі DSN

#### *digna* — конфігурація

На екрані **"Create a Database Connection"** вкажіть наступне:

```
Technology:      PostgreSQL
Database Name:   База даних, що містить схему джерела
Schema Name:     Схема, що містить вихідні дані
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "DSN",    value: "PostgreSQL35W"
```

> `DSN` повинен відповідати назві, визначеній у конфігурації вашого ODBC-драйвера.

---

### B. Конфігурація без DSN (DSN-less)

#### *digna* — конфігурація

На екрані **"Create a Database Connection"** вкажіть наступне:

```
Technology:      PostgreSQL
Database Name:   Схема, що містить вихідні дані (те ж, що і Schema Name)
Schema Name:     Схема, що містить вихідні дані
Use ODBC:        Enabled
```

#### Властивості ODBC

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user"
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```
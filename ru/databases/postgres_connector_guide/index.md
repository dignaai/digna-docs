# Source Connector for PostgreSQL

В этом руководстве описано, как настроить *digna* для подключения к Postgres с использованием либо нативного Python-коннектора, либо ODBC-драйвера.

Речь идёт о экране **"Create a Database Connection"**.

![Создать подключение к базе данных](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Supported Authentication:** Только аутентификация по паролю

> Для других методов аутентификации используйте, пожалуйста, ODBC-драйвер.

### *digna* Configuration (Native Driver)

Укажите следующую информацию на экране **"Create a Database Connection"**:

```
Technology:      Postgres
Host Address:    Имя сервера или IP-адрес
Host Port:       Номер порта, например 5432
Database Name:   Имя базы данных
Schema Name:     Схема, содержащая исходные данные
User Name:       Имя пользователя базы данных
User Password:   Пароль пользователя
Use ODBC:        Disabled (по умолчанию)
```

---

## ODBC Driver

ODBC-драйвер может поддерживать более широкий набор методов аутентификации и вариантов подключения. Этот раздел фокусируется на аутентификации по паролю с использованием драйвера **PostgreSQL Unicode(x64)**.

### 1. Установите ODBC-драйвер

Установите **PostgreSQL Unicode(x64)** (или аналогичный) следуя официальному руководству поставщика.

### 2. Настройте источник данных ODBC

Выполните следующие шаги, чтобы настроить новый источник данных ODBC с аутентификацией по паролю:

#### Шаг 1
![Шаг 1](images/postgres/create_odbc_data_source_step1.png)

Примечание: если ваша настройка базы данных требует выбора конкретного "SSLMode", обязательно используйте то же значение при определении DSN-less конфигурации.

#### Шаг 2 — Тест подключения

Нажмите кнопку **Test Connection**.

![Шаг 2](images/postgres/create_odbc_data_source_step2.png)

---

Теперь вы можете настроить *digna* для использования ODBC-подключения — либо с **DSN (Data Source Name)**, либо в **DSN-less** варианте.

---

### A. DSN-Based Configuration

#### *digna* Configuration

На экране **"Create a Database Connection"** укажите следующее:

```
Technology:      PostgreSQL
Database Name:   База данных, содержащая исходную схему
Schema Name:     Схема, содержащая исходные данные
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "PostgreSQL35W"
```

> `DSN` должен совпадать с именем, определённым в конфигурации вашего ODBC-драйвера.

---

### B. DSN-less Configuration

#### *digna* Configuration

На экране **"Create a Database Connection"** укажите следующее:

```
Technology:      PostgreSQL
Database Name:   Схема, содержащая исходные данные (то же, что и Schema Name)
Schema Name:     Схема, содержащая исходные данные
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```
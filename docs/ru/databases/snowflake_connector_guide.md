---
title: Snowflake Connector – Интеграция базы данных | digna Documentation
description: Настройте digna для подключения к Snowflake с помощью Python-коннектора или ODBC-драйвера Snowflake. Поддерживается аутентификация по паролю с конфигурациями через DSN или без DSN.
image: /assets/logo_square.png
---


# Source Connector for Snowflake

В этом руководстве описывается, как настроить *digna* для подключения к Snowflake с использованием либо нативного Python-коннектора, либо ODBC-драйвера.

Оно относится к экрану **"Создать подключение к базе данных"**.

![Создать подключение к базе данных](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Библиотека:** `snowflake-connector-python`  
**Поддерживаемая аутентификация:** Только аутентификация по паролю

> Для других методов аутентификации используйте ODBC-драйвер.

### Конфигурация *digna* (нативный драйвер)

Укажите следующую информацию на экране **"Создать подключение к базе данных"**:

```
Technology:      Snowflake
Host Address:    имя аккаунта Snowflake
Host Port:       Не требуется
Database Name:   База данных, содержащая исходную схему
Schema Name:     Схема, содержащая исходные данные
User Name:       Имя пользователя и warehouse в формате "user<@>warehouse"
User Password:   Пароль пользователя
Use ODBC:        Отключено (по умолчанию)
```

---

## ODBC Driver

ODBC-драйвер может поддерживать более широкий набор вариантов аутентификации и подключения. В этом разделе рассматривается аутентификация по паролю с использованием **SnowflakeDSIIDriver**.

### 1. Установите ODBC-драйвер

Установите **SnowflakeDSIIDriver**, следуя официальному руководству поставщика.

### 2. Настройте источник данных ODBC

Выполните следующие шаги для настройки нового источника данных ODBC с аутентификацией по паролю:

#### Шаг 1
![Шаг 1](images/snowflake/create_odbc_data_source_step1.png)

Примечания:
- Если вы не укажете значения для Database, Schema и Warehouse, то их нужно будет передать как ODBC-свойства при конфигурации источника данных в *digna*.
- Значение для "Server" состоит из имени вашего аккаунта Snowflake, за которым следует ".snowflakecomputing.com"

#### Шаг 2 – Тестирование подключения

Нажмите кнопку **TEST**. Успешное подключение должно выглядеть так:

![Шаг 2](images/snowflake/create_odbc_data_source_step2.png)

---

Теперь вы можете настроить *digna* для использования ODBC-подключения либо с **DSN (Data Source Name)**, либо в **DSN-less** конфигурации.

---

### A. Конфигурация на основе DSN

#### Конфигурация *digna*

На экране **"Создать подключение к базе данных"** укажите следующее:

```
Technology:      Snowflake
Database Name:   База данных, содержащая исходную схему
Schema Name:     Схема, содержащая исходные данные
Use ODBC:        Включено
```

#### ODBC-свойства

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{ваш пароль в фигурных скобках}"

опционально:
name: "Database",       value: "База данных, содержащая исходную схему"
name: "Schema",         value: "Схема, содержащая исходные данные"
name: "Warehouse",      value: "Warehouse для выполнения SQL-запросов"
```

> `DSN` должен совпадать с именем, определённым в конфигурации вашего ODBC-драйвера.

---

### B. DSN-less конфигурация

#### Конфигурация *digna*

На экране **"Создать подключение к базе данных"** укажите следующее:

```
Technology:      Snowflake
Database Name:   Схема, содержащая исходные данные (то же, что Schema Name)
Schema Name:     Схема, содержащая исходные данные
Use ODBC:        Включено
```

#### ODBC-свойства

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "База данных, содержащая исходную схему"
name: "Schema",     value: "Схема, содержащая исходные данные"
name: "Warehouse",  value: "Warehouse для выполнения SQL-запросов"
```
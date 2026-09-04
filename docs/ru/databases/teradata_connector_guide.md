---
title: Коннектор Teradata — интеграция с базой данных | документация digna
description: Настройка digna для подключения к Teradata с использованием Python-драйвера teradatasql или ODBC-драйвера Teradata. Поддерживается аутентификация по паролю с DSN и без DSN.
image: /assets/logo_square.png
---


# Source Connector for Teradata

Это руководство описывает, как настроить *digna* для подключения к Teradata с помощью нативного Python-коннектора или ODBC-драйвера.

Речь идёт о экране **"Создать подключение к базе данных"**.

![Создание подключения к базе данных](images/data_source_config_input_mask.png)

---

## Нативный Python-драйвер

**Library:** `teradatasql`  
**Supported Authentication:** Password-based authentication only

> Для других методов аутентификации используйте драйвер ODBC.

### *digna* Configuration (Native Driver)

Provide the following information in the **"Create a Database Connection"** screen:

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

## ODBC Driver

ODBC-драйвер может поддерживать более широкий набор методов аутентификации и вариантов подключения. Этот раздел посвящён аутентификации по паролю с использованием драйвера **Teradata Database ODBC Driver 20.00**.

### 1. Установите ODBC-драйвер

Установите драйвер **Teradata Database ODBC Driver 20.00** (или аналогичный), следуя официальному руководству по установке от вендора.

### 2. Настройте источник данных ODBC

Выполните следующие шаги, чтобы настроить новый источник данных ODBC с аутентификацией по паролю:

#### Шаг 1
![Шаг 1](images/teradata/create_odbc_data_source_step1.png)

Нажмите кнопку **Test**.

#### Шаг 2
![Шаг 2](images/teradata/create_odbc_data_source_step2.png)

Укажите имя пользователя и пароль.

Нажмите кнопку **OK**.
Когда появится экран с сообщением об успешном подключении, ODBC сконфигурирован корректно.

---

Теперь вы можете настроить *digna* на использование ODBC-подключения — либо через **DSN (Data Source Name)**, либо в **DSN-less** режиме.

---

### A. Конфигурация на основе DSN

#### *digna* Configuration

На экране **"Создать подключение к базе данных"** укажите следующее:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Свойства ODBC

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN` должен соответствовать имени, указанному в конфигурации вашего ODBC-драйвера.

---

### B. Конфигурация без DSN

#### *digna* Configuration

На экране **"Создать подключение к базе данных"** укажите следующее:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Свойства ODBC

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
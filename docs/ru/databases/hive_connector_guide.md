---
title: Коннектор Apache Hive – интеграция с базой данных | digna Documentation
description: Настройте digna для подключения к Apache Hive с использованием нативного драйвера PyHive или ODBC-драйвера Cloudera. Поддерживаются аутентификация по паролю и конфигурации через DSN или без DSN.
image: /assets/logo_square.png
---


# Коннектор источника для Hive

В этом руководстве описано, как настроить *digna* для подключения к Hive с помощью либо нативного Python-коннектора, либо ODBC-драйвера.

Руководство относится к экрану **«Create a Database Connection»**.

![Создание подключения к базе данных](images/data_source_config_input_mask.png)

---

## Нативный Python-драйвер

**Library:** `PyHive`  
**Поддерживаемая аутентификация:** только аутентификация по паролю

> Для других методов аутентификации используйте ODBC-драйвер.

### Конфигурация *digna* (нативный драйвер)

Укажите следующую информацию на экране **«Create a Database Connection»**:

```
Technology:      Apache Hive
Host Address:    Имя сервера или IP-адрес
Host Port:       Номер порта, например 10000
Database Name:   Схема, содержащая исходные данные
Schema Name:     Схема, содержащая исходные данные
User Name:       Имя пользователя базы данных
User Password:   Пароль пользователя
Use ODBC:        Отключено (по умолчанию)
```

---

## ODBC-драйвер

ODBC-драйвер может поддерживать более широкий набор опций аутентификации и подключения. В этом разделе рассматривается аутентификация по паролю с использованием драйвера **Cloudera ODBC Driver for Apache Hive**.

### 1. Установите ODBC-драйвер

Установите **Cloudera ODBC Driver for Apache Hive** (или аналогичный) в соответствии с официальным руководством поставщика.

### 2. Настройте источник данных ODBC

Выполните следующие шаги, чтобы настроить новый источник данных ODBC с использованием аутентификации по паролю:

#### Шаг 1
![Шаг 1](images/hive/create_odbc_data_source_step1.png)


#### Шаг 2 – Тест подключения

Введите пароль и нажмите кнопку **Test**.

![Шаг 2](images/hive/create_odbc_data_source_step2.png)

После успешного теста нажмите кнопку **OK**.

---

Теперь вы можете настроить *digna* для использования ODBC-подключения — либо через **DSN (Data Source Name)**, либо в конфигурации без DSN.

---

### A. Конфигурация на основе DSN

#### Конфигурация *digna*

На экране **«Create a Database Connection»** укажите следующее:

```
Technology:      Apache Hive
Database Name:   Схема, содержащая исходные данные (то же, что и Schema Name)
Schema Name:     Схема, содержащая исходные данные
Use ODBC:        Включено
```

#### Свойства ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{ваш пароль в фигурных скобках}"
```

> `DSN` должен совпадать с именем, указанным в конфигурации вашего ODBC-драйвера.

---

### B. Конфигурация без DSN

#### Конфигурация *digna*

На экране **«Create a Database Connection»** укажите следующее:

```
Technology:      Apache Hive
Database Name:   Схема, содержащая исходные данные (то же, что и Schema Name)
Schema Name:     Схема, содержащая исходные данные
Use ODBC:        Включено
```

#### Свойства ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "имя вашего сервера или IP-адрес"
name: "PORT",       value: "Номер порта, например 10000"
name: "Schema",     value: "Схема, содержащая исходные данные"
name: "UID",        value: "ваш пользователь Hive"
name: "PWD",        value: "ваш пароль Hive"
name: "AuthMech",   value: "3"
```
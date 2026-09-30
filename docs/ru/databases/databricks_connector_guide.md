---
title: Коннектор Databricks – интеграция с базой данных | digna Documentation
description: Настройте подключение digna к Databricks с Unity Catalog через ODBC со строкой подключения без DSN. Описаны драйвер Databricks ODBC, personal access tokens, HTTP path и настройки подключения на стороне digna.
image: /assets/logo_square.png
---

# Коннектор источника для Databricks

Это руководство описывает, как настроить *digna* для подключения к Databricks через **ODBC** со
строкой подключения **без DSN** (DSN-less).

Сторона *digna* одинакова для всех технологий — где создаются подключения, как шифруются
значения свойств, как проверяется подключение и что означают режимы профилирования. Она описана
в разделе [Обзор подключений к базам данных](overview.md). Эта страница описывает то, что
специфично для Databricks.

!!! note "Требуется Unity Catalog"

    *digna* считывает доступные каталоги из `system.information_schema.catalogs`, поэтому в
    рабочей области должен быть включён Unity Catalog. В ранних релизах *digna* для рабочих
    областей без Unity Catalog была отдельная технология «Databricks Legacy»; она больше
    недоступна.

---

## 1. Установка драйвера ODBC {: #1-install-the-odbc-driver }

Установите **Databricks ODBC Driver** на машину, где работает бэкенд *digna*, следуя
[руководству по установке Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

В зависимости от версии драйвер регистрируется как **Simba Spark ODBC Driver** или как
**Databricks ODBC Driver**. Узнайте точное зарегистрированное имя на вашем хосте, как описано в
разделе [Установка драйвера ODBC на хосте digna](overview.md#install-the-driver).

---

## 2. Сбор параметров подключения {: #2-gather-the-connection-details }

Все значения берутся из SQL warehouse (или кластера), который должна использовать *digna*.
Откройте его в рабочей области Databricks и перейдите в **Connection details**:

| Поле Databricks | Используется как |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, обычно `443` |
| **HTTP path** | `HTTPPath` |

Для аутентификации создайте **personal access token** — см.
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Токены принадлежат пользователю или сервисному принципалу (service principal), и этому
принципалу нужны права `USE CATALOG`, `USE SCHEMA` и `SELECT` на исходные данные.

---

## 3. Свойства ODBC {: #3-odbc-properties }

!!! important "Пример, а не спецификация"

    Набор ниже — одна комбинация, которая заведомо работает. Свойства принадлежат драйверу
    Databricks/Simba, поэтому их имена, значения по умолчанию и допустимые значения различаются
    между версиями драйвера — драйвер не раз переименовывали и расширяли его параметры
    аутентификации — и между платформами. Используйте этот набор как отправную точку и
    сверяйтесь с документацией установленной версии драйвера.

Добавьте следующие свойства на экране **Add DB Connection**:

| Ключ | Пример значения | Примечания |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Должно совпадать с именем драйвера, зарегистрированным на хосте *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | Server hostname хранилища, например `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP path хранилища или кластера |
| `SSL` | `1` | Конечные точки Databricks работают только по TLS |
| `ThriftTransport` | `2` | Транспорт HTTP, который используют конечные точки SQL |
| `AuthMech` | `3` | Аутентификация по токену |
| `UID` | `token` | Буквально слово `token`, а не имя пользователя |
| `PWD` | `dapi…` | Personal access token. Отметьте **Encrypted** |
| `UseNativeQuery` | `1` | Передаёт SQL *digna* без изменений — см. ниже |

Итоговая строка подключения выглядит так:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Оставляйте `UseNativeQuery=1`"

    При `UseNativeQuery=0` — значении драйвера по умолчанию — драйвер переписывает входящий SQL
    в то, что он считает переносимым синтаксисом ODBC. *digna* уже генерирует Databricks SQL,
    поэтому такое переписывание может изменить экранирование обратными кавычками и литералы дат,
    и профилирование завершается ошибкой на операторах, которые корректны в исходном виде.

### OAuth вместо токена

Для сервисного принципала с аутентификацией OAuth machine-to-machine замените `AuthMech`,
`UID` и `PWD` на:

| Ключ | Пример значения | Примечания |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Сервисный принципал |
| `Auth_Client_Secret` | `<client secret>` | Отметьте **Encrypted** |

---

## 4. Настройка *digna* {: #4-digna-configuration }

На экране **Add DB Connection** укажите следующее:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Особенности Databricks {: #5-notes-on-databricks }

- **Хранилище (warehouse) должно быть запущено** или иметь возможность запуститься в момент
  подключения *digna*. Запуск хранилища из остановленного состояния может занять больше времени,
  чем тайм-аут подключения, — если проверка не проходит с первой попытки после простоя,
  повторите её.
- **Каталоги берутся из рабочей области.** В отличие от большинства технологий, одно подключение
  к Databricks охватывает все каталоги, которые разрешено видеть принципалу, поэтому одно
  подключение может обслуживать источники из разных каталогов.
- **Режимы профилирования.** *Permanent* создаёт рабочие таблицы в **Work Schema** внутри
  каталога источника, поэтому принципалу нужно право `CREATE TABLE` в ней. *Session* использует
  `CREATE TEMPORARY TABLE` и не затрагивает **Work Schema**. Для *Standard* нужен только доступ на
  чтение.
- **Бессерверные хранилища (serverless warehouses) работают** так же; отличается только
  `HTTPPath`.

---

## 6. Проверка драйвера (необязательно) {: #6-verifying-the-driver-optional }

Для подключения без DSN настраивать источник данных ODBC не требуется, но собственный диалог
драйвера — удобный способ убедиться, что драйвер, хранилище и токен работают, прежде чем
вводить их в *digna*.

#### Шаг 1
![Шаг 1](images/databricks/create_odbc_data_source_step1.png)

#### Шаг 2
![Шаг 2](images/databricks/create_odbc_data_source_step2.png)

#### Шаг 3
![Шаг 3](images/databricks/create_odbc_data_source_step3.png)

#### Шаг 4
![Шаг 4](images/databricks/create_odbc_data_source_step4.png)

#### Шаг 5 – проверка подключения

Нажмите кнопку **TEST**. Успешное подключение должно выглядеть так:

![Шаг 5](images/databricks/create_odbc_data_source_step5.png)

Введённые здесь хост, HTTP path и токен — это именно те значения, которые принимают свойства из
[раздела 3](#3-odbc-properties).

# Конектор джерела для Databricks

У цьому посібнику описано, як налаштувати *digna* для підключення до Databricks через **ODBC** за
допомогою рядка підключення **без DSN**.

Налаштування на боці *digna* однакове для всіх технологій — де створюються підключення, як
шифруються значення властивостей, як тестується підключення та що означають режими профілювання.
Це описано в розділі [Огляд підключень до баз даних](overview.md). Ця сторінка охоплює те, що
специфічне для Databricks.

!!! note "Потрібен Unity Catalog"

    *digna* зчитує доступні каталоги з `system.information_schema.catalogs`, тому в робочій області
    має бути ввімкнено Unity Catalog. Попередні випуски *digna* пропонували окрему технологію
    "Databricks Legacy" для робочих областей без Unity Catalog; вона більше недоступна.

---

## 1. Встановлення драйвера ODBC {: #1-install-the-odbc-driver }

Встановіть **Databricks ODBC Driver** на машині, де працює бекенд *digna*, відповідно до
[посібника зі встановлення Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

Залежно від версії драйвер реєструється як **Simba Spark ODBC Driver** або як
**Databricks ODBC Driver**. Прочитайте точну зареєстровану назву на своєму хості, як описано в розділі
[Встановлення драйвера ODBC на хості digna](overview.md#install-the-driver).

---

## 2. Збирання параметрів підключення {: #2-gather-the-connection-details }

Усі значення беруться зі сховища SQL (SQL warehouse) або кластера, яке має використовувати *digna*.
Відкрийте його в робочій області Databricks і перейдіть до **Connection details**:

| Поле Databricks | Використовується як |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, зазвичай `443` |
| **HTTP path** | `HTTPPath` |

Для автентифікації створіть **персональний токен доступу** — див.
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Токени належать користувачеві або принципалу служби (service principal), і цьому принципалу потрібні
права `USE CATALOG`, `USE SCHEMA` і `SELECT` на дані джерела.

---

## 3. Властивості ODBC {: #3-odbc-properties }

!!! important "Приклад, а не специфікація"

    Наведений нижче набір — одна комбінація, яка гарантовано працює. Властивості належать драйверу
    Databricks/Simba, тому їхні назви, значення за замовчуванням і допустимі значення відрізняються
    між версіями драйвера — драйвер неодноразово перейменовували й розширювали його параметри
    автентифікації — і між платформами. Використовуйте це як відправну точку та звіряйтеся з
    документацією встановленої версії драйвера.

Додайте такі властивості на екрані **Add DB Connection**:

| Ключ | Приклад значення | Примітки |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Має збігатися з назвою драйвера, зареєстрованою на хості *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | Ім'я хоста сервера сховища, наприклад `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP-шлях сховища або кластера |
| `SSL` | `1` | Кінцеві точки Databricks працюють лише через TLS |
| `ThriftTransport` | `2` | Транспорт HTTP, який використовують кінцеві точки SQL |
| `AuthMech` | `3` | Автентифікація токеном |
| `UID` | `token` | Буквально слово `token`, а не ім'я користувача |
| `PWD` | `dapi…` | Персональний токен доступу. Позначте **Encrypted** |
| `UseNativeQuery` | `1` | Передає SQL від *digna* без змін — див. нижче |

Отриманий рядок підключення виглядає так:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Залишайте `UseNativeQuery=1`"

    З `UseNativeQuery=0` — значенням драйвера за замовчуванням — драйвер переписує вхідний SQL у
    те, що вважає переносимим синтаксисом ODBC. *digna* вже генерує Databricks SQL, тому таке
    переписування може змінити екранування зворотними апострофами та літерали дат, і тоді
    профілювання не вдається на інструкціях, які в початковому вигляді є коректними.

### OAuth замість токена

Для принципала служби з автентифікацією OAuth між машинами (machine-to-machine) замініть `AuthMech`,
`UID` і `PWD` на:

| Ключ | Приклад значення | Примітки |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Облікові дані клієнта |
| `Auth_Client_ID` | `<application id>` | Принципал служби |
| `Auth_Client_Secret` | `<client secret>` | Позначте **Encrypted** |

---

## 4. Налаштування *digna* {: #4-digna-configuration }

На екрані **Add DB Connection** вкажіть таке:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Примітки щодо Databricks {: #5-notes-on-databricks }

- **Сховище має працювати** або мати змогу запуститися, коли *digna* підключається. Сховищу, яке
  відновлюється зі стану зупинки, може знадобитися більше часу, ніж тайм-аут підключення — якщо
  тест не вдається з першої спроби після періоду простою, повторіть його.
- **Каталоги беруться з робочої області.** На відміну від більшості технологій, одне підключення
  Databricks має доступ до кожного каталогу, який дозволено бачити принципалу, тому одне
  підключення може обслуговувати джерела з різних каталогів.
- **Режими профілювання.** *Permanent* створює робочі таблиці в **Work Schema** всередині каталогу
  джерела, тому принципалу потрібне там право `CREATE TABLE`. *Session* використовує
  `CREATE TEMPORARY TABLE` і не зачіпає **Work Schema**. *Standard* потребує лише доступу
  для читання.
- **Безсерверні сховища працюють** так само; відрізняється лише `HTTPPath`.

---

## 6. Перевірка драйвера (необов'язково) {: #6-verifying-the-driver-optional }

Для підключення без DSN налаштовувати джерело даних ODBC не потрібно, але власний діалог драйвера —
зручний спосіб переконатися, що драйвер, сховище й токен працюють, перш ніж вводити їх у *digna*.

#### Крок 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Крок 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Крок 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Крок 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Крок 5 – Тестування підключення

Натисніть кнопку **TEST**. Успішне підключення має виглядати так:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

Хост, HTTP-шлях і токен, введені тут, — саме ті значення, які приймають властивості з
[розділу 3](#3-odbc-properties).
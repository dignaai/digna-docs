---
title: Посібник зі встановлення на Windows – digna Release 2026.06 | Документація digna
description: Покроковий посібник зі встановлення digna Release 2026.06 на Windows — системні вимоги, налаштування PostgreSQL, конфігурація веб‑сервера, налаштування backend і dashboard, запуск digna як служби Windows та оновлення до нової версії.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Windows Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** August 30, 2026


---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Setup](#pre-installation-setup)
4. [PostgreSQL Server Setup](#postgresql-server-setup)
5. [Web Server Configuration](#web-server-configuration)
6. [Initial Installation](#initial-installation)
7. [Backend Configuration](#backend-configuration)
8. [Dashboard Configuration](#dashboard-configuration)
9. [Running digna as a Windows Service](#running-digna-as-a-windows-service)
10. [Upgrading to a New Release](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### About digna

digna — це комплексна платформа з підтримкою AI, призначена для оптимізації управління якістю даних у різних середовищах (warehouses, lakes, lakehouses). Побудована для високої масштабованості та адаптивності, digna вирішує сучасні завдання роботи з даними через автоматизацію, моніторинг у реальному часі та виявлення аномалій.

digna складається з двох основних компонентів:

- **digna**: ядро застосунку, відповідальне за обробку даних і виконання перевірок якості. Воно поєднує серверну частину та інтерфейс командного рядка в одному виконуваному файлі, замінюючи окремі програми `dignabackend` і `dignacli` з попередніх випусків.
- **dignadashboard**: веб‑інтерфейс, розміщений на веб‑сервері, що забезпечує зручний спосіб взаємодії з платформою digna та візуалізації метрик якості даних.

### What's New in Release 2026.06

У цьому релізі можливості спостереження за даними інтегровані безпосередньо в код, що дозволяє розробникам контролювати якість даних на джерелі. Деталі див. у [release notes](http://docs.digna.ai/changelog/Release_202606/).

### Шукаєте macOS або Linux?

Цей посібник охоплює Windows. Для інших платформ див. [Посібник зі встановлення macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) або [Посібник зі встановлення Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## System Requirements {: #system-requirements }

Перед початком встановлення переконайтесь, що ваша система відповідає мінімальним вимогам:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server or Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB available storage |
| **Database** | PostgreSQL Server 12 or higher |
| **Web Server** | IIS, Apache Tomcat, or equivalent |

### Database Installation Options

**If PostgreSQL is already installed:**
Ви можете додати нову базу даних для digna у вже існуючий сервер PostgreSQL.

**If installing PostgreSQL on the same machine as digna:**

!!! info "Recommended Specifications"

    - **Memory**: 32 GB RAM (замість 16 GB)
    - **Disk Space**: 50 GB available storage (замість 10 GB)

    Ці підвищені характеристики враховують одночасну роботу digna та PostgreSQL на одній машині.

---

## Pre-Installation Setup {: #pre-installation-setup }

Перед встановленням digna переконайтесь, що на місці є два ключові попередні компоненти:

1. **PostgreSQL Server** – для зберігання обчислених метрик та даних про продуктивність
2. **Web Server** – для розміщення digna Dashboard

Якщо ці компоненти ще не налаштовані, слідуйте розділам нижче для їх встановлення та конфігурації.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### If You Already Have PostgreSQL

Якщо PostgreSQL вже встановлений і працює локально або ви використовуєте керований віддалений PostgreSQL-сервер, можете перейти до [наступного розділу](#web-server-configuration).

### Installing PostgreSQL

Виконайте наступні кроки, щоб встановити PostgreSQL на Windows:

#### Step 1: Download PostgreSQL

1. Перейдіть на сторінку [PostgreSQL Downloads](https://www.postgresql.org/download/)
2. Оберіть **Windows**
3. Завантажте останній інсталятор

#### Step 2: Run the Installer

1. Двічі клацніть завантажений інсталятор
2. Дійте за підказками майстра встановлення

#### Step 3: Choose Installation Directory

Обрати каталог, куди буде встановлено PostgreSQL. Звичайне значення за замовчуванням підходить.

#### Step 4: Select Components

Для стандартної конфігурації залиште опції компонентів за замовчуванням.

#### Step 5: Set PostgreSQL Superuser Password

Введіть та підтвердіть пароль для суперкористувача PostgreSQL (`postgres`). **Збережіть цей пароль у безпечному місці** — він знадобиться пізніше.

#### Step 6: Configure Port Number

Стандартний порт PostgreSQL — `5432`. Можете використовувати значення за замовчуванням або вказати інший порт за потреби.

!!! tip "Tip"

    Якщо порт 5432 вже використовується, виберіть альтернативний порт і зафіксуйте його для подальшої конфігурації.

#### Step 7: Choose Locale

Виберіть локаль для вашої бази даних. За замовчуванням зазвичай підходить для більшості інсталяцій.

#### Step 8: Complete Installation

Клікайте **Next** у наступних кроках, потім **Finish**.

#### Step 9: Verify Installation

Відкрийте Command Prompt і перевірте установку PostgreSQL:

```bash
psql --version
```

Якщо інсталяція пройшла успішно, ви побачите версію PostgreSQL.

---

## Web Server Configuration {: #web-server-configuration }

digna потребує веб‑сервер для розміщення dashboard. Виберіть один із наступних варіантів:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Потрібно встановити і налаштувати лише **один** із цих серверів.

### IIS Setup {: #iis-setup }

#### Overview

Internet Information Services (IIS) — веб‑сервер Microsoft для розміщення сайтів і веб‑застосунків.

#### Enabling IIS

1. **Open Control Panel**
   - Натисніть `Win + R`
   - Введіть `control` і натисніть Enter

2. **Navigate to Windows Features**
   - Клацніть **Programs**
   - Оберіть **Turn Windows features on or off**

3. **Enable Internet Information Services**
   - Знайдіть **Internet Information Services (IIS)**
   - Позначте чекбокс, щоб увімкнути його
   - Розкрийте вкладку за допомогою **+** і переконайтеся, що вибрано такі підкомпоненти:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Click OK** для застосування змін

5. **Verify IIS Installation**
   - Відкрийте браузер
   - Перейдіть на `http://localhost`
   - Ви повинні побачити сторінку привітання IIS

#### Required: URL Rewrite Module

IIS вимагає компонент URL Rewrite. Завантажте та встановіть його з [офіційної сторінки Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Required: MIME Type for Markdown Files

Щоб Markdown‑файли (`.md`) коректно віддавались IIS:

1. Відкрийте **IIS Manager** (натисніть `Win + R`, введіть `inetmgr`, натисніть Enter)
2. Перейдіть до **Your Site > MIME Types**
3. Натисніть **Add...**
4. Налаштуйте:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Important"

    Без цієї настройки `.md` файли можуть не віддаватися коректно.

---

### Apache Tomcat Setup {: #apache-tomcat-setup }

#### Overview

Apache Tomcat — відкрите середовище для виконання Java‑серветів і веб‑сервер.

#### Installation

1. **Download Apache Tomcat**
   - Перейдіть на сторінку [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Завантажте ZIP‑розповсюдження для Windows

2. **Extract the Archive**
   - Розпакуйте ZIP у каталог на вашій системі
   - Наприклад: `C:\Program Files\Apache Tomcat`

3. **Verify Tomcat is Running**
   - Відкрийте браузер
   - Перейдіть на `http://localhost:8080`
   - Ви повинні побачити сторінку привітання Apache Tomcat

!!! tip "Tip"

    Зазвичай Apache Tomcat запускається автоматично після встановлення. Якщо ні, відкрийте папку `bin` і запустіть `startup.bat`.

---

## Initial Installation {: #initial-installation }

### Step 1: Set Up the digna Repository

Репозиторій digna зберігає всі метрики, обчислені digna. Він виступає центральною базою для аналітичних та показників продуктивності.

#### Create Repository Schema and User

Відкрийте ваш клієнт PostgreSQL (pgAdmin, psql або інший) і виконайте такі SQL‑команди:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Замініть наступні заповнювачі:**

- `<digna_repo_schema>` — бажана назва схеми (наприклад, `dignarepo`)
- `<digna_repo_user>` — бажане ім'я користувача (наприклад, `digna_user`)
- `<digna_repo_password>` — безпечний пароль для цього користувача

**Приклад:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Best Practice"

    Використовуйте сильні, складні паролі для користувачів бази даних. Уникайте легко вгадуваних облікових даних.

---

### Step 2: Extract the digna Installation Package

1. Знайдіть ZIP‑файл інсталяції digna, переданий вам
2. Розпакуйте його в обране місце встановлення
3. Після розпакування ви побачите наступні елементи:
   - `dashboard/` — веб‑інтерфейс
   - `digna` — основний виконуваний файл (backend + CLI разом)
   - `config.toml` — файл конфігурації
   - `license.toml` — файл ліцензії (скопіюйте сюди свій)

### Step 3: Install the License File

!!! warning "Important"

    Файл ліцензії **не** входить до пакета встановлення і надається окремо компанією digna.

1. Знайдіть файл `license.toml`, наданий вам
2. Скопіюйте його в кореневий каталог встановлення digna (там, де знаходяться `config.toml` та виконуваний файл `digna`)

**Чому це важливо:**
Файл ліцензії містить інформацію про клієнта, дату закінчення ліцензії та цифровий підпис. **Не змінюйте цей файл** — будь‑які зміни зроблять його недійсним.

**Структура директорії після налаштування:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend Configuration {: #backend-configuration }

### Step 1: Create and Edit the Configuration File

Файл `config_template.toml` постачається у вашому каталозі встановлення digna. Потрібно лише перейменувати його на `config.toml`.

**Location:** `digna_installation/config.toml`

Відкрийте `config.toml` у текстовому редакторі і налаштуйте кожен розділ нижче.

#### [app] Section

Цей розділ конфігурує налаштування backend застосунку digna:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | Якщо dashboard знаходиться на іншому сервері, додайте його URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Потрібно для CORS з обліковими даними |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Дозволити всі HTTP‑методи |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Дозволити всі заголовки |

#### [repo] Section

Цей розділ налаштовує підключення до PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` or IP | Хостнейм/IP PostgreSQL |
| `digna_REPO_PORT` | `5432` (default) | Порт PostgreSQL |
| `digna_REPO_DB` | `postgres` | Назва бази даних |
| `digna_REPO_SCHEMA` | `dignarepo` | Схема, створена раніше |
| `digna_REPO_USER` | `digna_user` | Користувач, створений у PostgreSQL |
| `digna_REPO_PASSWORD` | Your password | Пароль, заданий при створенні користувача |

#### [base] Section

Розділ з параметрами безпеки та cookie:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Має відповідати домену frontend |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (production) | Використовуйте `true` для HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Завжди увімкнено для безпеки |
| `digna_COOKIE_SAME_SITE` | `lax` | Запобігає CSRF‑атакам |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 hours) | Час життя сесії в секундах |
| `digna_MAX_WORKERS` | Number of CPU cores - 1 | Кількість паралельних завдань інспекції |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Максимальна затримка в секундах, яку планувальник може додати перед запуском завдання, термін якого настав |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Час доби (24-годинний формат `HH:MM`), коли починається щоденне очищення |

#### [encryption] Section

Цей розділ містить ключ, яким шифруються конфіденційні значення, що зберігаються в репозиторії. Він **обов'язковий** — `config check` повідомляє про розділ `[encryption]` як FAILED, якщо ключа немає.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Ключ у кодуванні Base64 | Шифрує конфіденційні значення, що зберігаються в репозиторії digna |

!!! warning "Захистіть config.toml"

    Цей ключ — фіксоване значення, однакове в усіх установленнях digna, і саме він розшифровує конфіденційні значення вашого репозиторію. Обмежте доступ до `config.toml` обліковим записом, під яким працює digna, тримайте файл поза системою контролю версій і спільними дисками та виключіть його з будь-якої резервної копії, що зберігається менш захищено, ніж сам репозиторій.

#### [logging] Section

Розділ конфігурації логування:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` or `DEBUG` | `INFO` — для production, `DEBUG` — для діагностики |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Кількість щоденних резервних логів для збереження |

---

### Step 2: Перевірте конфігурацію

Перед ініціалізацією репозиторію переконайтеся, що `config.toml` повний і правильно побудований. У каталозі встановлення digna виконайте:

```bash
digna config check
```

Кожен розділ перевіряється окремо, тож одна помилка не приховує стан решти:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK

Overall: OK
```

Виправте все, про що повідомлено як FAILED, і виконайте команду ще раз, перш ніж продовжувати. Повний перелік параметрів наведено в [довіднику CLI](../../../cli/Command_Line_Interface_202606.md).

### Step 3: Initialize the Repository

1. Відкрийте Command Prompt
2. Перейдіть до каталогу встановлення digna (там, де `config.toml` та виконуваний файл `digna`)
3. Запустіть перевірку підключення:

```bash
digna repo check
```

Ви повинні побачити підтвердження встановленого з'єднання (сам репозиторій ще не ініціалізовано).

### Step 4: Install the Repository Schema

У тому ж каталозі виконайте:

```bash
digna repo install
```

Ця команда встановить необхідні таблиці та схему у вашій базі даних PostgreSQL.

### Step 5: Create an Admin User

1. Відкрийте **нове** вікно Command Prompt
2. Перейдіть у каталог встановлення digna
3. Виконайте команду для створення адміністратора:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Приклад:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Це створить користувача з повними адміністративними правами.

!!! tip "Best Practice"

    Використовуйте сильний пароль із комбінацією великих і малих літер, цифр та спеціальних символів.

---

### Step 6: Start the digna Server

У каталозі встановлення digna запустіть сервер:

```bash
digna serve --address <host> --port <port>
```

**Параметри:**
- `--address` — хостнейм/IP сервера
- `--port` — порт сервера

Ви повинні побачити повідомлення про запуск сервера:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "Сервер займає термінал"

    `serve` виконується на передньому плані й працює, доки ви не зупините його комбінацією ++ctrl+c++. Залиште його працювати, доки завершуєте налаштування; щоб натомість запускати його автоматично під час завантаження, див. [Запуск digna як служби Windows](#running-digna-as-a-windows-service).

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

У директорії `dashboard/` знаходиться окремий `config.toml` для digna dashboard. Ця конфігурація вже забезпечена і не потребує змін під час початкового налаштування. Змінювати її потрібно лише за потреби (наприклад, для мультиінстансних деплойментів).

Якщо потрібно модифікувати конфігурацію dashboard (наприклад, для підключення до іншого backend), див. документацію dashboard.

Оберіть свій веб‑сервер і дотримуйтесь відповідних кроків для деплою.

#### Deploying to IIS

1. **Open IIS Manager**
   - Натисніть `Win + R`, введіть `inetmgr`, натисніть Enter

2. **Create a New Website**
   - У лівій панелі правою кнопкою миші клікніть **Sites**
   - Оберіть **Add Website...**

3. **Configure the Website**
   - **Site Name**: введіть ім'я (наприклад, "dignaDashboard")
   - **Physical Path**: натисніть Browse і вкажіть папку `dashboard`
   - **Binding**: встановіть IP‑адресу та порт (за замовчуванням порт 80 для HTTP, 443 для HTTPS)

4. **Start the Website**
   - Натисніть **OK**, щоб створити сайт
   - Правою кнопкою миші клікніть новий сайт і оберіть **Start**

5. **Test the Installation**
   - Відкрийте браузер
   - Перейдіть на `http://localhost` (або ваш налаштований URL)
   - Ви повинні побачити сторінку входу digna dashboard

#### Deploying to Apache Tomcat

1. **Copy Dashboard to Tomcat**
   - Скопіюйте папку `dashboard` у директорію `webapps` вашого Tomcat
   - За потреби перейменуйте (наприклад, в `digna`)
   - Приклад: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verify Deployment**
   - Оновіть або перезавантажте сторінку менеджменту Tomcat (http://localhost:8080)
   - Ви повинні побачити "digna" (або обране ім'я) у списку розгорнутих застосунків

3. **Access the Dashboard**
   - Відкрийте браузер
   - Перейдіть на `http://localhost:8080/digna`
   - Ви повинні побачити сторінку входу digna dashboard

---

## Running digna as a Windows Service {: #running-digna-as-a-windows-service }

### Why Use a Windows Service?

Запуск digna backend як служби Windows гарантує, що він:
- Автоматично стартує під час завантаження сервера
- Працює у фоні без відкритого Command Prompt
- Перезапускається автоматично у разі падіння
- Керується через інструмент Windows Services

### Service Management Files

Усі необхідні файли розташовані в каталозі встановлення digna під: `bin/`

Доступні такі батч‑файли:
- `install_service.bat` — реєстрація digna як служби Windows
- `uninstall_service.bat` — видалення реєстрації служби
- `start_service.bat` — запуск служби
- `stop_service.bat` — зупинка служби

!!! warning "Administrator Required"

    Усі батч‑файли повинні виконуватись з правами Адміністратора.

### Installing the Service

1. **Open Command Prompt as Administrator**
   - Клікніть правою кнопкою по Command Prompt
   - Оберіть "Run as Administrator"

2. **Navigate to the bin Folder**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Run the Installation Script**
   ```bash
   install_service.bat
   ```

Тепер digna зареєстровано як служба Windows з увімкненим **automatic startup**. Служба не запускається одразу після встановлення — див. наступний розділ для запуску.

### Starting and Stopping the Service

#### To Start the Service

1. Відкрийте Command Prompt як Адміністратор
2. Перейдіть у `digna\bin`
3. Запустіть:
   ```bash
   start_service.bat
   ```

#### To Stop the Service

1. Відкрийте Command Prompt як Адміністратор
2. Перейдіть у `digna\bin`
3. Запустіть:
   ```bash
   stop_service.bat
   ```

!!! tip "Tip"

    Завжди зупиняйте службу перед оновленням файлів застосунку.

### Moving the Service to a New Directory

Якщо потрібно перемістити інсталяцію digna:

1. **Uninstall the Current Service**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Move the Application Files**
   - Перемістіть всю папку встановлення digna в нове місце

3. **Reinstall the Service**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Start the Service**
   ```bash
   start_service.bat
   ```

### Uninstalling the Service

1. **Stop the Running Service**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Uninstall the Service**
   ```bash
   uninstall_service.bat
   ```

digna тепер знято з реєстрації як служба Windows.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Before You Upgrade

**Спершу перевірте всі підключення до баз даних**

Починаючи з випуску 2026.06, digna звертається до кожної технології-джерела через **ODBC**. Попередні випуски пропонували вибір між окремим драйвером для кожної технології та ODBC, що задавався перемикачем **Use ODBC**. Команда digna вирішила спиратися лише на ODBC, бо єдиний стандартний інтерфейс дає більше, ніж набір драйверів, написаних на замовлення:

- **Автентифікація** — автентифікація є частиною ODBC, тож підключення може використовувати все, що підтримує його драйвер: паролі, токени та PAT, Kerberos і Active Directory, MFA та єдиний вхід через браузер, хмарні ідентичності, клієнтські сертифікати й TLS. Нові методи з'являються разом з оновленням драйвера, а не після очікування випуску digna.
- **Драйвери, які підтримують виробники баз даних** — власний драйвер виробника стежить за новими версіями сервера та виправленнями безпеки, і ви можете оновлювати його у власному темпі, незалежно від digna.
- **Єдиний спосіб налаштувати все** — кожна технологія — це список властивостей «ключ/значення» з тим самим інтерфейсом, тим самим шифруванням конфіденційних значень і тим самим усуненням несправностей, замість різного набору полів для кожного джерела.
- **Тонке налаштування та охоплення** — параметри драйвера, такі як тайм-аути, налаштування TLS, проксі-сервери та розміри вибірки, доступні для кожного джерела, а підключити можна будь-яку технологію із сумісним драйвером ODBC, зокрема ті, для яких digna не публікує окремого посібника.

На практиці це означає, що перемикача **Use ODBC** та окремих полів вузла, порту, бази даних, користувача й пароля більше немає. **Кожне підключення, яке ще не використовує ODBC, має бути переведене на ODBC** — автоматичного перетворення немає, тож сплануйте це до оновлення:

1. Перегляньте кожне підключення до бази даних, визначене у вашому встановленні, і занотуйте ті, що ще не використовують ODBC — кожне з них доведеться налаштувати заново.
2. Встановіть відповідний драйвер ODBC на вузлі digna — підключення відкриваються із сервера, на якому працює серверна частина digna, а не з браузера. Див. [Встановлення драйвера ODBC на вузлі digna](../../../databases/overview.md#install-the-driver).
3. Підготуйте властивості ODBC для кожного зачепленого підключення. [Посібники за технологіями](../../../databases/overview.md#technology-guides) наводять для кожного джерела перевірений набір властивостей.

Після оновлення переведіть кожне зачеплене підключення на ODBC і перевірте його з панелі — див. [Створення підключення до бази даних](../../../databases/overview.md#create-a-database-connection) та [Перевірка підключення](../../../databases/overview.md#testing-a-connection).

!!! warning "Підключення Databricks Legacy"

    Конектор Databricks Legacy вилучено в цьому випуску. Переведіть такі підключення на конектор [Databricks](../../../databases/databricks_connector_guide.md).

**Creating a digna Repository Backup is Mandatory**

Перед оновленням digna обов'язково створіть резервну копію вашого репозиторію (PostgreSQL), щоб захистити дані від втрати.
Резервна копія дозволить відновити стан у разі виникнення непередбачених проблем під час оновлення.

### Upgrade Process

#### Step 1: Stop digna Service

Якщо digna працює як служба Windows, спочатку зупиніть її:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Step 2: Резервне копіювання поточного встановлення

У каталозі встановлення digna перейменуйте теки поточного встановлення, щоб новий випуск можна було розгорнути поруч із ними:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend і dignacli більше не використовуються"

    Починаючи з випуску 2026.06, `dignabackend` і `dignacli` замінено одним виконуваним файлом `digna`, що поєднує серверну частину та CLI. Зберігайте `dignabackend_old` і `dignacli_old` лише доти, доки не перевірите оновлення — після цього обидві теки можна видалити. Зберігайте `dashboard_old`, доки не відновите з неї свої файли конфігурації (див. крок 4).

#### Step 3: Extract and Deploy New Version

1. Розпакуйте ZIP‑файл нової інсталяції digna
2. Скопіюйте новий виконуваний файл `digna`, папку `dashboard` у ваш каталог встановлення


!!! warning "Important"

    Файл `config.toml` **ніколи** не включається до ZIP‑пакета інсталяції. Ваша існуюча конфігурація залишається безпечною.

#### Step 4: Restore Your Configuration Files

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "Випуск 2026.06 змінює config.toml"

    Три параметри нові й обов'язкові, а три більше не використовуються. `config.toml`, перенесений із попереднього випуску, нових параметрів не містить, і digna не запуститься, доки їх бракує. Додайте до наявного `config.toml` таке:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Додайте два ключі `[base]` до наявного розділу `[base]` і додайте `[encryption]` як новий розділ. Потім вилучіть параметри, які більше не використовуються: **`digna_FERNET_KEY`** з `[base]`, а також **`digna_APP_HOST`** і **`digna_APP_PORT`** з `[app]` — адресу та порт сервер тепер бере з `digna serve`.

    Призначення кожного параметра описано в розділі [Налаштування серверної частини](#backend-configuration).

!!! warning "Єдиний вхід: формат [oidc_clients] змінився"

    У випуску 2026.06 масив таблиць замінено окремою таблицею для кожного постачальника, названою за ключем постачальника. `DIGNA_OIDC_KEY` зникає — ключ тепер є частиною заголовка розділу.

    Було:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Стало:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Повторіть розділ для кожного постачальника і стежте, щоб кожен ключ збігався з `key` у файлі `dashboard_config.toml`. `digna config check` повідомляє про розділ `oidc_clients` як FAILED, доки лишається попередня форма. Це стосується лише інсталяцій, що використовують єдиний вхід.

#### Step 5: Перевірте конфігурацію

Перш ніж торкатися репозиторію, переконайтеся, що оновлений `config.toml` повний:

```bash
digna config check
```

Кожен розділ має повідомити OK. Виправте все, про що повідомлено як FAILED, і виконайте команду ще раз, перш ніж продовжувати.

#### Step 6: Upgrade the Repository Schema

Перейдіть у каталог встановлення digna і виконайте:

```bash
digna repo upgrade
```

Це оновить схему PostgreSQL до останньої версії, зберігаючи всі існуючі дані.

#### Step 7: Restart Services

Якщо використовується служба Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Якщо запускаєте вручну, перезапустіть сервер:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Якщо використовуєте IIS або Tomcat, перезапустіть відповідний веб‑сервер.

#### Step 8: Verify the Upgrade

1. Відкрийте digna dashboard
2. Переконайтеся, що інтерфейс завантажується коректно
3. Перевірте журнали сервера на наявність помилок
4. Переведіть на ODBC кожне підключення, яке його ще не використовувало, а потім перевірте всі підключення — див. [Перевірка підключення](../../../databases/overview.md#testing-a-connection)
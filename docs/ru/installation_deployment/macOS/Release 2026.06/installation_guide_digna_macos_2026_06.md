---
title: Руководство по установке macOS – digna Release 2026.06 | Документация digna
description: Пошаговое руководство по установке digna Release 2026.06 на macOS — системные требования, настройка Homebrew и PostgreSQL, конфигурация nginx или Apache, настройка backend и dashboard, запуск digna как фонового сервиса и обновление до новой версии.
keywords: установка digna на macOS, руководство по развертыванию digna на mac, настройка backend digna, установка dashboard digna, postgresql через homebrew, nginx на macos, сервис launchd для digna, руководство по обновлению digna
image: /assets/logo_square.png
---

# macOS Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** September 5, 2026


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
9. [Running digna as a Background Service](#running-digna-as-a-background-service)
10. [Upgrading to a New Release](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### About digna

digna — это комплексная платформа на базе ИИ, разработанная для оптимизации управления качеством данных в различных средах, таких как хранилища данных (warehouses), озёра данных (lakes) и lakehouses. Платформа спроектирована для высокой масштабируемости и адаптируемости и решает современные задачи обработки данных с помощью автоматизации, мониторинга в реальном времени и обнаружения аномалий.

digna состоит из двух основных компонентов:

- **dignabackend**: основной движок приложения, отвечающий за обработку данных и выполнение проверок качества.
- **dignadashboard**: веб-интерфейс, размещаемый на веб-сервере, обеспечивающий удобный способ взаимодействия с платформой digna и визуализации метрик качества данных.

### What's New in Release 2026.06

В этом выпуске возможности наблюдаемости данных (data observability) интегрированы непосредственно в ваш код, что позволяет разработчикам отслеживать качество данных у источника. Полные подробности см. в [release notes](http://docs.digna.ai/changelog/Release_202606/).

### Looking for Windows or Linux?

Это руководство охватывает macOS. Для других платформ см. [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) или [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## System Requirements {: #system-requirements }

Перед началом установки убедитесь, что ваша система соответствует следующим минимальным требованиям:

| Requirement | Specification |
|---|---|
| **Operating System** | macOS 13 (Ventura) или новее |
| **Architecture** | Apple Silicon (arm64) или Intel (x86_64) |
| **Memory (Minimal Setup)** | 16 ГБ ОЗУ |
| **Disk Space** | 10 ГБ свободного места |
| **Database** | PostgreSQL Server 12 или выше |
| **Web Server** | nginx, Apache httpd или эквивалент |
| **Command Line Tools** | Xcode Command Line Tools (требуется для Homebrew) |

### Database Installation Options

**Если PostgreSQL уже установлен:**
Вы можете добавить новую базу данных для digna в ваш существующий сервер PostgreSQL.

**Если вы устанавливаете PostgreSQL на той же машине, что и digna:**

!!! info "Рекомендуемые характеристики"

    - **Память**: 32 ГБ ОЗУ (вместо 16 ГБ)
    - **Место на диске**: 50 ГБ свободного места (вместо 10 ГБ)

    Эти повышенные характеристики учитывают одновременную работу digna и PostgreSQL на одной машине.

### Checking Your Architecture

Некоторые пути в этом руководстве отличаются для Apple Silicon и Intel Mac. Чтобы узнать, какая у вас архитектура, откройте **Terminal** и выполните:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew устанавливается в `/opt/homebrew`.
- `x86_64` — Intel. Homebrew устанавливается в `/usr/local`.

!!! tip "Совет"

    Вместо жёсткой привязки к одному из путей в этом руководстве используется `$(brew --prefix)`, который разворачивается в правильное расположение на обеих архитектурах. Вы можете копировать команды без изменений.

---

## Pre-Installation Setup {: #pre-installation-setup }

Перед установкой digna убедитесь, что выполнены три ключевых предварительных условия:

1. **Homebrew** – менеджер пакетов, используемый для установки компонентов, описанных ниже
2. **PostgreSQL Server** – для хранения вычисляемых метрик и данных производительности
3. **Web Server** – для размещения digna Dashboard

Если эти компоненты ещё не установлены, следуйте разделам ниже, чтобы установить и настроить их.

### Installing Homebrew

Homebrew — стандартный менеджер пакетов для macOS и используется в этом руководстве для установки PostgreSQL и nginx.

#### Step 1: Check Whether Homebrew Is Already Installed

Откройте **Terminal** (нажмите `Cmd + Space`, введите `Terminal`, нажмите Enter) и выполните:

```bash
brew --version
```

Если возвращается номер версии, перейдите к разделу [PostgreSQL Server Setup](#postgresql-server-setup).

#### Step 2: Install Homebrew

Если команда не найдена, установите Homebrew, следуя инструкциям на [официальном сайте Homebrew](https://brew.sh). Установщик также установит Xcode Command Line Tools, если они ещё не установлены.

#### Step 3: Add Homebrew to Your PATH

На Apple Silicon установщик выводит две команды для добавления Homebrew в окружение вашей оболочки. Выполните их, как указано, затем подтвердите:

```bash
brew --prefix
```

Это должно вывести `/opt/homebrew` на Apple Silicon или `/usr/local` на Intel.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### If You Already Have PostgreSQL

Если PostgreSQL уже установлен и запущен на вашей локальной машине или вы используете управляемый удалённый сервер PostgreSQL, вы можете перейти к [следующему разделу](#web-server-configuration).

### Installation Options

macOS предлагает два простых способа установки PostgreSQL. Выберите **один**:

- [Homebrew](#postgresql-homebrew) — установка через командную строку, рекомендуется для серверных развёртываний
- [Postgres.app](#postgresql-app) — графическая установка, удобная для локальной оценки

### Installing PostgreSQL with Homebrew {: #postgresql-homebrew }

#### Step 1: Install the PostgreSQL Formula

```bash
brew install postgresql@16
```

#### Step 2: Add PostgreSQL to Your PATH

Версионированные формулы PostgreSQL являются *keg-only*, что означает, что Homebrew не добавляет их команды в PATH автоматически. Добавьте их сами:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Примечание"

    Предполагается, что вы используете оболочку `zsh`, установленную по умолчанию в macOS. Если вы используете `bash`, добавьте ту же строку в `~/.bash_profile`.

#### Step 3: Start the PostgreSQL Service

```bash
brew services start postgresql@16
```

Эта команда запустит PostgreSQL немедленно и настроит его на автоматический запуск при входе в систему.

#### Step 4: Verify the Installation

```bash
psql --version
```

Вы должны увидеть версию PostgreSQL, если установка прошла успешно.

#### Step 5: Connect to the Server

```bash
psql postgres
```

!!! warning "Важно — macOS отличается от Windows в этом моменте"

    Установщик для Windows предлагает создать суперпользователя `postgres` и задать пароль. Homebrew этого не делает. Вместо этого создаётся суперпользователь с именем вашей **учётной записи macOS**, без пароля, доступный только с локальной машины.

    Это означает, что роли `postgres` на свежей установке Homebrew может не существовать. Используйте своё имя учётной записи при необходимости суперпользователя и создайте явного пользователя для digna, как описано в разделе [Initial Installation](#initial-installation).

#### Step 6: Confirm the Port

Порт PostgreSQL по умолчанию — `5432`. Чтобы подтвердить порт, на котором слушает сервер:

```bash
psql postgres -c "SHOW port;"
```

Запомните значение — оно понадобится при настройке backend digna.

### Installing PostgreSQL with Postgres.app {: #postgresql-app }

Если вы предпочитаете графическую установку:

1. Скачайте [Postgres.app](https://postgresapp.com) и перетащите его в папку **Applications**
2. Откройте приложение и нажмите **Initialize**, чтобы создать новый сервер
3. Следуйте инструкциям приложения, чтобы добавить его инструменты командной строки в PATH
4. Проверьте установку:

```bash
psql --version
```

Postgres.app также создаёт суперпользователя с именем вашей учётной записи macOS.

---

## Web Server Configuration {: #web-server-configuration }

digna требует веб-сервера для размещения dashboard. Выберите один из следующих вариантов:

- [nginx](#nginx-setup) — устанавливается через Homebrew, рекомендуется
- [Apache httpd](#apache-setup) — входит в состав macOS

Требуется установить и настроить **только один** из этих серверов.

Оба раздела настраивают два требования, от которых зависит dashboard:

- **Переадресация для single-page-приложения**, чтобы обновление URL dashboard не приводило к 404
- **MIME-тип для `.md`**, чтобы Markdown-файлы отдавались корректно

### nginx Setup {: #nginx-setup }

#### Overview

nginx — это лёгкий высокопроизводительный веб-сервер, хорошо подходящий для обслуживания статического dashboard digna.

#### Installation

```bash
brew install nginx
```

#### Starting nginx

```bash
brew services start nginx
```

#### Verify the Installation

1. Откройте браузер
2. Перейдите по адресу `http://localhost:8080`
3. Вы должны увидеть страницу приветствия nginx

!!! note "Примечание — порт по умолчанию 8080, а не 80"

    Homebrew настраивает nginx на прослушивание порта `8080`, чтобы сервер мог работать без привилегий администратора. На macOS привязка к порту `80` или любому другому порту ниже 1024 требует прав root.

    Чтобы обслуживать dashboard на порту 80, измените `listen 8080;` на `listen 80;` в конфигурации ниже и запустите nginx с `sudo brew services start nginx`.

#### Configuring a Site for the Dashboard

Конфигурация nginx от Homebrew включает все файлы в каталоге `servers`. Создайте отдельный файл конфигурации для digna там:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Вставьте следующее, заменив `/path/to/digna/dashboard` на фактический путь к вашей распакованной папке `dashboard`:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

(Комментарии в конфигурации выше поясняют поведение сервера и не влияют на команды.)

!!! warning "Важно"

    Без директивы `try_files` перезагрузка любой страницы dashboard, отличной от корневого URL, вернёт 404. Это эквивалент модуля URL Rewrite в IIS на Windows.

#### Apply the Configuration

Проверьте конфигурацию на синтаксические ошибки, затем перезапустите nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd Setup {: #apache-setup }

#### Overview

macOS включает Apache httpd, поэтому установка не требуется. По умолчанию он отключён.

#### Starting Apache

```bash
sudo apachectl start
```

#### Verify the Installation

1. Откройте браузер
2. Перейдите по адресу `http://localhost`
3. Вы должны увидеть сообщение "It works!"

#### Required: Enable mod_rewrite

Dashboard требует перенаправления URL. Откройте конфигурационный файл Apache:

```bash
sudo nano /etc/apache2/httpd.conf
```

Найдите следующую строку и уберите ведущий `#`, чтобы раскомментировать её:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Required: Allow .htaccess Overrides

В том же файле найдите блок `<Directory "/Library/WebServer/Documents">` и измените:

```apache
AllowOverride None
```

на:

```apache
AllowOverride All
```

#### Required: MIME Type for Markdown Files

Всё ещё в `httpd.conf` добавьте следующую строку, чтобы Markdown-файлы отдавались корректно:

```apache
AddType text/markdown .md
```

!!! warning "Важно"

    Без этой настройки `.md` файлы могут обслуживаться некорректно.

#### Apply the Configuration

Проверьте конфигурацию на синтаксические ошибки, затем перезапустите Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Initial Installation {: #initial-installation }

### Step 1: Set Up the digna Repository

Репозиторий digna хранит все метрики, вычисляемые digna. Он выступает в качестве центральной базы данных для аналитических и производительных данных.

#### Create Repository Schema and User

Откройте ваш клиент PostgreSQL (psql, pgAdmin или аналогичный) и выполните следующие SQL-команды:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Замените следующие заполнители:**

- `<digna_repo_schema>` — имя схемы по вашему выбору (например, `dignarepo`)
- `<digna_repo_user>` — имя пользователя по вашему выбору (например, `digna_user`)
- `<digna_repo_password>` — безопасный пароль для этого пользователя

**Пример:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Чтобы выполнить эти команды из Terminal в один шаг:

```bash
psql postgres
```

Затем вставьте команды в приглашении `postgres=#` и введите `\q` для выхода.

!!! tip "Лучше практики"

    Используйте сложные, надёжные пароли для пользователей базы данных. Избегайте легко угадываемых учётных данных.

---

### Step 2: Extract the digna Installation Package

1. Найдите ZIP-файл установки digna, предоставленный вам
2. Распакуйте его в желаемое место установки — например `/opt/digna` или `~/digna`
3. После распаковки вы должны увидеть следующие элементы:
   - `dashboard/` — веб-интерфейс dashboard
   - `digna` — основной исполняемый файл (backend + CLI в одном)
   - `config.toml` — файл конфигурации
   - `license.toml` — файл лицензии (скопируйте сюда ваш файл)

Чтобы распаковать через Terminal:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Make the Executable Runnable

В зависимости от способа передачи архива, бит выполнения (executable bit) может не сохраниться при распаковке. Установите его явно:

```bash
cd /opt/digna
chmod +x digna
```

#### If macOS Blocks the Application

Файлы, скачанные через браузер или почтовый клиент, помечаются атрибутом quarantine. Если macOS сообщает, что приложение *"cannot be opened because the developer cannot be verified"*, снимите атрибут карантина с каталога установки:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Альтернативно, откройте **System Settings → Privacy & Security**, найдите заблокированный элемент в нижней части страницы и нажмите **Open Anyway**.

!!! note "Примечание"

    Этот шаг требуется только если macOS действительно блокирует исполняемый файл. Пакеты, переданные по SSH или из внутренних файловых шаров, как правило, не помечаются карантином.

### Step 3: Install the License File

!!! warning "Важно"

    Файл лицензии **не** включён в установочный пакет и будет предоставлен отдельно компанией digna.

1. Найдите файл `license.toml`, предоставленный вам
2. Скопируйте его в корневой каталог установки digna (ту же папку, где находятся `config.toml` и исполняемый файл `digna`)

**Почему это важно:**
Файл лицензии содержит информацию о заказчике, дату истечения лицензии и цифровую подпись. **Не изменяйте этот файл** — любые изменения аннулируют подпись и сделают файл недействительным.

**Структура каталогов после настройки:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend Configuration {: #backend-configuration }

### Step 1: Create and Edit the Configuration File

Файл `config_template.toml` предоставлен в каталоге установки digna. Вам нужно только переименовать его в `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Расположение:** `/opt/digna/config.toml`

Откройте `config.toml` в текстовом редакторе и настройте каждый раздел ниже.

#### [app] Section

Этот раздел настраивает параметры приложения digna backend:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` или IP-адрес | Хостнейм или IP, где размещён dignabackend |
| `digna_APP_PORT` | `8082` (по умолчанию) | Порт для REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL фронтенда | Если dashboard размещён на другом сервере, укажите его URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Требуется для CORS с учётом учётных данных |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Разрешить все HTTP-методы |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Разрешить все заголовки |

!!! note "Примечание"

    Если вы обслуживаете dashboard через nginx от Homebrew на порту по умолчанию, значение origin для разрешения будет `http://localhost:8080`.

#### [repo] Section

Этот раздел настраивает подключение к базе данных PostgreSQL:

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
| `digna_REPO_HOST` | `localhost` или IP | Хост PostgreSQL / IP-адрес |
| `digna_REPO_PORT` | `5432` (по умолчанию) | Порт PostgreSQL |
| `digna_REPO_DB` | `postgres` | Имя базы данных |
| `digna_REPO_SCHEMA` | `dignarepo` | Схема, созданная ранее |
| `digna_REPO_USER` | `digna_user` | Пользователь, созданный при настройке PostgreSQL |
| `digna_REPO_PASSWORD` | Ваш пароль | Пароль, заданный при создании пользователя |

#### [base] Section

Этот раздел содержит параметры безопасности и cookie:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | Ключ шифрования | Используется для шифрования токенов и cookies (по умолчанию предоставлен) |
| `digna_COOKIE_DOMAIN` | `localhost` | Домен, соответствующий вашему фронтенду |
| `digna_COOKIE_SECURE` | `false` (локально) / `true` (production) | Используйте `true` для HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Всегда включено для безопасности |
| `digna_COOKIE_SAME_SITE` | `lax` | Предотвращает CSRF-атаки |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 часа) | Время жизни сессии в секундах |
| `digna_MAX_WORKERS` | Количество ядер CPU - 1 | Количество параллельных задач инспекции |

!!! tip "Совет"

    Чтобы узнать количество ядер CPU на вашем Mac, выполните `sysctl -n hw.ncpu`.

#### [logging] Section

Этот раздел настраивает поведение логирования:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` или `DEBUG` | `INFO` для production, `DEBUG` для отладки |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Количество ежедневных резервных копий логов, которые сохраняются |

---

### Step 2: Initialize the Repository

1. Откройте **Terminal**
2. Перейдите в каталог установки digna (где находятся `config.toml` и исполняемый файл `digna`)
3. Выполните проверку подключения:

```bash
cd /opt/digna
./digna repo check
```

Вы должны увидеть подтверждение установления соединения (сам репозиторий ещё не инициализирован).

!!! note "Примечание"

    На macOS команды в текущем каталоге не находятся в PATH, поэтому исполняемый файл вызывается как `./digna`, а не просто `digna`. Чтобы иметь возможность запускать его без предшествующего `./`, добавьте каталог установки в PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Step 3: Install the Repository Schema

В том же каталоге выполните:

```bash
./digna repo install
```

Эта команда установит необходимые таблицы и схему в вашей базе данных PostgreSQL.

### Step 4: Start the digna Server

В каталоге установки digna запустите сервер:

```bash
./digna serve --address <host> --port <port>
```

**Параметры:**
- `--address` — хостнейм/IP сервера
- `--port` — порт сервера

Вы должны увидеть сообщения при запуске, подтверждающие, что сервер работает:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Совет"

    При первом запуске macOS может запросить, разрешить ли приложению входящие сетевые соединения. Нажмите **Allow**, иначе dashboard не сможет подключиться к backend.

### Step 5: Create an Admin User

1. Откройте **новое** окно Terminal
2. Перейдите в каталог установки digna
3. Выполните команду для создания администратора:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Пример:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Это создаст пользователя с именем `admin` и полными административными привилегиями.

!!! tip "Совет"

    Офорните пароль в одинарные кавычки. `zsh` обрабатывает такие символы, как `!`, `$` и `*` особым образом, и незаключённый пароль, содержащий их, может быть передан неправильно.

!!! tip "Лучшие практики"

    Используйте надёжный пароль, сочетающий прописные и строчные буквы, цифры и специальные символы.

---

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

У dashboard есть собственный отдельный файл `config.toml`, расположенный в каталоге `dashboard/`. Эта конфигурация уже предоставлена и в первоначальной настройке менять её не требуется. Меняйте её только при необходимости изменить подключение к backend.

Если нужно изменить конфигурацию dashboard (например, для мульти-инстансного развёртывания), обратитесь к документации dashboard.

Выберите ваш веб-сервер и следуйте соответствующим шагам развертывания.

#### Deploying to nginx

Если вы следовали разделу [nginx Setup](#nginx-setup), блок сервера уже указывает на вашу папку `dashboard` и копирование не требуется.

1. **Подтвердите путь**
   - Откройте `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Убедитесь, что `root` указывает на распакованную папку `dashboard`

2. **Убедитесь, что папка доступна для чтения**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Перезагрузите nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Проверьте установку**
   - Откройте браузер
   - Перейдите по адресу `http://localhost:8080` (или по вашему настроенному URL)
   - Вы должны увидеть страницу входа в digna dashboard

#### Deploying to Apache httpd

1. **Скопируйте Dashboard в Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Добавьте правила переписывания (Rewrite Rules)**

   Создайте файл `.htaccess` внутри развернутой папки, чтобы маршруты dashboard не ломались при обновлении страницы:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Вставьте следующее:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Перезапустите Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Доступ к Dashboard**
   - Откройте браузер
   - Перейдите по адресу `http://localhost/digna`
   - Вы должны увидеть страницу входа в digna dashboard

---

## Running digna as a Background Service {: #running-digna-as-a-background-service }

### Why Run digna as a Service?

Запуск backend digna как фонового сервиса гарантирует, что он:

- Автоматически запускается при загрузке машины
- Работает в фоновом режиме без открытого окна Terminal
- Автоматически перезапускается при сбое
- Управляется через `launchctl`, менеджер сервисов macOS

### Service Management Files

Все необходимые файлы находятся в каталоге установки digna в папке: `bin/`

Доступны следующие shell-скрипты:

- `install_service.sh` — регистрирует digna в launchd
- `uninstall_service.sh` — удаляет регистрацию сервиса
- `start_service.sh` — запускает зарегистрированный сервис
- `stop_service.sh` — останавливает запущенный сервис

!!! warning "Требуется привилегии администратора"

    Все скрипты должны выполняться с `sudo`, поскольку регистрация сервиса с автозапуском при старте системы записывает файлы в `/Library/LaunchDaemons`.

### Making the Scripts Executable

При распаковке бит выполнения мог не сохраниться. Перед первым использованием:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Installing the Service

1. **Откройте Terminal**

2. **Перейдите в папку bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Запустите скрипт установки**
   ```bash
   sudo ./install_service.sh
   ```

Сервис digna теперь зарегистрирован в launchd с включённым автоматическим запуском. Сервис не запускается сразу — см. следующий раздел для его запуска.

### Starting and Stopping the Service

#### To Start the Service

1. Откройте Terminal
2. Перейдите в `/opt/digna/bin`
3. Выполните:
   ```bash
   sudo ./start_service.sh
   ```

#### To Stop the Service

1. Откройте Terminal
2. Перейдите в `/opt/digna/bin`
3. Выполните:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Совет"

    Всегда останавливайте сервис перед обновлением файлов приложения.

### Verifying the Service

Чтобы убедиться, что сервис зарегистрирован и запущен:

```bash
sudo launchctl list | grep digna
```

Строка, начинающаяся с идентификатора процесса, означает, что сервис запущен. `-` в первом столбце означает, что он зарегистрирован, но остановлен.

### Moving the Service to a New Directory

launchd хранит абсолютный путь к исполняемому файлу, поэтому при переносе установки требуется повторная регистрация сервиса:

1. **Удалите текущий сервис**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Переместите файлы приложения**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Переустановите сервис**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Запустите сервис**
   ```bash
   sudo ./start_service.sh
   ```

### Uninstalling the Service

1. **Остановите запущенный сервис**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Удалите регистрацию сервиса**
   ```bash
   sudo ./uninstall_service.sh
   ```

Сервис digna теперь удалён из launchd.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Before You Upgrade

**Создание резервной копии репозитория digna обязательно**

Перед обновлением digna сделайте резервную копию вашего репозитория (PostgreSQL), чтобы защититься от потери данных.
Резервная копия позволит восстановиться в случае непредвиденных проблем при обновлении.

Чтобы создать резервную копию из Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Upgrade Process

#### Step 1: Stop the digna Service

Если digna запущен как фоновый сервис, сначала остановите его:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Если digna запущен в первом плане, нажмите `Ctrl + C` в окне Terminal, где он работает.

#### Step 2: Backup Current Backend Installation

В каталоге установки digna:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Step 3: Extract and Deploy New Version

1. Распакуйте новый ZIP-файл установки digna
2. Скопируйте новый исполняемый файл `digna` и папку `dashboard` в каталог установки
3. Восстановите бит выполнения и при необходимости снимите атрибут карантина:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Важно"

    Файл `config.toml` **никогда** не включается в ZIP с установкой. Ваша существующая конфигурация останется неизменной.

### Step 4: Restore Your Configuration Files

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Step 5: Upgrade the Repository Schema

Перейдите в каталог установки digna и выполните:

```bash
cd /opt/digna
./digna repo upgrade
```

Это обновит схему PostgreSQL до последней версии, сохранив все существующие данные.

### Step 6: Restart Services

Если вы используете фоновые сервисы:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Если запускаете вручную, перезапустите сервер:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Если используется nginx или Apache, перезапустите соответствующий веб-сервер:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Step 7: Verify the Upgrade

1. Откройте интерфейс digna dashboard
2. Убедитесь, что интерфейс загружается корректно
3. Проверьте журналы сервера на наличие ошибок
---
title: Руководство по установке Linux – digna Release 2026.11 | Документация digna
description: Пошаговое руководство по установке digna Release 2026.11 на Linux — системные требования, настройка PostgreSQL, конфигурация nginx или Apache, настройка backend и dashboard, запуск digna как сервиса systemd и обновление с Release 2026.06.
keywords: установка digna на linux, руководство по развертыванию digna, настройка backend digna, установка dashboard digna, postgresql в linux, nginx в linux, сервис systemd для digna, руководство по обновлению digna
image: /assets/logo_square.png
---

# Руководство по установке на Linux для digna Release 2026.11

**Релиз:** 2026.11

**Последнее обновление:** 7 ноября 2026


---

## Содержание

1. [Введение](#introduction)
2. [Требования к системе](#system-requirements)
3. [Подготовка к установке](#pre-installation-setup)
4. [Настройка PostgreSQL сервера](#postgresql-server-setup)
5. [Настройка веб-сервера](#web-server-configuration)
6. [Первоначальная установка](#initial-installation)
7. [Конфигурация backend](#backend-configuration)
8. [Конфигурация Dashboard](#dashboard-configuration)
9. [Запуск digna как сервиса systemd](#running-digna-as-a-systemd-service)
10. [Обновление до новой версии](#upgrading-to-a-new-release)

---

## Введение {: #introduction }

### О digna

digna — это комплексная платформа на базе ИИ, разработанная для оптимизации управления качеством данных в различных средах, таких как хранилища данных (warehouses), озёра данных (lakes) и lakehouses. Платформа спроектирована для высокой масштабируемости и адаптируемости и решает современные задачи обработки данных с помощью автоматизации, мониторинга в реальном времени и обнаружения аномалий.

digna состоит из двух основных компонентов:

- **digna**: ядро приложения, отвечающее за обработку данных и выполнение проверок качества. Оно объединяет серверную часть и интерфейс командной строки в одном исполняемом файле, заменяя отдельные программы `dignabackend` и `dignacli` из прежних выпусков.
- **dignadashboard**: веб-интерфейс, размещаемый на веб-сервере, обеспечивающий удобный способ взаимодействия с платформой digna и визуализации метрик качества данных.

### Что нового в Release 2026.11

В этом выпуске появились digna Data Reconciliation, digna Agentic с digna MCP Server, а также digna Engine, который может профилировать данные внутри digna и проверять ссылочную целостность между разными технологиями баз данных. Полные подробности см. в [примечаниях к выпуску](../../../changelog/Release_202611.md).

Для установки выпуск приносит новый механизм миграции репозитория, необязательный раздел `[duckdb]` в `config.toml` для digna Engine и новый файл лицензии. Каждое из этих изменений описано в [разделе об обновлении](#upgrading-to-a-new-release).

### Ищете Windows или macOS?

Это руководство охватывает Linux. Для других платформ см. [руководство по установке на Windows](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) или [руководство по установке на macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Какие дистрибутивы охватывает это руководство?

Инструкции написаны для двух наиболее распространённых семейств серверных дистрибутивов. Там, где они различаются, приводятся обе команды:

- **Семейство Debian** — Debian, Ubuntu. Менеджер пакетов: `apt`.
- **Семейство RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Менеджер пакетов: `dnf`.

Подойдёт любой современный дистрибутив с `systemd`; меняются только имена пакетов и несколько путей к конфигурации.

---

## Требования к системе {: #system-requirements }

Перед началом установки убедитесь, что ваша система соответствует следующим минимальным требованиям:

| Требование | Характеристика |
|---|---|
| **Операционная система** | Ubuntu 22.04 LTS или новее, Debian 12 или новее, RHEL 9 / Rocky 9 / AlmaLinux 9 или новее |
| **Архитектура** | x86_64 (amd64) или arm64 |
| **Система инициализации** | systemd |
| **Память (минимальная конфигурация)** | 16 ГБ ОЗУ |
| **Место на диске** | 10 ГБ свободного места |
| **База данных** | PostgreSQL Server 12 или выше |
| **Веб-сервер** | nginx, Apache httpd или эквивалент |

!!! info "digna Engine"

    Подключения к базам данных, использующие digna Engine в качестве места профилирования, профилируются на
    самом хосте digna. Запланируйте для них дополнительную память и место на диске, см.
    [раздел \[duckdb\]](#duckdb-section).

### Варианты установки базы данных

**Если PostgreSQL уже установлен:**
Вы можете добавить новую базу данных для digna в ваш существующий сервер PostgreSQL.

**Если вы устанавливаете PostgreSQL на той же машине, что и digna:**

!!! info "Рекомендуемые характеристики"

    - **Память**: 32 ГБ ОЗУ (вместо 16 ГБ)
    - **Место на диске**: 50 ГБ свободного места (вместо 10 ГБ)

    Эти повышенные характеристики учитывают одновременную работу digna и PostgreSQL на одной машине.

### Как узнать дистрибутив и архитектуру

Некоторые команды в этом руководстве отличаются для семейств Debian и RHEL. Чтобы узнать, какое у вас семейство, выполните:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` или `ID=debian` — используйте команды `apt`.
- `ID=rhel`, `rocky`, `almalinux` или `fedora` — используйте команды `dnf`.
- `x86_64` или `aarch64` — архитектура нужного вам установочного пакета.

---

## Подготовка к установке {: #pre-installation-setup }

Перед установкой digna убедитесь, что выполнены два ключевых предварительных условия:

1. **PostgreSQL Server** – для хранения вычисляемых метрик и данных производительности
2. **Веб-сервер** – для размещения digna Dashboard

Если эти компоненты ещё не установлены, следуйте разделам ниже, чтобы установить и настроить их.

### Обновление индекса пакетов

Перед установкой чего-либо обновите списки пакетов:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Примечание"

    Во всём этом руководстве первая команда в паре предназначена для **семейства Debian**, а вторая — для **семейства RHEL**. Выполняйте только ту, которая соответствует вашей системе.

---

## Настройка PostgreSQL сервера {: #postgresql-server-setup }

### Если PostgreSQL уже установлен

Если PostgreSQL уже установлен и запущен на вашей локальной машине или вы используете управляемый удалённый сервер PostgreSQL, вы можете перейти к [следующему разделу](#web-server-configuration).

### Установка PostgreSQL

#### Шаг 1: Установите пакет сервера

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Совет"

    Пакеты дистрибутива могут отставать от текущего выпуска PostgreSQL. Если вам нужна определённая более новая версия, используйте вместо них официальный [репозиторий PostgreSQL для apt или yum](https://www.postgresql.org/download/linux/).

#### Шаг 2: Инициализируйте кластер баз данных

В **семействе Debian** пакет создаёт и запускает кластер автоматически — перейдите к следующему шагу.

В **семействе RHEL** кластер нужно создать явно:

```bash
sudo postgresql-setup --initdb
```

#### Шаг 3: Запустите сервис и включите автозапуск

```bash
sudo systemctl enable --now postgresql
```

Эта команда запустит PostgreSQL немедленно и настроит его на автоматический запуск при загрузке системы.

#### Шаг 4: Проверьте установку

```bash
psql --version
sudo systemctl status postgresql
```

Вы должны увидеть версию PostgreSQL и сервис в состоянии `active (running)`.

#### Шаг 5: Подключитесь к серверу

Пакет PostgreSQL для Linux создаёт системную учётную запись `postgres`, которой принадлежит кластер. Подключайтесь через неё:

```bash
sudo -u postgres psql
```

!!! note "Примечание — Linux отличается от Windows в этом моменте"

    Установщик для Windows во время установки предлагает задать пароль для суперпользователя `postgres`. Пакеты для Linux этого не делают. Вместо этого локальные подключения проходят **peer-аутентификацию** (peer authentication): пользователю операционной системы `postgres` разрешено подключаться как пользователь базы данных `postgres` без пароля.

    Именно поэтому в команде выше используется `sudo -u postgres`. Backend digna подключается по TCP с именем пользователя и паролем, поэтому вы создадите отдельного пользователя для digna в разделе [Первоначальная установка](#initial-installation).

#### Шаг 6: Проверьте порт

Порт PostgreSQL по умолчанию — `5432`. Чтобы подтвердить порт, на котором слушает сервер:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Запомните значение — оно понадобится при настройке backend digna.

#### Шаг 7: Включите парольную аутентификацию для пользователя digna

digna подключается к PostgreSQL по TCP как `digna_user`, что требует парольной аутентификации, а не peer-аутентификации. Убедитесь, что ваш `pg_hba.conf` это разрешает.

Найдите файл:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Откройте его в редакторе и убедитесь, что в строках для локального TCP указан метод `scram-sha-256` (или `md5` на старых серверах), а не `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

После любого изменения перезагрузите конфигурацию PostgreSQL:

```bash
sudo systemctl reload postgresql
```

!!! warning "Важно"

    Если digna сообщает `FATAL: Ident authentication failed for user "digna_user"`, причина именно в этой настройке.

#### Шаг 8: Если PostgreSQL работает на другой машине

Чтобы принимать подключения с другого узла, задайте `listen_addresses` в `postgresql.conf` и добавьте соответствующую строку `host` для вашей сети в `pg_hba.conf`:

```
listen_addresses = '*'
```

Затем откройте порт в брандмауэре и перезапустите сервис:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Настройка веб-сервера {: #web-server-configuration }

digna требует веб-сервера для размещения dashboard. Выберите один из следующих вариантов:

- [nginx](#nginx-setup) — лёгкий, рекомендуется
- [Apache httpd](#apache-setup) — широко распространённая альтернатива

Требуется установить и настроить **только один** из этих серверов.

Оба раздела настраивают два требования, от которых зависит dashboard:

- **Переадресация для single-page-приложения**, чтобы обновление URL dashboard не приводило к 404
- **MIME-тип для `.md`**, чтобы Markdown-файлы отдавались корректно

### Настройка nginx {: #nginx-setup }

#### Обзор

nginx — это лёгкий высокопроизводительный веб-сервер, хорошо подходящий для обслуживания статического dashboard digna.

#### Установка

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Запуск nginx

```bash
sudo systemctl enable --now nginx
```

#### Проверьте установку

1. Откройте браузер
2. Перейдите по адресу `http://localhost`
3. Вы должны увидеть страницу приветствия nginx

#### Открытие брандмауэра

Если к серверу обращаются с других машин, разрешите HTTP-трафик:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Настройка сайта для dashboard

В обоих семействах дистрибутивов nginx подключает все файлы из своего каталога `conf.d`. Создайте там отдельный файл конфигурации для digna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Вставьте следующее, заменив `/opt/digna/dashboard` на фактический путь к вашей распакованной папке `dashboard`:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

!!! warning "Важно"

    Без директивы `try_files` перезагрузка любой страницы dashboard, отличной от корневого URL, вернёт 404. Это эквивалент модуля URL Rewrite, который требуется для IIS в Windows.

#### Отключите сайт по умолчанию

Только один блок server может быть `default_server` для порта. В **семействе Debian** удалите сайт по умолчанию из пакета, чтобы он не конфликтовал:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

В **семействе RHEL** закомментируйте или удалите блок `server { ... }` в файле `/etc/nginx/nginx.conf`.

#### Примените конфигурацию

Проверьте конфигурацию на синтаксические ошибки, затем перезагрузите nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Настройка Apache httpd {: #apache-setup }

#### Обзор

Apache httpd доступен в стандартных репозиториях всех поддерживаемых дистрибутивов. В семействе Debian пакет называется `apache2`, в семействе RHEL — `httpd`.

#### Установка

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Запуск Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Проверьте установку

1. Откройте браузер
2. Перейдите по адресу `http://localhost`
3. Вы должны увидеть стандартную страницу Apache вашего дистрибутива

#### Обязательно: включите mod_rewrite

Dashboard требует перенаправления URL.

В **семействе Debian** включите модуль и перезапустите сервер:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

В **семействе RHEL** `mod_rewrite` загружается по умолчанию. Убедитесь в этом:

```bash
httpd -M | grep rewrite
```

#### Обязательно: разрешите переопределения в .htaccess

Откройте конфигурационный файл для вашего корневого каталога документов:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Найдите блок `<Directory>`, относящийся к корневому каталогу документов (`/var/www/html` в обоих семействах), и измените:

```apache
AllowOverride None
```

на:

```apache
AllowOverride All
```

#### Обязательно: MIME-тип для файлов Markdown

В том же файле добавьте следующую строку, чтобы Markdown-файлы отдавались корректно:

```apache
AddType text/markdown .md
```

!!! warning "Важно"

    Без этой настройки `.md` файлы могут обслуживаться некорректно.

#### Примените конфигурацию

Проверьте конфигурацию на синтаксические ошибки, затем перезапустите Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Первоначальная установка {: #initial-installation }

### Шаг 1: Настройка репозитория digna

Репозиторий digna хранит все метрики, вычисляемые digna. Он выступает в качестве центральной базы данных для аналитических данных и данных производительности.

#### Создание схемы репозитория и пользователя

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

Чтобы выполнить эти команды из оболочки в один шаг:

```bash
sudo -u postgres psql
```

Затем вставьте команды в приглашении `postgres=#` и введите `\q` для выхода.

!!! tip "Лучшие практики"

    Используйте сложные, надёжные пароли для пользователей базы данных. Избегайте легко угадываемых учётных данных.

---

### Шаг 2: Распакуйте установочный пакет digna

1. Найдите ZIP-файл установки digna, предоставленный вам
2. Распакуйте его в желаемое место установки — например `/opt/digna`
3. После распаковки вы должны увидеть следующие элементы:
   - `dashboard/` — веб-интерфейс dashboard
   - `digna` — основной исполняемый файл (backend + CLI в одном)

!!! info "Файлы конфигурации и лицензии не входят в пакет"

    Ни `config.toml`, ни `dashboard/dashboard_config.toml` не поставляются вместе с установкой — вы
    создаёте оба файла самостоятельно, в разделах [Конфигурация backend](#backend-configuration) и
    [Конфигурация Dashboard](#dashboard-configuration). `license.toml` тоже не поставляется;
    digna предоставляет его отдельно, как описано в шаге 3.

Чтобы распаковать из оболочки:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Примечание"

    Если `unzip` не установлен, добавьте его командой `sudo apt install -y unzip` или `sudo dnf install -y unzip`.

#### Сделайте файл исполняемым

В зависимости от способа передачи архива, бит выполнения (executable bit) может не сохраниться при распаковке. Установите его явно:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Создайте служебную учётную запись

Для производственных развёртываний рекомендуется запускать backend от имени отдельного непривилегированного пользователя:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Примечание"

    В семействе RHEL эквивалентный путь к оболочке — `/sbin/nologin`.

### Шаг 3: Установите файл лицензии

!!! warning "Важно"

    Файл лицензии **не** включён в установочный пакет и будет предоставлен отдельно компанией digna.

1. Найдите файл `license.toml`, предоставленный вам
2. Скопируйте его в корневой каталог установки digna (ту же папку, где находятся `config.toml` и исполняемый файл `digna`)

**Почему это важно:**
Файл лицензии содержит информацию о заказчике, дату истечения лицензии и цифровую подпись. **Не изменяйте этот файл** — любые изменения сделают его недействительным.

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

## Конфигурация backend {: #backend-configuration }

### Шаг 1: Создание и редактирование файла конфигурации

Файл `config_template.toml` предоставлен в каталоге установки digna. Вам нужно только переименовать его в `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Расположение:** `/opt/digna/config.toml`

Откройте `config.toml` в текстовом редакторе и настройте каждый раздел ниже.

#### Раздел [app]

Этот раздел настраивает совместное использование ресурсов между источниками (CORS) для dashboard и backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Параметр | Значение | Примечания |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URL dashboard | URL, с которых обслуживается dashboard. Запросы браузера с любого другого origin отклоняются |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Обязательно, чтобы браузер отправлял cookie сессии с каждым запросом |

!!! note "Примечание"

    Если вы обслуживаете dashboard через nginx или Apache на стандартном HTTP-порту, разрешаемым origin будет `http://localhost` — или публичный URL сервера, если к dashboard обращаются с других машин.

!!! info "Раздел [app] необязателен"

    Начиная с Release 2026.11, оба ключа, а также весь раздел `[app]`, можно не указывать. Это
    правильная настройка, когда обратный прокси обслуживает dashboard и backend под одним origin: тогда
    браузер не выполняет запросов между источниками, и по умолчанию ни один такой запрос не разрешён.

#### Раздел [repo]

Этот раздел настраивает подключение к базе данных PostgreSQL:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Параметр | Значение | Примечания |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` или IP | Хост PostgreSQL / IP-адрес |
| `DIGNA_REPO_PORT` | `5432` (по умолчанию) | Порт PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Имя базы данных |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Схема, созданная ранее |
| `DIGNA_REPO_USER` | `digna_user` | Пользователь, созданный при настройке PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Ваш пароль | Пароль, заданный при создании схемы |
| `DIGNA_REPO_SSLMODE` | `prefer` (по умолчанию) | Необязательно. Режим SSL для PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` или `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (по умолчанию) | Необязательно. Количество подключений к репозиторию, которые digna держит открытыми |

!!! tip "Лучшие практики"

    `config.toml` содержит пароль базы данных в открытом виде. Ограничьте права доступа к нему, чтобы читать его могла только служебная учётная запись:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### Раздел [base]

Этот раздел содержит параметры безопасности, cookie и инспекций:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Параметр | Значение | Примечания |
|---|---|---|
| `DIGNA_FERNET_KEY` | Значение, приведённое выше | Ключ шифрования, которое использовалось в прежних выпусках. Он должен присутствовать; сохраните приведённое значение |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Хост, по которому открывается dashboard. `""` не задаёт домен — это правильно за прокси, который обслуживает dashboard и backend под одним origin |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Должно быть `true` всегда, когда digna обслуживается по HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Делает cookie сессии недоступным для скриптов |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 часа) | Время жизни сессии в секундах |
| `DIGNA_MAX_WORKERS` | Количество ядер CPU - 1 | Количество инспекций, которые могут выполняться одновременно |
| `DIGNA_FRONTEND_BASEURL` | URL dashboard | Обязательно. Используется для ссылок в уведомлениях, поэтому это должен быть URL, который получатели могут открыть |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (по умолчанию) | Необязательно. Сколько секунд может выполняться один запрос к исходной базе данных, прежде чем он будет прерван; `0` отключает тайм-аут |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (по умолчанию) | Необязательно. Сколько секунд ждать подключения к исходной базе данных; `0` — ждать без ограничения |

!!! tip "Совет"

    Чтобы узнать количество ядер CPU, доступных на вашем сервере, выполните `nproc`.

#### Раздел [encryption]

Этот раздел содержит ключ, которым шифруются конфиденциальные значения, хранящиеся в репозитории. Он **обязателен** — `config check` сообщает о разделе `[encryption]` как FAILED, если ключ отсутствует.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Параметр | Значение | Примечания |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Ключ в кодировке Base64 | Шифрует конфиденциальные значения, хранящиеся в репозитории digna |

!!! warning "Защитите config.toml"

    Этот ключ — фиксированное значение, одинаковое во всех установках digna, и именно он
    расшифровывает конфиденциальные значения вашего репозитория. Ограничьте доступ к `config.toml`
    учётной записью, под которой работает digna, держите файл вне системы контроля версий и общих
    дисков и исключите его из любой резервной копии, которая хранится менее защищённо, чем сам репозиторий.

#### Раздел [logging]

Этот раздел настраивает поведение логирования:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Параметр | Значение | Примечания |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` или `DEBUG` | `INFO` для production, `DEBUG` для отладки. Также принимаются `TRACE`, `WARN` и `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (по умолчанию) | Необязательно. Каталог для файлов логов с ротацией, относительно рабочего каталога |
| `DIGNA_LOGGING_MAX_FILES` | `30` (по умолчанию) | Необязательно. Количество хранимых файлов логов после ротации |

#### Раздел [duckdb] (необязательный) {: #duckdb-section }

Новое в Release 2026.11. Этот раздел задаёт ресурсы **digna Engine**, который профилирует
данные внутри digna для подключений к базам данных, местом профилирования которых является **digna Engine**, и
выполняет проверки ссылочной целостности между источниками данных на разных подключениях к базам данных. См.
[Место профилирования](../../../platform/profiling/profiling_location.md).

Раздел необязателен. Без него действуют приведённые ниже значения по умолчанию.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Параметр | Значение | Примечания |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (по умолчанию) | Память в МБ, которую может использовать один запуск digna Engine. Одновременно могут быть активны до `DIGNA_MAX_WORKERS` запусков |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | По умолчанию: системный временный каталог (`$TMPDIR` или `/tmp`, если переменная не задана) | Каталог для временных файлов, когда данные не помещаются в память |

!!! tip "Расчёт ресурсов для digna Engine"

    Запланируйте до `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` памяти на хосте digna
    сверх того, что использует сам digna, а также достаточно свободного места на диске во временном
    каталоге, чтобы вместить данные самой большой инспектируемой даты источников данных, использующих digna Engine.
    Укажите в `DIGNA_DUCKDB_TEMP_DIRECTORY` диск с таким объёмом свободного места, доступный для записи
    учётной записи, под которой работает digna:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
    ```

    Этот раздел нужен, только если хотя бы одно подключение к базе данных использует digna Engine или
    проверка ссылочной целостности сравнивает источники данных на разных подключениях.

---

### Шаг 2: Проверьте конфигурацию

Перед инициализацией репозитория убедитесь, что `config.toml` полон и корректно построен. В каталоге установки digna выполните:

```bash
./digna config check
```

Каждый раздел проверяется отдельно, поэтому одна ошибка не скрывает состояние остальных:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Исправьте всё, о чём сообщено как FAILED, и выполните команду ещё раз, прежде чем продолжить. WARNING в пункте **Unknown keys** перечисляет ключи в `config.toml`, которые digna не считывает; они ни на что не влияют, поэтому удалите их или исправьте их написание. Полный список параметров приведён в [справочнике CLI](../../../cli/Command_Line_Interface_202611.md).

### Шаг 3: Инициализируйте репозиторий

1. Откройте терминал
2. Перейдите в каталог установки digna (где находятся `config.toml` и исполняемый файл `digna`)
3. Выполните проверку подключения:

```bash
cd /opt/digna
./digna repo check
```

Для новой схемы команда подключается и затем сообщает, что репозиторий ещё не установлен:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

На этом этапе это ожидаемый результат: он подтверждает, что digna достигает PostgreSQL и схемы. Ошибка подключения или аутентификации, напротив, указывает на раздел `[repo]` или на настройку PostgreSQL.

!!! note "Примечание"

    В Linux текущий каталог не входит в PATH, поэтому исполняемый файл вызывается как `./digna`, а не `digna`. Чтобы везде использовать короткую форму, добавьте символическую ссылку:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Шаг 4: Установите схему репозитория

В том же каталоге выполните:

```bash
./digna repo upgrade
```

Эта команда устанавливает необходимые таблицы в схеме репозитория и завершается сообщением:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade устанавливает и обновляет"

    Начиная с Release 2026.11, `repo upgrade` устанавливает новый репозиторий и обновляет существующий.
    `repo install` по-прежнему работает как другое имя той же команды.

### Шаг 5: Создайте пользователя с правами администратора

Пользователь-администратор создаётся непосредственно в схеме репозитория, поэтому сервер пока не обязательно запускать. В каталоге установки digna выполните:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Пример:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Это создаёт пользователя с адресом электронной почты `admin@example.com` и полными правами администратора.

!!! tip "Совет"

    Заключайте пароль в одинарные кавычки. `bash` и `zsh` обрабатывают такие символы, как `!`, `$` и `*`, особым образом, и пароль без кавычек, содержащий их, не будет передан в том виде, в котором вы его ввели.

!!! tip "Лучшие практики"

    Используйте надёжный пароль, сочетающий прописные и строчные буквы, цифры и специальные символы.

### Шаг 6: Запустите сервер digna

В каталоге установки digna запустите сервер:

```bash
./digna serve --address <host> --port <port>
```

**Параметры:**
- `--address` — хостнейм/IP сервера (по умолчанию `127.0.0.1`)
- `--port` — порт сервера (по умолчанию `8000`)

Когда сервер запущен, он выводит адрес, который прослушивает:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Совет"

    Если dashboard обслуживается с другой машины, чем backend, откройте в брандмауэре также порт API:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Сервер занимает терминал"

    `serve` выполняется на переднем плане и продолжает работать, пока вы не остановите его сочетанием ++ctrl+c++. Оставьте его работающим, пока завершаете настройку; чтобы вместо этого запускать его автоматически при загрузке, см. [Запуск digna как сервиса systemd](#running-digna-as-a-systemd-service).

---

## Конфигурация Dashboard {: #dashboard-configuration }

### Шаг 1: Разверните Dashboard на веб-сервере

Dashboard digna считывает собственную конфигурацию из файла `dashboard/dashboard_config.toml`. Этот файл не поставляется вместе с установкой — вы создаёте его в каталоге `dashboard/` рядом с файлами dashboard.

Его содержимое описано в разделе [Единый вход (SSO)](../../../sso/overview.md), где этот файл и требуется: в нём задаются варианты входа, которые предлагает dashboard, а для мульти-инстансных развёртываний — подключение к backend.

Выберите ваш веб-сервер и следуйте соответствующим шагам развертывания.

#### Развёртывание в nginx

Если вы следовали разделу [Настройка nginx](#nginx-setup), блок server уже указывает на вашу папку `dashboard` и копирование не требуется.

1. **Подтвердите путь**
   - Откройте `/etc/nginx/conf.d/digna.conf`
   - Убедитесь, что `root` указывает на распакованную папку `dashboard`

2. **Убедитесь, что папка доступна для чтения**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Перезагрузите nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Проверьте установку**
   - Откройте браузер
   - Перейдите по адресу `http://localhost` (или по вашему настроенному URL)
   - Вы должны увидеть страницу входа в digna dashboard

#### Развёртывание в Apache httpd

1. **Скопируйте Dashboard в корневой каталог документов**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Добавьте правила переписывания (Rewrite Rules)**

   Создайте файл `.htaccess` внутри развёрнутой папки, чтобы маршруты dashboard не ломались при обновлении страницы:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Доступ к Dashboard**
   - Откройте браузер
   - Перейдите по адресу `http://localhost/digna`
   - Вы должны увидеть страницу входа в digna dashboard

### Шаг 2: SELinux (только семейство RHEL)

В RHEL, Rocky, AlmaLinux и Fedora SELinux по умолчанию работает в принудительном режиме (enforcing) и не позволяет веб-серверу читать файлы за пределами ожидаемых расположений. Проверьте, активен ли он:

```bash
getenforce
```

Если результат — `Enforcing` и вы обслуживаете dashboard из `/opt/digna/dashboard`, назначьте каталогу метку, чтобы веб-сервер мог его читать:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Примечание"

    Если `semanage` не найден, установите его командой `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Важно"

    Если dashboard на только что настроенном сервере RHEL возвращает **403 Forbidden**, это почти всегда проблема меток SELinux, а не прав доступа к файлам. Убедитесь в этом с помощью `sudo ausearch -m avc -ts recent`.

---

## Запуск digna как сервиса systemd {: #running-digna-as-a-systemd-service }

### Зачем запускать digna как сервис?

Запуск backend digna как сервиса systemd гарантирует, что он:

- Автоматически запускается при загрузке машины
- Работает в фоновом режиме без открытого окна терминала
- Автоматически перезапускается при сбое
- Управляется через `systemctl`, стандартный менеджер сервисов Linux

### Файлы управления сервисом

Все необходимые файлы находятся в каталоге установки digna в папке: `bin/`

Доступны следующие shell-скрипты:

- `install_service.sh` — регистрирует digna в systemd
- `uninstall_service.sh` — удаляет регистрацию сервиса
- `start_service.sh` — запускает зарегистрированный сервис
- `stop_service.sh` — останавливает запущенный сервис

!!! warning "Требуются права root"

    Все скрипты должны выполняться с `sudo`, поскольку регистрация сервиса с автозапуском при загрузке записывает unit-файл в `/etc/systemd/system`.

### Как сделать скрипты исполняемыми

При распаковке бит выполнения мог не сохраниться. Перед первым использованием:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Установка сервиса

1. **Откройте терминал**

2. **Перейдите в папку bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Запустите скрипт установки**
   ```bash
   sudo ./install_service.sh
   ```

Сервер digna теперь зарегистрирован в systemd с включённым **автоматическим запуском**. Сервис не запускается сразу — см. следующий раздел для его запуска.

### Запуск и остановка сервиса

#### Чтобы запустить сервис

1. Откройте терминал
2. Перейдите в `/opt/digna/bin`
3. Выполните:
   ```bash
   sudo ./start_service.sh
   ```

#### Чтобы остановить сервис

1. Откройте терминал
2. Перейдите в `/opt/digna/bin`
3. Выполните:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Совет"

    Всегда останавливайте сервис перед обновлением файлов приложения.

### Управление сервисом с помощью systemctl

После регистрации сервисом также можно управлять стандартными командами systemd из любого каталога:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Проверка сервиса

Чтобы убедиться, что сервис зарегистрирован и запущен:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` означает, что сервис запускается при загрузке; `active` — что он работает сейчас.

### Просмотр журналов сервиса

systemd перехватывает всё, что backend выводит в консоль. Чтобы прочитать эти записи:

```bash
sudo journalctl -u digna -n 100
```

Чтобы следить за журналом в реальном времени, воспроизводя проблему:

```bash
sudo journalctl -u digna -f
```

!!! tip "Совет"

    Это самый быстрый способ диагностировать сервис, который запускается и сразу же останавливается. Ошибка подключения к репозиторию или отсутствующий `license.toml` отображаются именно здесь.

### Перенос сервиса в новый каталог

Unit-файл хранит абсолютный путь к исполняемому файлу, поэтому при переносе установки требуется повторная регистрация сервиса:

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

### Удаление сервиса

1. **Остановите запущенный сервис**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Удалите сервис**
   ```bash
   sudo ./uninstall_service.sh
   ```

Сервер digna теперь удалён из systemd.

---

## Обновление до новой версии {: #upgrading-to-a-new-release }

Этот раздел описывает обновление установки Release 2026.06 до Release 2026.11. Если ваша
установка старше, сначала прочитайте раздел [Обновление с выпуска старше 2026.06](#upgrading-from-a-release-before-2026-06).

### Перед обновлением

**Создание резервной копии репозитория digna обязательно**

Перед обновлением digna сделайте резервную копию вашего репозитория (PostgreSQL), чтобы защититься от потери данных.
Резервная копия позволит восстановиться в случае непредвиденных проблем при обновлении.

Чтобы создать резервную копию из оболочки:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Запрос файла лицензии для Release 2026.11**

Release 2026.11 требует нового `license.toml`. Запросите его у команды digna до начала обновления и
держите его наготове для [шага 7](#step-7-replace-the-license-file).

### Обновление с выпуска старше 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 принёс три изменения, которые по-прежнему действуют, когда вы обновляете более старую установку
сразу до 2026.11:

- **Только ODBC.** digna обращается к каждой технологии-источнику через ODBC. Каждое подключение к базе данных, которое
  ещё не использует ODBC, после обновления нужно перевести на ODBC; автоматического
  преобразования нет. Заранее установите драйверы ODBC на хосте digna, см.
  [Установка драйвера ODBC на узле digna](../../../databases/overview.md#install-the-driver),
  и подготовьте свойства каждого подключения по
  [руководствам по технологиям](../../../databases/overview.md#technology-guides). Коннектора Databricks Legacy
  больше нет; переведите такие подключения на
  коннектор [Databricks](../../../databases/databricks_connector_guide.md).
- **Один исполняемый файл.** `dignabackend` и `dignacli` заменены одним исполняемым файлом `digna`,
  который объединяет серверную часть и CLI.
- **config.toml.** Раздел `[encryption]` обязателен, а `DIGNA_APP_HOST` и
  `DIGNA_APP_PORT` больше не считываются: адрес и порт сервер берёт из `digna serve`.
  Сравните свой файл с разделом [Конфигурация backend](#backend-configuration).

Приведённые ниже шаги указывают, где более старой установке нужны другие действия. Обновление
репозитория в шаге 8 переводит репозиторий любого прежнего выпуска сразу на 2026.11.

### Процесс обновления

#### Шаг 1: Остановите сервис digna {: #step-1-stop-the-digna-service }

Если digna запущен как сервис systemd, сначала остановите его:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Если digna запущен на переднем плане, нажмите ++ctrl+c++ в окне терминала, где он работает.

#### Шаг 2: Резервное копирование текущей установки {: #step-2-backup-current-installation }

В каталоге установки digna переименуйте исполняемый файл и папку dashboard текущей
установки, чтобы новый выпуск можно было развернуть рядом с ними:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Сохраняйте `digna_old`, пока не проверите обновление, а `dashboard_old` — пока не восстановите
из неё свои файлы конфигурации (см. шаг 4). После этого оба можно удалить.

!!! info "Обновление с выпуска старше 2026.06"

    Переименуйте папки `dignabackend` и `dignacli` вместо исполняемого файла:
    `sudo mv dignabackend dignabackend_old` и `sudo mv dignacli dignacli_old`. Ни одна из них не используется в Release 2026.11.

#### Шаг 3: Распакуйте и разверните новую версию {: #step-3-extract-and-deploy-new-version }

1. Распакуйте новый ZIP-файл установки digna
2. Скопируйте новый исполняемый файл `digna` и папку `dashboard` в каталог установки
3. Восстановите бит выполнения и владельца — служебную учётную запись:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Важно"

    Ни `config.toml`, ни `dashboard/dashboard_config.toml` никогда не включаются в
    ZIP с установкой — команда digna никогда не поставляет эти файлы. Поэтому обновление
    не затрагивает вашу существующую конфигурацию, а копии в переименованных папках `*_old` — единственные,
    которые у вас есть.

#### Шаг 4: Восстановите файлы конфигурации {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 не требует изменений в `config.toml`: файл, который работает с Release 2026.06, продолжает
работать. Два изменения необязательны:

- Добавьте [раздел `[duckdb]`](#duckdb-section), если подключения к базам данных должны использовать digna Engine,
  а его значения по умолчанию не подходят для вашего хоста.
- Не указывайте раздел `[app]`, если обратный прокси обслуживает dashboard и backend под одним
  origin.

!!! warning "Параметры, которые digna не считывает"

    Прежние версии этого руководства приводили некоторые параметры, которые digna не считывает. Они ни на что не
    влияют, а `config check` в шаге 6 перечисляет их в пункте **Unknown keys**. Удалите или исправьте
    их:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` и
      `digna_LOGGING_BACKUP_COUNT` не существуют. Удалите их.
    - Имена параметров чувствительны к регистру. digna считывает `DIGNA_REPO_HOST`, а не `digna_REPO_HOST`.
      Пишите каждое имя прописными буквами, как в разделе [Конфигурация backend](#backend-configuration).

!!! warning "Единый вход: сохраните [[oidc_clients]]"

    digna считывает поставщиков единого входа как список записей `[[oidc_clients]]`, каждая со своим
    `DIGNA_OIDC_KEY`. Если вы изменили своих поставщиков на разделы `[oidc_clients.<key>]`, как показывала
    прежняя версия этого руководства, верните прежнюю форму. `config check` сообщает о
    `OIDC config(s)` как FAILED, пока действует такая форма:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Повторите запись для каждого поставщика и следите, чтобы каждый `DIGNA_OIDC_KEY` совпадал с `key` в
    `dashboard_config.toml`. Это касается только установок, использующих единый вход.

#### Шаг 5: Перезагрузите веб-сервер {: #step-5-reload-the-web-server }

Dashboard — это набор статических файлов, поэтому ваш веб-сервер, а также браузер, могут по-прежнему
отдавать предыдущую версию. Перезагрузите или перезапустите веб-сервер, на котором размещена папка `dashboard`,
затем обновите страницу с полной перезагрузкой (++ctrl+f5++).

#### Шаг 6: Проверьте конфигурацию {: #step-6-validate-the-configuration }

Прежде чем трогать репозиторий, убедитесь, что `config.toml` полон:

```bash
./digna config check
```

Каждый раздел должен сообщить OK. Исправьте всё, о чём сообщено как FAILED, удалите ключи, перечисленные в пункте
**Unknown keys**, и выполните команду ещё раз, прежде чем продолжить.

#### Шаг 7: Замените файл лицензии {: #step-7-replace-the-license-file }

Файл лицензии обычно переходит из одного выпуска в следующий. Release 2026.11 — исключение:
он добавляет два лицензируемых модуля, digna Data Reconciliation и digna Agentic, а лицензия,
выданная до 2026.11, их не содержит. Скопируйте `license.toml`, предоставленный командой digna
для Release 2026.11, в каталог установки, заменив старый:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Не оставляйте прежнюю лицензию"

    С прежней лицензией digna запускается, но digna Data Reconciliation и digna
    MCP Server остаются отключёнными. Каждая команда, проверяющая лицензию, — `user`,
    `inspection`, `repo` — прерывается, не затрагивая репозиторий, если проверка не пройдена. Проверьте
    новую лицензию, прежде чем продолжить:

    ```bash
    ./digna license check
    ```

#### Шаг 8: Обновите схему репозитория {: #step-8-upgrade-the-repository-schema }

В каталоге установки digna выполните:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 управляет схемой репозитория с помощью версионированных миграций. Первое обновление с
прежнего выпуска приводит схему к последней версии прежней системы, записывает это как
исходную точку, а затем применяет миграции Release 2026.11. Оно завершается так:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Все существующие данные сохраняются. Чтобы в любой момент увидеть состояние репозитория, выполните
`./digna repo check`: команда показывает последнюю применённую миграцию и все ожидающие применения.

!!! warning "digna не запускается с устаревшим репозиторием"

    Начиная с Release 2026.11, сервер отказывается запускаться, пока репозиторию требуется обновление, и
    сообщает об этом, например:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Выполните `repo upgrade`, прежде чем запускать сервер или сервис.

#### Шаг 9: Перезапустите сервисы {: #step-9-restart-services }

Если вы используете сервис systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Если запускаете вручную, перезапустите сервер:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Если используется nginx или Apache, перезагрузите соответствующий веб-сервер:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

В семействе RHEL повторно примените метки SELinux, если каталог `dashboard` был заменён:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Шаг 10: Проверьте корректность обновления {: #step-10-verify-the-upgrade }

1. Проверьте выпуск нового исполняемого файла:

    ```bash
    ./digna version
    ```

    Первая строка должна быть `Release: 2026.11`.

2. Откройте digna dashboard и убедитесь, что интерфейс загружается корректно.
3. Проверьте журналы сервера на наличие ошибок:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Проверьте свои подключения к базам данных — см.
   [Проверка подключения](../../../databases/overview.md#testing-a-connection). После обновления
   с выпуска старше 2026.06 сначала переведите на ODBC каждое подключение, которое его ещё не
   использовало.

Чтобы начать работу с новыми модулями, см. [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Подключение ИИ-агента](../../../platform/agentic/connect_ai_agent.md) для digna MCP Server и
[Место профилирования](../../../platform/profiling/profiling_location.md) для digna Engine.

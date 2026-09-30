# Руководство по установке на Linux для digna Release 2026.06

**Релиз:** 2026.06

**Последнее обновление:** 5 сентября 2026


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

### Что нового в Release 2026.06

В этом выпуске возможности наблюдаемости данных (data observability) интегрированы непосредственно в ваш код, что позволяет разработчикам отслеживать качество данных у источника. Полные подробности см. в [примечаниях к выпуску](http://docs.digna.ai/changelog/Release_202606/).

### Ищете Windows или macOS?

Это руководство охватывает Linux. Для других платформ см. [руководство по установке на Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) или [руководство по установке на macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

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
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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

Этот раздел настраивает параметры приложения digna backend:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Параметр | Значение | Примечания |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | URL фронтенда | Если dashboard размещён на другом сервере, укажите его URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Требуется для CORS с учётными данными |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Разрешить все HTTP-методы |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Разрешить все заголовки |

!!! note "Примечание"

    Если вы обслуживаете dashboard через nginx или Apache на стандартном HTTP-порту, разрешаемым origin будет `http://localhost` — или публичный URL сервера, если к dashboard обращаются с других машин.

#### Раздел [repo]

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

| Параметр | Значение | Примечания |
|---|---|---|
| `digna_REPO_HOST` | `localhost` или IP | Хост PostgreSQL / IP-адрес |
| `digna_REPO_PORT` | `5432` (по умолчанию) | Порт PostgreSQL |
| `digna_REPO_DB` | `postgres` | Имя базы данных |
| `digna_REPO_SCHEMA` | `dignarepo` | Схема, созданная ранее |
| `digna_REPO_USER` | `digna_user` | Пользователь, созданный при настройке PostgreSQL |
| `digna_REPO_PASSWORD` | Ваш пароль | Пароль, заданный при создании схемы |

!!! tip "Лучшие практики"

    `config.toml` содержит пароль базы данных в открытом виде. Ограничьте права доступа к нему, чтобы читать его могла только служебная учётная запись:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### Раздел [base]

Этот раздел содержит параметры безопасности и cookie:

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

| Параметр | Значение | Примечания |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Домен, соответствующий вашему фронтенду |
| `digna_COOKIE_SECURE` | `false` (локально) / `true` (production) | Используйте `true` для HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Всегда включено для безопасности |
| `digna_COOKIE_SAME_SITE` | `lax` | Предотвращает CSRF-атаки |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 часа) | Время жизни сессии в секундах |
| `digna_MAX_WORKERS` | Количество ядер CPU - 1 | Количество параллельных задач инспекции |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Максимальная задержка в секундах, которую планировщик может добавить перед запуском наступившей задачи |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Время суток (24-часовой формат `HH:MM`), когда начинается ежедневная очистка |

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Параметр | Значение | Примечания |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` или `DEBUG` | `INFO` для production, `DEBUG` для отладки |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Количество ежедневных резервных копий логов, которые сохраняются |

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

Overall: OK
```

Исправьте всё, о чём сообщено как FAILED, и выполните команду ещё раз, прежде чем продолжить. Полный список параметров приведён в [справочнике CLI](../../../cli/Command_Line_Interface_202606.md).

### Шаг 3: Инициализируйте репозиторий

1. Откройте терминал
2. Перейдите в каталог установки digna (где находятся `config.toml` и исполняемый файл `digna`)
3. Выполните проверку подключения:

```bash
cd /opt/digna
./digna repo check
```

Вы должны увидеть подтверждение установления соединения (сам репозиторий ещё не инициализирован).

!!! note "Примечание"

    В Linux текущий каталог не входит в PATH, поэтому исполняемый файл вызывается как `./digna`, а не `digna`. Чтобы везде использовать короткую форму, добавьте символическую ссылку:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Шаг 4: Установите схему репозитория

В том же каталоге выполните:

```bash
./digna repo install
```

Эта команда установит необходимые таблицы и схему в вашей базе данных PostgreSQL.

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

### Перед обновлением

**Сначала проверьте все подключения к базам данных**

Начиная с выпуска 2026.06 digna обращается к каждой исходной технологии через **ODBC**. Прежние выпуски
предлагали выбор между отдельным драйвером для каждой технологии и ODBC, задаваемый переключателем **Use ODBC**.
Команда digna решила опираться только на ODBC, потому что единый стандартный интерфейс даёт больше,
чем набор драйверов, написанных под заказ:

- **Аутентификация** — аутентификация является частью ODBC, поэтому подключение может использовать всё, что
  поддерживает его драйвер: пароли, токены и PAT, Kerberos и Active Directory, MFA и единый вход через браузер,
  облачные удостоверения, клиентские сертификаты и TLS. Новые методы появляются вместе с обновлением
  драйвера, а не после ожидания выпуска digna.
- **Драйверы, поддерживаемые производителями баз данных** — собственный драйвер производителя отслеживает новые версии
  сервера и исправления безопасности, и вы можете обновлять его в своём темпе, независимо от digna.
- **Единый способ настроить всё** — каждая технология — это список свойств «ключ/значение» с
  одним и тем же интерфейсом, одинаковым шифрованием конфиденциальных значений и одинаковой диагностикой,
  вместо разного набора полей для каждого источника.
- **Тонкая настройка и охват** — параметры драйвера, такие как тайм-ауты, настройки TLS, прокси-серверы и размеры
  выборки, доступны для любого источника, а подключить можно любую технологию с совместимым драйвером ODBC,
  в том числе те, для которых digna не публикует отдельного руководства.

На практике это означает, что переключателя **Use ODBC** и отдельных полей узла, порта, базы данных, пользователя и
пароля больше нет. **Каждое подключение, ещё не использующее ODBC, должно быть
переведено на ODBC** — автоматического преобразования нет, поэтому спланируйте это до обновления:

1. Просмотрите каждое подключение к базе данных, определённое в вашей установке, и отметьте те, которые
   ещё не используют ODBC — каждое из них придётся настроить заново.
2. Установите соответствующий драйвер ODBC на узле digna — подключения открываются с сервера,
   на котором работает серверная часть digna, а не из браузера. См.
   [Установка драйвера ODBC на узле digna](../../../databases/overview.md#install-the-driver).
3. Подготовьте свойства ODBC для каждого затронутого подключения.
   [Руководства по технологиям](../../../databases/overview.md#technology-guides) приводят для каждого источника
   проверенный набор свойств.

После обновления переведите каждое затронутое подключение на ODBC и проверьте его из панели управления —
см. [Создание подключения к базе данных](../../../databases/overview.md#create-a-database-connection)
и [Проверка подключения](../../../databases/overview.md#testing-a-connection).

!!! warning "Подключения Databricks Legacy"

    Коннектор Databricks Legacy удалён в этом выпуске. Переведите такие подключения
    на коннектор [Databricks](../../../databases/databricks_connector_guide.md).

**Создание резервной копии репозитория digna обязательно**

Перед обновлением digna сделайте резервную копию вашего репозитория (PostgreSQL), чтобы защититься от потери данных.
Резервная копия позволит восстановиться в случае непредвиденных проблем при обновлении.

Чтобы создать резервную копию из оболочки:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Процесс обновления

#### Шаг 1: Остановите сервис digna

Если digna запущен как сервис systemd, сначала остановите его:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Если digna запущен на переднем плане, нажмите `Ctrl + C` в окне терминала, где он работает.

#### Шаг 2: Резервное копирование текущей установки

В каталоге установки digna переименуйте папки текущей установки, чтобы новый выпуск можно было развернуть рядом с ними:

```bash
cd /opt/digna
sudo mv dignabackend dignabackend_old
```
```bash
sudo mv dignacli dignacli_old
```
```bash
sudo mv dashboard dashboard_old
```

!!! info "dignabackend и dignacli больше не используются"

    Начиная с выпуска 2026.06 `dignabackend` и `dignacli` заменены одним исполняемым файлом `digna`, объединяющим серверную часть и CLI. Сохраняйте `dignabackend_old` и `dignacli_old` только до тех пор, пока не проверите обновление, — после этого обе папки можно удалить. Сохраняйте `dashboard_old`, пока не восстановите из неё свои файлы конфигурации (см. шаг 4).

#### Шаг 3: Распакуйте и разверните новую версию

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

#### Шаг 4: Восстановите файлы конфигурации

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

!!! warning "Выпуск 2026.06 изменяет config.toml"

    Три параметра новые и обязательные, а три больше не используются. `config.toml`, перенесённый из прежнего выпуска, новых параметров не содержит, и digna не запустится, пока они отсутствуют. Добавьте в существующий `config.toml` следующее:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Добавьте два ключа `[base]` в существующий раздел `[base]` и добавьте `[encryption]` как новый раздел. Затем удалите параметры, которые больше не используются: **`digna_FERNET_KEY`** из `[base]`, а также **`digna_APP_HOST`** и **`digna_APP_PORT`** из `[app]` — адрес и порт сервер теперь берёт из `digna serve`.

    Назначение каждого параметра описано в разделе [Конфигурация backend](#backend-configuration).

!!! warning "Единый вход: формат [oidc_clients] изменился"

    В выпуске 2026.06 массив таблиц заменён отдельной таблицей для каждого поставщика, названной по
    ключу поставщика. `DIGNA_OIDC_KEY` исчезает — ключ теперь является частью заголовка раздела.

    Было:

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

    Повторите раздел для каждого поставщика и следите, чтобы каждый ключ совпадал с `key` в файле
    `dashboard_config.toml`. `digna config check` сообщает о разделе `oidc_clients` как FAILED, пока
    сохраняется прежняя форма. Это касается только установок, использующих единый вход.

#### Шаг 5: Перезагрузите веб-сервер

Dashboard — это набор статических файлов, поэтому ваш веб-сервер, а также браузер, могут по-прежнему
отдавать предыдущую версию. Перезагрузите или перезапустите веб-сервер, на котором размещена папка `dashboard`,
затем обновите страницу с полной перезагрузкой (++ctrl+f5++).

#### Шаг 6: Проверьте конфигурацию

Прежде чем трогать репозиторий, убедитесь, что обновлённый `config.toml` полон:

```bash
./digna config check
```

Каждый раздел должен сообщить OK. Исправьте всё, о чём сообщено как FAILED, и выполните команду ещё раз, прежде чем продолжить.

#### Шаг 7: Замените файл лицензии

Каждый выпуск лицензируется отдельно. Скопируйте `license.toml`, предоставленный командой digna для
этого выпуска, в каталог установки, заменив старый:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Не оставляйте прежнюю лицензию"

    `license.toml`, выданный для более раннего выпуска, не распространяется на этот, и каждая команда,
    проверяющая лицензию, — `user`, `inspection`, `repo` — прерывается, не затрагивая
    репозиторий, если проверка не пройдена. Проверьте лицензию, прежде чем продолжить:

    ```bash
    ./digna license check
    ```

#### Шаг 8: Обновите схему репозитория

Перейдите в каталог установки digna и выполните:

```bash
cd /opt/digna
./digna repo upgrade
```

Это обновит схему PostgreSQL до последней версии, сохранив все существующие данные.

#### Шаг 9: Перезапустите сервисы

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

#### Шаг 10: Проверьте корректность обновления

1. Откройте интерфейс digna dashboard
2. Убедитесь, что интерфейс загружается корректно
3. Проверьте журналы сервера на наличие ошибок
4. Переведите на ODBC каждое подключение, которое его ещё не использовало, затем проверьте все подключения
   — см. [Проверка подключения](../../../databases/overview.md#testing-a-connection):

```bash
sudo journalctl -u digna -n 100
```
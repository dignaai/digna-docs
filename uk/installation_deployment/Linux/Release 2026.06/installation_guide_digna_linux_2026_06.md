# Посібник зі встановлення digna Release 2026.06 на Linux

**Випуск:** 2026.06

**Останнє оновлення:** 5 вересня 2026 р.


---

## Зміст

1. [Вступ](#introduction)
2. [Системні вимоги](#system-requirements)
3. [Підготовка до встановлення](#pre-installation-setup)
4. [Налаштування сервера PostgreSQL](#postgresql-server-setup)
5. [Налаштування веб‑сервера](#web-server-configuration)
6. [Початкове встановлення](#initial-installation)
7. [Налаштування серверної частини](#backend-configuration)
8. [Налаштування панелі](#dashboard-configuration)
9. [Запуск digna як служби systemd](#running-digna-as-a-systemd-service)
10. [Оновлення до нового випуску](#upgrading-to-a-new-release)

---

## Вступ {: #introduction }

### Про digna

digna — це комплексна платформа на основі AI, призначена для оптимізації управління якістю даних у різних середовищах даних, таких як сховища даних (warehouses), озера даних (lakes) і lakehouses. Побудована з розрахунком на високу масштабованість та адаптивність, digna вирішує сучасні завдання роботи з даними завдяки автоматизації, моніторингу в реальному часі та виявленню аномалій.

digna складається з двох основних компонентів:

- **digna**: ядро застосунку, відповідальне за обробку даних і виконання перевірок якості. Воно поєднує серверну частину та інтерфейс командного рядка в одному виконуваному файлі, замінюючи окремі програми `dignabackend` і `dignacli` з попередніх випусків.
- **dignadashboard**: веб‑інтерфейс, розміщений на веб‑сервері, що забезпечує зручний спосіб взаємодії з платформою digna та візуалізації метрик якості даних.

### Що нового в Release 2026.06

Цей випуск вбудовує можливості спостереження за даними безпосередньо у ваш код, що дає змогу розробникам контролювати якість даних на джерелі. Повні відомості див. у [примітках до випуску](http://docs.digna.ai/changelog/Release_202606/).

### Шукаєте Windows або macOS?

Цей посібник охоплює Linux. Для інших платформ див. [Посібник зі встановлення на Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) або [Посібник зі встановлення на macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

### Які дистрибутиви охоплює цей посібник?

Інструкції написано для двох найпоширеніших сімейств серверних дистрибутивів. Там, де вони відрізняються, наведено обидві команди:

- **Сімейство Debian** — Debian, Ubuntu. Менеджер пакетів: `apt`.
- **Сімейство RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Менеджер пакетів: `dnf`.

Підійде будь-який сучасний дистрибутив із `systemd`; змінюються лише назви пакетів і кілька шляхів конфігурації.

---

## Системні вимоги {: #system-requirements }

Перш ніж почати встановлення, переконайтеся, що ваша система відповідає таким мінімальним вимогам:

| Вимога | Специфікація |
|---|---|
| **Операційна система** | Ubuntu 22.04 LTS або новіша, Debian 12 або новіша, RHEL 9 / Rocky 9 / AlmaLinux 9 або новіша |
| **Архітектура** | x86_64 (amd64) або arm64 |
| **Система ініціалізації** | systemd |
| **Пам'ять (мінімальна конфігурація)** | 16 GB RAM |
| **Дисковий простір** | 10 GB вільного місця |
| **База даних** | PostgreSQL Server 12 або новіший |
| **Веб‑сервер** | nginx, Apache httpd або аналог |

### Варіанти встановлення бази даних

**Якщо PostgreSQL уже встановлено:**
Ви можете додати нову базу даних для digna до наявного сервера PostgreSQL.

**Якщо PostgreSQL встановлюється на тій самій машині, що й digna:**

!!! info "Рекомендовані характеристики"

    - **Пам'ять**: 32 GB RAM (замість 16 GB)
    - **Дисковий простір**: 50 GB вільного місця (замість 10 GB)

    Ці підвищені характеристики розраховані на одночасну роботу digna та бази даних PostgreSQL.

### Перевірка дистрибутива та архітектури

Кілька команд у цьому посібнику відрізняються для сімейств Debian і RHEL. Щоб перевірити, яке у вас, виконайте:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` або `ID=debian` — використовуйте команди `apt`.
- `ID=rhel`, `rocky`, `almalinux` або `fedora` — використовуйте команди `dnf`.
- `x86_64` або `aarch64` — архітектура інсталяційного пакета, який вам потрібен.

---

## Підготовка до встановлення {: #pre-installation-setup }

Перед встановленням digna переконайтеся, що наявні дві ключові передумови:

1. **Сервер PostgreSQL** – для зберігання обчислених метрик і даних про продуктивність
2. **Веб‑сервер** – для розміщення панелі digna (digna Dashboard)

Якщо ці компоненти ще не налаштовано, скористайтеся наведеними нижче розділами, щоб установити та налаштувати їх.

### Оновлення індексу пакетів

Перш ніж щось установлювати, оновіть списки пакетів:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Примітка"

    У всьому цьому посібнику перша команда з пари призначена для **сімейства Debian**, а друга — для **сімейства RHEL**. Виконуйте лише ту, що відповідає вашій системі.

---

## Налаштування сервера PostgreSQL {: #postgresql-server-setup }

### Якщо у вас уже є PostgreSQL

Якщо PostgreSQL уже встановлено й запущено на вашій локальній машині або ви використовуєте керований віддалений сервер PostgreSQL, можете перейти до [наступного розділу](#web-server-configuration).

### Встановлення PostgreSQL

#### Крок 1: Встановіть пакет сервера

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Порада"

    Пакети дистрибутива можуть відставати від поточного випуску PostgreSQL. Якщо вам потрібна конкретна новіша версія, використовуйте натомість офіційний [репозиторій PostgreSQL для apt або yum](https://www.postgresql.org/download/linux/).

#### Крок 2: Ініціалізуйте кластер бази даних

У **сімействі Debian** пакет автоматично створює та запускає кластер — переходьте до наступного кроку.

У **сімействі RHEL** кластер потрібно створити явно:

```bash
sudo postgresql-setup --initdb
```

#### Крок 3: Запустіть службу й увімкніть автозапуск

```bash
sudo systemctl enable --now postgresql
```

Ця команда одразу запускає PostgreSQL і налаштовує його автоматичний запуск під час завантаження системи.

#### Крок 4: Перевірте встановлення

```bash
psql --version
sudo systemctl status postgresql
```

Ви повинні побачити версію PostgreSQL і службу в стані `active (running)`.

#### Крок 5: Підключіться до сервера

Пакет PostgreSQL для Linux створює системний обліковий запис `postgres`, якому належить кластер. Підключайтеся через нього:

```bash
sudo -u postgres psql
```

!!! note "Примітка — тут Linux відрізняється від Windows"

    Інсталятор для Windows під час налаштування пропонує задати пароль суперкористувача `postgres`. Пакети для Linux цього не роблять. Натомість локальні підключення автентифікуються за допомогою **peer‑автентифікації**: користувачеві операційної системи `postgres` дозволено підключатися як користувач бази даних `postgres` без пароля.

    Саме тому команда вище використовує `sudo -u postgres`. Серверна частина digna підключається через TCP з ім'ям користувача та паролем, тож ви створите окремого користувача digna в розділі [Початкове встановлення](#initial-installation).

#### Крок 6: Перевірте порт

Стандартний порт PostgreSQL — `5432`. Щоб перевірити, який порт прослуховує ваш сервер:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Запишіть це значення — воно знадобиться під час налаштування серверної частини digna.

#### Крок 7: Увімкніть автентифікацію за паролем для користувача digna

digna підключається до PostgreSQL через TCP як `digna_user`, що потребує автентифікації за паролем, а не peer‑автентифікації. Переконайтеся, що ваш `pg_hba.conf` це дозволяє.

Знайдіть файл:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Відкрийте його в редакторі й переконайтеся, що рядки для локального TCP використовують `scram-sha-256` (або `md5` на старіших серверах), а не `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Після будь-яких змін перезавантажте конфігурацію PostgreSQL:

```bash
sudo systemctl reload postgresql
```

!!! warning "Важливо"

    Якщо digna повідомляє `FATAL: Ident authentication failed for user "digna_user"`, причина саме в цьому налаштуванні.

#### Крок 8: Якщо PostgreSQL працює на іншій машині

Щоб приймати підключення з іншого хоста, задайте `listen_addresses` у `postgresql.conf` і додайте відповідний рядок `host` для вашої мережі в `pg_hba.conf`:

```
listen_addresses = '*'
```

Потім відкрийте порт у брандмауері та перезапустіть службу:

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

## Налаштування веб‑сервера {: #web-server-configuration }

digna потребує веб‑сервера для розміщення панелі. Виберіть один із таких варіантів:

- [nginx](#nginx-setup) — легкий і рекомендований
- [Apache httpd](#apache-setup) — широко поширена альтернатива

Потрібно встановити й налаштувати лише **один** із цих серверів.

Обидва розділи налаштовують дві речі, від яких залежить панель:

- **Резервний маршрут для односторінкового застосунку (SPA fallback)**, щоб оновлення URL панелі не повертало 404
- **Тип MIME для `.md`**, щоб файли Markdown віддавалися коректно

### Налаштування nginx {: #nginx-setup }

#### Огляд

nginx — легкий високопродуктивний веб‑сервер, що добре підходить для віддавання статичної панелі digna.

#### Встановлення

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

#### Перевірте встановлення

1. Відкрийте браузер
2. Перейдіть за адресою `http://localhost`
3. Ви повинні побачити сторінку привітання nginx

#### Відкриття брандмауера

Якщо до сервера звертаються з інших машин, дозвольте трафік HTTP:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Налаштування сайту для панелі

В обох сімействах дистрибутивів nginx підключає кожен файл зі свого каталогу `conf.d`. Створіть там окремий файл конфігурації для digna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Вставте наведене нижче, замінивши `/opt/digna/dashboard` фактичним шляхом до розпакованої теки `dashboard`:

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

!!! warning "Важливо"

    Без директиви `try_files` перезавантаження будь-якої сторінки панелі, окрім кореневого URL, повертає 404. Це відповідник модуля URL Rewrite, якого потребує IIS у Windows.

#### Вимкніть сайт за замовчуванням

Лише один блок server може бути `default_server` для порту. У **сімействі Debian** видаліть стандартний сайт із пакета, щоб він не конфліктував:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

У **сімействі RHEL** закоментуйте або видаліть блок `server { ... }` у `/etc/nginx/nginx.conf`.

#### Застосуйте конфігурацію

Перевірте конфігурацію на синтаксичні помилки, а потім перезавантажте nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Налаштування Apache httpd {: #apache-setup }

#### Огляд

Apache httpd доступний у стандартних репозиторіях кожного підтримуваного дистрибутива. У сімействі Debian пакет називається `apache2`, а в сімействі RHEL — `httpd`.

#### Встановлення

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

#### Перевірте встановлення

1. Відкрийте браузер
2. Перейдіть за адресою `http://localhost`
3. Ви повинні побачити стандартну сторінку Apache вашого дистрибутива

#### Обов'язково: увімкніть mod_rewrite

Панель потребує перезапису URL.

У **сімействі Debian** увімкніть модуль і перезапустіть сервер:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

У **сімействі RHEL** `mod_rewrite` завантажується за замовчуванням. Переконайтеся в цьому:

```bash
httpd -M | grep rewrite
```

#### Обов'язково: дозвольте перевизначення через .htaccess

Відкрийте файл конфігурації для кореневого каталогу документів:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Знайдіть блок `<Directory>`, що охоплює кореневий каталог документів (`/var/www/html` в обох сімействах), і змініть:

```apache
AllowOverride None
```

на:

```apache
AllowOverride All
```

#### Обов'язково: тип MIME для файлів Markdown

У тому самому файлі додайте такий рядок, щоб файли Markdown віддавалися коректно:

```apache
AddType text/markdown .md
```

!!! warning "Важливо"

    Без цього налаштування файли `.md` можуть віддаватися некоректно.

#### Застосуйте конфігурацію

Перевірте конфігурацію на синтаксичні помилки, а потім перезапустіть Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Початкове встановлення {: #initial-installation }

### Крок 1: Налаштуйте репозиторій digna

Репозиторій digna зберігає всі метрики, обчислені digna. Він слугує центральною базою даних для аналітичних даних і даних про продуктивність.

#### Створіть схему репозиторію та користувача

Відкрийте свій клієнт PostgreSQL (psql, pgAdmin або подібний) і виконайте такі SQL‑команди:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Замініть такі заповнювачі:**

- `<digna_repo_schema>` — бажана назва схеми (наприклад, `dignarepo`)
- `<digna_repo_user>` — бажане ім'я користувача (наприклад, `digna_user`)
- `<digna_repo_password>` — надійний пароль для цього користувача

**Приклад:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Щоб виконати їх з оболонки за один крок:

```bash
sudo -u postgres psql
```

Потім вставте оператори в запрошенні `postgres=#` і введіть `\q`, щоб вийти.

!!! tip "Найкраща практика"

    Використовуйте надійні, складні паролі для користувачів бази даних. Уникайте облікових даних, які легко вгадати.

---

### Крок 2: Розпакуйте інсталяційний пакет digna

1. Знайдіть наданий вам ZIP‑файл інсталяції digna
2. Розпакуйте його в бажане місце встановлення — наприклад, `/opt/digna`
3. Після розпакування ви побачите такі елементи:
   - `dashboard/` — веб‑інтерфейс панелі
   - `digna` — основний виконуваний файл (серверна частина та CLI разом)

!!! info "Файли конфігурації та ліцензії не входять до пакета"

    Ні `config.toml`, ні `dashboard/dashboard_config.toml` не постачаються разом зі встановленням — ви
    створюєте обидва файли самостійно, у розділах [Налаштування серверної частини](#backend-configuration) і
    [Налаштування панелі](#dashboard-configuration). `license.toml` також не постачається;
    digna надає його окремо, як описано в кроці 3.

Щоб розпакувати з оболонки:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Примітка"

    Якщо `unzip` не встановлено, додайте його командою `sudo apt install -y unzip` або `sudo dnf install -y unzip`.

#### Зробіть файл виконуваним

Залежно від того, як передавався архів, біт виконання може не зберегтися після розпакування. Задайте його явно:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Створіть службовий обліковий запис

Для production‑розгортань рекомендується запускати серверну частину від імені окремого непривілейованого користувача:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Примітка"

    У сімействі RHEL відповідний шлях до оболонки — `/sbin/nologin`.

### Крок 3: Встановіть файл ліцензії

!!! warning "Важливо"

    Файл ліцензії **не** входить до інсталяційного пакета й надається digna окремо.

1. Знайдіть наданий вам файл `license.toml`
2. Скопіюйте його в кореневий каталог встановлення digna (там, де розташовані `config.toml` і виконуваний файл `digna`)

**Чому це важливо:**
Файл ліцензії містить відомості про клієнта, дату закінчення терміну дії ліцензії та цифровий підпис. **Не змінюйте цей файл** — будь‑які зміни зроблять його недійсним.

**Структура каталогу після налаштування:**

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

## Налаштування серверної частини {: #backend-configuration }

### Крок 1: Створіть і відредагуйте файл конфігурації

Файл `config_template.toml` постачається у вашому каталозі встановлення digna. Потрібно лише перейменувати його на `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Розташування:** `/opt/digna/config.toml`

Відкрийте `config.toml` у текстовому редакторі й налаштуйте кожен із наведених нижче розділів.

#### Розділ [app]

Цей розділ налаштовує параметри серверного застосунку digna:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Параметр | Значення | Примітки |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontend | Якщо панель розміщено на іншому сервері, додайте її URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Потрібно для CORS з обліковими даними |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Дозволити всі методи HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Дозволити всі заголовки |

!!! note "Примітка"

    Якщо ви віддаєте панель через nginx або Apache на стандартному порту HTTP, дозволити потрібно джерело `http://localhost` — або публічний URL сервера, якщо до панелі звертаються з інших машин.

#### Розділ [repo]

Цей розділ налаштовує підключення до бази даних PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Параметр | Значення | Примітки |
|---|---|---|
| `digna_REPO_HOST` | `localhost` або IP | Ім'я хоста / IP сервера PostgreSQL |
| `digna_REPO_PORT` | `5432` (за замовчуванням) | Порт PostgreSQL |
| `digna_REPO_DB` | `postgres` | Назва бази даних |
| `digna_REPO_SCHEMA` | `dignarepo` | Схема, створена раніше |
| `digna_REPO_USER` | `digna_user` | Користувач, створений під час налаштування PostgreSQL |
| `digna_REPO_PASSWORD` | Ваш пароль | Пароль, заданий під час створення схеми |

!!! tip "Найкраща практика"

    `config.toml` містить пароль до бази даних у відкритому вигляді. Обмежте права доступу до нього, щоб читати його міг лише службовий обліковий запис:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### Розділ [base]

Цей розділ містить параметри безпеки та cookie:

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

| Параметр | Значення | Примітки |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Має відповідати домену frontend |
| `digna_COOKIE_SECURE` | `false` (локально) / `true` (production) | Використовуйте `true` для з'єднань HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Завжди ввімкнено з міркувань безпеки |
| `digna_COOKIE_SAME_SITE` | `lax` | Запобігає атакам CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 години) | Тайм‑аут сесії в секундах |
| `digna_MAX_WORKERS` | Кількість ядер CPU - 1 | Кількість паралельних завдань інспекції |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Максимальна затримка в секундах, яку планувальник може додати перед запуском завдання, термін якого настав |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Час доби (24-годинний формат `HH:MM`), коли починається щоденне очищення |

!!! tip "Порада"

    Щоб дізнатися кількість ядер CPU, доступних на вашому сервері, виконайте `nproc`.

#### Розділ [encryption]

Цей розділ містить ключ, яким шифруються конфіденційні значення, що зберігаються в репозиторії. Він **обов'язковий** — `config check` повідомляє про розділ `[encryption]` як FAILED, якщо ключа немає.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Параметр | Значення | Примітки |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Ключ у кодуванні Base64 | Шифрує конфіденційні значення, що зберігаються в репозиторії digna |

!!! warning "Захистіть config.toml"

    Цей ключ — фіксоване значення, однакове в усіх установленнях digna, і саме він розшифровує
    конфіденційні значення у вашому репозиторії. Обмежте доступ до `config.toml` обліковим записом, під яким працює
    digna, тримайте файл поза системою контролю версій і спільними дисками та виключіть його з будь-якої резервної копії,
    що зберігається менш захищено, ніж сам репозиторій.

#### Розділ [logging]

Цей розділ налаштовує поведінку журналювання:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Параметр | Значення | Примітки |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` або `DEBUG` | `INFO` — для production, `DEBUG` — для усунення несправностей |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Кількість щоденних резервних копій журналів, які зберігаються |

---

### Крок 2: Перевірте конфігурацію

Перед ініціалізацією репозиторію переконайтеся, що `config.toml` повний і правильно сформований. У каталозі встановлення digna виконайте:

```bash
./digna config check
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

### Крок 3: Ініціалізуйте репозиторій

1. Відкрийте термінал
2. Перейдіть до каталогу встановлення digna (там, де розташовані `config.toml` і виконуваний файл `digna`)
3. Запустіть перевірку підключення:

```bash
cd /opt/digna
./digna repo check
```

Ви повинні побачити підтвердження, що з'єднання встановлено (сам репозиторій ще не ініціалізовано).

!!! note "Примітка"

    У Linux поточний каталог не входить до PATH, тож виконуваний файл викликається як `./digna`, а не `digna`. Щоб скрізь використовувати коротшу форму, додайте символьне посилання:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Крок 4: Встановіть схему репозиторію

У тому самому каталозі виконайте:

```bash
./digna repo install
```

Ця команда встановлює необхідні таблиці та схему у вашій базі даних PostgreSQL.

### Крок 5: Створіть користувача‑адміністратора

Користувач‑адміністратор створюється безпосередньо у схемі репозиторію, тож сервер поки що не мусить працювати. У каталозі встановлення digna виконайте:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Приклад:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Це створює користувача з адресою електронної пошти `admin@example.com` і повними адміністративними правами.

!!! tip "Порада"

    Беріть пароль в одинарні лапки. `bash` і `zsh` обробляють такі символи, як `!`, `$` і `*`, по-особливому, і пароль без лапок, що містить їх, не буде передано так, як його введено.

!!! tip "Найкраща практика"

    Використовуйте надійний пароль, що поєднує великі й малі літери, цифри та спеціальні символи.

### Крок 6: Запустіть сервер digna

У каталозі встановлення digna запустіть сервер командою:

```bash
./digna serve --address <host> --port <port>
```

**Параметри:**
- `--address` — ім'я хоста / IP сервера
- `--port` — порт сервера

Ви повинні побачити повідомлення про запуск, що підтверджують роботу сервера:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Порада"

    Якщо панель розміщено на іншій машині, ніж серверну частину, відкрийте в брандмауері також порт API:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Сервер займає термінал"

    `serve` виконується на передньому плані й працює, доки ви не зупините його комбінацією ++ctrl+c++. Залиште його працювати, доки завершуєте налаштування; щоб натомість запускати його автоматично під час завантаження системи, див. [Запуск digna як служби systemd](#running-digna-as-a-systemd-service).

---

## Налаштування панелі {: #dashboard-configuration }

### Крок 1: Розгорніть панель на веб‑сервері

Панель digna зчитує власну конфігурацію з `dashboard/dashboard_config.toml`. Цей файл не постачається разом зі встановленням — ви створюєте його в каталозі `dashboard/` поруч із файлами панелі.

Його вміст описано в розділі [Single Sign-On](../../../sso/overview.md), і саме там цей файл і потрібен: він містить варіанти входу, які пропонує панель, а для розгортань із кількома екземплярами — підключення до серверної частини.

Виберіть свій веб‑сервер і виконайте відповідні кроки розгортання.

#### Розгортання в nginx

Якщо ви виконали кроки розділу [Налаштування nginx](#nginx-setup), блок server уже вказує на вашу теку `dashboard`, і нічого копіювати не потрібно.

1. **Перевірте шлях**
   - Відкрийте `/etc/nginx/conf.d/digna.conf`
   - Переконайтеся, що `root` вказує на розпаковану теку `dashboard`

2. **Переконайтеся, що теку можна читати**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Перезавантажте nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Перевірте встановлення**
   - Відкрийте браузер
   - Перейдіть за адресою `http://localhost` (або за налаштованим вами URL)
   - Ви повинні побачити сторінку входу панелі digna

#### Розгортання в Apache httpd

1. **Скопіюйте панель до кореневого каталогу документів**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Додайте правила перезапису**

   Створіть файл `.htaccess` у розгорнутій теці, щоб маршрути панелі зберігалися після оновлення сторінки в браузері:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Вставте наведене нижче:

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

3. **Перезапустіть Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Відкрийте панель**
   - Відкрийте браузер
   - Перейдіть за адресою `http://localhost/digna`
   - Ви повинні побачити сторінку входу панелі digna

### Крок 2: SELinux (лише сімейство RHEL)

У RHEL, Rocky, AlmaLinux і Fedora SELinux за замовчуванням працює в примусовому режимі й блокуватиме веб‑серверу читання файлів поза очікуваними розташуваннями. Перевірте, чи він активний:

```bash
getenforce
```

Якщо результат — `Enforcing` і ви віддаєте панель з `/opt/digna/dashboard`, позначте каталог міткою, щоб веб‑сервер міг його читати:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Примітка"

    Якщо `semanage` не знайдено, встановіть його командою `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Важливо"

    Якщо панель на щойно налаштованому сервері RHEL повертає **403 Forbidden**, це майже завжди проблема міток SELinux, а не прав доступу до файлів. Перевірте це командою `sudo ausearch -m avc -ts recent`.

---

## Запуск digna як служби systemd {: #running-digna-as-a-systemd-service }

### Навіщо запускати digna як службу?

Запуск серверної частини digna як служби systemd гарантує, що вона:

- Автоматично запускається під час завантаження машини
- Працює у фоновому режимі без відкритого вікна термінала
- Автоматично перезапускається в разі збою
- Керується через `systemctl` — стандартний менеджер служб Linux

### Файли керування службою

Усі необхідні файли розташовані в каталозі встановлення digna, у підкаталозі `bin/`

Доступні такі скрипти оболонки:

- `install_service.sh` — реєструє digna в systemd
- `uninstall_service.sh` — скасовує реєстрацію служби
- `start_service.sh` — запускає зареєстровану службу
- `stop_service.sh` — зупиняє запущену службу

!!! warning "Потрібні права root"

    Усі скрипти потрібно виконувати через `sudo`, оскільки реєстрація служби, що запускається під час завантаження системи, записує unit‑файл до `/etc/systemd/system`.

### Як зробити скрипти виконуваними

Розпакування може не зберегти біт виконання. Перед першим використанням виконайте:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Встановлення служби

1. **Відкрийте термінал**

2. **Перейдіть до теки bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Запустіть скрипт встановлення**
   ```bash
   sudo ./install_service.sh
   ```

Тепер сервер digna зареєстровано в systemd з увімкненим **автоматичним запуском**. Служба не запускається одразу — щоб запустити її, див. наступний розділ.

### Запуск і зупинка служби

#### Щоб запустити службу

1. Відкрийте термінал
2. Перейдіть до `/opt/digna/bin`
3. Виконайте:
   ```bash
   sudo ./start_service.sh
   ```

#### Щоб зупинити службу

1. Відкрийте термінал
2. Перейдіть до `/opt/digna/bin`
3. Виконайте:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Порада"

    Завжди зупиняйте службу перед оновленням файлів застосунку.

### Керування службою через systemctl

Після реєстрації службою також можна керувати стандартними командами systemd з будь-якого каталогу:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Перевірка служби

Щоб переконатися, що службу зареєстровано й вона працює:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` означає, що служба запускається під час завантаження системи; `active` означає, що вона працює зараз.

### Перегляд журналів служби

systemd перехоплює все, що серверна частина виводить на консоль. Щоб прочитати це:

```bash
sudo journalctl -u digna -n 100
```

Щоб стежити за журналом наживо під час відтворення проблеми:

```bash
sudo journalctl -u digna -f
```

!!! tip "Порада"

    Це найшвидший спосіб діагностувати службу, яка запускається й одразу зупиняється. Тут з'являються повідомлення про збій підключення до репозиторію або відсутній `license.toml`.

### Перенесення служби до нового каталогу

Unit‑файл зберігає абсолютний шлях до виконуваного файлу, тож перенесення встановлення потребує повторної реєстрації служби:

1. **Видаліть поточну службу**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Перемістіть файли застосунку**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Повторно встановіть службу**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Запустіть службу**
   ```bash
   sudo ./start_service.sh
   ```

### Видалення служби

1. **Зупиніть запущену службу**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Видаліть службу**
   ```bash
   sudo ./uninstall_service.sh
   ```

Реєстрацію сервера digna в systemd скасовано.

---

## Оновлення до нового випуску {: #upgrading-to-a-new-release }

### Перед оновленням

**Спершу перевірте всі підключення до баз даних**

Починаючи з Release 2026.06, digna звертається до кожної технології-джерела через **ODBC**. Попередні випуски
пропонували вибір між окремим драйвером для кожної технології та ODBC, що задавався перемикачем **Use ODBC**.
Команда digna вирішила спиратися лише на ODBC, бо єдиний стандартний інтерфейс дає вам
більше, ніж набір спеціально написаних драйверів:

- **Автентифікація** — автентифікація є частиною ODBC, тож підключення може використовувати все, що підтримує його
  драйвер: паролі, токени та PAT, Kerberos і Active Directory, MFA та єдиний вхід через браузер,
  хмарні ідентичності, клієнтські сертифікати й TLS. Нові методи з'являються разом з оновленням драйвера,
  а не після очікування випуску digna.
- **Драйвери, які підтримують виробники баз даних** — власний драйвер виробника стежить за новими версіями
  сервера та виправленнями безпеки, і ви можете оновлювати його за власним графіком, незалежно від digna.
- **Єдиний спосіб налаштувати все** — кожна технологія — це список властивостей «ключ/значення» з
  тим самим інтерфейсом, тим самим шифруванням конфіденційних значень і тим самим усуненням несправностей,
  замість різного набору полів для кожного джерела.
- **Тонке налаштування та охоплення** — параметри рівня драйвера, такі як тайм-аути, налаштування TLS, проксі та
  розміри вибірки, доступні для кожного джерела, а підключити можна будь-яку технологію із сумісним драйвером ODBC,
  зокрема ті, для яких digna не публікує окремого посібника.

На практиці це означає, що перемикача **Use ODBC** та окремих полів хоста, порту, бази даних, користувача й
пароля більше немає. **Кожне підключення, яке ще не використовує ODBC, має бути
переведене на ODBC** — автоматичного перетворення немає, тож сплануйте це до оновлення:

1. Перегляньте кожне підключення до бази даних, визначене у вашому встановленні, і складіть список тих, що ще
   не використовують ODBC — кожне з них доведеться налаштувати заново.
2. Встановіть відповідний драйвер ODBC на хості digna — підключення відкриваються із сервера,
   на якому працює серверна частина digna, а не з браузера. Див.
   [Встановлення драйвера ODBC на хості digna](../../../databases/overview.md#install-the-driver).
3. Підготуйте властивості ODBC для кожного зачепленого підключення.
   [Посібники за технологіями](../../../databases/overview.md#technology-guides) наводять для кожного джерела
   перевірений набір властивостей.

Після оновлення переведіть кожне зачеплене підключення на ODBC і перевірте його з панелі —
див. [Створення підключення до бази даних](../../../databases/overview.md#create-a-database-connection)
та [Перевірка підключення](../../../databases/overview.md#testing-a-connection).

!!! warning "Підключення Databricks Legacy"

    Конектор Databricks Legacy вилучено в цьому випуску. Переведіть такі підключення
    на конектор [Databricks](../../../databases/databricks_connector_guide.md).

**Створення резервної копії репозиторію digna обов'язкове**

Перед оновленням digna створіть резервну копію свого репозиторію (PostgreSQL), щоб захиститися від втрати даних.
Резервна копія дає змогу відновитися, якщо під час оновлення виникнуть непередбачені проблеми.

Щоб створити резервну копію з оболонки:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Процес оновлення

#### Крок 1: Зупиніть службу digna

Якщо digna працює як служба systemd, спершу зупиніть її:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Якщо digna працює на передньому плані, натисніть `Ctrl + C` у вікні її термінала.

#### Крок 2: Створіть резервну копію поточного встановлення

У каталозі встановлення digna перейменуйте теки поточного встановлення, щоб новий випуск можна було розгорнути поруч із ними:

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

!!! info "dignabackend і dignacli більше не використовуються"

    Починаючи з Release 2026.06, `dignabackend` і `dignacli` замінено одним виконуваним файлом `digna`, що поєднує серверну частину та CLI. Зберігайте `dignabackend_old` і `dignacli_old` лише доти, доки не перевірите оновлення — після цього обидві теки можна видалити. Зберігайте `dashboard_old`, доки не відновите з неї свої файли конфігурації (див. крок 4).

#### Крок 3: Розпакуйте та розгорніть нову версію

1. Розпакуйте ZIP‑файл нової інсталяції digna
2. Скопіюйте новий виконуваний файл `digna` і теку `dashboard` до свого каталогу встановлення
3. Відновіть біт виконання та належність файлів службовому обліковому запису:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Важливо"

    Ні `config.toml`, ні `dashboard/dashboard_config.toml` ніколи не входять до
    інсталяційного ZIP‑файлу — команда digna ніколи не постачає жодного з цих файлів. Тож оновлення
    не зачіпає вашої наявної конфігурації, а копії в перейменованих теках `*_old` — це
    єдині копії, які у вас є.

#### Крок 4: Відновіть свої файли конфігурації

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

!!! warning "Release 2026.06 змінює config.toml"

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

    У Release 2026.06 масив таблиць замінено окремою таблицею для кожного постачальника, названою за
    ключем постачальника. `DIGNA_OIDC_KEY` більше немає — ключ тепер є частиною заголовка розділу.

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

    Повторіть розділ для кожного постачальника і стежте, щоб кожен ключ збігався з `key` у
    `dashboard_config.toml`. `digna config check` повідомляє про `oidc_clients` як FAILED, доки
    лишається попередня форма. Це стосується лише встановлень, що використовують єдиний вхід.

#### Крок 5: Перезавантажте веб‑сервер

Панель — це набір статичних файлів, тож ваш веб‑сервер — і браузер — можуть досі
віддавати попередню версію. Перезавантажте або перезапустіть веб‑сервер, на якому розміщено теку `dashboard`,
а потім перезавантажте сторінку з примусовим оновленням (++ctrl+f5++).

#### Крок 6: Перевірте конфігурацію

Перш ніж торкатися репозиторію, переконайтеся, що оновлений `config.toml` повний:

```bash
./digna config check
```

Кожен розділ має повідомити OK. Виправте все, про що повідомлено як FAILED, і виконайте команду ще раз, перш ніж продовжувати.

#### Крок 7: Замініть файл ліцензії

Кожен випуск ліцензується окремо. Скопіюйте `license.toml`, який команда digna надала для
цього випуску, до каталогу встановлення, замінивши старий:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Не залишайте попередню ліцензію"

    `license.toml`, виданий для попереднього випуску, не поширюється на цей, і кожна команда,
    що перевіряє ліцензію, — `user`, `inspection`, `repo` — завершується, не торкаючись
    репозиторію, якщо перевірка не пройдена. Перевірте ліцензію, перш ніж продовжувати:

    ```bash
    ./digna license check
    ```

#### Крок 8: Оновіть схему репозиторію

Перейдіть до каталогу встановлення digna і виконайте:

```bash
cd /opt/digna
./digna repo upgrade
```

Це оновлює схему PostgreSQL до найновішої версії, зберігаючи всі наявні дані.

#### Крок 9: Перезапустіть служби

Якщо digna працює як служба systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Якщо сервер запускається вручну, перезапустіть його:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Якщо використовуєте nginx або Apache, перезавантажте відповідний веб‑сервер:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

У сімействі RHEL повторно застосуйте мітки SELinux, якщо каталог `dashboard` було замінено:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Крок 10: Перевірте оновлення

1. Відкрийте панель digna
2. Переконайтеся, що інтерфейс завантажується коректно
3. Перевірте журнали сервера на наявність помилок
4. Переведіть на ODBC кожне підключення, яке його ще не використовувало, а потім перевірте всі підключення
   — див. [Перевірка підключення](../../../databases/overview.md#testing-a-connection):

```bash
sudo journalctl -u digna -n 100
```
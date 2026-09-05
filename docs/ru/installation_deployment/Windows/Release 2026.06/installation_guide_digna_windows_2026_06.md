---
title: Руководство по установке на Windows – digna Release 2026.06 | Документация digna
description: Пошаговое руководство по установке digna Release 2026.06 на Windows — системные требования, настройка PostgreSQL, конфигурация веб-сервера, настройка backend и dashboard, запуск digna как службы Windows и обновление до новой версии.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Руководство по установке на Windows для digna Release 2026.06

**Релиз:** 2026.06

**Последнее обновление:** 30 августа 2026


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

## Введение {: #introduction }

### О digna

digna — это комплексная платформа на базе ИИ, предназначенная для оптимизации управления качеством данных в различных средах хранения данных: хранилищах, Data Lakes и lakehouses. Разработанная с упором на масштабируемость и адаптивность, digna решает современные задачи работы с данными через автоматизацию, мониторинг в реальном времени и обнаружение аномалий.

digna состоит из двух основных компонентов:

- **dignabackend**: основной движок приложения, отвечающий за обработку данных и выполнение проверок качества.
- **dignadashboard**: веб-интерфейс, размещаемый на веб-сервере, предоставляющий удобный способ взаимодействия с платформой digna и визуализации метрик качества данных.

### Что нового в релизе 2026.06

В этом релизе возможности наблюдаемости данных (data observability) интегрированы прямо в ваш код, позволяя разработчикам отслеживать качество данных у источника. Полный список изменений см. в [release notes](http://docs.digna.ai/changelog/Release_202606/).

---

## Системные требования {: #system-requirements }

Перед началом установки убедитесь, что ваша система соответствует следующим минимальным требованиям:

| Требование | Спецификация |
|---|---|
| **Операционная система** | Windows Server или Windows 10/11 |
| **Память (минимальная конфигурация)** | 16 ГБ ОЗУ |
| **Место на диске** | 10 ГБ свободного места |
| **База данных** | PostgreSQL Server 12 или выше |
| **Веб-сервер** | IIS, Apache Tomcat или эквивалент |

### Варианты установки базы данных

**Если PostgreSQL уже установлен:**
Вы можете добавить новую базу данных для digna в существующий сервер PostgreSQL.

**Если вы устанавливаете PostgreSQL на ту же машину, что и digna:**

!!! info "Рекомендуемые характеристики"

    - **Память**: 32 ГБ ОЗУ (вместо 16 ГБ)
    - **Место на диске**: 50 ГБ свободного места (вместо 10 ГБ)

    Эти повышенные характеристики рассчитаны на одновременную работу digna и PostgreSQL.

---

## Предварительная настройка {: #pre-installation-setup }

Перед установкой digna убедитесь, что выполнены два ключевых требования:

1. **PostgreSQL Server** — для хранения вычисленных метрик и данных о производительности
2. **Веб-сервер** — для размещения digna Dashboard

Если эти компоненты не настроены, следуйте разделам ниже для их установки и конфигурации.

---

## Настройка PostgreSQL Server {: #postgresql-server-setup }

### Если PostgreSQL уже установлен

Если PostgreSQL уже установлен и запущен на локальной машине или вы используете управляемый удалённый PostgreSQL, вы можете перейти к следующему разделу — [Web Server Configuration](#web-server-configuration).

### Установка PostgreSQL

Выполните следующие шаги для установки PostgreSQL на Windows:

#### Шаг 1: Загрузка PostgreSQL

1. Перейдите на страницу загрузок [PostgreSQL Downloads](https://www.postgresql.org/download/)
2. Выберите **Windows**
3. Скачайте последний установщик

#### Шаг 2: Запуск установщика

1. Дважды щёлкните загруженный файл установщика
2. Следуйте подсказкам мастера установки

#### Шаг 3: Выбор каталога установки

Выберите директорию для установки PostgreSQL. Обычно рекомендуется оставить значение по умолчанию.

#### Шаг 4: Выбор компонентов

Для стандартной установки оставьте выбранными компоненты по умолчанию.

#### Шаг 5: Установка пароля суперпользователя PostgreSQL

Введите и подтвердите пароль для суперпользователя PostgreSQL (`postgres`). **Сохраните этот пароль в надёжном месте** — он понадобится позже.

#### Шаг 6: Настройка номера порта

По умолчанию PostgreSQL использует порт `5432`. Вы можете оставить этот порт или указать другой при необходимости.

!!! tip "Совет"

    Если порт 5432 уже занят, выберите альтернативный порт и запомните его для последующей настройки.

#### Шаг 7: Выбор локали

Выберите локаль для вашей базы данных. Значение по умолчанию подходит для большинства установок.

#### Шаг 8: Завершение установки

Нажмите **Далее** на оставшихся шагах мастера, затем нажмите **Готово**.

#### Шаг 9: Проверка установки

Откройте Command Prompt и проверьте установку PostgreSQL:

```bash
psql --version
```

Если установка прошла успешно, вы увидите версию PostgreSQL.

---

## Конфигурация веб-сервера {: #web-server-configuration }

digna требует веб-сервер для размещения dashboard. Выберите один из следующих вариантов:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Достаточно установить и настроить **один** из этих серверов.

### Настройка IIS {: #iis-setup }

#### Обзор

Internet Information Services (IIS) — веб-сервер Microsoft для размещения сайтов и веб-приложений.

#### Включение IIS

1. **Откройте Панель управления**
   - Нажмите `Win + R`
   - Введите `control` и нажмите Enter

2. **Перейдите к функциям Windows**
   - Нажмите **Программы**
   - Выберите **Включение или отключение компонентов Windows**

3. **Включите Internet Information Services**
   - Прокрутите список и найдите **Internet Information Services (IIS)**
   - Установите флажок для включения
   - Нажмите **+**, чтобы развернуть и убедиться, что выбраны следующие подсистемы:
     - **Web Management Tools**
     - **World Wide Web Services**

4. Нажмите **ОК**, чтобы применить изменения

5. **Проверка установки IIS**
   - Откройте браузер
   - Перейдите на `http://localhost`
   - Вы должны увидеть страницу приветствия IIS

#### Обязательно: модуль URL Rewrite

Для IIS требуется компонент URL Rewrite. Скачайте и установите его с [официальной страницы Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Обязательно: MIME-тип для файлов Markdown

Чтобы обеспечить корректную отдачу файлов Markdown (`.md`) через IIS:

1. Откройте **IIS Manager** (нажмите `Win + R`, введите `inetmgr`, нажмите Enter)
2. Перейдите к **Ваш сайт > MIME Types**
3. Нажмите **Add...**
4. Настройте:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Важно"

    Без этой настройки файлы `.md` могут не отображаться корректно.

---

### Настройка Apache Tomcat {: #apache-tomcat-setup }

#### Обзор

Apache Tomcat — это open-source контейнер Java сервлетов и веб-сервер.

#### Установка

1. **Загрузите Apache Tomcat**
   - Перейдите на страницу [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Скачайте ZIP-распространение для Windows

2. **Распакуйте архив**
   - Распакуйте ZIP в директорию на вашей системе
   - Пример: `C:\Program Files\Apache Tomcat`

3. **Проверьте, что Tomcat запущен**
   - Откройте браузер
   - Перейдите на `http://localhost:8080`
   - Вы должны увидеть приветственную страницу Apache Tomcat

!!! tip "Совет"

    Apache Tomcat обычно запускается автоматически после установки. Если этого не произошло, перейдите в папку `bin` и запустите `startup.bat`.

---

## Первоначальная установка {: #initial-installation }

### Шаг 1: Создание репозитория digna

Репозиторий digna хранит все метрики, вычисленные digna. Он служит центральной базой данных для аналитических и данных о производительности.

#### Создайте схему репозитория и пользователя

Откройте ваш клиент PostgreSQL (pgAdmin, psql или аналог) и выполните следующие SQL-команды:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Замените следующие плейсхолдеры:**

- `<digna_repo_schema>` — желаемое имя схемы (например, `dignarepo`)
- `<digna_repo_user>` — желаемое имя пользователя (например, `digna_user`)
- `<digna_repo_password>` — надёжный пароль для этого пользователя

**Пример:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Рекомендация"

    Используйте сильные, сложные пароли для учетных записей базы данных. Избегайте легко угадываемых паролей.

---

### Шаг 2: Распаковка установочного пакета digna

1. Найдите ZIP-файл установщика digna, предоставленный вам
2. Распакуйте его в желаемую директорию установки
3. После распаковки вы увидите следующие элементы:
   - `dashboard/` — веб-интерфейс
   - `digna` — главный исполняемый файл (включает backend и CLI)
   - `config.toml` — файл конфигурации
   - `license.toml` — файл лицензии (скопируйте сюда ваш файл)

### Шаг 3: Установка файла лицензии

!!! warning "Важно"

    Файл лицензии **не** включён в установочный пакет и предоставляется отдельно компанией digna.

1. Найдите файл `license.toml`, предоставленный вам
2. Скопируйте его в корневую директорию установки digna (где находятся `config.toml` и исполняемый файл `digna`)

**Почему это важно:**
Файл лицензии содержит информацию о клиенте, дате окончания лицензии и цифровую подпись. **Не изменяйте этот файл** — любые изменения сделают его недействительным.

**Структура директорий после настройки:**

```
digna_installation/
├── config.toml         (файл конфигурации)
├── license.toml        (ВАШ ФАЙЛ ЛИЦЕНЗИИ - скопируйте сюда)
├── digna               (главный исполняемый файл)
└── dashboard/          (веб-интерфейс)
    └── (файлы dashboard)
```

---

## Конфигурация backend {: #backend-configuration }

### Шаг 1: Создание и редактирование файла конфигурации

Файл `config_template.toml` поставляется в директории установки digna. Вам нужно лишь переименовать его в `config.toml`.

**Расположение:** `digna_installation/config.toml`

Откройте `config.toml` в текстовом редакторе и настройте каждый раздел, указанный ниже.

#### Раздел [app]

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

| Параметр | Значение | Примечания |
|---|---|---|
| `digna_APP_HOST` | `localhost` или IP-адрес | Хост или IP, где размещён dignabackend |
| `digna_APP_PORT` | `8082` (по умолчанию) | Порт для REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL фронтенда | Если dashboard на другом сервере, укажите его URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Нужно при CORS с учётными данными |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Разрешить все HTTP-методы |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Разрешить все заголовки |

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
| `digna_REPO_HOST` | `localhost` или IP | Хост/IP сервера PostgreSQL |
| `digna_REPO_PORT` | `5432` (по умолчанию) | Порт PostgreSQL |
| `digna_REPO_DB` | `postgres` | Имя базы данных |
| `digna_REPO_SCHEMA` | `dignarepo` | Ранее созданная схема |
| `digna_REPO_USER` | `digna_user` | Пользователь, созданный при настройке PostgreSQL |
| `digna_REPO_PASSWORD` | Ваш пароль | Пароль, заданный при создании пользователя |

#### Раздел [base]

Этот раздел содержит настройки безопасности и cookie:

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

| Параметр | Значение | Примечания |
|---|---|---|
| `digna_FERNET_KEY` | Ключ шифрования | Используется для шифрования токенов и cookie (предоставлен по умолчанию) |
| `digna_COOKIE_DOMAIN` | `localhost` | Соответствует домену фронтенда |
| `digna_COOKIE_SECURE` | `false` (локально) / `true` (в продакшн) | Используйте `true` для HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Всегда включено для безопасности |
| `digna_COOKIE_SAME_SITE` | `lax` | Предотвращает CSRF-атаки |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 часа) | Время действия сессии в секундах |
| `digna_MAX_WORKERS` | Число ядер CPU - 1 | Количество параллельных задач инспекции |

#### Раздел [logging]

Этот раздел настраивает поведение логирования:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Параметр | Значение | Примечания |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` или `DEBUG` | `INFO` для продакшна, `DEBUG` для отладки |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Количество ежедневных резервных логов для хранения |

---

### Шаг 3: Инициализация репозитория

1. Откройте Command Prompt
2. Перейдите в директорию установки digna (где находятся `config.toml` и исполняемый файл `digna`)
3. Запустите проверку подключения:

```bash
digna repo check
```

Вы должны увидеть подтверждение установления соединения (сам репозиторий ещё не инициализирован).

### Шаг 4: Установка схемы репозитория

В той же директории выполните:

```bash
digna repo install
```

Эта команда создаёт необходимые таблицы и схему в вашей базе PostgreSQL.

### Шаг 5: Запуск сервера digna

В директории установки digna запустите сервер:

```bash
digna serve --address <host> --port <port>
```

**Параметры:**
- `--address` — имя хоста/IP сервера
- `--port` — порт сервера

Вы увидите стартовые сообщения, подтверждающие запуск сервера:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Шаг 6: Создание администратора

1. Откройте **новое** окно Command Prompt
2. Перейдите в директорию установки digna
3. Выполните команду для создания администратора:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Пример:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Эта команда создаёт пользователя с полными административными правами.

!!! tip "Рекомендация"

    Используйте надёжный пароль, содержащий заглавные и строчные буквы, цифры и специальные символы.

---

## Конфигурация Dashboard {: #dashboard-configuration }

### Шаг 1: Развёртывание Dashboard на веб-сервере

У dashboard есть собственный файл `config.toml`, расположенный в каталоге `dashboard/`. Этот файл уже предоставлен и не требует изменений при первоначальной настройке. Изменять его нужно только в случае кастомизации подключений к backend или при мультиинстансной конфигурации.

Если требуется изменить конфигурацию dashboard (например, для многосерверных развёртываний), обратитесь к документации dashboard.

Выберите веб-сервер и выполните соответствующие действия по развёртыванию.

#### Развёртывание в IIS

1. **Откройте IIS Manager**
   - Нажмите `Win + R`, введите `inetmgr`, нажмите Enter

2. **Создайте новый сайт**
   - В левой панели правой кнопкой мыши кликните **Sites**
   - Выберите **Add Website...**

3. **Настройте сайт**
   - **Site Name**: Введите имя (например, "dignaDashboard")
   - **Physical Path**: Нажмите Browse и выберите папку `dashboard`
   - **Binding**: Установите IP-адрес и порт (порт по умолчанию 80 для HTTP, 443 для HTTPS)

4. **Запустите сайт**
   - Нажмите **ОК** для создания сайта
   - Правой кнопкой мыши кликните по новому сайту и выберите **Start**

5. **Проверьте установку**
   - Откройте браузер
   - Перейдите на `http://localhost` (или на ваш настроенный URL)
   - Вы должны увидеть страницу входа в digna dashboard

#### Развёртывание в Apache Tomcat

1. **Скопируйте dashboard в Tomcat**
   - Скопируйте папку `dashboard` в директорию `webapps` Tomcat
   - При необходимости переименуйте (например, в `digna`)
   - Пример: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Проверьте развёртывание**
   - Обновите страницу администратора Tomcat (http://localhost:8080)
   - Вы должны увидеть приложение "digna" (или выбранное вами имя) в списке развернутых приложений

3. **Доступ к Dashboard**
   - Откройте браузер
   - Перейдите на `http://localhost:8080/digna`
   - Вы должны увидеть страницу входа в digna dashboard

---

## Запуск digna как службы Windows {: #running-digna-as-a-windows-service }

### Зачем использовать службу Windows?

Запуск digna backend как службы Windows обеспечивает:
- Автоматический старт при загрузке сервера
- Работа в фоне без открытого окна Command Prompt
- Автоматический перезапуск в случае аварийного завершения
- Управление через стандартные средства Windows Services

### Файлы управления службой

Все необходимые файлы находятся в директории установки digna в папке: `bin/`

Доступные батники:
- `install_service.bat` — регистрирует digna как службу Windows
- `uninstall_service.bat` — удаляет регистрацию службы
- `start_service.bat` — запускает службу
- `stop_service.bat` — останавливает службу

!!! warning "Требуются права администратора"

    Все батники должны выполняться с правами администратора.

### Установка службы

1. **Откройте Command Prompt от имени администратора**
   - Правый клик по Command Prompt
   - Выберите "Запуск от имени администратора"

2. **Перейдите в папку bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Запустите скрипт установки**
   ```bash
   install_service.bat
   ```

Сервис digna зарегистрирован как служба Windows с включённым автоматическим запуском. Сразу после установки служба не стартует — см. следующий раздел о запуске.

### Запуск и остановка службы

#### Для запуска службы

1. Откройте Command Prompt от имени администратора
2. Перейдите в `digna\bin`
3. Выполните:
   ```bash
   start_service.bat
   ```

#### Для остановки службы

1. Откройте Command Prompt от имени администратора
2. Перейдите в `digna\bin`
3. Выполните:
   ```bash
   stop_service.bat
   ```

!!! tip "Совет"

    Всегда останавливайте службу перед обновлением файлов приложения.

### Перенос службы в новый каталог

Если необходимо переместить установку digna:

1. **Удалите текущую службу**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Переместите файлы приложения**
   - Перенесите всю папку установки digna в новое место

3. **Переустановите службу**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Запустите службу**
   ```bash
   start_service.bat
   ```

### Удаление службы

1. **Остановите работающую службу**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Удалите регистрацию службы**
   ```bash
   uninstall_service.bat
   ```

Служба digna будет удалена из реестра служб Windows.

---

## Обновление до новой версии {: #upgrading-to-a-new-release }

### Перед обновлением

**Обязательно создайте резервную копию репозитория digna**

Перед обновлением digna обязательно сделайте бэкап репозитория (PostgreSQL), чтобы защитить данные от потери. Резервная копия позволит восстановиться в случае проблем при обновлении.

### Процесс обновления

#### Шаг 1: Остановите службу digna

Если digna запущен как служба Windows, остановите её:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Шаг 2: Резервное копирование текущей установки backend

В директории установки digna выполните:

```bash
# Переименовать папку с dignabackend
ren dignabackend dignabackend_old
```
```bash
# Переименовать dashboard
ren dashboard dashboard_old
```

#### Шаг 3: Распакуйте и разверните новую версию

1. Распакуйте новый ZIP-файл digna
2. Скопируйте новый исполняемый файл `digna` и папку `dashboard` в директорию установки

!!! warning "Важно"

    Файл `config.toml` **никогда** не включается в ZIP-архив установки. Ваша существующая конфигурация сохраняется.

### Шаг 4: Восстановите файлы конфигурации

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

### Шаг 5: Обновление схемы репозитория

Перейдите в директорию установки digna и выполните:

```bash
digna repo upgrade
```

Это обновит схему PostgreSQL до последней версии, сохранив все существующие данные.

### Шаг 6: Перезапуск сервисов

Если вы используете службу Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Если запуск производится вручную, перезапустите сервер:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Если вы используете IIS или Tomcat — перезапустите соответствующий веб-сервер.

#### Шаг 7: Проверка обновления

1. Откройте digna dashboard
2. Убедитесь, что интерфейс загружается корректно
3. Проверьте журналы сервера на наличие ошибок
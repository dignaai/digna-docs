# Обзор единого входа (SSO)

---

## Содержание

1. [Введение и обзор](#introduction-and-overview)
2. [Руководства по провайдерам](#provider-guides)
3. [Шаги конфигурации](#configuration-steps)
4. [Настройка панели (Dashboard)](#dashboard-configuration)
5. [Настройка бэкенда](#backend-configuration)
6. [Тестирование входа](#testing-login)
7. [Устранение неполадок](#troubleshooting)
8. [Поддерживаемые провайдеры](#supported-providers)

---

## Введение и обзор {: #introduction-and-overview }

Это руководство содержит пошаговые инструкции по интеграции единого входа (SSO) в платформу digna с использованием **OpenID Connect (OIDC)**.

### Что такое SSO?

Единый вход (SSO) позволяет пользователям безопасно входить в digna, используя корпоративные учетные данные через внешних провайдеров идентификации. Пользователям не нужно создавать отдельные пароли для digna — они аутентифицируются с помощью корпоративных учетных данных.

### Как это работает

SSO в digna реализован с помощью протокола OIDC. Несколько провайдеров идентификации могут быть настроены параллельно путем изменения двух ключевых конфигурационных файлов:

- **`dashboard_config.toml`** — управляет интерфейсом входа на frontend
- **`config.toml`** — настраивает OIDC-подключения на бэкенде

### Поддерживаемые провайдеры {: #supported-providers-overview }

В примерах этого руководства используются **Microsoft** и **Google**, но **любой провайдер, совместимый с OIDC**, может быть интегрирован по той же схеме.

---

## Руководства по провайдерам {: #provider-guides }

Каждому провайдеру нужны одни и те же четыре значения — client ID, client secret, redirect URI и discovery URL — но в консоли администратора у каждого провайдера они находятся в разных местах, и у некоторых есть шаги, специфичные для этого провайдера. Руководства ниже покрывают эту часть работы; эта страница описывает сторону digna, которая одинакова для всех провайдеров.

| Provider | Guide | Worth knowing |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | Self-hosted; the only provider here where you control the token service |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | Discovery URL is per-tenant, and custom domains change it |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | Consent screen must be published before non-test users can log in |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | Self-hosted; discovery URL is per-realm |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID appears in the discovery URL; secrets expire |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | Authorization server choice changes the discovery URL |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | The OIDC app type must be chosen at creation and cannot be changed |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | Environment ID appears in the discovery URL |

Любой другой провайдер, совместимый с OIDC, работает аналогично — см. [Other OIDC Providers](#supported-providers).

---

## Шаги конфигурации {: #configuration-steps }

Для настройки SSO требуется внести изменения в два файла. В этом разделе объясняется, как настроить каждый из них.

### Обзор конфигурационных файлов

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend login interface |
| **config.toml** | `/config.toml` | Backend OIDC connections |

Оба файла должны быть настроены, чтобы SSO работал корректно.

---

## Настройка панели (Dashboard) {: #dashboard-configuration }

### Расположение файла

```
dashboard/dashboard_config.toml
```

### Шаг 1: Добавьте провайдеров OIDC

Добавьте записи в массив `[[login.oidc]]` для каждого провайдера идентификации, который вы хотите поддерживать.

**Пример с Microsoft и Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Шаг 2: Настройте параметры входа

Укажите, следует ли разрешать вход по паролю:

```toml
[login]
usePassword = true
```

### Параметры конфигурации

#### `[[login.oidc]]` секция

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Уникальный идентификатор для OIDC-подключения (должен соответствовать key в config.toml) |
| `label` | string | Yes | Текст, отображаемый на кнопке входа (например, "Login with Microsoft") |

#### `[login]` секция

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Разрешить вход по паролю в дополнение к SSO |

### Понимание usePassword

**Если `usePassword = true`:**
- На экране входа отображаются кнопки SSO (например, "Login with Microsoft")
- Также отображаются поля для имени пользователя и пароля
- Пользователи могут аутентифицироваться любым из методов
- Поддерживает гибридные сценарии, когда некоторые пользователи используют SSO, а другие — пароли

**Если `usePassword = false` (или параметр опущен):**
- На экране входа отображаются только кнопки SSO
- Поля для имени пользователя и пароля отсутствуют
- Доступна только аутентификация через OIDC

!!! tip "Совет"

    Вход по паролю доступен только для пользователей, созданных с паролями командой `digna user add` или через панель управления.

### Полный пример

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Настройка бэкенда {: #backend-configuration }

### Расположение файла

```
/config.toml
```

(Корневая директория установки digna)

### Шаг 1: Добавьте секции для провайдеров OIDC

Для каждого провайдера должна быть выделенная секция `[oidc.<key>]`. Ключ должен совпадать с `key`, указанным в `dashboard_config.toml`.

### Конфигурация Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Конфигурация Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Параметры конфигурации

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID от провайдера идентификации | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret от провайдера идентификации | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | URL обратного вызова после аутентификации | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | Конечная точка конфигурации OIDC | `https://login.microsoftonline.com/...` |

!!! warning "Важно"

    Замените заполнители (`<client_id>`, `<client_secret>`, `<tenant_id>`) на реальные учетные данные из портала разработчика вашего провайдера идентификации.

### Redirect URI

Redirect URI должен совпадать с тем, что зарегистрирован у провайдера идентификации:

```
http://localhost:5173/oidc/callback
```

Если digna размещена на другом домене, обновите URI соответствующим образом:
- Локально: `http://localhost:5173/oidc/callback`
- В продакшене: `https://digna.yourdomain.com/oidc/callback`

### Полный пример

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Тестирование входа {: #testing-login }

После завершения настройки проверьте, что SSO работает корректно.

### Контрольный список перед тестированием

Перед тестированием убедитесь, что:

- [ ] `dashboard_config.toml` обновлен с провайдерами OIDC
- [ ] `config.toml` обновлен с учетными данными OIDC
- [ ] Оба файла сохранены
- [ ] Учетные данные верны (client ID, client secret)
- [ ] Redirect URI соответствует URL вашей установки
- [ ] Приложение у провайдера идентификации настроено с этим redirect URI

### Шаги тестирования

#### Шаг 1: Перезапустите сервисы

Перезапустите бэкенд digna и веб-сервер, чтобы применить изменения.

**Если запущено как служба в Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Если запущено как служба в Linux или macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Если запускаете вручную:**
```bash
digna serve --address localhost --port 8082
```

**Также перезапустите веб-сервер** — IIS или Tomcat на Windows, nginx или Apache на Linux и macOS.

#### Шаг 2: Откройте панель управления

Откройте панель digna в браузере:

```
http://localhost:5173
```

(или ваш настроенный URL панели)

#### Шаг 3: Проверьте кнопки входа

Убедитесь, что кнопки входа отображаются для каждого настроенного провайдера:

- Должна быть кнопка "Login with Microsoft"
- Должна быть кнопка "Login with Google"
- (Если usePassword = true) Должны отображаться поля для имени пользователя/пароля

Если кнопки не отображаются:
- Проверьте, что `dashboard_config.toml` сохранен
- Проверьте, что служба панели была перезапущена
- Проверьте консоль браузера (F12) на наличие ошибок

#### Шаг 4: Протестируйте вход через SSO

Нажмите одну из кнопок SSO (например, "Login with Microsoft"):

1. Вы должны быть перенаправлены на страницу входа провайдера идентификации
2. Выполните вход с корпоративными учетными данными
3. Вы должны быть перенаправлены обратно в digna
4. Вы должны оказаться в системе под своей учетной записью

#### Шаг 5: Проверьте создание пользователя

После успешного входа через SSO:

- Пользователь должен быть автоматически создан в digna
- Пользователь должен быть вошел в систему
- Профиль пользователя должен отображать данные провайдера идентификации
- Вы должны увидеть панель digna

#### Шаг 6: Протестируйте вход по паролю (если включен)

Если `usePassword = true`:

1. Выйдите из digna
2. На экране входа введите имя пользователя и пароль
3. Вы должны иметь возможность войти с помощью пароля

---

## Устранение неполадок {: #troubleshooting }

### Кнопки входа не отображаются

**Симптомы:**
- Кнопки входа OIDC не видны на странице входа
- Видны только поля пароля (если usePassword = true)

**Причины и решения:**
1. Проверьте, что `dashboard_config.toml` находится в каталоге `dashboard/`
2. Убедитесь, что секции `[[login.oidc]]` присутствуют и синтаксис корректен
3. Перезапустите службу панели
4. Очистите кэш браузера (Ctrl+Shift+Delete или Cmd+Shift+Delete)
5. Проверьте консоль браузера (F12 → Console) на наличие ошибок

---

### Ошибка несоответствия Redirect URI

**Симптомы:**
- После нажатия кнопки SSO возникает ошибка "redirect_uri mismatch"
- Ошибка "The redirect URI is not registered"

**Причины и решения:**
1. Проверьте значение `DIGNA_OIDC_REDIRECT_URI` в `config.toml`
2. Убедитесь, что redirect URI зарегистрирован в настройках провайдера идентификации
3. Убедитесь, что URLы полностью идентичны (включая протокол, домен, путь)
4. Проверьте опечатки в redirect URI
5. Если используется HTTPS, проверьте валидность сертификата

---

### Ошибка неверных учетных данных клиента

**Симптомы:**
- Ошибка "Invalid client ID or secret"
- Аутентификация не проходит из-за ошибки с учетными данными

**Причины и решения:**
1. Проверьте `DIGNA_OIDC_CLIENT_ID` и `DIGNA_OIDC_CLIENT_SECRET`
2. Убедитесь, что нет лишних пробелов или спецсимволов
3. Проверьте, не истекли ли учетные данные и не были ли они отозваны
4. Перезапустите бэкенд после обновления конфигурации
5. Проверьте консоль провайдера идентификации, чтобы убедиться, что учетные данные активны

---

### Вход зависает или истекает время ожидания

**Симптомы:**
- Ничего не происходит после нажатия кнопки SSO
- Таймаут через несколько секунд
- Браузер показывает "Failed to connect" или похожее

**Причины и решения:**
1. Убедитесь, что бэкенд digna запущен: `digna repo check`
2. Проверьте сетевое соединение с провайдером идентификации
3. Убедитесь, что `DIGNA_OIDC_CONFIGURATION_URL` доступен
4. Проверьте правила брандмауэра, разрешающие исходящие HTTPS-соединения
5. Убедитесь, что бэкенд и панель могут взаимодействовать между собой

---

### Пользователи не создаются автоматически

**Симптомы:**
- Вход через SSO успешен, но пользователь не создается в digna
- Возникает ошибка прав доступа после входа через SSO

**Причины и решения:**
1. Проверьте корректность OIDC-конфигурации
2. Убедитесь, что права пользователя настроены правильно
3. Просмотрите логи digna на предмет сообщений об ошибках
4. Перезапустите бэкенд
5. Обратитесь в support@digna.ai, если проблема сохраняется

---

## Поддерживаемые провайдеры {: #supported-providers }

### Протестировано и поддерживается

Следующие провайдеры OIDC были протестированы и известны как рабочие:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### Другие провайдеры OIDC

Любой провайдер, поддерживающий OpenID Connect, может быть интегрирован. Необходимая информация:

- Client ID
- Client secret
- OpenID configuration URL (обычно по адресу `/.well-known/openid-configuration`)
- Поддерживаемые scope'ы (обычно `openid profile email`)

Обратитесь в support@digna.ai, если вам нужна помощь с интеграцией конкретного провайдера.

---

## Рекомендуемые практики

**ДЕЛАЙТЕ:**
- Используйте HTTPS в продакшене (не HTTP)
- Храните client secret безопасно (по возможности используйте переменные окружения)
- Регулярно меняйте секреты
- Тестируйте в непроизводственной среде в первую очередь
- Документируйте, какие провайдеры настроены
- Отслеживайте логи входов на предмет подозрительной активности
- Синхронизируйте настройки провайдера идентификации с конфигурацией digna

**НЕ ДЕЛАЙТЕ:**
- Не храните client secret в системе контроля версий
- Не используйте HTTP redirect URI в продакшене
- Не настраивайте несколько провайдеров с одним и тем же key
- Не оставляйте тестовые/дефолтные учетные данные в продакшене
- Не раскрывайте файлы конфигурации, содержащие секреты
- Не смешивайте учетные данные разработки и продакшена

---

## Поддержка

Нужна помощь с настройкой SSO?

- **Email:** support@digna.ai
- **Документация:** https://docs.digna.ai
- **Веб-сайт:** https://www.digna.ai

---

**Последнее обновление:** 30 августа 2026  
**Релиз:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
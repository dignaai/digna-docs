---
title: Руководство по интеграции Single Sign-On (SSO) | документация digna
description: Пошаговое руководство по настройке Single Sign-On (SSO) для digna с использованием OpenID Connect (OIDC). Охватывает конфигурацию dashboard и backend, тестирование, устранение неполадок и поддерживаемые провайдеры удостоверений, включая Microsoft Entra ID, Google Workspace и Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - единый вход
  - oidc интеграция
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integration
  - корпоративная аутентификация
lang: en
robots: index, follow
og_title: digna Руководство по интеграции Single Sign-On (SSO)
og_description: Настройка Single Sign-On для digna с использованием OpenID Connect. Пошаговая настройка для Microsoft Entra ID, Google Workspace, Okta и других провайдеров, совместимых с OIDC.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Руководство по интеграции Single Sign-On

---

## Содержание

1. [Введение и обзор](#introduction-and-overview)
2. [Шаги настройки](#configuration-steps)
3. [Конфигурация Dashboard](#dashboard-configuration)
4. [Конфигурация Backend](#backend-configuration)
5. [Тестирование входа](#testing-login)
6. [Устранение неполадок](#troubleshooting)
7. [Поддерживаемые провайдеры](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

Это руководство содержит пошаговые инструкции по интеграции Single Sign-On (SSO) с платформой digna с использованием **OpenID Connect (OIDC)**.

### Что такое SSO?

Single Sign-On позволяет пользователям безопасно входить в digna, используя корпоративные учётные данные через внешних провайдеров удостоверений. Пользователи могут аутентифицироваться корпоративными учётными данными вместо того, чтобы управлять отдельными паролями для digna.

### Как это работает

SSO в digna реализован с использованием протокола OIDC. Можно настроить несколько провайдеров удостоверений параллельно, изменив два ключевых конфигурационных файла:

- **`dashboard_config.toml`** — управляет интерфейсом входа на frontend
- **`config.toml`** — настраивает OIDC-подключения на backend

### Поддерживаемые провайдеры {: #supported-providers-overview }

Примеры в этом руководстве используют **Microsoft** и **Google**, но **любой провайдер, совместимый с OIDC**, можно интегрировать по той же схеме.

Распространённые OIDC-провайдеры:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Другие провайдеры удостоверений, совместимые с OIDC

---

## Configuration Steps {: #configuration-steps }

Настройка SSO требует обновления двух файлов. В этом разделе объясняется, как настроить каждый из них.

### Обзор конфигурационных файлов

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Интерфейс входа на frontend |
| **config.toml** | `/config.toml` | OIDC-подключения на backend |

Оба файла должны быть настроены для корректной работы SSO.

---

## Dashboard Configuration {: #dashboard-configuration }

### Местоположение файла

```
dashboard/dashboard_config.toml
```

### Шаг 1: Добавьте провайдеров OIDC

Добавьте записи в массив `[[login.oidc]]` для каждого провайдера удостоверений, которого вы хотите поддерживать.

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

Укажите, разрешён ли вход по паролю:

```toml
[login]
usePassword = true
```

### Параметры конфигурации

#### `[[login.oidc]]` Раздел

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Уникальный идентификатор для OIDC-подключения (должен совпадать с ключом в config.toml) |
| `label` | string | Yes | Текст, отображаемый на кнопке входа (например, "Login with Microsoft") |

#### `[login]` Раздел

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Разрешить вход по паролю в дополнение к SSO |

### Понимание usePassword

**Если `usePassword = true`:**
- На экране входа отображаются кнопки SSO (например, "Login with Microsoft")
- Также отображаются поля для имени пользователя и пароля
- Пользователи могут аутентифицироваться любым из методов
- Поддерживает гибридные настройки, когда часть пользователей использует SSO, а часть — пароли

**Если `usePassword = false` (или опция отсутствует):**
- На экране входа отображаются только кнопки SSO
- Поля для имени пользователя/пароля отсутствуют
- Доступна только OIDC-аутентификация

> **💡 Совет**
>
> Вход по паролю доступен только для пользователей, созданных с паролями с помощью команды `digna user add` или через dashboard.

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

## Backend Configuration {: #backend-configuration }

### Местоположение файла

```
/config.toml
```

(Корневая директория установки digna)

### Шаг 1: Добавьте секции для провайдеров OIDC

Для каждого провайдера должна быть выделенная секция `[oidc.<key>]`. Значение ключа должно совпадать с `key`, указанным в `dashboard_config.toml`.

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
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID от провайдера удостоверений | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret от провайдера удостоверений | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | URL обратного вызова после аутентификации | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | Точка конфигурации OIDC | `https://login.microsoftonline.com/...` |

> **⚠️ Важно**
>
> Замените значения-заполнители (`<client_id>`, `<client_secret>`, `<tenant_id>`) реальными учётными данными из портала разработчика вашего провайдера удостоверений.

### Redirect URI

Redirect URI должен совпадать с тем, что настроено у провайдера удостоверений:

```
http://localhost:5173/oidc/callback
```

Если digna размещён на другом домене, обновите значение соответственно:
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

## Testing Login {: #testing-login }

После завершения настройки убедитесь, что SSO работает корректно.

### Контрольный список перед тестированием

Перед тестированием убедитесь, что:

- [ ] `dashboard_config.toml` обновлён с провайдерами OIDC
- [ ] `config.toml` обновлён с OIDC-учётными данными
- [ ] Оба файла сохранены
- [ ] Учётные данные правильные (client ID, client secret)
- [ ] Redirect URI совпадает с URL вашего развертывания
- [ ] Приложение у провайдера удостоверений настроено с этим Redirect URI

### Шаги тестирования

#### Шаг 1: Перезапустите сервисы

Перезапустите backend и веб-сервер digna, чтобы применить изменения.

**Если работаете как служба Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Если запускаете вручную:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Если используете IIS или Tomcat:**
Перезапустите соответствующий веб-сервер.

#### Шаг 2: Откройте Dashboard

Откройте dashboard digna в браузере:

```
http://localhost:5173
```

(или ваш настроенный URL dashboard)

#### Шаг 3: Проверьте кнопки входа

Убедитесь, что для каждого настроенного провайдера отображается соответствующая кнопка входа:

- ✅ Должна отображаться кнопка "Login with Microsoft"
- ✅ Должна отображаться кнопка "Login with Google"
- ✅ (Если usePassword = true) Должны отображаться поля для имени пользователя/пароля

Если кнопок нет:
- Проверьте, что `dashboard_config.toml` сохранён
- Проверьте, что сервис dashboard был перезапущен
- Проверьте консоль браузера (F12) на наличие ошибок

#### Шаг 4: Протестируйте SSO-вход

Нажмите одну из SSO-кнопок (например, "Login with Microsoft"):

1. Вы должны быть перенаправлены на страницу входа провайдера удостоверений
2. Войдите с корпоративными учётными данными
3. Вы должны быть перенаправлены обратно в digna
4. Вы должны быть авторизованы в digna

#### Шаг 5: Проверьте создание пользователя

После успешного SSO-входа:

- ✅ Пользователь должен быть автоматически создан в digna
- ✅ Пользователь должен быть авторизован
- ✅ Профиль пользователя должен содержать данные провайдера удостоверений
- ✅ Вы должны увидеть dashboard digna

#### Шаг 6: Протестируйте вход по паролю (если включён)

Если `usePassword = true`:

1. Выйдите из digna
2. На странице входа введите имя пользователя и пароль
3. Вы должны иметь возможность войти с учётными данными по паролю

---

## Troubleshooting {: #troubleshooting }

### Кнопки входа не отображаются

**Симптомы:**
- Кнопки OIDC для входа не видны на странице входа
- Видны только поля пароля (если usePassword = true)

**Причины и решения:**
1. Проверьте, что `dashboard_config.toml` находится в каталоге `dashboard/`
2. Убедитесь, что секции `[[login.oidc]]` присутствуют и синтаксис верен
3. Перезапустите сервис dashboard
4. Очистите кэш браузера (Ctrl+Shift+Delete или Cmd+Shift+Delete)
5. Проверьте консоль браузера (F12 → вкладка Console) на ошибки

---

### Ошибка несоответствия Redirect URI

**Симптомы:**
- После нажатия на кнопку SSO возникает ошибка про "redirect_uri mismatch"
- Ошибка "The redirect URI is not registered"

**Причины и решения:**
1. Проверьте `DIGNA_OIDC_REDIRECT_URI` в `config.toml`
2. Убедитесь, что Redirect URI зарегистрирован в настройках провайдера удостоверений
3. Убедитесь, что URLы идентичны (включая протокол, домен, путь)
4. Проверьте опечатки в Redirect URI
5. Если используется HTTPS, убедитесь, что сертификат действителен

---

### Ошибка недействительных учётных данных клиента

**Симптомы:**
- Ошибка "Invalid client ID or secret"
- Аутентификация завершается с ошибкой учётных данных

**Причины и решения:**
1. Проверьте, что `DIGNA_OIDC_CLIENT_ID` и `DIGNA_OIDC_CLIENT_SECRET` корректны
2. Убедитесь, что нет лишних пробелов или специальных символов
3. Проверьте, не истёк ли срок действия учётных данных и не были ли они отозваны
4. Перезапустите backend после обновления конфигурации
5. Проверьте консоль провайдера удостоверений, чтобы подтвердить активность учётных данных

---

### Вход зависает или истекает по времени

**Симптомы:**
- Ничего не происходит после нажатия на кнопку SSO
- Таймаут через несколько секунд
- Браузер показывает "Failed to connect" или похожее

**Причины и решения:**
1. Убедитесь, что backend digna запущен: `digna repo check`
2. Проверьте сетевое соединение с провайдером удостоверений
3. Убедитесь, что `DIGNA_OIDC_CONFIGURATION_URL` доступен
4. Проверьте правила брандмауэра, разрешающие исходящие HTTPS-соединения
5. Убедитесь, что backend и dashboard могут достучаться друг до друга

---

### Пользователи не создаются автоматически

**Симптомы:**
- SSO-вход проходит успешно, но пользователь не создаётся в digna
- После SSO-входа возникает ошибка прав доступа

**Причины и решения:**
1. Проверьте корректность OIDC-конфигурации
2. Убедитесь, что права пользователей настроены правильно
3. Просмотрите логи digna на предмет сообщений об ошибках
4. Перезапустите backend
5. Обратитесь в поддержку по адресу support@digna.ai, если проблема сохраняется

---

## Supported Providers {: #supported-providers }

### Тестированные и поддерживаемые

Следующие OIDC-провайдеры были протестированы и известны как совместимые:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Другие OIDC-провайдеры

Любой провайдер, поддерживающий OpenID Connect, можно интегрировать. Необходимая информация:

- Client ID
- Client secret
- URL конфигурации OpenID (обычно `/.well-known/openid-configuration`)
- Поддерживаемые scope (обычно `openid profile email`)

Свяжитесь с support@digna.ai, если вам нужна помощь с интеграцией конкретного провайдера.

---

## Лучшие практики

✅ **ДЕЛАТЬ:**
- Использовать HTTPS в продакшене (не HTTP)
- Хранить client secrets безопасно (по возможности использовать переменные окружения)
- Периодически ротировать секреты
- Тестировать в непроизводственной среде в первую очередь
- Документировать, какие провайдеры настроены
- Мониторить логи входов на предмет подозрительной активности
- Поддерживать конфигурацию провайдера удостоверений в актуальном состоянии в соответствии с конфигурацией digna

❌ **НЕ ДЕЛАТЬ:**
- Хранить client secrets в системе контроля версий
- Использовать HTTP Redirect URI в продакшене
- Настраивать несколько провайдеров с одинаковым ключом
- Оставлять учетные данные по умолчанию/тестовые в продакшене
- Разглашать файлы конфигурации, содержащие секреты
- Смешивать учётные данные разработки и производства

---

## Поддержка

Нужна помощь с настройкой SSO?

- 📧 **Email:** support@digna.ai
- 📚 **Документация:** https://docs.digna.ai
- 🌐 **Сайт:** https://www.digna.ai

---

**Последнее обновление:** 30 августа 2026  
**Релиз:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
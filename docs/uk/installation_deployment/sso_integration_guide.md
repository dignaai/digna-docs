---
title: Single Sign-On (SSO) Integration Guide | digna Documentation
description: Step-by-step guide to configuring Single Sign-On (SSO) for digna using OpenID Connect (OIDC). Covers dashboard and backend configuration, testing, troubleshooting, and supported identity providers including Microsoft Entra ID, Google Workspace, and Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc integration
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integration
  - enterprise authentication
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integration Guide
og_description: Configure Single Sign-On for digna using OpenID Connect. Step-by-step setup for Microsoft Entra ID, Google Workspace, Okta, and other OIDC-compliant identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Інтеграція Single Sign-On (SSO)

---

## Зміст

1. [Вступ та огляд](#introduction-and-overview)
2. [Кроки конфігурації](#configuration-steps)
3. [Конфігурація Dashboard](#dashboard-configuration)
4. [Конфігурація Backend](#backend-configuration)
5. [Тестування входу](#testing-login)
6. [Усунення несправностей](#troubleshooting)
7. [Підтримувані провайдери](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

Цей посібник містить покрокові інструкції з інтеграції Single Sign-On (SSO) з платформою digna за допомогою **OpenID Connect (OIDC)**.

### Що таке SSO?

Single Sign-On дозволяє користувачам безпечно входити в digna, використовуючи корпоративні облікові дані через зовнішніх постачальників ідентифікації. Користувачі можуть автентифікуватися своїми корпоративними обліковими даними замість окремого пароля для digna.

### Як це працює

SSO у digna реалізовано за допомогою протоколу OIDC. Можна налаштувати кілька постачальників ідентифікації паралельно, відредагувавши два ключові конфігураційні файли:

- **`dashboard_config.toml`** — керує інтерфейсом входу на фронтенді
- **`config.toml`** — конфігурує OIDC-з’єднання на бекенді

### Підтримувані постачальники {: #supported-providers-overview }

Приклади в цьому посібнику показані на основі **Microsoft** та **Google**, але **будь-який постачальник, сумісний з OIDC**, може бути інтегрований за тією самою структурою.

Поширені OIDC-провайдери включають:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Інші постачальники, сумісні з OIDC

---

## Configuration Steps {: #configuration-steps }

Налаштування SSO вимагає змін у двох файлах. У цьому розділі пояснюється, як налаштувати кожен із них.

### Огляд конфігураційних файлів

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend login interface |
| **config.toml** | `/config.toml` | Backend OIDC connections |

Обидва файли повинні бути налаштовані для коректної роботи SSO.

---

## Dashboard Configuration {: #dashboard-configuration }

### Розташування файлу

```
dashboard/dashboard_config.toml
```

### Крок 1: Додайте OIDC-провайдерів

Додайте записи під масивом `[[login.oidc]]` для кожного провайдера ідентифікації, якого хочете підтримувати.

**Приклад для Microsoft та Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Крок 2: Налаштуйте опції входу

Вкажіть, чи дозволяти вхід з паролем:

```toml
[login]
usePassword = true
```

### Параметри конфігурації

#### `[[login.oidc]]` Розділ

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Унікальний ідентифікатор для OIDC-з’єднання (повинен збігатися з key у config.toml) |
| `label` | string | Yes | Текст, що відображається на кнопці входу (наприклад, "Login with Microsoft") |

#### `[login]` Розділ

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Дозволяє вхід із паролем додатково до SSO |

### Розуміння usePassword

**Якщо `usePassword = true`:**
- На екрані входу відображаються кнопки SSO (наприклад, "Login with Microsoft")
- На екрані входу також відображаються поля для імені користувача та пароля
- Користувачі можуть автентифікуватися будь-яким із методів
- Дозволяє гібридні налаштування, де частина користувачів використовує SSO, а інші — паролі

**Якщо `usePassword = false` (або пропущено):**
- На екрані входу відображаються лише кнопки SSO
- Поля для імені користувача/пароля відсутні
- Доступна лише автентифікація через OIDC

> **💡 Порада**
>
> Вхід за паролем доступний тільки для користувачів, які були створені з паролями за допомогою команди `digna user add` або через панель керування.

### Повний приклад

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

### Розташування файлу

```
/config.toml
```

(Коренева директорія інсталяції digna)

### Крок 1: Додайте секції для OIDC-провайдерів

Кожен провайдер повинен мати окремий розділ `[oidc.<key>]`. Значення key має збігатися з `key`, визначеним у `dashboard_config.toml`.

### Конфігурація Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Конфігурація Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Параметри конфігурації

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID від постачальника ідентифікації | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret від постачальника ідентифікації | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | URL зворотного виклику після автентифікації | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | Пункт конфігурації OIDC | `https://login.microsoftonline.com/...` |

> **⚠️ Важливо**
>
> Замініть значення-заміщувачі (`<client_id>`, `<client_secret>`, `<tenant_id>`) на реальні облікові дані з панелі розробника вашого провайдера ідентифікації.

### Redirect URI

Redirect URI має бути однаковим у конфігурації провайдера і у налаштуваннях identity provider:

```
http://localhost:5173/oidc/callback
```

Якщо digna розгорнуто на іншому домені, оновіть відповідно:
- Локально: `http://localhost:5173/oidc/callback`
- У продакшні: `https://digna.yourdomain.com/oidc/callback`

### Повний приклад

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

Після завершення конфігурації перевірте, чи SSO працює коректно.

### Контрольний список перед тестуванням

Перед тестуванням переконайтеся, що:

- [ ] `dashboard_config.toml` оновлено з OIDC-провайдерами
- [ ] `config.toml` оновлено з OIDC-обліковими даними
- [ ] Обидва файли збережено
- [ ] Облікові дані вірні (client ID, client secret)
- [ ] Redirect URI відповідає URL вашого розгортання
- [ ] У додатку провайдера ідентифікації налаштовано redirect URI

### Кроки тестування

#### Крок 1: Перезапустіть сервіси

Перезапустіть бекенд digna і вебсервер, щоб застосувати зміни.

**Якщо працює як сервіс у Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Якщо запускаєте вручну:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Якщо використовуєте IIS або Tomcat:**
Перезапустіть сервіс вашого вебсерверу.

#### Крок 2: Відкрийте Dashboard

Відкрийте панель digna у браузері:

```
http://localhost:5173
```

(або ваш налаштований URL для dashboard)

#### Крок 3: Перевірте кнопки входу

Переконайтеся, що з’явилися кнопки входу для кожного налаштованого провайдера:

- ✅ Повинна бути кнопка "Login with Microsoft"
- ✅ Повинна бути кнопка "Login with Google"
- ✅ (Якщо usePassword = true) Повинні бути поля для імені користувача/пароля

Якщо кнопок немає:
- Перевірте, що `dashboard_config.toml` збережено
- Перезапустіть сервіс dashboard
- Перевірте консоль браузера (F12) на наявність помилок

#### Крок 4: Перевірте SSO-вхід

Натисніть одну з кнопок SSO (наприклад, "Login with Microsoft"):

1. Ви маєте бути перенаправлені на сторінку входу провайдера ідентифікації
2. Увійдіть за корпоративними обліковими даними
3. Вас має бути перенаправлено назад до digna
4. Ви повинні бути увійшли в систему digna

#### Крок 5: Перевірте створення користувача

Після успішного SSO-входу:

- ✅ Користувач має автоматично створитися в digna
- ✅ Користувач має бути увійшов у систему
- ✅ У профілі користувача мають відображатися дані провайдера ідентифікації
- ✅ Ви маєте бачити панель digna

#### Крок 6: Перевірте вхід за паролем (якщо увімкнено)

Якщо `usePassword = true`:

1. Вийдіть з digna
2. На сторінці входу введіть ім’я користувача та пароль
3. Ви повинні мати можливість увійти з використанням пароля

---

## Troubleshooting {: #troubleshooting }

### Кнопки входу не відображаються

**Симптоми:**
- Кнопки OIDC для входу не видно на сторінці входу
- Відображаються лише поля пароля (якщо usePassword = true)

**Причини та рішення:**
1. Переконайтеся, що `dashboard_config.toml` знаходиться в директорії `dashboard/`
2. Перевірте наявність секцій `[[login.oidc]]` з коректним синтаксисом
3. Перезапустіть сервіс dashboard
4. Очистіть кеш браузера (Ctrl+Shift+Delete або Cmd+Shift+Delete)
5. Перевірте консоль браузера (F12 → вкладка Console) на помилки

---

### Помилка невідповідності Redirect URI

**Симптоми:**
- Після натискання кнопки SSO з’являється помилка про "redirect_uri mismatch"
- Помилка "The redirect URI is not registered"

**Причини та рішення:**
1. Перевірте, що `DIGNA_OIDC_REDIRECT_URI` у `config.toml` вказано правильно
2. Переконайтеся, що redirect URI зареєстровано в налаштуваннях провайдера ідентифікації
3. Переконайтеся, що URL-адреси ідентичні (включаючи протокол, домен, шлях)
4. Перевірте на помилки введення в redirect URI
5. Якщо використовується HTTPS, переконайтеся, що сертифікат дійсний

---

### Помилка невірних облікових даних клієнта

**Симптоми:**
- Помилка "Invalid client ID or secret"
- Автентифікація не вдається через помилку облікових даних

**Причини та рішення:**
1. Перевірте `DIGNA_OIDC_CLIENT_ID` та `DIGNA_OIDC_CLIENT_SECRET` на правильність
2. Переконайтеся, що немає зайвих пробілів або невидимих символів
3. Перевірте, що облікові дані не минули або не були відкликані
4. Перезапустіть бекенд після оновлення конфігурації
5. Перевірте консоль провайдера ідентифікації, щоб підтвердити активність облікових даних

---

### Вхід зависає або час очікування спливає

**Симптоми:**
- Після натискання кнопки SSO нічого не відбувається
- Таймаут через кілька секунд
- Браузер показує "Failed to connect" або подібне

**Причини та рішення:**
1. Переконайтеся, що бекенд digna запущено: `digna repo check`
2. Перевірте мережеве підключення до провайдера ідентифікації
3. Переконайтеся, що `DIGNA_OIDC_CONFIGURATION_URL` доступний
4. Перевірте правила брандмауера, щоб дозволити вихідні HTTPS-з’єднання
5. Переконайтеся, що бекенд і dashboard можуть дістатися один до одного

---

### Користувачі не створюються автоматично

**Симптоми:**
- SSO-вхід пройшов успішно, але користувач не створився в digna
- Після SSO-входу з’являється помилка дозволів

**Причини та рішення:**
1. Перевірте правильність OIDC-конфігурації
2. Переконайтеся, що дозволи користувачів налаштовані правильно
3. Перегляньте логи digna на наявність повідомлень про помилки
4. Перезапустіть бекенд-сервіс
5. Зверніться на support@digna.ai, якщо проблема залишається

---

## Supported Providers {: #supported-providers }

### Тестовані та підтримувані

Нижче наведені OIDC-провайдери, які були протестовані та відомо, що працюють:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Інші OIDC-провайдери

Будь-який провайдер, що підтримує OpenID Connect, можна інтегрувати. Необхідна інформація:

- Client ID
- Client secret
- URL конфігурації OpenID (зазвичай на `/.well-known/openid-configuration`)
- Підтримувані scopes (зазвичай `openid profile email`)

Зверніться на support@digna.ai, якщо потрібна допомога з інтеграцією конкретного провайдера.

---

## Найкращі практики

✅ **РЕКОМЕНДУЄТЬСЯ:**
- Використовувати HTTPS у продакшні (не HTTP)
- Зберігати client secrets у безпечному місці (за можливості використовувати змінні оточення)
- Періодично змінювати секрети
- Тестувати спочатку в непроникному середовищі (non-production)
- Документувати, які провайдери налаштовано
- Моніторити логи входу на предмет підозрілої активності
- Синхронізувати конфігурацію провайдера ідентифікації з конфігом digna

❌ **НЕ РЕКОМЕНДУЄТЬСЯ:**
- Зберігати client secrets у системі контролю версій
- Використовувати HTTP redirect URI у продакшні
- Налаштовувати кілька провайдерів з однаковим key
- Залишати стандартні/тестові облікові дані у продакшні
- Розкривати конфігураційні файли, що містять секрети
- Змішувати облікові дані для розробки та продакшну

---

## Підтримка

Потрібна допомога з налаштуванням SSO?

- 📧 **Email:** support@digna.ai
- 📚 **Документація:** https://docs.digna.ai
- 🌐 **Вебсайт:** https://www.digna.ai

---

**Last Updated:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
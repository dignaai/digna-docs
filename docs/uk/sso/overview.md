---
title: Огляд єдиного входу (SSO) | Документація digna
description: Як працює єдиний вхід у digna на основі OpenID Connect (OIDC). Охоплює налаштування дашборду та бекенду, тестування, усунення несправностей і посилання на посібники з налаштування для Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne та AD FS.
image: /assets/logo_square.png
keywords:
  - digna sso
  - єдиний вхід
  - інтеграція oidc
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - інтеграція okta
  - корпоративна автентифікація
lang: uk
robots: index, follow
og_title: Посібник з інтеграції єдиного входу (SSO) для digna
og_description: Налаштуйте єдиний вхід для digna за допомогою OpenID Connect. Покрокове налаштування для Microsoft Entra ID, Google Workspace, Okta та інших постачальників ідентичності, сумісних з OIDC.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Огляд єдиного входу

---

## Зміст

1. [Вступ і огляд](#introduction-and-overview)
2. [Посібники для постачальників](#provider-guides)
3. [Кроки налаштування](#configuration-steps)
4. [Налаштування дашборду](#dashboard-configuration)
5. [Налаштування бекенду](#backend-configuration)
6. [Тестування входу](#testing-login)
7. [Усунення несправностей](#troubleshooting)
8. [Підтримувані постачальники](#supported-providers)

---

## Вступ і огляд {: #introduction-and-overview }

У цьому посібнику наведено покрокові інструкції з інтеграції єдиного входу (SSO) з платформою digna за допомогою **OpenID Connect (OIDC)**.

### Що таке SSO?

Єдиний вхід дозволяє користувачам безпечно входити в digna з корпоративними обліковими даними через зовнішніх постачальників ідентичності. Користувачі можуть автентифікуватися за допомогою корпоративних облікових даних, а не керувати окремими паролями digna.

### Як це працює

SSO у digna реалізовано за допомогою протоколу OIDC. Кілька постачальників ідентичності можна налаштувати паралельно, змінивши два ключові файли конфігурації:

- **`dashboard_config.toml`** — керує інтерфейсом входу у фронтенді
- **`config.toml`** — налаштовує підключення OIDC у бекенді

### Підтримувані постачальники {: #supported-providers-overview }

У прикладах цього посібника використано **Microsoft** і **Google**, але **будь-якого постачальника, сумісного з OIDC**, можна інтегрувати за тією самою схемою.

---

## Посібники для постачальників {: #provider-guides }

Кожному постачальнику потрібні ті самі чотири значення — ідентифікатор клієнта, секрет клієнта, URI перенаправлення та URL виявлення (discovery URL), — але кожен розміщує їх у різних місцях своєї консолі адміністратора, а в кількох є специфічний крок, якого немає в інших. Наведені нижче посібники охоплюють цю половину роботи; ця сторінка описує половину на боці digna, яка однакова для всіх.

| Постачальник | Посібник | Варто знати |
|---|---|---|
| **AD FS** | [Налаштування SSO з AD FS](adfs_sso_guide.md) | Власний хостинг; єдиний постачальник у списку, де ви самі керуєте службою токенів |
| **Auth0** | [Налаштування SSO з Auth0](auth0_sso_guide.md) | URL виявлення свій для кожного тенанта, і власні домени його змінюють |
| **Google Workspace** | [Налаштування SSO з Google Workspace](google_workspace_sso_guide.md) | Екран згоди має бути опубліковано, перш ніж зможуть входити користувачі, які не є тестовими |
| **Keycloak** | [Налаштування SSO з Keycloak](keycloak_sso_guide.md) | Власний хостинг; URL виявлення свій для кожного realm |
| **Microsoft Entra ID** | [Налаштування SSO з Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Ідентифікатор тенанта входить до URL виявлення; термін дії секретів обмежений |
| **Okta** | [Налаштування SSO з Okta](okta_sso_guide.md) | Вибір сервера авторизації змінює URL виявлення |
| **OneLogin** | [Налаштування SSO з OneLogin](onelogin_sso_guide.md) | Тип застосунку OIDC вибирається під час створення і не може бути змінений |
| **PingOne** | [Налаштування SSO з PingOne](pingone_sso_guide.md) | Ідентифікатор середовища входить до URL виявлення |

Будь-який інший постачальник, сумісний з OIDC, працює так само — див. [Інші постачальники OIDC](#supported-providers).

---

## Кроки налаштування {: #configuration-steps }

Для налаштування SSO потрібно оновити два файли. У цьому розділі пояснюється, як налаштувати кожен із них.

### Огляд файлів конфігурації

| Файл | Розташування | Призначення |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Інтерфейс входу у фронтенді |
| **config.toml** | `/config.toml` | Підключення OIDC у бекенді |

Щоб SSO працював правильно, необхідно налаштувати обидва файли.

---

## Налаштування дашборду {: #dashboard-configuration }

### Розташування файлу

```
dashboard/dashboard_config.toml
```

### Крок 1: Додайте постачальників OIDC

Додайте записи в масив `[[login.oidc]]` для кожного постачальника ідентичності, якого ви хочете підтримувати.

**Приклад з Microsoft і Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Крок 2: Налаштуйте параметри входу

Укажіть, чи дозволено вхід за паролем:

```toml
[login]
usePassword = true
```

### Параметри конфігурації

#### Розділ `[[login.oidc]]`

| Параметр | Тип | Обов'язковий | Опис |
|---|---|---|---|
| `key` | string | Так | Унікальний ідентифікатор підключення OIDC (має збігатися з ключем у config.toml) |
| `label` | string | Так | Текст, що відображається на кнопці входу (наприклад, "Login with Microsoft") |

#### Розділ `[login]`

| Параметр | Тип | За замовчуванням | Опис |
|---|---|---|---|
| `usePassword` | boolean | false | Дозволити вхід за паролем на додачу до SSO |

### Як працює usePassword

**Якщо `usePassword = true`:**
- Екран входу показує кнопки SSO (наприклад, "Login with Microsoft")
- Екран входу також показує поля імені користувача та пароля
- Користувачі можуть автентифікуватися будь-яким із цих способів
- Можливі гібридні налаштування, коли одні користувачі входять через SSO, а інші — за паролем

**Якщо `usePassword = false` (або параметр не вказано):**
- Екран входу показує лише кнопки SSO
- Полів імені користувача та пароля немає
- Доступна лише автентифікація OIDC

!!! tip "Порада"

    Вхід за паролем доступний лише для користувачів, створених із паролем за допомогою команди `digna user add` або через дашборд.

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

## Налаштування бекенду {: #backend-configuration }

### Розташування файлу

```
/config.toml
```

(Кореневий каталог інсталяції digna)

### Крок 1: Додайте розділи постачальників OIDC

Кожен постачальник повинен мати окремий розділ `[oidc_clients.<key>]`. Ключ має збігатися зі значенням `key`, визначеним у `dashboard_config.toml`.

### Налаштування Microsoft

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Налаштування Google

```toml
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Параметри конфігурації

| Параметр | Тип | Обов'язковий | Опис | Приклад |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Так | Ідентифікатор клієнта від постачальника ідентичності | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Так | Секрет клієнта від постачальника ідентичності | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Так | URL зворотного виклику після автентифікації | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Так | Кінцева точка конфігурації OIDC | `https://login.microsoftonline.com/...` |

!!! warning "Важливо"

    Замініть значення-заповнювачі (`<client_id>`, `<client_secret>`, `<tenant_id>`) на справжні облікові дані з порталу розробника вашого постачальника ідентичності.

### URI перенаправлення

URI перенаправлення має бути таким самим у конфігурації вашого постачальника ідентичності:

```
http://localhost:5173/oidc/callback
```

Якщо digna розміщено на іншому домені, змініть його відповідно:
- Локально: `http://localhost:5173/oidc/callback`
- Робоче середовище: `https://digna.yourdomain.com/oidc/callback`

### Повний приклад

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Тестування входу {: #testing-login }

Після завершення налаштування переконайтеся, що SSO працює правильно.

### Контрольний список перед тестуванням

Перед тестуванням переконайтеся, що:

- [ ] `dashboard_config.toml` оновлено з постачальниками OIDC
- [ ] `config.toml` оновлено з обліковими даними OIDC
- [ ] Обидва файли збережено
- [ ] Облікові дані правильні (ідентифікатор клієнта, секрет клієнта)
- [ ] URI перенаправлення відповідає URL вашого розгортання
- [ ] Застосунок у постачальника ідентичності налаштовано з цим URI перенаправлення

### Кроки тестування

#### Крок 1: Перезапустіть служби

Перезапустіть бекенд digna і вебсервер, щоб застосувати зміни.

**Якщо digna працює як служба у Windows:**
```bash
cd C:\path\to\digna
digna windows stop
digna windows start
```

**Якщо digna працює як служба в Linux або macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Якщо digna запущено вручну:**
```bash
digna serve --address localhost --port 8082
```

**Перезапустіть також вебсервер** — IIS або Tomcat у Windows, nginx або Apache в Linux і macOS.

#### Крок 2: Відкрийте дашборд

Відкрийте дашборд digna у браузері:

```
http://localhost:5173
```

(або налаштований вами URL дашборду)

#### Крок 3: Перевірте кнопки входу

Переконайтеся, що для кожного налаштованого постачальника з'являються кнопки входу:

- Має бути кнопка "Login with Microsoft"
- Має бути кнопка "Login with Google"
- (Якщо usePassword = true) Мають бути поля імені користувача та пароля

Якщо кнопки не з'являються:
- Перевірте, чи збережено `dashboard_config.toml`
- Перевірте, чи перезапущено службу дашборду
- Перевірте консоль браузера (F12) на наявність помилок

#### Крок 4: Перевірте вхід через SSO

Натисніть одну з кнопок SSO (наприклад, "Login with Microsoft"):

1. Вас має бути перенаправлено на сторінку входу постачальника ідентичності
2. Увійдіть із корпоративними обліковими даними
3. Вас має бути перенаправлено назад до digna
4. Ви маєте увійти в digna

#### Крок 5: Перевірте створення користувача

Після успішного входу через SSO:

- Користувача має бути автоматично створено в digna
- Користувач має бути в системі
- Профіль користувача має показувати ваші облікові дані від постачальника ідентичності
- Ви маєте бачити дашборд digna

#### Крок 6: Перевірте вхід за паролем (якщо ввімкнено)

Якщо `usePassword = true`:

1. Вийдіть із digna
2. На сторінці входу введіть ім'я користувача та пароль
3. Ви маєте змогу увійти з обліковими даними за паролем

---

## Усунення несправностей {: #troubleshooting }

### Кнопки входу не з'являються

**Симптоми:**
- Кнопки входу OIDC не видно на сторінці входу
- Видно лише поля пароля (якщо usePassword = true)

**Причини та рішення:**
1. Перевірте, чи `dashboard_config.toml` знаходиться в каталозі `dashboard/`
2. Переконайтеся, що розділи `[[login.oidc]]` присутні та мають правильний синтаксис
3. Перезапустіть службу дашборду
4. Очистіть кеш браузера (Ctrl+Shift+Delete або Cmd+Shift+Delete)
5. Перевірте консоль браузера (F12 → вкладка Console) на наявність помилок

---

### Помилка невідповідності URI перенаправлення

**Симптоми:**
- Після натискання кнопки SSO з'являється помилка "redirect_uri mismatch"
- Помилка "The redirect URI is not registered"

**Причини та рішення:**
1. Перевірте, чи правильний `DIGNA_OIDC_REDIRECT_URI` у `config.toml`
2. Перевірте, чи зареєстровано URI перенаправлення в налаштуваннях постачальника ідентичності
3. Переконайтеся, що обидва місця використовують ідентичні URL (включно з протоколом, доменом і шляхом)
4. Перевірте URI перенаправлення на наявність друкарських помилок
5. Якщо використовується HTTPS, переконайтеся, що сертифікат дійсний

---

### Помилка недійсних облікових даних клієнта

**Симптоми:**
- Помилка "Invalid client ID or secret"
- Автентифікація не вдається з помилкою облікових даних

**Причини та рішення:**
1. Перевірте, чи правильні `DIGNA_OIDC_CLIENT_ID` і `DIGNA_OIDC_CLIENT_SECRET`
2. Переконайтеся, що немає зайвих пробілів або спеціальних символів
3. Перевірте, чи не минув термін дії облікових даних і чи їх не відкликано
4. Перезапустіть службу бекенду після оновлення конфігурації
5. Перевірте в консолі постачальника ідентичності, що облікові дані активні

---

### Вхід зависає або завершується за тайм-аутом

**Симптоми:**
- Натискання кнопки SSO нічого не робить
- Тайм-аут через кілька секунд
- Браузер показує "Failed to connect" або подібне повідомлення

**Причини та рішення:**
1. Перевірте, чи працює бекенд digna: `digna repo check`
2. Перевірте мережеве з'єднання з постачальником ідентичності
3. Перевірте доступність `DIGNA_OIDC_CONFIGURATION_URL`
4. Переконайтеся, що правила брандмауера дозволяють вихідні підключення HTTPS
5. Переконайтеся, що бекенд і дашборд можуть зв'язатися один з одним

---

### Користувачі не створюються автоматично

**Симптоми:**
- Вхід через SSO успішний, але користувача в digna не створено
- Після входу через SSO з'являється помилка дозволів

**Причини та рішення:**
1. Перевірте правильність конфігурації OIDC
2. Перевірте, чи налаштовано дозволи користувачів
3. Перегляньте журнали digna на наявність повідомлень про помилки
4. Перезапустіть службу бекенду
5. Якщо проблема не зникає, зверніться на support@digna.ai

---

## Підтримувані постачальники {: #supported-providers }

### Протестовані та підтримувані

Наведених нижче постачальників OIDC протестовано, і вони гарантовано працюють:

| Постачальник | URL конфігурації | Посібник з налаштування |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Налаштування SSO з AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Налаштування SSO з Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Налаштування SSO з Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Налаштування SSO з Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Налаштування SSO з Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Налаштування SSO з Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Налаштування SSO з OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Налаштування SSO з PingOne](pingone_sso_guide.md) |

### Інші постачальники OIDC

Можна інтегрувати будь-якого постачальника, що підтримує OpenID Connect. Потрібна інформація:

- Ідентифікатор клієнта (Client ID)
- Секрет клієнта (Client secret)
- URL конфігурації OpenID (зазвичай за адресою `/.well-known/openid-configuration`)
- Підтримувані області (scopes) (зазвичай `openid profile email`)

Якщо вам потрібна допомога з інтеграцією певного постачальника, зверніться на support@digna.ai.

---

## Найкращі практики

**РОБІТЬ:**
- Використовуйте HTTPS у робочому середовищі (а не HTTP)
- Зберігайте секрети клієнта в безпечному місці (за можливості використовуйте змінні середовища)
- Періодично змінюйте секрети
- Спочатку тестуйте в неробочому середовищі
- Документуйте, які постачальники налаштовано
- Відстежуйте журнали входу на предмет незвичної активності
- Підтримуйте конфігурацію постачальника ідентичності синхронізованою з конфігурацією digna

**НЕ РОБІТЬ:**
- Не зберігайте секрети клієнта в системі керування версіями
- Не використовуйте URI перенаправлення HTTP у робочому середовищі
- Не налаштовуйте кількох постачальників з однаковим ключем
- Не залишайте стандартні або тестові облікові дані в робочому середовищі
- Не відкривайте доступ до файлів конфігурації, що містять секрети
- Не змішуйте облікові дані середовищ розробки та робочого середовища

---

## Підтримка

Потрібна допомога з налаштуванням SSO?

- **Електронна пошта:** support@digna.ai
- **Документація:** https://docs.digna.ai
- **Вебсайт:** https://www.digna.ai

---

**Останнє оновлення:** 30 серпня 2026 р.  
**Випуск:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**

---
title: SSO з Microsoft Entra ID – інтеграція єдиного входу | Документація digna
description: Налаштуйте єдиний вхід для digna з Microsoft Entra ID (раніше Azure AD) за допомогою OpenID Connect — реєстрація застосунку, URI перенаправлення, секрет клієнта, ідентифікатор тенанта та відповідна конфігурація digna.
image: /assets/logo_square.png
keywords: digna sso, microsoft entra id, azure ad sso, інтеграція oidc, реєстрація застосунку, корпоративна автентифікація
---

# Налаштування SSO з Microsoft Entra ID

Microsoft Entra ID (раніше Azure Active Directory) — постачальник, повністю сумісний з OIDC, тому digna інтегрується з ним через стандартну кінцеву точку виявлення.

Цей посібник охоплює **бік Entra ID**: реєстрацію застосунку та збирання чотирьох значень, потрібних digna. Бік digna — `dashboard_config.toml`, тестування та усунення несправностей — однаковий для всіх постачальників і описаний в [Огляді єдиного входу](overview.md).

---

## Перш ніж почати

| Вимога | Примітки |
|---|---|
| **Роль в Entra ID** | Application Administrator, Cloud Application Administrator або Global Administrator |
| **URI перенаправлення digna** | URL, на який користувачі повертаються після входу, наприклад `https://digna.yourdomain.com/oidc/callback` |
| **Тенант** | Каталог, у який входять ваші користувачі |

---

## Крок 1: Зареєструйте застосунок

1. Увійдіть у [Microsoft Entra admin center](https://entra.microsoft.com)
2. Перейдіть до **Identity → Applications → App registrations**
3. Натисніть **New registration**
4. Налаштуйте:
   - **Name**: `digna` (показується користувачам на екрані згоди)
   - **Supported account types**: *Accounts in this organizational directory only* для розгортання з одним тенантом
5. У розділі **Redirect URI** виберіть платформу **Web** і введіть URL зворотного виклику digna:

```
https://digna.yourdomain.com/oidc/callback
```

6. Натисніть **Register**

!!! warning "Важливо"

    Платформа має бути **Web**, а не *Single-page application*. digna обмінює код авторизації на бекенді за допомогою секрету клієнта, чого тип платформи SPA не дозволяє.

---

## Крок 2: Зберіть ідентифікатори клієнта та тенанта

На сторінці **Overview** застосунку скопіюйте:

- **Application (client) ID** → це буде `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → входить до URL виявлення

---

## Крок 3: Створіть секрет клієнта

1. Перейдіть до **Certificates & secrets → Client secrets**
2. Натисніть **New client secret**
3. Введіть опис і виберіть термін дії
4. Натисніть **Add**
5. Одразу скопіюйте значення зі стовпця **Value**

!!! warning "Копіюйте Value, а не Secret ID"

    **Value** показується лише один раз, на цій сторінці, і згодом його неможливо отримати. **Secret ID** поруч виглядає схоже, але не є секретом — його використання призводить до помилки `invalid_client` під час входу. Якщо ви перейшли зі сторінки, не скопіювавши значення, видаліть секрет і створіть новий.

!!! tip "Порада"

    Entra ID обмежує термін дії секрету 24 місяцями, тому кожна інтеграція SSO має дату закінчення терміну дії. Запишіть її там, де ви її побачите — прострочений секрет вимикає SSO одразу для всіх користувачів без жодного попередження на сторінці входу.

---

## Крок 4: Перевірте дозволи API

1. Перейдіть до **API permissions**
2. Переконайтеся, що **Microsoft Graph → User.Read** (делегований) присутній — його додано за замовчуванням

Області `openid`, `profile` і `email`, які запитує digna, входять до стандартного набору OIDC і не потребують окремого надання. Якщо ваш тенант вимагає згоди адміністратора для всіх застосунків, натисніть **Grant admin consent for &lt;tenant&gt;**.

---

## Крок 5: Складіть URL виявлення

Підставте **Directory (tenant) ID** з кроку 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Використовуйте кінцеву точку v2.0"

    Сегмент `/v2.0/` має значення. Кінцева точка v1.0 за адресою `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` видає токени в старішому форматі і не повертає стандартних тверджень (claims) OIDC, яких очікує digna.

Перш ніж продовжити, відкрийте URL у браузері. Документ JSON підтверджує, що ідентифікатор тенанта правильний.

---

## Крок 6: Налаштуйте digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

`key` в обох файлах має збігатися — тут це `microsoft`.

---

## Крок 7: Тестування

Перезапустіть бекенд і вебсервер, потім відкрийте дашборд. Повний контрольний список див. у розділі [Тестування входу](overview.md#testing-login).

---

## Усунення несправностей Entra ID

### AADSTS50011: Redirect URI Mismatch

URI в `DIGNA_OIDC_REDIRECT_URI` відрізняється від зареєстрованого на кроці 1. Entra ID порівнює рядок повністю, тому кінцева скісна риска, `http` замість `https` або інший порт — усе це вважається невідповідністю. Перевірте **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Або замість **Value** було скопійовано **Secret ID**, або термін дії секрету минув. Створіть новий секрет і скопіюйте значення зі стовпця Value.

### AADSTS650057: Invalid Resource

Реєстрацію застосунку видалено, або вона належить іншому тенанту, ніж указаний в URL виявлення. Перевірте Directory (tenant) ID на сторінці Overview.

### Користувачі входять, але нічого не відбувається

Якщо тенант вимагає згоди адміністратора, а її не надано, перенаправлення повертається без придатного токена. Надайте згоду адміністратора в **API permissions**.

---

## Див. також

- [Огляд єдиного входу](overview.md) — довідник з конфігурації, тестування та загальне усунення несправностей
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)

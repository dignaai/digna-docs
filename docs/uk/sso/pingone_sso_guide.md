---
title: SSO з PingOne – інтеграція єдиного входу | Документація digna
description: Налаштуйте єдиний вхід для digna з PingOne за допомогою OpenID Connect — налаштування вебзастосунку OIDC, URI перенаправлення, облікові дані клієнта, ідентифікатор середовища, регіональні домени та відповідна конфігурація digna.
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, ідентифікатор середовища, openid connect, корпоративна автентифікація
---

# Налаштування SSO з PingOne

PingOne сумісний з OIDC. Два його значення потребують уваги: **ідентифікатор середовища**, який входить до URL кожної кінцевої точки, і **регіональний домен**, що відрізняється для північноамериканських, європейських, канадських, азійсько-тихоокеанських та австралійських тенантів.

Цей посібник охоплює **бік PingOne**: створення застосунку та збирання значень, потрібних digna. Бік digna — `dashboard_config.toml`, тестування та усунення несправностей — однаковий для всіх постачальників і описаний в [Огляді єдиного входу](overview.md).

---

## Перш ніж почати

| Вимога | Примітки |
|---|---|
| **Роль у PingOne** | Environment Admin або Identity Data Admin у цільовому середовищі |
| **Середовище** | Середовище PingOne, до якого належать користувачі digna |
| **URI перенаправлення digna** | URL, на який користувачі повертаються після входу, наприклад `https://digna.yourdomain.com/oidc/callback` |

---

## Крок 1: Створіть застосунок

1. Увійдіть у консоль адміністратора PingOne і виберіть своє середовище
2. Перейдіть до **Applications → Applications**
3. Натисніть кнопку **+**
4. Введіть `digna` як **Application Name**
5. Виберіть **OIDC Web App**
6. Натисніть **Save**

!!! warning "Вибирайте OIDC Web App, а не Single-Page App"

    *Single-Page App* і *Native App* створюють публічних клієнтів, які не можуть зберігати секрет. digna обмінює код авторизації зі свого бекенду, і їй потрібен конфіденційний тип **OIDC Web App**.

---

## Крок 2: Налаштуйте URI перенаправлення

1. Відкрийте вкладку **Configuration** застосунку
2. Натисніть піктограму олівця, щоб редагувати
3. Переконайтеся, що **Response Type** має значення *Code*, а **Grant Type** — *Authorization Code*
4. У розділі **Redirect URIs** введіть URL зворотного виклику digna:

```
https://digna.yourdomain.com/oidc/callback
```

5. Установіть для **Token Endpoint Authentication Method** значення *Client Secret Post* або *Client Secret Basic*
6. Натисніть **Save**

---

## Крок 3: Увімкніть застосунок

У рядку застосунку або на панелі відомостей переведіть перемикач у стан **enabled**.

!!! warning "Нові застосунки спочатку вимкнені"

    PingOne створює застосунки у вимкненому стані. Вимкнений застосунок спричиняє помилку на кроці авторизації, яка не згадує перемикач, тому варто перевірити це, перш ніж шукати інші причини.

---

## Крок 4: Надайте області

1. Відкрийте вкладку **Resources**
2. Переконайтеся, що `openid` надано, і додайте `profile` та `email` з ресурсу **OpenID Connect**
3. Натисніть **Save**

---

## Крок 5: Призначте користувачів

1. Відкрийте вкладку **Access**
2. Додайте популяцію (population) або групи, учасникам яких дозволено використовувати digna
3. Натисніть **Save**

---

## Крок 6: Зберіть облікові дані та ідентифікатор середовища

На вкладці **Configuration** розгорніть **General**:

- **Client ID** → це буде `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → це буде `DIGNA_OIDC_CLIENT_SECRET` (натисніть піктограму ока)
- **Environment ID** → входить до URL виявлення

На тій самій вкладці наведено готовий **OIDC Discovery Endpoint**, який можна скопіювати безпосередньо, а не складати вручну.

---

## Крок 7: Складіть URL виявлення

Підставте ідентифікатор середовища та домен свого регіону:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Регіон | Домен |
|---|---|
| Північна Америка | `auth.pingone.com` |
| Європа | `auth.pingone.eu` |
| Канада | `auth.pingone.ca` |
| Азійсько-Тихоокеанський регіон | `auth.pingone.asia` |
| Австралія | `auth.pingone.com.au` |

Для європейського середовища:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Копіюйте, а не вводьте вручну"

    Регіональний домен — найпоширеніша помилка в інтеграції PingOne, а неправильний регіон дає 404 замість корисного повідомлення. Використовуйте значення **OIDC Discovery Endpoint** з кроку 6.

---

## Крок 8: Налаштуйте digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc_clients.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

`key` в обох файлах має збігатися — тут це `pingone`.

---

## Крок 9: Тестування

Перезапустіть бекенд і вебсервер, потім відкрийте дашборд. Повний контрольний список див. у розділі [Тестування входу](overview.md#testing-login).

---

## Усунення несправностей PingOne

### 404 для URL виявлення

Регіональний домен або ідентифікатор середовища неправильний. Порівняйте з **OIDC Discovery Endpoint**, показаним на вкладці Configuration застосунку.

### NOT_FOUND або Application Disabled

Перемикач застосунку з кроку 3 досі вимкнено.

### Невідповідність URI перенаправлення

PingOne порівнює рядок повністю. Перевірте **Configuration → Redirect URIs** на наявність кінцевої скісної риски або відмінності у схемі.

### Вхід успішний, але твердження email не надходить до digna

Області `email` і `profile` не надано на вкладці **Resources**.

### Користувач не бачить застосунку

На вкладці **Access** не надано доступу жодній популяції чи групі.

---

## Див. також

- [Огляд єдиного входу](overview.md) — довідник з конфігурації, тестування та загальне усунення несправностей
- [PingOne: налаштування застосунку OIDC](https://docs.pingidentity.com/pingone/)

---
title: SSO з OneLogin – інтеграція єдиного входу | Документація digna
description: Налаштуйте єдиний вхід для digna з OneLogin за допомогою OpenID Connect — створення застосунку OIDC, URI перенаправлення, облікові дані клієнта, автентифікація на кінцевій точці токенів та відповідна конфігурація digna.
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, автентифікація на кінцевій точці токенів, корпоративна автентифікація
---

# Налаштування SSO з OneLogin

OneLogin сумісний з OIDC. Його відмінна риса — тип конектора вибирається з каталогу під час створення застосунку і згодом не може бути змінений.

Цей посібник охоплює **бік OneLogin**: створення застосунку та збирання значень, потрібних digna. Бік digna — `dashboard_config.toml`, тестування та усунення несправностей — однаковий для всіх постачальників і описаний в [Огляді єдиного входу](overview.md).

---

## Перш ніж почати

| Вимога | Примітки |
|---|---|
| **Роль в OneLogin** | Власник облікового запису або адміністратор із правом додавати застосунки |
| **Піддомен** | наприклад, `yourcompany.onelogin.com` |
| **URI перенаправлення digna** | URL, на який користувачі повертаються після входу, наприклад `https://digna.yourdomain.com/oidc/callback` |

---

## Крок 1: Створіть застосунок OIDC

1. Увійдіть в OneLogin Admin portal
2. Перейдіть до **Applications → Applications**
3. Натисніть **Add App**
4. Знайдіть `OpenId Connect` і виберіть конектор **OpenId Connect (OIDC)**
5. Установіть для **Display Name** значення `digna`
6. Натисніть **Save**

!!! warning "Тип конектора фіксується під час створення"

    OneLogin має окремі записи в каталозі для SAML і OIDC, і застосунок неможливо перетворити з одного на інший. Якщо ви помилково вибрали конектор SAML, видаліть застосунок і додайте його знову — параметра для перемикання протоколів немає.

---

## Крок 2: Налаштуйте URI перенаправлення

1. Відкрийте вкладку **Configuration**
2. У полі **Redirect URI's** введіть URL зворотного виклику digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. За бажанням укажіть у **Post Logout Redirect URIs** URL свого дашборду
4. Натисніть **Save**

!!! note "Один URI на рядок"

    На відміну від постачальників, які очікують список через кому, поле **Redirect URI's** в OneLogin приймає один URI на рядок.

---

## Крок 3: Установіть тип застосунку та метод автентифікації

1. Відкрийте вкладку **SSO**
2. Переконайтеся, що **Application Type** має значення *Web*
3. Установіть для **Token Endpoint → Authentication Method** значення *POST* (`client_secret_post`) або *Basic* (`client_secret_basic`)

!!! warning "Не вибирайте None"

    Якщо встановити метод автентифікації *None*, застосунок стане публічним клієнтом без секрету, і обмін кодом на бекенді digna буде відхилено. Працює як POST, так і Basic.

---

## Крок 4: Зберіть облікові дані

Там само, на вкладці **SSO**:

- **Client ID** → це буде `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → це буде `DIGNA_OIDC_CLIENT_SECRET` (натисніть **Show client secret**)

На сторінці також показано **Issuer URL**, який підтверджує URL виявлення з наступного кроку.

---

## Крок 5: Призначте користувачів

1. Відкрийте вкладку **Access**
2. Додайте ролі або групи, учасникам яких дозволено використовувати digna
3. Натисніть **Save**

!!! note "Непризначені користувачі отримують відмову після входу"

    Як і більшість постачальників, OneLogin спочатку автентифікує користувача, а потім перевіряє його права. Непризначений користувач успішно входить і лише потім отримує відмову, що виглядає як помилка digna, а не як рішення контролю доступу.

---

## Крок 6: Складіть URL виявлення

Підставте свій піддомен OneLogin:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Наприклад:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 — це версія API"

    Поточна реалізація OIDC в OneLogin розміщена під `/oidc/2/`. У старішій документації показано `/oidc/` без версії, що вказує на виведену з експлуатації першу версію. Якщо сумніваєтеся, перевірте **Issuer URL** на вкладці SSO — URL виявлення складається з видавця плюс `/.well-known/openid-configuration`.

---

## Крок 7: Налаштуйте digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc_clients.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

`key` в обох файлах має збігатися — тут це `onelogin`.

---

## Крок 8: Тестування

Перезапустіть бекенд і вебсервер, потім відкрийте дашборд. Повний контрольний список див. у розділі [Тестування входу](overview.md#testing-login).

---

## Усунення несправностей OneLogin

### redirect_uri did not match

URL зворотного виклику відсутній у **Configuration → Redirect URI's**, або записи розділено комами, а не новими рядками.

### invalid_client на кроці отримання токена

Для **Token Endpoint → Authentication Method** встановлено *None*, або секрет клієнта в `config.toml` застарів. Покажіть секрет на вкладці **SSO** і порівняйте.

### Застосунок не з'являється для користувачів

На вкладці **Access** не надано доступу жодній ролі чи групі.

### 404 для URL виявлення

Піддомен неправильний, або в URL бракує `/oidc/2/`. Порівняйте з **Issuer URL**, показаним на вкладці SSO.

---

## Див. також

- [Огляд єдиного входу](overview.md) — довідник з конфігурації, тестування та загальне усунення несправностей
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)

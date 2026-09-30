# Налаштування SSO з Okta

Okta сумісна з OIDC, але має одну особливість, на якій спотикається більшість перших інтеграцій: організація Okta надає більше одного сервера авторизації, і кожен має власний URL виявлення.

Цей посібник охоплює **бік Okta**: створення інтеграції застосунку та збирання значень, потрібних digna. Бік digna — `dashboard_config.toml`, тестування та усунення несправностей — однаковий для всіх постачальників і описаний в [Огляді єдиного входу](overview.md).

---

## Перш ніж почати

| Вимога | Примітки |
|---|---|
| **Роль в Okta** | Super Administrator або роль адміністратора з правом створювати інтеграції застосунків |
| **Домен Okta** | наприклад, `yourcompany.okta.com` або власний домен, якщо його налаштовано |
| **URI перенаправлення digna** | URL, на який користувачі повертаються після входу, наприклад `https://digna.yourdomain.com/oidc/callback` |

---

## Крок 1: Створіть інтеграцію застосунку

1. Увійдіть в Okta Admin Console
2. Перейдіть до **Applications → Applications**
3. Натисніть **Create App Integration**
4. Виберіть:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Натисніть **Next**

!!! warning "Тип застосунку неможливо змінити"

    Якщо вибрати *Single-Page Application* замість *Web Application*, буде створено публічного клієнта без секрету, і обмін кодом на бекенді digna завершиться помилкою `invalid_client`. Тип фіксується під час створення — неправильний вибір означає, що доведеться видалити застосунок і почати заново.

---

## Крок 2: Налаштуйте інтеграцію

1. **App integration name**: `digna`
2. **Grant type**: залиште вибраним *Authorization Code*
3. **Sign-in redirect URIs**: введіть URL зворотного виклику digna:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: необов'язково
5. У розділі **Assignments** виберіть, хто може використовувати інтеграцію — конкретна група безпечніша, ніж *Allow everyone in your organization to access*
6. Натисніть **Save**

!!! note "Призначення обов'язкове"

    Okta автентифікує користувача, а потім перевіряє, чи його призначено до застосунку. Непризначений користувач потрапляє на сторінку входу Okta, успішно входить, і отримує відмову під час перенаправлення назад. Якщо вхід працює для вас, але не для колег, насамперед перевірте призначення.

---

## Крок 3: Зберіть облікові дані

На вкладці **General** застосунку, у розділі **Client Credentials**:

- **Client ID** → це буде `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → це буде `DIGNA_OIDC_CLIENT_SECRET` (натисніть піктограму ока, щоб показати)

---

## Крок 4: Виберіть сервер авторизації

Саме цей крок визначає ваш URL виявлення. Перейдіть до **Security → API**, щоб побачити сервери авторизації у вашій організації.

**Сервер авторизації організації (org)** — видає токени для самої організації Okta:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Власний сервер авторизації (custom)** — зокрема той, який Okta створює під назвою `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Для вбудованого сервера `<auth_server_id>` — це буквально `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Який вибрати?"

    Використовуйте сервер авторизації **org**, якщо ваша організація ще не стандартизувала власний сервер для політик доступу до API. В облікових записах Okta Developer за замовчуванням використовується `default`; у багатьох корпоративних організаціях його вимкнено. Відкрийте обидва URL у браузері — той, що повертає JSON, а не помилку, і є доступним для вас.

---

## Крок 5: Налаштуйте digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc_clients.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

`key` в обох файлах має збігатися — тут це `okta`.

---

## Крок 6: Тестування

Перезапустіть бекенд і вебсервер, потім відкрийте дашборд. Повний контрольний список див. у розділі [Тестування входу](overview.md#testing-login).

---

## Усунення несправностей Okta

### The redirect URI Is Not Registered

Okta називає проблемний URI в повідомленні про помилку. Порівняйте його з **General → Sign-in redirect URIs**; Okta порівнює рядок повністю, включно з кінцевою скісною рискою.

### User Is Not Assigned to the Client Application

Обліковий запис відсутній у списку призначень застосунку. Додайте користувача або його групу в розділі **Assignments**.

### 400 Bad Request: Invalid Authorization Server

`<auth_server_id>` в URL виявлення не існує — найчастіше це `default` в організації, де його видалено. Перевірте в **Security → API**, які сервери насправді доступні.

### invalid_client на кроці отримання токена

Інтеграцію створено як Single-Page Application, і вона не має секрету клієнта. Створіть її заново як Web Application.

---

## Див. також

- [Огляд єдиного входу](overview.md) — довідник з конфігурації, тестування та загальне усунення несправностей
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
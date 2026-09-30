# Налаштування SSO з Auth0

Auth0 сумісний з OIDC і надає кінцеву точку виявлення для кожного тенанта. Найважливіше — правильно вказати домен тенанта, який входить до URL виявлення і змінюється, якщо ввімкнути власний домен.

Цей посібник охоплює **бік Auth0**: створення застосунку та збирання значень, потрібних digna. Бік digna — `dashboard_config.toml`, тестування та усунення несправностей — однаковий для всіх постачальників і описаний в [Огляді єдиного входу](overview.md).

---

## Перш ніж почати

| Вимога | Примітки |
|---|---|
| **Роль в Auth0** | Адміністратор тенанта |
| **Домен тенанта** | наприклад, `yourcompany.eu.auth0.com` — сегмент регіону має значення |
| **URI перенаправлення digna** | URL, на який користувачі повертаються після входу, наприклад `https://digna.yourdomain.com/oidc/callback` |

---

## Крок 1: Створіть застосунок

1. Увійдіть в [Auth0 Dashboard](https://manage.auth0.com)
2. Перейдіть до **Applications → Applications**
3. Натисніть **Create Application**
4. Назвіть його `digna` і виберіть **Regular Web Applications**
5. Натисніть **Create**

!!! warning "Виберіть Regular Web Applications"

    *Single Page Application* і *Native* створюють публічних клієнтів без секрету. digna виконує обмін кодом зі свого бекенду, і їй потрібен конфіденційний клієнт, тому правильний тип — **Regular Web Applications**. На відміну від деяких постачальників, Auth0 дозволяє змінити тип пізніше в **Settings → Application Type**.

---

## Крок 2: Додайте URL зворотного виклику

На вкладці **Settings** застосунку:

1. Знайдіть **Allowed Callback URLs**
2. Введіть URL зворотного виклику digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. За бажанням укажіть в **Allowed Logout URLs** URL свого дашборду
4. Прокрутіть донизу і натисніть **Save Changes**

!!! note "Розділяйте комами, а не новими рядками"

    Auth0 приймає в цьому полі кілька URL зворотного виклику, розділених комами. Список, розділений лише новими рядками, сприймається як один некоректний URL і непомітно не збігається ні з чим.

---

## Крок 3: Зберіть облікові дані

Там само, у **Settings**, на панелі **Basic Information**:

- **Domain** → входить до URL виявлення
- **Client ID** → це буде `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → це буде `DIGNA_OIDC_CLIENT_SECRET` (натисніть, щоб показати)

---

## Крок 4: Перевірте тип дозволу (grant type)

1. Перейдіть до **Settings → Advanced Settings → Grant Types**
2. Переконайтеся, що **Authorization Code** позначено

Для Regular Web Applications його ввімкнено за замовчуванням. Якщо позначку знято, вхід у digna не вдається з помилкою `unauthorized_client`.

---

## Крок 5: Складіть URL виявлення

Підставте **Domain** з кроку 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Наприклад:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Власні домени змінюють видавця (issuer)"

    Якщо ваш тенант використовує власний домен, наприклад `login.yourcompany.com`, укажіть цей домен в URL виявлення. Змішування обох — канонічного домену в URL виявлення і власного в браузері — призводить до невідповідності видавця, і токен відхиляється після загалом успішного входу.

---

## Крок 6: Налаштуйте digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc_clients.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

`key` в обох файлах має збігатися — тут це `auth0`.

---

## Крок 7: Тестування

Перезапустіть бекенд і вебсервер, потім відкрийте дашборд. Повний контрольний список див. у розділі [Тестування входу](overview.md#testing-login).

---

## Усунення несправностей Auth0

### Невідповідність URL зворотного виклику

Сторінка помилки Auth0 показує отриманий URL. Додайте його в **Allowed Callback URLs**, перевіривши, що записи розділено комами.

### unauthorized_client

**Authorization Code** не ввімкнено в **Advanced Settings → Grant Types**, або тип застосунку не Regular Web Applications.

### Доступ заборонено після успішного входу

Правило (Rule), дія (Action) або тригер Post-Login у тенанті відхиляє користувача. Перевірте **Actions → Flows → Login** і журнали тенанта в **Monitoring → Logs**, де вказано точну причину.

### Невідповідність видавця

URL виявлення і домен, на який було спрямовано браузер, відрізняються — зазвичай це канонічний домен тенанта і власний домен. Використовуйте один із них послідовно.

---

## Див. також

- [Огляд єдиного входу](overview.md) — довідник з конфігурації, тестування та загальне усунення несправностей
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
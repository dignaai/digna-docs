# Налаштування SSO з Google Workspace

Платформа ідентичності Google сумісна з OIDC і використовує єдиний загальновідомий URL виявлення для всіх клієнтів, тому єдині значення, специфічні для організації, — це ідентифікатор і секрет клієнта.

Цей посібник охоплює **бік Google**: створення клієнта OAuth і збирання значень, потрібних digna. Бік digna — `dashboard_config.toml`, тестування та усунення несправностей — однаковий для всіх постачальників і описаний в [Огляді єдиного входу](overview.md).

---

## Перш ніж почати

| Вимога | Примітки |
|---|---|
| **Проєкт Google Cloud** | Будь-який проєкт у тій самій організації, що й ваш домен Workspace |
| **Роль** | Editor або Owner у проєкті |
| **URI перенаправлення digna** | URL, на який користувачі повертаються після входу, наприклад `https://digna.yourdomain.com/oidc/callback` |

---

## Крок 1: Налаштуйте екран згоди OAuth

Google не видасть облікові дані, доки не буде створено екран згоди.

1. Відкрийте [Google Cloud Console](https://console.cloud.google.com) і виберіть свій проєкт
2. Перейдіть до **APIs & Services → OAuth consent screen**
3. Виберіть тип користувачів:
   - **Internal** — входити можуть лише облікові записи з вашого домену Workspace. Рекомендовано.
   - **External** — спробувати увійти може будь-який обліковий запис Google.
4. Заповніть назву застосунку, електронну адресу підтримки користувачів і контактну адресу розробника
5. На кроці **Scopes** додайте `openid`, `.../auth/userinfo.email` і `.../auth/userinfo.profile`
6. Збережіть

!!! warning "Зовнішні застосунки мають бути опубліковані"

    Екран згоди типу **External** спочатку має статус *Testing*, у якому завершити вхід можуть лише облікові записи, явно додані до списку тестових користувачів. Усі інші бачать "digna has not completed the Google verification process". Або переведіть застосунок у стан **In production** у розділі **Publishing status**, або використовуйте **Internal** — цей тип не має такого обмеження і є правильним вибором для розгортання лише в межах Workspace.

---

## Крок 2: Створіть клієнта OAuth

1. Перейдіть до **APIs & Services → Credentials**
2. Натисніть **Create Credentials → OAuth client ID**
3. Установіть для **Application type** значення **Web application**
4. Дайте йому назву, наприклад `digna`
5. У розділі **Authorized redirect URIs** натисніть **Add URI** і введіть:

```
https://digna.yourdomain.com/oidc/callback
```

6. Натисніть **Create**

!!! note "Authorized JavaScript Origins не потрібні"

    digna обмінює код авторизації на бекенді, а не в браузері, тому поле **Authorized JavaScript origins** можна залишити порожнім. Має значення лише URI перенаправлення.

---

## Крок 3: Зберіть облікові дані

Діалог, що з'являється після створення, показує:

- **Client ID** — закінчується на `.apps.googleusercontent.com` → це буде `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → це буде `DIGNA_OIDC_CLIENT_SECRET`

На відміну від більшості інших постачальників, обидва значення можна пізніше отримати на сторінці відомостей облікових даних.

---

## Крок 4: URL виявлення

Google використовує один URL виявлення для всіх клієнтів — нічого підставляти не потрібно:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Крок 5: Налаштуйте digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

`key` в обох файлах має збігатися — тут це `google`.

---

## Крок 6: Тестування

Перезапустіть бекенд і вебсервер, потім відкрийте дашборд. Повний контрольний список див. у розділі [Тестування входу](overview.md#testing-login).

---

## Усунення несправностей Google Workspace

### Error 400: redirect_uri_mismatch

URI в `DIGNA_OIDC_REDIRECT_URI` відсутній у списку **Authorized redirect URIs** або відрізняється кінцевою скісною рискою чи схемою. Сторінка помилки Google показує отриманий URI — порівняйте його символ за символом із зареєстрованим.

### This App Is Blocked / Has Not Completed Verification

Екран згоди має тип **External** і досі перебуває в стані *Testing*. Опублікуйте його або переведіть застосунок на **Internal**.

### Access Blocked: Authorization Error

Обліковий запис, з якого намагаються увійти, не належить до вашого домену Workspace, а екран згоди має тип **Internal**. Це очікувана поведінка — застосунки Internal приймають лише облікові записи організації.

### Зміни набувають чинності через кілька хвилин

Google поширює зміни облікових даних і екрана згоди асинхронно. Новододаний URI перенаправлення може почати діяти лише через кілька хвилин; якщо здається, що зміну проігноровано, зачекайте і повторіть спробу, перш ніж шукати причину далі.

---

## Див. також

- [Огляд єдиного входу](overview.md) — довідник з конфігурації, тестування та загальне усунення несправностей
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
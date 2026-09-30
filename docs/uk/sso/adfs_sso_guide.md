---
title: SSO з AD FS – інтеграція єдиного входу | Документація digna
description: Налаштуйте єдиний вхід для digna з Active Directory Federation Services за допомогою OpenID Connect — група застосунків, серверний застосунок, спільний секрет, дозволені області та відповідна конфігурація digna.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, active directory federation services, adfs oidc, група застосунків, openid connect, локальний постачальник ідентичності
---

# Налаштування SSO з AD FS

Active Directory Federation Services — локальний варіант: токени видають ваші власні сервери, а URL виявлення містить ваше власне ім'я хоста. AD FS підтримує OpenID Connect, починаючи з **Windows Server 2016**.

Цей посібник охоплює **бік AD FS**: створення групи застосунків і збирання значень, потрібних digna. Бік digna — `dashboard_config.toml`, тестування та усунення несправностей — однаковий для всіх постачальників і описаний в [Огляді єдиного входу](overview.md).

---

## Перш ніж почати

| Вимога | Примітки |
|---|---|
| **Версія AD FS** | Windows Server 2016 або новіший — попередні версії не підтримують OIDC |
| **Доступ** | Локальний адміністратор на сервері AD FS |
| **Ім'я служби федерації** | наприклад, `adfs.yourdomain.com` |
| **URI перенаправлення digna** | URL, на який користувачі повертаються після входу, наприклад `https://digna.yourdomain.com/oidc/callback` |

---

## Крок 1: Створіть групу застосунків

1. На сервері AD FS відкрийте **AD FS Management**
2. Клацніть правою кнопкою миші **Application Groups** і виберіть **Add Application Group**
3. Введіть назву `digna`
4. У розділі **Standalone applications** — або **Client-Server applications**, залежно від версії, — виберіть **Server application accessing a web API**
5. Натисніть **Next**

---

## Крок 2: Налаштуйте серверний застосунок

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS генерує GUID. Скопіюйте його — це буде `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: введіть URL зворотного виклику digna і натисніть **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Натисніть **Next**

!!! warning "Натисніть Add, а не лише Next"

    Поле URI перенаправлення має власну кнопку **Add**. Якщо ввести URI і натиснути **Next**, не натиснувши **Add**, його буде відкинуто, а майстер не покаже жодного попередження. Перш ніж продовжити, переконайтеся, що URI з'явився у списку під полем.

---

## Крок 3: Згенеруйте спільний секрет

1. Позначте **Generate a shared secret**
2. Скопіюйте згенерований секрет → це буде `DIGNA_OIDC_CLIENT_SECRET`
3. Натисніть **Next**

!!! warning "Секрет показується лише один раз"

    AD FS показує спільний секрет лише на цій сторінці майстра і не може показати його повторно. Якщо ви його втратите, скиньте його пізніше у властивостях групи застосунків.

---

## Крок 4: Налаштуйте веб-API

1. **Identifier**: введіть той самий ідентифікатор клієнта з кроку 2 і натисніть **Add**
2. Натисніть **Next**
3. Виберіть **Access Control Policy** — *Permit everyone* є найпростішою відправною точкою; для робочого середовища обмежте доступ групою
4. Натисніть **Next**

---

## Крок 5: Надайте дозволені області

На кроці **Configure Application Permissions** позначте:

- `openid`
- `profile`
- `email`

Потім натисніть **Next** і завершіть роботу майстра.

!!! warning "openid не позначено за замовчуванням"

    У деяких версіях AD FS попередньо вибирає лише `user_impersonation`. Без `openid` кінцева точка токенів повертає токен доступу OAuth замість ID-токена, і digna не може ідентифікувати користувача.

---

## Крок 6: Перевірте кінцеву точку виявлення

Підставте ім'я своєї служби федерації:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Наприклад:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Відкрийте цю адресу в браузері. Документ JSON підтверджує, що OIDC увімкнено, а ім'я хоста правильне.

!!! note "Бекенд має довіряти сертифікату"

    Для AD FS часто використовується внутрішній центр сертифікації. Машина, на якій працює бекенд digna, сама виконує вихідний запит HTTPS до цього URL, тому центр сертифікації, що видав сертифікат, має бути в сховищі довірених сертифікатів цієї машини — а не лише в браузерах користувачів, які входять.

---

## Крок 7: Налаштуйте digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Login with Active Directory"
```

### `config.toml`

```toml
[oidc_clients.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

`key` в обох файлах має збігатися — тут це `adfs`.

---

## Крок 8: Тестування

Перезапустіть бекенд і вебсервер, потім відкрийте дашборд. Повний контрольний список див. у розділі [Тестування входу](overview.md#testing-login).

---

## Усунення несправностей AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

Ідентифікатор веб-API з кроку 4 не збігається з ідентифікатором клієнта, або області з кроку 5 не надано. Обидва параметри можна змінити у властивостях групи застосунків.

### MSIS9602: Invalid redirect_uri

URI було введено, але не додано кнопкою **Add**, або він відрізняється від `DIGNA_OIDC_REDIRECT_URI`. Перевірте **Application Groups → digna → digna backend → Properties**.

### ID-токен не повертається

В дозволах застосунку бракує області `openid`.

### Бекенд не може звернутися до URL виявлення

Або DNS на хості бекенду не розпізнає ім'я служби федерації, або сертифікат AD FS там не є довіреним. Перевірте це командою `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` безпосередньо із сервера digna.

### Події для перевірки

Сервер AD FS записує збої в **Applications and Services Logs → AD FS → Admin** у засобі перегляду подій (Event Viewer), зазвичай із конкретнішою причиною, ніж показує браузер.

---

## Див. також

- [Огляд єдиного входу](overview.md) — довідник з конфігурації, тестування та загальне усунення несправностей
- [Microsoft: сценарії AD FS OpenID Connect](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)

# Налаштування SSO з Keycloak

Keycloak — постачальник ідентичності з власним хостингом, повністю сумісний з OIDC. Оскільки ви запускаєте його самостійно, URL виявлення складається з вашого власного імені хоста та realm, а не з домену постачальника.

Цей посібник охоплює **бік Keycloak**: створення клієнта та збирання значень, потрібних digna. Бік digna — `dashboard_config.toml`, тестування та усунення несправностей — однаковий для всіх постачальників і описаний в [Огляді єдиного входу](overview.md).

---

## Перш ніж почати

| Вимога | Примітки |
|---|---|
| **Версія Keycloak** | 17 або новіша для використаних тут шляхів URL — див. примітку в кроці 5 |
| **Роль у Keycloak** | `realm-admin` у цільовому realm або адміністратор сервера |
| **Realm** | Realm, до якого належать користувачі digna, не обов'язково `master` |
| **URI перенаправлення digna** | URL, на який користувачі повертаються після входу, наприклад `https://digna.yourdomain.com/oidc/callback` |

---

## Крок 1: Виберіть realm

1. Відкрийте консоль адміністратора Keycloak
2. За допомогою селектора realm у верхньому лівому куті перейдіть до realm, у якому знаходяться ваші користувачі

!!! warning "Не використовуйте realm master"

    Realm `master` призначений для адміністрування самого Keycloak. Клієнти застосунків мають розміщуватися в окремому realm; якщо помістити digna в `master`, її користувачі отримають шлях до консолі адміністрування Keycloak.

---

## Крок 2: Створіть клієнта

1. Перейдіть до **Clients** і натисніть **Create client**
2. Налаштуйте:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — це буде `DIGNA_OIDC_CLIENT_ID`
3. Натисніть **Next**
4. На кроці **Capability config** увімкніть **Client authentication** (**On**)
5. Залиште **Standard flow** увімкненим; інші потоки не потрібні
6. Натисніть **Next**

!!! warning "Client Authentication має бути ввімкнено"

    Якщо **Client authentication** вимкнено, Keycloak створює *публічного* клієнта, який не має жодних облікових даних — вкладки **Credentials** з кроку 4 не буде. digna потрібен конфіденційний клієнт. Якщо ви помилилися, цей перемикач можна змінити після створення.

---

## Крок 3: Установіть URI перенаправлення

На кроці **Login settings** (або згодом на вкладці **Settings**):

1. **Valid redirect URIs**: введіть URL зворотного виклику digna:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: залиште порожнім або встановіть `+`, щоб віддзеркалити URI перенаправлення
3. Натисніть **Save**

!!! tip "Уникайте шаблонів із символами підстановки"

    Keycloak приймає шаблони на кшталт `https://digna.yourdomain.com/*`. Символ підстановки дозволяє будь-якому шляху на цьому хості отримати код авторизації, тому краще вказувати точний URL зворотного виклику.

---

## Крок 4: Отримайте секрет клієнта

1. Відкрийте вкладку **Credentials**
2. Переконайтеся, що **Client Authenticator** має значення *Client Id and Secret*
3. Скопіюйте **Client secret** → це буде `DIGNA_OIDC_CLIENT_SECRET`

Секрет можна отримати тут і пізніше, а також згенерувати заново кнопкою **Regenerate**.

---

## Крок 5: Складіть URL виявлення

Підставте свій хост Keycloak та назву realm:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Наприклад:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 і старіші містять /auth"

    До Keycloak 17 кожна кінцева точка розміщувалася під префіксом `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Дистрибутиви, у яких встановлено `KC_HTTP_RELATIVE_PATH=/auth`, зберігають стару структуру і в поточних версіях. Якщо URL без `/auth` повертає 404, спробуйте з ним.

Перш ніж продовжити, відкрийте URL у браузері. Документ JSON підтверджує, що хост і realm правильні.

---

## Крок 6: Налаштуйте digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc_clients.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

`key` в обох файлах має збігатися — тут це `keycloak`. Зверніть увагу: він не обов'язково має дорівнювати **Client ID** у Keycloak, хоча однакові значення простіше відстежувати.

---

## Крок 7: Тестування

Перезапустіть бекенд і вебсервер, потім відкрийте дашборд. Повний контрольний список див. у розділі [Тестування входу](overview.md#testing-login).

---

## Усунення несправностей Keycloak

### Invalid parameter: redirect_uri

URL зворотного виклику не охоплено **Valid redirect URIs**. Keycloak записує отриманий URI в журнал сервера — це найшвидший спосіб побачити точну невідповідність.

### Вкладка Credentials відсутня

Клієнт публічний. Увімкніть **Client authentication** у **Settings → Capability config**.

### 404 для URL виявлення

Або назва realm неправильна, або розгортання використовує префікс `/auth`. Перевірте список realm у консолі адміністратора і спробуйте обидві форми URL.

### unauthorized_client або invalid_client

**Standard flow** вимкнено в **Capability config**, або секрет було згенеровано заново в Keycloak без оновлення `config.toml`.

### Помилки сертифіката з боку бекенду

Keycloak із власним хостингом за приватним або самопідписаним сертифікатом не пройде вихідний запит HTTPS від digna до URL виявлення. Встановіть центр сертифікації, що видав сертифікат, у сховище довірених сертифікатів машини, на якій працює бекенд digna.

---

## Див. також

- [Огляд єдиного входу](overview.md) — довідник з конфігурації, тестування та загальне усунення несправностей
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)
---
title: Keycloak SSO – интеграция Single Sign-On | digna Documentation
description: Настройте Single Sign-On для digna с Keycloak с помощью OpenID Connect — настройка realm и клиента, аутентификация клиента, допустимые redirect URI, client secret и соответствующая конфигурация digna.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, конфиденциальный клиент, openid connect, собственный провайдер идентификации
---

# Настройка SSO с Keycloak

Keycloak — это самостоятельно размещаемый (self-hosted) провайдер идентификации, полностью совместимый с OIDC. Поскольку вы управляете им сами, discovery URL формируется из вашего собственного имени хоста и realm, а не из домена поставщика.

Это руководство покрывает **сторону Keycloak**: создание клиента и сбор значений, необходимых digna. Сторона digna — `dashboard_config.toml`, тестирование и устранение неполадок — одинакова для всех провайдеров и описана в [обзоре Single Sign-On](overview.md).

---

## Прежде чем начать

| Требование | Примечания |
|---|---|
| **Версия Keycloak** | 17 или новее для путей URL, используемых здесь, — см. примечание в Шаге 5 |
| **Роль в Keycloak** | `realm-admin` в целевом realm или администратор сервера |
| **Realm** | Realm, к которому относятся пользователи digna, — не обязательно `master` |
| **digna redirect URI** | URL, на который пользователи возвращаются после входа, например `https://digna.yourdomain.com/oidc/callback` |

---

## Шаг 1: Выберите realm

1. Откройте консоль администратора Keycloak
2. С помощью переключателя realm в левом верхнем углу перейдите в realm, в котором находятся ваши пользователи

!!! warning "Не используйте realm master"

    Realm `master` предназначен для администрирования самого Keycloak. Клиенты приложений должны находиться в отдельном realm; если разместить digna в `master`, её пользователи получат путь в консоль администрирования Keycloak.

---

## Шаг 2: Создайте клиента

1. Перейдите в **Clients** и нажмите **Create client**
2. Настройте:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — становится `DIGNA_OIDC_CLIENT_ID`
3. Нажмите **Next**
4. На шаге **Capability config** переключите **Client authentication** в положение **On**
5. Оставьте **Standard flow** включённым; остальные потоки не нужны
6. Нажмите **Next**

!!! warning "Client authentication должен быть включён"

    Если **Client authentication** выключен, Keycloak создаёт *публичного* клиента, у которого вообще нет учётных данных, — вкладки **Credentials** из Шага 4 не будет. digna нужен конфиденциальный клиент. Если вы ошиблись, этот переключатель можно изменить после создания.

---

## Шаг 3: Укажите Redirect URI

На шаге **Login settings** (или позже на вкладке **Settings**):

1. **Valid redirect URIs**: введите ваш callback URL для digna:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: оставьте пустым или укажите `+`, чтобы использовать те же значения, что и в redirect URI
3. Нажмите **Save**

!!! tip "Избегайте подстановочных знаков"

    Keycloak принимает шаблоны вида `https://digna.yourdomain.com/*`. Подстановочный знак позволяет любому пути на этом хосте получить код авторизации, поэтому лучше указывать точный callback URL.

---

## Шаг 4: Скопируйте client secret

1. Откройте вкладку **Credentials**
2. Убедитесь, что для **Client Authenticator** выбрано *Client Id and Secret*
3. Скопируйте **Client secret** → становится `DIGNA_OIDC_CLIENT_SECRET`

Секрет остаётся доступным здесь, и его можно сгенерировать заново кнопкой **Regenerate**.

---

## Шаг 5: Сформируйте Discovery URL

Подставьте ваш хост Keycloak и имя realm:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Например:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 и более ранние версии используют /auth"

    До Keycloak 17 все endpoint находились под префиксом `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Дистрибутивы, в которых задано `KC_HTTP_RELATIVE_PATH=/auth`, сохраняют старую структуру и в текущих версиях. Если URL без `/auth` возвращает 404, попробуйте с ним.

Прежде чем продолжить, откройте URL в браузере. Если отображается JSON-документ, хост и realm указаны верно.

---

## Шаг 6: Настройте digna

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

Поле `key` в обоих файлах должно совпадать — здесь это `keycloak`. Обратите внимание, что оно не обязано совпадать с **Client ID** в Keycloak, хотя одинаковые значения проще отслеживать.

---

## Шаг 7: Тестирование

Перезапустите бэкенд и веб-сервер, затем откройте панель управления. Полный чеклист см. в разделе [Тестирование входа](overview.md#testing-login).

---

## Устранение неполадок с Keycloak

### Invalid parameter: redirect_uri

Callback URL не входит в **Valid redirect URIs**. Keycloak записывает полученный URI в журнал сервера — это самый быстрый способ увидеть точное расхождение.

### Отсутствует вкладка Credentials

Клиент является публичным. Включите **Client authentication** в **Settings → Capability config**.

### 404 при обращении к Discovery URL

Либо неверно указано имя realm, либо в развёртывании используется префикс `/auth`. Проверьте список realm в консоли администратора и попробуйте обе формы URL.

### unauthorized_client или invalid_client

**Standard flow** отключён в **Capability config**, или секрет был сгенерирован заново в Keycloak без обновления `config.toml`.

### Ошибки сертификата на бэкенде

Самостоятельно размещённый Keycloak с частным или самоподписанным сертификатом приведёт к сбою исходящего HTTPS-запроса digna к discovery URL. Установите сертификат выпускающего центра сертификации (CA) в хранилище доверенных сертификатов машины, на которой работает бэкенд digna.

---

## См. также

- [Обзор Single Sign-On](overview.md) — справочник по конфигурации, тестированию и общему устранению неполадок
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)

---
title: Okta SSO – интеграция Single Sign-On | digna Documentation
description: Настройте Single Sign-On для digna с Okta с помощью OpenID Connect — интеграция приложения, sign-in redirect URI, учётные данные клиента, выбор сервера авторизации и соответствующая конфигурация digna.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, интеграция приложения, сервер авторизации, openid connect, корпоративная аутентификация
---

# Настройка SSO с Okta

Okta совместим с OIDC, но с одной особенностью, на которой спотыкается большинство первых интеграций: организация (org) Okta предоставляет несколько серверов авторизации, и у каждого свой discovery URL.

Это руководство покрывает **сторону Okta**: создание интеграции приложения и сбор значений, необходимых digna. Сторона digna — `dashboard_config.toml`, тестирование и устранение неполадок — одинакова для всех провайдеров и описана в [обзоре Single Sign-On](overview.md).

---

## Прежде чем начать

| Требование | Примечания |
|---|---|
| **Роль в Okta** | Super Administrator или роль администратора с правом создавать интеграции приложений |
| **Домен Okta** | например `yourcompany.okta.com` или пользовательский домен, если он настроен |
| **digna redirect URI** | URL, на который пользователи возвращаются после входа, например `https://digna.yourdomain.com/oidc/callback` |

---

## Шаг 1: Создайте интеграцию приложения

1. Войдите в Okta Admin Console
2. Перейдите в **Applications → Applications**
3. Нажмите **Create App Integration**
4. Выберите:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Нажмите **Next**

!!! warning "Тип приложения нельзя изменить"

    Если выбрать *Single-Page Application* вместо *Web Application*, будет создан публичный клиент без секрета, и обмен кода на бэкенде digna завершится ошибкой `invalid_client`. Тип фиксируется при создании — при неверном выборе придётся удалить приложение и начать заново.

---

## Шаг 2: Настройте интеграцию

1. **App integration name**: `digna`
2. **Grant type**: оставьте выбранным *Authorization Code*
3. **Sign-in redirect URIs**: введите ваш callback URL для digna:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: необязательно
5. В разделе **Assignments** выберите, кто может использовать интеграцию, — конкретная группа безопаснее, чем *Allow everyone in your organization to access*
6. Нажмите **Save**

!!! note "Назначение обязательно"

    Okta аутентифицирует пользователя, а затем проверяет, назначен ли он приложению. Неназначенный пользователь попадает на страницу входа Okta, успешно входит и получает отказ при перенаправлении обратно. Если вход работает у вас, но не у коллег, в первую очередь проверьте назначения.

---

## Шаг 3: Соберите учётные данные

На вкладке приложения **General**, в разделе **Client Credentials**:

- **Client ID** → становится `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → становится `DIGNA_OIDC_CLIENT_SECRET` (нажмите значок глаза, чтобы показать)

---

## Шаг 4: Выберите сервер авторизации

Именно этот шаг определяет ваш discovery URL. Перейдите в **Security → API**, чтобы увидеть серверы авторизации вашей организации.

**Org authorization server** — выдаёт токены для самой организации Okta:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — в том числе сервер с именем `default`, который создаёт Okta:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Для встроенного сервера `<auth_server_id>` — это буквально `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Какой выбрать?"

    Используйте сервер авторизации **org**, если только ваша организация уже не использует стандартно пользовательский сервер для политик доступа к API. В учётных записях Okta Developer по умолчанию используется `default`; во многих корпоративных организациях он отключён. Откройте оба URL в браузере — тот, что возвращает JSON, а не ошибку, вам и доступен.

---

## Шаг 5: Настройте digna

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

Поле `key` в обоих файлах должно совпадать — здесь это `okta`.

---

## Шаг 6: Тестирование

Перезапустите бэкенд и веб-сервер, затем откройте панель управления. Полный чеклист см. в разделе [Тестирование входа](overview.md#testing-login).

---

## Устранение неполадок с Okta

### The redirect URI Is Not Registered

Okta указывает проблемный URI в сообщении об ошибке. Сравните его с **General → Sign-in redirect URIs**; Okta сравнивает строку целиком, включая завершающую косую черту.

### User Is Not Assigned to the Client Application

Учётная запись отсутствует в списке назначений приложения. Добавьте пользователя или его группу в разделе **Assignments**.

### 400 Bad Request: Invalid Authorization Server

`<auth_server_id>` в discovery URL не существует — чаще всего это `default` в организации, где он был удалён. Проверьте в **Security → API**, какие серверы действительно доступны.

### invalid_client на этапе получения токена

Интеграция была создана как Single-Page Application и не имеет client secret. Создайте её заново как Web Application.

---

## См. также

- [Обзор Single Sign-On](overview.md) — справочник по конфигурации, тестированию и общему устранению неполадок
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)

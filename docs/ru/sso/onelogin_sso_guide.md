---
title: OneLogin SSO – интеграция Single Sign-On | digna Documentation
description: Настройте Single Sign-On для digna с OneLogin с помощью OpenID Connect — создание OIDC-приложения, redirect URI, учётные данные клиента, аутентификация на token endpoint и соответствующая конфигурация digna.
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, аутентификация token endpoint, корпоративная аутентификация
---

# Настройка SSO с OneLogin

OneLogin совместим с OIDC. Его отличительная особенность в том, что тип коннектора выбирается из каталога при создании приложения и не может быть изменён впоследствии.

Это руководство покрывает **сторону OneLogin**: создание приложения и сбор значений, необходимых digna. Сторона digna — `dashboard_config.toml`, тестирование и устранение неполадок — одинакова для всех провайдеров и описана в [обзоре Single Sign-On](overview.md).

---

## Прежде чем начать

| Требование | Примечания |
|---|---|
| **Роль в OneLogin** | Владелец учётной записи или администратор с правом добавлять приложения |
| **Поддомен** | например `yourcompany.onelogin.com` |
| **digna redirect URI** | URL, на который пользователи возвращаются после входа, например `https://digna.yourdomain.com/oidc/callback` |

---

## Шаг 1: Создайте OIDC-приложение

1. Войдите в портал администратора OneLogin (Admin portal)
2. Перейдите в **Applications → Applications**
3. Нажмите **Add App**
4. Найдите `OpenId Connect` и выберите коннектор **OpenId Connect (OIDC)**
5. Укажите **Display Name** `digna`
6. Нажмите **Save**

!!! warning "Тип коннектора фиксируется при создании"

    В каталоге OneLogin есть отдельные записи для SAML и OIDC, и приложение нельзя преобразовать из одного типа в другой. Если вы по ошибке выбрали коннектор SAML, удалите приложение и добавьте его заново — настройки для переключения протокола нет.

---

## Шаг 2: Укажите Redirect URI

1. Откройте вкладку **Configuration**
2. В поле **Redirect URI's** введите ваш callback URL для digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. При желании укажите **Post Logout Redirect URIs** как URL панели управления
4. Нажмите **Save**

!!! note "Один URI на строку"

    В отличие от провайдеров, которые ожидают список через запятую, поле **Redirect URI's** в OneLogin принимает по одному URI на строку.

---

## Шаг 3: Задайте тип приложения и метод аутентификации

1. Откройте вкладку **SSO**
2. Убедитесь, что для **Application Type** выбрано *Web*
3. Установите для **Token Endpoint → Authentication Method** значение *POST* (`client_secret_post`) или *Basic* (`client_secret_basic`)

!!! warning "Не выбирайте None"

    Если выбрать метод аутентификации *None*, приложение станет публичным клиентом без секрета, и обмен кода на бэкенде digna будет отклонён. Подходит как POST, так и Basic.

---

## Шаг 4: Соберите учётные данные

По-прежнему на вкладке **SSO**:

- **Client ID** → становится `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → становится `DIGNA_OIDC_CLIENT_SECRET` (нажмите **Show client secret**)

На странице также показан **Issuer URL**, по которому можно проверить discovery URL на следующем шаге.

---

## Шаг 5: Назначьте пользователей

1. Откройте вкладку **Access**
2. Добавьте роли или группы, участники которых могут пользоваться digna
3. Нажмите **Save**

!!! note "Неназначенные пользователи получают отказ после входа"

    Как и большинство провайдеров, OneLogin сначала аутентифицирует пользователя, а затем проверяет его права. Неназначенный пользователь успешно входит и затем получает отказ, что выглядит как ошибка digna, а не как решение системы контроля доступа.

---

## Шаг 6: Сформируйте Discovery URL

Подставьте ваш поддомен OneLogin:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Например:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 — это версия API"

    Текущая реализация OIDC в OneLogin находится под `/oidc/2/`. В старой документации указан `/oidc/` без версии, что ведёт на выведенную из эксплуатации первую версию. Если сомневаетесь, проверьте **Issuer URL** на вкладке SSO — discovery URL равен issuer плюс `/.well-known/openid-configuration`.

---

## Шаг 7: Настройте digna

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

Поле `key` в обоих файлах должно совпадать — здесь это `onelogin`.

---

## Шаг 8: Тестирование

Перезапустите бэкенд и веб-сервер, затем откройте панель управления. Полный чеклист см. в разделе [Тестирование входа](overview.md#testing-login).

---

## Устранение неполадок с OneLogin

### redirect_uri did not match

Callback URL отсутствует в **Configuration → Redirect URI's**, или записи разделены запятыми, а не переводами строк.

### invalid_client на этапе получения токена

Для **Token Endpoint → Authentication Method** установлено *None*, или client secret в `config.toml` устарел. Покажите секрет на вкладке **SSO** и сравните.

### Приложение не отображается у пользователей

Ни одной роли или группе не предоставлен доступ на вкладке **Access**.

### 404 при обращении к Discovery URL

Неверно указан поддомен, или в URL отсутствует `/oidc/2/`. Сравните с **Issuer URL** на вкладке SSO.

---

## См. также

- [Обзор Single Sign-On](overview.md) — справочник по конфигурации, тестированию и общему устранению неполадок
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)

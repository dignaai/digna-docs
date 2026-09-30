---
title: PingOne SSO – интеграция Single Sign-On | digna Documentation
description: Настройте Single Sign-On для digna с PingOne с помощью OpenID Connect — настройка OIDC Web App, redirect URI, учётные данные клиента, идентификатор среды, региональные домены и соответствующая конфигурация digna.
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, идентификатор среды, openid connect, корпоративная аутентификация
---

# Настройка SSO с PingOne

PingOne совместим с OIDC. Два его значения требуют внимания: **идентификатор среды** (environment ID), который входит в URL каждого endpoint, и **региональный домен**, который различается для тенантов в Северной Америке, Европе, Канаде, Азиатско-Тихоокеанском регионе и Австралии.

Это руководство покрывает **сторону PingOne**: создание приложения и сбор значений, необходимых digna. Сторона digna — `dashboard_config.toml`, тестирование и устранение неполадок — одинакова для всех провайдеров и описана в [обзоре Single Sign-On](overview.md).

---

## Прежде чем начать

| Требование | Примечания |
|---|---|
| **Роль в PingOne** | Environment Admin или Identity Data Admin в целевой среде |
| **Среда** | Среда PingOne, к которой относятся пользователи digna |
| **digna redirect URI** | URL, на который пользователи возвращаются после входа, например `https://digna.yourdomain.com/oidc/callback` |

---

## Шаг 1: Создайте приложение

1. Войдите в консоль администратора PingOne и выберите вашу среду
2. Перейдите в **Applications → Applications**
3. Нажмите кнопку **+**
4. Введите `digna` в поле **Application Name**
5. Выберите **OIDC Web App**
6. Нажмите **Save**

!!! warning "Выбирайте OIDC Web App, а не Single-Page App"

    *Single-Page App* и *Native App* создают публичных клиентов, которые не могут хранить секрет. digna обменивает код авторизации на своём бэкенде, и ей нужен конфиденциальный тип **OIDC Web App**.

---

## Шаг 2: Укажите Redirect URI

1. Откройте вкладку приложения **Configuration**
2. Нажмите значок карандаша, чтобы перейти к редактированию
3. Убедитесь, что **Response Type** — *Code*, а **Grant Type** — *Authorization Code*
4. В разделе **Redirect URIs** введите ваш callback URL для digna:

```
https://digna.yourdomain.com/oidc/callback
```

5. Установите для **Token Endpoint Authentication Method** значение *Client Secret Post* или *Client Secret Basic*
6. Нажмите **Save**

---

## Шаг 3: Включите приложение

В строке приложения или на его панели сведений переведите переключатель в положение **enabled**.

!!! warning "Новые приложения создаются отключёнными"

    PingOne создаёт приложения в отключённом состоянии. Отключённое приложение вызывает на этапе авторизации ошибку, в которой переключатель не упоминается, поэтому стоит проверить его, прежде чем отлаживать что-либо ещё.

---

## Шаг 4: Предоставьте scope

1. Откройте вкладку **Resources**
2. Убедитесь, что `openid` предоставлен, и добавьте `profile` и `email` из ресурса **OpenID Connect**
3. Нажмите **Save**

---

## Шаг 5: Назначьте пользователей

1. Откройте вкладку **Access**
2. Добавьте популяцию (population) или группы, участники которых могут пользоваться digna
3. Нажмите **Save**

---

## Шаг 6: Соберите учётные данные и идентификатор среды

На вкладке **Configuration** разверните раздел **General**:

- **Client ID** → становится `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → становится `DIGNA_OIDC_CLIENT_SECRET` (нажмите значок глаза)
- **Environment ID** → используется в discovery URL

На этой же вкладке указан готовый **OIDC Discovery Endpoint**, который можно скопировать напрямую, а не собирать вручную.

---

## Шаг 7: Сформируйте Discovery URL

Подставьте идентификатор среды и домен вашего региона:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Регион | Домен |
|---|---|
| Северная Америка | `auth.pingone.com` |
| Европа | `auth.pingone.eu` |
| Канада | `auth.pingone.ca` |
| Азиатско-Тихоокеанский регион | `auth.pingone.asia` |
| Австралия | `auth.pingone.com.au` |

Для европейской среды:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Копируйте, а не вводите вручную"

    Региональный домен — самая распространённая ошибка при интеграции с PingOne, а неверный регион даёт ошибку 404 вместо понятного сообщения. Используйте значение **OIDC Discovery Endpoint** из Шага 6.

---

## Шаг 8: Настройте digna

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

Поле `key` в обоих файлах должно совпадать — здесь это `pingone`.

---

## Шаг 9: Тестирование

Перезапустите бэкенд и веб-сервер, затем откройте панель управления. Полный чеклист см. в разделе [Тестирование входа](overview.md#testing-login).

---

## Устранение неполадок с PingOne

### 404 при обращении к Discovery URL

Неверно указан региональный домен или идентификатор среды. Сравните с **OIDC Discovery Endpoint** на вкладке приложения Configuration.

### NOT_FOUND или приложение отключено

Переключатель приложения из Шага 3 по-прежнему выключен.

### Несоответствие Redirect URI

PingOne сравнивает строку целиком. Проверьте **Configuration → Redirect URIs** на наличие завершающей косой черты или различия в схеме.

### Вход выполнен, но claim email не доходит до digna

Scope `email` и `profile` не предоставлены на вкладке **Resources**.

### Пользователь не видит приложение

Ни одной популяции или группе не предоставлен доступ на вкладке **Access**.

---

## См. также

- [Обзор Single Sign-On](overview.md) — справочник по конфигурации, тестированию и общему устранению неполадок
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)

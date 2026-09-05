---
title: Настройка SSO AD FS — интеграция Single Sign-On | digna Documentation
description: Настройте Single Sign-On для digna с помощью Active Directory Federation Services через OpenID Connect — группа приложений, серверное приложение, общий секрет, разрешённые scope и соответствующая конфигурация digna.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, службы федерации Active Directory, adfs oidc, группа приложений, openid connect, on-premises identity provider
---

# Настройка SSO с AD FS

Active Directory Federation Services — это on-premises вариант: ваши собственные серверы выдаёт токены, а discovery URL — это ваше собственное имя хоста. AD FS поддерживает OpenID Connect, начиная с **Windows Server 2016**.

Это руководство покрывает **сторону AD FS**: создание группы приложений и сбор значений, необходимых digna. Сторона digna — `dashboard_config.toml`, тестирование и устранение неполадок — одинаковы для любого провайдера и описаны в [Single Sign-On Overview](overview.md).

---

## Прежде чем начать

| Требование | Примечания |
|---|---|
| **Версия AD FS** | Windows Server 2016 или новее — в более ранних версиях поддержки OIDC нет |
| **Доступ** | Локальный администратор на сервере AD FS |
| **Имя службы федерации** | например `adfs.yourdomain.com` |
| **URI перенаправления digna** | URL, на который пользователи возвращаются после входа, например `https://digna.yourdomain.com/oidc/callback` |

---

## Шаг 1: Создание группы приложений

1. На сервере AD FS откройте **AD FS Management**
2. Щёлкните правой кнопкой **Application Groups** и выберите **Add Application Group**
3. Введите `digna` в поле имени
4. В разделе **Standalone applications** — или **Client-Server applications** в зависимости от версии — выберите **Server application accessing a web API**
5. Нажмите **Next**

---

## Шаг 2: Настройка серверного приложения

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS сгенерирует GUID. Скопируйте его — это станет `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: введите ваш callback URL для digna и нажмите **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Нажмите **Next**

!!! warning "Нажмите Add, а не только Next"

    Поле Redirect URI имеет собственную кнопку **Add**. Если ввести URI и нажать **Next**, не нажав **Add**, он не будет сохранён, и мастер не покажет предупреждение. Убедитесь, что URI отображается в списке под полем перед продолжением.

---

## Шаг 3: Генерация общего секрета

1. Отметьте **Generate a shared secret**
2. Скопируйте сгенерированный секрет → он становится `DIGNA_OIDC_CLIENT_SECRET`
3. Нажмите **Next**

!!! warning "Секрет показывается только один раз"

    AD FS отображает общий секрет только на этой странице мастера и больше не может показать его снова. Если вы его потеряете, сбросьте секрет позднее в свойствах группы приложений.

---

## Шаг 4: Настройка Web API

1. **Identifier**: введите тот же client identifier, что и в Шаге 2, и нажмите **Add**
2. Нажмите **Next**
3. Выберите **Access Control Policy** — *Permit everyone* — самый простой старт; для продакшна ограничьте доступ группой
4. Нажмите **Next**

---

## Шаг 5: Предоставление разрешённых scope

На шаге **Configure Application Permissions** отметьте:

- `openid`
- `profile`
- `email`

Затем нажмите **Next** и завершите мастер.

!!! warning "openid не отмечен по умолчанию"

    В некоторых версиях AD FS предвыбрано только `user_impersonation`. Без `openid` endpoint токена вернёт OAuth access token, а не ID token, и digna не сможет идентифицировать пользователя.

---

## Шаг 6: Подтвердите endpoint обнаружения

Подставьте имя вашей службы федерации:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Например:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Откройте его в браузере. JSON-документ подтвердит, что OIDC включён и имя хоста указано правильно.

!!! note "Бэкенд должен доверять сертификату"

    Внутренний центр сертификации часто используется для AD FS. Машина, на которой запущен бэкенд digna, сама делает исходящий HTTPS-запрос к этому URL, поэтому issuing CA должен быть в хранилище доверенных центров этой машины — не только в браузерах пользователей.

---

## Шаг 7: Настройте digna

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
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Значение `key` в обоих файлах должно совпадать — здесь `adfs`.

---

## Шаг 8: Тестирование

Перезапустите бэкенд и веб-сервер, затем откройте панель управления. См. [Testing Login](overview.md#testing-login) для полного чеклиста.

---

## Устранение неполадок AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

Идентификатор Web API в Шаге 4 не совпадает с client identifier, или в Шаге 5 не были предоставлены нужные scope. Обе настройки можно изменить в свойствах группы приложений.

### MSIS9602: Invalid redirect_uri

URI был введён, но не добавлен через кнопку **Add**, либо отличается от `DIGNA_OIDC_REDIRECT_URI`. Проверьте **Application Groups → digna → digna backend → Properties**.

### ID Token не возвращается

В разрешениях приложения отсутствует scope `openid`.

### Бэкенд не может достучаться до discovery URL

Либо DNS на хосте бэкенда не разрешает имя службы федерации, либо сертификат AD FS там не доверен. Проверьте с помощью `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` непосредственно с сервера digna.

### События для проверки

Сервер AD FS записывает ошибки в **Applications and Services Logs → AD FS → Admin** в Event Viewer, обычно с более конкретной причиной, чем показывает браузер.

---

## См. также

- [Single Sign-On Overview](overview.md) — справочник по конфигурации, тестированию и общему устранению неполадок
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
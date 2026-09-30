# Настройка SSO с Microsoft Entra ID

Microsoft Entra ID (ранее Azure Active Directory) — провайдер, полностью совместимый с OIDC, поэтому digna интегрируется с ним через стандартный discovery endpoint.

Это руководство покрывает **сторону Entra ID**: регистрацию приложения и сбор четырёх значений, необходимых digna. Сторона digna — `dashboard_config.toml`, тестирование и устранение неполадок — одинакова для всех провайдеров и описана в [обзоре Single Sign-On](overview.md).

---

## Прежде чем начать

| Требование | Примечания |
|---|---|
| **Роль в Entra ID** | Application Administrator, Cloud Application Administrator или Global Administrator |
| **digna redirect URI** | URL, на который пользователи возвращаются после входа, например `https://digna.yourdomain.com/oidc/callback` |
| **Тенант** | Каталог, в который входят ваши пользователи |

---

## Шаг 1: Зарегистрируйте приложение

1. Войдите в [Microsoft Entra admin center](https://entra.microsoft.com)
2. Перейдите в **Identity → Applications → App registrations**
3. Нажмите **New registration**
4. Настройте:
   - **Name**: `digna` (показывается пользователям на экране согласия)
   - **Supported account types**: *Accounts in this organizational directory only* для развёртывания с одним тенантом
5. В разделе **Redirect URI** выберите платформу **Web** и введите ваш callback URL для digna:

```
https://digna.yourdomain.com/oidc/callback
```

6. Нажмите **Register**

!!! warning "Важно"

    Платформа должна быть **Web**, а не *Single-page application*. digna обменивает код авторизации на бэкенде с помощью client secret, а тип платформы SPA этого не допускает.

---

## Шаг 2: Скопируйте идентификаторы клиента и тенанта

На странице приложения **Overview** скопируйте:

- **Application (client) ID** → становится `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → используется в discovery URL

---

## Шаг 3: Создайте client secret

1. Перейдите в **Certificates & secrets → Client secrets**
2. Нажмите **New client secret**
3. Введите описание и выберите срок действия
4. Нажмите **Add**
5. Сразу скопируйте значение из столбца **Value**

!!! warning "Копируйте Value, а не Secret ID"

    **Value** показывается только один раз, на этой странице, и позже его нельзя получить. **Secret ID** рядом с ним выглядит похоже, но секретом не является — при его использовании вход завершается ошибкой `invalid_client`. Если вы ушли со страницы, не скопировав значение, удалите секрет и создайте новый.

!!! tip "Совет"

    Entra ID ограничивает срок действия секрета 24 месяцами, поэтому у каждой интеграции SSO есть дата окончания действия. Запишите её там, где вы её увидите, — просроченный секрет отключает SSO сразу для всех пользователей, без какого-либо предупреждения на странице входа.

---

## Шаг 4: Проверьте разрешения API

1. Перейдите в **API permissions**
2. Убедитесь, что присутствует **Microsoft Graph → User.Read** (delegated) — оно добавляется по умолчанию

Scope `openid`, `profile` и `email`, которые запрашивает digna, входят в стандартный набор OIDC и не требуют отдельного предоставления. Если ваш тенант требует согласия администратора для всех приложений, нажмите **Grant admin consent for &lt;tenant&gt;**.

---

## Шаг 5: Сформируйте Discovery URL

Подставьте **Directory (tenant) ID** из Шага 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Используйте endpoint v2.0"

    Сегмент `/v2.0/` важен. Endpoint v1.0 по адресу `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` выдаёт токены в устаревшем формате и не возвращает стандартные claims OIDC, которые ожидает digna.

Прежде чем продолжить, откройте URL в браузере. Если отображается JSON-документ, идентификатор тенанта указан верно.

---

## Шаг 6: Настройте digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

Поле `key` в обоих файлах должно совпадать — здесь это `microsoft`.

---

## Шаг 7: Тестирование

Перезапустите бэкенд и веб-сервер, затем откройте панель управления. Полный чеклист см. в разделе [Тестирование входа](overview.md#testing-login).

---

## Устранение неполадок с Entra ID

### AADSTS50011: Redirect URI Mismatch

URI в `DIGNA_OIDC_REDIRECT_URI` отличается от зарегистрированного в Шаге 1. Entra ID сравнивает строку целиком, поэтому завершающая косая черта, `http` вместо `https` или другой порт — всё это считается несоответствием. Проверьте **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Либо скопирован **Secret ID** вместо **Value**, либо срок действия секрета истёк. Создайте новый секрет и скопируйте значение из столбца Value.

### AADSTS650057: Invalid Resource

Регистрация приложения удалена или относится к другому тенанту, чем указанный в discovery URL. Проверьте Directory (tenant) ID на странице Overview.

### Пользователи входят, но ничего не происходит

Если тенант требует согласия администратора, а оно не предоставлено, перенаправление возвращается без пригодного токена. Предоставьте согласие администратора в разделе **API permissions**.

---

## См. также

- [Обзор Single Sign-On](overview.md) — справочник по конфигурации, тестированию и общему устранению неполадок
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
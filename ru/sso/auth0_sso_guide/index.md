# Настройка SSO с Auth0

Auth0 совместим с OIDC и предоставляет discovery endpoint для каждого тенанта. Главное — правильно указать домен тенанта, он встречается в URL discovery и меняется, если вы включаете пользовательский домен.

Это руководство покрывает **сторону Auth0**: создание приложения и сбор значений, необходимых digna. Сторона digna — `dashboard_config.toml`, тестирование и устранение неполадок — одинакова для всех провайдеров и описана в [Single Sign-On Overview](overview.md).

---

## Прежде чем начать

| Требование | Примечания |
|---|---|
| **Роль в Auth0** | Администратор тенанта |
| **Домен тенанта** | например `yourcompany.eu.auth0.com` — сегмент региона важен |
| **digna redirect URI** | URL, на который пользователи возвращаются после входа, например `https://digna.yourdomain.com/oidc/callback` |

---

## Шаг 1: Создайте приложение

1. Войдите в [Auth0 Dashboard](https://manage.auth0.com)
2. Перейдите в **Applications → Applications**
3. Нажмите **Create Application**
4. Назовите его `digna` и выберите **Regular Web Applications**
5. Нажмите **Create**

!!! warning "Choose Regular Web Applications"

    *Single Page Application* и *Native* создают публичных клиентов без секрета. digna выполняет обмен кода на токен на бэкенде и требует конфиденциального клиента, поэтому правильный тип — **Regular Web Applications**. В отличие от некоторых провайдеров, Auth0 позволяет изменить тип позже в **Settings → Application Type**.

---

## Шаг 2: Добавьте Callback URL

На вкладке приложения **Settings**:

1. Найдите **Allowed Callback URLs**
2. Введите ваш callback URL для digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. При желании укажите **Allowed Logout URLs** как URL панели управления
4. Прокрутите вниз и нажмите **Save Changes**

!!! note "Comma-Separated, Not Newline-Separated"

    Auth0 принимает несколько callback URL в этом поле, разделённых запятыми. Список, разделённый только переводами строк, будет воспринят как один некорректный URL и ничего не совпадёт.

---

## Шаг 3: Соберите учётные данные

По-прежнему на вкладке **Settings**, в панели **Basic Information**:

- **Domain** → используется для формирования discovery URL
- **Client ID** → становится `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → становится `DIGNA_OIDC_CLIENT_SECRET` (щелкните, чтобы показать)

---

## Шаг 4: Подтвердите тип гранта

1. Перейдите в **Settings → Advanced Settings → Grant Types**
2. Убедитесь, что отмечен **Authorization Code**

Для Regular Web Applications он включён по умолчанию. Если он снят, вход в digna завершится ошибкой `unauthorized_client`.

---

## Шаг 5: Сформируйте Discovery URL

Подставьте **Domain** из Шага 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Например:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Custom Domains Change the Issuer"

    Если у вашего тенанта используется пользовательский домен, например `login.yourcompany.com`, используйте этот домен в discovery URL. Смешивание двух доменов — канонического домена в discovery URL и пользовательского в браузере — приводит к несоответствию issuer, и токен будет отклонён после успешного входа.

---

## Шаг 6: Настройте digna

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
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

Поле `key` в обоих файлах должно совпадать — здесь это `auth0`.

---

## Шаг 7: Тестирование

Перезапустите бэкенд и веб-сервер, затем откройте панель управления. Полный чеклист см. в [Testing Login](overview.md#testing-login).

---

## Устранение неполадок с Auth0

### Несоответствие Callback URL

Страница ошибки Auth0 показывает URL, который он получил. Добавьте его в **Allowed Callback URLs**, убедившись, что записи разделены запятыми.

### unauthorized_client

Не включён **Authorization Code** в **Advanced Settings → Grant Types**, или тип приложения не является Regular Web Applications.

### Доступ отклонён после успешного входа

Правило (Rule), Action или Post-Login триггер в тенанте отклоняет пользователя. Проверьте **Actions → Flows → Login** и логи тенанта в **Monitoring → Logs**, которые показывают точную причину.

### Несоответствие issuer

Discovery URL и домен, на который был отправлен браузер, различаются — обычно канонический домен тенанта и пользовательский домен. Используйте один и тот же домен последовательно.

---

## См. также

- [Single Sign-On Overview](overview.md) — справочник по конфигурации, тестированию и общему устранению неполадок
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
# Настройка SSO с Google Workspace

Платформа идентификации Google совместима с OIDC и использует один общий URL discovery для всех клиентов, поэтому единственные значения, зависящие от организации — это client ID и secret.

Это руководство охватывает **сторону Google**: создание OAuth-клиента и сбор значений, необходимых digna. Сторона digna — `dashboard_config.toml`, тестирование и отладка — одинакова для всех провайдеров и описана в [Обзор Single Sign-On](overview.md).

---

## Перед началом

| Требование | Примечания |
|---|---|
| **Google Cloud project** | Любой проект в той же организации, что и ваш домен Workspace |
| **Role** | Editor или Owner в проекте |
| **digna redirect URI** | URL, на который пользователи возвращаются после входа, например `https://digna.yourdomain.com/oidc/callback` |

---

## Шаг 1: Настройка OAuth consent screen

Google не выдаст учетные данные до тех пор, пока не будет создан экран согласия.

1. Откройте [Консоль Google Cloud](https://console.cloud.google.com) и выберите ваш проект
2. Перейдите в **APIs & Services → OAuth consent screen**
3. Выберите тип пользователя:
   - **Internal** — вход могут выполнять только аккаунты из вашего домена Workspace. Рекомендуется.
   - **External** — любой аккаунт Google может попытаться войти.
4. Заполните имя приложения, адрес поддержки пользователей и контактный email разработчика
5. На шаге **Scopes** добавьте `openid`, `.../auth/userinfo.email` и `.../auth/userinfo.profile`
6. Сохраните

!!! warning "Внешние приложения должны быть опубликованы"

    Экран согласия **External** по умолчанию имеет статус *Testing*, при котором вход смогут завершить только аккаунты, явно добавленные в список тестовых пользователей. Остальные увидят сообщение «digna has not completed the Google verification process». Либо переключите приложение в **In production** в разделе **Publishing status**, либо используйте **Internal** — у него нет такого ограничения и это правильный выбор для развертывания, ограниченного Workspace.

---

## Шаг 2: Создание OAuth-клиента

1. Перейдите в **APIs & Services → Credentials**
2. Нажмите **Create Credentials → OAuth client ID**
3. Установите **Application type** в значение **Web application**
4. Дайте ему имя, например `digna`
5. В разделе **Authorized redirect URIs** нажмите **Add URI** и введите:

```
https://digna.yourdomain.com/oidc/callback
```

6. Нажмите **Create**

!!! note "Указывать Authorized JavaScript origins не требуется"

    digna обменивается кодом авторизации с бэкенда, а не с браузера, поэтому поле **Authorized JavaScript origins** можно оставить пустым. Важен только redirect URI.

---

## Шаг 3: Получение учетных данных

В появившемся диалоговом окне после создания отображается:

- **Client ID** — заканчивается на `.apps.googleusercontent.com` → становится `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → становится `DIGNA_OIDC_CLIENT_SECRET`

Оба значения позже можно будет извлечь со страницы деталей учетных данных, в отличие от большинства других провайдеров.

---

## Шаг 4: Discovery URL

Google использует один discovery URL для всех клиентов — ничего заменять не нужно:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Шаг 5: Настройка digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Войти через Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Параметр `key` в обоих файлах должен совпадать — здесь это `google`.

---

## Шаг 6: Тестирование

Перезапустите бэкенд и веб-сервер, затем откройте дашборд. Смотрите [Тестирование входа](overview.md#testing-login) для полного чек-листа.

---

## Устранение неполадок в Google Workspace

### Error 400: redirect_uri_mismatch

URI в `DIGNA_OIDC_REDIRECT_URI` отсутствует в списке **Authorized redirect URIs** или отличается из‑за завершающего слеша или схемы. Страница ошибки Google показывает полученный URI — сравните его посимвольно с зарегистрированным.

### This App Is Blocked / Has Not Completed Verification

Экран согласия настроен как **External** и всё ещё в статусе *Testing*. Опубликуйте его или переключите приложение на **Internal**.

### Access Blocked: Authorization Error

Аккаунт, пытающийся войти, находится вне вашего домена Workspace, в то время как экран согласия — **Internal**. Это ожидаемое поведение — Internal-приложения принимают только аккаунты организации.

### Изменения применяются в течение нескольких минут

Google распространяет изменения учетных данных и экрана согласия асинхронно. Новый redirect URI может заработать через несколько минут; если изменение кажется проигнорированным, подождите и повторите попытку перед тем, как углубляться в расследование.

---

## См. также

- [Обзор Single Sign-On](overview.md) — справочник по конфигурации, тестированию и общей отладке
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
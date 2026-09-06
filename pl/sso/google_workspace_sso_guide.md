# Skonfiguruj SSO z Google Workspace

Platforma tożsamości Google jest zgodna z OIDC i używa jednego, dobrze znanego discovery URL dla każdego klienta, więc jedynymi wartościami specyficznymi dla organizacji są identyfikator klienta i sekret.

Ten przewodnik obejmuje **stronę Google**: tworzenie klienta OAuth i zebranie wartości, których potrzebuje digna. Strona digna — `dashboard_config.toml`, testowanie i rozwiązywanie problemów — jest taka sama dla każdego dostawcy i opisana w [Single Sign-On Overview](overview.md).

---

## Zanim zaczniesz

| Wymaganie | Uwagi |
|---|---|
| **Google Cloud project** | Dowolny projekt w tej samej organizacji co Twoja domena Workspace |
| **Role** | Editor lub Owner w projekcie |
| **digna redirect URI** | URL, na który użytkownicy wracają po logowaniu, np. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Skonfiguruj ekran zgody OAuth

Google nie wystawi poświadczeń, dopóki ekran zgody nie istnieje.

1. Otwórz [Google Cloud Console](https://console.cloud.google.com) i wybierz swój projekt
2. Przejdź do **APIs & Services → OAuth consent screen**
3. Wybierz typ użytkownika:
   - **Internal** — tylko konta w Twojej domenie Workspace mogą się logować. Zalecane.
   - **External** — każde konto Google może spróbować się zalogować.
4. Wypełnij nazwę aplikacji, adres e-mail wsparcia użytkownika oraz adres e-mail kontaktu dewelopera
5. Na kroku **Scopes** dodaj `openid`, `.../auth/userinfo.email` i `.../auth/userinfo.profile`
6. Zapisz

!!! warning "Aplikacje zewnętrzne muszą być opublikowane"

    Ekran zgody **External** rozpoczyna w statusie *Testing*, gdzie tylko konta wyraźnie dodane do listy testowych użytkowników mogą ukończyć logowanie. Wszyscy inni zobaczą "digna has not completed the Google verification process". Przełącz aplikację na **In production** w sekcji **Publishing status**, albo użyj **Internal** — które nie ma takiego ograniczenia i jest właściwym wyborem dla wdrożenia tylko dla Workspace.

---

## Krok 2: Utwórz klienta OAuth

1. Przejdź do **APIs & Services → Credentials**
2. Kliknij **Create Credentials → OAuth client ID**
3. Ustaw **Application type** na **Web application**
4. Nadaj mu nazwę, np. `digna`
5. W sekcji **Authorized redirect URIs** kliknij **Add URI** i wpisz:

```
https://digna.yourdomain.com/oidc/callback
```

6. Kliknij **Create**

!!! note "Nie są wymagane Authorized JavaScript origins"

    digna wymienia kod autoryzacji z backendu, nie z przeglądarki, więc pole **Authorized JavaScript origins** można pozostawić puste. Liczy się tylko redirect URI.

---

## Krok 3: Zbierz poświadczenia

Dialog, który pojawia się po utworzeniu, pokazuje:

- **Client ID** — kończy się na `.apps.googleusercontent.com` → staje się `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → staje się `DIGNA_OIDC_CLIENT_SECRET`

Obie wartości pozostają dostępne później na stronie szczegółów poświadczenia, w przeciwieństwie do większości innych dostawców.

---

## Krok 4: URL discovery

Google używa jednego discovery URL dla wszystkich klientów — nic nie trzeba podstawiać:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Krok 5: Skonfiguruj digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Klucz `key` w obu plikach musi się zgadzać — tutaj `google`.

---

## Krok 6: Testuj

Zrestartuj backend i serwer WWW, a następnie otwórz dashboard. Zobacz [Testowanie logowania](overview.md#testing-login) po pełną listę kontrolną.

---

## Rozwiązywanie problemów z Google Workspace

### Błąd 400: redirect_uri_mismatch

URI w `DIGNA_OIDC_REDIRECT_URI` nie znajduje się na liście **Authorized redirect URIs**, albo różni się znakiem końcowym (ukośnikiem) lub schematem. Strona błędu Google pokazuje URI, które otrzymała — porównaj je znak po znaku z zarejestrowanym.

### Ta aplikacja jest zablokowana / Nie zakończyła weryfikacji

Ekran zgody jest **External** i nadal w stanie *Testing*. Opublikuj go lub przełącz aplikację na **Internal**.

### Access Blocked: Authorization Error

Konto próbujące się zalogować znajduje się poza Twoją domeną Workspace, podczas gdy ekran zgody jest ustawiony na **Internal**. To zamierzone zachowanie — aplikacje Internal akceptują tylko konta z organizacji.

### Zmiany wymagają kilku minut

Google rozprowadza zmiany poświadczeń i ekranu zgody asynchronicznie. Nowo dodane redirect URI może potrzebować kilku minut, by zacząć działać; jeśli zmiana wygląda na zignorowaną, odczekaj i spróbuj ponownie przed dalszymi dochodzeniami.

---

## Zobacz także

- [Single Sign-On Overview](overview.md) — odniesienie konfiguracji, testowanie i ogólne rozwiązywanie problemów
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
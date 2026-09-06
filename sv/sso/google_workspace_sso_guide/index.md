# Ställ in SSO med Google Workspace

Googles identitetsplattform är OIDC-kompatibel och använder en enda, välkänd discovery-URL för alla kunder, så de enda värdena som är per-organisation är klient-ID och hemlighet.

Denna guide täcker **Google-sidan**: skapa OAuth-klienten och samla in de värden digna behöver. digna-sidan — `dashboard_config.toml`, testning och felsökning — är samma för alla leverantörer och beskrivs i [Single Sign-On Overview](overview.md).

---

## Innan du börjar

| Krav | Anteckningar |
|---|---|
| **Google Cloud project** | Valfritt projekt i samma organisation som din Workspace-domän |
| **Roll** | Editor eller Owner i projektet |
| **digna redirect URI** | URL dit användare återvänder efter inloggning, t.ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Steg 1: Konfigurera OAuth-samtyckesskärmen

Google utfärdar inte referenser förrän samtyckesskärmen finns.

1. Öppna [Google Cloud Console](https://console.cloud.google.com) och välj ditt projekt
2. Gå till **APIs & Services → OAuth consent screen**
3. Välj användartyp:
   - **Internal** — endast konton i din Workspace-domän kan logga in. Rekommenderas.
   - **External** — vilket Google-konto som helst kan försöka logga in.
4. Fyll i appnamn, användarsupport-e-post och utvecklarkontakt-e-post
5. På steget **Scopes**, lägg till `openid`, `.../auth/userinfo.email` och `.../auth/userinfo.profile`
6. Spara

!!! warning "Externa appar måste publiceras"

    En **External** samtyckesskärm startar i *Testing*-status, där endast konton som uttryckligen lagts till i testanvändarlistan kan slutföra en inloggning. Alla andra ser "digna has not completed the Google verification process". Antingen byt appen till **In production** under **Publishing status**, eller använd **Internal** — vilket inte har denna begränsning och är rätt val för en Workspace-endast-distribution.

---

## Steg 2: Skapa OAuth-klienten

1. Gå till **APIs & Services → Credentials**
2. Klicka **Create Credentials → OAuth client ID**
3. Sätt **Application type** till **Web application**
4. Ge den ett namn, t.ex. `digna`
5. Under **Authorized redirect URIs**, klicka **Add URI** och ange:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klicka **Create**

!!! note "Auktoriserade JavaScript-originer behövs inte"

    digna byter auktoriseringskoden från backend, inte webbläsaren, så fältet **Authorized JavaScript origins** kan lämnas tomt. Endast redirect-URI:n spelar roll.

---

## Steg 3: Hämta referenserna

Dialogrutan som visas efter skapandet visar:

- **Client ID** — slutar på `.apps.googleusercontent.com` → blir `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → blir `DIGNA_OIDC_CLIENT_SECRET`

Båda kan hämtas senare från credential-detaljsidan, till skillnad från de flesta andra leverantörer.

---

## Steg 4: Discovery-URL

Google använder en discovery-URL för alla kunder — det finns inget att byta ut:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Steg 5: Konfigurera digna

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

Värdet för `key` i båda filerna måste matcha — `google` här.

---

## Steg 6: Testa

Starta om backend och webbservern, och öppna sedan dashboarden. Se [Testing Login](overview.md#testing-login) för hela checklistan.

---

## Felsökning för Google Workspace

### Error 400: redirect_uri_mismatch

URI:n i `DIGNA_OIDC_REDIRECT_URI` finns inte i listan **Authorized redirect URIs**, eller skiljer sig åt genom en avslutande snedstreck eller schema. Googles fel-sida visar vilken URI den mottog — jämför tecken för tecken med den registrerade.

### This App Is Blocked / Has Not Completed Verification

Samtyckesskärmen är **External** och fortfarande i *Testing*. Publicera den, eller byt appen till **Internal**.

### Access Blocked: Authorization Error

Kontot som försöker logga in ligger utanför din Workspace-domän medan samtyckesskärmen är **Internal**. Detta är avsedd funktionalitet — Internal-appar accepterar endast konton i organisationen.

### Ändringar tar flera minuter

Google sprider credential- och samtyckesskärmsändringar asynkront. En ny redirect-URI kan ta några minuter innan den gäller; om en ändring verkar ignoreras, vänta och testa igen innan du påbörjar vidare felsökning.

---

## Se även

- [Single Sign-On Overview](overview.md) — konfigurationsreferens, testning och allmän felsökning
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
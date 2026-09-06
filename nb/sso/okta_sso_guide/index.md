# Sett opp SSO med Okta

Okta er OIDC-kompatibel, med en liten vridning som fanger opp de fleste første gangs integrasjoner: en Okta-organisasjon eksponerer mer enn én autorisasjonsserver, og hver har sin egen discovery-URL.

Denne veiledningen dekker **Okta-siden**: opprette app-integrasjonen og samle verdiene digna trenger. digna-siden — `dashboard_config.toml`, testing og feilsøking — er den samme for alle leverandører og beskrives i [Single Sign-On-oversikt](overview.md).

---

## Før du begynner

| Krav | Merknader |
|---|---|
| **Okta-rolle** | Super Administrator, eller en adminrolle som har tillatelse til å opprette app-integrasjoner |
| **Okta-domene** | f.eks. `yourcompany.okta.com`, eller et tilpasset domene hvis konfigurert |
| **digna redirect URI** | URL-en brukere returnerer til etter innlogging, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trinn 1: Opprett app-integrasjonen

1. Logg på Okta Admin Console
2. Gå til **Applications → Applications**
3. Klikk **Create App Integration**
4. Velg:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Klikk **Next**

!!! warning "Applikasjonstype kan ikke endres"

    Å velge *Single-Page Application* i stedet for *Web Application* oppretter en public client uten secret, og dignas backend-kode for tokenutveksling vil feile med `invalid_client`. Typen er fast ved opprettelse — et feilvalg betyr å slette appen og starte på nytt.

---

## Trinn 2: Konfigurer integrasjonen

1. **App integration name**: `digna`
2. **Grant type**: la *Authorization Code* stå valgt
3. **Sign-in redirect URIs**: legg inn din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: valgfritt
5. Under **Assignments**, velg hvem som kan bruke integrasjonen — en bestemt gruppe er tryggere enn *Allow everyone in your organization to access*
6. Klikk **Save**

!!! note "Tildeling er påkrevd"

    Okta autentiserer brukeren og sjekker deretter om de er tildelt applikasjonen. En ikke-tildelt bruker kommer til Okta-påloggingssiden, logger inn vellykket, og blir nektet ved omdirigeringen tilbake. Hvis pålogging fungerer for deg, men ikke for kolleger, er tildeling det første du bør sjekke.

---

## Trinn 3: Hent legitimasjonen

På applikasjonens **General**-fane, under **Client Credentials**:

- **Client ID** → blir `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → blir `DIGNA_OIDC_CLIENT_SECRET` (klikk på øyeikonet for å vise)

---

## Trinn 4: Velg autorisasjonsserver

Dette er trinnet som bestemmer discovery-URL-en. Gå til **Security → API** for å se autorisasjonsserverne i organisasjonen din.

**Org-autorisasjonsserver** — utsteder tokens for selve Okta-organisasjonen:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Tilpasset autorisasjonsserver** — inkludert den Okta oppretter kalt `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

For den innebygde serveren er `<auth_server_id>` bokstavelig talt `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Hvilken?"

    Bruk **org**-autorisasjonsserveren med mindre organisasjonen din allerede standardiserer på en tilpasset for API-tilgangspolicyer. Okta Developer-kontoer bruker `default` som standard; mange enterprise-organisasjoner deaktiverer den. Åpne begge URL-ene i en nettleser — den som returnerer JSON i stedet for en feil er den som er tilgjengelig for deg.

---

## Trinn 5: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Logg inn med Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Nøkkelen i begge filer må samsvare — `okta` her.

---

## Trinn 6: Test

Start backend og webserver på nytt, og åpne dashbordet. Se [Test av innlogging](overview.md#testing-login) for full sjekkliste.

---

## Feilsøking for Okta

### Omdirigerings-URI-en er ikke registrert

Okta oppgir den problematiske URI-en i feilen. Sammenlign den med **General → Sign-in redirect URIs**; Okta sammenligner hele strengen inkludert eventuelle avsluttende slash.

### Bruker er ikke tildelt klientapplikasjonen

Kontoen er ikke i applikasjonens tildelingsliste. Legg til brukeren eller gruppen deres under **Assignments**.

### 400 Bad Request: Invalid Authorization Server

`<auth_server_id>` i discovery-URL-en finnes ikke, oftest `default` i en org hvor den er fjernet. Sjekk **Security → API** for hvilke servere som faktisk er tilgjengelige.

### invalid_client ved token-steget

Integrasjonen ble opprettet som en Single-Page Application og har ingen client secret. Opprett den på nytt som en Web Application.

---

## Se også

- [Single Sign-On-oversikt](overview.md) — konfigurasjonsreferanse, testing og generell feilsøking
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
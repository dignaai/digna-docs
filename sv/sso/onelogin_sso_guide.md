# Ställ in SSO med OneLogin

OneLogin följer OIDC-standarden. Det som utmärker den är att connector-typen väljs ur en katalog när appen skapas och inte kan ändras i efterhand.

Denna guide täcker **OneLogin-sidan**: skapa applikationen och samla de värden digna behöver. digna-sidan — `dashboard_config.toml`, testning och felsökning — är densamma för alla leverantörer och beskrivs i [Översikt över Single Sign-On](overview.md).

---

## Innan du börjar

| Krav | Noteringar |
|---|---|
| **OneLogin-roll** | Kontoägare eller en administratör med behörighet att lägga till applikationer |
| **Underdomän** | t.ex. `yourcompany.onelogin.com` |
| **digna redirect URI** | URL:en dit användarna återvänder efter inloggning, t.ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Steg 1: Skapa OIDC-applikationen

1. Logga in i OneLogins Admin-portal
2. Gå till **Applications → Applications**
3. Klicka på **Add App**
4. Sök efter `OpenId Connect` och välj connectorn **OpenId Connect (OIDC)**
5. Ange `digna` som **Display Name**
6. Klicka på **Save**

!!! warning "Connector-typen bestäms när appen skapas"

    OneLogin har separata katalogposter för SAML och OIDC, och en applikation kan inte konverteras från den ena till den andra. Om du av misstag väljer en SAML-connector, ta bort appen och lägg till den igen — det finns ingen inställning för att byta protokoll.

---

## Steg 2: Konfigurera redirect URI

1. Öppna fliken **Configuration**
2. I **Redirect URI's**, ange din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Ange vid behov **Post Logout Redirect URIs** till din dashboard-URL
4. Klicka på **Save**

!!! note "En URI per rad"

    Till skillnad från leverantörer som förväntar sig en kommaseparerad lista tar OneLogins fält **Redirect URI's** en URI per rad.

---

## Steg 3: Ange applikationstyp och autentiseringsmetod

1. Öppna fliken **SSO**
2. Bekräfta att **Application Type** är *Web*
3. Ange **Token Endpoint → Authentication Method** till *POST* (`client_secret_post`) eller *Basic* (`client_secret_basic`)

!!! warning "Välj inte None"

    Om autentiseringsmetoden sätts till *None* blir applikationen en publik klient utan hemlighet, och kodutbytet i dignas backend avvisas. Både POST och Basic fungerar.

---

## Steg 4: Samla in inloggningsuppgifterna

Fortfarande på fliken **SSO**:

- **Client ID** → blir `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → blir `DIGNA_OIDC_CLIENT_SECRET` (klicka på **Show client secret**)

Sidan visar även **Issuer URL**, som bekräftar discovery-URL:en i nästa steg.

---

## Steg 5: Tilldela användare

1. Öppna fliken **Access**
2. Lägg till de roller eller grupper vars medlemmar får använda digna
3. Klicka på **Save**

!!! note "Användare som inte är tilldelade nekas efter inloggning"

    Som hos de flesta leverantörer autentiserar OneLogin först användaren och kontrollerar behörigheten därefter. En användare som inte är tilldelad loggar in utan problem och nekas sedan, vilket ser ut som ett fel i digna snarare än ett beslut i åtkomstkontrollen.

---

## Steg 6: Bygg discovery-URL:en

Ersätt med din OneLogin-underdomän:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Till exempel:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 är API-versionen"

    OneLogins nuvarande OIDC-implementation finns under `/oidc/2/`. Äldre dokumentation visar `/oidc/` utan version, vilket pekar på den avvecklade första versionen. Kontrollera **Issuer URL** på fliken SSO om du är osäker — discovery-URL:en är utfärdaren plus `/.well-known/openid-configuration`.

---

## Steg 7: Konfigurera digna

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

`key` i båda filerna måste matcha — här `onelogin`.

---

## Steg 8: Testa

Starta om backend och webbserver och öppna sedan dashboarden. Se [Testa inloggningen](overview.md#testing-login) för den fullständiga checklistan.

---

## Felsökning av OneLogin

### redirect_uri did not match

Callback-URL:en saknas i **Configuration → Redirect URI's**, eller så separerades posterna med kommatecken i stället för radbrytningar.

### invalid_client i token-steget

**Token Endpoint → Authentication Method** är satt till *None*, eller så är klienthemligheten i `config.toml` inaktuell. Visa hemligheten på fliken **SSO** och jämför.

### Appen visas inte för användarna

Ingen roll eller grupp har fått åtkomst på fliken **Access**.

### 404 på discovery-URL:en

Underdomänen är fel, eller så saknar URL:en `/oidc/2/`. Jämför med **Issuer URL** som visas på fliken SSO.

---

## Se även

- [Översikt över Single Sign-On](overview.md) — konfigurationsreferens, testning och allmän felsökning
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)
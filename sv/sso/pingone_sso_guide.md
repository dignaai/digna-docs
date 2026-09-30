# Ställ in SSO med PingOne

PingOne följer OIDC-standarden. Två av dess värden kräver noggrannhet: **miljö-ID:t** (environment ID), som ingår i varje endpoint-URL, och den **regionala domänen**, som skiljer sig mellan tenanter i Nordamerika, Europa, Kanada, Asien-Stillahavsområdet och Australien.

Denna guide täcker **PingOne-sidan**: skapa applikationen och samla de värden digna behöver. digna-sidan — `dashboard_config.toml`, testning och felsökning — är densamma för alla leverantörer och beskrivs i [Översikt över Single Sign-On](overview.md).

---

## Innan du börjar

| Krav | Noteringar |
|---|---|
| **PingOne-roll** | Environment Admin eller Identity Data Admin i målmiljön |
| **Miljö** | Den PingOne-miljö som dina digna-användare tillhör |
| **digna redirect URI** | URL:en dit användarna återvänder efter inloggning, t.ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Steg 1: Skapa applikationen

1. Logga in i PingOnes administrationskonsol och välj din miljö
2. Gå till **Applications → Applications**
3. Klicka på knappen **+**
4. Ange `digna` som **Application Name**
5. Välj **OIDC Web App**
6. Klicka på **Save**

!!! warning "Välj OIDC Web App, inte Single-Page App"

    *Single-Page App* och *Native App* skapar publika klienter som inte kan ha en hemlighet. digna byter auktoriseringskoden från sin backend och behöver den konfidentiella typen **OIDC Web App**.

---

## Steg 2: Konfigurera redirect URI

1. Öppna applikationens flik **Configuration**
2. Klicka på pennikonen för att redigera
3. Bekräfta att **Response Type** är *Code* och **Grant Type** är *Authorization Code*
4. Under **Redirect URIs**, ange din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

5. Ange **Token Endpoint Authentication Method** till *Client Secret Post* eller *Client Secret Basic*
6. Klicka på **Save**

---

## Steg 3: Aktivera applikationen

På applikationens rad eller i dess detaljpanel, slå om reglaget till **enabled**.

!!! warning "Nya applikationer är inaktiverade från början"

    PingOne skapar applikationer i inaktiverat läge. En inaktiverad applikation ger ett fel i auktoriseringssteget som inte nämner reglaget, så det är värt att kontrollera detta innan du felsöker något annat.

---

## Steg 4: Bevilja scopes

1. Öppna fliken **Resources**
2. Bekräfta att `openid` är beviljat, och lägg till `profile` och `email` från resursen **OpenID Connect**
3. Klicka på **Save**

---

## Steg 5: Tilldela användare

1. Öppna fliken **Access**
2. Lägg till den population eller de grupper vars medlemmar får använda digna
3. Klicka på **Save**

---

## Steg 6: Samla in inloggningsuppgifterna och miljö-ID

På fliken **Configuration**, expandera **General**:

- **Client ID** → blir `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → blir `DIGNA_OIDC_CLIENT_SECRET` (klicka på ögonikonen)
- **Environment ID** → används i discovery-URL:en

Samma flik visar den färdiga **OIDC Discovery Endpoint**, som du kan kopiera direkt i stället för att sätta ihop den för hand.

---

## Steg 7: Bygg discovery-URL:en

Ersätt med miljö-ID:t och domänen för din region:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Region | Domän |
|---|---|
| Nordamerika | `auth.pingone.com` |
| Europa | `auth.pingone.eu` |
| Kanada | `auth.pingone.ca` |
| Asien-Stillahavsområdet | `auth.pingone.asia` |
| Australien | `auth.pingone.com.au` |

För en europeisk miljö:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Kopiera i stället för att skriva"

    Den regionala domänen är det i särklass vanligaste misstaget i en PingOne-integration, och en felaktig region ger ett 404 i stället för ett användbart meddelande. Använd värdet **OIDC Discovery Endpoint** från Steg 6.

---

## Steg 8: Konfigurera digna

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

`key` i båda filerna måste matcha — här `pingone`.

---

## Steg 9: Testa

Starta om backend och webbserver och öppna sedan dashboarden. Se [Testa inloggningen](overview.md#testing-login) för den fullständiga checklistan.

---

## Felsökning av PingOne

### 404 på discovery-URL:en

Den regionala domänen eller miljö-ID:t är fel. Jämför med **OIDC Discovery Endpoint** som visas på applikationens flik Configuration.

### NOT_FOUND eller Application Disabled

Applikationens reglage från Steg 3 är fortfarande avslaget.

### Redirect URI mismatch

PingOne matchar hela strängen. Kontrollera **Configuration → Redirect URIs** med avseende på ett avslutande snedstreck eller ett annat schema (http/https).

### Inloggningen lyckas men ingen e-postclaim når digna

Scopes `email` och `profile` har inte beviljats på fliken **Resources**.

### Användaren ser inte applikationen

Ingen population eller grupp har fått åtkomst på fliken **Access**.

---

## Se även

- [Översikt över Single Sign-On](overview.md) — konfigurationsreferens, testning och allmän felsökning
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)
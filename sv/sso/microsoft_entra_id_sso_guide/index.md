# Ställ in SSO med Microsoft Entra ID

Microsoft Entra ID (tidigare Azure Active Directory) är en leverantör som fullt ut följer OIDC-standarden, så digna integreras med den via den vanliga discovery-endpointen.

Denna guide täcker **Entra ID-sidan**: registrera applikationen och samla de fyra värden digna behöver. digna-sidan — `dashboard_config.toml`, testning och felsökning — är densamma för alla leverantörer och beskrivs i [Översikt över Single Sign-On](overview.md).

---

## Innan du börjar

| Krav | Noteringar |
|---|---|
| **Entra ID-roll** | Application Administrator, Cloud Application Administrator eller Global Administrator |
| **digna redirect URI** | URL:en dit användarna återvänder efter inloggning, t.ex. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | Katalogen som dina användare loggar in i |

---

## Steg 1: Registrera applikationen

1. Logga in i [Microsoft Entra admin center](https://entra.microsoft.com)
2. Gå till **Identity → Applications → App registrations**
3. Klicka på **New registration**
4. Konfigurera:
   - **Name**: `digna` (visas för användarna på samtyckesskärmen)
   - **Supported account types**: *Accounts in this organizational directory only* för en installation med en enda tenant
5. Under **Redirect URI**, välj plattformen **Web** och ange din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klicka på **Register**

!!! warning "Viktigt"

    Plattformen måste vara **Web**, inte *Single-page application*. digna byter auktoriseringskoden från backenden med hjälp av en klienthemlighet, vilket plattformstypen SPA inte tillåter.

---

## Steg 2: Hämta klient- och tenant-ID

På applikationens sida **Overview**, kopiera:

- **Application (client) ID** → blir `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → används i discovery-URL:en

---

## Steg 3: Skapa en klienthemlighet

1. Gå till **Certificates & secrets → Client secrets**
2. Klicka på **New client secret**
3. Ange en beskrivning och välj giltighetstid
4. Klicka på **Add**
5. Kopiera kolumnen **Value** omedelbart

!!! warning "Kopiera Value, inte Secret ID"

    **Value** visas bara en gång, på denna sida, och kan inte hämtas i efterhand. **Secret ID** bredvid ser liknande ut men är inte hemligheten — om du använder den får du felet `invalid_client` vid inloggning. Om du lämnar sidan innan du kopierat, ta bort hemligheten och skapa en ny.

!!! tip "Tips"

    Entra ID begränsar hemligheters livslängd till 24 månader, så varje SSO-integration har ett utgångsdatum. Anteckna det där du kommer att se det — en utgången hemlighet slår ut SSO för alla användare på en gång, utan någon varning på inloggningssidan.

---

## Steg 4: Bekräfta API-behörigheterna

1. Gå till **API permissions**
2. Bekräfta att **Microsoft Graph → User.Read** (delegerad) finns — den läggs till som standard

De scopes `openid`, `profile` och `email` som digna begär ingår i standarduppsättningen för OIDC och kräver inget separat medgivande. Om din tenant kräver administratörsmedgivande för alla applikationer, klicka på **Grant admin consent for &lt;tenant&gt;**.

---

## Steg 5: Bygg discovery-URL:en

Ersätt med **Directory (tenant) ID** från Steg 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Använd v2.0-endpointen"

    Segmentet `/v2.0/` spelar roll. v1.0-endpointen på `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` utfärdar token i ett äldre format och returnerar inte de vanliga OIDC-claims som digna förväntar sig.

Öppna URL:en i en webbläsare innan du fortsätter. Ett JSON-dokument bekräftar att tenant-ID:t är korrekt.

---

## Steg 6: Konfigurera digna

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

`key` i båda filerna måste matcha — här `microsoft`.

---

## Steg 7: Testa

Starta om backend och webbserver och öppna sedan dashboarden. Se [Testa inloggningen](overview.md#testing-login) för den fullständiga checklistan.

---

## Felsökning av Entra ID

### AADSTS50011: Redirect URI Mismatch

URI:n i `DIGNA_OIDC_REDIRECT_URI` skiljer sig från den som registrerades i Steg 1. Entra ID jämför hela strängen, så ett avslutande snedstreck, `http` jämfört med `https` eller en annan port räknas alla som en avvikelse. Kontrollera **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Antingen kopierades **Secret ID** i stället för **Value**, eller så har hemligheten gått ut. Skapa en ny hemlighet och kopiera kolumnen Value.

### AADSTS650057: Invalid Resource

Appregistreringen har tagits bort eller tillhör en annan tenant än den i discovery-URL:en. Bekräfta Directory (tenant) ID på sidan Overview.

### Användare loggar in men ingenting händer

Om tenanten kräver administratörsmedgivande och det inte har beviljats, återvänder omdirigeringen utan en användbar token. Bevilja administratörsmedgivande under **API permissions**.

---

## Se även

- [Översikt över Single Sign-On](overview.md) — konfigurationsreferens, testning och allmän felsökning
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
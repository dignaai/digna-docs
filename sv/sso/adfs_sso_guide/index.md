# Ställ in SSO med AD FS

Active Directory Federation Services är on-premises-alternativet: dina egna servrar utfärdar token, och discovery-URL:en är ditt eget värdnamn. AD FS stöder OpenID Connect från **Windows Server 2016** och framåt.

Denna guide täcker **AD FS-sidan**: skapa applikationsgruppen och samla de värden digna behöver. Digna-sidan — `dashboard_config.toml`, testning och felsökning — är samma för alla leverantörer och beskrivs i [Single Sign-On Overview](overview.md).

---

## Innan du börjar

| Krav | Noteringar |
|---|---|
| **AD FS-version** | Windows Server 2016 eller senare — tidigare versioner har ingen OIDC-support |
| **Åtkomst** | Lokal administratör på AD FS-servern |
| **Federation service-namn** | t.ex. `adfs.yourdomain.com` |
| **digna redirect URI** | URL dit användarna återvänder efter inloggning, t.ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Steg 1: Skapa applikationsgruppen

1. På AD FS-servern, öppna **AD FS Management**
2. Högerklicka på **Application Groups** och välj **Add Application Group**
3. Ange `digna` som namn
4. Under **Standalone applications** — eller **Client-Server applications** beroende på din version — välj **Server application accessing a web API**
5. Klicka **Next**

---

## Steg 2: Konfigurera serverapplikationen

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS genererar en GUID. Kopiera den — detta blir `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: ange din digna callback-URL och klicka **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Klicka **Next**

!!! warning "Klicka på Add, inte bara Next"

    Fältet Redirect URI har sin egen **Add**-knapp. Att skriva en URI och klicka **Next** utan att trycka **Add** gör att den försvinner, och guiden varnar inte. Bekräfta att URI:en visas i listan under fältet innan du fortsätter.

---

## Steg 3: Generera den delade hemligheten

1. Kryssa i **Generate a shared secret**
2. Kopiera den genererade hemligheten → blir `DIGNA_OIDC_CLIENT_SECRET`
3. Klicka **Next**

!!! warning "Hemligheten visas bara en gång"

    AD FS visar den delade hemligheten endast på denna sida i guiden och kan inte visa den igen. Om du tappar bort den, återställ den senare från applikationsgruppens egenskaper.

---

## Steg 4: Konfigurera Web API

1. **Identifier**: ange samma client identifier från Steg 2 och klicka **Add**
2. Klicka **Next**
3. Välj en **Access Control Policy** — *Permit everyone* är den enklaste startpunkten; begränsa den till en grupp i produktion
4. Klicka **Next**

---

## Steg 5: Ge tillåtna scopes

På steget **Configure Application Permissions**, kryssa i:

- `openid`
- `profile`
- `email`

Klicka sedan **Next** och slutför guiden.

!!! warning "openid är inte förkryssat som standard"

    AD FS förvanskar i vissa versioner endast `user_impersonation`. Utan `openid` returnerar token-endpointen en OAuth access token istället för en ID-token, och digna kan inte identifiera användaren.

---

## Steg 6: Bekräfta discovery-endpointen

Byt ut ditt federation service-namn:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Till exempel:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Öppna den i en webbläsare. Ett JSON-dokument bekräftar att OIDC är aktiverat och att värdnamnet är korrekt.

!!! note "Backenden måste lita på certifikatet"

    En intern certifikatutfärdare är vanlig för AD FS. Maskinen som kör digna-backenden gör ett eget utgående HTTPS-anrop till denna URL, så utfärdarens CA måste finnas i den maskinens betrodda certifikatbutik — inte endast i webbläsarna hos de som loggar in.

---

## Steg 7: Konfigurera digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Logga in med Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

`key` i båda filerna måste matcha — `adfs` här.

---

## Steg 8: Testa

Starta om backend och webbserver, och öppna sedan dashboarden. Se [Testing Login](overview.md#testing-login) för full checklista.

---

## Felsökning AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

Web API-identifieraren i Steg 4 matchar inte client identifier, eller så gavs inte de scopes som krävs i Steg 5. Båda kan redigeras från applikationsgruppens egenskaper.

### MSIS9602: Invalid redirect_uri

URI:n skrevs in men lades inte till med **Add**-knappen, eller skiljer sig från `DIGNA_OIDC_REDIRECT_URI`. Kontrollera **Application Groups → digna → digna backend → Properties**.

### Ingen ID-token returneras

`openid`-scope saknas från applikationsbehörigheterna.

### Backend kan inte nå discovery-URL:en

Antingen löser inte DNS på backend-värden federation service-namnet, eller så är AD FS-certifikatet inte betrott där. Testa med `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` från digna-servern själv.

### Händelser att kontrollera

AD FS-servern loggar fel i **Applications and Services Logs → AD FS → Admin** i Event Viewer, vanligtvis med en mer specifik anledning än vad webbläsaren visar.

---

## Se även

- [Single Sign-On Overview](overview.md) — konfigurationsreferens, testning och allmän felsökning
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
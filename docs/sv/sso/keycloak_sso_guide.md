---
title: Keycloak SSO – Single Sign-On-integration | digna Dokumentation
description: Konfigurera Single Sign-On för digna med Keycloak via OpenID Connect — konfiguration av realm och klient, klientautentisering, giltiga redirect-URI:er, klienthemlighet och motsvarande digna-konfiguration.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, konfidentiell klient, openid connect, egenhostad identitetsleverantör
---

# Ställ in SSO med Keycloak

Keycloak är en egenhostad identitetsleverantör som fullt ut följer OIDC-standarden. Eftersom du driver den själv byggs discovery-URL:en från ditt eget värdnamn och din realm i stället för en leverantörsdomän.

Denna guide täcker **Keycloak-sidan**: skapa klienten och samla de värden digna behöver. digna-sidan — `dashboard_config.toml`, testning och felsökning — är densamma för alla leverantörer och beskrivs i [Översikt över Single Sign-On](overview.md).

---

## Innan du börjar

| Krav | Noteringar |
|---|---|
| **Keycloak-version** | 17 eller senare för de URL-sökvägar som används här — se noteringen i Steg 4 |
| **Keycloak-roll** | `realm-admin` i mål-realmen, eller serveradministratör |
| **Realm** | Den realm som dina digna-användare tillhör, inte nödvändigtvis `master` |
| **digna redirect URI** | URL:en dit användarna återvänder efter inloggning, t.ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Steg 1: Välj realm

1. Öppna Keycloaks administrationskonsol
2. Använd realm-väljaren uppe till vänster för att byta till den realm där dina användare finns

!!! warning "Använd inte master-realmen"

    Realmen `master` är avsedd för att administrera Keycloak självt. Applikationsklienter hör hemma i en dedikerad realm; om digna placeras i `master` får dess användare en väg in i Keycloaks administrationskonsol.

---

## Steg 2: Skapa klienten

1. Gå till **Clients** och klicka på **Create client**
2. Konfigurera:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — detta blir `DIGNA_OIDC_CLIENT_ID`
3. Klicka på **Next**
4. I steget **Capability config**, slå **On** för **Client authentication**
5. Låt **Standard flow** vara aktiverat; de andra flödena behövs inte
6. Klicka på **Next**

!!! warning "Client authentication måste vara på"

    Med **Client authentication** avstängd skapar Keycloak en *publik* klient, som inte har några inloggningsuppgifter alls — fliken **Credentials** i Steg 4 kommer inte att finnas. digna behöver en konfidentiell klient. Reglaget kan ändras efter att klienten skapats om du gör fel.

---

## Steg 3: Ange redirect URI

I steget **Login settings** (eller på fliken **Settings** i efterhand):

1. **Valid redirect URIs**: ange din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: lämna tomt, eller ange `+` för att spegla redirect-URI:erna
3. Klicka på **Save**

!!! tip "Undvik jokertecken"

    Keycloak accepterar mönster som `https://digna.yourdomain.com/*`. Ett jokertecken låter vilken sökväg som helst på den värden ta emot en auktoriseringskod, så använd hellre den exakta callback-URL:en.

---

## Steg 4: Hämta klienthemligheten

1. Öppna fliken **Credentials**
2. Bekräfta att **Client Authenticator** är *Client Id and Secret*
3. Kopiera **Client secret** → blir `DIGNA_OIDC_CLIENT_SECRET`

Hemligheten kan alltid hämtas här igen och kan genereras på nytt med **Regenerate**.

---

## Steg 5: Bygg discovery-URL:en

Ersätt med din Keycloak-värd och ditt realm-namn:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Till exempel:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 och tidigare inkluderar /auth"

    Före Keycloak 17 låg alla endpoints under prefixet `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distributioner som anger `KC_HTTP_RELATIVE_PATH=/auth` behåller den gamla strukturen även i aktuella versioner. Om URL:en utan `/auth` returnerar 404, prova med.

Öppna URL:en i en webbläsare innan du fortsätter. Ett JSON-dokument bekräftar att värd och realm är korrekta.

---

## Steg 6: Konfigurera digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc_clients.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

`key` i båda filerna måste matcha — här `keycloak`. Observera att den inte behöver vara lika med Keycloaks **Client ID**, även om det är lättare att följa om de är desamma.

---

## Steg 7: Testa

Starta om backend och webbserver och öppna sedan dashboarden. Se [Testa inloggningen](overview.md#testing-login) för den fullständiga checklistan.

---

## Felsökning av Keycloak

### Invalid parameter: redirect_uri

Callback-URL:en täcks inte av **Valid redirect URIs**. Keycloak loggar den URI som togs emot i serverloggen, vilket är det snabbaste sättet att se exakt var avvikelsen ligger.

### Fliken Credentials saknas

Klienten är publik. Slå på **Client authentication** under **Settings → Capability config**.

### 404 på discovery-URL:en

Antingen är realm-namnet fel, eller så använder installationen prefixet `/auth`. Kontrollera realm-listan i administrationskonsolen och prova båda URL-formerna.

### unauthorized_client eller invalid_client

**Standard flow** är inaktiverat under **Capability config**, eller så har hemligheten genererats på nytt i Keycloak utan att `config.toml` uppdaterats.

### Certifikatfel från backenden

En egenhostad Keycloak bakom ett privat eller självsignerat certifikat gör att dignas utgående HTTPS-anrop till discovery-URL:en misslyckas. Installera den utfärdande certifikatutfärdaren (CA) i certifikatarkivet på maskinen som kör digna-backenden.

---

## Se även

- [Översikt över Single Sign-On](overview.md) — konfigurationsreferens, testning och allmän felsökning
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)

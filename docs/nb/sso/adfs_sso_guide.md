---
title: Konfigurer AD FS SSO – Single Sign-On-integrasjon | digna-dokumentasjon
description: Konfigurer Single Sign-On for digna med Active Directory Federation Services ved bruk av OpenID Connect — applikasjonsgruppe, serverapplikasjon, delt hemmelighet, tillatte scopes og tilhørende digna-konfigurasjon.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, active directory federation services, adfs oidc, application group, openid connect, on-premises identity provider
---

# Konfigurer SSO med AD FS

Active Directory Federation Services er on-premises-alternativet: dine egne servere utsteder tokenene, og discovery-URL-en er ditt eget vertsnavn. AD FS støtter OpenID Connect fra **Windows Server 2016** og senere.

Denne veiledningen dekker **AD FS-siden**: opprette applikasjonsgruppen og samle inn verdiene digna trenger. digna-siden — `dashboard_config.toml`, testing og feilsøking — er den samme for alle leverandører og beskrives i [Oversikt over Single Sign-On](overview.md).

---

## Før du begynner

| Krav | Notater |
|---|---|
| **AD FS-versjon** | Windows Server 2016 eller nyere — eldre versjoner har ingen OIDC-støtte |
| **Tilgang** | Lokal administrator på AD FS-serveren |
| **Federasjonstjenestens navn** | f.eks. `adfs.yourdomain.com` |
| **digna redirect URI** | URL-en brukerne returneres til etter innlogging, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trinn 1: Opprett applikasjonsgruppen

1. På AD FS-serveren, åpne **AD FS Management**
2. Høyreklikk **Application Groups** og velg **Add Application Group**
3. Skriv inn `digna` som navn
4. Under **Standalone applications** — eller **Client-Server applications** avhengig av versjon — velg **Server application accessing a web API**
5. Klikk **Next**

---

## Trinn 2: Konfigurer serverapplikasjonen

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS genererer en GUID. Kopier den — dette blir `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: skriv inn din digna callback-URL og klikk **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Klikk **Next**

!!! warning "Klikk Legg til, ikke bare Neste"

    Feltet for redirect URI har sin egen **Add**-knapp. Hvis du skriver inn en URI og klikker **Next** uten å trykke **Add**, blir den forkastet, og veiviseren gir ingen advarsel. Bekreft at URI-en vises i listen under feltet før du fortsetter.

---

## Trinn 3: Generer den delte hemmeligheten

1. Huk av **Generate a shared secret**
2. Kopier den genererte hemmeligheten → blir `DIGNA_OIDC_CLIENT_SECRET`
3. Klikk **Next**

!!! warning "Hemmeligheten vises bare én gang"

    AD FS viser den delte hemmeligheten bare på denne veivisersiden og kan ikke vise den igjen. Hvis du mister den, tilbakestill den senere fra applikasjonsgruppens egenskaper.

---

## Trinn 4: Konfigurer Web API

1. **Identifier**: skriv inn samme client identifier fra Trinn 2 og klikk **Add**
2. Klikk **Next**
3. Velg en **Access Control Policy** — *Permit everyone* er enklest å starte med; begrens til en gruppe i produksjon
4. Klikk **Next**

---

## Trinn 5: Gi tillatte scopes

På steget **Configure Application Permissions**, huk av:

- `openid`
- `profile`
- `email`

Deretter klikker du **Next** og fullfører veiviseren.

!!! warning "openid er ikke huket av som standard"

    AD FS forhaker i noen versjoner kun `user_impersonation`. Uten `openid` returnerer token-endepunktet et OAuth-tilgangstoken i stedet for et ID-token, og digna kan ikke identifisere brukeren.

---

## Trinn 6: Bekreft discovery-endepunktet

Bytt ut ditt federasjonstjenestenavn:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

For eksempel:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Åpne dette i en nettleser. Et JSON-dokument bekrefter at OIDC er aktivert og at vertsnavnet er riktig.

!!! note "Backenden må stole på sertifikatet"

    Et internt sertifikatutførende organ er vanlig for AD FS. Maskinen som kjører digna-backenden gjør sitt eget utgående HTTPS-kall til denne URL-en, så den utstedende CA-en må være i den maskinens trust store — ikke bare i nettleserne til de som logger inn.

---

## Trinn 7: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Login with Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

`key` i begge filer må stemme overens — `adfs` her.

---

## Trinn 8: Test

Start backend og webserver på nytt, og åpne deretter dashbordet. Se [Test av innlogging](overview.md#testing-login) for full sjekkliste.

---

## Feilsøking AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

Web API-identifikatoren i Trinn 4 samsvarer ikke med client-identifikatoren, eller scopes i Trinn 5 ble ikke gitt. Begge kan redigeres fra applikasjonsgruppens egenskaper.

### MSIS9602: Invalid redirect_uri

URI-en ble skrevet inn men ikke lagt til med **Add**-knappen, eller skiller seg fra `DIGNA_OIDC_REDIRECT_URI`. Sjekk **Application Groups → digna → digna backend → Properties**.

### Ingen ID-token returneres

`openid`-scope mangler fra applikasjonstillatelsene.

### Backend kan ikke nå discovery-URL-en

Enten løser ikke DNS på backend-hostnavnet federasjonstjenestens navn, eller AD FS-sertifikatet er ikke betrodd der. Test med `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` fra digna-serveren selv.

### Hendelser å sjekke

AD FS-serveren logger feil til **Applications and Services Logs → AD FS → Admin** i Event Viewer, vanligvis med en mer spesifikk årsak enn det nettleseren viser.

---

## Se også

- [Oversikt over Single Sign-On](overview.md) — konfigurasjonsreferanse, testing og generell feilsøking
- [Microsoft: AD FS OpenID Connect-scenarier](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
---
title: AD FS SSO – Single Sign-On-integration | digna-dokumentation
description: Konfigurer Single Sign-On for digna med Active Directory Federation Services via OpenID Connect — applikationsgruppe, serverapplikation, delt hemmelighed, tilladte scopes og den tilsvarende digna-konfiguration.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, active directory federation services, adfs oidc, applikationsgruppe, openid connect, lokal identitetsudbyder
---

# Opsæt SSO med AD FS

Active Directory Federation Services er on-premises‑muligheden: dine egne servere udsteder tokenene, og discovery‑URL'en er dit eget værtsnavn. AD FS understøtter OpenID Connect fra **Windows Server 2016** og fremefter.

Denne vejledning dækker **AD FS-siden**: oprettelse af applikationsgruppen og indsamling af de værdier, digna har brug for. Digna-siden — `dashboard_config.toml`, test og fejlfinding — er den samme for alle udbydere og beskrives i [Single Sign-On Overview](overview.md).

---

## Før du går i gang

| Krav | Noter |
|---|---|
| **AD FS version** | Windows Server 2016 eller nyere — tidligere versioner understøtter ikke OIDC |
| **Adgang** | Lokal administrator på AD FS-serveren |
| **Federation service name** | f.eks. `adfs.yourdomain.com` |
| **digna redirect URI** | Den URL, brugerne vender tilbage til efter login, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trin 1: Opret applikationsgruppen

1. På AD FS-serveren, åbn **AD FS Management**
2. Højreklik på **Application Groups** og vælg **Add Application Group**
3. Indtast `digna` som navn
4. Under **Standalone applications** — eller **Client-Server applications** afhængigt af din version — vælg **Server application accessing a web API**
5. Klik **Next**

---

## Trin 2: Konfigurer serverapplikationen

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS genererer en GUID. Kopiér den — dette bliver `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: indtast din digna callback‑URL og klik **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Klik **Next**

!!! warning "Klik Tilføj, Ikke Kun Næste"

    Feltet til redirect URI har sin egen **Add**‑knap. Hvis du skriver en URI og klikker **Next** uden at trykke **Add**, bliver den kasseret, og guiden giver ingen advarsel. Bekræft, at URI'en dukker op i listen under feltet, før du fortsætter.

---

## Trin 3: Generér den delte hemmelighed

1. Sæt flueben ved **Generate a shared secret**
2. Kopiér den genererede hemmelighed → bliver `DIGNA_OIDC_CLIENT_SECRET`
3. Klik **Next**

!!! warning "Hemmeligheden vises kun én gang"

    AD FS viser den delte hemmelighed kun på denne side i guiden og kan ikke vise den igen. Hvis du mister den, nulstil den senere fra applikationsgruppens egenskaber.

---

## Trin 4: Konfigurer Web API'et

1. **Identifier**: indtast samme client identifier fra Trin 2 og klik **Add**
2. Klik **Next**
3. Vælg en **Access Control Policy** — *Permit everyone* er det simpleste udgangspunkt; begræns det til en gruppe i produktion
4. Klik **Next**

---

## Trin 5: Tildel de tilladte scopes

På trinnet **Configure Application Permissions**, sæt flueben ved:

- `openid`
- `profile`
- `email`

Klik derefter **Next** og fuldfør guiden.

!!! warning "openid er ikke valgt som standard"

    AD FS forudvælger i nogle versioner kun `user_impersonation`. Uden `openid` returnerer token‑endpointet et OAuth access token i stedet for et ID‑token, og digna kan ikke identificere brugeren.

---

## Trin 6: Bekræft discovery‑endpointet

Udskift dit federation service name:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

For eksempel:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Åbn det i en browser. Et JSON‑dokument bekræfter, at OIDC er aktiveret, og at værtsnavnet er korrekt.

!!! note "Backenden skal stole på certifikatet"

    En intern certifikatmyndighed er almindelig for AD FS. Maskinen, der kører digna‑backend, foretager sit eget udgående HTTPS‑kald til denne URL, så den udstedende CA skal være i den maskines trust store — ikke kun i browsere hos de personer, der logger ind.

---

## Trin 7: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Log ind med Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Nøglen `key` i begge filer skal matche — `adfs` her.

---

## Trin 8: Test

Genstart backend og webserver, og åbn derefter dashboardet. Se [Test af login](overview.md#testing-login) for den komplette tjekliste.

---

## Fejlfinding for AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

Web API‑identifikatoren i Trin 4 stemmer ikke overens med client identifier, eller scopes i Trin 5 blev ikke tildelt. Begge kan redigeres fra applikationsgruppens egenskaber.

### MSIS9602: Invalid redirect_uri

URI'en blev indtastet, men ikke tilføjet med **Add**‑knappen, eller den afviger fra `DIGNA_OIDC_REDIRECT_URI`. Tjek **Application Groups → digna → digna backend → Properties**.

### Der returneres intet ID‑token

`openid`‑scope mangler i applikations‑tilladelserne.

### Backenden kan ikke nå discovery‑URL'en

Enten kan DNS på backend‑hosten ikke opløse federation service‑navnet, eller AD FS‑certifikatet er ikke betroet der. Test med `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` fra digna‑serveren selv.

### Begivenheder at tjekke

AD FS‑serveren logger fejl i **Applications and Services Logs → AD FS → Admin** i Event Viewer, normalt med en mere specifik årsag end den, browseren viser.

---

## Se også

- [Single Sign-On Overview](overview.md) — konfigurationsreference, test og generel fejlfinding
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
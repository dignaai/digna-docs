---
title: Okta SSO – Single Sign-On integratsioon | digna dokumentatsioon
description: Seadista digna jaoks Single Sign-On Okta abil kasutades OpenID Connecti — rakenduse integratsioon, sisselogimise ümbersuunamise URI-d, kliendi mandaadid, autoriseerimiserveri valik ja vastav digna konfiguratsioon.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, rakenduse integratsioon, autoriseerimiserver, OpenID Connect, ettevõtte autentimine
---

# SSO seadistamine Okta abil

Okta järgib OIDC standardit, kuid üks peamine peibutis, mis esimest korda integreerijad segadusse ajab: Okta org näitab rohkem kui ühte autoriseerimisserverit ja igaühel neist on oma discovery URL.

See juhend käsitleb **Okta poolt tehtavat**: rakenduse integratsiooni loomist ja väärtuste kogumist, mida digna vajab. digna pool — `dashboard_config.toml`, testimine ja tõrkeotsing — on sama iga pakkuja puhul ja on kirjeldatud lehel [Single Sign-On Overview](overview.md).

---

## Enne alustamist

| Nõue | Märkused |
|---|---|
| **Okta roll** | Super Administrator või administraatori roll, millel on õigus luua rakenduse integratsioone |
| **Okta domeen** | nt `yourcompany.okta.com` või kohandatud domeen, kui see on konfigureeritud |
| **digna redirect URI** | URL, kuhu kasutaja pärast sisselogimist tagasi suunatakse, nt `https://digna.yourdomain.com/oidc/callback` |

---

## Samm 1: Loo rakenduse integratsioon

1. Logi sisse Okta Admin Console'i
2. Mine menüüsse **Applications → Applications**
3. Klõpsa **Create App Integration**
4. Vali:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Klõpsa **Next**

!!! warning "Rakenduse tüüpi ei saa muuta"

    Kui valid *Single-Page Application* asemel *Web Application*, tekib avalik klient ilma salajata ning digna backendi koodi vahetus ebaõnnestub veaga `invalid_client`. Tüüp on fikseeritud loomisel — vale valik tähendab, et rakendus tuleb kustutada ja alustada uuesti.

---

## Samm 2: Konfigureeri integratsioon

1. **App integration name**: `digna`
2. **Grant type**: jäta valituks *Authorization Code*
3. **Sign-in redirect URIs**: sisesta oma digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: valikuline
5. Alumises jaotises **Assignments** vali, kes võivad integratsiooni kasutada — kindel grupp on turvalisem kui *Allow everyone in your organization to access*
6. Klõpsa **Save**

!!! note "Määramine on kohustuslik"

    Okta autentib kasutaja ja kontrollib seejärel, kas kasutaja on rakendusele määratud. Määramata kasutaja jõuab Okta sisselogimislehele, logib edukalt sisse, kuid tagasilükkamine toimub ümbersuunamisel tagasi. Kui sisselogimine töötab sinu puhul, aga mitte kolleegide puhul, on esimene kontrollkoht rakenduse määramine.

---

## Samm 3: Kogu kliendi mandaadid

Rakenduse **General** vahekaardil, jaotises **Client Credentials**:

- **Client ID** → muutub `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → muutub `DIGNA_OIDC_CLIENT_SECRET` (klõpsa silmaikooni, et näha)

---

## Samm 4: Valige autoriseerimisserver

See samm määrab sinu discovery URL-i. Mine menüüsse **Security → API**, et näha orgis saadaolevaid autoriseerimisservereid.

**Org authorization server** — väljastab tokenid Okta org ise jaoks:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — sh see, mida Okta loob nimega `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Sisseehitatud serveri puhul on `<auth_server_id>` sõnasõnaliselt `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Kumba valida?"

    Kasuta **org** autoriseerimisserverit, välja arvatud juhul, kui teie organisatsioon on juba standardiseerinud kohandatud serveri API juurdepääsupoliitikate jaoks. Okta Developer kontod kasutavad vaikimisi `default`; paljud ettevõtteorgid selle keelavad. Ava mõlemad URL-id brauseris — see, mis tagastab JSONi, mitte vea, on see, mis on sinu jaoks saadaval.

---

## Samm 5: Seadista digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Mõlemas failis peab `key` kattuma — siin on see `okta`.

---

## Samm 6: Testimine

Taaskäivita backend ja veebiserver, seejärel ava juhtpaneel. Täieliku kontrollnimekirja jaoks vaata [Testing Login](overview.md#testing-login).

---

## Okta tõrkeotsing

### Ümbersuunamise URI ei ole registreeritud

Okta nimetab vea käigus probleemi põhjustava URI. Võrdle seda jaotise **General → Sign-in redirect URIs** väärtusega; Okta võrdleb täispikka stringi, kaasa arvatud lõppkaldkriipsu.

### Kasutaja ei ole kliendirakendusele määratud

Konto ei ole lisatud rakenduse määramise nimekirja. Lisa kasutaja või tema grupp jaotises **Assignments**.

### 400 Bad Request: Invalid Authorization Server

Discovery URL-is kasutatud `<auth_server_id>` ei eksisteeri, kõige sagedamini `default` orgis, kus see on eemaldatud. Kontrolli menüüst **Security → API**, millised serverid tegelikult saadaolevad on.

### invalid_client tokeni vahetuse sammul

Integratsioon loodi kui Single-Page Application ja tal puudub kliendisaladus. Loo see uuesti kui Web Application.

---

## Vt ka

- [Üksik-sisselogimine — ülevaade](overview.md) — konfiguratsiooni viide, testimine ja üldine tõrkeotsing
- [Okta: OpenID Connect ja OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
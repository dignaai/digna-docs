---
title: Microsoft Entra ID SSO – Single Sign-On integratsioon | digna dokumentatsioon
description: Seadista Single Sign-On digna jaoks Microsoft Entra ID-ga (endine Azure AD) kasutades OpenID Connecti — rakenduse registreerimine, redirect URI, kliendisaladus, tenant ID ja vastav digna konfiguratsioon.
image: /assets/logo_square.png
keywords: digna sso, microsoft entra id, azure ad sso, oidc integratsioon, rakenduse registreerimine, ettevõtte autentimine
---

# SSO seadistamine Microsoft Entra ID-ga

Microsoft Entra ID (endine Azure Active Directory) on täielikult OIDC-ühilduv pakkuja, nii et digna integreerub sellega läbi standardse discovery lõpp-punkti.

See juhend käsitleb **Entra ID poolt** toimuvaid samme: rakenduse registreerimist ja nelja väärtuse kogumist, mida digna vajab. digna pool — `dashboard_config.toml`, testimine ja tõrkeotsing — on kõigi pakkujatega sama ja on kirjeldatud [Single Sign-On Overview](overview.md)-s.

---

## Enne alustamist

| Nõue | Märkused |
|---|---|
| **Entra ID roll** | Application Administrator, Cloud Application Administrator või Global Administrator |
| **digna redirect URI** | URL, kuhu kasutaja suunatakse peale sisselogimist, nt `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | See kataloog, kuhu teie kasutajad sisse logivad |

---

## 1. samm: Registreeri rakendus

1. Logi sisse [Microsoft Entra halduskeskusesse](https://entra.microsoft.com)
2. Mine jaotisse **Identity → Applications → App registrations**
3. Klõpsa **New registration**
4. Konfigureeri:
   - **Name**: `digna` (kuvatakse kasutajatele nõusoleku ekraanil)
   - **Supported account types**: *Accounts in this organizational directory only* ühe-tenantilise juurutuse jaoks
5. Jaotises **Redirect URI** vali platvorm **Web** ja sisesta oma digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klõpsa **Register**

!!! warning "Oluline"

    Platvormiks peab olema **Web**, mitte *Single-page application*. digna vahetab autoriseerimiskoodi backendis kliendisaladuse abil, mida SPA platvormitüüp ei luba.

---

## 2. samm: Kogu Client ja Tenant ID-d

Rakenduse **Overview** lehel kopeeri:

- **Application (client) ID** → saab `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → lisatakse discovery URL-ile

---

## 3. samm: Loo kliendisaladus

1. Mine **Certificates & secrets → Client secrets**
2. Klõpsa **New client secret**
3. Sisesta kirjeldus ja vali aegumiskuupäev
4. Klõpsa **Add**
5. Kopeeri kohe veerg **Value**

!!! warning "Kopeeri Value, mitte Secret ID"

    **Value** kuvatakse ainult üks kord, sel lehel, ja seda ei saa hiljem taastada. Selle kõrval olev **Secret ID** näeb sarnane välja, kuid ei ole salajane väärtus — selle kasutamine tekitab sisselogimisel `invalid_client` vea. Kui lahkud lehelt enne kopeerimist, kustuta salajane väärtus ja loo uus.

!!! tip "Vihje"

    Entra ID piirab salajaste väärtuste eluiga maksimaalselt 24 kuule, nii et iga SSO integratsioonil on aegumiskuupäev. Pane see kuskile nähtavale — aegunud salajane võtme peatab SSO kõigi kasutajate jaoks ilma sisselogimislehel hoiatamata.

---

## 4. samm: Kinnita API õigused

1. Mine **API permissions**
2. Kinnita, et **Microsoft Graph → User.Read** (delegated) on olemas — see lisatakse vaikimisi

`openid`, `profile` ja `email` skoopid, mida digna nõuab, on standardse OIDC komplekti osa ja ei vaja eraldi loa andmist. Kui teie tenant nõuab admin-nõusolekut kõigi rakenduste jaoks, klõpsake **Grant admin consent for &lt;tenant&gt;**.

---

## 5. samm: Koosta discovery URL

Asenda **Directory (tenant) ID** 2. sammast:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Kasuta v2.0 lõpp-punkti"

    `/v2.0/` osa on oluline. v1.0 lõpp-punkt aadressil `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` väljastab tokenid vanemas formaadis ja ei tagasta standardseid OIDC väiteid, mida digna eeldab.

Ava URL brauseris enne jätkamist. JSON-dokument kinnitab, et tenant ID on õige.

---

## 6. samm: Konfigureeri digna

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
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

Mõlemas failis peab `key` kattuma — siin on see `microsoft`.

---

## 7. samm: Testi

Taaskäivita backend ja veebiserver, seejärel ava dashboard. Täispõhjaliku kontrollnimekirja jaoks vaata [Testing Login](overview.md#testing-login).

---

## Entra ID tõrkeotsing

### AADSTS50011: Redirect URI Mismatch

URI `DIGNA_OIDC_REDIRECT_URI`-s erineb sellest, mis registreeriti 1. sammus. Entra ID võrdleb kogu stringi, nii et lõpus olev kaldkriips, `http` versus `https` või erinev port loevad kõik erinevuseks. Kontrolli **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Võimalik, et kopeeriti **Secret ID** asemel **Value**, või salajane väärtus on aegunud. Loo uus secret ja kopeeri Value veerg.

### AADSTS650057: Invalid Resource

Rakenduse registreering kustutati või kuulub teise tenanti kui see, mis on discovery URL-is. Kinnita Directory (tenant) ID Overview lehel.

### Kasutajad logivad sisse, aga midagi ei juhtu

Kui tenant nõuab admin-nõusolekut ja see pole antud, tagastatakse ümbersuunamisel kasutuskõlbmatu token. Anna admin-nõusolek all **API permissions**.

---

## Vaata ka

- [Single Sign-On Overview](overview.md) — konfiguratsiooni viide, testimine ja üldine tõrkeotsing
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
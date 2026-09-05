---
title: AD FS SSO – Ühekordse sisselogimise (SSO) integratsioon | digna dokumentatsioon
description: Konfigureerige digna jaoks ühekordne sisselogimine (SSO) Active Directory Federation Servicesiga kasutades OpenID Connecti — rakenduste grupp, serverirakendus, jagatud salajane võti, lubatud skoopid ja vastav digna konfiguratsioon.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, Active Directory Federation Services, adfs oidc, rakenduste grupp, OpenID Connect, kohapealne identiteedipakkuja
---

# SSO seadistamine AD FS-iga

Active Directory Federation Services on kohapealne (on‑premises) variant: teie enda serverid väljastavad tokenid ja avastuse URL on teie oma hostinimi. AD FS toetab OpenID Connecti alates **Windows Server 2016** versioonist.

See juhend käsitleb **AD FS-i poolt tehtavat osa**: rakenduste grupi loomist ja väärtuste kogumist, mida digna vajab. Digna pool — `dashboard_config.toml`, testimine ja tõrkeotsing — on iga pakkuja puhul sama ja on kirjeldatud [Single Sign-On Overview](overview.md)-s.

---

## Enne alustamist

| Nõue | Märkused |
|---|---|
| **AD FS versioon** | Windows Server 2016 või uuem — varasemad versioonid ei toeta OIDC-i |
| **Ligipääs** | Kohalik administraator AD FS serveris |
| **Föderatsiooniteenuse nimi** | nt `adfs.yourdomain.com` |
| **digna ümbersuunamise URI** | URL, kuhu kasutajaid suunatakse pärast sisselogimist, nt `https://digna.yourdomain.com/oidc/callback` |

---

## Samm 1: Loo rakenduste grupp

1. AD FS serveris avage **AD FS Management**
2. Paremklõpsake **Application Groups** ja valige **Add Application Group**
3. Sisestage nimeks `digna`
4. Valige **Standalone applications** — või sõltuvalt versioonist **Client-Server applications** — ning valige **Server application accessing a web API**
5. Klõpsake **Next**

---

## Samm 2: Konfigureerige serverirakendus

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS genereerib GUID-i. Kopeerige see — sellest saab `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: sisestage oma digna callback URL ja klõpsake **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Klõpsake **Next**

!!! warning "Klõpsake Add, mitte ainult Next"

    Redirect URI väljail on oma **Add** nupp. Kui kirjutate URI ja klikite ainult **Next** ilma **Add**-i vajutamata, see kadestatakse ning wizard ei anna hoiatust. Veenduge, et URI ilmub väljale allpool enne jätkamist.

---

## Samm 3: Genereerige jagatud salajane võti

1. Märkige **Generate a shared secret**
2. Kopeerige genereeritud secret → sellest saab `DIGNA_OIDC_CLIENT_SECRET`
3. Klõpsake **Next**

!!! warning "Salajast võtit kuvatakse ainult üks kord"

    AD FS kuvab jagatud salajast võtit ainult sellel viisardi lehel ja ei saa seda hiljem uuesti näidata. Kui kaotate selle, lähtestage see hiljem rakenduse grupi atribuutidest.

---

## Samm 4: Konfigureerige Web API

1. **Identifier**: sisestage sama client identifier nagu Samm 2-st ja klõpsake **Add**
2. Klõpsake **Next**
3. Valige **Access Control Policy** — *Permit everyone* on lihtsaim alguseks; tootmises piira see grupile
4. Klõpsake **Next**

---

## Samm 5: Määrake lubatud skoopid

Configure Application Permissions sammuga, märkige:

- `openid`
- `profile`
- `email`

Seejärel klõpsake **Next** ja lõpetage viisard.

!!! warning "openid ei ole vaikimisi valitud"

    Mõnes AD FS versioonis on eelvalitud ainult `user_impersonation`. Ilma `openid`-ita tagastab token endpoint OAuth access tokeni, mitte ID tokeni, ja digna ei saa kasutajat tuvastada.

---

## Samm 6: Kinnitage avastuse (discovery) lõpp-punkt

Asendage oma föderatsiooniteenuse nimi:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Näiteks:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Avage see brauseris. JSON-dokument kinnitab, et OIDC on lubatud ja hostinimi on õige.

!!! note "Backend peab sertifikaati usaldama"

    Sise-sertifikaadi väljaandja on AD FS puhul tavaline. Masin, kus jookseb digna backend, teeb selle URL-i poole väljamineva HTTPS-päringu, seega peab sertifikaati väljastanud CA olema selle masina usaldatud sertifikaatide hulgas — mitte ainult nende inimeste brauserites, kes sisse logivad.

---

## Samm 7: Konfigureerige digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Logi sisse Active Directory'ga"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Mõlemas failis peab `key` vastama — siin on see `adfs`.

---

## Samm 8: Testimine

Taaskäivitage backend ja veebiserver, seejärel avage dashboard. Täispuhuliku kontrollnimekirja jaoks vaadake [Testing Login](overview.md#testing-login).

---

## AD FS tõrkeotsing

### MSIS9611: The Client Is Not Allowed to Access the Resource

Web API identifier Samm 4-s ei kattu client identifieriga või Samm 5-s ei olnud skoopid antud. Mõlemat saab muuta rakenduse grupi omadustest.

### MSIS9602: Invalid redirect_uri

URI kirjutati välja, aga ei lisatud **Add** nupuga, või see erineb `DIGNA_OIDC_REDIRECT_URI`-st. Kontrollige **Application Groups → digna → digna backend → Properties**.

### ID-tokeni ei tagastata

Rakenduse õigustest puudub `openid` skoop.

### Backend ei saa avastuse URL-ini ühendust

Või DNS resolvib föderatsiooniteenuse nime valesti backend-masinas, või AD FS sertifikaati ei usaldata seal. Testimiseks käivitage serverist ise `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration`.

### Sündmused, mida kontrollida

AD FS server logib vead Event Viewerisse sektsiooni **Applications and Services Logs → AD FS → Admin**, kus on tavaliselt brauserile kuvatust konkreetsem põhjus.

---

## Vaata ka

- [Single Sign-On Overview](overview.md) — konfiguratsiooni viide, testimine ja üldine tõrkeotsing
- [Microsoft: AD FS OpenID Connect stsenaariumid](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
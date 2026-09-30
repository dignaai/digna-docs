---
title: AD FS SSO — Single Sign-On integrācija | digna dokumentācija
description: Konfigurējiet Single Sign-On (SSO) digna, izmantojot Active Directory Federation Services un OpenID Connect — lietotņu grupa, servera lietotne, koplietotā slepenā atslēga, atļautie scope un atbilstošā digna konfigurācija.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, active directory federation services, adfs oidc, lietotņu grupa, OpenID Connect, lokāls identitātes nodrošinātājs
---

# Iestatīt SSO ar AD FS

Active Directory Federation Services ir lokālās (on-premises) izvietošanas variants: tokenus izsniedz jūsu pašu serveri, un atklāšanas (discovery) URL ir jūsu pašu resursdatora nosaukums. AD FS atbalsta OpenID Connect, sākot no **Windows Server 2016**.

Šis ceļvedis aptver **AD FS pusi**: lietotņu grupas izveidi un vērtību vākšanu, kas nepieciešamas digna. digna puse — `dashboard_config.toml`, testēšana un problēmu novēršana — ir vienāda visiem pakalpojumu sniedzējiem un aprakstīta [Single Sign-On pārskatā](overview.md).

---

## Pirms sākat

| Prasība | Piezīmes |
|---|---|
| **AD FS versija** | Windows Server 2016 vai jaunāka — vecākās versijās nav OIDC atbalsta |
| **Piekļuve** | Lokālā administratora tiesības AD FS serverī |
| **Federācijas pakalpojuma nosaukums** | piem. `adfs.yourdomain.com` |
| **digna redirect URI** | URL, uz kuru lietotāji atgriežas pēc pieteikšanās, piem. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. solis: Izveidot lietotņu grupu

1. AD FS serverī atveriet **AD FS Management**
2. Ar peles labo pogu noklikšķiniet uz **Application Groups** un izvēlieties **Add Application Group**
3. Kā nosaukumu ievadiet `digna`
4. Sadaļā **Standalone applications** — vai **Client-Server applications**, atkarībā no jūsu versijas — atlasiet **Server application accessing a web API**
5. Noklikšķiniet **Next**

---

## 2. solis: Konfigurēt servera lietotni

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS ģenerē GUID. Nokopējiet to — tas kļūst par `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: ievadiet savu digna callback URL un noklikšķiniet **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Noklikšķiniet **Next**

!!! warning "Noklikšķiniet Add, nevis tikai Next"

    Redirect URI laukam ir sava **Add** poga. Ja ievadāt URI un noklikšķināt **Next**, nenospiežot **Add**, tas tiek atmests, un vednis nebrīdina. Pirms turpināt, pārliecinieties, ka URI ir redzams sarakstā zem lauka.

---

## 3. solis: Ģenerēt koplietoto slepeno atslēgu

1. Atzīmējiet **Generate a shared secret**
2. Nokopējiet ģenerēto slepeno atslēgu → kļūst par `DIGNA_OIDC_CLIENT_SECRET`
3. Noklikšķiniet **Next**

!!! warning "Slepenā atslēga tiek parādīta tikai vienreiz"

    AD FS parāda koplietoto slepeno atslēgu tikai šajā vedņa lapā un vairs nevar to parādīt atkārtoti. Ja to pazaudējat, vēlāk atiestatiet to lietotņu grupas rekvizītos.

---

## 4. solis: Konfigurēt Web API

1. **Identifier**: ievadiet to pašu klienta identifikatoru no 2. soļa un noklikšķiniet **Add**
2. Noklikšķiniet **Next**
3. Izvēlieties **Access Control Policy** — *Permit everyone* ir vienkāršākais sākumpunkts; ražošanas videi ierobežojiet to ar grupu
4. Noklikšķiniet **Next**

---

## 5. solis: Piešķirt atļautos scope

Solī **Configure Application Permissions** atzīmējiet:

- `openid`
- `profile`
- `email`

Pēc tam noklikšķiniet **Next** un pabeidziet vedni.

!!! warning "openid pēc noklusējuma nav atzīmēts"

    Dažās versijās AD FS iepriekš atlasa tikai `user_impersonation`. Bez `openid` tokena gala punkts atgriež OAuth piekļuves tokenu, nevis ID tokenu, un digna nevar identificēt lietotāju.

---

## 6. solis: Pārbaudīt discovery gala punktu

Ievietojiet sava federācijas pakalpojuma nosaukumu:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Piemēram:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Atveriet to pārlūkā. JSON dokuments apstiprina, ka OIDC ir iespējots un resursdatora nosaukums ir pareizs.

!!! note "Backend jāuzticas sertifikātam"

    AD FS bieži izmanto iekšēju sertifikācijas iestādi (CA). Dators, kurā darbojas digna backend, pats veic izejošu HTTPS pieprasījumu uz šo URL, tāpēc izdevējai CA jābūt šī datora uzticamo sertifikātu krātuvē — ne tikai to lietotāju pārlūkos, kuri piesakās.

---

## 7. solis: Konfigurēt digna

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
[oidc_clients.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Abos failos `key` vērtībai jāsakrīt — šeit `adfs`.

---

## 8. solis: Testēt

Restartējiet backend un web serveri, pēc tam atveriet dashboard. Pilnu pārbaudes sarakstu skatiet sadaļā [Pieteikšanās testēšana](overview.md#testing-login).

---

## AD FS problēmu novēršana

### MSIS9611: The Client Is Not Allowed to Access the Resource

Web API identifikators 4. solī nesakrīt ar klienta identifikatoru, vai arī 5. solī netika piešķirti scope. Abus var rediģēt lietotņu grupas rekvizītos.

### MSIS9602: Invalid redirect_uri

URI tika ievadīts, bet nav pievienots ar pogu **Add**, vai arī tas atšķiras no `DIGNA_OIDC_REDIRECT_URI`. Pārbaudiet **Application Groups → digna → digna backend → Properties**.

### ID tokens netiek atgriezts

Lietotnes atļaujās trūkst `openid` scope.

### Backend nevar sasniegt discovery URL

Vai nu backend resursdatora DNS neatrisina federācijas pakalpojuma nosaukumu, vai arī AD FS sertifikāts tur nav uzticams. Pārbaudiet ar `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` tieši no digna servera.

### Pārbaudāmie notikumi

AD FS serveris reģistrē kļūmes Event Viewer sadaļā **Applications and Services Logs → AD FS → Admin**, parasti ar konkrētāku iemeslu, nekā redzams pārlūkā.

---

## Skatīt arī

- [Single Sign-On pārskats](overview.md) — konfigurācijas atsauce, testēšana un vispārīga problēmu novēršana
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)

---
title: AD FS SSO – Vienkartinis prisijungimas | digna dokumentacija
description: Konfigūruokite vienkartinį prisijungimą (Single Sign-On) digna su Active Directory Federation Services naudojant OpenID Connect — aplikacijos grupė, serverio aplikacija, bendras slaptasis raktas, leidžiami scopes ir atitinkama digna konfigūracija.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, Active Directory Federation Services, adfs oidc, aplikacijų grupė, OpenID Connect, on-premises tapatybės teikėjas
---

# SSO nustatymas su AD FS

Active Directory Federation Services yra vietinis sprendimas: jūsų patys serveriai išduoda žetonus, o discovery URL yra jūsų host vardas. AD FS palaiko OpenID Connect nuo **Windows Server 2016** versijos ir vėlesnių.

Šis vadovas aptaria **AD FS pusę**: aplikacijos grupės kūrimą ir reikšmių, kurių reikia digna, surinkimą. digna pusė — `dashboard_config.toml`, testavimas ir trikčių šalinimas — yra vienoda visiems tiekėjams ir aprašyta [Single Sign-On apžvalgoje](overview.md).

---

## Prieš pradėdami

| Reikalavimas | Pastabos |
|---|---|
| **AD FS versija** | Windows Server 2016 arba naujesnė — ankstesnės versijos neturi OIDC palaikymo |
| **Prieiga** | Vietinis administratorius AD FS serveryje |
| **Federacijos paslaugos pavadinimas** | pvz. `adfs.yourdomain.com` |
| **digna persiuntimo URI** | URL, į kurį vartotojai grįžta po prisijungimo, pvz. `https://digna.yourdomain.com/oidc/callback` |

---

## 1 žingsnis: Sukurkite aplikacijų grupę

1. AD FS serveryje atidarykite **AD FS Management**
2. Dešiniuoju pelės mygtuku spustelėkite **Application Groups** ir pasirinkite **Add Application Group**
3. Įveskite pavadinimą `digna`
4. Skiltyje **Standalone applications** — arba **Client-Server applications** priklausomai nuo versijos — pasirinkite **Server application accessing a web API**
5. Spustelėkite **Next**

---

## 2 žingsnis: Konfigūruokite serverio aplikaciją

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS sugeneruos GUID. Kopijuokite jį — tai taps `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: įveskite savo digna callback URL ir spustelėkite **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Spustelėkite **Next**

!!! warning "Spustelėkite Add, ne tik Next"

    Redirect URI laukas turi savo **Add** mygtuką. Įvedus URI ir spustelėjus **Next** be **Add** paspaudimo, jis bus atmestas, o vedlys nepateiks įspėjimo. Prieš tęsiant įsitikinkite, kad URI matomas po lauku esančiame sąraše.

---

## 3 žingsnis: Sugeneruokite bendrą slaptą raktą

1. Pažymėkite **Generate a shared secret**
2. Nukopijuokite sugeneruotą slaptą raktą → taps `DIGNA_OIDC_CLIENT_SECRET`
3. Spustelėkite **Next**

!!! warning "Slaptasis raktas rodomas tik vieną kartą"

    AD FS šį slaptą raktą parodo tik šiame vedlio puslapyje ir negali jo parodyti vėliau. Jeigu jį prarasite, vėliau atstatykite iš aplikacijos grupės nuostatų.

---

## 4 žingsnis: Konfigūruokite Web API

1. **Identifier**: įveskite tą patį klientų identifikatorių iš 2 žingsnio ir spustelėkite **Add**
2. Spustelėkite **Next**
3. Pasirinkite **Access Control Policy** — *Permit everyone* yra paprasčiausias pradinis pasirinkimas; gamyboje apribokite prieigą konkrečiai grupei
4. Spustelėkite **Next**

---

## 5 žingsnis: Priskirkite leidžiamus scopes

Konfigūracijos žingsnyje **Configure Application Permissions** pažymėkite:

- `openid`
- `profile`
- `email`

Tada spustelėkite **Next** ir užbaikite vedlį.

!!! warning "openid nėra pažymėtas pagal numatytąją reikšmę"

    Kai kuriose AD FS versijose pagal numatytąją reikšmę pažymima tik `user_impersonation`. Jei nėra `openid`, token endpoint grąžina OAuth access token vietoje ID token, ir digna negalės identifikuoti vartotojo.

---

## 6 žingsnis: Patikrinkite discovery endpointą

Pakeiskite savo federacijos paslaugos vardą:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Pavyzdžiui:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Atidarykite naršyklėje. JSON dokumentas patvirtins, kad OIDC įjungtas ir host vardas teisingas.

!!! note "Back-end'as turi pasitikėti sertifikatu"

    Vidinė sertifikavimo institucija dažnai naudojama AD FS diegimuose. Mašina, kurioje veikia digna backend'as, pati atlieka išeinančius HTTPS užklausimus į šį URL, todėl išduodančios CA sertifikatas turi būti pridėtas į tos mašinos trust store — ne tik naršyklių tų, kurie prisijungia.

---

## 7 žingsnis: Konfigūruokite digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Prisijungti per Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<slaptasis raktas nukopijuotas 3 žingsnyje>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Abiejuose failuose `key` turi sutapti — čia `adfs`.

---

## 8 žingsnis: Testavimas

Perkraukite backend'ą ir žiniatinklio serverį, tada atidarykite dashboard. Pilną kontrolinį sąrašą rasite [Single Sign-On apžvalgoje](overview.md#testing-login).

---

## Trikčių šalinimas AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

Web API identifikatorius 4 žingsnyje neatitinka klientų identifikatoriaus, arba 5 žingsnyje nebuvo priskirtos reikalingos priemonės (scopes). Abu nustatymai keičiami aplikacijos grupės savybėse.

### MSIS9602: Invalid redirect_uri

URI buvo įvestas, bet neįtrauktas per **Add** mygtuką, arba skiriasi nuo `DIGNA_OIDC_REDIRECT_URI`. Patikrinkite **Application Groups → digna → digna backend → Properties**.

### ID token negrąžinamas

Trūksta `openid` scope iš aplikacijos leidimų.

### Backend'as negali pasiekti discovery URL

Arba DNS backend'o serveryje neišsprendžia federacijos paslaugos vardo, arba AD FS sertifikatas ten nėra pasitikimas. Išbandykite su `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` iš digna serverio.

### Įvykiai, kuriuos verta patikrinti

AD FS serveris klaidas užrašo Event Viewer'e: **Applications and Services Logs → AD FS → Admin**, dažnai su konkretesne informacija nei naršyklės rodoma klaida.

---

## Taip pat žiūrėkite

- [Single Sign-On apžvalga](overview.md) — konfigūravimo nuoroda, testavimas ir bendras trikčių šalinimas
- [Microsoft: AD FS OpenID Connect scenarijai](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
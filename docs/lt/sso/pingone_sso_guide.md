---
title: PingOne SSO – Vienkartinio prisijungimo (SSO) integracija | digna dokumentacija
description: Sukonfigūruokite vienkartinį prisijungimą (Single Sign-On) digna naudojant PingOne per OpenID Connect — OIDC Web App nustatymas, peradresavimo URI, kliento kredencialai, aplinkos ID, regioniniai domenai ir atitinkama digna konfigūracija.
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, aplinkos ID, environment id, openid connect, įmonės autentifikacija
---

# SSO su PingOne nustatymas

PingOne atitinka OIDC standartą. Dvi jo reikšmės reikalauja dėmesio: **aplinkos ID** (environment ID), kuris yra kiekvieno galinio taško URL dalis, ir **regioninis domenas**, kuris skiriasi Šiaurės Amerikos, Europos, Kanados, Azijos ir Ramiojo vandenyno bei Australijos nuomininkams (tenants).

Ši instrukcija apima **PingOne pusę**: programos sukūrimą ir verčių, kurių reikia digna, surinkimą. digna pusė — `dashboard_config.toml`, testavimas ir trikčių šalinimas — yra tokia pati visiems tiekėjams ir aprašyta [Vienkartinio prisijungimo (SSO) apžvalgoje](overview.md).

---

## Prieš pradėdami

| Reikalavimas | Pastabos |
|---|---|
| **PingOne rolė** | Environment Admin arba Identity Data Admin tikslinėje aplinkoje |
| **Aplinka** | PingOne aplinka, kuriai priklauso jūsų digna vartotojai |
| **digna peradresavimo URI** | URL, į kurį vartotojai grįžta po prisijungimo, pvz. `https://digna.yourdomain.com/oidc/callback` |

---

## 1 žingsnis: Sukurkite programą

1. Prisijunkite prie PingOne administravimo konsolės ir pasirinkite savo aplinką
2. Eikite į **Applications → Applications**
3. Spauskite mygtuką **+**
4. Laukelyje **Application Name** įveskite `digna`
5. Pasirinkite **OIDC Web App**
6. Spauskite **Save**

!!! warning "Rinkitės OIDC Web App, o ne Single-Page App"

    *Single-Page App* ir *Native App* sukuria viešuosius klientus, kurie negali saugoti slaptumo rakto. digna keičia autorizacijos kodą savo backend'e, todėl jai reikia konfidencialaus **OIDC Web App** tipo.

---

## 2 žingsnis: Sukonfigūruokite peradresavimo URI

1. Atidarykite programos skirtuką **Configuration**
2. Spauskite pieštuko piktogramą, kad redaguotumėte
3. Patikrinkite, ar **Response Type** yra *Code*, o **Grant Type** yra *Authorization Code*
4. Skiltyje **Redirect URIs** įveskite savo digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

5. **Token Endpoint Authentication Method** nustatykite į *Client Secret Post* arba *Client Secret Basic*
6. Spauskite **Save**

---

## 3 žingsnis: Įjunkite programą

Programos eilutėje arba detalių skydelyje perjunkite jungiklį į **enabled**.

!!! warning "Naujos programos sukuriamos išjungtos"

    PingOne sukuria programas išjungtoje būsenoje. Išjungta programa autorizacijos žingsnyje grąžina klaidą, kurioje jungiklis neminimas, todėl verta tai patikrinti prieš ieškant kitų klaidų.

---

## 4 žingsnis: Suteikite apimtis (scopes)

1. Atidarykite skirtuką **Resources**
2. Patikrinkite, ar suteikta `openid`, ir pridėkite `profile` bei `email` iš resurso **OpenID Connect**
3. Spauskite **Save**

---

## 5 žingsnis: Priskirkite vartotojus

1. Atidarykite skirtuką **Access**
2. Pridėkite populiaciją (population) arba grupes, kurių nariai gali naudotis digna
3. Spauskite **Save**

---

## 6 žingsnis: Surinkite kredencialus ir aplinkos ID

Skirtuke **Configuration** išskleiskite **General**:

- **Client ID** → tampa `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → tampa `DIGNA_OIDC_CLIENT_SECRET` (spauskite akies piktogramą)
- **Environment ID** → įrašomas į atradimo (discovery) URL

Tame pačiame skirtuke nurodytas ir paruoštas **OIDC Discovery Endpoint**, kurį galite nukopijuoti tiesiogiai, užuot sudarinėję rankiniu būdu.

---

## 7 žingsnis: Sudarykite atradimo URL

Įrašykite aplinkos ID ir savo regiono domeną:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Regionas | Domenas |
|---|---|
| Šiaurės Amerika | `auth.pingone.com` |
| Europa | `auth.pingone.eu` |
| Kanada | `auth.pingone.ca` |
| Azija ir Ramusis vandenynas | `auth.pingone.asia` |
| Australija | `auth.pingone.com.au` |

Europos aplinkai:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Kopijuokite, o ne rašykite ranka"

    Regioninis domenas yra dažniausia klaida PingOne integracijoje, o neteisingas regionas grąžina 404, o ne naudingą pranešimą. Naudokite **OIDC Discovery Endpoint** reikšmę iš 6 žingsnio.

---

## 8 žingsnis: Konfigūruokite digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc_clients.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Abiejuose failuose `key` turi sutapti — čia `pingone`.

---

## 9 žingsnis: Išbandykite

Perkraukite backend ir web serverį, tada atidarykite dashboard. Visą kontrolinį sąrašą rasite skyriuje [Prisijungimo testavimas](overview.md#testing-login).

---

## PingOne trikčių šalinimas

### 404 atradimo URL

Neteisingas regioninis domenas arba aplinkos ID. Palyginkite su **OIDC Discovery Endpoint**, rodomu programos skirtuke Configuration.

### NOT_FOUND arba Application Disabled

Programos jungiklis iš 3 žingsnio vis dar išjungtas.

### Redirect URI Mismatch

PingOne lygina visą eilutę. Patikrinkite **Configuration → Redirect URIs**, ar nėra galinio brūkšnio (/) arba schemos skirtumo.

### Prisijungimas pavyksta, bet email teiginys (claim) nepasiekia digna

Skirtuke **Resources** nesuteiktos apimtys `email` ir `profile`.

### Vartotojas nemato programos

Skirtuke **Access** jokiai populiacijai ar grupei nesuteikta prieiga.

---

## Taip pat žiūrėkite

- [Vienkartinio prisijungimo (SSO) apžvalga](overview.md) — konfigūracijos nuorodos, testavimas ir bendras trikčių šalinimas
- [PingOne: OIDC programos konfigūracija](https://docs.pingidentity.com/pingone/)

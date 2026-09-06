# SSO su Okta nustatymas

Okta atitinka OIDC standartą, tačiau yra vienas niuansas, kuris dažnai painioja pirmą kartą integruojančius: Okta organizacija gali turėti daugiau nei vieną autorizacijos serverį, ir kiekvienas jų turi savo atradimo (discovery) URL.

Ši instrukcija apima **Okta pusę**: programos integracijos sukūrimą ir verčių, kurių reikia digna, surinkimą. digna pusė — `dashboard_config.toml`, testavimas ir trikčių šalinimas — yra tokia pati visiems tiekėjams ir aprašyta [Single Sign-On Overview](overview.md).

---

## Prieš pradėdami

| Reikalavimas | Pastabos |
|---|---|
| **Okta teisės** | Super Administratorius arba admin rolė, kuriai leista kurti programų integracijas |
| **Okta domenas** | pvz. `yourcompany.okta.com`, arba pritaikytas domenas, jei sukonfigūruotas |
| **digna peradresavimo URI** | URL, į kurį vartotojai grįžta po prisijungimo, pvz. `https://digna.yourdomain.com/oidc/callback` |

---

## 1 žingsnis: Sukurkite programos integraciją

1. Prisijunkite prie Okta administravimo konsolės
2. Eikite į **Applications → Applications**
3. Spauskite **Create App Integration**
4. Pasirinkite:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Spauskite **Next**

!!! warning "Programos tipo negalima pakeisti"

    Jei vietoje *Web Application* pasirinksite *Single-Page Application*, bus sukurtas viešasis klientas be slaptumo rakto, ir digna backend'o kodo mainas (code exchange) nepavyks su klaida `invalid_client`. Tipo negalima pakeisti po sukūrimo — klaidingas pasirinkimas reiškia, kad reikės ištrinti programą ir pradėti iš naujo.

---

## 2 žingsnis: Konfigūruokite integraciją

1. **App integration name**: `digna`
2. **Grant type**: palikite pažymėtą *Authorization Code*
3. **Sign-in redirect URIs**: įveskite savo digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: neprivaloma
5. Skiltyje **Assignments** pasirinkite, kas gali naudotis integracija — saugiau nurodyti konkrečią grupę nei *Allow everyone in your organization to access*
6. Spauskite **Save**

!!! note "Paskyrimas būtinas"

    Okta autentifikuoja vartotoją ir tada tikrina, ar jis yra priskirtas programai. Nepriskirtas vartotojas pasiekia Okta prisijungimo puslapį, sėkmingai prisijungia, bet jam bus uždrausta pereiti per peradresavimą atgal. Jei prisijungimas veikia jums, bet neveikia kolegoms, pirmas dalykas — patikrinti priskyrimą.

---

## 3 žingsnis: Surinkite kredencialus

Programos **General** skirtuke, skiltyje **Client Credentials**:

- **Client ID** → tampa `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → tampa `DIGNA_OIDC_CLIENT_SECRET` (spauskite akies piktogramą, kad atskleistumėte)

---

## 4 žingsnis: Pasirinkite autorizacijos serverį

Tai yra žingsnis, kuris nulemia jūsų atradimo URL. Eikite į **Security → API**, kad pamatytumėte organizacijos autorizacijos serverius.

**Org autorizacijos serveris** — išduoda žetonus pačiai Okta organizacijai:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom autorizacijos serveris** — įskaitant tą, kurį Okta sukuria pavadinimu `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Integruotam serveriui `<auth_server_id>` tiesiogiai yra `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Kurį pasirinkti?"

    Naudokite **org** autorizacijos serverį, nebent jūsų organizacija jau standartizavo naudoti custom serverį API prieigos politikoms. Okta Developer paskyrose pagal nutylėjimą naudojamas `default`; daugelyje įmonių organizacijų jis gali būti išjungtas. Atidarykite abu URL naršyklėje — tas, kuris grąžina JSON vietoje klaidos, yra prieinamas jums.

---

## 5 žingsnis: Konfigūruokite digna

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

Abiejuose failuose `key` turi sutapti — čia `okta`.

---

## 6 žingsnis: Išbandykite

Perkraukite backend ir web serverį, tada atidarykite dashboard. Visą kontrolinį sąrašą rasite [Prisijungimo testavimas](overview.md#testing-login).

---

## Trikčių šalinimas Okta

### Peradresavimo URI nėra registruotas

Okta klaidoje nurodo probleminį URI. Palyginkite jį su **General → Sign-in redirect URIs**; Okta lygina visą eilutę, įskaitant bet kokį galinį brūkšnį (/).

### Vartotojas nėra priskirtas klientinei programai

Paskyra nėra programos priskyrimų sąraše. Pridėkite vartotoją arba jo grupę skiltyje **Assignments**.

### 400 Bad Request: Invalid Authorization Server

Atraskyto URL `<auth_server_id>` neegzistuoja — dažniausiai `default` org, kur jis buvo pašalintas. Patikrinkite **Security → API**, kokie serveriai iš tiesų yra prieinami.

### invalid_client token žingsnyje

Integracija buvo sukurta kaip Single-Page Application ir neturi kliento slaptumo rakto. Sukurkite ją iš naujo kaip Web Application.

---

## Taip pat žiūrėkite

- [Single Sign-On Overview](overview.md) — konfigūracijos nuorodos, testavimas ir bendras trikčių šalinimas
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
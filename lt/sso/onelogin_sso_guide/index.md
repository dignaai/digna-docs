# SSO nustatymas su OneLogin

OneLogin palaiko OIDC. Jo išskirtinė savybė yra ta, kad konektoriaus tipas pasirenkamas iš katalogo kuriant programą ir vėliau negali būti pakeistas.

Šis gidas apima **OneLogin pusę**: programos kūrimą ir reikšmes, kurių reikia digna surinkimą. digna pusė — `dashboard_config.toml`, testavimas ir trikčių šalinimas — yra ta pati kiekvienam tiekėjui ir aprašyta [Single Sign-On Overview](overview.md).

---

## Prieš pradėdami

| Reikalavimas | Pastabos |
|---|---|
| **OneLogin vaidmuo** | Sąskaitos savininkas arba administratorius, kuriam leidžiama pridėti programas |
| **Subdomenas** | pvz. `yourcompany.onelogin.com` |
| **digna peradresavimo URI** | URL, į kurį vartotojai grįžta po prisijungimo, pvz. `https://digna.yourdomain.com/oidc/callback` |

---

## 1 žingsnis: Sukurkite OIDC programą

1. Prisijunkite prie OneLogin administravimo portalo
2. Eikite į **Applications → Applications**
3. Spustelėkite **Add App**
4. Ieškokite `OpenId Connect` ir pasirinkite **OpenId Connect (OIDC)** konektorių
5. Nustatykite **Display Name** į `digna`
6. Spustelėkite **Save**

!!! warning "Konektoriaus tipas nustatomas kūrimo metu"

    OneLogin turi atskiras katalogo įrašų eilutes SAML ir OIDC, ir programos negalima konvertuoti iš vieno į kitą. Jei netyčia pasirinkote SAML konektorių, ištrinkite programą ir pridėkite ją iš naujo — nėra nustatymo, kad būtų galima perjungti protokolus.

---

## 2 žingsnis: Konfigūruokite peradresavimo URI

1. Atidarykite **Configuration** skirtuką
2. Lauke **Redirect URI's** įrašykite savo digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Pasirinktinai nustatykite **Post Logout Redirect URIs** į savo dashboard URL
4. Spustelėkite **Save**

!!! note "Vienas URI per eilutę"

    Skirtingai nuo tiekėjų, kurie tikisi kableliu atskirto sąrašo, OneLogin laukas **Redirect URI's** priima po vieną URI kiekvienoje eilutėje.

---

## 3 žingsnis: Nustatykite programos tipą ir autentifikacijos metodą

1. Atidarykite **SSO** skirtuką
2. Patikrinkite, kad **Application Type** būtų *Web*
3. Nustatykite **Token Endpoint → Authentication Method** į *POST* (`client_secret_post`) arba *Basic* (`client_secret_basic`)

!!! warning "Nesirinkite *None*"

    Jei autentifikacijos metodą nustatysite į *None*, programa taps viešu klientu be slaptojo rakto ir digna backend'o kodo mainai bus atmesti. Tinka arba POST, arba Basic.

---

## 4 žingsnis: Surinkite kredencialus

Vis dar **SSO** skirtuke:

- **Client ID** → tampa `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → tampa `DIGNA_OIDC_CLIENT_SECRET` (spustelėkite **Show client secret**)

Puslapyje taip pat matyti **Issuer URL**, kuris patvirtina atradimo (discovery) URL kitame žingsnyje.

---

## 5 žingsnis: Priskirkite vartotojus

1. Atidarykite **Access** skirtuką
2. Pridėkite vaidmenis arba grupes, kurių nariai gali naudotis digna
3. Spustelėkite **Save**

!!! note "Nepriskirti vartotojai po prisijungimo yra atmetami"

    Kaip ir daugelyje tiekėjų, OneLogin pirmiausia autentifikuoja vartotoją, o antra patikrina jo teises. Nepriskirtas vartotojas sėkmingai prisijungia, bet po to jam yra uždrausta prieiga — tai atrodo kaip digna klaida, o ne kaip sprendimas dėl prieigos kontrolės.

---

## 6 žingsnis: Sudarykite discovery URL

Pakeiskite savo OneLogin subdomeną:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Pavyzdžiui:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip " /2 yra API versija"

    Dabartinė OneLogin OIDC įgyvendinimo vieta yra po `/oidc/2/`. Senesnė dokumentacija rodo `/oidc/` be versijos, kuri nurodo pasenusią pirmąją versiją. Jei abejojate, palyginkite su **Issuer URL** SSO skirtuke — discovery URL yra issuer plius `/.well-known/openid-configuration`.

---

## 7 žingsnis: Konfigūruokite digna

### Konfigūracija: `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### Konfigūracija: `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Raktas `key` abiejuose failuose turi sutapti — čia `onelogin`.

---

## 8 žingsnis: Testavimas

Paleiskite iš naujo backend'ą ir web serverį, tada atidarykite dashboard. Pilną patikrų sąrašą žr. [Testing Login](overview.md#testing-login).

---

## OneLogin trikčių šalinimas

### redirect_uri nesutapo

Callback URL nėra įtrauktas į **Configuration → Redirect URI's**, arba įrašai buvo atskirti kableliais vietoje naujų eilučių.

### invalid_client token žingsnyje

**Token Endpoint → Authentication Method** nustatytas į *None*, arba `config.toml` esantis kliento slaptažodis yra pasenęs. Atidarykite paslaptį **SSO** skirtuke ir palyginkite.

### Programa nėra matoma vartotojams

Nėra priskirtos rolės arba grupės **Access** skirtuke.

### 404 atradimo (Discovery) URL

Neteisingas subdomenas arba URL praleidžia `/oidc/2/`. Palyginkite su **Issuer URL**, rodomu SSO skirtuke.

---

## Žr. taip pat

- [Single Sign-On Overview](overview.md) — konfigūracijos nuoroda, testavimas ir bendras trikčių šalinimas
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)
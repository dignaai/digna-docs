# SSO nustatymas su Auth0

Auth0 atitinka OIDC specifikaciją ir kiekvienam nuomininkui pateikia discovery endpoint'ą. Svarbiausia teisingai nurodyti nuomininko domeną, kuris atsiranda discovery URL ir keičiasi, jei įjungiate pasirinktą (custom) domeną.

Šis vadovas apima **Auth0 pusę**: programėlės sukūrimą ir reikšmių, kurių reikia digna, surinkimą. digna pusė — `dashboard_config.toml`, testavimas ir trikčių šalinimas — yra vienoda visiems tiekėjams ir aprašyta [Single Sign-On Overview](overview.md).

---

## Prieš pradėdami

| Reikalavimas | Pastabos |
|---|---|
| **Auth0 vaidmuo** | Nuomininko administratorius |
| **Nuomininko domenas** | pvz. `yourcompany.eu.auth0.com` — regiono segmentas yra svarbus |
| **digna redirect URI** | URL, į kurį vartotojai grįžta po prisijungimo, pvz. `https://digna.yourdomain.com/oidc/callback` |

---

## 1 žingsnis: Sukurkite programą

1. Prisijunkite prie [Auth0 Dashboard](https://manage.auth0.com)
2. Eikite į **Applications → Applications**
3. Spauskite **Create Application**
4. Pavadinkite ją `digna` ir pasirinkite **Regular Web Applications**
5. Spauskite **Create**

!!! warning "Pasirinkite Regular Web Applications"

    *Single Page Application* ir *Native* sukuria viešus klientus be slaptumo (secret). digna atlieka kodų mainus iš savo backend'o ir reikalauja konfidencialaus kliento, todėl teisingas tipas yra **Regular Web Applications**. Skirtingai nuo kai kurių tiekėjų, Auth0 leidžia vėliau pakeisti tipą skiltyje **Settings → Application Type**.

---

## 2 žingsnis: Pridėkite callback URL

Programėlės skiltyje **Settings**:

1. Suraskite **Allowed Callback URLs**
2. Įveskite savo digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Pagal pageidavimą nustatykite **Allowed Logout URLs** į savo dashbord URL
4. Slinkite žemyn ir spauskite **Save Changes**

!!! note "Kableliais atskirta, o ne naujomis eilutėmis"

    Auth0 priima kelis callback URL šiame lauke, atskirtus kableliais. Sąrašas, atskirtas tik naujomis eilutėmis, bus skaitomas kaip vienas neteisingas URL ir tyliai niekam neatitiks.

---

## 3 žingsnis: Surinkite kredencialus

Vis dar skiltyje **Settings**, bloke **Basic Information**:

- **Domain** → patenka į discovery URL
- **Client ID** → tampa `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → tampa `DIGNA_OIDC_CLIENT_SECRET` (spauskite, kad parodytumėte)

---

## 4 žingsnis: Patikrinkite grant tipo nustatymą

1. Eikite į **Settings → Advanced Settings → Grant Types**
2. Patikrinkite, ar pažymėta **Authorization Code**

Tai yra įjungta pagal nutylėjimą Regular Web Applications tipo programėlėms. Jei tai buvo atžymėta, digna prisijungimas nepavyksta su klaida `unauthorized_client`.

---

## 5 žingsnis: Sudarykite discovery URL

Pakeiskite **Domain** iš 3 žingsnio:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Pavyzdžiui:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Pasirinkti domenai keičia issuer reikšmę"

    Jei jūsų nuomininkas naudoja pasirinktą domeną, pvz. `login.yourcompany.com`, naudokite tą domeną discovery URL. Maišymas — canonical domenas discovery URL, o naršyklėje naudojamas custom domenas — sukelia issuer neatitikimą, ir tokenas bus atmestas po kitaip sėkmingo prisijungimo.

---

## 6 žingsnis: Konfigūruokite digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Prisijungti su Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

`key` abiejuose failuose turi sutapti — čia tai `auth0`.

---

## 7 žingsnis: Testavimas

Paleiskite iš naujo backend'ą ir web serverį, tada atverkite dashboard. Pilną testavimo kontrolinį sąrašą žr. [Testing Login](overview.md#testing-login).

---

## Trikčių šalinimas su Auth0

### Callback URL neatitikimas

Auth0 klaidų puslapis nurodo gautą URL. Pridėkite jį prie **Allowed Callback URLs**, patikrinkite, kad įrašai būtų atskirti kableliais.

### unauthorized_client

**Authorization Code** nėra įjungtas skiltyje **Advanced Settings → Grant Types**, arba programėlės tipas nėra Regular Web Applications.

### Prieiga uždrausta po sėkmingo prisijungimo

Nuomininko Rule, Action arba Post-Login trigger'is atmeta vartotoją. Patikrinkite **Actions → Flows → Login** ir nuomininko žurnalus skiltyje **Monitoring → Logs**, kuriuose nurodoma tiksli priežastis.

### Issuer neatitikimas

Discovery URL ir domenas, į kurį naršyklė buvo nukreipta, skiriasi — dažniausiai canonical nuomininko domenas prieš custom domeną. Naudokite vienodą domeną visur.

---

## Taip pat žiūrėkite

- [Single Sign-On Overview](overview.md) — konfigūracijos nuoroda, testavimas ir bendras trikčių šalinimas
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
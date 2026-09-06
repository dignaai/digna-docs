# SSO nustatymas su Google Workspace

Google identiteto platforma atitinka OIDC standartą ir naudoja vieną, bendrą discovery URL kiekvienam klientui, todėl vienintelės organizacijai specifinės reikšmės yra kliento ID ir slaptasis raktas.

Šis vadovas apima **Google pusę**: OAuth kliento sukūrimą ir reikšmių surinkimą, kurių reikės digna. digna pusė — `dashboard_config.toml`, testavimas ir trikčių šalinimas — yra ta pati visiems tiekėjams ir aprašyta [Single Sign-On Overview](overview.md).

---

## Prieš pradėdami

| Reikalavimas | Pastabos |
|---|---|
| **Google Cloud projektas** | Bet koks projektas toje pačioje organizacijoje kaip jūsų Workspace domenas |
| **Rolė** | Editor arba Owner projekte |
| **digna peradresavimo URI** | URL, į kurį vartotojas grįžta po prisijungimo, pvz. `https://digna.yourdomain.com/oidc/callback` |

---

## 1 žingsnis: Sukonfigūruokite OAuth sutikimo ekraną

Google neišduos kredencialų, kol nebus sukurtas sutikimo ekranas.

1. Atidarykite [Google Cloud Console](https://console.cloud.google.com) ir pasirinkite savo projektą
2. Eikite į **APIs & Services → OAuth consent screen**
3. Pasirinkite naudotojo tipą:
   - **Internal** — prisijungti gali tik paskyros jūsų Workspace domene. Rekomenduojama.
   - **External** — bet kuri Google paskyra gali pabandyti prisijungti.
4. Užpildykite programos pavadinimą, pagalbos el. paštą vartotojams ir kūrėjo kontaktinį el. paštą
5. Scopes žingsnyje pridėkite `openid`, `.../auth/userinfo.email` ir `.../auth/userinfo.profile`
6. Išsaugokite

!!! warning "Išorinės programos turi būti paskelbtos"

    **External** sutikimo ekranas pradžioje būna *Testing* būsenoje, kur prisijungimą gali užbaigti tik sąraše aiškiai nurodytos testavimo paskyros. Visi kiti mato pranešimą „digna has not completed the Google verification process“. Arba perjunkite programą į **In production** skiltyje **Publishing status**, arba naudokite **Internal** — tai neturi tokių apribojimų ir yra tinkamas pasirinkimas tik Workspace naudojimui.

---

## 2 žingsnis: Sukurkite OAuth klientą

1. Eikite į **APIs & Services → Credentials**
2. Spauskite **Create Credentials → OAuth client ID**
3. Nustatykite **Application type** į **Web application**
4. Suteikite pavadinimą, pavyzdžiui `digna`
5. Skiltyje **Authorized redirect URIs** spauskite **Add URI** ir įveskite:

```
https://digna.yourdomain.com/oidc/callback
```

6. Spauskite **Create**

!!! note "Nereikia nurodyti Authorized JavaScript Origins"

    digna keičia autorizacijos kodą iš backend'o, o ne per naršyklę, todėl lauką **Authorized JavaScript origins** galima palikti tuščią. Svarbus tik peradresavimo URI.

---

## 3 žingsnis: Surinkite kredencialus

Langas, kuris pasirodo po sukūrimo, rodo:

- **Client ID** — baigiasi `.apps.googleusercontent.com` → tampa `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → tampa `DIGNA_OIDC_CLIENT_SECRET`

Abu vėliau galima rasti kredencialo detalėse, skirtingai nei pas daugumą kitų tiekėjų.

---

## 4 žingsnis: Discovery URL

Google naudoja vieną discovery URL visiems klientams — nieko nereikia keisti:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## 5 žingsnis: Sukonfigūruokite digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Prisijungti per Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Reikšmė `key` abiejuose failuose turi sutapti — čia `google`.

---

## 6 žingsnis: Testavimas

Perkraukite backend ir web serverį, tada atidarykite valdymo pultą. Pilną kontrolinį sąrašą rasite [Testing Login](overview.md#testing-login).

---

## Trikčių šalinimas Google Workspace

### Klaida 400: redirect_uri_mismatch

URI, nurodytas `DIGNA_OIDC_REDIRECT_URI`, nėra **Authorized redirect URIs** sąraše arba skiriasi dėl užbaigiančio šliaužiklio ar schemos. Google klaidos puslapyje rodomas gautas URI — palyginkite jį simbolis po simbolio su užregistruotu.

### This App Is Blocked / Has Not Completed Verification

Sutikimo ekranas yra **External** ir vis dar *Testing* būsenoje. Paskelbkite jį arba perjunkite programą į **Internal**.

### Access Blocked: Authorization Error

Paskyra, kuri bando prisijungti, yra už jūsų Workspace domeno ribų, tuo tarpu sutikimo ekranas yra **Internal**. Tai numatytas elgesys — Internal programos priima tik organizacijos paskyras.

### Pokyčiai praeina kelias minutes

Google asinchroniškai skleidžia kredencialų ir sutikimo ekrano pakeitimus. Naujas peradresavimo URI gali pradėti veikti per kelias minutes; jei pakeitimas atrodo nepakeistas, palaukite ir pamėginkite dar kartą prieš gilindamiesi į problemą.

---

## Taip pat žiūrėkite

- [Single Sign-On Overview](overview.md) — konfigūracijos nuoroda, testavimas ir bendras trikčių šalinimas
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
# Iestatīt SSO ar Google Workspace

Google identitātes platforma atbilst OIDC un izmanto vienu, labi zināmu atklāšanas (discovery) URL visiem klientiem, tāpēc vienīgās organizācijai specifiskās vērtības ir klienta ID un slepenā atslēga.

Šis ceļvedis aptver **Google pusi**: OAuth klienta izveidi un vērtību vākšanu, kas nepieciešamas digna. digna puse — `dashboard_config.toml`, testēšana un problēmu novēršana — ir vienāda visiem sniedzējiem un aprakstīta [Single Sign-On pārskats](overview.md).

---

## Pirms sākat

| Prasība | Piezīmes |
|---|---|
| **Google Cloud project** | Jebkurš projekts tajā pašā organizācijā, kurā atrodas jūsu Workspace domēns |
| **Role** | Editor vai Owner projektā |
| **digna redirect URI** | URL, uz kuru lietotāji tiek atgriezti pēc pieslēgšanās, piemēram `https://digna.yourdomain.com/oidc/callback` |

---

## 1. solis: Konfigurēt OAuth piekrišanas ekrānu

Google neizsniegs akreditācijas datus, kamēr piekrišanas ekrāns nebūs izveidots.

1. Atveriet [Google Cloud konsoli](https://console.cloud.google.com) un izvēlieties savu projektu
2. Dodieties uz **APIs & Services → OAuth consent screen**
3. Izvēlieties lietotāja tipu:
   - **Internal** — pieslēgties var tikai konti jūsu Workspace domēnā. Ieteicams.
   - **External** — mēģināt pieslēgties var jebkurš Google konts.
4. Aizpildiet lietotnes nosaukumu, lietotāju atbalsta e-pastu un izstrādātāja kontaktu e-pastu
5. Sadaļā **Scopes** pievienojiet `openid`, `.../auth/userinfo.email` un `.../auth/userinfo.profile`
6. Saglabāt

!!! warning "Ārējām lietotnēm jābūt publicētām"

    **External** piekrišanas ekrāns sāk darbību *Testing* statusā, kur tikai konti, kas tieši pievienoti testlietotāju sarakstam, var pabeigt pieslēgšanos. Pārējiem tiek rādīts "digna has not completed the Google verification process". Vai nu pārslēdziet lietotni uz **In production** zem **Publishing status**, vai izmantojiet **Internal** — tam nav šāda ierobežojuma un tas ir pareizā izvēle, ja izvietojums ir tikai Workspace organizācijai.

---

## 2. solis: Izveidot OAuth klientu

1. Dodieties uz **APIs & Services → Credentials**
2. Noklikšķiniet **Create Credentials → OAuth client ID**
3. Iestatiet **Application type** uz **Web application**
4. Piešķiriet nosaukumu, piem., `digna`
5. Sadaļā **Authorized redirect URIs** noklikšķiniet **Add URI** un ievadiet:

```
https://digna.yourdomain.com/oidc/callback
```

6. Noklikšķiniet **Create**

!!! note "Authorized JavaScript Origins nav nepieciešami"

    digna apmaina autorizācijas kodu no backend puses, nevis pārlūkprogrammas, tāpēc lauku **Authorized JavaScript origins** var atstāt tukšu. Svarīgs ir tikai redirect URI.

---

## 3. solis: Savākt akreditācijas datus

Dialoglodziņš, kas parādās pēc izveides, rāda:

- **Client ID** — beidzas ar `.apps.googleusercontent.com` → kļūs par `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → kļūs par `DIGNA_OIDC_CLIENT_SECRET`

Abas vērtības vēlāk varat atgūt no akreditācijas detaļu lapas, atšķirībā no daudziem citiem pakalpojumu sniedzējiem.

---

## 4. solis: Atklāšanas (Discovery) URL

Google izmanto vienu atklāšanas URL visiem klientiem — nav jāveic nekāda aizvietošana:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## 5. solis: Konfigurēt digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

`key` abos failos jāatbilst — šeit `google`.

---

## 6. solis: Testēšana

Restartējiet backend un web serveri, pēc tam atveriet paneli. Skatīt [Pieslēgšanās testēšana](overview.md#testing-login) pilnai kontrolsarakstam.

---

## Problēmu novēršana Google Workspace

### Kļūda 400: redirect_uri_mismatch

URI, kas norādīts `DIGNA_OIDC_REDIRECT_URI`, nav iekļauts **Authorized redirect URIs** sarakstā, vai atšķiras ar papildslashi vai shēmu. Google kļūdas lapa parāda URI, ko tā saņēma — salīdziniet to rakstzīmi pa rakstzīmei ar reģistrēto URI.

### Šī lietotne ir bloķēta / nav pabeigta verifikācija

Piekrišanas ekrāns ir iestatīts kā **External** un joprojām atrodas *Testing* režīmā. Publicējiet to, vai pārslēdziet lietotni uz **Internal**.

### Piekļuve bloķēta: autorizācijas kļūda

Konts, kas mēģina pieslēgties, atrodas ārpus jūsu Workspace domēna, kamēr piekrišanas ekrāns ir **Internal**. Tas ir paredzēts uzvedība — Internal lietotnes pieņem tikai organizācijas kontus.

### Izmaiņu propagācija aizņem vairākas minūtes

Google asinkroni izplata akreditācijas datus un piekrišanas ekrāna izmaiņas. Ja nesen pievienots redirect URI vai cits iestatījums šķiet nereģistrēts, pagaidiet dažas minūtes un mēģiniet vēlreiz pirms sarežģītākas izmeklēšanas.

---

## Skatīt arī

- [Single Sign-On pārskats](overview.md) — konfigurācijas atsauce, testēšana un vispārīga problēmu novēršana
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
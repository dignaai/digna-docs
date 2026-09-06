# Vienreizējā autentifikācija — pārskats

---

## Satura rādītājs

1. [Ievads un pārskats](#introduction-and-overview)
2. [Pakalpojumu sniedzēju rokasgrāmatas](#provider-guides)
3. [Konfigurācijas soļi](#configuration-steps)
4. [Informācijas paneļa konfigurācija](#dashboard-configuration)
5. [Backend konfigurācija](#backend-configuration)
6. [Pieteikšanās testēšana](#testing-login)
7. [Problēmu novēršana](#troubleshooting)
8. [Atbalstītie pakalpojumu sniedzēji](#supported-providers)

---

## Ievads un pārskats {: #introduction-and-overview }

Šajā rokasgrāmatā ir soli pa solim norādījumi, kā integrēt vienreizējo autentifikāciju (SSO) ar digna platformu, izmantojot **OpenID Connect (OIDC)**.

### Kas ir SSO?

Vienreizējā autentifikācija (SSO) ļauj lietotājiem droši pieteikties digna, izmantojot savas uzņēmuma akreditācijas lielajiem identitātes sniedzējiem. Lietotāji var autentificēties ar korporatīvajiem akreditācijas datiem, nevis pārvaldīt atsevišķas digna paroles.

### Kā tas darbojas

SSO digna tiek īstenots, izmantojot OIDC protokolu. Var konfigurēt vairākus identitātes sniedzējus paralēli, pielāgojot divus galvenos konfigurācijas failus:

- **`dashboard_config.toml`** — kontrolē frontend pieteikšanās saskarni
- **`config.toml`** — konfigurē backend OIDC savienojumus

### Atbalstītie sniedzēji {: #supported-providers-overview }

Šīs rokasgrāmatas piemēri izmanto **Microsoft** un **Google**, taču **jebkurš OIDC saderīgs sniedzējs** var tikt integrēts, sekojot tai pašai struktūrai.

---

## Pakalpojumu sniedzēju rokasgrāmatas {: #provider-guides }

Katrā sniedzējā nepieciešamas tās pašas četras vērtības — klienta ID, klienta noslēpums (client secret), pāradresācijas URI (redirect URI) un atklāšanas (discovery) URL — taču katrs to ievieto savā vietā administrācijas konsolē, un vairākiem ir sniedzējam specifisks solis, kas pārējiem nav. Zemāk esošās rokasgrāmatas aptver šo daļu; šī lapa aptver digna daļu, kas visiem sniedzējiem ir identiska.

| Pakalpojumu sniedzējs | Rokasgrāmata | Vērts zināt |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | Pašpārvaldīts; vienīgais šeit minētais sniedzējs, kurā jūs kontrolējat token servisu |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | Discovery URL ir uz katru tenant — pielāgoti domēni to maina |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | Atļauju ekrānam jābūt publicētam, lai netestējoši lietotāji var pieteikties |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | Pašpārvaldīts; discovery URL ir uz katru realm |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID parādās discovery URL; noslēpumi var beigties |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | Autorizācijas servera izvēle maina discovery URL |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | OIDC lietotnes tips jānokļūst izveides brīdī un to nevar mainīt |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | Environment ID parādās discovery URL |

Jebkurš cits OIDC saderīgs sniedzējs darbojas tāpat — skatīt [Other OIDC Providers](#supported-providers).

---

## Konfigurācijas soļi {: #configuration-steps }

SSO konfigurācija prasa atjauninājumus divos failos. Šajā sadaļā aprakstīts, kā konfigurēt katru no tiem.

### Konfigurācijas failu pārskats

| Fails | Atrašanās vieta | Mērķis |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend pieteikšanās saskarne |
| **config.toml** | `/config.toml` | Backend OIDC savienojumi |

Abi faili jākonfigurē, lai SSO darbotos pareizi.

---

## Informācijas paneļa konfigurācija {: #dashboard-configuration }

### Faila atrašanās vieta

```
dashboard/dashboard_config.toml
```

### 1. solis: Pievienot OIDC sniedzējus

Pievienojiet ierakstus zem masīva `[[login.oidc]]` katram identitātes sniedzējam, ko vēlaties atbalstīt.

**Piemērs ar Microsoft un Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### 2. solis: Konfigurēt pieteikšanās opcijas

Norādiet, vai jāļauj pieteikšanās ar paroli:

```toml
[login]
usePassword = true
```

### Konfigurācijas parametri

#### `[[login.oidc]]` sadaļa

| Parametrs | Tips | Obligāts | Apraksts |
|---|---:|---:|---|
| `key` | string | Jā | Unikāls identifikators OIDC savienojumam (jāatbilst key config.toml) |
| `label` | string | Jā | Teksts, kas tiek rādīts pieteikšanās pogā (piem., "Login with Microsoft") |

#### `[login]` sadaļa

| Parametrs | Tips | Noklusējums | Apraksts |
|---|---:|---:|---|
| `usePassword` | boolean | false | Ļaut pieteikšanos, izmantojot paroli papildus SSO |

### Izpratne par usePassword

**Ja `usePassword = true`:**
- Pieteikšanās ekrānā redzamas SSO pogas (piem., "Login with Microsoft")
- Pieteikšanās ekrānā arī redzami lietotājvārds un paroles lauki
- Lietotāji var autentificēties ar jebkuru no metodēm
- Ļauj hibrīdus iestatījumus, kur daži lietotāji izmanto SSO, bet citi paroles

**Ja `usePassword = false` (vai izlaists):**
- Pieteikšanās ekrānā redzamas tikai SSO pogas
- Nav lietotājvārda/paroles lauku
- Pieejama tikai OIDC autentifikācija

!!! tip "Padoms"

    Pieteikšanās ar paroli ir pieejama tikai lietotājiem, kuri tika izveidoti ar parolēm, izmantojot komandu `digna user add` vai caur informācijas paneli.

### Pilns piemērs

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Backend konfigurācija {: #backend-configuration }

### Faila atrašanās vieta

```
/config.toml
```

(Root digna instalācijas direktorija)

### 1. solis: Pievienot OIDC sniedzēju sadaļas

Katram sniedzējam jābūt atsevišķai `[oidc.<key>]` sadaļai. Key jāatbilst `key`, kas definēts `dashboard_config.toml`.

### Microsoft konfigurācija

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google konfigurācija

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfigurācijas parametri

| Parametrs | Tips | Obligāts | Apraksts | Piemērs |
|---|---:|---:|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Jā | Klienta ID no identitātes sniedzēja | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Jā | Klienta noslēpums no identitātes sniedzēja | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Jā | Callback URL pēc autentifikācijas | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Jā | OIDC konfigurācijas galapunkts | `https://login.microsoftonline.com/...` |

!!! warning "Svarīgi"

    Aizstājiet viettura vērtības (`<client_id>`, `<client_secret>`, `<tenant_id>`) ar reāliem akreditācijas datiem no jūsu identitātes sniedzēja izstrādātāja portāla.

### Redirect URI

Pāradresācijas URI jābūt identiskai jūsu identitātes sniedzēja konfigurācijā:

```
http://localhost:5173/oidc/callback
```

Ja digna ir mitināts citā domēnā, atjauniniet atbilstoši:
- Lokāli: `http://localhost:5173/oidc/callback`
- Ražošanā: `https://digna.yourdomain.com/oidc/callback`

### Pilns piemērs

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Pieteikšanās testēšana {: #testing-login }

Pabeidzot konfigurāciju, pārbaudiet, vai SSO darbojas pareizi.

### Pārbaudes priekšnosacījumu saraksts

Pirms testēšanas pārliecinieties:

- [ ] `dashboard_config.toml` ir atjaunināts ar OIDC sniedzējiem
- [ ] `config.toml` ir atjaunināts ar OIDC akreditācijām
- [ ] Abi faili ir saglabāti
- [ ] Akreditācijas ir pareizas (client ID, client secret)
- [ ] Redirect URI atbilst jūsu izvietošanas URL
- [ ] Identitātes sniedzēja lietotne ir konfigurēta ar redirect URI

### Testēšanas soļi

#### 1. solis: Restartēt servisus

Restartējiet digna backend un tīmekļa serveri, lai piemērotu izmaiņas.

**Ja darbojas kā serviss Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Ja darbojas kā serviss Linux vai macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Ja darbojat manuāli:**
```bash
digna serve --address localhost --port 8082
```

**Restartējiet arī tīmekļa serveri** — IIS vai Tomcat uz Windows, nginx vai Apache uz Linux un macOS.

#### 2. solis: Atvērt informācijas paneli

Atveriet digna informācijas paneli pārlūkā:

```
http://localhost:5173
```

(ja nav — atveriet jūsu konfigurēto paneļa URL)

#### 3. solis: Pārbaudīt pieteikšanās pogas

Pārliecinieties, ka katram konfigurētajam sniedzējam redzama pieteikšanās poga:

- Jāredz poga "Login with Microsoft"
- Jāredz poga "Login with Google"
- (Ja usePassword = true) Jāredz lietotājvārda/paroles lauki

Ja pogas neparādās:
- Pārbaudiet, vai `dashboard_config.toml` ir saglabāts
- Pārbaudiet, vai informācijas paneļa serviss tika restartēts
- Pārbaudiet pārlūkprogrammas konsoli (F12) par kļūdām

#### 4. solis: Testēt SSO pieteikšanos

Noklikšķiniet uz vienas no SSO pogām (piem., "Login with Microsoft"):

1. Jums jābūt pāradresētam uz identitātes sniedzēja pieteikšanās lapu
2. Piesakieties ar saviem uzņēmuma akreditācijas datiem
3. Jums jābūt pāradresētam atpakaļ uz digna
4. Jums jābūt pieteikušamies digna

#### 5. solis: Pārbaudīt lietotāja izveidi

Pēc veiksmīgas SSO pieteikšanās:

- Lietotājs jāizveido automātiski digna
- Lietotājam jābūt pieteiktam
- Lietotāja profilā jāparādās jūsu identitātes sniedzēja datiem
- Jums jāredz digna informācijas panelis

#### 6. solis: Testēt pieteikšanos ar paroli (ja iespējots)

Ja `usePassword = true`:

1. Atslēdzieties no digna
2. Pieteikšanās lapā ievadiet lietotājvārdu un paroli
3. Jums jābūt iespējai pieteikties ar paroli

---

## Problēmu novēršana {: #troubleshooting }

### Pieteikšanās pogas neparādās

**Simptomi:**
- OIDC pieteikšanās pogas nav redzamas pieteikšanās lapā
- Redzami tikai paroles lauki (ja usePassword = true)

**Cēloņi un risinājumi:**
1. Pārbaudiet, ka `dashboard_config.toml` atrodas `dashboard/` direktorijā
2. Pārbaudiet, vai `[[login.oidc]]` sadaļas ir klāt un ar pareizu sintaksi
3. Restartējiet informācijas paneļa servisu
4. Notīriet pārlūkprogrammas kešatmiņu (Ctrl+Shift+Delete vai Cmd+Shift+Delete)
5. Pārbaudiet pārlūkprogrammas konsoli (F12 → Console cilne) par kļūdām

---

### Redirect URI neatbilstības kļūda

**Simptomi:**
- Noklikšķinot uz SSO pogas, tiek rādīta kļūda par "redirect_uri mismatch"
- Kļūda "The redirect URI is not registered"

**Cēloņi un risinājumi:**
1. Pārbaudiet, vai `DIGNA_OIDC_REDIRECT_URI` `config.toml` ir pareizs
2. Pārbaudiet, vai redirect URI ir reģistrēts identitātes sniedzēja iestatījumos
3. Pārliecinieties, ka abi izmanto identiskas URL (ieskaitot protokolu, domēnu, ceļu)
4. Pārbaudiet rakstzīmju kļūdas redirect URI
5. Ja izmantojat HTTPS, pārbaudiet sertifikāta derīgumu

---

### Ne derīgi klienta akreditāciju kļūda

**Simptomi:**
- Kļūda "Invalid client ID or secret"
- Autentifikācija neizdodas ar akreditāciju kļūdu

**Cēloņi un risinājumi:**
1. Pārbaudiet, vai `DIGNA_OIDC_CLIENT_ID` un `DIGNA_OIDC_CLIENT_SECRET` ir pareizi
2. Pārliecinieties, ka nav lieku atstarpju vai speciālu rakstzīmju
3. Pārbaudiet, vai akreditācijas nav beigušās vai atsauktas
4. Restartējiet backend servisu pēc konfigurācijas atjaunināšanas
5. Pārbaudiet identitātes sniedzēja konsoli, lai apstiprinātu akreditāciju statusu

---

### Pieteikšanās iestrēgst vai notiek taimauts

**Simptomi:**
- Noklikšķinot SSO pogu, nekas nenotiek
- Pēc dažām sekundēm tiek taimauts
- Pārlūkā parādās "Failed to connect" vai līdzīga ziņa

**Cēloņi un risinājumi:**
1. Pārbaudiet, vai digna backend darbojas: `digna repo check`
2. Pārbaudiet tīkla savienojumu uz identitātes sniedzēju
3. Pārliecinieties, ka `DIGNA_OIDC_CONFIGURATION_URL` ir pieejams
4. Pārbaudiet ugunsmūra noteikumus, lai atļautu izejošos HTTPS savienojumus
5. Pārliecinieties, ka backend un informācijas panelis var sasniegt viens otru

---

### Lietotāji netiek automātiski izveidoti

**Simptomi:**
- SSO pieteikšanās izdodas, bet lietotājs netiek izveidots digna
- Pēc SSO pieteikšanās rodas atļauju kļūda

**Cēloņi un risinājumi:**
1. Pārbaudiet OIDC konfigurāciju
2. Pārbaudiet lietotāju atļauju iestatījumus
3. Pārskatiet digna žurnālus pēc kļūdu ziņojumiem
4. Restartējiet backend servisu
5. Ja problēma saglabājas, sazinieties ar support@digna.ai

---

## Atbalstītie pakalpojumu sniedzēji {: #supported-providers }

### Testēti un atbalstīti

Zemāk uzskaitītie OIDC sniedzēji ir testēti un zināmi kā strādājoši:

| Pakalpojumu sniedzējs | Konfigurācijas URL | Uzstādīšanas rokasgrāmata |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### Citi OIDC sniedzēji

Jebkurš pakalpojumu sniedzējs, kas atbalsta OpenID Connect, var tikt integrēts. Nepieciešamā informācija:

- Client ID
- Client secret
- OpenID konfigurācijas URL (parasti pie `/.well-known/openid-configuration`)
- Atbalstītie scopes (parasti `openid profile email`)

Ja nepieciešama palīdzība ar konkrēta sniedzēja integrāciju, sazinieties ar support@digna.ai.

---

## Labākā prakse

**DARĪT:**
- Ražošanā izmantot HTTPS (nevis HTTP)
- Glabāt klienta noslēpumus droši (izmantojiet vides mainīgos, ja iespējams)
- Regulāri rotēt noslēpumus
- Vispirms testēt ne- ražošanas vidē
- Dokumentēt, kuri sniedzēji ir konfigurēti
- Monitorēt pieteikšanās žurnālus pēc aizdomīgas darbības
- Uzturēt identitātes sniedzēja konfigurāciju sinhronā ar digna konfigurāciju

**NEDARĪT:**
- Glabāt klienta noslēpumus versiju kontrolē
- Ražošanā izmantot HTTP redirect URI
- Konfigurēt vairākus sniedzējus ar to pašu key
- Atstāt noklusējuma/testa akreditācijas ražošanā
- Pakļaut konfigurācijas failus ar noslēpumiem
- Sajaukt izstrādes un ražošanas akreditācijas

---

## Atbalsts

Nepieciešama palīdzība ar SSO konfigurāciju?

- **E-pasts:** support@digna.ai
- **Dokumentācija:** https://docs.digna.ai
- **Tīmekļa vietne:** https://www.digna.ai

---

**Pēdējoreiz atjaunināts:** August 30, 2026  
**Izlaidums:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
---
title: Ghid de integrare Single Sign-On (SSO) | documentația digna
description: Ghid pas cu pas pentru configurarea Single Sign-On (SSO) pentru digna folosind OpenID Connect (OIDC). Acoperă configurarea în dashboard și backend, testarea, depanarea și furnizorii de identitate compatibili, inclusiv Microsoft Entra ID, Google Workspace și Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - integrare oidc
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integrare
  - autentificare enterprise
lang: ro
robots: index, follow
og_title: digna Ghid de integrare Single Sign-On (SSO)
og_description: Configurează Single Sign-On pentru digna folosind OpenID Connect. Configurare pas cu pas pentru Microsoft Entra ID, Google Workspace, Okta și alți furnizori OIDC.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Ghid de integrare Single Sign-On

---

## Cuprins

1. [Introducere și prezentare](#introduction-and-overview)
2. [Pași de configurare](#configuration-steps)
3. [Configurare Dashboard](#dashboard-configuration)
4. [Configurare Backend](#backend-configuration)
5. [Testarea autentificării](#testing-login)
6. [Depanare](#troubleshooting)
7. [Furnizori suportați](#supported-providers)

---

## Introducere și prezentare {: #introduction-and-overview }

Acest ghid oferă instrucțiuni pas cu pas pentru integrarea Single Sign-On (SSO) cu platforma digna folosind **OpenID Connect (OIDC)**.

### Ce este SSO?

Single Sign-On permite utilizatorilor să se autentifice în digna în mod securizat folosind acreditările lor enterprise prin furnizori de identitate externi. Utilizatorii se pot autentifica cu datele corporative în loc să gestioneze parole separate pentru digna.

### Cum funcționează

SSO în digna este implementat folosind protocolul OIDC. Pot fi configurate mai mulți furnizori de identitate în paralel prin ajustarea a două fișiere cheie de configurare:

- **`dashboard_config.toml`** — Controlează interfața de autentificare a frontend-ului
- **`config.toml`** — Configurează conexiunile OIDC pentru backend

### Furnizori suportați {: #supported-providers-overview }

Exemplele din acest ghid folosesc **Microsoft** și **Google**, dar **orice furnizor compatibil OIDC** poate fi integrat urmând aceeași structură.

Furnizori OIDC comuni includ:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Alți furnizori de identitate compatibili OIDC

---

## Pași de configurare {: #configuration-steps }

Configurarea SSO necesită actualizări în două fișiere. Această secțiune explică cum se configurează fiecare.

### Prezentare a fișierelor de configurare

| Fișier | Locație | Scop |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Interfața de autentificare a frontend-ului |
| **config.toml** | `/config.toml` | Conexiunile OIDC pentru backend |

Ambele fișiere trebuie configurate pentru ca SSO să funcționeze corect.

---

## Configurare Dashboard {: #dashboard-configuration }

### Locația fișierului

```
dashboard/dashboard_config.toml
```

### Pasul 1: Adăugați furnizori OIDC

Adăugați intrări sub matricea `[[login.oidc]]` pentru fiecare furnizor de identitate pe care doriți să îl suportați.

**Exemplu cu Microsoft și Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Pasul 2: Configurați opțiunile de autentificare

Specificați dacă autentificarea pe bază de parolă ar trebui permisă:

```toml
[login]
usePassword = true
```

### Parametrii de configurare

#### Secțiunea `[[login.oidc]]`

| Parametru | Tip | Obligatoriu | Descriere |
|---|---|---|---|
| `key` | string | Da | Identificator unic pentru conexiunea OIDC (trebuie să corespundă cu key din config.toml) |
| `label` | string | Da | Textul afișat pe butonul de autentificare (de ex., "Login with Microsoft") |

#### Secțiunea `[login]`

| Parametru | Tip | Implicit | Descriere |
|---|---|---|---|
| `usePassword` | boolean | false | Permite autentificarea pe bază de parolă în plus față de SSO |

### Înțelegerea lui usePassword

**Dacă `usePassword = true`:**
- Ecranul de autentificare afișează butoanele SSO (de ex., "Login with Microsoft")
- Ecranul afișează și câmpuri pentru nume de utilizator și parolă
- Utilizatorii se pot autentifica prin oricare dintre metode
- Permite configurații hibride unde unii utilizatori folosesc SSO și alții parole

**Dacă `usePassword = false` (sau omis):**
- Ecranul de autentificare afișează doar butoanele SSO
- Nu există câmpuri pentru nume de utilizator/parolă
- Este disponibilă doar autentificarea OIDC

> **💡 Sfat**
>
> Autentificarea pe bază de parolă este disponibilă doar pentru utilizatorii creați cu parole folosind comanda `digna user add` sau prin dashboard.

### Exemplu complet

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

## Configurare Backend {: #backend-configuration }

### Locația fișierului

```
/config.toml
```

(Directorul rădăcină al instalării digna)

### Pasul 1: Adăugați secțiuni pentru furnizorii OIDC

Fiecare furnizor trebuie să aibă o secțiune dedicată `[oidc.<key>]`. cheia trebuie să corespundă cu `key` definit în `dashboard_config.toml`.

### Configurare Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Configurare Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Parametrii de configurare

| Parametru | Tip | Obligatoriu | Descriere | Exemplu |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Da | Client ID de la furnizorul de identitate | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Da | Secretul clientului de la furnizorul de identitate | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Da | URL-ul de callback după autentificare | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Da | Endpoint-ul de configurare OIDC | `https://login.microsoftonline.com/...` |

> **⚠️ Important**
>
> Înlocuiți valorile placeholder (`<client_id>`, `<client_secret>`, `<tenant_id>`) cu acreditările reale din portalul dezvoltatorului furnizorului vostru de identitate.

### Redirect URI

Redirect URI trebuie să fie identic în configurația furnizorului de identitate:

```
http://localhost:5173/oidc/callback
```

Dacă digna este găzduit pe un domeniu diferit, actualizați corespunzător:
- Local: `http://localhost:5173/oidc/callback`
- Producție: `https://digna.yourdomain.com/oidc/callback`

### Exemplu complet

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

## Testarea autentificării {: #testing-login }

După finalizarea configurării, verificați că SSO funcționează corect.

### Lista de verificare înainte de testare

Înainte de testare asigurați-vă că:

- [ ] `dashboard_config.toml` a fost actualizat cu furnizorii OIDC
- [ ] `config.toml` a fost actualizat cu acreditările OIDC
- [ ] Ambele fișiere au fost salvate
- [ ] Acreditările sunt corecte (client ID, client secret)
- [ ] Redirect URI corespunde URL-ului de deploy
- [ ] Aplicația din furnizorul de identitate este configurată cu redirect URI

### Pașii de testare

#### Pasul 1: Reporniți serviciile

Reporniți backend-ul digna și serverul web pentru a aplica modificările.

**Dacă rulează ca serviciu Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Dacă rulează manual:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Dacă folosiți IIS sau Tomcat:**
Reporniți serviciul web.

#### Pasul 2: Deschideți dashboard-ul

Deschideți dashboard-ul digna în browser:

```
http://localhost:5173
```

(sau URL-ul dashboard-ului configurat)

#### Pasul 3: Verificați butoanele de autentificare

Verificați dacă apar butoanele de autentificare pentru fiecare furnizor configurat:

- ✅ Ar trebui să vedeți butonul "Login with Microsoft"
- ✅ Ar trebui să vedeți butonul "Login with Google"
- ✅ (Dacă usePassword = true) Ar trebui să vedeți câmpuri pentru nume de utilizator/parolă

Dacă butoanele nu apar:
- Verificați că `dashboard_config.toml` a fost salvat
- Verificați că serviciul dashboard a fost repornit
- Verificați consola browserului (F12) pentru erori

#### Pasul 4: Testați autentificarea SSO

Faceți clic pe unul dintre butoanele SSO (de ex., "Login with Microsoft"):

1. Ar trebui să fiți redirecționat către pagina de autentificare a furnizorului de identitate
2. Autentificați-vă cu acreditările enterprise
3. Ar trebui să fiți redirecționat înapoi la digna
4. Ar trebui să fiți autentificat în digna

#### Pasul 5: Verificați crearea utilizatorului

După autentificarea SSO cu succes:

- ✅ Utilizatorul ar trebui creat automat în digna
- ✅ Utilizatorul ar trebui autentificat
- ✅ Profilul utilizatorului ar trebui să afișeze acreditările furnizorului de identitate
- ✅ Ar trebui să vedeți dashboard-ul digna

#### Pasul 6: Testați autentificarea prin parolă (dacă este activată)

Dacă `usePassword = true`:

1. Deconectați-vă din digna
2. Pe pagina de autentificare, introduceți un nume de utilizator și parolă
3. Ar trebui să vă puteți autentifica cu acreditările pe bază de parolă

---

## Depanare {: #troubleshooting }

### Butoanele de autentificare nu apar

**Simptome:**
- Butoanele OIDC nu sunt vizibile pe pagina de autentificare
- Se văd doar câmpurile de parolă (dacă usePassword = true)

**Cauze și soluții:**
1. Verificați că `dashboard_config.toml` se află în directorul `dashboard/`
2. Verificați că secțiunile `[[login.oidc]]` sunt prezente și sintaxa e corectă
3. Reporniți serviciul dashboard
4. Goliți memoria cache a browserului (Ctrl+Shift+Delete sau Cmd+Shift+Delete)
5. Verificați consola browserului (F12 → fila Console) pentru erori

---

### Eroare de tip Redirect URI Mismatch

**Simptome:**
- După clic pe butonul SSO, apare eroare despre "redirect_uri mismatch"
- Eroare "The redirect URI is not registered"

**Cauze și soluții:**
1. Verificați `DIGNA_OIDC_REDIRECT_URI` din `config.toml` că este corect
2. Verificați că redirect URI este înregistrat în setările furnizorului de identitate
3. Asigurați-vă că ambele folosesc același URL (inclusiv protocolul, domeniul, calea)
4. Verificați eventualele greșeli de tipar în redirect URI
5. Dacă folosiți HTTPS, asigurați-vă că certificatul este valid

---

### Eroare de tip Credențiale Client Invalide

**Simptome:**
- Eroare "Invalid client ID or secret"
- Autentificarea eșuează cu eroare de credențiale

**Cauze și soluții:**
1. Verificați că `DIGNA_OIDC_CLIENT_ID` și `DIGNA_OIDC_CLIENT_SECRET` sunt corecte
2. Asigurați-vă că nu există spații suplimentare sau caractere speciale
3. Verificați dacă acreditările nu au expirat sau nu au fost revocate
4. Reporniți serviciul backend după actualizarea config
5. Verificați în consola furnizorului de identitate dacă acreditările sunt active

---

### Autentificarea se blochează sau expiră

**Simptome:**
- Clic pe butonul SSO nu produce nimic
- Timp de așteptare urmat de timeout
- Browserul afișează "Failed to connect" sau similar

**Cauze și soluții:**
1. Verificați că backend-ul digna rulează: `digna repo check`
2. Verificați conectivitatea de rețea către furnizorul de identitate
3. Verificați că `DIGNA_OIDC_CONFIGURATION_URL` este accesibil
4. Verificați regulile de firewall pentru a permite conexiuni HTTPS outbound
5. Verificați că backend-ul și dashboard-ul pot comunica între ele

---

### Utilizatorii nu sunt creați automat

**Simptome:**
- Autentificarea SSO reușește dar utilizatorul nu este creat în digna
- Primește eroare de permisiuni după autentificare SSO

**Cauze și soluții:**
1. Verificați că configurația OIDC este corectă
2. Verificați setările de permisiuni pentru utilizatori
3. Consultați log-urile digna pentru mesaje de eroare
4. Reporniți serviciul backend
5. Contactați support@digna.ai dacă problema persistă

---

## Furnizori suportați {: #supported-providers }

### Testați & Suportați

Următorii furnizori OIDC au fost testați și se știe că funcționează:

| Furnizor | URL de configurare | Ghid de configurare |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Alți furnizori OIDC

Orice furnizor care suportă OpenID Connect poate fi integrat. Informațiile necesare:

- Client ID
- Client secret
- URL-ul de configurare OpenID (de obicei la `/.well-known/openid-configuration`)
- Scopuri suportate (de regulă `openid profile email`)

Contactați support@digna.ai dacă aveți nevoie de ajutor pentru integrarea unui furnizor specific.

---

## Practici recomandate

✅ **FACEȚI:**
- Folosiți HTTPS în producție (nu HTTP)
- Stocați secretele clientului în siguranță (folosiți variabile de mediu dacă este posibil)
- Rotați secretele periodic
- Testați întâi într-un mediu non-producție
- Documentați ce furnizori sunt configurați
- Monitorizați log-urile de autentificare pentru activitate neobișnuită
- Mențineți configurația furnizorului de identitate sincronizată cu configurația digna

❌ **NU FACEȚI:**
- Nu stocați secretele clientului în controlul versiunii
- Nu folosiți redirect URI-uri HTTP în producție
- Nu configurați mai mulți furnizori cu aceeași cheie
- Nu lăsați acreditări implicite/test în producție
- Nu expuneți fișiere de configurare care conțin secrete
- Nu amestecați acreditările de dezvoltare cu cele de producție

---

## Suport

Aveți nevoie de ajutor pentru configurarea SSO?

- 📧 **Email:** support@digna.ai
- 📚 **Documentație:** https://docs.digna.ai
- 🌐 **Website:** https://www.digna.ai

---

**Ultima actualizare:** 30 august 2026  
**Versiune:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
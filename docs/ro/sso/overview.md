---
title: Prezentarea Single Sign-On (SSO) | Documentația digna
description: Cum funcționează Single Sign-On în digna folosind OpenID Connect (OIDC). Acoperă configurarea dashboard-ului și a backend-ului, testarea, depanarea și linkurile către ghidurile de configurare pentru Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne și AD FS.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - integrare oidc
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - integrare okta
  - autentificare enterprise
lang: ro
robots: index, follow
og_title: Ghid de integrare digna Single Sign-On (SSO)
og_description: Configurați Single Sign-On pentru digna folosind OpenID Connect. Configurare pas cu pas pentru Microsoft Entra ID, Google Workspace, Okta și alți furnizori de identitate compatibili OIDC.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Prezentarea Single Sign-On

---

## Cuprins

1. [Introducere și prezentare generală](#introduction-and-overview)
2. [Ghiduri pe furnizori](#provider-guides)
3. [Pașii de configurare](#configuration-steps)
4. [Configurarea dashboard-ului](#dashboard-configuration)
5. [Configurarea backend-ului](#backend-configuration)
6. [Testarea autentificării](#testing-login)
7. [Depanare](#troubleshooting)
8. [Furnizori acceptați](#supported-providers)

---

## Introducere și prezentare generală {: #introduction-and-overview }

Acest ghid oferă instrucțiuni pas cu pas pentru integrarea Single Sign-On (SSO) cu platforma digna folosind **OpenID Connect (OIDC)**.

### Ce este SSO?

Single Sign-On permite utilizatorilor să se autentifice în siguranță în digna folosind acreditările enterprise prin furnizori de identitate externi. Utilizatorii se pot autentifica cu acreditările corporative în loc să gestioneze parole digna separate.

### Cum funcționează

SSO în digna este implementat folosind protocolul OIDC. Mai mulți furnizori de identitate pot fi configurați în paralel prin ajustarea a două fișiere de configurare principale:

- **`dashboard_config.toml`** — Controlează interfața de autentificare din frontend
- **`config.toml`** — Configurează conexiunile OIDC din backend

### Furnizori acceptați {: #supported-providers-overview }

Exemplele din acest ghid folosesc **Microsoft** și **Google**, dar **orice furnizor compatibil OIDC** poate fi integrat urmând aceeași structură.

---

## Ghiduri pe furnizori {: #provider-guides }

Fiecare furnizor are nevoie de aceleași patru valori — un client ID, un client secret, un redirect URI și un URL de discovery — dar fiecare le plasează în alt loc în consola sa de administrare, iar unii au un pas specific pe care ceilalți nu îl au. Ghidurile de mai jos acoperă această jumătate a muncii; această pagină acoperă jumătatea digna, care este identică pentru toți.

| Furnizor | Ghid | Bine de știut |
|---|---|---|
| **AD FS** | [Configurați SSO cu AD FS](adfs_sso_guide.md) | Auto-găzduit; singurul furnizor de aici la care controlați serviciul de token-uri |
| **Auth0** | [Configurați SSO cu Auth0](auth0_sso_guide.md) | URL-ul de discovery este specific fiecărui tenant, iar domeniile personalizate îl modifică |
| **Google Workspace** | [Configurați SSO cu Google Workspace](google_workspace_sso_guide.md) | Ecranul de consimțământ trebuie publicat înainte ca utilizatorii care nu sunt de test să se poată autentifica |
| **Keycloak** | [Configurați SSO cu Keycloak](keycloak_sso_guide.md) | Auto-găzduit; URL-ul de discovery este specific fiecărui realm |
| **Microsoft Entra ID** | [Configurați SSO cu Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | ID-ul tenantului apare în URL-ul de discovery; secretele expiră |
| **Okta** | [Configurați SSO cu Okta](okta_sso_guide.md) | Alegerea serverului de autorizare modifică URL-ul de discovery |
| **OneLogin** | [Configurați SSO cu OneLogin](onelogin_sso_guide.md) | Tipul aplicației OIDC trebuie ales la creare și nu poate fi schimbat |
| **PingOne** | [Configurați SSO cu PingOne](pingone_sso_guide.md) | ID-ul mediului (environment) apare în URL-ul de discovery |

Orice alt furnizor compatibil OIDC funcționează în același mod — consultați [Alți furnizori OIDC](#supported-providers).

---

## Pașii de configurare {: #configuration-steps }

Configurarea SSO necesită actualizarea a două fișiere. Această secțiune explică cum se configurează fiecare.

### Prezentarea fișierelor de configurare

| Fișier | Locație | Scop |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Interfața de autentificare din frontend |
| **config.toml** | `/config.toml` | Conexiunile OIDC din backend |

Ambele fișiere trebuie configurate pentru ca SSO să funcționeze corect.

---

## Configurarea dashboard-ului {: #dashboard-configuration }

### Locația fișierului

```
dashboard/dashboard_config.toml
```

### Pasul 1: Adăugați furnizorii OIDC

Adăugați intrări în array-ul `[[login.oidc]]` pentru fiecare furnizor de identitate pe care doriți să îl acceptați.

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

Specificați dacă autentificarea cu parolă trebuie permisă:

```toml
[login]
usePassword = true
```

### Parametrii de configurare

#### Secțiunea `[[login.oidc]]`

| Parametru | Tip | Obligatoriu | Descriere |
|---|---|---|---|
| `key` | string | Da | Identificator unic pentru conexiunea OIDC (trebuie să corespundă cheii din config.toml) |
| `label` | string | Da | Textul afișat pe butonul de autentificare (de ex. „Login with Microsoft”) |

#### Secțiunea `[login]`

| Parametru | Tip | Implicit | Descriere |
|---|---|---|---|
| `usePassword` | boolean | false | Permite autentificarea cu parolă pe lângă SSO |

### Înțelegerea usePassword

**Dacă `usePassword = true`:**
- Ecranul de autentificare afișează butoanele SSO (de ex. „Login with Microsoft”)
- Ecranul de autentificare afișează și câmpurile pentru nume de utilizator și parolă
- Utilizatorii se pot autentifica prin oricare dintre metode
- Permite configurări hibride, în care unii utilizatori folosesc SSO, iar alții parole

**Dacă `usePassword = false` (sau omis):**
- Ecranul de autentificare afișează doar butoanele SSO
- Nu există câmpuri pentru nume de utilizator/parolă
- Este disponibilă doar autentificarea OIDC

!!! tip "Sfat"

    Autentificarea cu parolă este disponibilă doar pentru utilizatorii care au fost creați cu parole folosind comanda `digna user add` sau prin dashboard.

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

## Configurarea backend-ului {: #backend-configuration }

### Locația fișierului

```
/config.toml
```

(Directorul rădăcină al instalării digna)

### Pasul 1: Adăugați secțiunile pentru furnizorii OIDC

Fiecare furnizor trebuie să aibă o secțiune dedicată `[oidc_clients.<key>]`. Cheia trebuie să corespundă valorii `key` definite în `dashboard_config.toml`.

### Configurația Microsoft

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Configurația Google

```toml
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Parametrii de configurare

| Parametru | Tip | Obligatoriu | Descriere | Exemplu |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Da | Client ID de la furnizorul de identitate | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Da | Client secret de la furnizorul de identitate | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Da | URL-ul de callback după autentificare | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Da | Endpoint-ul de configurare OIDC | `https://login.microsoftonline.com/...` |

!!! warning "Important"

    Înlocuiți valorile substituent (`<client_id>`, `<client_secret>`, `<tenant_id>`) cu acreditările reale din portalul pentru dezvoltatori al furnizorului de identitate.

### Redirect URI

Redirect URI-ul trebuie să fie același în configurația furnizorului de identitate:

```
http://localhost:5173/oidc/callback
```

Dacă digna este găzduită pe un alt domeniu, actualizați-l corespunzător:
- Local: `http://localhost:5173/oidc/callback`
- Producție: `https://digna.yourdomain.com/oidc/callback`

### Exemplu complet

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Testarea autentificării {: #testing-login }

După finalizarea configurării, verificați că SSO funcționează corect.

### Listă de verificare înainte de testare

Înainte de testare, asigurați-vă că:

- [ ] `dashboard_config.toml` a fost actualizat cu furnizorii OIDC
- [ ] `config.toml` a fost actualizat cu acreditările OIDC
- [ ] Ambele fișiere au fost salvate
- [ ] Acreditările sunt corecte (client ID, client secret)
- [ ] Redirect URI-ul corespunde URL-ului implementării dvs.
- [ ] Aplicația din furnizorul de identitate este configurată cu redirect URI-ul

### Pașii de testare

#### Pasul 1: Reporniți serviciile

Reporniți backend-ul digna și serverul web pentru a aplica modificările.

**Dacă rulează ca serviciu pe Windows:**
```bash
cd C:\path\to\digna
digna windows stop
digna windows start
```

**Dacă rulează ca serviciu pe Linux sau macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Dacă rulează manual:**
```bash
digna serve --address localhost --port 8082
```

**Reporniți și serverul web** — IIS sau Tomcat pe Windows, nginx sau Apache pe Linux și macOS.

#### Pasul 2: Deschideți dashboard-ul

Deschideți dashboard-ul digna în browser:

```
http://localhost:5173
```

(sau URL-ul dashboard-ului configurat de dvs.)

#### Pasul 3: Verificați butoanele de autentificare

Verificați că apar butoanele de autentificare pentru fiecare furnizor configurat:

- Ar trebui să vedeți butonul „Login with Microsoft”
- Ar trebui să vedeți butonul „Login with Google”
- (Dacă usePassword = true) Ar trebui să vedeți câmpurile pentru nume de utilizator/parolă

Dacă butoanele nu apar:
- Verificați că `dashboard_config.toml` a fost salvat
- Verificați că serviciul dashboard a fost repornit
- Verificați consola browserului (F12) pentru erori

#### Pasul 4: Testați autentificarea SSO

Faceți clic pe unul dintre butoanele SSO (de ex. „Login with Microsoft”):

1. Ar trebui să fiți redirecționat către pagina de autentificare a furnizorului de identitate
2. Autentificați-vă cu acreditările enterprise
3. Ar trebui să fiți redirecționat înapoi către digna
4. Ar trebui să fiți autentificat în digna

#### Pasul 5: Verificați crearea utilizatorului

După o autentificare SSO reușită:

- Utilizatorul ar trebui creat automat în digna
- Utilizatorul ar trebui să fie autentificat
- Profilul utilizatorului ar trebui să afișeze datele de la furnizorul de identitate
- Ar trebui să vedeți dashboard-ul digna

#### Pasul 6: Testați autentificarea cu parolă (dacă este activată)

Dacă `usePassword = true`:

1. Deconectați-vă din digna
2. Pe pagina de autentificare, introduceți un nume de utilizator și o parolă
3. Ar trebui să vă puteți autentifica cu acreditările cu parolă

---

## Depanare {: #troubleshooting }

### Butoanele de autentificare nu apar

**Simptome:**
- Butoanele de autentificare OIDC nu sunt vizibile pe pagina de autentificare
- Se văd doar câmpurile pentru parolă (dacă usePassword = true)

**Cauze și soluții:**
1. Verificați că `dashboard_config.toml` se află în directorul `dashboard/`
2. Verificați că secțiunile `[[login.oidc]]` sunt prezente, cu sintaxa corectă
3. Reporniți serviciul dashboard
4. Goliți memoria cache a browserului (Ctrl+Shift+Delete sau Cmd+Shift+Delete)
5. Verificați consola browserului (F12 → fila Console) pentru erori

---

### Eroare de nepotrivire a redirect URI-ului

**Simptome:**
- După clic pe butonul SSO, apare o eroare despre „redirect_uri mismatch”
- Eroare „The redirect URI is not registered”

**Cauze și soluții:**
1. Verificați că `DIGNA_OIDC_REDIRECT_URI` din `config.toml` este corect
2. Verificați că redirect URI-ul este înregistrat în setările furnizorului de identitate
3. Asigurați-vă că ambele folosesc URL-uri identice (inclusiv protocolul, domeniul și calea)
4. Verificați dacă există greșeli de scriere în redirect URI
5. Dacă folosiți HTTPS, asigurați-vă că certificatul este valid

---

### Eroare de acreditări client invalide

**Simptome:**
- Eroare „Invalid client ID or secret”
- Autentificarea eșuează cu o eroare de acreditări

**Cauze și soluții:**
1. Verificați că `DIGNA_OIDC_CLIENT_ID` și `DIGNA_OIDC_CLIENT_SECRET` sunt corecte
2. Asigurați-vă că nu există spații sau caractere speciale în plus
3. Verificați că acreditările nu au expirat și nu au fost revocate
4. Reporniți serviciul backend după actualizarea configurației
5. Verificați în consola furnizorului de identitate că acreditările sunt active

---

### Autentificarea se blochează sau expiră

**Simptome:**
- Clic pe butonul SSO nu are niciun efect
- Timeout după câteva secunde
- Browserul afișează „Failed to connect” sau un mesaj similar

**Cauze și soluții:**
1. Verificați că backend-ul digna rulează: `digna repo check`
2. Verificați conectivitatea la rețea către furnizorul de identitate
3. Verificați că `DIGNA_OIDC_CONFIGURATION_URL` este accesibil
4. Verificați că regulile firewall permit conexiunile HTTPS de ieșire
5. Verificați că backend-ul și dashboard-ul pot comunica între ele

---

### Utilizatorii nu sunt creați automat

**Simptome:**
- Autentificarea SSO reușește, dar utilizatorul nu este creat în digna
- Apare o eroare de permisiune după autentificarea SSO

**Cauze și soluții:**
1. Verificați că configurația OIDC este corectă
2. Verificați că permisiunile utilizatorilor sunt configurate
3. Examinați logurile digna pentru mesaje de eroare
4. Reporniți serviciul backend
5. Contactați support@digna.ai dacă problema persistă

---

## Furnizori acceptați {: #supported-providers }

### Testați și acceptați

Următorii furnizori OIDC au fost testați și se știe că funcționează:

| Furnizor | URL de configurare | Ghid de configurare |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Configurați SSO cu AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Configurați SSO cu Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Configurați SSO cu Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Configurați SSO cu Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Configurați SSO cu Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Configurați SSO cu Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Configurați SSO cu OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Configurați SSO cu PingOne](pingone_sso_guide.md) |

### Alți furnizori OIDC

Orice furnizor care acceptă OpenID Connect poate fi integrat. Informații necesare:

- Client ID
- Client secret
- URL-ul de configurare OpenID (de obicei la `/.well-known/openid-configuration`)
- Scope-urile acceptate (de obicei `openid profile email`)

Contactați support@digna.ai dacă aveți nevoie de ajutor pentru integrarea unui anumit furnizor.

---

## Bune practici

**RECOMANDAT:**
- Folosiți HTTPS în producție (nu HTTP)
- Stocați client secret-urile în siguranță (folosiți variabile de mediu, dacă este posibil)
- Rotiți secretele periodic
- Testați mai întâi într-un mediu care nu este de producție
- Documentați ce furnizori sunt configurați
- Monitorizați logurile de autentificare pentru activități neobișnuite
- Păstrați configurația furnizorului de identitate sincronizată cu configurația digna

**DE EVITAT:**
- Stocarea client secret-urilor în sistemul de control al versiunilor
- Utilizarea redirect URI-urilor HTTP în producție
- Configurarea mai multor furnizori cu aceeași cheie
- Lăsarea acreditărilor implicite/de test în producție
- Expunerea fișierelor de configurare care conțin secrete
- Amestecarea acreditărilor de dezvoltare cu cele de producție

---

## Suport

Aveți nevoie de ajutor cu configurarea SSO?

- **E-mail:** support@digna.ai
- **Documentație:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Ultima actualizare:** 30 august 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**

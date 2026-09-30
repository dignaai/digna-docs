---
title: Google Workspace SSO – Integrare Single Sign-On | Documentația digna
description: Configurați Single Sign-On pentru digna cu Google Workspace folosind OpenID Connect — ecranul de consimțământ OAuth, OAuth client ID, URI-urile de redirect autorizate și configurația digna corespunzătoare.
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, ecran de consimțământ oauth, openid connect, autentificare enterprise
---

# Configurați SSO cu Google Workspace

Platforma de identitate Google este compatibilă OIDC și folosește un singur URL de discovery (descoperire), bine cunoscut, pentru toți clienții, astfel încât singurele valori specifice organizației sunt client ID-ul și secretul.

Acest ghid acoperă **partea Google**: crearea clientului OAuth și colectarea valorilor de care digna are nevoie. Partea digna — `dashboard_config.toml`, testarea și depanarea — este aceeași pentru orice furnizor și este descrisă în [Prezentarea Single Sign-On](overview.md).

---

## Înainte de a începe

| Cerință | Note |
|---|---|
| **Google Cloud project** | Orice proiect din aceeași organizație cu domeniul dvs. Workspace |
| **Rol** | Editor sau Owner pe proiect |
| **digna redirect URI** | URL-ul la care utilizatorii revin după autentificare, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Pasul 1: Configurați ecranul de consimțământ OAuth

Google nu emite acreditări până când nu există ecranul de consimțământ.

1. Deschideți [Google Cloud Console](https://console.cloud.google.com) și selectați proiectul
2. Accesați **APIs & Services → OAuth consent screen**
3. Alegeți tipul de utilizator:
   - **Internal** — doar conturile din domeniul dvs. Workspace se pot autentifica. Recomandat.
   - **External** — orice cont Google poate încerca să se autentifice.
4. Completați numele aplicației, adresa de e-mail pentru asistența utilizatorilor și adresa de e-mail de contact a dezvoltatorului
5. La pasul **Scopes**, adăugați `openid`, `.../auth/userinfo.email` și `.../auth/userinfo.profile`
6. Salvați

!!! warning "Aplicațiile External trebuie publicate"

    Un ecran de consimțământ **External** pornește în starea *Testing*, în care doar conturile adăugate explicit în lista de utilizatori de test pot finaliza o autentificare. Toți ceilalți văd „digna has not completed the Google verification process”. Fie treceți aplicația în starea **In production** sub **Publishing status**, fie folosiți **Internal** — care nu are o astfel de restricție și este alegerea potrivită pentru o implementare doar pentru Workspace.

---

## Pasul 2: Creați clientul OAuth

1. Accesați **APIs & Services → Credentials**
2. Faceți clic pe **Create Credentials → OAuth client ID**
3. Setați **Application type** la **Web application**
4. Dați-i un nume, ex. `digna`
5. Sub **Authorized redirect URIs**, faceți clic pe **Add URI** și introduceți:

```
https://digna.yourdomain.com/oidc/callback
```

6. Faceți clic pe **Create**

!!! note "Authorized JavaScript Origins nu sunt necesare"

    digna face schimbul codului de autorizare din backend, nu din browser, astfel încât câmpul **Authorized JavaScript origins** poate fi lăsat gol. Contează doar redirect URI-ul.

---

## Pasul 3: Colectați acreditările

Dialogul care apare după creare afișează:

- **Client ID** — se termină în `.apps.googleusercontent.com` → devine `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → devine `DIGNA_OIDC_CLIENT_SECRET`

Ambele pot fi recuperate și ulterior din pagina de detalii a acreditării, spre deosebire de majoritatea celorlalți furnizori.

---

## Pasul 4: URL-ul de discovery

Google folosește un singur URL de discovery pentru toți clienții — nu este nimic de înlocuit:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Pasul 5: Configurați digna

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
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Cheia (`key`) din ambele fișiere trebuie să se potrivească — `google` aici.

---

## Pasul 6: Testați

Reporniți backend-ul și serverul web, apoi deschideți dashboard-ul. Consultați [Testarea autentificării](overview.md#testing-login) pentru lista completă de verificări.

---

## Depanarea Google Workspace

### Error 400: redirect_uri_mismatch

URI-ul din `DIGNA_OIDC_REDIRECT_URI` nu se află în lista **Authorized redirect URIs** sau diferă printr-un slash final ori prin schemă. Pagina de eroare Google afișează URI-ul primit — comparați-l caracter cu caracter cu cel înregistrat.

### Aplicația este blocată / nu a finalizat verificarea

Ecranul de consimțământ este **External** și încă în *Testing*. Publicați-l sau treceți aplicația la **Internal**.

### Access Blocked: Authorization Error

Contul care încearcă să se autentifice se află în afara domeniului dvs. Workspace, în timp ce ecranul de consimțământ este **Internal**. Acesta este comportamentul intenționat — aplicațiile Internal acceptă doar conturi din organizație.

### Modificările durează câteva minute

Google propagă asincron modificările acreditărilor și ale ecranului de consimțământ. Un redirect URI nou adăugat poate avea nevoie de câteva minute pentru a intra în vigoare; dacă o modificare pare ignorată, așteptați și reîncercați înainte de a investiga mai departe.

---

## Vezi și

- [Prezentarea Single Sign-On](overview.md) — referință de configurare, testare și depanare generală
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)

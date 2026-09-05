---
title: Microsoft Entra ID SSO – Integrare Single Sign-On | Documentație digna
description: Configurați Single Sign-On pentru digna cu Microsoft Entra ID (anterior Azure AD) folosind OpenID Connect — înregistrarea aplicației, redirect URI, client secret, ID-ul tenantului și configurația digna corespunzătoare.
image: /assets/logo_square.png
keywords: digna sso, microsoft entra id, azure ad sso, integrare OIDC, înregistrare aplicație, autentificare enterprise
---

# Configurați SSO cu Microsoft Entra ID

Microsoft Entra ID (anterior Azure Active Directory) este un furnizor complet compatibil OIDC, astfel că digna se integrează cu el prin endpoint-ul standard de discovery.

Acest ghid acoperă **partea Entra ID**: înregistrarea aplicației și colectarea celor patru valori de care are nevoie digna. Partea digna — `dashboard_config.toml`, testarea și depanarea — este aceeași pentru toți furnizorii și este descrisă în [Prezentare generală Single Sign-On](overview.md).

---

## Înainte de a începe

| Cerință | Observații |
|---|---|
| **Rol Entra ID** | Application Administrator, Cloud Application Administrator sau Global Administrator |
| **digna redirect URI** | URL-ul la care utilizatorii revin după autentificare, ex. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | Directorul în care se autentifică utilizatorii |

---

## Pasul 1: Înregistrați aplicația

1. Autentificați-vă în [Microsoft Entra admin center](https://entra.microsoft.com)
2. Accesați **Identity → Applications → App registrations**
3. Faceți clic pe **New registration**
4. Configurați:
   - **Name**: `digna` (afișat utilizatorilor pe ecranul de consimțământ)
   - **Supported account types**: *Accounts in this organizational directory only* pentru o implementare single-tenant
5. Sub **Redirect URI**, selectați platforma **Web** și introduceți URL-ul de callback al digna:

```
https://digna.yourdomain.com/oidc/callback
```

6. Faceți clic pe **Register**

!!! warning "Important"

    Platforma trebuie să fie **Web**, nu *Single-page application*. digna face schimbul codului de autorizare de pe backend folosind un client secret, lucru pe care tipul SPA nu îl permite.

---

## Pasul 2: Colectați ID-ul client și ID-ul tenantului

Pe pagina **Overview** a aplicației, copiați:

- **Application (client) ID** → devine `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → intră în URL-ul de discovery

---

## Pasul 3: Creați un Client Secret

1. Accesați **Certificates & secrets → Client secrets**
2. Faceți clic pe **New client secret**
3. Introduceți o descriere și alegeți o perioadă de expirare
4. Faceți clic pe **Add**
5. Copiați imediat coloana **Value**

!!! warning "Copiați Value, nu Secret ID"

    Coloana **Value** este afișată o singură dată, pe această pagină, și nu poate fi recuperată ulterior. **Secret ID** afișat lângă arată similar, dar nu este secretul — folosirea lui generează eroarea `invalid_client` la autentificare. Dacă părăsiți pagina înainte de a copia, ștergeți secretul și creați unul nou.

!!! tip "Sfat"

    Entra ID limitează durata de viață a secretelor la 24 de luni, astfel încât fiecare integrare SSO are o dată de expirare. Notați-o undeva vizibil — un secret expirat oprește SSO pentru toți utilizatorii deodată, fără avertisment pe pagina de login.

---

## Pasul 4: Confirmați permisiunile API

1. Accesați **API permissions**
2. Confirmați că **Microsoft Graph → User.Read** (delegated) este prezentă — este adăugată implicit

Scopurile `openid`, `profile` și `email` pe care le solicită digna fac parte din setul standard OIDC și nu necesită un grant separat. Dacă tenantul vostru solicită consimțământ de administrator pentru toate aplicațiile, faceți clic pe **Grant admin consent for <tenant>**.

---

## Pasul 5: Construiți URL-ul de discovery

Substituiți **Directory (tenant) ID** din Pasul 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Folosiți endpoint-ul v2.0"

    Segmentul `/v2.0/` este important. Endpoint-ul v1.0 la `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` emite tokenuri într-un format mai vechi și nu returnează revendicările standard OIDC pe care le așteaptă digna.

Deschideți URL-ul într-un browser înainte de a continua. Un document JSON confirmă că tenant ID-ul este corect.

---

## Pasul 6: Configurați digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

`key` din ambele fișiere trebuie să coincidă — aici `microsoft`.

---

## Pasul 7: Testați

Reporniți backend-ul și serverul web, apoi deschideți dashboard-ul. Vezi [Testarea autentificării](overview.md#testing-login) pentru lista completă de verificare.

---

## Depanare Entra ID

### AADSTS50011: Nepotrivire Redirect URI

URI-ul din `DIGNA_OIDC_REDIRECT_URI` diferă de cel înregistrat la Pasul 1. Entra ID compară întregul șir, așa că un slash final, `http` versus `https` sau un port diferit contează ca diferență. Verificați **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Secretul clientului nevalid

Fie a fost copiat **Secret ID** în loc de **Value**, fie secretul a expirat. Creați un secret nou și copiați coloana Value.

### AADSTS650057: Resursă invalidă

Înregistrarea aplicației a fost ștearsă sau aparține unui alt tenant decât cel din URL-ul de discovery. Confirmați Directory (tenant) ID pe pagina Overview.

### Utilizatorii se autentifică, dar nu se întâmplă nimic

Dacă tenantul necesită consimțământ de administrator și acesta nu a fost acordat, redirect-ul se întoarce fără un token utilizabil. Acordați consimțământul de administrator sub **API permissions**.

---

## Vezi și

- [Prezentare generală Single Sign-On](overview.md) — referință de configurare, testare și depanare generală
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
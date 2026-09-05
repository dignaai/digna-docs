---
title: Keycloak SSO – Integrare Single Sign-On | Documentație digna
description: Configurează Single Sign-On pentru digna cu Keycloak folosind OpenID Connect — configurare realm și client, autentificarea clientului, URI-uri de redirect valide, secretul clientului și configurația digna corespunzătoare.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, client confidențial, openid connect, furnizor de identitate self-hosted
---

# Configurați SSO cu Keycloak

Keycloak este un furnizor de identitate self-hosted, complet compatibil OIDC. Pentru că îl rulați dvs., URL-ul de discovery este construit din propriul nume de host și realm, nu dintr-un domeniu al unui furnizor.

Acest ghid acoperă **partea Keycloak**: crearea clientului și colectarea valorilor de care are nevoie digna. Partea digna — `dashboard_config.toml`, testarea și depanarea — este aceeași pentru orice furnizor și este descrisă în [Prezentare generală Single Sign-On](overview.md).

---

## Înainte de a începe

| Cerință | Notițe |
|---|---|
| **Versiune Keycloak** | 17 sau mai recent pentru căile URL folosite aici — vedeți nota din Pasul 4 |
| **Rol Keycloak** | `realm-admin` în realm-ul țintă, sau administrator de server |
| **Realm** | Realm-ul din care fac parte utilizatorii digna, nu neapărat `master` |
| **URI de redirect digna** | URL-ul la care utilizatorii revin după autentificare, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Pasul 1: Selectați realm-ul

1. Deschideți consola de administrare Keycloak
2. Folosiți selectorul de realm din stânga sus pentru a comuta la realm-ul în care se află utilizatorii dvs.

!!! warning "Nu folosiți realm-ul master"

    Realm-ul `master` este destinat administrării Keycloak în sine. Clienții aplicațiilor trebuie să aparțină unui realm dedicat; punerea digna în `master` oferă utilizatorilor ei acces în consola de administrare Keycloak.

---

## Pasul 2: Creați clientul

1. Mergeți la **Clients** și faceți clic pe **Create client**
2. Configurați:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — acesta devine `DIGNA_OIDC_CLIENT_ID`
3. Faceți clic pe **Next**
4. La pasul **Capability config**, porniți **Client authentication**
5. Lăsați **Standard flow** activat; celelalte flow-uri nu sunt necesare
6. Faceți clic pe **Next**

!!! warning "Client authentication trebuie activată"

    Cu **Client authentication** dezactivat, Keycloak creează un client *public*, care nu are deloc credențiale — fila **Credentials** din Pasul 4 nu va exista. digna are nevoie de un client confidențial. Această setare poate fi schimbată după creare dacă ați greșit.

---

## Pasul 3: Configurați URI-ul de redirect

La pasul **Login settings** (sau la fila **Settings** ulterior):

1. **Valid redirect URIs**: introduceți URL-ul callback al digna:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: lăsați gol, sau setați la `+` pentru a oglindi redirect URIs
3. Faceți clic pe **Save**

!!! tip "Evitați wildcard-urile"

    Keycloak acceptă pattern-uri precum `https://digna.yourdomain.com/*`. Un wildcard permite oricărui path de pe acel host să primească un cod de autorizare, deci preferați URL-ul exact al callback-ului.

---

## Pasul 4: Obțineți secretul clientului

1. Deschideți fila **Credentials**
2. Confirmați că **Client Authenticator** este *Client Id and Secret*
3. Copiați **Client secret** → devine `DIGNA_OIDC_CLIENT_SECRET`

Secretul rămâne recuperabil aici și poate fi regénérat cu **Regenerate**.

---

## Pasul 5: Construiți URL-ul de discovery

Înlocuiți host-ul Keycloak și numele realm-ului:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

De exemplu:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 și versiunile anterioare includ /auth"

    Înainte de Keycloak 17, fiecare endpoint se afla sub prefixul `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distribuțiile care setează `KC_HTTP_RELATIVE_PATH=/auth` păstrează și pe versiunile curente layout-ul vechi. Dacă URL-ul fără `/auth` returnează 404, încercați-l cu.

Deschideți URL-ul într-un browser înainte de a continua. Un document JSON confirmă că host-ul și realm-ul sunt corecte.

---

## Pasul 6: Configurați digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Autentificare cu Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<secretul clientului copiat la Pasul 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Cheia `key` din ambele fișiere trebuie să se potrivească — aici `keycloak`. Observați că nu trebuie neapărat să fie egală cu **Client ID** din Keycloak, deși păstrarea lor identice face documentarea mai ușoară.

---

## Pasul 7: Testați

Repornți backend-ul și serverul web, apoi deschideți dashboard-ul. Consultați [Testarea autentificării](overview.md#testing-login) pentru lista completă de verificări.

---

## Depanare Keycloak

### Invalid parameter: redirect_uri

URL-ul callback nu este acoperit de **Valid redirect URIs**. Keycloak înregistrează URI-ul primit în log-ul serverului, ceea ce este cel mai rapid mod de a vedea nepotrivirea exactă.

### Fila Credentials lipsește

Clientul este public. Porniți **Client authentication** din **Settings → Capability config**.

### 404 la URL-ul de discovery

Fie numele realm-ului este greșit, fie deployment-ul folosește prefixul `/auth`. Verificați lista de realm-uri în consola de administrare și încercați ambele forme de URL.

### unauthorized_client sau invalid_client

**Standard flow** este dezactivat în **Capability config**, sau secretul a fost regénérat în Keycloak fără a actualiza `config.toml`.

### Erori de certificare din partea backend-ului

Un Keycloak self-hosted, aflat în spatele unui certificat privat sau semnat self-signed, va cauza eșecul apelului HTTPS outbound al digna către URL-ul de discovery. Instalați CA-ul emitent în trust store-ul mașinii care rulează backend-ul digna.

---

## Vezi și

- [Prezentare generală Single Sign-On](overview.md) — referință de configurare, testare și depanare generală
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)
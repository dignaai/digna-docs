---
title: Okta SSO – Integrare Single Sign-On | Documentația digna
description: Configurați Single Sign-On pentru digna cu Okta folosind OpenID Connect — integrarea aplicației, URI-urile de redirect pentru autentificare, acreditările clientului, alegerea serverului de autorizare și configurația digna corespunzătoare.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, integrare aplicație, server autorizare, openid connect, autentificare enterprise
---

# Configurați SSO cu Okta

Okta este compatibil cu OIDC, cu o particularitate care surprinde majoritatea integrărilor făcute pentru prima dată: un organizație Okta expune mai mult de un server de autorizare, iar fiecare are propria cale de discovery (descoperire).

Acest ghid acoperă **partea Okta**: crearea integrării aplicației și colectarea valorilor de care digna are nevoie. Partea digna — `dashboard_config.toml`, testarea și depanarea — este aceeași pentru orice furnizor și este descrisă în [Prezentarea Single Sign-On](overview.md).

---

## Înainte de a începe

| Cerință | Note |
|---|---|
| **Okta role** | Super Administrator, sau un rol de administrator permis să creeze integrări de aplicații |
| **Okta domain** | ex. `yourcompany.okta.com`, sau un domeniu personalizat dacă este configurat |
| **digna redirect URI** | URL-ul la care utilizatorii revin după autentificare, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Pasul 1: Creați integrarea aplicației

1. Conectați-vă la Okta Admin Console
2. Accesați **Applications → Applications**
3. Faceți clic pe **Create App Integration**
4. Selectați:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Faceți clic pe **Next**

!!! warning "Tipul aplicației nu poate fi schimbat"

    Alegerea *Single-Page Application* în loc de *Web Application* creează un client public fără secret, iar schimbul de cod la backend-ul digna va eșua cu `invalid_client`. Tipul este fixat la creare — o alegere greșită înseamnă ștergerea aplicației și reluarea procesului.

---

## Pasul 2: Configurați integrarea

1. **App integration name**: `digna`
2. **Grant type**: lăsați selectat *Authorization Code*
3. **Sign-in redirect URIs**: introduceți URL-ul callback digna:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: opțional
5. Sub **Assignments**, alegeți cine poate utiliza integrarea — un grup specific este mai sigur decât *Allow everyone in your organization to access*
6. Faceți clic pe **Save**

!!! note "Atribuirea este necesară"

    Okta autentifică utilizatorul și apoi verifică dacă îi este asignată aplicația. Un utilizator neasignat ajunge la pagina de login Okta, se autentifică cu succes și este refuzat la redirect-ul înapoi. Dacă autentificarea funcționează pentru dvs. dar nu pentru colegi, atribuirea este primul lucru de verificat.

---

## Pasul 3: Colectați acreditările

Pe fila aplicației **General**, sub **Client Credentials**:

- **Client ID** → devine `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → devine `DIGNA_OIDC_CLIENT_SECRET` (faceți clic pe pictograma ochi pentru a-l dezvălui)

---

## Pasul 4: Alegeți serverul de autorizare

Acesta este pasul care determină URL-ul de discovery. Accesați **Security → API** pentru a vedea serverele de autorizare din organizația dvs.

**Org authorization server** — emite token-uri pentru organizația Okta în sine:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — inclusiv cel pe care Okta îl creează numit `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Pentru serverul încorporat, `<auth_server_id>` este literal `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Pe care?"

    Folosiți serverul de autorizare **org** decât dacă organizația dvs. standardizează deja pe unul custom pentru politicile de acces API. Conturile Okta Developer au ca valoare implicită `default`; multe organizații enterprise îl dezactivează. Deschideți ambele URL-uri într-un browser — cel care returnează JSON în loc de o eroare este cel disponibil pentru dvs.

---

## Pasul 5: Configurați digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Autentificare cu Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<secretul clientului copiat la Pasul 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Cheia (`key`) din ambele fișiere trebuie să se potrivească — `okta` aici.

---

## Pasul 6: Testați

Reporniți backend-ul și serverul web, apoi deschideți dashboard-ul. Consultați [Testing Login](overview.md#testing-login) pentru lista completă de verificări.

---

## Depanarea Okta

### URI-ul de redirect nu este înregistrat

Okta afișează URI-ul problematic în eroare. Comparați-l cu **General → Sign-in redirect URIs**; Okta potrivește șirul complet, inclusiv eventualul slash final.

### Utilizatorul nu este atribuit aplicației client

Contul nu se află în lista de atribuiri a aplicației. Adăugați utilizatorul sau grupul său sub **Assignments**.

### 400 Bad Request: Server de autorizare invalid

`<auth_server_id>` din URL-ul de discovery nu există, de cele mai multe ori `default` pe un org unde a fost eliminat. Verificați **Security → API** pentru serverele disponibile efectiv.

### invalid_client la pasul Token

Integrarea a fost creată ca Single-Page Application și nu are secret de client. Recreați-o ca Web Application.

---

## Vezi și

- [Prezentarea Single Sign-On](overview.md) — referință de configurare, testare și depanare generală
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
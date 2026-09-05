---
title: AD FS SSO – Integrare Single Sign-On | Documentație digna
description: Configurați Single Sign-On pentru digna cu Active Directory Federation Services folosind OpenID Connect — grupul de aplicații, aplicația server, secretul partajat, scope-urile permise și configurația digna corespunzătoare.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, active directory federation services, adfs oidc, application group, openid connect, furnizor de identitate on-premises
---

# Configurați SSO cu AD FS

Active Directory Federation Services este opțiunea on-premises: propriile servere emit tokenurile, iar URL-ul de descoperire este numele dvs. de gazdă. AD FS suportă OpenID Connect din **Windows Server 2016** încolo.

Acest ghid acoperă **partea AD FS**: crearea grupului de aplicații și colectarea valorilor de care are nevoie digna. Partea digna — `dashboard_config.toml`, testarea și depanarea — este aceeași pentru toți furnizorii și este descrisă în [Prezentarea generală Single Sign-On](overview.md).

---

## Înainte de a începe

| Cerință | Notițe |
|---|---|
| **Versiune AD FS** | Windows Server 2016 sau ulterior — versiunile anterioare nu au suport OIDC |
| **Acces** | Administrator local pe serverul AD FS |
| **Nume serviciu de federare** | de ex. `adfs.yourdomain.com` |
| **URI de redirecționare digna** | URL-ul la care utilizatorii se întorc după autentificare, de ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Pasul 1: Creați grupul de aplicații

1. Pe serverul AD FS, deschideți **AD FS Management**
2. Click dreapta pe **Application Groups** și alegeți **Add Application Group**
3. Introduceți `digna` ca nume
4. Sub **Standalone applications** — sau **Client-Server applications** în funcție de versiunea dvs. — selectați **Server application accessing a web API**
5. Click **Next**

---

## Pasul 2: Configurați aplicația server

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS generează un GUID. Copiați-l — acesta devine `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: introduceți URL-ul de callback digna și click pe **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Click **Next**

!!! warning "Apăsați Add, nu doar Next"

    Câmpul pentru redirect URI are propriul buton **Add**. Dacă tastați un URI și apăsați **Next** fără să apăsați **Add**, acesta este ignorat și expertul nu afișează niciun avertisment. Confirmați că URI-ul apare în lista de sub câmp înainte de a continua.

---

## Pasul 3: Generați secretul partajat

1. Bifați **Generate a shared secret**
2. Copiați secretul generat → devine `DIGNA_OIDC_CLIENT_SECRET`
3. Click **Next**

!!! warning "Secretul este afișat o singură dată"

    AD FS afișează secretul partajat doar pe această pagină a expertului și nu îl poate afișa din nou. Dacă îl pierdeți, resetați-l ulterior din proprietățile grupului de aplicații.

---

## Pasul 4: Configurați Web API-ul

1. **Identifier**: introduceți același identificator de client din Pasul 2 și click pe **Add**
2. Click **Next**
3. Alegeți o **Access Control Policy** — *Permit everyone* este cel mai simplu punct de plecare; restricționați la un grup pentru producție
4. Click **Next**

---

## Pasul 5: Acordați scope-urile permise

La pasul **Configure Application Permissions**, bifați:

- `openid`
- `profile`
- `email`

Apoi click **Next** și finalizați expertul.

!!! warning "openid nu este bifat implicit"

    AD FS selectează prestabilit doar `user_impersonation` în unele versiuni. Fără `openid`, endpointul de token returnează un token OAuth de acces în loc de un ID token, iar digna nu poate identifica utilizatorul.

---

## Pasul 6: Confirmați endpoint-ul de descoperire

Înlocuiți numele serviciului dvs. de federare:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

De exemplu:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Deschideți-l într-un browser. Un document JSON confirmă că OIDC este activat și că numele gazdei este corect.

!!! note "Backend-ul trebuie să aibă încredere în certificat"

    O autoritate de certificare internă este comună pentru AD FS. Mașina care rulează backend-ul digna face propria cerere HTTPS către acest URL, deci CA-ul emitent trebuie să fie în magazinul de încredere al acelei mașini — nu doar în browserele persoanelor care se autentifică.

---

## Pasul 7: Configurați digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Autentificare cu Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Cheia `key` din ambele fișiere trebuie să coincidă — `adfs` aici.

---

## Pasul 8: Testare

Reporniți backend-ul și serverul web, apoi deschideți dashboard-ul. Consultați [Testarea autentificării](overview.md#testing-login) pentru lista completă de verificări.

---

## Depanare AD FS

### MSIS9611: Clientul nu are permisiunea de a accesa resursa

Identificatorul API-ului web din Pasul 4 nu corespunde cu identificatorul clientului, sau scope-urile din Pasul 5 nu au fost acordate. Ambele pot fi editate din proprietățile grupului de aplicații.

### MSIS9602: redirect_uri invalid

URI-ul a fost tastat, dar nu a fost adăugat cu butonul **Add**, sau diferă de `DIGNA_OIDC_REDIRECT_URI`. Verificați **Application Groups → digna → digna backend → Properties**.

### Nu se returnează ID Token

Lipsește scope-ul `openid` din permisiunile aplicației.

### Backend-ul nu poate accesa URL-ul de descoperire

Fie DNS pe gazda backend nu rezolvă numele serviciului de federare, fie certificatul AD FS nu este de încredere acolo. Testați cu `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` direct de pe serverul digna.

### Evenimente de verificat

Serverul AD FS înregistrează erorile în **Applications and Services Logs → AD FS → Admin** din Event Viewer, de obicei cu un motiv mai specific decât cel afișat în browser.

---

## Vezi și

- [Prezentarea generală Single Sign-On](overview.md) — referință de configurare, testare și depanare generală
- [Microsoft: scenarii AD FS OpenID Connect](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
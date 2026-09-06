# Configurați SSO cu Auth0

Auth0 este compatibil cu OIDC și expune un endpoint de discovery pentru fiecare tenant. Principalul lucru de configurat corect este domeniul tenantului, care apare în URL-ul de discovery și se schimbă dacă activați un domeniu personalizat.

Acest ghid acoperă partea **Auth0**: crearea aplicației și colectarea valorilor de care are nevoie digna. Partea digna — `dashboard_config.toml`, testarea și depanarea — este aceeași pentru toți furnizorii și este descrisă în [Prezentare generală Single Sign-On](overview.md).

---

## Înainte de a începe

| Cerință | Note |
|---|---|
| **Rol Auth0** | Administrator pe tenant |
| **Domeniul tenantului** | ex. `yourcompany.eu.auth0.com` — segmentul regiunii contează |
| **URI de redirecționare pentru digna** | URL-ul la care utilizatorii se întorc după autentificare, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Pasul 1: Creați aplicația

1. Autentificați-vă în [Panoul Auth0](https://manage.auth0.com)
2. Accesați **Applications → Applications**
3. Click pe **Create Application**
4. Denumiți-o `digna` și alegeți **Regular Web Applications**
5. Click pe **Create**

!!! warning "Selectați Regular Web Applications"

    *Single Page Application* și *Native* creează clienți publici fără secret. digna efectuează schimbul de cod din backend-ul său și are nevoie de un client confidențial, deci **Regular Web Applications** este tipul corect. Spre deosebire de unii furnizori, Auth0 vă permite să schimbați tipul mai târziu din **Settings → Application Type**.

---

## Pasul 2: Adăugați URL-ul de callback

Pe fila **Settings** a aplicației:

1. Găsiți **Allowed Callback URLs**
2. Introduceți URL-ul de callback digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Opțional, setați **Allowed Logout URLs** la URL-ul dashboard-ului dvs.
4. Derulați în jos și click pe **Save Changes**

!!! note "Separate prin virgulă, nu prin linii noi"

    Auth0 acceptă mai multe URL-uri de callback în acest câmp, separate prin virgule. O listă separată doar prin linii noi este citită ca un singur URL corupt și nu se potrivește cu nimic (fără niciun avertisment).

---

## Pasul 3: Colectați acreditările

Tot în **Settings**, în panoul **Basic Information**:

- **Domain** → se folosește în URL-ul de discovery
- **Client ID** → devine `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → devine `DIGNA_OIDC_CLIENT_SECRET` (click pentru a-l dezvălui)

---

## Pasul 4: Confirmați tipul de grant

1. Accesați **Settings → Advanced Settings → Grant Types**
2. Confirmați că **Authorization Code** este bifat

Este activat implicit pentru Regular Web Applications. Dacă a fost debifat, autentificarea digna eșuează cu `unauthorized_client`.

---

## Pasul 5: Construiți URL-ul de discovery

Înlocuiți **Domain** din Pasul 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

De exemplu:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Domeniile personalizate schimbă issuer-ul"

    Dacă tenantul folosește un domeniu personalizat precum `login.yourcompany.com`, folosiți acel domeniu în URL-ul de discovery. Amestecarea celor două — domeniul canonic în URL-ul de discovery și domeniul personalizat în browser — produce o nepotrivire a issuer-ului, iar tokenul este respins după o autentificare aparent reușită.

---

## Pasul 6: Configurați digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

Valoarea `key` din ambele fișiere trebuie să coincidă — aici este `auth0`.

---

## Pasul 7: Testați

Reporniti backend-ul și serverul web, apoi deschideți dashboard-ul. Vezi [Testarea autentificării](overview.md#testing-login) pentru lista completă de verificări.

---

## Depanare Auth0

### Neconcordanță a URL-ului de callback

Pagina de eroare Auth0 afișează URL-ul pe care l-a primit. Adăugați-l la **Allowed Callback URLs**, verificând că intrările sunt separate prin virgule.

### unauthorized_client

**Authorization Code** nu este activat din **Advanced Settings → Grant Types**, sau tipul aplicației nu este Regular Web Applications.

### Acces refuzat după un login reușit

Un Rule, Action sau trigger Post-Login din tenant respinge utilizatorul. Verificați **Actions → Flows → Login** și jurnalele tenantului din **Monitoring → Logs**, care arată motivul exact.

### Neconcordanță a issuer-ului

URL-ul de discovery și domeniul către care a fost trimis browser-ul diferă — de obicei domeniul canonic al tenantului versus un domeniu personalizat. Folosiți unul în mod consecvent.

---

## Vezi și

- [Prezentare generală Single Sign-On](overview.md) — referință de configurare, testare și depanare generală
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
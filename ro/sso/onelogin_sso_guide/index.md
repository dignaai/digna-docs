# Configurați SSO cu OneLogin

OneLogin este compatibil OIDC. Particularitatea sa este că tipul de conector se alege dintr-un catalog la crearea aplicației și nu mai poate fi schimbat ulterior.

Acest ghid acoperă **partea OneLogin**: crearea aplicației și colectarea valorilor de care digna are nevoie. Partea digna — `dashboard_config.toml`, testarea și depanarea — este aceeași pentru orice furnizor și este descrisă în [Prezentarea Single Sign-On](overview.md).

---

## Înainte de a începe

| Cerință | Note |
|---|---|
| **OneLogin role** | Proprietarul contului sau un administrator cu permisiunea de a adăuga aplicații |
| **Subdomain** | ex. `yourcompany.onelogin.com` |
| **digna redirect URI** | URL-ul la care utilizatorii revin după autentificare, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Pasul 1: Creați aplicația OIDC

1. Conectați-vă la portalul OneLogin Admin
2. Accesați **Applications → Applications**
3. Faceți clic pe **Add App**
4. Căutați `OpenId Connect` și selectați conectorul **OpenId Connect (OIDC)**
5. Setați **Display Name** la `digna`
6. Faceți clic pe **Save**

!!! warning "Tipul conectorului este fixat la creare"

    OneLogin are intrări separate în catalog pentru SAML și OIDC, iar o aplicație nu poate fi convertită de la una la alta. Dacă alegeți din greșeală un conector SAML, ștergeți aplicația și adăugați-o din nou — nu există nicio setare pentru schimbarea protocolului.

---

## Pasul 2: Configurați redirect URI-ul

1. Deschideți fila **Configuration**
2. În **Redirect URI's**, introduceți URL-ul callback digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Opțional, setați **Post Logout Redirect URIs** la URL-ul dashboard-ului
4. Faceți clic pe **Save**

!!! note "Un URI pe linie"

    Spre deosebire de furnizorii care așteaptă o listă separată prin virgule, câmpul **Redirect URI's** din OneLogin acceptă câte un URI pe fiecare linie.

---

## Pasul 3: Setați tipul aplicației și metoda de autentificare

1. Deschideți fila **SSO**
2. Confirmați că **Application Type** este *Web*
3. Setați **Token Endpoint → Authentication Method** la *POST* (`client_secret_post`) sau *Basic* (`client_secret_basic`)

!!! warning "Nu alegeți None"

    Setarea metodei de autentificare la *None* transformă aplicația într-un client public fără secret, iar schimbul de cod de la backend-ul digna va fi respins. Funcționează atât POST, cât și Basic.

---

## Pasul 4: Colectați acreditările

Tot în fila **SSO**:

- **Client ID** → devine `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → devine `DIGNA_OIDC_CLIENT_SECRET` (faceți clic pe **Show client secret**)

Pagina afișează și **Issuer URL**, care confirmă URL-ul de discovery de la pasul următor.

---

## Pasul 5: Atribuiți utilizatorii

1. Deschideți fila **Access**
2. Adăugați rolurile sau grupurile ai căror membri pot folosi digna
3. Faceți clic pe **Save**

!!! note "Utilizatorii neatribuiți sunt refuzați după autentificare"

    Ca la majoritatea furnizorilor, OneLogin autentifică mai întâi utilizatorul și abia apoi verifică dreptul de acces. Un utilizator neatribuit se autentifică cu succes și este apoi refuzat, ceea ce pare o eroare digna, nu o decizie de control al accesului.

---

## Pasul 6: Construiți URL-ul de discovery

Înlocuiți cu subdomeniul dvs. OneLogin:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

De exemplu:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 este versiunea API"

    Implementarea OIDC actuală a OneLogin se află sub `/oidc/2/`. Documentația mai veche arată `/oidc/` fără versiune, ceea ce indică prima versiune, retrasă. Dacă aveți dubii, verificați **Issuer URL** din fila SSO — URL-ul de discovery este issuer-ul plus `/.well-known/openid-configuration`.

---

## Pasul 7: Configurați digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc_clients.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Cheia (`key`) din ambele fișiere trebuie să se potrivească — `onelogin` aici.

---

## Pasul 8: Testați

Reporniți backend-ul și serverul web, apoi deschideți dashboard-ul. Consultați [Testarea autentificării](overview.md#testing-login) pentru lista completă de verificări.

---

## Depanarea OneLogin

### redirect_uri did not match

URL-ul callback lipsește din **Configuration → Redirect URI's**, sau intrările au fost separate prin virgule în loc de linii noi.

### invalid_client la pasul Token

**Token Endpoint → Authentication Method** este setat la *None*, sau client secret-ul din `config.toml` este învechit. Afișați secretul în fila **SSO** și comparați.

### Aplicația nu apare pentru utilizatori

Niciunui rol sau grup nu i s-a acordat acces în fila **Access**.

### 404 la URL-ul de discovery

Subdomeniul este greșit sau URL-ul omite `/oidc/2/`. Comparați cu **Issuer URL** afișat în fila SSO.

---

## Vezi și

- [Prezentarea Single Sign-On](overview.md) — referință de configurare, testare și depanare generală
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)
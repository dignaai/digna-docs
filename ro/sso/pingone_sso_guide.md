# Configurați SSO cu PingOne

PingOne este compatibil OIDC. Două dintre valorile sale necesită atenție: **ID-ul mediului** (environment ID), care apare în fiecare URL de endpoint, și **domeniul regional**, care diferă între tenanții din America de Nord, Europa, Canada, Asia-Pacific și Australia.

Acest ghid acoperă **partea PingOne**: crearea aplicației și colectarea valorilor de care digna are nevoie. Partea digna — `dashboard_config.toml`, testarea și depanarea — este aceeași pentru orice furnizor și este descrisă în [Prezentarea Single Sign-On](overview.md).

---

## Înainte de a începe

| Cerință | Note |
|---|---|
| **PingOne role** | Environment Admin sau Identity Data Admin pe mediul țintă |
| **Environment** | Mediul PingOne căruia îi aparțin utilizatorii digna |
| **digna redirect URI** | URL-ul la care utilizatorii revin după autentificare, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Pasul 1: Creați aplicația

1. Conectați-vă la consola de administrare PingOne și selectați mediul
2. Accesați **Applications → Applications**
3. Faceți clic pe butonul **+**
4. Introduceți `digna` ca **Application Name**
5. Selectați **OIDC Web App**
6. Faceți clic pe **Save**

!!! warning "Alegeți OIDC Web App, nu Single-Page App"

    *Single-Page App* și *Native App* creează clienți publici care nu pot păstra un secret. digna face schimbul codului de autorizare din backend și are nevoie de tipul confidențial **OIDC Web App**.

---

## Pasul 2: Configurați redirect URI-ul

1. Deschideți fila **Configuration** a aplicației
2. Faceți clic pe pictograma creion pentru editare
3. Confirmați că **Response Type** este *Code* și **Grant Type** este *Authorization Code*
4. Sub **Redirect URIs**, introduceți URL-ul callback digna:

```
https://digna.yourdomain.com/oidc/callback
```

5. Setați **Token Endpoint Authentication Method** la *Client Secret Post* sau *Client Secret Basic*
6. Faceți clic pe **Save**

---

## Pasul 3: Activați aplicația

Pe rândul aplicației sau în panoul de detalii, treceți comutatorul pe **enabled**.

!!! warning "Aplicațiile noi pornesc dezactivate"

    PingOne creează aplicațiile în stare dezactivată. O aplicație dezactivată produce la pasul de autorizare o eroare care nu menționează comutatorul, așa că merită verificat acest lucru înainte de a depana orice altceva.

---

## Pasul 4: Acordați scope-urile

1. Deschideți fila **Resources**
2. Confirmați că `openid` este acordat și adăugați `profile` și `email` din resursa **OpenID Connect**
3. Faceți clic pe **Save**

---

## Pasul 5: Atribuiți utilizatorii

1. Deschideți fila **Access**
2. Adăugați populația sau grupurile ai căror membri pot folosi digna
3. Faceți clic pe **Save**

---

## Pasul 6: Colectați acreditările și ID-ul mediului

În fila **Configuration**, extindeți **General**:

- **Client ID** → devine `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → devine `DIGNA_OIDC_CLIENT_SECRET` (faceți clic pe pictograma ochi)
- **Environment ID** → intră în URL-ul de discovery

Aceeași filă listează și **OIDC Discovery Endpoint** gata construit, pe care îl puteți copia direct în loc să îl asamblați manual.

---

## Pasul 7: Construiți URL-ul de discovery

Înlocuiți ID-ul mediului și domeniul pentru regiunea dvs.:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Regiune | Domeniu |
|---|---|
| America de Nord | `auth.pingone.com` |
| Europa | `auth.pingone.eu` |
| Canada | `auth.pingone.ca` |
| Asia-Pacific | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

Pentru un mediu european:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Copiați-l în loc să îl tastați"

    Domeniul regional este cea mai frecventă greșeală într-o integrare PingOne, iar o regiune greșită produce un 404 în loc de un mesaj util. Folosiți valoarea **OIDC Discovery Endpoint** de la Pasul 6.

---

## Pasul 8: Configurați digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc_clients.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Cheia (`key`) din ambele fișiere trebuie să se potrivească — `pingone` aici.

---

## Pasul 9: Testați

Reporniți backend-ul și serverul web, apoi deschideți dashboard-ul. Consultați [Testarea autentificării](overview.md#testing-login) pentru lista completă de verificări.

---

## Depanarea PingOne

### 404 la URL-ul de discovery

Domeniul regional sau ID-ul mediului este greșit. Comparați cu **OIDC Discovery Endpoint** afișat în fila Configuration a aplicației.

### NOT_FOUND sau Application Disabled

Comutatorul aplicației de la Pasul 3 este încă dezactivat.

### Nepotrivirea redirect URI-ului

PingOne potrivește șirul complet. Verificați în **Configuration → Redirect URIs** dacă există un slash final sau o diferență de schemă.

### Autentificarea reușește, dar niciun claim email nu ajunge la digna

Scope-urile `email` și `profile` nu au fost acordate în fila **Resources**.

### Utilizatorul nu poate vedea aplicația

Niciunei populații sau niciunui grup nu i s-a acordat acces în fila **Access**.

---

## Vezi și

- [Prezentarea Single Sign-On](overview.md) — referință de configurare, testare și depanare generală
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)
---
title: Panoramica Single Sign-On (SSO) | digna Documentation
description: Come funziona il Single Sign-On in digna usando OpenID Connect (OIDC). Copre la configurazione del dashboard e del backend, i test, la risoluzione dei problemi e collegamenti alle guide per provider per Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne e AD FS.
image: /assets/logo_square.png
keywords:
  - digna sso
  - accesso Single Sign-On
  - integrazione OIDC
  - OpenID Connect
  - Microsoft Entra ID
  - SSO Azure AD
  - SSO Google Workspace
  - integrazione Okta
  - autenticazione aziendale
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integration Guide
og_description: Configure Single Sign-On for digna using OpenID Connect. Step-by-step setup for Microsoft Entra ID, Google Workspace, Okta, and other OIDC-compliant identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Panoramica Single Sign-On

---

## Indice

1. [Introduzione e panoramica](#introduction-and-overview)
2. [Guide per i provider](#provider-guides)
3. [Passaggi di configurazione](#configuration-steps)
4. [Configurazione del dashboard](#dashboard-configuration)
5. [Configurazione del backend](#backend-configuration)
6. [Test di accesso](#testing-login)
7. [Risoluzione dei problemi](#troubleshooting)
8. [Provider supportati](#supported-providers)

---

## Introduzione e panoramica {: #introduction-and-overview }

Questa guida fornisce istruzioni passo-passo per integrare il Single Sign-On (SSO) con la piattaforma digna usando **OpenID Connect (OIDC)**.

### Cos'è SSO?

Single Sign-On permette agli utenti di accedere a digna in modo sicuro utilizzando le credenziali aziendali tramite provider di identità esterni. Gli utenti possono autenticarsi con le proprie credenziali corporate invece di gestire password separate per digna.

### Come funziona

Lo SSO in digna è implementato usando il protocollo OIDC. Possono essere configurati più provider di identità in parallelo modificando due file di configurazione chiave:

- **`dashboard_config.toml`** — Controlla l'interfaccia di accesso frontend
- **`config.toml`** — Configura le connessioni OIDC del backend

### Provider supportati {: #supported-providers-overview }

Gli esempi in questa guida utilizzano **Microsoft** e **Google**, ma **qualsiasi provider compatibile con OIDC** può essere integrato seguendo la stessa struttura.

---

## Guide per i provider {: #provider-guides }

Ogni provider richiede gli stessi quattro valori — un client ID, un client secret, una redirect URI e una discovery URL — ma ciascuno li posiziona in modo diverso nella sua console di amministrazione, e diversi hanno un passaggio specifico che gli altri non richiedono. Le guide qui sotto coprono quella metà del lavoro; questa pagina copre la parte relativa a digna, che è identica per tutti loro.

| Provider | Guida | Da sapere |
|---|---|---|
| **AD FS** | [Configura SSO con AD FS](adfs_sso_guide.md) | Self-hosted; l'unico provider qui dove controlli il servizio token |
| **Auth0** | [Configura SSO con Auth0](auth0_sso_guide.md) | La discovery URL è per-tenant, e i domini personalizzati la cambiano |
| **Google Workspace** | [Configura SSO con Google Workspace](google_workspace_sso_guide.md) | La schermata di consenso deve essere pubblicata prima che utenti non di test possano accedere |
| **Keycloak** | [Configura SSO con Keycloak](keycloak_sso_guide.md) | Self-hosted; la discovery URL è per-realm |
| **Microsoft Entra ID** | [Configura SSO con Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | L'ID tenant appare nella discovery URL; i secret scadono |
| **Okta** | [Configura SSO con Okta](okta_sso_guide.md) | La scelta del server di autorizzazione cambia la discovery URL |
| **OneLogin** | [Configura SSO con OneLogin](onelogin_sso_guide.md) | Il tipo di app OIDC deve essere scelto alla creazione e non può essere cambiato |
| **PingOne** | [Configura SSO con PingOne](pingone_sso_guide.md) | L'ID ambiente appare nella discovery URL |

Qualsiasi altro provider compatibile con OIDC funziona allo stesso modo — vedi [Altri provider OIDC](#supported-providers).

---

## Passaggi di configurazione {: #configuration-steps }

La configurazione dello SSO richiede aggiornamenti a due file. Questa sezione spiega come configurare ciascuno di essi.

### Panoramica dei file di configurazione

| File | Posizione | Scopo |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Interfaccia di accesso frontend |
| **config.toml** | `/config.toml` | Connessioni OIDC del backend |

Entrambi i file devono essere configurati perché lo SSO funzioni correttamente.

---

## Configurazione del dashboard {: #dashboard-configuration }

### Posizione del file

```
dashboard/dashboard_config.toml
```

### Passaggio 1: Aggiungere provider OIDC

Aggiungi voci sotto l'array `[[login.oidc]]` per ogni provider di identità che vuoi supportare.

**Esempio con Microsoft e Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Passaggio 2: Configurare le opzioni di accesso

Specifica se l'accesso tramite password deve essere consentito:

```toml
[login]
usePassword = true
```

### Parametri di configurazione

#### Sezione `[[login.oidc]]`

| Parametro | Tipo | Obbligatorio | Descrizione |
|---|---|---|---|
| `key` | string | Sì | Identificatore univoco per la connessione OIDC (deve corrispondere alla key in config.toml) |
| `label` | string | Sì | Testo mostrato sul pulsante di accesso (es. "Login with Microsoft") |

#### Sezione `[login]`

| Parametro | Tipo | Predefinito | Descrizione |
|---|---|---|---|
| `usePassword` | boolean | false | Consentire l'accesso tramite password oltre allo SSO |

### Capire usePassword

**Se `usePassword = true`:**
- La schermata di accesso mostra i pulsanti SSO (es. "Login with Microsoft")
- La schermata di accesso mostra anche i campi username e password
- Gli utenti possono autenticarsi con uno dei due metodi
- Consente configurazioni ibride dove alcuni utenti usano SSO e altri password

**Se `usePassword = false` (o omesso):**
- La schermata di accesso mostra solo i pulsanti SSO
- Nessun campo username/password
- È disponibile solo l'autenticazione OIDC

!!! tip "Suggerimento"

    L'accesso tramite password è disponibile solo per gli utenti creati con password usando il comando `digna user add` o tramite il dashboard.

### Esempio completo

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

## Configurazione del backend {: #backend-configuration }

### Posizione del file

```
/config.toml
```

(Directory di installazione root di digna)

### Passaggio 1: Aggiungere sezioni provider OIDC

Ogni provider deve avere una sezione dedicata `[oidc.<key>]`. La key deve corrispondere alla `key` definita in `dashboard_config.toml`.

### Configurazione Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Configurazione Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Parametri di configurazione

| Parametro | Tipo | Obbligatorio | Descrizione | Esempio |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Sì | Client ID dal provider di identità | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Sì | Client secret dal provider di identità | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Sì | URL di callback dopo l'autenticazione | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Sì | Endpoint di configurazione OIDC | `https://login.microsoftonline.com/...` |

!!! warning "Importante"

    Sostituisci i valori segnaposto (`<client_id>`, `<client_secret>`, `<tenant_id>`) con le credenziali reali dal portale sviluppatori del tuo provider di identità.

### Redirect URI

La redirect URI deve essere la stessa configurata nel provider di identità:

```
http://localhost:5173/oidc/callback
```

Se digna è ospitato in un dominio diverso, aggiorna di conseguenza:
- Locale: `http://localhost:5173/oidc/callback`
- Produzione: `https://digna.yourdomain.com/oidc/callback`

### Esempio completo

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

## Test di accesso {: #testing-login }

Dopo aver completato la configurazione, verifica che lo SSO funzioni correttamente.

### Checklist prima del test

Prima di eseguire i test, assicurati che:

- [ ] `dashboard_config.toml` sia stato aggiornato con i provider OIDC
- [ ] `config.toml` sia stato aggiornato con le credenziali OIDC
- [ ] Entrambi i file siano stati salvati
- [ ] Le credenziali siano corrette (client ID, client secret)
- [ ] La redirect URI corrisponda all'URL di deployment
- [ ] L'applicazione nel provider di identità sia configurata con la redirect URI

### Passaggi di test

#### Passaggio 1: Riavviare i servizi

Riavvia il backend di digna e il web server per applicare le modifiche.

**Se in esecuzione come servizio su Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Se in esecuzione come servizio su Linux o macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Se eseguito manualmente:**
```bash
digna serve --address localhost --port 8082
```

**Riavvia anche il web server** — IIS o Tomcat su Windows, nginx o Apache su Linux e macOS.

#### Passaggio 2: Aprire il dashboard

Apri il dashboard di digna nel browser:

```
http://localhost:5173
```

(o l'URL del dashboard configurato)

#### Passaggio 3: Verificare i pulsanti di accesso

Controlla che appaiano i pulsanti di accesso per ogni provider configurato:

- Dovrebbe apparire il pulsante "Login with Microsoft"
- Dovrebbe apparire il pulsante "Login with Google"
- (Se usePassword = true) Dovrebbero apparire i campi username/password

Se i pulsanti non appaiono:
- Verifica che `dashboard_config.toml` sia stato salvato
- Verifica che il servizio del dashboard sia stato riavviato
- Controlla la console del browser (F12) per errori

#### Passaggio 4: Testare l'accesso SSO

Clicca uno dei pulsanti SSO (es. "Login with Microsoft"):

1. Dovresti essere reindirizzato alla pagina di accesso del provider di identità
2. Effettua il login con le credenziali aziendali
3. Verresti reindirizzato indietro a digna
4. Dovresti risultare autenticato in digna

#### Passaggio 5: Verificare la creazione utente

Dopo un accesso SSO riuscito:

- L'utente dovrebbe essere creato automaticamente in digna
- L'utente dovrebbe risultare autenticato
- Il profilo utente dovrebbe mostrare le credenziali del provider di identità
- Dovresti vedere il dashboard di digna

#### Passaggio 6: Testare l'accesso con password (se abilitato)

Se `usePassword = true`:

1. Effettua il logout da digna
2. Nella pagina di accesso, inserisci username e password
3. Dovresti poter effettuare l'accesso con le credenziali a password

---

## Risoluzione dei problemi {: #troubleshooting }

### I pulsanti di accesso non compaiono

**Sintomi:**
- Pulsanti di accesso OIDC non visibili nella pagina di login
- Vedi solo i campi password (se usePassword = true)

**Cause e soluzioni:**
1. Controlla che `dashboard_config.toml` sia nella directory `dashboard/`
2. Verifica che siano presenti le sezioni `[[login.oidc]]` con la sintassi corretta
3. Riavvia il servizio del dashboard
4. Svuota la cache del browser (Ctrl+Shift+Delete o Cmd+Shift+Delete)
5. Controlla la console del browser (F12 → tab Console) per errori

---

### Errore di mismatch della Redirect URI

**Sintomi:**
- Dopo aver cliccato il pulsante SSO, errore su "redirect_uri mismatch"
- Errore "The redirect URI is not registered"

**Cause e soluzioni:**
1. Verifica che `DIGNA_OIDC_REDIRECT_URI` in `config.toml` sia corretto
2. Verifica che la redirect URI sia registrata nelle impostazioni del provider di identità
3. Assicurati che entrambi usino URL identiche (inclusi protocollo, dominio, path)
4. Controlla eventuali errori di battitura nella redirect URI
5. Se usi HTTPS, assicurati che il certificato sia valido

---

### Errore credenziali client non valide

**Sintomi:**
- Errore "Invalid client ID or secret"
- L'autenticazione fallisce con errore di credenziali

**Cause e soluzioni:**
1. Verifica che `DIGNA_OIDC_CLIENT_ID` e `DIGNA_OIDC_CLIENT_SECRET` siano corretti
2. Assicurati che non ci siano spazi in eccesso o caratteri speciali non voluti
3. Controlla che le credenziali non siano scadute o revocate
4. Riavvia il servizio backend dopo aver aggiornato la configurazione
5. Controlla la console del provider di identità per confermare che le credenziali siano attive

---

### Login bloccato o in timeout

**Sintomi:**
- Cliccando il pulsante SSO non succede nulla
- Timeout dopo alcuni secondi
- Il browser mostra "Failed to connect" o messaggi simili

**Cause e soluzioni:**
1. Verifica che il backend di digna sia in esecuzione: `digna repo check`
2. Controlla la connettività di rete verso il provider di identità
3. Verifica che `DIGNA_OIDC_CONFIGURATION_URL` sia accessibile
4. Controlla le regole del firewall che permettano connessioni HTTPS in uscita
5. Verifica che backend e dashboard possano raggiungersi a vicenda

---

### Utenti non creati automaticamente

**Sintomi:**
- Login SSO ha successo ma l'utente non viene creato in digna
- Si riceve errore di permessi dopo il login SSO

**Cause e soluzioni:**
1. Verifica che la configurazione OIDC sia corretta
2. Controlla che i permessi utente siano impostati correttamente
3. Revisiona i log di digna per messaggi di errore
4. Riavvia il servizio backend
5. Contatta support@digna.ai se il problema persiste

---

## Provider supportati {: #supported-providers }

### Testati e supportati

I seguenti provider OIDC sono stati testati e sono noti per funzionare:

| Provider | Configuration URL | Guida di setup |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Configura SSO con AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Configura SSO con Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Configura SSO con Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Configura SSO con Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Configura SSO con Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Configura SSO con Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Configura SSO con OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Configura SSO con PingOne](pingone_sso_guide.md) |

### Altri provider OIDC

Qualsiasi provider che supporti OpenID Connect può essere integrato. Informazioni richieste:

- Client ID
- Client secret
- OpenID configuration URL (di solito in `/.well-known/openid-configuration`)
- Scopes supportati (tipicamente `openid profile email`)

Contatta support@digna.ai se hai bisogno di aiuto per integrare un provider specifico.

---

## Best practice

**FARE:**
- Usare HTTPS in produzione (non HTTP)
- Conservare i client secret in modo sicuro (usare variabili d'ambiente se possibile)
- Ruotare i secret periodicamente
- Testare prima in un ambiente non di produzione
- Documentare quali provider sono configurati
- Monitorare i log di accesso per attività sospette
- Tenere la configurazione del provider di identità sincronizzata con la configurazione di digna

**NON FARE:**
- Conservare i client secret nel version control
- Usare redirect URI HTTP in produzione
- Configurare più provider con la stessa key
- Lasciare credenziali di default/test in produzione
- Esporre file di configurazione contenenti secret
- Mischiare credenziali di sviluppo e produzione

---

## Supporto

Hai bisogno di aiuto con la configurazione dello SSO?

- **Email:** support@digna.ai
- **Documentazione:** https://docs.digna.ai
- **Sito web:** https://www.digna.ai

---

**Ultimo aggiornamento:** 30 agosto 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
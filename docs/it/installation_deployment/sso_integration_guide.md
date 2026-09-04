---
title: Guida all'integrazione Single Sign-On (SSO) | Documentazione digna
description: Guida passo-passo per configurare Single Sign-On (SSO) per digna usando OpenID Connect (OIDC). Copre configurazione della dashboard e del backend, test, risoluzione dei problemi e provider di identità supportati tra cui Microsoft Entra ID, Google Workspace e Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - integrazione oidc
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - integrazione okta
  - autenticazione enterprise
lang: it
robots: index, follow
og_title: digna Single Sign-On (SSO) Integration Guide
og_description: Configure Single Sign-On for digna using OpenID Connect. Step-by-step setup for Microsoft Entra ID, Google Workspace, Okta, and other OIDC-compliant identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Guida all'integrazione Single Sign-On

---

## Indice

1. [Introduzione e panoramica](#introduction-and-overview)
2. [Passaggi di configurazione](#configuration-steps)
3. [Configurazione della dashboard](#dashboard-configuration)
4. [Configurazione del backend](#backend-configuration)
5. [Test di accesso](#testing-login)
6. [Risoluzione dei problemi](#troubleshooting)
7. [Provider supportati](#supported-providers)

---

## Introduzione e panoramica {: #introduction-and-overview }

Questa guida fornisce istruzioni passo-passo per integrare Single Sign-On (SSO) con la piattaforma digna usando **OpenID Connect (OIDC)**.

### Cos'è SSO?

Single Sign-On permette agli utenti di accedere a digna in modo sicuro usando le credenziali aziendali tramite provider di identità esterni. Gli utenti possono autenticarsi con le credenziali aziendali invece di gestire password separate per digna.

### Come funziona

Lo SSO in digna è implementato usando il protocollo OIDC. Possono essere configurati più provider di identità in parallelo modificando due file di configurazione chiave:

- **`dashboard_config.toml`** — Controlla l'interfaccia di login frontend
- **`config.toml`** — Configura le connessioni OIDC del backend

### Provider supportati {: #supported-providers-overview }

Gli esempi in questa guida utilizzano **Microsoft** e **Google**, ma **qualsiasi provider compatibile OIDC** può essere integrato seguendo la stessa struttura.

Provider OIDC comuni includono:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Altri provider di identità compatibili OIDC

---

## Passaggi di configurazione {: #configuration-steps }

La configurazione SSO richiede aggiornamenti a due file. Questa sezione spiega come configurare ciascuno di essi.

### Panoramica dei file di configurazione

| File | Posizione | Scopo |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Interfaccia di login frontend |
| **config.toml** | `/config.toml` | Connessioni OIDC del backend |

Entrambi i file devono essere configurati affinché lo SSO funzioni correttamente.

---

## Configurazione della dashboard {: #dashboard-configuration }

### Posizione del file

```
dashboard/dashboard_config.toml
```

### Passo 1: Aggiungere provider OIDC

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

### Passo 2: Configurare le opzioni di login

Specifica se il login tramite password deve essere consentito:

```toml
[login]
usePassword = true
```

### Parametri di configurazione

#### Sezione `[[login.oidc]]`

| Parametro | Tipo | Richiesto | Descrizione |
|---|---|---|---|
| `key` | string | Sì | Identificatore univoco per la connessione OIDC (deve corrispondere alla key in config.toml) |
| `label` | string | Sì | Testo visualizzato sul pulsante di login (es., "Login with Microsoft") |

#### Sezione `[login]`

| Parametro | Tipo | Predefinito | Descrizione |
|---|---|---|---|
| `usePassword` | boolean | false | Consente il login tramite password oltre allo SSO |

### Comprendere usePassword

**Se `usePassword = true`:**
- La schermata di login mostra i pulsanti SSO (es., "Login with Microsoft")
- La schermata di login mostra anche i campi username e password
- Gli utenti possono autenticarsi con entrambi i metodi
- Consente configurazioni ibride in cui alcuni utenti usano SSO e altri password

**Se `usePassword = false` (o omesso):**
- La schermata di login mostra solo i pulsanti SSO
- Nessun campo username/password
- Disponibile solo l'autenticazione OIDC

> **💡 Suggerimento**
>
> Il login tramite password è disponibile solo per gli utenti creati con password usando il comando `digna user add` o tramite la dashboard.

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

(Directory principale dell'installazione digna)

### Passo 1: Aggiungere sezioni provider OIDC

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

| Parametro | Tipo | Richiesto | Descrizione | Esempio |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Sì | Client ID fornito dal provider di identità | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Sì | Client secret fornito dal provider di identità | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Sì | URL di callback dopo l'autenticazione | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Sì | Endpoint di configurazione OIDC | `https://login.microsoftonline.com/...` |

> **⚠️ Importante**
>
> Sostituisci i valori segnaposto (`<client_id>`, `<client_secret>`, `<tenant_id>`) con le credenziali effettive ottenute dal portale sviluppatori del tuo provider di identità.

### Redirect URI

Il redirect URI deve essere lo stesso nella configurazione del provider di identità:

```
http://localhost:5173/oidc/callback
```

Se digna è ospitato su un dominio diverso, aggiornalo di conseguenza:
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

### Checklist pre-test

Prima di testare, assicurati di:

- [ ] aver aggiornato `dashboard_config.toml` con i provider OIDC
- [ ] aver aggiornato `config.toml` con le credenziali OIDC
- [ ] aver salvato entrambi i file
- [ ] le credenziali siano corrette (client ID, client secret)
- [ ] il redirect URI corrisponda all'URL del tuo deployment
- [ ] l'applicazione del provider di identità sia configurata con il redirect URI

### Passaggi per il test

#### Passo 1: Riavviare i servizi

Riavvia il backend e il web server di digna per applicare le modifiche.

**Se eseguito come servizio Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Se eseguito manualmente:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Se si usa IIS o Tomcat:**
Riavvia il servizio del web server.

#### Passo 2: Aprire la dashboard

Apri la dashboard di digna nel browser:

```
http://localhost:5173
```

(o il tuo URL configurato per la dashboard)

#### Passo 3: Verificare i pulsanti di login

Controlla che appaiano i pulsanti di login per ogni provider configurato:

- ✅ Dovrebbe comparire il pulsante "Login with Microsoft"
- ✅ Dovrebbe comparire il pulsante "Login with Google"
- ✅ (Se usePassword = true) Dovrebbero comparire i campi username/password

Se i pulsanti non appaiono:
- Verifica che `dashboard_config.toml` sia stato salvato
- Verifica che il servizio della dashboard sia stato riavviato
- Controlla la console del browser (F12) per errori

#### Passo 4: Testare il login SSO

Clicca uno dei pulsanti SSO (es., "Login with Microsoft"):

1. Verrai reindirizzato alla pagina di login del provider di identità
2. Accedi con le tue credenziali aziendali
3. Verrai reindirizzato di nuovo a digna
4. Dovresti risultare autenticato su digna

#### Passo 5: Verificare la creazione utente

Dopo un login SSO riuscito:

- ✅ L'utente dovrebbe essere creato automaticamente in digna
- ✅ L'utente dovrebbe risultare autenticato
- ✅ Il profilo utente dovrebbe mostrare le informazioni del provider di identità
- ✅ Dovresti vedere la dashboard di digna

#### Passo 6: Testare il login con password (se abilitato)

Se `usePassword = true`:

1. Effettua il logout da digna
2. Nella pagina di login, inserisci username e password
3. Dovresti essere in grado di accedere con le credenziali di password

---

## Risoluzione dei problemi {: #troubleshooting }

### I pulsanti di login non appaiono

**Sintomi:**
- Pulsanti di login OIDC non visibili nella pagina di login
- Vedi solo i campi password (se usePassword = true)

**Cause e soluzioni:**
1. Verifica che `dashboard_config.toml` si trovi nella directory `dashboard/`
2. Verifica che le sezioni `[[login.oidc]]` siano presenti con la sintassi corretta
3. Riavvia il servizio della dashboard
4. Pulisci la cache del browser (Ctrl+Shift+Delete o Cmd+Shift+Delete)
5. Controlla la console del browser (F12 → scheda Console) per errori

---

### Errore di mismatch del Redirect URI

**Sintomi:**
- Dopo aver cliccato il pulsante SSO, errore su "redirect_uri mismatch"
- Errore "The redirect URI is not registered"

**Cause e soluzioni:**
1. Verifica che `DIGNA_OIDC_REDIRECT_URI` in `config.toml` sia corretto
2. Verifica che il redirect URI sia registrato nelle impostazioni del provider di identità
3. Assicurati che entrambi usino URL identici (inclusi protocollo, dominio, path)
4. Controlla eventuali errori di battitura nel redirect URI
5. Se usi HTTPS, assicurati che il certificato sia valido

---

### Errore credenziali client non valide

**Sintomi:**
- Errore "Invalid client ID or secret"
- Autenticazione fallisce per errore di credenziali

**Cause e soluzioni:**
1. Verifica che `DIGNA_OIDC_CLIENT_ID` e `DIGNA_OIDC_CLIENT_SECRET` siano corretti
2. Assicurati che non ci siano spazi extra o caratteri speciali
3. Controlla che le credenziali non siano scadute o revocate
4. Riavvia il servizio backend dopo l'aggiornamento della config
5. Controlla la console del provider di identità per confermare che le credenziali siano attive

---

### Login bloccato o in timeout

**Sintomi:**
- Cliccando sul pulsante SSO non succede nulla
- Timeout dopo alcuni secondi
- Il browser mostra "Failed to connect" o simile

**Cause e soluzioni:**
1. Verifica che il backend digna sia in esecuzione: `digna repo check`
2. Controlla la connettività di rete verso il provider di identità
3. Verifica che `DIGNA_OIDC_CONFIGURATION_URL` sia accessibile
4. Controlla le regole del firewall che permettono connessioni HTTPS in uscita
5. Verifica che backend e dashboard possano raggiungersi reciprocamente

---

### Utenti non creati automaticamente

**Sintomi:**
- Il login SSO ha successo ma l'utente non viene creato in digna
- Si ottiene un errore di autorizzazione dopo il login SSO

**Cause e soluzioni:**
1. Verifica che la configurazione OIDC sia corretta
2. Controlla che i permessi utente siano configurati correttamente
3. Rivedi i log di digna per messaggi di errore
4. Riavvia il servizio backend
5. Contatta support@digna.ai se il problema persiste

---

## Provider supportati {: #supported-providers }

### Testati e supportati

I seguenti provider OIDC sono stati testati e sono noti per funzionare:

| Provider | Configuration URL | Guida alla configurazione |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Altri provider OIDC

Qualsiasi provider che supporti OpenID Connect può essere integrato. Informazioni richieste:

- Client ID
- Client secret
- URL di configurazione OpenID (di solito in `/.well-known/openid-configuration`)
- Scopes supportati (tipicamente `openid profile email`)

Contatta support@digna.ai se hai bisogno di aiuto per integrare un provider specifico.

---

## Best Practices

✅ FARE:
- Usa HTTPS in produzione (non HTTP)
- Conserva i client secret in modo sicuro (usa variabili d'ambiente se possibile)
- Ruota i secret periodicamente
- Testa prima in un ambiente non di produzione
- Documenta quali provider sono configurati
- Monitora i log di accesso per attività sospette
- Mantieni la configurazione del provider di identità in sincronizzazione con la config di digna

❌ NON FARE:
- Conservare i client secret nel controllo di versione
- Usare redirect URI HTTP in produzione
- Configurare più provider con la stessa key
- Lasciare credenziali di default/test in produzione
- Esporre file di configurazione contenenti secret
- Mescolare credenziali di sviluppo e produzione

---

## Supporto

Hai bisogno di aiuto con la configurazione SSO?

- 📧 **Email:** support@digna.ai
- 📚 **Documentazione:** https://docs.digna.ai
- 🌐 **Sito web:** https://www.digna.ai

---

**Ultimo aggiornamento:** 30 agosto 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**

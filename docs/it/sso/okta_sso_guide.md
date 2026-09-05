---
title: Okta SSO – Integrazione Single Sign-On | Documentazione digna
description: Configura Single Sign-On per digna con Okta usando OpenID Connect — integrazione dell'app, redirect URI di accesso, credenziali client, scelta del server di autorizzazione e la corrispondente configurazione di digna.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, integrazione app, server autorizzazione, openid connect, autenticazione aziendale
---

# Configurare SSO con Okta

Okta è compatibile con OIDC, con però una particolarità che sorprende la maggior parte delle integrazioni fatte la prima volta: un'organizzazione Okta espone più server di autorizzazione, ognuno con la propria URL di discovery.

Questa guida copre il **lato Okta**: creare l'integrazione dell'app e raccogliere i valori di cui digna ha bisogno. Il lato digna — `dashboard_config.toml`, test e risoluzione dei problemi — è lo stesso per ogni provider ed è descritto nella [Panoramica Single Sign-On](overview.md).

---

## Prima di Iniziare

| Requisito | Note |
|---|---|
| **Ruolo Okta** | Super Administrator, o un ruolo amministrativo autorizzato a creare integrazioni di app |
| **Dominio Okta** | es. `yourcompany.okta.com`, o un dominio personalizzato se configurato |
| **digna redirect URI** | L'URL a cui gli utenti ritornano dopo il login, es. `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Creare l'integrazione dell'app

1. Accedi alla Okta Admin Console
2. Vai su **Applications → Applications**
3. Clicca **Create App Integration**
4. Seleziona:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Clicca **Next**

!!! warning "Il tipo di applicazione non può essere modificato"

    Scegliere *Single-Page Application* invece di *Web Application* crea un client pubblico senza secret, e lo scambio codice-segreto del backend di digna fallirà con `invalid_client`. Il tipo è fissato al momento della creazione — una scelta errata significa eliminare l'app e ricominciare da capo.

---

## Passo 2: Configurare l'integrazione

1. **Nome integrazione app**: `digna`
2. **Grant type**: lascia selezionato *Authorization Code*
3. **Sign-in redirect URIs**: inserisci il tuo URL di callback digna:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: facoltativo
5. Sotto **Assignments**, scegli chi può usare l'integrazione — un gruppo specifico è più sicuro di *Allow everyone in your organization to access*
6. Clicca **Save**

!!! note "È richiesta l'assegnazione"

    Okta autentica l'utente e poi verifica se è assegnato all'applicazione. Un utente non assegnato arriva alla pagina di login Okta, effettua l'accesso correttamente e viene poi rifiutato al redirect di ritorno. Se il login funziona per te ma non per i colleghi, l'assegnazione è la prima cosa da verificare.

---

## Passo 3: Raccogliere le credenziali

Nella scheda **General** dell'applicazione, sotto **Client Credentials**:

- **Client ID** → diventa `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → diventa `DIGNA_OIDC_CLIENT_SECRET` (clicca l'icona a occhio per rivelarlo)

---

## Passo 4: Scegliere il server di autorizzazione

Questo è il passo che determina la tua URL di discovery. Vai su **Security → API** per vedere i server di autorizzazione nella tua org.

**Org authorization server** — emette token per l'intera org Okta:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — incluso quello che Okta crea chiamato `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Per il server integrato, `<auth_server_id>` è letteralmente `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Quale scegliere?"

    Usa il server di autorizzazione **org** a meno che la tua organizzazione non standardizzi già su uno custom per le policy di accesso API. Gli account Okta Developer usano `default` di default; molte org enterprise lo disabilitano. Apri entrambe le URL in un browser — quella che restituisce JSON anziché un errore è quella disponibile per te.

---

## Passo 5: Configurare digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

La `key` in entrambi i file deve corrispondere — `okta` in questo esempio.

---

## Passo 6: Test

Riavvia il backend e il web server, poi apri la dashboard. Vedi [Test di accesso](overview.md#testing-login) per la checklist completa.

---

## Risoluzione dei problemi Okta

### La redirect URI non è registrata

Okta indica nella segnalazione l'URI incriminata. Confrontala con **General → Sign-in redirect URIs**; Okta confronta l'intera stringa inclusa qualsiasi slash finale.

### L'utente non è assegnato all'applicazione client

L'account non è nella lista di assegnazione dell'applicazione. Aggiungi l'utente o il suo gruppo sotto **Assignments**.

### 400 Bad Request: Invalid Authorization Server

L'`<auth_server_id>` nell'URL di discovery non esiste, più spesso `default` su una org dove è stato rimosso. Controlla **Security → API** per i server effettivamente disponibili.

### invalid_client al passo del Token

L'integrazione è stata creata come Single-Page Application e non ha client secret. Ricreala come Web Application.

---

## Vedi anche

- [Panoramica Single Sign-On](overview.md) — riferimento di configurazione, test e risoluzione generale dei problemi
- [Okta: OpenID Connect e OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
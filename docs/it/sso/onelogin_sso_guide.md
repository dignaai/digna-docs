---
title: OneLogin SSO – Integrazione Single Sign-On | Documentazione digna
description: Configura il Single Sign-On per digna con OneLogin usando OpenID Connect — creazione dell'app OIDC, redirect URI, credenziali client, autenticazione del token endpoint e la corrispondente configurazione di digna.
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, autenticazione del token endpoint, autenticazione aziendale
---

# Configura SSO con OneLogin

OneLogin è compatibile con OIDC. La sua caratteristica distintiva è che il tipo di connettore viene scelto da un catalogo quando l'app viene creata e non può essere modificato successivamente.

Questa guida copre il **lato OneLogin**: la creazione dell'applicazione e la raccolta dei valori di cui digna ha bisogno. Il lato digna — `dashboard_config.toml`, test e risoluzione dei problemi — è lo stesso per ogni provider ed è descritto nella [Panoramica Single Sign-On](overview.md).

---

## Prima di Iniziare

| Requisito | Note |
|---|---|
| **Ruolo OneLogin** | Proprietario dell'account o amministratore autorizzato ad aggiungere applicazioni |
| **Sottodominio** | es. `yourcompany.onelogin.com` |
| **digna redirect URI** | L'URL di ritorno dopo il login, es. `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Crea l'Applicazione OIDC

1. Accedi al portale Admin di OneLogin
2. Vai su **Applications → Applications**
3. Clicca **Add App**
4. Cerca `OpenId Connect` e seleziona il connettore **OpenId Connect (OIDC)**
5. Imposta il **Display Name** su `digna`
6. Clicca **Save**

!!! warning "Il tipo di connettore è fisso alla creazione"

    OneLogin ha voci del catalogo separate per SAML e OIDC, e un'applicazione non può essere convertita da una all'altra. Se scegli per errore un connettore SAML, elimina l'app e aggiungila di nuovo — non esiste un'impostazione per cambiare protocollo.

---

## Passo 2: Configura il Redirect URI

1. Apri la scheda **Configuration**
2. In **Redirect URI's**, inserisci il tuo URL di callback di digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Facoltativamente imposta **Post Logout Redirect URIs** sul tuo URL della dashboard
4. Clicca **Save**

!!! note "Un URI per riga"

    Diversamente dai provider che si aspettano una lista separata da virgole, il campo **Redirect URI's** di OneLogin accetta un URI per riga.

---

## Passo 3: Imposta il Tipo di Applicazione e il Metodo di Autenticazione

1. Apri la scheda **SSO**
2. Conferma che **Application Type** sia *Web*
3. Imposta **Token Endpoint → Authentication Method** su *POST* (`client_secret_post`) o *Basic* (`client_secret_basic`)

!!! warning "Non scegliere 'None'"

    Impostare il metodo di autenticazione su *None* rende l'applicazione un client pubblico senza secret, e lo scambio del codice sul backend di digna verrà rifiutato. Sia POST che Basic funzionano.

---

## Passo 4: Raccogli le Credenziali

Sempre nella scheda **SSO**:

- **Client ID** → diventa `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → diventa `DIGNA_OIDC_CLIENT_SECRET` (clicca **Show client secret**)

La pagina mostra anche l'**Issuer URL**, che conferma l'URL di discovery nel passaggio successivo.

---

## Passo 5: Assegna gli Utenti

1. Apri la scheda **Access**
2. Aggiungi i ruoli o i gruppi i cui membri possono usare digna
3. Clicca **Save**

!!! note "Gli utenti non assegnati vengono rifiutati dopo l'accesso"

    Come per la maggior parte dei provider, OneLogin autentica prima l'utente e verifica l'appartenenza dopo. Un utente non assegnato effettua il login con successo e viene poi rifiutato, il che appare come un errore di digna invece che come una decisione di controllo accessi.

---

## Passo 6: Costruisci l'URL di Discovery

Sostituisci il tuo sottodominio OneLogin:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Per esempio:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "Il /2 è la versione dell'API"

    L'implementazione OIDC corrente di OneLogin risiede sotto `/oidc/2/`. Documentazione più vecchia mostra `/oidc/` senza versione, che punta alla prima versione ritirata. Controlla l'**Issuer URL** nella scheda SSO se hai dubbi — l'URL di discovery è l'issuer più `/.well-known/openid-configuration`.

---

## Passo 7: Configura digna

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
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

La `key` in entrambi i file deve corrispondere — `onelogin` in questo esempio.

---

## Passo 8: Test

Riavvia il backend e il web server, poi apri la dashboard. Vedi [Panoramica Single Sign-On](overview.md#testing-login) per la checklist completa.

---

## Risoluzione dei Problemi OneLogin

### redirect_uri did not match

L'URL di callback è assente in **Configuration → Redirect URI's**, oppure le voci sono state separate da virgole anziché da nuove righe.

### invalid_client at the Token Step

**Token Endpoint → Authentication Method** è impostato su *None*, oppure il client secret in `config.toml` è obsoleto. Mostra il secret nella scheda **SSO** e confrontalo.

### L'app non appare per gli utenti

Nessun ruolo o gruppo ha avuto accesso concesso nella scheda **Access**.

### 404 sull'URL di Discovery

Il sottodominio è errato, oppure l'URL omette `/oidc/2/`. Confrontalo con l'**Issuer URL** mostrato nella scheda SSO.

---

## Vedi anche

- [Panoramica Single Sign-On](overview.md) — riferimento configurazione, test e risoluzione generale dei problemi
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)
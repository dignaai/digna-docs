---
title: Keycloak SSO – Integrazione Single Sign-On | Documentazione digna
description: Configura il Single Sign-On per digna con Keycloak usando OpenID Connect — configurazione del realm e del client, autenticazione del client, URI di redirect validi, client secret e la corrispondente configurazione di digna.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, client confidenziale, openid connect, fornitore di identità self-hosted
---

# Configurare SSO con Keycloak

Keycloak è un identity provider self-hosted, pienamente compatibile con OIDC. Poiché lo gestisci tu, l'URL di discovery è costruita dal tuo nome host e dal tuo realm, anziché da un dominio di terze parti.

Questa guida copre il **lato Keycloak**: creazione del client e raccolta dei valori necessari a digna. Il lato digna — `dashboard_config.toml`, test e risoluzione dei problemi — è identico per ogni provider ed è descritto nella [Panoramica Single Sign-On](overview.md).

---

## Prima di iniziare

| Requisito | Note |
|---|---|
| **Versione di Keycloak** | 17 o successiva per i percorsi URL usati qui — vedi la nota al Passo 4 |
| **Ruolo Keycloak** | `realm-admin` sul realm target, o un amministratore del server |
| **Realm** | Il realm a cui appartengono gli utenti di digna, non necessariamente `master` |
| **digna redirect URI** | L'URL a cui gli utenti tornano dopo il login, es. `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Seleziona il realm

1. Apri la console di amministrazione di Keycloak
2. Usa il selettore del realm in alto a sinistra per passare al realm in cui si trovano i tuoi utenti

!!! warning "Non usare il realm master"

    Il realm `master` è pensato per amministrare lo stesso Keycloak. I client delle applicazioni devono appartenere a un realm dedicato; mettere digna in `master` dà ai suoi utenti una via d'accesso alla console di amministrazione di Keycloak.

---

## Passo 2: Crea il client

1. Vai su **Clients** e clicca **Create client**
2. Configura:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — questo diventerà `DIGNA_OIDC_CLIENT_ID`
3. Clicca **Next**
4. Nella schermata **Capability config**, attiva **Client authentication** **On**
5. Lascia abilitato **Standard flow**; gli altri flow non sono necessari
6. Clicca **Next**

!!! warning "L'autenticazione del client deve essere attiva"

    Con **Client authentication** disattivata, Keycloak crea un client *public*, che non ha credenziali — la scheda **Credentials** nello Step 4 non esisterà. digna richiede un client confidenziale. Questo interruttore può essere modificato dopo la creazione se lo imposti in modo errato.

---

## Passo 3: Imposta l'URI di redirect

Nella schermata **Login settings** (o nella scheda **Settings** successivamente):

1. **Valid redirect URIs**: inserisci l'URL di callback di digna:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: lascia vuoto, oppure imposta `+` per rispecchiare gli URI di redirect
3. Fai clic su **Save**

!!! tip "Evita i caratteri jolly"

    Keycloak accetta pattern come `https://digna.yourdomain.com/*`. Un carattere jolly permette a qualsiasi percorso su quell'host di ricevere un authorization code, quindi preferisci l'URL di callback esatto.

---

## Passo 4: Recupera il secret del client

1. Apri la scheda **Credentials**
2. Conferma che **Client Authenticator** sia *Client Id and Secret*
3. Copia il **Client secret** → diventa `DIGNA_OIDC_CLIENT_SECRET`

Il secret resta recuperabile qui e può essere rigenerato con **Regenerate**.

---

## Passo 5: Costruisci l'URL di discovery

Sostituisci il tuo host Keycloak e il nome del realm:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Per esempio:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 e versioni precedenti includono /auth"

    Prima di Keycloak 17, ogni endpoint era sotto il prefisso `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Le distribuzioni che impostano `KC_HTTP_RELATIVE_PATH=/auth` mantengono la vecchia disposizione anche nelle versioni correnti. Se l'URL senza `/auth` restituisce 404, provane uno con.

Apri l'URL in un browser prima di proseguire. Un documento JSON confermerà che host e realm sono corretti.

---

## Passo 6: Configura digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Accedi con Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

La `key` in entrambi i file deve corrispondere — `keycloak` qui. Nota che non deve necessariamente essere uguale al **Client ID** di Keycloak, anche se mantenerli identici è più semplice da seguire.

---

## Passo 7: Test

Riavvia il backend e il web server, quindi apri la dashboard. Vedi [Testare l'accesso](overview.md#testing-login) per la checklist completa.

---

## Risoluzione dei problemi con Keycloak

### Parametro non valido: redirect_uri

L'URL di callback non è coperto da **Valid redirect URIs**. Keycloak registra l'URI ricevuto nel log del server, che è il modo più rapido per vedere l'esatta discrepanza.

### La scheda Credentials è assente

Il client è pubblico. Attiva **Client authentication** sotto **Settings → Capability config**.

### 404 sull'URL di discovery

O il nome del realm è errato, oppure la distribuzione usa il prefisso `/auth`. Controlla la lista dei realm nella console di amministrazione e prova entrambe le forme di URL.

### unauthorized_client o invalid_client

Il **Standard flow** è disabilitato sotto **Capability config**, oppure il secret è stato rigenerato in Keycloak senza aggiornare `config.toml`.

### Errori di certificato dal backend

Un Keycloak self-hosted dietro un certificato privato o self-signed fallirà la chiamata HTTPS in uscita del backend di digna all'URL di discovery. Installa la CA che ha emesso il certificato nello store di trust della macchina che esegue il backend di digna.

---

## Vedi anche

- [Panoramica Single Sign-On](overview.md) — riferimento alla configurazione, test e risoluzione generale dei problemi
- [Keycloak: Protezione delle applicazioni](https://www.keycloak.org/docs/latest/securing_apps/)
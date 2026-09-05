---
title: SSO AD FS – Integrazione Single Sign-On | digna Documentazione
description: Configurare il Single Sign-On per digna con Active Directory Federation Services usando OpenID Connect — application group, server application, shared secret, scope consentiti e la corrispondente configurazione di digna.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, Active Directory Federation Services, adfs oidc, application group, OpenID Connect, provider di identità on-premises
---

# Configurare SSO con AD FS

Active Directory Federation Services è l'opzione on-premises: i tuoi server emettono i token e l'URL di discovery è il tuo nome host. AD FS supporta OpenID Connect a partire da **Windows Server 2016**.

Questa guida copre il **lato AD FS**: creare l'application group e raccogliere i valori necessari a digna. Il lato digna — `dashboard_config.toml`, test e risoluzione dei problemi — è lo stesso per tutti i provider ed è descritto nella [Panoramica del Single Sign-On](overview.md).

---

## Prima di Iniziare

| Requisito | Note |
|---|---|
| **Versione AD FS** | Windows Server 2016 o successivo — le versioni precedenti non supportano OIDC |
| **Accesso** | Amministratore locale sul server AD FS |
| **Nome del federation service** | es. `adfs.yourdomain.com` |
| **URI di redirect per digna** | L'URL a cui gli utenti tornano dopo il login, es. `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Creare l'Application Group

1. Sul server AD FS, apri **AD FS Management**
2. Clic destro su **Application Groups** e scegli **Add Application Group**
3. Inserisci `digna` come nome
4. Sotto **Standalone applications** — o **Client-Server applications** a seconda della versione — seleziona **Server application accessing a web API**
5. Clicca **Next**

---

## Passo 2: Configurare il Server Application

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS genera un GUID. Copialo — questo diventerà `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: inserisci il tuo URL di callback di digna e clicca **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Clicca **Next**

!!! warning "Premi Aggiungi, non solo Avanti"

    Il campo redirect URI ha un proprio pulsante **Add**. Digitare un URI e cliccare **Next** senza premere **Add** lo scarta, e la procedura guidata non avvisa. Verifica che l'URI appaia nella lista sotto il campo prima di proseguire.

---

## Passo 3: Generare il Shared Secret

1. Seleziona **Generate a shared secret**
2. Copia il segreto generato → diventerà `DIGNA_OIDC_CLIENT_SECRET`
3. Clicca **Next**

!!! warning "Il segreto viene mostrato una sola volta"

    AD FS mostra il shared secret solo in questa pagina della procedura guidata e non può mostrarlo di nuovo. Se lo perdi, rigeneralo in seguito dalle proprietà dell'application group.

---

## Passo 4: Configurare la Web API

1. **Identifier**: inserisci lo stesso client identifier del Passo 2 e clicca **Add**
2. Clicca **Next**
3. Scegli una **Access Control Policy** — *Permit everyone* è il punto di partenza più semplice; limitarla a un gruppo è raccomandato per la produzione
4. Clicca **Next**

---

## Passo 5: Concedere gli Scope Consentiti

Nella fase **Configure Application Permissions**, seleziona:

- `openid`
- `profile`
- `email`

Poi clicca **Next** e completa la procedura guidata.

!!! warning "openid non è selezionato di default"

    AD FS in alcune versioni pre-seleziona solo `user_impersonation`. Senza `openid`, l'endpoint token restituisce un access token OAuth invece di un ID token, e digna non può identificare l'utente.

---

## Passo 6: Confermare l'Endpoint di Discovery

Sostituisci il nome del tuo federation service:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Per esempio:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Aprilo in un browser. Un documento JSON conferma che OIDC è abilitato e che il nome host è corretto.

!!! note "Il backend deve fidarsi del certificato"

    Un'autorità di certificazione interna è comune per AD FS. La macchina che esegue il backend di digna effettua una propria chiamata HTTPS outbound a questo URL, quindi la CA emittente deve essere presente nel trust store di quella macchina — non solo nei browser degli utenti che fanno il login.

---

## Passo 7: Configurare digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Accedi con Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

La `key` in entrambi i file deve corrispondere — `adfs` in questo esempio.

---

## Passo 8: Test

Riavvia il backend e il web server, poi apri la dashboard. Vedi [Test di accesso](overview.md#testing-login) per la checklist completa.

---

## Risoluzione dei problemi di AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

L'identificatore della web API nel Passo 4 non corrisponde al client identifier, oppure gli scope nel Passo 5 non sono stati concessi. Entrambi sono modificabili dalle proprietà dell'application group.

### MSIS9602: Invalid redirect_uri

L'URI è stato digitato ma non aggiunto con il pulsante **Add**, oppure differisce da `DIGNA_OIDC_REDIRECT_URI`. Controlla **Application Groups → digna → digna backend → Properties**.

### Nessun ID Token viene restituito

Manca lo scope `openid` tra i permessi dell'applicazione.

### Il backend non riesce a raggiungere l'URL di discovery

O DNS sull'host del backend non risolve il nome del federation service, oppure il certificato AD FS non è attendibile lì. Testa con `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` dal server di digna stesso.

### Eventi da controllare

Il server AD FS registra i fallimenti in **Applications and Services Logs → AD FS → Admin** in Event Viewer, normalmente con una motivazione più specifica rispetto a quella mostrata dal browser.

---

## Vedi anche

- [Panoramica del Single Sign-On](overview.md) — riferimento alla configurazione, test e risoluzione generale dei problemi
- [Microsoft: Scenari OpenID Connect di AD FS](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
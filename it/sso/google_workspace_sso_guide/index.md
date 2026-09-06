# Configurare SSO con Google Workspace

La piattaforma di identità di Google è conforme a OIDC e utilizza un singolo URL di discovery ben noto per ogni cliente, quindi gli unici valori specifici per organizzazione sono il client ID e il secret.

Questa guida copre il **lato Google**: creare il client OAuth e raccogliere i valori di cui digna ha bisogno. Il lato digna — `dashboard_config.toml`, testing e troubleshooting — è lo stesso per ogni provider ed è descritto nella [Panoramica Single Sign-On](overview.md).

---

## Prima di Iniziare

| Requisito | Note |
|---|---|
| **Progetto Google Cloud** | Qualsiasi progetto nella stessa organizzazione del dominio Workspace |
| **Ruolo** | Editor o Proprietario sul progetto |
| **URI di reindirizzamento di digna** | L'URL a cui gli utenti ritornano dopo il login, es. `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Configurare la Schermata di Consenso OAuth

Google non emetterà credenziali finché la schermata di consenso non esiste.

1. Apri la [Console Google Cloud](https://console.cloud.google.com) e seleziona il tuo progetto
2. Vai a **APIs & Services → OAuth consent screen**
3. Scegli il tipo di utente:
   - **Internal** — solo gli account nel tuo dominio Workspace possono accedere. Raccomandato.
   - **External** — qualsiasi account Google può tentare di accedere.
4. Compila il nome dell'app, l'email di supporto per gli utenti e l'email di contatto dello sviluppatore
5. Nella sezione **Scopes**, aggiungi `openid`, `.../auth/userinfo.email` e `.../auth/userinfo.profile`
6. Salva

!!! warning "Le app esterne devono essere pubblicate"

    Una schermata di consenso **External** inizia in stato *Testing*, in cui solo gli account aggiunti esplicitamente alla lista di test-user possono completare il login. Tutti gli altri vedono "digna has not completed the Google verification process". Occorre o passare l'app a **In production** sotto **Publishing status**, oppure usare **Internal** — che non ha questa restrizione ed è la scelta corretta per una distribuzione solo Workspace.

---

## Passo 2: Creare il Client OAuth

1. Vai a **APIs & Services → Credentials**
2. Clicca **Create Credentials → OAuth client ID**
3. Imposta **Application type** su **Web application**
4. Assegna un nome, es. `digna`
5. Sotto **Authorized redirect URIs**, clicca **Add URI** e inserisci:

```
https://digna.yourdomain.com/oidc/callback
```

6. Clicca **Create**

!!! note "Origini JavaScript autorizzate non sono necessarie"

    digna scambia il codice di autorizzazione dal backend, non dal browser, quindi il campo **Authorized JavaScript origins** può essere lasciato vuoto. Conta solo il redirect URI.

---

## Passo 3: Raccogliere le Credenziali

La finestra che appare dopo la creazione mostra:

- **Client ID** — termina con `.apps.googleusercontent.com` → diventa `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → diventa `DIGNA_OIDC_CLIENT_SECRET`

Entrambi restano recuperabili in seguito dalla pagina di dettaglio delle credenziali, a differenza della maggior parte degli altri provider.

---

## Passo 4: L'URL di Discovery

Google usa un unico URL di discovery per tutti i clienti — non c'è nulla da sostituire:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Passo 5: Configurare digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

La `key` in entrambi i file deve corrispondere — `google` in questo esempio.

---

## Passo 6: Test

Riavvia il backend e il web server, poi apri la dashboard. Vedi [Testing Login](overview.md#testing-login) per la checklist completa.

---

## Risoluzione dei problemi con Google Workspace

### Errore 400: redirect_uri_mismatch

L'URI in `DIGNA_OIDC_REDIRECT_URI` non è nella lista degli **Authorized redirect URIs**, o differisce per uno slash finale o per lo schema. La pagina di errore di Google mostra l'URI che ha ricevuto — confrontalo carattere per carattere con quello registrato.

### This App Is Blocked / Has Not Completed Verification

La schermata di consenso è **External** ed è ancora in *Testing*. Pubblica l'app, oppure passa l'app a **Internal**.

### Access Blocked: Authorization Error

L'account che tenta di accedere è esterno al tuo dominio Workspace mentre la schermata di consenso è **Internal**. Questo è il comportamento voluto — le app Internal accettano solo account dell'organizzazione.

### Le modifiche richiedono alcuni minuti

Google propaga le modifiche a credenziali e schermata di consenso in modo asincrono. Un redirect URI appena aggiunto può impiegare alcuni minuti prima di avere effetto; se una modifica sembra ignorata, aspetta e riprova prima di approfondire.

---

## Vedi anche

- [Panoramica Single Sign-On](overview.md) — riferimento di configurazione, testing e risoluzione dei problemi in generale
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
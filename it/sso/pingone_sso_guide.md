# Configura SSO con PingOne

PingOne è compatibile con OIDC. Due dei suoi valori richiedono attenzione: l'**Environment ID**, che compare in ogni URL endpoint, e il **dominio regionale**, che differisce tra i tenant Nord America, Europa, Canada, Asia-Pacifico e Australia.

Questa guida copre il **lato PingOne**: creare l'applicazione e raccogliere i valori di cui digna ha bisogno. Il lato digna — `dashboard_config.toml`, test e risoluzione dei problemi — è lo stesso per ogni provider ed è descritto nella [Panoramica Single Sign-On](overview.md).

---

## Prima di iniziare

| Requisito | Note |
|---|---|
| **Ruolo PingOne** | Environment Admin o Identity Data Admin sull'ambiente target |
| **Ambiente** | L'ambiente PingOne a cui appartengono gli utenti digna |
| **digna redirect URI** | L'URL a cui gli utenti tornano dopo il login, es. `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Crea l'applicazione

1. Accedi alla console admin di PingOne e seleziona il tuo ambiente
2. Vai su **Applications → Applications**
3. Clicca il pulsante **+**
4. Inserisci `digna` come **Application Name**
5. Seleziona **OIDC Web App**
6. Clicca **Save**

!!! warning "Scegli OIDC Web App, non Single-Page App"

    *Single-Page App* e *Native App* creano client pubblici che non possono contenere un secret. digna scambia il codice di autorizzazione dal backend e necessita del tipo confidenziale **OIDC Web App**.

---

## Passo 2: Configura il Redirect URI

1. Apri la scheda **Configuration** dell'applicazione
2. Clicca l'icona a matita per modificare
3. Conferma che **Response Type** sia *Code* e **Grant Type** sia *Authorization Code*
4. Sotto **Redirect URIs**, inserisci il tuo URL di callback per digna:

```
https://digna.yourdomain.com/oidc/callback
```

5. Imposta **Token Endpoint Authentication Method** su *Client Secret Post* o *Client Secret Basic*
6. Clicca **Save**

---

## Passo 3: Abilita l'applicazione

Nella riga dell'applicazione o nel pannello dei dettagli, attiva l'interruttore su **enabled**.

!!! warning "Le nuove applicazioni partono disabilitate"

    PingOne crea le applicazioni in stato disabilitato. Un'applicazione disabilitata produce un errore nella fase di autorizzazione che non menziona l'interruttore, quindi vale la pena confermare questo prima di indagare altro.

---

## Passo 4: Concedi gli scope

1. Apri la scheda **Resources**
2. Conferma che `openid` sia concesso, e aggiungi `profile` ed `email` dalla risorsa **OpenID Connect**
3. Clicca **Save**

---

## Passo 5: Assegna gli utenti

1. Apri la scheda **Access**
2. Aggiungi la popolazione o i gruppi i cui membri possono usare digna
3. Clicca **Save**

---

## Passo 6: Raccogli le credenziali e l'ID dell'ambiente

Nella scheda **Configuration**, espandi **General**:

- **Client ID** → diventa `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → diventa `DIGNA_OIDC_CLIENT_SECRET` (clicca l'icona dell'occhio)
- **Environment ID** → va nell'URL di discovery

La stessa scheda elenca l'**OIDC Discovery Endpoint** pronto all'uso, che puoi copiare direttamente invece di assemblarlo manualmente.

---

## Passo 7: Costruisci l'URL di discovery

Sostituisci l'environment ID e il dominio per la tua regione:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Regione | Dominio |
|---|---|
| North America | `auth.pingone.com` |
| Europe | `auth.pingone.eu` |
| Canada | `auth.pingone.ca` |
| Asia-Pacific | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

Per un ambiente europeo:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Copialo invece di digitarlo"

    Il dominio regionale è l'errore più comune in un'integrazione PingOne, e una regione sbagliata restituisce un 404 invece di un messaggio utile. Usa il valore **OIDC Discovery Endpoint** dal Passo 6.

---

## Passo 8: Configura digna

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
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

La `key` in entrambi i file deve corrispondere — `pingone` in questo esempio.

---

## Passo 9: Verifica

Riavvia il backend e il web server, poi apri la dashboard. Consulta [Testing Login](overview.md#testing-login) per la checklist completa.

---

## Risoluzione dei problemi con PingOne

### 404 sull'URL di discovery

Il dominio regionale o l'environment ID è sbagliato. Confronta con l'**OIDC Discovery Endpoint** mostrato nella scheda Configuration dell'applicazione.

### NOT_FOUND o Applicazione disabilitata

L'interruttore dell'applicazione del Passo 3 è ancora spento.

### Redirect URI non corrispondente

PingOne confronta la stringa completa. Controlla **Configuration → Redirect URIs** per una barra finale o una differenza di scheme.

### Login riuscito ma nessun claim email arriva a digna

Gli scope `email` e `profile` non sono stati concessi nella scheda **Resources**.

### L'utente non vede l'applicazione

Nessuna popolazione o gruppo è stato autorizzato nella scheda **Access**.

---

## Vedi anche

- [Panoramica Single Sign-On](overview.md) — riferimento di configurazione, test e risoluzione generale dei problemi
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)
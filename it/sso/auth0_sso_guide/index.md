# Configurare SSO con Auth0

Auth0 è conforme a OIDC ed espone un endpoint di discovery per ogni tenant. La cosa principale da impostare correttamente è il dominio del tenant, che compare nell'URL di discovery e cambia se abiliti un dominio personalizzato.

Questa guida copre il **lato Auth0**: creare l'applicazione e raccogliere i valori necessari a digna. Il lato digna — `dashboard_config.toml`, test e risoluzione dei problemi — è lo stesso per ogni provider ed è descritto nella [Panoramica Single Sign-On](overview.md).

---

## Prima di Iniziare

| Requisito | Note |
|---|---|
| **Ruolo Auth0** | Admin sul tenant |
| **Dominio del tenant** | es. `yourcompany.eu.auth0.com` — il segmento della regione è importante |
| **URI di redirect di digna** | L'URL a cui gli utenti ritornano dopo il login, es. `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Creare l'Applicazione

1. Accedi al [Dashboard di Auth0](https://manage.auth0.com)
2. Vai su **Applications → Applications**
3. Clicca **Create Application**
4. Nominala `digna` e scegli **Regular Web Applications**
5. Clicca **Create**

!!! warning "Scegliere Regular Web Applications"

    *Single Page Application* e *Native* creano client pubblici senza secret. digna esegue lo scambio del codice dal suo backend e ha bisogno di un client confidenziale, quindi **Regular Web Applications** è il tipo corretto. A differenza di alcuni provider, Auth0 permette di cambiare il tipo in seguito sotto **Settings → Application Type**.

---

## Passo 2: Aggiungere l'URL di Callback

Nella tab **Settings** dell'applicazione:

1. Trova **Allowed Callback URLs**
2. Inserisci il tuo URL di callback per digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Facoltativamente imposta **Allowed Logout URLs** sul tuo URL della dashboard
4. Scorri fino in fondo e clicca **Save Changes**

!!! note "Separati da virgola, non da nuova riga"

    Auth0 accetta diversi callback URL in questo campo, separati da virgole. Una lista separata solo da nuove righe viene letta come un unico URL malformato e non corrisponde silenziosamente a nulla.

---

## Passo 3: Raccogliere le Credenziali

Sempre in **Settings**, nel pannello **Basic Information**:

- **Domain** → va messo nell'URL di discovery
- **Client ID** → diventa `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → diventa `DIGNA_OIDC_CLIENT_SECRET` (clicca per rivelarlo)

---

## Passo 4: Confermare il Grant Type

1. Vai su **Settings → Advanced Settings → Grant Types**
2. Conferma che **Authorization Code** sia selezionato

È abilitato di default per le Regular Web Applications. Se è stato deselezionato, il login di digna fallisce con `unauthorized_client`.

---

## Passo 5: Costruire l'URL di Discovery

Sostituisci il **Domain** raccolto al Passo 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Per esempio:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Custom Domains Change the Issuer"

    Se il tuo tenant usa un dominio personalizzato come `login.yourcompany.com`, usa quel dominio nell'URL di discovery. Mischiare i due — il dominio canonico nell'URL di discovery e quello personalizzato nel browser — provoca un issuer mismatch, e il token viene rifiutato dopo un login altrimenti riuscito.

---

## Passo 6: Configurare digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

La `key` in entrambi i file deve corrispondere — `auth0` qui.

---

## Passo 7: Test

Riavvia il backend e il web server, poi apri la dashboard. Vedi [Test del login](overview.md#testing-login) per la checklist completa.

---

## Risoluzione dei Problemi con Auth0

### Mismatch dell'URL di Callback

La pagina di errore di Auth0 indica l'URL che ha ricevuto. Aggiungilo a **Allowed Callback URLs**, verificando che le voci siano separate da virgole.

### unauthorized_client

**Authorization Code** non è abilitato sotto **Advanced Settings → Grant Types**, oppure il tipo di applicazione non è Regular Web Applications.

### Accesso Negato Dopo un Login Riuscito

Una Rule, Action o un trigger Post-Login nel tenant sta rifiutando l'utente. Controlla **Actions → Flows → Login** e i log del tenant sotto **Monitoring → Logs**, che mostrano la ragione esatta.

### Issuer Mismatch

L'URL di discovery e il dominio a cui il browser è stato inviato differiscono — di solito il dominio canonico del tenant rispetto a un dominio personalizzato. Usa uno dei due in modo coerente.

---

## Vedi Anche

- [Panoramica Single Sign-On](overview.md) — riferimento alla configurazione, test e risoluzione generale dei problemi
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
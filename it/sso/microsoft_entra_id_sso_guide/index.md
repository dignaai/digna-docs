# Configura SSO con Microsoft Entra ID

Microsoft Entra ID (precedentemente Azure Active Directory) è un provider pienamente compatibile OIDC, quindi digna si integra con esso tramite il normale endpoint di discovery.

Questa guida copre il **lato Entra ID**: la registrazione dell'applicazione e la raccolta dei quattro valori di cui digna ha bisogno. Il lato digna — `dashboard_config.toml`, test e risoluzione dei problemi — è lo stesso per ogni provider ed è descritto nella [Single Sign-On Overview](overview.md).

---

## Prima di cominciare

| Requisito | Note |
|---|---|
| **Ruolo in Entra ID** | Application Administrator, Cloud Application Administrator, o Global Administrator |
| **digna redirect URI** | L'URL al quale gli utenti tornano dopo il login, es. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | La directory in cui i tuoi utenti eseguono l'accesso |

---

## Passo 1: Registra l'applicazione

1. Accedi al [Microsoft Entra admin center](https://entra.microsoft.com)
2. Vai su **Identity → Applications → App registrations**
3. Clicca **New registration**
4. Configura:
   - **Name**: `digna` (che verrà mostrato agli utenti nella schermata di consenso)
   - **Supported account types**: *Accounts in this organizational directory only* per una distribuzione single-tenant
5. Sotto **Redirect URI**, seleziona la piattaforma **Web** e inserisci la tua callback URL di digna:

```
https://digna.yourdomain.com/oidc/callback
```

6. Clicca **Register**

!!! warning "Importante"

    La piattaforma deve essere **Web**, non *Single-page application*. digna scambia il codice di autorizzazione dal backend usando un client secret, cosa che il tipo di piattaforma SPA non permette.

---

## Passo 2: Recupera gli ID Client e Tenant

Nella pagina **Overview** dell'applicazione, copia:

- **Application (client) ID** → diventa `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → va inserito nell'URL di discovery

---

## Passo 3: Crea un Client Secret

1. Vai su **Certificates & secrets → Client secrets**
2. Clicca **New client secret**
3. Inserisci una descrizione e scegli una scadenza
4. Clicca **Add**
5. Copia immediatamente il contenuto della colonna **Value**

!!! warning "Copia il Value, non il Secret ID"

    Il **Value** viene mostrato una sola volta, in questa pagina, e non può essere recuperato successivamente. Il **Secret ID** accanto può sembrare simile ma non è il secret — usarlo genera un errore `invalid_client` al login. Se navighi via prima di copiarlo, elimina il secret e creane uno nuovo.

!!! tip "Suggerimento"

    Entra ID limita la durata dei secret a 24 mesi, quindi ogni integrazione SSO ha una data di scadenza. Annotala in un posto visibile — un secret scaduto interrompe l'SSO per tutti gli utenti contemporaneamente, senza avviso nella pagina di login.

---

## Passo 4: Conferma le autorizzazioni API

1. Vai su **API permissions**
2. Conferma che **Microsoft Graph → User.Read** (delegated) sia presente — viene aggiunto di default

Gli scope `openid`, `profile` e `email` che digna richiede fanno parte del set standard OIDC e non necessitano di una concessione separata. Se il tuo tenant richiede il consenso amministrativo per tutte le applicazioni, clicca **Grant admin consent for <tenant>**.

---

## Passo 5: Costruisci l'URL di Discovery

Sostituisci il **Directory (tenant) ID** del Passo 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Usa l'endpoint v2.0"

    Il segmento `/v2.0/` è importante. L'endpoint v1.0 su `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` emette token in un formato più vecchio e non restituisce le claim OIDC standard che digna si aspetta.

Apri l'URL in un browser prima di proseguire. Un documento JSON confermerà che il tenant ID è corretto.

---

## Passo 6: Configura digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Accedi con Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<il Value copiato nel Passo 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

La `key` in entrambi i file deve corrispondere — qui è `microsoft`.

---

## Passo 7: Test

Riavvia il backend e il server web, poi apri la dashboard. Vedi [Testing Login](overview.md#testing-login) per la checklist completa.

---

## Risoluzione dei problemi Entra ID

### AADSTS50011: Redirect URI Mismatch

L'URI in `DIGNA_OIDC_REDIRECT_URI` differisce da quello registrato al Passo 1. Entra ID confronta l'intera stringa, quindi uno slash finale, `http` vs `https` o una porta diversa contano come mismatch. Controlla **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

O è stato copiato il **Secret ID** invece del **Value**, oppure il secret è scaduto. Crea un nuovo secret e copia il contenuto della colonna Value.

### AADSTS650057: Invalid Resource

La registrazione dell'applicazione è stata eliminata o appartiene a un tenant diverso da quello nell'URL di discovery. Conferma il Directory (tenant) ID nella pagina Overview.

### Gli utenti effettuano l'accesso ma non succede nulla

Se il tenant richiede il consenso amministrativo e questo non è stato concesso, il redirect ritorna senza un token utilizzabile. Concedi il consenso amministrativo sotto **API permissions**.

---

## Vedi anche

- [Single Sign-On Overview](overview.md) — riferimento alla configurazione, testing e risoluzione generale dei problemi
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
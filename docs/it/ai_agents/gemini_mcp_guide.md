---
title: Gemini – Collegare Antigravity e Gemini CLI a digna tramite MCP | Documentazione digna
description: Collega gli strumenti Gemini di Google a digna tramite il digna MCP Server — Antigravity CLI, IDE e app con mcp_config.json, e Gemini CLI con settings.json o gemini mcp add, con una chiave API nell'header Authorization.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, chiave API digna
---

# Collegare Gemini a digna

Questa guida collega gli strumenti Gemini di Google al **digna MCP Server**. Ti servono l'endpoint
MCP della tua installazione di *digna* e una chiave API, come descritto nella
[Panoramica degli agenti IA](overview.md).

Gli esempi usano `https://digna.example.com/mcp` come endpoint. Sostituiscilo con il tuo.

## Scegliere lo strumento {: #choose-your-tool }

| Strumento | Per | Configurazione |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE e app | Gli strumenti per agenti di Google. Antigravity CLI ha sostituito Gemini CLI per gli account Google personali a giugno 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Licenze Gemini Code Assist Standard ed Enterprise, e chiavi API Gemini a pagamento | `settings.json` o `gemini mcp add` |
| App Gemini Enterprise | — | Non supportata. Il suo connettore MCP personalizzato accede con OAuth o con un service account di Google Cloud, mentre il digna MCP Server si autentica con chiavi API |

Tutti questi strumenti si collegano dalla macchina su cui girano, quindi funzionano con *digna*
all'interno della rete aziendale, purché quella macchina raggiunga l'endpoint.

---

## Antigravity {: #antigravity }

Antigravity legge i suoi server MCP da `mcp_config.json`, condiviso da CLI, IDE e app.

### 1. Aprire mcp_config.json {: #1-open-mcp-config-json }

| Ambito | File |
|---|---|
| Tutti i tuoi progetti | `~/.gemini/config/mcp_config.json` |
| Un workspace | `.agents/mcp_config.json` nel workspace |

Per aprire il file in uso:

- **CLI**: digita `/mcp` e premi ++enter++ per aprire il gestore MCP.
- **IDE**: nel pannello laterale dell'agente, apri il menu **…**, seleziona **MCP Servers**, poi
  **Manage MCP Servers**, poi **View raw config**.
- **App**: vai su **Customizations** > **Installed** > **MCP Servers** e usa
  **Copy Config File Path**.

### 2. Aggiungere il server digna {: #2-add-the-digna-server }

Aggiungi la voce `digna`. Se il file ha già una sezione `mcpServers`, aggiungila lì:

```json
{
  "mcpServers": {
    "digna": {
      "serverUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

Antigravity raggiunge i server remoti solo tramite HTTP streamable, che è quello usato dal digna MCP
Server. Indica l'endpoint come `serverUrl`; la chiave `httpUrl` di Gemini CLI non è supportata.

### 3. Verificare la connessione {: #3-verify-the-connection }

Nella CLI, digita `/mcp`: il gestore MCP mostra il server `digna` con il suo stato e i suoi
strumenti, e può ricaricare la configurazione e mostrare i log di connessione. Nell'IDE, il server
compare in **Manage MCP Servers**.

!!! warning "Proteggi il file"

    `mcp_config.json` contiene la chiave API in chiaro. Tieni un file di workspace
    `.agents/mcp_config.json` fuori dal controllo di versione, e consenti solo al tuo account di
    leggere il file globale.

---

## Gemini CLI {: #gemini-cli }

### 1. Aggiungere il server {: #1-add-the-server }

Metti la chiave API in una variabile d'ambiente, poi aggiungi il server:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

La tua shell sostituisce `$DIGNA_API_KEY` con il suo valore quando esegui il comando, quindi Gemini
CLI salva la chiave nelle sue impostazioni. Senza `--scope user`, il server viene aggiunto solo al
progetto corrente.

### 2. Oppure modificare settings.json {: #2-or-edit-settings-json }

Il comando qui sopra scrive in `settings.json`. Per modificare il file tu stesso:

| Ambito | File |
|---|---|
| Tutti i tuoi progetti | `~/.gemini/settings.json` |
| Un progetto | `.gemini/settings.json` nel progetto |

```json
{
  "mcpServers": {
    "digna": {
      "httpUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

Usa `httpUrl`, la chiave per l'HTTP streamable. La chiave simile `url` seleziona il trasporto SSE più
vecchio, che il digna MCP Server non offre. Non usare trattini bassi nel nome del server.

!!! tip "Lascia trust disattivato"

    Gemini CLI chiede conferma prima di ogni chiamata a uno strumento, a meno che il server non abbia
    `"trust": true`. Lascia `trust` disattivato per *digna*, così confermi ogni modifica che un
    agente apporta alla tua configurazione.

### 3. Verificare la connessione {: #3-verify-the-connection-gemini-cli }

Dalla tua shell:

```bash
gemini mcp list
```

Il server `digna` deve risultare connesso. All'interno di una sessione di Gemini CLI, esegui `/mcp`
per vedere il server e i suoi strumenti.

---

## Risoluzione dei problemi di Gemini {: #troubleshooting-gemini }

### Il server risulta disconnesso

- Verifica che l'endpoint termini con `/mcp` e sia raggiungibile dalla tua macchina.
- Verifica il nome della chiave: `serverUrl` in Antigravity, `httpUrl` in Gemini CLI.
- Un `401` significa che la chiave è stata rifiutata; vedi
  [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI non si avvia più con il mio account

Da giugno 2026, gli account Google personali usano Antigravity CLI al posto di Gemini CLI. Sposta la
voce `digna` in `mcp_config.json` come descritto in [Antigravity](#antigravity), e rinomina
`httpUrl` in `serverUrl`.

---

## Vedi anche {: #see-also }

- [Panoramica degli agenti IA](overview.md): endpoint, chiave API, sicurezza e risoluzione dei problemi generale
- [Claude](claude_mcp_guide.md): collegare Claude Code, Claude Desktop o un connettore personalizzato
- [digna Agentic](../platform/agentic/Introduction.md): cosa possono fare gli agenti IA con *digna*

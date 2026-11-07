---
title: Claude – Collegare Claude a digna tramite MCP | Documentazione digna
description: Collega Claude a digna tramite il digna MCP Server — Claude Code dalla riga di comando o con un .mcp.json condiviso, Claude Desktop con un bridge locale e connettori personalizzati in claude.ai, con una chiave API nell'header Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, connettore personalizzato claude.ai, digna MCP server, mcp-remote, Authorization Bearer, chiave API digna
---

# Collegare Claude a digna

Questa guida collega Claude al **digna MCP Server**. Ti servono l'endpoint MCP della tua installazione
di *digna* e una chiave API, come descritto nella [Panoramica degli agenti IA](overview.md).

Gli esempi usano `https://digna.example.com/mcp` come endpoint. Sostituiscilo con il tuo.

## Scegliere come collegarsi {: #choose-how-to-connect }

| Prodotto Claude | Si collega da | Funziona con *digna* all'interno della tua rete |
|---|---|---|
| [Claude Code](#claude-code) | La tua macchina | Sì |
| [Claude Desktop con un bridge locale](#claude-desktop-with-a-local-bridge) | La tua macchina | Sì |
| [Connettore personalizzato](#custom-connector) in claude.ai, Claude Desktop e Claude mobile | Il cloud di Anthropic | No. L'endpoint deve essere raggiungibile da Internet |

Per un'installazione di *digna* che gira all'interno della rete aziendale, usa Claude Code o Claude
Desktop con un bridge locale.

---

## Claude Code {: #claude-code }

### 1. Aggiungere il server {: #1-add-the-server }

Metti la chiave API in una variabile d'ambiente, poi aggiungi il server:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

La tua shell sostituisce `$DIGNA_API_KEY` con il suo valore quando esegui il comando, quindi Claude
Code salva la chiave nella propria configurazione.

`--scope` stabilisce dove il server è disponibile:

| Ambito | Disponibile |
|---|---|
| `local` (predefinito) | Per te, solo nel progetto corrente |
| `user` | Per te, in ogni progetto |
| `project` | Per tutti coloro che lavorano al progetto, tramite un file `.mcp.json` nel progetto |

### 2. Condividere il server con il team (facoltativo) {: #2-share-the-server-with-your-team }

Per dare a tutti in un progetto lo stesso server, aggiungi un file `.mcp.json` nella radice del
progetto. Non scrivere la chiave nel file. Claude Code sostituisce `${DIGNA_API_KEY}` con il valore
dell'ambiente di ciascuna persona:

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${DIGNA_API_KEY}"
      }
    }
  }
}
```

Ogni persona imposta `DIGNA_API_KEY` con la propria chiave. La prima volta che Claude Code trova il
file, chiede se usare i server che contiene.

### 3. Verificare la connessione {: #3-verify-the-connection }

Dalla tua shell:

```bash
claude mcp list
```

Il server `digna` deve mostrare `✔ Connected`. All'interno di una sessione di Claude Code, esegui
`/mcp` per vedere il server e i suoi strumenti.

---

## Claude Desktop con un bridge locale {: #claude-desktop-with-a-local-bridge }

Il file di configurazione di Claude Desktop avvia server MCP locali sulla tua macchina. Un piccolo
bridge, il pacchetto open source [`mcp-remote`](https://github.com/geelen/mcp-remote), gira lì e
inoltra ogni richiesta all'endpoint di *digna* con la tua chiave API. Poiché il bridge gira sulla tua
macchina, funziona con *digna* all'interno della rete aziendale.

!!! note "Un pacchetto della community"

    `mcp-remote` è mantenuto dalla sua community open source, non da Anthropic né da digna. Verifica
    che la tua organizzazione ne consenta l'uso prima di utilizzarlo.

### 1. Installare Node.js {: #1-install-nodejs }

Il bridge richiede [Node.js](https://nodejs.org) 18 o successivo. Claude Desktop usa la versione di
Node.js installata sul tuo sistema. Verificala con:

```bash
node --version
```

### 2. Modificare il file di configurazione {: #2-edit-the-configuration-file }

Apri `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Aggiungi il server `digna`. Se il file ha già una sezione `mcpServers`, aggiungi lì la voce `digna`:

```json
{
  "mcpServers": {
    "digna": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://digna.example.com/mcp",
        "--transport",
        "http-only",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer <api key>"
      }
    }
  }
}
```

!!! warning "Scrivi l'header esattamente come mostrato"

    Scrivi `Authorization:${AUTH_HEADER}` senza spazi e metti `Bearer <api key>` in `env`. Claude
    Desktop su Windows non applica l'escape agli spazi all'interno di `args`, quindi uno spazio lì
    rende l'header non valido.

### 3. Riavviare Claude Desktop {: #3-restart-claude-desktop }

Chiudi completamente Claude Desktop e riavvialo. In una nuova chat, clicca **+** e apri
**Connectors**: `digna` deve essere presente nell'elenco e attivato.

---

## Connettore personalizzato {: #custom-connector }

Un connettore personalizzato rende *digna* disponibile in claude.ai, Claude Desktop e nelle app mobili
di Claude senza alcuna configurazione locale. È il cloud di Anthropic a collegarsi all'endpoint,
quindi funziona solo quando:

- L'endpoint di *digna* è raggiungibile da Internet tramite HTTPS
- La tua organizzazione Claude dispone dell'opzione **Request headers** nella finestra di dialogo
  **Add custom connector**. Anthropic la offre in beta a un numero limitato di organizzazioni

!!! warning "Non per digna all'interno della tua rete"

    I tunnel MCP di Claude, che raggiungono server all'interno di una rete privata, richiedono OAuth
    sul server MCP. Il digna MCP Server si autentica con chiavi API, quindi non è possibile usare un
    tunnel. Usa invece [Claude Code](#claude-code) o
    [Claude Desktop con un bridge locale](#claude-desktop-with-a-local-bridge).

### 1. Aprire le impostazioni dei connettori {: #1-open-the-connector-settings }

- **Piani Free, Pro, Max e Ultra**: vai su **Customize > Connectors** e clicca
  **Add custom connector**.
- **Piani Team ed Enterprise**: un Owner va su **Organization settings > Connectors**, clicca
  **Add**, poi **Custom**, e sceglie **Web** se viene chiesto il tipo.

### 2. Inserire i dettagli del connettore {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: scegli `authorization` come nome dell'header, inserisci `Bearer <api key>`
   come valore, compresi la parola `Bearer` e lo spazio, e contrassegnalo come **Required**.
4. Clicca **Add**.

!!! warning "Tutti condividono la chiave"

    Ogni membro che usa il connettore lavora con la stessa chiave API, e quindi con lo stesso utente
    *digna*. Crea un utente *digna* dedicato al connettore e assegnagli solo i progetti e i ruoli che
    tutti possono avere, ad es. il ruolo di lettore.

Nei piani Team ed Enterprise, i membri si collegano poi da **Customize > Connectors**, dove il
connettore riporta l'etichetta **Custom**.

Claude non può modificare l'header di un connettore esistente. Per usare una nuova chiave, rimuovi il
connettore e aggiungilo di nuovo.

---

## Risoluzione dei problemi di Claude {: #troubleshooting-claude }

### claude mcp list mostra Failed to connect

Esegui `claude mcp get digna` per vedere il motivo. Un `401` significa che la chiave è stata
rifiutata; vedi [401 Unauthorized](overview.md#troubleshooting). Claude Code avvisa anche in caso di
spazi o di un a capo all'inizio o alla fine della chiave, che spesso si aggiungono quando la si
copia.

### digna non compare in Claude Desktop

- Verifica che sia installato Node.js 18 o successivo: `node --version`.
- Verifica che `claude_desktop_config.json` sia un JSON valido. Una virgola mancante impedisce il
  caricamento di tutti i server del file.
- Chiudi completamente Claude Desktop, non solo la finestra, e riavvialo.

### Il connettore personalizzato non raggiunge il server

Il cloud di Anthropic non raggiunge l'endpoint. Verifica che sia raggiungibile da Internet tramite
HTTPS con un certificato valido, oppure collegati invece tramite [Claude Code](#claude-code).

---

## Vedi anche {: #see-also }

- [Panoramica degli agenti IA](overview.md): endpoint, chiave API, sicurezza e risoluzione dei problemi generale
- [Gemini](gemini_mcp_guide.md): collegare Antigravity o Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): cosa possono fare gli agenti IA con *digna*

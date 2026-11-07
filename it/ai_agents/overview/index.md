# Collegare agenti IA a digna

Il **digna MCP Server** permette agli agenti IA di lavorare con *digna* tramite il
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), uno standard aperto supportato da
Claude, Gemini e molti altri strumenti di IA. Un agente collegato a *digna* può rispondere a domande
sui tuoi dati, analizzare gli avvisi e aiutare a configurare *digna*. Consulta
[digna Agentic](../platform/agentic/Introduction.md) per scoprire cosa possono fare gli agenti.

Questa pagina tratta il lato *digna*, che è lo stesso per ogni client IA. Le guide dei client
mostrano poi dove inserirlo:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop e connettori personalizzati
- [Gemini](gemini_mcp_guide.md): Antigravity e Gemini CLI

!!! info "Beta"

    digna Agentic, e con esso il digna MCP Server, è distribuito come versione beta nella
    [Release 2026.11](../changelog/Release_202611.md).

---

## Prima di iniziare {: #before-you-start }

Ti servono:

- *digna* Release 2026.11 o successiva
- Una licenza che includa **digna Agentic**. Senza di essa, il server MCP rifiuta ogni richiesta
- Un account utente *digna*. L'agente agisce con i permessi di quell'utente in ogni progetto, vedi
  [Permessi](../platform/agentic/how_it_works.md#permissions)
- Un client IA che si colleghi a server MCP remoti tramite **HTTP streamable** e possa inviare un
  header `Authorization`

---

## 1. Trovare l'endpoint MCP {: #1-find-the-mcp-endpoint }

Il server MCP fa parte del backend di *digna*, quindi non c'è nulla di aggiuntivo da installare o
avviare. Il suo endpoint è l'indirizzo del backend seguito da `/mcp`:

```text
https://digna.example.com/mcp
```

Se il backend gira direttamente su un host e una porta, ad esempio dopo
`digna serve --address 0.0.0.0 --port 8082`, l'endpoint è quell'indirizzo con `/mcp`:

```text
http://digna-host:8082/mcp
```

Se davanti al backend c'è un reverse proxy, questo deve inoltrare `/mcp` al backend insieme
all'header `Authorization`.

!!! warning "Usa HTTPS in rete"

    Ogni richiesta contiene una chiave API. Usa HTTPS ogni volta che il client IA e *digna* non si
    trovano sulla stessa macchina.

### Da dove arriva la connessione {: #where-the-connection-comes-from }

La maggior parte dei client IA si collega dalla macchina su cui gira: Claude Code, Claude Desktop con
un bridge locale, Antigravity e Gemini CLI. Per questi client, *digna* deve solo essere raggiungibile
da quella macchina, ad esempio all'interno della rete aziendale.

I **connettori personalizzati** di Claude sono diversi: è il cloud di Anthropic a collegarsi
all'endpoint. Funzionano solo quando l'endpoint è raggiungibile da Internet tramite HTTPS. Per
un'installazione di *digna* raggiungibile solo all'interno della tua rete, usa un client che gira
sulla tua macchina.

---

## 2. Creare una chiave API {: #2-create-an-api-key }

Un client IA si autentica con la chiave API di un utente *digna*.

1. Accedi a *digna*.
2. Apri il tuo profilo utente nell'angolo in basso a sinistra.
3. Clicca **API Keys**, poi **Add API Key**.
4. Inserisci un nome che indichi a cosa serve la chiave, ad es. *Claude Code – Marcin*, e scegli
   quando scade.
5. Copia la chiave. Viene mostrata una sola volta.

Ogni richiesta al server MCP invia la chiave in questo header:

```text
Authorization: Bearer <api key>
```

La parola `Bearer` e lo spazio che la segue fanno parte del valore dell'header.

---

## 3. Collegare il tuo client IA {: #3-connect-your-ai-client }

| Client IA | Si collega da | Guida |
|---|---|---|
| Claude Code | La tua macchina | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop con un bridge locale | La tua macchina | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Connettore personalizzato Claude (claude.ai, Claude Desktop, Claude mobile) | Il cloud di Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE e app | La tua macchina | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | La tua macchina | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Funzionano anche altri client MCP, se supportano server remoti tramite HTTP streamable con un header
personalizzato. La maggior parte legge una configurazione come questa. Consulta la documentazione del
tuo client per i nomi esatti del file e delle chiavi:

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

---

## 4. Provalo {: #4-try-it }

Chiedi all'agente qualcosa a cui solo *digna* può rispondere:

- *"Elenca i miei progetti digna."*
- *"Quali sorgenti dati del progetto X oggi non sono verdi?"*
- *"Spiega l'ultimo controllo fallito della sorgente dati Y."*

Se l'agente elenca i tuoi progetti, la connessione funziona.

---

## Sicurezza {: #security }

- **Una chiave per persona e per client.** Così puoi revocare una singola chiave, con
  **Delete API Key**, senza influire su nessun altro.
- **Scegli l'utente con attenzione.** L'agente può fare tutto ciò che può fare l'utente della chiave.
  Se devi solo analizzare i dati, usa un utente con il ruolo di lettore nei progetti.
- **Tieni le chiavi fuori dai file condivisi.** Non fare il commit di un file di configurazione che
  contiene una chiave. Dove il client lo supporta, leggi la chiave da una variabile d'ambiente.
- **Imposta una scadenza.** Crea una nuova chiave prima che quella vecchia scada e aggiorna il
  client.
- **Controlla le chiamate agli strumenti.** Lascia attiva nel client la conferma delle chiamate agli
  strumenti, almeno per quelle che modificano la configurazione.

---

## Risoluzione dei problemi {: #troubleshooting }

### 401 Unauthorized

La risposta indica il motivo:

| Messaggio | Causa |
|---|---|
| `Missing or malformed Authorization header` | Non è stato inviato alcun header, oppure il valore non inizia con `Bearer ` |
| `Invalid API key` | La chiave è errata oppure è stata eliminata |
| `API key expired` | La chiave è scaduta. Creane una nuova |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

La licenza di *digna* non ha una voce digna Agentic, oppure quella voce è scaduta. Chiedi al team di
digna una licenza che includa digna Agentic e installala come descritto nella guida di installazione
del tuo sistema operativo.

### Ogni richiesta fallisce con un errore di licenza non valida

È scaduta la licenza di *digna* stessa. Il server MCP smette di rispondere, insieme al dashboard,
finché non viene installata una nuova licenza.

### L'agente può leggere la configurazione ma non modificarla

L'utente associato alla chiave API non ha il ruolo di editor in quel progetto. Usa la chiave di un
utente con il ruolo di editor, oppure chiedi a un amministratore del progetto di cambiare il ruolo.

### Il client non riesce proprio a collegarsi

La macchina che si collega non raggiunge l'endpoint. Apri l'indirizzo dell'endpoint da quella
macchina e controlla firewall, proxy e certificato. Per un connettore personalizzato Claude, quella
macchina si trova nel cloud di Anthropic, vedi
[Da dove arriva la connessione](#where-the-connection-comes-from).
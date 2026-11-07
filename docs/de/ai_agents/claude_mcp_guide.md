---
title: Claude – Claude über MCP mit digna verbinden | digna Dokumentation
description: Verbinden Sie Claude über den digna MCP Server mit digna — Claude Code über die Kommandozeile oder eine gemeinsame .mcp.json, Claude Desktop mit einer lokalen Bridge und benutzerdefinierte Konnektoren in claude.ai, mit einem API-Schlüssel im Authorization-Header.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai benutzerdefinierter Konnektor, digna MCP server, mcp-remote, Authorization Bearer, digna API-Schlüssel
---

# Claude mit digna verbinden

Diese Anleitung verbindet Claude mit dem **digna MCP Server**. Sie benötigen den MCP-Endpunkt Ihrer
*digna*-Installation und einen API-Schlüssel, wie in der [Übersicht KI-Agenten](overview.md)
beschrieben.

Die Beispiele verwenden `https://digna.example.com/mcp` als Endpunkt. Ersetzen Sie ihn durch Ihren.

## Verbindungsart wählen {: #choose-how-to-connect }

| Claude-Produkt | Verbindet sich von | Funktioniert mit *digna* in Ihrem Netzwerk |
|---|---|---|
| [Claude Code](#claude-code) | Ihrem Rechner | Ja |
| [Claude Desktop mit einer lokalen Bridge](#claude-desktop-with-a-local-bridge) | Ihrem Rechner | Ja |
| [Benutzerdefinierter Konnektor](#custom-connector) in claude.ai, Claude Desktop und Claude mobil | Der Cloud von Anthropic | Nein. Der Endpunkt muss aus dem Internet erreichbar sein |

Für eine *digna*-Installation in Ihrem Firmennetzwerk verwenden Sie Claude Code oder Claude Desktop
mit einer lokalen Bridge.

---

## Claude Code {: #claude-code }

### 1. Den Server hinzufügen {: #1-add-the-server }

Legen Sie den API-Schlüssel in einer Umgebungsvariablen ab und fügen Sie dann den Server hinzu:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Ihre Shell setzt `$DIGNA_API_KEY` beim Ausführen des Befehls ein, sodass Claude Code den Schlüssel
in seiner eigenen Konfiguration speichert.

`--scope` legt fest, wo der Server verfügbar ist:

| Scope | Verfügbar |
|---|---|
| `local` (Standard) | Für Sie, nur im aktuellen Projekt |
| `user` | Für Sie, in jedem Projekt |
| `project` | Für alle, die im Projekt arbeiten, über eine `.mcp.json`-Datei im Projekt |

### 2. Den Server mit Ihrem Team teilen (optional) {: #2-share-the-server-with-your-team }

Damit alle in einem Projekt denselben Server erhalten, legen Sie eine `.mcp.json`-Datei im
Projektstammverzeichnis an. Schreiben Sie den Schlüssel nicht in die Datei. Claude Code setzt
`${DIGNA_API_KEY}` aus der Umgebung der jeweiligen Person ein:

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

Jede Person setzt `DIGNA_API_KEY` auf ihren eigenen Schlüssel. Wenn Claude Code die Datei zum ersten
Mal findet, fragt es, ob die darin enthaltenen Server verwendet werden sollen.

### 3. Die Verbindung prüfen {: #3-verify-the-connection }

In Ihrer Shell:

```bash
claude mcp list
```

Der Server `digna` muss `✔ Connected` anzeigen. Innerhalb einer Claude-Code-Sitzung führen Sie `/mcp`
aus, um den Server und seine Tools zu sehen.

---

## Claude Desktop mit einer lokalen Bridge {: #claude-desktop-with-a-local-bridge }

Die Konfigurationsdatei von Claude Desktop startet lokale MCP-Server auf Ihrem Rechner. Eine kleine
Bridge, das Open-Source-Paket [`mcp-remote`](https://github.com/geelen/mcp-remote), läuft dort und
leitet jede Anfrage mit Ihrem API-Schlüssel an den *digna*-Endpunkt weiter. Da die Bridge auf Ihrem
Rechner läuft, funktioniert das auch mit *digna* in Ihrem Firmennetzwerk.

!!! note "Ein Community-Paket"

    `mcp-remote` wird von seiner Open-Source-Community gepflegt, nicht von Anthropic oder digna.
    Prüfen Sie, ob Ihre Organisation es erlaubt, bevor Sie es verwenden.

### 1. Node.js installieren {: #1-install-nodejs }

Die Bridge benötigt [Node.js](https://nodejs.org) 18 oder neuer. Claude Desktop verwendet die auf
Ihrem System installierte Node.js-Version. Prüfen Sie sie mit:

```bash
node --version
```

### 2. Die Konfigurationsdatei bearbeiten {: #2-edit-the-configuration-file }

Öffnen Sie `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Fügen Sie den Server `digna` hinzu. Enthält die Datei bereits einen Abschnitt `mcpServers`, ergänzen
Sie dort den Eintrag `digna`:

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

!!! warning "Den Header genau wie gezeigt übernehmen"

    Schreiben Sie `Authorization:${AUTH_HEADER}` ohne Leerzeichen und tragen Sie `Bearer <api key>`
    unter `env` ein. Claude Desktop unter Windows maskiert Leerzeichen in `args` nicht, daher macht
    ein Leerzeichen dort den Header unbrauchbar.

### 3. Claude Desktop neu starten {: #3-restart-claude-desktop }

Beenden Sie Claude Desktop vollständig und starten Sie es erneut. Klicken Sie in einem neuen Chat auf
**+** und öffnen Sie **Connectors**: `digna` muss dort aufgeführt und eingeschaltet sein.

---

## Benutzerdefinierter Konnektor {: #custom-connector }

Ein benutzerdefinierter Konnektor macht *digna* in claude.ai, Claude Desktop und den mobilen
Claude-Apps ohne lokale Einrichtung verfügbar. Die Cloud von Anthropic verbindet sich mit dem
Endpunkt, daher funktioniert das nur, wenn:

- Der *digna*-Endpunkt über HTTPS aus dem Internet erreichbar ist
- Ihre Claude-Organisation die Option **Request headers** im Dialog **Add custom connector** hat.
  Anthropic bietet sie als Beta für eine begrenzte Zahl von Organisationen an

!!! warning "Nicht für digna in Ihrem Netzwerk"

    Claudes MCP-Tunnel, die Server in einem privaten Netzwerk erreichen, setzen OAuth auf dem
    MCP-Server voraus. Der digna MCP Server authentifiziert mit API-Schlüsseln, daher kann kein Tunnel
    verwendet werden. Verwenden Sie stattdessen [Claude Code](#claude-code) oder
    [Claude Desktop mit einer lokalen Bridge](#claude-desktop-with-a-local-bridge).

### 1. Die Konnektor-Einstellungen öffnen {: #1-open-the-connector-settings }

- **Free-, Pro-, Max- und Ultra-Pläne**: Gehen Sie zu **Customize > Connectors** und klicken Sie auf
  **Add custom connector**.
- **Team- und Enterprise-Pläne**: Ein Owner geht zu **Organization settings > Connectors**, klickt auf
  **Add**, dann auf **Custom**, und wählt **Web**, wenn nach dem Typ gefragt wird.

### 2. Die Konnektor-Details eingeben {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: Wählen Sie `authorization` als Header-Namen, geben Sie `Bearer <api key>` als
   Wert ein, einschließlich des Worts `Bearer` und des Leerzeichens, und markieren Sie ihn als
   **Required**.
4. Klicken Sie auf **Add**.

!!! warning "Alle teilen sich den Schlüssel"

    Jedes Mitglied, das den Konnektor nutzt, arbeitet mit demselben API-Schlüssel und damit mit
    demselben *digna*-Benutzer. Legen Sie für den Konnektor einen eigenen *digna*-Benutzer an und
    geben Sie ihm nur die Projekte und Rollen, die alle haben dürfen, z. B. die Leserrolle.

In Team- und Enterprise-Plänen verbinden sich die Mitglieder anschließend unter
**Customize > Connectors**, wo der Konnektor das Label **Custom** trägt.

Claude kann den Header eines bestehenden Konnektors nicht ändern. Um einen neuen Schlüssel zu
verwenden, entfernen Sie den Konnektor und fügen Sie ihn erneut hinzu.

---

## Fehlerbehebung für Claude {: #troubleshooting-claude }

### claude mcp list zeigt Failed to connect

Führen Sie `claude mcp get digna` aus, um den Grund zu sehen. Ein `401` bedeutet, dass der Schlüssel
abgelehnt wurde; siehe [401 Unauthorized](overview.md#troubleshooting). Claude Code warnt außerdem
vor Leerzeichen oder einem Zeilenumbruch am Anfang oder Ende des Schlüssels, die oft beim Kopieren
mitkommen.

### digna erscheint nicht in Claude Desktop

- Prüfen Sie, ob Node.js 18 oder neuer installiert ist: `node --version`.
- Prüfen Sie, ob `claude_desktop_config.json` gültiges JSON ist. Ein fehlendes Komma verhindert, dass
  irgendein Server aus der Datei geladen wird.
- Beenden Sie Claude Desktop vollständig, nicht nur das Fenster, und starten Sie es erneut.

### Der benutzerdefinierte Konnektor erreicht den Server nicht

Die Cloud von Anthropic erreicht den Endpunkt nicht. Prüfen Sie, ob er über HTTPS mit einem gültigen
Zertifikat aus dem Internet erreichbar ist, oder verbinden Sie sich stattdessen über
[Claude Code](#claude-code).

---

## Siehe auch {: #see-also }

- [Übersicht KI-Agenten](overview.md): Endpunkt, API-Schlüssel, Sicherheit und allgemeine Fehlerbehebung
- [Gemini](gemini_mcp_guide.md): Antigravity oder Gemini CLI verbinden
- [digna Agentic](../platform/agentic/Introduction.md): was KI-Agenten mit *digna* tun können

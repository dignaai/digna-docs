---
title: Gemini – Antigravity und Gemini CLI über MCP mit digna verbinden | digna Dokumentation
description: Verbinden Sie die Gemini-Tools von Google über den digna MCP Server mit digna — Antigravity CLI, IDE und App mit mcp_config.json sowie Gemini CLI mit settings.json oder gemini mcp add, mit einem API-Schlüssel im Authorization-Header.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, digna API-Schlüssel
---

# Gemini mit digna verbinden

Diese Anleitung verbindet die Gemini-Tools von Google mit dem **digna MCP Server**. Sie benötigen den
MCP-Endpunkt Ihrer *digna*-Installation und einen API-Schlüssel, wie in der
[Übersicht KI-Agenten](overview.md) beschrieben.

Die Beispiele verwenden `https://digna.example.com/mcp` als Endpunkt. Ersetzen Sie ihn durch Ihren.

## Ihr Tool wählen {: #choose-your-tool }

| Tool | Für | Konfiguration |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE und App | Die Agenten-Tools von Google. Antigravity CLI hat Gemini CLI im Juni 2026 für private Google-Konten abgelöst | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Lizenzen für Gemini Code Assist Standard und Enterprise sowie kostenpflichtige Gemini-API-Schlüssel | `settings.json` oder `gemini mcp add` |
| Gemini Enterprise App | — | Nicht unterstützt. Ihr benutzerdefinierter MCP-Konnektor meldet sich mit OAuth oder einem Google-Cloud-Dienstkonto an, während der digna MCP Server mit API-Schlüsseln authentifiziert |

Alle diese Tools verbinden sich von dem Rechner aus, auf dem sie laufen. Sie funktionieren daher mit
*digna* in Ihrem Firmennetzwerk, solange dieser Rechner den Endpunkt erreicht.

---

## Antigravity {: #antigravity }

Antigravity liest seine MCP-Server aus `mcp_config.json`, die CLI, IDE und App gemeinsam nutzen.

### 1. mcp_config.json öffnen {: #1-open-mcp-config-json }

| Scope | Datei |
|---|---|
| Alle Ihre Projekte | `~/.gemini/config/mcp_config.json` |
| Ein Workspace | `.agents/mcp_config.json` im Workspace |

So öffnen Sie die verwendete Datei:

- **CLI**: Geben Sie `/mcp` ein und drücken Sie ++enter++, um den MCP-Manager zu öffnen.
- **IDE**: Öffnen Sie im Agenten-Seitenbereich das Menü **…**, wählen Sie **MCP Servers**, dann
  **Manage MCP Servers** und dann **View raw config**.
- **App**: Gehen Sie zu **Customizations** > **Installed** > **MCP Servers** und verwenden Sie
  **Copy Config File Path**.

### 2. Den digna-Server hinzufügen {: #2-add-the-digna-server }

Fügen Sie den Eintrag `digna` hinzu. Enthält die Datei bereits einen Abschnitt `mcpServers`, ergänzen
Sie ihn dort:

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

Antigravity erreicht entfernte Server nur über Streamable HTTP, das der digna MCP Server verwendet.
Geben Sie den Endpunkt als `serverUrl` an; der Schlüssel `httpUrl` von Gemini CLI wird nicht
unterstützt.

### 3. Die Verbindung prüfen {: #3-verify-the-connection }

Geben Sie in der CLI `/mcp` ein: Der MCP-Manager zeigt den Server `digna` mit seinem Status und seinen
Tools, kann die Konfiguration neu laden und Verbindungsprotokolle anzeigen. In der IDE erscheint der
Server unter **Manage MCP Servers**.

!!! warning "Die Datei schützen"

    `mcp_config.json` enthält den API-Schlüssel im Klartext. Halten Sie eine Workspace-Datei
    `.agents/mcp_config.json` aus der Versionskontrolle heraus, und erlauben Sie nur Ihrem eigenen
    Konto, die globale Datei zu lesen.

---

## Gemini CLI {: #gemini-cli }

### 1. Den Server hinzufügen {: #1-add-the-server }

Legen Sie den API-Schlüssel in einer Umgebungsvariablen ab und fügen Sie dann den Server hinzu:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Ihre Shell setzt `$DIGNA_API_KEY` beim Ausführen des Befehls ein, sodass Gemini CLI den Schlüssel in
seinen Einstellungen speichert. Ohne `--scope user` wird der Server nur zum aktuellen Projekt
hinzugefügt.

### 2. Oder settings.json bearbeiten {: #2-or-edit-settings-json }

Der Befehl oben schreibt in `settings.json`. So bearbeiten Sie die Datei selbst:

| Scope | Datei |
|---|---|
| Alle Ihre Projekte | `~/.gemini/settings.json` |
| Ein Projekt | `.gemini/settings.json` im Projekt |

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

Verwenden Sie `httpUrl`, den Schlüssel für Streamable HTTP. Der ähnliche Schlüssel `url` wählt den
älteren SSE-Transport, den der digna MCP Server nicht anbietet. Verwenden Sie keine Unterstriche im
Servernamen.

!!! tip "Trust ausgeschaltet lassen"

    Gemini CLI fragt vor jedem Tool-Aufruf nach, es sei denn, der Server hat `"trust": true`. Lassen
    Sie `trust` für *digna* ausgeschaltet, damit Sie jede Änderung bestätigen, die ein Agent an Ihrer
    Konfiguration vornimmt.

### 3. Die Verbindung prüfen {: #3-verify-the-connection-gemini-cli }

In Ihrer Shell:

```bash
gemini mcp list
```

Der Server `digna` muss als verbunden angezeigt werden. Innerhalb einer Gemini-CLI-Sitzung führen Sie
`/mcp` aus, um den Server und seine Tools zu sehen.

---

## Fehlerbehebung für Gemini {: #troubleshooting-gemini }

### Der Server wird als getrennt angezeigt

- Prüfen Sie, ob der Endpunkt auf `/mcp` endet und von Ihrem Rechner aus erreichbar ist.
- Prüfen Sie den Namen des Schlüssels: `serverUrl` in Antigravity, `httpUrl` in Gemini CLI.
- Ein `401` bedeutet, dass der Schlüssel abgelehnt wurde; siehe
  [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI startet für mein Konto nicht mehr

Seit Juni 2026 verwenden private Google-Konten Antigravity CLI statt Gemini CLI. Übertragen Sie den
Eintrag `digna` nach `mcp_config.json`, wie unter [Antigravity](#antigravity) beschrieben, und
benennen Sie `httpUrl` in `serverUrl` um.

---

## Siehe auch {: #see-also }

- [Übersicht KI-Agenten](overview.md): Endpunkt, API-Schlüssel, Sicherheit und allgemeine Fehlerbehebung
- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop oder einen benutzerdefinierten Konnektor verbinden
- [digna Agentic](../platform/agentic/Introduction.md): was KI-Agenten mit *digna* tun können

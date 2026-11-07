---
title: KI-Agenten – Übersicht der MCP-Integration | digna Dokumentation
description: Verbinden Sie Claude, Gemini und andere KI-Agenten über den digna MCP Server mit digna. Ermitteln Sie den MCP-Endpunkt, erstellen Sie einen API-Schlüssel, prüfen Sie Lizenz- und Netzwerkvoraussetzungen und wählen Sie die Anleitung für Ihren KI-Client.
image: /assets/logo_square.png
keywords: digna MCP server, Model Context Protocol, KI-Agent verbinden, Claude MCP, Gemini MCP, Antigravity MCP, digna API-Schlüssel, digna Agentic
---

# KI-Agenten mit digna verbinden

Der **digna MCP Server** ermöglicht es KI-Agenten, über das
[Model Context Protocol](https://modelcontextprotocol.io) (MCP) mit *digna* zu arbeiten – einen offenen
Standard, den Claude, Gemini und viele andere KI-Tools unterstützen. Ein mit *digna* verbundener Agent
kann Fragen zu Ihren Daten beantworten, Alarme untersuchen und bei der Konfiguration von *digna*
helfen. Was Agenten können, lesen Sie unter [digna Agentic](../platform/agentic/Introduction.md).

Diese Seite behandelt die *digna*-Seite, die für jeden KI-Client gleich ist. Die Client-Anleitungen
zeigen anschließend, wo Sie die Angaben eintragen:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop und benutzerdefinierte Konnektoren
- [Gemini](gemini_mcp_guide.md): Antigravity und Gemini CLI

!!! info "Beta"

    digna Agentic und damit der digna MCP Server wird in
    [Release 2026.11](../changelog/Release_202611.md) als Betaversion ausgeliefert.

---

## Bevor Sie beginnen {: #before-you-start }

Sie benötigen:

- *digna* Release 2026.11 oder neuer
- Eine Lizenz, die **digna Agentic** enthält. Ohne sie lehnt der MCP-Server jede Anfrage ab
- Ein *digna*-Benutzerkonto. Der Agent handelt in jedem Projekt mit den Berechtigungen dieses
  Benutzers, siehe [Berechtigungen](../platform/agentic/how_it_works.md#permissions)
- Einen KI-Client, der sich über **Streamable HTTP** mit entfernten MCP-Servern verbindet und einen
  `Authorization`-Header senden kann

---

## 1. Den MCP-Endpunkt ermitteln {: #1-find-the-mcp-endpoint }

Der MCP-Server ist Teil des *digna*-Backends, Sie müssen also nichts zusätzlich installieren oder
starten. Sein Endpunkt ist die Adresse des Backends, gefolgt von `/mcp`:

```text
https://digna.example.com/mcp
```

Läuft das Backend direkt auf einem Host und Port, zum Beispiel nach
`digna serve --address 0.0.0.0 --port 8082`, ist der Endpunkt diese Adresse mit `/mcp`:

```text
http://digna-host:8082/mcp
```

Steht ein Reverse Proxy vor dem Backend, muss er `/mcp` zusammen mit dem `Authorization`-Header an
das Backend weiterleiten.

!!! warning "Im Netzwerk HTTPS verwenden"

    Jede Anfrage enthält einen API-Schlüssel. Verwenden Sie HTTPS, sobald KI-Client und *digna* nicht
    auf demselben Rechner laufen.

### Woher die Verbindung kommt {: #where-the-connection-comes-from }

Die meisten KI-Clients verbinden sich von dem Rechner aus, auf dem sie laufen: Claude Code, Claude
Desktop mit einer lokalen Bridge, Antigravity und Gemini CLI. Für sie muss *digna* nur von diesem
Rechner aus erreichbar sein, zum Beispiel innerhalb Ihres Firmennetzwerks.

Bei Claudes **benutzerdefinierten Konnektoren** ist das anders: Hier verbindet sich die Cloud von
Anthropic mit dem Endpunkt. Sie funktionieren nur, wenn der Endpunkt über HTTPS aus dem Internet
erreichbar ist. Für eine *digna*-Installation, die nur innerhalb Ihres Netzwerks erreichbar ist,
verwenden Sie einen Client, der auf Ihrem Rechner läuft.

---

## 2. Einen API-Schlüssel erstellen {: #2-create-an-api-key }

Ein KI-Client authentifiziert sich mit dem API-Schlüssel eines *digna*-Benutzers.

1. Melden Sie sich bei *digna* an.
2. Öffnen Sie Ihr Benutzerprofil unten links.
3. Klicken Sie auf **API-Schlüssel** und dann auf **API-Schlüssel hinzufügen**.
4. Geben Sie einen Namen ein, der sagt, wofür der Schlüssel dient, z. B. *Claude Code – Marcin*, und
   wählen Sie, wann er abläuft.
5. Kopieren Sie den Schlüssel. Er wird nur einmal angezeigt.

Jede Anfrage an den MCP-Server sendet den Schlüssel in diesem Header:

```text
Authorization: Bearer <api key>
```

Das Wort `Bearer` und das Leerzeichen danach gehören zum Wert des Headers.

---

## 3. Ihren KI-Client verbinden {: #3-connect-your-ai-client }

| KI-Client | Verbindet sich von | Anleitung |
|---|---|---|
| Claude Code | Ihrem Rechner | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop mit einer lokalen Bridge | Ihrem Rechner | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Benutzerdefinierter Claude-Konnektor (claude.ai, Claude Desktop, Claude mobil) | Der Cloud von Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE und App | Ihrem Rechner | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Ihrem Rechner | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Andere MCP-Clients funktionieren ebenfalls, sofern sie entfernte Server über Streamable HTTP mit
einem eigenen Header unterstützen. Die meisten lesen eine Konfiguration wie diese. Die genauen
Datei- und Schlüsselnamen finden Sie in der Dokumentation Ihres Clients:

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

## 4. Ausprobieren {: #4-try-it }

Stellen Sie dem Agenten eine Frage, die nur *digna* beantworten kann:

- *„Liste meine digna-Projekte auf.“*
- *„Welche Datenquellen in Projekt X sind heute nicht grün?“*
- *„Erkläre den letzten fehlgeschlagenen Check der Datenquelle Y.“*

Wenn der Agent Ihre Projekte auflistet, funktioniert die Verbindung.

---

## Sicherheit {: #security }

- **Ein Schlüssel pro Person und Client.** Dann können Sie einen einzelnen Schlüssel mit
  **API-Schlüssel löschen** widerrufen, ohne andere zu beeinträchtigen.
- **Wählen Sie den Benutzer bewusst.** Der Agent kann alles, was der Benutzer des Schlüssels kann.
  Wenn nur Daten untersucht werden sollen, verwenden Sie einen Benutzer mit der Leserrolle in den
  Projekten.
- **Halten Sie Schlüssel aus gemeinsam genutzten Dateien heraus.** Committen Sie keine
  Konfigurationsdatei, die einen Schlüssel enthält. Wo der Client es unterstützt, lesen Sie den
  Schlüssel aus einer Umgebungsvariablen.
- **Legen Sie ein Ablaufdatum fest.** Erstellen Sie einen neuen Schlüssel, bevor der alte abläuft,
  und aktualisieren Sie den Client.
- **Prüfen Sie Tool-Aufrufe.** Lassen Sie die Bestätigung von Tool-Aufrufen im Client eingeschaltet,
  zumindest für Aufrufe, die die Konfiguration ändern.

---

## Fehlerbehebung {: #troubleshooting }

### 401 Unauthorized

Die Antwort nennt den Grund:

| Meldung | Ursache |
|---|---|
| `Missing or malformed Authorization header` | Es wurde kein Header gesendet, oder der Wert beginnt nicht mit `Bearer ` |
| `Invalid API key` | Der Schlüssel ist falsch oder wurde gelöscht |
| `API key expired` | Der Schlüssel ist abgelaufen. Erstellen Sie einen neuen |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

Die *digna*-Lizenz hat keinen Eintrag für digna Agentic, oder dieser Eintrag ist abgelaufen. Fragen
Sie das digna-Team nach einer Lizenz, die digna Agentic enthält, und installieren Sie sie wie in der
Installationsanleitung für Ihr Betriebssystem beschrieben.

### Jede Anfrage schlägt mit einem Fehler wegen ungültiger Lizenz fehl

Die *digna*-Lizenz selbst ist abgelaufen. Der MCP-Server antwortet dann ebenso wie das Dashboard
nicht mehr, bis eine neue Lizenz installiert ist.

### Der Agent kann die Konfiguration lesen, aber nicht ändern

Der Benutzer hinter dem API-Schlüssel hat in diesem Projekt nicht die Editorrolle. Verwenden Sie den
Schlüssel eines Benutzers mit der Editorrolle, oder bitten Sie einen Projektadministrator, die Rolle
zu ändern.

### Der Client kann sich überhaupt nicht verbinden

Der Rechner, der die Verbindung aufbaut, erreicht den Endpunkt nicht. Öffnen Sie die Adresse des
Endpunkts von diesem Rechner aus und prüfen Sie Firewalls, Proxys und das Zertifikat. Bei einem
benutzerdefinierten Claude-Konnektor steht dieser Rechner in der Cloud von Anthropic, siehe
[Woher die Verbindung kommt](#where-the-connection-comes-from).

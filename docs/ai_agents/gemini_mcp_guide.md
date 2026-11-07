---
title: Gemini – Connect Antigravity and Gemini CLI to digna via MCP | digna Documentation
description: Connect Google's Gemini tools to digna through the digna MCP Server — Antigravity CLI, IDE and app with mcp_config.json, and Gemini CLI with settings.json or gemini mcp add, using an API key in the Authorization header.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, digna API key
---

# Connect Gemini to digna

This guide connects Google's Gemini tools to the **digna MCP Server**. You need the MCP endpoint
of your *digna* installation and an API key, as described in the [AI Agents Overview](overview.md).

The examples use `https://digna.example.com/mcp` as the endpoint. Replace it with yours.

## Choose Your Tool {: #choose-your-tool }

| Tool | For | Configuration |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE and app | Google's agent tools. Antigravity CLI replaced Gemini CLI for individual Google accounts in June 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard and Enterprise licenses, and paid Gemini API keys | `settings.json` or `gemini mcp add` |
| Gemini Enterprise app | — | Not supported. Its custom MCP connector signs in with OAuth or a Google Cloud service account, while the digna MCP Server authenticates with API keys |

All of these tools connect from the machine they run on, so they work with *digna* inside your
company network as long as that machine can reach the endpoint.

---

## Antigravity {: #antigravity }

Antigravity reads its MCP servers from `mcp_config.json`, shared by the CLI, the IDE and the app.

### 1. Open mcp_config.json {: #1-open-mcp-config-json }

| Scope | File |
|---|---|
| All your projects | `~/.gemini/config/mcp_config.json` |
| One workspace | `.agents/mcp_config.json` in the workspace |

To open the file in use:

- **CLI**: type `/mcp` and press ++enter++ to open the MCP manager.
- **IDE**: in the agent side panel, open the **…** menu, select **MCP Servers**, then
  **Manage MCP Servers**, then **View raw config**.
- **App**: go to **Customizations** > **Installed** > **MCP Servers** and use
  **Copy Config File Path**.

### 2. Add the digna Server {: #2-add-the-digna-server }

Add the `digna` entry. If the file already has an `mcpServers` section, add it there:

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

Antigravity reaches remote servers only over streamable HTTP, which the digna MCP Server uses.
Write the endpoint as `serverUrl`; the `httpUrl` key of Gemini CLI is not supported.

### 3. Verify the Connection {: #3-verify-the-connection }

In the CLI, type `/mcp`: the MCP manager shows the `digna` server with its status and tools, and
can reload the configuration and show connection logs. In the IDE, the server appears under
**Manage MCP Servers**.

!!! warning "Protect the file"

    `mcp_config.json` holds the API key in plain text. Keep a workspace `.agents/mcp_config.json`
    out of version control, and let only your own account read the global file.

---

## Gemini CLI {: #gemini-cli }

### 1. Add the Server {: #1-add-the-server }

Put the API key in an environment variable, then add the server:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Your shell fills in `$DIGNA_API_KEY` when you run the command, so Gemini CLI stores the key in its
settings. Without `--scope user`, the server is added to the current project only.

### 2. Or Edit settings.json {: #2-or-edit-settings-json }

The command above writes to `settings.json`. To edit the file yourself:

| Scope | File |
|---|---|
| All your projects | `~/.gemini/settings.json` |
| One project | `.gemini/settings.json` in the project |

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

Use `httpUrl`, the key for streamable HTTP. The similar `url` key selects the older SSE transport,
which the digna MCP Server does not offer. Don't use underscores in the server name.

!!! tip "Leave trust off"

    Gemini CLI asks before each tool call unless the server has `"trust": true`. Leave `trust` off
    for *digna*, so that you confirm every change an agent makes to your configuration.

### 3. Verify the Connection {: #3-verify-the-connection-gemini-cli }

From your shell:

```bash
gemini mcp list
```

The `digna` server must show as connected. Inside a Gemini CLI session, run `/mcp` to see the
server and its tools.

---

## Troubleshooting Gemini {: #troubleshooting-gemini }

### The server shows as disconnected

- Check that the endpoint ends in `/mcp` and is reachable from your machine.
- Check the key name: `serverUrl` in Antigravity, `httpUrl` in Gemini CLI.
- A `401` means the key was rejected; see [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI no longer starts for my account

Since June 2026, individual Google accounts use Antigravity CLI instead of Gemini CLI. Move the
`digna` entry to `mcp_config.json` as described under [Antigravity](#antigravity), and rename
`httpUrl` to `serverUrl`.

---

## See Also {: #see-also }

- [AI Agents Overview](overview.md): endpoint, API key, security and general troubleshooting
- [Claude](claude_mcp_guide.md): connect Claude Code, Claude Desktop or a custom connector
- [digna Agentic](../platform/agentic/Introduction.md): what AI agents can do with *digna*

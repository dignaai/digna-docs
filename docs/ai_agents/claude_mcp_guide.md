---
title: Claude – Connect Claude to digna via MCP | digna Documentation
description: Connect Claude to digna through the digna MCP Server — Claude Code from the command line or a shared .mcp.json, Claude Desktop with a local bridge, and custom connectors in claude.ai, with an API key in the Authorization header.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai custom connector, digna MCP server, mcp-remote, Authorization Bearer, digna API key
---

# Connect Claude to digna

This guide connects Claude to the **digna MCP Server**. You need the MCP endpoint of your *digna*
installation and an API key, as described in the [AI Agents Overview](overview.md).

The examples use `https://digna.example.com/mcp` as the endpoint. Replace it with yours.

## Choose How to Connect {: #choose-how-to-connect }

| Claude product | Connects from | Works with *digna* inside your network |
|---|---|---|
| [Claude Code](#claude-code) | Your machine | Yes |
| [Claude Desktop with a local bridge](#claude-desktop-with-a-local-bridge) | Your machine | Yes |
| [Custom connector](#custom-connector) in claude.ai, Claude Desktop and Claude mobile | Anthropic's cloud | No. The endpoint must be reachable from the internet |

For a *digna* installation that runs inside your company network, use Claude Code or Claude
Desktop with a local bridge.

---

## Claude Code {: #claude-code }

### 1. Add the Server {: #1-add-the-server }

Put the API key in an environment variable, then add the server:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Your shell fills in `$DIGNA_API_KEY` when you run the command, so Claude Code stores the key in
its own configuration.

`--scope` decides where the server is available:

| Scope | Available |
|---|---|
| `local` (default) | To you, in the current project only |
| `user` | To you, in every project |
| `project` | To everyone who works in the project, through a `.mcp.json` file in the project |

### 2. Share the Server With Your Team (Optional) {: #2-share-the-server-with-your-team }

To give everyone in a project the same server, add a `.mcp.json` file to the project root. Don't
write the key into the file. Claude Code fills in `${DIGNA_API_KEY}` from each person's own
environment:

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

Each person sets `DIGNA_API_KEY` to their own key. The first time Claude Code finds the file, it
asks whether to use the servers in it.

### 3. Verify the Connection {: #3-verify-the-connection }

From your shell:

```bash
claude mcp list
```

The `digna` server must show `✔ Connected`. Inside a Claude Code session, run `/mcp` to see the
server and its tools.

---

## Claude Desktop With a Local Bridge {: #claude-desktop-with-a-local-bridge }

Claude Desktop's configuration file starts local MCP servers on your machine. A small bridge,
the open-source [`mcp-remote`](https://github.com/geelen/mcp-remote) package, runs there and
forwards every request to the *digna* endpoint with your API key. Because the bridge runs on your
machine, this works with *digna* inside your company network.

!!! note "A community package"

    `mcp-remote` is maintained by its open-source community, not by Anthropic or digna. Check that
    your organization allows it before you use it.

### 1. Install Node.js {: #1-install-nodejs }

The bridge needs [Node.js](https://nodejs.org) 18 or later. Claude Desktop uses the Node.js
version installed on your system. Check it with:

```bash
node --version
```

### 2. Edit the Configuration File {: #2-edit-the-configuration-file }

Open `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the `digna` server. If the file already has an `mcpServers` section, add the `digna` entry to
it:

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

!!! warning "Keep the header exactly as shown"

    Write `Authorization:${AUTH_HEADER}` without spaces, and put `Bearer <api key>` in `env`.
    Claude Desktop on Windows does not escape spaces inside `args`, so a space there breaks the
    header.

### 3. Restart Claude Desktop {: #3-restart-claude-desktop }

Quit Claude Desktop completely and start it again. In a new chat, click **+** and open
**Connectors**: `digna` must be listed and switched on.

---

## Custom Connector {: #custom-connector }

A custom connector makes *digna* available in claude.ai, Claude Desktop and the Claude mobile apps
without any local setup. Anthropic's cloud connects to the endpoint, so this only works when:

- The *digna* endpoint is reachable from the internet over HTTPS
- Your Claude organization has the **Request headers** option in the **Add custom connector**
  dialog. Anthropic offers it as a beta to a limited set of organizations

!!! warning "Not for digna inside your network"

    Claude's MCP tunnels, which reach servers inside a private network, require OAuth on the MCP
    server. The digna MCP Server authenticates with API keys, so a tunnel can't be used. Use
    [Claude Code](#claude-code) or [Claude Desktop with a local bridge](#claude-desktop-with-a-local-bridge)
    instead.

### 1. Open the Connector Settings {: #1-open-the-connector-settings }

- **Free, Pro, Max and Ultra plans**: go to **Customize > Connectors** and click
  **Add custom connector**.
- **Team and Enterprise plans**: an Owner goes to **Organization settings > Connectors**, clicks
  **Add**, then **Custom**, and chooses **Web** if asked for the type.

### 2. Enter the Connector Details {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: choose `authorization` as the header name, enter `Bearer <api key>` as the
   value, including the word `Bearer` and the space, and mark it **Required**.
4. Click **Add**.

!!! warning "Everyone shares the key"

    Every member who uses the connector works with the same API key, and so with the same *digna*
    user. Create a dedicated *digna* user for the connector and give it only the projects and
    roles everyone may have, e.g. the reader role.

On Team and Enterprise plans, members then connect under **Customize > Connectors**, where the
connector carries the **Custom** label.

Claude can't change the header of an existing connector. To use a new key, remove the connector
and add it again.

---

## Troubleshooting Claude {: #troubleshooting-claude }

### claude mcp list shows Failed to connect

Run `claude mcp get digna` to see the reason. A `401` means the key was rejected; see
[401 Unauthorized](overview.md#troubleshooting). Claude Code also warns about spaces or a line
break at the start or end of the key, which often come with copying it.

### digna does not appear in Claude Desktop

- Check that Node.js 18 or later is installed: `node --version`.
- Check that `claude_desktop_config.json` is valid JSON. A missing comma stops every server in the
  file from loading.
- Quit Claude Desktop completely, not just the window, and start it again.

### The custom connector cannot reach the server

Anthropic's cloud cannot reach the endpoint. Check that it is reachable from the internet over
HTTPS with a valid certificate, or connect through [Claude Code](#claude-code) instead.

---

## See Also {: #see-also }

- [AI Agents Overview](overview.md): endpoint, API key, security and general troubleshooting
- [Gemini](gemini_mcp_guide.md): connect Antigravity or Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): what AI agents can do with *digna*

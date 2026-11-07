# Connect AI Agents to digna

The **digna MCP Server** lets AI agents work with *digna* through the
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), an open standard supported by
Claude, Gemini and many other AI tools. An agent connected to *digna* can answer questions about
your data, investigate alerts and help configure *digna*. See
[digna Agentic](../platform/agentic/Introduction.md) for what agents can do.

This page covers the *digna* side, which is the same for every AI client. The client guides then
show where to enter the endpoint and the key:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop and custom connectors
- [Gemini](gemini_mcp_guide.md): Antigravity and Gemini CLI

!!! info "Beta"

    digna Agentic, and with it the digna MCP Server, is delivered as a beta version in
    [Release 2026.11](../changelog/Release_202611.md).

---

## Before You Start {: #before-you-start }

You need:

- *digna* Release 2026.11 or later
- A license that includes **digna Agentic**. Without it, the MCP server refuses every request
- A *digna* user account. The agent acts with that user's permissions in each project, see
  [Permissions](../platform/agentic/how_it_works.md#permissions)
- An AI client that connects to remote MCP servers over **streamable HTTP** and can send an
  `Authorization` header

---

## 1. Find the MCP Endpoint {: #1-find-the-mcp-endpoint }

The MCP server is part of the *digna* backend, so there is nothing extra to install or start. Its
endpoint is the backend's address followed by `/mcp`:

```text
https://digna.example.com/mcp
```

If the backend runs directly on a host and port, for example after
`digna serve --address 0.0.0.0 --port 8082`, the endpoint is that address with `/mcp`:

```text
http://digna-host:8082/mcp
```

If a reverse proxy sits in front of the backend, it must forward `/mcp` to the backend together
with the `Authorization` header.

!!! warning "Use HTTPS on a network"

    Every request carries an API key. Use HTTPS whenever the AI client and *digna* are not on the
    same machine.

### Where the Connection Comes From {: #where-the-connection-comes-from }

Most AI clients connect from the machine they run on: Claude Code, Claude Desktop with a local
bridge, Antigravity and Gemini CLI. For them, *digna* only has to be reachable from that machine,
for example inside your company network.

Claude's **custom connectors** are different: Anthropic's cloud connects to the endpoint. They
only work when the endpoint is reachable from the internet over HTTPS. For a *digna* installation
that is only reachable inside your network, use a client that runs on your machine.

---

## 2. Create an API Key {: #2-create-an-api-key }

An AI client authenticates with the API key of a *digna* user.

1. Log in to *digna*.
2. Open your user profile in the bottom-left corner.
3. Click **API Keys**, then **Add API Key**.
4. Enter a name that says what the key is for, e.g. *Claude Code – Marcin*, and choose when it
   expires.
5. Copy the key. It is shown only once.

Every request to the MCP server sends the key in this header:

```text
Authorization: Bearer <api key>
```

The word `Bearer` and the space after it are part of the header value.

---

## 3. Connect Your AI Client {: #3-connect-your-ai-client }

| AI client | Connects from | Guide |
|---|---|---|
| Claude Code | Your machine | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop with a local bridge | Your machine | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude custom connector (claude.ai, Claude Desktop, Claude mobile) | Anthropic's cloud | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE and app | Your machine | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Your machine | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Other MCP clients work as well if they support remote servers over streamable HTTP with a custom
header. Most of them read a configuration like this one. Check your client's documentation for
the exact file and key names:

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

## 4. Try It {: #4-try-it }

Ask the agent something only *digna* can answer:

- *"List my digna projects."*
- *"Which data sources in project X are not green today?"*
- *"Explain the latest failed check of data source Y."*

If the agent lists your projects, the connection works.

---

## Security {: #security }

- **One key per person and client.** Then you can revoke a single key, with **Delete API Key**,
  without affecting anyone else.
- **Choose the user deliberately.** The agent can do everything the key's user can do. For
  investigating data only, use a user with the reader role in the projects.
- **Keep keys out of shared files.** Don't commit a configuration file that contains a key. Where
  the client supports it, read the key from an environment variable.
- **Set an expiry.** Create a new key before the old one expires, and update the client.
- **Review tool calls.** Keep the client's confirmation for tool calls switched on, at least for
  calls that change the configuration.

---

## Troubleshooting {: #troubleshooting }

### 401 Unauthorized

The response says why:

| Message | Cause |
|---|---|
| `Missing or malformed Authorization header` | No header was sent, or the value doesn't start with `Bearer ` |
| `Invalid API key` | The key is wrong, or it was deleted |
| `API key expired` | The key has expired. Create a new one |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

The *digna* license has no digna Agentic entry, or that entry has expired. Ask the digna team for
a license that includes digna Agentic, and install it as the installation guide for your operating
system describes.

### Every request fails with an invalid license error

The *digna* license itself has expired. The MCP server stops answering together with the
dashboard until a new license is installed.

### The agent can read but not change configuration

The user behind the API key does not have the editor role in that project. Use the key of a user
with the editor role, or ask a project administrator to change the role.

### The client cannot connect at all

The machine that connects cannot reach the endpoint. Open the endpoint's address from that
machine, and check firewalls, proxies and the certificate. For a Claude custom connector, that
machine is in Anthropic's cloud, see [Where the Connection Comes From](#where-the-connection-comes-from).
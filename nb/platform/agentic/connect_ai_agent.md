# Connect an AI Agent

This page connects an AI agent to the **digna MCP Server**. You need three things: the address of the MCP server, an API key, and an MCP client that supports remote servers over **streamable HTTP** with a custom header.

---

## 1. Find the MCP Endpoint {: #1-find-the-mcp-endpoint }

The MCP server is part of the digna backend. Its endpoint is the backend's address followed by `/mcp`, the same address the [Python SDK](../../sdk/Release%202026.11/quickstart.md) uses as `base_url`:

```text
https://digna.example.com/mcp
```

The machine the AI agent runs on must be able to reach this address. Use HTTPS whenever the agent connects over a network, because every request carries an API key.

---

## 2. Create an API Key {: #2-create-an-api-key }

An agent authenticates with the API key of a digna user and acts with that user's permissions (see [Permissions](how_it_works.md#permissions)).

1. Log in to digna.
2. Open your user profile in the bottom-left corner.
3. Click **API Keys**, then **Add API Key**.
4. Enter a name that says what the key is for, e.g. *Claude Code – Marcin*, and choose when it expires.
5. Copy the key. It is shown only once.

Create one key per agent and per person, so you can revoke a single key without affecting the others. Keep the key out of source code and shared configuration files.

---

## 3. Add the Server to Your Client {: #3-add-the-server-to-your-client }

Every request to the MCP server sends the key in an `Authorization` header:

```text
Authorization: Bearer <api key>
```

### Claude Code {: #claude-code }

```bash
claude mcp add --transport http digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Start Claude Code and run `/mcp` to confirm that the `digna` server is connected.

### Other MCP clients {: #other-mcp-clients }

Most clients that support remote MCP servers read a JSON configuration like this one. Check your client's documentation for the exact file and key names:

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

Ask the agent something only digna can answer:

- *"List my digna projects."*
- *"Which data sources in project X are not green today?"*
- *"Explain the latest failed check of data source Y."*

If the agent lists your projects, the connection works.

---

## Troubleshooting {: #troubleshooting }

### The client reports 401 Unauthorized

The API key is missing, wrong or expired. Check that the header reads `Authorization: Bearer <api key>` with a single space, and create a new key if the old one expired.

### Every request fails with an invalid license error

The digna license has expired. The MCP server stops answering together with the dashboard until a new license is installed.

### The agent can read but not change configuration

The user behind the API key does not have the editor role in that project. Use a key of a user with the editor role, or ask a project administrator to change the role.

### The client cannot connect at all

The machine the agent runs on cannot reach the digna backend. Open the endpoint's address from that machine, and check firewalls, proxies and the certificate.

---

## Related Pages

- [digna Agentic – Introduction](Introduction.md)
- [digna Agentic – How It Works](how_it_works.md)
- [Python SDK Quickstart](../../sdk/Release%202026.11/quickstart.md)
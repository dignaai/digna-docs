# digna Agentic – How It Works

---

## The digna MCP Server

The **digna MCP Server** is part of the digna backend and is served at the `/mcp` path of the same address the [Python SDK](../../sdk/Release%202026.11/index.md) uses. It speaks the [Model Context Protocol](https://modelcontextprotocol.io) over streamable HTTP.

An AI agent sees the server as a set of **tools**: named actions with a description, such as *list the data sources of a project* or *get the anomaly check statuses of a data source*. The agent decides which tools to call to answer your request, calls them, and works with the results.

Every tool call is a separate request, authenticated with an API key (see [Connect an AI Agent](connect_ai_agent.md)).

---

## What an Agent Can Do

The tools cover the same ground as the dashboard. Grouped by what an agent does with them:

| Area | What the agent can do |
|---|---|
| **Explore** | List projects, data sources and their attributes; browse the catalogs, schemas, tables and columns of a database connection; read the statistics and the column profile of an attribute |
| **Configure** | Create and change projects, data sources, attributes and datasets; Data Validation, Data Analytics and Data Reconciliation rules; validation rule templates; anomaly model, threshold and notification settings; Timeliness and Schema Tracker settings |
| **Run** | Create, change and delete inspection schedules; start an inspection, follow its progress and stop it |
| **Read results** | Read inspection statuses for a project, data source or dataset, and the check statuses of every module down to the single check, with its value |
| **Notify** | Create and change subscriptions; test a notification channel |

Some areas are read-only on purpose. Database connections, notification channels and SMTP connections hold credentials, so an agent can list them and test them, but not create or change them.

---

## Descriptions

Every data source and attribute has a **Description** field. AI agents read it: the description is returned with the data source or attribute, and it is often the only place where the business meaning of a table or column is written down.

Good descriptions answer what an agent can't guess from a name:

| Field | Weak | Strong |
|---|---|---|
| Data source `T_ORD_L` | *Orders* | *Booked orders, one row per order line, loaded nightly from SAP. Cancelled orders are deleted, not flagged.* |
| Attribute `AMT_NET` | *Amount* | *Net order line amount in EUR, after discounts, before VAT* |

An agent can write descriptions too. Asking it to *"suggest descriptions for the attributes of this data source"* is a quick way to start, as long as someone who knows the data reviews the result.

---

## Answering a Business Question

A typical question, *"Which regions had unusually low sales last week?"*, is answered in steps:

1. The agent uses the descriptions to find the data source and attribute that hold sales.
2. It checks how digna measures them, e.g. whether the data source is split into datasets per region.
3. It reads the anomaly check statuses and values for last week and reports the regions outside their expected range.

When step 2 shows that digna doesn't measure what the question needs, for example because the data source isn't split by region, the agent says so and **suggests a configuration change**: here, a dataset per region. Once you agree, it can apply the change, and the next inspections answer the question.

---

## Permissions

An agent acts as the user whose API key it uses:

- It sees only the projects that user can access.
- It can change configuration only where that user's project role allows it. Without the editor role, write tools are refused.
- What an agent changes is visible in the dashboard immediately, like a change made by that user.

Give an agent a key of a user with the role it needs. An agent that only answers questions doesn't need the editor role.

---

## Related Pages

- [digna Agentic – Introduction](Introduction.md)
- [Connect an AI Agent](connect_ai_agent.md)
- [Changelog – Release 2026.11](../../changelog/Release_202611.md)
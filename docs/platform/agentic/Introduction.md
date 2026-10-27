---
title: digna Agentic – AI Agents for Data Quality | digna Documentation
description: Learn how digna Agentic lets Claude and other AI agents work with digna through the digna MCP Server. Ask business questions about your data, investigate alerts, and let agents suggest and apply configuration changes.
image: /assets/logo_square.png
keywords:
  - digna agentic
  - digna MCP server
  - Model Context Protocol
  - AI agents data quality
  - AI data observability
  - Claude MCP
  - data quality automation
lang: en
robots: index, follow
og_title: digna Agentic – AI Agents for Data Quality | digna Documentation
og_description: digna Agentic lets Claude and other AI agents work with digna through the digna MCP Server — answer business questions about your data, investigate alerts and suggest configuration changes.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# digna Agentic – AI Agents for Data Quality

**digna Agentic** was introduced in [Release 2026.11](../../changelog/Release_202611.md) as a beta version.

---

## Purpose

digna measures your data every day and keeps the results: statistics, predictions, rule outcomes and alerts. **digna Agentic** makes that knowledge available to AI agents, so you can work with it in plain language instead of navigating the dashboard.

An AI agent connected to digna can:

- **Answer business questions** about your data from what digna monitors
- **Investigate alerts**, from a red data source down to the single check and value behind it
- **Configure digna**: create data sources, datasets, rules and schedules
- **Suggest improvements** when digna's current configuration can't answer a question

---

## Ask Business Questions

With descriptions on your data sources and attributes, an AI agent understands what your tables contain and can answer questions such as:

- *"Did yesterday's load of the orders table arrive complete?"*
- *"Which regions had unusually low sales last week?"*
- *"Why is the Banking project red today?"*
- *"Is the number of new customers growing compared with last quarter?"*

If digna doesn't measure what a question needs, the agent says so and suggests a change, for example a new dataset that splits the orders table by region. If your role in the project allows it, the agent can apply the change once you agree.

---

## Components

### digna MCP Server

The **digna MCP Server** connects AI agents to digna through the [Model Context Protocol](https://modelcontextprotocol.io), an open standard supported by Claude and many other AI tools. It is part of the digna backend, so there is nothing extra to install. See [Connect an AI Agent](connect_ai_agent.md).

### Descriptions on data sources and attributes

Every data source and attribute has a **Description** field. A plain-language description, such as *"Booked orders, one row per order line, loaded nightly from SAP"*, is what lets an agent connect a business question to the right table and column.

---

## Technical Overview

- **Same permissions as in the dashboard** – An agent signs in with a user's API key and can see and change only what that user can.
- **Monitoring results, not raw data** – The MCP server exposes digna's configuration, statistics and results. It does not give agents access to the rows of your tables.
- **Runs in your environment** – The MCP server is part of your digna installation, on-premises or in your private cloud. Which AI agent connects to it is your choice. What the agent reads from digna is processed by the AI model behind that agent, so choose one your data policies allow.

---

## Related Pages

- [digna Agentic – How It Works](how_it_works.md)
- [Connect an AI Agent](connect_ai_agent.md)
- [Changelog – Release 2026.11](../../changelog/Release_202611.md)

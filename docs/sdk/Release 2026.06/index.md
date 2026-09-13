---
title: digna Python SDK Reference 2026.06 | digna Documentation
description: Complete reference for digna Python SDK release 2026.06
image: /assets/logo_square.png
---

# digna Python SDK Reference 2026.06

This section documents the Python SDK for ***digna***. It is organized as a multi-page reference: use this overview to understand the client, then continue with the dedicated pages for quickstart, resources, models, errors, and generated API documentation.

The SDK is published as the `digna-sdk` package and exposes a stable, versioned client for the ***digna*** REST API.

---

## SDK Basics

---

### Overview

The SDK follows a resource-oriented client design. Each API area is exposed as a first-class client on the top-level `DignaClient`, with typed request and response models and consistent error handling.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Core Features

- **Typed models** — every request and response is validated with pydantic, so your editor and type checker catch mistakes before you hit the network.
- **Resource-oriented** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests`, and `client.inspection_statuses` each expose simple `list` / `get` / `create` / `update` / `delete` methods.
- **Clear errors** — API errors raise `DignaAPIError` (or a more specific subclass like `DignaAuthenticationError`, `DignaAuthorizationError`, or `DignaNotFoundError`) instead of silently returning `None`.

### Installation

```bash
pip install digna-sdk
```

---

## Reference Pages

This release is organized across the following pages:

- [Quickstart](quickstart.md) — connect and make your first calls.
- [Resources](resources.md) — the full list of available resource clients.
- [Models](models.md) — the pydantic models used for input/output.
- [Errors](errors.md) — the exception hierarchy.
- [API Reference](reference.md) — auto-generated reference docs.

---
title: Справочник digna Python SDK 2026.06 | Документация digna
description: Полный справочник по выпуску digna Python SDK 2026.06
image: /assets/logo_square.png
---

# Справочник digna Python SDK 2026.06

В этом разделе описан Python SDK для ***digna***. Он построен как справочник из нескольких страниц: используйте этот обзор, чтобы разобраться в клиенте, а затем переходите к отдельным страницам о быстром старте, ресурсах, моделях, ошибках и сгенерированной документации API.

SDK публикуется в виде пакета `digna-sdk` и предоставляет стабильный версионированный клиент для REST API ***digna***.

---

## Основы SDK

---

### Обзор

SDK построен по принципу клиента, ориентированного на ресурсы. Каждая область API доступна как самостоятельный клиент в объекте верхнего уровня `DignaClient` — с типизированными моделями запросов и ответов и единообразной обработкой ошибок.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Ключевые возможности

- **Типизированные модели** — каждый запрос и каждый ответ проверяются с помощью pydantic, поэтому редактор и средство проверки типов находят ошибки ещё до обращения к сети.
- **Ориентация на ресурсы** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` и `client.inspection_statuses` предоставляют простые методы `list` / `get` / `create` / `update` / `delete`.
- **Понятные ошибки** — ошибки API вызывают исключение `DignaAPIError` (или более конкретный подкласс, например `DignaAuthenticationError`, `DignaAuthorizationError` либо `DignaNotFoundError`) вместо того, чтобы молча возвращать `None`.

### Установка

```bash
pip install digna-sdk
```

---

## Страницы справочника

Этот выпуск разделён на следующие страницы:

- [Быстрый старт](quickstart.md) — подключение и первые вызовы.
- [Ресурсы](resources.md) — полный список доступных клиентов ресурсов.
- [Модели](models.md) — модели pydantic, используемые для ввода и вывода.
- [Ошибки](errors.md) — иерархия исключений.
- [Справочник API](reference.md) — автоматически сгенерированная справочная документация.

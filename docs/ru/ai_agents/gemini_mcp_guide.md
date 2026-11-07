---
title: Gemini – подключение Antigravity и Gemini CLI к digna через MCP | digna Documentation
description: Подключите инструменты Gemini от Google к digna через digna MCP Server — Antigravity CLI, IDE и приложение с mcp_config.json, а также Gemini CLI с settings.json или gemini mcp add, с ключом API в заголовке Authorization.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, ключ API digna
---

# Подключение Gemini к digna

Это руководство подключает инструменты Gemini от Google к **digna MCP Server**. Вам понадобятся
конечная точка MCP вашей инсталляции *digna* и ключ API, как описано в [обзоре ИИ-агентов](overview.md).

В примерах в качестве конечной точки используется `https://digna.example.com/mcp`. Замените её на
свою.

## Выберите инструмент {: #choose-your-tool }

| Инструмент | Для кого | Конфигурация |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE и приложение | Агентные инструменты Google. Antigravity CLI заменил Gemini CLI для личных аккаунтов Google в июне 2026 года | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Лицензии Gemini Code Assist Standard и Enterprise, а также платные ключи Gemini API | `settings.json` или `gemini mcp add` |
| Приложение Gemini Enterprise | — | Не поддерживается. Его пользовательский коннектор MCP выполняет вход через OAuth или сервисный аккаунт Google Cloud, а digna MCP Server выполняет аутентификацию по ключам API |

Все эти инструменты подключаются с машины, на которой работают, поэтому они работают с *digna*
внутри корпоративной сети, если эта машина может достичь конечной точки.

---

## Antigravity {: #antigravity }

Antigravity читает свои серверы MCP из `mcp_config.json`, общего для CLI, IDE и приложения.

### 1. Откройте mcp_config.json {: #1-open-mcp-config-json }

| Область | Файл |
|---|---|
| Все ваши проекты | `~/.gemini/config/mcp_config.json` |
| Одно рабочее пространство | `.agents/mcp_config.json` в рабочем пространстве |

Чтобы открыть используемый файл:

- **CLI**: введите `/mcp` и нажмите ++enter++, чтобы открыть менеджер MCP.
- **IDE**: на боковой панели агента откройте меню **…**, выберите **MCP Servers**, затем
  **Manage MCP Servers**, затем **View raw config**.
- **Приложение**: перейдите в **Customizations** > **Installed** > **MCP Servers** и воспользуйтесь
  **Copy Config File Path**.

### 2. Добавьте сервер digna {: #2-add-the-digna-server }

Добавьте запись `digna`. Если в файле уже есть раздел `mcpServers`, добавьте её туда:

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

Antigravity обращается к удалённым серверам только по streamable HTTP, который использует digna
MCP Server. Указывайте конечную точку как `serverUrl`; ключ `httpUrl` из Gemini CLI не
поддерживается.

### 3. Проверьте подключение {: #3-verify-the-connection }

В CLI введите `/mcp`: менеджер MCP показывает сервер `digna` с его состоянием и инструментами, а
также может перезагрузить конфигурацию и показать журналы подключения. В IDE сервер появляется в
**Manage MCP Servers**.

!!! warning "Защитите файл"

    `mcp_config.json` хранит ключ API в открытом виде. Не добавляйте файл рабочего пространства
    `.agents/mcp_config.json` в систему контроля версий, а глобальный файл разрешите читать только
    своей учётной записи.

---

## Gemini CLI {: #gemini-cli }

### 1. Добавьте сервер {: #1-add-the-server }

Поместите ключ API в переменную окружения, затем добавьте сервер:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Командная оболочка подставляет `$DIGNA_API_KEY` при выполнении команды, поэтому Gemini CLI
сохраняет ключ в своих настройках. Без `--scope user` сервер добавляется только в текущий проект.

### 2. Или отредактируйте settings.json {: #2-or-edit-settings-json }

Приведённая выше команда записывает данные в `settings.json`. Чтобы отредактировать файл
самостоятельно:

| Область | Файл |
|---|---|
| Все ваши проекты | `~/.gemini/settings.json` |
| Один проект | `.gemini/settings.json` в проекте |

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

Используйте `httpUrl` — ключ для streamable HTTP. Похожий ключ `url` выбирает более старый
транспорт SSE, который digna MCP Server не поддерживает. Не используйте символы подчёркивания в
имени сервера.

!!! tip "Не включайте trust"

    Gemini CLI запрашивает подтверждение перед каждым вызовом инструмента, если для сервера не
    задано `"trust": true`. Не включайте `trust` для *digna*, чтобы подтверждать каждое изменение,
    которое агент вносит в вашу конфигурацию.

### 3. Проверьте подключение {: #3-verify-the-connection-gemini-cli }

В командной оболочке:

```bash
gemini mcp list
```

Сервер `digna` должен отображаться как подключённый. В сеансе Gemini CLI выполните `/mcp`, чтобы
увидеть сервер и его инструменты.

---

## Устранение неполадок Gemini {: #troubleshooting-gemini }

### Сервер отображается как отключённый

- Проверьте, что конечная точка заканчивается на `/mcp` и доступна с вашей машины.
- Проверьте имя ключа: `serverUrl` в Antigravity, `httpUrl` в Gemini CLI.
- `401` означает, что ключ отклонён; см. [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI больше не запускается для моего аккаунта

С июня 2026 года личные аккаунты Google используют Antigravity CLI вместо Gemini CLI. Перенесите
запись `digna` в `mcp_config.json`, как описано в разделе [Antigravity](#antigravity), и
переименуйте `httpUrl` в `serverUrl`.

---

## См. также {: #see-also }

- [Обзор ИИ-агентов](overview.md): конечная точка, ключ API, безопасность и общее устранение неполадок
- [Claude](claude_mcp_guide.md): подключение Claude Code, Claude Desktop или пользовательского коннектора
- [digna Agentic](../platform/agentic/Introduction.md): что ИИ-агенты могут делать с *digna*

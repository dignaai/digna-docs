---
title: Gemini – підключення Antigravity і Gemini CLI до digna через MCP | Документація digna
description: Підключіть інструменти Gemini від Google до digna через digna MCP Server — Antigravity CLI, IDE і застосунок з mcp_config.json, а також Gemini CLI з settings.json або gemini mcp add, з ключем API в заголовку Authorization.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, ключ API digna
---

# Підключення Gemini до digna

Цей посібник підключає інструменти Gemini від Google до **digna MCP Server**. Вам потрібні кінцева
точка MCP вашої інсталяції *digna* і ключ API, як описано в [Огляді ШІ-агентів](overview.md).

У прикладах як кінцеву точку використано `https://digna.example.com/mcp`. Замініть її на свою.

## Виберіть інструмент {: #choose-your-tool }

| Інструмент | Для кого | Конфігурація |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE і застосунок | Агентні інструменти Google. Antigravity CLI замінив Gemini CLI для особистих облікових записів Google у червні 2026 року | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Ліцензії Gemini Code Assist Standard і Enterprise, а також платні ключі Gemini API | `settings.json` або `gemini mcp add` |
| Застосунок Gemini Enterprise | — | Не підтримується. Його власний конектор MCP входить через OAuth або сервісний обліковий запис Google Cloud, а digna MCP Server автентифікує за допомогою ключів API |

Усі ці інструменти підключаються з машини, на якій працюють, тож вони працюють з *digna* у
корпоративній мережі, якщо ця машина може дістатися кінцевої точки.

---

## Antigravity {: #antigravity }

Antigravity читає свої сервери MCP з `mcp_config.json`, спільного для CLI, IDE і застосунку.

### 1. Відкрийте mcp_config.json {: #1-open-mcp-config-json }

| Область | Файл |
|---|---|
| Усі ваші проєкти | `~/.gemini/config/mcp_config.json` |
| Один робочий простір | `.agents/mcp_config.json` у робочому просторі |

Щоб відкрити файл, який використовується:

- **CLI**: введіть `/mcp` і натисніть ++enter++, щоб відкрити менеджер MCP.
- **IDE**: на бічній панелі агента відкрийте меню **…**, виберіть **MCP Servers**, потім
  **Manage MCP Servers**, потім **View raw config**.
- **Застосунок**: перейдіть до **Customizations** > **Installed** > **MCP Servers** і скористайтеся
  **Copy Config File Path**.

### 2. Додайте сервер digna {: #2-add-the-digna-server }

Додайте запис `digna`. Якщо у файлі вже є розділ `mcpServers`, додайте його туди:

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

Antigravity звертається до віддалених серверів лише через streamable HTTP, який використовує digna
MCP Server. Вказуйте кінцеву точку як `serverUrl`; ключ `httpUrl` із Gemini CLI не підтримується.

### 3. Перевірте підключення {: #3-verify-the-connection }

У CLI введіть `/mcp`: менеджер MCP показує сервер `digna` з його станом та інструментами, а також
може перезавантажити конфігурацію й показати журнали підключення. В IDE сервер з'являється в
**Manage MCP Servers**.

!!! warning "Захистіть файл"

    `mcp_config.json` зберігає ключ API відкритим текстом. Не додавайте файл робочого простору
    `.agents/mcp_config.json` до системи контролю версій, а глобальний файл дозвольте читати лише
    своєму обліковому запису.

---

## Gemini CLI {: #gemini-cli }

### 1. Додайте сервер {: #1-add-the-server }

Запишіть ключ API у змінну середовища, а потім додайте сервер:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Командна оболонка підставляє `$DIGNA_API_KEY` під час виконання команди, тож Gemini CLI зберігає
ключ у своїх налаштуваннях. Без `--scope user` сервер додається лише до поточного проєкту.

### 2. Або відредагуйте settings.json {: #2-or-edit-settings-json }

Наведена вище команда записує дані в `settings.json`. Щоб відредагувати файл самостійно:

| Область | Файл |
|---|---|
| Усі ваші проєкти | `~/.gemini/settings.json` |
| Один проєкт | `.gemini/settings.json` у проєкті |

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

Використовуйте `httpUrl` — ключ для streamable HTTP. Схожий ключ `url` вибирає старіший транспорт
SSE, якого digna MCP Server не пропонує. Не використовуйте символи підкреслення в назві сервера.

!!! tip "Не вмикайте trust"

    Gemini CLI запитує підтвердження перед кожним викликом інструмента, якщо для сервера не задано
    `"trust": true`. Не вмикайте `trust` для *digna*, щоб підтверджувати кожну зміну, яку агент
    вносить у вашу конфігурацію.

### 3. Перевірте підключення {: #3-verify-the-connection-gemini-cli }

У командній оболонці:

```bash
gemini mcp list
```

Сервер `digna` має бути показаний як підключений. У сеансі Gemini CLI виконайте `/mcp`, щоб
побачити сервер і його інструменти.

---

## Усунення несправностей Gemini {: #troubleshooting-gemini }

### Сервер показано як відключений

- Перевірте, чи кінцева точка закінчується на `/mcp` і чи доступна вона з вашої машини.
- Перевірте назву ключа: `serverUrl` в Antigravity, `httpUrl` у Gemini CLI.
- `401` означає, що ключ відхилено; див. [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI більше не запускається для мого облікового запису

З червня 2026 року особисті облікові записи Google використовують Antigravity CLI замість Gemini
CLI. Перенесіть запис `digna` до `mcp_config.json`, як описано в розділі [Antigravity](#antigravity),
і перейменуйте `httpUrl` на `serverUrl`.

---

## Див. також {: #see-also }

- [Огляд ШІ-агентів](overview.md): кінцева точка, ключ API, безпека та загальне усунення несправностей
- [Claude](claude_mcp_guide.md): підключення Claude Code, Claude Desktop або власного конектора
- [digna Agentic](../platform/agentic/Introduction.md): що ШІ-агенти можуть робити з *digna*

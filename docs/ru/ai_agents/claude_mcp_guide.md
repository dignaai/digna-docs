---
title: Claude – подключение Claude к digna через MCP | digna Documentation
description: Подключите Claude к digna через digna MCP Server — Claude Code из командной строки или через общий .mcp.json, Claude Desktop с локальным мостом и пользовательские коннекторы в claude.ai, с ключом API в заголовке Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, пользовательский коннектор claude.ai, digna MCP server, mcp-remote, Authorization Bearer, ключ API digna
---

# Подключение Claude к digna

Это руководство подключает Claude к **digna MCP Server**. Вам понадобятся конечная точка MCP вашей
инсталляции *digna* и ключ API, как описано в [обзоре ИИ-агентов](overview.md).

В примерах в качестве конечной точки используется `https://digna.example.com/mcp`. Замените её на
свою.

## Выберите способ подключения {: #choose-how-to-connect }

| Продукт Claude | Откуда подключается | Работает с *digna* внутри вашей сети |
|---|---|---|
| [Claude Code](#claude-code) | Ваша машина | Да |
| [Claude Desktop с локальным мостом](#claude-desktop-with-a-local-bridge) | Ваша машина | Да |
| [Пользовательский коннектор](#custom-connector) в claude.ai, Claude Desktop и Claude mobile | Облако Anthropic | Нет. Конечная точка должна быть доступна из интернета |

Для инсталляции *digna*, работающей внутри корпоративной сети, используйте Claude Code или Claude
Desktop с локальным мостом.

---

## Claude Code {: #claude-code }

### 1. Добавьте сервер {: #1-add-the-server }

Поместите ключ API в переменную окружения, затем добавьте сервер:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Командная оболочка подставляет `$DIGNA_API_KEY` при выполнении команды, поэтому Claude Code
сохраняет ключ в собственной конфигурации.

`--scope` определяет, где доступен сервер:

| Область | Доступен |
|---|---|
| `local` (по умолчанию) | Вам, только в текущем проекте |
| `user` | Вам, в каждом проекте |
| `project` | Всем, кто работает в проекте, через файл `.mcp.json` в проекте |

### 2. Предоставьте сервер команде (необязательно) {: #2-share-the-server-with-your-team }

Чтобы у всех участников проекта был один и тот же сервер, добавьте файл `.mcp.json` в корень
проекта. Не записывайте ключ в файл. Claude Code подставляет `${DIGNA_API_KEY}` из окружения
каждого человека:

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

Каждый задаёт в `DIGNA_API_KEY` собственный ключ. Когда Claude Code впервые находит этот файл, он
спрашивает, использовать ли серверы из него.

### 3. Проверьте подключение {: #3-verify-the-connection }

В командной оболочке:

```bash
claude mcp list
```

Сервер `digna` должен показывать `✔ Connected`. В сеансе Claude Code выполните `/mcp`, чтобы
увидеть сервер и его инструменты.

---

## Claude Desktop с локальным мостом {: #claude-desktop-with-a-local-bridge }

Файл конфигурации Claude Desktop запускает локальные серверы MCP на вашей машине. Небольшой мост —
пакет с открытым исходным кодом [`mcp-remote`](https://github.com/geelen/mcp-remote) — работает там
и пересылает каждый запрос на конечную точку *digna* с вашим ключом API. Поскольку мост работает на
вашей машине, этот способ подходит для *digna* внутри корпоративной сети.

!!! note "Пакет сообщества"

    `mcp-remote` поддерживается сообществом открытого исходного кода, а не Anthropic или digna.
    Прежде чем его использовать, убедитесь, что ваша организация это разрешает.

### 1. Установите Node.js {: #1-install-nodejs }

Мосту нужен [Node.js](https://nodejs.org) версии 18 или новее. Claude Desktop использует версию
Node.js, установленную в вашей системе. Проверьте её командой:

```bash
node --version
```

### 2. Отредактируйте файл конфигурации {: #2-edit-the-configuration-file }

Откройте `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Добавьте сервер `digna`. Если в файле уже есть раздел `mcpServers`, добавьте запись `digna` в него:

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

!!! warning "Оставьте заголовок точно таким, как показано"

    Пишите `Authorization:${AUTH_HEADER}` без пробелов, а `Bearer <api key>` поместите в `env`.
    Claude Desktop в Windows не экранирует пробелы внутри `args`, поэтому пробел там ломает
    заголовок.

### 3. Перезапустите Claude Desktop {: #3-restart-claude-desktop }

Полностью закройте Claude Desktop и запустите его снова. В новом чате нажмите **+** и откройте
**Connectors**: `digna` должен быть в списке и включён.

---

## Пользовательский коннектор {: #custom-connector }

Пользовательский коннектор делает *digna* доступной в claude.ai, Claude Desktop и мобильных
приложениях Claude без какой-либо локальной настройки. К конечной точке подключается облако
Anthropic, поэтому это работает только при следующих условиях:

- Конечная точка *digna* доступна из интернета по HTTPS
- В вашей организации Claude есть параметр **Request headers** в диалоговом окне
  **Add custom connector**. Anthropic предлагает его в виде беты ограниченному кругу организаций

!!! warning "Не для digna внутри вашей сети"

    Туннели MCP от Claude, которые достигают серверов в частной сети, требуют OAuth на сервере MCP.
    digna MCP Server выполняет аутентификацию по ключам API, поэтому туннель использовать нельзя.
    Вместо этого используйте [Claude Code](#claude-code) или [Claude Desktop с локальным мостом](#claude-desktop-with-a-local-bridge).

### 1. Откройте настройки коннекторов {: #1-open-the-connector-settings }

- **Тарифы Free, Pro, Max и Ultra**: перейдите в **Customize > Connectors** и нажмите
  **Add custom connector**.
- **Тарифы Team и Enterprise**: владелец (Owner) переходит в **Organization settings > Connectors**,
  нажимает **Add**, затем **Custom** и, если запрашивается тип, выбирает **Web**.

### 2. Введите данные коннектора {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: выберите `authorization` в качестве имени заголовка, введите
   `Bearer <api key>` в качестве значения, вместе со словом `Bearer` и пробелом, и отметьте его как
   **Required**.
4. Нажмите **Add**.

!!! warning "Все используют один ключ"

    Каждый участник, который пользуется коннектором, работает с одним и тем же ключом API, а
    значит, с одним и тем же пользователем *digna*. Создайте для коннектора отдельного пользователя
    *digna* и предоставьте ему только те проекты и роли, которые могут быть у всех, например роль
    читателя.

В тарифах Team и Enterprise участники затем подключаются в **Customize > Connectors**, где
коннектор отмечен меткой **Custom**.

Claude не может изменить заголовок существующего коннектора. Чтобы использовать новый ключ,
удалите коннектор и добавьте его снова.

---

## Устранение неполадок Claude {: #troubleshooting-claude }

### claude mcp list показывает Failed to connect

Выполните `claude mcp get digna`, чтобы увидеть причину. `401` означает, что ключ отклонён; см.
[401 Unauthorized](overview.md#troubleshooting). Claude Code также предупреждает о пробелах или
переносе строки в начале или в конце ключа, которые часто появляются при копировании.

### digna не появляется в Claude Desktop

- Проверьте, установлен ли Node.js 18 или новее: `node --version`.
- Проверьте, что `claude_desktop_config.json` содержит корректный JSON. Пропущенная запятая не
  даёт загрузиться ни одному серверу из файла.
- Полностью закройте Claude Desktop, а не только окно, и запустите его снова.

### Пользовательский коннектор не может достичь сервера

Облако Anthropic не может достичь конечной точки. Проверьте, что она доступна из интернета по
HTTPS с действительным сертификатом, или подключитесь вместо этого через [Claude Code](#claude-code).

---

## См. также {: #see-also }

- [Обзор ИИ-агентов](overview.md): конечная точка, ключ API, безопасность и общее устранение неполадок
- [Gemini](gemini_mcp_guide.md): подключение Antigravity или Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): что ИИ-агенты могут делать с *digna*

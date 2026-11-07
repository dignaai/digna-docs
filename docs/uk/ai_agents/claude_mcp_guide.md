---
title: Claude – підключення Claude до digna через MCP | Документація digna
description: Підключіть Claude до digna через digna MCP Server — Claude Code з командного рядка або через спільний .mcp.json, Claude Desktop з локальним мостом і власні конектори в claude.ai, з ключем API в заголовку Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, власний конектор claude.ai, digna MCP server, mcp-remote, Authorization Bearer, ключ API digna
---

# Підключення Claude до digna

Цей посібник підключає Claude до **digna MCP Server**. Вам потрібні кінцева точка MCP вашої
інсталяції *digna* і ключ API, як описано в [Огляді ШІ-агентів](overview.md).

У прикладах як кінцеву точку використано `https://digna.example.com/mcp`. Замініть її на свою.

## Виберіть спосіб підключення {: #choose-how-to-connect }

| Продукт Claude | Звідки підключається | Працює з *digna* у вашій мережі |
|---|---|---|
| [Claude Code](#claude-code) | Ваша машина | Так |
| [Claude Desktop з локальним мостом](#claude-desktop-with-a-local-bridge) | Ваша машина | Так |
| [Власний конектор](#custom-connector) у claude.ai, Claude Desktop і Claude mobile | Хмара Anthropic | Ні. Кінцева точка має бути доступна з інтернету |

Для інсталяції *digna*, що працює в корпоративній мережі, використовуйте Claude Code або Claude
Desktop з локальним мостом.

---

## Claude Code {: #claude-code }

### 1. Додайте сервер {: #1-add-the-server }

Запишіть ключ API у змінну середовища, а потім додайте сервер:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Командна оболонка підставляє `$DIGNA_API_KEY` під час виконання команди, тож Claude Code зберігає
ключ у власній конфігурації.

`--scope` визначає, де доступний сервер:

| Область | Доступний |
|---|---|
| `local` (за замовчуванням) | Вам, лише в поточному проєкті |
| `user` | Вам, у кожному проєкті |
| `project` | Усім, хто працює в проєкті, через файл `.mcp.json` у проєкті |

### 2. Надайте сервер своїй команді (необов'язково) {: #2-share-the-server-with-your-team }

Щоб усі учасники проєкту мали той самий сервер, додайте файл `.mcp.json` у корінь проєкту. Не
записуйте ключ у файл. Claude Code підставляє `${DIGNA_API_KEY}` із середовища кожної людини:

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

Кожна людина задає в `DIGNA_API_KEY` власний ключ. Коли Claude Code уперше знаходить цей файл, він
запитує, чи використовувати сервери з нього.

### 3. Перевірте підключення {: #3-verify-the-connection }

У командній оболонці:

```bash
claude mcp list
```

Сервер `digna` має показувати `✔ Connected`. У сеансі Claude Code виконайте `/mcp`, щоб побачити
сервер і його інструменти.

---

## Claude Desktop з локальним мостом {: #claude-desktop-with-a-local-bridge }

Файл конфігурації Claude Desktop запускає локальні сервери MCP на вашій машині. Невеликий міст —
пакет з відкритим кодом [`mcp-remote`](https://github.com/geelen/mcp-remote) — працює там і
пересилає кожен запит до кінцевої точки *digna* з вашим ключем API. Оскільки міст працює на вашій
машині, цей спосіб підходить для *digna* у корпоративній мережі.

!!! note "Пакет спільноти"

    `mcp-remote` підтримує спільнота відкритого коду, а не Anthropic чи digna. Перш ніж його
    використовувати, переконайтеся, що ваша організація це дозволяє.

### 1. Встановіть Node.js {: #1-install-nodejs }

Мостові потрібен [Node.js](https://nodejs.org) версії 18 або новішої. Claude Desktop використовує
версію Node.js, встановлену у вашій системі. Перевірте її командою:

```bash
node --version
```

### 2. Відредагуйте файл конфігурації {: #2-edit-the-configuration-file }

Відкрийте `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Додайте сервер `digna`. Якщо у файлі вже є розділ `mcpServers`, додайте запис `digna` до нього:

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

!!! warning "Залиште заголовок точно таким, як показано"

    Пишіть `Authorization:${AUTH_HEADER}` без пробілів, а `Bearer <api key>` розмістіть в `env`.
    Claude Desktop у Windows не екранує пробіли всередині `args`, тож пробіл там ламає заголовок.

### 3. Перезапустіть Claude Desktop {: #3-restart-claude-desktop }

Повністю закрийте Claude Desktop і запустіть його знову. У новому чаті натисніть **+** і відкрийте
**Connectors**: `digna` має бути в списку й увімкнений.

---

## Власний конектор {: #custom-connector }

Власний конектор робить *digna* доступною в claude.ai, Claude Desktop і мобільних застосунках
Claude без жодного локального налаштування. До кінцевої точки підключається хмара Anthropic, тож
це працює лише за таких умов:

- Кінцева точка *digna* доступна з інтернету через HTTPS
- У вашій організації Claude є параметр **Request headers** у діалоговому вікні
  **Add custom connector**. Anthropic пропонує його як бета-функцію обмеженому колу організацій

!!! warning "Не для digna у вашій мережі"

    Тунелі MCP від Claude, що дістаються серверів у приватній мережі, вимагають OAuth на сервері
    MCP. digna MCP Server автентифікує за допомогою ключів API, тому тунель використати не можна.
    Натомість використовуйте [Claude Code](#claude-code) або [Claude Desktop з локальним мостом](#claude-desktop-with-a-local-bridge).

### 1. Відкрийте налаштування конекторів {: #1-open-the-connector-settings }

- **Тарифи Free, Pro, Max і Ultra**: перейдіть до **Customize > Connectors** і натисніть
  **Add custom connector**.
- **Тарифи Team і Enterprise**: власник (Owner) переходить до **Organization settings > Connectors**,
  натискає **Add**, потім **Custom** і, якщо буде запит типу, вибирає **Web**.

### 2. Введіть дані конектора {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: виберіть `authorization` як назву заголовка, введіть `Bearer <api key>`
   як значення, разом зі словом `Bearer` і пробілом, і позначте його як **Required**.
4. Натисніть **Add**.

!!! warning "Усі використовують один ключ"

    Кожен учасник, який користується конектором, працює з тим самим ключем API, а отже, з тим
    самим користувачем *digna*. Створіть для конектора окремого користувача *digna* і надайте йому
    лише ті проєкти й ролі, які можуть мати всі, наприклад роль читача.

У тарифах Team і Enterprise учасники потім підключаються в **Customize > Connectors**, де конектор
має позначку **Custom**.

Claude не може змінити заголовок наявного конектора. Щоб використати новий ключ, видаліть конектор
і додайте його знову.

---

## Усунення несправностей Claude {: #troubleshooting-claude }

### claude mcp list показує Failed to connect

Виконайте `claude mcp get digna`, щоб побачити причину. `401` означає, що ключ відхилено; див.
[401 Unauthorized](overview.md#troubleshooting). Claude Code також попереджає про пробіли або
розрив рядка на початку чи в кінці ключа, які часто з'являються під час копіювання.

### digna не з'являється в Claude Desktop

- Перевірте, чи встановлено Node.js 18 або новіший: `node --version`.
- Перевірте, чи `claude_desktop_config.json` містить коректний JSON. Пропущена кома не дає
  завантажитися жодному серверу з файлу.
- Повністю закрийте Claude Desktop, а не лише вікно, і запустіть його знову.

### Власний конектор не може дістатися сервера

Хмара Anthropic не може дістатися кінцевої точки. Перевірте, чи вона доступна з інтернету через
HTTPS із дійсним сертифікатом, або підключіться натомість через [Claude Code](#claude-code).

---

## Див. також {: #see-also }

- [Огляд ШІ-агентів](overview.md): кінцева точка, ключ API, безпека та загальне усунення несправностей
- [Gemini](gemini_mcp_guide.md): підключення Antigravity або Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): що ШІ-агенти можуть робити з *digna*

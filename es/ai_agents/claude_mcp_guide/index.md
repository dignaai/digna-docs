# Conectar Claude a digna

Esta guía conecta Claude al **digna MCP Server**. Necesitas el endpoint MCP de tu instalación de
*digna* y una clave de API, como se describe en la
[descripción general de agentes de IA](overview.md).

Los ejemplos usan `https://digna.example.com/mcp` como endpoint. Sustitúyelo por el tuyo.

## Elegir cómo conectarse {: #choose-how-to-connect }

| Producto de Claude | Se conecta desde | Funciona con *digna* dentro de tu red |
|---|---|---|
| [Claude Code](#claude-code) | Tu máquina | Sí |
| [Claude Desktop con un puente local](#claude-desktop-with-a-local-bridge) | Tu máquina | Sí |
| [Conector personalizado](#custom-connector) en claude.ai, Claude Desktop y Claude para móvil | La nube de Anthropic | No. El endpoint debe ser accesible desde Internet |

Para una instalación de *digna* que se ejecuta dentro de la red de tu empresa, usa Claude Code o
Claude Desktop con un puente local.

---

## Claude Code {: #claude-code }

### 1. Añadir el servidor {: #1-add-the-server }

Guarda la clave de API en una variable de entorno y después añade el servidor:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Tu shell sustituye `$DIGNA_API_KEY` por su valor al ejecutar el comando, de modo que Claude Code
guarda la clave en su propia configuración.

`--scope` decide dónde está disponible el servidor:

| Ámbito | Disponible |
|---|---|
| `local` (predeterminado) | Para ti, solo en el proyecto actual |
| `user` | Para ti, en todos los proyectos |
| `project` | Para todas las personas que trabajan en el proyecto, mediante un archivo `.mcp.json` en el proyecto |

### 2. Compartir el servidor con tu equipo (opcional) {: #2-share-the-server-with-your-team }

Para dar a todas las personas de un proyecto el mismo servidor, añade un archivo `.mcp.json` en la
raíz del proyecto. No escribas la clave en el archivo. Claude Code sustituye `${DIGNA_API_KEY}` con el
valor del entorno de cada persona:

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

Cada persona asigna a `DIGNA_API_KEY` su propia clave. La primera vez que Claude Code encuentra el
archivo, pregunta si debe usar los servidores que contiene.

### 3. Verificar la conexión {: #3-verify-the-connection }

Desde tu shell:

```bash
claude mcp list
```

El servidor `digna` debe mostrar `✔ Connected`. Dentro de una sesión de Claude Code, ejecuta `/mcp`
para ver el servidor y sus herramientas.

---

## Claude Desktop con un puente local {: #claude-desktop-with-a-local-bridge }

El archivo de configuración de Claude Desktop inicia servidores MCP locales en tu máquina. Un pequeño
puente, el paquete de código abierto [`mcp-remote`](https://github.com/geelen/mcp-remote), se
ejecuta allí y reenvía cada petición al endpoint de *digna* con tu clave de API. Como el puente se
ejecuta en tu máquina, esto funciona con *digna* dentro de la red de tu empresa.

!!! note "Un paquete de la comunidad"

    `mcp-remote` lo mantiene su comunidad de código abierto, no Anthropic ni digna. Comprueba que tu
    organización lo permite antes de usarlo.

### 1. Instalar Node.js {: #1-install-nodejs }

El puente necesita [Node.js](https://nodejs.org) 18 o posterior. Claude Desktop usa la versión de
Node.js instalada en tu sistema. Compruébala con:

```bash
node --version
```

### 2. Editar el archivo de configuración {: #2-edit-the-configuration-file }

Abre `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Añade el servidor `digna`. Si el archivo ya tiene una sección `mcpServers`, añade en ella la entrada
`digna`:

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

!!! warning "Escribe el encabezado exactamente como se muestra"

    Escribe `Authorization:${AUTH_HEADER}` sin espacios y pon `Bearer <api key>` en `env`. Claude
    Desktop en Windows no escapa los espacios dentro de `args`, así que un espacio ahí rompe el
    encabezado.

### 3. Reiniciar Claude Desktop {: #3-restart-claude-desktop }

Cierra Claude Desktop por completo y vuelve a iniciarlo. En un chat nuevo, haz clic en **+** y abre
**Connectors**: `digna` debe aparecer en la lista y estar activado.

---

## Conector personalizado {: #custom-connector }

Un conector personalizado hace que *digna* esté disponible en claude.ai, Claude Desktop y las
aplicaciones móviles de Claude sin ninguna configuración local. La nube de Anthropic se conecta al
endpoint, así que esto solo funciona cuando:

- El endpoint de *digna* es accesible desde Internet mediante HTTPS
- Tu organización de Claude tiene la opción **Request headers** en el diálogo
  **Add custom connector**. Anthropic la ofrece como beta a un número limitado de organizaciones

!!! warning "No para digna dentro de tu red"

    Los túneles MCP de Claude, que llegan a servidores dentro de una red privada, requieren OAuth en
    el servidor MCP. El digna MCP Server se autentica con claves de API, así que no se puede usar un
    túnel. Usa en su lugar [Claude Code](#claude-code) o
    [Claude Desktop con un puente local](#claude-desktop-with-a-local-bridge).

### 1. Abrir la configuración de conectores {: #1-open-the-connector-settings }

- **Planes Free, Pro, Max y Ultra**: ve a **Customize > Connectors** y haz clic en
  **Add custom connector**.
- **Planes Team y Enterprise**: un Owner va a **Organization settings > Connectors**, hace clic en
  **Add**, después en **Custom**, y elige **Web** si se le pregunta por el tipo.

### 2. Introducir los datos del conector {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: elige `authorization` como nombre del encabezado, introduce
   `Bearer <api key>` como valor, incluida la palabra `Bearer` y el espacio, y márcalo como
   **Required**.
4. Haz clic en **Add**.

!!! warning "Todos comparten la clave"

    Todos los miembros que usan el conector trabajan con la misma clave de API y, por tanto, con el
    mismo usuario de *digna*. Crea un usuario de *digna* dedicado para el conector y dale solo los
    proyectos y roles que todos puedan tener, p. ej. el rol de lector.

En los planes Team y Enterprise, los miembros se conectan después en **Customize > Connectors**,
donde el conector lleva la etiqueta **Custom**.

Claude no puede cambiar el encabezado de un conector existente. Para usar una clave nueva, elimina el
conector y vuelve a añadirlo.

---

## Solución de problemas de Claude {: #troubleshooting-claude }

### claude mcp list muestra Failed to connect

Ejecuta `claude mcp get digna` para ver el motivo. Un `401` significa que la clave fue rechazada;
consulta [401 Unauthorized](overview.md#troubleshooting). Claude Code también avisa de espacios o de
un salto de línea al principio o al final de la clave, que suelen colarse al copiarla.

### digna no aparece en Claude Desktop

- Comprueba que Node.js 18 o posterior está instalado: `node --version`.
- Comprueba que `claude_desktop_config.json` es un JSON válido. Una coma que falta impide que se
  cargue cualquier servidor del archivo.
- Cierra Claude Desktop por completo, no solo la ventana, y vuelve a iniciarlo.

### El conector personalizado no llega al servidor

La nube de Anthropic no llega al endpoint. Comprueba que es accesible desde Internet mediante HTTPS
con un certificado válido, o conéctate en su lugar a través de [Claude Code](#claude-code).

---

## Ver también {: #see-also }

- [Descripción general de agentes de IA](overview.md): endpoint, clave de API, seguridad y solución de problemas general
- [Gemini](gemini_mcp_guide.md): conectar Antigravity o Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): lo que los agentes de IA pueden hacer con *digna*
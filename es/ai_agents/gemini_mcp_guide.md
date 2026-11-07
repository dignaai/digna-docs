# Conectar Gemini a digna

Esta guía conecta las herramientas Gemini de Google al **digna MCP Server**. Necesitas el endpoint
MCP de tu instalación de *digna* y una clave de API, como se describe en la
[descripción general de agentes de IA](overview.md).

Los ejemplos usan `https://digna.example.com/mcp` como endpoint. Sustitúyelo por el tuyo.

## Elegir tu herramienta {: #choose-your-tool }

| Herramienta | Para | Configuración |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE y aplicación | Las herramientas de agentes de Google. Antigravity CLI sustituyó a Gemini CLI para las cuentas de Google individuales en junio de 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Licencias de Gemini Code Assist Standard y Enterprise, y claves de API de Gemini de pago | `settings.json` o `gemini mcp add` |
| Aplicación Gemini Enterprise | — | No compatible. Su conector MCP personalizado inicia sesión con OAuth o con una cuenta de servicio de Google Cloud, mientras que el digna MCP Server se autentica con claves de API |

Todas estas herramientas se conectan desde la máquina en la que se ejecutan, así que funcionan con
*digna* dentro de la red de tu empresa siempre que esa máquina llegue al endpoint.

---

## Antigravity {: #antigravity }

Antigravity lee sus servidores MCP de `mcp_config.json`, que comparten la CLI, el IDE y la
aplicación.

### 1. Abrir mcp_config.json {: #1-open-mcp-config-json }

| Ámbito | Archivo |
|---|---|
| Todos tus proyectos | `~/.gemini/config/mcp_config.json` |
| Un espacio de trabajo | `.agents/mcp_config.json` en el espacio de trabajo |

Para abrir el archivo en uso:

- **CLI**: escribe `/mcp` y pulsa ++enter++ para abrir el gestor de MCP.
- **IDE**: en el panel lateral del agente, abre el menú **…**, selecciona **MCP Servers**, después
  **Manage MCP Servers** y después **View raw config**.
- **Aplicación**: ve a **Customizations** > **Installed** > **MCP Servers** y usa
  **Copy Config File Path**.

### 2. Añadir el servidor de digna {: #2-add-the-digna-server }

Añade la entrada `digna`. Si el archivo ya tiene una sección `mcpServers`, añádela ahí:

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

Antigravity solo llega a servidores remotos mediante HTTP con streaming, que es lo que usa el digna
MCP Server. Escribe el endpoint como `serverUrl`; la clave `httpUrl` de Gemini CLI no es compatible.

### 3. Verificar la conexión {: #3-verify-the-connection }

En la CLI, escribe `/mcp`: el gestor de MCP muestra el servidor `digna` con su estado y sus
herramientas, y puede recargar la configuración y mostrar los registros de conexión. En el IDE, el
servidor aparece en **Manage MCP Servers**.

!!! warning "Protege el archivo"

    `mcp_config.json` guarda la clave de API en texto plano. Mantén un archivo de espacio de trabajo
    `.agents/mcp_config.json` fuera del control de versiones, y permite que solo tu propia cuenta lea
    el archivo global.

---

## Gemini CLI {: #gemini-cli }

### 1. Añadir el servidor {: #1-add-the-server }

Guarda la clave de API en una variable de entorno y después añade el servidor:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Tu shell sustituye `$DIGNA_API_KEY` por su valor al ejecutar el comando, de modo que Gemini CLI
guarda la clave en su configuración. Sin `--scope user`, el servidor solo se añade al proyecto
actual.

### 2. O editar settings.json {: #2-or-edit-settings-json }

El comando anterior escribe en `settings.json`. Para editar el archivo tú mismo:

| Ámbito | Archivo |
|---|---|
| Todos tus proyectos | `~/.gemini/settings.json` |
| Un proyecto | `.gemini/settings.json` en el proyecto |

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

Usa `httpUrl`, la clave para HTTP con streaming. La clave parecida `url` selecciona el transporte SSE
más antiguo, que el digna MCP Server no ofrece. No uses guiones bajos en el nombre del servidor.

!!! tip "Deja trust desactivado"

    Gemini CLI pregunta antes de cada llamada a herramienta, salvo que el servidor tenga
    `"trust": true`. Deja `trust` desactivado para *digna*, para confirmar cada cambio que un agente
    haga en tu configuración.

### 3. Verificar la conexión {: #3-verify-the-connection-gemini-cli }

Desde tu shell:

```bash
gemini mcp list
```

El servidor `digna` debe aparecer como conectado. Dentro de una sesión de Gemini CLI, ejecuta `/mcp`
para ver el servidor y sus herramientas.

---

## Solución de problemas de Gemini {: #troubleshooting-gemini }

### El servidor aparece como desconectado

- Comprueba que el endpoint termina en `/mcp` y es accesible desde tu máquina.
- Comprueba el nombre de la clave: `serverUrl` en Antigravity, `httpUrl` en Gemini CLI.
- Un `401` significa que la clave fue rechazada; consulta
  [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI ya no se inicia con mi cuenta

Desde junio de 2026, las cuentas de Google individuales usan Antigravity CLI en lugar de Gemini CLI.
Mueve la entrada `digna` a `mcp_config.json` como se describe en [Antigravity](#antigravity), y
cambia el nombre de `httpUrl` a `serverUrl`.

---

## Ver también {: #see-also }

- [Descripción general de agentes de IA](overview.md): endpoint, clave de API, seguridad y solución de problemas general
- [Claude](claude_mcp_guide.md): conectar Claude Code, Claude Desktop o un conector personalizado
- [digna Agentic](../platform/agentic/Introduction.md): lo que los agentes de IA pueden hacer con *digna*
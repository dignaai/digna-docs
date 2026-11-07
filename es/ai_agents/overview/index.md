# Conectar agentes de IA a digna

El **digna MCP Server** permite que los agentes de IA trabajen con *digna* a través del
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), un estándar abierto compatible con
Claude, Gemini y muchas otras herramientas de IA. Un agente conectado a *digna* puede responder
preguntas sobre tus datos, investigar alertas y ayudar a configurar *digna*. Consulta
[digna Agentic](../platform/agentic/Introduction.md) para ver lo que pueden hacer los agentes.

Esta página cubre el lado de *digna*, que es el mismo para todos los clientes de IA. Las guías de
cada cliente muestran después dónde introducirlo:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop y conectores personalizados
- [Gemini](gemini_mcp_guide.md): Antigravity y Gemini CLI

!!! info "Beta"

    digna Agentic, y con él el digna MCP Server, se entrega como versión beta en la
    [Release 2026.11](../changelog/Release_202611.md).

---

## Antes de empezar {: #before-you-start }

Necesitas:

- *digna* Release 2026.11 o posterior
- Una licencia que incluya **digna Agentic**. Sin ella, el servidor MCP rechaza todas las peticiones
- Una cuenta de usuario de *digna*. El agente actúa con los permisos de ese usuario en cada proyecto,
  consulta [Permisos](../platform/agentic/how_it_works.md#permissions)
- Un cliente de IA que se conecte a servidores MCP remotos mediante **HTTP con streaming** (streamable
  HTTP) y pueda enviar un encabezado `Authorization`

---

## 1. Encontrar el endpoint MCP {: #1-find-the-mcp-endpoint }

El servidor MCP forma parte del backend de *digna*, así que no hay nada adicional que instalar ni
iniciar. Su endpoint es la dirección del backend seguida de `/mcp`:

```text
https://digna.example.com/mcp
```

Si el backend se ejecuta directamente en un host y un puerto, por ejemplo después de
`digna serve --address 0.0.0.0 --port 8082`, el endpoint es esa dirección con `/mcp`:

```text
http://digna-host:8082/mcp
```

Si hay un proxy inverso delante del backend, debe reenviar `/mcp` al backend junto con el encabezado
`Authorization`.

!!! warning "Usa HTTPS en una red"

    Cada petición lleva una clave de API. Usa HTTPS siempre que el cliente de IA y *digna* no estén
    en la misma máquina.

### De dónde viene la conexión {: #where-the-connection-comes-from }

La mayoría de los clientes de IA se conectan desde la máquina en la que se ejecutan: Claude Code,
Claude Desktop con un puente local, Antigravity y Gemini CLI. Para ellos, basta con que *digna* sea
accesible desde esa máquina, por ejemplo dentro de la red de tu empresa.

Los **conectores personalizados** de Claude son diferentes: es la nube de Anthropic la que se conecta
al endpoint. Solo funcionan cuando el endpoint es accesible desde Internet mediante HTTPS. Para una
instalación de *digna* que solo es accesible dentro de tu red, usa un cliente que se ejecute en tu
máquina.

---

## 2. Crear una clave de API {: #2-create-an-api-key }

Un cliente de IA se autentica con la clave de API de un usuario de *digna*.

1. Inicia sesión en *digna*.
2. Abre tu perfil de usuario en la esquina inferior izquierda.
3. Haz clic en **API Keys** y después en **Add API Key**.
4. Introduce un nombre que indique para qué sirve la clave, p. ej. *Claude Code – Marcin*, y elige
   cuándo caduca.
5. Copia la clave. Solo se muestra una vez.

Cada petición al servidor MCP envía la clave en este encabezado:

```text
Authorization: Bearer <api key>
```

La palabra `Bearer` y el espacio que la sigue forman parte del valor del encabezado.

---

## 3. Conectar tu cliente de IA {: #3-connect-your-ai-client }

| Cliente de IA | Se conecta desde | Guía |
|---|---|---|
| Claude Code | Tu máquina | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop con un puente local | Tu máquina | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Conector personalizado de Claude (claude.ai, Claude Desktop, Claude para móvil) | La nube de Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE y aplicación | Tu máquina | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Tu máquina | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Otros clientes MCP también funcionan si admiten servidores remotos mediante HTTP con streaming y un
encabezado personalizado. La mayoría lee una configuración como esta. Consulta la documentación de tu
cliente para conocer los nombres exactos del archivo y de las claves:

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

---

## 4. Pruébalo {: #4-try-it }

Pregunta al agente algo que solo *digna* pueda responder:

- *"Enumera mis proyectos de digna."*
- *"¿Qué fuentes de datos del proyecto X no están en verde hoy?"*
- *"Explica la última comprobación fallida de la fuente de datos Y."*

Si el agente enumera tus proyectos, la conexión funciona.

---

## Seguridad {: #security }

- **Una clave por persona y cliente.** Así puedes revocar una sola clave, con **Delete API Key**, sin
  afectar a nadie más.
- **Elige el usuario con cuidado.** El agente puede hacer todo lo que puede hacer el usuario de la
  clave. Si solo se van a investigar datos, usa un usuario con el rol de lector en los proyectos.
- **No pongas claves en archivos compartidos.** No hagas commit de un archivo de configuración que
  contenga una clave. Cuando el cliente lo permita, lee la clave desde una variable de entorno.
- **Establece una caducidad.** Crea una clave nueva antes de que caduque la anterior y actualiza el
  cliente.
- **Revisa las llamadas a herramientas.** Mantén activada la confirmación de llamadas a herramientas
  del cliente, al menos para las llamadas que modifican la configuración.

---

## Solución de problemas {: #troubleshooting }

### 401 Unauthorized

La respuesta indica el motivo:

| Mensaje | Causa |
|---|---|
| `Missing or malformed Authorization header` | No se envió ningún encabezado, o el valor no empieza por `Bearer ` |
| `Invalid API key` | La clave es incorrecta o se ha eliminado |
| `API key expired` | La clave ha caducado. Crea una nueva |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

La licencia de *digna* no tiene ninguna entrada de digna Agentic, o esa entrada ha caducado. Pide al
equipo de digna una licencia que incluya digna Agentic e instálala como se describe en la guía de
instalación de tu sistema operativo.

### Todas las peticiones fallan con un error de licencia no válida

La propia licencia de *digna* ha caducado. El servidor MCP deja de responder, igual que el dashboard,
hasta que se instale una licencia nueva.

### El agente puede leer la configuración pero no cambiarla

El usuario asociado a la clave de API no tiene el rol de editor en ese proyecto. Usa la clave de un
usuario con el rol de editor, o pide a un administrador del proyecto que cambie el rol.

### El cliente no consigue conectarse en absoluto

La máquina que se conecta no llega al endpoint. Abre la dirección del endpoint desde esa máquina y
revisa los firewalls, los proxies y el certificado. En el caso de un conector personalizado de
Claude, esa máquina está en la nube de Anthropic, consulta
[De dónde viene la conexión](#where-the-connection-comes-from).
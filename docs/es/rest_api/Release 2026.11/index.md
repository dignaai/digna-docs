---
title: Descripción general de la API REST 2026.11 | Documentación de digna
description: Use la API REST v1 de digna para leer proyectos y resultados de inspección, gestionar fuentes de datos, conjuntos de datos y atributos, e iniciar inspecciones — URL base, autenticación con clave de API, paginación, errores y el documento OpenAPI.
image: /assets/logo_square.png
keywords: API REST de digna, API de digna, OpenAPI de digna, clave de API de digna, API de solicitudes de inspección, API de calidad de datos, Swagger UI
---

# API REST de digna 2026.11

La API REST de *digna* permite que sus propias herramientas y pipelines trabajen con *digna* mediante
HTTP y JSON: leer proyectos y resultados de inspección, gestionar fuentes de datos, conjuntos de datos
y atributos, e iniciar inspecciones, por ejemplo al final de una carga de datos. El [Python SDK](../../sdk/Release%202026.11/index.md)
utiliza la misma API.

Esta página describe lo que tienen en común todas las solicitudes. Las páginas de recursos enumeran
cada endpoint con sus parámetros, el cuerpo de la solicitud, las respuestas y los esquemas:

| Recurso | Endpoints |
|---|---|
| [Projects](projects.md) | Leer proyectos |
| [DB Connections](db_connections.md) | Leer conexiones de base de datos |
| [Data Sources](data_sources.md) | Crear, leer, actualizar y eliminar fuentes de datos |
| [Data Sets](data_sets.md) | Crear, leer, actualizar y eliminar conjuntos de datos |
| [Attributes](attributes.md) | Crear, leer, actualizar y eliminar atributos |
| [Check Definitions](check_definitions.md) | Leer definiciones de comprobaciones |
| [Inspection Requests](inspection_requests.md) | Iniciar inspecciones y seguir su progreso |
| [Inspection Statuses](inspection_statuses.md) | Leer resultados de inspección por proyecto, fuente de datos y conjunto de datos |

---

## URL base {: #base-url }

La API forma parte del backend de *digna*. Cada ruta empieza por `/v1`, después de la dirección del
backend:

```text
https://digna.example.com/v1/projects
```

La dirección del backend es la misma que usa el dashboard: `baseUrl` en la sección `[api]` de
`dashboard/dashboard_config.toml`. Use HTTPS siempre que el cliente que llama y *digna* no estén en la
misma máquina, porque cada solicitud lleva una clave de API.

---

## Autenticación {: #authentication }

Cada solicitud envía la clave de API de un usuario de *digna* en la cabecera `Authorization`:

```text
Authorization: Bearer <api key>
```

Para crear una clave, abra su perfil de usuario en la esquina inferior izquierda del dashboard, haga clic
en **API Keys** y después en **Add API Key**, y copie la clave. Solo se muestra una vez. Las mismas
claves sirven para el [digna MCP Server](../../ai_agents/overview.md).

Una solicitud se ejecuta con los permisos del usuario de la clave. Crear, modificar y eliminar requiere
el rol de editor en el proyecto; de lo contrario, la solicitud se rechaza con `403` y el mensaje
`You don't have permission to edit this project`.

!!! tip "Use un usuario dedicado para la automatización"

    Cree un usuario de *digna* para cada integración, asígnele solo los proyectos y roles que necesite
    y cree su clave con una fecha de caducidad. Así podrá revocar el acceso de una integración
    eliminando su clave, sin afectar a nadie más.

---

## Enviar una solicitud {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Las respuestas son JSON. Las listas se devuelven como un array JSON. Los cuerpos de las solicitudes
también son JSON y se envían con `Content-Type: application/json`.

---

## Límites y filtros {: #limits-and-filters }

Los endpoints de lista devuelven como máximo `limit` elementos: 200 de forma predeterminada y hasta
5000. Un valor fuera de ese rango se rechaza con `400`. No hay offset ni token de página, así que acote
una lista con sus filtros, por ejemplo `project_id`, `data_source_id`, o `start_date` y `end_date` en
los estados de inspección.

Una solicitud que tarda más de 60 segundos se cancela con `408 Request Timeout`.

---

## Errores {: #errors }

Una respuesta de error tiene un cuerpo JSON con un código y un mensaje:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Estado | Código | Significado |
|---|---|---|
| `400` | `BAD_REQUEST` | La solicitud no es válida, por ejemplo un `limit` fuera de rango |
| `401` | `NOT_AUTHENTICATED` | La clave de API falta, tiene un formato incorrecto, es desconocida o ha caducado |
| `403` | `NOT_AUTHORIZED` | El usuario de la clave no tiene el rol que requiere esta solicitud |
| `403` | `INVALID_LICENSE` | La licencia de *digna* ha caducado |
| `404` | `NOT_FOUND` | El proyecto, la fuente de datos u otro elemento no existe |
| `500` | `INTERNAL_ERROR` | Un error inesperado en *digna*. El log del backend tiene los detalles |

El `message` de una respuesta `401` indica qué falla en la clave:

| Mensaje | Causa |
|---|---|
| `Missing Authorization header` | No se envió ninguna cabecera `Authorization` |
| `Invalid Authorization header format` | El valor no empieza por `Bearer ` |
| `Invalid API key` | La clave es incorrecta o se eliminó |
| `API key expired` | La clave ha caducado. Cree una nueva |

---

## Ejecutar una inspección {: #running-an-inspection }

Una integración típica inicia una inspección cuando ha terminado una carga de datos, espera a que
finalice y lee el resultado:

1. **Inicie la inspección** con [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   La respuesta contiene el `id` de la solicitud.
2. **Siga su progreso** con [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Su `status` pasa de `PENDING` a `RUNNING` y luego a `COMPLETED`, o termina como `FAILED`,
   `ABORTED` o `CANCELLED`. Vuelva a consultarlo cada pocos segundos hasta que deje de cambiar.
3. **Lea el resultado** con [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   para las fechas inspeccionadas. Cada elemento tiene un `status` general: `0` (OK), `1` (advertencia),
   `2` (crítico) o `-1` (sin estado), y un estado por módulo con el número de comprobaciones superadas,
   inciertas y fallidas.

```bash
curl -X POST https://digna.example.com/v1/inspection-requests \
  -H "Authorization: Bearer $DIGNA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "project_id": 1,
    "include_all_data_sources": true,
    "data_source_ids": [],
    "start_date": "2026-11-06",
    "end_date": "2026-11-06",
    "mode": "DAILY",
    "weekly_mode_weekdays": [],
    "monthly_mode_days": [],
    "use_notification": true
  }'
```

---

## Documento OpenAPI {: #openapi-document }

Cada instalación de *digna* describe esta API en un documento OpenAPI 3.1 y ofrece una Swagger UI
interactiva para probar solicitudes contra ella:

| Qué | Dirección |
|---|---|
| Documento OpenAPI | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

El documento de Release 2026.11 también está disponible aquí: [openapi.json](openapi.json). Úselo para
generar un cliente en otro lenguaje.

!!! note "Solo se cubren los endpoints /v1"

    El dashboard también se comunica con el backend a través de otros endpoints internos. No forman parte
    de esta API y pueden cambiar con cualquier versión, así que construya sus integraciones solo sobre
    los endpoints `/v1`.

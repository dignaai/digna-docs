# Referencia del SDK de Python de digna 2026.06

Esta sección documenta el SDK de Python para ***digna***. Está organizada como una referencia de varias páginas: use esta introducción para entender el cliente y continúe después con las páginas dedicadas al inicio rápido, los recursos, los modelos, los errores y la documentación de API generada.

El SDK se publica como el paquete `digna-sdk` y expone un cliente estable y versionado para la API REST de ***digna***.

---

## Conceptos básicos del SDK

---

### Descripción general

El SDK sigue un diseño de cliente orientado a recursos. Cada área de la API se expone como un cliente de primer nivel en el `DignaClient` principal, con modelos de solicitud y respuesta tipados y un manejo de errores coherente.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Funciones principales

- **Modelos tipados** — cada solicitud y cada respuesta se valida con pydantic, de modo que su editor y su verificador de tipos detectan los errores antes de llegar a la red.
- **Orientado a recursos** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` y `client.inspection_statuses` exponen cada uno métodos sencillos `list` / `get` / `create` / `update` / `delete`.
- **Errores claros** — los errores de la API lanzan `DignaAPIError` (o una subclase más específica como `DignaAuthenticationError`, `DignaAuthorizationError` o `DignaNotFoundError`) en lugar de devolver `None` de forma silenciosa.

### Instalación

```bash
pip install digna-sdk
```

---

## Páginas de referencia

Esta versión está organizada en las siguientes páginas:

- [Inicio rápido](quickstart.md) — conectarse y realizar las primeras llamadas.
- [Recursos](resources.md) — la lista completa de clientes de recursos disponibles.
- [Modelos](models.md) — los modelos de pydantic usados para la entrada y la salida.
- [Errores](errors.md) — la jerarquía de excepciones.
- [Referencia de la API](reference.md) — documentación de referencia generada automáticamente.
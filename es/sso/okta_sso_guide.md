# Configurar SSO con Okta

Okta es compatible con OIDC, con una peculiaridad que causa problemas en la mayoría de las integraciones por primera vez: una organización de Okta expone más de un servidor de autorización, y cada uno tiene su propia URL de descubrimiento.

Esta guía cubre el **lado de Okta**: crear la integración de la aplicación y recopilar los valores que digna necesita. El lado de digna — `dashboard_config.toml`, pruebas y solución de problemas — es el mismo para todos los proveedores y se describe en la [Single Sign-On Overview](overview.md).

---

## Antes de empezar

| Requisito | Notas |
|---|---|
| **Okta role** | Super Administrator, o un rol de administrador permitido para crear integraciones de aplicaciones |
| **Okta domain** | p. ej. `yourcompany.okta.com`, o un dominio personalizado si está configurado |
| **digna redirect URI** | La URL a la que los usuarios regresan después del inicio de sesión, p. ej. `https://digna.yourdomain.com/oidc/callback` |

---

## Paso 1: Crear la integración de la aplicación

1. Inicia sesión en la Okta Admin Console
2. Ve a **Applications → Applications**
3. Haz clic en **Create App Integration**
4. Selecciona:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Haz clic en **Next**

!!! warning "El tipo de aplicación no se puede cambiar"

    Elegir *Single-Page Application* en lugar de *Web Application* crea un cliente público sin secreto, y el intercambio de código en el backend de digna fallará con `invalid_client`. El tipo queda fijado al crear la aplicación: una elección errónea implica eliminar la aplicación y comenzar de nuevo.

---

## Paso 2: Configurar la integración

1. **App integration name**: `digna`
2. **Grant type**: deja seleccionado *Authorization Code*
3. **Sign-in redirect URIs**: introduce la URL de callback de digna:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: opcional
5. Bajo **Assignments**, elige quién puede usar la integración — un grupo específico es más seguro que *Allow everyone in your organization to access*
6. Haz clic en **Save**

!!! note "La asignación es obligatoria"

    Okta autentica al usuario y luego comprueba si está asignado a la aplicación. Un usuario no asignado llega a la página de inicio de sesión de Okta, inicia sesión correctamente y se le deniega el acceso al intentar la redirección de retorno. Si el inicio de sesión funciona para ti pero no para tus colegas, la asignación es lo primero que debes revisar.

---

## Paso 3: Recopilar las credenciales

En la pestaña **General** de la aplicación, bajo **Client Credentials**:

- **Client ID** → se convierte en `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → se convierte en `DIGNA_OIDC_CLIENT_SECRET` (haz clic en el icono del ojo para revelar)

---

## Paso 4: Elegir el servidor de autorización

Este es el paso que determina tu URL de descubrimiento. Ve a **Security → API** para ver los servidores de autorización en tu organización.

**Org authorization server** — emite tokens para la propia organización de Okta:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — incluido el que Okta crea llamado `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Para el servidor integrado, `<auth_server_id>` es literalmente `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "¿Cuál usar?"

    Usa el servidor de autorización **org** a menos que tu organización ya estandarice en uno personalizado para políticas de acceso a APIs. Las cuentas de Okta Developer por defecto usan `default`; muchas organizaciones empresariales lo deshabilitan. Abre ambas URLs en un navegador: la que devuelva JSON en lugar de un error es la que tienes disponible.

---

## Paso 5: Configurar digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

La `key` en ambos archivos debe coincidir — `okta` en este ejemplo.

---

## Paso 6: Probar

Reinicia el backend y el servidor web, luego abre el dashboard. Consulta [Testing Login](overview.md#testing-login) para la lista completa de verificación.

---

## Solución de problemas de Okta

### La redirect URI no está registrada

Okta indica en el error la URI incorrecta. Compárala con **General → Sign-in redirect URIs**; Okta compara la cadena completa incluyendo cualquier barra final.

### El usuario no está asignado a la aplicación cliente

La cuenta no está en la lista de asignaciones de la aplicación. Añade al usuario o a su grupo en **Assignments**.

### 400 Bad Request: Invalid Authorization Server

El `<auth_server_id>` en la URL de descubrimiento no existe, la causa más común es usar `default` en una organización donde se ha eliminado. Revisa **Security → API** para ver los servidores realmente disponibles.

### invalid_client en el paso de tokens

La integración se creó como Single-Page Application y no tiene client secret. Vuelve a crearla como Web Application.

---

## Véase también

- [Single Sign-On Overview](overview.md) — referencia de configuración, pruebas y solución de problemas general
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
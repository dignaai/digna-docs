# Configurar SSO con Auth0

Auth0 cumple con OIDC y expone un endpoint de discovery por tenant. Lo principal es configurar correctamente el dominio del tenant, que aparece en la URL de discovery y cambia si habilitas un dominio personalizado.

Esta guía cubre el **lado de Auth0**: crear la aplicación y recopilar los valores que digna necesita. El lado de digna — `dashboard_config.toml`, pruebas y resolución de problemas — es el mismo para cualquier proveedor y se describe en la [Descripción general del inicio de sesión único](overview.md).

---

## Antes de empezar

| Requisito | Notas |
|---|---|
| **Auth0 role** | Administrador en el tenant |
| **Tenant domain** | p. ej. `yourcompany.eu.auth0.com` — el segmento de región importa |
| **digna redirect URI** | La URL a la que vuelven los usuarios tras el inicio de sesión, p. ej. `https://digna.yourdomain.com/oidc/callback` |

---

## Paso 1: Crear la aplicación

1. Inicia sesión en el [Auth0 Dashboard](https://manage.auth0.com)
2. Ve a **Applications → Applications**
3. Haz clic en **Create Application**
4. Nómbrala `digna` y elige **Regular Web Applications**
5. Haz clic en **Create**

!!! warning "Elija Regular Web Applications"

    *Single Page Application* y *Native* crean clientes públicos sin secreto. digna realiza el intercambio de código desde su backend y necesita un cliente confidencial, por lo que **Regular Web Applications** es el tipo correcto. A diferencia de algunos proveedores, Auth0 sí permite cambiar el tipo más tarde en **Settings → Application Type**.

---

## Paso 2: Añadir la URL de callback

En la pestaña **Settings** de la aplicación:

1. Busca **Allowed Callback URLs**
2. Introduce tu URL de callback de digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Opcionalmente, configura **Allowed Logout URLs** a la URL del dashboard
4. Desplázate hasta el final y haz clic en **Save Changes**

!!! note "Separados por comas, no por saltos de línea"

    Auth0 acepta varias URLs de callback en este campo, separadas por comas. Una lista separada solo por saltos de línea se interpreta como una única URL mal formada y no coincide con nada de forma silenciosa.

---

## Paso 3: Recopilar las credenciales

Aún en **Settings**, en el panel **Basic Information**:

- **Domain** → va en la URL de discovery
- **Client ID** → pasa a `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → pasa a `DIGNA_OIDC_CLIENT_SECRET` (haz clic para revelar)

---

## Paso 4: Confirmar el tipo de grant

1. Ve a **Settings → Advanced Settings → Grant Types**
2. Confirma que **Authorization Code** está marcado

Viene habilitado por defecto para Regular Web Applications. Si se desmarca, el inicio de sesión de digna falla con `unauthorized_client`.

---

## Paso 5: Construir la URL de discovery

Sustituye el **Domain** del Paso 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Por ejemplo:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Los dominios personalizados cambian el emisor"

    Si tu tenant usa un dominio personalizado como `login.yourcompany.com`, usa ese dominio en la URL de discovery. Mezclar los dos — el dominio canónico en la URL de discovery y el personalizado en el navegador — produce un desajuste de issuer, y el token es rechazado después de un inicio de sesión que por lo demás fue correcto.

---

## Paso 6: Configurar digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Iniciar sesión con Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

La `key` en ambos archivos debe coincidir — `auth0` aquí.

---

## Paso 7: Probar

Reinicia el backend y el servidor web, luego abre el dashboard. Consulta [Probar inicio de sesión](overview.md#testing-login) para la lista de verificación completa.

---

## Resolución de problemas con Auth0

### Desajuste de la URL de callback

La página de error de Auth0 muestra la URL que recibió. Añádela a **Allowed Callback URLs**, comprobando que las entradas están separadas por comas.

### unauthorized_client

**Authorization Code** no está habilitado en **Advanced Settings → Grant Types**, o el tipo de aplicación no es Regular Web Applications.

### Acceso denegado después de un inicio de sesión correcto

Una Rule, Action o trigger post-login en el tenant está rechazando al usuario. Revisa **Actions → Flows → Login** y los logs del tenant en **Monitoring → Logs**, que muestran la razón exacta.

### Desajuste del emisor

La URL de discovery y el dominio al que se dirigió el navegador difieren — normalmente el dominio canónico del tenant frente a un dominio personalizado. Usa uno de ellos de forma consistente.

---

## Véase también

- [Descripción general del inicio de sesión único](overview.md) — referencia de configuración, pruebas y resolución general de problemas
- [Auth0: Descubrimiento de OpenID Connect](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
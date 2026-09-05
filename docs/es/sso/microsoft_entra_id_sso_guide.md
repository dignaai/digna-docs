---
title: Microsoft Entra ID SSO – Integración de inicio de sesión único | Documentación de digna
description: Configure el inicio de sesión único para digna con Microsoft Entra ID (anteriormente Azure AD) usando OpenID Connect — registro de la aplicación, URI de redirección, secreto de cliente, ID de inquilino y la configuración correspondiente de digna.
image: /assets/logo_square.png
keywords: digna sso, microsoft entra id, azure ad sso, integración OIDC, registro de aplicaciones, autenticación empresarial
---

# Configurar SSO con Microsoft Entra ID

Microsoft Entra ID (anteriormente Azure Active Directory) es un proveedor totalmente compatible con OIDC, por lo que digna se integra con él a través del endpoint estándar de descubrimiento.

Esta guía cubre el **lado de Entra ID**: registrar la aplicación y recopilar los cuatro valores que digna necesita. El lado de digna — `dashboard_config.toml`, pruebas y solución de problemas — es el mismo para todos los proveedores y se describe en la [Visión general de inicio de sesión único](overview.md).

---

## Antes de comenzar

| Requisito | Notas |
|---|---|
| **Rol en Entra ID** | Application Administrator, Cloud Application Administrator, o Global Administrator |
| **URI de redirección de digna** | La URL a la que los usuarios regresan después del inicio de sesión, p. ej. `https://digna.yourdomain.com/oidc/callback` |
| **Inquilino** | El directorio en el que inician sesión tus usuarios |

---

## Paso 1: Registrar la aplicación

1. Inicia sesión en el [centro de administración de Microsoft Entra](https://entra.microsoft.com)
2. Ve a **Identity → Applications → App registrations**
3. Haz clic en **New registration**
4. Configura:
   - **Name**: `digna` (se muestra a los usuarios en la pantalla de consentimiento)
   - **Supported account types**: *Accounts in this organizational directory only* para un despliegue de un solo inquilino
5. Bajo **Redirect URI**, selecciona la plataforma **Web** e introduce tu URL de callback de digna:

```
https://digna.yourdomain.com/oidc/callback
```

6. Haz clic en **Register**

!!! warning "Importante"

    La plataforma debe ser **Web**, no *Single-page application*. digna intercambia el código de autorización desde el backend usando un secreto de cliente, lo que el tipo de plataforma SPA no permite.

---

## Paso 2: Copiar los IDs de cliente e inquilino

En la página **Overview** de la aplicación, copia:

- **Application (client) ID** → se convierte en `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → va en la URL de descubrimiento

---

## Paso 3: Crear un secreto de cliente

1. Ve a **Certificates & secrets → Client secrets**
2. Haz clic en **New client secret**
3. Introduce una descripción y elige una caducidad
4. Haz clic en **Add**
5. Copia inmediatamente la columna **Value**

!!! warning "Copia el Value, no el Secret ID"

    El **Value** se muestra solo una vez, en esta página, y no se puede recuperar después. El **Secret ID** junto a él se parece pero no es el secreto — usarlo produce un error `invalid_client` al iniciar sesión. Si navegas fuera de la página antes de copiarlo, elimina el secreto y crea uno nuevo.

!!! tip "Consejo"

    Entra ID limita la vida útil del secreto a 24 meses, así que cada integración SSO tiene una fecha de caducidad. Apúntala en un lugar visible — un secreto caducado deja el SSO inactivo para todos los usuarios al mismo tiempo, sin advertencia en la página de inicio de sesión.

---

## Paso 4: Confirmar los permisos de API

1. Ve a **API permissions**
2. Confirma que **Microsoft Graph → User.Read** (delegado) esté presente — se añade por defecto

Los scopes `openid`, `profile` y `email` que digna solicita forman parte del conjunto estándar de OIDC y no requieren concesión separada. Si tu inquilino requiere consentimiento de administrador para todas las aplicaciones, haz clic en **Grant admin consent for &lt;tenant&gt;**.

---

## Paso 5: Construir la URL de descubrimiento

Sustituye el **Directory (tenant) ID** del Paso 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Usar el endpoint v2.0"

    El segmento `/v2.0/` importa. El endpoint v1.0 en `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` emite tokens en un formato más antiguo y no devuelve los claims estándar de OIDC que digna espera.

Abre la URL en un navegador antes de continuar. Un documento JSON confirma que el ID de inquilino es correcto.

---

## Paso 6: Configurar digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Iniciar sesión con Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

La `key` en ambos archivos debe coincidir — `microsoft` en este ejemplo.

---

## Paso 7: Prueba

Reinicia el backend y el servidor web, luego abre el dashboard. Consulta [Pruebas de inicio de sesión](overview.md#testing-login) para la lista completa de verificación.

---

## Solución de problemas de Entra ID

### AADSTS50011: Coincidencia de URI de redirección

La URI en `DIGNA_OIDC_REDIRECT_URI` difiere de la registrada en el Paso 1. Entra ID compara la cadena completa, por lo que una barra final, `http` frente a `https`, o un puerto distinto cuentan como diferencia. Revisa **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Secreto de cliente no válido

O bien se copió el **Secret ID** en lugar del **Value**, o el secreto ha caducado. Crea un secreto nuevo y copia la columna Value.

### AADSTS650057: Recurso no válido

El registro de la aplicación fue eliminado o pertenece a un inquilino distinto del indicado en la URL de descubrimiento. Confirma el Directory (tenant) ID en la página Overview.

### Los usuarios inician sesión pero no ocurre nada

Si el inquilino requiere consentimiento de administrador y no se ha concedido, el redirect vuelve sin un token utilizable. Concede el consentimiento de administrador en **API permissions**.

---

## Véase también

- [Visión general de inicio de sesión único](overview.md) — referencia de configuración, pruebas y solución de problemas general
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
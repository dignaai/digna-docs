---
title: Guía de Integración de Inicio de Sesión Único (SSO) | digna Documentation
description: Guía paso a paso para configurar Single Sign-On (SSO) para digna usando OpenID Connect (OIDC). Cubre la configuración del panel y del backend, pruebas, resolución de problemas y proveedores de identidad compatibles como Microsoft Entra ID, Google Workspace y Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - inicio de sesión único
  - oidc integration
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integration
  - enterprise authentication
lang: es
robots: index, follow
og_title: Guía de Integración de Single Sign-On (SSO) de digna
og_description: Configure Single Sign-On para digna utilizando OpenID Connect. Configuración paso a paso para Microsoft Entra ID, Google Workspace, Okta y otros proveedores de identidad compatibles con OIDC.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Guía de Integración de Single Sign-On (SSO)

---

## Tabla de Contenidos

1. [Introducción y Resumen](#introducción-y-resumen)
2. [Pasos de Configuración](#pasos-de-configuración)
3. [Configuración del Panel (Dashboard)](#configuración-del-panel-dashboard)
4. [Configuración del Backend](#configuración-del-backend)
5. [Probar el Inicio de Sesión](#probar-el-inicio-de-sesión)
6. [Resolución de Problemas](#resolución-de-problemas)
7. [Proveedores Compatibles](#proveedores-compatibles)

---

## Introducción y Resumen {: #introduction-and-overview }

Esta guía proporciona instrucciones paso a paso para integrar Single Sign-On (SSO) con la plataforma digna usando **OpenID Connect (OIDC)**.

### ¿Qué es SSO?

El Inicio de Sesión Único permite a los usuarios iniciar sesión en digna de forma segura usando sus credenciales empresariales a través de proveedores de identidad externos. Los usuarios pueden autenticarse con sus credenciales corporativas en lugar de gestionar contraseñas separadas para digna.

### Cómo Funciona

SSO en digna se implementa usando el protocolo OIDC. Se pueden configurar varios proveedores de identidad en paralelo ajustando dos archivos clave de configuración:

- **`dashboard_config.toml`** — Controla la interfaz de inicio de sesión del frontend
- **`config.toml`** — Configura las conexiones OIDC del backend

### Proveedores Compatibles {: #supported-providers-overview }

Los ejemplos en esta guía usan **Microsoft** y **Google**, pero **cualquier proveedor compatible con OIDC** puede integrarse siguiendo la misma estructura.

Proveedores OIDC comunes incluyen:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Otros proveedores de identidad compatibles con OIDC

---

## Pasos de Configuración {: #configuration-steps }

La configuración de SSO requiere actualizaciones en dos archivos. Esta sección explica cómo configurar cada uno.

### Resumen de Archivos de Configuración

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Interfaz de inicio de sesión del frontend |
| **config.toml** | `/config.toml` | Conexiones OIDC del backend |

Ambos archivos deben configurarse para que SSO funcione correctamente.

---

## Configuración del Panel (Dashboard) {: #dashboard-configuration }

### Ubicación del Archivo

```
dashboard/dashboard_config.toml
```

### Paso 1: Agregar Proveedores OIDC

Agrega entradas bajo el array `[[login.oidc]]` para cada proveedor de identidad que desees soportar.

**Ejemplo con Microsoft y Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Iniciar sesión con Microsoft"

[[login.oidc]]
key = "google"
label = "Iniciar sesión con Google"
```

### Paso 2: Configurar Opciones de Inicio de Sesión

Especifica si se debe permitir el inicio de sesión basado en contraseña:

```toml
[login]
usePassword = true
```

### Parámetros de Configuración

#### Sección `[[login.oidc]]`

| Parameter | Type | Required | Description |
|---|---:|---:|---|
| `key` | string | Sí | Identificador único para la conexión OIDC (debe coincidir con la key en config.toml) |
| `label` | string | Sí | Texto mostrado en el botón de inicio de sesión (por ejemplo, "Iniciar sesión con Microsoft") |

#### Sección `[login]`

| Parameter | Type | Default | Description |
|---|---:|---:|---|
| `usePassword` | boolean | false | Permitir inicio de sesión con contraseña además de SSO |

### Entendiendo usePassword

**Si `usePassword = true`:**
- La pantalla de inicio de sesión muestra botones SSO (por ejemplo, "Iniciar sesión con Microsoft")
- La pantalla de inicio de sesión también muestra campos de usuario y contraseña
- Los usuarios pueden autenticarse por cualquiera de los métodos
- Permite configuraciones híbridas donde algunos usuarios usan SSO y otros usan contraseña

**Si `usePassword = false` (o se omite):**
- La pantalla de inicio de sesión muestra solo los botones SSO
- No hay campos de usuario/contraseña
- Solo está disponible la autenticación OIDC

> **💡 Consejo**
>
> El inicio de sesión basado en contraseña solo está disponible para usuarios que fueron creados con contraseñas usando el comando `digna user add` o a través del panel.

### Ejemplo Completo

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Iniciar sesión con Microsoft"

[[login.oidc]]
key = "google"
label = "Iniciar sesión con Google"

[[login.oidc]]
key = "okta"
label = "Iniciar sesión con Okta"
```

---

## Configuración del Backend {: #backend-configuration }

### Ubicación del Archivo

```
/config.toml
```

(Directorio raíz de instalación de digna)

### Paso 1: Agregar Secciones de Proveedores OIDC

Cada proveedor debe tener una sección dedicada `[oidc.<key>]`. La key debe coincidir con la `key` definida en `dashboard_config.toml`.

### Configuración de Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Configuración de Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Parámetros de Configuración

| Parameter | Type | Required | Description | Example |
|---|---:|---:|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Sí | Client ID del proveedor de identidad | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Sí | Client secret del proveedor de identidad | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Sí | URL de callback después de la autenticación | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Sí | Endpoint de configuración OIDC | `https://login.microsoftonline.com/...` |

> **⚠️ Importante**
>
> Reemplaza los valores de marcador de posición (`<client_id>`, `<client_secret>`, `<tenant_id>`) con las credenciales reales desde el portal de desarrolladores de tu proveedor de identidad.

### Redirect URI

La redirect URI debe ser la misma en la configuración de tu proveedor de identidad:

```
http://localhost:5173/oidc/callback
```

Si digna está alojado en un dominio diferente, actualízalo en consecuencia:
- Local: `http://localhost:5173/oidc/callback`
- Producción: `https://digna.tudominio.com/oidc/callback`

### Ejemplo Completo

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Probar el Inicio de Sesión {: #testing-login }

Después de completar la configuración, verifica que SSO funcione correctamente.

### Lista de Verificación Previa a la Prueba

Antes de probar, asegúrate de que:

- [ ] `dashboard_config.toml` ha sido actualizado con proveedores OIDC
- [ ] `config.toml` ha sido actualizado con credenciales OIDC
- [ ] Ambos archivos han sido guardados
- [ ] Las credenciales son correctas (client ID, client secret)
- [ ] La redirect URI coincide con la URL de tu despliegue
- [ ] La aplicación del proveedor de identidad está configurada con la redirect URI

### Pasos de Prueba

#### Paso 1: Reiniciar Servicios

Reinicia el backend de digna y el servidor web para aplicar los cambios.

**Si se ejecuta como servicio de Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Si se ejecuta manualmente:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Si usas IIS o Tomcat:**
Reinicia el servicio de tu servidor web.

#### Paso 2: Abrir el Panel

Abre el panel de digna en tu navegador:

```
http://localhost:5173
```

(o la URL del panel que hayas configurado)

#### Paso 3: Verificar Botones de Inicio de Sesión

Comprueba que aparezcan botones de inicio de sesión para cada proveedor configurado:

- ✅ Deberías ver el botón "Iniciar sesión con Microsoft"
- ✅ Deberías ver el botón "Iniciar sesión con Google"
- ✅ (Si usePassword = true) Deberías ver campos de usuario/contraseña

Si los botones no aparecen:
- Verifica que `dashboard_config.toml` se haya guardado
- Verifica que el servicio del panel se haya reiniciado
- Revisa la consola del navegador (F12) en busca de errores

#### Paso 4: Probar Inicio de Sesión SSO

Haz clic en uno de los botones SSO (por ejemplo, "Iniciar sesión con Microsoft"):

1. Deberías ser redirigido a la página de inicio de sesión del proveedor de identidad
2. Inicia sesión con tus credenciales empresariales
3. Deberías ser redirigido de vuelta a digna
4. Deberías quedar autenticado en digna

#### Paso 5: Verificar Creación de Usuario

Después de un inicio de sesión SSO exitoso:

- ✅ El usuario debería crearse automáticamente en digna
- ✅ El usuario debería quedar autenticado
- ✅ El perfil del usuario debería mostrar tus credenciales del proveedor de identidad
- ✅ Deberías ver el panel de digna

#### Paso 6: Probar Inicio de Sesión con Contraseña (Si está Habilitado)

Si `usePassword = true`:

1. Cierra sesión en digna
2. En la página de inicio de sesión, ingresa un usuario y contraseña
3. Deberías poder iniciar sesión con credenciales de contraseña

---

## Resolución de Problemas {: #troubleshooting }

### Los Botones de Inicio de Sesión No Aparecen

**Síntomas:**
- Los botones de inicio de sesión OIDC no son visibles en la página de login
- Solo se ven campos de contraseña (si usePassword = true)

**Causas y Soluciones:**
1. Verifica que `dashboard_config.toml` esté en el directorio `dashboard/`
2. Asegura que las secciones `[[login.oidc]]` estén presentes con la sintaxis correcta
3. Reinicia el servicio del panel
4. Limpia la caché del navegador (Ctrl+Shift+Delete o Cmd+Shift+Delete)
5. Revisa la consola del navegador (F12 → pestaña Console) en busca de errores

---

### Error de Coincidencia de Redirect URI

**Síntomas:**
- Después de hacer clic en el botón SSO, aparece un error sobre "redirect_uri mismatch"
- Error "The redirect URI is not registered"

**Causas y Soluciones:**
1. Verifica que `DIGNA_OIDC_REDIRECT_URI` en `config.toml` sea correcto
2. Verifica que la redirect URI esté registrada en la configuración del proveedor de identidad
3. Asegúrate de que ambas URL sean idénticas (incluyendo protocolo, dominio y ruta)
4. Revisa si hay errores tipográficos en la redirect URI
5. Si usas HTTPS, asegúrate de que el certificado sea válido

---

### Error de Credenciales de Cliente Inválidas

**Síntomas:**
- Error "Invalid client ID or secret"
- La autenticación falla por error de credenciales

**Causas y Soluciones:**
1. Verifica que `DIGNA_OIDC_CLIENT_ID` y `DIGNA_OIDC_CLIENT_SECRET` sean correctos
2. Asegúrate de que no haya espacios extras o caracteres especiales
3. Comprueba que las credenciales no hayan expirado o sido revocadas
4. Reinicia el servicio del backend después de actualizar la configuración
5. Revisa la consola del proveedor de identidad para confirmar que las credenciales están activas

---

### El Inicio de Sesión Se Cuelga o Agota el Tiempo

**Síntomas:**
- Al hacer clic en el botón SSO no sucede nada
- Tiempo de espera después de varios segundos
- El navegador muestra "Failed to connect" o similar

**Causas y Soluciones:**
1. Verifica que el backend de digna esté en ejecución: `digna repo check`
2. Comprueba la conectividad de red hacia el proveedor de identidad
3. Verifica que `DIGNA_OIDC_CONFIGURATION_URL` sea accesible
4. Revisa las reglas de firewall para permitir conexiones HTTPS salientes
5. Asegura que el backend y el panel puedan comunicarse entre sí

---

### Usuarios No Se Crean Automáticamente

**Síntomas:**
- El inicio de sesión SSO tiene éxito pero el usuario no se crea en digna
- Aparece un error de permisos tras el inicio de sesión SSO

**Causas y Soluciones:**
1. Verifica que la configuración OIDC sea correcta
2. Revisa que los permisos de usuario estén configurados
3. Revisa los logs de digna en busca de mensajes de error
4. Reinicia el servicio del backend
5. Contacta a support@digna.ai si el problema persiste

---

## Proveedores Compatibles {: #supported-providers }

### Probados y Soportados

Los siguientes proveedores OIDC han sido probados y se sabe que funcionan:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Otros Proveedores OIDC

Cualquier proveedor que soporte OpenID Connect puede integrarse. Información requerida:

- Client ID
- Client secret
- URL de configuración OpenID (normalmente en `/.well-known/openid-configuration`)
- Scopes soportados (típicamente `openid profile email`)

Contacta a support@digna.ai si necesitas ayuda integrando un proveedor específico.

---

## Buenas Prácticas

✅ **HACER:**
- Usar HTTPS en producción (no HTTP)
- Almacenar client secrets de forma segura (usar variables de entorno si es posible)
- Rotar secretos periódicamente
- Probar en un entorno no productivo primero
- Documentar qué proveedores están configurados
- Monitorizar logs de inicio de sesión por actividad inusual
- Mantener la configuración del proveedor de identidad sincronizada con la configuración de digna

❌ **NO HACER:**
- Almacenar client secrets en control de versiones
- Usar redirect URIs HTTP en producción
- Configurar múltiples proveedores con la misma key
- Dejar credenciales por defecto/prueba en producción
- Exponer archivos de configuración que contengan secretos
- Mezclar credenciales de desarrollo y producción

---

## Soporte

¿Necesitas ayuda con la configuración de SSO?

- 📧 **Email:** support@digna.ai
- 📚 **Documentación:** https://docs.digna.ai
- 🌐 **Sitio web:** https://www.digna.ai

---

**Última actualización:** 30 de agosto de 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**

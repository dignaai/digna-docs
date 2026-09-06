# Descripción general de Single Sign-On (SSO)

---

## Tabla de contenidos

1. [Introducción y descripción general](#introduction-and-overview)
2. [Guías por proveedor](#provider-guides)
3. [Pasos de configuración](#configuration-steps)
4. [Configuración del dashboard](#dashboard-configuration)
5. [Configuración del backend](#backend-configuration)
6. [Probar el inicio de sesión](#testing-login)
7. [Resolución de problemas](#troubleshooting)
8. [Proveedores compatibles](#supported-providers)

---

## Introducción y descripción general {: #introduction-and-overview }

Esta guía proporciona instrucciones paso a paso para integrar Single Sign-On (SSO) con la plataforma digna usando **OpenID Connect (OIDC)**.

### ¿Qué es SSO?

Single Sign-On permite a los usuarios iniciar sesión en digna de forma segura utilizando sus credenciales empresariales a través de proveedores de identidad externos. Los usuarios pueden autenticarse con sus credenciales corporativas en lugar de gestionar contraseñas separadas de digna.

### Cómo funciona

SSO en digna se implementa usando el protocolo OIDC. Se pueden configurar varios proveedores de identidad en paralelo ajustando dos archivos de configuración clave:

- **`dashboard_config.toml`** — Controla la interfaz de inicio de sesión del frontend
- **`config.toml`** — Configura las conexiones OIDC del backend

### Proveedores compatibles {: #supported-providers-overview }

Los ejemplos en esta guía usan **Microsoft** y **Google**, pero **cualquier proveedor compatible con OIDC** puede integrarse siguiendo la misma estructura.

---

## Guías por proveedor {: #provider-guides }

Cada proveedor necesita los mismos cuatro valores: un client ID, un client secret, una redirect URI y una discovery URL, pero cada uno los coloca en un lugar diferente en su consola de administración, y varios tienen un paso específico del proveedor que los demás no tienen. Las guías abajo cubren esa mitad del trabajo; esta página cubre la mitad de digna, que es idéntica para todos ellos.

| Proveedor | Guía | A tener en cuenta |
|---|---|---|
| **AD FS** | [Configurar SSO con AD FS](adfs_sso_guide.md) | Autoalojado; el único proveedor aquí donde usted controla el servicio de tokens |
| **Auth0** | [Configurar SSO con Auth0](auth0_sso_guide.md) | La discovery URL es por tenant, y los dominios personalizados la cambian |
| **Google Workspace** | [Configurar SSO con Google Workspace](google_workspace_sso_guide.md) | La pantalla de consentimiento debe publicarse antes de que usuarios no de prueba puedan iniciar sesión |
| **Keycloak** | [Configurar SSO con Keycloak](keycloak_sso_guide.md) | Autoalojado; la discovery URL es por realm |
| **Microsoft Entra ID** | [Configurar SSO con Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | El tenant ID aparece en la discovery URL; los secretos expiran |
| **Okta** | [Configurar SSO con Okta](okta_sso_guide.md) | La elección del servidor de autorización cambia la discovery URL |
| **OneLogin** | [Configurar SSO con OneLogin](onelogin_sso_guide.md) | El tipo de app OIDC debe elegirse al crearla y no se puede cambiar |
| **PingOne** | [Configurar SSO con PingOne](pingone_sso_guide.md) | El environment ID aparece en la discovery URL |

Cualquier otro proveedor compatible con OIDC funciona de la misma manera — vea [Otros proveedores OIDC](#supported-providers).

---

## Pasos de configuración {: #configuration-steps }

La configuración de SSO requiere actualizaciones en dos archivos. Esta sección explica cómo configurar cada uno.

### Visión general de los archivos de configuración

| Archivo | Ubicación | Propósito |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Interfaz de inicio de sesión del frontend |
| **config.toml** | `/config.toml` | Conexiones OIDC del backend |

Ambos archivos deben configurarse para que SSO funcione correctamente.

---

## Configuración del dashboard {: #dashboard-configuration }

### Ubicación del archivo

```
dashboard/dashboard_config.toml
```

### Paso 1: Agregar proveedores OIDC

Agregue entradas bajo el arreglo `[[login.oidc]]` para cada proveedor de identidad que desee soportar.

**Ejemplo con Microsoft y Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Paso 2: Configurar opciones de inicio de sesión

Especifique si se debe permitir el inicio de sesión mediante contraseña:

```toml
[login]
usePassword = true
```

### Parámetros de configuración

#### Sección `[[login.oidc]]`

| Parámetro | Tipo | Requerido | Descripción |
|---|---|---|---|
| `key` | string | Sí | Identificador único para la conexión OIDC (debe coincidir con la key en config.toml) |
| `label` | string | Sí | Texto mostrado en el botón de inicio de sesión (por ejemplo, "Login with Microsoft") |

#### Sección `[login]`

| Parámetro | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `usePassword` | boolean | false | Permitir inicio de sesión mediante contraseña además del SSO |

### Entendiendo usePassword

**Si `usePassword = true`:**
- La pantalla de inicio de sesión muestra botones SSO (por ejemplo, "Login with Microsoft")
- La pantalla de inicio de sesión también muestra campos de nombre de usuario y contraseña
- Los usuarios pueden autenticarse con cualquiera de los dos métodos
- Permite configuraciones híbridas donde algunos usuarios usan SSO y otros usan contraseñas

**Si `usePassword = false` (o se omite):**
- La pantalla de inicio de sesión muestra solo botones SSO
- No hay campos de usuario/contraseña
- Solo está disponible la autenticación OIDC

!!! tip "Consejo"

    El inicio de sesión mediante contraseña solo está disponible para usuarios que fueron creados con contraseñas usando el comando `digna user add` o mediante el dashboard.

### Ejemplo completo

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Configuración del backend {: #backend-configuration }

### Ubicación del archivo

```
/config.toml
```

(Directorio raíz de instalación de digna)

### Paso 1: Agregar secciones de proveedores OIDC

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

### Parámetros de configuración

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Sí | Client ID del proveedor de identidad | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Sí | Client secret del proveedor de identidad | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Sí | URL de callback después de la autenticación | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Sí | Endpoint de configuración OIDC | `https://login.microsoftonline.com/...` |

!!! warning "Importante"

    Reemplace los valores de marcador de posición (`<client_id>`, `<client_secret>`, `<tenant_id>`) con credenciales reales del portal de desarrollador de su proveedor de identidad.

### Redirect URI

La redirect URI debe ser la misma en la configuración de su proveedor de identidad:

```
http://localhost:5173/oidc/callback
```

Si digna está alojado en un dominio diferente, actualícelo en consecuencia:
- Local: `http://localhost:5173/oidc/callback`
- Producción: `https://digna.yourdomain.com/oidc/callback`

### Ejemplo completo

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

## Probar el inicio de sesión {: #testing-login }

Después de completar la configuración, verifique que SSO funcione correctamente.

### Lista de verificación previa a las pruebas

Antes de probar, asegúrese de:

- [ ] `dashboard_config.toml` ha sido actualizado con proveedores OIDC
- [ ] `config.toml` ha sido actualizado con credenciales OIDC
- [ ] Ambos archivos han sido guardados
- [ ] Las credenciales son correctas (client ID, client secret)
- [ ] La redirect URI coincide con la URL de su despliegue
- [ ] La aplicación del proveedor de identidad está configurada con la redirect URI

### Pasos de prueba

#### Paso 1: Reiniciar servicios

Reinicie el backend de digna y el servidor web para aplicar los cambios.

**Si se ejecuta como servicio en Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Si se ejecuta como servicio en Linux o macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Si se ejecuta manualmente:**
```bash
digna serve --address localhost --port 8082
```

**Reinicie también el servidor web** — IIS o Tomcat en Windows, nginx o Apache en Linux y macOS.

#### Paso 2: Abrir el dashboard

Abra el dashboard de digna en su navegador:

```
http://localhost:5173
```

(o la URL del dashboard configurada)

#### Paso 3: Verificar botones de inicio de sesión

Compruebe que aparezcan botones de inicio de sesión para cada proveedor configurado:

- Debería ver el botón "Login with Microsoft"
- Debería ver el botón "Login with Google"
- (Si usePassword = true) Debería ver campos de nombre de usuario/contraseña

Si los botones no aparecen:
- Verifique que `dashboard_config.toml` fue guardado
- Verifique que el servicio del dashboard se reinició
- Revise la consola del navegador (F12) en busca de errores

#### Paso 4: Probar inicio de sesión SSO

Haga clic en uno de los botones SSO (por ejemplo, "Login with Microsoft"):

1. Debería redirigirse a la página de inicio de sesión del proveedor de identidad
2. Inicie sesión con sus credenciales empresariales
3. Debería redirigirse de vuelta a digna
4. Debería haber iniciado sesión en digna

#### Paso 5: Verificar creación de usuario

Después de un inicio de sesión SSO exitoso:

- El usuario debería crearse automáticamente en digna
- El usuario debería iniciar sesión
- El perfil del usuario debería mostrar las credenciales del proveedor de identidad
- Debería ver el dashboard de digna

#### Paso 6: Probar inicio de sesión con contraseña (si está habilitado)

Si `usePassword = true`:

1. Cierre sesión en digna
2. En la página de inicio de sesión, introduzca un nombre de usuario y contraseña
3. Debería poder iniciar sesión con credenciales de contraseña

---

## Resolución de problemas {: #troubleshooting }

### Los botones de inicio de sesión no aparecen

**Síntomas:**
- Los botones de inicio de sesión OIDC no son visibles en la página de inicio de sesión
- Solo ve campos de contraseña (si usePassword = true)

**Causas y soluciones:**
1. Compruebe que `dashboard_config.toml` está en el directorio `dashboard/`
2. Verifique que las secciones `[[login.oidc]]` estén presentes con la sintaxis correcta
3. Reinicie el servicio del dashboard
4. Borre la caché del navegador (Ctrl+Shift+Delete o Cmd+Shift+Delete)
5. Revise la consola del navegador (F12 → pestaña Console) en busca de errores

---

### Error de mismatch en Redirect URI

**Síntomas:**
- Después de hacer clic en el botón SSO, aparece un error sobre "redirect_uri mismatch"
- Error "The redirect URI is not registered"

**Causas y soluciones:**
1. Verifique que `DIGNA_OIDC_REDIRECT_URI` en `config.toml` sea correcto
2. Verifique que la redirect URI esté registrada en la configuración del proveedor de identidad
3. Asegúrese de que ambos usen URLs idénticas (incluyendo protocolo, dominio y ruta)
4. Compruebe errores tipográficos en la redirect URI
5. Si usa HTTPS, asegúrese de que el certificado sea válido

---

### Error de credenciales de cliente inválidas

**Síntomas:**
- Error "Invalid client ID or secret"
- La autenticación falla con error de credenciales

**Causas y soluciones:**
1. Verifique que `DIGNA_OIDC_CLIENT_ID` y `DIGNA_OIDC_CLIENT_SECRET` sean correctos
2. Asegúrese de que no haya espacios adicionales o caracteres especiales
3. Compruebe que las credenciales no hayan expirado o sido revocadas
4. Reinicie el servicio del backend después de actualizar la configuración
5. Revise la consola del proveedor de identidad para confirmar que las credenciales estén activas

---

### El inicio de sesión se queda colgado o caduca

**Síntomas:**
- Al hacer clic en el botón SSO no ocurre nada
- Tiempo de espera después de varios segundos
- El navegador muestra "Failed to connect" o similar

**Causas y soluciones:**
1. Verifique que el backend de digna esté en ejecución: `digna repo check`
2. Compruebe la conectividad de red hacia el proveedor de identidad
3. Verifique que `DIGNA_OIDC_CONFIGURATION_URL` sea accesible
4. Compruebe las reglas de firewall que permitan conexiones HTTPS salientes
5. Verifique que el backend y el dashboard puedan comunicarse entre sí

---

### Los usuarios no se crean automáticamente

**Síntomas:**
- El inicio de sesión SSO tiene éxito pero el usuario no se crea en digna
- Obtiene error de permisos después del inicio de sesión SSO

**Causas y soluciones:**
1. Verifique que la configuración OIDC sea correcta
2. Compruebe que los permisos de usuario estén configurados
3. Revise los logs de digna en busca de mensajes de error
4. Reinicie el servicio del backend
5. Contacte a support@digna.ai si el problema persiste

---

## Proveedores compatibles {: #supported-providers }

### Probados y compatibles

Los siguientes proveedores OIDC han sido probados y se sabe que funcionan:

| Proveedor | URL de configuración | Guía de configuración |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Configurar SSO con AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Configurar SSO con Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Configurar SSO con Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Configurar SSO con Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Configurar SSO con Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Configurar SSO con Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Configurar SSO con OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Configurar SSO con PingOne](pingone_sso_guide.md) |

### Otros proveedores OIDC

Cualquier proveedor que soporte OpenID Connect puede integrarse. Información requerida:

- Client ID
- Client secret
- URL de configuración OpenID (usualmente en `/.well-known/openid-configuration`)
- Scopes soportados (típicamente `openid profile email`)

Contacte a support@digna.ai si necesita ayuda integrando un proveedor específico.

---

## Buenas prácticas

**HACER:**
- Use HTTPS en producción (no HTTP)
- Almacene los client secrets de forma segura (use variables de entorno si es posible)
- Rotee los secretos periódicamente
- Pruebe primero en un entorno no productivo
- Documente qué proveedores están configurados
- Monitoree los logs de inicio de sesión por actividad inusual
- Mantenga la configuración del proveedor de identidad sincronizada con la configuración de digna

**NO HACER:**
- Almacene client secrets en control de versiones
- Use redirect URIs HTTP en producción
- Configure múltiples proveedores con la misma key
- Deje credenciales por defecto/de prueba en producción
- Exponga archivos de configuración que contengan secretos
- Mezcle credenciales de desarrollo y producción

---

## Soporte

¿Necesita ayuda con la configuración de SSO?

- **Email:** support@digna.ai
- **Documentación:** https://docs.digna.ai
- **Sitio web:** https://www.digna.ai

---

**Última actualización:** 30 de agosto de 2026  
**Versión:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
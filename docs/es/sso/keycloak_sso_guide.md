---
title: "Keycloak SSO – Integración Single Sign-On | Documentación de digna"
description: "Configura el Single Sign-On para digna con Keycloak usando OpenID Connect — configuración del realm y del cliente, autenticación del cliente, URIs de redirección válidos, secreto del cliente y la configuración correspondiente de digna."
image: "/assets/logo_square.png"
keywords: "digna sso, keycloak sso, keycloak oidc, realm, cliente confidencial, openid connect, proveedor de identidad autohospedado"
---

# Configurar SSO con Keycloak

Keycloak es un proveedor de identidad autohospedado y totalmente compatible con OIDC. Como lo ejecutas tú mismo, la URL de descubrimiento se construye a partir del nombre de host y el realm propios en lugar de un dominio de proveedor.

Esta guía cubre el **lado de Keycloak**: crear el cliente y recopilar los valores que digna necesita. El lado de digna — `dashboard_config.toml`, pruebas y resolución de problemas — es el mismo para todos los proveedores y se describe en la [Descripción general de Single Sign-On](overview.md).

---

## Antes de empezar

| Requisito | Notas |
|---|---|
| **Versión de Keycloak** | 17 o posterior para las rutas URL usadas aquí — vea la nota en el Paso 4 |
| **Rol de Keycloak** | `realm-admin` en el realm objetivo, o un administrador del servidor |
| **Realm** | El realm al que pertenecen los usuarios de digna, no necesariamente `master` |
| **URI de redirección de digna** | La URL a la que los usuarios vuelven tras iniciar sesión, p. ej. `https://digna.yourdomain.com/oidc/callback` |

---

## Paso 1: Seleccione el realm

1. Abra la consola de administración de Keycloak
2. Use el selector de realm en la esquina superior izquierda para cambiar al realm en el que están sus usuarios

!!! warning "No use el realm master"

    El realm `master` está destinado a administrar el propio Keycloak. Los clientes de las aplicaciones deben estar en un realm dedicado; poner digna en `master` da a sus usuarios una vía al panel de administración de Keycloak.

---

## Paso 2: Cree el cliente

1. Vaya a **Clients** y haga clic en **Create client**
2. Configure:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — esto se convertirá en `DIGNA_OIDC_CLIENT_ID`
3. Haga clic en **Next**
4. En el paso **Capability config**, active **Client authentication**
5. Deje **Standard flow** habilitado; los otros flujos no son necesarios
6. Haga clic en **Next**

!!! warning "La autenticación del cliente debe estar activada"

    Si **Client authentication** está desactivada, Keycloak crea un cliente *public*, que no tiene credenciales en absoluto — la pestaña **Credentials** en el Paso 4 no existirá. digna necesita un cliente confidential. Este ajuste puede cambiarse después de la creación si lo configuró mal.

---

## Paso 3: Establezca la URI de redirección

En el paso **Login settings** (o en la pestaña **Settings** posteriormente):

1. **Valid redirect URIs**: introduzca la URL de callback de digna:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: déjelo vacío, o póngalo en `+` para reflejar las redirect URIs
3. Haga clic en **Save**

!!! tip "Evite los comodines"

    Keycloak acepta patrones como `https://digna.yourdomain.com/*`. Un comodín permite que cualquier ruta en ese host reciba un código de autorización, por lo que es preferible usar la URL exacta de callback.

---

## Paso 4: Obtenga el secreto del cliente

1. Abra la pestaña **Credentials**
2. Confirme que **Client Authenticator** es *Client Id and Secret*
3. Copie el **Client secret** → se convertirá en `DIGNA_OIDC_CLIENT_SECRET`

El secreto permanece recuperable aquí y puede regenerarse con **Regenerate**.

---

## Paso 5: Construya la URL de descubrimiento

Sustituya su host de Keycloak y el nombre del realm:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Por ejemplo:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 y versiones anteriores incluyen /auth"

    Antes de Keycloak 17, todos los endpoints estaban bajo el prefijo `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Las distribuciones que establecen `KC_HTTP_RELATIVE_PATH=/auth` mantienen el diseño antiguo también en versiones actuales. Si la URL sin `/auth` devuelve 404, inténtela con `/auth`.

Abra la URL en un navegador antes de continuar. Un documento JSON confirma que el host y el realm son correctos.

---

## Paso 6: Configure digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

La `key` en ambos archivos debe coincidir — `keycloak` aquí. Tenga en cuenta que no tiene que ser igual al **Client ID** de Keycloak, aunque mantenerlos iguales facilita el seguimiento.

---

## Paso 7: Pruebe

Reinicie el backend y el servidor web, luego abra el dashboard. Vea [Prueba de inicio de sesión](overview.md#testing-login) para la lista de comprobación completa.

---

## Resolución de problemas de Keycloak

### Invalid parameter: redirect_uri

La URL de callback no está cubierta por **Valid redirect URIs**. Keycloak registra la URI que recibió en el registro del servidor, que es la forma más rápida de ver la discrepancia exacta.

### Falta la pestaña Credentials

El cliente es público. Active **Client authentication** en **Settings → Capability config**.

### 404 en la URL de descubrimiento

O bien el nombre del realm es incorrecto, o el despliegue usa el prefijo `/auth`. Compruebe la lista de realms en la consola de administración y pruebe ambas formas de URL.

### unauthorized_client o invalid_client

**Standard flow** está deshabilitado en **Capability config**, o el secreto fue regenerado en Keycloak sin actualizar `config.toml`.

### Errores de certificado desde el backend

Un Keycloak autohospedado detrás de un certificado privado o autofirmado hará que la llamada HTTPS saliente de digna al URL de descubrimiento falle. Instale la CA emisora en el almacén de confianza de la máquina que ejecuta el backend de digna.

---

## Véase también

- [Descripción general de Single Sign-On](overview.md) — referencia de configuración, pruebas y resolución general de problemas
- [Keycloak: Asegurando aplicaciones](https://www.keycloak.org/docs/latest/securing_apps/)
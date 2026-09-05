---
title: OneLogin SSO – Integración de Single Sign-On | Documentación de digna
description: Configure Single Sign-On para digna con OneLogin usando OpenID Connect — creación de la app OIDC, URIs de redirección, credenciales de cliente, autenticación del endpoint de token y la configuración correspondiente en digna.
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, autenticación del endpoint de token, autenticación empresarial
---

# Configurar SSO con OneLogin

OneLogin es compatible con OIDC. Su característica distintiva es que el tipo de conector se elige desde un catálogo cuando se crea la aplicación y no puede cambiarse después.

Esta guía cubre el **lado de OneLogin**: crear la aplicación y recopilar los valores que digna necesita. El lado de digna — `dashboard_config.toml`, pruebas y resolución de problemas — es el mismo para todos los proveedores y se describe en la [Descripción general de Single Sign-On](overview.md).

---

## Antes de Empezar

| Requisito | Notas |
|---|---|
| **OneLogin role** | Account owner or an administrator permitted to add applications |
| **Subdomain** | e.g. `yourcompany.onelogin.com` |
| **digna redirect URI** | La URL a la que los usuarios vuelven tras iniciar sesión, p. ej. `https://digna.yourdomain.com/oidc/callback` |

---

## Paso 1: Crear la Aplicación OIDC

1. Inicie sesión en el portal de administración de OneLogin
2. Vaya a **Applications → Applications**
3. Haga clic en **Add App**
4. Busque `OpenId Connect` y seleccione el conector **OpenId Connect (OIDC)**
5. Establezca el **Display Name** en `digna`
6. Haga clic en **Save**

!!! warning "El tipo de conector queda fijado al crearlo"

    OneLogin tiene entradas de catálogo separadas para SAML y OIDC, y una aplicación no se puede convertir de una a otra. Si elige por error un conector SAML, elimine la aplicación y añádala de nuevo: no existe ninguna opción para cambiar el protocolo.

---

## Paso 2: Configure la URI de Redirección

1. Abra la pestaña **Configuration**
2. En **Redirect URI's**, introduzca su URL de callback de digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Opcionalmente establezca **Post Logout Redirect URIs** en la URL de su dashboard
4. Haga clic en **Save**

!!! note "Una URI por línea"

    A diferencia de los proveedores que esperan una lista separada por comas, el campo **Redirect URI's** de OneLogin acepta una URI por línea.

---

## Paso 3: Configure el Tipo de Aplicación y el Método de Autenticación

1. Abra la pestaña **SSO**
2. Confirme que **Application Type** sea *Web*
3. Establezca **Token Endpoint → Authentication Method** en *POST* (`client_secret_post`) o *Basic* (`client_secret_basic`)

!!! warning "No seleccione None"

    Establecer el método de autenticación en *None* convierte la aplicación en un cliente público sin secreto, y el intercambio de código en el backend de digna será rechazado. Tanto POST como Basic funcionan.

---

## Paso 4: Recopile las Credenciales

Aún en la pestaña **SSO**:

- **Client ID** → se convierte en `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → se convierte en `DIGNA_OIDC_CLIENT_SECRET` (haga clic en **Show client secret**)

La página también muestra la **Issuer URL**, que confirma la URL de discovery en el siguiente paso.

---

## Paso 5: Asigne Usuarios

1. Abra la pestaña **Access**
2. Añada los roles o grupos cuyos miembros puedan usar digna
3. Haga clic en **Save**

!!! note "Los usuarios no asignados son rechazados después del inicio de sesión"

    Como con la mayoría de los proveedores, OneLogin autentica al usuario primero y comprueba la pertenencia después. Un usuario no asignado inicia sesión correctamente y luego es rechazado, lo que se parece más a un error de digna que a una decisión de control de acceso.

---

## Paso 6: Construya la URL de Discovery

Sustituya su subdominio de OneLogin:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Por ejemplo:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "El /2 es la versión de la API"

    La implementación OIDC actual de OneLogin vive bajo `/oidc/2/`. La documentación antigua muestra `/oidc/` sin versión, que apunta a la primera versión retirada. Compruebe la **Issuer URL** en la pestaña SSO si tiene dudas: la URL de discovery es el issuer más `/.well-known/openid-configuration`.

---

## Paso 7: Configure digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Iniciar sesión con OneLogin"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

La `key` en ambos archivos debe coincidir — `onelogin` aquí.

---

## Paso 8: Pruebe

Reinicie el backend y el servidor web, luego abra el dashboard. Consulte [Probar inicio de sesión](overview.md#testing-login) para la lista de verificación completa.

---

## Solución de Problemas de OneLogin

### redirect_uri did not match

La URL de callback falta en **Configuration → Redirect URI's**, o las entradas se separaron por comas en lugar de saltos de línea.

### invalid_client at the Token Step

**Token Endpoint → Authentication Method** está configurado en *None*, o el client secret en `config.toml` está obsoleto. Revele el secreto en la pestaña **SSO** y compárelo.

### La app no aparece para los usuarios

No se ha concedido acceso a ningún rol o grupo en la pestaña **Access**.

### 404 en la URL de Discovery

El subdominio es incorrecto, o la URL omite `/oidc/2/`. Compárelo con la **Issuer URL** que se muestra en la pestaña SSO.

---

## Véase también

- [Descripción general de Single Sign-On](overview.md) — referencia de configuración, pruebas y solución de problemas general
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)
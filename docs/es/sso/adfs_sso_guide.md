---
title: AD FS SSO – Integración de inicio de sesión único | Documentación de digna
description: Configure Single Sign-On para digna con Active Directory Federation Services usando OpenID Connect — grupo de aplicaciones, aplicación del servidor, secreto compartido, ámbitos permitidos y la configuración correspondiente en digna.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, active directory federation services, adfs oidc, grupo de aplicaciones, openid connect, proveedor de identidad on-premises
---

# Configurar SSO con AD FS

Active Directory Federation Services es la opción on‑premises: sus propios servidores emiten los tokens y la URL de descubrimiento es su propio nombre de host. AD FS soporta OpenID Connect desde **Windows Server 2016** en adelante.

Esta guía cubre el **lado de AD FS**: crear el grupo de aplicaciones y recopilar los valores que digna necesita. El lado de digna — `dashboard_config.toml`, pruebas y resolución de problemas — es el mismo para cualquier proveedor y se describe en la [Visión general de Single Sign-On](overview.md).

---

## Antes de Empezar

| Requisito | Notas |
|---|---|
| **Versión de AD FS** | Windows Server 2016 o posterior — las versiones anteriores no tienen soporte OIDC |
| **Acceso** | Administrador local en el servidor AD FS |
| **Nombre del servicio de federación** | p. ej. `adfs.yourdomain.com` |
| **URI de redirección de digna** | La URL a la que los usuarios regresan después del inicio de sesión, p. ej. `https://digna.yourdomain.com/oidc/callback` |

---

## Paso 1: Crear el Grupo de Aplicaciones

1. En el servidor AD FS, abra **AD FS Management**
2. Haga clic derecho en **Application Groups** y elija **Add Application Group**
3. Introduzca `digna` como nombre
4. Bajo **Standalone applications** — o **Client-Server applications** dependiendo de su versión — seleccione **Server application accessing a web API**
5. Haga clic en **Next**

---

## Paso 2: Configurar la Aplicación del Servidor

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS genera un GUID. Cópielo — esto será `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: introduzca su URL de callback de digna y haga clic en **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Haga clic en **Next**

!!! warning "Haga clic en Add, no solo en Next"

    El campo Redirect URI tiene su propio botón **Add**. Si escribe una URI y hace clic en **Next** sin pulsar **Add**, se descarta y el asistente no lo avisa. Confirme que la URI aparece en la lista debajo del campo antes de continuar.

---

## Paso 3: Generar el Secreto Compartido

1. Marque **Generate a shared secret**
2. Copie el secreto generado → pasa a ser `DIGNA_OIDC_CLIENT_SECRET`
3. Haga clic en **Next**

!!! warning "El secreto solo se muestra una vez"

    AD FS muestra el secreto compartido únicamente en esta página del asistente y no puede mostrarlo de nuevo. Si lo pierde, restablézcalo más tarde desde las propiedades del grupo de aplicaciones.

---

## Paso 4: Configurar la Web API

1. **Identifier**: introduzca el mismo client identifier del Paso 2 y haga clic en **Add**
2. Haga clic en **Next**
3. Elija una **Access Control Policy** — *Permit everyone* es el punto de partida más sencillo; restrínjala a un grupo en producción
4. Haga clic en **Next**

---

## Paso 5: Conceder los Scopes Permitidos

En el paso **Configure Application Permissions**, marque:

- `openid`
- `profile`
- `email`

Luego haga clic en **Next** y complete el asistente.

!!! warning "openid no está marcado por defecto"

    AD FS preselecciona solo `user_impersonation` en algunas versiones. Sin `openid`, el endpoint de token devuelve un token de acceso OAuth en lugar de un ID token, y digna no puede identificar al usuario.

---

## Paso 6: Confirmar el Endpoint de Descubrimiento

Sustituya su nombre del servicio de federación:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Por ejemplo:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Ábralo en un navegador. Un documento JSON confirma que OIDC está habilitado y que el nombre de host es correcto.

!!! note "El backend debe confiar en el certificado"

    Es habitual que AD FS use una autoridad de certificación interna. La máquina que ejecuta el backend de digna realiza su propia llamada HTTPS saliente a esta URL, por lo que la CA emisora debe estar en el almacén de confianza de esa máquina — no solo en los navegadores de las personas que inician sesión.

---

## Paso 7: Configurar digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Iniciar sesión con Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

La `key` en ambos archivos debe coincidir — `adfs` en este ejemplo.

---

## Paso 8: Probar

Reinicie el backend y el servidor web, luego abra el dashboard. Consulte [Pruebas de inicio de sesión](overview.md#testing-login) para la lista de verificación completa.

---

## Resolución de Problemas de AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

El identificador de la web API del Paso 4 no coincide con el client identifier, o no se concedieron los scopes en el Paso 5. Ambos son editables desde las propiedades del grupo de aplicaciones.

### MSIS9602: Invalid redirect_uri

La URI se escribió pero no se añadió con el botón **Add**, o difiere de `DIGNA_OIDC_REDIRECT_URI`. Verifique **Application Groups → digna → digna backend → Properties**.

### No se Devuelve un ID Token

Falta el scope `openid` en los permisos de la aplicación.

### El Backend No Puede Alcanzar la URL de Descubrimiento

O bien el DNS del host del backend no resuelve el nombre del servicio de federación, o el certificado de AD FS no es de confianza allí. Pruebe con `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` desde el servidor de digna.

### Eventos a Comprobar

El servidor AD FS registra fallos en **Applications and Services Logs → AD FS → Admin** en Event Viewer, normalmente con una razón más específica que la que muestra el navegador.

---

## Véase también

- [Visión general de Single Sign-On](overview.md) — referencia de configuración, pruebas y resolución general de problemas
- [Microsoft: Escenarios de OpenID Connect en AD FS](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
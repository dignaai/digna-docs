# Configurar SSO con PingOne

PingOne es compatible con OIDC. Dos de sus valores requieren atención: el **ID de entorno**, que aparece en cada URL de endpoint, y el **dominio regional**, que difiere entre los tenants de Norteamérica, Europa, Canadá, Asia-Pacífico y Australia.

Esta guía cubre el **lado de PingOne**: crear la aplicación y recopilar los valores que digna necesita. El lado de digna — `dashboard_config.toml`, pruebas y solución de problemas — es el mismo para todos los proveedores y se describe en la [Descripción general de Single Sign-On](overview.md).

---

## Antes de empezar

| Requisito | Notas |
|---|---|
| **Rol en PingOne** | Environment Admin o Identity Data Admin en el entorno objetivo |
| **Entorno** | El entorno de PingOne al que pertenecen los usuarios de digna |
| **URI de redirección de digna** | La URL a la que los usuarios regresan después del inicio de sesión, p. ej. `https://digna.yourdomain.com/oidc/callback` |

---

## Paso 1: Crear la aplicación

1. Inicie sesión en la consola de administración de PingOne y seleccione su entorno
2. Vaya a **Applications → Applications**
3. Haga clic en el botón **+**
4. Introduzca `digna` como **Application Name**
5. Seleccione **OIDC Web App**
6. Haga clic en **Save**

!!! warning "Elija OIDC Web App, no Single-Page App"

    *Single-Page App* y *Native App* crean clientes públicos que no pueden mantener un secreto. digna intercambia el código de autorización desde su backend y necesita el tipo confidencial **OIDC Web App**.

---

## Paso 2: Configurar la URI de redirección

1. Abra la pestaña **Configuration** de la aplicación
2. Haga clic en el icono de lápiz para editar
3. Compruebe que **Response Type** esté en *Code* y **Grant Type** en *Authorization Code*
4. En **Redirect URIs**, introduzca su URL de callback de digna:

```
https://digna.yourdomain.com/oidc/callback
```

5. Configure **Token Endpoint Authentication Method** en *Client Secret Post* o *Client Secret Basic*
6. Haga clic en **Save**

---

## Paso 3: Habilitar la aplicación

En la fila o panel de detalles de la aplicación, cambie el interruptor a **enabled**.

!!! warning "Las aplicaciones nuevas empiezan deshabilitadas"

    PingOne crea las aplicaciones en estado deshabilitado. Una aplicación deshabilitada produce un error en el paso de autorización que no menciona el interruptor, así que vale la pena confirmar esto antes de depurar cualquier otra cosa.

---

## Paso 4: Conceder los scopes

1. Abra la pestaña **Resources**
2. Confirme que `openid` esté concedido, y añada `profile` y `email` desde el recurso **OpenID Connect**
3. Haga clic en **Save**

---

## Paso 5: Asignar usuarios

1. Abra la pestaña **Access**
2. Añada la población o los grupos cuyos miembros puedan usar digna
3. Haga clic en **Save**

---

## Paso 6: Recopilar las credenciales y el ID de entorno

En la pestaña **Configuration**, expanda **General**:

- **Client ID** → se convierte en `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → se convierte en `DIGNA_OIDC_CLIENT_SECRET` (haga clic en el icono del ojo)
- **Environment ID** → se utiliza en la URL de descubrimiento

La misma pestaña lista el **OIDC Discovery Endpoint** ya formado, que puede copiar directamente en lugar de montarlo a mano.

---

## Paso 7: Construir la URL de descubrimiento

Sustituya el ID de entorno y el dominio por el de su región:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Región | Dominio |
|---|---|
| Norteamérica | `auth.pingone.com` |
| Europa | `auth.pingone.eu` |
| Canadá | `auth.pingone.ca` |
| Asia-Pacífico | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

Para un entorno europeo:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Cópialo en vez de escribirlo"

    El dominio regional es el error más común en una integración con PingOne, y una región equivocada devuelve un 404 en lugar de un mensaje útil. Use el valor **OIDC Discovery Endpoint** del Paso 6.

---

## Paso 8: Configurar digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

La `key` en ambos archivos debe coincidir — `pingone` aquí.

---

## Paso 9: Probar

Reinicie el backend y el servidor web, luego abra el dashboard. Vea [Probar inicio de sesión](overview.md#testing-login) para la lista de verificación completa.

---

## Solución de problemas de PingOne

### 404 en la URL de descubrimiento

El dominio regional o el ID de entorno es incorrecto. Compare con el **OIDC Discovery Endpoint** que se muestra en la pestaña Configuration de la aplicación.

### NOT_FOUND o aplicación deshabilitada

El interruptor de la aplicación del Paso 3 sigue apagado.

### Coincidencia de URI de redirección incorrecta

PingOne compara la cadena completa. Compruebe **Configuration → Redirect URIs** por una barra final o una diferencia en el esquema.

### El inicio de sesión tiene éxito pero no llega el claim de email a digna

No se han concedido los scopes `email` y `profile` en la pestaña **Resources**.

### El usuario no puede ver la aplicación

No se ha concedido acceso a ninguna población o grupo en la pestaña **Access**.

---

## Véase también

- [Descripción general de Single Sign-On](overview.md) — referencia de configuración, pruebas y solución de problemas general
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)
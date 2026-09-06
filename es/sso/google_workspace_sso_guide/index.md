# Configurar SSO con Google Workspace

La plataforma de identidad de Google cumple con OIDC y utiliza una única URL de descubrimiento well-known para todos los clientes, por lo que los únicos valores por organización son el client ID y el secret.

Esta guía cubre el **lado de Google**: crear el cliente OAuth y recopilar los valores que digna necesita. El lado de digna — `dashboard_config.toml`, pruebas y resolución de problemas — es el mismo para todos los proveedores y se describe en la [Descripción general de Single Sign-On](overview.md).

---

## Antes de comenzar

| Requisito | Notas |
|---|---|
| **Google Cloud project** | Cualquier proyecto en la misma organización que su dominio Workspace |
| **Role** | Editor u Owner en el proyecto |
| **digna redirect URI** | La URL a la que los usuarios regresan después del inicio de sesión, p. ej. `https://digna.yourdomain.com/oidc/callback` |

---

## Paso 1: Configurar la pantalla de consentimiento de OAuth

Google no emitirá credenciales hasta que exista la pantalla de consentimiento.

1. Abra la [Consola de Google Cloud](https://console.cloud.google.com) y seleccione su proyecto
2. Vaya a **APIs & Services → OAuth consent screen**
3. Elija el tipo de usuario:
   - **Internal** — solo las cuentas de su dominio Workspace pueden iniciar sesión. Recomendado.
   - **External** — cualquier cuenta de Google puede intentar iniciar sesión.
4. Rellene el nombre de la app, el correo de soporte al usuario y el correo de contacto del desarrollador
5. En el paso **Scopes**, añada `openid`, `.../auth/userinfo.email` y `.../auth/userinfo.profile`
6. Guardar

!!! warning "Las aplicaciones externas deben publicarse"

    Una pantalla de consentimiento **External** comienza en estado *Testing*, donde solo las cuentas añadidas explícitamente a la lista de test-users pueden completar un inicio de sesión. El resto verá "digna has not completed the Google verification process". Cambie la app a **In production** en **Publishing status**, o use **Internal** — que no tiene tal restricción y es la opción adecuada para un despliegue limitado a Workspace.

---

## Paso 2: Crear el cliente OAuth

1. Vaya a **APIs & Services → Credentials**
2. Haga clic en **Create Credentials → OAuth client ID**
3. Establezca **Application type** en **Web application**
4. Déle un nombre, p. ej. `digna`
5. En **Authorized redirect URIs**, haga clic en **Add URI** e introduzca:

```
https://digna.yourdomain.com/oidc/callback
```

6. Haga clic en **Create**

!!! note "No se necesitan Authorized JavaScript Origins"

    digna intercambia el authorization code desde el backend, no desde el navegador, así que el campo **Authorized JavaScript origins** puede dejarse vacío. Solo importa la redirect URI.

---

## Paso 3: Recopilar las credenciales

El diálogo que aparece tras la creación muestra:

- **Client ID** — termina en `.apps.googleusercontent.com` → se convierte en `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → se convierte en `DIGNA_OIDC_CLIENT_SECRET`

Ambos pueden recuperarse más tarde desde la página de detalles de las credenciales, a diferencia de la mayoría de otros proveedores.

---

## Paso 4: La URL de descubrimiento

Google usa una única URL de descubrimiento para todos los clientes — no hay nada que sustituir:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Paso 5: Configurar digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

La `key` en ambos archivos debe coincidir — `google` aquí.

---

## Paso 6: Probar

Reinicie el backend y el servidor web, luego abra el dashboard. Vea [Prueba de inicio de sesión](overview.md#testing-login) para la lista de verificación completa.

---

## Resolución de problemas de Google Workspace

### Error 400: redirect_uri_mismatch

La URI en `DIGNA_OIDC_REDIRECT_URI` no está en la lista de **Authorized redirect URIs**, o difiere por una barra final o por el esquema. La página de error de Google muestra la URI que recibió — compárela carácter por carácter con la registrada.

### Esta aplicación está bloqueada / No ha completado la verificación

La pantalla de consentimiento es **External** y todavía está en *Testing*. Publíquela, o cambie la app a **Internal**.

### Acceso bloqueado: Authorization Error

La cuenta que intenta iniciar sesión está fuera de su dominio Workspace mientras la pantalla de consentimiento es **Internal**. Este es el comportamiento previsto — las apps Internal aceptan solo cuentas de la organización.

### Los cambios tardan varios minutos

Google propaga los cambios de credenciales y de la pantalla de consentimiento de forma asíncrona. Una redirect URI añadida recientemente puede tardar unos minutos en surtir efecto; si un cambio parece ignorado, espere y vuelva a intentarlo antes de investigar más a fondo.

---

## Véase también

- [Descripción general de Single Sign-On](overview.md) — referencia de configuración, pruebas y resolución general de problemas
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
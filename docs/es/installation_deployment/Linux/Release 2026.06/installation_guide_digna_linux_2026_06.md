---
title: Guía de instalación en Linux – digna Release 2026.06 | Documentación de digna
description: Guía paso a paso para instalar digna Release 2026.06 en Linux — requisitos del sistema, configuración de PostgreSQL, configuración de nginx o Apache, configuración del backend y del dashboard, ejecución de digna como servicio systemd y actualización a una nueva versión.
keywords: instalación digna linux, guía de despliegue digna, configuración backend digna, instalación dashboard digna, postgresql linux, nginx linux, servicio systemd digna, guía de actualización digna
image: /assets/logo_square.png
---

# Guía de instalación en Linux para digna Release 2026.06

**Versión:** 2026.06

**Última actualización:** 5 de septiembre de 2026


---

## Tabla de contenidos

1. [Introducción](#introduction)
2. [Requisitos del sistema](#system-requirements)
3. [Preparación antes de la instalación](#pre-installation-setup)
4. [Configuración del servidor PostgreSQL](#postgresql-server-setup)
5. [Configuración del servidor web](#web-server-configuration)
6. [Instalación inicial](#initial-installation)
7. [Configuración del backend](#backend-configuration)
8. [Configuración del dashboard](#dashboard-configuration)
9. [Ejecutar digna como servicio systemd](#running-digna-as-a-systemd-service)
10. [Actualización a una nueva versión](#upgrading-to-a-new-release)

---

## Introducción {: #introduction }

### Acerca de digna

digna es una plataforma completa impulsada por IA diseñada para optimizar la gestión de la calidad de datos en distintos entornos de datos como almacenes, data lakes y lakehouses. Diseñada para ser altamente escalable y adaptable, digna aborda los retos modernos de datos mediante automatización, monitorización en tiempo real y detección de anomalías.

digna consta de dos componentes principales:

- **dignabackend**: El motor central de la aplicación, responsable de procesar datos y ejecutar las comprobaciones de calidad.
- **dignadashboard**: Una interfaz web alojada en un servidor web, que proporciona una forma amigable de interactuar con la plataforma digna y visualizar métricas de calidad de datos.

### Novedades en la Release 2026.06

Esta versión incorpora capacidades de observabilidad de datos directamente en tu código, permitiendo a los desarrolladores supervisar la calidad de los datos en el origen. Consulta las [notas de la versión](http://docs.digna.ai/changelog/Release_202606/) para obtener detalles completos.

### ¿Buscas Windows o macOS?

Esta guía cubre Linux. Para otras plataformas, consulta la [Guía de instalación para Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) o la [Guía de instalación para macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

### ¿Qué distribución cubre esta guía?

Las instrucciones están escritas para las dos familias de servidor más comunes. Donde difieren, se muestran ambos comandos:

- **familia Debian** — Debian, Ubuntu. Gestor de paquetes: `apt`.
- **familia RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Gestor de paquetes: `dnf`.

Cualquier distribución moderna con `systemd` funcionará; solo cambian algunos nombres de paquetes y rutas de configuración.

---

## Requisitos del sistema {: #system-requirements }

Antes de comenzar la instalación, asegúrate de que tu sistema cumpla los siguientes requisitos mínimos:

| Requisito | Especificación |
|---|---|
| **Sistema operativo** | Ubuntu 22.04 LTS o posterior, Debian 12 o posterior, RHEL 9 / Rocky 9 / AlmaLinux 9 o posterior |
| **Arquitectura** | x86_64 (amd64) o arm64 |
| **Sistema init** | systemd |
| **Memoria (instalación mínima)** | 16 GB de RAM |
| **Espacio en disco** | 10 GB de almacenamiento disponible |
| **Base de datos** | PostgreSQL Server 12 o superior |
| **Servidor web** | nginx, Apache httpd u equivalente |

### Opciones de instalación de la base de datos

**Si PostgreSQL ya está instalado:**
Puedes añadir una nueva base de datos para digna en tu servidor PostgreSQL existente.

**Si vas a instalar PostgreSQL en la misma máquina que digna:**

!!! info "Especificaciones recomendadas"

    - **Memoria**: 32 GB de RAM (en lugar de 16 GB)
    - **Espacio en disco**: 50 GB de almacenamiento disponible (en lugar de 10 GB)

    Estas especificaciones superiores permiten que digna y la base de datos PostgreSQL se ejecuten simultáneamente.

### Comprobar tu distribución y arquitectura

Varios comandos en esta guía difieren entre las familias Debian y RHEL. Para comprobar en cuál estás, ejecuta:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` o `ID=debian` — usa los comandos `apt`.
- `ID=rhel`, `rocky`, `almalinux` o `fedora` — usa los comandos `dnf`.
- `x86_64` o `aarch64` — la arquitectura del paquete de instalación que necesitas.

---

## Preparación antes de la instalación {: #pre-installation-setup }

Antes de instalar digna, asegúrate de que dos prerrequisitos clave estén en su lugar:

1. **Servidor PostgreSQL** – para almacenar métricas calculadas y datos de rendimiento
2. **Servidor web** – para alojar el dashboard de digna

Si estos componentes no están instalados, sigue las secciones siguientes para instalarlos y configurarlos.

### Actualizar el índice de paquetes

Actualiza las listas de paquetes antes de instalar cualquier cosa:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Nota"

    A lo largo de esta guía, el primer comando de cada par es para la **familia Debian** y el segundo para la **familia RHEL**. Ejecuta solo el que corresponda a tu sistema.

---

## Configuración del servidor PostgreSQL {: #postgresql-server-setup }

### Si ya tienes PostgreSQL

Si PostgreSQL ya está instalado y en ejecución en tu máquina local o si estás usando un servidor PostgreSQL gestionado de forma remota, puedes saltar a la [sección siguiente](#web-server-configuration).

### Instalación de PostgreSQL

#### Paso 1: Instalar el paquete del servidor

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Consejo"

    Los paquetes de la distribución pueden quedarse atrás respecto a la versión actual de PostgreSQL. Si necesitas una versión más nueva específica, usa el repositorio oficial de [PostgreSQL apt o yum](https://www.postgresql.org/download/linux/).

#### Paso 2: Inicializar el clúster de la base de datos

En la **familia Debian**, el paquete crea y arranca un clúster automáticamente — pasa al siguiente paso.

En la **familia RHEL**, el clúster debe crearse explícitamente:

```bash
sudo postgresql-setup --initdb
```

#### Paso 3: Iniciar y habilitar el servicio

```bash
sudo systemctl enable --now postgresql
```

Esto inicia PostgreSQL inmediatamente y lo configura para que arranque automáticamente en el inicio.

#### Paso 4: Verificar la instalación

```bash
psql --version
sudo systemctl status postgresql
```

Deberías ver la versión de PostgreSQL y el servicio con estado `active (running)`.

#### Paso 5: Conectarse al servidor

El paquete PostgreSQL para Linux crea una cuenta del sistema `postgres` que posee el clúster. Conéctate a través de ella:

```bash
sudo -u postgres psql
```

!!! note "Nota — Linux difiere de Windows aquí"

    El instalador de Windows te solicita establecer una contraseña para el superusuario `postgres` durante la instalación. Los paquetes de Linux no lo hacen. En su lugar, las conexiones locales se autentican mediante **peer authentication**: el usuario del sistema operativo `postgres` puede conectarse como el usuario de la base de datos `postgres` sin contraseña.

    Por eso el comando anterior usa `sudo -u postgres`. El backend de digna se conecta por TCP con un nombre de usuario y contraseña, por lo que crearás un usuario explícito para digna en [Instalación inicial](#initial-installation).

#### Paso 6: Confirmar el puerto

El puerto por defecto de PostgreSQL es `5432`. Para confirmar el puerto en el que tu servidor está escuchando:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Anota el valor — lo necesitarás al configurar el backend de digna.

#### Paso 7: Habilitar la autenticación por contraseña para el usuario digna

digna se conecta a PostgreSQL por TCP como `digna_user`, lo que requiere autenticación por contraseña en lugar de peer. Comprueba que tu `pg_hba.conf` lo permita.

Localiza el archivo:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Ábrelo en un editor y confirma que las líneas TCP locales usen `scram-sha-256` (o `md5` en servidores más antiguos) en lugar de `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Recarga PostgreSQL tras cualquier cambio:

```bash
sudo systemctl reload postgresql
```

!!! warning "Importante"

    Si digna informa `FATAL: Ident authentication failed for user "digna_user"`, esta configuración es la causa.

#### Paso 8: Si PostgreSQL se ejecuta en otra máquina

Para aceptar conexiones desde un host distinto, ajusta `listen_addresses` en `postgresql.conf` y añade una línea `host` correspondiente para tu red en `pg_hba.conf`:

```
listen_addresses = '*'
```

Luego abre el puerto en el cortafuegos y reinicia el servicio:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Configuración del servidor web {: #web-server-configuration }

digna requiere un servidor web para alojar el dashboard. Elige una de las siguientes opciones:

- [nginx](#nginx-setup) — ligero y recomendado
- [Apache httpd](#apache-setup) — alternativa ampliamente desplegada

Solo necesitas instalar y configurar **uno** de estos servidores.

Ambas secciones configuran dos cosas de las que depende el dashboard:

- **Fallback para aplicaciones de una sola página (SPA)**, para que refrescar una URL del dashboard no devuelva un 404
- **Un tipo MIME para `.md`**, para que los archivos Markdown se sirvan correctamente

### Configuración de nginx {: #nginx-setup }

#### Descripción general

nginx es un servidor web ligero y de alto rendimiento, bien adaptado para servir el dashboard estático de digna.

#### Instalación

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Iniciar nginx

```bash
sudo systemctl enable --now nginx
```

#### Verificar la instalación

1. Abre tu navegador
2. Navega a `http://localhost`
3. Deberías ver la página de bienvenida de nginx

#### Abrir el cortafuegos

Si el servidor va a ser accesible desde otras máquinas, permite el tráfico HTTP:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Configurar un sitio para el dashboard

nginx incluye todos los archivos de su directorio `conf.d` en ambas familias de distribución. Crea un archivo de configuración dedicado para digna allí:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Pega lo siguiente, reemplazando `/opt/digna/dashboard` por la ruta real a tu carpeta `dashboard` extraída:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Importante"

    Sin la directiva `try_files`, recargar cualquier página del dashboard distinta de la URL raíz devolverá un 404. Esto es el equivalente en nginx del módulo URL Rewrite requerido por IIS en Windows.

#### Deshabilitar el sitio por defecto

Solo puede haber un bloque server que sea `default_server` para un puerto. En la **familia Debian**, elimina el sitio por defecto empaquetado para que no entre en conflicto:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

En la **familia RHEL**, comenta o elimina el bloque `server { ... }` dentro de `/etc/nginx/nginx.conf`.

#### Aplicar la configuración

Prueba la configuración en busca de errores de sintaxis y luego recarga nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Configuración de Apache httpd {: #apache-setup }

#### Descripción general

Apache httpd está disponible en los repositorios predeterminados de todas las distribuciones compatibles. El paquete se llama `apache2` en la familia Debian y `httpd` en la familia RHEL.

#### Instalación

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Iniciar Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Verificar la instalación

1. Abre tu navegador
2. Navega a `http://localhost`
3. Deberías ver la página predeterminada de Apache de la distribución

#### Requisito: habilitar mod_rewrite

El dashboard requiere reescritura de URL.

En la **familia Debian**, habilita el módulo y reinicia:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

En la **familia RHEL**, `mod_rewrite` se carga por defecto. Compruébalo:

```bash
httpd -M | grep rewrite
```

#### Requisito: permitir overrides con .htaccess

Abre el archivo de configuración de la raíz de documentos:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Localiza el bloque `<Directory>` que cubre tu raíz de documentos (`/var/www/html` en ambas familias) y cambia:

```apache
AllowOverride None
```

por:

```apache
AllowOverride All
```

#### Requisito: tipo MIME para archivos Markdown

En el mismo archivo, añade la siguiente línea para que los archivos Markdown se sirvan correctamente:

```apache
AddType text/markdown .md
```

!!! warning "Importante"

    Sin esta configuración, los archivos `.md` pueden no servirse correctamente.

#### Aplicar la configuración

Comprueba la configuración en busca de errores de sintaxis y luego reinicia Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Instalación inicial {: #initial-installation }

### Paso 1: Configurar el repositorio de digna

El repositorio de digna almacena todas las métricas calculadas por digna. Actúa como la base de datos central para datos analíticos y de rendimiento.

#### Crear esquema y usuario del repositorio

Abre tu cliente PostgreSQL (psql, pgAdmin o similar) y ejecuta las siguientes sentencias SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Reemplaza los siguientes marcadores de posición:**

- `<digna_repo_schema>` — El nombre de esquema que desees (por ej., `dignarepo`)
- `<digna_repo_user>` — El nombre de usuario que desees (por ej., `digna_user`)
- `<digna_repo_password>` — Una contraseña segura para este usuario

**Ejemplo:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Para ejecutar esto desde la shell en un solo paso:

```bash
sudo -u postgres psql
```

Luego pega las sentencias en el prompt `postgres=#` y escribe `\q` para salir.

!!! tip "Mejor práctica"

    Usa contraseñas fuertes y complejas para los usuarios de la base de datos. Evita credenciales fácilmente adivinables.

---

### Paso 2: Extraer el paquete de instalación de digna

1. Localiza el archivo ZIP de instalación de digna que se te proporcionó
2. Extrae su contenido en la ubicación deseada — por ejemplo `/opt/digna`
3. Después de la extracción, deberías ver los siguientes elementos:
   - `dashboard/` — Interfaz web del dashboard
   - `digna` — Ejecutable principal (backend + CLI combinados)
   - `config.toml` — Archivo de configuración
   - `license.toml` — Archivo de licencia (copia el tuyo aquí)

Para extraerlo desde la shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Nota"

    Si `unzip` no está instalado, añádelo con `sudo apt install -y unzip` o `sudo dnf install -y unzip`.

#### Hacer el ejecutable ejecutable

Dependiendo de cómo se transfirió el archivo, el bit de ejecutable puede no preservarse tras la extracción. Establécelo explícitamente:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Crear una cuenta de servicio

Se recomienda ejecutar el backend como un usuario dedicado y sin privilegios para despliegues en producción:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Nota"

    En la familia RHEL la ruta de shell equivalente es `/sbin/nologin`.

### Paso 3: Instalar el archivo de licencia

!!! warning "Importante"

    El archivo de licencia **no** está incluido en el paquete de instalación y se te proporcionará por separado desde digna.

1. Localiza el archivo `license.toml` que se te proporcionó
2. Cópialo al directorio raíz de instalación de digna (donde están `config.toml` y el ejecutable `digna`)

**Por qué es importante:**
El archivo de licencia contiene la información del cliente, la fecha de expiración y la firma digital. **No modifiques este archivo** — cualquier cambio lo invalidará.

**Estructura de directorios tras la configuración:**

```
/opt/digna/
├── config.toml         (archivo de configuración)
├── license.toml        (TU ARCHIVO DE LICENCIA - cópialo aquí)
├── digna               (ejecutable principal)
├── bin/                (scripts de gestión del servicio)
└── dashboard/          (interfaz web)
    └── (archivos del dashboard)
```

---

## Configuración del backend {: #backend-configuration }

### Paso 1: Crear y editar el archivo de configuración

El archivo `config_template.toml` se proporciona en tu directorio de instalación de digna. Solo necesitas renombrarlo a `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Ubicación:** `/opt/digna/config.toml`

Abre `config.toml` en un editor de texto y configura cada sección que se indica a continuación.

#### Sección [app]

Esta sección configura los ajustes de la aplicación del backend de digna:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parámetro | Valor | Notas |
|---|---|---|
| `digna_APP_HOST` | `localhost` o dirección IP | Nombre de host o IP donde se aloja dignabackend |
| `digna_APP_PORT` | `8082` (por defecto) | Puerto para los endpoints REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL del frontend | Si el dashboard está en un servidor distinto, incluye su URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Requerido para CORS con credenciales |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Permitir todos los métodos HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Permitir todos los encabezados |

!!! note "Nota"

    Si sirves el dashboard desde nginx o Apache en el puerto HTTP por defecto, el origen a permitir es `http://localhost` — o la URL pública del servidor cuando el dashboard se accede desde otras máquinas.

#### Sección [repo]

Esta sección configura la conexión a la base de datos PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parámetro | Valor | Notas |
|---|---|---|
| `digna_REPO_HOST` | `localhost` o IP | Hostname/IP del servidor PostgreSQL |
| `digna_REPO_PORT` | `5432` (por defecto) | Puerto de PostgreSQL |
| `digna_REPO_DB` | `postgres` | Nombre de la base de datos |
| `digna_REPO_SCHEMA` | `dignarepo` | Esquema creado anteriormente |
| `digna_REPO_USER` | `digna_user` | Usuario creado en la configuración de PostgreSQL |
| `digna_REPO_PASSWORD` | Tu contraseña | Contraseña establecida al crear el esquema |

!!! tip "Mejor práctica"

    `config.toml` contiene la contraseña de la base de datos en texto plano. Restringe sus permisos para que solo la cuenta del servicio pueda leerlo:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### Sección [base]

Esta sección contiene ajustes de seguridad y cookies:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parámetro | Valor | Notas |
|---|---|---|
| `digna_FERNET_KEY` | Clave de encriptación | Usada para cifrar tokens y cookies (se proporciona una por defecto) |
| `digna_COOKIE_DOMAIN` | `localhost` | Coincidir con tu dominio del frontend |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (producción) | Usa `true` para conexiones HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Siempre habilitado por seguridad |
| `digna_COOKIE_SAME_SITE` | `lax` | Previene ataques CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 horas) | Tiempo de expiración de sesión en segundos |
| `digna_MAX_WORKERS` | Número de núcleos de CPU - 1 | Número de tareas de inspección en paralelo |

!!! tip "Consejo"

    Para saber el número de núcleos de CPU disponibles en tu servidor, ejecuta `nproc`.

#### Sección [logging]

Esta sección configura el comportamiento del registro:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parámetro | Valor | Notas |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` para producción, `DEBUG` para resolución de problemas |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Número de copias diarias de registros a conservar |

---

### Paso 2: Inicializar el repositorio

1. Abre un terminal
2. Navega al directorio de instalación de digna (donde están `config.toml` y el ejecutable `digna`)
3. Ejecuta la prueba de conexión:

```bash
cd /opt/digna
./digna repo check
```

Deberías ver una confirmación de que la conexión se ha establecido (el repositorio en sí aún no se ha inicializado).

!!! note "Nota"

    En Linux, el directorio actual no está en tu PATH, por lo que el ejecutable se invoca como `./digna` en lugar de `digna`. Para usar la forma corta en cualquier lugar, añade un enlace simbólico:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Paso 3: Instalar el esquema del repositorio

En el mismo directorio, ejecuta:

```bash
./digna repo install
```

Este comando instala las tablas y el esquema necesarios en tu base de datos PostgreSQL.

### Paso 4: Iniciar el servidor digna

En el directorio de instalación de digna, inicia el servidor con:

```bash
./digna serve --address <host> --port <port>
```

**Parámetros:**
- `--address` — Nombre de host/IP del servidor
- `--port` — Puerto del servidor

Deberías ver mensajes de inicio que confirmen que el servidor se está ejecutando:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Consejo"

    Si el dashboard se sirve desde una máquina distinta al backend, abre también el puerto de la API en el cortafuegos:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Paso 5: Crear un usuario administrador

1. Abre una ventana de terminal **nueva**
2. Navega al directorio de instalación de digna
3. Ejecuta el siguiente comando para crear un usuario administrador:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Ejemplo:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Esto crea un usuario con nombre `admin` y privilegios administrativos completos.

!!! tip "Consejo"

    Encierra la contraseña entre comillas simples. `bash` y `zsh` tratan caracteres como `!`, `$` y `*` de forma especial, y una contraseña sin comillas que contenga estos caracteres no se pasará tal y como se escribe.

!!! tip "Mejor práctica"

    Usa una contraseña fuerte con mezcla de mayúsculas, minúsculas, números y caracteres especiales.

---

## Configuración del dashboard {: #dashboard-configuration }

### Paso 1: Desplegar el dashboard en el servidor web

El dashboard de digna tiene su propio archivo `config.toml` ubicado en el directorio `dashboard/`. Esta configuración ya se proporciona y no requiere cambios durante la instalación inicial. Solo necesitas modificarla si requieres personalizar la conexión al backend.

Si necesitas cambiar la configuración del dashboard (por ejemplo, para despliegues multi-instancia), consulta la documentación del dashboard.

Elige tu servidor web y sigue los pasos de despliegue correspondientes.

#### Desplegar en nginx

Si seguiste la sección de [Configuración de nginx](#nginx-setup), el bloque del servidor ya apunta a tu carpeta `dashboard` y no es necesario copiar nada.

1. **Confirma la ruta**
   - Abre `/etc/nginx/conf.d/digna.conf`
   - Verifica que `root` apunte a tu carpeta `dashboard` extraída

2. **Asegura que la carpeta sea legible**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Recargar nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Probar la instalación**
   - Abre tu navegador
   - Navega a `http://localhost` (o la URL configurada)
   - Deberías ver la página de inicio de sesión del dashboard de digna

#### Desplegar en Apache httpd

1. **Copiar el dashboard al Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Agregar las reglas de reescritura**

   Crea un archivo `.htaccess` dentro de la carpeta desplegada para que las rutas del dashboard sobrevivan a un refresco del navegador:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Pega lo siguiente:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Reiniciar Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Acceder al dashboard**
   - Abre tu navegador
   - Navega a `http://localhost/digna`
   - Deberías ver la página de inicio de sesión del dashboard de digna

### Paso 2: SELinux (solo familia RHEL)

En RHEL, Rocky, AlmaLinux y Fedora, SELinux está en modo enforcing por defecto y bloqueará al servidor web para leer archivos fuera de sus ubicaciones esperadas. Comprueba si está activo:

```bash
getenforce
```

Si el resultado es `Enforcing` y estás sirviendo el dashboard desde `/opt/digna/dashboard`, etiqueta el directorio para que el servidor web pueda leerlo:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Nota"

    Si `semanage` no se encuentra, instálalo con `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Importante"

    Un dashboard que devuelve **403 Forbidden** en un servidor RHEL recién configurado suele deberse casi siempre a un problema de etiquetado SELinux más que a los permisos de archivos. Confírmalo con `sudo ausearch -m avc -ts recent`.

---

## Ejecutar digna como servicio systemd {: #running-digna-as-a-systemd-service }

### ¿Por qué ejecutar digna como servicio?

Ejecutar el backend de digna como servicio systemd asegura que:

- Arranque automáticamente cuando la máquina lo haga
- Se ejecute en segundo plano sin una ventana de terminal abierta
- Se reinicie automáticamente si falla
- Puede gestionarse mediante `systemctl`, el gestor de servicios estándar de Linux

### Archivos de gestión del servicio

Todos los archivos necesarios se encuentran en el directorio de instalación de digna bajo: `bin/`

Los siguientes scripts shell están disponibles:

- `install_service.sh` — Registra digna en systemd
- `uninstall_service.sh` — Desregistra el servicio
- `start_service.sh` — Inicia el servicio registrado
- `stop_service.sh` — Detiene el servicio en ejecución

!!! warning "Se requieren privilegios de root"

    Todos los scripts deben ejecutarse con `sudo`, porque registrar un servicio que arranca al inicio escribe un unit file en `/etc/systemd/system`.

### Hacer los scripts ejecutables

La extracción puede no preservar el bit de ejecutable. Antes del primer uso:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Instalar el servicio

1. **Abre un terminal**

2. **Navega a la carpeta bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Ejecuta el script de instalación**
   ```bash
   sudo ./install_service.sh
   ```

El servidor digna ahora está registrado en systemd con el arranque automático habilitado. El servicio no se inicia de forma inmediata — consulta la sección siguiente para iniciarlo.

### Iniciar y detener el servicio

#### Para iniciar el servicio

1. Abre un terminal
2. Navega a `/opt/digna/bin`
3. Ejecuta:
   ```bash
   sudo ./start_service.sh
   ```

#### Para detener el servicio

1. Abre un terminal
2. Navega a `/opt/digna/bin`
3. Ejecuta:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Consejo"

    Siempre detén el servicio antes de actualizar los archivos de la aplicación.

### Gestionar el servicio con systemctl

Una vez registrado, el servicio también puede controlarse con los comandos systemd estándar desde cualquier directorio:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Verificar el servicio

Para confirmar que el servicio está registrado y en ejecución:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` significa que el servicio arranca en el inicio; `active` significa que se está ejecutando ahora.

### Ver los registros del servicio

systemd captura todo lo que el backend escribe en la consola. Para leerlo:

```bash
sudo journalctl -u digna -n 100
```

Para seguir el registro en vivo mientras reproduces un problema:

```bash
sudo journalctl -u digna -f
```

!!! tip "Consejo"

    Esta es la forma más rápida de diagnosticar un servicio que arranca y se detiene inmediatamente. Un fallo de conexión al repositorio o la falta de `license.toml` se informan aquí.

### Mover el servicio a un nuevo directorio

El unit file almacena la ruta absoluta al ejecutable, por lo que mover la instalación requiere volver a registrar el servicio:

1. **Desinstalar el servicio actual**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Mover los archivos de la aplicación**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Reinstalar el servicio**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Iniciar el servicio**
   ```bash
   sudo ./start_service.sh
   ```

### Desinstalar el servicio

1. **Detener el servicio en ejecución**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Desinstalar el servicio**
   ```bash
   sudo ./uninstall_service.sh
   ```

El servidor digna ahora está desregistrado de systemd.

---

## Actualización a una nueva versión {: #upgrading-to-a-new-release }

### Antes de actualizar

**Es obligatorio crear una copia de seguridad del repositorio digna**

Antes de actualizar digna, haz una copia de seguridad de tu repositorio (PostgreSQL) para protegerte contra pérdidas de datos.
Una copia de seguridad garantiza que puedas recuperar los datos si la actualización encuentra problemas inesperados.

Para crear una copia de seguridad desde la shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Proceso de actualización

#### Paso 1: Detener el servicio digna

Si digna se ejecuta como servicio systemd, deténlo primero:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Si digna se está ejecutando en primer plano, presiona `Ctrl + C` en su ventana de terminal.

#### Paso 2: Hacer una copia de seguridad de la instalación del backend actual

En tu directorio de instalación de digna:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Paso 3: Extraer y desplegar la nueva versión

1. Extrae el nuevo archivo ZIP de instalación de digna
2. Copia el nuevo ejecutable `digna` y la carpeta `dashboard` a tu directorio de instalación
3. Restaura el bit de ejecutable y la propiedad a la cuenta de servicio:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Importante"

    El archivo `config.toml` **nunca** se incluye en el ZIP de instalación. Tu configuración existente permanece a salvo.

### Paso 4: Restaurar tus archivos de configuración

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Paso 5: Actualizar el esquema del repositorio

Navega hasta tu directorio de instalación de digna y ejecuta:

```bash
cd /opt/digna
./digna repo upgrade
```

Esto actualiza el esquema de PostgreSQL a la versión más reciente preservando todos los datos existentes.

### Paso 6: Reiniciar los servicios

Si se ejecuta como servicio systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Si se ejecuta manualmente, reinicia el servidor:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Si usas nginx o Apache, recarga el servidor web correspondiente:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

En la familia RHEL, vuelve a aplicar el etiquetado SELinux si se sustituyó el directorio `dashboard`:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Paso 7: Verificar la actualización

1. Accede al dashboard de digna
2. Verifica que la interfaz cargue correctamente
3. Revisa los registros del servidor por si hay errores:

```bash
sudo journalctl -u digna -n 100
```
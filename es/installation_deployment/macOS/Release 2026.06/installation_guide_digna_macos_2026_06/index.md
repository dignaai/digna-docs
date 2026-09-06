# Guía de instalación en macOS para digna Release 2026.06

**Release:** 2026.06

**Última actualización:** 5 de septiembre de 2026


---

## Tabla de contenidos

1. [Introducción](#introduction)
2. [Requisitos del sistema](#system-requirements)
3. [Preparación previa a la instalación](#pre-installation-setup)
4. [Configuración del servidor PostgreSQL](#postgresql-server-setup)
5. [Configuración del servidor web](#web-server-configuration)
6. [Instalación inicial](#initial-installation)
7. [Configuración del backend](#backend-configuration)
8. [Configuración del dashboard](#dashboard-configuration)
9. [Ejecutar digna como servicio en segundo plano](#running-digna-as-a-background-service)
10. [Actualizar a una nueva versión](#upgrading-to-a-new-release)

---

## Introducción {: #introduction }

### Acerca de digna

digna es una plataforma completa impulsada por IA diseñada para optimizar la gestión de la calidad de los datos en diversos entornos de datos, como warehouses, lakes y lakehouses. Diseñada para ser altamente escalable y adaptable, digna aborda los desafíos modernos de datos mediante automatización, monitorización en tiempo real y detección de anomalías.

digna consta de dos componentes principales:

- **dignabackend**: El motor principal de la aplicación, responsable de procesar datos y realizar comprobaciones de calidad.
- **dignadashboard**: Una interfaz web alojada en un servidor web, que proporciona una forma amigable de interactuar con la plataforma digna y visualizar métricas de calidad de datos.

### Novedades en la Release 2026.06

Esta versión incorpora capacidades de observabilidad de datos directamente en tu código, permitiendo a los desarrolladores monitorear la calidad de los datos en su origen. Consulta las [notas de la versión](http://docs.digna.ai/changelog/Release_202606/) para más detalles.

### ¿Buscas Windows o Linux?

Esta guía cubre macOS. Para otras plataformas, consulta la [Guía de instalación para Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) o la [Guía de instalación para Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Requisitos del sistema {: #system-requirements }

Antes de comenzar la instalación, asegúrate de que tu sistema cumple los siguientes requisitos mínimos:

| Requisito | Especificación |
|---|---|
| **Sistema operativo** | macOS 13 (Ventura) o posterior |
| **Arquitectura** | Apple Silicon (arm64) o Intel (x86_64) |
| **Memoria (Configuración mínima)** | 16 GB RAM |
| **Espacio en disco** | 10 GB de almacenamiento disponible |
| **Base de datos** | PostgreSQL Server 12 o superior |
| **Servidor web** | nginx, Apache httpd u equivalente |
| **Herramientas de línea de comandos** | Xcode Command Line Tools (requerido por Homebrew) |

### Opciones de instalación de la base de datos

**Si PostgreSQL ya está instalado:**
Puedes añadir una nueva base de datos para digna en tu servidor PostgreSQL existente.

**Si vas a instalar PostgreSQL en la misma máquina que digna:**

!!! info "Especificaciones recomendadas"

    - **Memoria**: 32 GB RAM (en lugar de 16 GB)
    - **Espacio en disco**: 50 GB de almacenamiento disponible (en lugar de 10 GB)

    Estas especificaciones más altas acomodan tanto digna como la base de datos PostgreSQL ejecutándose simultáneamente.

### Verificar tu arquitectura

Varios caminos en esta guía difieren entre Macs con Apple Silicon e Intel. Para comprobar cuál tienes, abre **Terminal** y ejecuta:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew se instala en `/opt/homebrew`.
- `x86_64` — Intel. Homebrew se instala en `/usr/local`.

!!! tip "Consejo"

    En lugar de codificar una u otra ruta, esta guía usa `$(brew --prefix)`, que se expande a la ubicación correcta en ambas arquitecturas. Puedes copiar los comandos tal cual.

---

## Preparación previa a la instalación {: #pre-installation-setup }

Antes de instalar digna, asegúrate de que tres prerrequisitos clave estén presentes:

1. **Homebrew** – el gestor de paquetes usado para instalar los componentes que siguen
2. **PostgreSQL Server** – para almacenar métricas calculadas y datos de rendimiento
3. **Servidor web** – para alojar el Dashboard de digna

Si estos componentes aún no están configurados, sigue las secciones a continuación para instalarlos y configurarlos.

### Instalación de Homebrew

Homebrew es el gestor de paquetes estándar para macOS y se usa en toda esta guía para instalar PostgreSQL y nginx.

#### Paso 1: Comprobar si Homebrew ya está instalado

Abre **Terminal** (pulsa `Cmd + Space`, escribe `Terminal`, pulsa Enter) y ejecuta:

```bash
brew --version
```

Si se devuelve un número de versión, continúa con la sección de [Configuración del servidor PostgreSQL](#postgresql-server-setup).

#### Paso 2: Instalar Homebrew

Si el comando no se encontró, instala Homebrew siguiendo las instrucciones en el [sitio oficial de Homebrew](https://brew.sh). El instalador también instala las Xcode Command Line Tools si no están ya presentes.

#### Paso 3: Añadir Homebrew a tu PATH

En Apple Silicon, el instalador muestra dos comandos para añadir Homebrew a tu entorno de shell. Ejecútalos según se indique y luego confirma:

```bash
brew --prefix
```

Esto debería imprimir `/opt/homebrew` en Apple Silicon o `/usr/local` en Intel.

---

## Configuración del servidor PostgreSQL {: #postgresql-server-setup }

### Si ya tienes PostgreSQL

Si PostgreSQL ya está instalado y en ejecución en tu máquina local o si estás usando un servidor PostgreSQL remoto gestionado, puedes saltar a la [siguiente sección](#web-server-configuration).

### Opciones de instalación

macOS ofrece dos maneras sencillas de instalar PostgreSQL. Elige **una**:

- [Homebrew](#postgresql-homebrew) — instalación desde la línea de comandos, recomendada para despliegues de servidor
- [Postgres.app](#postgresql-app) — instalación gráfica, conveniente para evaluación local

### Instalar PostgreSQL con Homebrew {: #postgresql-homebrew }

#### Paso 1: Instalar la fórmula de PostgreSQL

```bash
brew install postgresql@16
```

#### Paso 2: Añadir PostgreSQL a tu PATH

Las fórmulas versionadas de PostgreSQL son *keg-only*, lo que significa que Homebrew no enlaza sus comandos en tu PATH automáticamente. Añádelos tú mismo:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Nota"

    Esto asume el shell `zsh` por defecto que usa macOS. Si usas `bash`, añade la misma línea a `~/.bash_profile` en su lugar.

#### Paso 3: Iniciar el servicio PostgreSQL

```bash
brew services start postgresql@16
```

Esto inicia PostgreSQL inmediatamente y lo configura para que se inicie automáticamente cuando inicies sesión.

#### Paso 4: Verificar la instalación

```bash
psql --version
```

Deberías ver la versión de PostgreSQL si la instalación fue exitosa.

#### Paso 5: Conectarse al servidor

```bash
psql postgres
```

!!! warning "Importante — macOS difiere de Windows aquí"

    El instalador de Windows te pide crear un superusuario `postgres` y una contraseña. Homebrew no lo hace. En su lugar, crea un superusuario con el mismo nombre que tu **cuenta de macOS**, sin contraseña, accesible solo desde la máquina local.

    Esto significa que no existe el rol `postgres` en una instalación nueva con Homebrew. Usa tu propio nombre de cuenta cuando necesites un superusuario, y crea un usuario explícito para digna como se describe en [Instalación inicial](#initial-installation).

#### Paso 6: Confirmar el puerto

El puerto por defecto de PostgreSQL es `5432`. Para confirmar el puerto en el que escucha tu servidor:

```bash
psql postgres -c "SHOW port;"
```

Anota el valor — lo necesitarás cuando configures el backend de digna.

### Instalar PostgreSQL con Postgres.app {: #postgresql-app }

Si prefieres una instalación gráfica:

1. Descarga [Postgres.app](https://postgresapp.com) y arrástralo a tu carpeta **Applications**
2. Abre la app y haz clic en **Initialize** para crear un nuevo servidor
3. Sigue las instrucciones de la app para añadir sus herramientas de línea de comandos a tu PATH
4. Verifica la instalación:

```bash
psql --version
```

Postgres.app también crea un superusuario con el mismo nombre que tu cuenta de macOS.

---

## Configuración del servidor web {: #web-server-configuration }

digna requiere un servidor web para alojar el dashboard. Elige una de las siguientes opciones:

- [nginx](#nginx-setup) — instalado vía Homebrew, recomendado
- [Apache httpd](#apache-setup) — incluido con macOS

Solo necesitas instalar y configurar **uno** de estos servidores.

Ambas secciones configuran dos cosas de las que depende el dashboard:

- **Un fallback para aplicaciones de una sola página**, de modo que al actualizar una URL del dashboard no devuelva 404
- **Un tipo MIME para `.md`**, para que los archivos Markdown se sirvan correctamente

### Configuración de nginx {: #nginx-setup }

#### Resumen

nginx es un servidor web ligero y de alto rendimiento, bien adaptado para servir el dashboard estático de digna.

#### Instalación

```bash
brew install nginx
```

#### Iniciar nginx

```bash
brew services start nginx
```

#### Verificar la instalación

1. Abre tu navegador
2. Navega a `http://localhost:8080`
3. Deberías ver la página de bienvenida de nginx

!!! note "Nota — el puerto por defecto es 8080, no 80"

    Homebrew configura nginx para escuchar en el puerto `8080` para que pueda ejecutarse sin privilegios de administrador. En macOS, enlazar al puerto `80` o a cualquier puerto por debajo de 1024 requiere root.

    Para servir el dashboard en el puerto 80, cambia `listen 8080;` por `listen 80;` en la configuración que sigue y arranca nginx con `sudo brew services start nginx` en su lugar.

#### Configurar un sitio para el dashboard

La configuración de nginx de Homebrew incluye todos los archivos en su directorio `servers`. Crea un archivo de configuración dedicado para digna ahí:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Pega lo siguiente, reemplazando `/path/to/digna/dashboard` por la ruta real a tu carpeta `dashboard` extraída:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Servir archivos Markdown con el tipo MIME correcto.
    types {
        text/markdown  md;
    }

    # Fallback para aplicación de una sola página: las rutas desconocidas devuelven index.html
    # en lugar de un 404, de modo que las rutas del dashboard sobrevivan a una actualización del navegador.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Importante"

    Sin la directiva `try_files`, recargar cualquier página del dashboard que no sea la URL raíz devuelve un 404. Esto es el equivalente en nginx del módulo URL Rewrite requerido por IIS en Windows.

#### Aplicar la configuración

Prueba la sintaxis de la configuración y luego recarga nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Configuración de Apache httpd {: #apache-setup }

#### Resumen

macOS incluye Apache httpd, por lo que no es necesario instalarlo. Está deshabilitado por defecto.

#### Iniciar Apache

```bash
sudo apachectl start
```

#### Verificar la instalación

1. Abre tu navegador
2. Navega a `http://localhost`
3. Deberías ver el mensaje "It works!"

#### Obligatorio: habilitar mod_rewrite

El dashboard requiere reescritura de URL. Abre la configuración de Apache:

```bash
sudo nano /etc/apache2/httpd.conf
```

Encuentra la siguiente línea y elimina el `#` inicial para descomentarlo:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Obligatorio: permitir overrides con .htaccess

En el mismo archivo, localiza el bloque `<Directory "/Library/WebServer/Documents">` y cambia:

```apache
AllowOverride None
```

por:

```apache
AllowOverride All
```

#### Obligatorio: tipo MIME para archivos Markdown

Aún en `httpd.conf`, añade la siguiente línea para que los archivos Markdown se sirvan correctamente:

```apache
AddType text/markdown .md
```

!!! warning "Importante"

    Sin esta configuración, los archivos `.md` podrían no servirse correctamente.

#### Aplicar la configuración

Comprueba la sintaxis de la configuración y luego reinicia Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Instalación inicial {: #initial-installation }

### Paso 1: Configurar el repositorio de digna

El repositorio de digna almacena todas las métricas calculadas por digna. Actúa como la base de datos central para datos analíticos y de rendimiento.

#### Crear esquema y usuario del repositorio

Abre tu cliente PostgreSQL (psql, pgAdmin u otro) y ejecuta las siguientes sentencias SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Reemplaza los siguientes marcadores:**

- `<digna_repo_schema>` — El nombre de esquema que desees (por ejemplo, `dignarepo`)
- `<digna_repo_user>` — El nombre de usuario que desees (por ejemplo, `digna_user`)
- `<digna_repo_password>` — Una contraseña segura para este usuario

**Ejemplo:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Para ejecutar esto desde Terminal en un solo paso:

```bash
psql postgres
```

Luego pega las sentencias en el prompt `postgres=#` y escribe `\q` para salir.

!!! tip "Buena práctica"

    Usa contraseñas fuertes y complejas para los usuarios de la base de datos. Evita credenciales fácilmente adivinables.

---

### Paso 2: Extraer el paquete de instalación de digna

1. Localiza el archivo ZIP de instalación de digna proporcionado
2. Extráelo en la ubicación de instalación deseada — por ejemplo `/opt/digna` o `~/digna`
3. Tras la extracción, deberías ver los siguientes elementos:
   - `dashboard/` — Interfaz web del dashboard
   - `digna` — Ejecutable principal (backend + CLI combinados)
   - `config.toml` — Archivo de configuración
   - `license.toml` — Archivo de licencia (copia el tuyo aquí)

Para extraer desde Terminal:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Hacer el ejecutable ejecutable

Dependiendo de cómo se transfirió el archivo, el bit de ejecutable puede no conservarse tras la extracción. Establécelo explícitamente:

```bash
cd /opt/digna
chmod +x digna
```

#### Si macOS bloquea la aplicación

Los archivos descargados mediante un navegador o cliente de correo se marcan con un atributo de cuarentena. Si macOS informa que la app *"cannot be opened because the developer cannot be verified"*, quita el atributo de cuarentena del directorio de instalación:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativamente, abre **System Settings → Privacy & Security**, encuentra el elemento bloqueado cerca del final de la página y haz clic en **Open Anyway**.

!!! note "Nota"

    Este paso solo es necesario si macOS realmente bloquea el ejecutable. Los paquetes transferidos por SSH o desde recursos compartidos internos no suelen estar en cuarentena.

### Paso 3: Instalar el archivo de licencia

!!! warning "Importante"

    El archivo de licencia **no** está incluido en el paquete de instalación y te será proporcionado por digna por separado.

1. Localiza el archivo `license.toml` que se te proporcionó
2. Copia este archivo al directorio raíz de instalación de digna (donde están `config.toml` y el ejecutable `digna`)

**Por qué importa:**
El archivo de licencia contiene la información de cliente, la fecha de expiración de la licencia y la firma digital. **No modifiques este archivo** — cualquier cambio lo invalidará.

**Estructura de directorios después de la configuración:**

```
/opt/digna/
├── config.toml         (archivo de configuración)
├── license.toml        (TU ARCHIVO DE LICENCIA - cópialo aquí)
├── digna               (ejecutable principal)
├── bin/                (scripts para gestión del servicio)
└── dashboard/          (interfaz web)
    └── (archivos del dashboard)
```

---

## Configuración del backend {: #backend-configuration }

### Paso 1: Crear y editar el archivo de configuración

El archivo `config_template.toml` se proporciona en el directorio de instalación de digna. Solo necesitas renombrarlo a `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Ubicación:** `/opt/digna/config.toml`

Abre `config.toml` en un editor de texto y configura cada sección a continuación.

#### Sección [app]

Esta sección configura los ajustes de la aplicación backend de digna:

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
| `digna_APP_CORS_ALLOW_ORIGINS` | URL del frontend | Si el dashboard está en otro servidor, incluye su URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Requerido para CORS con credenciales |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Permite todos los métodos HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Permite todos los encabezados |

!!! note "Nota"

    Si sirves el dashboard desde nginx de Homebrew en su puerto por defecto, el origin a permitir es `http://localhost:8080`.

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
| `digna_REPO_PASSWORD` | Tu contraseña | Contraseña establecida durante la creación del esquema |

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
| `digna_FERNET_KEY` | Clave de cifrado | Usada para cifrar tokens y cookies (se proporciona por defecto) |
| `digna_COOKIE_DOMAIN` | `localhost` | Debe coincidir con el dominio de tu frontend |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (producción) | Usa `true` para conexiones HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Siempre habilitado por seguridad |
| `digna_COOKIE_SAME_SITE` | `lax` | Previene ataques CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 horas) | Tiempo de expiración de sesión en segundos |
| `digna_MAX_WORKERS` | Número de núcleos CPU - 1 | Número de tareas de inspección paralelas |

!!! tip "Consejo"

    Para encontrar el número de núcleos CPU disponibles en tu Mac, ejecuta `sysctl -n hw.ncpu`.

#### Sección [logging]

Esta sección configura el comportamiento del registro (logging):

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parámetro | Valor | Notas |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` para producción, `DEBUG` para solución de problemas |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Número de copias de seguridad diarias de logs a retener |

---

### Paso 2: Inicializar el repositorio

1. Abre **Terminal**
2. Navega al directorio de instalación de digna (donde están `config.toml` y el ejecutable `digna`)
3. Ejecuta la prueba de conexión:

```bash
cd /opt/digna
./digna repo check
```

Deberías ver una confirmación de que la conexión está establecida (el repositorio en sí aún no ha sido inicializado).

!!! note "Nota"

    En macOS, los comandos en el directorio actual no están en tu PATH, así que el ejecutable se invoca como `./digna` en lugar de `digna`. Para usar la forma corta en todo momento, añade el directorio de instalación a tu PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
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

Deberías ver mensajes de inicio confirmando que el servidor está en ejecución:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Consejo"

    La primera vez que inicies el servidor, macOS puede preguntar si deseas que la aplicación acepte conexiones de red entrantes. Haz clic en **Allow**, de lo contrario el dashboard no podrá comunicarse con el backend.

### Paso 5: Crear un usuario administrador

1. Abre una ventana de Terminal **nueva**
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

    Envuelve la contraseña entre comillas simples. `zsh` trata caracteres como `!`, `$` y `*` de forma especial, y una contraseña sin comillas que los contenga no se pasará tal como se escribió.

!!! tip "Buena práctica"

    Usa una contraseña fuerte con una mezcla de mayúsculas, minúsculas, números y caracteres especiales.

---

## Configuración del dashboard {: #dashboard-configuration }

### Paso 1: Desplegar el dashboard en el servidor web

El dashboard de digna tiene su propio archivo `config.toml` ubicado en el directorio `dashboard/`. Esta configuración ya se proporciona y no requiere cambios durante la instalación inicial. Solo necesitas modificarla si quieres personalizar la conexión al backend.

Si necesitas ajustar la configuración del dashboard (por ejemplo, para despliegues multi-instancia), consulta la documentación del dashboard.

Elige tu servidor web y sigue los pasos de despliegue correspondientes.

#### Desplegar en nginx

Si seguiste la sección de [Configuración de nginx](#nginx-setup), el bloque del servidor ya apunta a tu carpeta `dashboard` y no es necesario copiar nada.

1. **Confirmar la ruta**
   - Abre `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Verifica que `root` apunte a tu carpeta `dashboard` extraída

2. **Asegurarse de que la carpeta sea legible**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Recargar nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Probar la instalación**
   - Abre tu navegador
   - Navega a `http://localhost:8080` (o a la URL configurada)
   - Deberías ver la página de inicio de sesión del dashboard de digna

#### Desplegar en Apache httpd

1. **Copiar el dashboard al Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Añadir las reglas de reescritura**

   Crea un archivo `.htaccess` dentro de la carpeta desplegada para que las rutas del dashboard sobrevivan a una actualización del navegador:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Pega lo siguiente:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Servir archivos y directorios existentes tal cual.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Todo lo demás vuelve al punto de entrada de la aplicación de una sola página.
   RewriteRule ^ index.html [L]
   ```

3. **Reiniciar Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Acceder al dashboard**
   - Abre tu navegador
   - Navega a `http://localhost/digna`
   - Deberías ver la página de inicio de sesión del dashboard de digna

---

## Ejecutar digna como servicio en segundo plano {: #running-digna-as-a-background-service }

### ¿Por qué ejecutar digna como servicio?

Ejecutar el backend de digna como un servicio en segundo plano garantiza que:

- Se inicie automáticamente cuando la máquina arranque
- Se ejecute en segundo plano sin una ventana de Terminal abierta
- Se reinicie automáticamente si falla
- Puede gestionarse mediante `launchctl`, el gestor de servicios de macOS

### Archivos de gestión del servicio

Todos los archivos necesarios se encuentran en el directorio de instalación de digna bajo: `bin/`

Los siguientes scripts shell están disponibles:

- `install_service.sh` — Registra digna con launchd
- `uninstall_service.sh` — Desregistra el servicio
- `start_service.sh` — Inicia el servicio registrado
- `stop_service.sh` — Detiene el servicio en ejecución

!!! warning "Se requiere administrador"

    Todos los scripts deben ejecutarse con `sudo`, porque registrar un servicio que se inicia en el arranque escribe en `/Library/LaunchDaemons`.

### Hacer los scripts ejecutables

La extracción puede no preservar el bit ejecutable. Antes del primer uso:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Instalar el servicio

1. **Abrir Terminal**

2. **Navegar a la carpeta bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Ejecutar el script de instalación**
   ```bash
   sudo ./install_service.sh
   ```

El servidor digna ahora está registrado en launchd con el inicio automático habilitado. El servicio no se inicia inmediatamente — consulta la sección siguiente para iniciarlo.

### Iniciar y detener el servicio

#### Para iniciar el servicio

1. Abre Terminal
2. Navega a `/opt/digna/bin`
3. Ejecuta:
   ```bash
   sudo ./start_service.sh
   ```

#### Para detener el servicio

1. Abre Terminal
2. Navega a `/opt/digna/bin`
3. Ejecuta:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Consejo"

    Siempre detén el servicio antes de actualizar archivos de la aplicación.

### Verificar el servicio

Para confirmar que el servicio está registrado y en ejecución:

```bash
sudo launchctl list | grep digna
```

Una línea que comience con un ID de proceso indica que el servicio está en ejecución. Un `-` en la primera columna significa que está registrado pero detenido.

### Mover el servicio a un nuevo directorio

launchd almacena la ruta absoluta al ejecutable, por lo que mover la instalación requiere volver a registrar el servicio:

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

El servidor digna ya no estará registrado en launchd.

---

## Actualizar a una nueva versión {: #upgrading-to-a-new-release }

### Antes de actualizar

**Es obligatorio crear una copia de seguridad del repositorio de digna**

Antes de actualizar digna, realiza una copia de seguridad de tu repositorio (PostgreSQL) para protegerte contra pérdida de datos.
Una copia de seguridad asegura que puedas recuperar los datos si la actualización encuentra problemas inesperados.

Para crear una copia de seguridad desde Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Proceso de actualización

#### Paso 1: Detener el servicio digna

Si digna se está ejecutando como servicio en segundo plano, deténlo primero:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Si digna se ejecuta en primer plano, presiona `Ctrl + C` en la ventana de Terminal donde se esté ejecutando.

#### Paso 2: Hacer copia de seguridad del backend actual

En tu directorio de instalación de digna:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Paso 3: Extraer y desplegar la nueva versión

1. Extrae el nuevo archivo ZIP de instalación de digna
2. Copia el nuevo ejecutable `digna` y la carpeta `dashboard` a tu directorio de instalación
3. Restaura el bit de ejecutable y, si es necesario, quita el atributo de cuarentena:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Importante"

    El archivo `config.toml` **nunca** está incluido en el ZIP de instalación. Tu configuración existente permanece segura.

### Paso 4: Restaurar tus archivos de configuración

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Paso 5: Actualizar el esquema del repositorio

Navega a tu directorio de instalación de digna y ejecuta:

```bash
cd /opt/digna
./digna repo upgrade
```

Esto actualiza el esquema de PostgreSQL a la versión más reciente preservando todos los datos existentes.

### Paso 6: Reiniciar servicios

Si se ejecuta como servicio en segundo plano:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Si se ejecuta manualmente, reinicia el servidor:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Si usas nginx o Apache, reinicia el servidor web correspondiente:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Paso 7: Verificar la actualización

1. Accede al dashboard de digna
2. Verifica que la interfaz cargue correctamente
3. Revisa los logs del servidor en busca de errores
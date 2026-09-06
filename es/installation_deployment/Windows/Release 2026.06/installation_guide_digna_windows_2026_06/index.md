# Guía de instalación en Windows para digna Release 2026.06

**Release:** 2026.06

**Última actualización:** 30 de agosto de 2026


---

## Tabla de contenidos

1. [Introducción](#introduction)
2. [Requisitos del sistema](#system-requirements)
3. [Preparativos previos a la instalación](#pre-installation-setup)
4. [Configuración del servidor PostgreSQL](#postgresql-server-setup)
5. [Configuración del servidor web](#web-server-configuration)
6. [Instalación inicial](#initial-installation)
7. [Configuración del backend](#backend-configuration)
8. [Configuración del panel (dashboard)](#dashboard-configuration)
9. [Ejecutar digna como servicio de Windows](#running-digna-as-a-windows-service)
10. [Actualizar a una nueva versión](#upgrading-to-a-new-release)

---

## Introducción {: #introduction }

### Acerca de digna

digna es una plataforma integral impulsada por IA diseñada para optimizar la gestión de la calidad de los datos en diversos entornos, como data warehouses, data lakes y lakehouses. Diseñada para ser altamente escalable y adaptable, digna aborda los desafíos modernos de datos mediante automatización, monitoreo en tiempo real y detección de anomalías.

digna consta de dos componentes principales:

- **dignabackend**: El motor central de la aplicación, responsable de procesar datos y realizar comprobaciones de calidad.
- **dignadashboard**: Una interfaz web alojada en un servidor web, que ofrece una forma amigable de interactuar con la plataforma digna y visualizar las métricas de calidad de datos.

### Novedades en la Release 2026.06

Esta versión incorpora capacidades de observabilidad de datos directamente en tu código, permitiendo a los desarrolladores supervisar la calidad de los datos en el origen. Consulta las [notas de la versión](http://docs.digna.ai/changelog/Release_202606/) para obtener detalles completos.

### ¿Buscas macOS o Linux?

Esta guía cubre Windows. Para otras plataformas, consulta la [Guía de instalación para macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) o la [Guía de instalación para Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Requisitos del sistema {: #system-requirements }

Antes de comenzar la instalación, asegúrate de que tu sistema cumpla con los siguientes requisitos mínimos:

| Requisito | Especificación |
|---|---|
| **Sistema operativo** | Windows Server o Windows 10/11 |
| **Memoria (instalación mínima)** | 16 GB RAM |
| **Espacio en disco** | 10 GB de almacenamiento disponible |
| **Base de datos** | PostgreSQL Server 12 o superior |
| **Servidor web** | IIS, Apache Tomcat, o equivalente |

### Opciones de instalación de la base de datos

**Si PostgreSQL ya está instalado:**
Puedes añadir una nueva base de datos para digna en tu servidor PostgreSQL existente.

**Si vas a instalar PostgreSQL en la misma máquina que digna:**

!!! info "Especificaciones recomendadas"

    - **Memoria**: 32 GB RAM (en lugar de 16 GB)
    - **Espacio en disco**: 50 GB de almacenamiento disponible (en lugar de 10 GB)

    Estas especificaciones superiores acomodan tanto digna como la base de datos PostgreSQL ejecutándose simultáneamente.

---

## Preparativos previos a la instalación {: #pre-installation-setup }

Antes de instalar digna, asegúrate de que dos prerrequisitos clave estén en su lugar:

1. **Servidor PostgreSQL** – para almacenar métricas calculadas y datos de rendimiento
2. **Servidor web** – para alojar el digna Dashboard

Si estos componentes aún no están configurados, sigue las secciones siguientes para instalarlos y configurarlos.

---

## Configuración del servidor PostgreSQL {: #postgresql-server-setup }

### Si ya tienes PostgreSQL

Si PostgreSQL ya está instalado y en funcionamiento en tu máquina local o si estás utilizando un servidor PostgreSQL gestionado de forma remota, puedes saltar a la [siguiente sección](#web-server-configuration).

### Instalación de PostgreSQL

Sigue estos pasos para instalar PostgreSQL en Windows:

#### Paso 1: Descargar PostgreSQL

1. Visita la [página de descargas de PostgreSQL](https://www.postgresql.org/download/)
2. Selecciona **Windows**
3. Descarga el instalador más reciente

#### Paso 2: Ejecutar el instalador

1. Haz doble clic en el archivo del instalador descargado
2. Sigue las indicaciones del asistente de instalación

#### Paso 3: Elegir el directorio de instalación

Selecciona el directorio donde se instalará PostgreSQL. La ubicación predeterminada suele ser adecuada.

#### Paso 4: Seleccionar componentes

Para una configuración estándar, mantiene las opciones de componentes predeterminadas seleccionadas.

#### Paso 5: Establecer la contraseña del superusuario de PostgreSQL

Introduce y confirma una contraseña para el superusuario de PostgreSQL (`postgres`). **Guarda esta contraseña de forma segura** — la necesitarás más adelante.

#### Paso 6: Configurar el número de puerto

El puerto predeterminado de PostgreSQL es `5432`. Puedes usar el predeterminado o especificar otro puerto si es necesario.

!!! tip "Consejo"

    Si el puerto 5432 ya está en uso, elige un puerto alternativo y anótalo para la configuración posterior.

#### Paso 7: Elegir la configuración regional (locale)

Selecciona la configuración regional para tu base de datos. La opción predeterminada suele ser adecuada para la mayoría de las instalaciones.

#### Paso 8: Completar la instalación

Haz clic en **Next** en los pasos restantes y luego en **Finish**.

#### Paso 9: Verificar la instalación

Abre el Símbolo del sistema y verifica que PostgreSQL esté instalado:

```bash
psql --version
```

Deberías ver la versión de PostgreSQL si la instalación fue exitosa.

---

## Configuración del servidor web {: #web-server-configuration }

digna requiere un servidor web para alojar el dashboard. Elige una de las siguientes opciones:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Solo necesitas instalar y configurar **uno** de estos servidores.

### Configuración de IIS {: #iis-setup }

#### Descripción general

Internet Information Services (IIS) es el servidor web de Microsoft para alojar sitios web y aplicaciones web.

#### Habilitar IIS

1. **Abrir el Panel de control**
   - Presiona `Win + R`
   - Escribe `control` y presiona Enter

2. **Ir a Funciones de Windows**
   - Haz clic en **Programs**
   - Selecciona **Turn Windows features on or off**

3. **Habilitar Internet Information Services**
   - Desplázate y busca **Internet Information Services (IIS)**
   - Marca la casilla para habilitarlo
   - Haz clic en el **+** para expandir y verifica que estos subcomponentes estén seleccionados:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Haz clic en OK** para aplicar los cambios

5. **Verificar la instalación de IIS**
   - Abre tu navegador
   - Navega a `http://localhost`
   - Deberías ver la página de bienvenida de IIS

#### Requerido: módulo URL Rewrite

IIS requiere el componente URL Rewrite. Descárgalo e instálalo desde la [página oficial de Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Requerido: tipo MIME para archivos Markdown

Para asegurar que los archivos Markdown (`.md`) se sirvan correctamente en IIS:

1. Abre **IIS Manager** (presiona `Win + R`, escribe `inetmgr`, presiona Enter)
2. Navega a **Your Site > MIME Types**
3. Haz clic en **Add...**
4. Configura:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Importante"

    Sin esta configuración, los archivos `.md` podrían no servirse correctamente.

---

### Configuración de Apache Tomcat {: #apache-tomcat-setup }

#### Descripción general

Apache Tomcat es un contenedor de servlets Java y servidor web de código abierto.

#### Instalación

1. **Descargar Apache Tomcat**
   - Visita [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Descarga la distribución ZIP para Windows

2. **Extraer el archivo**
   - Extrae el archivo ZIP en un directorio de tu sistema
   - Ejemplo: `C:\Program Files\Apache Tomcat`

3. **Verificar que Tomcat esté en ejecución**
   - Abre tu navegador
   - Navega a `http://localhost:8080`
   - Deberías ver la página de bienvenida de Apache Tomcat

!!! tip "Consejo"

    Apache Tomcat normalmente se inicia automáticamente después de la instalación. Si no lo hace, navega a la carpeta `bin` y ejecuta `startup.bat`.

---

## Instalación inicial {: #initial-installation }

### Paso 1: Configurar el repositorio de digna

El repositorio de digna almacena todas las métricas calculadas por digna. Actúa como la base de datos central para datos analíticos y de rendimiento.

#### Crear esquema y usuario del repositorio

Abre tu cliente de PostgreSQL (pgAdmin, psql u otro) y ejecuta los siguientes comandos SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Reemplaza los siguientes marcadores:**

- `<digna_repo_schema>` — El nombre de esquema que desees (p. ej., `dignarepo`)
- `<digna_repo_user>` — El nombre de usuario que desees (p. ej., `digna_user`)
- `<digna_repo_password>` — Una contraseña segura para este usuario

**Ejemplo:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Mejor práctica"

    Usa contraseñas fuertes y complejas para los usuarios de la base de datos. Evita credenciales fáciles de adivinar.

---

### Paso 2: Extraer el paquete de instalación de digna

1. Localiza el archivo ZIP de instalación de digna que se te proporcionó
2. Extrae el archivo en la ubicación de instalación deseada
3. Después de extraer, deberías ver los siguientes elementos:
   - `dashboard/` — Interfaz web del panel
   - `digna` — Ejecutable principal (backend + CLI combinados)
   - `config.toml` — Archivo de configuración
   - `license.toml` — Archivo de licencia (copia el tuyo aquí)

### Paso 3: Instalar el archivo de licencia

!!! warning "Importante"

    El archivo de licencia **no** está incluido en el paquete de instalación y se entregará por separado por digna.

1. Localiza el archivo `license.toml` que se te proporcionó
2. Cópialo en el directorio raíz de instalación de digna (donde están `config.toml` y el ejecutable `digna`)

**Por qué esto importa:**
El archivo de licencia contiene la información del cliente, la fecha de expiración de la licencia y la firma digital. **No modifiques este archivo** — cualquier cambio lo invalidará.

**Estructura de directorios después de la configuración:**

```
digna_installation/
├── config.toml         (archivo de configuración)
├── license.toml        (TU ARCHIVO DE LICENCIA - cópialo aquí)
├── digna               (ejecutable principal)
└── dashboard/          (interfaz web)
    └── (archivos del dashboard)
```

---

## Configuración del backend {: #backend-configuration }

### Paso 1: Crear y editar el archivo de configuración

Se proporciona el archivo `config_template.toml` en tu directorio de instalación de digna. Solo necesitas renombrarlo a `config.toml`.

**Ubicación:** `digna_installation/config.toml`

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
| `digna_APP_PORT` | `8082` (predeterminado) | Puerto para los endpoints REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL del frontend | Si el dashboard está en otro servidor, incluye su URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Requerido para CORS con credenciales |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Permitir todos los métodos HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Permitir todos los encabezados |

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
| `digna_REPO_PORT` | `5432` (predeterminado) | Puerto de PostgreSQL |
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
| `digna_FERNET_KEY` | Clave de cifrado | Se utiliza para cifrar tokens y cookies (se proporciona una por defecto) |
| `digna_COOKIE_DOMAIN` | `localhost` | Debe coincidir con el dominio del frontend |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (producción) | Usa `true` para conexiones HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Siempre habilitado por seguridad |
| `digna_COOKIE_SAME_SITE` | `lax` | Previene ataques CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 horas) | Tiempo de expiración de sesión en segundos |
| `digna_MAX_WORKERS` | Número de núcleos de CPU - 1 | Número de tareas de inspección en paralelo |

#### Sección [logging]

Esta sección configura el comportamiento del registro (logging):

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parámetro | Valor | Notas |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` para producción, `DEBUG` para depuración |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Número de copias de seguridad diarias de logs a conservar |

---

### Paso 3: Inicializar el repositorio

1. Abre el Símbolo del sistema
2. Navega al directorio de instalación de digna (donde están `config.toml` y el ejecutable `digna`)
3. Ejecuta la prueba de conexión:

```bash
digna repo check
```

Deberías ver una confirmación de que la conexión se ha establecido (el repositorio en sí aún no se ha inicializado).

### Paso 4: Instalar el esquema del repositorio

En el mismo directorio, ejecuta:

```bash
digna repo install
```

Este comando instala las tablas y el esquema necesarios en tu base de datos PostgreSQL.

### Paso 5: Iniciar el servidor digna

En el directorio de instalación de digna, inicia el servidor con:

```bash
digna serve --address <host> --port <port>
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

### Paso 6: Crear un usuario administrador

1. Abre una ventana **nueva** del Símbolo del sistema
2. Navega al directorio de instalación de digna
3. Ejecuta el siguiente comando para crear un usuario administrador:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Ejemplo:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Esto crea un usuario con privilegios administrativos completos.

!!! tip "Mejor práctica"

    Usa una contraseña fuerte con mezcla de mayúsculas, minúsculas, números y caracteres especiales.

---

## Configuración del panel (dashboard) {: #dashboard-configuration }

### Paso 1: Desplegar el dashboard en el servidor web

El dashboard de digna tiene su propio archivo `config.toml` ubicado en el directorio `dashboard/`. Esta configuración ya se proporciona y no requiere cambios durante la configuración inicial. Solo necesitas modificarla si requieres personalizar la conexión al backend.

Si necesitas modificar la configuración del dashboard (p. ej., para despliegues multi-instancia), consulta la documentación del dashboard.

Elige tu servidor web y sigue los pasos de despliegue correspondientes.

#### Despliegue en IIS

1. **Abrir IIS Manager**
   - Presiona `Win + R`, escribe `inetmgr`, presiona Enter

2. **Crear un nuevo sitio web**
   - En el panel izquierdo, clic derecho en **Sites**
   - Selecciona **Add Website...**

3. **Configurar el sitio**
   - **Site Name**: Introduce un nombre (p. ej., "dignaDashboard")
   - **Physical Path**: Haz clic en Browse y selecciona tu carpeta `dashboard`
   - **Binding**: Configura la dirección IP y el puerto (puerto 80 para HTTP, 443 para HTTPS por defecto)

4. **Iniciar el sitio**
   - Haz clic en **OK** para crear el sitio
   - Clic derecho en el nuevo sitio y selecciona **Start**

5. **Probar la instalación**
   - Abre tu navegador
   - Navega a `http://localhost` (o a la URL configurada)
   - Deberías ver la página de inicio de sesión del dashboard de digna

#### Despliegue en Apache Tomcat

1. **Copiar el dashboard a Tomcat**
   - Copia la carpeta `dashboard` a tu directorio `webapps` de Tomcat
   - Renómbrala si es necesario (p. ej., a `digna`)
   - Ejemplo: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verificar el despliegue**
   - Actualiza o recarga la página de administración de Tomcat (http://localhost:8080)
   - Deberías ver "digna" (o el nombre elegido) listado en las aplicaciones desplegadas

3. **Acceder al dashboard**
   - Abre tu navegador
   - Navega a `http://localhost:8080/digna`
   - Deberías ver la página de inicio de sesión del dashboard de digna

---

## Ejecutar digna como servicio de Windows {: #running-digna-as-a-windows-service }

### ¿Por qué usar un servicio de Windows?

Ejecutar el backend de digna como servicio de Windows asegura que:
- Se inicie automáticamente al arrancar el servidor
- Se ejecute en segundo plano sin necesidad de una ventana del Símbolo del sistema abierta
- Se reinicie automáticamente si se bloquea
- Se pueda gestionar a través de Servicios de Windows

### Archivos de gestión del servicio

Todos los archivos necesarios están ubicados en el directorio de instalación de digna bajo: `bin/`

Los siguientes archivos batch están disponibles:
- `install_service.bat` — Registra digna como servicio de Windows
- `uninstall_service.bat` — Anula el registro del servicio
- `start_service.bat` — Inicia el servicio en ejecución
- `stop_service.bat` — Detiene el servicio en ejecución

!!! warning "Se requieren privilegios de Administrador"

    Todos los archivos batch deben ejecutarse con privilegios de Administrador.

### Instalar el servicio

1. **Abrir Símbolo del sistema como Administrador**
   - Clic derecho en Símbolo del sistema
   - Selecciona "Run as Administrator"

2. **Navegar a la carpeta bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Ejecutar el script de instalación**
   ```bash
   install_service.bat
   ```

El servidor digna ahora está registrado como un servicio de Windows con inicio **automático** habilitado. El servicio no se inicia inmediatamente — consulta la sección siguiente para iniciarlo.

### Iniciar y detener el servicio

#### Para iniciar el servicio

1. Abre el Símbolo del sistema como Administrador
2. Navega a `digna\bin`
3. Ejecuta:
   ```bash
   start_service.bat
   ```

#### Para detener el servicio

1. Abre el Símbolo del sistema como Administrador
2. Navega a `digna\bin`
3. Ejecuta:
   ```bash
   stop_service.bat
   ```

!!! tip "Consejo"

    Siempre detén el servicio antes de actualizar los archivos de la aplicación.

### Mover el servicio a un nuevo directorio

Si necesitas reubicar la instalación de digna:

1. **Desinstalar el servicio actual**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Mover los archivos de la aplicación**
   - Mueve toda la carpeta de instalación de digna a la nueva ubicación

3. **Reinstalar el servicio**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Iniciar el servicio**
   ```bash
   start_service.bat
   ```

### Desinstalar el servicio

1. **Detener el servicio en ejecución**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Desinstalar el servicio**
   ```bash
   uninstall_service.bat
   ```

El servidor digna ahora está dado de baja como servicio de Windows.

---

## Actualizar a una nueva versión {: #upgrading-to-a-new-release }

### Antes de actualizar

**Es obligatorio crear una copia de seguridad del repositorio de digna**

Antes de actualizar digna, realiza una copia de seguridad de tu repositorio (PostgreSQL) para protegerte contra pérdida de datos.
Una copia de seguridad asegura que puedas recuperar si la actualización encuentra problemas inesperados.

### Proceso de actualización

#### Paso 1: Detener el servicio digna

Si digna se está ejecutando como servicio de Windows, deténlo primero:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Paso 2: Hacer una copia de seguridad de la instalación actual del backend

En tu directorio de instalación de digna:

```bash
# Cambiar el nombre de la carpeta que contiene dignabackend
ren dignabackend dignabackend_old
```
```bash
# Cambiar el nombre del dashboard
ren dashboard dashboard_old
```

#### Paso 3: Extraer y desplegar la nueva versión

1. Extrae el nuevo archivo ZIP de instalación de digna
2. Copia el nuevo ejecutable `digna` y la carpeta `dashboard` a tu directorio de instalación


!!! warning "Importante"

    El archivo `config.toml` **nunca** se incluye en el ZIP de instalación. Tu configuración existente permanece segura.

### Paso 4: Restaurar tus archivos de configuración

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Paso 5: Actualizar el esquema del repositorio

Navega a tu directorio de instalación de digna y ejecuta:

```bash
digna repo upgrade
```

Esto actualiza el esquema de PostgreSQL a la versión más reciente preservando todos los datos existentes.

### Paso 6: Reiniciar los servicios

Si se ejecuta como servicio de Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Si se ejecuta manualmente, reinicia el servidor:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Si usas IIS o Tomcat, reinicia el servidor web correspondiente.

#### Paso 7: Verificar la actualización

1. Accede al dashboard de digna
2. Verifica que la interfaz se cargue correctamente
3. Revisa los registros del servidor en busca de errores
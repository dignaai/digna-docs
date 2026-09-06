# Referencia de la CLI de digna 2026.06
**2026-09-05**

Esta página documenta el conjunto completo de comandos disponibles en la versión **2026.06** de la CLI de ***digna***, incluidos ejemplos de uso y opciones.

El ejecutable se llama `digna`.

---

## Fundamentos de la CLI

---

### Descripción general y sintaxis

La CLI de la versión **2026.06** utiliza una jerarquía de comandos estructurada y basada en categorías:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` y `serve` son comandos únicos sin subcomando:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Opciones globales

Las siguientes opciones globales se aplican a todos los comandos:

- `--help`, `-h`: Muestra información de ayuda de la CLI o de una categoría de comandos o subcomando concretos.
- `--stacktrace`: Muestra la cadena de errores completa en caso de fallo, en lugar de solo el mensaje de nivel superior.

`--stacktrace` es una opción global en sentido estricto: debe indicarse **antes** de la categoría del comando, no después.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

No existe ningún indicador `--version`. Utilice en su lugar el comando [`version`](#version).

### Requisitos previos

La mayoría de los comandos necesitan un archivo `config.toml` legible y válido; algunos requieren además una licencia válida.
La siguiente tabla recoge lo que carga cada categoría de comandos antes de hacer nada:

| Categoría de comandos | Necesita `config.toml` | Necesita una licencia válida |
|---|---|---|
| `version` | no | no |
| `config check` | no (es precisamente aquello sobre lo que informa el comando) | no |
| `license check` | no | *es* la propia comprobación |
| `crypt` | sí | no |
| `serve` | sí | no |
| `project` | sí | no |
| `user` | sí | sí |
| `inspection` | sí | sí |
| `repo` | sí | sí |

Cuando se requiere una licencia, se comprueban tanto su firma como su fecha de caducidad, y el comando se interrumpe antes de tocar el repositorio si cualquiera de las dos falla.

### Códigos de salida

- `0`: el comando se ejecutó correctamente.
- `1`: el comando falló. El mensaje de error se escribe en stderr, precedido del prefijo `Error: `.

### help

La opción `--help` proporciona información sobre las categorías de comandos, los subcomandos y las opciones disponibles:

1. **Mostrar la ayuda general:**
   ```bash
   digna --help
   ```

2. **Obtener ayuda de categorías y comandos concretos:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **La salida incluye:**
   - **Descripción del comando:** Resumen del propósito del comando.
   - **Sintaxis:** Argumentos obligatorios y opcionales.
   - **Opciones:** Indicadores y parámetros propios del comando.

### version

El comando `version` imprime la versión instalada de ***digna***. No lee ninguna configuración ni valida ninguna licencia, por lo que también funciona en una instalación cuyo `config.toml` o cuya licencia falten o sean inválidos.

La versión del producto es independiente de la versión del esquema del repositorio que informa [`repo check`](#repo-check).

#### Uso del comando
```bash
digna version
```

#### Ejemplo de salida
```text
2026.06
```

---

## Gestión de la configuración

---

### config check

El comando `config check` valida el archivo de configuración (`config.toml`), comprobando que todas las secciones y ajustes obligatorios estén presentes y correctamente formateados. Cada sección se valida por separado, de modo que una sección `[app]` defectuosa no oculta el estado de `[repo]`.

Las secciones sobre las que se informa son:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — opcional; una clave ausente supera la comprobación, mientras que una lista presente pero mal formada falla

El comando deliberadamente no carga la configuración de la aplicación del modo en que lo hacen los demás comandos, para poder diagnosticar un `config.toml` que impediría que ***digna*** llegara siquiera a arrancar.

#### Uso del comando
```bash
digna config check [OPTIONS]
```

#### Opciones
- `--configpath`, `-c`: Ruta al archivo de configuración o a un directorio que contenga `config.toml` (por defecto `./config.toml`).
- `--json`: Genera el informe de validación en formato JSON. Tiene prioridad sobre `--quiet`.
- `--quiet`, `-q`: Suprime el informe y se basa únicamente en el código de salida.

#### Ejemplo
```bash
digna config check
```

Validar un archivo de configuración concreto y dar formato JSON a la salida:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Ejemplo de salida
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

Un archivo ausente o un error de sintaxis TOML no deja nada que validar sección por sección y se notifica como un único error en lugar de como un informe, con independencia de `--quiet` o `--json`.

---

## Gestión del repositorio

---

### repo check

El comando `repo check` prueba la conexión con la base de datos y verifica la instalación y la versión del repositorio. Falla si el esquema configurado no existe, o si existe pero no contiene ningún repositorio de ***digna***.

La versión que se informa es la del esquema del repositorio, que se versiona de forma independiente de la versión de ***digna*** que imprime [`version`](#version).

#### Uso del comando
```bash
digna repo check
```

#### Ejemplo de salida
```text
Repo version 3.0.0 installed
```

### repo install

El comando `repo install` instala un nuevo repositorio de ***digna*** en el esquema configurado en `config.toml`, creando todas las secuencias, tablas, índices, restricciones y registros iniciales necesarios.

Este comando **no** crea el esquema en sí: debe existir previamente. El comando también se niega a ejecutarse si ya hay un repositorio instalado en ese esquema, y remite a [`repo upgrade`](#repo-upgrade) si la versión instalada es anterior.

#### Uso del comando
```bash
digna repo install
```

#### Ejemplo de salida
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

El comando `repo upgrade` aplica migraciones del esquema de base de datos para llevar un repositorio existente a la versión que espera la versión instalada. Las actualizaciones se aplican de un salto de versión en un salto de versión a lo largo de una ruta de actualización fija, y cada salto completado queda registrado en el repositorio.

Si el repositorio ya está en la versión esperada, el comando informa de que no es necesaria ninguna actualización y no realiza cambios.

#### Uso del comando
```bash
digna repo upgrade
```

#### Ejemplo de salida
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Gestión del cifrado

---

### crypt gen-key

El comando `crypt gen-key` genera una nueva clave de cifrado AES-GCM para utilizarla como clave de cifrado en `config.toml`. Debe existir ya un `config.toml` que se pueda cargar, aunque la clave generada no dependa de él.

#### Uso del comando
```bash
digna crypt gen-key
```

#### Ejemplo de salida
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

El comando `crypt encrypt` cifra una cadena (como una contraseña de base de datos) utilizando la clave AES-GCM configurada en `config.toml` e imprime el texto cifrado.

#### Uso del comando
```bash
digna crypt encrypt <VALUE>
```

#### Argumentos
- **VALUE**: La cadena en texto claro que se va a cifrar (obligatorio).

#### Ejemplo
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

El comando `crypt decrypt` descifra una cadena cifrada con AES-GCM utilizando la clave configurada en `config.toml` e imprime el texto claro.

#### Uso del comando
```bash
digna crypt decrypt <VALUE>
```

#### Argumentos
- **VALUE**: La cadena cifrada que se va a descifrar (obligatorio).

#### Ejemplo
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Gestión de usuarios

---

### user add

El comando `user add` crea una nueva cuenta de usuario en el repositorio de ***digna***. El comando falla si ya existe un usuario con la dirección de correo electrónico indicada.

#### Uso del comando
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumentos
- **EMAIL**: La dirección de correo electrónico del usuario (obligatorio).
- **PASSWORD**: La contraseña inicial del usuario (obligatorio).
- **DISPLAY_NAME**: El nombre completo para mostrar del usuario (obligatorio).

#### Opciones
- `--admin`, `-a`: Crea el usuario con privilegios de administrador (superusuario).

#### Ejemplo
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Para crear una cuenta de administrador:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Ejemplo de salida
```text
User created with ID: 42
```

### user list

El comando `user list` enumera todos los usuarios registrados en formato de tabla con el ID, el correo electrónico, el nombre para mostrar y el indicador de administrador.

#### Uso del comando
```bash
digna user list
```

#### Ejemplo de salida
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

El comando `user modify` actualiza el nombre para mostrar y los privilegios de administrador de una cuenta de usuario existente, identificada por su dirección de correo electrónico.

Tanto el nombre para mostrar como el indicador de administrador se escriben siempre. `--admin` es un conmutador, no un valor: **omitirlo revoca los privilegios de administrador**, así que indíquelo siempre que el usuario deba conservarlos u obtenerlos.

#### Uso del comando
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumentos
- **EMAIL**: El correo electrónico del usuario que se va a modificar (obligatorio).
- **DISPLAY_NAME**: El nombre para mostrar actualizado (obligatorio).

#### Opciones
- `--admin`, `-a`: Concede privilegios de administrador. Omítalo para revocarlos.
- `--valid-until`, `-v`: Se acepta por compatibilidad, pero **actualmente no se aplica**. Indicarlo imprime una advertencia y no cambia nada.

#### Ejemplo
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Ejemplo de salida
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

El comando `user modify-pwd` actualiza la contraseña de una cuenta de usuario existente.

#### Uso del comando
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumentos
- **EMAIL**: El correo electrónico del usuario cuya contraseña se va a actualizar (obligatorio).
- **PASSWORD**: La nueva contraseña (obligatorio).

#### Ejemplo
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

El comando `user delete` elimina una cuenta de usuario del sistema.

#### Uso del comando
```bash
digna user delete <EMAIL>
```

#### Argumentos
- **EMAIL**: El correo electrónico del usuario que se va a eliminar (obligatorio).

#### Ejemplo
```bash
digna user delete jdoe@example.com
```

---

## Gestión de proyectos y fuentes de datos

---

### project list

El comando `project list` enumera todos los proyectos disponibles en el repositorio, mostrando su ID, su nombre y su descripción.

#### Uso del comando
```bash
digna project list
```

#### Ejemplo de salida
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

El comando `project list-ds` enumera todas las fuentes de datos asociadas a un proyecto determinado, mostrando su ID, su nombre, su tipo, su esquema y su nombre de tabla.

#### Uso del comando
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto cuyas fuentes de datos se van a enumerar (obligatorio). El nombre debe coincidir exactamente.

#### Ejemplo
```bash
digna project list-ds ProjectA
```

#### Ejemplo de salida
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

El comando `project export-ds` exporta las fuentes de datos de un proyecto a un documento JSON.

Si no se indica ni `--table-name` ni `--table-id`, se exportan todas las fuentes de datos del proyecto.

#### Uso del comando
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto del que se van a exportar las fuentes de datos (obligatorio).

#### Opciones
- `--table-name`, `-n`: Nombres de las fuentes de datos que se van a exportar. Se pueden indicar varios nombres separados por espacios.
- `--table-id`, `-i`: ID de las fuentes de datos que se van a exportar. Se pueden indicar varios ID separados por espacios.
- `--exportfile`, `-f`: Ruta en la que se guardan las fuentes de datos exportadas (por defecto: `data_sources_export.json`).

#### Ejemplo
Para exportar todas las fuentes de datos de `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Para exportar tablas concretas:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Ejemplo de salida
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

El comando `project import-ds` importa fuentes de datos desde un archivo de exportación a un proyecto de destino e informa, objeto por objeto, de lo que se creó, se actualizó o se omitió.

#### Uso del comando
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumentos
- **PROJECT_NAME**: Nombre del proyecto de destino al que se importa (obligatorio).
- **EXPORT_FILE**: Ruta al archivo de exportación JSON (obligatorio).

#### Opciones
- `--output-file`, `-o`: Archivo en el que se escribe el informe de importación. Sin él, el informe va a stdout.
- `--output-format`, `-f`: Formato del informe de importación — `table`, `json` o `csv` (por defecto: `table`).

#### Ejemplo
```bash
digna project import-ds ProjectB my_export.json
```

Para obtener un informe legible por máquina:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

El informe abarca cuatro niveles de objetos —fuente de datos, definición de conjunto de datos, atributo y regla de validación—, cada uno con su acción de importación, su resultado, el ID del objeto resultante y cualquier información adicional.

### project plan-import-ds

El comando `project plan-import-ds` muestra una vista previa de la importación de fuentes de datos en un proyecto de destino, indicando qué objetos se crearían, se actualizarían o se omitirían, sin cambiar nada. Acepta el mismo archivo de exportación y las mismas opciones de informe que [`project import-ds`](#project-import-ds), y añade un número de paso por cada objeto planificado.

#### Uso del comando
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumentos
- **PROJECT_NAME**: Nombre del proyecto de destino (obligatorio).
- **EXPORT_FILE**: Ruta al archivo de exportación (obligatorio).

#### Opciones
- `--output-file`, `-o`: Archivo en el que se escribe el plan de importación. Sin él, el plan va a stdout.
- `--output-format`, `-f`: Formato del plan de importación — `table`, `json` o `csv` (por defecto: `table`).

#### Ejemplo
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Gestión de inspecciones

---

### inspection run

El comando `inspection run` crea una solicitud de inspección para un proyecto y un intervalo de fechas y, a continuación —según las opciones indicadas—, espera a que termine, devuelve el control de inmediato o la ejecuta en su propio proceso.

Los tres modos de ejecución son:

- **Predeterminado (sin indicador)**: la solicitud se pone en cola para el backend, y la CLI la consulta cada dos segundos e imprime el progreso de las tareas hasta que la inspección alcanza un estado final. Se requiere un `digna serve` en ejecución; de lo contrario, nadie recoge la solicitud.
- **`--async-mode`**: la solicitud se pone en cola y su ID se imprime de inmediato. Utilice [`inspection status`](#inspection-status) para seguirla.
- **`--bypass-backend`**: la inspección la ejecuta el propio proceso de la CLI y no se pone en cola, por lo que no se necesita ningún servidor en ejecución.

`--async-mode` y `--bypass-backend` son mutuamente excluyentes.

En todos los modos, el comando termina con un código de salida distinto de cero si la inspección no se completó correctamente.

#### Uso del comando
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto de destino (obligatorio). El nombre debe coincidir exactamente.
- **START_DATE**: Fecha de inicio del intervalo en formato `YYYY-MM-DD` (obligatorio).
- **END_DATE**: Fecha de fin del intervalo en formato `YYYY-MM-DD` (obligatorio).

#### Opciones
- `--table-name`: Restringe la inspección a una única fuente de datos del proyecto, indicada por su nombre de fuente de datos. Sin esta opción se inspeccionan todas las fuentes de datos del proyecto.
- `--async-mode`: Pone la inspección en cola e imprime el ID de la solicitud en lugar de esperarla. No se puede combinar con `--bypass-backend`.
- `--bypass-backend`: Ejecuta la inspección directamente en el proceso de la CLI en lugar de ponerla en cola para el backend. No se puede combinar con `--async-mode`.

#### Ejemplo
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Para enviar una inspección asíncrona:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Para inspeccionar una única fuente de datos:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Ejemplo de salida
Modo predeterminado:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Modo asíncrono:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

El comando `inspection status` consulta el estado y el progreso de las tareas de una solicitud de inspección a partir de su ID de solicitud.

#### Uso del comando
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumentos
- **INSPECTION_REQUEST_ID**: El ID numérico de la solicitud de inspección (obligatorio).

#### Ejemplo
```bash
digna inspection status 1024
```

#### Ejemplo de salida
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

El comando `inspection abort` solicita la cancelación de solicitudes de inspección en curso o pendientes. Registra un evento de parada para cada solicitud afectada; es el backend quien actúa en consecuencia, de modo que abortar es una petición de detención y no una terminación inmediata.

#### Uso del comando
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumentos
- **INSPECTION_REQUEST_ID**: El ID de la solicitud de inspección que se va a abortar. Obligatorio salvo que se indique `--killall`.

#### Opciones
- `--killall`: Aborta todas las solicitudes de inspección en curso y pendientes. Tiene prioridad sobre un ID de solicitud indicado junto a él.

#### Ejemplo
Para abortar una solicitud concreta:
```bash
digna inspection abort 1024
```

Para abortar todas las inspecciones activas y en cola:
```bash
digna inspection abort --killall
```

#### Ejemplo de salida
`--killall` informa de lo que hizo; abortar una única solicitud no produce salida alguna e informa del éxito mediante su código de salida.
```text
All running and pending inspections have been aborted.
```

---

## Gestión de licencias

---

### license check

El comando `license check` valida `license.toml`, verificando su firma frente a la clave pública incluida con la instalación y comprobando que no haya caducado. No lee ninguna configuración de la aplicación, por lo que también funciona antes de que `config.toml` esté configurado.

#### Uso del comando
```bash
digna license check
```

#### Ejemplo de salida
```text
License is valid
```

Una firma no válida y una licencia caducada se notifican como errores distintos, ambos con el código de salida 1.

---

## Servidor y servicios en segundo plano

---

### serve

El comando `serve` inicia el servidor de la API REST de ***digna*** junto con el planificador de inspecciones en segundo plano y el gestor de inspecciones. Al arrancar también marca como fallida toda inspección que el repositorio siga registrando como en curso, ya que nada puede haber sobrevivido de un proceso anterior.

El comando se ejecuta en primer plano hasta que se detiene.

#### Uso del comando
```bash
digna serve [OPTIONS]
```

#### Opciones
- `--address`: Dirección de red a la que se enlaza el servidor de la API (por defecto: `127.0.0.1`).
- `--port`: Número de puerto de escucha (por defecto: `8000`).

#### Ejemplo
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Ejemplo de salida
```text
Server running on http://0.0.0.0:8000
```
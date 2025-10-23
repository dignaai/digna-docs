---
title: Referencia CLI de digna 2025.09 – Comandos y Ejemplos | Documentación de digna
description: Referencia completa para la CLI de digna versión 2025.09. Aprende a gestionar usuarios, repositorios y datos con comandos como add-user, check-config, check-repo-connection, inspect, inspect-async y más.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# Referencia CLI de digna 2025.09
**2025-09-29**

Esta página documenta el conjunto completo de comandos disponibles en la CLI de ***digna***, versión **2025.09**, incluyendo ejemplos de uso y opciones.

---

## Conceptos básicos de la CLI

---

### help
La opción `--help` proporciona información sobre los comandos disponibles y su uso. Hay dos formas principales de usar esta opción:

1. **Mostrar ayuda general:**
   
    Use --help inmediatamente después de la palabra clave ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Obtener ayuda para comandos específicos:**  
  
    Para información detallada sobre un comando en particular, añada `--help` a ese comando.
    Por ejemplo, para obtener ayuda del comando `add-user`, ejecute:
     ```bash
     dignacli add-user --help
     ```

     ### salida:
      
     - **Descripción del comando:** Ofrece una descripción detallada de lo que hace el comando.  
     - **Sintaxis:** Muestra la sintaxis exacta, incluidos los argumentos obligatorios y opcionales.  
     - **Opciones:** Enumera las opciones específicas del comando, junto con sus explicaciones.  
     - **Ejemplos:** Proporciona ejemplos de cómo ejecutar el comando de forma efectiva.

### check-config

El comando check-config es una utilidad dentro de la CLI de ***digna*** diseñada para comprobar la configuración de ***digna***. Este comando asegura que los componentes de ***digna*** puedan encontrar los elementos de configuración necesarios en el config.toml.

#### Opciones

- `--configpath`, `-cp`: Archivo o directorio que contiene la configuración. Si se omite, se usará ../config.toml.
      
#### Uso del comando
```bash
dignacli check-config
```

Tras una ejecución exitosa, el comando muestra una confirmación de que la configuración está completa.  
  
Si la configuración parece estar incompleta, se listarán los elementos de configuración faltantes.

  
### check-repo-connection

El comando check-repo-connection es una utilidad dentro de la CLI de ***digna*** diseñada para probar la conectividad y el acceso a un repositorio especificado de ***digna***. Este comando garantiza que la CLI pueda interactuar con el repositorio.
      
#### Uso del comando
```bash
dignacli check-repo-connection
```

Tras una ejecución exitosa, el comando muestra una confirmación de la conexión, junto con detalles sobre el repositorio: versión del repositorio, Host, Base de datos y Esquema.  
  
Si la conexión al repositorio no es exitosa, revise el archivo config.toml para verificar que la configuración sea correcta.


### version

Para comprobar la versión instalada de *dignacli*, utilice la opción --version.  
  
#### Uso del comando
```bash
dignacli --version
```
  
#### Ejemplo de salida
```bash
dignacli version 2025.09
```

### opciones de registro (logging)
  
Por defecto, la salida en consola de los comandos de ***digna*** está diseñada para ser minimalista. La mayoría de los comandos ofrecen la posibilidad de proporcionar información adicional, usando las siguientes opciones:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” y “debug” definen el nivel de detalle, mientras que el interruptor “logfile” permite redirigir la salida para que se escriba en un archivo en lugar de mostrarse en la consola.

## Gestión de usuarios

### add-user
  
El comando add-user en la CLI de ***digna*** se utiliza para añadir un nuevo usuario al sistema ***digna***.
  
#### Uso del comando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentos

- **USER_NAME**: El nombre de usuario para el nuevo usuario (requerido).
- **USER_FULL_NAME**: El nombre completo del nuevo usuario (requerido).
- **USER_PASSWORD**: La contraseña del nuevo usuario (requerido).

#### Opciones

- `--is_superuser`, `-su`: Indicador para designar al nuevo usuario como administrador.
- `--valid_until`, `-vu`: Establece una fecha de expiración para la cuenta de usuario en el formato `YYYY-MM-DD HH:MI:SS`. Si no se establece, la cuenta no tendrá fecha de expiración.

#### Ejemplo

Para agregar un nuevo usuario con nombre de usuario `jdoe`, nombre completo `John Doe` y contraseña `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Para añadir un nuevo usuario y establecer una fecha de expiración de la cuenta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
El comando `delete-user` en la CLI de ***digna*** se utiliza para eliminar un usuario existente del sistema ***digna***.
  
#### Uso del comando
```bash
dignacli delete-user USER_NAME
```
  
#### Argumentos
- **USER_NAME**: El nombre de usuario del usuario a eliminar (requerido). Este es el único argumento requerido por el comando.

#### Ejemplo
```bash
dignacli delete-user jdoe
```
  
Al ejecutar este comando se eliminará el usuario `jdoe` del sistema ***digna***, revocando su acceso y eliminando sus datos y permisos asociados del repositorio.

### modify-user

El comando `modify-user` en la CLI de ***digna*** se utiliza para actualizar los detalles de un usuario existente en el sistema ***digna***.

#### Uso del comando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentos
  
- **USER_NAME**: El nombre de usuario del usuario a modificar (requerido).
- **USER_FULL_NAME**: El nuevo nombre completo del usuario (requerido).
  
#### Opciones  
  
- `--is_superuser`, `-su`: Establece al usuario como superusuario, otorgándole privilegios elevados. Este flag no requiere un valor.  
- `--valid_until`, `-vu`: Establece una fecha de expiración para la cuenta de usuario en el formato YYYY-MM-DD HH:MI:SS. Si no se proporciona, la cuenta permanece válida indefinidamente.  
  
#### Ejemplo
  
Para modificar el nombre completo del usuario `jdoe` a “Johnathan Doe” y establecer al usuario como superusuario:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
El comando `modify-user-pwd` en la CLI de ***digna*** se utiliza para cambiar la contraseña de un usuario existente en el sistema ***digna***.
  
#### Uso del comando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumentos
  
- **USER_NAME**: El nombre de usuario del usuario cuya contraseña se va a cambiar (requerido).
- **USER_PWD**: La nueva contraseña del usuario (requerido).
  
#### Ejemplo
  
Para cambiar la contraseña del usuario `jdoe` a `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

El comando `list-users` en la CLI de ***digna*** muestra una lista de todos los usuarios registrados en el sistema ***digna***.

#### Uso del comando

```bash
dignacli list-users
```

Al ejecutar este comando, la CLI de ***digna*** se conectará al repositorio de ***digna*** y listará todos los usuarios, mostrando su ID, nombre de usuario, nombre completo, estado de superusuario y las marcas de tiempo de expiración.

## Gestión del repositorio

### upgrade-repo
  
El comando `upgrade-repo` en la CLI de ***digna*** se utiliza para actualizar o inicializar el repositorio de ***digna***. Este comando es esencial para aplicar actualizaciones o configurar la infraestructura del repositorio por primera vez.
  
#### Uso del comando

```bash
dignacli upgrade-repo [options]
```
  
#### Opciones
  
- `--simulation-mode`, `-s`: Cuando está habilitado, esta opción ejecuta el comando en modo de simulación, que imprime las sentencias SQL que se ejecutarían pero no las ejecuta realmente. Esto es útil para previsualizar cambios sin realizar modificaciones en el repositorio.  

  
#### Ejemplo
  
Para actualizar el repositorio de ***digna***, puede ejecutar el comando sin opciones:
  
```bash
dignacli upgrade-repo
```  
Para ejecutar la actualización en modo de simulación (para ver las sentencias SQL sin aplicarlas):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Este comando es crucial para mantener el sistema ***digna***, asegurando que el esquema de la base de datos y otros componentes del repositorio estén actualizados con la última versión del software.

### encrypt
  
El comando `encrypt` en la CLI de ***digna*** se utiliza para cifrar una contraseña.
  
#### Uso del comando
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentos
- **PASSWORD**: La contraseña que necesita ser cifrada (requerido).
  
#### Ejemplo
  
Para cifrar una contraseña, debe proporcionar la contraseña como argumento.   
Por ejemplo, para cifrar la contraseña `mypassword123`, utilice:
```bash
dignacli encrypt mypassword123
```
Este comando devuelve la versión cifrada de la contraseña proporcionada, que puede luego usarse en contextos seguros. Si no se proporciona el argumento de contraseña, la CLI mostrará un error indicando el argumento faltante.

### generate-key
  
El comando `generate-key` se utiliza para generar una clave Fernet, que es esencial para asegurar las contraseñas almacenadas en el repositorio de ***digna***.
  
#### Uso del comando
```bash
dignacli generate-key
```
  
## Gestión de datos

### clean-up

El comando `clean-up` en la CLI de ***digna*** se utiliza para eliminar perfiles, predicciones y datos del sistema de semáforo para una o varias fuentes de datos dentro de un proyecto especificado. Este comando es esencial para la gestión del ciclo de vida de los datos, ayudando a mantener un entorno de datos ordenado y eficiente al eliminar datos obsoletos o innecesarios.

#### Uso del comando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto del cual se eliminarán datos (requerido). Usar la palabra clave all-projects en este argumento instruye a ***digna*** para iterar sobre todos los proyectos existentes y aplicar este comando.
- **FROM_DATE**: La fecha y hora de inicio para la eliminación de datos. Los formatos aceptables incluyen %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (requerido).
- **TO_DATE**: La fecha y hora de fin para la eliminación de datos, siguiendo los mismos formatos que FROM_DATE (requerido).
  
#### Opciones
  
- `--table-name`, `-tn`: Limita la operación de limpieza a una tabla específica dentro del proyecto.
- `--table-filter`, `-tf`: Filtros para limitar la limpieza a tablas que contengan la subcadena especificada en sus nombres.
- `--timing`, `-tm`: Muestra la duración temporal del proceso de limpieza al finalizar.
- `--help`: Muestra la información de ayuda para el comando clean-up y sale.
  
#### Ejemplo
  
Para eliminar datos del proyecto ProjectA entre el 1 de enero de 2023 y el 30 de junio de 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Para eliminar datos solo de una tabla específica llamada `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Este comando ayuda a gestionar el almacenamiento de datos y a asegurar que el repositorio contenga únicamente información relevante.

### remove-orphans
  
El comando `remove-orphans` en la CLI de ***digna*** se utiliza para tareas de mantenimiento en el repositorio de ***digna***.  
Cuando un usuario elimina proyectos o fuentes de datos, los perfiles y predicciones permanecen en el repositorio. Con este comando, dichas filas huérfanas se eliminarán del repositorio.
  
#### Uso del comando
  
```bash
dignacli list-projects
```

### list-projects
  
El comando `list-projects` en la CLI de ***digna*** se utiliza para mostrar una lista de todos los proyectos disponibles dentro del sistema ***digna***.
  
#### Uso del comando
  
```bash
dignacli list-projects
```

Este comando es especialmente útil para administradores y usuarios que gestionan múltiples proyectos, proporcionando una vista rápida de los proyectos disponibles en el repositorio de ***digna***.

### list-ds

El comando `list-ds` en la CLI de ***digna*** se utiliza para mostrar una lista de todas las fuentes de datos disponibles dentro de un proyecto especificado. Este comando es útil para entender los activos de datos disponibles para análisis y gestión en el sistema ***digna***.

#### Uso del comando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto para el cual se listan las fuentes de datos (requerido).
  
#### Ejemplo
  
Para listar todas las fuentes de datos en el proyecto llamado `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Este comando proporciona a los usuarios una visión general de las fuentes de datos disponibles en un proyecto, ayudándoles a navegar y gestionar el panorama de datos de forma más efectiva.


### inspect

El comando `inspect` en la CLI de ***digna*** se utiliza para crear perfiles, predicciones y datos del sistema de semáforos para una o varias fuentes de datos dentro de un proyecto especificado. Este comando ayuda a analizar y monitorizar los datos durante un período definido. Tras la finalización de la inspección, se devuelve el valor calculado del sistema de semáforos:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Uso del comando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto para el que se van a inspeccionar datos (requerido). Usar la palabra clave all-projects en este argumento instruye a ***digna*** para iterar sobre todos los proyectos existentes y aplicar este comando.
- **FROM_DATE**: La fecha y hora de inicio para la inspección de datos. Los formatos aceptables incluyen %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (requerido).
- **TO_DATE**: La fecha y hora de fin para la inspección de datos, siguiendo los mismos formatos que FROM_DATE (requerido).
  
#### Opciones

- `--table-name`, `-tn`: Limita la inspección a una tabla específica dentro del proyecto.
- `--table-filter`, `-tf`: Filtra para inspeccionar solo las tablas que contengan la subcadena especificada en sus nombres.
- `--enable_notification`, `-en`: Habilita el envío de notificaciones en caso de alertas.
- `--bypass-backend`, `-bb`: Omite el backend y ejecuta la inspección directamente desde la CLI (¡solo para pruebas!).

  
#### Ejemplo
  
Para inspeccionar datos del proyecto `ProjectA` desde el 1 de enero de 2024 hasta el 31 de enero de 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Para inspeccionar solo una tabla específica y forzar el recálculo de predicciones:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Este comando es útil para generar perfiles y predicciones actualizadas, monitorizar la integridad de los datos y gestionar sistemas de alerta dentro de un marco temporal especificado del proyecto.

### inspect-async

El comando `inspect-async` en la CLI de ***digna*** se utiliza para crear perfiles, predicciones y datos del sistema de semáforos para una o varias fuentes de datos dentro de un proyecto especificado. Este comando ayuda a analizar y monitorizar datos durante un período definido. A diferencia del comando `inspect`, este no espera a la finalización de la inspección.
En su lugar, devuelve el id de la solicitud para la inspección enviada. Para consultar el progreso del proceso de inspección, use el comando `inspect-status`.

#### Uso del comando

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto para el que se van a inspeccionar datos (requerido). Usar la palabra clave all-projects en este argumento instruye a ***digna*** para iterar sobre todos los proyectos existentes y aplicar este comando.
- **FROM_DATE**: La fecha y hora de inicio para la inspección de datos. Los formatos aceptables incluyen %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (requerido).
- **TO_DATE**: La fecha y hora de fin para la inspección de datos, siguiendo los mismos formatos que FROM_DATE (requerido).
  
#### Opciones

- `--table-name`, `-tn`: Limita la inspección a una tabla específica dentro del proyecto.
- `--table-filter`, `-tf`: Filtra para inspeccionar solo las tablas que contengan la subcadena especificada en sus nombres.
- `--enable_notification`, `-en`: Habilita el envío de notificaciones en caso de alertas.

  
#### Ejemplo
  
Para inspeccionar datos del proyecto `ProjectA` desde el 1 de enero de 2024 hasta el 31 de enero de 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

El comando `inspect-status` en la CLI de ***digna*** se utiliza para comprobar el progreso de una inspección asíncrona basándose en el ID de la solicitud.

#### Uso del comando

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentos
  
- **REQUEST_ID**: El id de la solicitud devuelto por el comando `inspect-async`. 
  
#### Ejemplo
  
Para comprobar el progreso de una inspección con ID de solicitud 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

El comando `inspect-cancel` en la CLI de ***digna*** se utiliza para cancelar inspecciones basadas en el ID de la solicitud o puede usarse para cancelar todas las solicitudes actuales.

#### Uso del comando

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentos
  
- **REQUEST_ID**: El id de la solicitud devuelto por el comando `inspect-async`. 
  
#### Ejemplo
  
Para cancelar la inspección con ID de solicitud 12345:
  
```bash
dignacli inspect-cancel 12345
```

Para cancelar todas las solicitudes que estén actualmente en ejecución o pendientes:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

El comando `export-ds` en la CLI de ***digna*** se utiliza para crear una exportación de fuentes de datos desde el repositorio de ***digna***. Por defecto, se exportarán todas las fuentes de datos de un proyecto dado.

#### Uso del comando
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto desde el cual se exportarán las fuentes de datos.

#### Opciones

- `--table_name`, `-tn`: Exporta una fuente de datos particular de un proyecto.
- `--exportfile`, `-ef`: Especifica el nombre de archivo para la exportación.
    
#### Ejemplo
  
Para exportar todas las fuentes de datos del proyecto llamado `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Este comando exporta todas las fuentes de datos de `ProjectA` como un documento JSON que puede importarse a otro proyecto o repositorio de ***digna***.


### import-ds

El comando `import-ds` en la CLI de ***digna*** se utiliza para importar fuentes de datos a un proyecto objetivo y crear un informe de importación.

#### Uso del comando
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto al que se importarán las fuentes de datos.
- **EXPORT_FILE**: El nombre de archivo de la exportación de fuentes de datos que se va a importar.

#### Opciones

- `--output-file`, `-o`: Archivo para guardar el informe de importación (si no se especifica, imprime en la terminal en forma tabular).
- `--output-format`, `-f`: Formato para guardar el informe de importación (json, csv).
    
#### Ejemplo
  
Para importar todas las fuentes de datos desde el archivo de exportación `my_export.json` en `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Después de la importación, este comando también mostrará un informe de los objetos importados y omitidos. Solo se importarán nuevas fuentes de datos en `ProjectB`. Para averiguar qué objetos se importarían y cuáles se omitirían, puede usar el comando `plan-import-ds`.

### plan-import-ds

El comando `plan-import-ds` en la CLI de ***digna*** se utiliza para analizar una exportación de fuentes de datos antes de importarla a un proyecto objetivo y crear un informe de planificación de la importación.

#### Uso del comando
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto al que se analizaría la importación de las fuentes de datos.
- **EXPORT_FILE**: El nombre de archivo de la exportación de fuentes de datos que se va a analizar antes de la importación.

#### Opciones

- `--output-file`, `-o`: Archivo para guardar el informe de importación (si no se especifica, imprime en la terminal en forma tabular).
- `--output-format`, `-f`: Formato para guardar el informe de importación (json, csv).
    
#### Ejemplo
  
Para comprobar qué fuentes de datos se importarían y cuáles se omitirían desde el archivo de exportación `my_export.json` al importarlo en `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Este comando solo mostrará un plan de importación de los objetos que se importarían y los que se omitirían.
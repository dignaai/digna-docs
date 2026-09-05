---
title: Referencia de la CLI de digna 2025.04 – Comandos y Ejemplos | Documentación de digna
description: Referencia completa de la CLI de digna versión 2025.04. Aprende a gestionar usuarios, repositorios y datos con comandos como add-user, check-repo-connection, upgrade-repo, inspect y más.
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Esta página documenta el conjunto completo de comandos disponibles en la CLI de ***digna***, versión **2025.04**, incluyendo ejemplos de uso y opciones.

---

## Principios básicos de la CLI

---

## Uso de la opción `help`

La opción `--help` proporciona información sobre los comandos disponibles y su uso. Hay dos formas principales de usar esta opción:

1. **Mostrar la ayuda general:**
   
    Use --help inmediatamente después de la palabra clave ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Obtener ayuda para comandos específicos:**  
  
    Para obtener información detallada sobre un comando específico, añada `--help` a ese comando.
    Por ejemplo, para obtener ayuda sobre el comando `add-user`, ejecute:
     ```bash
     dignacli add-user --help
     ```

     ### salida:
      
     - **Descripción del comando:** Ofrece una descripción detallada de lo que hace el comando.  
     - **Sintaxis:** Muestra la sintaxis exacta, incluyendo los argumentos obligatorios y opcionales.  
     - **Opciones:** Enumera las opciones específicas del comando, junto con sus explicaciones.  
     - **Ejemplos:** Proporciona ejemplos de cómo ejecutar el comando de forma efectiva.

  
## Uso del comando `check-repo-connection`

El comando check-repo-connection es una utilidad dentro de la CLI de ***digna*** diseñada para probar la conectividad y el acceso a un repositorio especificado de ***digna***. Este comando garantiza que la CLI pueda interactuar con el repositorio.
      
#### Uso del comando
```bash
dignacli check-repo-connection
```

Al ejecutarse correctamente, el comando muestra una confirmación de la conexión, junto con detalles sobre el repositorio: versión del repositorio, Host, Base de datos y Esquema.  
  
Si la conexión al repositorio no es exitosa, verifique el archivo config.toml para asegurarse de que las configuraciones sean correctas.

## Uso del comando ‘version’

Para comprobar la versión instalada de *dignacli*, utilice la opción --version.  
  
#### Uso del comando
```bash
dignacli --version
```
  
#### Ejemplo de salida
```bash
dignacli version 2025.04
```

## Uso de opciones de registro (logging)
  
Por defecto, la salida por consola de los comandos de ***digna*** está pensada para ser minimalista. La mayoría de los comandos ofrecen la posibilidad de proporcionar información adicional, usando las siguientes opciones:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” y “debug” definen el nivel de detalle, mientras que la opción “logfile” permite redirigir la salida para que se escriba en un archivo en lugar de la ventana de la consola.

## Gestión de usuarios

### Uso del comando ‘add-user’
  
El comando add-user en la CLI de ***digna*** se utiliza para añadir un nuevo usuario al sistema de ***digna***.
  
#### Uso del comando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumentos

- **USER_NAME**: El nombre de usuario para el nuevo usuario (obligatorio).
- **USER_FULL_NAME**: El nombre completo del nuevo usuario (obligatorio).
- **USER_PASSWORD**: La contraseña para el nuevo usuario (obligatorio).

#### Opciones

- `--is_superuser`, `-su`: Indicador para designar al nuevo usuario como administrador.
- `--valid_until`, `-vu`: Establece una fecha de expiración para la cuenta de usuario en el formato `YYYY-MM-DD HH:MI:SS`. Si no se establece, la cuenta no tiene fecha de expiración.

#### Ejemplo

Para añadir un nuevo usuario con nombre de usuario `jdoe`, nombre completo `John Doe` y contraseña `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Para añadir un nuevo usuario y establecer una fecha de expiración de la cuenta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Uso del comando `delete-user`
  
El comando `delete-user` en la CLI de ***digna*** se utiliza para eliminar un usuario existente del sistema de ***digna***.
  
#### Uso del comando
```bash
dignacli delete-user USER_NAME
```
  
##### Argumentos
- **USER_NAME**: El nombre de usuario del usuario que se va a eliminar (obligatorio). Este es el único argumento requerido por el comando.

#### Ejemplo
```bash
dignacli delete-user jdoe
```
  
Al ejecutar este comando se eliminará el usuario `jdoe` del sistema de ***digna***, revocando su acceso y eliminando sus datos y permisos asociados del repositorio.

### Uso del comando `modify-user`

El comando `modify-user` en la CLI de ***digna*** se utiliza para actualizar los detalles de un usuario existente en el sistema de ***digna***.

#### Uso del comando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumentos
  
- **USER_NAME**: El nombre de usuario del usuario que se va a modificar (obligatorio).
- **USER_FULL_NAME**: El nuevo nombre completo del usuario (obligatorio).
  
#### Opciones  
  
- `--is_superuser`, `-su`: Establece al usuario como superusuario, otorgando privilegios elevados. Este indicador no requiere un valor.  
- `--valid_until`, `-vu`: Establece una fecha de expiración para la cuenta de usuario en el formato YYYY-MM-DD HH:MI:SS. Si no se proporciona, la cuenta permanecerá válida indefinidamente.  
  
#### Ejemplo
  
Para modificar el nombre completo del usuario `jdoe` a “Johnathan Doe” y establecer al usuario como superusuario:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Uso del comando `modify-user-pwd`
  
El comando `modify-user-pwd` en la CLI de ***digna*** se utiliza para cambiar la contraseña de un usuario existente en el sistema de ***digna***.
  
#### Uso del comando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumentos
  
- **USER_NAME**: El nombre de usuario del usuario cuya contraseña se va a cambiar (obligatorio).
- **USER_PWD**: La nueva contraseña para el usuario (obligatorio).
  
#### Ejemplo
  
Para cambiar la contraseña del usuario `jdoe` a `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Uso del comando `list-users`

El comando `list-users` en la CLI de ***digna*** muestra una lista de todos los usuarios registrados en el sistema de ***digna***.

#### Uso del comando

```bash
dignacli list-users
```

Al ejecutar este comando en la CLI de ***digna*** se conectará al repositorio de ***digna*** y listará todos los usuarios, mostrando su ID, nombre de usuario, nombre completo, estado de superusuario y marcas de tiempo de expiración.

## Gestión de repositorios

### Uso del comando `upgrade-repo`
  
El comando `upgrade-repo` en la CLI de ***digna*** se utiliza para actualizar o inicializar el repositorio de ***digna***. Este comando es esencial para aplicar actualizaciones o configurar la infraestructura del repositorio por primera vez.
  
#### Uso del comando

```bash
dignacli upgrade-repo [options]
```
  
#### Opciones
  
- `--simulation-mode`, `-s`: Cuando está habilitada, esta opción ejecuta el comando en modo simulación, que imprime las sentencias SQL que se ejecutarían pero no las ejecuta realmente. Esto es útil para previsualizar los cambios sin modificar el repositorio.  

  
#### Ejemplo
  
Para actualizar el repositorio de ***digna***, puede ejecutar el comando sin opciones:
  
```bash
dignacli upgrade-repo
```  
Para ejecutar la actualización en modo simulación (para ver las sentencias SQL sin aplicarlas):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Este comando es crucial para mantener el sistema de ***digna***, asegurando que el esquema de la base de datos y otros componentes del repositorio estén actualizados con la última versión del software.

### Uso del comando `encrypt`
  
El comando `encrypt` en la CLI de ***digna*** se utiliza para cifrar una contraseña.
  
#### Uso del comando
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentos
- **PASSWORD**: La contraseña que debe cifrarse (obligatorio).
  
#### Ejemplo
  
Para cifrar una contraseña, debe proporcionar la contraseña como argumento.   
Por ejemplo, para cifrar la contraseña `mypassword123`, usaría:
```bash
dignacli encrypt mypassword123
```
Este comando muestra la versión cifrada de la contraseña proporcionada, que luego puede utilizarse en contextos seguros. Si no se proporciona el argumento de contraseña, la CLI mostrará un error indicando el argumento faltante.

## Uso del comando `generate-key`
  
El comando `generate-key` se utiliza para generar una clave Fernet, que es esencial para securizar las contraseñas almacenadas en el repositorio de ***digna***.
  
#### Uso del comando
```bash
dignacli generate-key
```
  
## Gestión de datos

## Uso del comando `clean-up`

El comando `clean-up` en la CLI de ***digna*** se utiliza para eliminar perfiles, predicciones y datos del Sistema de Semáforo (Traffic Light System) para una o más fuentes de datos dentro de un proyecto especificado. Este comando es esencial para la gestión del ciclo de vida de los datos, ayudando a mantener un entorno de datos organizado y eficiente al limpiar datos obsoletos o innecesarios.

#### Uso del comando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto del que se van a eliminar los datos (obligatorio). Usar la palabra clave all-projects en este argumento indica a ***digna*** que itere sobre todos los proyectos existentes y aplique este comando.
- **FROM_DATE**: La fecha y hora de inicio para la eliminación de datos. Los formatos aceptables incluyen %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obligatorio).
- **TO_DATE**: La fecha y hora de fin para la eliminación de datos, siguiendo los mismos formatos que FROM_DATE (obligatorio).
  
#### Opciones
  
- `--table-name`, `-tn`: Limita la operación de limpieza a una tabla específica dentro del proyecto.
- `--table-filter`, `-tf`: Filtra para limitar la limpieza a tablas que contengan la subcadena especificada en sus nombres.
- `--timing`, `-tm`: Muestra la duración del proceso de limpieza al finalizar.
- `--help`: Muestra información de ayuda para el comando clean-up y sale.
  
#### Ejemplo
  
Para eliminar datos del proyecto ProjectA entre el 1 de enero de 2023 y el 30 de junio de 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Para eliminar datos solo de una tabla específica llamada `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Este comando ayuda a gestionar el almacenamiento de datos y a garantizar que el repositorio contenga únicamente información relevante.

## Uso del comando `list-projects`
  
El comando `list-projects` en la CLI de ***digna*** se utiliza para mostrar una lista de todos los proyectos disponibles dentro del sistema de ***digna***.
  
#### Uso del comando
  
```bash
dignacli list-projects
```

Este comando es especialmente útil para administradores y usuarios que gestionan múltiples proyectos, proporcionando una visión rápida de los proyectos disponibles en el repositorio de ***digna***.

## Uso del comando `list-ds`

El comando `list-ds` en la CLI de ***digna*** se utiliza para mostrar una lista de todas las fuentes de datos disponibles dentro de un proyecto especificado. Este comando es útil para comprender los activos de datos disponibles para análisis y gestión en el sistema de ***digna***.

#### Uso del comando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto para el que se listan las fuentes de datos (obligatorio).
  
#### Ejemplo
  
Para listar todas las fuentes de datos en el proyecto llamado `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Este comando proporciona a los usuarios una visión general de las fuentes de datos disponibles en un proyecto, ayudándoles a navegar y gestionar el panorama de datos de manera más efectiva.


## Uso del comando `inspect`

El comando `inspect` en la CLI de ***digna*** se utiliza para crear perfiles, predicciones y datos del Sistema de Semáforo (Traffic Light System) para una o más fuentes de datos dentro de un proyecto especificado. Este comando ayuda a analizar y monitorizar datos durante un período definido.

#### Uso del comando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto que se va a inspeccionar (obligatorio). Usar la palabra clave all-projects en este argumento indica a ***digna*** que itere sobre todos los proyectos existentes y aplique este comando.
- **FROM_DATE**: La fecha y hora de inicio para la inspección de datos. Los formatos aceptables incluyen %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obligatorio).
- **TO_DATE**: La fecha y hora de fin para la inspección de datos, siguiendo los mismos formatos que FROM_DATE (obligatorio).
  
#### Opciones

- `--table-name`, `-tn`: Limita la inspección a una tabla específica dentro del proyecto.
- `--table-filter`, `-tf`: Filtra para inspeccionar solo tablas que contengan la subcadena especificada en sus nombres.
- `--do-profile`: Fuerza la recolección de perfiles. El valor predeterminado es do-profile.
- `--no-do-profile`: Impide la recolección de perfiles.
- `--do-prediction`: Fuerza el recalculo de predicciones. El valor predeterminado es do-prediction.
- `--no-do-prediction`: Impide el recalculo de predicciones.
- `--do-alert-status`: Fuerza el recalculo de los estados de alerta. El valor predeterminado es do-alert-status.
- `--no-do-alert-status`: Impide el recalculo de los estados de alerta.
- `--iterative`: Ejecuta la inspección de un periodo usando iteraciones diarias. El valor predeterminado es iterative.
- `--no-iterative`: Ejecuta la inspección de todo el periodo de una sola vez.
- `--enable_notification`, `-en`: Habilita el envío de notificaciones en caso de alertas.
- `--timing`, `-tm`: Muestra la duración del proceso de inspección al finalizar.
  
#### Ejemplo
  
Para inspeccionar datos del proyecto `ProjectA` desde el 1 de enero de 2024 hasta el 31 de enero de 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Para inspeccionar solo una tabla específica y forzar el recálculo de predicciones:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Este comando es útil para generar perfiles y predicciones actualizados, monitorizar la integridad de los datos y gestionar los sistemas de alerta dentro de un intervalo temporal específico del proyecto.

## Uso del comando `tls-status`

El comando `tls-status` en la CLI de ***digna*** se utiliza para consultar el estado del Traffic Light System (TLS) para una tabla específica dentro de un proyecto en una fecha determinada. El Traffic Light System ofrece información sobre la salud y calidad de los datos, indicando posibles incidencias o alertas que puedan requerir atención.
  
#### Uso del comando
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto para el cual se consulta el estado TLS (obligatorio).
- **TABLE_NAME**: La tabla específica dentro del proyecto para la cual se necesita el estado TLS (obligatorio).
- **DATE**: La fecha para la cual se consulta el estado TLS, típicamente en el formato %Y-%m-%d (obligatorio).
  
#### Ejemplo
  
Para comprobar el estado TLS de una tabla llamada UserData en el proyecto ProjectA el 1 de julio de 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Este comando ayuda a los usuarios a monitorizar y mantener la calidad de los datos proporcionando un informe claro y accionable basado en criterios predefinidos.

## Uso del comando `inspect-async`

El comando `inspect-async` en la CLI de ***digna*** se utiliza para indicar al backend que realice de forma asíncrona la inspección de una o más fuentes de datos de un proyecto dado. Si project_name se establece en all-projects, la inspección iterará sobre todos los proyectos disponibles y realizará la inspección. Devuelve un id de solicitud que puede usarse para rastrear el progreso de la inspección.

#### Uso del comando

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto que se va a inspeccionar (obligatorio). Usar la palabra clave all-projects en este argumento indica a ***digna*** que itere sobre todos los proyectos existentes y aplique este comando.
- **FROM_DATE**: La fecha y hora de inicio para la inspección de datos. Los formatos aceptables incluyen %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obligatorio).
- **TO_DATE**: La fecha y hora de fin para la inspección de datos, siguiendo los mismos formatos que FROM_DATE (obligatorio).
  
#### Opciones

- `--table-name`, `-tn`: Limita la inspección a una tabla específica dentro del proyecto.
- `--table-filter`, `-tf`: Filtra para inspeccionar solo tablas que contengan la subcadena especificada en sus nombres.

  
#### Ejemplo
  
Para inspeccionar datos del proyecto `ProjectA` desde el 1 de enero de 2024 hasta el 31 de enero de 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Uso del comando `inspect-status`

El comando `inspect-status` en la CLI de ***digna*** se utiliza para comprobar el progreso de una inspección asíncrona en base al id de solicitud.

#### Uso del comando

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumentos
  
- **REQUEST_ID**: El id de solicitud devuelto por el comando `inspect-async` 
  
#### Opciones

- `--report_level`, `-rl`: Establece el nivel de informe: 'task' o 'step' [predeterminado: task]
  
#### Ejemplo
  
Para comprobar el progreso de una inspección con id de solicitud 12345 en el nivel detallado por pasos:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Uso del comando `export-ds`

El comando `export-ds` en la CLI de ***digna*** se utiliza para crear una exportación de fuentes de datos desde el repositorio de ***digna***. Por defecto, se exportarán todas las fuentes de datos de un proyecto dado.

#### Uso del comando
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto desde el cual se exportarán las fuentes de datos.

#### Opciones

- `--table_name`, `-tn`: Exportar una fuente de datos particular desde un proyecto.
- `--exportfile`, `-ef`: Especificar el nombre de archivo para la exportación.
    
#### Ejemplo
  
Para exportar todas las fuentes de datos del proyecto llamado `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Este comando exporta todas las fuentes de datos de `ProjectA` como un documento JSON que puede importarse en otro proyecto o repositorio de ***digna***.


## Uso del comando `import-ds`

El comando `import-ds` en la CLI de ***digna*** se utiliza para importar fuentes de datos en un proyecto destino y crear un informe de importación.

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
  
Después de la importación, este comando también mostrará un informe de los objetos importados y omitidos. Solo se importarán nuevas fuentes de datos en `ProjectB`. Para averiguar qué objetos serían importados y omitidos, puede usar el comando `plan-import-ds`

## Uso del comando `plan-import-ds`

El comando `plan-import-ds` en la CLI de ***digna*** se utiliza para analizar una exportación de fuentes de datos antes de importarla en un proyecto destino y crear un informe de importación previsto.

#### Uso del comando
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto al que se importarían las fuentes de datos.
- **EXPORT_FILE**: El nombre de archivo de la exportación de fuentes de datos que se analizará antes de la importación.

#### Opciones

- `--output-file`, `-o`: Archivo para guardar el informe de importación (si no se especifica, imprime en la terminal en forma tabular).
- `--output-format`, `-f`: Formato para guardar el informe de importación (json, csv).
    
#### Ejemplo
  
Para comprobar qué fuentes de datos se importarían y cuáles se omitirían desde el archivo de exportación `my_export.json` cuando se importe en `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Este comando solo mostrará un plan de importación de los objetos que se importarán y los que se omitirán.
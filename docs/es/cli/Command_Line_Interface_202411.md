---
title: Referencia de la CLI de digna 2024.11 – Comandos y Ejemplos | Documentación de digna
description: Referencia completa de la CLI de digna, versión 2024.11. Aprenda cómo gestionar usuarios, repositorios y datos con comandos como add-user, check-repo-connection, upgrade-repo, inspect, tls-status y más.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# Referencia de la CLI de digna 2024.11
**2024-11-03**

Esta página documenta el conjunto completo de comandos disponibles en la CLI de ***digna***, versión **2024.11**, incluyendo ejemplos de uso y opciones.


---
## Conceptos básicos de la CLI

---

## Uso de la opción `--help`

La opción `--help` proporciona información sobre los comandos disponibles y su uso. Hay dos formas principales de utilizar esta opción:

1. **Mostrar la ayuda general:**
   
   Use `--help` inmediatamente después de la palabra clave ***dignacli***  
   ```bash
   dignacli --help

3.  **Obtener ayuda para comandos específicos:**  
  
    Para obtener información detallada sobre un comando específico, añada `--help` a ese comando.  
    Por ejemplo, para obtener ayuda sobre el comando `add-user`, ejecute:
     ```bash
     dignacli add-user --help
     ```

     ### salida:
      
     - **Descripción del comando:** Ofrece una descripción detallada de lo que hace el comando.  
     - **Sintaxis:** Muestra la sintaxis exacta, incluyendo argumentos obligatorios y opcionales.  
     - **Opciones:** Enumera las opciones específicas del comando, junto con sus explicaciones.  
     - **Ejemplos:** Proporciona ejemplos de cómo ejecutar el comando de forma efectiva.

  
## Uso del comando `check-repo-connection`

El comando `check-repo-connection` es una utilidad dentro de la herramienta de línea de comandos ***digna*** diseñada para probar la conectividad y el acceso a un repositorio especificado de ***digna***. Este comando asegura que la CLI puede interactuar con el repositorio.
      
### Uso del comando
```bash
dignacli check-repo-connection
```

Al ejecutarse correctamente, el comando devuelve una confirmación de la conexión, junto con detalles sobre el repositorio: versión del repositorio, Host, Base de datos y Esquema.  
  
Si la conexión al repositorio no es exitosa, verifique el archivo config.toml para confirmar que las configuraciones sean correctas.

## Uso del comando ‘version’

Para comprobar la versión instalada de *dignacli*, use la opción `--version`.  
  
### Uso del comando
```bash
dignacli --version
```
  
### Ejemplo de salida
```bash
dignacli version 2024.11
```

## Uso de las opciones de registro (logging)
  
Por defecto, la salida por consola de los comandos de ***digna*** está diseñada para ser minimalista. La mayoría de los comandos ofrecen la posibilidad de proporcionar información adicional mediante las siguientes opciones:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” y “debug” definen el nivel de detalle, mientras que la opción “logfile” permite redirigir la salida para que se almacene en un archivo en lugar de mostrarse en la consola.

# Gestión de usuarios

## Uso del comando ‘add-user’
  
El comando `add-user` en la CLI de ***digna*** se utiliza para añadir un nuevo usuario al sistema ***digna***.
  
### Uso del comando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentos

- **USER_NAME**: El nombre de usuario para el nuevo usuario (requerido).
- **USER_FULL_NAME**: El nombre completo del nuevo usuario (requerido).
- **USER_PASSWORD**: La contraseña del nuevo usuario (requerido).

### Opciones

- `--is_superuser`, `-su`: Indicador para designar al nuevo usuario como administrador.
- `--valid_until`, `-vu`: Establece una fecha de expiración para la cuenta del usuario en el formato `YYYY-MM-DD HH:MI:SS`. Si no se establece, la cuenta no tiene fecha de expiración.

### Ejemplo

Para añadir un nuevo usuario con nombre de usuario `jdoe`, nombre completo `John Doe` y contraseña `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Para añadir un nuevo usuario y establecer una fecha de expiración de la cuenta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Uso del comando `delete-user`
  
El comando `delete-user` en la CLI de ***digna*** se utiliza para eliminar un usuario existente del sistema ***digna***.
  
### Uso del comando
```bash
dignacli delete-user USER_NAME
```
  
### Argumentos
- **USER_NAME**: El nombre de usuario del usuario que se va a eliminar (requerido). Este es el único argumento requerido por el comando.

### Ejemplo
```bash
dignacli delete-user jdoe
```
  
Al ejecutar este comando se eliminará el usuario `jdoe` del sistema ***digna***, revocando su acceso y borrando sus datos y permisos asociados del repositorio.

## Uso del comando `modify-user`

El comando `modify-user` en la CLI de ***digna*** se utiliza para actualizar los detalles de un usuario existente en el sistema ***digna***.

### Uso del comando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentos
  
- **USER_NAME**: El nombre de usuario del usuario que se va a modificar (requerido).
- **USER_FULL_NAME**: El nuevo nombre completo del usuario (requerido).
  
### Opciones  
  
- `--is_superuser`, `-su`: Establece al usuario como superuser, otorgándole privilegios elevados. Este indicador no requiere un valor.  
- `--valid_until`, `-vu`: Establece una fecha de expiración para la cuenta del usuario en el formato YYYY-MM-DD HH:MI:SS. Si no se proporciona, la cuenta permanece válida indefinidamente.  
  
### Ejemplo
  
Para modificar el nombre completo del usuario `jdoe` a “Johnathan Doe” y establecer al usuario como superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Uso del comando `modify-user-pwd`
  
El comando `modify-user-pwd` en la CLI de ***digna*** se utiliza para cambiar la contraseña de un usuario existente en el sistema ***digna***.
  
### Uso del comando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentos
  
- **USER_NAME**: El nombre de usuario del usuario cuya contraseña se va a cambiar (requerido).
- **USER_PWD**: La nueva contraseña del usuario (requerido).
  
### Ejemplo
  
Para cambiar la contraseña del usuario `jdoe` a `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Uso del comando `list-users`

El comando `list-users` en la CLI de ***digna*** muestra una lista de todos los usuarios registrados en el sistema ***digna***.

### Uso del comando

```bash
dignacli list-users
```

Al ejecutar este comando, la CLI de ***digna*** se conectará al repositorio de ***digna*** y listará todos los usuarios, mostrando su ID, nombre de usuario, nombre completo, estado de superuser y marcas de tiempo de expiración.

# Gestión de repositorios

### Uso del comando `upgrade-repo`
  
El comando `upgrade-repo` en la CLI de ***digna*** se utiliza para actualizar o inicializar el repositorio de ***digna***. Este comando es esencial para aplicar actualizaciones o configurar la infraestructura del repositorio por primera vez.
  
### Uso del comando

```bash
dignacli upgrade-repo [options]
```
  
### Opciones
  
- `--simulation-mode`, `-s`: Cuando se habilita, esta opción ejecuta el comando en modo simulación, que imprime las sentencias SQL que se ejecutarían pero no las ejecuta realmente. Esto es útil para previsualizar cambios sin modificar el repositorio.  

  
### Ejemplo
  
Para actualizar el repositorio de ***digna***, puede ejecutar el comando sin opciones:
  
```bash
dignacli upgrade-repo
```  
Para ejecutar la actualización en modo simulación (para ver las sentencias SQL sin aplicarlas):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Este comando es crucial para mantener el sistema ***digna***, asegurando que el esquema de la base de datos y otros componentes del repositorio estén actualizados con la versión más reciente del software.

## Uso del comando `encrypt`
  
El comando `encrypt` en la CLI de ***digna*** se utiliza para cifrar una contraseña.
  
### Uso del comando
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentos
- **PASSWORD**: La contraseña que necesita ser cifrada (requerido).
  
### Ejemplo
  
Para cifrar una contraseña, debe proporcionar la contraseña como argumento.   
Por ejemplo, para cifrar la contraseña `mypassword123`, use:
```bash
dignacli encrypt mypassword123
```
Este comando devuelve la versión cifrada de la contraseña proporcionada, que luego puede usarse en contextos seguros. Si no se proporciona el argumento de contraseña, la CLI mostrará un error indicando el argumento faltante.

## Uso del comando `generate-key`
  
El comando `generate-key` se utiliza para generar una clave Fernet, que es esencial para proteger las contraseñas almacenadas en el repositorio de ***digna***.
  
### Uso del comando
```bash
dignacli generate-key
```
  
# Gestión de datos

## Uso del comando `clean-up`

El comando `clean-up` en la CLI de ***digna*** se utiliza para eliminar perfiles, predicciones y datos del sistema de semáforo (traffic light system) para una o más fuentes de datos dentro de un proyecto especificado. Este comando es esencial para la gestión del ciclo de vida de los datos, ayudando a mantener un entorno de datos organizado y eficiente al limpiar datos obsoletos o innecesarios.

### Uso del comando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto del cual se eliminarán los datos (requerido). Usar la palabra clave `all-projects` en este argumento indica a ***digna*** que itere sobre todos los proyectos existentes y aplique este comando.
- **FROM_DATE**: La fecha y hora de inicio para la eliminación de datos. Los formatos aceptables incluyen %Y-%m-%d, %Y-%m-%dT%H:%M:%S o %Y-%m-%d %H:%M:%S (requerido).
- **TO_DATE**: La fecha y hora de fin para la eliminación de datos, con los mismos formatos que FROM_DATE (requerido).
  
### Opciones
  
- `--table-name`, `-tn`: Limita la operación de limpieza a una tabla específica dentro del proyecto.
- `--table-filter`, `-tf`: Filtros para limitar la limpieza a tablas que contengan la subcadena especificada en sus nombres.
- `--timing`, `-tm`: Muestra la duración del proceso de limpieza al finalizar.
- `--help`: Muestra información de ayuda para el comando clean-up y sale.
  
### Ejemplo
  
Para eliminar datos del proyecto ProjectA entre el 1 de enero de 2023 y el 30 de junio de 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Para eliminar datos solo de una tabla específica llamada `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Este comando ayuda a gestionar el almacenamiento de datos y a garantizar que el repositorio solo contenga información relevante.

## Uso del comando `inspect`

El comando `inspect` en la CLI de ***digna*** se utiliza para crear perfiles, predicciones y datos del sistema de semáforo (traffic light system) para una o más fuentes de datos dentro de un proyecto especificado. Este comando ayuda a analizar y supervisar los datos durante un periodo definido.

### Uso del comando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto cuyo datos se van a inspeccionar (requerido). Usar la palabra clave `all-projects` en este argumento indica a ***digna*** que itere sobre todos los proyectos existentes y aplique este comando.
- **FROM_DATE**: La fecha y hora de inicio para la inspección de datos. Los formatos aceptables incluyen %Y-%m-%d, %Y-%m-%dT%H:%M:%S o %Y-%m-%d %H:%M:%S (requerido).
- **TO_DATE**: La fecha y hora de fin para la inspección de datos, con los mismos formatos que FROM_DATE (requerido).
  
### Opciones

- `--table-name`, `-tn`: Limita la inspección a una tabla específica dentro del proyecto.
- `--table-filter`, `-tf`: Filtra para inspeccionar solo tablas que contengan la subcadena especificada en sus nombres.
- `--do-profile`: Dispara la recolección de perfiles. El valor predeterminado es do-profile.
- `--no-do-profile`: Evita la recolección de perfiles.
- `--do-prediction`: Dispara el recálculo de predicciones. El valor predeterminado es do-prediction.
- `--no-do-prediction`: Evita el recálculo de predicciones.
- `--do-alert-status`: Dispara el recálculo de estados de alerta. El valor predeterminado es do-alert-status.
- `--no-do-alert-status`: Evita el recálculo de estados de alerta.
- `--timing`, `-tm`: Muestra la duración del proceso de inspección al finalizar.
  
### Ejemplo
  
Para inspeccionar datos del proyecto `ProjectA` desde el 1 de enero de 2024 hasta el 31 de enero de 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Para inspeccionar solo una tabla específica y forzar el recálculo de predicciones:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Este comando es útil para generar perfiles y predicciones actualizadas, supervisar la integridad de los datos y gestionar los sistemas de alerta dentro de un periodo de proyecto especificado.

## Uso del comando `tls-status`

El comando `tls-status` en la CLI de ***digna*** se utiliza para consultar el estado del Traffic Light System (TLS) para una tabla específica dentro de un proyecto en una fecha dada. El Traffic Light System proporciona información sobre la salud y la calidad de los datos, indicando posibles problemas o alertas que requieran atención.
  
### Uso del comando
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto para el cual se está consultando el estado TLS (requerido).
- **TABLE_NAME**: La tabla específica dentro del proyecto para la que se necesita el estado TLS (requerido).
- **DATE**: La fecha para la que se consulta el estado TLS, típicamente en el formato %Y-%m-%d (requerido).
  
### Ejemplo
  
Para comprobar el estado TLS de una tabla llamada UserData en el proyecto ProjectA el 1 de julio de 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Este comando ayuda a los usuarios a monitorizar y mantener la calidad de los datos proporcionando un informe claro y accionable basado en criterios predefinidos.

## Uso del comando `list-projects`
  
El comando `list-projects` en la CLI de ***digna*** se utiliza para mostrar una lista de todos los proyectos disponibles dentro del sistema ***digna***.
  
### Uso del comando
  
```bash
dignacli list-projects
```

Este comando es especialmente útil para administradores y usuarios que gestionan múltiples proyectos, proporcionando una vista rápida de los proyectos disponibles en el repositorio de ***digna***.

## Uso del comando `list-ds`

El comando `list-ds` en la CLI de ***digna*** se utiliza para mostrar una lista de todas las fuentes de datos disponibles dentro de un proyecto especificado. Este comando es útil para entender los activos de datos disponibles para análisis y gestión en el sistema ***digna***.

### Uso del comando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentos
- **PROJECT_NAME**: El nombre del proyecto cuyas fuentes de datos se van a listar (requerido).
  
### Ejemplo
  
Para listar todas las fuentes de datos en el proyecto llamado `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Este comando ofrece a los usuarios una visión general de las fuentes de datos disponibles en un proyecto, ayudándoles a navegar y gestionar el panorama de datos de forma más eficaz.
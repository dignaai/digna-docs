---
title: digna CLI Reference 2024.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.09. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.09
**2024-08-24**

---

## CLI Basics

---

###   help

La opción --help proporciona información sobre los comandos disponibles y su uso. Hay dos formas principales de usar esta opción:

1. **Mostrar ayuda general:**
   
    Use --help inmediatamente después de la palabra clave dignacli  
   bash
   dignacli --help

3.  **Obtener ayuda para comandos específicos:**  
  
    Para obtener información detallada sobre un comando específico, añada --help a ese comando.
    Por ejemplo, para obtener ayuda con el comando add-user, ejecute:
     bash
     dignacli add-user --help
     

     ### salida:
      
     - **Descripción del comando:** Ofrece una descripción detallada de lo que hace el comando.  
     - **Sintaxis:** Muestra la sintaxis exacta, incluidos los argumentos obligatorios y opcionales.  
     - **Opciones:** Enumera las opciones específicas del comando, junto con sus explicaciones.  
     - **Ejemplos:** Proporciona ejemplos de cómo ejecutar el comando de forma eficaz.

  
###   check-repo-connection

El comando check-repo-connection es una utilidad dentro de la herramienta digna CLI diseñada para probar la conectividad y el acceso a un repositorio especificado de digna. Este comando asegura que el CLI pueda interactuar con el repositorio.
      
##### Uso del comando
bash
dignacli check-repo-connection


Al ejecutarse correctamente, el comando muestra una confirmación de la conexión, junto con detalles sobre el repositorio: versión del repositorio, host, base de datos y esquema.  
  
Si la conexión al repositorio no tiene éxito, verifique el archivo config.toml para asegurarse de que la configuración sea correcta.

###   version

Para comprobar la versión instalada de dignacli, use la opción --version.  
  
#### Uso del comando
bash
dignacli --version

  
#### Ejemplo de salida
bash
dignacli version 2024.09


###   logging options
  
Por defecto, la salida en consola de los comandos de digna está diseñada para ser minimalista. La mayoría de los comandos ofrecen la posibilidad de proporcionar información adicional usando las siguientes opciones:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” y “debug” definen el nivel de detalle, mientras que el conmutador “logfile” permite redirigir la salida para que se envíe a un archivo en lugar de mostrarse en la consola.

## User Management

###   add-user
  
El comando add-user en el CLI de digna se utiliza para añadir un nuevo usuario al sistema de digna.
  
#### Uso del comando
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumentos

- **USER_NAME**: El nombre de usuario para el nuevo usuario (obligatorio).
- **USER_FULL_NAME**: El nombre completo del nuevo usuario (obligatorio).
- **USER_PASSWORD**: La contraseña para el nuevo usuario (obligatorio).

#### Opciones

- --is_superuser, -su: Indicador para designar al nuevo usuario como administrador.
- --valid_until, -vu: Establece una fecha de caducidad para la cuenta de usuario con el formato YYYY-MM-DD HH:MI:SS. Si no se establece, la cuenta no tiene fecha de caducidad.

#### Ejemplo

Para añadir un nuevo usuario con nombre de usuario jdoe, nombre completo John Doe y contraseña password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Para añadir un nuevo usuario y establecer una fecha de caducidad de la cuenta:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
El comando delete-user en el CLI de digna se utiliza para eliminar un usuario existente del sistema de digna.
  
##### Uso del comando
bash
dignacli delete-user USER_NAME

  
#### Argumentos
- **USER_NAME**: El nombre de usuario del usuario que será eliminado (obligatorio). Este es el único argumento requerido por el comando.

#### Ejemplo
bash
dignacli delete-user jdoe

  
Al ejecutar este comando se eliminará el usuario jdoe del sistema de digna, revocando su acceso y borrando sus datos y permisos asociados en el repositorio.

###   modify-user

El comando modify-user en el CLI de digna se utiliza para actualizar los detalles de un usuario existente en el sistema de digna.

##### Uso del comando
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumentos
  
- **USER_NAME**: El nombre de usuario del usuario que será modificado (obligatorio).
- **USER_FULL_NAME**: El nuevo nombre completo del usuario (obligatorio).
  
#### Opciones  
  
- --is_superuser, -su: Establece al usuario como superusuario, otorgándole privilegios elevados. Esta bandera no requiere un valor.  
- --valid_until, -vu: Establece una fecha de caducidad para la cuenta de usuario con el formato YYYY-MM-DD HH:MI:SS. Si no se proporciona, la cuenta permanece válida indefinidamente.  
  
#### Ejemplo
  
Para modificar el nombre completo del usuario jdoe a “Johnathan Doe” y establecer al usuario como superusuario:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
El comando modify-user-pwd en el CLI de digna se utiliza para cambiar la contraseña de un usuario existente en el sistema de digna.
  
##### Uso del comando
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumentos
  
- **USER_NAME**: El nombre de usuario del usuario cuya contraseña se va a cambiar (obligatorio).
- **USER_PWD**: La nueva contraseña del usuario (obligatorio).
  
#### Ejemplo
  
Para cambiar la contraseña del usuario jdoe a newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

El comando list-users en el CLI de digna muestra una lista de todos los usuarios registrados en el sistema de digna.

##### Uso del comando

bash
dignacli list-users


Al ejecutar este comando en el CLI de digna se conectará al repositorio de digna y listará todos los usuarios, mostrando su ID, nombre de usuario, nombre completo, estado de superusuario y marcas de tiempo de caducidad.

# Repository Management

###   upgrade-repo
  
El comando upgrade-repo en el CLI de digna se utiliza para actualizar o inicializar el repositorio de digna. Este comando es esencial para aplicar actualizaciones o configurar la infraestructura del repositorio por primera vez.
  
#### Uso del comando

bash
dignacli upgrade-repo [options]

  
#### Opciones
  
- --simulation-mode, -s: Cuando está habilitada, esta opción ejecuta el comando en modo simulación, que imprime las sentencias SQL que se ejecutarían pero no las ejecuta realmente. Esto es útil para previsualizar los cambios sin modificar el repositorio.  

  
#### Ejemplo
  
Para actualizar el repositorio de digna, puede ejecutar el comando sin opciones:
  
bash
dignacli upgrade-repo
  
Para ejecutar la actualización en modo simulación (para ver las sentencias SQL sin aplicarlas):
  
bash
dignacli upgrade-repo --simulation-mode

  
Este comando es crucial para mantener el sistema de digna, asegurando que el esquema de la base de datos y otros componentes del repositorio estén actualizados con la última versión del software.

###   encrypt
  
El comando encrypt en el CLI de digna se utiliza para encriptar una contraseña.
  
#### Uso del comando
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumentos
- **PASSWORD**: La contraseña que necesita ser encriptada (obligatorio).
  
#### Ejemplo
  
Para encriptar una contraseña, debe proporcionar la contraseña como argumento.   
Por ejemplo, para encriptar la contraseña mypassword123, usaría:
bash
dignacli encrypt mypassword123

Este comando muestra la versión encriptada de la contraseña proporcionada, que luego puede utilizarse en contextos seguros. Si no se proporciona el argumento de la contraseña, el CLI mostrará un error indicando el argumento faltante.

###   generate-key
  
El comando generate-key se utiliza para generar una clave Fernet, que es esencial para asegurar las contraseñas almacenadas en el repositorio de digna.
  
#### Uso del comando
bash
dignacli generate-key

  
## Data Management

###   clean-up

El comando clean-up en el CLI de digna se utiliza para eliminar perfiles, predicciones y datos del sistema de semáforos (Traffic Light System) para una o más fuentes de datos dentro de un proyecto especificado. Este comando es esencial para la gestión del ciclo de vida de los datos, ayudando a mantener un entorno de datos organizado y eficiente al limpiar datos obsoletos o innecesarios.

#### Uso del comando

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto del que se eliminarán los datos (obligatorio). Usar la palabra clave all-projects en este argumento instruye a digna para iterar sobre todos los proyectos existentes y aplicar este comando.
- **FROM_DATE**: La fecha y hora de inicio para la eliminación de datos. Los formatos aceptables incluyen %Y-%m-%d, %Y-%m-%dT%H:%M:%S o %Y-%m-%d %H:%M:%S (obligatorio).
- **TO_DATE**: La fecha y hora de fin para la eliminación de datos, siguiendo los mismos formatos que FROM_DATE (obligatorio).
  
#### Opciones
  
- --table-name, -tn: Limita la operación de limpieza a una tabla específica dentro del proyecto.
- --table-filter, -tf: Filtra para limitar la limpieza a tablas que contengan la subcadena especificada en sus nombres.
- --timing, -tm: Muestra la duración del proceso de limpieza al finalizar.
- --help: Muestra información de ayuda para el comando clean-up y sale.
  
#### Ejemplo
  
Para eliminar datos del proyecto ProjectA entre el 1 de enero de 2023 y el 30 de junio de 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Para eliminar datos solo de una tabla específica llamada Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Este comando ayuda a gestionar el almacenamiento de datos y a garantizar que el repositorio contenga únicamente información relevante.

###   inspect

El comando inspect en el CLI de digna se utiliza para crear perfiles, predicciones y datos del sistema de semáforos (Traffic Light System) para una o más fuentes de datos dentro de un proyecto especificado. Este comando ayuda a analizar y monitorear los datos durante un período definido.

#### Uso del comando

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto para el que se van a inspeccionar los datos (obligatorio). Usar la palabra clave all-projects en este argumento instruye a digna para iterar sobre todos los proyectos existentes y aplicar este comando.
- **FROM_DATE**: La fecha y hora de inicio para la inspección de datos. Los formatos aceptables incluyen %Y-%m-%d, %Y-%m-%dT%H:%M:%S o %Y-%m-%d %H:%M:%S (obligatorio).
- **TO_DATE**: La fecha y hora de fin para la inspección de datos, siguiendo los mismos formatos que FROM_DATE (obligatorio).
  
#### Opciones

- --table-name, -tn: Limita la inspección a una tabla específica dentro del proyecto.
- --table-filter, -tf: Filtra para inspeccionar solo tablas que contengan la subcadena especificada en sus nombres.
- --force-profile: Fuerza la recolección de perfiles. El valor predeterminado es force-profile.
- --no-force-profile: Impide la recolección de perfiles.
- --force-prediction: Fuerza el recálculo de predicciones. El valor predeterminado es force-prediction.
- --no-force-prediction: Impide el recálculo de predicciones.
- --force-alert-status: Fuerza el recálculo de los estados de alerta. El valor predeterminado es force-alert-status.
- --no-force-alert-status: Impide el recálculo de los estados de alerta.
- --timing, -tm: Muestra la duración del proceso de inspección al finalizar.
- --alert-notification, -an: Envía notificaciones de alerta a los canales suscritos.
  
#### Ejemplo
  
Para inspeccionar datos del proyecto ProjectA del 1 de enero de 2024 al 31 de enero de 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Para inspeccionar solo una tabla específica y forzar el recálculo de predicciones:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Este comando es útil para generar perfiles y predicciones actualizados, monitorear la integridad de los datos y gestionar los sistemas de alerta dentro de un período de tiempo especificado del proyecto.

###   tls-status

El comando tls-status en el CLI de digna se utiliza para consultar el estado del Traffic Light System (TLS) para una tabla específica dentro de un proyecto en una fecha dada. El Traffic Light System proporciona información sobre la salud y calidad de los datos, indicando posibles problemas o alertas que requieran atención.
  
#### Uso del comando
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumentos
  
- **PROJECT_NAME**: El nombre del proyecto para el cual se consulta el estado del TLS (obligatorio).
- **TABLE_NAME**: La tabla específica dentro del proyecto para la que se necesita el estado del TLS (obligatorio).
- **DATE**: La fecha para la cual se consulta el estado del TLS, normalmente en el formato %Y-%m-%d (obligatorio).
  
#### Ejemplo
  
Para comprobar el estado TLS de una tabla llamada UserData en el proyecto ProjectA el 1 de julio de 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Este comando ayuda a los usuarios a monitorear y mantener la calidad de los datos proporcionando un informe claro y accionable basado en criterios predefinidos.

###   list-projects
  
El comando list-projects en el CLI de digna se utiliza para mostrar una lista de todos los proyectos disponibles en el sistema de digna.
  
#### Uso del comando
  
bash
dignacli list-projects


Este comando es especialmente útil para administradores y usuarios que gestionan múltiples proyectos, proporcionando una visión rápida de los proyectos disponibles en el repositorio de digna.

###   list-ds

El comando list-ds en el CLI de digna se utiliza para mostrar una lista de todas las fuentes de datos disponibles dentro de un proyecto especificado. Este comando es útil para comprender los activos de datos disponibles para análisis y gestión en el sistema de digna.

#### Uso del comando
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumentos
- **PROJECT_NAME**: El nombre del proyecto para el cual se listan las fuentes de datos (obligatorio).
  
#### Ejemplo
  
Para listar todas las fuentes de datos en el proyecto llamado ProjectA:
  
bash
dignacli list-ds ProjectA

  
Este comando ofrece a los usuarios una visión general de las fuentes de datos disponibles en un proyecto, ayudándoles a navegar y gestionar el panorama de datos de manera más efectiva.
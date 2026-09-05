---
title: Conectar una base de datos | Documentación de digna
description: Guía paso a paso para conectar una base de datos a un proyecto existente en digna. Aprende a configurar conexiones, proporcionar credenciales y habilitar acceso seguro.
image: /assets/logo_square.png
---

# Conectar una base de datos

Esta guía muestra los pasos mínimos para agregar una conexión de base de datos a tu proyecto.

## Demostración interactiva

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="Connect a Database to a Project"
    frameborder="0"
    loading="lazy"
    webkitallowfullscreen
    mozallowfullscreen
    allowfullscreen
    allow="clipboard-write"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;">
  </iframe>
</div>
<!--ARCADE EMBED END-->

---

### Pasos

1. **Abre tu proyecto**  
   Desde la navegación lateral, haz clic en **Projects** y selecciona el proyecto objetivo.

2. **Agregar una conexión**  
   Ve a **Connections** y haz clic en **Add Connection**.

3. **Selecciona el tipo de base de datos**  
   Selecciona la base de datos que deseas conectar (p. ej., PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Introduce los detalles de la conexión**  
   Proporciona **Name**, **Host**, **Port**, **Database/Service** y **Credentials** (nombre de usuario/contraseña o SSO, según corresponda).

5. **Test & Save**  
   Haz clic en **Test**. Si tiene éxito, haz clic en **Save**. La conexión aparecerá en **Connections** del proyecto.
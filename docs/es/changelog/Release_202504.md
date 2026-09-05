---
title: digna Release 2025.04 | Inspection Hub, Soporte multilingüe, Module Analytics
description: Descubre las novedades de digna Release 2025.04. Esta versión introduce el Inspection Hub, soporte multilingüe (inglés, alemán, polaco), importación/exportación de fuentes de datos vía dignacli, la primera versión de Module Analytics y una experiencia de panel mejorada.
keywords: digna Release 2025.04, registro de cambios digna, digna Inspection Hub, digna soporte multilingüe, digna Module Analytics, digna import export, digna CLI, notas de la versión, observabilidad de datos, monitoreo de calidad de datos
image: /assets/logo_square.png
---

# Registro de cambios – Release 2025.04

Con el Release 2025.04, digna da un gran paso para facilitar la gestión de la calidad y la observabilidad de los datos, hacerla más transparente para los equipos y accesible a usuarios de todo el mundo.  
Esta versión combina **nuevas funcionalidades potentes**, **mejoras en la automatización de flujos de trabajo** y **ajustes en la experiencia de usuario**.  

---

## Nuevas funcionalidades

### Inspection Hub – Un nuevo centro de control
El **Inspection Hub** ya está disponible como el lugar central para gestionar todos tus trabajos de inspección. En lugar de saltar entre diferentes módulos o depender únicamente de la ejecución desde la línea de comandos, ahora puedes supervisar y controlar tus inspecciones desde una interfaz unificada.  

Principales capacidades:  
- Inspecciones bajo demanda: inicia nuevos trabajos al instante siempre que necesites resultados actualizados.  
- Historial de inspección: consulta una cronología de las inspecciones — qué se ejecutó, quién lo activó y cuándo.  
- Seguimiento de estado: los trabajos se marcan claramente como completados, en curso o pendientes.  
- Información del invocador: verifica rápidamente si una inspección fue activada por un usuario, el programador o la CLI.  
- Herramientas de limpieza: elimina trabajos obsoletos o innecesarios para mantener tu espacio de trabajo ordenado.  
- Registros detallados: profundiza en cada trabajo para ver cuánto tardó, qué fuentes se incluyeron y cómo se aplicaron los umbrales.  

El Inspection Hub ofrece a los equipos **visibilidad y control de extremo a extremo**, facilitando la gestión de inspecciones en proyectos de gran escala.  

---

### Soporte multilingüe – digna habla tu idioma
digna ya está preparada para equipos internacionales con la introducción del **soporte multilingüe**.  

En esta versión puedes configurar tu **idioma de interfaz preferido** directamente en Preferencias de usuario. Los idiomas compatibles incluyen:  
- Inglés (UK, US, CA, AU)  
- Alemán (DE, AT, CH)  
- Polaco (PL)  

Esto facilita el uso de digna en organizaciones multilingües y asegura una adopción más fluida entre equipos que trabajan en distintas regiones. Más idiomas se añadirán en futuras versiones.  

---

### Importación y exportación de fuentes de datos – Configuración simplificada
La coherencia entre entornos es esencial en despliegues empresariales. Con 2025.04, digna introduce la **importación/exportación de fuentes de datos** vía **dignacli**, la herramienta de línea de comandos para usuarios avanzados.  

Beneficios:  
- Exporta la configuración de una fuente de datos una vez y reutilízala en Desarrollo, Pruebas y Producción.  
- Elimina la reconfiguración manual y evita errores costosos.  
- Admite flujos de trabajo automatizados y pipelines CI/CD con comandos CLI sencillos (`export-ds` y `import-ds`).  
- Copia rápidamente fuentes de datos entre proyectos para facilitar la colaboración.  

Esta funcionalidad asegura que los equipos puedan desplegar con confianza, sabiendo que las configuraciones son coherentes en todos los entornos.  

---

### Module Analytics (v1) – De la detección a la comprensión
digna nació como una plataforma para la detección de anomalías y el monitoreo de la calidad de los datos. Con el Release 2025.04, evoluciona aún más con la **primera versión de Module Analytics**.  

Module Analytics ayuda a los usuarios a **entender sus datos** en lugar de solo reaccionar ante problemas. Con este nuevo módulo puedes:  
- Rastrear tendencias a largo plazo en tus conjuntos de datos.  
- Detectar y monitorizar la volatilidad para comprender las fluctuaciones.  
- Explorar el comportamiento de los datos a lo largo del tiempo para obtener un contexto más profundo.  

Por ejemplo, digna puede resaltar automáticamente que *"El recuento de filas aumentó un 15,8% desde el inicio del año."*  
Sin consultas SQL, sin comprobaciones manuales — solo **insights accionables de un vistazo**.  

Esto es la base del recorrido de digna hacia análisis de datos avanzados, permitiendo a los equipos de datos pasar de una monitorización reactiva a una proactiva.  

---

### Mejoras en el panel – Una experiencia de usuario más fluida
Más allá de las funcionalidades principales, el Release 2025.04 incluye varias **refinaciones en el panel** diseñadas para hacer digna más intuitiva y agradable:  
- Navegación más rápida entre proyectos e inspecciones.  
- Un diseño más limpio para los registros de inspección y las envíos de trabajos.  
- Ajustes de diseño sutiles que te ayudan a encontrar insights más rápido.  

Estas mejoras se basan directamente en el feedback de clientes y demuestran nuestro compromiso continuo con hacer de digna **una plataforma pensada para el uso diario**.  

---

## Mejoras generales
- Optimizaciones de rendimiento para trabajos de inspección en conjuntos de datos grandes.  
- Mejor manejo de errores en dignacli para proporcionar retroalimentación más clara.  
- Mejoras de estabilidad para proyectos con muchos trabajos simultáneos.  
- Ajustes en la interfaz de usuario para el filtrado de registros de trabajos y la gestión de proyectos.  

---

## Resumen
El Release 2025.04 trata sobre **control, accesibilidad y conocimiento**.  

- El nuevo **Inspection Hub** ofrece a los usuarios visibilidad completa de los trabajos de inspección.  
- El **soporte multilingüe** garantiza que digna pueda utilizarse en equipos globales.  
- La funcionalidad de **importación/exportación** simplifica la gestión de configuración entre entornos.  
- **Module Analytics (v1)** cambia el enfoque de la detección a la comprensión, con seguimiento de tendencias y volatilidad.  
- Las **mejoras en el panel** refinan la experiencia de usuario en general.  

En conjunto, estas actualizaciones hacen que digna sea más potente, fácil de usar y lista para un uso internacional como nunca antes.
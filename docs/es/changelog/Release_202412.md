---
title: digna Release 2024.12 | Registro de cambios y nuevas funciones
description: Descubre las novedades de digna Release 2024.12. Esta versión introduce un programador integrado, informes en PDF, columnas personalizadas flexibles, marcadores dinámicos en consultas snapshot y una optimización más inteligente de umbrales para mejorar la detección de anomalías y la monitorización de la calidad de los datos.
keywords: digna Release 2024.12, digna changelog, notas de la versión, programador integrado, informes PDF, tipo de columna CUSTOM, marcadores en consultas snapshot, optimización de umbrales, observabilidad de datos, monitorización de la calidad de datos, detección de anomalías
image: /assets/logo_square.png
---



# Registro de cambios – Release 2024.12

La versión 2024.12 ofrece un conjunto de nuevas funciones y mejoras que hacen que digna sea más automatizada, flexible y lista para el negocio.  
Esta versión mejora la programación, los informes, el manejo de consultas y la precisión en la detección de anomalías.  

---

## Nuevas funciones

### Programador integrado
Las inspecciones ya no dependen únicamente de la línea de comandos o de llamadas a la API.  
Con el **nuevo digna Scheduler**, las inspecciones pueden ejecutarse automáticamente en horarios definidos.  

- Soporta **expresiones Cron** para programaciones recurrentes (diarias, semanales o intervalos personalizados).  
- Ofrece control preciso mediante **desplazamientos (offsets)**, **fechas de inicio** y **fechas de fin**.  
- Permite a los equipos asegurarse de que todas las fuentes de datos críticas se inspeccionen de forma consistente y sin intervención manual.  

---

### Informes en formato PDF
Los equipos ahora pueden compartir fácilmente los resultados con las partes interesadas mediante **exportaciones en PDF**.  

- Los gráficos, métricas y resultados de anomalías se pueden exportar en un formato PDF profesional.  
- Los informes combinan **visualizaciones** y **datos subyacentes** para servir tanto a usuarios técnicos como de negocio.  
- Elimina la necesidad de herramientas externas para la creación de informes.  

---

### Nuevo tipo de columna: `CUSTOM`
Para ofrecer más flexibilidad, digna introduce un nuevo **tipo de columna `CUSTOM`**.  

- Los usuarios pueden definir exactamente qué **estadísticas y métricas** se aplican a atributos específicos.  
- Perfecto para casos especiales que no encajan en categorías estándar como NUMERICAL o CATEGORICAL.  
- Ayuda a mantener los análisis enfocados y los resultados relevantes para el contexto del negocio.  

---

### Nuevos marcadores en consultas snapshot
Las consultas snapshot son ahora más simples y menos propensas a errores gracias a **marcadores dinámicos**.  

- Tokens como `#date+n#` o `#date-n#` ajustan automáticamente las fechas en las consultas.  
- Ejemplo:  
  - `#date+1#` → mañana  
  - `#date-2#` → hace dos días  
- Elimina los cálculos manuales de fechas y asegura coherencia entre los equipos.  

---

### Optimización de umbrales
Los umbrales de anomalía son ahora más inteligentes y conscientes del contexto.  

- Para métricas como **NULL COUNT**, los umbrales inferiores se limitan automáticamente a **0**.  
- Evita umbrales inválidos o sin sentido.  
- Resulta en menos falsos positivos y una detección de anomalías más fiable.  

---

## Mejoras generales
- Componentes de **UI** refinados en las vistas de configuración de proyectos y atributos.  
- Mejor rendimiento del **dashboard** para volúmenes de datos grandes.  
- Mejora en el **registro (logging) y mensajes de error** para facilitar la solución de problemas.  

---

## Resumen
La Release 2024.12 refuerza a digna como una plataforma para la **calidad de datos, detección de anomalías y observabilidad**.  
Con automatización mediante programación, informes PDF compartibles, columnas personalizables, consultas snapshot simplificadas y umbrales más inteligentes, digna se vuelve aún más valiosa tanto para usuarios técnicos como para stakeholders de negocio.
---
title: digna Versión 2026.01 | Datasources lógicos, Conexiones globales y Avanzada Data Validation
description: Conoce las novedades de digna Versión 2026.01. Esta versión introduce conexiones de base de datos globales, datasources lógicos, condiciones de relevancia de anomalías, exportaciones CSV y validación de datos avanzada incluyendo comprobaciones de integridad referencial.
keywords: digna Versión 2026.01, digna changelog, digna datasource, digna database connections, digna Data Anomalies, digna Data Validation, referential integrity validation, reglas de calidad de datos, data observability, digna CSV export
image: /assets/logo_square.png
---

# Changelog – Release 2026.01  

Con la Versión 2026.01, digna introduce mejoras importantes en el modelado de datasource, la gestión de conexiones y la usabilidad de las inspecciones.  
Esta versión aumenta la flexibilidad en todos los módulos y amplía significativamente la **cobertura de calidad y validación de datos**.

---

## 🚀 Nuevas funciones  

### Conexiones de base de datos globales  
- Las conexiones de base de datos ahora se configuran a nivel **global**.  
- Las conexiones globales pueden reutilizarse en **todos los proyectos**, simplificando la configuración y el mantenimiento.  
- **Impacto:** Reduce la sobrecarga operativa y garantiza conectividad consistente entre entornos.

### Múltiples conexiones de origen por proyecto  
- Los proyectos ahora pueden referenciar **múltiples configuraciones de conexión de origen**.  
- Permite configuraciones más flexibles para paisajes de datos complejos por proyecto.  
- **Impacto:** Soporta arquitecturas empresariales realistas con fuentes de datos heterogéneas.

### Datasources lógicos  
- Los datasources ahora representan una **capa lógica** dentro de un proyecto.  
- Cada datasource puede estar respaldado por:
    - una **tabla de base de datos**
    - una **vista de base de datos**
    - una **sentencia SQL personalizada**  
- Esta separación mejora la reutilización, la claridad y el modelado de inspecciones en los distintos módulos.  
- **Impacto:** Desacopla las inspecciones y reglas de calidad de datos del almacenamiento físico, mejorando la mantenibilidad y la reutilización.

### Condición de relevancia de anomalías  
- Ahora se puede definir una **Condición de Relevancia de Anomalías** para controlar la evaluación del estado de anomalía a nivel de dataset.  
- Las estadísticas se calculan independientemente de si la condición está definida o se cumple.  
- Si la condición **no se cumple**, **digna Data Anomalies** no proporciona estado de anomalía (green / yellow / red).  
- **Ejemplo:** Excluir el dataset de la evaluación de anomalías cuando el conteo de registros sea inferior a 10.  
- **Impacto:** Asegura que las anomalías se evalúen solo en contextos de negocio relevantes.

### Configuración de notificaciones por módulo  
- Las notificaciones ahora se pueden configurar **por módulo** directamente en digna.  
- Permite el control independiente del comportamiento de alertas para **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** y otros módulos.  
- **Impacto:** Habilita estrategias de alertado precisas alineadas con las responsabilidades de los equipos y la criticidad.

### Exportación de resultados de inspección (CSV)  
- Los usuarios ahora pueden **descargar los resultados de inspección como archivos CSV**.  
- Facilita el análisis offline, la elaboración de informes y la integración con herramientas externas.  
- **Impacto:** Simplifica auditorías, reporting y el análisis de calidad de datos aguas abajo.

---

## 🧪 Capacidades ampliadas de validación de datos  

Con esta versión, **digna Data Validation** ahora soporta un conjunto completo de reglas de calidad de datos:

- **Reglas de validación a nivel de fila**  
- **Comprobaciones de unicidad multi-columna**  
- **Validación de integridad referencial entre datasources**

En conjunto, estas comprobaciones permiten aplicar **reglas estructurales y relacionales de calidad de datos** en paisajes de datos complejos.

### Comprobaciones de unicidad para múltiples columnas
- Se introducen **Comprobaciones de Unicidad** para un **conjunto configurable de columnas**.  
- Permite validar claves compuestas y restricciones de unicidad a nivel de negocio.  
- **Impacto:** Detecta entidades de negocio duplicadas que no pueden identificarse con comprobaciones de una sola columna.

### Comprobaciones de integridad referencial
- Se introducen **Comprobaciones de Integridad Referencial** para validar relaciones entre datasources.  
- Asegura que los **valores de claves foráneas** en un datasource origen existan en un datasource destino referenciado.  
- Ayuda a detectar registros huérfanos, relaciones rotas y problemas de consistencia de datos de forma temprana.  
- Diseñado para funcionar con **datasources lógicos**, incluidas vistas y SQL personalizado.  
- **Casos de uso:** integridad de data warehouse, reporting regulatorio, consistencia de datos maestros y analítica confiable aguas abajo.

---

## 🎯 Quién se beneficia de esta versión  

- **Ingenieros de datos:** Modelado de datasource más flexible y conexiones de base de datos reutilizables  
- **Equipos de Calidad de Datos y Gobierno:** Cobertura de validación ampliada, incluidas reglas de integridad relacional  
- **Equipos de Analytics y BI:** Entradas más limpias y resultados de inspección exportables  
- **Responsables de plataforma:** Complejidad de configuración reducida y mejor mantenibilidad operativa

---

## 🛠 Actualizaciones de la CLI  
- Sin cambios

---
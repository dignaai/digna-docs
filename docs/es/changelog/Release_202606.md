---
title: digna Versión 2026.06 | SDK de Python, despliegue con Docker y gestión de validaciones mejorada
description: Descubre las novedades de digna Versión 2026.06. Esta versión presenta el nuevo **SDK de Python de digna**, soporte oficial de **despliegue con Docker**, una experiencia de dashboard renovada y capacidades ampliadas de importación/exportación para reglas de validación.
keywords: digna Versión 2026.06, SDK de Python digna, soporte Docker digna, automatización de calidad de datos, perfilado de datos, importación exportación de reglas de validación, dashboard digna, plataforma de observabilidad de datos, API de Python, automatización de metadatos
image: /assets/logo_square.png
---

# Changelog – Versión 2026.06  

Con la Versión 2026.06, digna da un gran paso adelante en automatización, extensibilidad y usabilidad de la plataforma.  
Esta versión introduce el nuevo **SDK de Python de digna**, soporte oficial de **despliegue con Docker**, una experiencia de dashboard renovada y mayor portabilidad para la gestión de reglas de validación.

---

## Nuevas características  

### digna Python SDK – Automatiza todo con Python  
- Instalar mediante:
  ```bash
  pip install digna-sdk
  ```
- Gestiona y automatiza digna programáticamente usando Python  
- Crea y configura proyectos mediante código  
- Dispara inspecciones y ejecuciones de monitoreo  
- Gestiona datasets, reglas y configuraciones de forma programática  
- Perfila tablas y extrae insights de metadata  
- Exporta resultados de perfilado y calidad de datos a repositorios y sistemas externos  
- Integra con notebooks, herramientas de orquestación y pipelines de CI/CD  

**Impacto:** Habilita infraestructura como código (infrastructure-as-code) y una profunda automatización de flujos de trabajo de calidad y observabilidad de datos usando Python.

---

### Soporte Docker – Despliegue y operaciones simplificadas  
- Imagen oficial de Docker para digna  
- Configuración rápida y consistente entre entornos  
- Incorporación simplificada para desarrollo, pruebas y producción  
- Integración fácil con Kubernetes y plataformas de contenedores  
- Mejor portabilidad y reproducibilidad de despliegues  

**Impacto:** Facilita el despliegue y la operación de digna en arquitecturas cloud-native modernas.

---

### QueryMode – Estrategia flexible de ejecución SQL

Configura la estrategia de ejecución de consultas: modo **Single** o **Combined**

**Single Mode**: Cada estadística se calcula con una consulta SQL dedicada

  - Ideal para fuentes de datos grandes donde la memoria es limitada
  - Evita la agotación de recursos en consultas combinadas (out of memory, límites de spool)
  - Mayor número de consultas pero menor uso de memoria por consulta

**Combined Mode**: Todas las estadísticas se calculan dentro de una única consulta SQL

  - Reduce el número total de consultas y la sobrecarga de red
  - Optimiza el rendimiento cuando las fuentes de datos son manejables en memoria
  - Más eficiente para ejecuciones frecuentes y en paralelo

**Impacto:** Permite a los usuarios controlar con detalle la ejecución de consultas para equilibrar rendimiento, uso de recursos y seguridad de memoria según las características de su fuente de datos.

---

### Experiencia de Dashboard rediseñada  
- Diseño UI/UX modernizado y mejorado  
- Navegación y estructura más clara  
- Mejor visibilidad de resultados de monitoreo e insights de calidad de datos  
- Mayor legibilidad de alertas, estadísticas y paneles  
- Acceso más rápido a la información operacional clave  

**Impacto:** Mejora la usabilidad y la productividad diaria de todos los usuarios.

---

### Importación y exportación ampliada para reglas de validación  
- Funcionalidad mejorada de importación/exportación para reglas de validación  
- Migración más sencilla entre entornos y proyectos  
- Mayor reutilización de conjuntos de reglas estandarizados  
- Mejor gobernanza y gestión del ciclo de vida de las reglas  
- Colaboración simplificada entre equipos  

**Impacto:** Permite una gobernanza de calidad de datos escalable y consistente en toda la organización.

---

## Mejoras en la plataforma  

- Integración completa del SDK de Python para automatización  
- Despliegue en contenedores vía Docker  
- UX mejorada a través del dashboard rediseñado  
- Mayor portabilidad de la lógica de validación  

---

## Beneficiarios de esta versión  

- Data Engineers: automatización, uso del SDK, integración en pipelines  
- Platform Teams: despliegue simplificado vía Docker  
- Data Governance Teams: gestión reutilizable de reglas de validación  
- Analytics Teams: mejor usabilidad y visibilidad de insights  

---

## Actualizaciones del CLI  
- Añadido soporte de integración con el SDK  
- Flujo de trabajo de import/export mejorado  
- Mejoras generales de estabilidad y rendimiento
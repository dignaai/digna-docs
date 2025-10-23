---
title: Data Schema Tracker – Monitorear la evolución del esquema | Documentación de digna
description: Aprende cómo digna Data Schema Tracker supervisa cambios en columnas, actualizaciones de tipos de datos y deriva del esquema. Recibe alertas por cambios intencionales y no intencionales para prevenir fallos en ETL y errores en dashboards.
---

# Data Schema Tracker – Monitorear la evolución del esquema

## Propósito
Rastrear y alertar sobre la evolución del esquema.

## Características técnicas
- Supervisa:
  - Columnas añadidas o eliminadas
  - Cambios en los tipos de datos
- Envía alertas ante cambios de esquema, tanto intencionales como no intencionales  
- Previene la **deriva silenciosa del esquema** que puede romper pipelines ETL o dashboards  

## Ejemplos de uso
- Identificar cambios de tipo de dato (por ejemplo, `INT` → `VARCHAR`) que pueden causar errores aguas abajo  
- Alertar a los ingenieros de datos antes de que los pipelines fallen debido a desajustes en el esquema  

## Valor
Mantiene a los equipos en control de **conjuntos de datos que evolucionan rápidamente**.
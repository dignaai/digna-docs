---
title: Data Validation – Comprobaciones basadas en reglas para cumplimiento y auditabilidad | Documentación de digna
description: Descubra cómo digna Data Validation aplica comprobaciones deterministas basadas en reglas con umbrales, rangos y listas de referencia. Asegure cumplimiento, auditabilidad e informes regulatorios en finanzas, salud y otras industrias sensibles a los datos.
image: /assets/logo_square.png
keywords:
  - Data Validation
  - comprobaciones de datos basadas en reglas
  - calidad de datos
  - calidad de la información
  - observabilidad de datos
  - umbrales y rangos
  - validación con listas de referencia
  - auditabilidad
  - monitorización del cumplimiento
  - digna Data Validation
lang: es
robots: index, follow
og_title: Data Validation – Comprobaciones basadas en reglas para cumplimiento y auditabilidad | Documentación de digna
og_description: digna Data Validation aplica comprobaciones deterministas basadas en reglas con umbrales, rangos y listas de referencia. Diseñado para industrias reguladas, garantiza cumplimiento, transparencia y auditabilidad.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Rule-Based Checks
<h1 style="display:none;">Módulo impulsado por IA Data Validation para la calidad y la observabilidad de los datos – digna</h1>

---

## Propósito

El **Data Validation** module garantiza la **calidad de los datos** mediante comprobaciones precisas basadas en reglas.  
Permite a las organizaciones definir lógica de validación determinista, tanto de negocio como técnica, asegurando que los datos cumplan con estándares de cumplimiento, SLA contractuales y requisitos regulatorios.

Al combinar la *ejecución de reglas dentro de la base de datos*, *trazabilidad completa de auditoría* e *integración con otros módulos de digna*, **Data Validation** garantiza una **calidad y observabilidad de los datos** consistente y rastreable en entornos empresariales complejos.

---

## Descripción técnica

### Tipos de validación compatibles

- **Comprobaciones de igualdad**  
  Confirman que los valores coinciden con los resultados esperados (p. ej., códigos de referencia, banderas booleanas, mapeos categóricos).

- **Umbrales y rangos**  
  Validan medidas numéricas o KPI frente a límites definidos — estáticos o derivados dinámicamente.

- **Listas de referencia y búsquedas**  
  Verifican si los valores de campo existen dentro de conjuntos maestros aprobados (p. ej., códigos de IVA, listas ISO de países, catálogos de productos).

- **Consistencia entre columnas**  
  Aseguran la corrección relacional (p. ej., la moneda corresponde a la región, la categoría de riesgo coincide con el tipo de activo).

- **Reglas de manejo de nulos**  
  Detectan valores nulos o vacíos inesperados en columnas críticas.

### Ejecución y registro

- **Procesamiento en la base de datos** – Todas las reglas de validación se ejecutan directamente en su base de datos (Teradata, Snowflake, Databricks, PostgreSQL, etc.).  
- **Sin extracción de datos** – digna nunca transfiere datos crudos fuera de su entorno.  
- **Trazabilidad completa** – Cada resultado de regla se registra con sello temporal, dataset responsable, recuentos de registros y resultados de aprobado/fallado.  
- **Auditoría**
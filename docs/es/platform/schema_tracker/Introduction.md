---
title: Data Schema Tracker – Monitorización de la evolución del esquema | Documentación de digna
description: Aprende cómo digna Data Schema Tracker supervisa los cambios en columnas, actualizaciones de tipos de datos y la deriva de esquemas. Detecta y alerta sobre cambios de esquema intencionados o no intencionados para prevenir fallos de ETL, dashboards rotos y pérdida de observabilidad de datos.
canonical_url: https://docs.digna.ai/platform/data_schema_tracker/
image: /assets/logo_square.png
keywords:
  - data schema tracker
  - detección de deriva de esquema
  - monitorización de la evolución del esquema
  - observabilidad de metadatos
  - observabilidad de datos
  - calidad de los datos
  - monitorización de la estructura de datos
  - metadatos de la base de datos
  - estabilidad de pipelines ETL
  - digna data schema tracker
lang: es
robots: index, follow
og_title: Data Schema Tracker – Monitorización de la evolución del esquema | Documentación de digna
og_description: digna Data Schema Tracker supervisa la deriva de esquemas, cambios de tipos de datos y actualizaciones de columnas. Recibe alertas antes de que las pipelines ETL o los dashboards fallen por cambios de estructura inesperados.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Monitorización de la evolución del esquema
<h1 style="display:none;">Módulo impulsado por IA para la observabilidad de metadatos y la calidad de datos – digna Data Schema Tracker</h1>

---

## Propósito

El **Data Schema Tracker** te mantiene informado sobre cómo evolucionan las estructuras de tu base de datos.  
Supervisa continuamente **esquemas de tablas, columnas y tipos de datos** para detectar la **deriva de esquemas (schema drift)** — cambios estructurales intencionados o no que pueden interrumpir pipelines, trabajos ETL o dashboards de BI.

Al garantizar transparencia en la evolución del esquema, digna ayuda a las organizaciones a mantener la **confianza en la calidad de los datos**, sostener la **observabilidad de los sistemas de datos** y evitar incidentes de producción costosos provocados por cambios de esquema no detectados.

---

## Descripción técnica

### Qué supervisa

- **Columnas añadidas o eliminadas** – Detecta columnas recién introducidas, renombradas o eliminadas.  
- **Modificaciones de tipo de dato** – Identifica cambios como `INT → VARCHAR` o `DATE → TIMESTAMP`.  
- **Modificaciones de tablas y vistas** – Rastrea la creación, el renombrado o la eliminación de tablas y vistas.  
- **Diferencias entre entornos** – Compara versiones de esquema entre los entornos Dev, Test y Production.  

### Detección y alertas

- Escanea **metadatos de la base de datos** o **catálogos del sistema** directamente dentro de tu plataforma de datos.  
- Compara cada instantánea de esquema con la versión previamente conocida almacenada en el esquema de observabilidad de digna.  
- Genera **alertas en tiempo real** en el dashboard, vía API o a través de canales de notificación externos (email, Slack, webhook).  
- Registra cada versión de esquema para **seguimiento histórico y preparación para auditorías**.

---

## Arquitectura y ejecución

- **Ejecución dentro de la base de datos:** digna se ejecuta completamente dentro de tu entorno, consultando vistas de metadatos sin extraer ningún dato.  
- **Escaneo ligero:** accede solo a información estructural — nunca a datos de usuarios.  
- **Almacenamiento centralizado:** los metadatos de esquema y los registros de deriva se almacenan en el esquema de observabilidad de digna para visualización y análisis.  
- **Automatización:** soporta escaneos programados o basados en eventos mediante digna Core o herramientas de orquestación externas.  

---

## Ejemplos de casos de uso

| Caso de uso | Descripción |
|-----------|--------------|
| **Monitoreo de estabilidad de ETL** | Detecta cambios en la estructura upstream antes de que las pipelines fallen por incompatibilidades de esquema. |
| **Confiabilidad de Business Intelligence** | Evita dashboards rotos causados por columnas renombradas o ausentes. |
| **Gobernanza del Data Warehouse** | Mantén un historial auditable de la evolución del esquema para cumplimiento y análisis de impacto. |
| **Supervisión de integraciones** | Asegura que los esquemas del data lake y del warehouse permanezcan sincronizados tras actualizaciones estructurales. |

---

## Beneficios

| Área | Beneficio |
|------|----------|
| **Calidad de los datos** | Evita la deriva de esquema no detectada que puede corromper o invalidar pipelines de datos. |
| **Observabilidad** | Añade monitorización estructural a la observabilidad general de los ecosistemas de datos. |
| **Cumplimiento** | Mantiene un historial versionado de esquemas para auditoría, trazabilidad y control de cambios. |
| **Prevención** | Detecta problemas estructurales antes de que se conviertan en errores de reporting o de producción. |

---

## Cómo funciona

1. **Captura de instantáneas** – digna captura los metadatos del esquema actual.  
2. **Comparación** – la nueva instantánea se compara
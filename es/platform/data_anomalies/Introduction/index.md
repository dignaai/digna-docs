# Data Anomalies – Automated Detection
<h1 style="display:none;">Módulo impulsado por IA para calidad y observabilidad de datos – digna Data Anomalies</h1>

---

## Purpose

El módulo **Data Anomalies** identifica irregularidades en tus conjuntos de datos de forma automática — sin necesidad de escribir reglas.  
Monitorea continuamente **la calidad en la entrega de datos**, aprendiendo cómo es el comportamiento “normal” y detectando desviaciones en tiempo real.

Mediante detección basada en IA, digna reconoce *errores silenciosos en los datos* como registros faltantes, duplicados o corruptos que pueden distorsionar informes, modelos ML y dashboards.

---

## Technical Overview

### Metrics analyzed

digna realiza un perfilado continuo de los siguientes aspectos de tus datos:

- **Volumen de registros** – número total de filas, diario o por lotes  
- **Valores faltantes** – detección de campos nulos o vacíos  
- **Distribuciones e histogramas** – monitorización de cambios en la forma de los datos  
- **Rangos de valores** – identificación automática de valores fuera de rango o extremos  
- **Unicidad** – comprobaciones de claves duplicadas o entradas repetidas  

### Intelligent anomaly detection

- Utiliza **aprendizaje histórico** para definir dinámicamente los límites esperados  
- Detecta desviaciones en **volumen, distribuciones de valores o relaciones lógicas**  
- Emplea IA para adaptar los umbrales automáticamente en función de la hora del día o patrones estacionales  
- Distingue entre **fluctuaciones estadísticas** y anomalías reales  
- Genera métricas detalladas y puntuaciones de confianza por conjunto de datos y por columna  

---

## Detection Scenarios

A continuación, ejemplos de problemas reales detectados automáticamente por el módulo **Data Anomalies**:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | Falta la mitad de las transacciones diarias, cargas de lotes duplicadas o picos súbitos de datos |
| **Missing or null values** | Extracciones de datos completadas pero columnas críticas quedan vacías |
| **Distribution drifts** | El importe medio de compra o el número de transacciones por región cambia inesperadamente |
| **Column swaps** | Columnas como *first_name* y *last_name* intercambiadas accidentalmente durante el ETL |
| **Unexpected categorical values** | p. ej., “Zurich” aparece en la lista de ciudades austríacas |
| **Sudden uniqueness loss** | IDs que antes eran únicos empiezan a duplicarse por errores de joins aguas arriba |

---

## Architecture and Execution

- **In-database execution:** Toda la lógica de detección de anomalías se ejecuta *dentro del motor de base de datos* (Teradata, Snowflake, Databricks, PostgreSQL, etc.)  
- **No data movement:** digna lee solo métricas, nunca transfiere datos raw externamente  
- **Incremental updates:** Solo se analizan los segmentos de datos nuevos en cada ejecución para mayor eficiencia  
- **Configurable inspection frequency:** Horaria, diaria o desencadenada por procesos aguas arriba  
- **Result storage:** Las métricas y las banderas de anomalía se escriben de nuevo en el esquema de observabilidad de digna para visualización y alertas  

---

## Benefits

| Area | Benefit |
|------|----------|
| **Automation** | Elimina cientos de definiciones manuales en SQL o reglas |
| **Precision** | Detecta problemas que los umbrales estáticos suelen pasar por alto |
| **Scalability** | Monitoriza millones de registros por tabla de forma eficiente |
| **Integration** | Funciona sin fricciones con *digna Data Analytics* para análisis de tendencias |
| **Compliance** | Garantiza control continuo sobre la **calidad y la observabilidad de los datos** |
| **Transparency** | Proporciona puntuaciones de confianza, sellos de tiempo y códigos de motivo para cada anomalía |

---

## How digna Learns “Normal”

1. **Profiling phase:** digna recopila métricas de conjuntos de datos históricos.  
2. **Learning phase:** los modelos de IA identifican patrones recurrentes (estacionales, semanales, diarios).  
3. **Monitoring phase:** los conjuntos de datos futuros se comparan con umbrales aprendidos dinámicamente.  
4. **Alerting phase:** las desviaciones que exceden los límites de confianza estadística se elevan como anomalías.  

Todos los modelos son explicables, deterministas y están optimizados para volúmenes de datos empresariales.

---

## Example Use Cases

- Monitorización de la calidad de datos en **sistemas de transacciones bancarias**  
- Detección de fallos de carga en **trabajos ETL o data warehouse**  
- Identificación de actividad anómala de clientes en **registros de telecomunicaciones**  
- Observación de la consistencia de datos clínicos en **canalizaciones de análisis sanitario**  
- Prevención de dashboards rotos en **entornos de BI y reporting**

---

## Frequently Asked Questions

**Does Data Anomalies require predefined rules?**  
No — el módulo aprende automáticamente del comportamiento de los datos.

**Can I still define specific thresholds if needed?**  
Sí. digna permite combinar detección basada en IA y basada en reglas (vía *Data Validation*).

**How are false positives minimized?**  
El módulo utiliza aprendizaje adaptativo y puntuación de confianza estadística para ignorar variaciones estacionales normales.

**Where does computation happen?**  
Todo el procesamiento se ejecuta dentro de tu base de datos — digna nunca extrae datos raw.

**Is it suitable for sensitive or regulated data?**  
Sí. digna se ejecuta completamente **on-premises o en nube privada** y cumple con los estándares de cumplimiento europeos.

---
# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">Módulo Data Timeliness impulsado por IA para Calidad de Datos y Observabilidad – digna</h1>

---

## Propósito

El **módulo Data Timeliness** asegura que **los datos lleguen a tiempo** - siempre.  
Monitorea continuamente los horarios de entrega y detecta automáticamente cuando conjuntos de datos, tablas o archivos están **retrasados, faltantes o incompletos**.  

Al combinar el aprendizaje por IA con horarios definidos por el usuario, *digna* permite a las organizaciones prevenir errores en etapas posteriores y mantener estrictos objetivos de **SLA (Acuerdo de Nivel de Servicio)** tanto para la **Calidad de Datos** como para la **observabilidad de las canalizaciones de datos**.

---

## Visión técnica

### Modos de monitoreo dual
- **Patrones de llegada aprendidos por IA**  
  digna aprende automáticamente el ritmo natural de tus entregas de datos — diario, por horas o impulsado por eventos — analizando marcas de tiempo históricas y tiempos de finalización.  
  Se adapta a cambios en calendarios comerciales, fines de semana o picos de fin de mes.

- **Horarios definidos por el usuario**  
  Los usuarios pueden definir explícitamente los tiempos de entrega esperados (p. ej., *cada día laborable antes de las 7:30 AM*).  
  digna compara la hora de llegada real con el horario planificado y genera alertas cuando los datos están tardíos o faltan.

### Mecanismo de detección
- Evalúa **marcas de tiempo de metadatos**, **conteos de registros** y **frescura de tablas**  
- Detecta **trabajos ETL detenidos**, **extracciones fallidas** y **llegadas parciales de archivos**  
- Se integra con *Data Anomalies* y *Data Validation* para obtener insights combinados

---

## Escenarios de detección

| Scenario | Description |
|-----------|--------------|
| **Late data arrival** | Feed diario de datos de mercado retrasado por dos horas, provocando que los informes no cumplan los SLA |
| **Missing load** | Una tabla o partición programada no se actualiza para la fecha actual |
| **Chained dependency delay** | El retraso de un job upstream impacta la actualización del pipeline downstream |
| **Weekend pattern shift** | El modelo de IA se adapta automáticamente cuando no se esperan datos los domingos |

---

## Arquitectura y ejecución

- **Ejecución en la base de datos:** digna ejecuta las comprobaciones de puntualidad directamente dentro de tu base de datos o data warehouse.  
- **Acceso ligero a metadatos:** lee marcas de tiempo de jobs, conteos de registros e información de particiones — no se requiere extracción de datos.  
- **Frecuencia configurable:** programa el monitoreo por conjunto de datos, esquema o pipeline.  
- **Alertas entre módulos:** los resultados pueden desencadenar advertencias visuales en *Inspection Hub* o notificaciones vía email, Slack o API.  

---

## Ejemplos de uso

- **Feeds del mercado financiero:** detectar retrasos en las actualizaciones de precios o datos de trading.  
- **Cargas en el Data Warehouse:** monitorear cuando los trabajos ETL nocturnos terminan más tarde de lo esperado.  
- **Compartición de datos entre equipos:** asegurar que las entregas departamentales ocurran antes de los cortes diarios.  
- **Reportes regulatorios:** confirmar que las presentaciones incluyan la instantánea de datos más reciente disponible.  

---

## Beneficios

| Area | Benefit |
|------|----------|
| **Business Continuity** | Previene interrupciones operativas debido a datos tardíos o faltantes |
| **Data Quality** | Mejora la confiabilidad y consistencia de las canalizaciones de datos |
| **Compliance** | Asegura el cumplimiento de SLA y la transparencia en auditorías |
| **Automation** | La IA elimina el seguimiento manual de horarios |
| **Integration** | Funciona de forma nativa con *Data Analytics* para visualizar tendencias de puntualidad a lo largo del tiempo |

---

## Cómo aprende digna los tiempos de entrega esperados

1. **Análisis histórico:** digna observa los tiempos y duraciones de cargas previas.  
2. **Modelado por IA:** el aprendizaje automático crea una línea base dinámica para la llegada esperada.  
3. **Monitoreo:** cada nueva entrega se compara con la línea base.  
4. **Alertas:** las desviaciones disparan alertas con métricas contextuales y puntuaciones de confianza.  

Este enfoque de aprendizaje continuo se adapta a procesos en evolución mientras mantiene bajas las falsas alertas.

---

## Preguntas frecuentes

**¿Puedo definir mis propios tiempos de entrega?**  
Sí. digna soporta tanto horarios fijos definidos por el usuario como patrones aprendidos por IA.

**¿Puede integrarse con mi herramienta de ETL u orquestación?**  
Sí. digna se integra con herramientas como Airflow, dbt, Informatica o schedulers personalizados.

**¿Dónde ocurre la computación?**  
Todo el análisis se ejecuta dentro de tu base de datos o data warehouse en la nube — no se utiliza ningún servicio externo.

**¿Qué ocurre cuando los datos llegan tarde?**  
digna genera alertas en el dashboard, en Inspection Hub y vía API/webhooks para notificar al equipo de operaciones de inmediato.

---


**digna Data Timeliness** ayuda a garantizar la **confianza en los datos**, combinando **detección impulsada por IA**, **ejecución on‑premises** y **observabilidad de datos** — todo dentro de tu entorno controlado.
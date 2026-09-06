# digna Data Anomalies – Detección basada en IA de problemas de calidad de datos

**Observabilidad impulsada por IA para una confianza continua en los datos**

digna Data Anomalies forma parte de la **plataforma de observabilidad de datos de digna** — una solución modular que mejora la **calidad de los datos** analizando continuamente cómo se comportan los conjuntos de datos a lo largo del tiempo.

Aprende automáticamente cómo es lo “normal” para tus datos y te alerta cuando el comportamiento cambia — sin definir umbrales estáticos ni escribir una sola regla.  
El módulo se ejecuta directamente dentro de tu base de datos, por lo que los datos nunca salen de tu entorno.

---

## Propósito de digna Data Anomalies

El módulo **digna Data Anomalies** proporciona **observabilidad de los datos** continua calculando y rastreando métricas estadísticas predefinidas tales como:

- Volumen de datos y recuentos de registros  
- Proporciones de valores faltantes  
- Distribuciones de valores e histogramas  
- Rangos numéricos y promedios  
- Unicidad de columna y longitud de texto  

Estas métricas se recopilan automáticamente para cada conjunto de datos.  
Con ellas, digna construye modelos que representan el comportamiento típico de cada métrica — aprendiendo patrones diarios, semanales o estacionales.  
Una vez entrenado, el módulo predice valores esperados para nuevos datos y detecta desviaciones que pueden indicar problemas de calidad, fallos en los procesos o cambios en sistemas upstream.

---

## Capacidades clave

- Aprende automáticamente el comportamiento esperado de los datos usando IA — sin configurar umbrales.  
- Detecta caídas bruscas, picos o desplazamientos en el volumen de datos y en las distribuciones.  
- Identifica columnas intercambiadas o mapeos incorrectos entre atributos.  
- Señala valores categóricos inesperados (p. ej., nuevas regiones o códigos).  
- Soporta todo tipo de columnas: numéricas, categóricas o no especificadas.  
- Opera completamente en el entorno del cliente — sin movimiento de datos.  
- Se integra con **digna Data Analytics** para análisis de tendencias a largo plazo.

---

## Cómo funciona

### Paso 1 – Cálculo de métricas
digna calcula un conjunto de métricas de perfil para cada tabla y columna.  
Estas métricas describen la estructura y el comportamiento estadístico de tus datos y se almacenan para análisis posteriores.

### Paso 2 – Entrenamiento de modelos
Sobre la base de valores históricos de las métricas, digna entrena modelos compactos de aprendizaje automático (modelos de firma) que capturan el rango normal de cada métrica.

### Paso 3 – Umbral automático
Usando *inferencia conformal*, digna calcula intervalos de confianza adaptativos (umbrales automáticos) que evolucionan con tus datos.  
Si nuevos valores de métricas caen fuera del rango predicho, se marcan como anomalías.

Este bucle de retroalimentación continuo asegura que el monitoreo siga siendo relevante incluso cuando los volúmenes o los patrones de datos crecen de forma natural.

---

## Escenarios de ejemplo

### Caída inesperada en el volumen de registros
Un conjunto de datos normalmente contiene alrededor de 500 000 registros por día.  
Cuando una nueva entrega incluye solo 50 000 registros, digna marca una anomalía y muestra cuánto se desvía el valor de su rango aprendido.

### Detección de columnas intercambiadas
La longitud promedio de cadena de `last_name` de repente coincide con la de `first_name`.  
digna reconoce la desviación en los patrones de las métricas y señala un posible intercambio de columnas.

### Detección de categoría inesperada
Una columna que lista ciudades austríacas de repente contiene “Zurich”.  
Basándose en distribuciones históricas, digna marca el nuevo valor como inesperado y alerta al usuario.

---

## Integración con otros módulos

- **digna Data Analytics** — agrega historial de anomalías y métricas de volatilidad para revelar tendencias a largo plazo.  
- **digna Data Validation** — aplica reglas de negocio explícitas para comprobaciones determinísticas de calidad.  
- **digna Data Timeliness** — monitorea los horarios de llegada de los datos y correlaciona retrasos con la aparición de anomalías.  
- **digna Data Schema Tracker** — detecta cambios estructurales que pueden explicar nuevas anomalías.

---

## Casos de uso típicos

- Detectar cargas de datos faltantes o duplicadas.  
- Identificar columnas intercambiadas o truncadas.  
- Detectar deriva de distribución en características numéricas o categóricas.  
- Encontrar valores de referencia o códigos inesperados.  
- Monitorear canalizaciones de ingestión continua en busca de irregularidades.  
- Rastrear la **calidad y observabilidad de los datos** en dominios completos.

---

## Beneficios

- Detección inmediata de comportamientos anómalos en los datos.  
- Elimina el ajuste manual de umbrales.  
- Reduce el esfuerzo operativo en entornos de datos grandes.  
- Aumenta la confianza en sistemas de analítica e informes.  
- Refuerza la **calidad de los datos** y la **observabilidad de datos** de extremo a extremo.

---

## Módulos relacionados de digna

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — trend and volatility metrics.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — rule-based data verification.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — monitoring data delivery schedules.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — schema change detection.

---

## Resumen

El módulo **digna Data Anomalies** forma el núcleo de la **plataforma de observabilidad de datos** impulsada por IA de digna.  
Al monitorear continuamente métricas clave, aprender patrones e identificar desviaciones, ayuda a las organizaciones a garantizar que la **calidad de los datos** se mantenga confiable, estable y explicable — sin configuración manual.
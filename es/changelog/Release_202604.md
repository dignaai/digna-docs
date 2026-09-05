# Registro de cambios – Release 2026.04  

Con la Release 2026.04, digna mejora significativamente sus capacidades en analítica y validación de datos.  
Esta versión introduce análisis avanzado de series temporales, componentes reutilizables de validación y estandarización centralizada de valores.

---

## Nuevas funcionalidades  

### Analytics Chart – Análisis de series temporales sin necesidad de ciencia de datos  
- Nuevo **Analytics Chart** para análisis interactivo de series temporales  
- Métodos analíticos integrados:
    - Regresión lineal, cuadrática y cúbica  
    - Regresión por tramos con puntos de quiebre configurables  
    - Técnicas de suavizado  
    - Análisis de cuantiles  
- Identificación automática de tendencias, estacionalidad y cambios de patrón  
- Análisis de residuos para una comprensión más profunda de las desviaciones  
- Las series temporales se calculan automáticamente para cada conjunto de datos  

**Impacto:** Permite a los usuarios entender comportamientos complejos de los datos a lo largo del tiempo sin requerir conocimientos de ciencia de datos ni herramientas externas.

---

### Enumeraciones – Definición central de valores permitidos  
- Define conjuntos reutilizables de valores permitidos (p. ej., países, estados, códigos de estado)  
- Valida los valores de columna contra enumeraciones predefinidas en **digna Data Validation**  
- Reutiliza enumeraciones entre proyectos y fuentes de datos  
- Usa enumeraciones en cualquier lugar mediante `#ENUM:MY_ENUM#`  
- Todas las comprobaciones se ejecutan **directamente en la base de datos de origen**  

**Impacto:** Asegura valores de datos consistentes y estandarizados en toda la organización.

---

### Plantillas de reglas de validación – Lógica reutilizable de calidad de datos  
- Define reglas de validación reutilizables (p. ej., comprobaciones de espacios en blanco, NOT NULL, verificaciones de formato)  
- Aplica plantillas a múltiples conjuntos de datos  
- Garantiza lógica de reglas consistente entre proyectos  
- Reduce duplicación y configuración manual  
- Todas las comprobaciones se ejecutan **directamente en la base de datos de origen**  

**Impacto:** Permite una validación de datos escalable y de alto rendimiento sin mover los datos.

---

### Condiciones de relevancia a nivel de estadística  
- Define condiciones de relevancia a nivel de columna para cada estadística  
- Amplía el concepto de condiciones de relevancia de anomalías  
- Controla cuándo una estadística debe considerarse relevante  
- Reduce el ruido excluyendo situaciones no críticas  

**Impacto:** Mejora la calidad de la señal al centrarse únicamente en desviaciones significativas.

---

## Capacidades extendidas de Data Analytics y validación  

Con esta versión, digna amplía tanto la comprensión de los datos como la estandarización de la validación:

- Interpretación avanzada de **series temporales** sin necesidad de conocimientos en ciencia de datos  
- Definición centralizada de **valores permitidos mediante enumeraciones**  
- Lógica de validación reutilizable mediante **plantillas**  
- Control granular sobre la **relevancia de estadísticas y alertas**  

En conjunto, estas capacidades permiten a las organizaciones no solo detectar problemas, sino también **entender, estandarizar y controlar la calidad de los datos**.

---

## ¿Quién se beneficia de esta versión?  

- **Ingenieros de datos:** Lógica de validación reutilizable y mayor control sobre el comportamiento del monitoreo  
- **Equipos de calidad de datos y gobernanza:** Reglas estandarizadas y validación consistente de datos entre sistemas  
- **Equipos de analítica y BI:** Mejor comprensión de tendencias y desviaciones  
- **Responsables de plataforma:** Mayor adopción gracias a analítica simplificada y validación escalable  

---

## Actualizaciones del CLI  
- Sin cambios  

---
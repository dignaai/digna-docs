# Changelog – Versión 2026.11  

La Versión 2026.11 gira en torno a tres grandes novedades:

- **digna Data Reconciliation**: comprueba que los datos se mantienen consistentes al moverse entre sistemas  
- **digna Agentic**: abre digna a los agentes de IA a través del digna MCP Server  
- **digna Engine**: perfila opcionalmente los datos dentro de digna y permite comprobaciones de integridad referencial entre distintas tecnologías de bases de datos  

---

## Nuevas características  

### digna Data Reconciliation (Beta) – Consistencia de origen a destino  
Los datos suelen pasar por varios sistemas antes de llegar a un informe. digna Data Reconciliation compara una fuente de datos de **destino** con los **orígenes** a partir de los cuales se construyó, y alerta cuando dejan de coincidir.

- Se configura como reglas con nombre en la nueva pestaña **Data Reconciliation** de la fuente de datos de destino  
- Cualquier fuente de datos del proyecto con Data Reconciliation activado puede ser un origen  
- Entre los casos de uso se incluyen los procedimientos de conciliación estándar y la validación de los resultados de procesos ETL  
- Dos tipos de reglas: **Exact** y **AI**  

**Reglas Exact – La conciliación como regla de calidad de datos**: defines exactamente qué debe coincidir entre un origen y un destino, como en una regla de calidad de datos.

  - Compara una fuente de datos de origen con una fuente de datos de destino  
  - Empareja una comprobación de destino con una de origen por estadística y atributo, p. ej., el recuento de filas o la suma de una columna de importes  
  - Permite una diferencia con una tolerancia **Absolute** (p. ej., ± 10) o **Relative** (p. ej., ± 0,5 % del origen)  
  - La línea de tiempo muestra la diferencia de cada día frente a la tolerancia  

**Reglas AI – La conciliación como observabilidad de datos**: digna aprende cómo un destino sigue a sus orígenes, del mismo modo en que digna observa los datos en otros módulos, y alerta cuando esa relación se rompe.

  - Combina comprobaciones de varias fuentes de datos de origen con las comprobaciones de un destino  
  - No necesitas conocer ni documentar la lógica que las une (joins, filtros, agregaciones)  
  - Un modelo aprende del historial cómo el destino sigue a sus orígenes en el mismo día  
  - Cada comprobación de destino se predice a partir de los valores de origen del día, y digna alerta cuando el destino sale de la banda formada por los errores pasados de la propia regla  
  - Cada regla tiene sus propios **Model settings**: **Sensitivity**, **Memory** y **Model Complexity**  

Las comprobaciones de conciliación aparecen en el Dashboard con una línea de tiempo por regla. Cuentan para el estado global de la inspección y disparan notificaciones.

**Impacto:** Cubre ambas caras de la conciliación. Las reglas Exact aplican controles conocidos entre origen y destino, y las reglas AI supervisan flujos complejos como los procesos ETL, de modo que los datos perdidos o modificados por el camino se detectan sin SQL de conciliación escrito a mano.

---

### digna Agentic (Beta) – digna para agentes de IA  
La primera versión de digna Agentic. Los agentes de IA ya pueden trabajar con digna, responder preguntas de negocio sobre tus datos y ayudarte a mejorar tu configuración.

**digna MCP Server**: permite que Claude y otros agentes de IA trabajen con digna a través del Model Context Protocol.

  - Gestiona proyectos, fuentes de datos, reglas, programaciones de inspección y suscripciones  
  - Consulta los estados de inspección hasta el nivel de cada comprobación para investigar alertas  

**Descripciones en fuentes de datos y atributos**: describe en lenguaje sencillo qué contiene una fuente de datos o un atributo.

  - Los agentes de IA usan las descripciones para interpretar tus datos  
  - Haz preguntas de negocio sobre tus datos y los agentes de IA las responden a partir de lo que digna monitoriza  
  - Si la configuración actual de digna no puede responder a una pregunta, el agente de IA sugiere cambios en la fuente de datos y sus atributos cuando es posible, p. ej., añadir un nuevo dataset  

**Impacto:** Te permite hacer preguntas de negocio sobre tus datos en lenguaje sencillo, y permite que los agentes de IA ayuden a configurar digna y a investigar problemas de calidad de datos.

---

### digna Engine – Perfila donde elijas  
De forma predeterminada, digna perfila los datos donde residen, en la base de datos de origen. El digna Engine añade una opción: digna exporta los datos desde el origen y los perfila dentro del digna Engine.

- Opcional, no obligatorio: el perfilado en la base de datos de origen sigue disponible  
- Se selecciona por conexión de base de datos como ubicación de perfilado (**Profiling Location**): **Source Database** o **digna Engine**  
- Disponible para todas las tecnologías de origen compatibles  

**Integridad referencial entre conexiones**: algunas comprobaciones requieren exportar los datos. El digna Engine amplía **digna Data Validation** para estos casos.

  - **Comprobaciones de integridad referencial** entre fuentes de datos en **distintas conexiones de base de datos**, incluidas distintas tecnologías de bases de datos (p. ej., Oracle y PostgreSQL)  
  - Funciona con ambas ubicaciones de perfilado: con Source Database, solo se exportan las columnas clave al digna Engine  
  - El dashboard indica cuándo una comprobación se ejecuta entre dos conexiones  

**Impacto:** Te permite elegir dónde se perfilan los datos y hace cumplir las relaciones entre sistemas que funcionan con distintas tecnologías de bases de datos.

---

## Mejoras en el perfilado  

Esta versión también da a los usuarios más control sobre qué se perfila y cómo.

### Atributos de consulta – Columnas definidas por el usuario  
- Define columnas artificiales: una expresión SQL sobre una o varias columnas de la fuente de datos  
- Cada atributo de consulta tiene su propio nombre  
- Se perfila y se comprueba como cualquier otro atributo  

### Categoría de columna DATE  
- Nueva categoría **Date** para atributos  
- Métricas relativas a la fecha inspeccionada  

### Perfilado bajo demanda  
- Perfila cualquier atributo sobre la instantánea completa de una fecha, sin ejecutar una inspección  
- Ayuda a establecer el tipo de columna del atributo: **Numerical**, **Categorical**, **Date** o **Unspecified**  

---

## Beneficiarios de esta versión  

- **Data Engineers:** validación de los resultados de ETL con digna Data Reconciliation  
- **Equipos de Finanzas, Riesgos y Controlling:** procedimientos de conciliación estándar como reglas Exact en digna Data Reconciliation  
- **Equipos de Calidad de Datos y Gobernanza:** integridad referencial entre tecnologías de bases de datos con el digna Engine  
- **Usuarios de negocio:** preguntas de negocio sobre los datos respondidas por agentes de IA con digna Agentic  
- **Equipos de IA y Automatización:** agentes de IA que trabajan con digna a través de digna Agentic  

---

## Actualizaciones del CLI  
- Sin cambios  
---
title: Data Anomalies – Detección automatizada | digna Documentación
description: Descubre cómo digna Data Anomalies detecta automáticamente caídas de volumen, valores faltantes, desplazamientos en la distribución y patrones inesperados sin reglas manuales. Mejora la calidad de los datos con detección de anomalías impulsada por IA.
---

# Data Anomalies – Detección automatizada

## Propósito
Detectar anomalías sin escribir reglas.

## Características técnicas
### Métricas analizadas
- Volumen de registros  
- Valores faltantes  
- Distribuciones e histogramas  
- Rangos de valores  
- Unicidad  

### Detección inteligente
- Utiliza **aprendizaje histórico** para definir dinámicamente rangos esperados  
- Marca anomalías cuando los datos reales se encuentran fuera de los límites esperados  

## Escenarios de detección
- **Caídas/aumentos de volumen** → p. ej., faltan la mitad de las transacciones diarias  
- **Intercambio de columnas** → columnas de nombre y apellido invertidas  
- **Valores inesperados** → “Zurich” apareciendo en ciudades austriacas  

## Valor
Automatiza lo que normalmente requeriría cientos de reglas manuales.
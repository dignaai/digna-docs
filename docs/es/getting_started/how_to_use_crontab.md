---
title: Programación avanzada con crontab
description: Aprende cómo programar un trabajo en *digna* usando expresiones crontab para una planificación avanzada.
image: /assets/logo_square.png
---

# Programación avanzada con crontab

Esta guía muestra cómo programar trabajos en *digna* usando **expresiones crontab**.  
A diferencia de los patrones estándar (diario, semanal, mensual), crontab te da flexibilidad total para definir horarios personalizados.

---

## Demo interactiva

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Qué aprenderás

- Cómo abrir la sección **Scheduling** en el dashboard  
- Cómo crear un nuevo trabajo usando una **expresión crontab**  
- Cómo configurar una programación que se ejecute solo los **fines de semana a las 10:00**  

---

## Ejemplo: programación de fin de semana

Para programar un trabajo para que se ejecute todos los **sábados y domingos a las 10:00**, usa la siguiente expresión:


- `0` → minuto (en punto)  
- `10` → hora (10:00)  
- `*` → cada día del mes  
- `*` → cada mes  
- `sat,sun` → solo los sábados y domingos  

---

## ¿Por qué usar crontab?

- Crear programaciones más allá de los patrones estándar diarios, semanales o mensuales  
- Definir tiempos de ejecución precisos (días, horas o intervalos específicos)  
- Útil para trabajos de fin de semana, comprobaciones fuera de horario o monitoreo frecuente  

---
---
title: Geavanceerde planning met Crontab
description: Leer hoe je een taak plant in digna met crontab-expressies voor geavanceerde timing.
image: /assets/logo_square.png
---

# Geavanceerde planning met Crontab

Deze gids toont hoe je taken plant in *digna* met **crontab-expressies**.  
In tegenstelling tot de standaardpatronen (dagelijks, wekelijks, maandelijks) geeft crontab je volledige flexibiliteit om aangepaste schema's te definiëren.

---

## Interactive Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## What You Will Learn

- How to open the **Scheduling** section in the dashboard  
- How to create a new job using a **crontab-expressie**  
- How to set a schedule that runs only on **weekends at 10:00**  

---

## Example: Weekend Schedule

Om een taak te plannen die elke **zaterdag en zondag om 10:00 uur** draait, gebruik je de volgende expressie:


- `0` → minuut (op het uur)  
- `10` → uur (10:00)  
- `*` → elke dag van de maand  
- `*` → elke maand  
- `sat,sun` → alleen op zaterdag en zondag  

---

## Waarom Crontab gebruiken?

- Maak schema's buiten de standaard dagelijkse, wekelijkse of maandelijkse patronen  
- Definieer exacte uitvoertijden (specifieke dagen, uren of intervallen)  
- Handig voor weekendtaken, controles buiten piekuren of frequent toezicht  

---
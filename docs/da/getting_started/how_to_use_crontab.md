---
title: Avanceret planlægning med Crontab
description: Lær, hvordan du planlægger et job i *digna* ved hjælp af crontab-udtryk til avanceret planlægning.
image: /assets/logo_square.png
---

# Avanceret planlægning med Crontab

Denne vejledning viser, hvordan du planlægger jobs i *digna* ved hjælp af **crontab-udtryk**.  
I modsætning til standardmønstrene (dagligt, ugentligt, månedligt) giver crontab dig fuld fleksibilitet til at definere tilpassede tidsplaner.

---

## Interaktiv demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Hvad du vil lære

- Hvordan du åbner **Scheduling**-sektionen i dashboardet  
- Hvordan du opretter et nyt job ved hjælp af et **crontab-udtryk**  
- Hvordan du sætter en plan, der kun kører **i weekenden kl. 10:00**  

---

## Eksempel: Weekendplan

For at planlægge et job til at køre hver **lørdag og søndag kl. 10:00**, brug følgende udtryk:


- `0` → minut (på timen)  
- `10` → time (kl. 10)  
- `*` → hver dag i måneden  
- `*` → hver måned  
- `sat,sun` → kun på lørdage og søndage  

---

## Hvorfor bruge Crontab?

- Opret planer ud over standard daglige, ugentlige eller månedlige mønstre  
- Definér præcise køretidspunkter (specifikke dage, tidspunkter eller intervaller)  
- Nyttigt til jobs i weekenden, kontroller uden for arbejdstid eller hyppig overvågning  

---
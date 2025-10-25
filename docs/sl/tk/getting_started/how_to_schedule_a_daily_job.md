---
title: Kako ustvariti job, ki se izvaja vsak dan
description: Naučite se, kako z digna na dashboardu razporediti dnevni pregled podatkov.
keywords: digna razporejanje, avtomatizacija kakovosti podatkov, dnevni job
---

# Kako razporediti dnevni job

Razporejanje omogoča, da se preverjanja samodejno zaženejo brez ročnega poseganja.  
V tem vodiču se boste naučili, kako ustvariti job, ki se izvaja **enkrat na dan**.

---

## Interaktivni demo

Za praktičen prikaz postopka si oglejte interaktivni vodič:  

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/Ra9E19A0QfMpzKqm3Yhu?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a New Data Inspection Job" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Kaj se boste naučili

- kako dostopati do razdelka **Scheduling** v digna dashboardu  
- kako ustvariti nov razporejen job  
- kako ga konfigurirati, da se izvaja **dnevno, ob fiksni uri**  
- kako izbrati pravi projekt in datasource  
- kako omogočiti, da se job samodejno zažene  

---

## Zakaj so dnevni jobi koristni

Dnevno razporejanje je najbolj pogosta nastavitev v produkcijskih okoljih. Zagotavlja:  

- **Svežina** — podatki se preverjajo vsak dan.  
- **Doslednost** — anomalije se zaznajo zgodaj, preden se razširijo po downstreamu.  
- **Avtomatizacija** — preverjanja vam ni treba sprožati ročno.  

---

## Naslednji koraki

- Za bolj napredne in prilagojene razporeditve si oglejte razdelek [how_to_use_crontab.md](how_to_use_crontab.md).  
- Povežite dnevne jobe z **alerting**, da prejemate obvestila, ko so zaznane anomalije.
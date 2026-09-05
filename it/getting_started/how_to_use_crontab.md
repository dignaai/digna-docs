# Pianificazione avanzata con Crontab

Questa guida mostra come pianificare job in *digna* usando **espressioni crontab**.  
A differenza dei modelli standard (daily, weekly, monthly), crontab ti offre piena flessibilità per definire pianificazioni personalizzate.

---

## Demo interattiva

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Cosa imparerai

- Come aprire la sezione **Scheduling** della dashboard  
- Come creare un nuovo job usando una **espressione crontab**  
- Come impostare una pianificazione che venga eseguita solo nei **weekend alle 10:00**  

---

## Esempio: Pianificazione per il weekend

Per programmare un job che venga eseguito ogni **sabato e domenica alle 10:00**, usa la seguente espressione:


- `0` → minuto (all'inizio dell'ora)  
- `10` → ora (10:00)  
- `*` → ogni giorno del mese  
- `*` → ogni mese  
- `sat,sun` → solo il sabato e la domenica  

---

## Perché usare Crontab?

- Creare pianificazioni oltre i modelli standard daily, weekly o monthly  
- Definire orari di esecuzione precisi (giorni specifici, ore o intervalli)  
- Utile per job del weekend, controlli fuori orario o monitoraggi frequenti  

---
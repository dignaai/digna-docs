---
title: Papildu plānošana ar Crontab
description: Uzziniet, kā plānot darbu digna, izmantojot crontab izteiksmes sarežģītākai laika konfigurācijai.
---

# Papildu plānošana ar Crontab

This guide shows how to schedule jobs in *digna* using **crontab expressions**.  
Atšķirībā no standarta shēmām (dienas, nedēļas, mēneša), crontab nodrošina pilnu elastību pielāgotu grafiku definēšanai.

---

## Interaktīvā demonstrācija

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Ko jūs uzzināsiet

- Kā dashboardā atvērt sadaļu **Scheduling**  
- Kā izveidot jaunu darbu, izmantojot **crontab izteiksmi**  
- Kā iestatīt grafiku, kas darbojas tikai **nedēļas nogalēs pulksten 10:00**  

---

## Piemērs: nedēļas nogales grafiks

Lai plānotu darbu, kas tiek veikts katru **sestdienu un svētdienu pulksten 10:00**, izmantojiet šādu izteiksmi:


- `0` → minūte (pilnā stundā)  
- `10` → stunda (10:00)  
- `*` → katru mēneša dienu  
- `*` → katru mēnesi  
- `sat,sun` → tikai sestdienās un svētdienās  

---

## Kāpēc izmantot Crontab?

- Izveidot grafikus ārpus standarta dienas, nedēļas vai mēneša shēmām  
- Noteikt precīzus izpildes laikus (konkrētas dienas, stundas vai intervāli)  
- Noderīgi nedēļas nogales darbiem, ārpusdarba laika pārbaudēm vai biežai uzraudzībai  

---
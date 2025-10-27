---
title: Täpsem ajastamine Crontabi abil
description: Õpi, kuidas *digna*-s tööd ajastada, kasutades crontab expressions täpsemaks ajastuseks.
---

# Advanced Scheduling with Crontab

See juhend näitab, kuidas *digna*-s töid ajastada, kasutades **crontab expressions**.  
Erinevalt standardsetest mustritest (päevane, iganädalane, igakuine) annab crontab täieliku paindlikkuse kohandatud ajakavade määramiseks.

---

## Interaktiivne demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Mida sa õpid

- Kuidas avada armatuurlaual **Scheduling** jaotis  
- Kuidas luua uus töö, kasutades **crontab expression**  
- Kuidas seada ajakava, mis käivitub ainult **nädalavahetustel kell 10:00**  

---

## Näide: nädalavahetuse ajakava

Töö ajastamiseks nii, et see käivituks iga **laupäeval ja pühapäeval kell 10:00**, kasuta järgmist väljendit:


- `0` → minut (täistunnil)  
- `10` → tund (kell 10)  
- `*` → kõigil kuu päevadel  
- `*` → igal kuul  
- `sat,sun` → ainult laupäeviti ja pühapäeviti  

---

## Miks kasutada Crontabit?

- Loo ajakavasid, mis ei piirdu tavapäraste päevaste, iganädalaste või igakuiste mustritega  
- Määra täpsed käivitamisajad (konkreetseid päevi, tunde või intervalle)  
- Kasulik nädalavahetuse ülesannete, tööväliste kontrollide või sagedase jälgimise jaoks  

---
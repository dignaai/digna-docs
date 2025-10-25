---
title: Haladó ütemezés crontab használatával
description: Tudja meg, hogyan ütemezhet munkát a *digna*-ban crontab kifejezések segítségével összetettebb időpontokhoz.
---

# Haladó ütemezés crontab használatával

Ez az útmutató megmutatja, hogyan ütemezhetsz feladatokat a *digna*-ban **crontab-kifejezések** használatával.  
A szabványos mintákkal (napi, heti, havi) ellentétben a crontab teljes rugalmasságot ad az egyedi időzítések meghatározásához.

---

## Interaktív demó

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Mit fogsz megtanulni

- Hogyan nyisd meg a **Scheduling** szekciót a dashboardon  
- Hogyan hozz létre egy új feladatot **crontab-kifejezés** használatával  
- Hogyan állíts be egy ütemezést, amely csak **hétvégén 10:00-kor** fut  

---

## Példa: hétvégi ütemezés

Egy feladat ütemezéséhez, amely minden **szombaton és vasárnap 10:00-kor** fut, használd a következő kifejezést:


- `0` → perc (egész órakor)  
- `10` → óra (10:00-kor)  
- `*` → a hónap minden napja  
- `*` → minden hónap  
- `sat,sun` → csak szombaton és vasárnap  

---

## Miért használj crontab-ot?

- Hozz létre ütemezéseket a szabványos napi, heti vagy havi mintákon túl  
- Határozz meg pontos futási időpontokat (konkrét napok, időpontok vagy intervallumok)  
- Hasznos hétvégi feladatokhoz, munkaidőn kívüli ellenőrzésekhez vagy gyakori felügyelethez  

---
---
title: Fejlett ütemezés crontab használatával
description: Tanuld meg, hogyan ütemezhetsz feladatot a *digna*-ban crontab-kifejezések segítségével összetettebb időzítésekhez.
image: /assets/logo_square.png
---

# Fejlett ütemezés crontab használatával

Ez az útmutató megmutatja, hogyan ütemezhetsz feladatokat a *digna*-ban **crontab-kifejezések** használatával.  
A szabványos mintáktól (daily, weekly, monthly) eltérően a crontab teljes rugalmasságot ad egyéni ütemtervek meghatározásához.

---

## Interaktív bemutató

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Mit fogsz megtanulni

- Hogyan nyisd meg a **Scheduling** szekciót a dashboardon  
- Hogyan hozz létre egy új feladatot **crontab-kifejezés** használatával  
- Hogyan állíts be olyan ütemezést, amely csak a **hétvégéken 10:00-kor** fut  

---

## Példa: hétvégi ütemezés

A feladat ütemezéséhez, amely minden **szombaton és vasárnap 10:00-kor** fut, használd a következő kifejezést:


- `0` → perc (egész órában)  
- `10` → óra (10:00)  
- `*` → a hónap minden napja  
- `*` → minden hónap  
- `sat,sun` → csak szombaton és vasárnap  

---

## Miért érdemes crontabot használni?

- Olyan ütemezések létrehozása, amelyek túlmutatnak a napi, heti vagy havi standard mintákon  
- Pontos futási időpontok meghatározása (konkrét napok, órák vagy intervallumok)  
- Hasznos hétvégi feladatokhoz, munkaidőn kívüli ellenőrzésekhez vagy gyakori megfigyeléshez  

---
---
title: Kiterjesztett ütemezés crontab segítségével
description: Tudja meg, hogyan ütemezhet feladatokat a digna-ban crontab kifejezések segítségével a haladó időbeállításokhoz.
---

# Kiterjesztett ütemezés crontab segítségével

Ez az útmutató megmutatja, hogyan ütemezhet feladatokat a *digna*-ban crontab kifejezések segítségével.  
A szabványos sablonokkal (naponta, hetente, havonta) ellentétben a crontab teljes szabadságot ad egyedi ütemezések meghatározására.

---

## Interaktív bemutató

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Mit fog megtanulni

- Hogyan nyissa meg a **Scheduling** részt a dashboardon  
- Hogyan hozzon létre egy új feladatot, **crontab kifejezés** használatával  
- Hogyan állítson be ütemezést, amely csak a **hétvégéken 10:00-kor** fut  

---

## Példa: hétvégi ütemezés

Ha egy olyan feladatot szeretne ütemezni, amely minden **szombaton és vasárnap 10:00-kor** fut, használja az alábbi kifejezést:


- `0` → perc (az óra elején)  
- `10` → óra (10:00)  
- `*` → minden nap a hónapban  
- `*` → minden hónap  
- `sat,sun` → csak szombaton és vasárnap  

---

## Miért érdemes crontab-ot használni?

- Olyan ütemezések létrehozása, amelyek túllépnek a szabványos napi, heti vagy havi sablonokon  
- A pontos indítási idő megadása (konkrét napok, órák vagy intervallumok)  
- Hasznos hétvégi feladatokhoz, munkaidőn kívüli ellenőrzésekhez vagy gyakori monitorozáshoz  

---
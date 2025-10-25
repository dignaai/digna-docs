---
title: Fejlett ütemezés crontab használatával
description: Ismerje meg, hogyan ütemezhet egy feladatot a *digna*-ban crontab kifejezések használatával fejlett időzítésekhez.
---

# Fejlett ütemezés crontab használatával

Ez az útmutató bemutatja, hogyan ütemezhet feladatokat a *digna*-ban **crontab kifejezések** használatával.  
A szabványos minták (napi, heti, havi) helyett a crontab teljes rugalmasságot biztosít egyedi ütemezések megadásához.

---

## Interaktív demó

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Mit fog megtanulni

- Hogyan nyissa meg a vezérlőpanel **Ütemezés** részét  
- Hogyan hozzon létre új feladatot egy **crontab kifejezéssel**  
- Hogyan állítson be egy ütemezést, amely csak a **hétvégén 10:00-kor** fut  

---

## Példa: Hétvégi ütemezés

Egy feladat ütemezéséhez, hogy minden **szombaton és vasárnap 10:00-kor** fusson, használja az alábbi kifejezést:


- `0` → perc (óra elején)  
- `10` → óra (10:00)  
- `*` → a hónap minden napja  
- `*` → minden hónapban  
- `sat,sun` → csak szombat és vasárnap  

---

## Miért használjunk crontabot?

- Hozzon létre ütemezéseket a napi, heti vagy havi szabványos mintákon túl  
- Határozzon meg pontos futási időpontokat (konkrét napok, órák vagy időintervallumok)  
- Hasznos hétvégi feladatokhoz, munkaidőn kívüli ellenőrzésekhez vagy gyakori megfigyeléshez  

---
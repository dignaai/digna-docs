---
title: Hogyan ütemezzünk egy naponta futó jobot
description: Tudja meg, hogyan ütemezzen napi ellenőrző jobot a digna dashboardján keresztül.
keywords: digna ütemezés, adatminőség automatizálás, napi job
---

# Hogyan ütemezzünk egy naponta futó jobot

Az ütemezés lehetővé teszi, hogy az ellenőrzéseket kézi beavatkozás nélkül automatikusan futtassa.  
Ebben az útmutatóban megtanulja, hogyan hozzon létre egy, az adatait folyamatosan figyelő, **naponta egyszer** futó jobot.

---

## Interaktív demó

A folyamatot gyakorlati példán keresztül tekintheti meg az interaktív bemutatóban:  

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/Ra9E19A0QfMpzKqm3Yhu?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a New Data Inspection Job" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Mit fog megtanulni

- Hogyan férjen hozzá a digna dashboardon található **Scheduling** részhez  
- Hogyan hozzon létre egy új ütemezett jobot  
- Hogyan konfigurálja, hogy **naponta, rögzített időpontban** fusson  
- Hogyan válassza ki a megfelelő projektet és datasource-t  
- Hogyan engedélyezze, hogy a job automatikusan fusson  

---

## Miért hasznosak a napi jobok

A napi ütemezés az éles környezetekben a leggyakoribb beállítás. A következő előnyökkel jár:  

- **Frissesség** — az adatok naponta ellenőrzésre kerülnek.  
- **Következetesség** — az anomáliák korán észlelhetők, mielőtt lefelé terjednének.  
- **Automatizálás** — nincs szükség az ellenőrzések kézi indítására.  

---

## Következő lépések

- A fejlettebb, egyedi ütemezésekhez tekintse át a [Hogyan használjuk a crontab definíciót](how_to_use_crontab.md) részt.  
- Az anomáliák észlelésekor értesítések fogadásához kombinálja a napi jobokat a **alerting**-gel.
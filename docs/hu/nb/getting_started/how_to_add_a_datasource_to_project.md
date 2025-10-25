---
title: Kapcsolódás egy adatbázishoz | digna-dokumentáció
description: Lépésről lépésre útmutató, hogyan csatlakoztass egy adatbázist egy meglévő projekthez a digna-ban. Tanuld meg, hogyan válassz kapcsolatot, konfiguráld a beállításokat és engedélyezd a biztonságos hozzáférést.
---

# Datasource (Table) hozzáadása egy projekthez

Ez az útmutató bemutatja a minimális lépéseket, amelyek szükségesek egy datasource hozzáadásához a projektedhez.

## Interaktív demó

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/jvxy4tXv5xQlRAa1MsLI?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Add a Data Source to a Project" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

### Lépések

1. **Åpne prosjektet ditt**  
   A bal oldali menüből kattints a **Projects**-re, és válaszd ki a célprojektet.

2. **Legg til en Datasource**  
   Lépj a **Datasources**-hoz, és kattints a **Add Datasource**-ra.

3. **Velg type Datasource**  
   Válaszd ki a Datasource típusát: **Table** vagy **View**.

4. **Finn din Datasource i listen**  
   Válaszd ki a Datasource-odat a listából.

5. **Definer Snapshot Query**  
   Határozd meg a **Snapshot Query**-t. A Snapshot Query meghatározza, hogyan fog a *digna* hozzáférni egy napi adatokhoz.

6. **Forhåndsvisning**  
   Kattints a preview-re, hogy ellenőrizd, a Snapshot Query helyesen lett-e definiálva.

7. **Opprett datasource**  
   Ha minden helyesen van konfigurálva, elmentheted a konfigurációdat.
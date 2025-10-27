---
title: Ühenda andmebaas | digna dokumentatsioon
description: Samm-sammuline juhend andmebaasi ühendamiseks olemasoleva projektiga dignas. Õpi, kuidas konfigureerida ühendusi, esitada mandaate ja lubada turvaline juurdepääs.
---

# Ühenda andmebaas

See juhend näitab minimaalseid samme andmebaasiühenduse lisamiseks teie projekti.

## Interaktiivne demo

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="Connect a Database to a Project"
    frameborder="0"
    loading="lazy"
    webkitallowfullscreen
    mozallowfullscreen
    allowfullscreen
    allow="clipboard-write"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;">
  </iframe>
</div>
<!--ARCADE EMBED END-->

---

### Sammud

1. **Ava oma projekt**  
   Vasakust navigeerimisest klõpsake **Projektid** ja valige soovitud projekt.

2. **Lisa ühendus**  
   Minge jaotisse **Ühendused** ja klõpsake **Lisa ühendus**.

3. **Vali andmebaasi tüüp**  
   Valige andmebaas, millega soovite ühenduse luua (nt PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Sisestage ühenduse andmed**  
   Esitage **Nimi**, **Host**, **Port**, **Andmebaas/Teenuse** ja **Kasutajatunnused** (kasutajanimi/parool või SSO, vastavalt).

5. **Testi ja salvesta**  
   Klõpsake **Test**. Kui test õnnestub, klõpsake **Salvesta**. Ühendus kuvatakse projekti all jaotises **Ühendused**.
---
title: Prijungti duomenų bazę | digna dokumentacija
description: Žingsnis po žingsnio vadovas, kaip prijungti duomenų bazę prie esamo projekto digna. Sužinokite, kaip sukonfigūruoti ryšius, pateikti prisijungimo duomenis ir užtikrinti saugų prieigą.
---

# Prijungti duomenų bazę

Šis vadovas parodo minimalius žingsnius, kaip pridėti duomenų bazės ryšį prie jūsų projekto.

## Interaktyvi demonstracija

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

### Žingsniai

1. **Atidarykite savo projektą**  
   Kairėje naršymo juostoje spustelėkite **Projects** ir pasirinkite norimą projektą.

2. **Pridėti ryšį**  
   Eikite į **Connections** ir spustelėkite **Add Connection**.

3. **Pasirinkite duomenų bazės tipą**  
   Pasirinkite duomenų bazę, kurią norite prijungti (pvz., PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Įveskite ryšio duomenis**  
   Nurodykite **Name**, **Host**, **Port**, **Database/Service** ir **Credentials** (vartotojo vardą/slaptažodį arba SSO, jei taikoma).

5. **Išbandykite ir išsaugokite**  
   Spustelėkite **Test**. Jei bandymas pavyks, spustelėkite **Save**. Ryšys bus rodomas skiltyje **Connections** jūsų projekte.
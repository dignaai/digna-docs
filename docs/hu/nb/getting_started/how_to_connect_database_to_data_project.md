---
title: Csatlakozás egy adatbázishoz | digna-dokumentáció
description: Lépésről lépésre útmutató egy adatbázis csatlakoztatásához egy meglévő projekthez a digna rendszerben. Tanuld meg, hogyan konfiguráld a kapcsolatokat, add meg a hitelesítő adatokat és engedélyezd a biztonságos hozzáférést.
---

# Csatlakozás egy adatbázishoz

Ez az útmutató bemutatja a minimális lépéseket egy adatbázis-kapcsolat hozzáadásához a projektedhez.

## Interaktív demó

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="Koble en database til et prosjekt"
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

### Lépések

1. **Nyisd meg a projektedet**  
   A bal oldali menüből kattints a **Projektek** pontra, és válaszd ki a célprojektet.

2. **Adj hozzá egy kapcsolatot**  
   Menj a **Csatlakozások** részhez és kattints a **Csatlakozás hozzáadása** gombra.

3. **Válaszd ki az adatbázis típusát**  
   Válaszd ki azt az adatbázist, amelyhez csatlakozni szeretnél (pl. PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Add meg a kapcsolat részleteit**  
   Töltsd ki a **Név**, **Host**, **Port**, **Database/Service**, és **Credentials** mezőket (felhasználónév/jelszó vagy SSO, a megfelelőtől függően).

5. **Teszteld és mentsd el**  
   Kattints a **Teszt** gombra. Ha sikeres, kattints a **Mentés**-re. A kapcsolat meg fog jelenni a projekt **Csatlakozások** listájában.
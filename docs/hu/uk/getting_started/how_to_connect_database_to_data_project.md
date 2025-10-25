---
title: Adatbázis csatlakoztatása | digna dokumentáció
description: Lépésről lépésre útmutató egy adatbázis csatlakoztatásához egy meglévő projekthez a digna-ban. Tudja meg, hogyan állíthatja be a kapcsolatot, adhatja meg a hitelesítő adatokat és biztosíthatja a biztonságos hozzáférést.
---

# Adatbázis csatlakoztatása

Ebben az útmutatóban a minimális lépések találhatók egy adatbázis-kapcsolat hozzáadásához a projektjéhez.

## Interaktív bemutató

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

### Lépések

1. **Nyissa meg a projektjét**  
   A bal oldali navigációs sávban kattintson a **Projects**-re, és válassza ki a kívánt projektet.

2. **Kapcsolat hozzáadása**  
   Lépjen a **Connections**-hez, és kattintson az **Add Connection**-re.

3. **Válassza ki az adatbázis típusát**  
   Válassza ki azt az adatbázist, amelyhez csatlakozni kíván (például PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Adja meg a kapcsolati paramétereket**  
   Adja meg a **Name**, **Host**, **Port**, **Database/Service** és **Credentials** mezőket (felhasználónév/jelszó vagy SSO az esettől függően).

5. **Ellenőrizze és mentse**  
   Kattintson a **Test**-re. Ha a teszt sikeres, kattintson a **Save**-re. A kapcsolat megjelenik a projekt **Connections** részében.
# Adatbázis csatlakoztatása

Ez az útmutató a minimálisan szükséges lépéseket mutatja be egy adatbázis-kapcsolat hozzáadásához a projektedhez.

## Interaktív demó

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

1. **Nyisd meg a projekted**  
   A bal oldali navigációs sávból kattints a **Projects** elemre, és válaszd ki a célprojektet.

2. **Kapcsolat hozzáadása**  
   Menj a **Connections** részhez és kattints az **Add Connection** gombra.

3. **Válassz adatbázis-típust**  
   Válaszd ki azt az adatbázist, amelyhez csatlakozni szeretnél (pl. PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Add meg a kapcsolati adatokat**  
   Töltsd ki a **Name**, **Host**, **Port**, **Database/Service** és a **Credentials** mezőket (felhasználónév/jelszó vagy SSO, ahol alkalmazható).

5. **Tesztelés és mentés**  
   Kattints a **Test** gombra. Ha sikeres, kattints a **Save**-re. A kapcsolat meg fog jelenni a projekt **Connections** listájában.
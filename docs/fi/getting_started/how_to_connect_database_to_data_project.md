---
title: Yhdistä tietokanta | digna-dokumentaatio
description: Askel askeleelta -opas tietokannan yhdistämiseen olemassa olevaan projektiin dignassa. Opi konfiguroimaan yhteydet, antamaan tunnistetiedot ja ottamaan käyttöön turvallinen pääsy.
---

# Yhdistä tietokanta

Tämä opas näyttää vähimmäisvaiheet tietokantayhteyden lisäämiseksi projektiisi.

## Interaktiivinen demo

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

### Vaiheet

1. **Avaa projektisi**  
   Vasemmasta navigaatiosta klikkaa **Projects** ja valitse kohdeprojekti.

2. **Lisää yhteys**  
   Siirry kohtaan **Connections** ja klikkaa **Add Connection**.

3. **Valitse tietokantatyyppi**  
   Valitse yhdistettävä tietokanta (esim. PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Syötä yhteystiedot**  
   Anna **Name**, **Host**, **Port**, **Database/Service** ja **Credentials** (käyttäjätunnus/salasana tai SSO, tarpeen mukaan).

5. **Testaa ja tallenna**  
   Klikkaa **Test**. Jos yhteys onnistuu, klikkaa **Save**. Yhteys näkyy projektin **Connections**-kohdassa.
---
title: Anslut en databas | digna dokumentation
description: Steg-för-steg-guide för att ansluta en databas till ett befintligt projekt i digna. Lär dig hur du konfigurerar anslutningar, anger behörighetsuppgifter och möjliggör säker åtkomst.
image: /assets/logo_square.png
---

# Anslut en databas

Denna guide visar de minsta stegen för att lägga till en databasanslutning till ditt projekt.

## Interaktiv demo

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

### Steg

1. **Öppna ditt projekt**  
   I den vänstra navigeringen, klicka på **Projekt** och välj målprojektet.

2. **Lägg till en anslutning**  
   Gå till **Anslutningar** och klicka på **Lägg till anslutning**.

3. **Välj databas typ**  
   Välj den databas du vill ansluta (t.ex. PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Ange anslutningsdetaljer**  
   Ange **Namn**, **Host**, **Port**, **Databas/Tjänst** och **Behörighetsuppgifter** (användarnamn/lösenord eller SSO, om tillämpligt).

5. **Testa & Spara**  
   Klicka på **Testa**. Om det lyckas, klicka på **Spara**. Anslutningen visas under **Anslutningar** för projektet.
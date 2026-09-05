---
title: Připojení databáze | Dokumentace digna
description: Krok za krokem návod, jak připojit databázi k existujícímu projektu v digna. Naučte se, jak nakonfigurovat připojení, zadat přihlašovací údaje a zajistit bezpečný přístup.
image: /assets/logo_square.png
---

# Připojení databáze

Tento návod ukazuje minimální kroky potřebné k přidání připojení k databázi do vašeho projektu.

## Interaktivní ukázka

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="Připojení databáze k projektu"
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

### Kroky

1. **Open Your Project**  
   V levém navigačním panelu klikněte na **Projects** a vyberte cílový projekt.

2. **Add a Connection**  
   Přejděte do **Connections** a klikněte na **Add Connection**.

3. **Choose Database Type**  
   Vyberte databázi, ke které se chcete připojit (např. PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Enter Connection Details**  
   Zadejte **Name**, **Host**, **Port**, **Database/Service** a **Credentials** (uživatelské jméno/heslo nebo SSO, podle potřeby).

5. **Test & Save**  
   Klikněte na **Test**. Pokud je test úspěšný, klikněte na **Save**. Připojení se zobrazí v **Connections** pro daný projekt.
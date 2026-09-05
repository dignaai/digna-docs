---
title: Reference digna CLI – Úvod | digna Documentation
description: Úvod do rozhraní příkazové řádky (CLI) digna — textového nástroje pro automatizaci a správu zdrojů digna, včetně základů instalace ve Windows.
keywords: digna cli, příkazová řádka digna, automatizace digna, skriptování digna, reference cli, instalace dignacli
image: /assets/logo_square.png
---

## Účel rozhraní příkazového řádku (CLI)

Příkazové rozhraní (CLI) ***digna*** je výkonný nástroj navržený ke zjednodušení interakcí s platformou ***digna***. Poskytuje textové rozhraní, které uživatelům umožňuje efektivně provádět širokou škálu úkolů, aniž by bylo potřeba grafické uživatelské rozhraní.

### Hlavní funkce:

- **Efektivita a flexibilita:** CLI umožňuje rychlé provádění příkazů, což zvyšuje produktivitu.
- **Automatizace:** Podpora skriptování pro automatizaci opakujících se úloh.
- **Vzdálený přístup:** Spravujte zdroje ***digna*** odkudkoli.
- **Konzistence a spolehlivost:** Zajišťuje spolehlivý provoz s dokumentovanými, verzovanými příkazy.
- **Škálovatelnost:** Zvládá rozsáhlé operace pro podnikové úlohy.
- **Učení a zvládnutí:** Poskytuje hlubší porozumění funkcionalitě ***digna***.
- **Integrace s jinými nástroji:** Bezproblémová integrace s nástroji pro automatizaci jako Control-M, UC4, AutomateNOW!

---

## Instalační pokyny pro Windows

Chcete-li začít, postupujte podle níže uvedených kroků k rozbalení potřebných souborů, nasazení složky *dignacli* a nakonfigurování připojení k repozitáři ***digna***. Před zahájením si připravte přihlašovací údaje do repozitáře a veškeré požadované konfigurační údaje.

1. **Extracting the ***digna*** CLI:**
   - Získejte soubor `.zip` obsahující CLI ***digna***.
   - Rozbalte soubor do vámi zvoleného adresáře.

2. **Deploying the `dignacli` Folder:**
   - Zkopírujte složku `dignacli` do preferovaného instalačního umístění (např. `C:\Program Files\***digna***`).

3. **Configuring `config.toml`:**
   - Zkontrolujte přítomnost souboru `config.toml` uvnitř `dignacli`.
   - Přejmenujte `config_template.toml` na `config.toml`, pokud je to potřeba, a nakonfigurujte ho podle poskytnuté dokumentace.
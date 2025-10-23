---
title: Data Schema Tracker – Monitorování evoluce schématu | digna Dokumentace
description: Zjistěte, jak digna Data Schema Tracker sleduje změny sloupců, aktualizace datových typů a drift schématu. Získejte upozornění na záměrné i nezáměrné změny, aby se předešlo selháním ETL a chybám v dashboardech.
---

# Data Schema Tracker – Monitorování evoluce schématu

## Účel
Sledovat a upozorňovat na evoluci schématu.

## Technické funkce
- Sleduje:
  - Přidané nebo odebrané sloupce
  - Změny datových typů
- Upozornění na záměrné i nezáměrné změny schématu  
- Zabraňuje **tichému driftu schématu**, který může způsobit selhání ETL pipelines nebo chyby v dashboardech  

## Příklady použití
- Identifikace změn datových typů (např. `INT` → `VARCHAR`), které mohou způsobit chyby v následných procesech  
- Upozornění datových inženýrů před selháním pipelines kvůli neshodám ve schématu  

## Hodnota
Pomáhá týmům udržet kontrolu nad **rychle se měnícími, vyvíjejícími se datovými sadami**.
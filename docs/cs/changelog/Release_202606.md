---
title: digna Release 2026.06 | Python SDK, Docker nasazení & rozšířené řízení validací
description: Zjistěte, co je nového v digna Release 2026.06. Tato verze přináší nový digna Python SDK, podporu nasazení v Dockeru, přepracované rozhraní dashboardu a rozšířené možnosti importu/exportu validačních pravidel.
keywords: digna Release 2026.06, digna Python SDK, digna Docker support, automatizace kvality dat, profilování dat, import export validačních pravidel, digna dashboard, platforma pro observabilitu dat, Python API, automatizace metadat
image: /assets/logo_square.png
---

# Změny – Release 2026.06  

S vydáním Release 2026.06 dělá digna výrazný krok vpřed v oblasti automatizace, rozšiřitelnosti a použitelnosti platformy.  
Tato verze představuje nový **digna Python SDK**, oficiální podporu nasazení v **Dockeru**, přepracované uživatelské rozhraní dashboardu a vylepšenou přenositelnost pro správu validačních pravidel.

---

## Nové funkce  

### digna Python SDK – Automatizujte vše pomocí Pythonu  
- Nainstalujte pomocí:
  ```bash
  pip install digna-sdk
  ```
- Programatické řízení a automatizace digna pomocí Pythonu  
- Vytváření a konfigurace projektů přes kód  
- Spouštění inspekcí a monitorovacích běhů  
- Správa datasetů, pravidel a konfigurací programově  
- Profilování tabulek a extrakce metadatických informací  
- Export výsledků profilování a kvality dat do externích repozitářů a systémů  
- Integrace do notebooků, orchestrace nástrojů a CI/CD pipeline  

**Dopad:** Umožňuje plné infrastructure-as-code a hlubokou automatizaci pracovních toků pro kvalitu dat a observabilitu pomocí Pythonu.

---

### Podpora Dockeru – Zjednodušené nasazení a provoz  
- Oficiální podpora Docker image pro digna  
- Rychlé a konzistentní nastavení napříč prostředími  
- Zjednodušené onboarding pro vývoj, testování i produkci  
- Snadná integrace s Kubernetes a kontejnery založenými platformami  
- Zvýšená přenositelnost a reprodukovatelnost nasazení  

**Dopad:** Usnadňuje nasazení a provoz digna v moderních cloud-native architekturách.

---

### QueryMode – Flexibilní strategie vykonávání SQL dotazů

Konfigurujte strategii vykonávání dotazů: **Single** nebo **Combined** režim

**Single Mode**: Každá statistika je vypočtena jedním samostatným SQL dotazem

  - Ideální pro velké datové zdroje, kde hrají roli omezení paměti  
  - Zabraňuje vyčerpání zdrojů při kombinovaných dotazech (např. nedostatek paměti, limity spoolu)  
  - Vyšší počet dotazů, ale nižší paměťová náročnost na dotaz

**Combined Mode**: Všechny statistiky se vypočítávají v rámci jednoho SQL dotazu

  - Snižuje celkový počet dotazů a síťový overhead  
  - Optimalizuje výkon, pokud jsou datové zdroje zvládnutelné v paměti  
  - Efektivnější pro časté, paralelní spuštění

**Dopad:** Dává uživatelům jemnozrnné řízení vykonávání dotazů pro vyvážení výkonu, využití zdrojů a bezpečnost paměti podle charakteristik datového zdroje.

---

### Přepracované uživatelské rozhraní dashboardu  
- Modernizovaný a vylepšený UI/UX design  
- Přehlednější navigace a struktura  
- Lepší viditelnost výsledků monitoringu a přehledů kvality dat  
- Zlepšená čitelnost alertů, statistik a dashboardů  
- Rychlejší přístup k klíčovým provozním informacím  

**Dopad:** Zvyšuje použitelnost a denní produktivitu pro všechny uživatele.

---

### Rozšířený import a export validačních pravidel  
- Vylepšené funkce importu/exportu validačních pravidel  
- Snazší migrace mezi prostředími a projekty  
- Lepší opětovné použití standardizovaných sad pravidel  
- Lepší governance a řízení životního cyklu pravidel  
- Zjednodušená spolupráce mezi týmy  

**Dopad:** Umožňuje škálovatelné a konzistentní řízení kvality dat napříč organizací.

---

## Vylepšení platformy  

- Plná integrace Python SDK pro automatizaci  
- Kontejnerizované nasazení přes Docker  
- Zlepšené UX díky přepracovanému dashboardu  
- Rozšířená přenositelnost validační logiky  

---

## Pro koho je toto vydání určeno  

- Datoví inženýři: automatizace, používání SDK, integrace do pipeline  
- Platformní týmy: zjednodušené nasazení přes Docker  
- Týmy pro správu dat (Data Governance): spravovatelné a znovupoužitelné validační pravidla  
- Analytické týmy: lepší použitelnost a viditelnost přehledů  

---

## Aktualizace CLI  
- Přidána podpora integrace SDK  
- Vylepšené workflowy importu/exportu  
- Obecná zlepšení stability a výkonu
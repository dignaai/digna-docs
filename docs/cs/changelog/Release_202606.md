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

## Podívejte se na vydání

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — průvodce tímto vydáním na YouTube kanálu digna.*

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

### Konfigurovatelný predikční model

Model, na němž stojí detekce anomálií, nyní zvažuje konkurenční vysvětlení každé řady – vzor v kombinaci s vyhodnocením nejnovějších pozorování – a kombinuje jejich předpovědi podle toho, jak silně je každé z nich podložené. Jediná extrémní hodnota již nemůže prosakovat do následujících predikcí.

Řídí jej dvě nastavení na nové záložce **Model** datového zdroje, každé v rozsahu od `0.0` do `1.0` s výchozí hodnotou `0.5`:

- **Break Sensitivity** – jak rychle je skok na novou úroveň nebo obrat trendu přijat jako skutečný, místo aby byl považován za odlehlé hodnoty
- **Model Complexity** – kolik struktury model hledá, od kalendářních efektů a jediného posunu úrovně až po neznámé cykly, efekty dne v měsíci a měsíční resety

Obě lze kdykoli vrátit na výchozí hodnoty. Jak každé z nich působí, najdete v části [Nastavení modelu](../platform/data_anomalies/how_it_works.md#model-settings).

**Dopad:** Dává uživatelům kontrolu nad samotným predikčním modelem, vedle stávajících nastavení Sensitivity a Memory pro pásmo tolerance, která jsou nyní na záložce **Thresholds**.

---

### Řízení notifikací o anomáliích

- Nová záložka **Notifications** v nastavení anomálií datového zdroje:
  - **Minimum Alerts** – kolik neúspěšných kontrol (nikoli nejistých) musí inspekce mít, než je odeslána notifikace (výchozí `1`)
  - **Pause After Notification (Days)** – jak dlouho odběr po notifikaci o datovém zdroji mlčí (výchozí `0`, bez pauzy)
- Odběratelé jsou nyní upozorněni, když inspekce zcela selže (**Notify Inspection Errors**)
- Každá notifikace odkazuje přímo na stránku, které se týká – na neúspěšné kontroly inspekce nebo na zobrazení Schema Tracker a Timeliness
- Přehlednější přepínače odběru: **Notify on Passed Inspections**, **Notify Inspection Errors**, **Notify Data Volume Checks**

**Jak notifikace fungují:** notifikace se odesílají prostřednictvím **notifikačních kanálů** – Email (přes SMTP připojení), Slack nebo Jira –, které nastavují administrátoři a mohou je ověřit pomocí **Test Notification Channel**. **Odběr** propojuje kanál s projektem: pokrývá všechny nebo vybrané datové zdroje a jeho přepínače určují, o čem informuje – o každém modulu (Data Anomalies, Data Validation, Data Analytics, Timeliness, Schema Tracker a kontroly objemu dat), o inspekcích, které zcela selžou, a volitelně také o úspěšných inspekcích.

**Dopad:** Méně notifikací, ale s vyšší vypovídací hodnotou – izolované odchylky a přetrvávající anomálie již nezahlcují kanál.

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
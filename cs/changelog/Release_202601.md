# Záznam změn – Vydání 2026.01  

Ve vydání 2026.01 představuje digna zásadní vylepšení modelování zdrojů dat, správy připojení a použitelnosti inspekcí.  
Toto vydání zvyšuje flexibilitu napříč všemi moduly a výrazně rozšiřuje pokrytí kvality a validace dat.

---

## Nové funkce  

### Globální připojení k databázím  
- Připojení k databázím jsou nyní konfigurována na **globální úrovni**.  
- Globální připojení lze znovu použít napříč **všemi projekty**, což zjednodušuje konfiguraci a údržbu.  
- **Dopad:** Snižuje provozní režii a zajišťuje konzistentní konektivitu napříč prostředími.

### Více zdrojových připojení v rámci projektu  
- Projekty nyní mohou odkazovat na **více konfiguračních připojení zdrojů**.  
- Umožňuje flexibilnější nastavení pro složité datové architektury projektu.  
- **Dopad:** Podporuje reálné podnikové architektury s heterogenními zdroji dat.

### Logické zdroje dat  
- Zdroje dat nyní představují **logickou vrstvu** v rámci projektu.  
- Každý zdroj dat může být podložen:
    - **tabulkou v databázi**
    - **pohledem v databázi**
    - **vlastním SQL dotazem**  
- Toto oddělení zlepšuje znovupoužitelnost, přehlednost a modelování inspekcí napříč moduly.  
- **Dopad:** Odděluje inspekce a pravidla kvality dat od fyzického úložiště, čímž zlepšuje udržovatelnost a opětovné použití.

### Podmínka relevance anomálie  
- Nyní lze definovat **Podmínku relevance anomálie** pro řízení vyhodnocování stavu anomálie na úrovni datové sady.  
- Statistiky se počítají nezávisle na tom, zda je podmínka nastavena nebo splněna.  
- Pokud podmínka **není splněna**, **digna Data Anomalies** neposkytuje stav anomálie (zelená / žlutá / červená).  
- **Příklad:** Vyloučit datovou sadu z vyhodnocování anomálií, pokud je počet záznamů menší než 10.  
- **Dopad:** Zajišťuje, že anomálie jsou vyhodnocovány pouze v relevantních obchodních kontextech.

### Konfigurace notifikací pro jednotlivé moduly  
- Notifikace lze nyní konfigurovat **pro jednotlivé moduly** přímo v digna.  
- Umožňuje nezávislé řízení chování upozornění pro **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** a další moduly.  
- **Dopad:** Umožňuje přesné strategie upozornění sladěné s odpovědnostmi týmů a kritičností.

### Export výsledků inspekcí (CSV)  
- Uživatelé si nyní mohou **stáhnout výsledky inspekcí jako CSV soubory**.  
- Umožňuje offline analýzu, reporting a integraci s externími nástroji.  
- **Dopad:** Zjednodušuje audity, reportování a následnou analýzu kvality dat.

---

## Rozšířené možnosti validace dat  

S tímto vydáním nyní **digna Data Validation** podporuje komplexní sadu pravidel kvality dat:

- **Pravidla validace na úrovni řádku**  
- **Kontroly jedinečnosti napříč více sloupci**  
- **Validace referenční integrity napříč zdroji dat**

Tyto kontroly dohromady umožňují vynucení **strukturálních a relačních pravidel kvality dat** napříč složitými datovými prostředími.

### Kontroly jedinečnosti pro více sloupců
- Představeny **Kontroly jedinečnosti** pro konfigurovatelnou **sadu sloupců**.  
- Umožňuje validaci složených klíčů a obchodních pravidel jedinečnosti.  
- **Dopad:** Detekuje duplicitní obchodní entity, které nelze identifikovat pomocí kontrol jednotlivých sloupců.

### Kontroly referenční integrity
- Představeny **Kontroly referenční integrity** pro ověření vztahů mezi zdroji dat.  
- Zajišťují, že hodnoty cizích klíčů ve zdrojové datové sadě existují v odkazované cílové datové sadě.  
- Pomáhají včas odhalit sirotčí záznamy, přerušené vazby a problémy s konzistencí dat.  
- Navrženo tak, aby fungovalo s **logickými zdroji dat**, včetně pohledů a vlastních SQL dotazů.  
- **Případy použití:** integrita datového skladu, regulatorní reporting, konzistence hlavních dat a spolehlivá následná analytika.

---

## Komu toto vydání pomůže  

- **Datoví inženýři:** Flexibilnější modelování zdrojů dat a znovupoužitelná databázová připojení  
- **Týmy pro kvalitu a správu dat:** Rozšířené pokrytí validace včetně pravidel referenční integrity  
- **Týmy pro analytiku a BI:** Čistší vstupy a exportovatelné výsledky inspekcí  
- **Správci platformy:** Snížená složitost konfigurace a lepší provozní udržovatelnost

---

## Aktualizace CLI  
- Žádné změny

---
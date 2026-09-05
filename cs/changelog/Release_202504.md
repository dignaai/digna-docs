# Záznam změn – Vydání 2025.04

Ve vydání 2025.04 dělá digna výrazný krok vpřed v tom, aby byla správa kvality dat a observability jednodušší, transparentnější pro týmy a dostupnější pro uživatele po celém světě.  
Toto vydání kombinuje **silné nové funkce**, **vylepšení automatizace pracovních postupů** a **zdokonalení uživatelského prostředí**.  

---

## Nové funkce

### Inspection Hub – nové centrum řízení
**Inspection Hub** je nyní dostupný jako centrální místo pro správu všech vašich inspekčních úloh. Místo přepínání mezi různými moduly nebo spoléhání se pouze na spuštění z příkazové řádky můžete nyní monitorovat a řídit inspekce z jednoho zjednodušeného rozhraní.  

Klíčové možnosti zahrnují:  
- Inspekce na požádání: Spouštějte nové úlohy okamžitě vždy, když potřebujete čerstvé výsledky.  
- Historie inspekcí: Zobrazte časovou osu inspekcí — co bylo spuštěno, kdo to spustil a kdy.  
- Sledování stavu: Úlohy jsou jasně označené jako dokončené, probíhající nebo čekající.  
- Informace o iniciátorovi: Rychle zjistěte, zda byla inspekce spuštěna uživatelem, naplánovačem nebo CLI.  
- Nástroje pro úklid: Odstraňujte zastaralé nebo nepotřebné úlohy a udržujte pracovní prostor přehledný.  
- Podrobné logy: Prozkoumejte každou úlohu do detailu — jak dlouho trvala, které zdroje byly zahrnuty a jak byly aplikovány prahy.  

Inspection Hub dává týmům **komplexní přehled a kontrolu**, což usnadňuje správu inspekcí v rozsáhlých projektech.  

---

### Vícejazyčná podpora – digna mluví vaším jazykem
digna je nyní připravena pro mezinárodní týmy zavedením **vícejazyčné podpory**.  

V tomto vydání si můžete v **Uživatelských předvolbách** nastavit svůj **preferovaný jazyk rozhraní**. Podporované jazyky zahrnují:  
- angličtina (UK, US, CA, AU)  
- němčina (DE, AT, CH)  
- polština (PL)  

To činí digna snazší k používání pro vícejazyčné organizace a zajišťuje hladší adopci napříč týmy pracujícími v různých regionech. Další jazyky budou přidány v následujících vydáních.  

---

### Import a export datových zdrojů – jednoduchá konfigurace
Konzistence mezi prostředími je v enterprise nasazeních zásadní. S verzí 2025.04 představuje digna **import/export datových zdrojů** přes **dignacli**, nástroj příkazové řádky pro pokročilé uživatele.  

Výhody:  
- Exportujte konfiguraci datového zdroje jednou a poté ji znovu použijte napříč vývojem, testováním a produkcí.  
- Odstraňte ruční pře-konfigurace a vyhněte se nákladným chybám.  
- Podpora automatizovaných workflow a CI/CD pipeline pomocí jednoduchých příkazů CLI (`export-ds` a `import-ds`).  
- Rychle kopírujte datové zdroje mezi projekty pro snazší spolupráci.  

Tato funkce zajišťuje, že týmy mohou nasazovat s jistotou, protože konfigurace jsou konzistentní v každém prostředí.  

---

### Module Analytics (v1) – od detekce k porozumění
digna vznikla jako platforma pro detekci anomálií a monitorování kvality dat. S vydáním 2025.04 pokračuje v evoluci s **prvním vydáním Module Analytics**.  

Module Analytics pomáhá uživatelům **lépe porozumět svým datům** místo pouhého reagování na problémy. S tímto novým modulem můžete:  
- Sledovat dlouhodobé trendy ve vašich datových sadách.  
- Detekovat a monitorovat volatilitu pro pochopení výkyvů.  
- Prozkoumávat chování dat v čase pro hlubší kontext.  

Například digna může automaticky zvýraznit, že *“Počet řádků se od začátku roku zvýšil o 15,8 %.”*  
Žádné SQL dotazy, žádné manuální kontroly — jen **konkrétní poznatky na první pohled**.  

To je základ cesty digna směrem k pokročilé datové analytice, který umožní týmům přejít z reaktivního na proaktivní monitorování.  

---

### Vylepšení dashboardu – plynulejší uživatelský zážitek
Kromě hlavních funkcí obsahuje vydání 2025.04 několik **vylepšení dashboardu**, která mají za cíl učinit digna intuitivnější a příjemnější:  
- Rychlejší navigace mezi projekty a inspekcemi.  
- Čistší rozložení pro logy inspekcí a podávání úloh.  
- Jemné designové úpravy, které vám pomohou rychleji nalézt poznatky.  

Tato vylepšení vycházejí přímo z feedbacku zákazníků a ukazují náš trvalý závazek vytvářet digna **platformu postavenou pro každodenní použití**.  

---

## Obecná vylepšení
- Optimalizace výkonu pro inspekční úlohy nad rozsáhlými datovými sadami.  
- Vylepšené zpracování chyb v dignacli, které poskytuje jasnější zpětnou vazbu.  
- Stabilita pro projekty s mnoha současně běžícími úlohami.  
- UI úpravy pro filtrování logů úloh a správu projektů.  

---

## Shrnutí
Vydání 2025.04 je o **kontrole, dostupnosti a přehledu**.  

- Nový **Inspection Hub** dává uživatelům plný přehled o inspekčních úlohách.  
- **Vícejazyčná podpora** zajišťuje, že digna může být používána globálními týmy.  
- Funkce **import/export** zjednodušuje správu konfigurací mezi prostředími.  
- **Module Analytics (v1)** přesouvá zaměření od detekce k porozumění díky sledování trendů a volatility.  
- **Vylepšení dashboardu** zpřehledňují celkový uživatelský zážitek.  

Tyto aktualizace společně dělají digna silnější, uživatelsky přívětivější a připravenější pro mezinárodní nasazení než kdy dříve.
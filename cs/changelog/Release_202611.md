# Změny – Release 2026.11  

Release 2026.11 stojí na třech zásadních novinkách:

- **digna Data Reconciliation**: kontroluje, že data zůstávají konzistentní při přesunu mezi systémy  
- **digna Agentic**: otevírá digna AI agentům prostřednictvím digna MCP Server  
- **digna Engine**: volitelně profiluje data přímo v digna a umožňuje kontroly referenční integrity mezi různými databázovými technologiemi  

digna Data Reconciliation a digna Agentic jsou dodávány jako beta verze.

---

## Nové funkce  

### digna Data Reconciliation – Konzistence od zdroje k cíli  
Než se data dostanou do reportu, často projdou několika systémy. digna Data Reconciliation porovnává **cílový** datový zdroj se **zdroji**, ze kterých vznikl, a upozorní, když spolu přestanou souhlasit.

- Konfiguruje se jako pojmenovaná pravidla na nové záložce **Data Reconciliation** cílového datového zdroje  
- Zdrojem může být jakýkoli datový zdroj projektu se zapnutou funkcí Data Reconciliation  
- Mezi případy použití patří standardní rekonciliační postupy a validace výsledků ETL procesů  
- Dva typy pravidel: **Exact** a **AI**  

**Pravidla Exact – Rekonciliace jako pravidlo kvality dat**: přesně definujete, co musí souhlasit mezi jedním zdrojem a jedním cílem, stejně jako u pravidla kvality dat.

  - Porovnání jednoho zdrojového datového zdroje s jedním cílovým datovým zdrojem  
  - Spárování kontroly cíle s kontrolou zdroje podle statistiky a atributu, např. počty řádků nebo součet sloupce s částkou  
  - Povolení rozdílu s **absolute** tolerancí (např. ± 10) nebo **relative** tolerancí (např. ± 0,5 % hodnoty zdroje)  
  - Časová osa zobrazuje rozdíl za každý den vůči toleranci  

**Pravidla AI – Rekonciliace jako observabilita dat**: digna se učí, jak cíl sleduje své zdroje, stejně jako digna pozoruje data v ostatních modulech, a upozorní, když se tento vztah naruší.

  - Kombinace kontrol z několika zdrojových datových zdrojů s kontrolami jednoho cíle  
  - Logiku mezi nimi (joiny, filtry, agregace) není třeba znát ani zapisovat  
  - Model se z historie učí, jak cíl sleduje své zdroje v tentýž den  
  - Každá kontrola cíle je predikována z hodnot zdrojů za daný den a digna upozorní, když cíl opustí pásmo vlastních minulých chyb pravidla  
  - Každé pravidlo má vlastní **Model settings**: **Sensitivity**, **Memory** a **Model Complexity**  

Rekonciliační kontroly se zobrazují na dashboardu s časovou osou pro každé pravidlo. Započítávají se do celkového stavu inspekce a spouštějí notifikace.

**Dopad:** Pokrývá obě strany rekonciliace. Pravidla Exact vynucují známé kontroly mezi zdrojem a cílem a pravidla AI monitorují složité toky, jako jsou ETL procesy, takže data ztracená nebo změněná po cestě jsou zachycena bez ručně psaného rekonciliačního SQL.

---

### digna Agentic – digna pro AI agenty  
První verze digna Agentic. AI agenti nyní mohou s digna pracovat, odpovídat na obchodní otázky o vašich datech a pomáhat vylepšovat vaši konfiguraci.

**digna MCP Server**: umožňuje Claude a dalším AI agentům pracovat s digna prostřednictvím Model Context Protocol.

  - Správa projektů, datových zdrojů, pravidel, plánů inspekcí a odběrů  
  - Čtení stavů inspekcí až na úroveň jednotlivé kontroly pro vyšetřování alertů  

**Popisy datových zdrojů a atributů**: popište běžným jazykem, co datový zdroj nebo atribut obsahuje.

  - AI agenti používají popisy k interpretaci vašich dat  
  - Pokládejte obchodní otázky o svých datech a AI agenti na ně odpovědí na základě toho, co digna monitoruje  
  - Pokud současná konfigurace digna na otázku odpovědět nedokáže, AI agent tam, kde je to možné, navrhne změny datového zdroje a jeho atributů, např. přidání nového datasetu  

**Dopad:** Umožňuje pokládat obchodní otázky o vašich datech běžným jazykem a nechat AI agenty pomáhat s konfigurací digna a s vyšetřováním problémů s kvalitou dat.

---

### digna Engine – Profilujte tam, kde si zvolíte  
Ve výchozím nastavení digna profiluje data tam, kde se nacházejí, tedy ve zdrojové databázi. digna Engine přidává další možnost: digna data ze zdroje exportuje a profiluje je uvnitř digna Engine.

- Volitelné, nikoli povinné: profilování ve zdrojové databázi zůstává k dispozici  
- Volí se pro každé databázové připojení jako jeho **místo profilování**: **Source Database** nebo **digna Engine**  
- K dispozici pro všechny podporované zdrojové technologie  

**Referenční integrita napříč připojeními**: některé kontroly vyžadují export dat. Pro tyto případy digna Engine rozšiřuje **digna Data Validation**.

  - **Kontroly referenční integrity** mezi datovými zdroji na **různých databázových připojeních**, včetně různých databázových technologií (např. Oracle a PostgreSQL)  
  - Funguje s oběma místy profilování: u Source Database se do digna Engine exportují pouze klíčové sloupce  
  - Dashboard zobrazuje, když kontrola běží napříč dvěma připojeními  

**Dopad:** Umožňuje zvolit, kde se data profilují, a vynucuje vztahy mezi systémy, které běží na různých databázových technologiích.

---

## Vylepšení profilování  

Toto vydání také dává uživatelům větší kontrolu nad tím, co a jak se profiluje.

### Dotazové atributy – Uživatelsky definované sloupce  
- Definice umělých sloupců: SQL výraz nad jedním nebo více sloupci datového zdroje  
- Každý dotazový atribut má vlastní název  
- Profiluje se a kontroluje jako jakýkoli jiný atribut  

### Kategorie sloupců DATE  
- Nová kategorie **Date** pro atributy  
- Metriky vztažené k inspektovanému datu  

### Profilování na vyžádání  
- Profilování libovolného atributu nad úplným snímkem jednoho data, bez spuštění inspekce  
- Pomáhá nastavit typ sloupce atributu: **Numerical**, **Categorical**, **Date** nebo **Unspecified**  

---

## Pro koho je toto vydání určeno  

- **Datoví inženýři:** validace výsledků ETL pomocí digna Data Reconciliation  
- **Finanční, rizikové a controllingové týmy:** standardní rekonciliační postupy jako pravidla Exact v digna Data Reconciliation  
- **Týmy pro kvalitu dat a Data Governance:** referenční integrita napříč databázovými technologiemi pomocí digna Engine  
- **Obchodní uživatelé:** odpovědi AI agentů na obchodní otázky o datech pomocí digna Agentic  
- **Týmy pro AI a automatizaci:** AI agenti pracující s digna prostřednictvím digna Agentic  

---

## Aktualizace CLI  
- Beze změn  

---
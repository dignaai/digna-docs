# Data Schema Tracker – Monitorování evoluce schématu
<h1 style="display:none;">Modul řízený AI pro observabilitu metadat a kvalitu dat – digna Data Schema Tracker</h1>

---

## Účel

The **Data Schema Tracker** vás informuje o tom, jak se vyvíjejí struktury vaší databáze.  
Průběžně monitoruje **schémata tabulek, sloupce a datové typy** a detekuje **schema drift** — úmyslné i neúmyslné strukturální změny, které mohou narušit pipeline, ETL úlohy nebo BI dashboardy.

Zajištěním přehlednosti evoluce schémat pomáhá digna organizacím udržet **důvěru v kvalitu dat**, zachovat **observability datových systémů** a předejít nákladným incidentům v produkci způsobeným nezaznamenanými změnami schématu.

---

## Technický přehled

### Co monitoruje

- **Přidané nebo odstraněné sloupce** – Detekuje nově zavedené, přejmenované nebo smazané sloupce.  
- **Změny datových typů** – Identifikuje změny jako `INT → VARCHAR` nebo `DATE → TIMESTAMP`.  
- **Úpravy tabulek a view** – Sleduje vytvoření, přejmenování nebo odstranění tabulek a view.  
- **Rozdíly mezi prostředími** – Porovnává verze schémat mezi Dev, Test a Production prostředími.  

### Detekce a upozornění

- Prohledává **metadata databáze** nebo **systémové katalogy** přímo ve vaší datové platformě.  
- Porovnává každý snímek schématu s předchozí známou verzí uloženou v digna observability schema.  
- Generuje **okamžitá upozornění** na dashboardu, přes API nebo do externích notifikačních kanálů (email, Slack, webhook).  
- Loguje každou verzi schématu pro **historické sledování a připravenost na audit**.

---

## Architektura a provádění

- **Spuštění v databázi:** digna běží zcela ve vašem prostředí a dotazuje se na metadata views, aniž by extrahovalo jakákoliv uživatelská data.  
- **Lehký scanning:** přistupuje pouze k strukturálním informacím — nikdy k uživatelským datům.  
- **Centralizované úložiště:** metadata schémat a záznamy o driftech jsou uloženy v digna observability schema pro vizualizaci a analýzy.  
- **Automatizace:** podporuje plánované i event-driven skeny přes digna Core nebo externí orchestrace.

---

## Příklady použití

| Use Case | Description |
|-----------|--------------|
| **ETL Stability Monitoring** | Detekujte změny struktury upstream před tím, než pipeline selžou kvůli neshodám schématu. |
| **Business Intelligence Reliability** | Zabraňte rozbitým dashboardům způsobeným přejmenovanými nebo chybějícími sloupci. |
| **Data Warehouse Governance** | Udržujte auditovatelnou historii evoluce schématu pro shodu a analýzu dopadů. |
| **Integration Oversight** | Zajistěte, aby schémata datového jezera a datového skladu zůstala synchronizovaná po strukturálních aktualizacích. |

---

## Výhody

| Area | Benefit |
|------|----------|
| **Data Quality** | Předejde nezaznamenanému driftu schématu, který může poškodit nebo zpřesnit validitu datových pipeline. |
| **Observability** | Přidává strukturální monitoring do celkové observability datových ekosystémů. |
| **Compliance** | Udržuje verzované historie schémat pro audit, dohledatelnost a řízení změn. |
| **Prevention** | Detekuje strukturální problémy dříve, než se rozšíří do reportingu nebo produkčních chyb. |

---

## Jak to funguje

1. **Sběr snapshotu** – digna zachytí aktuální metadata schématu.  
2. **Porovnání** – nový snapshot je porovnán
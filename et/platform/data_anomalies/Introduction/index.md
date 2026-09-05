# Data Anomalies – Automated Detection
<h1 style="display:none;">AI-põhine moodul andmekvaliteedi ja nähtavuse jaoks – digna Data Anomalies</h1>

---

## Eesmärk

**Data Anomalies** moodul tuvastab automaatselt ebakorrapärasusi sinu andmekogudes — reegleid kirjutada ei ole vaja.  
See jälgib pidevalt **andmete edastuse kvaliteeti**, õppides ära, milline on „tavaline“, ning tuvastades reaalajas kõrvalekaldeid.

AI-põhise tuvastuse abil märkab digna vaikseid andmevigu, nagu puuduvad, duplikaatsed või rikutud kirjed, mis võivad moonutada aruandeid, ML-mudeleid ja juhtplaate.

---

## Tehniline ülevaade

### Analüüsitavad mõõdikud

digna profiilib pidevalt järgmisi andmeaspekte:

- **Kirjete maht** – ridade koguarv, päevapõhine või partiipõhine  
- **Puuduvad väärtused** – nullide või tühjade väljade tuvastus  
- **Jaotused ja histogrammid** – andmete kuju muutuste jälgimine  
- **Väärtuste vahemikud** – automaatne äärmuslike või väljaspool oodatud vahemikku jäävate väärtuste tuvastus  
- **Ainulaadsus** – kontrollid duplikaatvõtmete või korduvate kirjete kohta  

### Intelligente anomaaliatuvastus

- Kasutab **ajaloolist õppimist**, et dünaamiliselt määratleda eeldatavad piirid  
- Tuvastab kõrvalekaldeid **mahus, väärtuste jaotustes või loogilistes seostes**  
- Rakendab AI-d, et automaatselt kohandada läveväärtusi päevaaja või hooajaliste mustrite alusel  
- Eristab **statistilisi kõikumisi** tõelistest anomaaliatest  
- Toob iga andmekogu ja veeru kohta üksikasjalikud mõõdikud ja usaldusväärtused  

---

## Tuvastussituatsioonid

Allpool on näited reaalsetest probleemidest, mida **Data Anomalies** moodul automaatselt tabab:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | Päevaste tehingute poole kadumine, duplikaatsed partii laadimised või järsud andmealad |
| **Missing or null values** | Andmeekstraktsioonid lõpetati, kuid olulised veerud jäid tühjaks |
| **Distribution drifts** | Keskmine ostusumma või tehingute arv regiooniti muutub ootamatult |
| **Column swaps** | Veerud nagu *first_name* ja *last_name* vahetati ETL-i ajal kogemata |
| **Unexpected categorical values** | nt „Zurich“ ilmub Austria linnade nimekirjas |
| **Sudden uniqueness loss** | Varem unikaalsed ID-d hakkavad duplikeeruma ülesvoolu liitumisvigade tõttu |

---

## Arhitektuur ja täitmine

- **Andmebaasisiseselt täidetav:** Kogu anomaaliatuvastuse loogika käivitub *andmebaasi mootoris* (Teradata, Snowflake, Databricks, PostgreSQL jne.)  
- **Andmete liigutamiseta:** digna loeb ainult mõõdikuid, ei liiguta kunagi toorandmeid väljaspool süsteemi  
- **Inkrementaalsed uuendused:** Iga käivitus analüüsib efektiivsuse huvides ainult uusi andmesegmenti  
- **Konfigureeritav inspekteerimise sagedus:** Tunnipõhine, päevane või käivitatud ülalkgnevate protsesside poolt  
- **Tulemuste salvestus:** Mõõdikud ja anomaaliamärgid kirjutatakse tagasi digna observability skeemi visualiseerimiseks ja alarmideks  

---

## Kasud

| Area | Benefit |
|------|----------|
| **Automation** | Kaotab vajaduse sadade manuaalsete SQL- või reeglimääratluste järele |
| **Precision** | Tuvastab probleeme, mida staatilised läved sageli ei märka |
| **Scalability** | Jälgib efektiivselt miljoneid kirjeid ühe tabeli kohta |
| **Integration** | Töötleb sujuvalt koos *digna Data Analytics* trendianalüüsi jaoks |
| **Compliance** | Tagab pideva kontrolli **andmete kvaliteedi ja nähtavuse** üle |
| **Transparency** | Pakub iga anomaalia kohta usalduskoode, ajatempleid ja põhjakoodide selgitusi |

---

## Kuidas digna õpib „tavalist“

1. **Profiling phase:** digna kogub mõõdikuid ajaloolistest andmekogudest.  
2. **Learning phase:** AI-mudelid tuvastavad korduvaid mustreid (hooajalised, nädalapõhised, päevapõhised).  
3. **Monitoring phase:** Tulevasi andmekogusid võrreldakse dünaamiliselt õpitud läveväärtustega.  
4. **Alerting phase:** Statistilise usalduspiiri ületavad kõrvalekalded tõstetakse anomaaliatena.

Kõik mudelid on seletatavad, deterministlikud ja optimeeritud ettevõttekasutuse andmemahtudele.

---

## Näidispõhised kasutusjuhtumid

- Andmekvaliteedi jälgimine **pangatehingute süsteemides**  
- Laadimisvigade tuvastamine **ETL-i või andmeladude töödes**  
- Ebatavalise kliendikäitumise avastamine **telekommunikatsiooni kirjetes**  
- Kliiniliste andmete järjepidevuse jälgimine **terviseanalüüsi torustikes**  
- Purunemise vältimine juhtpaneelidel **BI ja aruandluskeskkondades**

---

## Korduma kippuvad küsimused

**Kas Data Anomalies nõuab eeldefineeritud reegleid?**  
Ei — moodul õpib käitumisest automaatselt.

**Kas ma saan siiski määratleda spetsiifilisi läveväärtusi, kui vaja?**  
Jah. digna võimaldab kombineerida AI-põhist ja reegel-põhist tuvastust (kaudu *Data Validation*).

**Kuidas vähendatakse valepositiivseid?**  
Moodul kasutab adaptiivset õppimist ja statistilist usaldushindamist, et ignoreerida tavalisi hooajalisi kõikumisi.

**Kus toimub arvutus?**  
Kogu töötlus käib sinu andmebaasis — digna ei ekstraheeri toorandmeid.

**Kas see sobib tundlikele või reguleeritud andmetele?**  
Jah. digna töötab täielikult **on-premises või privaatpilves** ning järgib Euroopa nõuetele vastavust.

---
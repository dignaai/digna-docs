# Muudatused – väljalase 2026.01  

Versiooniga 2026.01 toob digna olulisi täiustusi andmeallikate modelleerimisse, ühenduste haldamisse ja inspekteerimise kasutatavusse.  
See väljalase suurendab paindlikkust kõigis moodulites ja laiendab oluliselt **andmekvaliteedi ja valideerimise ulatust**.

---

## Uued funktsioonid  

### Globaalsed andmebaasiühendused  
- Andmebaasiühendused konfigureeritakse nüüd **globaalsel tasemel**.  
- Globaalseid ühendusi saab taaskasutada **kõikides projektides**, lihtsustades seadistust ja hooldust.  
- **Mõju:** Vähendab operatiivset koormust ja tagab järjepideva ühenduvuse eri keskkondades.

### Mitmed allikaühendused projekti kohta  
- Projektid võivad nüüd viidata **mitmele allikaühenduse konfiguratsioonile**.  
- Võimaldab keerukamate andmaalaste jaoks paindlikumaid seadistusi.  
- **Mõju:** Toetab reaalseid ettevõtte arhitektuure, kus kasutatakse heterogeenseid andmeallikaid.

### Loogilised andmeallikad  
- Andmeallikad esindavad nüüd projekti sees **loogilist kihti**.  
- Iga andmeallikas võib toetuda:
    - **andmebaasi tabelile**
    - **andmebaasi vaatele**
    - **kohandatud SQL-lausele**  
- See eristamine parandab taaskasutust, selgust ja inspekteerimise modelleerimist erinevates moodulites.  
- **Mõju:** Eraldab inspekteerimised ja andmekvaliteedi reeglid füüsilisest salvestusest, parandades hooldatavust ja taaskasutust.

### Anomaalia asjakohasuse tingimus  
- Nüüd saab määratleda **Anomaalia asjakohasuse tingimuse**, et kontrollida anomaalia staatuse hindamist andmekogu tasemel.  
- Statistika arvutatakse sõltumatult sellest, kas tingimus on määratud või täidetud.  
- Kui tingimus **ei ole täidetud**, ei anna **digna Data Anomalies** anomaaliastaatust (roheline / kollane / punane).  
- **Näide:** Jäta andmekogu anomaaliate hindamisest välja, kui kirjete arv on alla 10.  
- **Mõju:** Tagab, et anomaaliaid hinnatakse vaid äriliselt asjakohastes kontekstides.

### Teavituste seadistus mooduli kaupa  
- Teavitusi saab nüüd konfigureerida **iga mooduli jaoks eraldi** otse digna-s.  
- Võimaldab sõltumatult juhtida häirekäitumist moodulite, nagu **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** jt jaoks.  
- **Mõju:** Lubab täpseid alarmistrateegiaid, mis vastavad meeskondade vastutusaladele ja kriitilisusele.

### Inspektsiooni tulemuste eksport (CSV)  
- Kasutajad saavad nüüd **laadida inspektsiooni tulemusi CSV-failidena**.  
- Võimaldab offline-analüüsi, aruandlust ja integratsiooni välistesse tööriistadesse.  
- **Mõju:** Lihtsustab auditeid, aruandlust ja edasi suunatud andmekvaliteedi analüüsi.

---

## Laiendatud andmevalideerimise võimalused  

Selle väljalasega toetab **digna Data Validation** nüüd põhjalikku komplekti andmekvaliteedi reegleid:

- **Rea-taseme valideerimisreeglid**  
- **Mitmeveeruline ainulaadsuse kontroll**  
- **Viitelise terviklikkuse kontrollid andmeallikate vahel**

Koos võimaldavad need kontrollid kehtestada **struktuurseid ja relatsioonilisi andmekvaliteedi reegleid** keerukates andmaalastes.

### Mitme veeru ainulaadsuse kontrollid
- Lisatud **ainulaadsuse kontrollid** konfigureeritava **veerukogumi** jaoks.  
- Võimaldab valideerida liitud võtmeid ja ärilistest reeglitest tulenevaid ainulaadsuspiiranguid.  
- **Mõju:** Avastab dubleeritud ärilisi üksusi, mida ühe veeru kontrolliga ei tuvastata.

### Viitelise terviklikkuse kontrollid
- Lisatud **viitelise terviklikkuse kontrollid**, et valideerida suhteid andmeallikate vahel.  
- Tagab, et **välisvõtme väärtused** allika andmeallikas eksisteerivad viidatud sihtandmeallikas.  
- Aitab varakult tuvastada hüljatud kirjeid, katkiseid seoseid ja andmete järjepidevuse probleeme.  
- Disainitud töötama koos **loogiliste andmeallikatega**, hõlmates vaateid ja kohandatud SQL-päringuid.  
- **Kasutusjuhtumid:** andmehoidla terviklikkus, regulatiivne aruandlus, põhiandmete järjepidevus ja usaldusväärne edasi suunatud analüütika.

---

## Kes sellest väljalasest kasu saab  

- **Andmeinsenerid:** paindlikum andmeallikate modelleerimine ja taaskasutatavad andmebaasiühendused  
- **Andmekvaliteedi ja halduse meeskonnad:** laiendatud valideerimise ulatus, sealhulgas relatsioonilise terviklikkuse reeglid  
- **Analüütika ja BI meeskonnad:** puhtamad sisendid ja eksportitavad inspektsiooni tulemused  
- **Platvormi omanikud:** vähenenud seadistuste keerukus ja paranenud operatiivne hooldatavus

---

## CLI uuendused  
- Puuduvad muudatused

---
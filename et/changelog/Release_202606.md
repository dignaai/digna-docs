# Muudatused – Väljalase 2026.06  

Väljalase 2026.06 viib digna olulise sammu edasi automatiseerimise, laiendatavuse ja platvormi kasutusmugavuse osas.  
See versioon toob kaasa uue **digna Python SDK**, ametliku **Docker‑deploy toe**, värskendatud dashboardi kasutajakogemuse ja parema kandepinna valideerimisreeglite haldamiseks.

---

## Vaadake väljalaset

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — ülevaade sellest väljalaskest digna YouTube'i kanalil.*

---

## Uued funktsioonid  

### digna Python SDK – automatiseeri kõik Pythoniga  
- Installi:
  ```bash
  pip install digna-sdk
  ```
- Halda ja automatiseeri dignat programmiliselt Pythoniga  
- Loo ja konfigureeri projekte koodi kaudu  
- Käivita inspectioneid ja monitooringu täitmisi  
- Halda andmekogusid, reegleid ja konfiguratsioone programmiliselt  
- Profiili tabeleid ja eralda metaandmete ülevaateid  
- Eksporti profilingu ja andmekvaliteedi tulemusi välistele repositooriumitele ja süsteemidele  
- Integreeri notebook'ide, orkestratsioonitööriistade ja CI/CD torujuhtmetega  

**Mõju:** Võimaldab täielikku infrastructure-as-code lähenemist ja sügavat automatiseerimist andmekvaliteedi ning observability töövoogudele Pythoniga.

---

### Docker‑toe tugi – lihtsustatud kasutuselevõtt ja haldus  
- Ametlik Docker imagе‑tugi voor digna  
- Kiire ja ühtlane seadistus eri keskkondades  
- Lihtsam onboardimine arenduse, testi ja tootmiskeskkondades  
- Lihtne integreerimine Kubernetes’i ja konteineriplatvormidega  
- Parem kandepind ja taasesitatavus deploy’de puhul  

**Mõju:** Teeb digna lihtsamini juurutatavaks ja hallatavaks kaasaegsetes cloud‑native arhitektuurides.

---

### QueryMode – paindlik SQL‑täitmise strateegia

Seadista päringute täitmise strateegia: **Single** või **Combined** mode

**Single Mode**: Iga statistika arvutatakse ühe eraldiseisva SQL‑päringuga

  - Sobib suurematele andmeallikatele, kus mälupiirangud on olulised  
  - Vältib kombineeritud päringu ressursikulu (mälu lõppemine, spool‑piirangud)  
  - Rohkem päringuid, kuid madalam mälukulu päringu kohta

**Combined Mode**: Kõik statistika arvutused tehakse üheainsa SQL‑päringu sees

  - Vähendab päringute koguarvu ja võrguüleseid kulusid  
  - Optimeeritud jõudluseks, kui andmeallikad mahuvad mällu  
  - Tõhusam sagedaste, paralleelsete täitmiste puhul

**Mõju:** Annab kasutajatele täpse kontrolli päringute täitmise üle, et tasakaalustada jõudlust, ressursikasutust ja mäluturvalisust vastavalt andmeallika omadustele.

---

### Seadistatav ennustusmudel

Anomaaliatuvastuse aluseks olev mudel kaalub nüüd iga aegrea puhul konkureerivaid selgitusi – mustrit koos viimaste vaatluste tõlgendusega – ja kombineerib nende prognoosid vastavalt sellele, kui tugevalt igaüht neist toetatakse. Üksik äärmuslik väärtus ei saa enam järgnevatesse ennustustesse lekkida.

Mudelit juhivad kaks seadet andmeallika uuel vahekaardil **Model**, kumbki vahemikus `0.0` kuni `1.0`, vaikeväärtusega `0.5`:

- **Break Sensitivity** – kui kiiresti hüpet uuele tasemele või pöörduvat trendi usutakse, selle asemel et käsitleda neid erinditena
- **Model Complexity** – kui palju struktuuri mudel otsib, alates kalendriefektidest ja ühest tasemenihkest kuni tundmatute tsüklite, kuupäevaefektide ja igakuiste lähtestamisteni

Mõlemad saab igal ajal vaikeväärtustele taastada. Kuidas kumbki toimib, vaadake jaotisest [Mudeli seaded](../platform/data_anomalies/how_it_works.md#model-settings).

**Mõju:** Annab kasutajatele kontrolli ennustusmudeli enda üle, kõrvuti olemasolevate tolerantsiriba seadetega Sensitivity ja Memory, mis asuvad nüüd vahekaardil **Thresholds**.

---

### Anomaaliate teavituste juhtimine

- Uus vahekaart **Notifications** andmeallika anomaaliaseadetes:
  - **Minimum Alerts** – mitu ebaõnnestunud kontrolli (mitte ebakindlat) peab inspektsioonil olema, enne kui teavitus saadetakse (vaikimisi `1`)
  - **Pause After Notification (Days)** – kui kaua tellimus pärast andmeallika kohta teavitamist vaikib (vaikimisi `0`, pausi pole)
- Tellijaid teavitatakse nüüd, kui inspektsioon täielikult ebaõnnestub (**Notify Inspection Errors**)
- Iga teavitus viib otse lehele, mida see puudutab – inspektsiooni ebaõnnestunud kontrollideni või Schema Trackeri ja Timeliness vaadeteni
- Selgemad tellimuse lülitid: **Notify on Passed Inspections**, **Notify Inspection Errors**, **Notify Data Volume Checks**

**Kuidas teavitused toimivad:** teavitused saadetakse **teavituskanalite** kaudu – Email (SMTP-ühenduse kaudu), Slack või Jira –, mille seadistavad administraatorid ja mida saab kontrollida funktsiooniga **Test Notification Channel**. **Tellimus** seob kanali projektiga: see hõlmab kõiki või valitud andmeallikaid ning selle lülitid määravad, millest see teatab – iga moodul (Data Anomalies, Data Validation, Data Analytics, Timeliness, Schema Tracker ja andmemahu kontrollid), täielikult ebaõnnestunud inspektsioonid ning soovi korral ka edukad inspektsioonid.

**Mõju:** Vähem, kuid sisukamaid teavitusi – üksikud kõrvalekalded ja püsivad anomaaliad ei ujuta enam kanalit üle.

---

### Uuendatud dashboardi kasutajakogemus  
- Moderniseeritud ja parandatud UI/UX disain  
- Selgem navigatsioon ja struktuur  
- Paremini nähtavad monitooringu tulemused ja andmekvaliteedi ülevaated  
- Paranenud loetavus alertide, statistika ja dashboardide puhul  
- Kiirem ligipääs olulisele operatiivsele infole  

**Mõju:** Suurendab kasutusmugavust ja igapäevast tootlikkust kõigi kasutajate jaoks.

---

### Valideerimisreeglite import/eksport – laiendatud võimalused  
- Täiustatud import/eksport funktsionaalsus valideerimisreeglitele  
- Lihtsam migratsioon keskkondade ja projektide vahel  
- Paranenud taaskasutus standardiseeritud reegistikomplektide puhul  
- Parema juhtimise ja reeglite elutsükli halduse võimalused  
- Lihtsustatud koostöö meeskondade vahel  

**Mõju:** Võimaldab skaleeritavat ja järjepidevat andmekvaliteedi juhtimist kogu organisatsioonis.

---

## Platvormi täiustused  

- Täielik Python SDK integratsioon automatiseerimiseks  
- Konteineripõhine juurutus Dockeriga  
- Paranenud UX tänu ümberkujundatud dashboardile  
- Laiendatud valideerimisloogika kandepind  

---

## Kellele see väljalase kasulik on  

- Andmeinsenerid: automatiseerimine, SDK‑kasutus, torujuhtmete integratsioon  
- Platvormimeeskonnad: lihtsustatud juurutus Dockeriga  
- Andmejuhtimise meeskonnad: taaskasutatavad valideerimisreeglid ja haldus  
- Analüütikameeskonnad: parem kasutatavus ja nähtavus ülevaadete jaoks  

---

## CLI uuendused  
- Lisatud SDK integratsiooni tugi  
- Parendatud import/eksport töövood  
- Üldised stabiilsuse ja jõudluse parandused
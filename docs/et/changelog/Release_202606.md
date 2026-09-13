---
title: digna Väljalase 2026.06 | Python SDK, Docker-i kasutuselevõtt ja täiustatud valideerimishaldus
description: Tutvuge, mis on uut digna väljalases 2026.06. See versioon toob kaasa uue digna Python SDK, ametliku Docker‑deploy toe, ümberkujundatud dashboardi kasutajakogemuse ja laiendatud import/eksport võimalused valideerimisreeglite haldamiseks.
keywords: digna Release 2026.06, digna Python SDK, digna Docker support, andmekvaliteedi automatiseerimine, andmeprofiling, valideerimisreeglite import export, digna dashboard, data observability platform, Python API, metadata automation
image: /assets/logo_square.png
---

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

Anomaaliatuvastuse aluseks olev mudel on nüüd seadistatav. Seitse parameetrit juhivad, kuidas ennustus sobitatakse:

- Break Sensitivity
- Outlier Sensitivity
- Memory
- Ridge Strength
- Gap Tolerance
- Outlier Correction
- Plausible Range Tightness

Vaikeväärtused sobivad valdavale enamikule aegridadest ja iga parameetri saab igal ajal vaikeväärtusele taastada.

**Mõju:** Annab kasutajatele kontrolli ennustusmudeli enda üle, kõrvuti olemasolevate tolerantsiriba seadetega Sensitivity ja Memory. Juhiste saamiseks, millal mõne parameetri juurde pöörduda ja kuidas seda seadistada, võtke ühendust dignaga.

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
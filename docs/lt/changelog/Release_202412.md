---
title: digna Leidimas 2024.12 | Pakeitimų žurnalas ir naujos funkcijos
description: Sužinokite, kas naujo digna leidime 2024.12. Ši versija pristato integruotą planuotoją, PDF ataskaitas, lanksčias pasirinktines stulpelių tipus, dinamiškus snapshot užklausų vietos žymeklius ir protingesnę ribų optimizaciją, kad pagerintų anomalijų aptikimą ir duomenų kokybės stebėseną.
keywords: digna leidimas 2024.12, digna pakeitimų žurnalas, leidimo pastabos, integruotas planuotojas, PDF ataskaitos, custom column type, snapshot query placeholders, threshold optimization, data observability, data quality monitoring, anomaly detection
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Pakeitimų žurnalas – Leidimas 2024.12

2024.12 leidimas pristato naujų funkcijų ir patobulinimų, kurie daro digna labiau automatizuotą, lanksčią ir paruoštą verslui.  
Ši versija pagerina planavimą, ataskaitų kūrimą, užklausų valdymą ir anomalijų aptikimo tikslumą.  

---

## Naujos funkcijos

### Integruotas planuotojas
Inspekcijos nebepriklauso tik nuo komandų eilutės arba API kvietimų.  
Su **naujuoju digna Scheduler** inspekcijos gali būti vykdomos automatiškai nustatytu laiku.  

- Palaiko **Cron expressions** pasikartojančioms tvarkaraščiams (kasdien, kas savaitę arba pritaikyti intervalai).  
- Siūlo tikslią kontrolę per **offsetus**, **pradžios datas** ir **pabaigos datas**.  
- Leidžia komandoms užtikrinti, kad visi svarbūs duomenų šaltiniai būtų patikrinami nuosekliai ir be rankinių veiksmų.  

---

### PDF formato ataskaitos
Komandos dabar gali lengvai dalintis rezultatais su suinteresuotosiomis šalimis per **PDF eksportus**.  

- Grafikai, metrikos ir anomalijų rezultatai gali būti eksportuoti profesionaliu PDF formatu.  
- Ataskaitos sujungia **vizualizacijas** ir **pagrindinius duomenis**, kad tarnautų tiek techniniams, tiek verslo vartotojams.  
- Pašalina išorinių įrankių poreikį ataskaitoms ruošti.  

---

### Naujas stulpelio tipas: `CUSTOM`
Siekiant didesnio lankstumo, digna pristato naują `CUSTOM` stulpelio tipą.  

- Vartotojai gali tiksliai nurodyti, kurios **statistikos ir metrikos** taikomos konkretiems atributams.  
- Puikiai tinka specialiems atvejams, kurie netelpa į standartines kategorijas, tokias kaip NUMERICAL ar CATEGORICAL.  
- Padeda sutelkti analizę ir išlaikyti rezultatus aktualius verslo kontekstui.  

---

### Nauji vietos žymekliai snapshot užklausose
Snapshot užklausos tapo paprastesnės ir mažiau klaidų linkusios su **dinamiškais vietos žymekliais**.  

- Tokie žetonai kaip `#date+n#` arba `#date-n#` automatiškai koreguoja datas užklausose.  
- Pavyzdys:  
  - `#date+1#` → rytoj  
  - `#date-2#` → prieš du dienas  
- Pašalina rankinius datų skaičiavimus ir užtikrina nuoseklumą tarp komandų.  

---

### Ribų optimizacija
Anomalijų ribos dabar yra protingesnės ir konteksto atsižvelgiančios.  

- Tokiems metrikoms kaip **NULL COUNT**, apatinės ribos automatiškai apribojamos **0**.  
- Neleidžia nustatyti neteisingų ar beprasmių ribų.  
- Sumažina klaidingų teigiamų atvejų skaičių ir pagerina anomalijų aptikimo patikimumą.  

---

## Bendri patobulinimai
- Patobulinti **UI komponentai** projekto ir atributo konfigūracijos rodiniuose.  
- Pagerintas **skydelio veikimas** dirbant su dideliais duomenų kiekiais.  
- Sustiprinta **registracija ir klaidų žinutės** gedimų šalinimui.  

---

## Santrauka
Leidimas 2024.12 sustiprina digna kaip platformą **duomenų kokybei, anomalijų aptikimui ir stebimumui**.  
Su automatizavimu per planuotoją, dalinamomis PDF ataskaitomis, pritaikomais stulpeliais, supaprastintomis snapshot užklausomis ir protingesnėmis ribomis, digna tampa dar vertingesnė tiek techniniams vartotojams, tiek verslo suinteresuotiesiems.
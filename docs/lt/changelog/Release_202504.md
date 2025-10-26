---
title: digna Išleidimas 2025.04 | Inspection Hub, kelių kalbų palaikymas, Module Analytics
description: Sužinokite, kas naujo digna Išleidime 2025.04. Ši versija pristato Inspection Hub, kelių kalbų palaikymą (anglų, vokiečių, lenkų), duomenų šaltinių importą/eksportą per dignacli, pirmąją Module Analytics versiją ir patobulintą prietaisų skydelio patirtį.
keywords: digna Išleidimas 2025.04, digna pakeitimų žurnalas, digna inspection hub, digna kelių kalbų palaikymas, digna module analytics, digna import export, digna CLI, leidimo pastabos, duomenų stebėsena, duomenų kokybės stebėjimas
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Pakeitimų žurnalas – Išleidimas 2025.04

Su Išleidimu 2025.04 digna žengia didelį žingsnį į priekį, kad duomenų kokybės ir stebėsenos valdymas taptų paprastesnis, labiau skaidrus komandoms ir prieinamesnis vartotojams visame pasaulyje.  
Šis leidimas apjungia **galingas naujas funkcijas**, **darbo eigų automatizavimo patobulinimus** ir **naudotojo patirties tobulinimus**.  

---

## Naujos funkcijos

### Inspection Hub – naujas valdymo centras
**Inspection Hub** dabar pasiekiamas kaip centrinė vieta visiems jūsų inspection užduotims valdyti. Vietoje peršokimų tarp skirtingų modulių ar vien tik komandinės eilutės naudojimo, dabar galite stebėti ir valdyti savo inspections iš vienos vientisos sąsajos.  

Pagrindinės galimybės:  
- Inspekcijos pagal poreikį: Pradėkite naujas užduotis akimirksniu, kai tik reikia naujų rezultatų.  
- Inspekcijų istorija: Matykite inspekcijų laiko juostą — kas buvo paleista, kas tai inicijavo ir kada.  
- Būsenos sekimas: Užduotys aiškiai pažymėtos kaip užbaigtos, vykdomos arba laukiančios.  
- Informacija apie inicijuotoją: Greitai patikrinkite, ar inspekcija buvo paleista vartotojo, tvarkaraščio ar CLI.  
- Išvalymo įrankiai: Ištrinkite pasenusias ar nereikalingas užduotis, kad darbo aplinka liktų tvarkinga.  
- Išsamūs žurnalai: Įsigilkite į kiekvieną užduotį ir pamatykite, kiek laiko ji truko, kurie šaltiniai buvo įtraukti ir kaip taikyti slenkstiai.  

Inspection Hub suteikia komandoms **visišką matomumą ir kontrolę nuo pradžios iki galo**, todėl inspections valdyti dideliuose projektuose tampa paprasčiau.  

---

### Kelių kalbų palaikymas – digna kalba jūsų kalba
digna dabar pasiruošusi tarptautinėms komandoms su **kelių kalbų palaikymo** įvedimu.  

Šiame leidime galite pasirinkti savo **pageidaujamą sąsajos kalbą** tiesiog Vartotojo nuostatose. Palaikomos kalbos:  
- Anglų (UK, US, CA, AU)  
- Vokiečių (DE, AT, CH)  
- Lenkų (PL)  

Tai palengvina digna naudojimą bendrovėms, kurios dirba daugiaformėse komandose, ir užtikrina sklandesnį priėmimą skirtingose regionuose. Daugiau kalbų bus pridėta būsimuose leidimuose.  

---

### Duomenų šaltinių importas ir eksportas – konfigūracija tapo paprasta
Nuoseklumas tarp aplinkų yra esminis įmonių diegimuose. Su 2025.04, digna pristato **duomenų šaltinių importą/eksportą** per **dignacli**, komandų eilutės įrankį pažengusiems vartotojams.  

Privalumai:  
- Eksportuokite duomenų šaltinio konfigūraciją vieną kartą ir pakartotinai naudokite ją Development, Test ir Production aplinkose.  
- Atsikratykite rankinio konfigūravimo ir išvenkite brangių klaidų.  
- Palaikykite automatizuotas darbo eigas ir CI/CD pipelines su paprastomis CLI komandomis (`export-ds` ir `import-ds`).  
- Greitai kopijuokite duomenų šaltinius tarp projektų, kad būtų lengviau bendradarbiauti.  

Ši funkcija užtikrina, kad komandos gali diegti užtikrintai, žinodamos, jog konfigūracijos yra vienodos kiekvienoje aplinkoje.  

---

### Module Analytics (v1) – nuo aptikimo iki supratimo
digna pradėjo kaip platforma anomalijų aptikimui ir duomenų kokybės stebėsenai. Su Išleidimu 2025.04 ji toliau vystosi pristatydama **pirmąją Module Analytics versiją**.  

Module Analytics padeda vartotojams **suprasti savo duomenis**, o ne vien reaguoti į problemas. Su šiuo nauju moduliu galite:  
- Stebėti ilgalaikes tendencijas savo duomenų rinkiniuose.  
- Aptikti ir sekti kintamumą, kad suprastumėte svyravimus.  
- Tyrinėti duomenų elgseną laikui bėgant, kad gautumėte giluminį kontekstą.  

Pavyzdžiui, digna gali automatiškai pažymėti, kad *„Eilučių skaičius nuo metų pradžios padidėjo 15,8 %.“*  
Nėra SQL užklausų, jokių rankinių patikrinimų — tik **veiksmais pagrįstos įžvalgos akimirksniu**.  

Tai yra pagrindas dignos keliui link pažangios duomenų analizės, leidžiant komandoms pereiti nuo reaguojančio prie proaktyvaus stebėjimo.  

---

### Prietaisų skydelio patobulinimai – sklandesnė naudotojo patirtis
Be pagrindinių funkcijų, Išleidimas 2025.04 apima kelis **prietaisų skydelio patobulinimus**, skirtus padaryti digna intuityvesnę ir malonesnę naudoti:  
- Greitesnė navigacija tarp projektų ir inspekcijų.  
- Švaresnis išdėstymas inspekcijų žurnalams ir užduočių pateikimams.  
- Subtilūs dizaino patobulinimai, kurie padeda greičiau rasti įžvalgas.  

Šie patobulinimai remiasi tiesioginiu klientų grįžtamuoju ryšiu ir rodo mūsų nuolatinį įsipareigojimą kurti digna **platformą, pritaikytą kasdieniam darbui**.  

---

## Bendri patobulinimai
- Veikimo optimizacijos inspection užduotims su dideliais duomenų rinkiniais.  
- Patobulinta klaidų tvarkymo sistema dignacli, kad būtų suteikiamas aiškesnis grįžtamasis ryšys.  
- Stabilumo gerinimas projektams su daugybe vienu metu vykstančių užduočių.  
- Sąsajos patobulinimai užduočių žurnalų filtravimui ir projektų valdymui.  

---

## Santrauka
Išleidimas 2025.04 yra apie **kontrolę, prieinamumą ir įžvalgą**.  

- Naujas **Inspection Hub** suteikia vartotojams pilną matomumą į inspection užduotis.  
- **Kelių kalbų palaikymas** užtikrina, kad digna gali būti naudojama tarptautinėse komandose.  
- **Importo/eksporto funkcionalumas** supaprastina konfigūracijų valdymą tarp aplinkų.  
- **Module Analytics (v1)** perkelia dėmesį nuo aptikimo prie supratimo, siūlydamas tendencijų ir kintamumo stebėjimą.  
- **Prietaisų skydelio patobulinimai** pagerina bendrą naudotojo patirtį.  

Visi šie atnaujinimai daro digna galingesnę, patogesnę naudoti ir labiau pasiruošusią tarptautiniam naudojimui nei bet kada anksčiau.
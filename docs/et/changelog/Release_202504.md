---
title: digna Release 2025.04 | Inspection Hub, Multi-language, Module Analytics
description: Loe, mis on uut digna versioonis 2025.04. See versioon toob kaasa Inspection Hubi, mitmekeelsuse (inglise, saksa, poola), andmeallikate importimise/ekspordimise dignacli kaudu, Module Analyticsi esialgse väljaande ja täiustatud armatuurlaua kasutuskogemuse.
keywords: digna Release 2025.04, digna changelog, digna inspection hub, digna multi-language support, digna module analytics, digna import export, digna CLI, release notes, data observability, data quality monitoring
image: /assets/logo_square.png
---

# Changelog – Release 2025.04

Versiooniga Release 2025.04 astub digna olulise sammu edasi, et muuta andmepõhine kvaliteedi- ja jälgitavuse haldamine lihtsamaks, meeskondade jaoks läbipaistvamaks ning kasutajatele üle kogu maailma ligipääsetavamaks.  
See väljalase ühendab endas **võimsad uued funktsioonid**, **töövoo automatiseerimise täiustused** ja **kasutajakogemuse nüansid**.  

---

## Uued funktsioonid

### Inspection Hub – uus juhtimiskeskus
Inspection Hub on nüüd saadaval kui keskne koht kõigi inspekteerimistööde haldamiseks. Selle asemel et hüpata eri moodulite vahel või tugineda ainult käsureale, saad nüüd jälgida ja juhtida inspekteerimisi ühest sujuvast liidesest.  

Peamised võimalused:  
- Nõudmisel tehtavad inspekteerimised: alusta uusi ülesandeid koheselt, kui vajad värskeid tulemusi.  
- Inspekteerimise ajalugu: vaata inspekteerimiste ajajoont — mis käivitati, kes selle käivitas ja millal.  
- Oleku jälgimine: tööd on selgelt märgistatud lõpetatuks, pooleli olevaks või ootel.  
- Käivitaja ülevaade: kontrolli kiirelt, kas inspekteerimise käivitas kasutaja, ajakava või CLI.  
- Puhastustööriistad: kustuta aegunud või mittevajalikud tööd, et hoida tööruum korras.  
- Üksikasjalikud logid: vaata iga töö kohta, kui kaua see kestis, millised allikad olid kaasatud ja kuidas läviväärtusi rakendati.  

Inspection Hub annab meeskondadele **lõpp-to-lõpp nähtavuse ja kontrolli**, muutes inspekteerimiste haldamise suuremates projektides lihtsamaks.  

---

### Mitmekeelsus – digna räägib sinu keelt
digna on nüüd rahvusvaheliste meeskondade jaoks valmis, tuues sisse **mitmekeelse toe**.  

Selles versioonis saad oma **eelistatud liidese keele** seada otse Kasutaja eelistustes. Toetatud keeled on:  
- Inglise (UK, US, CA, AU)  
- Saksa (DE, AT, CH)  
- Poola (PL)  

See muudab digna kasutamise lihtsamaks mitmekeelsetes organisatsioonides ja tagab sujuvama vastuvõtu meeskondade seas, kes töötavad eri piirkondades. Rohkem keeli lisandub tulevastes väljaannetes.  

---

### Andmeallikate import ja eksport – konfiguratsioon lihtsaks tehtud
Keskkondade vahelise järjepidevuse tagamine on ettevõtte paigalduste puhul hädavajalik. Versiooniga 2025.04 tutvustab digna andmeallikate **importimise/eksportimise** funktsiooni läbi **dignacli**, käsurea tööriista edasijõudnud kasutajatele.  

Eelised:  
- Eksporti andmeallika konfiguratsioon korra ja kasuta seda uuesti Arenduses, Testis ja Produktiivkeskkonnas.  
- Vähenda käsitsi ümberkonfigureerimist ja väldi kulukaid vigu.  
- Toeta automatiseeritud töövooge ja CI/CD torusid lihtsate CLI-käskudega (`export-ds` ja `import-ds`).  
- Kopeeri andmeallikaid kiiresti projektide vahel lihtsama koostöö jaoks.  

See funktsionaalsus tagab, et meeskonnad saavad paigaldada kindlusega, teades, et konfiguratsioonid on igas keskkonnas järjepidevad.  

---

### Module Analytics (v1) – avastamisest arusaamiseni
digna alustas platvormina anomaaliate tuvastamiseks ja andmekvaliteedi jälgimiseks. Versiooniga Release 2025.04 liigub see edasi esmakordse väljaandega **Module Analytics (v1)**.  

Module Analytics aitab kasutajatel **mõista oma andmeid**, mitte ainult reageerida probleemidele. Selle uue mooduliga saad:  
- Jälgida pikaajalisi trende oma andmekogumites.  
- Tuvastada ja jälgida volatiilsust, et mõista kõikumisi.  
- Uurida andmete käitumist aja jooksul sügavamaks kontekstiks.  

Näiteks võib digna automaatselt välja tuua, et *„ridade arv on aastast alates kasvanud 15,8%.”*  
Pole vaja SQL-päringuid ega käsitsi kontrollimisi — vaid **toimivad ülevaated silmapilkselt**.  

See on alusepanek digna teekonnale edasijõudnud andmeanalüütika suunas, võimaldades andmemeeskondadel liikuda reageerivast jälgimisest proaktiivse juurde.  

---

### Armatuurlaua täiustused – sujuvam kasutajakogemus
Peamiste funktsioonide kõrval sisaldab Release 2025.04 mitmeid **armatuurlaua viimistlusi**, mis on mõeldud digna muutmiseks intuitiivsemaks ja meeldivamaks kasutada:  
- Kiirem navigeerimine projektide ja inspekteerimiste vahel.  
- Puhtam paigutus inspekteerimise logide ja tööde esitamiste jaoks.  
- Peened disaini kohendused, mis aitavad kiiremini leida ülevaateid.  

Need täiustused põhinevad otseselt klienditagasisidel ja näitavad meie jätkuvat pühendumust teha dignast **igal päeval kasutatav platvorm**.  

---

## Üldised parandused
- Tulemuslikkuse optimeerimised inspekteerimistöödele suurte andmekogumite puhul.  
- Paranenud veakäsitlus dignacli-s selgema tagasiside andmiseks.  
- Stabiilsuse parandused projektide jaoks, kus töötab palju samaaegseid töid.  
- UI-parandused töölogide filtreerimiseks ja projektihalduseks.  

---

## Kokkuvõte
Release 2025.04 keskendub **kontrollile, ligipääsetavusele ja arusaamisele**.  

- Uus **Inspection Hub** annab kasutajatele täieliku ülevaate inspekteerimistöödest.  
- **Mitmekeelsus** tagab, et dignat saab kasutada ülemaailmsetes meeskondades.  
- **Import/eksport funktsioon** lihtsustab konfiguratsioonihaldust keskkondade vahel.  
- **Module Analytics (v1)** nihutab fookust tuvastamiselt arusaamisele, pakkudes trendi- ja volatiilsusanalüüsi.  
- **Armatuurlaua täiustused** lihvivad üldist kasutajakogemust.  

Koos teevad need uuendused dignast võimekama, kasutajasõbralikuma ja rahvusvaheliselt valmisolekuga lahenduse kui kunagi varem.
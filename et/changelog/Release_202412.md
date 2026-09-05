# Muudatuste logi – Väljalase 2024.12

Väljalase 2024.12 toob kaasa uue funktsioonide ja täiustuste komplekti, mis muudab digna automatiseeritumaks, paindlikumaks ja ärivalmis.  
See versioon täiustab ajastamist, aruandlust, päringukäsitlust ja anomaaliate tuvastamise täpsust.  

---

## Uued funktsioonid

### Sisseehitatud ajastaja
Inspektsioonid ei sõltu enam ainult käsureast või API-kutsetest.  
Uue **digna Scheduler**i abil saab inspektsioone käivitada automaatselt määratud ajal.  

- Toetab **Cron expressions** korduvate ajastuste jaoks (päevased, iganädalased või kohandatud intervallid).  
- Pakub täpset juhtimist läbi **offsetide**, **alguskuupäevade** ja **lõppkuupäevade**.  
- Võimaldab meeskondadel tagada, et kõik kriitilised andmeallikad kontrollitakse järjepidevalt ja ilma käsitsi sekkumiseta.  

---

### Aruanded PDF-vormingus
Meeskonnad saavad nüüd tulemusi hõlpsasti huvigruppidega jagada läbi **PDF-ekspordi**.  

- Diagrammid, mõõdikud ja anomaaliate tulemused saab eksportida professionaalsesse PDF-vormingusse.  
- Aruanded ühendavad **visualiseeringud** ja **aluseks olevad andmed**, et teenindada nii tehnilisi kui ärikasutajaid.  
- Vähendab vajadust väliste tööriistade järele aruannete koostamisel.  

---

### Uus veeru tüüp: `CUSTOM`
Suurendamaks paindlikkust, tutvustab digna uut **`CUSTOM` veeru tüüpi**.  

- Kasutajad saavad täpselt määratleda, milliseid **statistikaid ja mõõdikuid** rakendatakse konkreetsetele atribuutidele.  
- Ideaalne erijuhtude jaoks, mis ei sobitu standardkategooriatesse nagu NUMERICAL või CATEGORICAL.  
- Aitab hoida analüüsid keskendununa ja tulemused ärikonteksti jaoks asjakohased.  

---

### Uued kohatäitjad snapshot-päringutes
Snapshot-päringud on nüüd lihtsamad ja vähem vigadele kalduvad tänu **dünaamilistele kohatäitjatele**.  

- Tokenid nagu `#date+n#` või `#date-n#` muudavad päringutes kuupäevi automaatselt.  
- Näide:  
  - `#date+1#` → homme  
  - `#date-2#` → kaks päeva tagasi  
- Vähendab käsitsi tehtavate kuupäevakalkulatsioonide vajadust ja tagab järjepidevuse meeskondade vahel.  

---

### Künniste optimeerimine
Anomaaliate künnised on nüüd intelligentsemad ja kontekstiteadlikumad.  

- Mõõdikute puhul nagu **NULL COUNT** on madalamad künnised automaatselt piiratud väärtusega **0**.  
- Vältib kehtetuid või tähendusetuid künniseid.  
- Tulemusena on vähem väärhäireid ja anomaaliate tuvastamine usaldusväärsem.  

---

## Üldised parandused
- Täiustatud **UI-komponendid** projekti ja atribuudi konfiguratsioonivaadetes.  
- Parem **dashboardi jõudlus** suurte andmemahtude puhul.  
- Täiustatud **logimine ja veateated** tõrkeotsingu jaoks.  

---

## Kokkuvõte
Väljalase 2024.12 tugevdab digna positsiooni platvormina andmekvaliteedi, anomaaliate tuvastamise ja seire valdkonnas.  
Ajastamise automatiseerimise, jagatavate PDF-aruannete, kohandatavate veergude, lihtsustatud snapshot-päringute ja nutikamate künniste kaudu muutub digna veelgi väärtuslikumaks nii tehnilistele kasutajatele kui äripooltele.
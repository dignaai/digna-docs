# Leidimo pastabos – 2026.06  

Su leidimu 2026.06 digna žengia reikšmingą žingsnį į priekį automatizavimo, praplėtimumo ir platformos naudojimo patogumo srityse.  
Šis leidimas pristato naują **digna Python SDK**, oficialų **Docker** diegimo palaikymą, atnaujintą dashboard patirtį ir pagerintą validacijos taisyklių valdymo perkeliamosios galimybes.

---

## Peržiūrėkite leidimo apžvalgą

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — šio leidimo apžvalga digna YouTube kanale.*

---

## Naujos funkcijos  

### digna Python SDK – Automatizuokite viską naudodami Python  
- Diegimas:
  ```bash
  pip install digna-sdk
  ```
- Programiškai valdykite ir automatizuokite digna naudodami Python  
- Kurkite ir konfigūruokite projektus per kodą  
- Paleiskite inspections ir monitoring vykdymus  
- Programiškai valdykite datasetus, taisykles ir konfigūracijas  
- Profilizuokite lenteles ir ištraukite metaduomenų įžvalgas  
- Eksportuokite profiliavimo ir duomenų kokybės rezultatus į išorines saugyklas ir sistemas  
- Integruokite su notebook’ais, orkestracijos įrankiais ir CI/CD pipeline’ais  

**Poveikis:** Leidžia pilną infrastruktūrą-kaip-kodą ir gilią duomenų kokybės bei stebėjimo darbo srautų automatizaciją naudojant Python.

---

### Docker palaikymas – Supaprastintas diegimas ir eksploatavimas  
- Oficiali Docker image palaikymas digna  
- Greitas ir nuoseklus diegimas skirtingose aplinkose  
- Supaprastintas įsitraukimas kūrimo, testavimo ir produkcijos aplinkose  
- Lengva integracija su Kubernetes ir kitomis konteinerių platformomis  
- Pagerinta diegimų perkeliama ir atkartojamumas  

**Poveikis:** Palengvina digna diegimą ir valdymą moderniose cloud-native architektūrose.

---

### QueryMode – Lanksti SQL vykdymo strategija

Sukonfigūruokite užklausų vykdymo strategiją: **Single** arba **Combined** režimas

**Single Mode**: Kiekvienas statistinis rodiklis apskaičiuojamas atskira SQL užklausa

  - Idealiai tinka didelėms duomenų saugykloms, kur riboja atmintis  
  - Apsaugo nuo užklausų sujungimo metu įvykstančio išteklių išeikvojimo (pvz., atminties trūkumo ar spool limitų)  
  - Didesnis užklausų skaičius, bet mažesnis atminties poreikis vienai užklausai

**Combined Mode**: Visi statistiniai rodikliai apskaičiuojami vienoje SQL užklausoje

  - Sumažina bendrą užklausų skaičių ir tinklo overhead’ą  
  - Optimizuoja našumą, kai duomenų šaltiniai yra valdomi atmintyje  
  - Efektyviau dažnai ir lygiagrečiai vykdomoms užklausoms

**Poveikis:** Leidžia vartotojams smulkiai valdyti užklausų vykdymą, subalansuojant našumą, resursų naudojimą ir atminties saugumą pagal duomenų šaltinio charakteristikas.

---

### Konfigūruojamas prognozavimo modelis

Anomalijų aptikimo pagrindu esantis modelis dabar pasveria konkuruojančius kiekvienos eilutės paaiškinimus – dėsningumą kartu su naujausių stebėjimų interpretacija – ir sujungia jų prognozes pagal tai, kiek stipriai kiekvienas iš jų pagrįstas. Viena ekstremali reikšmė nebegali prasiskverbti į tolesnes prognozes.

Jį valdo du nustatymai naujame duomenų šaltinio skirtuke **Model**, kiekvienas nuo `0.0` iki `1.0`, numatytoji reikšmė – `0.5`:

- **Break Sensitivity** – kaip greitai šuolis į naują lygį ar besikeičianti tendencija priimami kaip tikri, užuot laikius juos išskirtimis
- **Model Complexity** – kiek struktūros modelis stengiasi aptikti: nuo kalendorinių efektų ir vieno lygio poslinkio iki nežinomų ciklų, mėnesio dienos efektų ir mėnesinių atstatymų

Abu nustatymus bet kada galima grąžinti į numatytąsias reikšmes. Kaip veikia kiekvienas iš jų, žr. [Modelio nustatymai](../platform/data_anomalies/how_it_works.md#model-settings).

**Poveikis:** Suteikia naudotojams galimybę valdyti patį prognozavimo modelį šalia esamų tolerancijos juostos nuostatų Sensitivity ir Memory, kurios dabar yra skirtuke **Thresholds**.

---

### Anomalijų pranešimų valdymas

- Naujas skirtukas **Notifications** duomenų šaltinio anomalijų nustatymuose:
  - **Minimum Alerts** – kiek nepavykusių patikrų (ne neapibrėžtų) turi surinkti inspekcija, kad būtų išsiųstas pranešimas (numatytoji reikšmė `1`)
  - **Pause After Notification (Days)** – kiek laiko prenumerata nutyla po pranešimo apie duomenų šaltinį (numatytoji reikšmė `0`, be pauzės)
- Prenumeratoriai dabar informuojami, kai inspekcija visiškai nepavyksta (**Notify Inspection Errors**)
- Kiekvienas pranešimas veda tiesiai į puslapį, su kuriuo jis susijęs – į nepavykusias inspekcijos patikras arba į Schema Tracker ir Timeliness rodinius
- Aiškesni prenumeratos jungikliai: **Notify on Passed Inspections**, **Notify Inspection Errors**, **Notify Data Volume Checks**

**Kaip veikia pranešimai:** pranešimai siunčiami per **pranešimų kanalus** – Email (per SMTP ryšį), Slack arba Jira, – kuriuos nustato administratoriai ir kuriuos galima patikrinti naudojant **Test Notification Channel**. **Prenumerata** susieja kanalą su projektu: ji apima visus arba pasirinktus duomenų šaltinius, o jos jungikliai nustato, apie ką ji praneša – kiekvieną modulį (Data Anomalies, Data Validation, Data Analytics, Timeliness, Schema Tracker ir duomenų apimties patikras), visiškai nepavykusias inspekcijas ir, pasirinktinai, taip pat sėkmingas inspekcijas.

**Poveikis:** Mažiau, bet naudingesnių pranešimų – pavieniai nuokrypiai ir išliekančios anomalijos nebeužtvindo kanalo.

---

### Perdaryta dashboard patirtis  
- Modernizuotas ir pagerintas UI/UX dizainas  
- Aiškesnė navigacija ir struktūra  
- Geresnis monitoring rezultatų ir duomenų kokybės įžvalgų matomumas  
- Pagerintas perspėjimų, statistikos ir dashboardų skaitomumas  
- Greitesnis priėjimas prie svarbios operacinės informacijos  

**Poveikis:** Didina naudojimo patogumą ir kasdienį produktyvumą visiems vartotojams.

---

### Išplėstas validacijos taisyklių importas ir eksportas  
- Patobulinta importo/eksporto funkcionalumas validacijos taisyklėms  
- Lengvesnė migracija tarp aplinkų ir projektų  
- Pagerintas standartizuotų taisyklių rinkinių pakartotinis naudojimas  
- Geresnė valdymo ir taisyklių gyvavimo ciklo kontrolė  
- Supaprastintas bendradarbiavimas tarp komandų  

**Poveikis:** Leidžia mastelį didinančią ir nuoseklią duomenų kokybės valdymo praktiką visoje organizacijoje.

---

## Platformos patobulinimai  

- Pilna Python SDK integracija automatizavimui  
- Konteinerizuotas diegimas per Docker  
- Pagerintas UX per perdarytą dashboard  
- Išplėstas validacijos logikos perkeliamosis gebėjimas  

---

## Kam naudingas šis leidimas  

- Duomenų inžinieriams: automatizavimas, SDK naudojimas, pipeline integracija  
- Platformos komandoms: supaprastintas diegimas per Docker  
- Duomenų valdymo (governance) komandoms: pakartotinai naudojamų validacijos taisyklių valdymas  
- Analitikos komandoms: geresnis naudojimosi patogumas ir įžvalgų matomumas  

---

## CLI atnaujinimai  
- Įtraukta SDK integracijos palaikymas  
- Patobulinti importo/eksporto darbo srautai  
- Bendri stabilumo ir našumo pagerinimai
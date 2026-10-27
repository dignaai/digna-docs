# Leidimo pastabos – 2026.11  

Leidimas 2026.11 sukurtas aplink tris svarbius papildymus:

- **digna Data Reconciliation (Beta)**: tikrina, ar duomenys išlieka nuoseklūs keliaudami tarp sistemų  
- **digna Agentic (Beta)**: atveria digna AI agentams per digna MCP Server  
- **digna Engine**: pasirinktinai profiliuoja duomenis pačioje digna ir leidžia tikrinti nuorodinį vientisumą tarp skirtingų duomenų bazių technologijų  

---

## Naujos funkcijos  

### digna Data Reconciliation (Beta) – Šaltinio ir tikslo nuoseklumas  
Prieš pasiekdami ataskaitą, duomenys dažnai pereina per kelias sistemas. digna Data Reconciliation (Beta) palygina **tikslinį** duomenų šaltinį su **šaltiniais**, iš kurių jis buvo sukurtas, ir įspėja, kai jie nebesutampa.

- Konfigūruojama kaip pavadintos taisyklės naujame tikslinio duomenų šaltinio skirtuke **Data Reconciliation**  
- Šaltiniu gali būti bet kuris projekto duomenų šaltinis, kuriame įjungta Data Reconciliation  
- Naudojimo atvejai apima standartines suderinimo procedūras ir ETL procesų rezultatų validavimą  
- Dviejų tipų taisyklės: **Exact** ir **AI**  

**Exact taisyklės – Suderinimas kaip duomenų kokybės taisyklė**: tiksliai apibrėžiate, kas turi sutapti tarp vieno šaltinio ir vieno tikslo, kaip duomenų kokybės taisyklėje.

  - Palyginkite vieną šaltinio duomenų šaltinį su vienu tiksliniu duomenų šaltiniu  
  - Susiekite tikslo patikrą su šaltinio patikra pagal statistinį rodiklį ir atributą, pvz., eilučių skaičių arba sumos stulpelio bendrą sumą  
  - Leiskite skirtumą su **absolute** tolerancija (pvz., ± 10) arba **relative** tolerancija (pvz., ± 0,5 % šaltinio reikšmės)  
  - Laiko juosta rodo kiekvienos dienos skirtumą, palyginti su tolerancija  

**AI taisyklės – Suderinimas kaip duomenų stebėjimas (data observability)**: digna išmoksta, kaip tikslas seka savo šaltinius, taip pat kaip digna stebi duomenis kituose moduliuose, ir įspėja, kai šis ryšys nutrūksta.

  - Sujunkite kelių šaltinio duomenų šaltinių patikras su vieno tikslo patikromis  
  - Nereikia žinoti ar užrašyti logikos tarp jų (sujungimų, filtrų, agregacijų)  
  - Modelis iš istorijos išmoksta, kaip tikslas tą pačią dieną seka savo šaltinius  
  - Kiekviena tikslo patikra prognozuojama pagal tos dienos šaltinių reikšmes, o digna įspėja, kai tikslas išeina už pačios taisyklės ankstesnių paklaidų juostos  
  - Kiekviena taisyklė turi savo **Model settings**: **Sensitivity**, **Memory** ir **Model Complexity**  

Suderinimo patikros rodomos dashboard su atskira laiko juosta kiekvienai taisyklei. Jos įskaičiuojamos į bendrą inspekcijos būseną ir sukelia pranešimus.

**Poveikis:** Apima abi suderinimo puses. Exact taisyklės užtikrina žinomas kontroles tarp šaltinio ir tikslo, o AI taisyklės stebi sudėtingus srautus, tokius kaip ETL procesai, todėl pakeliui prarasti ar pakeisti duomenys aptinkami be rankomis rašyto suderinimo SQL.

---

### digna Agentic (Beta) – digna AI agentams  
Pirmoji digna Agentic (Beta) versija. AI agentai dabar gali dirbti su digna, atsakyti į verslo klausimus apie jūsų duomenis ir padėti patobulinti jūsų konfigūraciją.

**digna MCP Server**: leidžia Claude ir kitiems AI agentams dirbti su digna per Model Context Protocol.

  - Valdykite projektus, duomenų šaltinius, taisykles, inspekcijų tvarkaraščius ir prenumeratas  
  - Skaitykite inspekcijų būsenas iki pavienės patikros, kad ištirtumėte įspėjimus  

**Duomenų šaltinių ir atributų aprašymai**: paprasta kalba aprašykite, ką apima duomenų šaltinis ar atributas.

  - AI agentai naudoja aprašymus jūsų duomenims interpretuoti  
  - Užduokite verslo klausimus apie savo duomenis, o AI agentai į juos atsakys remdamiesi tuo, ką stebi digna  
  - Jei dabartinė digna konfigūracija negali atsakyti į klausimą, AI agentas, kai įmanoma, pasiūlo duomenų šaltinio ir jo atributų pakeitimus, pvz., pridėti naują duomenų rinkinį  

**Poveikis:** Leidžia paprasta kalba užduoti verslo klausimus apie savo duomenis, o AI agentams – padėti konfigūruoti digna ir tirti duomenų kokybės problemas.

---

### digna Engine – Profiliuokite ten, kur pasirenkate  
Pagal numatytuosius nustatymus digna profiliuoja duomenis ten, kur jie yra, – šaltinio duomenų bazėje. digna Engine prideda pasirinkimą: digna eksportuoja duomenis iš šaltinio ir profiliuoja juos digna Engine viduje.

- Pasirinktinai, ne privalomai: profiliavimas šaltinio duomenų bazėje lieka prieinamas  
- Pasirenkama kiekvienai duomenų bazės jungčiai kaip jos **profiliavimo vieta**: **Source Database** arba **digna Engine**  
- Prieinama visoms palaikomoms šaltinių technologijoms  

**Nuorodinis vientisumas tarp jungčių**: kai kurioms patikroms reikia eksportuoti duomenis. Tokiais atvejais digna Engine išplečia **digna Data Validation**.

  - **Nuorodinio vientisumo patikros** tarp duomenų šaltinių, esančių **skirtingose duomenų bazių jungtyse**, įskaitant skirtingas duomenų bazių technologijas (pvz., Oracle ir PostgreSQL)  
  - Veikia su abiem profiliavimo vietomis: naudojant Source Database, į digna Engine eksportuojami tik raktiniai stulpeliai  
  - Dashboard parodo, kai patikra vykdoma tarp dviejų jungčių  

**Poveikis:** Leidžia pasirinkti, kur profiliuojami duomenys, ir užtikrina ryšius tarp sistemų, veikiančių skirtingomis duomenų bazių technologijomis.

---

## Profiliavimo patobulinimai  

Šis leidimas taip pat suteikia naudotojams daugiau kontrolės, ką ir kaip profiliuoti.

### Užklausų atributai – Naudotojo apibrėžti stulpeliai  
- Apibrėžkite dirbtinius stulpelius: SQL išraišką, apimančią vieną ar kelis duomenų šaltinio stulpelius  
- Kiekvienas užklausos atributas turi savo pavadinimą  
- Profiliuojamas ir tikrinamas kaip bet kuris kitas atributas  

### DATE stulpelių kategorija  
- Nauja atributų kategorija **Date**  
- Metrikos, susietos su inspektuojama data  

### Profiliavimas pagal poreikį  
- Profiliuokite bet kurį atributą pagal vienos datos pilną momentinę kopiją, nepaleidę inspekcijos  
- Padeda nustatyti atributo stulpelio tipą: **Numerical**, **Categorical**, **Date** arba **Unspecified**  

---

## Kam naudingas šis leidimas  

- **Duomenų inžinieriams:** ETL rezultatų validavimas su digna Data Reconciliation (Beta)  
- **Finansų, rizikos ir kontrolingo komandoms:** standartinės suderinimo procedūros kaip Exact taisyklės digna Data Reconciliation (Beta)  
- **Duomenų kokybės ir valdymo (governance) komandoms:** nuorodinis vientisumas tarp duomenų bazių technologijų su digna Engine  
- **Verslo naudotojams:** į verslo klausimus apie duomenis atsako AI agentai su digna Agentic (Beta)  
- **AI ir automatizavimo komandoms:** AI agentai, dirbantys su digna per digna Agentic (Beta)  

---

## CLI atnaujinimai  
- Pakeitimų nėra  

---
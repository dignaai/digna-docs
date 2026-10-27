---
title: digna Väljalase 2026.11 | Data Reconciliation, digna Agentic ja digna Engine
description: Tutvuge, mis on uut digna väljalases 2026.11. See versioon toob kolm suurt lisandust - digna Data Reconciliation, digna Agentic koos digna MCP Serveriga ning digna Engine, mis võimaldab viiteterviklikkuse kontrolle eri andmebaasitehnoloogiate vahel.
keywords: digna Release 2026.11, digna muudatuste logi, digna Data Reconciliation, andmete kooskõlastamine, ETL valideerimine, allika ja sihi kooskõlastamine, digna Agentic, digna MCP Server, AI-agendid andmekvaliteet, digna Engine, ühenduste ülene viiteterviklikkus, päringuatribuudid, andmete profileerimine, data observability
image: /assets/logo_square.png
---

# Muudatused – Väljalase 2026.11  

Väljalase 2026.11 keskendub kolmele suurele lisandusele:

- **digna Data Reconciliation**: kontrollib, et andmed püsiksid süsteemide vahel liikudes kooskõlas  
- **digna Agentic**: avab digna AI-agentidele digna MCP Serveri kaudu  
- **digna Engine**: profileerib soovi korral andmeid digna sees ja võimaldab viiteterviklikkuse kontrolle eri andmebaasitehnoloogiate vahel  

digna Data Reconciliation ja digna Agentic tarnitakse beetaversioonidena.

---

## Uued funktsioonid  

### digna Data Reconciliation – allika ja sihi kooskõla  
Enne aruandesse jõudmist läbivad andmed sageli mitu süsteemi. digna Data Reconciliation võrdleb **siht**-andmeallikat **allikatega**, millest see on koostatud, ja annab märku, kui need enam ei klapi.

- Seadistatakse nimeliste reeglitena siht-andmeallika uuel vahekaardil **Data Reconciliation**  
- Allikaks võib olla projekti mis tahes andmeallikas, millel on Data Reconciliation sisse lülitatud  
- Kasutusjuhtude hulka kuuluvad standardsed kooskõlastusprotseduurid ja ETL-protsesside tulemuste valideerimine  
- Kaks reeglitüüpi: **Exact** ja **AI**  

**Exact-reeglid – kooskõlastamine andmekvaliteedi reeglina**: määrate täpselt, mis peab ühe allika ja ühe sihi vahel klappima, nagu andmekvaliteedi reeglis.

  - Võrrelge üht lähte-andmeallikat ühe siht-andmeallikaga  
  - Siduge sihi kontroll allika kontrolliga statistiku ja atribuudi järgi, nt ridade arv või summaveeru kogusumma  
  - Lubage erinevust **absolute** tolerantsiga (nt ± 10) või **relative** tolerantsiga (nt ± 0,5 % allika väärtusest)  
  - Ajajoon näitab iga päeva erinevust tolerantsi suhtes  

**AI-reeglid – kooskõlastamine kui data observability**: digna õpib, kuidas siht oma allikaid järgib, samamoodi nagu digna jälgib andmeid teistes moodulites, ja annab märku, kui see seos katkeb.

  - Kombineerige mitme lähte-andmeallika kontrollid ühe sihi kontrollidega  
  - Nendevahelist loogikat (joinid, filtrid, agregatsioonid) ei pea teadma ega üles kirjutama  
  - Mudel õpib ajaloost, kuidas siht samal päeval oma allikaid järgib  
  - Iga sihi kontrolli väärtus ennustatakse päeva lähteväärtuste põhjal ja digna annab märku, kui siht väljub reegli enda varasemate vigade vahemikust  
  - Igal reeglil on oma **Model settings**: **Sensitivity**, **Memory** ja **Model Complexity**  

Kooskõlastuskontrollid kuvatakse dashboardil, iga reegli kohta oma ajajoonega. Need arvestatakse inspektsiooni üldolekusse ja käivitavad teavitusi.

**Mõju:** Katab kooskõlastamise mõlemad pooled. Exact-reeglid jõustavad teadaolevaid kontrolle allika ja sihi vahel ning AI-reeglid jälgivad keerukaid andmevooge, näiteks ETL-protsesse, nii et teel kaotsi läinud või muutunud andmed tabatakse ilma käsitsi kirjutatud kooskõlastus-SQL-ita.

---

### digna Agentic – digna AI-agentidele  
digna Agentic esimene versioon. AI-agendid saavad nüüd dignaga töötada, vastata äriküsimustele teie andmete kohta ja aidata teie konfiguratsiooni parandada.

**digna MCP Server**: võimaldab Claude'il ja teistel AI-agentidel dignaga töötada Model Context Protocoli kaudu.

  - Hallake projekte, andmeallikaid, reegleid, inspektsioonide ajakavasid ja tellimusi  
  - Lugege inspektsioonide olekuid kuni üksiku kontrollini, et hoiatusi uurida  

**Kirjeldused andmeallikatel ja atribuutidel**: kirjeldage lihtsas keeles, mida andmeallikas või atribuut sisaldab.

  - AI-agendid kasutavad kirjeldusi teie andmete tõlgendamiseks  
  - Esitage oma andmete kohta äriküsimusi ja AI-agendid vastavad neile selle põhjal, mida digna jälgib  
  - Kui digna praegune konfiguratsioon küsimusele vastata ei suuda, pakub AI-agent võimaluse korral välja muudatusi andmeallikale ja selle atribuutidele, nt uue andmekogumi lisamise  

**Mõju:** Võimaldab esitada oma andmete kohta äriküsimusi lihtsas keeles ning laseb AI-agentidel aidata dignat seadistada ja andmekvaliteedi probleeme uurida.

---

### digna Engine – profileerige seal, kus soovite  
Vaikimisi profileerib digna andmeid seal, kus need asuvad, ehk lähteandmebaasis. digna Engine lisab uue võimaluse: digna ekspordib andmed allikast ja profileerib need digna Engine'i sees.

- Valikuline, mitte kohustuslik: profileerimine lähteandmebaasis jääb endiselt kättesaadavaks  
- Valitakse iga andmebaasiühenduse jaoks eraldi selle **profileerimiskohana**: **Source Database** või **digna Engine**  
- Saadaval kõigi toetatud lähtetehnoloogiate jaoks  

**Ühenduste ülene viiteterviklikkus**: mõned kontrollid nõuavad andmete eksportimist. Nendel juhtudel laiendab digna Engine moodulit **digna Data Validation**.

  - **Viiteterviklikkuse kontrollid** andmeallikate vahel, mis asuvad **eri andmebaasiühendustel**, sealhulgas eri andmebaasitehnoloogiatel (nt Oracle ja PostgreSQL)  
  - Töötab mõlema profileerimiskohaga: Source Database puhul eksporditakse digna Engine'i ainult võtmeveerud  
  - Dashboard näitab, kui kontroll töötab üle kahe ühenduse  

**Mõju:** Võimaldab valida, kus andmeid profileeritakse, ja jõustab seoseid süsteemide vahel, mis töötavad eri andmebaasitehnoloogiatel.

---

## Profileerimise täiustused  

See väljalase annab kasutajatele ka rohkem kontrolli selle üle, mida ja kuidas profileeritakse.

### Päringuatribuudid – kasutaja määratud veerud  
- Määrake tehisveerge: SQL-avaldis andmeallika ühe või mitme veeru põhjal  
- Igal päringuatribuudil on oma nimi  
- Profileeritakse ja kontrollitakse nagu mis tahes muud atribuuti  

### Veerukategooria DATE  
- Uus kategooria **Date** atribuutidele  
- Mõõdikud inspekteeritava kuupäeva suhtes  

### Profileerimine nõudmisel  
- Profileerige mis tahes atribuuti ühe kuupäeva täieliku hetktõmmise põhjal, ilma inspektsiooni käivitamata  
- Aitab määrata atribuudi veerutüüpi: **Numerical**, **Categorical**, **Date** või **Unspecified**  

---

## Kellele see väljalase kasulik on  

- **Andmeinsenerid:** ETL-tulemuste valideerimine digna Data Reconciliation abil  
- **Finants-, riski- ja kontrollingumeeskonnad:** standardsed kooskõlastusprotseduurid Exact-reeglitena digna Data Reconciliation abil  
- **Andmekvaliteedi ja andmehalduse meeskonnad:** viiteterviklikkus eri andmebaasitehnoloogiate vahel digna Engine'i abil  
- **Ärikasutajad:** AI-agendid vastavad andmeid puudutavatele äriküsimustele digna Agentic abil  
- **AI- ja automatiseerimismeeskonnad:** AI-agendid töötavad dignaga digna Agentic kaudu  

---

## CLI uuendused  
- Muudatusi pole  

---

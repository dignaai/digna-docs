# Changelog – Release 2026.04  

digna versioon 2026.04 laiendab oluliselt oma võimalusi analüütikas ja andmete valideerimises.  
See väljalase toob kaasa täiustatud ajaseeriate analüüsi, taaskasutatavad valideerimiskomponendid ja keskse väärtuste standardiseerimise.

---

## Uued funktsioonid  

### Analytics Chart – ajaseeriate analüüs ilma andmeteaduseta  
- Uus **Analytics Chart** interaktiivseks ajaseeriate analüüsiks  
- Sisseehitatud analüütilised meetodid:
    - Lineaarne, kvadratiivne ja kuupiline regressioon  
    - Tükeldatud regressioon konfigureeritavate purunemispunktidega  
    - Silumisvõtted  
    - Kvantiilianalüüs  
- Trendide, hooajalisuse ja mustrimuutuste automaatne tuvastamine  
- Jääkide analüüs sügavamate kõrvalekallete mõistmiseks  
- Ajaseeriad arvutatakse automaatselt iga andmekogumi jaoks  

**Mõju:** Võimaldab kasutajatel mõista keerukat andmekäitumist ajas ilma andmeteaduse oskuseta või välistööriistadeta.

---

### Enumerations – lubatud väärtuste keskne määratlus  
- Määra taaskasutatavad komplektid lubatud väärtustest (nt riigid, osariigid, staatusekoodid)  
- Valideeri veeru väärtusi vastavalt eeldefineeritud enumeratsioonidele **digna Data Validation**-is  
- Taaskasuta enumeratsioone projektide ja andmeallikate vahel  
- Kasuta enumeratsioone kõikjal läbi `#ENUM:MY_ENUM#`  
- Kõik kontrollid käivitatakse **otse allikaandmebaasis**  

**Mõju:** Tagab ühtlase ja standardiseeritud andmesisu organisatsiooni ulatuses.

---

### Validation Rule Templates – taaskasutatav andmekvaliteedi loogika  
- Määra taaskasutatavad valideerimisreeglid (nt tühikute kontroll, NOT NULL, formaadi kontrollid)  
- Rakenda malle mitmel andmekogumil  
- Tagab reegli loogika järjepidevuse projektide lõikes  
- Vähendab dubleerimist ja käsitsi seadistamist  
- Kõik kontrollid käivitatakse **otse allikaandmebaasis**  

**Mõju:** Võimaldab skaleeruvat ja kõrge jõudlusega andmete valideerimist ilma andmete liigutamiseta.

---

### Statistikatüübi tasandi asjakohasuskonditsioonid  
- Määra asjakohasuskonditsioonid **veerutasemel iga statistika** jaoks  
- Laiendab anomaaliate asjakohasuskonditsioonide kontseptsiooni  
- Kontrolli, millal statistikat tuleks pidada asjakohaseks  
- Vähenda müra, välistades mitteolulisi olukordi  

**Mõju:** Parandab signaali kvaliteeti, keskendudes ainult tähenduslikele kõrvalekalletele.

---

## Laiendatud Data Analytics & Validation võimalused  

Selle väljalaske abil laiendab digna nii **andmete mõistmist** kui ka **andmete valideerimise standardiseerimist**:

- Täiustatud **ajaseeriate tõlgendamine** ilma andmeteadmiste nõudeta  
- Lubatud väärtuste keskne määratlus läbi **enumeratsioonide**  
- Taaskasutatav **valideerimisloogika mallide kaudu**  
- Peenhäälestatud kontroll statistika ja hoiatuste **asjakohasuse üle**  

Koos võimaldavad need funktsioonid organisatsioonidel mitte ainult tuvastada probleeme, vaid ka **mõista, standardiseerida ja juhtida andmete kvaliteeti**.

---

## Kellele see väljalase kasulik on  

- **Andmeinsenerid:** Taaskasutatav valideerimisloogika ja parem kontroll monitooringu käitumise üle  
- **Andmekvaliteedi & halduse meeskonnad:** Standardiseeritud reeglid ja järjepidev andmete valideerimine süsteemide lõikes  
- **Analüütika & BI meeskonnad:** Paremini mõistetavad trendid ja kõrvalekalded  
- **Platvormi omanikud:** Suurem kasutuselevõtt läbi lihtsustatud analüütika ja skaleeritava valideerimise  

---

## CLI uuendused  
- Muudatusi pole  

---
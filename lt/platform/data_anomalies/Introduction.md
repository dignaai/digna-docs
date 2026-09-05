# Data Anomalies – Automatizuotas netaisyklingumų aptikimas
<h1 style="display:none;">AI varomas modulis duomenų kokybei ir stebimumui – digna Data Anomalies</h1>

---

## Paskirtis

**Data Anomalies** modulis automatiškai identifikuoja netaisyklingumus jūsų duomenų rinkiniuose — nereikia rašyti taisyklių.  
Jis nuolat stebi **duomenų tiekimo kokybę**, mokosi, kas yra „normalu“, ir realiu laiku aptinka nukrypimus.

Naudodamas AI pagrįstą aptikimą, digna atpažįsta *tylias duomenų klaidas*, tokias kaip trūkstami, pasikartojantys ar sugadinti įrašai, galinčias iškraipyti ataskaitas, ML modelius ir informacinius panelius.

---

## Techninis apžvalga

### Analizuojami metrikai

digna nuolat profiliuoja šiuos jūsų duomenų aspektus:

- **Įrašų apimtis** – bendras eilučių skaičius, kasdien arba partijų pagrindu  
- **Trūkstamos reikšmės** – nulinių arba tuščių laukų aptikimas  
- **Pasiskirstymai ir histogramos** – duomenų formos pokyčių stebėjimas  
- **Reikšmių intervalai** – automatinis ribų pažeidimų arba ekstremalių reikšmių identifikavimas  
- **Unikalumas** – patikrinimai dėl dublikatų raktų ar pasikartojančių įrašų  

### Išmanusis anomalijų aptikimas

- Naudoja **istorinį mokymąsi**, kad dinamiškai apibrėžtų laukiamas ribas  
- Aptinka nukrypimus **apimtyje, reikšmių pasiskirstymuose arba loginiuose ryšiuose**  
- Taiko AI, kad automatiškai prisitaikytų prie paros laiko ar sezoniškumo modelių  
- Skiria **statistinius svyravimus** nuo tikrų anomalijų  
- Generuoja detalias metrikas ir pasitikėjimo balus kiekvienam duomenų rinkiniui ir stulpeliui  

---

## Aptikimo scenarijai

Žemiau pateikti realaus pasaulio problemų pavyzdžiai, kuriuos automatiškai pagauna **Data Anomalies** modulis:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | Per dieną trūksta pusės transakcijų, pasikartojantys partijų užkrovimai arba staigūs duomenų srautų šuoliai |
| **Missing or null values** | Duomenų ištraukos užbaigtos, tačiau kritiniai stulpeliai lieka tušti |
| **Distribution drifts** | Vidutinė pirkimo suma arba sandorių skaičius regione netikėtai pasikeičia |
| **Column swaps** | Tokie stulpeliai kaip *first_name* ir *last_name* netyčia sukeisti ETL procese |
| **Unexpected categorical values** | pvz., „Zurich“ atsiranda Austrijos miestų sąraše |
| **Sudden uniqueness loss** | Anksčiau unikalūs ID pradeda dubliuotis dėl upstream sujungimo klaidų |

---

## Architektūra ir vykdymas

- **Vykdymas duomenų bazėje:** Visa anomalijų aptikimo logika vykdoma *duomenų bazės variklyje* (Teradata, Snowflake, Databricks, PostgreSQL ir kt.)  
- **Be duomenų perdavimo:** digna skaito tik metrikas, niekada neišveža žalių duomenų iš išorės  
- **Inkrementiniai atnaujinimai:** Kiekvieno paleidimo metu analizuojami tik nauji duomenų segmentai efektyvumui užtikrinti  
- **Konfigūruojamas tikrinimo dažnis:** Kiekvieną valandą, kasdien arba iškviečiant kilmės procesų  
- **Rezultatų saugojimas:** Metrikos ir anomalijų žymos įrašomos atgal į digna stebimumo schemą vizualizacijai ir įspėjimams  

---

## Privalumai

| Area | Benefit |
|------|----------|
| **Automation** | Pašalina šimtus rankinių SQL arba taisyklių aprašymų |
| **Precision** | Aptinka problemas, kurias dažnai praleidžia statinės ribos |
| **Scalability** | Efektyviai stebi milijonus įrašų vienoje lentelėje |
| **Integration** | Sklandžiai veikia su *Data Analytics* analizei ir tendencijoms |
| **Compliance** | Užtikrina nuolatinę kontrolę dėl **duomenų kokybės ir stebimumo** |
| **Transparency** | Teikia pasitikėjimo balus, laiko žymes ir priežasčių kodus kiekvienai anomalijai |

---

## Kaip digna išmoksta, kas yra „normalu“

1. **Profilavimo etapas:** digna renka metrikas iš istorinių duomenų rinkinių.  
2. **Mokymosi etapas:** AI modeliai identifikuoja periodiškus modelius (sezoninius, savaitinius, dieninius).  
3. **Stebėjimo etapas:** Būsimieji duomenų rinkiniai lyginami su dinaminiu mokymosi metu nustatytomis ribomis.  
4. **Įspėjimų etapas:** Nukrypimai už statistinio pasitikėjimo ribų keliauja kaip anomalijos.

Visi modeliai yra aiškinami, deterministiniai ir optimizuoti įmonių duomenų apimtims.

---

## Pavyzdinės taikymo sritys

- Duomenų kokybės stebėjimas **bankinių operacijų sistemose**  
- Užkrovimo klaidų aptikimas **ETL ar duomenų sandėlio užduotyse**  
- Abnormalios klientų veiklos identifikavimas **telekomunikacijų įrašuose**  
- Klinikinio duomenų nuoseklumo stebėjimas **sveikatos priežiūros analizės srautuose**  
- Sugadintų informacinių panelių prevencija **BI ir ataskaitų aplinkose**

---

## Dažniausiai užduodami klausimai

**Ar Data Anomalies reikalauja iš anksto apibrėžtų taisyklių?**  
Ne — modulis automatiškai mokosi iš duomenų elgesio.

**Ar vis tiek galiu apibrėžti konkrečias ribas, jei reikia?**  
Taip. digna leidžia derinti AI pagrįstą ir taisyklių pagrindu atliekamą aptikimą (per *Data Validation*).

**Kaip sumažinami klaidingi teigiami signalai?**  
Modulis naudoja adaptacinį mokymąsi ir statistinio pasitikėjimo įvertinimus, kad ignoruotų įprastus sezoniškumo svyravimus.

**Kur vyksta skaičiavimai?**  
Visa apdorojimo eiga vykdoma jūsų duomenų bazėje — digna niekada neištraukia žalių duomenų.

**Ar tinka jautriems ar reguliuojamiems duomenims?**  
Taip. digna gali veikti visiškai vietoje (on-premises) arba privačiame debesyje ir atitinka Europos reikalavimus.
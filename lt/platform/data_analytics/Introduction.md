# Data Analytics – Tendencijos ir stabilumas
<h1 style="display:none;">AI-Driven Data Analytics Module for Data Quality and Observability – digna</h1>

---

## Paskirtis

**Data Analytics** modulis atskleidžia **ilgalaikius modelius, stabilumą ir volatilumą** jūsų duomenų rinkiniuose — paversdamas žalius metrikų duomenis prasmingomis įžvalgomis.  
Jis suteikia aukštesnio lygio analitinį sluoksnį virš *Data Anomalies* rezultatų, leidžiant komandoms **suprasti pokyčius laike** ir gerinti tiek **duomenų kokybę**, tiek **duomenų perdavimo vamzdynų stebimumą**.

Identifikavęs tendencijų pertrūkius, pasikartojančius modelius ir volatilumo pokyčius, digna Data Analytics padeda atskirti **lūkesčių atitinkančius sezoninius elgesius** nuo **realių duomenų kokybės problemų**.

---

## Techninis apžvalga

### Išvestinės statistikos
*digna Data Analytics* apskaičiuoja statistines savybes, tokias kaip:

- **Tendencija** – metrikos ilgalaikė kryptis (didėjanti, mažėjanti, stabili)  
- **Volatilumas** – kiek metrika svyruoja per nurodytą laiko langą  
- **Sezoniškumas** – pasikartojantys laikiniai modeliai (dieniniai, savaitiniai, mėnesiniai)  
- **Pakeitimų taškai** – statistiškai reikšmingi elgesio pokyčiai  

### Palaikomi metrikai
Modulis gali analizuoti bet kurią metriką, sugeneruotą kitų digna modulių, įskaitant:

- Įrašų skaičius  
- Trūkstamų reikšmių dažnis  
- Pasiskirstymo statistika (min, max, vidurkis, dispersija)  
- KPI agregatai (pvz., pajamos, transakcijos, pretenzijos)  
- Laiku atlikimo nukrypimai arba anomalijų dažnis  

### Laiko eilučių analizė
Data Analytics vertina **stabilumą tarp periodų** — lygindamas vieną savaitę, mėnesį ar ketvirtį su kitu — naudodamas statistinį pasitikėjimą ir vizualines metrikas tendencijų stabilumui.

---

## Kaip tai veikia

1. **Įvesties duomenys** – digna renka laiko eilučių metrikas iš kitų modulių (pvz., aptiktų anomalijų skaičius).  
2. **Statistinis modeliavimas** – AI ir statistinės funkcijos identifikuoja pagrindines tendencijas ir volatilumo lygius.  
3. **Periodų palyginimas** – digna lygina istorinį ir esamą KPI arba kokybės rodiklių našumą.  
4. **Įžvalgų generavimas** – prietaisų skydai rodo aptiktas tendencijas, stabilias atkarpas ir pakeitimų taškus *Inspection Hub* ir analitiniuose vaizduose.  

Tai leidžia proaktyviai aptikti *lėtus poslinkius* arba *palaipsnį degraduojantį* duomenų kokybės sumažėjimą, kol tai tampa kritiniu.

---

## Panaudojimo scenarijai

| Use Case | Description |
|-----------|--------------|
| **Monitoring KPI stability** | Stebėkite pardavimus, transakcijas ar pretenzijas per laiką ir aptikite neįprastą volatilumą. |
| **Detecting hidden data drift** | Stebėkite lėtus pasiskirstymo ar trūkstamų reikšmių pokyčius, kuriuos įprastos taisyklės nepastebi. |
| **Change point analysis** | Nustatykite, kada metrika pakeičia elgesį (pvz., staigus anomalijų skaičiaus padidėjimas). |
| **Operational reliability** | Įvertinkite aukšto ir žemo duomenų stabilumo periodus skirtingose sistemose ar padaliniuose. |
| **Business insights** | Išryškinkite geriausiai veikiančias kategorijas ar produktus per judančius periodus. |

---

## Privalumai

| Area | Benefit |
|------|----------|
| **Matomumas** | Suteikia ilgalaikes įžvalgas apie duomenų kokybės tendencijas ir modelius. |
| **Ankstyvas įspėjimas** | Aptinka lėtus poslinkius prieš jiems išprovokuojant anomalijas ar SLA pažeidimus. |
| **Optimizavimas** | Padeda identifikuoti nestabilius duomenų šaltinius ar sistemas, kurioms reikia proceso optimizavimo. |
| **Cross-Module Analysis** | Kombinuoja duomenis iš Data Anomalies, Data Validation ir Data Timeliness, kad suteiktų holistines įžvalgas. |
| **Actionable Insights** | Padeda tiek techninėms komandoms, tiek verslo naudotojams suprasti ir veikti pagal duomenų įžvalgas. |
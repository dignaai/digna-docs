---
title: Data Timeliness – Savlaicīgas piegādes uzraudzība | digna Dokumentācija
description: Uzziniet, kā digna Data Timeliness nodrošina, ka dati ierodas noteiktajā laikā. Atklājiet aizkavētas vai trūkstošas piegādes, uzraugiet SLA un aizsargājiet biznesa procesus no klusām kavēšanām. AI darbināta detektēšana labākai datu kvalitātei un datu kanālu novērojamībai.
canonical_url: https://docs.digna.ai/platform/data_timeliness/
image: /assets/logo_square.png
keywords:
  - datu savlaicīgums
  - piegādes uzraudzība
  - datu kvalitāte
  - datu kvalitātes pārvaldība
  - datu novērojamība
  - novēlota datu atklāšana
  - trūkstošu datu brīdinājumi
  - SLA uzraudzība
  - AI piegādes analīze
  - digna Data Timeliness
lang: lv
robots: index, follow
og_title: Data Timeliness – Savlaicīgas piegādes uzraudzība | digna Dokumentācija
og_description: digna Data Timeliness automātiski atklāj aizkavētas vai trūkstošas datu piegādes, izmantojot AI. Aizsargājiet biznesa procesus, uzraugiet SLA un nodrošiniet savlaicīgus, uzticamus datus visos datu kanālos.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">AI vadīts Data Timeliness modulis datu kvalitātei un novērojamībai – digna</h1>

---

## Mērķis

**Data Timeliness** modulis nodrošina, ka **dati ierodas savlaicīgi** — katru reizi.  
Tas pastāvīgi uzrauga piegādes grafikus un automātiski atklāj, kad datu kopas, tabulas vai faili ir **aizkavējušies, trūkst vai ir nepilnīgi**.  

Apvienojot AI mācīšanos ar lietotāja definētiem grafikiem, *digna* ļauj organizācijām novērst turpmākas kļūdas un uzturēt stingrus **SLA (Service Level Agreement)** mērķus gan **Datu kvalitātei**, gan **datu kanālu novērojamībai**.

---

## Tehnisks pārskats

### Divi uzraudzības režīmi
- **AI-izmācītas ierašanās shēmas**  
  digna automātiski izprot jūsu datu piegādes dabisko ritmu — ikdienu, stundu vai notikumiem balstītu — analizējot vēsturiskos laika zīmogus un pabeigšanas laikus.  
  Tas pielāgojas izmaiņām biznesa kalendāros, brīvdienās vai mēneša beigās radušajiem pīķiem.

- **Lietotāja definēti grafiki**  
  Lietotāji var skaidri norādīt gaidāmos piegādes laikus (piem., *katru darba dienu pirms 7:30*).  
  digna salīdzina faktisko ierašanās laiku ar plānoto grafiku un izsūta brīdinājumus, ja dati kavējas vai trūkst.

### Detekcijas mehānisms
- Novērtē **metadatu laika zīmogus**, **ierakstu skaitus** un **tabulu svaigumu**  
- Atklāj **apstājušos ETL uzdevumus**, **neizdevušās ekstrakcijas** un **daļējas failu piegādes**  
- Integrējas ar *Data Anomalies* un *Data Validation* kombinētām ieskatiem

---

## Detekcijas scenāriji

| Scenario | Description |
|-----------|--------------|
| **Late data arrival** | Daily market data feed delayed by two hours, causing reports to miss SLAs |
| **Missing load** | A scheduled table or partition not updated for the current date |
| **Chained dependency delay** | Upstream job delay impacts downstream pipeline refresh |
| **Weekend pattern shift** | AI model adapts automatically when no data is expected on Sundays |

---

## Arhitektūra un izpilde

- **Izpilde datubāzē:** digna veic savlaicīguma pārbaudes tieši jūsu datubāzē vai datu noliktavā.  
- **Viegls metadatu piekļuves režīms:** nolasītas darba laika zīmogus, ierakstu skaitus un partīciju informāciju — datu izvilkšana nav nepieciešama.  
- **Konfigurējama frekvence:** plānojiet uzraudzību pēc datu kopas, shēmas vai kanāla.  
- **Krustmoduļu brīdinājumi:** rezultāti var izsaukt vizuālus brīdinājumus *Inspection Hub* vai paziņojumus pa e-pastu, Slack vai API.

---

## Piemēru lietošanas gadījumi

- **Finanšu tirgus plūsmas:** atklāj kavējumus cenu vai tirdzniecības datu atjaunināšanās.  
- **Datu noliktavas ielādes:** uzrauga, kad nakts ETL darbi beidzas vēlāk nekā paredzēts.  
- **Datu apmaiņa starp komandām:** nodrošina, ka departamentu datu piegādes notiek pirms dienas termiņiem.  
- **Regulatīvā ziņošana:** pārliecinieties, ka iesniegumi ietver jaunāko pieejamo datu momentuzņēmumu.

---

## Ieguvumi

| Area | Benefit |
|------|----------|
| **Business Continuity** | Prevents operational disruptions due to delayed or missing data |
| **Data Quality** | Improves reliability and consistency of data pipelines |
| **Compliance** | Ensures SLA adherence and audit transparency |
| **Automation** | AI eliminates manual schedule tracking |
| **Integration** | Works seamlessly with *Data Analytics* to visualize timeliness trends over time |

---

## Kā digna mācās gaidāmos piegādes laikus

1. **Vēsturiska analīze:** digna novēro iepriekšējos ielādes laikus un to ilgumu.  
2. **AI modelēšana:** machine learning izveido dinamisku pamata līniju gaidāmajai ierašanās reizei.  
3. **Uzraudzība:** katra jauna piegāde tiek salīdzināta ar šo pamata līniju.  
4. **Brīdināšana:** novirzes izraisa brīdinājumus ar kontekstiem metriku un uzticības rādītājiem.  

Šī nepārtrauktā mācīšanās pieeja pielāgojas mainīgiem procesiem, vienlaikus uzturot zemu viltus pozitīvo līmeni.

---

## Biežāk uzdotie jautājumi

**Vai es varu pašrocīgi definēt piegādes laikus?**  
Jā. digna atbalsta gan fiksētus lietotāja grafikus, gan AI-izmācītas shēmas.

**Vai tas var integrēties ar manu ETL vai orkestrācijas rīku?**  
Jā. digna integrējas ar rīkiem, piemēram, Airflow, dbt, Informatica vai pielāgotiem plānotājiem.

**Kur notiek aprēķini?**  
Visa analīze tiek veikta jūsu datubāzē vai mākoņa noliktavā — ārpakalpojums netiek izmantots.

**Kas notiek, ja dati kavējas?**  
digna izsūta brīdinājumus informācijas panelī, Inspection Hub un caur API/webhook, lai nekavējoties informētu operāciju komandas.

---


**digna Data Timeliness** palīdz nodrošināt **uzticību datiem**, apvienojot **AI-darbinātu detektēšanu**, **on-premises izpildi** un **datu novērojamību** — visu jūsu kontrolētā vidē.
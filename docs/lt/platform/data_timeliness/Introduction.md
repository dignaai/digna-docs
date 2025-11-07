---
title: Data Timeliness – Laiku pristatymo stebėjimas | digna dokumentacija
description: Sužinokite, kaip digna Data Timeliness užtikrina, kad duomenys atvyksta laiku. Aptinka vėlavimus ar trūkstamus pristatymus, stebi SLA ir apsaugo verslo procesus nuo tylinių delsimų. AI pagrįstas aptikimas geresnei duomenų kokybei ir duomenų srautų stebimumui.
canonical_url: https://docs.digna.ai/platform/data_timeliness/
image: /assets/logo_square.png
keywords:
  - duomenų laiku pristatymas
  - pristatymo stebėjimas
  - duomenų kokybė
  - duomenų kokybės užtikrinimas
  - duomenų stebimumas
  - vėluojančių duomenų aptikimas
  - trūkstamų duomenų įspėjimai
  - SLA stebėjimas
  - ai pristatymo analizė
  - digna data timeliness
lang: en
robots: index, follow
og_title: Data Timeliness – Laiku pristatymo stebėjimas | digna dokumentacija
og_description: digna Data Timeliness automatiškai aptinka vėluojamus ar trūkstamus duomenų pristatymus naudodama AI. Apsaugokite verslo procesus, stebėkite SLA ir užtikrinkite laiku bei patikimus duomenis visuose srautuose.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">AI valdomas Data Timeliness modulis duomenų kokybei ir stebimumui – digna</h1>

---

## Paskirtis

**Data Timeliness** modulis užtikrina, kad **duomenys atvyksta laiku** — kiekvieną kartą.  
Jis nuolat stebi pristatymo tvarkaraščius ir automatiškai aptinka, kada duomenų rinkiniai, lentelės arba failai yra **vėluojantys, trūkstami ar nepilni**.  

Derindama AI mokymąsi su vartotojo apibrėžtais tvarkaraščiais, *digna* leidžia organizacijoms išvengti tolimesnių klaidų ir laikytis griežtų **SLA (Service Level Agreement)** reikalavimų tiek **duomenų kokybei**, tiek **duomenų srautų stebimumui**.

---

## Techninė apžvalga

### Dvigubi stebėjimo režimai
- **AI išmokti atvykimo modeliai**  
  digna automatiškai išmoksta natūralų jūsų duomenų pristatymų ritmą — kasdienį, kasvalandinį arba įvykiais paremtą — analizuodama istorinius žymėjimus ir užbaigimo laikus.  
  Ji prisitaiko prie verslo kalendorių pakeitimų, savaitgalių ar mėnesio pabaigos piko.

- **Vartotojo apibrėžti tvarkaraščiai**  
  Vartotojai gali aiškiai nurodyti tikėtinus pristatymo laikus (pvz., *kiekvieną darbo dieną iki 7:30 ryto*).  
  digna palygina faktinį atvykimo laiką su suplanuotu tvarkaraščiu ir kelia įspėjimus, kai duomenys vėluoja arba jų nėra.

### Aptikimo mechanizmas
- Vertina **metaduomenų žymes**, **įrašų skaičių** ir **lentelių šviežumą**  
- Aptinka **sustojusius ETL darbus**, **nesėkmingas ištraukas** ir **dalis failo atvykimus**  
- Integruojasi su *Data Anomalies* ir *Data Validation* dėl papildomų įžvalgų

---

## Aptikimo scenarijai

| Scenario | Description |
|-----------|--------------|
| **Late data arrival** | Kasdieninis rinkos duomenų srautas vėluoja dvi valandas, todėl ataskaitos praleidžia SLA |
| **Missing load** | Suplanuota lentelė arba particija nėra atnaujinta už einamąją datą |
| **Chained dependency delay** | Aukštesnio lygio užduoties vėlavimas paveikia žemiau esančio srauto atnaujinimą |
| **Weekend pattern shift** | AI modelis automatiškai prisitaiko, kai sekmadieniais duomenų nėra tikėtina |

---

## Architektūra ir vykdymas

- **Vykdymas duomenų bazėje:** digna atlieka laiko patikrinimus tiesiogiai jūsų duomenų bazėje arba duomenų sandėlyje.  
- **Lengvas priėjimas prie metaduomenų:** skaito darbo žymes, įrašų skaičių ir partity informaciją — nereikia ištraukti duomenų.  
- **Konfigūruojamas dažnis:** suplanuokite stebėjimą pagal duomenų rinkinį, schemą arba srautą.  
- **Tarpmoduliniai įspėjimai:** rezultatai gali sukelti vizualinius įspėjimus *Inspection Hub* arba pranešimus el. paštu, Slack ar per API.  

---

## Pavyzdinės naudojimo scenarijos

- **Finansiniai rinkos srautai:** aptinka vėlavimus kainų ar prekybos duomenų atnaujinimuose.  
- **Duomenų sandėlio užkrovimai:** stebi, kada naktiniai ETL darbai užbaigiami vėliau nei tikėtasi.  
- **Duomenų dalijimasis tarp komandų:** užtikrina, kad departamentiniai duomenų pristatymai įvyktų iki dienos pabaigos ribinių laikų.  
- **Reguliacinė atskaita:** patikrina, ar pateikimuose yra naujausias duomenų momentinis vaizdas.  

---

## Privalumai

| Area | Benefit |
|------|----------|
| **Business Continuity** | Apsaugo nuo operacinių sutrikimų dėl vėluojančių ar trūkstamų duomenų |
| **Data Quality** | Gerina duomenų srautų patikimumą ir nuoseklumą |
| **Compliance** | UžuTinklina SLA laikymąsi ir audito skaidrumą |
| **Automation** | AI eliminuoja rankinį tvarkaraščių stebėjimą |
| **Integration** | Sklandžiai veikia su *Data Analytics*, kad vizualizuotų laiku pristatymo tendencijas per tam tikrą laiką |

---

## Kaip digna nustato tikėtinus pristatymo laikus

1. **Istorijos analizė:** digna stebi ankstesnius užkrovimo laikus ir trukmes.  
2. **AI modeliavimas:** mašininis mokymasis sukuria dinaminį bazinį lygį tikėtinam atvykimui.  
3. **Stebėjimas:** kiekvienas naujas pristatymas lyginamas su baziniu lygiu.  
4. **Įspėjimai:** nukrypimai sukelia įspėjimus su kontekstiniais metrikais ir pasitikėjimo balais.  

Šis nuolatinio mokymosi metodas prisitaiko prie kintančių procesų, tuo pačiu palaikydamas mažą klaidingų teigiamų rodiklių skaičių.

---

## Dažnai užduodami klausimai

**Ar galiu nurodyti savo pristatymo laikus?**  
Taip. digna palaiko tiek fiksuotus vartotojo tvarkaraščius, tiek AI išmoktas nuostatas.

**Ar ji gali integruotis su mano ETL arba orkestracijos įrankiu?**  
Taip. digna integruojasi su tokiais įrankiais kaip Airflow, dbt, Informatica ar pasirinktinais tvarkaraščiais.

**Kur vyksta skaičiavimai?**  
Visa analizė vykdoma jūsų duomenų bazėje arba debesies sandėlyje — nenaudojama išorinė paslauga.

**Kas nutinka, kai duomenys vėluoja?**  
digna kelia įspėjimus prietaisų skydelyje, *Inspection Hub* ir per API/webhook'us, kad operacijų komandos būtų nedelsiant informuotos.

---


**digna Data Timeliness** padeda užtikrinti **pasitikėjimą duomenimis**, derindama **AI valdomą aptikimą**, **vietinį vykdymą (on-premises)** ir **duomenų stebimumą** — viską jūsų kontroliuojamoje aplinkoje.
---
title: Data Anomalies – Anomāliju automātiska atklāšana | digna Dokumentācija
description: Uzziniet, kā digna Data Anomalies automātiski nosaka apjoma kritumus, trūkstošas vērtības, distribūcijas nobīdes un negaidītas pazīmes bez manuālas noteikumu rakstīšanas. Uzlabojiet datu kvalitāti un datu caurskatāmību datu plūsmās ar AI darbinātu anomāliju atklāšanu.
image: /assets/logo_square.png
keywords:
  - Data Anomalies
  - AI anomāliju atklāšana
  - datu kvalitātes uzraudzība
  - datu kvalitāte
  - datu novērojamība
  - trūkstošo datu atklāšana
  - datu apjoma uzraudzība
  - distribūcijas nobīde
  - datu uzticamība
  - digna Data Anomalies
lang: lv
robots: index, follow
og_title: Data Anomalies – Automātiska atklāšana | digna Dokumentācija
og_description: digna Data Anomalies automātiski atklāj novirzes datu apjomā, vērtībās un distribūcijās bez manuāli definētiem noteikumiem — uzlabojot datu kvalitāti un novērojamību dažādās platformās.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Anomalies – Anomāliju automātiska atklāšana
<h1 style="display:none;">Mākslīgā intelekta darbināts modulis datu kvalitātei un novērojamībai – digna Data Anomalies</h1>

---

## Mērķis

Modulis **Data Anomalies** automātiski identificē novirzes jūsu datu kopās — bez nepieciešamības rakstīt noteikumus.  
Tas nepārtraukti uzrauga **datu piegādes kvalitāti**, apgūstot, kā izskatās “normāls” stāvoklis, un reālā laikā konstatē novirzes.

Izmantojot AI bāzētu atklāšanu, digna atpazīst *klusās datu kļūdas*, piemēram, trūkstošus, dublētus vai bojātus ierakstus, kas var izkropļot atskaites, ML modeļus un paneļus.

---

## Tehniskais pārskats

### Analizētie metriķi

digna nepārtraukti profilē sekojošus datu aspektus:

- **Ierakstu apjoms** – kopējais rindu skaits, dienas vai partiju bāzē  
- **Trūkstošas vērtības** – nulles vai tukšu lauku atklāšana  
- **Distribūcijas un histogrammas** – datu formas izmaiņu uzraudzība  
- **Vērtību diapazoni** – automātiska ārpus diapazona vai ekstremālu vērtību identifikācija  
- **Unikalitāte** – pārbaudes dublētu atslēgu vai atkārtotu ierakstu konstatēšanai  

### Inteliģenta anomāliju atklāšana

- Izmanto **vēsturisko mācīšanos**, lai dinamiski definētu gaidāmās robežas  
- Atklāj novirzes **apjomā, vērtību distribūcijās vai loģiskajās attiecībās**  
- Pielieto AI, lai automātiski pielāgotu sliekšņus atkarībā no diennakts laika vai sezonālām svārstībām  
- Atšķir **statistiskas svārstības** no īstām anomālijām  
- Ģenerē detalizētus metriķus un pārliecības skorings katrai datu kopai un kolonnai  

---

## Atklāšanas scenāriji

Zemāk ir reālu problēmu piemēri, ko automātiski konstatē modulis **Data Anomalies**:

| Scenārijs | Apraksts |
|-----------|----------|
| **Apjoma kritumi vai pieaugumi** | Pusdienā trūkst pusei no dienas darījumiem, dubultas partiju ielādes vai pēkšņi datu pieplūdumi |
| **Trūkstošas vai nulles vērtības** | Datu izgūšana pabeigta, bet kritiskas kolonnas atstātas tukšas |
| **Distribūcijas nobīdes** | Vidējā pirkuma summa vai darījumu skaits reģionā mainās negaidīti |
| **Kolonnu apmaiņas** | Kolonnas kā *first_name* un *last_name* nejauši sakārtotas ETL procesā |
| **Negaidītas kategoriskās vērtības** | piem., “Zurich” parādās Austrijas pilsētu sarakstā |
| **Strauja unikālitātes zudums** | Iepriekš unikāli ID sāk dublēties sakarā ar augšupēja savienojuma kļūdām |

---

## Arhitektūra un izpilde

- **Izpilde datu bāzē:** Visa anomāliju atklāšanas loģika tiek izpildīta *datu bāzes dzinī* (Teradata, Snowflake, Databricks, PostgreSQL utt.)  
- **Bez datu pārvietošanas:** digna lasa tikai metriķus, nekad neizdala izejmateriālu datus ārpusē  
- **Inkrementālas atjaunināšanas:** Katru reizi analizēti tiek tikai jauni datu segmenti efektivitātes nolūkos  
- **Konfigurējama pārbaudes biežuma:** Ikstundu, ikdienas vai aktivizēta pēc augšupēja procesa  
- **Rezultātu glabāšana:** Metriķi un anomāliju marķieri tiek ierakstīti atpakaļ digna novērojamības shēmā vizualizācijai un brīdinājumiem  

---

## Ieguvumi

| Joma | Ieguvums |
|------|----------|
| **Automatizācija** | Izslēdz simtiem manuālu SQL vai noteikumu definīciju |
| **Precizitāte** | Atklāj problēmas, ko statiskie sliekšņi bieži nepamana |
| **Mērogojamība** | Efektīvi uzrauga miljonus ierakstu vienā tabulā |
| **Integrācija** | Strādā bez piepūles kopā ar *digna Data Analytics* tendences analīzei |
| **Atbilstība** | Nodrošina nepārtrauktu kontroli pār **datu kvalitāti un novērojamību** |
| **Caurspīdīgums** | Katram anomālijai nodrošina pārliecības skoru, laika zīmogu un iemesla kodus |

---

## Kā digna apgūst “normālu”

1. **Profilēšanas fāze:** digna apkopo metriķus no vēsturiskajām datu kopām.  
2. **Mācīšanās fāze:** AI modeļi identificē atkārtotas tendences (sezonālas, nedēļas, diennakts).  
3. **Uzraudzības fāze:** Nākamās datu kopas tiek salīdzinātas ar dinamiski apgūtiem sliekšņiem.  
4. **Brīdināšanas fāze:** Novirzes, kas pārsniedz statistiskās pārliecības robežas, tiek ziņotas kā anomālijas.  

Visi modeļi ir izskaidrojami, deterministiski un optimizēti uzņēmuma datu apjomiem.

---

## Piemēri lietošanas gadījumiem

- Datu kvalitātes uzraudzība **banku darījumu sistēmās**  
- Ielādes kļūdu atklāšana **ETL vai datu noliktavas uzdevumos**  
- Abnormālas klientu aktivitātes identificēšana **telekomunikāciju ierakstos**  
- Klīnisko datu konsekvences novērošana **veselības aprūpes analītikas plūsmās**  
- Salauztu panelu novēršana **BI un atskaišu vidēs**

---

## Bieži uzdotie jautājumi

**Vai Data Anomalies prasa iepriekš definētus noteikumus?**  
Nē — modulis automātiski mācās no datu uzvedības.

**Vai es joprojām varu definēt konkrētus sliekšņus, ja nepieciešams?**  
Jā. digna ļauj kombinēt AI bāzētu un noteikumu bāzētu atklāšanu (izmantojot *Data Validation*).

**Kā tiek samazinātas kļūdaini pozitīvas atrādes?**  
Modulis izmanto adaptīvu mācīšanos un statistiskā pārliecības skoringu, lai ignorētu normālas sezonālās variācijas.

**Kur notiek aprēķini?**  
Visa apstrāde notiek jūsu datu bāzē — digna nekad neizvelk izejmateriālu datus.

**Vai tas ir piemērots sensitīviem vai regulētiem datiem?**  
Jā. digna darbojas pilnībā lokāli (on-premises) vai privātā mākoņā un ievēro Eiropas atbilstības standartus.

---
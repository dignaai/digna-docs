# Data Schema Tracker – Monitor Schema Evolution
<h1 style="display:none;">AI-Driven Module for Metadata Observability and Data Quality – digna Data Schema Tracker</h1>

---

## Mērķis

The **Data Schema Tracker** informē jūs par to, kā mainās jūsu datubāzu struktūras.  
Tas nepārtraukti uzrauga **tabulu shēmas, kolonnas un datu tipus**, lai atklātu **schema drift** — mērķtiecīgas vai nejaušas strukturālas izmaiņas, kas var traucēt cauruļvadus, ETL darbus vai BI paneļus.

Nodrošinot pārredzamību shēmas evolūcijā, digna palīdz organizācijām saglabāt **uzticību datu kvalitātei**, uzturēt **datu sistēmu novērojamību** un izvairīties no dārgiem ražošanas incidentiem, ko izraisa neatklātas shēmas izmaiņas.

---

## Tehniskais pārskats

### Ko tas uzrauga

- **Pievienotas vai noņemtas kolonnas** – atklāj jaunas, pārdēvētas vai izdzēstas kolonnas.  
- **Datu tipu modifikācijas** – identificē izmaiņas, piemēram, `INT → VARCHAR` vai `DATE → TIMESTAMP`.  
- **Tabulu un skatu modifikācijas** – seko tabulu un skatu izveidei, pārdēvēšanai vai noņemšanai.  
- **Starppieredzes atšķirības** – salīdzina shēmas versijas starp Dev, Test un Production vidi.  

### Atklāšana un brīdināšana

- Skenē **datubāzes metadatus** vai **sistēmas katalogus** tieši jūsu datu platformā.  
- Salīdzina katru shēmas momentuzņēmumu ar iepriekš zināmo versiju, kas saglabāta digna observability shēmā.  
- Ģenerē **reāllaika brīdinājumus** informācijas panelī, caur API vai ārējos paziņošanas kanālos (e-pasts, Slack, webhook).  
- Reģistrē katru shēmas versiju **vēsturiskai izsekošanai un audita sagatavotībai**.

---

## Arhitektūra un izpilde

- **In-Database izpilde:** digna darbojas pilnīgi jūsu vidē, vaicājot metadatu skatus, neizvelkot nevienu lietotāju datus.  
- **Viegls skenēšanas režīms:** piekļūst tikai strukturālajai informācijai — nekad lietotāja datiem.  
- **Centralizēta uzglabāšana:** shēmas metadati un driftu ieraksti tiek glabāti digna observability shēmā vizualizācijai un analītikai.  
- **Automatizācija:** atbalsta plānotus vai notikumu bāzētus skenējumus caur digna Core vai ārējiem orķestrācijas rīkiem.  

---

## Piemēri lietošanas gadījumiem

| Use Case | Description |
|-----------|--------------|
| **ETL Stability Monitoring** | Atklāj augšupvērstās struktūras izmaiņas, pirms cauruļvadi avarē sakarā ar shēmas neatbilstībām. |
| **Business Intelligence Reliability** | Novērš bojātus paneļus, ko izraisa pārdēvētas vai trūkstošas kolonnas. |
| **Data Warehouse Governance** | Uztur auditable vēsturi par shēmas evolūciju atbilstībai un ietekmes analīzei. |
| **Integration Oversight** | Nodrošina, ka datu ezera un noliktavas shēmas paliek sinhronizētas pēc strukturālām atjaunināšanām. |

---

## Ieguvumi

| Area | Benefit |
|------|----------|
| **Data Quality** | Novērš neatklātu shēmas driftu, kas var korumpēt vai devalidēt datu cauruļvadus. |
| **Observability** | Pievieno strukturālo uzraudzību kopējai datu ekosistēmu novērojamībai. |
| **Compliance** | Saglabā versiju shēmas vēsturi auditiem, izsekojamībai un izmaiņu kontrolei. |
| **Prevention** | Atklāj strukturālas problēmas pirms tām pāraugot ziņošanas vai ražošanas kļūdās. |

---

## Kā tas darbojas

1. **Momentuzņēmuma vākšana** – digna savāc pašreizējos shēmas metadatus.  
2. **Salīdzināšana** – jaunais momentuzņēmums tiek salīdzināts
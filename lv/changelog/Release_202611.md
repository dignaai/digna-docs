# Izmaiņu žurnāls – versija 2026.11  

Izlaidums 2026.11 ir veidots ap trim lieliem papildinājumiem:

- **digna Data Reconciliation (Beta)**: pārbauda, vai dati paliek saskaņoti, pārvietojoties starp sistēmām  
- **digna Agentic (Beta)**: atver digna AI aģentiem, izmantojot digna MCP Server  
- **digna Engine**: pēc izvēles profilē datus pašā digna un ļauj veikt referenciālās integritātes pārbaudes starp dažādām datu bāzu tehnoloģijām  

---

## Jaunumi  

### digna Data Reconciliation (Beta) – avota un mērķa saskaņotība  
Pirms dati nonāk atskaitē, tie bieži iziet cauri vairākām sistēmām. digna Data Reconciliation (Beta) salīdzina **mērķa** datu avotu ar **avotiem**, no kuriem tas izveidots, un brīdina, ja tie vairs nesakrīt.

- Konfigurē kā nosauktus noteikumus mērķa datu avota jaunajā cilnē **Data Reconciliation**  
- Par avotu var būt jebkurš projekta datu avots, kuram ir ieslēgts Data Reconciliation  
- Lietojuma gadījumi ietver standarta saskaņošanas procedūras un ETL procesu rezultātu validāciju  
- Divu veidu noteikumi: **Exact** un **AI**  

**Exact noteikumi – saskaņošana kā datu kvalitātes noteikums**: jūs precīzi nosakāt, kam jāsakrīt starp vienu avotu un vienu mērķi, līdzīgi kā datu kvalitātes noteikumā.

  - Salīdziniet vienu avota datu avotu ar vienu mērķa datu avotu  
  - Sasaistiet mērķa pārbaudi ar avota pārbaudi pēc statistikas un atribūta, piem., rindu skaitu vai summas kolonnas kopsummu  
  - Pieļaujiet atšķirību ar **absolute** pielaidi (piem., ± 10) vai **relative** pielaidi (piem., ± 0,5 % no avota vērtības)  
  - Laika skala parāda katras dienas atšķirību attiecībā pret pielaidi  

**AI noteikumi – saskaņošana kā datu novērošana (data observability)**: digna iemācās, kā mērķis seko saviem avotiem, līdzīgi kā digna novēro datus citos moduļos, un brīdina, kad šī sakarība tiek pārrauta.

  - Apvienojiet vairāku avota datu avotu pārbaudes ar viena mērķa pārbaudēm  
  - Nav jāzina vai jāpieraksta loģika starp tiem (savienojumi, filtri, agregācijas)  
  - Modelis no vēstures iemācās, kā mērķis tajā pašā dienā seko saviem avotiem  
  - Katra mērķa pārbaude tiek prognozēta no dienas avota vērtībām, un digna brīdina, kad mērķis iziet ārpus noteikuma paša iepriekšējo kļūdu joslas  
  - Katram noteikumam ir savi **Model settings**: **Sensitivity**, **Memory** un **Model Complexity**  

Saskaņošanas pārbaudes tiek rādītas informācijas panelī ar atsevišķu laika skalu katram noteikumam. Tās tiek ieskaitītas kopējā inspekcijas statusā un izraisa paziņojumus.

**Ietekme:** Aptver abas saskaņošanas puses. Exact noteikumi nodrošina zināmas kontroles starp avotu un mērķi, bet AI noteikumi uzrauga sarežģītas plūsmas, piemēram, ETL procesus, tāpēc ceļā pazaudēti vai mainīti dati tiek pamanīti bez manuāli rakstīta saskaņošanas SQL.

---

### digna Agentic (Beta) – digna AI aģentiem  
Pirmā digna Agentic (Beta) versija. AI aģenti tagad var strādāt ar digna, atbildēt uz biznesa jautājumiem par jūsu datiem un palīdzēt uzlabot jūsu konfigurāciju.

**digna MCP Server**: ļauj Claude un citiem AI aģentiem strādāt ar digna, izmantojot Model Context Protocol.

  - Pārvaldiet projektus, datu avotus, noteikumus, inspekciju grafikus un abonementus  
  - Lasiet inspekciju statusus līdz pat atsevišķai pārbaudei, lai izmeklētu brīdinājumus  

**Datu avotu un atribūtu apraksti**: vienkāršā valodā aprakstiet, ko satur datu avots vai atribūts.

  - AI aģenti izmanto aprakstus, lai interpretētu jūsu datus  
  - Uzdodiet biznesa jautājumus par saviem datiem, un AI aģenti uz tiem atbild, balstoties uz to, ko digna uzrauga  
  - Ja pašreizējā digna konfigurācija nespēj atbildēt uz jautājumu, AI aģents, ja iespējams, iesaka izmaiņas datu avotā un tā atribūtos, piem., jaunas datu kopas pievienošanu  

**Ietekme:** Ļauj vienkāršā valodā uzdot biznesa jautājumus par saviem datiem un ļauj AI aģentiem palīdzēt konfigurēt digna un izmeklēt datu kvalitātes problēmas.

---

### digna Engine – profilējiet tur, kur izvēlaties  
Pēc noklusējuma digna profilē datus tur, kur tie atrodas, – avota datu bāzē. digna Engine piedāvā papildu iespēju: digna eksportē datus no avota un profilē tos digna Engine iekšienē.

- Pēc izvēles, nevis obligāti: profilēšana avota datu bāzē joprojām ir pieejama  
- Tiek izvēlēta katram datu bāzes savienojumam kā tā **profilēšanas vieta**: **Source Database** vai **digna Engine**  
- Pieejams visām atbalstītajām avota tehnoloģijām  

**Referenciālā integritāte starp savienojumiem**: dažām pārbaudēm dati ir jāeksportē. Šādos gadījumos digna Engine paplašina **digna Data Validation**.

  - **Referenciālās integritātes pārbaudes** starp datu avotiem, kas atrodas **dažādos datu bāzes savienojumos**, tostarp dažādās datu bāzu tehnoloģijās (piem., Oracle un PostgreSQL)  
  - Darbojas ar abām profilēšanas vietām: Source Database gadījumā uz digna Engine tiek eksportētas tikai atslēgas kolonnas  
  - Informācijas panelis parāda, kad pārbaude darbojas starp diviem savienojumiem  

**Ietekme:** Ļauj izvēlēties, kur dati tiek profilēti, un nodrošina sakarības starp sistēmām, kas darbojas ar dažādām datu bāzu tehnoloģijām.

---

## Profilēšanas uzlabojumi  

Šis izlaidums arī dod lietotājiem lielāku kontroli pār to, kas un kā tiek profilēts.

### Vaicājumu atribūti – lietotāja definētas kolonnas  
- Definējiet mākslīgas kolonnas: SQL izteiksmi pār vienu vai vairākām datu avota kolonnām  
- Katram vaicājuma atribūtam ir savs nosaukums  
- Tiek profilēts un pārbaudīts tāpat kā jebkurš cits atribūts  

### DATE kolonnu kategorija  
- Jauna atribūtu kategorija **Date**  
- Metrikas attiecībā pret inspicēto datumu  

### Profilēšana pēc pieprasījuma  
- Profilējiet jebkuru atribūtu pret vienas dienas pilnu momentuzņēmumu, nepalaižot inspekciju  
- Palīdz iestatīt atribūta kolonnas tipu: **Numerical**, **Categorical**, **Date** vai **Unspecified**  

---

## Kam šī versija noder  

- **Datu inženieri:** ETL rezultātu validācija ar digna Data Reconciliation (Beta)  
- **Finanšu, risku un kontrolinga komandas:** standarta saskaņošanas procedūras kā Exact noteikumi digna Data Reconciliation (Beta)  
- **Datu kvalitātes un pārvaldības komandas:** referenciālā integritāte starp datu bāzu tehnoloģijām ar digna Engine  
- **Biznesa lietotāji:** atbildes uz biznesa jautājumiem par datiem no AI aģentiem ar digna Agentic (Beta)  
- **AI un automatizācijas komandas:** AI aģenti, kas strādā ar digna, izmantojot digna Agentic (Beta)  

---

## CLI atjauninājumi  
- Izmaiņu nav  

---
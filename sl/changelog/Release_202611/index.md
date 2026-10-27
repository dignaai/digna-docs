# Changelog – Izdaja 2026.11  

Izdaja 2026.11 temelji na treh pomembnih novostih:

- **digna Data Reconciliation (Beta)**: preverja, ali podatki ostanejo konsistentni, ko se premikajo med sistemi  
- **digna Agentic (Beta)**: prek digna MCP Server odpre digno AI agentom  
- **digna Engine**: po želji profilira podatke znotraj digne in omogoča preverjanja referenčne celovitosti med različnimi tehnologijami baz podatkov  

---

## Nove Funkcije  

### digna Data Reconciliation (Beta) – Konsistentnost od Vira do Cilja  
Podatki pogosto potujejo skozi več sistemov, preden pridejo v poročilo. digna Data Reconciliation (Beta) primerja **ciljni** podatkovni vir z **viri**, iz katerih je bil zgrajen, in sproži opozorilo, ko se ne ujemajo več.

- Konfigurira se kot poimenovana pravila na novem zavihku **Data Reconciliation** ciljnega podatkovnega vira  
- Vir je lahko kateri koli podatkovni vir projekta, ki ima vklopljen Data Reconciliation  
- Primeri uporabe vključujejo standardne postopke usklajevanja in validacijo rezultatov procesov ETL  
- Dve vrsti pravil: **Exact** in **AI**  

**Pravila Exact – usklajevanje kot pravilo kakovosti podatkov**: Natančno določite, kaj se mora ujemati med enim virom in enim ciljem, podobno kot pri pravilu kakovosti podatkov.

  - Primerjava enega izvornega podatkovnega vira z enim ciljnim podatkovnim virom  
  - Povezovanje preverjanja cilja s preverjanjem vira po statistiki in atributu, npr. število vrstic ali vsota stolpca z zneski  
  - Dovoljeno odstopanje z **absolute** toleranco (npr. ± 10) ali **relative** toleranco (npr. ± 0,5 % vira)  
  - Časovnica za vsak dan prikazuje odstopanje glede na toleranco  

**Pravila AI – usklajevanje kot opazovanje podatkov**: digna se nauči, kako cilj sledi svojim virom, na enak način, kot opazuje podatke v drugih modulih, in sproži opozorilo, ko se ta odnos prekine.

  - Združevanje preverjanj iz več izvornih podatkovnih virov s preverjanji enega cilja  
  - Logike med njimi (joini, filtri, agregacije) ni treba poznati ali zapisati  
  - Model se iz zgodovine nauči, kako cilj na isti dan sledi svojim virom  
  - Vsako preverjanje cilja je napovedano iz vrednosti virov tistega dne, digna pa sproži opozorilo, ko cilj zapusti pas lastnih preteklih napak pravila  
  - Vsako pravilo ima lastne **Model settings**: **Sensitivity**, **Memory** in **Model Complexity**  

Preverjanja usklajevanja so prikazana na Dashboardu s časovnico za vsako pravilo. Štejejo v skupni status inšpekcije in sprožajo obvestila.

**Vpliv:** Pokriva obe strani usklajevanja. Pravila Exact uveljavljajo znane kontrole med virom in ciljem, pravila AI pa nadzorujejo kompleksne tokove, kot so procesi ETL, tako da so podatki, ki se na poti izgubijo ali spremenijo, zaznani brez ročno napisanega SQL za usklajevanje.

---

### digna Agentic (Beta) – digna za AI Agente  
Prva različica digna Agentic (Beta). AI agenti lahko zdaj delajo z digno, odgovarjajo na poslovna vprašanja o vaših podatkih in pomagajo izboljšati vašo konfiguracijo.

**digna MCP Server**: Omogoča, da Claude in drugi AI agenti delajo z digno prek Model Context Protocol.

  - Upravljanje projektov, podatkovnih virov, pravil, urnikov inšpekcij in naročnin  
  - Branje statusov inšpekcij vse do posameznega preverjanja za preiskovanje opozoril  

**Opisi podatkovnih virov in atributov**: Z navadnim jezikom opišite, kaj vsebuje podatkovni vir ali atribut.

  - AI agenti uporabljajo opise za interpretacijo vaših podatkov  
  - Postavljajte poslovna vprašanja o svojih podatkih, AI agenti pa nanje odgovorijo na podlagi tega, kar nadzoruje digna  
  - Če trenutna konfiguracija digne ne more odgovoriti na vprašanje, AI agent, kjer je mogoče, predlaga spremembe podatkovnega vira in njegovih atributov, npr. dodajanje novega dataseta  

**Vpliv:** Omogoča vam, da v navadnem jeziku postavljate poslovna vprašanja o svojih podatkih, AI agentom pa, da pomagajo konfigurirati digno in preiskovati težave s kakovostjo podatkov.

---

### digna Engine – Profiliranje Tam, Kjer Izberete  
Privzeto digna profilira podatke tam, kjer so, v izvorni bazi podatkov. digna Engine doda možnost: digna izvozi podatke iz vira in jih profilira znotraj digna Engine.

- Izbirno, ne obvezno: profiliranje v izvorni bazi podatkov ostaja na voljo  
- Izbere se za vsako povezavo do baze podatkov kot njena **lokacija profiliranja**: **Source Database** ali **digna Engine**  
- Na voljo za vse podprte izvorne tehnologije  

**Referenčna celovitost med povezavami**: Nekatera preverjanja zahtevajo izvoz podatkov. digna Engine za te primere razširi **digna Data Validation**.

  - **Preverjanja referenčne celovitosti** med podatkovnimi viri na **različnih povezavah do baz podatkov**, vključno z različnimi tehnologijami baz podatkov (npr. Oracle in PostgreSQL)  
  - Deluje z obema lokacijama profiliranja: pri Source Database se v digna Engine izvozijo le ključni stolpci  
  - Nadzorna plošča prikaže, kdaj se preverjanje izvaja prek dveh povezav  

**Vpliv:** Omogoča izbiro, kje se podatki profilirajo, in uveljavlja odnose med sistemi, ki delujejo na različnih tehnologijah baz podatkov.

---

## Izboljšave Profiliranja  

Ta izdaja uporabnikom daje tudi več nadzora nad tem, kaj se profilira in kako.

### Poizvedbeni Atributi – Uporabniško Definirani Stolpci  
- Definirajte umetne stolpce: izraz SQL nad enim ali več stolpci podatkovnega vira  
- Vsak poizvedbeni atribut ima svoje ime  
- Profilira in preverja se kot kateri koli drug atribut  

### Kategorija Stolpcev DATE  
- Nova kategorija **Date** za atribute  
- Metrike glede na datum inšpekcije  

### Profiliranje na Zahtevo  
- Profilirajte kateri koli atribut na celotnem posnetku enega datuma, brez zagona inšpekcije  
- Pomaga nastaviti vrsto stolpca atributa: **Numerical**, **Categorical**, **Date** ali **Unspecified**  

---

## Kdo Ima Koristi od Te Izdaje  

- **Data Engineers:** validacija rezultatov ETL z digna Data Reconciliation (Beta)  
- **Ekipe za finance, tveganja in kontroling:** standardni postopki usklajevanja kot pravila Exact v digna Data Reconciliation (Beta)  
- **Data Quality & Governance Teams:** referenčna celovitost med tehnologijami baz podatkov z digna Engine  
- **Poslovni uporabniki:** poslovna vprašanja o podatkih, na katera odgovarjajo AI agenti z digna Agentic (Beta)  
- **Ekipe za AI in avtomatizacijo:** AI agenti, ki delajo z digno prek digna Agentic (Beta)  

---

## Posodobitve CLI  
- Brez sprememb  

---
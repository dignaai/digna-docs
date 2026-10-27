# Ændringslog – Release 2026.11  

Release 2026.11 er bygget op omkring tre store nyheder:

- **digna Data Reconciliation**: kontrollerer, at data forbliver konsistente, når de flyttes mellem systemer  
- **digna Agentic**: åbner digna for AI-agenter via digna MCP Server  
- **digna Engine**: profilerer valgfrit data inde i digna og muliggør kontroller af referentiel integritet mellem forskellige databaseteknologier  

---

## Nye funktioner  

### digna Data Reconciliation (Beta) – Konsistens fra kilde til mål  
Data passerer ofte gennem flere systemer, før de når frem til en rapport. digna Data Reconciliation sammenligner en **mål**-datakilde med de **kilder**, den er bygget ud fra, og advarer, når de ikke længere stemmer overens.

- Konfigureres som navngivne regler på den nye fane **Data Reconciliation** i måldatakilden  
- Enhver datakilde i projektet, hvor Data Reconciliation er slået til, kan være en kilde  
- Anvendelser omfatter blandt andet standardafstemningsprocedurer og validering af resultaterne fra ETL-processer  
- To typer regler: **Exact** og **AI**  

**Exact-regler – Afstemning som en datakvalitetsregel**: Du definerer præcist, hvad der skal stemme overens mellem én kilde og ét mål, ligesom i en datakvalitetsregel.

  - Sammenlign én kildedatakilde med én måldatakilde  
  - Par en kontrol i målet med en kontrol i kilden efter statistik og attribut, f.eks. antal rækker eller summen af en beløbskolonne  
  - Tillad en difference med en **absolute** tolerance (f.eks. ± 10) eller en **relative** tolerance (f.eks. ± 0,5 % af kilden)  
  - Tidslinjen viser hver dags difference i forhold til tolerancen  

**AI-regler – Afstemning som data observability**: digna lærer, hvordan et mål følger sine kilder, på samme måde som digna observerer data i andre moduler, og advarer, når sammenhængen brydes.

  - Kombiner kontroller fra flere kildedatakilder med kontrollerne i ét mål  
  - Du behøver ikke at kende eller nedskrive logikken mellem dem (joins, filtre, aggregeringer)  
  - En model lærer ud fra historikken, hvordan målet følger sine kilder på samme dag  
  - Hver kontrol i målet forudsiges ud fra dagens kildeværdier, og digna advarer, når målet forlader det bånd, som reglens egne tidligere fejl danner  
  - Hver regel har sine egne **Model settings**: **Sensitivity**, **Memory** og **Model Complexity**  

Afstemningskontroller vises på Dashboard med en tidslinje pr. regel. De tæller med i den samlede inspektionsstatus og udløser notifikationer.

**Indvirkning:** Dækker begge sider af afstemningen. Exact-regler håndhæver kendte kontroller mellem kilde og mål, og AI-regler overvåger komplekse flows som ETL-processer, så data, der går tabt eller ændres undervejs, fanges uden håndskrevet afstemnings-SQL.

---

### digna Agentic (Beta) – digna til AI-agenter  
Den første version af digna Agentic. AI-agenter kan nu arbejde med digna, besvare forretningsspørgsmål om dine data og hjælpe med at forbedre din konfiguration.

**digna MCP Server**: Lader Claude og andre AI-agenter arbejde med digna via Model Context Protocol.

  - Administrer projekter, datakilder, regler, inspektionsplaner og abonnementer  
  - Læs inspektionsstatusser helt ned til den enkelte kontrol for at undersøge alerts  

**Beskrivelser af datakilder og attributter**: Beskriv i almindeligt sprog, hvad en datakilde eller en attribut indeholder.

  - AI-agenter bruger beskrivelserne til at fortolke dine data  
  - Stil forretningsspørgsmål om dine data, og AI-agenter besvarer dem ud fra det, digna overvåger  
  - Hvis dignas nuværende konfiguration ikke kan besvare et spørgsmål, foreslår AI-agenten så vidt muligt ændringer af datakilden og dens attributter, f.eks. at tilføje et nyt datasæt  

**Indvirkning:** Lader dig stille forretningsspørgsmål om dine data i almindeligt sprog og lader AI-agenter hjælpe med at konfigurere digna og undersøge datakvalitetsproblemer.

---

### digna Engine – Profilér, hvor du vælger  
Som standard profilerer digna data dér, hvor de ligger, i kildedatabasen. digna Engine tilføjer en mulighed: digna eksporterer data fra kilden og profilerer dem inde i digna Engine.

- Valgfrit, ikke obligatorisk: profilering i kildedatabasen er fortsat tilgængelig  
- Vælges pr. databaseforbindelse som dens **profileringssted**: **Source Database** eller **digna Engine**  
- Tilgængelig for alle understøttede kildeteknologier  

**Referentiel integritet på tværs af forbindelser**: Nogle kontroller kræver, at data eksporteres. digna Engine udvider **digna Data Validation** til disse tilfælde.

  - **Kontroller af referentiel integritet** mellem datakilder på **forskellige databaseforbindelser**, også med forskellige databaseteknologier (f.eks. Oracle og PostgreSQL)  
  - Fungerer med begge profileringssteder: for Source Database eksporteres kun nøglekolonnerne til digna Engine  
  - Dashboardet viser, når en kontrol kører på tværs af to forbindelser  

**Indvirkning:** Lader dig vælge, hvor data profileres, og håndhæver relationer mellem systemer, der kører på forskellige databaseteknologier.

---

## Forbedringer af profilering  

Denne udgivelse giver også brugerne mere kontrol over, hvad der profileres, og hvordan.

### Forespørgselsattributter – Brugerdefinerede kolonner  
- Definer kunstige kolonner: et SQL-udtryk over en eller flere kolonner i datakilden  
- Hver forespørgselsattribut har sit eget navn  
- Profileres og kontrolleres som enhver anden attribut  

### Kolonnekategorien DATE  
- Ny kategori **Date** til attributter  
- Målinger i forhold til den inspicerede dato  

### Profilering efter behov  
- Profilér en vilkårlig attribut mod et fuldt øjebliksbillede for én dato uden at køre en inspektion  
- Hjælper med at angive attributtens kolonnetype: **Numerical**, **Categorical**, **Date** eller **Unspecified**  

---

## Hvem får gavn af denne udgivelse  

- **Data Engineers:** Validering af ETL-resultater med digna Data Reconciliation  
- **Finans-, risiko- og controllingteams:** Standardafstemningsprocedurer som eksakte regler i digna Data Reconciliation  
- **Datakvalitets- og governance-teams:** Referentiel integritet på tværs af databaseteknologier med digna Engine  
- **Forretningsbrugere:** Forretningsspørgsmål om data besvaret af AI-agenter med digna Agentic  
- **AI- og automationsteams:** AI-agenter, der arbejder med digna via digna Agentic  

---

## CLI-opdateringer  
- Ingen ændringer  

---
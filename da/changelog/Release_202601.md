# Ændringslog – Release 2026.01  

Med Release 2026.01 introducerer digna væsentlige forbedringer i datasource-modellering, håndtering af forbindelser og brugervenlighed ved inspektioner.  
Denne release øger fleksibiliteten på tværs af alle moduler og udvider markant dækningen af **data quality og validering**.

---

## Nye funktioner  

### Global Database Connections  
- Databaseforbindelser konfigureres nu på et **globalt niveau**.  
- Globale forbindelser kan genbruges på tværs af **alle projekter**, hvilket forenkler konfiguration og vedligehold.  
- **Betydning:** Reducerer operationelt arbejde og sikrer konsistent forbindelse på tværs af miljøer.

### Multiple Source Connections per Project  
- Projekter kan nu referere til **flere source connection-konfigurationer**.  
- Muliggør mere fleksible setup til komplekse datalandskaber per projekt.  
- **Betydning:** Understøtter realistiske enterprise-arkitekturer med heterogene datakilder.

### Logical Datasources  
- Datasources repræsenterer nu et **logisk lag** i et projekt.  
- Hver datasource kan være baseret på:
    - en **database table**
    - en **database view**
    - en **custom SQL statement**  
- Denne separation forbedrer genbrug, tydelighed og inspektionsmodellering på tværs af moduler.  
- **Betydning:** Afkobler inspektioner og data quality-regler fra fysisk lagring, hvilket forbedrer vedligeholdelse og genbrug.

### Anomaly Relevance Condition  
- En **Anomaly Relevance Condition** kan nu defineres for at styre evalueringen af anomalier på datasætniveau.  
- Statistikker beregnes uafhængigt af, om betingelsen er sat eller opfyldt.  
- Hvis betingelsen **ikke er opfyldt**, leverer **digna Data Anomalies** ikke anomalistatus (grøn / gul / rød).  
- **Eksempel:** Udeluk datasættet fra anomalievurdering, når antallet af rækker er under 10.  
- **Betydning:** Sikrer, at anomalier kun vurderes i relevante forretningskontekster.

### Per-Module Notification Configuration  
- Notifikationer kan nu konfigureres **per modul** direkte i digna.  
- Giver uafhængig styring af alert-adfærd for **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** og andre moduler.  
- **Betydning:** Muliggør præcise alarmeringsstrategier, der matcher teamansvar og kritikalitet.

### Inspection Results Export (CSV)  
- Brugere kan nu **downloade inspektionsresultater som CSV-filer**.  
- Muliggør offline-analyse, rapportering og integration med eksterne værktøjer.  
- **Betydning:** Forenkler revisioner, rapportering og efterfølgende data quality-analyser.

---

## Udvidede data-valideringsmuligheder  

Med denne release understøtter **digna Data Validation** nu et omfattende sæt af data quality-regler:

- **Row-level validation rules**  
- **Multi-column uniqueness checks**  
- **Referential integrity validation across datasources**

Sammen gør disse kontroller det muligt at håndhæve **strukturelle og relationelle data quality-regler** på tværs af komplekse datalandskaber.

### Uniqueness Checks for Multiple Columns
- Introduceret **Uniqueness Checks** for et konfigurerbart **sæt af kolonner**.  
- Muliggør validering af sammensatte nøgler og forretningsmæssige unikhedskrav.  
- **Betydning:** Finder dubletter af forretningsentiteter, som ikke kan identificeres med enkeltkolonne-kontroller.

### Referential Integrity Checkss
- Introduceret **Referential Integrity Checks** til validering af relationer mellem datasources.  
- Sikrer, at **foreign key values** i en kilde-datasource findes i en refereret target-datasource.  
- Hjælper med at opdage forældreløse rækker, brudte relationer og dataintegritetsproblemer tidligt.  
- Designet til at fungere med **logiske datasources**, herunder views og custom SQL.  
- **Anvendelsestilfælde:** datalager-integritet, regulatorisk rapportering, masterdata-konsistens og pålidelig downstream-analyse.

---

## Hvem får gavn af denne release  

- **Data Engineers:** Mere fleksibel datasource-modellering og genbrugelige databaseforbindelser  
- **Data Quality & Governance Teams:** Udvidet valideringsdækning inklusive relationelle integritetsregler  
- **Analytics & BI Teams:** Renere input og eksporterbare inspektionsresultater  
- **Platform Owners:** Mindre konfigurationskompleksitet og forbedret operationel vedligehold

---

## CLI-opdateringer  
- Ingen ændringer

---
# Endringslogg – Release 2026.06  

Med Release 2026.06 tar digna et stort steg fremover innen automatisering, utvidbarhet og plattformbrukervennlighet.  
Denne utgivelsen introduserer det nye **digna Python SDK**, offisiell **Docker-distribusjonsstøtte**, en oppfrisket dashboard-opplevelse og forbedret portabilitet for håndtering av valideringsregler.

---

## Se utgivelsen

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — en gjennomgang av denne utgivelsen på dignas YouTube-kanal.*

---

## Nye funksjoner  

### digna Python SDK – Automatiser alt med Python  
- Installer via:
  ```bash
  pip install digna-sdk
  ```
- Administrer og automatiser digna programmessig med Python  
- Opprett og konfigurer prosjekter gjennom kode  
- Utløs inspeksjoner og overvåkningskjøringer  
- Håndter datasett, regler og konfigurasjoner programmessig  
- Profiler tabeller og hent ut metadata‑innsikt  
- Eksporter profilering og resultater for datakvalitet til eksterne repoer og systemer  
- Integrer med notebooks, orkestreringsverktøy og CI/CD‑pipelines  

Effekt: Gjør det mulig med full infrastruktur som kode og dyp automatisering av arbeidsflyter for datakvalitet og observabilitet ved hjelp av Python.

---

### Docker-støtte – Forenklet distribusjon og drift  
- Offisiell Docker-image-støtte for digna  
- Rask og konsistent oppsett på tvers av miljøer  
- Forenklet onboarding for utvikling, test og produksjon  
- Enkel integrasjon med Kubernetes og containerplattformer  
- Bedre portabilitet og reproduserbarhet av utrullinger  

Effekt: Gjør digna enklere å distribuere og drifte i moderne cloud-native arkitekturer.

---

### QueryMode – Fleksibel strategi for SQL‑utførelse

Konfigurer spørringsutførelsesstrategi: **Single** eller **Combined** modus

**Single Mode**: Hver statistikk beregnes med én dedikert SQL-spørring

  - Ideelt for store datakilder hvor minnebegrensninger er en utfordring  
  - Hindrer ressursuttømming i kombinerte spørringer (out of memory, spool‑begrensninger)  
  - Høyere antall spørringer, men lavere minnebruk per spørring

**Combined Mode**: Alle statistikker beregnes innenfor én enkelt SQL-spørring

  - Reduserer totalt antall spørringer og nettverkskostnader  
  - Optimaliserer ytelse når datakilder er håndterbare i minnet  
  - Mer effektivt for hyppige, parallelle kjøringer

Effekt: Gir brukere finmasket kontroll over spørringsutførelse for å balansere ytelse, ressursbruk og minnesikkerhet basert på egenskapene til deres datakilder.

---

### Konfigurerbar prediksjonsmodell

Modellen bak avviksdeteksjonen veier nå konkurrerende forklaringer av hver serie opp mot hverandre – et mønster kombinert med en tolkning av de nyeste observasjonene – og blander prognosene deres etter hvor sterkt hver av dem støttes. En enkelt ekstremverdi kan ikke lenger lekke inn i de påfølgende prediksjonene.

To innstillinger på datakildens nye fane **Model** styrer den, hver fra `0.0` til `1.0` med `0.5` som standard:

- **Break Sensitivity** – hvor raskt et hopp til et nytt nivå eller en trend som snur blir godtatt i stedet for å behandles som uteliggere
- **Model Complexity** – hvor mye struktur modellen leter etter, fra kalendereffekter og ett enkelt nivåskift opp til ukjente sykluser, effekter knyttet til dag i måneden og månedlige nullstillinger

Begge kan når som helst tilbakestilles til standardverdiene. Se [Modellinnstillinger](../platform/data_anomalies/how_it_works.md#model-settings) for hvordan hver av dem virker.

Effekt: Gir brukerne kontroll over selve prediksjonsmodellen, ved siden av de eksisterende innstillingene Sensitivity og Memory på toleransebåndet, som nå ligger på fanen **Thresholds**.

---

### Kontroll over avviksvarsler

- Ny fane **Notifications** i datakildens avviksinnstillinger:
  - **Minimum Alerts** – hvor mange mislykkede kontroller (ikke usikre) en inspeksjon trenger før et varsel sendes (standard `1`)
  - **Pause After Notification (Days)** – hvor lenge et abonnement forblir stille etter å ha varslet om datakilden (standard `0`, ingen pause)
- Abonnenter varsles nå når en inspeksjon feiler fullstendig (**Notify Inspection Errors**)
- Hvert varsel lenker direkte til siden det gjelder – de mislykkede kontrollene i inspeksjonen, eller visningene for Schema Tracker og Timeliness
- Tydeligere abonnementsbrytere: **Notify on Passed Inspections**, **Notify Inspection Errors**, **Notify Data Volume Checks**

Slik fungerer varsler: varsler sendes gjennom **varslingskanaler** – Email (via en SMTP-tilkobling), Slack eller Jira – som administratorer setter opp og kan kontrollere med **Test Notification Channel**. Et **abonnement** kobler en kanal til et prosjekt: det dekker alle datakilder eller utvalgte, og bryterne velger hva det rapporterer – hver modul (Data Anomalies, Data Validation, Data Analytics, Timeliness, Schema Tracker og kontroller av datavolum), inspeksjoner som feiler fullstendig, og eventuelt også beståtte inspeksjoner.

Effekt: Færre og mer handlingsrettede varsler – isolerte avvik og vedvarende anomalier oversvømmer ikke lenger kanalen.

---

### Omdesignet dashboard-opplevelse  
- Modernisert og forbedret UI/UX‑design  
- Klarere navigasjon og struktur  
- Bedre synlighet av overvåkingsresultater og innsikt i datakvalitet  
- Forbedret lesbarhet av varsler, statistikker og dashboards  
- Raskere tilgang til viktig driftsinformasjon  

Effekt: Øker brukervennlighet og daglig produktivitet for alle brukere.

---

### Utvidet import og eksport for valideringsregler  
- Forbedret import-/eksportfunksjonalitet for valideringsregler  
- Enklere migrering mellom miljøer og prosjekter  
- Bedre gjenbruk av standardiserte regelsett  
- Forbedret styring og livssyklushåndtering av regler  
- Forenklet samarbeid på tvers av team  

Effekt: Legger til rette for skalerbar og konsistent styring av datakvalitet i hele organisasjonen.

---

## Plattformforbedringer  

- Full Python SDK‑integrasjon for automatisering  
- Containerisert utrulling via Docker  
- Forbedret UX gjennom omdesignet dashboard  
- Utvidet portabilitet for valideringslogikk  

---

## Hvem drar nytte av denne utgivelsen  

- Dataingeniører: automatisering, bruk av SDK, pipeline-integrasjon  
- Plattformteam: forenklet utrulling via Docker  
- Team for datastyring: gjenbrukbar håndtering av valideringsregler  
- Analyseteam: forbedret brukervennlighet og bedre synlighet av innsikt  

---

## CLI‑oppdateringer  
- La til støtte for SDK‑integrasjon  
- Forbedrede import-/eksportarbeidsflyter  
- Generelle stabilitets‑ og ytelsesforbedringer
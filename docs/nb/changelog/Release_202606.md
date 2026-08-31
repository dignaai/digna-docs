---
title: digna Release 2026.06 | Python SDK, Docker-distribusjon og forbedret valideringshåndtering
description: Lær hva som er nytt i digna Release 2026.06. Denne versjonen introduserer det nye digna Python SDK, Docker-distribusjonsstøtte, en omdesignet dashboard-opplevelse og utvidede import-/eksportmuligheter for valideringsregler.
keywords: digna Release 2026.06, digna Python SDK, digna Docker-støtte, automatisering av datakvalitet, dataprofiler, import/eksport av valideringsregler, digna dashboard, plattform for dataobservabilitet, Python API, metadata-automatisering
image: /assets/logo_square.png
---

# Endringslogg – Release 2026.06  

Med Release 2026.06 tar digna et stort steg fremover innen automatisering, utvidbarhet og plattformbrukervennlighet.  
Denne utgivelsen introduserer det nye **digna Python SDK**, offisiell **Docker-distribusjonsstøtte**, en oppfrisket dashboard-opplevelse og forbedret portabilitet for håndtering av valideringsregler.

---

## 🚀 Nye funksjoner  

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

## 🧪 Plattformforbedringer  

- Full Python SDK‑integrasjon for automatisering  
- Containerisert utrulling via Docker  
- Forbedret UX gjennom omdesignet dashboard  
- Utvidet portabilitet for valideringslogikk  

---

## 🎯 Hvem drar nytte av denne utgivelsen  

- Dataingeniører: automatisering, bruk av SDK, pipeline-integrasjon  
- Plattformteam: forenklet utrulling via Docker  
- Team for datastyring: gjenbrukbar håndtering av valideringsregler  
- Analyseteam: forbedret brukervennlighet og bedre synlighet av innsikt  

---

## 🛠 CLI‑oppdateringer  
- La til støtte for SDK‑integrasjon  
- Forbedrede import-/eksportarbeidsflyter  
- Generelle stabilitets‑ og ytelsesforbedringer
# Utgivelsesnotater – 2025.09  

Med Release 2025.09 introduserer digna en ny **modulær arkitektur** og lanserer **fem spesialiserte moduler** for datakvalitet og observability.  
Denne utgivelsen styrker også autentisering og forbedrer håndtering av varsler på tvers av plattformen.  

---

## Nye funksjoner  

### Modulær arkitektur  
- digna følger nå en **modulær arkitektur**.  
- Kunder kan aktivere kun de modulene de trenger og legge til flere etter hvert som kravene vokser.  
- Tidligere funksjonalitet er nå en del av **digna Data Anomalies**.  

### Nye moduler  
- **digna Data Anomalies** – AI-drevet deteksjon av anomalier i datavolumer, fordelinger og manglende verdier.  
- **digna Data Analytics** – Tidsserieanalyse av observability-metrikker for å oppdage langsiktige trender og volatilitet.  
- **digna Data Timeliness** – Overvåking av forventede ankomsttider for data, både AI-basert og regelbasert.  
- **digna Data Validation** – Regelbaserte kontroll på postnivå for å sikre samsvar med forretningsregler.  
- **digna Data Schema Tracker** – Oppdagelse av skjemaendringer (DDL-modifikasjoner) i overvåkede databaser.  

### MFA via OIDC  
- Støtte for **Multi-Factor Authentication (MFA)** med OIDC Single Sign-On.  
- Gir bedriftsnivå sikkerhet for alle brukerpålogginger.  

### Varsler per modul  
- Varsler sendes nå **per modul**, noe som gjør det enklere å skille varsler fra Data Anomalies, Data Analytics og andre moduler.  

---

## CLI-oppdateringer  

- **Ny kommando: `inspect-cancel`** – Avbryt inspeksjoner etter forespørsels-ID eller terminer alle aktive forespørsler.  
- **Ny kommando: `check-config`** – Valider konfigurasjonsfiler før oppstart.  
- **Ny kommando: `remove-orphans`** – Rydd opp i foreldreløse repository-oppføringer.  
- **Forbedret `inspect`-kommando** – Nytt alternativ `--bypass-backend` (`-bb`) og standardiserte returkoder (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Dokumentasjon  
- Nye guider:  
  - Integrasjonsguide for Single Sign-On
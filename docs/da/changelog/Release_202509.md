---
title: digna Release 2025.09 | Modulært design, fem nye moduler, MFA via OIDC
description: Læs om nyhederne i digna Release 2025.09. Denne version introducerer en modulær arkitektur, fem nye moduler, MFA via OIDC og notifikationer pr. modul.
keywords: digna Release 2025.09, digna ændringslog, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modulær arkitektur, digna OIDC MFA
image: /assets/logo_square.png
---

# Ændringslog – Udgivelse 2025.09  

Med Udgivelse 2025.09 introducerer digna en ny **modulær arkitektur** og lancerer **fem specialiserede moduler** til Data Quality og observability.  
Denne udgivelse styrker også autentifikationen og forbedrer håndteringen af notifikationer på tværs af platformen.  

---

## Nye funktioner  

### Modulært design  
- digna følger nu en **modulær arkitektur**.  
- Kunder kan aktivere kun de moduler, de har brug for, og tilføje flere efterhånden som behovet vokser.  
- Tidligere funktionalitet er nu en del af **digna Data Anomalies**.  

### Nye moduler  
- **digna Data Anomalies** – AI-drevet detektion af anomalier i datavolumener, fordelinger og manglende værdier.  
- **digna Data Analytics** – Tidsserievurdering af observability-metrikker for at opdage langsigtede tendenser og volatilitet.  
- **digna Data Timeliness** – Overvågning af forventede ankomsttider for data, både AI-baseret og regelbaseret.  
- **digna Data Validation** – Regelbaserede tjek på postniveau for at sikre overholdelse af forretningsregler.  
- **digna Data Schema Tracker** – Detektion af schemaændringer (DDL-ændringer) i overvågede databaser.  

### MFA via OIDC  
- Understøttelse af **Multi-Factor Authentication (MFA)** med OIDC Single Sign-On.  
- Giver virksomhedsniveau-sikkerhed for alle brugerlogins.  

### Notifikationer pr. modul via e-mail  
- Notifikationer sendes nu **pr. modul**, hvilket gør det nemmere at adskille alarmer fra Data Anomalies, Data Analytics og andre moduler.  

---

## CLI-opdateringer  

- **Ny kommando: `inspect-cancel`** – Annuller inspektioner efter request-ID eller afslut alle aktive forespørgsler.  
- **Ny kommando: `check-config`** – Valider konfigurationsfiler før opstart.  
- **Ny kommando: `remove-orphans`** – Ryd op i forældreløse repository-poster.  
- **Forbedret `inspect`-kommando** – Ny option `--bypass-backend` (`-bb`) og standardiserede returkoder (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Dokumentation  
- Nye guider:  
  - Guide til integration af Single Sign-On
---
title: digna Release 2025.09 | Architettura modulare, cinque nuovi moduli, MFA via OIDC
description: Scopri le novità della digna Release 2025.09. Questa versione introduce un'architettura modulare, cinque nuovi moduli, MFA via OIDC e notifiche per modulo.
keywords: digna Release 2025.09, changelog digna, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna architettura modulare, digna OIDC MFA
image: /assets/logo_square.png
---

# Registro modifiche – Release 2025.09  

Con la Release 2025.09, digna introduce una nuova **architettura modulare** e lancia **cinque moduli specializzati** per Data Quality e Observability.  
Questa release rafforza inoltre l'autenticazione e migliora la gestione delle notifiche su tutta la piattaforma.  

---

## Nuove funzionalità  

### Design modulare  
- digna ora adotta una **architettura modulare**.  
- I clienti possono abilitare solo i moduli necessari e aggiungerne altri man mano che le esigenze crescono.  
- Le funzionalità precedenti sono ora parte di **digna Data Anomalies**.  

### Nuovi moduli  
- **digna Data Anomalies** – Rilevamento basato su AI di anomalie nei volumi dei dati, nelle distribuzioni e nei valori mancanti.  
- **digna Data Analytics** – Valutazione in serie temporale delle metriche di osservabilità per individuare tendenze a lungo termine e volatilità.  
- **digna Data Timeliness** – Monitoraggio dei tempi di arrivo attesi dei dati, sia basato su AI che su regole.  
- **digna Data Validation** – Controlli a livello di record basati su regole per garantire la conformità alle regole di business.  
- **digna Data Schema Tracker** – Rilevamento delle modifiche di schema (modifiche DDL) nei database monitorati.  

### MFA via OIDC  
- Supporto per **Autenticazione a più fattori (MFA)** con Single Sign-On OIDC.  
- Fornisce sicurezza di livello enterprise per tutti gli accessi utente.  

### Email di notifica per modulo  
- Le notifiche vengono ora inviate **per modulo**, facilitando la separazione degli alert da Data Anomalies, Data Analytics e altri moduli.  

---

## Aggiornamenti CLI  

- **Nuovo comando: `inspect-cancel`** – Annulla le ispezioni tramite ID richiesta o termina tutte le richieste attive.  
- **Nuovo comando: `check-config`** – Valida i file di configurazione prima dell'avvio.  
- **Nuovo comando: `remove-orphans`** – Ripulisce le voci di repository orfane.  
- **Comando `inspect` migliorato** – Nuova opzione `--bypass-backend` (`-bb`) e codici di ritorno standardizzati (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Documentazione  
- Nuove guide:  
  - Guida all'integrazione Single Sign-On
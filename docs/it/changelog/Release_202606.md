---
title: digna Release 2026.06 | Python SDK, Deployment Docker e Gestione della Validazione Potenziata
description: Scopri le novità di digna Release 2026.06. Questa versione introduce il nuovo digna Python SDK, il supporto ufficiale per il deployment via Docker, un'esperienza di dashboard rinnovata e funzionalità avanzate di import/export per le regole di validazione.
keywords: digna Release 2026.06, digna Python SDK, digna Docker support, automazione qualità dati, data profiling, import export regole di validazione, digna dashboard, piattaforma di data observability, Python API, automazione metadata
image: /assets/logo_square.png
---

# Changelog – Release 2026.06  

Con la Release 2026.06, digna compie un importante passo avanti in termini di automazione, estendibilità e usabilità della piattaforma.  
Questa release introduce il nuovo **digna Python SDK**, il supporto ufficiale per il **deployment via Docker**, un'esperienza di dashboard rinnovata e una maggiore portabilità nella gestione delle regole di validazione.

---

## Nuove funzionalità  

### digna Python SDK – Automatizza tutto con Python  
- Installazione:
  ```bash
  pip install digna-sdk
  ```
- Gestisci e automatizza digna programmaticamente con Python  
- Crea e configura progetti tramite codice  
- Avvia ispezioni ed esecuzioni di monitoring  
- Gestisci dataset, regole e configurazioni in modo programmatico  
- Profila tabelle ed estrai insight di metadata  
- Esporta i risultati di profiling e data quality verso repository e sistemi esterni  
- Integra con notebook, strumenti di orchestrazione e pipeline CI/CD  

**Impatto:** Abilita infrastruttura-as-code completa e profonda automazione dei workflow di qualità e osservabilità dei dati usando Python.

---

### Supporto Docker – Deployment e operation semplificati  
- Immagine Docker ufficiale per digna  
- Setup rapido e coerente tra gli ambienti  
- Onboarding semplificato per sviluppo, test e produzione  
- Integrazione facilitata con Kubernetes e piattaforme container  
- Maggiore portabilità e riproducibilità dei deployment  

**Impatto:** Rende digna più semplice da distribuire e gestire nelle architetture cloud-native moderne.

---

### QueryMode – Strategia flessibile di esecuzione delle SQL

Configura la strategia di esecuzione delle query: modalità **Single** o **Combined**

**Single Mode**: Ogni statistica viene calcolata con una singola query SQL dedicata

  - Ideale per datasource di grandi dimensioni dove la memoria è critica  
  - Previene l'esaurimento delle risorse nelle query combinate (out of memory, limiti di spool)  
  - Maggior numero di query ma minore consumo di memoria per singola query

**Combined Mode**: Tutte le statistiche vengono calcolate all'interno di un'unica query SQL

  - Riduce il numero totale di query e l'overhead di rete  
  - Ottimizza le prestazioni quando i datasource sono gestibili in memoria  
  - Più efficiente per esecuzioni frequenti e parallele

**Impatto:** Offre agli utenti un controllo granulare sull'esecuzione delle query per bilanciare prestazioni, utilizzo delle risorse e sicurezza della memoria in base alle caratteristiche del datasource.

---

### Dashboard ridisegnata  
- UI/UX modernizzata e migliorata  
- Navigazione e struttura più chiare  
- Maggiore visibilità dei risultati di monitoring e degli insight sulla qualità dei dati  
- Migliore leggibilità di alert, statistiche e dashboard  
- Accesso più rapido alle informazioni operative chiave  

**Impatto:** Migliora l'usabilità e la produttività quotidiana di tutti gli utenti.

---

### Import & Export estesi per le regole di validazione  
- Funzionalità di import/export delle regole di validazione potenziata  
- Migrazione più semplice tra ambienti e progetti  
- Riutilizzo facilitato di set di regole standardizzati  
- Migliore governance e gestione del ciclo di vita delle regole  
- Collaborazione semplificata tra team  

**Impatto:** Permette una governance della qualità dei dati scalabile e coerente in tutta l'organizzazione.

---

## Miglioramenti della piattaforma  

- Integrazione completa del Python SDK per l'automazione  
- Deployment containerizzato tramite Docker  
- UX migliorata grazie alla dashboard ridisegnata  
- Maggior portabilità della logica di validazione  

---

## Beneficiari di questa release  

- Data Engineer: automazione, utilizzo del SDK, integrazione in pipeline  
- Team di piattaforma: deployment semplificato tramite Docker  
- Team di Data Governance: gestione riutilizzabile delle regole di validazione  
- Team di Analytics: migliore usabilità e visibilità degli insight  

---

## Aggiornamenti CLI  
- Aggiunto supporto all'integrazione con lo SDK  
- Migliorati i flussi di import/export  
- Miglioramenti generali di stabilità e prestazioni
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

## Guarda la presentazione della release

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — una panoramica di questa release sul canale YouTube di digna.*

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

### Modello di previsione configurabile

Il modello alla base del rilevamento delle anomalie ora mette a confronto spiegazioni alternative di ciascuna serie – un pattern combinato con una lettura delle osservazioni più recenti – e fonde le loro previsioni in base a quanto ciascuna è supportata. Un singolo valore estremo non può più propagarsi nelle previsioni successive.

Due impostazioni nella nuova scheda **Model** del datasource lo governano, ciascuna da `0.0` a `1.0` con `0.5` come valore predefinito:

- **Break Sensitivity** – quanto rapidamente un salto a un nuovo livello o un'inversione di trend viene considerato reale anziché trattato come outlier
- **Model Complexity** – quanta struttura cerca il modello, dagli effetti di calendario e da un singolo cambio di livello fino a cicli sconosciuti, effetti legati al giorno del mese e reset mensili

Entrambe possono essere ripristinate ai valori predefiniti in qualsiasi momento. Consultate [Impostazioni del modello](../platform/data_anomalies/how_it_works.md#model-settings) per sapere come agisce ciascuna.

**Impatto:** Dà agli utenti il controllo sul modello di previsione stesso, accanto alle impostazioni Sensitivity e Memory già presenti sulla banda di tolleranza, ora nella scheda **Thresholds**.

---

### Controllo delle notifiche sulle anomalie

- Nuova scheda **Notifications** nelle impostazioni delle anomalie del datasource:
  - **Minimum Alerts** – quanti controlli falliti (non quelli incerti) servono a un'ispezione prima che venga inviata una notifica (predefinito `1`)
  - **Pause After Notification (Days)** – per quanto tempo una sottoscrizione resta silenziosa dopo aver inviato una notifica sul datasource (predefinito `0`, nessuna pausa)
- Gli iscritti ora ricevono una notifica quando un'ispezione fallisce del tutto (**Notify Inspection Errors**)
- Ogni notifica rimanda direttamente alla pagina a cui si riferisce – i controlli falliti dell'ispezione, oppure le viste Schema Tracker e Timeliness
- Interruttori di sottoscrizione più chiari: **Notify on Passed Inspections**, **Notify Inspection Errors**, **Notify Data Volume Checks**

**Come funzionano le notifiche:** le notifiche vengono inviate tramite **canali di notifica** – Email (tramite una connessione SMTP), Slack o Jira – che gli amministratori configurano e possono verificare con **Test Notification Channel**. Una **sottoscrizione** collega un canale a un progetto: copre tutti i datasource o solo quelli selezionati, e i suoi interruttori stabiliscono cosa segnala – ciascun modulo (Data Anomalies, Data Validation, Data Analytics, Timeliness, Schema Tracker e controlli del volume dei dati), le ispezioni che falliscono del tutto e, facoltativamente, anche le ispezioni superate.

**Impatto:** Notifiche meno numerose e più utili – le deviazioni isolate e le anomalie persistenti non inondano più il canale.

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
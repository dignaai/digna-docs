---
title: Data Schema Tracker – Monitora l'evoluzione dello schema | Documentazione digna
description: Scopri come digna Data Schema Tracker monitora modifiche alle colonne, aggiornamenti dei tipi di dato e schema drift. Rileva e segnala cambiamenti di schema intenzionali o non intenzionali per prevenire errori ETL, dashboard rotte e perdita di osservabilità dei dati.
canonical_url: https://docs.digna.ai/platform/data_schema_tracker/
image: /assets/logo_square.png
keywords:
  - monitoraggio evoluzione schema
  - rilevamento schema drift
  - monitoraggio evoluzione dello schema
  - osservabilità dei metadati
  - osservabilità dei dati
  - qualità dei dati
  - monitoraggio della struttura dei dati
  - metadati del database
  - stabilità delle pipeline ETL
  - digna Data Schema Tracker
lang: it
robots: index, follow
og_title: Data Schema Tracker – Monitora l'evoluzione dello schema | Documentazione digna
og_description: digna Data Schema Tracker monitora schema drift, modifiche ai tipi di dato e aggiornamenti delle colonne. Ricevi avvisi prima che pipeline ETL o dashboard falliscano a causa di cambiamenti strutturali inattesi.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Monitor Schema Evolution
<h1 style="display:none;">Modulo guidato dall'IA per l'osservabilità dei metadati e la qualità dei dati – digna Data Schema Tracker</h1>

---

## Scopo

Il **Data Schema Tracker** ti tiene informato su come evolvono le strutture del tuo database.  
Monitora continuamente **schemi di tabelle, colonne e tipi di dato** per rilevare il **schema drift** — cambiamenti strutturali intenzionali o non intenzionali che possono interrompere pipeline, job ETL o dashboard BI.

Garantendo trasparenza nell'evoluzione degli schemi, digna aiuta le organizzazioni a mantenere la **fiducia nella qualità dei dati**, preservare l'**osservabilità dei sistemi dati** e evitare costosi incidenti di produzione causati da cambiamenti di schema non rilevati.

---

## Panoramica tecnica

### Cosa monitora

- **Colonne aggiunte o rimosse** – Rileva colonne introdotte di recente, rinominate o eliminate.  
- **Modifiche ai tipi di dato** – Identifica cambiamenti come `INT → VARCHAR` o `DATE → TIMESTAMP`.  
- **Modifiche a tabelle e viste** – Monitora la creazione, il rinominamento o la rimozione di tabelle e viste.  
- **Differenze tra ambienti** – Confronta le versioni dello schema tra ambienti Dev, Test e Production.  

### Rilevamento e avvisi

- Esegue scansioni dei **metadati del database** o dei **cataloghi di sistema** direttamente sulla tua piattaforma dati.  
- Confronta ogni snapshot dello schema con la versione precedente memorizzata nello schema di osservabilità di digna.  
- Genera **avvisi in tempo reale** nella dashboard, via API o su canali di notifica esterni (email, Slack, webhook).  
- Registra ogni versione dello schema per la **tracciabilità storica e la prontezza all'audit**.

---

## Architettura e esecuzione

- **Esecuzione in-database:** digna opera interamente all'interno del tuo ambiente, interrogando viste di metadati senza estrarre alcun dato.  
- **Scansione leggera:** accede solo alle informazioni strutturali — mai ai dati degli utenti.  
- **Archiviazione centralizzata:** i metadati dello schema e i record di drift sono memorizzati nello schema di osservabilità di digna per visualizzazione e analisi.  
- **Automazione:** supporta scansioni pianificate o basate su eventi tramite digna Core o strumenti di orchestrazione esterni.  

---

## Esempi di casi d'uso

| Use Case | Description |
|-----------|--------------|
| **ETL Stability Monitoring** | Rilevare cambiamenti della struttura a monte prima che le pipeline falliscano a causa di discrepanze di schema. |
| **Business Intelligence Reliability** | Impedire dashboard rotte causate da colonne rinominate o mancanti. |
| **Data Warehouse Governance** | Mantenere una storia auditabile dell'evoluzione dello schema per conformità e analisi d'impatto. |
| **Integration Oversight** | Assicurare che gli schemi di data lake e data warehouse rimangano sincronizzati dopo aggiornamenti strutturali. |

---

## Benefici

| Area | Benefit |
|------|----------|
| **Data Quality** | Previene lo schema drift non rilevato che può corrompere o invalidare le pipeline di dati. |
| **Observability** | Aggiunge il monitoraggio strutturale all'osservabilità complessiva degli ecosistemi dati. |
| **Compliance** | Mantiene una cronologia versionata degli schemi per audit, tracciabilità e controllo delle modifiche. |
| **Prevention** | Rileva problemi strutturali prima che si propaghino in errori di reporting o produzione. |

---

## Come funziona

1. **Raccolta snapshot** – digna cattura i metadati correnti dello schema.  
2. **Confronto** – il nuovo snapshot viene confrontato
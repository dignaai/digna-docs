---
title: Data Validation – Controlli basati su regole per conformità & auditabilità | digna Documentazione
description: Scopri come digna Data Validation applica controlli deterministici basati su regole con soglie, intervalli e liste di riferimento. Garantisci conformità, auditabilità e reporting regolamentare nei settori finanziario, sanitario e in altri ambiti sensibili ai dati.
image: /assets/logo_square.png
keywords:
  - convalida dei dati
  - controlli basati su regole
  - qualità dei dati
  - osservabilità dei dati
  - soglie e intervalli
  - validazione tramite liste di riferimento
  - auditabilità
  - monitoraggio della conformità
  - digna data validation
lang: it
robots: index, follow
og_title: Data Validation – Controlli basati su regole per conformità & auditabilità | digna Documentazione
og_description: digna Data Validation applica controlli deterministici basati su regole con soglie, intervalli e liste di riferimento. Progettato per settori regolamentati, garantisce conformità, trasparenza e auditabilità.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Controlli basati su regole
<h1 style="display:none;">Modulo Data Validation guidato dall'IA per la qualità dei dati e l'osservabilità – digna</h1>

---

## Scopo

Il modulo **Data Validation** garantisce la **qualità dei dati** tramite controlli precisi basati su regole.  
Consente alle organizzazioni di definire logiche di validazione deterministiche, sia di business che tecniche, assicurando che i dati rispettino standard di conformità, SLA contrattuali e requisiti normativi.

Combinando *esecuzione delle regole in-database*, *tracce di audit complete* e *integrazione con altri moduli digna*, **Data Validation** garantisce una **Qualità dei Dati e osservabilità** coerente e tracciabile in ambienti aziendali complessi.

---

## Panoramica tecnica

### Tipi di validazione supportati

- **Verifiche di uguaglianza**  
  Confermare che i valori corrispondano ai risultati attesi (es. codici di riferimento, flag booleani, mappature categoriali).

- **Soglie e intervalli**  
  Validare misure numeriche o KPI rispetto a limiti definiti — statici o derivati dinamicamente.

- **Liste di riferimento e lookup**  
  Verificare se i valori dei campi esistono all'interno di set di master data approvati (es. codici IVA, liste ISO dei paesi, cataloghi prodotti).

- **Coerenza tra colonne**  
  Assicurare correttezza relazionale (es. la valuta corrisponde alla regione, la categoria di rischio è coerente con il tipo di asset).

- **Regole di gestione dei valori null**  
  Rilevare valori null o vuoti non attesi in colonne critiche.

### Esecuzione e logging

- **Elaborazione in-database** – Tutte le regole di validazione vengono eseguite direttamente nel tuo database (Teradata, Snowflake, Databricks, PostgreSQL, ecc.).  
- **Nessuna estrazione dei dati** – digna non trasferisce mai i dati grezzi fuori dal tuo ambiente.  
- **Tracciabilità completa** – Ogni risultato di regola viene registrato con timestamp, dataset responsabile, conteggi di record e esiti di pass/fail.  
- **Audit**
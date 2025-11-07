---
title: Data Anomalies – Rilevamento automatico delle irregolarità nei dati | documentazione digna
description: Scopri come digna Data Anomalies rileva automaticamente cali di volume, valori mancanti, cambiamenti di distribuzione e pattern inattesi senza scrivere regole manuali. Migliora la qualità e l'osservabilità dei flussi di dati con il rilevamento anomalie guidato dall'IA.
image: /assets/logo_square.png
keywords:
  - anomalie dei dati
  - rilevamento anomalie AI
  - monitoraggio qualità dati
  - qualità dei dati
  - osservabilità dei dati
  - rilevamento dati mancanti
  - monitoraggio volume dati
  - deriva di distribuzione
  - affidabilità dei dati
  - digna Data Anomalies
lang: it
robots: index, follow
og_title: Data Anomalies – Rilevamento automatico | documentazione digna
og_description: digna Data Anomalies individua automaticamente irregolarità nel volume, nei valori e nelle distribuzioni dei dati senza regole manuali — migliorando qualità e osservabilità su più piattaforme.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Anomalies – Automated Detection
<h1 style="display:none;">Modulo guidato da IA per la qualità e l'osservabilità dei dati – digna Data Anomalies</h1>

---

## Scopo

Il modulo **Data Anomalies** identifica automaticamente le irregolarità nei tuoi dataset — senza bisogno di scrivere regole.  
Monitora in modo continuo **la qualità della consegna dei dati**, imparando cosa è “normale” e rilevando deviazioni in tempo reale.

Grazie al rilevamento basato su IA, digna riconosce errori silenziosi nei dati come record mancanti, duplicati o corrotti che possono distorcere report, modelli ML e dashboard.

---

## Panoramica tecnica

### Metriche analizzate

digna profila continuamente i seguenti aspetti dei tuoi dati:

- **Volume dei record** – numero totale di righe, quotidiano o per batch  
- **Valori mancanti** – individuazione di campi null o vuoti  
- **Distribuzioni e istogrammi** – monitoraggio delle variazioni nella forma dei dati  
- **Intervalli di valori** – identificazione automatica di valori fuori intervallo o estremi  
- **Unicità** – controlli per chiavi duplicate o voci ripetute  

### Rilevamento intelligente delle anomalie

- Utilizza **apprendimento storico** per definire dinamicamente i confini attesi  
- Rileva deviazioni in **volume, distribuzioni dei valori o relazioni logiche**  
- Impiega l'IA per adattare automaticamente le soglie in base all'ora del giorno o a pattern stagionali  
- Distingue tra **fluttuazioni statistiche** e vere anomalie  
- Produce metriche dettagliate e punteggi di confidenza per dataset e colonne  

---

## Scenari di rilevamento

Di seguito esempi di problemi reali catturati automaticamente dal modulo **Data Anomalies**:

| Scenario | Descrizione |
|-----------|--------------|
| **Calibro o picchi di volume** | Mancano metà delle transazioni giornaliere, caricamenti batch duplicati o improvvisi picchi di dati |
| **Valori mancanti o null** | Estrazioni dati completate ma colonne critiche vuote |
| **Derive di distribuzione** | La spesa media o il numero di transazioni per regione cambia inaspettatamente |
| **Scambio di colonne** | Colonne come *first_name* e *last_name* scambiate accidentalmente durante l'ETL |
| **Valori categorici inattesi** | ad es., “Zurigo” appare nella lista delle città austriache |
| **Perdita improvvisa di unicità** | ID precedentemente unici iniziano a duplicarsi a causa di errori di join a monte |

---

## Architettura ed esecuzione

- **Esecuzione in-database:** Tutta la logica di rilevamento delle anomalie viene eseguita *all'interno del motore di database* (Teradata, Snowflake, Databricks, PostgreSQL, ecc.)  
- **Nessun trasferimento di dati:** digna legge solo metriche, non trasferisce mai i dati grezzi all'esterno  
- **Aggiornamenti incrementali:** Analizza ad ogni esecuzione solo i segmenti di dati nuovi per efficienza  
- **Frequenza di ispezione configurabile:** Oraria, giornaliera o attivata dai processi a monte  
- **Archiviazione dei risultati:** Metriche e flag di anomalia vengono scritti nello schema di observability di digna per visualizzazione e alerting  

---

## Benefici

| Area | Beneficio |
|------|----------|
| **Automazione** | Elimina centinaia di definizioni SQL o regole manuali |
| **Precisione** | Rileva problemi che le soglie statiche spesso non individuano |
| **Scalabilità** | Monitora in modo efficiente milioni di record per tabella |
| **Integrazione** | Funziona perfettamente con *digna Data Analytics* per l'analisi delle tendenze |
| **Conformità** | Garantisce controllo continuo sulla **qualità e osservabilità dei dati** |
| **Trasparenza** | Fornisce punteggi di confidenza, timestamp e codici motivo per ogni anomalia |

---

## Come digna impara il “normale”

1. **Fase di profilazione:** digna raccoglie metriche dai dataset storici.  
2. **Fase di apprendimento:** i modelli di IA identificano pattern ricorrenti (stagionali, settimanali, giornalieri).  
3. **Fase di monitoraggio:** i dataset futuri vengono confrontati con soglie apprese dinamicamente.  
4. **Fase di alerting:** le deviazioni oltre i confini di confidenza statistica vengono segnalate come anomalie.  

Tutti i modelli sono spiegabili, deterministici e ottimizzati per volumi di dati enterprise.

---

## Esempi d'uso

- Monitoraggio della qualità dei dati nei **sistemi di transazioni bancarie**  
- Rilevamento di errori di caricamento in job **ETL o di data warehouse**  
- Identificazione di attività cliente anomale nei **record di telecomunicazioni**  
- Osservazione della coerenza dei dati clinici nelle **pipeline di analytics per la sanità**  
- Prevenzione di dashboard rotte in **ambienti BI e di reporting**

---

## Domande frequenti

**Data Anomalies richiede regole predefinite?**  
No — il modulo apprende automaticamente dal comportamento dei dati.

**Posso comunque definire soglie specifiche se necessario?**  
Sì. digna permette di combinare rilevamento basato su IA e basato su regole (tramite *Data Validation*).

**Come si riducono i falsi positivi?**  
Il modulo utilizza apprendimento adattivo e punteggi di confidenza statistica per ignorare le normali variazioni stagionali.

**Dove avviene l'elaborazione?**  
Tutte le elaborazioni avvengono all'interno del tuo database — digna non estrae mai i dati grezzi.

**È adatto a dati sensibili o regolamentati?**  
Sì. digna funziona completamente on-premises o in cloud privato e aderisce agli standard di conformità europei.
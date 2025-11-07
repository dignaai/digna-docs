---
title: Data Timeliness – Monitoraggio della Consegna Puntuale | Documentazione digna
description: Scopri come digna Data Timeliness assicura che i dati arrivino quando previsto. Rileva consegne in ritardo o mancanti, monitora gli SLA e proteggi i processi aziendali da ritardi silenziosi. Rilevamento potenziato da AI per migliorare la qualità dei dati e l'osservabilità delle pipeline.
canonical_url: https://docs.digna.ai/platform/data_timeliness/
image: /assets/logo_square.png
keywords:
  - Data Timeliness
  - monitoraggio delle consegne
  - qualità dei dati
  - qualità dei dati
  - osservabilità dei dati
  - rilevamento dati in ritardo
  - segnalazione dati mancanti
  - monitoraggio SLA
  - analisi delle consegne con AI
  - digna Data Timeliness
lang: it
robots: index, follow
og_title: Data Timeliness – Monitoraggio della Consegna Puntuale | Documentazione digna
og_description: digna Data Timeliness rileva automaticamente consegne di dati in ritardo o mancanti usando l'AI. Proteggi i processi aziendali, monitora gli SLA e assicurati dati tempestivi e affidabili in tutte le pipeline.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – Monitoraggio della Consegna Puntuale
<h1 style="display:none;">Modulo Data Timeliness guidato da AI per Qualità dei Dati e Osservabilità – digna</h1>

---

## Scopo

Il **Data Timeliness** module assicura che i **dati siano puntuali** - ogni volta.  
Monitora continuamente i programmi di consegna e rileva automaticamente quando dataset, tabelle o file sono **in ritardo, mancanti o incompleti**.  

Combinando l'apprendimento AI con schedule definite dall'utente, *digna* consente alle organizzazioni di prevenire errori a valle e rispettare rigorosi obiettivi di **SLA (Service Level Agreement)** per la **qualità dei dati** e per **l'osservabilità delle pipeline dati**.

---

## Panoramica tecnica

### Due modalità di monitoraggio
- **Pattern di arrivo appresi dall'AI**  
  digna apprende automaticamente il ritmo naturale delle tue consegne di dati — giornaliero, orario o guidato da eventi — analizzando timestamp storici e tempi di completamento.  
  Si adatta ai cambi di calendario aziendale, ai weekend o ai picchi di fine mese.

- **Schedule definite dall'utente**  
  Gli utenti possono definire esplicitamente i tempi di consegna previsti (es. *ogni giorno feriale prima delle 7:30*).  
  digna confronta l'orario effettivo di arrivo con lo schedule pianificato e genera avvisi quando i dati sono in ritardo o mancanti.

### Meccanismo di rilevamento
- Valuta **timestamp nei metadata**, **conteggi di record** e **freschezza delle tabelle**  
- Rileva **job ETL bloccati**, **estrazioni fallite** e **arrivi parziali di file**  
- Si integra con *Data Anomalies* e *Data Validation* per insight combinati

---

## Scenari di rilevamento

| Scenario | Descrizione |
|-----------|--------------|
| **Arrivo dati in ritardo** | Feed giornaliero dei dati di mercato ritardato di due ore, causando il mancato rispetto degli SLA nei report |
| **Caricamento mancante** | Una tabella o una partizione programmata non aggiornata per la data corrente |
| **Ritardo per dipendenza a catena** | Il ritardo di un job upstream impatta il refresh della pipeline downstream |
| **Variazione del pattern nel weekend** | Il modello AI si adatta automaticamente quando non ci si aspetta dati di domenica |

---

## Architettura ed esecuzione

- **Esecuzione in-database:** digna esegue i controlli di timeliness direttamente all'interno del tuo database o data warehouse.  
- **Accesso leggero ai metadata:** legge timestamp dei job, conteggi dei record e informazioni sulle partizioni — nessuna estrazione dati richiesta.  
- **Frequenza configurabile:** schedula il monitoraggio per dataset, schema o pipeline.  
- **Avvisi tra moduli:** i risultati possono attivare avvisi visivi in *Inspection Hub* o notifiche via email, Slack o API.  

---

## Esempi di utilizzo

- **Feed dei mercati finanziari:** rilevare ritardi negli aggiornamenti di prezzi o dati di trading.  
- **Caricamenti nel Data Warehouse:** monitorare quando i job ETL notturni terminano oltre il previsto.  
- **Condivisione dati tra team:** garantire che le consegne dipartimentali avvengano prima dei cutoff giornalieri.  
- **Reportistica regolamentare:** confermare che le sottomissioni includano l'istantanea dati più recente disponibile.  

---

## Benefici

| Area | Beneficio |
|------|----------|
| **Continuità operativa** | Previene interruzioni operative dovute a dati in ritardo o mancanti |
| **Qualità dei dati** | Migliora l'affidabilità e la coerenza delle pipeline dati |
| **Conformità** | Garantisce il rispetto degli SLA e la trasparenza per gli audit |
| **Automazione** | L'AI elimina il monitoraggio manuale degli schedule |
| **Integrazione** | Funziona senza soluzione di continuità con *Data Analytics* per visualizzare le tendenze di timeliness nel tempo |

---

## Come digna apprende i tempi di consegna previsti

1. **Analisi storica:** digna osserva i precedenti orari di caricamento e le durate.  
2. **Modellazione AI:** il machine learning crea una baseline dinamica per l'arrivo previsto.  
3. **Monitoraggio:** ogni nuova consegna viene confrontata con la baseline.  
4. **Allertamento:** le deviazioni generano avvisi con metriche contestuali e punteggi di confidenza.  

Questo approccio di apprendimento continuo si adatta ai processi in evoluzione mantenendo basso il numero di falsi positivi.

---

## Domande frequenti

**Posso definire i miei tempi di consegna?**  
Sì. digna supporta sia schedule fissi definiti dall'utente sia pattern appresi dall'AI.

**Si integra con il mio tool ETL o di orchestrazione?**  
Sì. digna si integra con strumenti come Airflow, dbt, Informatica o scheduler personalizzati.

**Dove avviene il calcolo?**  
Tutte le analisi vengono eseguite nel tuo database o cloud warehouse — non viene utilizzato alcun servizio esterno.

**Cosa succede quando i dati sono in ritardo?**  
digna genera avvisi nella dashboard, nell'Inspection Hub e tramite API/webhook per notificare immediatamente i team operativi.

---


**digna Data Timeliness** aiuta a garantire la **fiducia nei dati**, combinando **rilevamento guidato da AI**, **esecuzione on-premises**, e **osservabilità dei dati** — tutto all'interno del tuo ambiente controllato.
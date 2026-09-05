# Registro delle modifiche – Release 2026.04  

Con la Release 2026.04, digna potenzia significativamente le sue capacità in ambito analytics e validazione dei dati.  
Questa versione introduce analisi avanzate delle serie temporali, componenti di validazione riutilizzabili e la centralizzazione della standardizzazione dei valori.

---

## Novità  

### Analytics Chart – Analisi delle serie temporali senza competenze di Data Science  
- Nuovo **Analytics Chart** per l’analisi interattiva delle serie temporali  
- Metodi analitici inclusi:
    - Regressione lineare, quadratica e cubica  
    - Regressione a tratti con breakpoints configurabili  
    - Tecniche di smoothing  
    - Analisi dei quantili  
- Identificazione automatica di trend, stagionalità e cambi di pattern  
- Analisi dei residui per approfondire le deviazioni  
- Le serie temporali vengono calcolate automaticamente per ogni dataset  

**Impatto:** Permette agli utenti di comprendere comportamenti complessi dei dati nel tempo senza richiedere competenze di data science o strumenti esterni.

---

### Enumerations – Definizione centrale dei valori ammessi  
- Definisci set riutilizzabili di valori ammessi (es. paesi, stati, codici di stato)  
- Valida i valori delle colonne rispetto alle enumerazioni predefinite in **digna Data Validation**  
- Riutilizza le enumerazioni tra progetti e fonti dati  
- Usa le enumerazioni ovunque tramite `#ENUM:MY_ENUM#`  
- Tutti i controlli vengono eseguiti **direttamente nel database di origine**  

**Impatto:** Garantisce valori coerenti e standardizzati nei dati a livello organizzativo.

---

### Validation Rule Templates – Logica riutilizzabile per la qualità dei dati  
- Definisci regole di validazione riutilizzabili (es. controlli di spazi bianchi, NOT NULL, controlli di formato)  
- Applica i template a più dataset  
- Assicura logiche di regola coerenti tra i progetti  
- Riduce duplicazioni e configurazioni manuali  
- Tutti i controlli vengono eseguiti **direttamente nel database di origine**  

**Impatto:** Abilita validazioni dei dati scalabili e ad alte prestazioni senza spostamento dei dati.

---

### Condizioni di rilevanza a livello di statistica per colonna  
- Definisci condizioni di rilevanza a livello di **colonna per ciascuna statistica**  
- Estende il concetto di condizioni di rilevanza per anomalie  
- Controlla quando una statistica deve essere considerata rilevante  
- Riduce il rumore escludendo situazioni non critiche  

**Impatto:** Migliora la qualità del segnale concentrandosi solo sulle deviazioni significative.

---

## Capacità estese di Data Analytics e Validazione  

Con questa release, digna amplia sia la comprensione dei dati sia la standardizzazione della validazione:

- Interpretazione avanzata delle **serie temporali** senza conoscenze di data science  
- Definizione centralizzata dei **valori ammessi tramite enumerazioni**  
- Logica di validazione riutilizzabile tramite template  
- Controllo granulare sulla **rilevanza di statistiche e alert**  

Insieme, queste capacità consentono alle organizzazioni non solo di rilevare problemi, ma anche di **comprendere, standardizzare e controllare la qualità dei dati**.

---

## A chi è utile questa release  

- **Data Engineers:** Logica di validazione riutilizzabile e maggiore controllo sul comportamento del monitoring  
- **Team di Data Quality & Governance:** Regole standardizzate e validazione coerente dei dati tra i sistemi  
- **Team Analytics & BI:** Migliore comprensione di trend e deviazioni  
- **Platform Owners:** Adozione aumentata grazie ad analytics semplificati e validazione scalabile  

---

## Aggiornamenti CLI  
- Nessuna modifica  

---
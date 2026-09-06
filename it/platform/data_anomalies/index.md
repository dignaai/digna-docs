# digna Data Anomalies – Rilevamento basato su AI di problemi di qualità dei dati

**Osservabilità guidata dall'AI per una fiducia nei dati sempre attiva**

digna Data Anomalies fa parte della **digna Data Observability Platform** — una soluzione modulare che migliora la **qualità dei dati** analizzando continuamente il comportamento dei dataset nel tempo.

Impara automaticamente cosa significa “normale” per i tuoi dati e ti avvisa quando il comportamento cambia — senza definire soglie statiche o scrivere una singola regola.  
Il modulo esegue direttamente all'interno del tuo database, quindi i dati non lasciano mai il tuo ambiente.

---

## Scopo di digna Data Anomalies

Il modulo **digna Data Anomalies** fornisce un'osservabilità continua dei dati calcolando e tracciando metriche statistiche predefinite come:

- Volume dei dati e conteggi dei record  
- Rapporti di valori mancanti  
- Distribuzioni dei valori e istogrammi  
- Intervalli numerici e medie  
- Unicità delle colonne e lunghezza dei testi  

Queste metriche vengono raccolte automaticamente per ogni dataset.  
Usandole, digna costruisce modelli che rappresentano il comportamento tipico di ciascuna metrica — apprendendo pattern giornalieri, settimanali o stagionali.  
Una volta addestrato, il modulo predice i valori attesi per i nuovi dati e rileva deviazioni che possono indicare problemi di qualità, errori di processo o cambiamenti a monte.

---

## Capacità principali

- Apprende automaticamente il comportamento atteso dei dati usando l'AI — nessuna configurazione di soglie.  
- Rileva cali improvvisi, picchi o drift nei volumi e nelle distribuzioni dei dati.  
- Identifica colonne scambiate o mappature errate tra attributi.  
- Evidenzia valori categorici inattesi (es. nuove regioni o codici).  
- Supporta tutti i tipi di colonna: numeriche, categoriche o non specificate.  
- Opera interamente nell'ambiente del cliente — nessun trasferimento di dati.  
- Si integra con **digna Data Analytics** per l'analisi delle tendenze a lungo termine.

---

## Come funziona

### Fase 1 – Calcolo delle metriche
digna calcola un insieme di metriche di profilo per ogni tabella e colonna.  
Queste metriche descrivono la struttura e il comportamento statistico dei tuoi dati e vengono memorizzate per analisi successive.

### Fase 2 – Addestramento del modello
Sulla base dei valori storici delle metriche, digna addestra modelli compatti di machine learning (signature models) che catturano l'intervallo normale di ciascuna metrica.

### Fase 3 – Soglie automatiche
Usando *conformal inference*, digna calcola intervalli di confidenza adattivi (soglie automatiche) che si evolvono con i tuoi dati.  
Se nuovi valori di metrica cadono al di fuori dell'intervallo previsto, vengono segnalati come anomalie.

Questo ciclo di feedback continuo assicura che il monitoraggio rimanga rilevante anche quando i volumi o i pattern dei dati crescono naturalmente.

---

## Esempi di scenari

### Calo imprevisto del volume di record
Un dataset contiene tipicamente circa 500.000 record al giorno.  
Quando una nuova consegna include solo 50.000 record, digna segnala un'anomalia e mostra quanto il valore si discosta dal range appreso.

### Rilevate colonne scambiate
La lunghezza media della stringa di `last_name` improvvisamente corrisponde a quella di `first_name`.  
digna riconosce la deviazione nei pattern delle metriche e segnala un possibile scambio di colonne.

### Categoria imprevista rilevata
Una colonna con le città austriache contiene improvvisamente “Zurich”.  
Basandosi sulle distribuzioni storiche, digna marca il nuovo valore come inatteso e avvisa l'utente.

---

## Integrazione con altri moduli

- **digna Data Analytics** — aggrega la cronologia delle anomalie e le metriche di volatilità per rivelare tendenze a lungo termine.  
- **digna Data Validation** — applica regole aziendali esplicite per controlli di qualità deterministici.  
- **digna Data Timeliness** — monitora i tempi di arrivo dei dati e correla i ritardi con il verificarsi di anomalie.  
- **digna Data Schema Tracker** — rileva cambiamenti strutturali che possono spiegare nuove anomalie.

---

## Casi d'uso tipici

- Rilevamento di caricamenti di dati mancanti o duplicati.  
- Identificazione di colonne scambiate o troncate.  
- Rilevamento di drift nelle distribuzioni di feature numeriche o categoriche.  
- Individuazione di valori di riferimento o codici inattesi.  
- Monitoraggio di pipeline di ingestione continua per irregolarità.  
- Monitoraggio complessivo della **qualità dei dati** e dell'**osservabilità dei dati** tra i domini.

---

## Benefici

- Rilevamento immediato di comportamenti anomali nei dati.  
- Elimina la taratura manuale delle soglie.  
- Riduce lo sforzo operativo in ambienti dati di grandi dimensioni.  
- Aumenta la fiducia nei sistemi di analisi e reporting.  
- Rafforza la **qualità dei dati** e l'**osservabilità dei dati** end-to-end.

---

## Related digna Modules

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — metriche di tendenza e volatilità.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — verifica dei dati basata su regole.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — monitoraggio delle tempistiche di consegna dei dati.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — rilevamento delle modifiche dello schema.

---

## Riepilogo

Il modulo **digna Data Anomalies** costituisce il cuore della **digna Data Observability Platform** guidata dall'AI.  
Monitorando continuamente metriche chiave, apprendendo pattern e identificando deviazioni, aiuta le organizzazioni a garantire che la **qualità dei dati** rimanga affidabile, stabile e spiegabile — senza configurazioni manuali.
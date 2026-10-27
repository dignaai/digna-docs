# Changelog – Release 2026.11  

La Release 2026.11 ruota attorno a tre importanti novità:

- **digna Data Reconciliation**: verifica che i dati restino coerenti mentre si spostano tra i sistemi  
- **digna Agentic**: apre digna agli agenti AI tramite il digna MCP Server  
- **digna Engine**: esegue facoltativamente il profiling dei dati all'interno di digna e abilita i controlli di integrità referenziale tra diverse tecnologie di database  

digna Data Reconciliation e digna Agentic sono rilasciati in versione beta.

---

## Nuove funzionalità  

### digna Data Reconciliation – Coerenza dalla sorgente alla destinazione  
I dati attraversano spesso diversi sistemi prima di arrivare in un report. digna Data Reconciliation confronta un datasource di **destinazione** con le **sorgenti** da cui è stato costruito, e genera un alert quando non corrispondono più.

- Configurata come regole con nome nella nuova scheda **Data Reconciliation** del datasource di destinazione  
- Qualsiasi datasource del progetto con Data Reconciliation attivato può fungere da sorgente  
- I casi d'uso includono le procedure di riconciliazione standard e la validazione dei risultati dei processi ETL  
- Due tipi di regole: **Exact** e **AI**  

**Regole Exact – La riconciliazione come regola di data quality**: definisci esattamente cosa deve corrispondere tra una sorgente e una destinazione, come in una regola di data quality.

  - Confronta un datasource sorgente con un datasource di destinazione  
  - Abbina un controllo di destinazione a un controllo sorgente per statistica e attributo, ad es. il conteggio delle righe o la somma di una colonna di importi  
  - Consenti una differenza con una tolleranza **Absolute** (ad es. ± 10) o **Relative** (ad es. ± 0,5% della sorgente)  
  - La timeline mostra la differenza di ogni giorno rispetto alla tolleranza  

**Regole AI – La riconciliazione come data observability**: digna apprende come una destinazione segue le proprie sorgenti, nello stesso modo in cui digna osserva i dati negli altri moduli, e genera un alert quando la relazione si interrompe.

  - Combina i controlli di più datasource sorgente con i controlli di una destinazione  
  - Non serve conoscere né formalizzare la logica che li collega (join, filtri, aggregazioni)  
  - Un modello apprende dallo storico come la destinazione segue le proprie sorgenti nello stesso giorno  
  - Ogni controllo di destinazione viene previsto a partire dai valori sorgente del giorno, e digna genera un alert quando la destinazione esce dalla banda degli errori passati della regola stessa  
  - Ogni regola ha i propri **Model settings**: **Sensitivity**, **Memory** e **Model Complexity**  

I controlli di riconciliazione compaiono nella Dashboard con una timeline per regola. Contribuiscono allo stato complessivo dell'ispezione e attivano le notifiche.

**Impatto:** Copre entrambi i lati della riconciliazione. Le regole Exact applicano controlli noti tra sorgente e destinazione, e le regole AI monitorano flussi complessi come i processi ETL, così i dati persi o modificati lungo il percorso vengono intercettati senza SQL di riconciliazione scritto a mano.

---

### digna Agentic – digna per gli agenti AI  
La prima versione di digna Agentic. Gli agenti AI ora possono lavorare con digna, rispondere a domande di business sui tuoi dati e aiutarti a migliorare la configurazione.

**digna MCP Server**: consente a Claude e ad altri agenti AI di lavorare con digna tramite il Model Context Protocol.

  - Gestisci progetti, datasource, regole, pianificazioni delle ispezioni e sottoscrizioni  
  - Leggi gli stati delle ispezioni fino al singolo controllo, per analizzare gli alert  

**Descrizioni su datasource e attributi**: descrivi in linguaggio semplice cosa contiene un datasource o un attributo.

  - Gli agenti AI usano le descrizioni per interpretare i tuoi dati  
  - Poni domande di business sui tuoi dati e gli agenti AI rispondono in base a ciò che digna monitora  
  - Se la configurazione attuale di digna non permette di rispondere a una domanda, l'agente AI suggerisce, ove possibile, modifiche al datasource e ai suoi attributi, ad es. l'aggiunta di un nuovo dataset  

**Impatto:** Ti permette di porre domande di business sui tuoi dati in linguaggio semplice, e consente agli agenti AI di aiutare a configurare digna e ad analizzare i problemi di qualità dei dati.

---

### digna Engine – Profiling dove preferisci  
Per impostazione predefinita, digna esegue il profiling dei dati dove risiedono, nel database sorgente. Il digna Engine aggiunge un'opzione: digna esporta i dati dalla sorgente e ne esegue il profiling all'interno del digna Engine.

- Facoltativo, non obbligatorio: il profiling nel database sorgente resta disponibile  
- Si seleziona per ogni connessione al database come posizione di profiling (**Profiling Location**): **Source Database** o **digna Engine**  
- Disponibile per tutte le tecnologie sorgente supportate  

**Integrità referenziale tra connessioni**: alcuni controlli richiedono l'esportazione dei dati. Il digna Engine estende **digna Data Validation** per questi casi.

  - **Controlli di integrità referenziale** tra datasource su **connessioni al database diverse**, incluse tecnologie di database diverse (ad es. Oracle e PostgreSQL)  
  - Funziona con entrambe le posizioni di profiling: con Source Database, solo le colonne chiave vengono esportate nel digna Engine  
  - La dashboard indica quando un controllo viene eseguito su due connessioni  

**Impatto:** Ti permette di scegliere dove eseguire il profiling dei dati e garantisce le relazioni tra sistemi basati su tecnologie di database diverse.

---

## Miglioramenti del profiling  

Questa release offre inoltre agli utenti un maggiore controllo su cosa viene profilato e come.

### Attributi query – Colonne definite dall'utente  
- Definisci colonne artificiali: un'espressione SQL su una o più colonne del datasource  
- Ogni attributo query ha un proprio nome  
- Profilato e controllato come qualsiasi altro attributo  

### Categoria di colonna DATE  
- Nuova categoria **Date** per gli attributi  
- Metriche relative alla data ispezionata  

### Profiling on demand  
- Esegui il profiling di qualsiasi attributo sullo snapshot completo di una data, senza avviare un'ispezione  
- Aiuta a impostare il tipo di colonna dell'attributo: **Numerical**, **Categorical**, **Date** o **Unspecified**  

---

## Beneficiari di questa release  

- **Data Engineer:** validazione dei risultati ETL con digna Data Reconciliation  
- **Team Finance, Risk e Controlling:** procedure di riconciliazione standard come regole Exact in digna Data Reconciliation  
- **Team di Data Quality e Governance:** integrità referenziale tra tecnologie di database con il digna Engine  
- **Utenti di business:** domande di business sui dati a cui rispondono gli agenti AI con digna Agentic  
- **Team AI e Automazione:** agenti AI che lavorano con digna tramite digna Agentic  

---

## Aggiornamenti CLI  
- Nessuna modifica  
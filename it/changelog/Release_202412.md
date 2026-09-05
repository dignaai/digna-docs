# Changelog – Release 2024.12

La release 2024.12 introduce una nuova serie di funzionalità e miglioramenti che rendono digna più automatizzata, flessibile e pronta per l'uso aziendale.  
Questa versione migliora la schedulazione, il reporting, la gestione delle query e l'accuratezza del rilevamento delle anomalie.  

---

## Nuove funzionalità

### Built-in Scheduler
Le ispezioni non dipendono più esclusivamente dalla riga di comando o dalle chiamate API.  
Con il **nuovo digna Scheduler**, le ispezioni possono essere eseguite automaticamente in orari definiti.  

- Supporta **espressioni Cron** per pianificazioni ricorrenti (giornaliere, settimanali o intervalli personalizzati).  
- Offre controllo preciso tramite **offset**, **date di inizio** e **date di fine**.  
- Permette ai team di garantire che tutte le sorgenti dati critiche vengano ispezionate in modo coerente e senza intervento manuale.  

---

### Report in formato PDF
I team possono ora condividere facilmente i risultati con gli stakeholder tramite **esportazioni in PDF**.  

- Grafici, metriche e risultati delle anomalie possono essere esportati in un PDF professionale.  
- I report combinano **visualizzazioni** e **dati sottostanti** per servire sia gli utenti tecnici sia quelli aziendali.  
- Elimina la necessità di strumenti esterni per la creazione dei report.  

---

### Nuovo tipo di colonna: `CUSTOM`
Per offrire maggiore flessibilità, digna introduce un nuovo **tipo di colonna `CUSTOM`**.  

- Gli utenti possono definire esattamente quali **statistiche e metriche** vengono applicate ad attributi specifici.  
- Perfetto per casi speciali che non rientrano nelle categorie standard come NUMERICAL o CATEGORICAL.  
- Aiuta a mantenere le analisi focalizzate e i risultati rilevanti per il contesto aziendale.  

---

### Nuovi segnaposto nelle query snapshot
Le snapshot query sono ora più semplici e meno soggette a errori grazie ai **segnaposto dinamici**.  

- Token come `#date+n#` o `#date-n#` regolano automaticamente le date nelle query.  
- Esempio:  
  - `#date+1#` → domani  
  - `#date-2#` → due giorni fa  
- Elimina i calcoli manuali delle date e garantisce coerenza tra i team.  

---

### Ottimizzazione delle soglie
Le soglie per le anomalie sono ora più intelligenti e contestuali.  

- Per metriche come **NULL COUNT**, le soglie inferiori sono automaticamente limitate a **0**.  
- Previene soglie non valide o prive di significato.  
- Riduce i falsi positivi e rende il rilevamento delle anomalie più affidabile.  

---

## Miglioramenti generali
- Componenti **UI** perfezionati nelle viste di configurazione di progetto e attributi.  
- Migliorate le **prestazioni della dashboard** per grandi volumi di dati.  
- Migliorati i **log e i messaggi di errore** per il troubleshooting.  

---

## Riepilogo
La release 2024.12 rafforza digna come piattaforma per la **qualità dei dati, il rilevamento delle anomalie e l'osservabilità**.  
Con l'automazione tramite schedulazione, report PDF condivisibili, colonne personalizzabili, query snapshot semplificate e soglie più intelligenti, digna diventa ancora più preziosa sia per gli utenti tecnici sia per gli stakeholder aziendali.
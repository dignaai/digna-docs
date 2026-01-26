---
title: digna Release 2026.01 | Datasource logici, Connessioni globali e Data Validation avanzata
description: Scopri le novità di digna Release 2026.01. Questa versione introduce connessioni globali al database, datasource logici, condizioni di rilevanza per le anomalie, esportazioni CSV e Data Validation avanzata inclusi controlli di integrità referenziale.
keywords: digna Release 2026.01, digna changelog, digna datasource, digna database connections, digna Data Anomalies, digna Data Validation, referential integrity validation, regole di qualità dei dati, data observability, digna CSV export
image: /assets/logo_square.png
---

# Changelog – Release 2026.01  

Con la Release 2026.01, digna introduce importanti miglioramenti nella modellazione delle datasource, nella gestione delle connessioni e nell'usabilità delle ispezioni.  
Questa versione aumenta la flessibilità in tutti i moduli e amplia notevolmente la copertura di **data quality e validation**.

---

## 🚀 Nuove funzionalità  

### Connessioni globali al database  
- Le connessioni al database vengono ora configurate a livello **globale**.  
- Le connessioni globali possono essere riutilizzate in **tutti i progetti**, semplificando configurazione e manutenzione.  
- **Impatto:** Riduce l'onere operativo e garantisce connettività coerente tra gli ambienti.

### Connessioni multiple di origine per progetto  
- I progetti possono ora fare riferimento a **più configurazioni di connessione di origine**.  
- Consente setup più flessibili per paesaggi dati complessi per progetto.  
- **Impatto:** Supporta architetture enterprise realistiche con sorgenti dati eterogenee.

### Datasource logici  
- Le datasource rappresentano ora un **livello logico** all'interno di un progetto.  
- Ogni datasource può essere supportata da:
    - una **tabella del database**
    - una **vista del database**
    - una **query SQL personalizzata**  
- Questa separazione migliora il riuso, la chiarezza e la modellazione delle ispezioni tra i moduli.  
- **Impatto:** Disaccoppia ispezioni e regole di qualità dei dati dallo storage fisico, migliorando manutenibilità e riuso.

### Condizione di rilevanza per le anomalie  
- È ora possibile definire una **Condizione di Rilevanza dell'Anomalia** per controllare la valutazione dello stato delle anomalie a livello di dataset.  
- Le statistiche vengono calcolate indipendentemente dal fatto che la condizione sia impostata o soddisfatta.  
- Se la condizione **non è soddisfatta**, **digna Data Anomalies** non fornisce lo stato di anomalia (verde / giallo / rosso).  
- **Esempio:** Escludere il dataset dalla valutazione delle anomalie quando il conteggio dei record è inferiore a 10.  
- **Impatto:** Garantisce che le anomalie siano valutate solo nei contesti di business rilevanti.

### Configurazione notifiche per modulo  
- Le notifiche possono ora essere configurate **per modulo** direttamente in digna.  
- Permette il controllo indipendente del comportamento degli alert per **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** e altri moduli.  
- **Impatto:** Abilita strategie di notifica precise, allineate alle responsabilità dei team e alla criticità.

### Esportazione risultati ispezione (CSV)  
- Gli utenti possono ora **scaricare i risultati delle ispezioni come file CSV**.  
- Consente analisi offline, reportistica e integrazione con strumenti esterni.  
- **Impatto:** Semplifica audit, report e analisi della qualità dei dati a valle.

---

## 🧪 Capacità estese di Data Validation  

Con questa release, **digna Data Validation** supporta ora un set completo di regole di qualità dei dati:

- **Regole di validazione a livello di riga**  
- **Controlli di unicità multi-colonna**  
- **Controlli di integrità referenziale tra datasource**

Questi controlli permettono di applicare regole di qualità strutturali e relazionali in paesaggi dati complessi.

### Controlli di unicità per colonne multiple
- Introdotti i **Controlli di Unicità** per un **insieme configurabile di colonne**.  
- Permette la validazione di chiavi composte e vincoli di unicità a livello di business.  
- **Impatto:** Rileva entità di business duplicate che non possono essere identificate con controlli su singola colonna.

### Controlli di integrità referenziale
- Introdotti i **Controlli di Integrità Referenziale** per validare le relazioni tra datasource.  
- Garantisce che i **valori delle chiavi esterne** in una datasource di origine esistano nella datasource target referenziata.  
- Aiuta a individuare record orfani, relazioni interrotte e problemi di coerenza dei dati in anticipo.  
- Progettato per funzionare con **datasource logiche**, incluse viste e query SQL personalizzate.  
- **Casi d'uso:** integrità dei data warehouse, reportistica regolatoria, coerenza dei master data e analisi downstream affidabili.

---

## 🎯 Chi beneficia di questa release  

- **Data Engineer:** Modellazione delle datasource più flessibile e connessioni al database riutilizzabili  
- **Team di Qualità dei Dati & Governance:** Copertura di validazione ampliata inclusi vincoli di integrità relazionale  
- **Team Analytics & BI:** Input più puliti ed esportazione dei risultati delle ispezioni  
- **Platform Owner:** Complessità di configurazione ridotta e manutenibilità operativa migliorata

---

## 🛠 Aggiornamenti CLI  
- Nessuna modifica

---
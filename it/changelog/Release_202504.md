# Changelog – Release 2025.04

Con la Release 2025.04, digna compie un passo importante per rendere la qualità dei dati e l’osservabilità più facili da gestire, più trasparenti per i team e accessibili agli utenti di tutto il mondo.  
Questa release combina **nuove funzionalità potenti**, **miglioramenti all’automazione dei flussi di lavoro** e **affinamenti dell’esperienza utente**.  

---

## Nuove funzionalità

### Inspection Hub – Un nuovo centro di controllo
L’**Inspection Hub** è ora disponibile come punto centrale per gestire tutti i job di ispezione. Invece di passare da un modulo all’altro o di affidarsi esclusivamente all’esecuzione tramite riga di comando, puoi ora monitorare e controllare le tue ispezioni da un’unica interfaccia snella.  

Principali funzionalità:  
- Ispezioni on-demand: Avvia nuovi job all’istante ogni volta che hai bisogno di risultati aggiornati.  
- Cronologia delle ispezioni: Visualizza una timeline delle ispezioni — cosa è stato eseguito, chi l’ha avviato e quando.  
- Monitoraggio dello stato: I job sono chiaramente segnalati come completati, in corso o in sospeso.  
- Informazioni sull’invoker: Controlla rapidamente se un’ispezione è stata avviata da un utente, dallo scheduler o dalla CLI.  
- Strumenti di pulizia: Elimina job obsoleti o non necessari per mantenere l’area di lavoro ordinata.  
- Log dettagliati: Esamina ogni job per vedere quanto è durato, quali sorgenti sono state incluse e come sono state applicate le soglie.  

L’Inspection Hub offre ai team **visibilità e controllo end-to-end**, rendendo le ispezioni più semplici da gestire in progetti di grandi dimensioni.  

---

### Supporto multilingue – digna parla la tua lingua
digna è ora pronta per team internazionali con l’introduzione del **supporto multilingue**.  

In questa release puoi impostare la tua **lingua dell’interfaccia preferita** direttamente nelle Preferenze utente. Le lingue supportate includono:  
- Inglese (UK, US, CA, AU)  
- Tedesco (DE, AT, CH)  
- Polacco (PL)  

Questo rende digna più semplice da usare per organizzazioni multilingue e favorisce una più rapida adozione tra i team che lavorano in regioni diverse. Altre lingue saranno aggiunte nelle prossime release.  

---

### Import & Export delle sorgenti dati – Configurazione semplificata
La coerenza tra gli ambienti è essenziale nelle distribuzioni enterprise. Con la 2025.04, digna introduce l’**import/export delle sorgenti dati** tramite **dignacli**, lo strumento da riga di comando per utenti avanzati.  

Vantaggi:  
- Esporta la configurazione di una sorgente dati una volta e riutilizzala in Sviluppo, Test e Produzione.  
- Elimina la riconfigurazione manuale e riduci il rischio di errori costosi.  
- Supporta flussi di lavoro automatizzati e pipeline CI/CD con semplici comandi CLI (`export-ds` e `import-ds`).  
- Copia rapidamente le sorgenti dati tra progetti per facilitare la collaborazione.  

Questa funzionalità garantisce che i team possano distribuire con fiducia, sapendo che le configurazioni sono coerenti in ogni ambiente.  

---

### Module Analytics (v1) – Dalla rilevazione alla comprensione
digna è nata come piattaforma per il rilevamento di anomalie e il monitoraggio della qualità dei dati. Con la Release 2025.04, evolve ulteriormente con la **prima versione di Module Analytics**.  

Module Analytics aiuta gli utenti a **comprendere i propri dati** invece di limitarsi a reagire ai problemi. Con questo nuovo modulo puoi:  
- Monitorare le tendenze a lungo termine nei tuoi dataset.  
- Rilevare e monitorare la volatilità per comprendere le fluttuazioni.  
- Esplorare il comportamento dei dati nel tempo per ottenere un contesto più profondo.  

Ad esempio, digna può evidenziare automaticamente che *“Il conteggio delle righe è aumentato del 15,8% dall’inizio dell’anno.”*  
Niente query SQL, niente verifiche manuali — solo **insight azionabili a colpo d’occhio**.  

Questa è la base del percorso di digna verso analytics dati avanzati, permettendo ai team di dati di passare da un monitoraggio reattivo a uno proattivo.  

---

### Miglioramenti alla dashboard – Un’esperienza utente più fluida
Oltre alle funzionalità principali, la Release 2025.04 include diversi **affinamenti della dashboard** progettati per rendere digna più intuitiva e piacevole da usare:  
- Navigazione più veloce tra progetti e ispezioni.  
- Layout più pulito per i log delle ispezioni e l’invio dei job.  
- Piccoli aggiustamenti di design che aiutano a trovare gli insight più rapidamente.  

Questi miglioramenti si basano direttamente sul feedback dei clienti e dimostrano il nostro impegno continuo nel rendere digna **una piattaforma pensata per l’uso quotidiano**.  

---

## Miglioramenti generali
- Ottimizzazioni delle prestazioni per i job di ispezione su dataset di grandi dimensioni.  
- Migliore gestione degli errori in dignacli per fornire feedback più chiari.  
- Miglioramenti di stabilità per progetti con molti job simultanei.  
- Affinamenti dell’interfaccia per il filtraggio dei log dei job e la gestione dei progetti.  

---

## Riepilogo
La Release 2025.04 riguarda **controllo, accessibilità e insight**.  

- Il nuovo **Inspection Hub** offre agli utenti piena visibilità sui job di ispezione.  
- Il **supporto multilingue** garantisce che digna possa essere utilizzata da team globali.  
- La funzionalità di **import/export** semplifica la gestione delle configurazioni tra ambienti.  
- **Module Analytics (v1)** sposta il focus dalla rilevazione alla comprensione, con monitoraggio di trend e volatilità.  
- I **miglioramenti alla dashboard** rifiniscono l’esperienza utente complessiva.  

Insieme, questi aggiornamenti rendono digna più potente, facile da usare e pronta per il mercato internazionale come mai prima d’ora.
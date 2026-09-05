---
title: digna CLI Reference 2025.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2025.109 Learn how to manage users, repositories, and data with commands such as add-user, check-config, check-repo-connection, inspect, inspect-async, and more.
image: /assets/logo_square.png
---

# digna CLI Reference 2025.09
**2025-09-29**

Questa pagina documenta l'insieme completo di comandi disponibili nella CLI di ***digna*** release **2025.09**, incluse esempi d'uso e opzioni.

---

## Nozioni di base sulla CLI

---

### help
L'opzione `--help` fornisce informazioni sui comandi disponibili e sul loro utilizzo. Ci sono due modi principali per usare questa opzione:

1. **Visualizzare l'help generale:**
   
    Usare --help immediatamente dopo il comando ***digna***  
   ```bash
   dignacli --help
   ```

2. **Ottenere aiuto per comandi specifici:**  
  
    Per informazioni dettagliate su un comando specifico, aggiungere `--help` a quel comando.
    Ad esempio, per ottenere aiuto sul comando `add-user`, eseguire:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Descrizione del comando:** Fornisce una descrizione dettagliata di cosa fa il comando.  
     - **Sintassi:** Mostra la sintassi esatta, inclusi argomenti obbligatori e opzionali.  
     - **Opzioni:** Elenca le opzioni specifiche del comando, insieme alle loro spiegazioni.  
     - **Esempi:** Fornisce esempi di come eseguire il comando in modo efficace.

### check-config

Il comando check-config è un'utility all'interno della CLI di ***digna*** progettata per testare la configurazione di ***digna***. Questo comando verifica che i componenti di ***digna*** riescano a trovare gli elementi di configurazione necessari nel file config.toml.

#### Opzioni

- `--configpath`, `-cp`: File o directory che contiene la configurazione. Se omesso, verrà usato ../config.toml.
      
#### Utilizzo del comando
```bash
dignacli check-config
```

All'esecuzione con successo, il comando stampa una conferma della completezza della configurazione.  
  
Se la configurazione risulta incompleta, verranno elencati gli elementi di configurazione mancanti.

  
### check-repo-connection

Il comando check-repo-connection è un'utility nella CLI di ***digna*** progettata per testare la connettività e l'accesso a un repository ***digna*** specificato. Questo comando verifica che la CLI possa interagire con il repository.
      
#### Utilizzo del comando
```bash
dignacli check-repo-connection
```

All'esecuzione con successo, il comando restituisce una conferma della connessione, insieme ai dettagli sul repository: versione del Repository, Host, Database e Schema.  
  
Se la connessione al repository non va a buon fine, controllare il file config.toml per impostazioni di configurazione corrette.


### version

Per verificare la versione installata di *dignacli*, usare l'opzione --version.  
  
#### Utilizzo del comando
```bash
dignacli --version
```
  
#### Esempio di output
```bash
dignacli version 2025.09
```

### opzioni di logging
  
Per impostazione predefinita, l'output in console dei comandi ***digna*** è pensato per essere minimalista. La maggior parte dei comandi offre la possibilità di fornire informazioni aggiuntive, utilizzando le seguenti opzioni:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” e “debug” definiscono il livello di dettaglio, mentre l'opzione “logfile” consente di reindirizzare l'output in streaming su un file anziché sulla finestra della console.

## Gestione utenti

### add-user
  
Il comando add-user nella CLI di ***digna*** è usato per aggiungere un nuovo utente al sistema ***digna***.
  
#### Utilizzo del comando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argomenti

- **USER_NAME**: Il nome utente per il nuovo utente (obbligatorio).
- **USER_FULL_NAME**: Il nome completo del nuovo utente (obbligatorio).
- **USER_PASSWORD**: La password per il nuovo utente (obbligatorio).

#### Opzioni

- `--is_superuser`, `-su`: Flag per designare il nuovo utente come amministratore.
- `--valid_until`, `-vu`: Imposta una data di scadenza per l'account utente nel formato `YYYY-MM-DD HH:MI:SS`. Se non impostata, l'account non ha data di scadenza.

#### Esempio

Per aggiungere un nuovo utente con username `jdoe`, nome completo `John Doe` e password `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Per aggiungere un nuovo utente e impostare una data di scadenza dell'account:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Il comando `delete-user` nella CLI di ***digna*** è usato per rimuovere un utente esistente dal sistema ***digna***.
  
#### Utilizzo del comando
```bash
dignacli delete-user USER_NAME
```
  
#### Argomenti
- **USER_NAME**: Il nome utente dell'utente da eliminare (obbligatorio). Questo è l'unico argomento richiesto dal comando.

#### Esempio
```bash
dignacli delete-user jdoe
```
  
L'esecuzione di questo comando rimuoverà l'utente `jdoe` dal sistema ***digna***, revocandone l'accesso ed eliminando i dati e i permessi associati dal repository.

### modify-user

Il comando `modify-user` nella CLI di ***digna*** è usato per aggiornare i dettagli di un utente esistente nel sistema ***digna***.

#### Utilizzo del comando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argomenti
  
- **USER_NAME**: Il nome utente dell'utente da modificare (obbligatorio).
- **USER_FULL_NAME**: Il nuovo nome completo per l'utente (obbligatorio).
  
#### Opzioni  
  
- `--is_superuser`, `-su`: Imposta l'utente come superuser, concedendo privilegi elevati. Questo flag non richiede un valore.  
- `--valid_until`, `-vu`: Imposta una data di scadenza per l'account utente nel formato YYYY-MM-DD HH:MI:SS. Se non fornita, l'account rimane valido indefinitamente.  
  
#### Esempio
  
Per modificare il nome completo dell'utente `jdoe` in “Johnathan Doe” e impostare l'utente come superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Il comando `modify-user-pwd` nella CLI di ***digna*** è usato per cambiare la password di un utente esistente nel sistema ***digna***.
  
#### Utilizzo del comando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argomenti
  
- **USER_NAME**: Il nome utente dell'utente di cui cambiare la password (obbligatorio).
- **USER_PWD**: La nuova password per l'utente (obbligatorio).
  
#### Esempio
  
Per cambiare la password dell'utente `jdoe` in `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Il comando `list-users` nella CLI di ***digna*** visualizza l'elenco di tutti gli utenti registrati nel sistema ***digna***.

#### Utilizzo del comando

```bash
dignacli list-users
```

L'esecuzione di questo comando nella CLI di ***digna*** si connetterà al repository ***digna*** e elencherà tutti gli utenti, mostrando il loro ID, username, nome completo, stato di superuser e timestamp di scadenza.

## Gestione del repository

### upgrade-repo
  
Il comando `upgrade-repo` nella CLI di ***digna*** è usato per aggiornare o inizializzare il repository di ***digna***. Questo comando è essenziale per applicare aggiornamenti o impostare l'infrastruttura del repository per la prima volta.
  
#### Utilizzo del comando

```bash
dignacli upgrade-repo [options]
```
  
#### Opzioni
  
- `--simulation-mode`, `-s`: Quando abilitata, questa opzione esegue il comando in modalità simulazione, stampando le istruzioni SQL che verrebbero eseguite ma senza applicarle effettivamente. Questo è utile per anteprime delle modifiche senza apportare modifiche al repository.  

  
#### Esempio
  
Per aggiornare il repository di ***digna***, è possibile eseguire il comando senza opzioni:
  
```bash
dignacli upgrade-repo
```  
Per eseguire l'upgrade in modalità simulazione (per vedere le istruzioni SQL senza applicarle):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Questo comando è cruciale per mantenere il sistema ***digna***, garantendo che lo schema del database e gli altri componenti del repository siano aggiornati con l'ultima versione del software.

### encrypt
  
Il comando `encrypt` nella CLI di ***digna*** è usato per crittografare una password.
  
#### Utilizzo del comando
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argomenti
- **PASSWORD**: La password che deve essere crittografata (obbligatorio).
  
#### Esempio
  
Per crittografare una password, è necessario fornire la password come argomento.   
Ad esempio, per crittografare la password `mypassword123`, si utilizzerà:
```bash
dignacli encrypt mypassword123
```
Questo comando restituisce la versione crittografata della password fornita, che può poi essere utilizzata in contesti sicuri. Se l'argomento della password non viene fornito, la CLI mostrerà un errore indicando l'argomento mancante.

### generate-key
  
Il comando `generate-key` viene utilizzato per generare una chiave Fernet, essenziale per proteggere le password memorizzate nel repository di ***digna***.
  
#### Utilizzo del comando
```bash
dignacli generate-key
```
  
## Gestione dei dati

### clean-up

Il comando `clean-up` nella CLI di ***digna*** è utilizzato per rimuovere profili, predizioni e i dati del sistema semaforico per una o più sorgenti di dati all'interno di un progetto specificato. Questo comando è essenziale per la gestione del ciclo di vita dei dati, aiutando a mantenere un ambiente dati organizzato ed efficiente eliminando dati obsoleti o non necessari.

#### Utilizzo del comando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto dal quale rimuovere i dati (obbligatorio). Usando la parola chiave all-projects in questo argomento si istruisce ***digna*** a iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per la rimozione dei dati. I formati accettati includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per la rimozione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
#### Opzioni
  
- `--table-name`, `-tn`: Limita l'operazione di clean-up a una specifica tabella all'interno del progetto.
- `--table-filter`, `-tf`: Filtri per limitare il clean-up alle tabelle che contengono la sottostringa specificata nei loro nomi.
- `--timing`, `-tm`: Visualizza la durata temporale del processo di clean-up al termine.
- `--help`: Mostra informazioni di aiuto per il comando clean-up ed esce.
  
#### Esempio
  
Per rimuovere i dati dal progetto ProjectA tra il 1° gennaio 2023 e il 30 giugno 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Per rimuovere i dati solo da una tabella specifica chiamata `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Questo comando aiuta nella gestione dello spazio dati e garantisce che il repository contenga solo informazioni rilevanti.

### remove-orphans
  
Il comando `remove-orphans` nella CLI di ***digna*** è usato per attività di manutenzione nel repository di ***digna***.  
Quando un utente elimina progetti o sorgenti di dati, i profili e le predizioni possono rimanere nel repository. Con questo comando è possibile rimuovere tali righe orfane dal repository.
  
#### Utilizzo del comando
  
```bash
dignacli list-projects
```

### list-projects
  
Il comando `list-projects` nella CLI di ***digna*** è usato per visualizzare l'elenco di tutti i progetti disponibili nel sistema ***digna***.
  
#### Utilizzo del comando
  
```bash
dignacli list-projects
```

Questo comando è particolarmente utile per amministratori e utenti che gestiscono più progetti, fornendo una panoramica rapida dei progetti disponibili nel repository di ***digna***.

### list-ds

Il comando `list-ds` nella CLI di ***digna*** è usato per visualizzare l'elenco di tutte le sorgenti di dati disponibili all'interno di un progetto specificato. Questo comando è utile per comprendere le risorse dati disponibili per analisi e gestione nel sistema ***digna***.

#### Utilizzo del comando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto per il quale vengono elencate le sorgenti di dati (obbligatorio).
  
#### Esempio
  
Per elencare tutte le sorgenti di dati nel progetto chiamato `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Questo comando fornisce agli utenti una panoramica delle sorgenti di dati disponibili in un progetto, aiutandoli a navigare e gestire più efficacemente il panorama dei dati.


### inspect

Il comando `inspect` nella CLI di ***digna*** è usato per creare profili, predizioni e i dati del sistema semaforico per una o più sorgenti di dati all'interno di un progetto specificato. Questo comando aiuta ad analizzare e monitorare i dati in un periodo definito. Al termine dell'ispezione, viene restituito il valore calcolato del sistema semaforico:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Utilizzo del comando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto per cui ispezionare i dati (obbligatorio). Usando la parola chiave all-projects in questo argomento si istruisce ***digna*** a iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per l'ispezione dei dati. I formati accettati includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per l'ispezione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
#### Opzioni

- `--table-name`, `-tn`: Limita l'ispezione a una specifica tabella all'interno del progetto.
- `--table-filter`, `-tf`: Filtri per ispezionare solo le tabelle che contengono la sottostringa specificata nei loro nomi.
- `--enable_notification`, `-en`: Abilita l'invio di notifiche in caso di allerta.
- `--bypass-backend`, `-bb`: Bypassa il backend ed esegue l'ispezione direttamente dalla CLI (solo per scopi di test!).

  
#### Esempio
  
Per ispezionare i dati del progetto `ProjectA` dal 1° gennaio 2024 al 31 gennaio 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Per ispezionare solo una tabella specifica e forzare il ricalcolo delle predizioni:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Questo comando è utile per generare profili e predizioni aggiornate, monitorare l'integrità dei dati e gestire i sistemi di allerta all'interno di un intervallo temporale specificato per il progetto.

### inspect-async

Il comando `inspect-async` nella CLI di ***digna*** è usato per creare profili, predizioni e i dati del sistema semaforico per una o più sorgenti di dati all'interno di un progetto specificato. Questo comando aiuta ad analizzare e monitorare i dati in un periodo definito. A differenza del comando `inspect`, questo non attende il completamento dell'ispezione.
Invece, restituisce l'id della richiesta per l'ispezione inviata. Per interrogare lo stato di avanzamento del processo di ispezione, utilizzare il comando `inspect-status`.

#### Utilizzo del comando

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto per cui ispezionare i dati (obbligatorio). Usando la parola chiave all-projects in questo argomento si istruisce ***digna*** a iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per l'ispezione dei dati. I formati accettati includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per l'ispezione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
#### Opzioni

- `--table-name`, `-tn`: Limita l'ispezione a una specifica tabella all'interno del progetto.
- `--table-filter`, `-tf`: Filtri per ispezionare solo le tabelle che contengono la sottostringa specificata nei loro nomi.
- `--enable_notification`, `-en`: Abilita l'invio di notifiche in caso di allerta.

  
#### Esempio
  
Per ispezionare i dati del progetto `ProjectA` dal 1° gennaio 2024 al 31 gennaio 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Il comando `inspect-status` nella CLI di ***digna*** viene utilizzato per controllare l'avanzamento di un'ispezione asincrona in base all'ID della richiesta.

#### Utilizzo del comando

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argomenti
  
- **REQUEST_ID**: L'id della richiesta restituito dal comando `inspect-async` 
  
#### Esempio
  
Per controllare l'avanzamento di un'ispezione con request ID 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Il comando `inspect-cancel` nella CLI di ***digna*** è usato per annullare ispezioni basate sull'ID della richiesta oppure per annullare tutte le richieste correnti.

#### Utilizzo del comando

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argomenti
  
- **REQUEST_ID**: L'id della richiesta restituito dal comando `inspect-async` 
  
#### Esempio
  
Per annullare l'ispezione con request ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Per annullare tutte le richieste attualmente in esecuzione o in coda:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Il comando `export-ds` nella CLI di ***digna*** è usato per creare un'esportazione delle sorgenti di dati dal repository di ***digna***. Per impostazione predefinita, verranno esportate tutte le sorgenti di dati di un dato progetto.

#### Utilizzo del comando
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto dal quale verranno esportate le sorgenti di dati.

#### Opzioni

- `--table_name`, `-tn`: Esporta una particolare sorgente di dati da un progetto.
- `--exportfile`, `-ef`: Specifica il nome del file per l'esportazione.
    
#### Esempio
  
Per esportare tutte le sorgenti di dati dal progetto chiamato `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Questo comando esporta tutte le sorgenti di dati di `ProjectA` come documento JSON che può essere importato in un altro progetto o repository ***digna***.


### import-ds

Il comando `import-ds` nella CLI di ***digna*** è usato per importare sorgenti di dati in un progetto target e creare un report di importazione.

#### Utilizzo del comando
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto nel quale verranno importate le sorgenti di dati.
- **EXPORT_FILE**: Il nome del file dell'esportazione delle sorgenti di dati da importare.

#### Opzioni

- `--output-file`, `-o`: File in cui salvare il report di importazione (se non specificato, stampa in terminale in forma tabellare).
- `--output-format`, `-f`: Formato per salvare il report di importazione (json, csv).
    
#### Esempio
  
Per importare tutte le sorgenti di dati dal file di esportazione `my_export.json` in `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Dopo l'importazione, questo comando mostrerà anche un report degli oggetti importati e saltati. Verranno importate in `ProjectB` solo le sorgenti di dati nuove. Per scoprire quali oggetti verrebbero importati e quali saltati, è possibile utilizzare il comando `plan-import-ds`.

### plan-import-ds

Il comando `plan-import-ds` nella CLI di ***digna*** è usato per analizzare un'esportazione di sorgenti di dati rispetto a un progetto target e creare un report di importazione pianificata.

#### Utilizzo del comando
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto nel quale le sorgenti di dati verrebbero importate.
- **EXPORT_FILE**: Il nome del file dell'esportazione delle sorgenti di dati da analizzare prima dell'importazione.

#### Opzioni

- `--output-file`, `-o`: File in cui salvare il report di importazione (se non specificato, stampa in terminale in forma tabellare).
- `--output-format`, `-f`: Formato per salvare il report di importazione (json, csv).
    
#### Esempio
  
Per controllare quali sorgenti di dati verrebbero importate e quali verrebbero saltate dal file di esportazione `my_export.json` quando importato in `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Questo comando mostrerà solo un piano di importazione degli oggetti da importare e da saltare.
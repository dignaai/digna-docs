---
title: Riferimento CLI di digna 2026.01 – Comandi & Esempi | Documentazione digna
description: Riferimento completo per la CLI di digna release 2026.01. Scopri come gestire utenti, repository e dati con comandi come add-user, check-config, check-repo-connection, inspect, inspect-async e altri.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202601/
image: /assets/logo_square.png
---

# digna CLI Reference 2026.01
**2026-01-15**

Questa pagina documenta l'insieme completo di comandi disponibili nella CLI ***digna*** release **2026.01**, inclusi esempi di utilizzo e opzioni.

---

## Nozioni di base sulla CLI

---

### help
L'opzione `--help` fornisce informazioni sui comandi disponibili e sul loro utilizzo. Ci sono due modi principali per usare questa opzione:

1. **Visualizzare l'help generale:**
   
    Usa --help immediatamente dopo la parola chiave ***dignacli***
   ```bash
   dignacli --help
   ```

2. **Ottenere help per comandi specifici:**  
  
    Per informazioni dettagliate su un comando specifico, aggiungi `--help` a quel comando.
    Ad esempio, per ottenere aiuto sul comando `add-user`, esegui:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Descrizione del comando:** Offre una descrizione dettagliata di cosa fa il comando.  
     - **Sintassi:** Mostra la sintassi esatta, inclusi argomenti obbligatori e opzionali.  
     - **Opzioni:** Elenca eventuali opzioni specifiche del comando, insieme alle spiegazioni.  
     - **Esempi:** Fornisce esempi su come eseguire efficacemente il comando.

### check-config

Il comando check-config è una utility all'interno della CLI ***digna*** progettata per testare la configurazione di ***digna***. Questo comando verifica che i componenti di ***digna*** possano trovare gli elementi di configurazione necessari nel file config.toml.

#### Opzioni

- `--configpath`, `-cp`: File o directory che contiene la configurazione. Se omesso, verrà utilizzato ../config.toml.
      
#### Uso del comando
```bash
dignacli check-config
```

Alla corretta esecuzione, il comando restituisce una conferma della completezza della configurazione.  
  
Se la configurazione risulta incompleta, verranno elencati gli elementi di configurazione mancanti.

  
### check-repo-connection

Il comando check-repo-connection è una utility nella CLI ***digna*** progettata per testare la connettività e l'accesso a un repository ***digna*** specificato. Questo comando verifica che la CLI possa interagire con il repository.
      
#### Uso del comando
```bash
dignacli check-repo-connection
```

Alla corretta esecuzione, il comando restituisce una conferma della connessione, insieme a dettagli sul repository: versione del repository, Host, Database e Schema.  
  
Se la connessione al repository non riesce, controlla il file config.toml per le impostazioni di configurazione corrette.


### version

Per verificare la versione installata di *dignacli*, usa l'opzione --version.  
  
#### Uso del comando
```bash
dignacli --version
```
  
#### Esempio di output
```bash
dignacli version 2026.01
```

### opzioni di logging
  
Per impostazione predefinita, l'output della console dei comandi ***digna*** è pensato per essere minimalista. La maggior parte dei comandi offre la possibilità di fornire informazioni aggiuntive, utilizzando le seguenti opzioni:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” e “debug” definiscono il livello di dettaglio, mentre l'opzione “logfile” permette di reindirizzare l'output verso un file invece che sulla console.

## Gestione utenti

### add-user
  
Il comando add-user nella CLI ***digna*** viene utilizzato per aggiungere un nuovo utente al sistema ***digna***.
  
#### Uso del comando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argomenti

- **USER_NAME**: Il nome utente per il nuovo account (obbligatorio).
- **USER_FULL_NAME**: Il nome completo del nuovo utente (obbligatorio).
- **USER_PASSWORD**: La password per il nuovo utente (obbligatorio).

#### Opzioni

- `--is_superuser`, `-su`: Flag per designare il nuovo utente come amministratore.
- `--valid_until`, `-vu`: Imposta una data di scadenza per l'account utente nel formato `YYYY-MM-DD HH:MI:SS`. Se non impostata, l'account non ha una data di scadenza.

#### Esempio

Per aggiungere un nuovo utente con username `jdoe`, nome completo `John Doe` e password `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Per aggiungere un nuovo utente e impostare la data di scadenza dell'account:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Il comando `delete-user` nella CLI ***digna*** viene utilizzato per rimuovere un utente esistente dal sistema ***digna***.
  
#### Uso del comando
```bash
dignacli delete-user USER_NAME
```
  
#### Argomenti
- **USER_NAME**: Il nome utente dell'account da eliminare (obbligatorio). Questo è l'unico argomento richiesto dal comando.

#### Esempio
```bash
dignacli delete-user jdoe
```
  
Eseguendo questo comando verrà rimosso l'utente `jdoe` dal sistema ***digna***, revocando il suo accesso ed eliminando i dati e i permessi associati nel repository.

### modify-user

Il comando `modify-user` nella CLI ***digna*** viene utilizzato per aggiornare i dettagli di un utente esistente nel sistema ***digna***.

#### Uso del comando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argomenti
  
- **USER_NAME**: Il nome utente dell'account da modificare (obbligatorio).
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
  
Il comando `modify-user-pwd` nella CLI ***digna*** viene utilizzato per cambiare la password di un utente esistente nel sistema ***digna***.
  
#### Uso del comando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argomenti
  
- **USER_NAME**: Il nome utente dell'account di cui cambiare la password (obbligatorio).
- **USER_PWD**: La nuova password per l'utente (obbligatorio).
  
#### Esempio
  
Per cambiare la password dell'utente `jdoe` in `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Il comando `list-users` nella CLI ***digna*** visualizza l'elenco di tutti gli utenti registrati nel sistema ***digna***.

#### Uso del comando

```bash
dignacli list-users
```

Eseguendo questo comando la CLI si connetterà al repository ***digna*** e elencherà tutti gli utenti, mostrando il loro ID, username, nome completo, stato di superuser e timestamp di scadenza.

## Gestione del repository

### upgrade-repo
  
Il comando `upgrade-repo` nella CLI ***digna*** viene utilizzato per aggiornare o inizializzare il repository ***digna***. Questo comando è essenziale per applicare aggiornamenti o per impostare l'infrastruttura del repository per la prima volta.
  
#### Uso del comando

```bash
dignacli upgrade-repo [options]
```
  
#### Opzioni
  
- `--simulation-mode`, `-s`: Quando abilitata, questa opzione esegue il comando in modalità simulazione, stampando le istruzioni SQL che verrebbero eseguite ma senza effettivamente eseguirle. È utile per visualizzare le modifiche senza apportare modifiche al repository.  

  
#### Esempio
  
Per aggiornare il repository ***digna***, puoi eseguire il comando senza opzioni:
  
```bash
dignacli upgrade-repo
```  
Per eseguire l'upgrade in modalità simulazione (per vedere gli statement SQL senza applicarli):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Questo comando è cruciale per la manutenzione del sistema ***digna***, garantendo che lo schema del database e gli altri componenti del repository siano aggiornati con l'ultima versione del software.

### encrypt
  
Il comando `encrypt` nella CLI ***digna*** viene utilizzato per cifrare una password.
  
#### Uso del comando
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argomenti
- **PASSWORD**: La password da cifrare (obbligatorio).
  
#### Esempio
  
Per cifrare una password, è necessario fornire la password come argomento.   
Ad esempio, per cifrare la password `mypassword123`, useresti:
```bash
dignacli encrypt mypassword123
```
Questo comando restituisce la versione cifrata della password fornita, che può poi essere utilizzata in contesti sicuri. Se l'argomento password non viene fornito, la CLI mostrerà un errore indicando l'argomento mancante.

### generate-key
  
Il comando `generate-key` viene utilizzato per generare una chiave Fernet, necessaria per proteggere le password memorizzate nel repository ***digna***.
  
#### Uso del comando
```bash
dignacli generate-key
```
  
## Gestione dei dati

### clean-up

Il comando `clean-up` nella CLI ***digna*** viene utilizzato per rimuovere profili, predizioni e dati del sistema a semaforo per una o più sorgenti di dati all'interno di un progetto specificato. Questo comando è essenziale per la gestione del ciclo di vita dei dati, aiutando a mantenere un ambiente dati organizzato ed efficiente eliminando dati obsoleti o non necessari.

#### Uso del comando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto dal quale rimuovere i dati (obbligatorio). L'uso della parola chiave all-projects in questo argomento istruisce ***digna*** a iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per la rimozione dei dati. I formati accettabili includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per la rimozione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
#### Opzioni
  
- `--table-name`, `-tn`: Limita l'operazione di clean-up a una specifica tabella all'interno del progetto.
- `--table-filter`, `-tf`: Filtri per limitare il clean-up alle tabelle che contengono la sottostringa specificata nel loro nome.
- `--timing`, `-tm`: Mostra la durata temporale del processo di clean-up al termine.
- `--help`: Mostra le informazioni di help per il comando clean-up ed esce.
  
#### Esempio
  
Per rimuovere dati dal progetto ProjectA tra il 1 gennaio 2023 e il 30 giugno 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Per rimuovere dati solo da una tabella specifica chiamata `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Questo comando aiuta nella gestione dello storage dei dati e garantisce che il repository contenga solo informazioni pertinenti.

### remove-orphans
  
Il comando `remove-orphans` nella CLI ***digna*** è utilizzato per attività di manutenzione nel repository ***digna***.  
Quando un utente elimina progetti o sorgenti di dati, profili e predizioni possono rimanere nel repository. Con questo comando, tali righe orfane verranno rimosse dal repository.
  
#### Uso del comando
  
```bash
dignacli list-projects
```

### list-projects
  
Il comando `list-projects` nella CLI ***digna*** viene utilizzato per visualizzare un elenco di tutti i progetti disponibili all'interno del sistema ***digna***.
  
#### Uso del comando
  
```bash
dignacli list-projects
```

Questo comando è particolarmente utile per amministratori e utenti che gestiscono più progetti, fornendo una panoramica rapida dei progetti disponibili nel repository ***digna***.

### list-ds

Il comando `list-ds` nella CLI ***digna*** viene utilizzato per visualizzare un elenco di tutte le sorgenti di dati disponibili all'interno di un progetto specificato. Questo comando è utile per comprendere gli asset dati disponibili per analisi e gestione nel sistema ***digna***.

#### Uso del comando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto per il quale si elencano le sorgenti di dati (obbligatorio).
  
#### Esempio
  
Per elencare tutte le sorgenti di dati nel progetto denominato `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Questo comando fornisce agli utenti una panoramica delle sorgenti di dati disponibili in un progetto, aiutandoli a navigare e gestire più efficacemente il panorama dei dati.


### inspect

Il comando `inspect` nella CLI ***digna*** viene utilizzato per creare profili, predizioni e dati del sistema a semaforo per una o più sorgenti di dati all'interno di un progetto specificato. Questo comando aiuta ad analizzare e monitorare i dati in un periodo definito. Al termine dell'ispezione, viene restituito il valore del sistema a semaforo calcolato:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Uso del comando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto per cui ispezionare i dati (obbligatorio). L'uso della parola chiave all-projects in questo argomento istruisce ***digna*** a iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per l'ispezione dei dati. I formati accettabili includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per l'ispezione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
#### Opzioni

- `--table-name`, `-tn`: Limita l'ispezione a una specifica tabella all'interno del progetto.
- `--table-filter`, `-tf`: Filtra per ispezionare solo le tabelle che contengono la sottostringa specificata nei loro nomi.
- `--enable_notification`, `-en`: Abilita l'invio di notifiche in caso di alert.
- `--bypass-backend`, `-bb`: Ignora il backend ed esegue l'ispezione direttamente dalla CLI (solo per scopi di test!).

  
#### Esempio
  
Per ispezionare i dati del progetto `ProjectA` dal 1 gennaio 2024 al 31 gennaio 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Per ispezionare solo una tabella specifica e forzare il ricalcolo delle predizioni:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Questo comando è utile per generare profili e predizioni aggiornate, monitorare l'integrità dei dati e gestire i sistemi di alert all'interno di un intervallo temporale di progetto specificato.

### inspect-async

Il comando `inspect-async` nella CLI ***digna*** viene utilizzato per creare profili, predizioni e dati del sistema a semaforo per una o più sorgenti di dati all'interno di un progetto specificato. Questo comando aiuta ad analizzare e monitorare i dati in un periodo definito. A differenza del comando `inspect`, questo non attende il completamento dell'ispezione.
Invece, restituisce l'id della richiesta per l'ispezione inviata. Per interrogare l'avanzamento del processo di ispezione, usa il comando `inspect-status`.

#### Uso del comando

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto per cui ispezionare i dati (obbligatorio). L'uso della parola chiave all-projects in questo argomento istruisce ***digna*** a iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per l'ispezione dei dati. I formati accettabili includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per l'ispezione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
#### Opzioni

- `--table-name`, `-tn`: Limita l'ispezione a una specifica tabella all'interno del progetto.
- `--table-filter`, `-tf`: Filtra per ispezionare solo le tabelle che contengono la sottostringa specificata nei loro nomi.
- `--enable_notification`, `-en`: Abilita l'invio di notifiche in caso di alert.

  
#### Esempio
  
Per ispezionare i dati del progetto `ProjectA` dal 1 gennaio 2024 al 31 gennaio 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Il comando `inspect-status` nella CLI ***digna*** viene utilizzato per controllare l'avanzamento di un'ispezione asincrona basata sull'id della richiesta.

#### Uso del comando

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

Il comando `inspect-cancel` nella CLI ***digna*** viene utilizzato per cancellare ispezioni basate sull'id della richiesta oppure può essere usato per cancellare tutte le richieste correnti.

#### Uso del comando

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argomenti
  
- **REQUEST_ID**: L'id della richiesta restituito dal comando `inspect-async` 
  
#### Esempio
  
Per cancellare l'ispezione con request ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Per cancellare tutte le richieste attualmente in esecuzione o in coda:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Il comando `export-ds` nella CLI ***digna*** viene utilizzato per creare un'esportazione delle sorgenti di dati dal repository ***digna***. Per impostazione predefinita, verranno esportate tutte le sorgenti di dati di un dato progetto.

#### Uso del comando
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto dal quale verranno esportate le sorgenti di dati.

#### Opzioni

- `--table_name`, `-tn`: Esporta una specifica sorgente di dati da un progetto.
- `--exportfile`, `-ef`: Specifica il nome del file per l'esportazione.
    
#### Esempio
  
Per esportare tutte le sorgenti di dati dal progetto denominato `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Questo comando esporta tutte le sorgenti di dati di `ProjectA` come un documento JSON che può essere importato in un altro progetto o repository ***digna***.


### import-ds

Il comando `import-ds` nella CLI ***digna*** viene utilizzato per importare sorgenti di dati in un progetto di destinazione e creare un report di importazione.

#### Uso del comando
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto nel quale verranno importate le sorgenti di dati.
- **EXPORT_FILE**: Il nome del file dell'esportazione delle sorgenti di dati da importare.

#### Opzioni

- `--output-file`, `-o`: File in cui salvare il report di importazione (se non specificato, viene stampato in terminale in forma tabellare).
- `--output-format`, `-f`: Formato per salvare il report di importazione (json, csv).
    
#### Esempio
  
Per importare tutte le sorgenti di dati dal file di export `my_export.json` in `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Dopo l'importazione, questo comando mostrerà anche un report degli oggetti importati e saltati. Verranno importate solo le nuove sorgenti di dati in `ProjectB`. Per scoprire quali oggetti verrebbero importati e quali saltati, puoi usare il comando `plan-import-ds`.

### plan-import-ds

Il comando `plan-import-ds` nella CLI ***digna*** viene utilizzato per analizzare un'esportazione di sorgenti di dati rispetto a un progetto di destinazione e creare un report di pianificazione dell'importazione.

#### Uso del comando
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto nel quale le sorgenti di dati verrebbero importate.
- **EXPORT_FILE**: Il nome del file dell'esportazione delle sorgenti di dati da analizzare prima dell'importazione.

#### Opzioni

- `--output-file`, `-o`: File in cui salvare il report di importazione (se non specificato, viene stampato in terminale in forma tabellare).
- `--output-format`, `-f`: Formato per salvare il report di importazione (json, csv).
    
#### Esempio
  
Per verificare quali sorgenti di dati verrebbero importate e quali verrebbero saltate dal file di export `my_export.json` quando importato in `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Questo comando mostrerà solo un piano di importazione degli oggetti da importare e da saltare.
---
title: digna CLI Reference 2025.04 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2025.04. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Questa pagina documenta l'insieme completo di comandi disponibili nella CLI ***digna***, release **2025.04**, inclusi esempi d'uso e opzioni.

---

## Nozioni di base sulla CLI

---

## Utilizzo dell'opzione `--help`

L'opzione `--help` fornisce informazioni sui comandi disponibili e sul loro utilizzo. Ci sono due modi principali per usarla:

1. **Visualizzare l'help generale:**
   
   Usa --help immediatamente dopo il comando principale ***digna***
   ```bash
   dignacli --help
   ```

2. **Ottenere help per comandi specifici:**  
  
   Per informazioni dettagliate su un comando specifico, aggiungi `--help` dopo quel comando.
   Per esempio, per ottenere aiuto sul comando `add-user`, esegui:
   ```bash
   dignacli add-user --help
   ```

   ### output:
      
   - **Descrizione del comando:** Offre una descrizione dettagliata di ciò che fa il comando.  
   - **Sintassi:** Mostra la sintassi esatta, inclusi argomenti obbligatori e opzionali.  
   - **Opzioni:** Elenca le opzioni specifiche del comando, con le relative spiegazioni.  
   - **Esempi:** Fornisce esempi su come eseguire correttamente il comando.

  
## Utilizzo del comando `check-repo-connection`

Il comando `check-repo-connection` è uno strumento della CLI ***digna*** progettato per testare la connettività e l'accesso a un repository ***digna*** specificato. Questo comando verifica che la CLI possa interagire con il repository.
      
#### Utilizzo del comando
```bash
dignacli check-repo-connection
```

Se l'esecuzione ha successo, il comando restituisce una conferma della connessione, insieme ai dettagli del repository: versione del repository, host, database e schema.  
  
Se la connessione al repository non riesce, controlla il file config.toml per verificare le impostazioni di configurazione corrette.

## Utilizzo del comando `--version`

Per verificare la versione installata di *dignacli*, usa l'opzione --version.  
  
#### Utilizzo del comando
```bash
dignacli --version
```
  
#### Esempio di output
```bash
dignacli version 2025.04
```

## Utilizzo delle opzioni di logging
  
Per impostazione predefinita, l'output della console dei comandi ***digna*** è pensato per essere minimalista. La maggior parte dei comandi offre la possibilità di fornire informazioni aggiuntive, usando le seguenti opzioni:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” e “debug” definiscono il livello di dettaglio, mentre l'opzione “logfile” permette di reindirizzare l'output su un file invece che sulla console.

## Gestione utenti

### Utilizzo del comando `add-user`
  
Il comando `add-user` nella CLI ***digna*** viene utilizzato per aggiungere un nuovo utente al sistema ***digna***.
  
#### Utilizzo del comando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argomenti

- **USER_NAME**: Il nome utente per il nuovo account (obbligatorio).
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

### Utilizzo del comando `delete-user`
  
Il comando `delete-user` nella CLI ***digna*** viene utilizzato per rimuovere un utente esistente dal sistema ***digna***.
  
#### Utilizzo del comando
```bash
dignacli delete-user USER_NAME
```
  
##### Argomenti
- **USER_NAME**: Il nome utente dell'utente da eliminare (obbligatorio). Questo è l'unico argomento richiesto dal comando.

#### Esempio
```bash
dignacli delete-user jdoe
```
  
Eseguendo questo comando verrà rimosso l'utente `jdoe` dal sistema ***digna***, revocando il suo accesso e cancellando i dati e i permessi associati dal repository.

### Utilizzo del comando `modify-user`

Il comando `modify-user` nella CLI ***digna*** viene utilizzato per aggiornare i dettagli di un utente esistente nel sistema ***digna***.

#### Utilizzo del comando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argomenti
  
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

### Utilizzo del comando `modify-user-pwd`
  
Il comando `modify-user-pwd` nella CLI ***digna*** viene utilizzato per cambiare la password di un utente esistente nel sistema ***digna***.
  
#### Utilizzo del comando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argomenti
  
- **USER_NAME**: Il nome utente dell'utente di cui cambiare la password (obbligatorio).
- **USER_PWD**: La nuova password per l'utente (obbligatorio).
  
#### Esempio
  
Per cambiare la password dell'utente `jdoe` in `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Utilizzo del comando `list-users`

Il comando `list-users` nella CLI ***digna*** visualizza l'elenco di tutti gli utenti registrati nel sistema ***digna***.

#### Utilizzo del comando

```bash
dignacli list-users
```

Eseguendo questo comando la CLI ***digna*** si connetterà al repository ***digna*** e elencherà tutti gli utenti, mostrando il loro ID, username, nome completo, stato di superuser e timestamp di scadenza.

## Gestione del repository

### Utilizzo del comando `upgrade-repo`
  
Il comando `upgrade-repo` nella CLI ***digna*** viene utilizzato per aggiornare o inizializzare il repository ***digna***. Questo comando è essenziale per applicare aggiornamenti o per configurare l'infrastruttura del repository per la prima volta.
  
#### Utilizzo del comando

```bash
dignacli upgrade-repo [options]
```
  
#### Opzioni
  
- `--simulation-mode`, `-s`: Quando abilitata, questa opzione esegue il comando in modalità simulazione, stampando le istruzioni SQL che verrebbero eseguite ma senza eseguirle effettivamente. Utile per visualizzare le modifiche senza applicarle al repository.  

  
#### Esempio
  
Per aggiornare il repository ***digna***, puoi eseguire il comando senza opzioni:
  
```bash
dignacli upgrade-repo
```  
Per eseguire l'upgrade in modalità simulazione (per vedere le istruzioni SQL senza applicarle):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Questo comando è cruciale per mantenere il sistema ***digna***, assicurando che lo schema del database e gli altri componenti del repository siano aggiornati alla versione più recente del software.

### Utilizzo del comando `encrypt`
  
Il comando `encrypt` nella CLI ***digna*** viene utilizzato per criptare una password.
  
#### Utilizzo del comando
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argomenti
- **PASSWORD**: La password da criptare (obbligatorio).
  
#### Esempio
  
Per criptare una password, devi fornire la password come argomento.   
Per esempio, per criptare la password `mypassword123`, utilizzeresti:
```bash
dignacli encrypt mypassword123
```
Questo comando restituisce la versione criptata della password fornita, che può poi essere usata in contesti sicuri. Se l'argomento password non viene fornito, la CLI mostrerà un errore indicando l'argomento mancante.

## Utilizzo del comando `generate-key`
  
Il comando `generate-key` viene utilizzato per generare una chiave Fernet, essenziale per proteggere le password memorizzate nel repository ***digna***.
  
#### Utilizzo del comando
```bash
dignacli generate-key
```
  
## Gestione dati

## Utilizzo del comando `clean-up`

Il comando `clean-up` nella CLI ***digna*** viene utilizzato per rimuovere profili, previsioni e dati del Traffic Light System per una o più sorgenti di dati all'interno di un progetto specificato. Questo comando è essenziale per la gestione del ciclo di vita dei dati, aiutando a mantenere un ambiente dati organizzato ed efficiente eliminando dati obsoleti o non necessari.

#### Utilizzo del comando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto dal quale rimuovere i dati (obbligatorio). Usando la parola chiave all-projects in questo argomento si istruisce ***digna*** ad iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per la rimozione dei dati. I formati accettati includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per la rimozione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
#### Opzioni
  
- `--table-name`, `-tn`: Limita l'operazione di clean-up a una specifica tabella all'interno del progetto.
- `--table-filter`, `-tf`: Filtra per limitare il clean-up alle tabelle che contengono la sottostringa specificata nel loro nome.
- `--timing`, `-tm`: Mostra la durata del processo di clean-up al termine dell'operazione.
- `--help`: Mostra le informazioni di help per il comando clean-up ed esce.
  
#### Esempio
  
Per rimuovere i dati dal progetto ProjectA tra il 1° gennaio 2023 e il 30 giugno 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Per rimuovere i dati solo da una tabella specifica chiamata `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Questo comando aiuta a gestire lo spazio di archiviazione dei dati e a garantire che il repository contenga solo informazioni rilevanti.

## Utilizzo del comando `list-projects`
  
Il comando `list-projects` nella CLI ***digna*** viene utilizzato per visualizzare l'elenco di tutti i progetti disponibili nel sistema ***digna***.
  
#### Utilizzo del comando
  
```bash
dignacli list-projects
```

Questo comando è particolarmente utile per amministratori e utenti che gestiscono più progetti, fornendo una panoramica rapida dei progetti disponibili nel repository ***digna***.

## Utilizzo del comando `list-ds`

Il comando `list-ds` nella CLI ***digna*** viene utilizzato per visualizzare l'elenco di tutte le sorgenti dati disponibili all'interno di un progetto specificato. Questo comando è utile per comprendere gli asset dati disponibili per analisi e gestione nel sistema ***digna***.

#### Utilizzo del comando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto per il quale si stanno elencando le sorgenti dati (obbligatorio).
  
#### Esempio
  
Per elencare tutte le sorgenti dati nel progetto chiamato `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Questo comando fornisce agli utenti una panoramica delle sorgenti dati disponibili in un progetto, aiutandoli a navigare e gestire il panorama dei dati più efficacemente.


## Utilizzo del comando `inspect`

Il comando `inspect` nella CLI ***digna*** viene utilizzato per creare profili, previsioni e dati del Traffic Light System per una o più sorgenti dati all'interno di un progetto specificato. Questo comando aiuta ad analizzare e monitorare i dati in un periodo definito.

#### Utilizzo del comando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto per cui eseguire l'ispezione dei dati (obbligatorio). Usando la parola chiave all-projects in questo argomento si istruisce ***digna*** ad iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per l'ispezione dei dati. I formati accettati includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per l'ispezione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
#### Opzioni

- `--table-name`, `-tn`: Limita l'ispezione a una specifica tabella all'interno del progetto.
- `--table-filter`, `-tf`: Filtra per ispezionare solo le tabelle che contengono la sottostringa specificata nei loro nomi.
- `--do-profile`: Avvia la ricostruzione dei profili. Il valore predefinito è do-profile.
- `--no-do-profile`: Impedisce la ricostruzione dei profili.
- `--do-prediction`: Avvia il ricalcolo delle previsioni. Il valore predefinito è do-prediction.
- `--no-do-prediction`: Impedisce il ricalcolo delle previsioni.
- `--do-alert-status`: Avvia il ricalcolo degli stati di allerta. Il valore predefinito è do-alert-status.
- `--no-do-alert-status`: Impedisce il ricalcolo degli stati di allerta.
- `--iterative`: Esegue l'ispezione del periodo utilizzando iterazioni giornaliere. Il valore predefinito è iterative.
- `--no-iterative`: Esegue l'ispezione dell'intero periodo in un'unica soluzione.
- `--enable_notification`, `-en`: Abilita l'invio di notifiche in caso di alert.
- `--timing`, `-tm`: Mostra la durata del processo di ispezione al termine.
  
#### Esempio
  
Per ispezionare i dati del progetto `ProjectA` dal 1° gennaio 2024 al 31 gennaio 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Per ispezionare solo una tabella specifica e forzare il ricalcolo delle previsioni:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Questo comando è utile per generare profili e previsioni aggiornate, monitorare l'integrità dei dati e gestire i sistemi di allerta all'interno di un intervallo temporale specificato del progetto.

## Utilizzo del comando `tls-status`

Il comando `tls-status` nella CLI ***digna*** viene utilizzato per interrogare lo stato del Traffic Light System (TLS) per una specifica tabella all'interno di un progetto in una data definita. Il Traffic Light System fornisce informazioni sulla salute e la qualità dei dati, indicando eventuali problemi o allarmi che richiedono attenzione.
  
#### Utilizzo del comando
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto per cui si sta interrogando lo stato TLS (obbligatorio).
- **TABLE_NAME**: La tabella specifica all'interno del progetto per la quale è richiesto lo stato TLS (obbligatorio).
- **DATE**: La data per la quale si richiede lo stato TLS, tipicamente nel formato %Y-%m-%d (obbligatorio).
  
#### Esempio
  
Per verificare lo stato TLS della tabella UserData nel progetto ProjectA il 1° luglio 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Questo comando aiuta gli utenti a monitorare e mantenere la qualità dei dati fornendo un report chiaro e operativo basato su criteri predefiniti.

## Utilizzo del comando `inspect-async`

Il comando `inspect-async` nella CLI ***digna*** viene utilizzato per istruire il backend a eseguire in modo asincrono l'ispezione per una o più sorgenti di dati di un dato progetto. Se project_name è impostato a all-projects, l'ispezione itererà su tutti i progetti disponibili ed eseguirà l'ispezione. Restituisce un request id che può essere usato per monitorare lo stato di avanzamento dell'ispezione.

#### Utilizzo del comando

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto per cui eseguire l'ispezione (obbligatorio). Usando la parola chiave all-projects in questo argomento si istruisce ***digna*** ad iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per l'ispezione dei dati. I formati accettati includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S, o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per l'ispezione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
#### Opzioni

- `--table-name`, `-tn`: Limita l'ispezione a una specifica tabella all'interno del progetto.
- `--table-filter`, `-tf`: Filtra per ispezionare solo le tabelle che contengono la sottostringa specificata nei loro nomi.

  
#### Esempio
  
Per ispezionare i dati del progetto `ProjectA` dal 1° gennaio 2024 al 31 gennaio 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Utilizzo del comando `inspect-status`

Il comando `inspect-status` nella CLI ***digna*** viene utilizzato per controllare l'avanzamento di un'ispezione asincrona basandosi sul request ID.

#### Utilizzo del comando

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argomenti
  
- **REQUEST_ID**: L'ID della richiesta restituito dal comando `inspect-async` 
  
#### Opzioni

- `--report_level`, `-rl`: Imposta il livello di report: 'task' o 'step' [default: task]
  
#### Esempio
  
Per controllare l'avanzamento di un'ispezione con request ID 12345 al livello dettagliato step:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Utilizzo del comando `export-ds`

Il comando `export-ds` nella CLI ***digna*** viene utilizzato per creare un'esportazione delle sorgenti dati dal repository ***digna***. Per impostazione predefinita, tutte le sorgenti dati di un dato progetto verranno esportate.

#### Utilizzo del comando
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto da cui verranno esportate le sorgenti dati.

#### Opzioni

- `--table_name`, `-tn`: Esporta una particolare sorgente dati da un progetto.
- `--exportfile`, `-ef`: Specifica il nome del file per l'esportazione.
    
#### Esempio
  
Per esportare tutte le sorgenti dati dal progetto chiamato `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Questo comando esporta tutte le sorgenti dati di `ProjectA` come documento JSON che può essere importato in un altro progetto o repository ***digna***.


## Utilizzo del comando `import-ds`

Il comando `import-ds` nella CLI ***digna*** viene utilizzato per importare sorgenti dati in un progetto di destinazione e creare un report di importazione.

#### Utilizzo del comando
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto nel quale verranno importate le sorgenti dati.
- **EXPORT_FILE**: Il nome del file dell'esportazione delle sorgenti dati da importare.

#### Opzioni

- `--output-file`, `-o`: File in cui salvare il report di importazione (se non specificato, stampa in terminale in forma tabellare).
- `--output-format`, `-f`: Formato per salvare il report di importazione (json, csv).
    
#### Esempio
  
Per importare tutte le sorgenti dati dal file di esportazione `my_export.json` in `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Dopo l'importazione, questo comando mostrerà anche un report degli oggetti importati e saltati. Verranno importate in `ProjectB` solo le sorgenti dati nuove. Per scoprire quali oggetti verrebbero importati e quali saltati, puoi usare il comando `plan-import-ds`.

## Utilizzo del comando `plan-import-ds`

Il comando `plan-import-ds` nella CLI ***digna*** viene utilizzato per analizzare un'esportazione di sorgenti dati rispetto a un progetto di destinazione e creare un report pianificato di importazione.

#### Utilizzo del comando
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto nel quale le sorgenti dati verrebbero importate.
- **EXPORT_FILE**: Il nome del file dell'esportazione delle sorgenti dati da analizzare prima dell'importazione.

#### Opzioni

- `--output-file`, `-o`: File in cui salvare il report di importazione (se non specificato, stampa in terminale in forma tabellare).
- `--output-format`, `-f`: Formato per salvare il report di importazione (json, csv).
    
#### Esempio
  
Per verificare quali sorgenti dati verrebbero importate e quali saltate dal file di esportazione `my_export.json` quando importate in `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Questo comando mostrerà soltanto un piano di importazione degli oggetti che verrebbero importati e saltati.
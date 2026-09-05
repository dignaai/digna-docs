---
title: Riferimento CLI di digna 2024.12 – Comandi ed Esempi | documentazione di digna
description: Riferimento completo per la CLI digna release 2024.12. Scopri come gestire utenti, repository e dati con comandi come add-user, check-repo-connection, upgrade-repo, inspect e altri.
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Questa pagina documenta l'insieme completo dei comandi disponibili nella CLI di ***digna*** release **2024.12**, inclusi esempi d'uso e opzioni.

---


**2024-12-09**


---

## Nozioni di base sulla CLI

---

## Uso dell'opzione `help`

L'opzione `--help` fornisce informazioni sui comandi disponibili e sul loro utilizzo. Ci sono due modi principali per usare questa opzione:

1. **Visualizzare l'aiuto generale:**
   
    Usa `--help` immediatamente dopo la keyword `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Ottenere aiuto per comandi specifici:**  
  
    Per informazioni dettagliate su un comando specifico, aggiungi `--help` a quel comando.
    Ad esempio, per ottenere aiuto sul comando `add-user`, esegui:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Descrizione del comando:** Fornisce una descrizione dettagliata di ciò che fa il comando.  
     - **Sintassi:** Mostra la sintassi esatta, inclusi argomenti obbligatori e opzionali.  
     - **Opzioni:** Elenca le opzioni specifiche del comando, con le relative spiegazioni.  
     - **Esempi:** Fornisce esempi di come eseguire efficacemente il comando.

  
## Uso del comando `check-repo-connection`

Il comando `check-repo-connection` è una utility all'interno della CLI di ***digna*** progettata per testare la connettività e l'accesso a un repository ***digna*** specificato. Questo comando verifica che la CLI possa interagire con il repository.
      
### Uso del comando
```bash
dignacli check-repo-connection
```

In caso di esecuzione riuscita, il comando restituisce una conferma della connessione, insieme a dettagli sul repository: versione del repository, host, database e schema.  
  
Se la connessione al repository non ha successo, controllare il file config.toml per verificare le impostazioni di configurazione corrette.

## Uso del comando `version`

Per verificare la versione installata di `dignacli`, usa l'opzione `--version`.  
  
### Uso del comando
```bash
dignacli --version
```
  
### Esempio di output
```bash
dignacli version 2024.12
```

## Uso delle opzioni di logging
  
Per impostazione predefinita, l'output console dei comandi di ***digna*** è minimalista. La maggior parte dei comandi offre la possibilità di fornire informazioni aggiuntive, utilizzando le seguenti opzioni:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” e “debug” definiscono il livello di dettaglio, mentre l'opzione “logfile” permette di reindirizzare l'output su un file invece che sulla console.

# Gestione utenti

## Uso del comando `add-user`
  
Il comando `add-user` nella CLI di ***digna*** viene usato per aggiungere un nuovo utente al sistema ***digna***.
  
### Uso del comando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argomenti

- **USER_NAME**: Il nome utente per il nuovo utente (obbligatorio).
- **USER_FULL_NAME**: Il nome completo del nuovo utente (obbligatorio).
- **USER_PASSWORD**: La password per il nuovo utente (obbligatorio).

### Opzioni

- `--is_superuser`, `-su`: Flag per designare il nuovo utente come amministratore.
- `--valid_until`, `-vu`: Imposta una data di scadenza per l'account utente nel formato `YYYY-MM-DD HH:MI:SS`. Se non impostata, l'account non ha data di scadenza.

### Esempio

Per aggiungere un nuovo utente con username `jdoe`, nome completo `John Doe` e password `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Per aggiungere un nuovo utente e impostare una data di scadenza per l'account:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Uso del comando `delete-user`
  
Il comando `delete-user` nella CLI di ***digna*** viene usato per rimuovere un utente esistente dal sistema ***digna***.
  
### Uso del comando
```bash
dignacli delete-user USER_NAME
```
  
### Argomenti
- **USER_NAME**: Il nome utente dell'utente da eliminare (obbligatorio). Questo è l'unico argomento richiesto dal comando.

### Esempio
```bash
dignacli delete-user jdoe
```
  
Eseguendo questo comando verrà rimosso l'utente `jdoe` dal sistema ***digna***, revocando il suo accesso ed eliminando i dati e i permessi associati nel repository.

## Uso del comando `modify-user`

Il comando `modify-user` nella CLI di ***digna*** viene usato per aggiornare i dettagli di un utente esistente nel sistema ***digna***.

### Uso del comando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argomenti
  
- **USER_NAME**: Il nome utente dell'utente da modificare (obbligatorio).
- **USER_FULL_NAME**: Il nuovo nome completo per l'utente (obbligatorio).
  
### Opzioni  
  
- `--is_superuser`, `-su`: Imposta l'utente come superuser, concedendo privilegi elevati. Questo flag non richiede un valore.  
- `--valid_until`, `-vu`: Imposta una data di scadenza per l'account utente nel formato YYYY-MM-DD HH:MI:SS. Se non fornita, l'account rimane valido indefinitamente.  
  
### Esempio
  
Per modificare il nome completo dell'utente `jdoe` in “Johnathan Doe” e impostare l'utente come superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Uso del comando `modify-user-pwd`
  
Il comando `modify-user-pwd` nella CLI di ***digna*** viene usato per cambiare la password di un utente esistente nel sistema ***digna***.
  
### Uso del comando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argomenti
  
- **USER_NAME**: Il nome utente dell'utente la cui password deve essere cambiata (obbligatorio).
- **USER_PWD**: La nuova password per l'utente (obbligatorio).
  
### Esempio
  
Per cambiare la password dell'utente `jdoe` in `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Uso del comando `list-users`

Il comando `list-users` nella CLI di ***digna*** visualizza l'elenco di tutti gli utenti registrati nel sistema ***digna***.

### Uso del comando

```bash
dignacli list-users
```

Eseguendo questo comando la CLI di ***digna*** si connetterà al repository ***digna*** e elencherà tutti gli utenti, mostrando il loro ID, username, nome completo, stato di superuser e timestamp di scadenza.

# Gestione del repository

### Uso del comando `upgrade-repo`
  
Il comando `upgrade-repo` nella CLI di ***digna*** viene usato per aggiornare o inizializzare il repository di ***digna***. Questo comando è essenziale per applicare aggiornamenti o configurare l'infrastruttura del repository per la prima volta.
  
### Uso del comando

```bash
dignacli upgrade-repo [options]
```
  
### Opzioni
  
- `--simulation-mode`, `-s`: Quando abilitata, questa opzione esegue il comando in modalità simulazione, stampando le istruzioni SQL che verrebbero eseguite ma senza applicarle effettivamente. È utile per anteprime delle modifiche senza modificare il repository.  

  
### Esempio
  
Per aggiornare il repository di ***digna***, puoi eseguire il comando senza opzioni:
  
```bash
dignacli upgrade-repo
```  
Per eseguire l'upgrade in modalità simulazione (per vedere le istruzioni SQL senza applicarle):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Questo comando è cruciale per mantenere il sistema ***digna***, garantendo che lo schema del database e gli altri componenti del repository siano aggiornati all'ultima versione del software.

## Uso del comando `encrypt`
  
Il comando `encrypt` nella CLI di ***digna*** viene usato per criptare una password.
  
### Uso del comando
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argomenti
- **PASSWORD**: La password da criptare (obbligatorio).
  
### Esempio
  
Per criptare una password, è necessario fornire la password come argomento.   
Ad esempio, per criptare la password `mypassword123`, useresti:
```bash
dignacli encrypt mypassword123
```
Questo comando restituisce la versione criptata della password fornita, che può poi essere utilizzata in contesti sicuri. Se l'argomento della password non viene fornito, la CLI mostrerà un errore indicando l'argomento mancante.

## Uso del comando `generate-key`
  
Il comando `generate-key` viene usato per generare una chiave Fernet, essenziale per mettere in sicurezza le password memorizzate nel repository di ***digna***.
  
### Uso del comando
```bash
dignacli generate-key
```
  
# Gestione dei dati

## Uso del comando `clean-up`

Il comando `clean-up` nella CLI di ***digna*** viene usato per rimuovere profili, predizioni e dati del sistema a semaforo (traffic light system) per una o più sorgenti dati all'interno di un progetto specificato. Questo comando è essenziale per la gestione del ciclo di vita dei dati, aiutando a mantenere un ambiente dati ordinato ed efficiente eliminando dati obsoleti o non necessari.

### Uso del comando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto dal quale rimuovere i dati (obbligatorio). Usare la keyword `all-projects` in questo argomento istruisce ***digna*** a iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per la rimozione dei dati. I formati accettati includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per la rimozione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
### Opzioni
  
- `--table-name`, `-tn`: Limita l'operazione di clean-up a una tabella specifica all'interno del progetto.
- `--table-filter`, `-tf`: Filtra per limitare il clean-up alle tabelle che contengono la sottostringa specificata nel loro nome.
- `--timing`, `-tm`: Mostra la durata del processo di clean-up al termine.
- `--help`: Mostra le informazioni di aiuto per il comando clean-up ed esce.
  
### Esempio
  
Per rimuovere i dati dal progetto ProjectA tra il 1° gennaio 2023 e il 30 giugno 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Per rimuovere dati solo da una tabella specifica chiamata `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Questo comando aiuta nella gestione dello storage dei dati e garantisce che il repository contenga solo informazioni rilevanti.

## Uso del comando `inspect`

Il comando `inspect` nella CLI di ***digna*** viene usato per creare profili, predizioni e dati del sistema a semaforo (traffic light system) per una o più sorgenti dati all'interno di un progetto specificato. Questo comando aiuta ad analizzare e monitorare i dati su un periodo definito.

### Uso del comando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto per il quale ispezionare i dati (obbligatorio). Usare la keyword `all-projects` in questo argomento istruisce ***digna*** a iterare su tutti i progetti esistenti e applicare questo comando.
- **FROM_DATE**: La data e ora di inizio per l'ispezione dei dati. I formati accettati includono %Y-%m-%d, %Y-%m-%dT%H:%M:%S o %Y-%m-%d %H:%M:%S (obbligatorio).
- **TO_DATE**: La data e ora di fine per l'ispezione dei dati, seguendo gli stessi formati di FROM_DATE (obbligatorio).
  
### Opzioni

- `--table-name`, `-tn`: Limita l'ispezione a una tabella specifica all'interno del progetto.
- `--table-filter`, `-tf`: Filtra per ispezionare solo le tabelle che contengono la sottostringa specificata nel loro nome.
- `--do-profile`: Forza la raccolta dei profili. Il valore predefinito è do-profile.
- `--no-do-profile`: Impedisce la raccolta dei profili.
- `--do-prediction`: Forza il ricalcolo delle predizioni. Il valore predefinito è do-prediction.
- `--no-do-prediction`: Impedisce il ricalcolo delle predizioni.
- `--do-alert-status`: Forza il ricalcolo degli stati di allerta. Il valore predefinito è do-alert-status.
- `--no-do-alert-status`: Impedisce il ricalcolo degli stati di allerta.
- `--iterative`: Esegue l'ispezione di un periodo usando iterazioni giornaliere. Il valore predefinito è iterative.
- `--no-iterative`: Esegue l'ispezione dell'intero periodo in un'unica esecuzione.
- `--timing`, `-tm`: Mostra la durata del processo di ispezione al termine.
  
### Esempio
  
Per ispezionare i dati del progetto `ProjectA` dal 1° gennaio 2024 al 31 gennaio 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Per ispezionare solo una tabella specifica e forzare il ricalcolo delle predizioni:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Questo comando è utile per generare profili e predizioni aggiornate, monitorare l'integrità dei dati e gestire i sistemi di allerta all'interno di un periodo di progetto specificato.

## Uso del comando `tls-status`

Il comando `tls-status` nella CLI di ***digna*** viene usato per interrogare lo stato del Traffic Light System (TLS) per una specifica tabella all'interno di un progetto in una data specifica. Il Traffic Light System fornisce indicazioni sulla salute e la qualità dei dati, segnalando eventuali problemi o allerta che richiedono attenzione.
  
### Uso del comando
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argomenti
  
- **PROJECT_NAME**: Il nome del progetto per il quale si sta interrogando lo stato TLS (obbligatorio).
- **TABLE_NAME**: La tabella specifica all'interno del progetto per la quale è necessario lo stato TLS (obbligatorio).
- **DATE**: La data per la quale si sta interrogando lo stato TLS, tipicamente nel formato %Y-%m-%d (obbligatorio).
  
### Esempio
  
Per controllare lo stato TLS di una tabella chiamata UserData nel progetto ProjectA il 1° luglio 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Questo comando aiuta gli utenti a monitorare e mantenere la qualità dei dati fornendo un rapporto chiaro e azionabile basato su criteri predefiniti.

## Uso del comando `list-projects`
  
Il comando `list-projects` nella CLI di ***digna*** viene usato per visualizzare l'elenco di tutti i progetti disponibili nel sistema ***digna***.
  
### Uso del comando
  
```bash
dignacli list-projects
```

Questo comando è particolarmente utile per amministratori e utenti che gestiscono più progetti, fornendo una panoramica rapida dei progetti disponibili nel repository di ***digna***.

## Uso del comando `list-ds`

Il comando `list-ds` nella CLI di ***digna*** viene usato per visualizzare l'elenco di tutte le sorgenti dati disponibili all'interno di un progetto specificato. Questo comando è utile per capire le risorse dati disponibili per analisi e gestione nel sistema ***digna***.

### Uso del comando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argomenti
- **PROJECT_NAME**: Il nome del progetto per il quale si stanno elencando le sorgenti dati (obbligatorio).
  
### Esempio
  
Per elencare tutte le sorgenti dati nel progetto chiamato `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Questo comando fornisce agli utenti una panoramica delle sorgenti dati disponibili in un progetto, aiutandoli a navigare e gestire il panorama dei dati in modo più efficace.
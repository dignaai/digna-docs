---
title: Riferimento CLI digna 2026.06 – Comandi ed esempi | Documentazione digna
description: Riferimento completo per la versione 2026.06 della CLI di digna
image: /assets/logo_square.png
---

# Riferimento CLI digna 2026.06
**2026-09-05**

Questa pagina documenta l'insieme completo dei comandi disponibili nella versione **2026.06** della CLI di ***digna***, inclusi esempi d'uso e opzioni.

L'eseguibile si chiama `digna`.

---

## Nozioni di base sulla CLI

---

### Panoramica e sintassi

La CLI della versione **2026.06** utilizza una gerarchia di comandi strutturata e basata su categorie:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` e `serve` sono comandi singoli, privi di sottocomando:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Opzioni globali

Le seguenti opzioni globali si applicano a tutti i comandi:

- `--help`, `-h`: Mostra le informazioni della guida per la CLI o per una specifica categoria di comandi o sottocomando.
- `--stacktrace`: In caso di errore mostra l'intera catena di errori anziché il solo messaggio di livello superiore.

`--stacktrace` è un'opzione globale in senso stretto: va indicata **prima** della categoria del comando, non dopo.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Non esiste alcun flag `--version`. Utilizzare invece il comando [`version`](#version).

### Prerequisiti

La maggior parte dei comandi richiede un file `config.toml` leggibile e valido; alcuni richiedono inoltre una licenza valida.
La tabella seguente riporta ciò che ogni categoria di comandi carica prima di fare qualsiasi cosa:

| Categoria di comandi | Richiede `config.toml` | Richiede una licenza valida |
|---|---|---|
| `version` | no | no |
| `config check` | no (è proprio ciò su cui il comando riferisce) | no |
| `license check` | no | *è* la verifica stessa |
| `crypt` | sì | no |
| `serve` | sì | no |
| `project` | sì | no |
| `user` | sì | sì |
| `inspection` | sì | sì |
| `repo` | sì | sì |

Dove è richiesta una licenza, vengono verificate sia la sua firma sia la data di scadenza, e il comando si interrompe prima di toccare il repository se una delle due non è valida.

### Codici di uscita

- `0`: il comando è riuscito.
- `1`: il comando è fallito. Il messaggio di errore viene scritto su stderr, preceduto dal prefisso `Error: `.

### help

L'opzione `--help` fornisce informazioni sulle categorie di comandi, sui sottocomandi e sulle opzioni disponibili:

1. **Visualizzazione della guida generale:**
   ```bash
   digna --help
   ```

2. **Ottenere la guida per categorie e comandi specifici:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **L'output include:**
   - **Descrizione del comando:** Sintesi dello scopo del comando.
   - **Sintassi:** Argomenti obbligatori e facoltativi.
   - **Opzioni:** Flag e parametri specifici del comando.

### version

Il comando `version` stampa la versione di ***digna*** installata. Non legge alcuna configurazione e non convalida alcuna licenza, quindi funziona anche su un'installazione il cui `config.toml` o la cui licenza siano mancanti o non validi.

La versione del prodotto è indipendente dalla versione dello schema del repository riportata da [`repo check`](#repo-check).

#### Utilizzo del comando
```bash
digna version
```

#### Esempio di output
```text
2026.06
```

---

## Gestione della configurazione

---

### config check

Il comando `config check` convalida il file di configurazione (`config.toml`), verificando che tutte le sezioni e le impostazioni obbligatorie siano presenti e correttamente formattate. Ogni sezione viene convalidata singolarmente, così una sezione `[app]` danneggiata non nasconde lo stato di `[repo]`.

Le sezioni riportate sono:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — facoltativa; una chiave assente supera il controllo, mentre un elenco presente ma malformato non lo supera

Il comando volutamente non carica la configurazione dell'applicazione come fanno gli altri comandi, così da poter diagnosticare un `config.toml` che impedirebbe a ***digna*** perfino di avviarsi.

#### Utilizzo del comando
```bash
digna config check [OPTIONS]
```

#### Opzioni
- `--configpath`, `-c`: Percorso del file di configurazione o di una directory contenente `config.toml` (predefinito `./config.toml`).
- `--json`: Restituisce il rapporto di convalida in formato JSON. Ha la precedenza su `--quiet`.
- `--quiet`, `-q`: Sopprime il rapporto e si basa esclusivamente sul codice di uscita.

#### Esempio
```bash
digna config check
```

Convalidare un file di configurazione specifico e formattare l'output come JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Esempio di output
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

Un file mancante o un errore di sintassi TOML non lascia nulla da convalidare sezione per sezione e viene segnalato come un singolo errore anziché come un rapporto, indipendentemente da `--quiet` o `--json`.

---

## Gestione del repository

---

### repo check

Il comando `repo check` verifica la connessione al database e controlla l'installazione e la versione del repository. Fallisce se lo schema configurato non esiste, oppure se esiste ma non contiene alcun repository ***digna***.

La versione riportata è quella dello schema del repository, che segue una numerazione separata rispetto alla versione di ***digna*** stampata da [`version`](#version).

#### Utilizzo del comando
```bash
digna repo check
```

#### Esempio di output
```text
Repo version 3.0.0 installed
```

### repo install

Il comando `repo install` installa un nuovo repository ***digna*** nello schema configurato in `config.toml`, creando tutte le sequenze, le tabelle, gli indici, i vincoli e i record iniziali necessari.

Lo schema in sé **non** viene creato da questo comando: deve esistere in precedenza. Il comando si rifiuta inoltre di essere eseguito se in quello schema è già installato un repository, e rimanda a [`repo upgrade`](#repo-upgrade) se la versione installata è precedente.

#### Utilizzo del comando
```bash
digna repo install
```

#### Esempio di output
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Il comando `repo upgrade` applica le migrazioni dello schema del database per portare un repository esistente alla versione attesa dalla release installata. Gli aggiornamenti vengono applicati un salto di versione alla volta lungo un percorso di aggiornamento prestabilito, e ogni salto completato viene registrato nel repository.

Se il repository si trova già alla versione attesa, il comando segnala che non è necessario alcun aggiornamento e non apporta modifiche.

#### Utilizzo del comando
```bash
digna repo upgrade
```

#### Esempio di output
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Gestione della crittografia

---

### crypt gen-key

Il comando `crypt gen-key` genera una nuova chiave di crittografia AES-GCM da utilizzare come chiave di crittografia in `config.toml`. Deve già essere presente un `config.toml` caricabile, anche se la chiave generata non dipende da esso.

#### Utilizzo del comando
```bash
digna crypt gen-key
```

#### Esempio di output
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Il comando `crypt encrypt` cifra una stringa (ad esempio una password di database) utilizzando la chiave AES-GCM configurata in `config.toml` e stampa il testo cifrato.

#### Utilizzo del comando
```bash
digna crypt encrypt <VALUE>
```

#### Argomenti
- **VALUE**: La stringa in chiaro da cifrare (obbligatorio).

#### Esempio
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Il comando `crypt decrypt` decifra una stringa cifrata con AES-GCM utilizzando la chiave configurata in `config.toml` e stampa il testo in chiaro.

#### Utilizzo del comando
```bash
digna crypt decrypt <VALUE>
```

#### Argomenti
- **VALUE**: La stringa cifrata da decifrare (obbligatorio).

#### Esempio
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Gestione degli utenti

---

### user add

Il comando `user add` crea un nuovo account utente nel repository ***digna***. Il comando fallisce se esiste già un utente con l'indirizzo e-mail indicato.

#### Utilizzo del comando
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argomenti
- **EMAIL**: L'indirizzo e-mail dell'utente (obbligatorio).
- **PASSWORD**: La password iniziale dell'utente (obbligatorio).
- **DISPLAY_NAME**: Il nome visualizzato completo dell'utente (obbligatorio).

#### Opzioni
- `--admin`, `-a`: Crea l'utente con privilegi di amministratore (superutente).

#### Esempio
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Per creare un account amministratore:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Esempio di output
```text
User created with ID: 42
```

### user list

Il comando `user list` elenca tutti gli utenti registrati in formato tabellare con ID, e-mail, nome visualizzato e flag di amministratore.

#### Utilizzo del comando
```bash
digna user list
```

#### Esempio di output
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Il comando `user modify` aggiorna il nome visualizzato e i privilegi di amministratore di un account utente esistente, identificato dall'indirizzo e-mail.

Sia il nome visualizzato sia il flag di amministratore vengono sempre scritti. `--admin` è un interruttore, non un valore: **ometterlo revoca i privilegi di amministratore**, quindi indicarlo ogni volta che l'utente deve mantenerli o ottenerli.

#### Utilizzo del comando
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argomenti
- **EMAIL**: L'e-mail dell'utente da modificare (obbligatorio).
- **DISPLAY_NAME**: Il nome visualizzato aggiornato (obbligatorio).

#### Opzioni
- `--admin`, `-a`: Concede i privilegi di amministratore. Ometterlo per revocarli.
- `--valid-until`, `-v`: Accettato per compatibilità ma **attualmente non applicato**. Indicarlo stampa un avviso e non modifica nulla.

#### Esempio
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Esempio di output
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Il comando `user modify-pwd` aggiorna la password di un account utente esistente.

#### Utilizzo del comando
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argomenti
- **EMAIL**: L'e-mail dell'utente di cui aggiornare la password (obbligatorio).
- **PASSWORD**: La nuova password (obbligatorio).

#### Esempio
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Il comando `user delete` rimuove un account utente dal sistema.

#### Utilizzo del comando
```bash
digna user delete <EMAIL>
```

#### Argomenti
- **EMAIL**: L'e-mail dell'utente da eliminare (obbligatorio).

#### Esempio
```bash
digna user delete jdoe@example.com
```

---

## Gestione di progetti e origini dati

---

### project list

Il comando `project list` elenca tutti i progetti disponibili nel repository, mostrandone ID, nome e descrizione.

#### Utilizzo del comando
```bash
digna project list
```

#### Esempio di output
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Il comando `project list-ds` elenca tutte le origini dati associate a un determinato progetto, mostrandone ID, nome, tipo, schema e nome della tabella.

#### Utilizzo del comando
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto di cui elencare le origini dati (obbligatorio). Il nome deve corrispondere esattamente.

#### Esempio
```bash
digna project list-ds ProjectA
```

#### Esempio di output
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Il comando `project export-ds` esporta le origini dati di un progetto in un documento JSON.

Se non viene indicato né `--table-name` né `--table-id`, vengono esportate tutte le origini dati del progetto.

#### Utilizzo del comando
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto da cui esportare le origini dati (obbligatorio).

#### Opzioni
- `--table-name`, `-n`: Nomi delle origini dati da esportare. È possibile indicare più nomi separati da spazi.
- `--table-id`, `-i`: ID delle origini dati da esportare. È possibile indicare più ID separati da spazi.
- `--exportfile`, `-f`: Percorso in cui salvare le origini dati esportate (predefinito: `data_sources_export.json`).

#### Esempio
Per esportare tutte le origini dati da `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Per esportare tabelle specifiche:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Esempio di output
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Il comando `project import-ds` importa le origini dati da un file di esportazione in un progetto di destinazione e riferisce, oggetto per oggetto, cosa è stato creato, aggiornato o ignorato.

#### Utilizzo del comando
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argomenti
- **PROJECT_NAME**: Nome del progetto di destinazione in cui importare (obbligatorio).
- **EXPORT_FILE**: Percorso del file di esportazione JSON (obbligatorio).

#### Opzioni
- `--output-file`, `-o`: File in cui scrivere il rapporto di importazione. Senza di esso, il rapporto viene inviato a stdout.
- `--output-format`, `-f`: Formato del rapporto di importazione — `table`, `json` o `csv` (predefinito: `table`).

#### Esempio
```bash
digna project import-ds ProjectB my_export.json
```

Per ottenere un rapporto leggibile da una macchina:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Il rapporto copre quattro livelli di oggetti — origine dati, definizione del set di dati, attributo e regola di convalida — ciascuno con la relativa azione di importazione, il risultato, l'ID dell'oggetto risultante ed eventuali informazioni aggiuntive.

### project plan-import-ds

Il comando `project plan-import-ds` mostra un'anteprima dell'importazione di origini dati in un progetto di destinazione, indicando quali oggetti verrebbero creati, aggiornati o ignorati, senza modificare nulla. Accetta lo stesso file di esportazione e le stesse opzioni di rapporto di [`project import-ds`](#project-import-ds), e aggiunge un numero di passaggio per ogni oggetto pianificato.

#### Utilizzo del comando
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argomenti
- **PROJECT_NAME**: Nome del progetto di destinazione (obbligatorio).
- **EXPORT_FILE**: Percorso del file di esportazione (obbligatorio).

#### Opzioni
- `--output-file`, `-o`: File in cui scrivere il piano di importazione. Senza di esso, il piano viene inviato a stdout.
- `--output-format`, `-f`: Formato del piano di importazione — `table`, `json` o `csv` (predefinito: `table`).

#### Esempio
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Gestione delle ispezioni

---

### inspection run

Il comando `inspection run` crea una richiesta di ispezione per un progetto e un intervallo di date e poi — a seconda delle opzioni indicate — la attende, restituisce immediatamente il controllo oppure la esegue nel proprio processo.

Le tre modalità di esecuzione sono:

- **Predefinita (senza flag)**: la richiesta viene messa in coda per il backend e la CLI la interroga ogni due secondi, stampando l'avanzamento delle attività finché l'ispezione non raggiunge uno stato finale. È necessario un `digna serve` in esecuzione, altrimenti nessuno preleva la richiesta.
- **`--async-mode`**: la richiesta viene messa in coda e il suo ID viene stampato immediatamente. Utilizzare [`inspection status`](#inspection-status) per seguirla.
- **`--bypass-backend`**: l'ispezione viene eseguita dal processo stesso della CLI e non viene messa in coda, quindi non è necessario alcun server in esecuzione.

`--async-mode` e `--bypass-backend` si escludono a vicenda.

In tutte le modalità il comando termina con un codice di uscita diverso da zero se l'ispezione non si è conclusa correttamente.

#### Utilizzo del comando
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argomenti
- **PROJECT_NAME**: Il nome del progetto di destinazione (obbligatorio). Il nome deve corrispondere esattamente.
- **START_DATE**: Data di inizio dell'intervallo nel formato `YYYY-MM-DD` (obbligatorio).
- **END_DATE**: Data di fine dell'intervallo nel formato `YYYY-MM-DD` (obbligatorio).

#### Opzioni
- `--table-name`: Limita l'ispezione a una sola origine dati del progetto, indicata dal nome dell'origine dati. Senza questa opzione vengono ispezionate tutte le origini dati del progetto.
- `--async-mode`: Mette l'ispezione in coda e stampa l'ID della richiesta anziché attenderla. Non può essere combinata con `--bypass-backend`.
- `--bypass-backend`: Esegue l'ispezione direttamente nel processo della CLI anziché metterla in coda per il backend. Non può essere combinata con `--async-mode`.

#### Esempio
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Per inviare un'ispezione asincrona:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Per ispezionare una sola origine dati:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Esempio di output
Modalità predefinita:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Modalità asincrona:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Il comando `inspection status` interroga lo stato e l'avanzamento delle attività di una richiesta di ispezione a partire dal suo ID.

#### Utilizzo del comando
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argomenti
- **INSPECTION_REQUEST_ID**: L'ID numerico della richiesta di ispezione (obbligatorio).

#### Esempio
```bash
digna inspection status 1024
```

#### Esempio di output
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Il comando `inspection abort` richiede l'annullamento delle richieste di ispezione in esecuzione o in attesa. Registra un evento di arresto per ciascuna richiesta interessata; è il backend ad agire di conseguenza, quindi l'interruzione è una richiesta di arresto e non una terminazione immediata.

#### Utilizzo del comando
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argomenti
- **INSPECTION_REQUEST_ID**: L'ID della richiesta di ispezione da interrompere. Obbligatorio a meno che non venga indicato `--killall`.

#### Opzioni
- `--killall`: Interrompe tutte le richieste di ispezione attualmente in esecuzione e in attesa. Ha la precedenza su un ID di richiesta indicato insieme a essa.

#### Esempio
Per interrompere una richiesta specifica:
```bash
digna inspection abort 1024
```

Per interrompere tutte le ispezioni attive e in coda:
```bash
digna inspection abort --killall
```

#### Esempio di output
`--killall` riferisce cosa ha fatto; l'interruzione di una singola richiesta non produce output e segnala l'esito positivo tramite il proprio codice di uscita.
```text
All running and pending inspections have been aborted.
```

---

## Gestione delle licenze

---

### license check

Il comando `license check` convalida `license.toml`, verificandone la firma rispetto alla chiave pubblica fornita con l'installazione e controllando che non sia scaduta. Non legge alcuna configurazione dell'applicazione, quindi funziona anche prima che `config.toml` sia stato predisposto.

#### Utilizzo del comando
```bash
digna license check
```

#### Esempio di output
```text
License is valid
```

Una firma non valida e una licenza scaduta vengono segnalate come errori distinti, entrambi con codice di uscita 1.

---

## Server e servizi in background

---

### serve

Il comando `serve` avvia il server dell'API REST di ***digna*** insieme allo scheduler delle ispezioni in background e al gestore delle ispezioni. All'avvio, inoltre, fa fallire ogni ispezione che il repository registra ancora come in esecuzione, poiché nulla può essere sopravvissuto a un processo precedente.

Il comando viene eseguito in primo piano finché non viene arrestato.

#### Utilizzo del comando
```bash
digna serve [OPTIONS]
```

#### Opzioni
- `--address`: Indirizzo di rete a cui associare il server dell'API (predefinito: `127.0.0.1`).
- `--port`: Numero della porta su cui rimanere in ascolto (predefinito: `8000`).

#### Esempio
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Esempio di output
```text
Server running on http://0.0.0.0:8000
```

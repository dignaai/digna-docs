# Guida all'Installazione su Windows per digna Release 2026.06

**Release:** 2026.06

**Ultimo Aggiornamento:** 30 agosto 2026


---

## Indice

1. [Introduzione](#introduction)
2. [Requisiti di Sistema](#system-requirements)
3. [Preparazione Pre-Installazione](#pre-installation-setup)
4. [Configurazione del Server PostgreSQL](#postgresql-server-setup)
5. [Configurazione del Web Server](#web-server-configuration)
6. [Installazione Iniziale](#initial-installation)
7. [Configurazione del Backend](#backend-configuration)
8. [Configurazione della Dashboard](#dashboard-configuration)
9. [Eseguire digna come Servizio Windows](#running-digna-as-a-windows-service)
10. [Aggiornamento a una Nuova Release](#upgrading-to-a-new-release)

---

## Introduzione {: #introduction }

### Informazioni su digna

digna è una piattaforma completa basata su AI progettata per ottimizzare la gestione della qualità dei dati in vari ambienti dati come warehouse, lake e lakehouse. Progettata per essere altamente scalabile e adattabile, digna affronta le sfide moderne dei dati tramite automazione, monitoraggio in tempo reale e rilevamento delle anomalie.

digna è composta da due componenti principali:

- **dignabackend**: Il motore centrale dell'applicazione, responsabile dell'elaborazione dei dati e dell'esecuzione dei controlli di qualità.
- **dignadashboard**: Un'interfaccia web ospitata su un web server, che fornisce un modo intuitivo per interagire con la piattaforma digna e visualizzare le metriche di qualità dei dati.

### Novità nella Release 2026.06

Questa release porta funzionalità di osservabilità dei dati direttamente nel tuo codice, permettendo agli sviluppatori di monitorare la qualità dei dati alla fonte. Consulta le [note di rilascio](http://docs.digna.ai/changelog/Release_202606/) per i dettagli completi.

---

## Requisiti di Sistema {: #system-requirements }

Prima di iniziare l'installazione, assicurati che il sistema soddisfi i seguenti requisiti minimi:

| Requisito | Specifica |
|---|---|
| **Sistema Operativo** | Windows Server o Windows 10/11 |
| **Memoria (Installazione Minima)** | 16 GB RAM |
| **Spazio su Disco** | 10 GB di spazio disponibile |
| **Database** | PostgreSQL Server 12 o superiore |
| **Web Server** | IIS, Apache Tomcat o equivalente |

### Opzioni di Installazione del Database

**Se PostgreSQL è già installato:**
Puoi aggiungere un nuovo database per digna al tuo PostgreSQL esistente.

**Se installi PostgreSQL sulla stessa macchina di digna:**

!!! info "Specifiche Consigliate"

    - **Memoria**: 32 GB RAM (invece di 16 GB)
    - **Spazio su Disco**: 50 GB di spazio disponibile (invece di 10 GB)

    Queste specifiche più elevate permettono l'esecuzione simultanea di digna e del database PostgreSQL.

---

## Preparazione Pre-Installazione {: #pre-installation-setup }

Prima di installare digna, assicurati che siano presenti due prerequisiti fondamentali:

1. **Server PostgreSQL** – per memorizzare metriche calcolate e dati sulle prestazioni
2. **Web Server** – per ospitare la Dashboard di digna

Se questi componenti non sono già configurati, segui le sezioni di seguito per installarli e configurarli.

---

## Configurazione del Server PostgreSQL {: #postgresql-server-setup }

### Se Hai già PostgreSQL

Se PostgreSQL è già installato e in esecuzione sulla macchina locale o se stai usando un server PostgreSQL remoto gestito, puoi saltare alla [sezione successiva](#web-server-configuration).

### Installazione di PostgreSQL

Segui questi passaggi per installare PostgreSQL su Windows:

#### Passo 1: Scarica PostgreSQL

1. Visita la [pagina di download di PostgreSQL](https://www.postgresql.org/download/)
2. Seleziona **Windows**
3. Scarica l'installer più recente

#### Passo 2: Esegui l'Installer

1. Fai doppio clic sul file dell'installer scaricato
2. Segui le istruzioni della procedura guidata di installazione

#### Passo 3: Scegli la Directory di Installazione

Seleziona la directory in cui verrà installato PostgreSQL. La posizione predefinita è solitamente appropriata.

#### Passo 4: Seleziona i Componenti

Per un setup standard, mantieni le opzioni dei componenti predefinite selezionate.

#### Passo 5: Imposta la Password del Superutente PostgreSQL

Inserisci e conferma una password per il superutente PostgreSQL (`postgres`). **Conserva questa password in modo sicuro** — ti servirà in seguito.

#### Passo 6: Configura il Numero di Porta

La porta predefinita di PostgreSQL è `5432`. Puoi usare la porta predefinita o specificarne una diversa se necessario.

!!! tip "Suggerimento"

    Se la porta 5432 è già in uso, scegli una porta alternativa e annotala per la configurazione successiva.

#### Passo 7: Scegli il Locale

Seleziona il locale per il database. Il valore predefinito è solitamente adeguato per la maggior parte delle installazioni.

#### Passo 8: Completa l'Installazione

Clicca **Next** nei passaggi rimanenti, quindi clicca **Finish**.

#### Passo 9: Verifica l'Installazione

Apri il Prompt dei comandi e verifica che PostgreSQL sia installato:

```bash
psql --version
```

Dovresti vedere la versione di PostgreSQL se l'installazione è andata a buon fine.

---

## Configurazione del Web Server {: #web-server-configuration }

digna richiede un web server per ospitare la dashboard. Scegli una delle seguenti opzioni:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

È necessario installare e configurare **solo uno** di questi server.

### Configurazione IIS {: #iis-setup }

#### Panoramica

Internet Information Services (IIS) è il web server Microsoft per l'hosting di siti web e applicazioni web.

#### Abilitare IIS

1. **Apri il Pannello di Controllo**
   - Premi `Win + R`
   - Digita `control` e premi Invio

2. **Vai a Funzionalità di Windows**
   - Clicca su **Programmi**
   - Seleziona **Attiva o disattiva funzionalità di Windows**

3. **Abilita Internet Information Services**
   - Scorri e trova **Internet Information Services (IIS)**
   - Seleziona la casella per abilitarlo
   - Clicca il **+** per espandere e verifica che siano selezionati questi sotto-componenti:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Clicca OK** per applicare le modifiche

5. **Verifica l'Installazione di IIS**
   - Apri il browser
   - Vai su `http://localhost`
   - Dovresti vedere la pagina di benvenuto di IIS

#### Obbligatorio: Modulo URL Rewrite

IIS richiede il componente URL Rewrite. Scaricalo e installalo dalla [pagina ufficiale Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Obbligatorio: Tipo MIME per File Markdown

Per garantire che i file Markdown (`.md`) vengano serviti correttamente da IIS:

1. Apri **IIS Manager** (premi `Win + R`, digita `inetmgr`, premi Invio)
2. Naviga in **Il tuo sito > MIME Types**
3. Clicca **Aggiungi...**
4. Configura:
   - **Estensione nome file**: `.md`
   - **Tipo MIME**: `text/markdown`

!!! warning "Importante"

    Senza questa impostazione, i file `.md` potrebbero non essere serviti correttamente.

---

### Configurazione Apache Tomcat {: #apache-tomcat-setup }

#### Panoramica

Apache Tomcat è un contenitore di servlet Java open-source e un web server.

#### Installazione

1. **Scarica Apache Tomcat**
   - Visita [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Scarica la distribuzione ZIP per Windows

2. **Estrai l'Archivio**
   - Estrai il file ZIP in una directory del sistema
   - Esempio: `C:\Program Files\Apache Tomcat`

3. **Verifica che Tomcat sia in Esecuzione**
   - Apri il browser
   - Vai su `http://localhost:8080`
   - Dovresti vedere la pagina di benvenuto di Apache Tomcat

!!! tip "Suggerimento"

    Apache Tomcat di solito si avvia automaticamente dopo l'installazione. Se non lo fa, vai nella cartella `bin` ed esegui `startup.bat`.

---

## Installazione Iniziale {: #initial-installation }

### Passo 1: Configurare il Repository di digna

Il repository digna memorizza tutte le metriche calcolate da digna. Agisce come database centrale per i dati analitici e di performance.

#### Creare lo Schema del Repository e l'Utente

Apri il tuo client PostgreSQL (pgAdmin, psql o simili) ed esegui i seguenti comandi SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Sostituisci i seguenti segnaposto:**

- `<digna_repo_schema>` — Il nome dello schema desiderato (es., `dignarepo`)
- `<digna_repo_user>` — Il nome utente desiderato (es., `digna_user`)
- `<digna_repo_password>` — Una password sicura per questo utente

**Esempio:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Migliore Pratica"

    Usa password forti e complesse per gli utenti del database. Evita credenziali facilmente indovinabili.

---

### Passo 2: Estrarre il Pacchetto di Installazione digna

1. Individua il file ZIP di installazione di digna fornito
2. Estrailo nella posizione di installazione desiderata
3. Dopo l'estrazione, dovresti vedere i seguenti elementi:
   - `dashboard/` — Interfaccia web della dashboard
   - `digna` — Eseguibile principale (backend + CLI combinati)
   - `config.toml` — File di configurazione
   - `license.toml` — File di licenza (copia il tuo qui)

### Passo 3: Installare il File di Licenza

!!! warning "Importante"

    Il file di licenza **non** è incluso nel pacchetto di installazione e verrà fornito separatamente da digna.

1. Individua il file `license.toml` fornito a parte
2. Copialo nella directory principale di installazione di digna (dove si trovano `config.toml` e l'eseguibile `digna`)

**Perché è importante:**
Il file di licenza contiene le informazioni cliente, la data di scadenza della licenza e la firma digitale. **Non modificare questo file** — qualsiasi modifica lo renderà invalido.

**Struttura delle directory dopo la configurazione:**

```
digna_installation/
├── config.toml         (file di configurazione)
├── license.toml        (IL TUO FILE DI LICENZA - copialo qui)
├── digna               (eseguibile principale)
└── dashboard/          (interfaccia web)
    └── (file della dashboard)
```

---

## Configurazione del Backend {: #backend-configuration }

### Passo 1: Creare e Modificare il File di Configurazione

Il file `config_template.toml` è fornito nella directory di installazione di digna. Devi solo rinominarlo in `config.toml`.

**Posizione:** `digna_installation/config.toml`

Apri `config.toml` in un editor di testo e configura ciascuna sezione mostrata di seguito.

#### Sezione [app]

Questa sezione configura le impostazioni dell'applicazione backend di digna:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametro | Valore | Note |
|---|---|---|
| `digna_APP_HOST` | `localhost` o indirizzo IP | Hostname o IP dove è ospitato dignabackend |
| `digna_APP_PORT` | `8082` (default) | Porta per gli endpoint REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL del frontend | Se la dashboard è su un server diverso, includi il suo URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Necessario per CORS con credenziali |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Consenti tutti i metodi HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Consenti tutte le intestazioni |

#### Sezione [repo]

Questa sezione configura la connessione al database PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parametro | Valore | Note |
|---|---|---|
| `digna_REPO_HOST` | `localhost` o IP | Hostname/IP del server PostgreSQL |
| `digna_REPO_PORT` | `5432` (default) | Porta PostgreSQL |
| `digna_REPO_DB` | `postgres` | Nome del database |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema creato in precedenza |
| `digna_REPO_USER` | `digna_user` | Utente creato nella fase di setup PostgreSQL |
| `digna_REPO_PASSWORD` | La tua password | Password impostata durante la creazione dello schema |

#### Sezione [base]

Questa sezione contiene impostazioni di sicurezza e cookie:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parametro | Valore | Note |
|---|---|---|
| `digna_FERNET_KEY` | Chiave di crittografia | Usata per cifrare token e cookie (default fornito) |
| `digna_COOKIE_DOMAIN` | `localhost` | Deve corrispondere al dominio del frontend |
| `digna_COOKIE_SECURE` | `false` (locale) / `true` (produzione) | Usa `true` per connessioni HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Sempre abilitato per sicurezza |
| `digna_COOKIE_SAME_SITE` | `lax` | Previene attacchi CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ore) | Timeout della sessione in secondi |
| `digna_MAX_WORKERS` | Numero di core CPU - 1 | Numero di task di ispezione paralleli |

#### Sezione [logging]

Questa sezione configura il comportamento del logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametro | Valore | Note |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` per produzione, `DEBUG` per troubleshooting |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Numero di backup giornalieri dei log da conservare |

---

### Passo 3: Inizializzare il Repository

1. Apri il Prompt dei comandi
2. Vai nella directory di installazione di digna (dove si trovano `config.toml` e l'eseguibile `digna`)
3. Esegui il test di connessione:

```bash
digna repo check
```

Dovresti vedere una conferma che la connessione è stata stabilita (il repository in sé non è ancora stato inizializzato).

### Passo 4: Installare lo Schema del Repository

Nella stessa directory, esegui:

```bash
digna repo install
```

Questo comando installa le tabelle e lo schema necessari nel tuo database PostgreSQL.

### Passo 5: Avviare il Server digna

Nella directory di installazione di digna, avvia il server con:

```bash
digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — Hostname/IP del server
- `--port` — Porta del server

Dovresti vedere messaggi di avvio che confermano che il server è in esecuzione:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Passo 6: Creare un Utente Admin

1. Apri una finestra del Prompt dei comandi **nuova**
2. Vai nella directory di installazione di digna
3. Esegui il seguente comando per creare un utente admin:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Esempio:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Questo crea un utente con privilegi amministrativi completi.

!!! tip "Migliore Pratica"

    Usa una password forte con una combinazione di maiuscole, minuscole, numeri e caratteri speciali.

---

## Configurazione della Dashboard {: #dashboard-configuration }

### Passo 1: Distribuire la Dashboard sul Web Server

La dashboard di digna ha un proprio file `config.toml` separato situato nella directory `dashboard/`. Questa configurazione è già fornita e non richiede modifiche durante l'installazione iniziale. Devi modificarla solo se è necessario personalizzare la connessione al backend.

Se devi modificare la configurazione della dashboard (es., per deploy multi-istanza), consulta la documentazione della dashboard.

Scegli il tuo web server e segui i relativi passaggi di deployment.

#### Distribuzione su IIS

1. **Apri IIS Manager**
   - Premi `Win + R`, digita `inetmgr`, premi Invio

2. **Crea un Nuovo Sito Web**
   - Nel pannello a sinistra, clicca con il tasto destro su **Siti**
   - Seleziona **Aggiungi sito Web...**

3. **Configura il Sito**
   - **Nome sito**: Inserisci un nome (es., "dignaDashboard")
   - **Percorso fisico**: Clicca Sfoglia e seleziona la cartella `dashboard`
   - **Binding**: Imposta indirizzo IP e porta (porta predefinita 80 per HTTP, 443 per HTTPS)

4. **Avvia il Sito**
   - Clicca **OK** per creare il sito
   - Clicca con il destro sul nuovo sito e seleziona **Avvia**

5. **Testa l'Installazione**
   - Apri il browser
   - Vai su `http://localhost` (o l'URL configurato)
   - Dovresti vedere la pagina di login della dashboard di digna

#### Distribuzione su Apache Tomcat

1. **Copia la Dashboard in Tomcat**
   - Copia la cartella `dashboard` nella directory `webapps` di Tomcat
   - Rinominala se necessario (es., in `digna`)
   - Esempio: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verifica il Deployment**
   - Aggiorna o ricarica la pagina di gestione di Tomcat (http://localhost:8080)
   - Dovresti vedere "digna" (o il nome scelto) elencata nelle applicazioni deployate

3. **Accedi alla Dashboard**
   - Apri il browser
   - Vai su `http://localhost:8080/digna`
   - Dovresti vedere la pagina di login della dashboard di digna

---

## Eseguire digna come Servizio Windows {: #running-digna-as-a-windows-service }

### Perché Usare un Servizio Windows?

Eseguire il backend digna come servizio Windows garantisce che:
- Si avvii automaticamente all'avvio del server
- Giri in background senza una finestra del Prompt dei comandi aperta
- Si riavvii automaticamente in caso di crash
- Può essere gestito tramite i Servizi di Windows

### File di Gestione del Servizio

Tutti i file necessari si trovano nella directory di installazione di digna sotto: `bin/`

I seguenti file batch sono disponibili:
- `install_service.bat` — Registra digna come servizio Windows
- `uninstall_service.bat` — Annulla la registrazione del servizio
- `start_service.bat` — Avvia il servizio
- `stop_service.bat` — Ferma il servizio

!!! warning "Privilegi di Amministratore Richiesti"

    Tutti gli script batch devono essere eseguiti con privilegi di Amministratore.

### Installazione del Servizio

1. **Apri il Prompt dei comandi come Amministratore**
   - Clicca con il tasto destro su Prompt dei comandi
   - Seleziona "Esegui come amministratore"

2. **Vai nella Cartella bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Esegui lo Script di Installazione**
   ```bash
   install_service.bat
   ```

Il server digna è ora registrato come servizio Windows con avvio **automatico** abilitato. Il servizio non viene avviato immediatamente — vedi la sezione successiva per avviarlo.

### Avviare e Fermare il Servizio

#### Per Avviare il Servizio

1. Apri il Prompt dei comandi come Amministratore
2. Vai in `digna\bin`
3. Esegui:
   ```bash
   start_service.bat
   ```

#### Per Fermare il Servizio

1. Apri il Prompt dei comandi come Amministratore
2. Vai in `digna\bin`
3. Esegui:
   ```bash
   stop_service.bat
   ```

!!! tip "Suggerimento"

    Ferma sempre il servizio prima di aggiornare i file dell'applicazione.

### Spostare il Servizio in una Nuova Directory

Se è necessario spostare l'installazione di digna:

1. **Disinstalla il Servizio Corrente**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Sposta i File dell'Applicazione**
   - Sposta l'intera cartella di installazione di digna nella nuova posizione

3. **Reinstalla il Servizio**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Avvia il Servizio**
   ```bash
   start_service.bat
   ```

### Disinstallare il Servizio

1. **Ferma il Servizio in Esecuzione**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Disinstalla il Servizio**
   ```bash
   uninstall_service.bat
   ```

Il server digna è ora stato rimosso come servizio Windows.

---

## Aggiornamento a una Nuova Release {: #upgrading-to-a-new-release }

### Prima di Aggiornare

**È OBBLIGATORIO Creare un Backup del Repository digna**

Prima di aggiornare digna, esegui il backup del tuo repository (PostgreSQL) per proteggerti dalla perdita di dati.
Un backup ti permette di recuperare in caso di problemi durante l'upgrade.

### Processo di Aggiornamento

#### Passo 1: Ferma il Servizio digna

Se digna è in esecuzione come servizio Windows, fermalo prima:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Passo 2: Fai il Backup dell'Installazione Backend Corrente

Nella directory di installazione di digna:

```bash
# Rinomina la cartella contenente dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rinomina la dashboard
ren dashboard dashboard_old
```

#### Passo 3: Estrai e Distribuisci la Nuova Versione

1. Estrai il nuovo file ZIP di installazione di digna
2. Copia il nuovo eseguibile `digna` e la cartella `dashboard` nella directory di installazione

!!! warning "Importante"

    Il file `config.toml` **non** è mai incluso nel file ZIP di installazione. La tua configurazione esistente rimane al sicuro.

### Passo 4: Ripristina i Tuoi File di Configurazione

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Passo 5: Aggiorna lo Schema del Repository

Vai nella directory di installazione di digna ed esegui:

```bash
digna repo upgrade
```

Questo aggiorna lo schema PostgreSQL all'ultima versione preservando tutti i dati esistenti.

### Passo 6: Riavvia i Servizi

Se in esecuzione come servizio Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Se in esecuzione manualmente, riavvia il server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Se usi IIS o Tomcat, riavvia il rispettivo web server.

#### Passo 7: Verifica l'Aggiornamento

1. Accedi alla dashboard di digna
2. Verifica che l'interfaccia si carichi correttamente
3. Controlla i log del server per eventuali errori
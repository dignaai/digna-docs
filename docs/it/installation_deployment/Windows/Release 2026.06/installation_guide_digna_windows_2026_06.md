---
title: Guida all'installazione per Windows – digna Release 2026.06 | Documentazione digna
description: Guida passo passo per l'installazione di digna Release 2026.06 su Windows — requisiti di sistema, configurazione di PostgreSQL, configurazione del web server, configurazione del backend e della dashboard, esecuzione di digna come servizio Windows e aggiornamento a una nuova release.
keywords: digna installazione windows, guida deploy digna, configurazione backend digna, installazione dashboard digna, configurazione postgresql, servizio windows digna, guida aggiornamento digna
image: /assets/logo_square.png
---

# Guida all'installazione per Windows di digna Release 2026.06

**Rilascio:** 2026.06

**Ultimo aggiornamento:** 30 agosto 2026


---

## Indice

1. [Introduzione](#introduction)
2. [Requisiti di sistema](#system-requirements)
3. [Configurazione pre-installazione](#pre-installation-setup)
4. [Configurazione del server PostgreSQL](#postgresql-server-setup)
5. [Configurazione del web server](#web-server-configuration)
6. [Installazione iniziale](#initial-installation)
7. [Configurazione del backend](#backend-configuration)
8. [Configurazione della dashboard](#dashboard-configuration)
9. [Eseguire digna come servizio Windows](#running-digna-as-a-windows-service)
10. [Aggiornamento a una nuova release](#upgrading-to-a-new-release)

---

## Introduzione {: #introduction }

### Informazioni su digna

digna è una piattaforma completa guidata dall'IA progettata per ottimizzare la gestione della qualità dei dati in diversi ambienti dati come warehouse, lake e lakehouse. Progettata per essere altamente scalabile e adattabile, digna affronta le sfide moderne dei dati tramite automazione, monitoraggio in tempo reale e rilevamento delle anomalie.

digna è composta da due componenti principali:

- **digna**: il cuore dell'applicazione, responsabile dell'elaborazione dei dati e dell'esecuzione dei controlli di qualità. Unisce il backend e l'interfaccia a riga di comando in un unico eseguibile, sostituendo i programmi separati `dignabackend` e `dignacli` delle versioni precedenti.
- **dignadashboard**: un'interfaccia web ospitata su un web server, che fornisce un modo user-friendly per interagire con la piattaforma digna e visualizzare le metriche di qualità dei dati.

### Novità nella Release 2026.06

Questa release integra funzionalità di osservabilità dei dati direttamente nel tuo codice, permettendo agli sviluppatori di monitorare la qualità dei dati alla fonte. Vedi le [note di rilascio](http://docs.digna.ai/changelog/Release_202606/) per i dettagli completi.

### Cerchi macOS o Linux?

Questa guida copre Windows. Per altre piattaforme, consulta la [Guida all'installazione per macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) o la [Guida all'installazione per Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Requisiti di sistema {: #system-requirements }

Prima di iniziare l'installazione, assicurati che il sistema soddisfi i seguenti requisiti minimi:

| Requisito | Specifica |
|---|---|
| **Sistema operativo** | Windows Server o Windows 10/11 |
| **Memoria (Installazione minima)** | 16 GB RAM |
| **Spazio su disco** | 10 GB di spazio disponibile |
| **Database** | PostgreSQL Server 12 o superiore |
| **Web Server** | IIS, Apache Tomcat o equivalente |

### Opzioni di installazione del database

**Se PostgreSQL è già installato:**
Puoi aggiungere un nuovo database per digna al tuo server PostgreSQL esistente.

**Se installi PostgreSQL sulla stessa macchina di digna:**

!!! info "Specifiche consigliate"

    - **Memoria**: 32 GB RAM (invece di 16 GB)
    - **Spazio su disco**: 50 GB di spazio disponibile (invece di 10 GB)

    Queste specifiche maggiori consentono l'esecuzione simultanea di digna e del database PostgreSQL.

---

## Configurazione pre-installazione {: #pre-installation-setup }

Prima di installare digna, assicurati che siano presenti due prerequisiti chiave:

1. **Server PostgreSQL** – per memorizzare le metriche calcolate e i dati di performance
2. **Web Server** – per ospitare la digna Dashboard

Se questi componenti non sono già configurati, segui le sezioni seguenti per installarli e configurarli.

---

## Configurazione del server PostgreSQL {: #postgresql-server-setup }

### Se PostgreSQL è già installato

Se PostgreSQL è già installato e in esecuzione sulla tua macchina locale o se stai usando un server PostgreSQL gestito remoto, puoi saltare alla [sezione successiva](#web-server-configuration).

### Installazione di PostgreSQL

Segui questi passaggi per installare PostgreSQL su Windows:

#### Passo 1: Scarica PostgreSQL

1. Visita la [pagina dei download di PostgreSQL](https://www.postgresql.org/download/)
2. Seleziona **Windows**
3. Scarica l'installer più recente

#### Passo 2: Esegui l'Installer

1. Fai doppio clic sul file dell'installer scaricato
2. Segui le istruzioni della procedura guidata di installazione

#### Passo 3: Scegli la directory di installazione

Seleziona la directory in cui verrà installato PostgreSQL. La posizione predefinita è solitamente appropriata.

#### Passo 4: Seleziona i componenti

Per una configurazione standard, mantieni le opzioni dei componenti predefinite selezionate.

#### Passo 5: Imposta la password del superuser PostgreSQL

Inserisci e conferma una password per il superuser PostgreSQL (`postgres`). **Salva questa password in modo sicuro** — ti servirà più avanti.

#### Passo 6: Configura il numero di porta

La porta predefinita di PostgreSQL è `5432`. Puoi usare la porta predefinita o specificarne un'altra se necessario.

!!! tip "Suggerimento"

    Se la porta 5432 è già in uso, scegli una porta alternativa e annotala per la configurazione successiva.

#### Passo 7: Scegli la localizzazione (locale)

Seleziona la localizzazione per il tuo database. La predefinita è generalmente adatta alla maggior parte delle installazioni.

#### Passo 8: Completa l'installazione

Clicca su **Avanti** attraverso le restanti schermate, quindi clicca **Fine**.

#### Passo 9: Verifica l'installazione

Apri il Prompt dei comandi e verifica che PostgreSQL sia installato:

```bash
psql --version
```

Dovresti vedere la versione di PostgreSQL se l'installazione è andata a buon fine.

---

## Configurazione del web server {: #web-server-configuration }

digna richiede un web server per ospitare la dashboard. Scegli una delle seguenti opzioni:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Devi installare e configurare **solo uno** di questi server.

### Configurazione di IIS {: #iis-setup }

#### Panoramica

Internet Information Services (IIS) è il web server di Microsoft per ospitare siti web e applicazioni web.

#### Abilitare IIS

1. **Apri il Pannello di controllo**
   - Premi `Win + R`
   - Digita `control` e premi Invio

2. **Vai a Funzionalità Windows**
   - Clicca **Programmi**
   - Seleziona **Attiva o disattiva funzionalità di Windows**

3. **Abilita Internet Information Services**
   - Scorri verso il basso e trova **Internet Information Services (IIS)**
   - Seleziona la casella per abilitarlo
   - Clicca il **+** per espandere e verifica che questi sottocomponenti siano selezionati:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Clicca OK** per applicare le modifiche

5. **Verifica l'installazione di IIS**
   - Apri il browser
   - Vai a `http://localhost`
   - Dovresti vedere la pagina di benvenuto di IIS

#### Obbligatorio: URL Rewrite Module

IIS richiede il componente URL Rewrite. Scaricalo e installalo dalla [pagina ufficiale Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Obbligatorio: Tipo MIME per i file Markdown

Per assicurare che i file Markdown (`.md`) siano serviti correttamente da IIS:

1. Apri **IIS Manager** (premi `Win + R`, digita `inetmgr`, premi Invio)
2. Vai a **Your Site > MIME Types**
3. Clicca **Add...**
4. Configura:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Importante"

    Senza questa impostazione, i file `.md` potrebbero non essere serviti correttamente.

---

### Configurazione di Apache Tomcat {: #apache-tomcat-setup }

#### Panoramica

Apache Tomcat è un contenitore di servlet Java open-source e un web server.

#### Installazione

1. **Scarica Apache Tomcat**
   - Visita [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Scarica la distribuzione ZIP per Windows

2. **Estrai l'archivio**
   - Estrai il file ZIP in una directory sul tuo sistema
   - Esempio: `C:\Program Files\Apache Tomcat`

3. **Verifica che Tomcat sia in esecuzione**
   - Apri il browser
   - Vai a `http://localhost:8080`
   - Dovresti vedere la pagina di benvenuto di Apache Tomcat

!!! tip "Suggerimento"

    Apache Tomcat di solito si avvia automaticamente dopo l'installazione. Se non lo fa, vai nella cartella `bin` ed esegui `startup.bat`.

---

## Installazione iniziale {: #initial-installation }

### Passo 1: Configura il repository digna

Il repository digna memorizza tutte le metriche calcolate da digna. Funziona come database centrale per dati analitici e di performance.

#### Crea lo schema del repository e l'utente

Apri il client PostgreSQL (pgAdmin, psql o simili) ed esegui i seguenti comandi SQL:

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

!!! tip "Buona pratica"

    Usa password forti e complesse per gli utenti del database. Evita credenziali facilmente indovinabili.

---

### Passo 2: Estrai il pacchetto di installazione di digna

1. Individua il file ZIP di installazione di digna fornito a te
2. Estrailo nella posizione di installazione desiderata
3. Dopo l'estrazione, dovresti vedere i seguenti elementi:
   - `dashboard/` — Interfaccia web della dashboard
   - `digna` — Eseguibile principale (backend + CLI combinati)
   - `config.toml` — File di configurazione
   - `license.toml` — File di licenza (copia il tuo qui)

### Passo 3: Installa il file di licenza

!!! warning "Importante"

    Il file di licenza **non** è incluso nel pacchetto di installazione e verrà fornito separatamente da digna.

1. Individua il file `license.toml` fornito a te
2. Copialo nella directory di installazione principale di digna (dove si trovano `config.toml` e l'eseguibile `digna`)

**Perché è importante:**
Il file di licenza contiene le informazioni del cliente, la data di scadenza della licenza e la firma digitale. **Non modificare questo file** — qualsiasi modifica lo invaliderà.

**Struttura delle directory dopo la configurazione:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Configurazione del backend {: #backend-configuration }

### Passo 1: Crea e modifica il file di configurazione

Il file `config_template.toml` è fornito nella directory di installazione di digna. Devi solo rinominarlo in `config.toml`.

**Posizione:** `digna_installation/config.toml`

Apri `config.toml` in un editor di testo e configura ciascuna sezione descritta di seguito.

#### Sezione [app]

Questa sezione configura le impostazioni dell'applicazione backend di digna:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametro | Valore | Note |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | URL del frontend | Se la dashboard è su un server diverso, includi il suo URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Richiesto per CORS con credenziali |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Consenti tutti i metodi HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Consenti tutti gli header |

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
| `digna_REPO_PORT` | `5432` (predefinito) | Porta di PostgreSQL |
| `digna_REPO_DB` | `postgres` | Nome del database |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema creato in precedenza |
| `digna_REPO_USER` | `digna_user` | Utente creato durante la configurazione di PostgreSQL |
| `digna_REPO_PASSWORD` | La tua password | Password impostata durante la creazione dello schema |

#### Sezione [base]

Questa sezione contiene impostazioni di sicurezza e cookie:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| Parametro | Valore | Note |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Deve corrispondere al dominio del frontend |
| `digna_COOKIE_SECURE` | `false` (locale) / `true` (produzione) | Usa `true` per connessioni HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Sempre abilitato per sicurezza |
| `digna_COOKIE_SAME_SITE` | `lax` | Previene attacchi CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ore) | Timeout della sessione in secondi |
| `digna_MAX_WORKERS` | Numero di core CPU - 1 | Numero di task di ispezione in parallelo |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Ritardo massimo, in secondi, che lo scheduler può aggiungere prima di avviare un'attività in scadenza |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Ora del giorno (formato 24 ore `HH:MM`) in cui parte la pulizia quotidiana |

#### Sezione [encryption]

Questa sezione contiene la chiave usata per cifrare i valori sensibili memorizzati nel repository. È **obbligatoria**: `config check` segnala la sezione `[encryption]` come FAILED se la chiave manca.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametro | Valore | Note |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Chiave codificata in Base64 | Cifra i valori sensibili memorizzati nel repository digna |

!!! warning "Proteggere config.toml"

    Questa chiave è un valore fisso, identico in tutte le installazioni digna, ed è ciò che decifra i valori sensibili del repository. Limitate `config.toml` all'account che esegue digna, tenetelo fuori dal controllo di versione e dalle unità condivise ed escludetelo da qualsiasi backup conservato in modo meno sicuro del repository stesso.

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

### Passo 2: Verificare la configurazione

Prima di inizializzare il repository, verificate che `config.toml` sia completo e ben formato. Nella directory di installazione di digna eseguite:

```bash
digna config check
```

Ogni sezione viene validata singolarmente, così un singolo errore non nasconde lo stato delle altre:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK

Overall: OK
```

Correggete tutto ciò che viene segnalato come FAILED e rieseguite il comando prima di proseguire. L'elenco completo delle opzioni è nel [riferimento CLI](../../../cli/Command_Line_Interface_202606.md).

### Passo 3: Inizializza il repository

1. Apri il Prompt dei comandi
2. Vai nella directory di installazione di digna (dove si trovano `config.toml` e l'eseguibile `digna`)
3. Esegui il test di connessione:

```bash
digna repo check
```

Dovresti vedere una conferma che la connessione è stabilita (il repository vero e proprio non è ancora stato inizializzato).

### Passo 4: Installa lo schema del repository

Nella stessa directory, esegui:

```bash
digna repo install
```

Questo comando installa le tabelle e lo schema necessari nel tuo database PostgreSQL.

### Passo 5: Crea un utente Admin

1. Apri una nuova finestra del Prompt dei comandi
2. Vai nella directory di installazione di digna
3. Esegui il seguente comando per creare un utente amministratore:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Esempio:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Questo crea un utente con pieni privilegi amministrativi.

!!! tip "Buona pratica"

    Usa una password forte con una combinazione di maiuscole, minuscole, numeri e caratteri speciali.

---

### Passo 6: Avvia il server digna

Nella directory di installazione di digna, avvia il server con:

```bash
digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — Hostname/IP del server
- `--port` — Porta del server

Dovresti vedere messaggi di avvio che confermano l'esecuzione del server:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "Il server occupa il terminale"

    `serve` viene eseguito in primo piano e continua finché non lo fermate con ++ctrl+c++. Lasciatelo in esecuzione mentre completate la configurazione; per avviarlo automaticamente all'avvio vedi [Eseguire digna come servizio Windows](#running-digna-as-a-windows-service).

## Configurazione della dashboard {: #dashboard-configuration }

### Passo 1: Distribuisci la dashboard sul web server

La dashboard di digna ha un proprio file `config.toml` separato situato nella directory `dashboard/`. Questa configurazione è già fornita e non richiede modifiche durante l'installazione iniziale. Devi modificarla solo se devi personalizzare la connessione al backend.

Se è necessario modificare la configurazione della dashboard (ad esempio per deployment multi-instance), fai riferimento alla documentazione della dashboard.

Scegli il tuo web server e segui i relativi passaggi di deployment.

#### Distribuzione su IIS

1. **Apri IIS Manager**
   - Premi `Win + R`, digita `inetmgr`, premi Invio

2. **Crea un nuovo sito web**
   - Nel pannello a sinistra, fai clic destro su **Sites**
   - Seleziona **Add Website...**

3. **Configura il sito**
   - **Site Name**: Inserisci un nome (es., "dignaDashboard")
   - **Physical Path**: Clicca Browse e seleziona la cartella `dashboard`
   - **Binding**: Imposta indirizzo IP e porta (porta predefinita 80 per HTTP, 443 per HTTPS)

4. **Avvia il sito**
   - Clicca **OK** per creare il sito
   - Fai clic destro sul nuovo sito e seleziona **Start**

5. **Testa l'installazione**
   - Apri il browser
   - Vai a `http://localhost` (o all'URL configurato)
   - Dovresti vedere la pagina di login della dashboard digna

#### Distribuzione su Apache Tomcat

1. **Copia la dashboard in Tomcat**
   - Copia la cartella `dashboard` nella directory `webapps` di Tomcat
   - Rinominala se necessario (es., in `digna`)
   - Esempio: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verifica il deployment**
   - Aggiorna o ricarica la pagina di gestione di Tomcat (http://localhost:8080)
   - Dovresti vedere "digna" (o il nome scelto) elencata nelle applicazioni deployate

3. **Accedi alla dashboard**
   - Apri il browser
   - Vai a `http://localhost:8080/digna`
   - Dovresti vedere la pagina di login della dashboard digna

---

## Eseguire digna come servizio Windows {: #running-digna-as-a-windows-service }

### Perché utilizzare un servizio di Windows?

Eseguire il backend digna come servizio di Windows garantisce che:
- Si avvii automaticamente all'accensione del server
- Sia in esecuzione in background senza un Prompt dei comandi aperto
- Si riavvii automaticamente in caso di crash
- Possa essere gestito tramite i Servizi di Windows

### File di gestione del servizio

Tutti i file necessari si trovano nella directory di installazione di digna sotto: `bin/`

I seguenti file batch sono disponibili:
- `install_service.bat` — Registra digna come servizio di Windows
- `uninstall_service.bat` — Deregistra il servizio
- `start_service.bat` — Avvia il servizio registrato
- `stop_service.bat` — Ferma il servizio registrato

!!! warning "Amministratore richiesto"

    Tutti i file batch devono essere eseguiti con privilegi di Amministratore.

### Installazione del servizio

1. **Apri il Prompt dei comandi come Amministratore**
   - Fai clic destro su Prompt dei comandi
   - Seleziona "Esegui come amministratore"

2. **Vai nella cartella bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Esegui lo script di installazione**
   ```bash
   install_service.bat
   ```

Il server digna è ora registrato come servizio di Windows con avvio **automatico** abilitato. Il servizio non si avvia immediatamente — vedi la sezione successiva per avviarlo.

### Avviare e fermare il servizio

#### Per avviare il servizio

1. Apri il Prompt dei comandi come Amministratore
2. Vai in `digna\bin`
3. Esegui:
   ```bash
   start_service.bat
   ```

#### Per fermare il servizio

1. Apri il Prompt dei comandi come Amministratore
2. Vai in `digna\bin`
3. Esegui:
   ```bash
   stop_service.bat
   ```

!!! tip "Suggerimento"

    Ferma sempre il servizio prima di aggiornare i file dell'applicazione.

### Spostare il servizio in una nuova directory

Se è necessario spostare l'installazione di digna:

1. **Disinstalla il servizio corrente**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Sposta i file dell'applicazione**
   - Sposta l'intera cartella di installazione digna nella nuova posizione

3. **Reinstalla il servizio**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Avvia il servizio**
   ```bash
   start_service.bat
   ```

### Disinstallare il servizio

1. **Ferma il servizio in esecuzione**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Disinstalla il servizio**
   ```bash
   uninstall_service.bat
   ```

Il server digna è ora deregistrato come servizio di Windows.

---

## Aggiornamento a una nuova release {: #upgrading-to-a-new-release }

### Prima di aggiornare

**Verificate prima tutte le connessioni ai database**

A partire dalla Release 2026.06, digna raggiunge ogni tecnologia sorgente tramite **ODBC**. Le versioni precedenti offrivano la scelta tra un driver specifico per tecnologia e ODBC, selezionata con l'interruttore **Use ODBC**. Il team digna ha deciso di basarsi solo su ODBC, perché un'unica interfaccia standard offre più di un insieme di driver su misura:

- **Autenticazione** — l'autenticazione fa parte di ODBC, quindi una connessione può usare tutto ciò che il suo driver supporta: password, token e PAT, Kerberos e Active Directory, MFA e single sign-on da browser, identità cloud, certificati client e TLS. I nuovi metodi arrivano con un aggiornamento del driver, senza attendere una release di digna.
- **Driver mantenuti dai produttori dei database** — il driver del produttore segue le nuove versioni del server e le correzioni di sicurezza, e potete aggiornarlo secondo i vostri tempi, indipendentemente da digna.
- **Un solo modo di configurare tutto** — ogni tecnologia è un elenco di proprietà chiave/valore, con la stessa interfaccia, la stessa cifratura dei valori sensibili e la stessa diagnostica, invece di un insieme di campi diverso per ogni sorgente.
- **Regolazione e portata** — le opzioni del driver come timeout, impostazioni TLS, proxy e dimensioni di fetch sono disponibili per ogni sorgente, e qualsiasi tecnologia con un driver ODBC conforme può essere collegata, comprese quelle per cui digna non pubblica una guida dedicata.

In pratica questo significa che l'interruttore **Use ODBC** e i campi separati host, porta, database, utente e password non esistono più. **Ogni connessione che non usa già ODBC deve essere convertita a ODBC**: non esiste una conversione automatica, quindi pianificatela prima dell'aggiornamento:

1. Esaminate ogni connessione definita nella vostra installazione e annotate quelle che non usano ancora ODBC: ciascuna dovrà essere riconfigurata.
2. Installate il driver ODBC corrispondente sull'host digna: le connessioni vengono aperte dal server che esegue il backend digna, non dal browser. Vedi [Installare il driver ODBC sull'host digna](../../../databases/overview.md#install-the-driver).
3. Tenete pronte le proprietà ODBC per ogni connessione interessata. Le [guide per tecnologia](../../../databases/overview.md#technology-guides) riportano, per ogni sorgente, un insieme di proprietà collaudato.

Dopo l'aggiornamento, convertite a ODBC ogni connessione interessata e provatela dalla dashboard: vedi [Creare una connessione al database](../../../databases/overview.md#create-a-database-connection) e [Testare una connessione](../../../databases/overview.md#testing-a-connection).

!!! warning "Connessioni Databricks Legacy"

    Il connettore Databricks Legacy è stato rimosso in questa release. Migrate quelle connessioni al connettore [Databricks](../../../databases/databricks_connector_guide.md).

**È obbligatorio creare un backup del repository digna**

Prima di aggiornare digna, esegui il backup del tuo repository (PostgreSQL) per proteggerti da perdita di dati.
Un backup garantisce il recupero in caso di problemi imprevisti durante l'aggiornamento.

### Procedura di aggiornamento

#### Passo 1: Ferma il servizio digna

Se digna è in esecuzione come servizio di Windows, fermalo prima:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Passo 2: Eseguire il backup dell'installazione attuale

Nella directory di installazione di digna, rinominate le cartelle dell'installazione attuale in modo che la nuova release possa essere distribuita accanto a esse:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend e dignacli non sono più utilizzati"

    A partire dalla Release 2026.06, `dignabackend` e `dignacli` sono sostituiti dall'unico eseguibile `digna`, che unisce backend e CLI. Conservate `dignabackend_old` e `dignacli_old` solo finché non avete verificato l'aggiornamento: dopo potete eliminare entrambe le cartelle. Conservate `dashboard_old` finché non avete ripristinato da esso i vostri file di configurazione (vedi passo 4).

#### Passo 3: Estrai e distribuisci la nuova versione

1. Estrai il nuovo file ZIP di installazione di digna
2. Copia il nuovo eseguibile `digna` e la cartella `dashboard` nella directory di installazione

!!! warning "Importante"

    Il file `config.toml` **non** è mai incluso nel file ZIP di installazione. La tua configurazione esistente rimane al sicuro.

#### Passo 4: Ripristina i tuoi file di configurazione

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "La Release 2026.06 modifica config.toml"

    Tre impostazioni sono nuove e obbligatorie, tre non sono più utilizzate. Un `config.toml` ereditato da una versione precedente non contiene le nuove impostazioni e digna non si avvierà finché mancano. Aggiungete quanto segue al vostro `config.toml` esistente:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Aggiungete le due chiavi `[base]` alla vostra sezione `[base]` esistente e aggiungete `[encryption]` come nuova sezione. Poi rimuovete le impostazioni non più utilizzate: **`digna_FERNET_KEY`** da `[base]`, e **`digna_APP_HOST`** e **`digna_APP_PORT`** da `[app]`: il server prende ora indirizzo e porta da `digna serve`.

    Il significato di ogni impostazione è descritto in [Configurazione del backend](#backend-configuration).

!!! warning "Single sign-on: il formato di [oidc_clients] è cambiato"

    La release 2026.06 sostituisce l'array di tabelle con una tabella per ogni provider, denominata in base alla chiave del provider. `DIGNA_OIDC_KEY` non c'è più: la chiave fa ora parte dell'intestazione della sezione.

    Prima:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Dopo:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Ripeti la sezione per ogni provider e mantieni ogni chiave uguale al `key` definito in `dashboard_config.toml`. `digna config check` segnala `oidc_clients` come FAILED finché resta la vecchia forma. Sono interessate solo le installazioni che usano il single sign-on.

#### Passo 5: Verificare la configurazione

Verificate che il `config.toml` aggiornato sia completo prima di toccare il repository:

```bash
digna config check
```

Ogni sezione deve riportare OK. Correggete tutto ciò che viene segnalato come FAILED e rieseguite il comando prima di proseguire.

#### Passo 6: Aggiorna lo schema del repository

Vai nella directory di installazione di digna ed esegui:

```bash
digna repo upgrade
```

Questo aggiorna lo schema PostgreSQL all'ultima versione preservando tutti i dati esistenti.

#### Passo 7: Riavvia i servizi

Se è in esecuzione come servizio di Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Se in esecuzione manualmente, riavvia il server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Se usi IIS o Tomcat, riavvia il relativo web server.

#### Passo 8: Verifica l'aggiornamento

1. Accedi alla dashboard di digna
2. Verifica che l'interfaccia si carichi correttamente
3. Controlla i log del server per eventuali errori
4. Convertite a ODBC ogni connessione che non lo usava ancora, poi testate tutte le connessioni: vedi [Testare una connessione](../../../databases/overview.md#testing-a-connection)
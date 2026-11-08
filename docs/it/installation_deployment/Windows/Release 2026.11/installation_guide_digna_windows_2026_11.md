---
title: Guida all'installazione per Windows – digna Release 2026.11 | Documentazione digna
description: Guida passo passo per l'installazione di digna Release 2026.11 su Windows — requisiti di sistema, configurazione di PostgreSQL, configurazione del web server, configurazione del backend e della dashboard, esecuzione di digna come servizio Windows e aggiornamento dalla Release 2026.06.
keywords: digna installazione windows, guida deploy digna, configurazione backend digna, installazione dashboard digna, configurazione postgresql, servizio windows digna, guida aggiornamento digna
image: /assets/logo_square.png
---

# Guida all'installazione per Windows di digna Release 2026.11

**Rilascio:** 2026.11

**Ultimo aggiornamento:** 7 novembre 2026


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

### Novità nella Release 2026.11

Questa release aggiunge digna Data Reconciliation, digna Agentic con il digna MCP Server e il digna Engine, che può profilare i dati all'interno di digna e verificare l'integrità referenziale tra tecnologie di database diverse. Consulta le [note di rilascio](../../../changelog/Release_202611.md) per i dettagli completi.

Per l'installazione, la release introduce un nuovo meccanismo di migrazione del repository, una sezione facoltativa `[duckdb]` in `config.toml` per il digna Engine e un nuovo file di licenza. La [sezione sull'aggiornamento](#upgrading-to-a-new-release) li tratta uno per uno.

### Cerchi macOS o Linux?

Questa guida copre Windows. Per altre piattaforme, consulta la [Guida all'installazione per macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) o la [Guida all'installazione per Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Le connessioni al database che usano il digna Engine come posizione di profilazione vengono profilate
    direttamente sull'host di digna. Prevedi memoria e spazio su disco aggiuntivi per queste connessioni; vedi la
    [sezione \[duckdb\]](#duckdb-section).

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

!!! info "I file di configurazione e di licenza non sono inclusi nel pacchetto"

    Né `config.toml` né `dashboard/dashboard_config.toml` sono inclusi nell'installazione: li
    create entrambi voi, in [Configurazione del backend](#backend-configuration) e
    [Configurazione della dashboard](#dashboard-configuration). Nemmeno `license.toml` è incluso;
    digna lo fornisce separatamente, come descritto nel Passo 3.

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

Questa sezione configura la condivisione delle risorse tra origini diverse (CORS) tra la dashboard e il backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parametro | Valore | Note |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URL della dashboard | Gli URL da cui viene servita la dashboard. Le richieste del browser provenienti da qualsiasi altra origine vengono rifiutate |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Obbligatorio, affinché il browser invii il cookie di sessione con ogni richiesta |

!!! info "La sezione [app] è facoltativa"

    A partire dalla Release 2026.11, entrambe le chiavi, e l'intera sezione `[app]`, possono essere omesse. È la
    configurazione corretta quando un reverse proxy serve la dashboard e il backend sotto un'unica origine: il
    browser allora non effettua richieste cross-origin, e per impostazione predefinita non ne viene consentita nessuna.

#### Sezione [repo]

Questa sezione configura la connessione al database PostgreSQL:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Parametro | Valore | Note |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` o IP | Hostname/IP del server PostgreSQL |
| `DIGNA_REPO_PORT` | `5432` (predefinito) | Porta di PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Nome del database |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema creato in precedenza |
| `DIGNA_REPO_USER` | `digna_user` | Utente creato durante la configurazione di PostgreSQL |
| `DIGNA_REPO_PASSWORD` | La tua password | Password impostata durante la creazione dello schema |
| `DIGNA_REPO_SSLMODE` | `prefer` (predefinito) | Facoltativo. Modalità SSL di PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` o `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (predefinito) | Facoltativo. Numero di connessioni che digna mantiene aperte verso il repository |

#### Sezione [base]

Questa sezione contiene impostazioni di sicurezza, dei cookie e delle ispezioni:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Parametro | Valore | Note |
|---|---|---|
| `DIGNA_FERNET_KEY` | Valore mostrato sopra | Chiave della cifratura usata dalle release precedenti. Deve essere presente; mantieni il valore mostrato |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host con cui si raggiunge la dashboard. `""` non imposta alcun dominio, che è la scelta giusta dietro un proxy che serve la dashboard e il backend sotto un'unica origine |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Deve essere `true` ogni volta che digna è servito tramite HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Mantiene il cookie di sessione fuori dalla portata degli script |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 ore) | Timeout della sessione in secondi |
| `DIGNA_MAX_WORKERS` | Numero di core CPU - 1 | Numero di ispezioni che possono essere eseguite contemporaneamente |
| `DIGNA_FRONTEND_BASEURL` | URL della dashboard | Obbligatorio. Usato per i link nei messaggi di notifica, quindi deve essere un URL che i destinatari possono aprire |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (predefinito) | Facoltativo. Secondi per cui una singola query su un database di origine può essere eseguita prima di essere interrotta; `0` disattiva il timeout |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (predefinito) | Facoltativo. Secondi di attesa per una connessione a un database di origine; `0` attende indefinitamente |

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
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parametro | Valore | Note |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` per produzione, `DEBUG` per troubleshooting. Sono accettati anche `TRACE`, `WARN` ed `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (predefinito) | Facoltativo. Directory per i file di log a rotazione, relativa alla directory di lavoro |
| `DIGNA_LOGGING_MAX_FILES` | `30` (predefinito) | Facoltativo. Numero di file di log ruotati da conservare |

!!! warning "Mantieni la directory dei log quando digna è eseguito come servizio"

    Un servizio Windows non ha una console, quindi i file di log sono l'unica traccia di ciò che fa il
    servizio. Non impostare `DIGNA_LOGGING_DIR` su una stringa vuota, perché in questo modo i file di log vengono disattivati.

#### Sezione [duckdb] (facoltativa) {: #duckdb-section }

Novità della Release 2026.11. Questa sezione imposta le risorse del **digna Engine**, che profila
i dati all'interno di digna per le connessioni al database la cui posizione di profilazione è **digna Engine**, ed
esegue i controlli di integrità referenziale tra origini dati su connessioni al database diverse. Vedi
[Posizione di profilazione](../../../platform/profiling/profiling_location.md).

La sezione è facoltativa. Senza di essa si applicano i valori predefiniti riportati di seguito.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parametro | Valore | Note |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (predefinito) | Memoria, in MB, che può usare una singola esecuzione del digna Engine. Possono essere attive contemporaneamente fino a `DIGNA_MAX_WORKERS` esecuzioni |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Predefinito: la directory temporanea dell'account che esegue digna (`%TEMP%`) | Directory per i file temporanei quando i dati non entrano in memoria |

!!! tip "Dimensionare il digna Engine"

    Prevedi fino a `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` di memoria sull'host di
    digna, in aggiunta a quella usata da digna stesso, e spazio libero su disco sufficiente nella directory
    temporanea per contenere la data ispezionata più grande delle origini dati che usano il digna Engine.
    Imposta `DIGNA_DUCKDB_TEMP_DIRECTORY` su un disco con questo spazio, scrivibile dall'account che
    esegue digna:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Questa sezione serve solo se almeno una connessione al database usa il digna Engine, o se un
    controllo di integrità referenziale confronta origini dati su connessioni diverse.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Correggete tutto ciò che viene segnalato come FAILED e rieseguite il comando prima di proseguire. Un WARNING sotto **Unknown keys** elenca le chiavi di `config.toml` che digna non legge; non hanno alcun effetto, quindi rimuovetele o correggetene l'ortografia. L'elenco completo delle opzioni è nel [riferimento CLI](../../../cli/Command_Line_Interface_202611.md).

### Passo 3: Inizializza il repository

1. Apri il Prompt dei comandi
2. Vai nella directory di installazione di digna (dove si trovano `config.toml` e l'eseguibile `digna`)
3. Esegui il test di connessione:

```bash
digna repo check
```

Su uno schema nuovo, il comando si connette e poi segnala che non è ancora installato alcun repository:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

A questo punto è il risultato atteso: conferma che digna raggiunge PostgreSQL e lo schema. Un errore di connessione o di autenticazione indica invece un problema nella sezione `[repo]` o nella configurazione di PostgreSQL.

### Passo 4: Installa lo schema del repository

Nella stessa directory, esegui:

```bash
digna repo upgrade
```

Questo comando installa le tabelle necessarie nello schema del repository e termina con:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installa e aggiorna"

    A partire dalla Release 2026.11, `repo upgrade` installa un nuovo repository e aggiorna uno esistente.
    `repo install` funziona ancora come nome alternativo dello stesso comando.

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
- `--address` — Hostname/IP del server (predefinito `127.0.0.1`)
- `--port` — Porta del server (predefinito `8000`)

Quando il server è attivo, stampa l'indirizzo su cui è in ascolto:

```text
Server running on http://127.0.0.1:8082
```

!!! note "Il server occupa il terminale"

    `serve` viene eseguito in primo piano e continua finché non lo fermate con ++ctrl+c++. Lasciatelo in esecuzione mentre completate la configurazione; per avviarlo automaticamente all'avvio vedi [Eseguire digna come servizio Windows](#running-digna-as-a-windows-service).

## Configurazione della dashboard {: #dashboard-configuration }

### Passo 1: Distribuisci la dashboard sul web server

La dashboard digna legge la propria configurazione da `dashboard/dashboard_config.toml`. Questo file non è incluso nell'installazione: lo create nella directory `dashboard/`, insieme ai file della dashboard.

Il suo contenuto è descritto in [Single Sign-On](../../../sso/overview.md), che è anche il punto in cui il file diventa necessario: contiene le opzioni di accesso offerte dalla dashboard e, per i deployment multi-istanza, la connessione al backend.

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

### I comandi `windows`

Il servizio viene gestito dall'eseguibile `digna` stesso, tramite i sottocomandi `digna windows`.
Non ci sono file batch da eseguire.

| Comando | Scopo |
|---|---|
| `digna windows install` | Registra digna come servizio di Windows |
| `digna windows start` | Avvia il servizio registrato |
| `digna windows stop` | Ferma il servizio in esecuzione |
| `digna windows uninstall` | Deregistra il servizio |

!!! warning "Amministratore richiesto"

    Tutti e quattro i comandi devono essere eseguiti da un Prompt dei comandi aperto come Amministratore.

Ogni comando accetta `--name` per indicare un servizio registrato con un nome diverso da quello
predefinito. L'elenco completo delle opzioni si trova nel [riferimento della CLI](../../../cli/Command_Line_Interface_202611.md).

### Installazione del servizio

1. **Apri il Prompt dei comandi come Amministratore**
   - Fai clic destro su Prompt dei comandi
   - Seleziona "Esegui come amministratore"

2. **Vai nella directory di installazione di digna**
   ```bash
   cd C:\path\to\digna
   ```

3. **Registra il servizio**
   ```bash
   digna windows install
   ```

!!! important "Specificate indirizzo e porta, a meno che i valori predefiniti non vadano bene"

    `install` registra l'indirizzo e la porta nella registrazione del servizio, e il servizio si
    mette in ascolto esattamente su quanto registrato. I valori predefiniti sono `127.0.0.1` e
    `8000`, che accettano connessioni solo dalla macchina stessa. Una dashboard su un altro host
    non può raggiungerli, quindi indicate l'indirizzo su cui il backend deve restare in ascolto:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Questi valori non vengono letti da `config.toml`. Per modificarli in seguito, disinstallate il
    servizio e installatelo di nuovo con i nuovi valori.

Il servizio viene registrato con avvio **automatico**, quindi si avvierà insieme a Windows. Non si
avvia immediatamente — vedi la sezione successiva.

#### Opzioni di installazione

| Opzione | Predefinito | Scopo |
|---|---|---|
| `--name` | `digna` | Nome con cui registrare il servizio |
| `--display-name` | `digna` | Nome mostrato in services.msc |
| `--description` | `digna data quality backend` | Descrizione mostrata in services.msc |
| `--address` | `127.0.0.1` | Indirizzo su cui il servizio espone la sua API |
| `--port` | `8000` | Porta su cui il servizio espone la sua API |
| `--working-dir` | la directory dell'eseguibile `digna` | Directory che contiene `config.toml` e `license.toml`, che il servizio usa come directory di lavoro |
| `--start-type` | `auto` | `auto` si avvia con Windows, `manual` si avvia solo su richiesta, `disabled` registra il servizio ma ne impedisce l'avvio |
| `--account` | `LocalSystem` | Account con cui eseguire il servizio, ad es. `DOMAIN\user` o `.\user` |
| `--password` | | Password di `--account` |

!!! tip "Esecuzione con un account di dominio"

    `LocalSystem` non ha un'identità di rete, quindi l'autenticazione di Windows verso SQL Server e
    qualsiasi accesso a una condivisione di rete non riusciranno. Installate con `--account` e
    `--password` quando il servizio deve accedere a risorse come utente specifico.

### Avviare e fermare il servizio

#### Per avviare il servizio

```bash
digna windows start
```

#### Per fermare il servizio

```bash
digna windows stop
```

!!! tip "Suggerimento"

    Ferma sempre il servizio prima di aggiornare i file dell'applicazione.

### Spostare il servizio in una nuova directory

Se è necessario spostare l'installazione di digna:

1. **Ferma e deregistra il servizio corrente**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Sposta i file dell'applicazione**
   - Sposta l'intera cartella di installazione digna nella nuova posizione

3. **Registra di nuovo il servizio dalla nuova posizione**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Ripeti gli eventuali valori di `--address`, `--port` o `--account` usati la prima volta: la
   registrazione precedente non esiste più.

4. **Avvia il servizio**
   ```bash
   digna windows start
   ```

### Disinstallare il servizio

1. **Ferma il servizio in esecuzione**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Deregistra il servizio**
   ```bash
   digna windows uninstall
   ```

Il server digna è ora deregistrato come servizio di Windows.

---

## Aggiornamento a una nuova release {: #upgrading-to-a-new-release }

Questa sezione aggiorna un'installazione della Release 2026.06 alla Release 2026.11.

!!! warning "Aggiornamento da una release precedente alla 2026.06"

    Eseguite prima i passaggi di aggiornamento della Release 2026.06: [Aggiornamento a una nuova release](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). Poi proseguite con i passaggi seguenti.

### Prima di aggiornare

**È obbligatorio creare un backup del repository digna**

Prima di aggiornare digna, esegui il backup del tuo repository (PostgreSQL) per proteggerti da perdita di dati.
Un backup garantisce il recupero in caso di problemi imprevisti durante l'aggiornamento.

**Richiedere il file di licenza per la Release 2026.11**

La Release 2026.11 richiede un nuovo `license.toml`. Richiedetelo al team digna prima di iniziare e
tenetelo pronto per il [passo 7](#step-7-replace-the-license-file).

### Procedura di aggiornamento

#### Passo 1: Ferma il servizio digna {: #step-1-stop-the-digna-service }

Aprite un Prompt dei comandi come amministratore e fermate il servizio con l'eseguibile `digna`
dell'installazione attuale:

```bash
cd C:\path\to\digna
digna windows stop
```

Il servizio resta registrato. Il nuovo eseguibile prende il posto di quello vecchio nella stessa
directory, quindi la registrazione continua a puntare al file corretto.

Se digna è in esecuzione in primo piano, premete ++ctrl+c++ nella sua finestra del Prompt dei comandi.

#### Passo 2: Eseguire il backup dell'installazione attuale {: #step-2-backup-current-installation }

Nella directory di installazione di digna, rinominate l'eseguibile e la cartella della dashboard
dell'installazione attuale, in modo che la nuova release possa essere distribuita accanto a essi:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Conservate `digna_old.exe` finché non avete verificato l'aggiornamento, e `dashboard_old` finché non avete
ripristinato da essa i vostri file di configurazione (vedi passo 4). Dopo potete eliminarli entrambi.

#### Passo 3: Estrai e distribuisci la nuova versione {: #step-3-extract-and-deploy-new-version }

1. Estrai il nuovo file ZIP di installazione di digna
2. Copia il nuovo eseguibile `digna` e la cartella `dashboard` nella directory di installazione

!!! warning "Importante"

    Né `config.toml` né `dashboard/dashboard_config.toml` sono mai inclusi nello ZIP di
    installazione: il team digna non fornisce mai nessuno dei due file. La vostra configurazione
    esistente non viene quindi toccata dall'aggiornamento, e le copie nelle cartelle rinominate
    `*_old` sono le uniche che avete.

#### Passo 4: Ripristina i tuoi file di configurazione {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

La Release 2026.11 non richiede alcuna modifica a `config.toml`: un file che funziona con la Release 2026.06
continua a funzionare. Due modifiche sono facoltative:

- Aggiungete una [sezione `[duckdb]`](#duckdb-section) se le connessioni al database devono usare il digna Engine
  e i suoi valori predefiniti non sono adatti al vostro host.
- Omettete la sezione `[app]` se un reverse proxy serve la dashboard e il backend sotto un'unica
  origine.

!!! warning "Impostazioni che digna non legge"

    Versioni precedenti di questa guida mostravano alcune impostazioni che digna non legge. Non hanno
    alcun effetto, e `config check` le elenca sotto **Unknown keys** nel passo 6. Rimuovetele o
    correggetele:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` e
      `digna_LOGGING_BACKUP_COUNT` non esistono. Rimuovetele.
    - I nomi delle impostazioni distinguono tra maiuscole e minuscole. digna legge `DIGNA_REPO_HOST`, non
      `digna_REPO_HOST`. Scrivete ogni nome in maiuscolo, come in [Configurazione del backend](#backend-configuration).

!!! warning "Single sign-on: mantenete [[oidc_clients]]"

    digna legge i provider di single sign-on come un elenco di voci `[[oidc_clients]]`, ognuna con il proprio
    `DIGNA_OIDC_KEY`. Se avete convertito i vostri provider in sezioni `[oidc_clients.<key>]`, come mostrava
    una versione precedente di questa guida, ripristinate la forma originale. `config check` segnala
    `OIDC config(s)` come FAILED finché quella forma è presente:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Ripetete la voce per ogni provider e mantenete ogni `DIGNA_OIDC_KEY` uguale alla `key` in
    `dashboard_config.toml`. Sono interessate solo le installazioni che usano il single sign-on.

#### Passo 5: Ricaricare il web server {: #step-5-reload-the-web-server }

La dashboard è un insieme di file statici, quindi il web server (e il browser) potrebbe ancora
servire la versione precedente. Ricaricate o riavviate il web server che ospita la cartella
`dashboard`, quindi ricaricate la pagina con un aggiornamento forzato (++ctrl+f5++).

#### Passo 6: Verificare la configurazione {: #step-6-validate-the-configuration }

Verificate che `config.toml` sia completo prima di toccare il repository:

```bash
digna config check
```

Ogni sezione deve riportare OK. Correggete tutto ciò che viene segnalato come FAILED, rimuovete le chiavi
elencate sotto **Unknown keys** e rieseguite il comando prima di proseguire.

#### Passo 7: Sostituire il file di licenza {: #step-7-replace-the-license-file }

Un file di licenza emesso per una release precedente non funziona con la Release 2026.11. Copiate il
`license.toml` che il team digna vi ha fornito per la Release 2026.11 nella directory di
installazione, sostituendo quello vecchio:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Non mantenete la licenza precedente"

    Con la licenza precedente ogni comando che verifica la licenza (`serve`, `user`, `inspection`,
    `repo`) fallisce, quindi digna non si avvia e il repository non può essere aggiornato.
    Verificate la nuova licenza prima di proseguire:

    ```bash
    digna license check
    ```

#### Passo 8: Aggiorna lo schema del repository {: #step-8-upgrade-the-repository-schema }

Nella directory di installazione di digna, eseguite:

```bash
digna repo upgrade
```

La Release 2026.11 gestisce lo schema del repository con migrazioni versionate. Il primo aggiornamento da
una release precedente porta lo schema all'ultima versione del sistema precedente, registra questo stato
come punto di partenza e poi applica le migrazioni della Release 2026.11. Termina con:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Tutti i dati esistenti vengono conservati. Per vedere in qualsiasi momento lo stato del repository, eseguite
`digna repo check`: elenca l'ultima migrazione applicata ed eventuali migrazioni in sospeso.

!!! warning "digna non si avvia su un repository non aggiornato"

    A partire dalla Release 2026.11, il server si rifiuta di avviarsi finché il repository richiede un
    aggiornamento, e lo segnala, ad esempio:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Eseguite `repo upgrade` prima di avviare il server o il servizio.

#### Passo 9: Riavvia i servizi {: #step-9-restart-services }

Se digna è eseguito come servizio Windows, avviatelo di nuovo:

```bash
cd C:\path\to\digna
digna windows start
```

Se digna è eseguito manualmente, riavviate il server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Se usate IIS o Tomcat, riavviate il rispettivo web server.

#### Passo 10: Verifica l'aggiornamento {: #step-10-verify-the-upgrade }

1. Verificate la release del nuovo eseguibile:

    ```bash
    digna version
    ```

    La prima riga deve riportare `Release: 2026.11`.

2. Accedete alla dashboard di digna e verificate che l'interfaccia si carichi correttamente.
3. Controllate i file nella directory `logs` dell'installazione per verificare la presenza di errori.
4. Testate le vostre connessioni al database (vedi
   [Testare una connessione](../../../databases/overview.md#testing-a-connection)).

Per iniziare con i nuovi moduli, consultate [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Collegare un agente IA](../../../platform/agentic/connect_ai_agent.md) per il digna MCP Server e
[Posizione di profilazione](../../../platform/profiling/profiling_location.md) per il digna Engine.

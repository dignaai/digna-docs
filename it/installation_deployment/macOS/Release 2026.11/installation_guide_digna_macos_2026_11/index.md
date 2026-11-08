# Guida all'installazione su macOS per digna Release 2026.11

**Release:** 2026.11

**Ultimo aggiornamento:** 7 novembre 2026


---

## Sommario

1. [Introduzione](#introduction)
2. [Requisiti di sistema](#system-requirements)
3. [Prerequisiti prima dell'installazione](#pre-installation-setup)
4. [Configurazione del server PostgreSQL](#postgresql-server-setup)
5. [Configurazione del web server](#web-server-configuration)
6. [Installazione iniziale](#initial-installation)
7. [Configurazione del backend](#backend-configuration)
8. [Configurazione della dashboard](#dashboard-configuration)
9. [Esecuzione di digna come servizio in background](#running-digna-as-a-background-service)
10. [Aggiornamento a una nuova release](#upgrading-to-a-new-release)

---

## Introduzione {: #introduction }

### Informazioni su digna

digna è una piattaforma completa guidata dall'AI progettata per ottimizzare la gestione della qualità dei dati in diversi ambienti dati come data warehouse, data lake e lakehouse. Progettata per essere altamente scalabile e adattabile, digna affronta le sfide moderne dei dati tramite automazione, monitoraggio in tempo reale e rilevamento di anomalie.

digna è composta da due componenti principali:

- **digna**: il cuore dell'applicazione, responsabile dell'elaborazione dei dati e dell'esecuzione dei controlli di qualità. Unisce il backend e l'interfaccia a riga di comando in un unico eseguibile, sostituendo i programmi separati `dignabackend` e `dignacli` delle versioni precedenti.
- **dignadashboard**: Un'interfaccia web ospitata su un web server, che fornisce un modo intuitivo per interagire con la piattaforma digna e visualizzare le metriche di qualità dei dati.

### Novità nella Release 2026.11

Questa release aggiunge digna Data Reconciliation, digna Agentic con il digna MCP Server e il digna Engine, che può profilare i dati all'interno di digna e verificare l'integrità referenziale tra tecnologie di database diverse. Consulta le [note di rilascio](../../../changelog/Release_202611.md) per i dettagli completi.

Per l'installazione, la release introduce un nuovo meccanismo di migrazione del repository, una sezione facoltativa `[duckdb]` in `config.toml` per il digna Engine e un nuovo file di licenza. La [sezione sull'aggiornamento](#upgrading-to-a-new-release) li tratta uno per uno.

### Cerchi Windows o Linux?

Questa guida copre macOS. Per altre piattaforme, vedi la [Guida all'installazione per Windows](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) o la [Guida all'installazione per Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Requisiti di sistema {: #system-requirements }

Prima di iniziare l'installazione, assicurati che il tuo sistema soddisfi i seguenti requisiti minimi:

| Requisito | Specifica |
|---|---|
| **Sistema operativo** | macOS 13 (Ventura) o successivo |
| **Architettura** | Apple Silicon (arm64) o Intel (x86_64) |
| **Memoria (Configurazione minima)** | 16 GB RAM |
| **Spazio su disco** | 10 GB disponibile |
| **Database** | PostgreSQL Server 12 o superiore |
| **Web Server** | nginx, Apache httpd o equivalente |
| **Strumenti a riga di comando** | Xcode Command Line Tools (richiesti da Homebrew) |

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
    - **Spazio su disco**: 50 GB disponibili (invece di 10 GB)

    Queste specifiche più elevate permettono a digna e al database PostgreSQL di funzionare contemporaneamente senza problemi.

### Verificare l'architettura

Diversi percorsi in questa guida differiscono tra Mac Apple Silicon e Intel. Per verificare quale hai, apri il **Terminale** ed esegui:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew installa in `/opt/homebrew`.
- `x86_64` — Intel. Homebrew installa in `/usr/local`.

!!! tip "Suggerimento"

    Piuttosto che codificare a mano uno dei due percorsi, questa guida usa `$(brew --prefix)`, che si espande nella posizione corretta per entrambe le architetture. Puoi copiare i comandi così come sono.

---

## Prerequisiti prima dell'installazione {: #pre-installation-setup }

Prima di installare digna, assicurati che siano presenti tre prerequisiti chiave:

1. **Homebrew** – il package manager usato per installare i componenti seguenti
2. **Server PostgreSQL** – per memorizzare le metriche calcolate e i dati di performance
3. **Web Server** – per ospitare la Dashboard di digna

Se questi componenti non sono già configurati, segui le sezioni qui sotto per installarli e configurarli.

### Installare Homebrew

Homebrew è il package manager standard per macOS ed è usato in tutta la guida per installare PostgreSQL e nginx.

#### Passo 1: Verificare se Homebrew è già installato

Apri il **Terminale** (premi `Cmd + Space`, digita `Terminal`, premi Invio) ed esegui:

```bash
brew --version
```

Se viene restituito un numero di versione, passa alla sezione [Configurazione del server PostgreSQL](#postgresql-server-setup).

#### Passo 2: Installare Homebrew

Se il comando non è stato trovato, installa Homebrew seguendo le istruzioni sul [sito ufficiale di Homebrew](https://brew.sh). L'installer installa anche gli Xcode Command Line Tools se non sono già presenti.

#### Passo 3: Aggiungere Homebrew al PATH

Su Apple Silicon, l'installer stampa due comandi per aggiungere Homebrew all'ambiente della shell. Eseguili come indicato, poi conferma:

```bash
brew --prefix
```

Questo dovrebbe stampare `/opt/homebrew` su Apple Silicon o `/usr/local` su Intel.

---

## Configurazione del server PostgreSQL {: #postgresql-server-setup }

### Se hai già PostgreSQL

Se PostgreSQL è già installato e in esecuzione sulla tua macchina locale o se stai usando un server PostgreSQL remoto gestito, puoi saltare alla [sezione successiva](#web-server-configuration).

### Opzioni di installazione

macOS offre due modi semplici per installare PostgreSQL. Scegli **uno**:

- [Homebrew](#postgresql-homebrew) — installazione da riga di comando, raccomandata per distribuzioni server
- [Postgres.app](#postgresql-app) — installazione grafica, comoda per valutazioni locali

### Installare PostgreSQL con Homebrew {: #postgresql-homebrew }

#### Passo 1: Installare la formula PostgreSQL

```bash
brew install postgresql@16
```

#### Passo 2: Aggiungere PostgreSQL al PATH

Le formule PostgreSQL versionate sono *keg-only*, il che significa che Homebrew non collega automaticamente i loro comandi nel tuo PATH. Aggiungili manualmente:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Nota"

    Questo presuppone la shell `zsh` predefinita usata da macOS. Se usi `bash`, aggiungi la stessa riga in `~/.bash_profile` invece.

#### Passo 3: Avviare il servizio PostgreSQL

```bash
brew services start postgresql@16
```

Questo avvia PostgreSQL immediatamente e lo configura per l'avvio automatico al login.

#### Passo 4: Verificare l'installazione

```bash
psql --version
```

Dovresti vedere la versione di PostgreSQL se l'installazione ha avuto successo.

#### Passo 5: Collegarsi al server

```bash
psql postgres
```

!!! warning "Importante — macOS è diverso da Windows qui"

    L'installer per Windows ti chiede di creare un superuser `postgres` e una password. Homebrew non lo fa. Invece crea un superuser con il nome del tuo **account macOS**, senza password, raggiungibile solo dalla macchina locale.

    Questo significa che non esiste un ruolo `postgres` su un'installazione Homebrew fresca. Usa il nome del tuo account quando ti serve un superuser e crea un utente digna esplicito come descritto in [Installazione iniziale](#initial-installation).

#### Passo 6: Confermare la porta

La porta predefinita di PostgreSQL è `5432`. Per confermare su quale porta il server è in ascolto:

```bash
psql postgres -c "SHOW port;"
```

Annota il valore — ti servirà quando configurerai il backend di digna.

### Installare PostgreSQL con Postgres.app {: #postgresql-app }

Se preferisci un'installazione grafica:

1. Scarica [Postgres.app](https://postgresapp.com) e trascinalo nella cartella **Applications**
2. Apri l'app e clicca su **Initialize** per creare un nuovo server
3. Segui le istruzioni dell'app per aggiungere gli strumenti da riga di comando al tuo PATH
4. Verifica l'installazione:

```bash
psql --version
```

Postgres.app crea anch'esso un superuser con il nome del tuo account macOS.

---

## Configurazione del web server {: #web-server-configuration }

digna richiede un web server per ospitare la dashboard. Scegli una delle seguenti opzioni:

- [nginx](#nginx-setup) — installato tramite Homebrew, raccomandato
- [Apache httpd](#apache-setup) — incluso con macOS

Devi installare e configurare **solo uno** di questi server.

Entrambe le sezioni configurano due aspetti di cui la dashboard dipende:

- **Fallback per single-page application**, in modo che aggiornare un URL della dashboard non ritorni un 404
- **Tipo MIME per i file `.md`**, in modo che i file Markdown vengano serviti correttamente

### Configurazione di nginx {: #nginx-setup }

#### Panoramica

nginx è un web server leggero e ad alte prestazioni, adatto per servire la dashboard statica di digna.

#### Installazione

```bash
brew install nginx
```

#### Avvio di nginx

```bash
brew services start nginx
```

#### Verificare l'installazione

1. Apri il browser
2. Vai a `http://localhost:8080`
3. Dovresti vedere la pagina di benvenuto di nginx

!!! note "Nota — La porta predefinita è 8080, non 80"

    Homebrew configura nginx per ascoltare sulla porta `8080` in modo che possa essere eseguito senza privilegi di amministratore. Su macOS, legare la porta `80` o qualsiasi porta inferiore a 1024 richiede i privilegi di root.

    Per servire la dashboard sulla porta 80, cambia `listen 8080;` in `listen 80;` nella configurazione sotto e avvia nginx con `sudo brew services start nginx` invece.

#### Configurare un sito per la Dashboard

La configurazione di nginx di Homebrew include ogni file nella directory `servers`. Crea un file di configurazione dedicato per digna lì:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Incolla quanto segue, sostituendo `/path/to/digna/dashboard` con il percorso effettivo alla cartella `dashboard` estratta:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Importante"

    Senza la direttiva `try_files`, ricaricare qualsiasi pagina della dashboard diversa dall'URL root restituisce un 404. Questa è l'equivalente nginx del modulo URL Rewrite richiesto da IIS su Windows.

#### Applicare la configurazione

Testa la configurazione per errori di sintassi, poi ricarica nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Configurazione di Apache httpd {: #apache-setup }

#### Panoramica

macOS include Apache httpd, quindi non è richiesta alcuna installazione. È disabilitato di default.

#### Avviare Apache

```bash
sudo apachectl start
```

#### Verificare l'installazione

1. Apri il browser
2. Vai a `http://localhost`
3. Dovresti vedere il messaggio "It works!"

#### Obbligatorio: Abilitare mod_rewrite

La dashboard richiede la riscrittura degli URL. Apri la configurazione di Apache:

```bash
sudo nano /etc/apache2/httpd.conf
```

Trova la seguente riga e rimuovi il `#` iniziale per decommentarla:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Obbligatorio: Consentire override tramite .htaccess

Nello stesso file, individua il blocco `<Directory "/Library/WebServer/Documents">` e cambia:

```apache
AllowOverride None
```

in:

```apache
AllowOverride All
```

#### Obbligatorio: Tipo MIME per i file Markdown

Sempre in `httpd.conf`, aggiungi la seguente riga in modo che i file Markdown vengano serviti correttamente:

```apache
AddType text/markdown .md
```

!!! warning "Importante"

    Senza questa impostazione, i file `.md` potrebbero non essere serviti correttamente.

#### Applicare la configurazione

Controlla la configurazione per errori di sintassi, poi riavvia Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Installazione iniziale {: #initial-installation }

### Passo 1: Configurare il Repository digna

Il repository digna memorizza tutte le metriche calcolate da digna. Funziona come database centrale per i dati analitici e di performance.

#### Creare lo schema del repository e l'utente

Apri il tuo client PostgreSQL (psql, pgAdmin o simili) ed esegui i seguenti comandi SQL:

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

Per eseguire questi comandi dal Terminale in un unico passaggio:

```bash
psql postgres
```

Poi incolla le istruzioni al prompt `postgres=#` e digita `\q` per uscire.

!!! tip "Buona pratica"

    Usa password forti e complesse per gli utenti del database. Evita credenziali facilmente intuibili.

---

### Passo 2: Estrarre il pacchetto di installazione di digna

1. Individua il file ZIP di installazione di digna fornito
2. Estrailo nella posizione di installazione desiderata — per esempio `/opt/digna` o `~/digna`
3. Dopo l'estrazione dovresti vedere i seguenti elementi:
   - `dashboard/` — Interfaccia web della dashboard
   - `digna` — Eseguibile principale (backend + CLI combinati)

!!! info "I file di configurazione e di licenza non sono inclusi nel pacchetto"

    Né `config.toml` né `dashboard/dashboard_config.toml` sono inclusi nell'installazione: li
    create entrambi voi, in [Configurazione del backend](#backend-configuration) e
    [Configurazione della dashboard](#dashboard-configuration). Nemmeno `license.toml` è incluso;
    digna lo fornisce separatamente, come descritto nel Passo 3.

Per estrarre dal Terminale:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Rendere l'eseguibile eseguibile

A seconda di come è stato trasferito l'archivio, il bit eseguibile potrebbe non essere preservato. Impostalo esplicitamente:

```bash
cd /opt/digna
chmod +x digna
```

#### Se macOS blocca l'applicazione

I file scaricati tramite browser o client di posta sono contrassegnati con un attributo di quarantine. Se macOS segnala che l'app *"non può essere aperta perché lo sviluppatore non può essere verificato"*, rimuovi l'attributo dalla directory di installazione:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

In alternativa, apri **Impostazioni di Sistema → Privacy e sicurezza**, trova l'elemento bloccato verso il fondo della pagina e clicca **Apri comunque**.

!!! note "Nota"

    Questo passaggio è necessario solo se macOS blocca effettivamente l'eseguibile. I pacchetti trasferiti via SSH o tramite condivisioni interne di file di solito non vengono messi in quarantine.

### Passo 3: Installare il file di licenza

!!! warning "Importante"

    Il file di licenza **non** è incluso nel pacchetto di installazione e ti verrà fornito separatamente da digna.

1. Individua il file `license.toml` fornito
2. Copialo nella directory principale di installazione di digna (dove si trovano `config.toml` e l'eseguibile `digna`)

**Perché è importante:**
Il file di licenza contiene le informazioni cliente, la data di scadenza della licenza e la firma digitale. **Non modificare questo file** — qualsiasi modifica lo invaliderà.

**Struttura di directory dopo la configurazione:**

```
/opt/digna/
├── config.toml         (file di configurazione)
├── license.toml        (IL TUO FILE DI LICENZA - copialo qui)
├── digna               (eseguibile principale)
├── bin/                (script per la gestione del servizio)
└── dashboard/          (interfaccia web)
    └── (file della dashboard)
```

---

## Configurazione del backend {: #backend-configuration }

### Passo 1: Creare e modificare il file di configurazione

Il file `config_template.toml` è fornito nella directory di installazione di digna. È sufficiente rinominarlo in `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Posizione:** `/opt/digna/config.toml`

Apri `config.toml` in un editor di testo e configura ciascuna sezione riportata di seguito.

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

!!! note "Nota"

    Se servi la dashboard da nginx di Homebrew sulla porta predefinita, l'origine da consentire è `http://localhost:8080`.

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
| `DIGNA_REPO_PORT` | `5432` (default) | Porta PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Nome del database |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema creato in precedenza |
| `DIGNA_REPO_USER` | `digna_user` | Utente creato nella configurazione PostgreSQL |
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

!!! tip "Suggerimento"

    Per trovare il numero di core CPU disponibili sul tuo Mac, esegui `sysctl -n hw.ncpu`.

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
| `DIGNA_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` per produzione, `DEBUG` per il troubleshooting. Sono accettati anche `TRACE`, `WARN` ed `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (predefinito) | Facoltativo. Directory per i file di log a rotazione, relativa alla directory di lavoro |
| `DIGNA_LOGGING_MAX_FILES` | `30` (predefinito) | Facoltativo. Numero di file di log ruotati da conservare |

#### Sezione [duckdb] (facoltativa) {: #duckdb-section }

Novità della Release 2026.11. Questa sezione imposta le risorse del **digna Engine**, che profila
i dati all'interno di digna per le connessioni al database la cui posizione di profilazione è **digna Engine**, ed
esegue i controlli di integrità referenziale tra origini dati su connessioni al database diverse. Vedi
[Posizione di profilazione](../../../platform/profiling/profiling_location.md).

La sezione è facoltativa. Senza di essa si applicano i valori predefiniti riportati di seguito.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parametro | Valore | Note |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (predefinito) | Memoria, in MB, che può usare una singola esecuzione del digna Engine. Possono essere attive contemporaneamente fino a `DIGNA_MAX_WORKERS` esecuzioni |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Predefinito: la directory temporanea del sistema (`$TMPDIR` dell'account che esegue digna) | Directory per i file temporanei quando i dati non entrano in memoria |

!!! tip "Dimensionare il digna Engine"

    Prevedi fino a `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` di memoria sull'host di
    digna, in aggiunta a quella usata da digna stesso, e spazio libero su disco sufficiente nella directory
    temporanea per contenere la data ispezionata più grande delle origini dati che usano il digna Engine.
    Imposta `DIGNA_DUCKDB_TEMP_DIRECTORY` su un disco con questo spazio, scrivibile dall'account che
    esegue digna:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Questa sezione serve solo se almeno una connessione al database usa il digna Engine, o se un
    controllo di integrità referenziale confronta origini dati su connessioni diverse.

---

### Passo 2: Verificare la configurazione

Prima di inizializzare il repository, verificate che `config.toml` sia completo e ben formato. Nella directory di installazione di digna eseguite:

```bash
./digna config check
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

### Passo 3: Inizializzare il Repository

1. Apri il **Terminale**
2. Vai nella directory di installazione di digna (dove si trovano `config.toml` e l'eseguibile `digna`)
3. Esegui il test di connessione:

```bash
cd /opt/digna
./digna repo check
```

Su uno schema nuovo, il comando si connette e poi segnala che non è ancora installato alcun repository:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

A questo punto è il risultato atteso: conferma che digna raggiunge PostgreSQL e lo schema. Un errore di connessione o di autenticazione indica invece un problema nella sezione `[repo]` o nella configurazione di PostgreSQL.

!!! note "Nota"

    Su macOS, i comandi nella directory corrente non sono nella tua PATH, quindi l'eseguibile viene chiamato come `./digna` anziché `digna`. Per usare la forma più corta ovunque, aggiungi la directory di installazione al tuo PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Passo 4: Installare lo schema del Repository

Nella stessa directory, esegui:

```bash
./digna repo upgrade
```

Questo comando installa le tabelle necessarie nello schema del repository e termina con:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installa e aggiorna"

    A partire dalla Release 2026.11, `repo upgrade` installa un nuovo repository e aggiorna uno esistente.
    `repo install` funziona ancora come nome alternativo dello stesso comando.

### Passo 5: Creare un utente amministratore

1. Apri una nuova finestra del Terminale
2. Vai nella directory di installazione di digna
3. Esegui il seguente comando per creare un utente admin:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Esempio:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Questo crea un utente con l'indirizzo e-mail `admin@example.com` e privilegi amministrativi completi.

!!! tip "Suggerimento"

    Metti la password tra virgolette singole. `zsh` tratta caratteri come `!`, `$` e `*` in modo speciale, e una password non quotata che li contiene non verrà passata correttamente.

!!! tip "Buona pratica"

    Usa una password forte con un mix di maiuscole, minuscole, numeri e caratteri speciali.

---

### Passo 6: Avviare il server digna

Nella directory di installazione di digna, avvia il server con:

```bash
./digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — Hostname/IP del server (predefinito `127.0.0.1`)
- `--port` — Porta del server (predefinito `8000`)

Quando il server è attivo, stampa l'indirizzo su cui è in ascolto:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Suggerimento"

    La prima volta che avvii il server, macOS potrebbe chiederti se vuoi consentire all'applicazione di accettare connessioni di rete in ingresso. Clicca **Allow**, altrimenti la dashboard non potrà raggiungere il backend.

!!! note "Il server occupa il terminale"

    `serve` viene eseguito in primo piano e continua finché non lo fermate con ++ctrl+c++. Lasciatelo in esecuzione mentre completate la configurazione; per avviarlo automaticamente all'avvio vedi [Eseguire digna come servizio in background](#running-digna-as-a-background-service).

## Configurazione della dashboard {: #dashboard-configuration }

### Passo 1: Distribuire la dashboard sul web server

La dashboard digna legge la propria configurazione da `dashboard/dashboard_config.toml`. Questo file non è incluso nell'installazione: lo create nella directory `dashboard/`, insieme ai file della dashboard.

Il suo contenuto è descritto in [Single Sign-On](../../../sso/overview.md), che è anche il punto in cui il file diventa necessario: contiene le opzioni di accesso offerte dalla dashboard e, per i deployment multi-istanza, la connessione al backend.

Scegli il tuo web server e segui i corrispondenti passi di distribuzione.

#### Distribuzione su nginx

Se hai seguito la sezione [nginx Setup](#nginx-setup), il blocco server punta già alla tua cartella `dashboard` ed è quindi inutile copiare i file.

1. **Conferma il percorso**
   - Apri `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Verifica che `root` punti alla cartella `dashboard` estratta

2. **Assicurati che la cartella sia leggibile**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Ricarica nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Test dell'installazione**
   - Apri il browser
   - Vai a `http://localhost:8080` (o all'URL configurato)
   - Dovresti vedere la pagina di login della dashboard di digna

#### Distribuzione su Apache httpd

1. **Copiare la dashboard nella Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Aggiungere le regole di riscrittura**

   Crea un file `.htaccess` nella cartella distribuita in modo che le route della dashboard sopravvivano a un refresh del browser:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Incolla quanto segue:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Riavviare Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Accedere alla Dashboard**
   - Apri il browser
   - Vai a `http://localhost/digna`
   - Dovresti vedere la pagina di login della dashboard di digna

---

## Esecuzione di digna come servizio in background {: #running-digna-as-a-background-service }

### Perché eseguire digna come servizio?

Eseguire il backend digna come servizio in background garantisce che:

- Si avvii automaticamente all'accensione della macchina
- Giri in background senza una finestra Terminale aperta
- Si riavvii automaticamente in caso di crash
- Possa essere gestito tramite `launchctl`, il gestore di servizi di macOS

### File per la gestione del servizio

Tutti i file necessari si trovano nella directory di installazione di digna sotto: `bin/`

Gli script shell disponibili sono:

- `install_service.sh` — Registra digna con launchd
- `uninstall_service.sh` — Annulla la registrazione del servizio
- `start_service.sh` — Avvia il servizio registrato
- `stop_service.sh` — Ferma il servizio in esecuzione

!!! warning "Richiesto l'account amministratore"

    Tutti gli script devono essere eseguiti con `sudo`, perché registrare un servizio che si avvia all'avvio scrive in `/Library/LaunchDaemons`.

### Rendere gli script eseguibili

L'estrazione potrebbe non preservare il bit eseguibile. Prima del primo uso:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Installare il servizio

1. **Apri il Terminale**

2. **Vai nella cartella bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Esegui lo script di installazione**
   ```bash
   sudo ./install_service.sh
   ```

Il server digna è ora registrato con launchd con l'avvio automatico abilitato. Il servizio non parte immediatamente — vedi la sezione successiva per avviarlo.

### Avviare e fermare il servizio

#### Per avviare il servizio

1. Apri il Terminale
2. Vai in `/opt/digna/bin`
3. Esegui:
   ```bash
   sudo ./start_service.sh
   ```

#### Per fermare il servizio

1. Apri il Terminale
2. Vai in `/opt/digna/bin`
3. Esegui:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Suggerimento"

    Ferma sempre il servizio prima di aggiornare i file dell'applicazione.

### Verificare il servizio

Per confermare che il servizio è registrato e in esecuzione:

```bash
sudo launchctl list | grep digna
```

Una riga che inizia con un process ID indica che il servizio è in esecuzione. Un `-` nella prima colonna significa che è registrato ma fermo.

### Spostare il servizio in una nuova directory

launchd memorizza il percorso assoluto dell'eseguibile, quindi spostare l'installazione richiede la registrazione nuovamente del servizio:

1. **Disinstallare il servizio corrente**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Spostare i file dell'applicazione**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Reinstallare il servizio**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Avviare il servizio**
   ```bash
   sudo ./start_service.sh
   ```

### Disinstallare il servizio

1. **Fermare il servizio in esecuzione**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Disinstallare il servizio**
   ```bash
   sudo ./uninstall_service.sh
   ```

Il server digna è ora rimosso dalla registrazione in launchd.

---

## Aggiornamento a una nuova release {: #upgrading-to-a-new-release }

Questa sezione aggiorna un'installazione della Release 2026.06 alla Release 2026.11.

!!! warning "Aggiornamento da una release precedente alla 2026.06"

    Eseguite prima i passaggi di aggiornamento della Release 2026.06: [Aggiornamento a una nuova release](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release). Poi proseguite con i passaggi seguenti.

### Prima di aggiornare

**È OBBLIGATORIO creare un backup del repository digna**

Prima di aggiornare digna, esegui il backup del tuo repository (PostgreSQL) per proteggerti da perdite di dati.
Un backup ti permette di recuperare in caso l'aggiornamento incontri problemi inattesi.

Per creare un backup dal Terminale:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Richiedere il file di licenza per la Release 2026.11**

La Release 2026.11 richiede un nuovo `license.toml`. Richiedetelo al team digna prima di iniziare e
tenetelo pronto per il [passo 7](#step-7-replace-the-license-file).

### Processo di aggiornamento

#### Passo 1: Fermare il servizio digna {: #step-1-stop-the-digna-service }

Se digna è in esecuzione come servizio in background, fermalo prima:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Se digna è in esecuzione in primo piano, premi ++ctrl+c++ nella finestra Terminale in cui è in esecuzione.

#### Passo 2: Eseguire il backup dell'installazione attuale {: #step-2-backup-current-installation }

Nella directory di installazione di digna, rinominate l'eseguibile e la cartella della dashboard
dell'installazione attuale, in modo che la nuova release possa essere distribuita accanto a essi:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Conservate `digna_old` finché non avete verificato l'aggiornamento, e `dashboard_old` finché non avete
ripristinato da essa i vostri file di configurazione (vedi passo 4). Dopo potete eliminarli entrambi.

#### Passo 3: Estrarre e distribuire la nuova versione {: #step-3-extract-and-deploy-new-version }

1. Estrai il nuovo file ZIP di installazione di digna
2. Copia il nuovo eseguibile `digna` e la cartella `dashboard` nella directory di installazione
3. Ripristina il bit eseguibile e, se necessario, rimuovi l'attributo di quarantine:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Importante"

    Né `config.toml` né `dashboard/dashboard_config.toml` sono mai inclusi nello ZIP di
    installazione: il team digna non fornisce mai nessuno dei due file. La vostra configurazione
    esistente non viene quindi toccata dall'aggiornamento, e le copie nelle cartelle rinominate
    `*_old` sono le uniche che avete.

#### Passo 4: Ripristinare i file di configurazione {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
`dashboard`, quindi ricaricate la pagina con un aggiornamento forzato (++cmd+shift+r++).

#### Passo 6: Verificare la configurazione {: #step-6-validate-the-configuration }

Verificate che `config.toml` sia completo prima di toccare il repository:

```bash
./digna config check
```

Ogni sezione deve riportare OK. Correggete tutto ciò che viene segnalato come FAILED, rimuovete le chiavi
elencate sotto **Unknown keys** e rieseguite il comando prima di proseguire.

#### Passo 7: Sostituire il file di licenza {: #step-7-replace-the-license-file }

Un file di licenza emesso per una release precedente non funziona con la Release 2026.11. Copiate il
`license.toml` che il team digna vi ha fornito per la Release 2026.11 nella directory di
installazione, sostituendo quello vecchio:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Non mantenete la licenza precedente"

    Con la licenza precedente ogni comando che verifica la licenza (`serve`, `user`, `inspection`,
    `repo`) fallisce, quindi digna non si avvia e il repository non può essere aggiornato.
    Verificate la nuova licenza prima di proseguire:

    ```bash
    ./digna license check
    ```

#### Passo 8: Aggiornare lo schema del Repository {: #step-8-upgrade-the-repository-schema }

Nella directory di installazione di digna, eseguite:

```bash
cd /opt/digna
./digna repo upgrade
```

La Release 2026.11 gestisce lo schema del repository con migrazioni versionate. Il primo aggiornamento da
una release precedente porta lo schema all'ultima versione del sistema precedente, registra questo stato
come punto di partenza e poi applica le migrazioni della Release 2026.11. Termina con:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Tutti i dati esistenti vengono conservati. Per vedere in qualsiasi momento lo stato del repository, eseguite
`./digna repo check`: elenca l'ultima migrazione applicata ed eventuali migrazioni in sospeso.

!!! warning "digna non si avvia su un repository non aggiornato"

    A partire dalla Release 2026.11, il server si rifiuta di avviarsi finché il repository richiede un
    aggiornamento, e lo segnala, ad esempio:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Eseguite `repo upgrade` prima di avviare il server o il servizio.

#### Passo 9: Riavviare i servizi {: #step-9-restart-services }

Se stai eseguendo digna come servizio in background:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Se lo esegui manualmente, riavvia il server:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Se usi nginx o Apache, riavvia il relativo web server:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Passo 10: Verificare l'aggiornamento {: #step-10-verify-the-upgrade }

1. Verificate la release del nuovo eseguibile:

    ```bash
    ./digna version
    ```

    La prima riga deve riportare `Release: 2026.11`.

2. Accedete alla dashboard di digna e verificate che l'interfaccia si carichi correttamente.
3. Controllate l'output del server e i file nella directory `logs` per verificare la presenza di errori.
4. Testate le vostre connessioni al database (vedi
   [Testare una connessione](../../../databases/overview.md#testing-a-connection)).

Per iniziare con i nuovi moduli, consultate [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Collegare un agente IA](../../../platform/agentic/connect_ai_agent.md) per il digna MCP Server e
[Posizione di profilazione](../../../platform/profiling/profiling_location.md) per il digna Engine.
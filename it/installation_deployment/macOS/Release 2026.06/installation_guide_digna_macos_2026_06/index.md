# Guida all'installazione su macOS per digna Release 2026.06

**Release:** 2026.06

**Ultimo aggiornamento:** 5 settembre 2026


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

- **dignabackend**: Il motore principale dell'applicazione, responsabile dell'elaborazione dei dati e dell'esecuzione dei controlli di qualità.
- **dignadashboard**: Un'interfaccia web ospitata su un web server, che fornisce un modo intuitivo per interagire con la piattaforma digna e visualizzare le metriche di qualità dei dati.

### Novità nella Release 2026.06

Questa release integra funzionalità di data observability direttamente nel tuo codice, permettendo agli sviluppatori di monitorare la qualità dei dati alla fonte. Consulta le [note di rilascio](http://docs.digna.ai/changelog/Release_202606/) per i dettagli completi.

### Cerchi Windows o Linux?

Questa guida copre macOS. Per altre piattaforme, vedi la [Guida all'installazione per Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) o la [Guida all'installazione per Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — File di configurazione
   - `license.toml` — File di licenza (copia qui la tua)

Per estrarre dal Terminale:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
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

Questa sezione configura le impostazioni dell'app backend di digna:

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
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Richiesto per CORS con credenziali |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Consente tutti i metodi HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Consente tutte le intestazioni |

!!! note "Nota"

    Se servi la dashboard da nginx di Homebrew sulla porta predefinita, l'origine da consentire è `http://localhost:8080`.

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
| `digna_REPO_USER` | `digna_user` | Utente creato nella configurazione PostgreSQL |
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
| `digna_FERNET_KEY` | Chiave di crittografia | Usata per criptare token e cookie (fornita di default) |
| `digna_COOKIE_DOMAIN` | `localhost` | Deve corrispondere al dominio del frontend |
| `digna_COOKIE_SECURE` | `false` (locale) / `true` (produzione) | Usa `true` per connessioni HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Sempre abilitato per sicurezza |
| `digna_COOKIE_SAME_SITE` | `lax` | Previene attacchi CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ore) | Timeout della sessione in secondi |
| `digna_MAX_WORKERS` | Numero di core CPU - 1 | Numero di task di ispezione in parallelo |

!!! tip "Suggerimento"

    Per trovare il numero di core CPU disponibili sul tuo Mac, esegui `sysctl -n hw.ncpu`.

#### Sezione [logging]

Questa sezione configura il comportamento del logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametro | Valore | Note |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` per produzione, `DEBUG` per il troubleshooting |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Numero di backup giornalieri dei log da conservare |

---

### Passo 2: Inizializzare il Repository

1. Apri il **Terminale**
2. Vai nella directory di installazione di digna (dove si trovano `config.toml` e l'eseguibile `digna`)
3. Esegui il test di connessione:

```bash
cd /opt/digna
./digna repo check
```

Dovresti vedere una conferma che la connessione è stabilita (il repository in sé non è ancora stato inizializzato).

!!! note "Nota"

    Su macOS, i comandi nella directory corrente non sono nella tua PATH, quindi l'eseguibile viene chiamato come `./digna` anziché `digna`. Per usare la forma più corta ovunque, aggiungi la directory di installazione al tuo PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Passo 3: Installare lo schema del Repository

Nella stessa directory, esegui:

```bash
./digna repo install
```

Questo comando installa le tabelle e lo schema necessari nel tuo database PostgreSQL.

### Passo 4: Avviare il server digna

Nella directory di installazione di digna, avvia il server con:

```bash
./digna serve --address <host> --port <port>
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

!!! tip "Suggerimento"

    La prima volta che avvii il server, macOS potrebbe chiederti se vuoi consentire all'applicazione di accettare connessioni di rete in ingresso. Clicca **Allow**, altrimenti la dashboard non potrà raggiungere il backend.

### Passo 5: Creare un utente amministratore

1. Apri una nuova finestra del Terminale
2. Vai nella directory di installazione di digna
3. Esegui il seguente comando per creare un utente admin:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Esempio:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Questo crea un utente con username `admin` e privilegi amministrativi completi.

!!! tip "Suggerimento"

    Metti la password tra virgolette singole. `zsh` tratta caratteri come `!`, `$` e `*` in modo speciale, e una password non quotata che li contiene non verrà passata correttamente.

!!! tip "Buona pratica"

    Usa una password forte con un mix di maiuscole, minuscole, numeri e caratteri speciali.

---

## Configurazione della dashboard {: #dashboard-configuration }

### Passo 1: Distribuire la dashboard sul web server

La dashboard di digna ha un proprio file `config.toml` separato nella directory `dashboard/`. Questa configurazione è già fornita e non richiede modifiche durante l'installazione iniziale. Devi modificarla solo se è necessario personalizzare la connessione al backend.

Se hai bisogno di modificare la configurazione della dashboard (ad es. per deployment multi-istanza), consulta la documentazione della dashboard.

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

### Prima di aggiornare

**È OBBLIGATORIO creare un backup del repository digna**

Prima di aggiornare digna, esegui il backup del tuo repository (PostgreSQL) per proteggerti da perdite di dati.
Un backup ti permette di recuperare in caso l'aggiornamento incontri problemi inattesi.

Per creare un backup dal Terminale:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Processo di aggiornamento

#### Passo 1: Fermare il servizio digna

Se digna è in esecuzione come servizio in background, fermalo prima:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Se digna è in esecuzione in primo piano, premi `Ctrl + C` nella finestra Terminale in cui è in esecuzione.

#### Passo 2: Eseguire il backup dell'installazione corrente del backend

Nella directory di installazione di digna:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Passo 3: Estrarre e distribuire la nuova versione

1. Estrai il nuovo file ZIP di installazione di digna
2. Copia il nuovo eseguibile `digna` e la cartella `dashboard` nella directory di installazione
3. Ripristina il bit eseguibile e, se necessario, rimuovi l'attributo di quarantine:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Importante"

    Il file `config.toml` **non** è mai incluso nello ZIP di installazione. La tua configurazione esistente rimane al sicuro.

### Passo 4: Ripristinare i file di configurazione

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Passo 5: Aggiornare lo schema del Repository

Vai nella directory di installazione di digna ed esegui:

```bash
cd /opt/digna
./digna repo upgrade
```

Questo aggiorna lo schema PostgreSQL all'ultima versione preservando tutti i dati esistenti.

### Passo 6: Riavviare i servizi

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

#### Passo 7: Verificare l'aggiornamento

1. Accedi alla dashboard di digna
2. Verifica che l'interfaccia venga caricata correttamente
3. Controlla i log del server per eventuali errori
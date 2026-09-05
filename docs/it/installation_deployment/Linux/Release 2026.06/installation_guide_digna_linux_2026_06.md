---
title: Guida all'installazione Linux – digna Release 2026.06 | Documentazione digna
description: Guida passo passo all'installazione di digna Release 2026.06 su Linux — requisiti di sistema, configurazione di PostgreSQL, configurazione di nginx o Apache, configurazione del backend e della dashboard, esecuzione di digna come servizio systemd e aggiornamento a una nuova release.
keywords: guida installazione digna linux, guida deployment digna, configurazione backend digna, installazione dashboard digna, postgresql linux, nginx linux, servizio systemd digna, guida aggiornamento digna
image: /assets/logo_square.png
---

# Guida all'installazione Linux per digna Release 2026.06

**Release:** 2026.06

**Ultimo aggiornamento:** 5 settembre 2026


---

## Indice

1. [Introduzione](#introduction)
2. [Requisiti di sistema](#system-requirements)
3. [Preparazione pre-installazione](#pre-installation-setup)
4. [Configurazione del server PostgreSQL](#postgresql-server-setup)
5. [Configurazione del Web Server](#web-server-configuration)
6. [Installazione iniziale](#initial-installation)
7. [Configurazione del backend](#backend-configuration)
8. [Configurazione della dashboard](#dashboard-configuration)
9. [Eseguire digna come servizio systemd](#running-digna-as-a-systemd-service)
10. [Aggiornamento a una nuova release](#upgrading-to-a-new-release)

---

## Introduzione {: #introduction }

### Informazioni su digna

digna è una piattaforma completa basata su AI progettata per ottimizzare la gestione della qualità dei dati in vari ambienti dati come data warehouse, data lake e lakehouse. Progettata per essere altamente scalabile e adattabile, digna affronta le sfide moderne dei dati tramite automazione, monitoraggio in tempo reale e rilevamento di anomalie.

digna è composta da due componenti principali:

- **dignabackend**: il motore core dell'applicazione, responsabile dell'elaborazione dei dati e dell'esecuzione dei controlli di qualità.
- **dignadashboard**: un'interfaccia web ospitata su un web server, che fornisce un modo user-friendly per interagire con la piattaforma digna e visualizzare le metriche sulla qualità dei dati.

### Novità nella Release 2026.06

Questa release integra capacità di osservabilità dei dati direttamente nel codice, permettendo agli sviluppatori di monitorare la qualità dei dati alla fonte. Vedi le [note di rilascio](http://docs.digna.ai/changelog/Release_202606/) per i dettagli completi.

### Cerchi Windows o macOS?

Questa guida copre Linux. Per altre piattaforme, vedi la [Guida all'installazione per Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) o la [Guida all'installazione per macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

### Quale distribuzione copre questa guida?

Le istruzioni sono scritte per le due famiglie di server più comuni. Dove differiscono, vengono forniti entrambi i comandi:

- **Famiglia Debian** — Debian, Ubuntu. Gestore pacchetti: `apt`.
- **Famiglia RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Gestore pacchetti: `dnf`.

Qualsiasi distribuzione moderna con `systemd` funzionerà; cambiano solo i nomi dei pacchetti e alcuni percorsi di configurazione.

---

## Requisiti di sistema {: #system-requirements }

Prima di iniziare l'installazione, assicurati che il sistema soddisfi i seguenti requisiti minimi:

| Requisito | Specifica |
|---|---|
| **Sistema operativo** | Ubuntu 22.04 LTS o successivo, Debian 12 o successivo, RHEL 9 / Rocky 9 / AlmaLinux 9 o successivo |
| **Architettura** | x86_64 (amd64) o arm64 |
| **Sistema di init** | systemd |
| **Memoria (Installazione minima)** | 16 GB RAM |
| **Spazio su disco** | 10 GB di spazio disponibile |
| **Database** | PostgreSQL Server 12 o superiore |
| **Web Server** | nginx, Apache httpd o equivalente |

### Opzioni di installazione del database

**Se PostgreSQL è già installato:**
Puoi aggiungere un nuovo database per digna al tuo server PostgreSQL esistente.

**Se installi PostgreSQL sulla stessa macchina di digna:**

!!! info "Specifiche consigliate"

    - **Memoria**: 32 GB RAM (invece di 16 GB)
    - **Spazio su disco**: 50 GB di spazio disponibile (invece di 10 GB)

    Queste specifiche maggiori sono consigliate per ospitare contemporaneamente digna e il database PostgreSQL.

### Verifica della distribuzione e dell'architettura

Diversi comandi in questa guida differiscono tra le famiglie Debian e RHEL. Per verificare quale stai usando, esegui:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` o `ID=debian` — usa i comandi `apt`.
- `ID=rhel`, `rocky`, `almalinux` o `fedora` — usa i comandi `dnf`.
- `x86_64` o `aarch64` — l'architettura del pacchetto di installazione di cui hai bisogno.

---

## Preparazione pre-installazione {: #pre-installation-setup }

Prima di installare digna, assicurati che siano presenti due prerequisiti chiave:

1. **Server PostgreSQL** – per memorizzare le metriche calcolate e i dati di performance
2. **Web Server** – per ospitare la digna Dashboard

Se questi componenti non sono già configurati, segui le sezioni sottostanti per installarli e configurarli.

### Aggiornamento dell'indice dei pacchetti

Aggiorna le liste dei pacchetti prima di installare qualsiasi cosa:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Nota"

    In tutta questa guida, il primo comando in una coppia è per la **famiglia Debian** e il secondo per la **famiglia RHEL**. Esegui solo quello che corrisponde al tuo sistema.

---

## Configurazione del server PostgreSQL {: #postgresql-server-setup }

### Se hai già PostgreSQL

Se PostgreSQL è già installato e in esecuzione sulla tua macchina locale o se stai usando un server PostgreSQL gestito remoto, puoi saltare alla [sezione successiva](#web-server-configuration).

### Installazione di PostgreSQL

#### Passo 1: Installa il pacchetto server

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Suggerimento"

    I pacchetti delle distribuzioni possono essere in ritardo rispetto all'ultima release di PostgreSQL. Se hai bisogno di una versione più recente specifica, usa il [repository ufficiale PostgreSQL apt o yum](https://www.postgresql.org/download/linux/).

#### Passo 2: Inizializza il cluster di database

Sulla **famiglia Debian**, il pacchetto crea e avvia automaticamente un cluster — passa al passo successivo.

Sulla **famiglia RHEL**, il cluster deve essere creato esplicitamente:

```bash
sudo postgresql-setup --initdb
```

#### Passo 3: Avvia e abilita il servizio

```bash
sudo systemctl enable --now postgresql
```

Questo avvia PostgreSQL immediatamente e lo configura per avviarsi automaticamente al boot.

#### Passo 4: Verifica l'installazione

```bash
psql --version
sudo systemctl status postgresql
```

Dovresti vedere la versione di PostgreSQL e un servizio `active (running)`.

#### Passo 5: Connettiti al server

Il pacchetto PostgreSQL per Linux crea un account di sistema `postgres` che possiede il cluster. Connettiti tramite quell'account:

```bash
sudo -u postgres psql
```

!!! note "Nota — qui Linux differisce da Windows"

    L'installer di Windows ti chiede di impostare una password per l'utente superuser `postgres` durante l'installazione. I pacchetti Linux no. Le connessioni locali vengono invece autenticate tramite **peer authentication**: l'utente del sistema operativo `postgres` è autorizzato a connettersi come utente del database `postgres` senza password.

    Per questo il comando sopra usa `sudo -u postgres`. Il backend di digna si connette via TCP con username e password, quindi creerai un utente esplicito per digna in [Installazione iniziale](#initial-installation).

#### Passo 6: Conferma la porta

La porta predefinita di PostgreSQL è `5432`. Per confermare su quale porta sta ascoltando il tuo server:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Annota il valore — ti servirà quando configurerai il backend di digna.

#### Passo 7: Abilita l'autenticazione tramite password per l'utente digna

digna si connette a PostgreSQL via TCP come `digna_user`, il che richiede l'autenticazione tramite password invece della peer authentication. Verifica che il tuo `pg_hba.conf` lo permetta.

Individua il file:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Aprilo in un editor e conferma che le righe TCP locali usino `scram-sha-256` (o `md5` su server più vecchi) invece di `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Ricarica PostgreSQL dopo ogni modifica:

```bash
sudo systemctl reload postgresql
```

!!! warning "Importante"

    Se digna riporta `FATAL: Ident authentication failed for user "digna_user"`, questa impostazione è la causa.

#### Passo 8: Se PostgreSQL è su un'altra macchina

Per accettare connessioni da un host diverso, imposta `listen_addresses` in `postgresql.conf` e aggiungi una riga `host` corrispondente per la tua rete in `pg_hba.conf`:

```
listen_addresses = '*'
```

Poi apri la porta nel firewall e riavvia il servizio:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Configurazione del Web Server {: #web-server-configuration }

digna richiede un web server per ospitare la dashboard. Scegli una delle seguenti opzioni:

- [nginx](#nginx-setup) — leggero e raccomandato
- [Apache httpd](#apache-setup) — alternativa ampiamente diffusa

È necessario installare e configurare **solo uno** di questi server.

Entrambe le sezioni configurano due elementi di cui la dashboard dipende:

- **Un fallback per single-page-application**, in modo che aggiornando un URL della dashboard non venga restituito un 404
- **Un tipo MIME per i file `.md`**, in modo che i file Markdown siano serviti correttamente

### Configurazione di nginx {: #nginx-setup }

#### Panoramica

nginx è un web server leggero e ad alte prestazioni adatto a servire la dashboard statica di digna.

#### Installazione

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Avvio di nginx

```bash
sudo systemctl enable --now nginx
```

#### Verifica dell'installazione

1. Apri il browser
2. Vai su `http://localhost`
3. Dovresti vedere la pagina di benvenuto di nginx

#### Apertura del firewall

Se il server è raggiunto da altre macchine, consenti il traffico HTTP:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Configurazione di un sito per la dashboard

nginx carica ogni file nella sua directory `conf.d` su entrambe le famiglie di distribuzioni. Crea un file di configurazione dedicato per digna lì:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Incolla il seguente contenuto, sostituendo `/opt/digna/dashboard` con il percorso effettivo alla cartella estratta `dashboard`:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

    Senza la direttiva `try_files`, ricaricare qualsiasi pagina della dashboard diversa dall'URL root restituirà un 404. Questa è l'equivalente nginx del modulo URL Rewrite richiesto da IIS su Windows.

#### Disabilita il sito di default

Solo un blocco server può essere `default_server` per una porta. Sulla **famiglia Debian**, rimuovi il sito preconfezionato per evitare conflitti:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

Sulla **famiglia RHEL**, commenta o elimina il blocco `server { ... }` dentro `/etc/nginx/nginx.conf`.

#### Applica la configurazione

Testa la configurazione per errori di sintassi, poi ricarica nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Configurazione di Apache httpd {: #apache-setup }

#### Panoramica

Apache httpd è disponibile nei repository predefiniti di tutte le distribuzioni supportate. Il pacchetto si chiama `apache2` sulla famiglia Debian e `httpd` sulla famiglia RHEL.

#### Installazione

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Avvio di Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Verifica dell'installazione

1. Apri il browser
2. Vai su `http://localhost`
3. Dovresti vedere la pagina di default di Apache della distribuzione

#### Obbligatorio: abilitare mod_rewrite

La dashboard richiede il rewrite degli URL.

Sulla **famiglia Debian**, abilita il modulo e riavvia:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

Sulla **famiglia RHEL**, `mod_rewrite` è caricato di default. Confermalo:

```bash
httpd -M | grep rewrite
```

#### Obbligatorio: consentire override con .htaccess

Apri il file di configurazione per la tua document root:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Individua il blocco `<Directory>` che copre la tua document root (`/var/www/html` in entrambe le famiglie) e cambia:

```apache
AllowOverride None
```

in:

```apache
AllowOverride All
```

#### Obbligatorio: tipo MIME per file Markdown

Nello stesso file, aggiungi la seguente riga in modo che i file Markdown siano serviti correttamente:

```apache
AddType text/markdown .md
```

!!! warning "Importante"

    Senza questa impostazione, i file `.md` potrebbero non essere serviti correttamente.

#### Applica la configurazione

Controlla la configurazione per errori di sintassi, poi riavvia Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Installazione iniziale {: #initial-installation }

### Passo 1: Configurare il repository digna

Il repository digna memorizza tutte le metriche calcolate da digna. Funziona come database centrale per dati analitici e di performance.

#### Crea lo schema e l'utente del repository

Apri il client PostgreSQL (psql, pgAdmin o simili) ed esegui i seguenti comandi SQL:

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

Per eseguirli dalla shell in un unico passaggio:

```bash
sudo -u postgres psql
```

Poi incolla le istruzioni al prompt `postgres=#` e digita `\q` per uscire.

!!! tip "Buona pratica"

    Usa password forti e complesse per gli utenti del database. Evita credenziali facilmente indovinabili.

---

### Passo 2: Estrai il pacchetto di installazione digna

1. Individua il file ZIP di installazione di digna che ti è stato fornito
2. Estrai il contenuto nella posizione di installazione desiderata — ad esempio `/opt/digna`
3. Dopo l'estrazione, dovresti vedere i seguenti elementi:
   - `dashboard/` — Interfaccia web della dashboard
   - `digna` — Eseguibile principale (backend + CLI combinati)
   - `config.toml` — File di configurazione
   - `license.toml` — File di licenza (copia il tuo qui)

Per estrarre da shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Nota"

    Se `unzip` non è installato, aggiungilo con `sudo apt install -y unzip` o `sudo dnf install -y unzip`.

#### Rendi eseguibile l'eseguibile

A seconda di come è stato trasferito l'archivio, il bit eseguibile potrebbe non essere preservato. Impostalo esplicitamente:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Crea un account di servizio

È consigliabile eseguire il backend come utente non privilegiato dedicato per le distribuzioni di produzione:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Nota"

    Sulla famiglia RHEL il percorso della shell equivalente è `/sbin/nologin`.

### Passo 3: Installa il file di licenza

!!! warning "Importante"

    Il file di licenza **non** è incluso nel pacchetto di installazione e ti sarà fornito separatamente da digna.

1. Individua il file `license.toml` che ti è stato fornito
2. Copialo nella directory radice di installazione di digna (dove si trovano `config.toml` e l'eseguibile `digna`)

**Perché è importante:**
Il file di licenza contiene le informazioni cliente, la data di scadenza della licenza e la firma digitale. **Non modificare questo file** — qualsiasi modifica lo renderà invalido.

**Struttura della directory dopo la configurazione:**

```
/opt/digna/
├── config.toml         (file di configurazione)
├── license.toml        (IL TUO FILE DI LICENZA - copia qui)
├── digna               (eseguibile principale)
├── bin/                (script di gestione del servizio)
└── dashboard/          (interfaccia web)
    └── (file della dashboard)
```

---

## Configurazione del backend {: #backend-configuration }

### Passo 1: Crea e modifica il file di configurazione

Il file `config_template.toml` è fornito nella directory di installazione di digna. Devi solo rinominarlo in `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Posizione:** `/opt/digna/config.toml`

Apri `config.toml` in un editor di testo e configura ogni sezione descritta di seguito.

#### Sezione [app]

Questa sezione configura le impostazioni dell'applicazione backend digna:

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
| `digna_APP_PORT` | `8082` (predefinito) | Porta per gli endpoint REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL del frontend | Se la dashboard è su un server differente, includi il suo URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Necessario per CORS con credenziali |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Permette tutti i metodi HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Permette tutte le intestazioni |

!!! note "Nota"

    Se servi la dashboard da nginx o Apache sulla porta HTTP predefinita, l'origine da consentire è `http://localhost` — o l'URL pubblico del server se la dashboard è raggiunta da altre macchine.

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
| `digna_REPO_PORT` | `5432` (predefinito) | Porta PostgreSQL |
| `digna_REPO_DB` | `postgres` | Nome del database |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema creato in precedenza |
| `digna_REPO_USER` | `digna_user` | Utente creato nella configurazione PostgreSQL |
| `digna_REPO_PASSWORD` | La tua password | Password impostata durante la creazione dello schema |

!!! tip "Buona pratica"

    `config.toml` contiene la password del database in testo chiaro. Restringi i permessi in modo che solo l'account di servizio possa leggerlo:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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
| `digna_FERNET_KEY` | Chiave di crittografia | Usata per criptare token e cookie (default fornito) |
| `digna_COOKIE_DOMAIN` | `localhost` | Deve corrispondere al dominio del frontend |
| `digna_COOKIE_SECURE` | `false` (locale) / `true` (produzione) | Usa `true` per connessioni HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Sempre abilitato per sicurezza |
| `digna_COOKIE_SAME_SITE` | `lax` | Previene attacchi CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ore) | Timeout della sessione in secondi |
| `digna_MAX_WORKERS` | Numero di core CPU - 1 | Numero di task di ispezione paralleli |

!!! tip "Suggerimento"

    Per trovare il numero di core CPU disponibili sul server, esegui `nproc`.

#### Sezione [logging]

Questa sezione configura il comportamento del logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametro | Valore | Note |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` per la produzione, `DEBUG` per il troubleshooting |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Numero di backup giornalieri dei log da conservare |

---

### Passo 2: Inizializza il repository

1. Apri un terminale
2. Vai nella directory di installazione di digna (dove si trovano `config.toml` e l'eseguibile `digna`)
3. Esegui il test di connessione:

```bash
cd /opt/digna
./digna repo check
```

Dovresti vedere una conferma che la connessione è stabilita (il repository stesso non è ancora stato inizializzato).

!!! note "Nota"

    Su Linux, la directory corrente non è sulla PATH, quindi l'eseguibile viene invocato come `./digna` invece di `digna`. Per usare la forma più breve ovunque, aggiungi un link simbolico:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Passo 3: Installa lo schema del repository

Nella stessa directory, esegui:

```bash
./digna repo install
```

Questo comando installa le tabelle e lo schema necessari nel tuo database PostgreSQL.

### Passo 4: Avvia il server digna

Nella directory di installazione digna, avvia il server con:

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

    Se la dashboard è servita da una macchina diversa rispetto al backend, apri anche la porta API nel firewall:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Passo 5: Crea un utente admin

1. Apri una nuova finestra del terminale
2. Vai nella directory di installazione digna
3. Esegui il seguente comando per creare un utente amministratore:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Esempio:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Questo crea un utente con username `admin` e privilegi amministrativi completi.

!!! tip "Suggerimento"

    Racchiudi la password tra virgolette singole. `bash` e `zsh` trattano caratteri come `!`, `$` e `*` in modo speciale, e una password non quotata che li contiene non sarà passata così come digitata.

!!! tip "Buona pratica"

    Usa una password forte con una combinazione di maiuscole, minuscole, numeri e caratteri speciali.

---

## Configurazione della dashboard {: #dashboard-configuration }

### Passo 1: Distribuisci la dashboard sul Web Server

La dashboard digna ha un proprio file `config.toml` separato nella directory `dashboard/`. Questa configurazione è già fornita e di solito non richiede modifiche durante l'installazione iniziale. Devi modificarla solo se vuoi personalizzare la connessione al backend.

Se devi modificare la configurazione della dashboard (es., per deployment multi-istanza), fai riferimento alla documentazione della dashboard.

Scegli il tuo web server e segui i passaggi di deployment corrispondenti.

#### Distribuzione su nginx

Se hai seguito la sezione [nginx Setup](#nginx-setup), il blocco server punta già alla tua cartella `dashboard` ed è quindi inutile copiare i file.

1. **Conferma il percorso**
   - Apri `/etc/nginx/conf.d/digna.conf`
   - Verifica che `root` punti alla cartella `dashboard` estratta

2. **Assicurati che la cartella sia leggibile**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Ricarica nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Testa l'installazione**
   - Apri il browser
   - Vai su `http://localhost` (o sull'URL configurato)
   - Dovresti vedere la pagina di login della dashboard digna

#### Distribuzione su Apache httpd

1. **Copia la dashboard nella document root**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Aggiungi le regole di rewrite**

   Crea un file `.htaccess` all'interno della cartella distribuita in modo che le route della dashboard sopravvivano a un refresh del browser:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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

3. **Riavvia Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Accedi alla dashboard**
   - Apri il browser
   - Vai su `http://localhost/digna`
   - Dovresti vedere la pagina di login della dashboard digna

### Passo 2: SELinux (solo famiglia RHEL)

Su RHEL, Rocky, AlmaLinux e Fedora, SELinux è in modalità enforcing di default e bloccherà il web server dal leggere file al di fuori delle posizioni previste. Verifica se è attivo:

```bash
getenforce
```

Se il risultato è `Enforcing` e stai servendo la dashboard da `/opt/digna/dashboard`, etichetta la directory in modo che il web server possa leggerla:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Nota"

    Se `semanage` non è presente, installalo con `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Importante"

    Una dashboard che restituisce **403 Forbidden** su un server RHEL appena configurato è quasi sempre un problema di etichettatura SELinux piuttosto che di permessi sui file. Verifica con `sudo ausearch -m avc -ts recent`.

---

## Eseguire digna come servizio systemd {: #running-digna-as-a-systemd-service }

### Perché eseguire digna come servizio?

Eseguire il backend digna come servizio systemd garantisce che:

- Si avvii automaticamente all'accensione della macchina
- Giri in background senza una finestra di terminale aperta
- Si riavvii automaticamente in caso di crash
- Possa essere gestito tramite `systemctl`, il gestore servizi standard di Linux

### File di gestione del servizio

Tutti i file necessari sono nella directory di installazione digna sotto: `bin/`

Gli script shell disponibili sono:

- `install_service.sh` — registra digna con systemd
- `uninstall_service.sh` — deregistra il servizio
- `start_service.sh` — avvia il servizio registrato
- `stop_service.sh` — ferma il servizio in esecuzione

!!! warning "Privilegi di root richiesti"

    Tutti gli script devono essere eseguiti con `sudo`, perché la registrazione di un servizio che parte all'avvio scrive un file di unità in `/etc/systemd/system`.

### Rendi eseguibili gli script

L'estrazione potrebbe non preservare il bit eseguibile. Prima del primo utilizzo:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Installazione del servizio

1. **Apri un terminale**

2. **Vai nella cartella bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Esegui lo script di installazione**
   ```bash
   sudo ./install_service.sh
   ```

Il server digna è ora registrato in systemd con l'avvio automatico abilitato. Il servizio non parte immediatamente — vedi la sezione successiva per avviarlo.

### Avvio e arresto del servizio

#### Per avviare il servizio

1. Apri un terminale
2. Vai in `/opt/digna/bin`
3. Esegui:
   ```bash
   sudo ./start_service.sh
   ```

#### Per fermare il servizio

1. Apri un terminale
2. Vai in `/opt/digna/bin`
3. Esegui:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Suggerimento"

    Ferma sempre il servizio prima di aggiornare i file dell'applicazione.

### Gestione del servizio con systemctl

Una volta registrato, il servizio può anche essere controllato con i comandi systemd standard da qualsiasi directory:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Verifica del servizio

Per confermare che il servizio è registrato e in esecuzione:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` significa che il servizio si avvia al boot; `active` significa che è in esecuzione adesso.

### Visualizzare i log del servizio

systemd cattura tutto ciò che il backend scrive sulla console. Per leggerlo:

```bash
sudo journalctl -u digna -n 100
```

Per seguire i log in tempo reale mentre riproduci un problema:

```bash
sudo journalctl -u digna -f
```

!!! tip "Suggerimento"

    Questo è il modo più veloce per diagnosticare un servizio che si avvia e si arresta immediatamente. Un errore di connessione al repository o la mancanza di `license.toml` viene segnalata qui.

### Spostare il servizio in una nuova directory

Il file unit contiene il percorso assoluto all'eseguibile, quindi spostare l'installazione richiede la registrazione del servizio:

1. **Disinstalla il servizio corrente**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Sposta i file dell'applicazione**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Reinstalla il servizio**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Avvia il servizio**
   ```bash
   sudo ./start_service.sh
   ```

### Disinstallare il servizio

1. **Ferma il servizio in esecuzione**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Disinstalla il servizio**
   ```bash
   sudo ./uninstall_service.sh
   ```

Il server digna è ora deregistrato da systemd.

---

## Aggiornamento a una nuova release {: #upgrading-to-a-new-release }

### Prima di aggiornare

**È OBBLIGATORIO creare un backup del repository digna**

Prima di aggiornare digna, esegui il backup del repository (PostgreSQL) per proteggerti dalla perdita di dati.
Un backup ti permette di recuperare se l'aggiornamento incontra problemi imprevisti.

Per creare un backup dalla shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Processo di aggiornamento

#### Passo 1: Ferma il servizio digna

Se digna è in esecuzione come servizio systemd, fermalo prima:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Se digna è in esecuzione in primo piano, premi `Ctrl + C` nella finestra del terminale in cui è avviato.

#### Passo 2: Esegui il backup dell'installazione corrente del backend

Nella directory di installazione digna:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Passo 3: Estrai e distribuisci la nuova versione

1. Estrai il nuovo file ZIP di installazione digna
2. Copia il nuovo eseguibile `digna` e la cartella `dashboard` nella directory di installazione
3. Ripristina il bit eseguibile e la proprietà dell'account di servizio:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Importante"

    Il file `config.toml` **non** è mai incluso nell'archivio di installazione. La tua configurazione esistente resta al sicuro.

### Passo 4: Ripristina i file di configurazione

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Passo 5: Aggiorna lo schema del repository

Vai nella directory di installazione digna ed esegui:

```bash
cd /opt/digna
./digna repo upgrade
```

Questo aggiorna lo schema PostgreSQL all'ultima versione preservando tutti i dati esistenti.

### Passo 6: Riavvia i servizi

Se in esecuzione come servizio systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Se eseguito manualmente, riavvia il server:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Se usi nginx o Apache, ricarica il web server pertinente:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

Sulla famiglia RHEL, riapplica l'etichettatura SELinux se la directory `dashboard` è stata sostituita:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Passo 7: Verifica l'aggiornamento

1. Accedi alla dashboard digna
2. Verifica che l'interfaccia si carichi correttamente
3. Controlla i log del server per eventuali errori:

```bash
sudo journalctl -u digna -n 100
```
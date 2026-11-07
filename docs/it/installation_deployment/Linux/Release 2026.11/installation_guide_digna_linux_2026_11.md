---
title: Guida all'installazione Linux – digna Release 2026.11 | Documentazione digna
description: Guida passo passo all'installazione di digna Release 2026.11 su Linux — requisiti di sistema, configurazione di PostgreSQL, configurazione di nginx o Apache, configurazione del backend e della dashboard, esecuzione di digna come servizio systemd e aggiornamento dalla Release 2026.06.
keywords: guida installazione digna linux, guida deployment digna, configurazione backend digna, installazione dashboard digna, postgresql linux, nginx linux, servizio systemd digna, guida aggiornamento digna
image: /assets/logo_square.png
---

# Guida all'installazione Linux per digna Release 2026.11

**Release:** 2026.11

**Ultimo aggiornamento:** 7 novembre 2026


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

- **digna**: il cuore dell'applicazione, responsabile dell'elaborazione dei dati e dell'esecuzione dei controlli di qualità. Unisce il backend e l'interfaccia a riga di comando in un unico eseguibile, sostituendo i programmi separati `dignabackend` e `dignacli` delle versioni precedenti.
- **dignadashboard**: un'interfaccia web ospitata su un web server, che fornisce un modo user-friendly per interagire con la piattaforma digna e visualizzare le metriche sulla qualità dei dati.

### Novità nella Release 2026.11

Questa release aggiunge digna Data Reconciliation, digna Agentic con il digna MCP Server e il digna Engine, che può profilare i dati all'interno di digna e verificare l'integrità referenziale tra tecnologie di database diverse. Consulta le [note di rilascio](../../../changelog/Release_202611.md) per i dettagli completi.

Per l'installazione, la release introduce un nuovo meccanismo di migrazione del repository, una sezione facoltativa `[duckdb]` in `config.toml` per il digna Engine e un nuovo file di licenza. La [sezione sull'aggiornamento](#upgrading-to-a-new-release) li tratta uno per uno.

### Cerchi Windows o macOS?

Questa guida copre Linux. Per altre piattaforme, vedi la [Guida all'installazione per Windows](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) o la [Guida all'installazione per macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

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

!!! info "I file di configurazione e di licenza non sono inclusi nel pacchetto"

    Né `config.toml` né `dashboard/dashboard_config.toml` sono inclusi nell'installazione: li
    create entrambi voi, in [Configurazione del backend](#backend-configuration) e
    [Configurazione della dashboard](#dashboard-configuration). Nemmeno `license.toml` è incluso;
    digna lo fornisce separatamente, come descritto nel Passo 3.

Per estrarre da shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
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

    Se servi la dashboard da nginx o Apache sulla porta HTTP predefinita, l'origine da consentire è `http://localhost` — o l'URL pubblico del server se la dashboard è raggiunta da altre macchine.

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
| `DIGNA_REPO_PORT` | `5432` (predefinito) | Porta PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Nome del database |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema creato in precedenza |
| `DIGNA_REPO_USER` | `digna_user` | Utente creato nella configurazione PostgreSQL |
| `DIGNA_REPO_PASSWORD` | La tua password | Password impostata durante la creazione dello schema |
| `DIGNA_REPO_SSLMODE` | `prefer` (predefinito) | Facoltativo. Modalità SSL di PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` o `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (predefinito) | Facoltativo. Numero di connessioni che digna mantiene aperte verso il repository |

!!! tip "Buona pratica"

    `config.toml` contiene la password del database in testo chiaro. Restringi i permessi in modo che solo l'account di servizio possa leggerlo:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

    Per trovare il numero di core CPU disponibili sul server, esegui `nproc`.

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
| `DIGNA_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` per la produzione, `DEBUG` per il troubleshooting. Sono accettati anche `TRACE`, `WARN` ed `ERROR` |
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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Predefinito: la directory temporanea del sistema (`$TMPDIR`, o `/tmp` se non è impostata) | Directory per i file temporanei quando i dati non entrano in memoria |

!!! tip "Dimensionare il digna Engine"

    Prevedi fino a `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` di memoria sull'host di
    digna, in aggiunta a quella usata da digna stesso, e spazio libero su disco sufficiente nella directory
    temporanea per contenere la data ispezionata più grande delle origini dati che usano il digna Engine.
    Imposta `DIGNA_DUCKDB_TEMP_DIRECTORY` su un disco con questo spazio, scrivibile dall'account che
    esegue digna:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
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

### Passo 3: Inizializza il repository

1. Apri un terminale
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

    Su Linux, la directory corrente non è sulla PATH, quindi l'eseguibile viene invocato come `./digna` invece di `digna`. Per usare la forma più breve ovunque, aggiungi un link simbolico:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Passo 4: Installa lo schema del repository

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

### Passo 5: Crea un utente admin

1. Apri una nuova finestra del terminale
2. Vai nella directory di installazione digna
3. Esegui il seguente comando per creare un utente amministratore:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Esempio:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Questo crea un utente con l'indirizzo e-mail `admin@example.com` e privilegi amministrativi completi.

!!! tip "Suggerimento"

    Racchiudi la password tra virgolette singole. `bash` e `zsh` trattano caratteri come `!`, `$` e `*` in modo speciale, e una password non quotata che li contiene non sarà passata così come digitata.

!!! tip "Buona pratica"

    Usa una password forte con una combinazione di maiuscole, minuscole, numeri e caratteri speciali.

---

### Passo 6: Avvia il server digna

Nella directory di installazione digna, avvia il server con:

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

    Se la dashboard è servita da una macchina diversa rispetto al backend, apri anche la porta API nel firewall:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Il server occupa il terminale"

    `serve` viene eseguito in primo piano e continua finché non lo fermate con ++ctrl+c++. Lasciatelo in esecuzione mentre completate la configurazione; per avviarlo automaticamente all'avvio vedi [Eseguire digna come servizio systemd](#running-digna-as-a-systemd-service).

## Configurazione della dashboard {: #dashboard-configuration }

### Passo 1: Distribuisci la dashboard sul Web Server

La dashboard digna legge la propria configurazione da `dashboard/dashboard_config.toml`. Questo file non è incluso nell'installazione: lo create nella directory `dashboard/`, insieme ai file della dashboard.

Il suo contenuto è descritto in [Single Sign-On](../../../sso/overview.md), che è anche il punto in cui il file diventa necessario: contiene le opzioni di accesso offerte dalla dashboard e, per i deployment multi-istanza, la connessione al backend.

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

Questa sezione aggiorna un'installazione della Release 2026.06 alla Release 2026.11. Se la vostra
installazione è più vecchia, leggete prima [Aggiornamento da una release precedente alla 2026.06](#upgrading-from-a-release-before-2026-06).

### Prima di aggiornare

**È OBBLIGATORIO creare un backup del repository digna**

Prima di aggiornare digna, esegui il backup del repository (PostgreSQL) per proteggerti dalla perdita di dati.
Un backup ti permette di recuperare se l'aggiornamento incontra problemi imprevisti.

Per creare un backup dalla shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Richiedere il file di licenza per la Release 2026.11**

La Release 2026.11 richiede un nuovo `license.toml`. Richiedetelo al team digna prima di iniziare e
tenetelo pronto per il [passo 7](#step-7-replace-the-license-file).

### Aggiornamento da una release precedente alla 2026.06 {: #upgrading-from-a-release-before-2026-06 }

La Release 2026.06 ha introdotto tre modifiche che valgono ancora quando aggiornate un'installazione
più vecchia direttamente alla 2026.11:

- **Solo ODBC.** digna accede a ogni tecnologia di origine tramite ODBC. Ogni connessione al database che
  non usa ancora ODBC deve essere convertita a ODBC dopo l'aggiornamento; non esiste una conversione
  automatica. Installate prima i driver ODBC sull'host di digna (vedi
  [Installare il driver ODBC sull'host digna](../../../databases/overview.md#install-the-driver))
  e tenete pronte le proprietà di ogni connessione, prendendole dalle
  [guide per tecnologia](../../../databases/overview.md#technology-guides). Il connettore Databricks Legacy
  non esiste più; spostate quelle connessioni al connettore
  [Databricks](../../../databases/databricks_connector_guide.md).
- **Un unico eseguibile.** `dignabackend` e `dignacli` sono sostituiti dall'unico eseguibile `digna`,
  che unisce backend e CLI.
- **config.toml.** La sezione `[encryption]` è obbligatoria, e `DIGNA_APP_HOST` e
  `DIGNA_APP_PORT` non vengono più letti: il server prende indirizzo e porta da `digna serve`.
  Confrontate il vostro file con [Configurazione del backend](#backend-configuration).

I passi seguenti indicano dove un'installazione più vecchia richiede qualcosa di diverso. L'aggiornamento
del repository nel passo 8 porta un repository di qualsiasi release precedente direttamente alla 2026.11.

### Processo di aggiornamento

#### Passo 1: Ferma il servizio digna {: #step-1-stop-the-digna-service }

Se digna è in esecuzione come servizio systemd, fermalo prima:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Se digna è in esecuzione in primo piano, premi ++ctrl+c++ nella finestra del terminale in cui è avviato.

#### Passo 2: Eseguire il backup dell'installazione attuale {: #step-2-backup-current-installation }

Nella directory di installazione di digna, rinominate l'eseguibile e la cartella della dashboard
dell'installazione attuale, in modo che la nuova release possa essere distribuita accanto a essi:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Conservate `digna_old` finché non avete verificato l'aggiornamento, e `dashboard_old` finché non avete
ripristinato da essa i vostri file di configurazione (vedi passo 4). Dopo potete eliminarli entrambi.

!!! info "Aggiornamento da una release precedente alla 2026.06"

    Rinominate le cartelle `dignabackend` e `dignacli` invece dell'eseguibile:
    `sudo mv dignabackend dignabackend_old` e `sudo mv dignacli dignacli_old`. Nessuna delle due è usata dalla Release 2026.11.

#### Passo 3: Estrai e distribuisci la nuova versione {: #step-3-extract-and-deploy-new-version }

1. Estrai il nuovo file ZIP di installazione digna
2. Copia il nuovo eseguibile `digna` e la cartella `dashboard` nella directory di installazione
3. Ripristina il bit eseguibile e la proprietà dell'account di servizio:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Importante"

    Né `config.toml` né `dashboard/dashboard_config.toml` sono mai inclusi nello ZIP di
    installazione: il team digna non fornisce mai nessuno dei due file. La vostra configurazione
    esistente non viene quindi toccata dall'aggiornamento, e le copie nelle cartelle rinominate
    `*_old` sono le uniche che avete.

#### Passo 4: Ripristina i file di configurazione {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
./digna config check
```

Ogni sezione deve riportare OK. Correggete tutto ciò che viene segnalato come FAILED, rimuovete le chiavi
elencate sotto **Unknown keys** e rieseguite il comando prima di proseguire.

#### Passo 7: Sostituire il file di licenza {: #step-7-replace-the-license-file }

Di norma un file di licenza resta valido da una release alla successiva. La Release 2026.11 è
un'eccezione: aggiunge due moduli soggetti a licenza, digna Data Reconciliation e digna Agentic, e una
licenza emessa prima della 2026.11 non li contiene. Copiate il `license.toml` che il team digna vi ha
fornito per la Release 2026.11 nella directory di installazione, sostituendo quello vecchio:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Non mantenete la licenza precedente"

    Con la licenza precedente digna si avvia comunque, ma digna Data Reconciliation e il digna
    MCP Server restano disattivati. Ogni comando che verifica la licenza (`user`,
    `inspection`, `repo`) si interrompe prima di toccare il repository se la verifica fallisce.
    Verificate la nuova licenza prima di proseguire:

    ```bash
    ./digna license check
    ```

#### Passo 8: Aggiorna lo schema del repository {: #step-8-upgrade-the-repository-schema }

Nella directory di installazione di digna, eseguite:

```bash
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

#### Passo 9: Riavvia i servizi {: #step-9-restart-services }

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

#### Passo 10: Verifica l'aggiornamento {: #step-10-verify-the-upgrade }

1. Verificate la release del nuovo eseguibile:

    ```bash
    ./digna version
    ```

    La prima riga deve riportare `Release: 2026.11`.

2. Accedete alla dashboard di digna e verificate che l'interfaccia si carichi correttamente.
3. Controllate i log del server per verificare la presenza di errori:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Testate le vostre connessioni al database (vedi
   [Testare una connessione](../../../databases/overview.md#testing-a-connection)). Dopo un aggiornamento
   da una release precedente alla 2026.06, convertite prima a ODBC tutte le connessioni che non lo
   usavano già.

Per iniziare con i nuovi moduli, consultate [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Collegare un agente IA](../../../platform/agentic/connect_ai_agent.md) per il digna MCP Server e
[Posizione di profilazione](../../../platform/profiling/profiling_location.md) per il digna Engine.

---
title: Ghid de instalare pe Linux – digna Release 2026.06 | Documentația digna
description: Ghid pas cu pas pentru instalarea digna Release 2026.06 pe Linux — cerințe de sistem, configurarea PostgreSQL, configurarea nginx sau Apache, configurarea backend-ului și a dashboard-ului, rularea digna ca serviciu systemd și actualizarea la o versiune nouă.
keywords: digna instalare linux, ghid implementare digna, configurare backend digna, instalare dashboard digna, postgresql linux, nginx linux, serviciu systemd digna, ghid actualizare digna
image: /assets/logo_square.png
---

# Ghid de instalare pe Linux pentru digna Release 2026.06

**Release:** 2026.06

**Ultima actualizare:** 5 septembrie 2026


---

## Cuprins

1. [Introducere](#introduction)
2. [Cerințe de sistem](#system-requirements)
3. [Pregătirea înainte de instalare](#pre-installation-setup)
4. [Configurarea serverului PostgreSQL](#postgresql-server-setup)
5. [Configurarea web serverului](#web-server-configuration)
6. [Instalarea inițială](#initial-installation)
7. [Configurarea backend-ului](#backend-configuration)
8. [Configurarea dashboard-ului](#dashboard-configuration)
9. [Rularea digna ca serviciu systemd](#running-digna-as-a-systemd-service)
10. [Actualizarea la o versiune nouă](#upgrading-to-a-new-release)

---

## Introducere {: #introduction }

### Despre digna

digna este o platformă completă, bazată pe AI, concepută pentru a optimiza gestionarea calității datelor în diverse medii de date, cum ar fi data warehouses, data lakes și lakehouses. Construită pentru scalabilitate și adaptabilitate ridicate, digna abordează provocările moderne ale datelor prin automatizare, monitorizare în timp real și detectarea anomaliilor.

digna este alcătuită din două componente principale:

- **digna**: nucleul aplicației, responsabil de prelucrarea datelor și de efectuarea verificărilor de calitate. Reunește backend-ul și interfața în linie de comandă într-un singur executabil, înlocuind programele separate `dignabackend` și `dignacli` din versiunile anterioare.
- **dignadashboard**: o interfață web găzduită pe un web server, care oferă o modalitate prietenoasă de a interacționa cu platforma digna și de a vizualiza metricile de calitate a datelor.

### Noutăți în Release 2026.06

Această versiune aduce capabilitățile de observabilitate a datelor direct în codul dumneavoastră, permițând dezvoltatorilor să monitorizeze calitatea datelor la sursă. Consultați [notele de lansare](http://docs.digna.ai/changelog/Release_202606/) pentru detalii complete.

### Căutați Windows sau macOS?

Acest ghid acoperă Linux. Pentru alte platforme, consultați [Ghidul de instalare Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) sau [Ghidul de instalare macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

### Ce distribuții acoperă acest ghid?

Instrucțiunile sunt scrise pentru cele mai răspândite două familii de servere. Acolo unde cele două diferă, sunt indicate ambele comenzi:

- **Familia Debian** — Debian, Ubuntu. Manager de pachete: `apt`.
- **Familia RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Manager de pachete: `dnf`.

Orice distribuție modernă cu `systemd` va funcționa; se schimbă doar numele pachetelor și câteva căi de configurare.

---

## Cerințe de sistem {: #system-requirements }

Înainte de a începe instalarea, asigurați-vă că sistemul dumneavoastră îndeplinește următoarele cerințe minime:

| Cerință | Specificație |
|---|---|
| **Sistem de operare** | Ubuntu 22.04 LTS sau mai nou, Debian 12 sau mai nou, RHEL 9 / Rocky 9 / AlmaLinux 9 sau mai nou |
| **Arhitectură** | x86_64 (amd64) sau arm64 |
| **Sistem de inițializare** | systemd |
| **Memorie (configurație minimă)** | 16 GB RAM |
| **Spațiu pe disc** | 10 GB spațiu de stocare disponibil |
| **Bază de date** | PostgreSQL Server 12 sau o versiune superioară |
| **Web server** | nginx, Apache httpd sau echivalent |

### Opțiuni de instalare a bazei de date

**Dacă PostgreSQL este deja instalat:**
Puteți adăuga o bază de date nouă pentru digna pe serverul PostgreSQL existent.

**Dacă instalați PostgreSQL pe aceeași mașină cu digna:**

!!! info "Specificații recomandate"

    - **Memorie**: 32 GB RAM (în loc de 16 GB)
    - **Spațiu pe disc**: 50 GB spațiu de stocare disponibil (în loc de 10 GB)

    Aceste specificații mai mari permit rularea simultană a digna și a bazei de date PostgreSQL.

### Verificarea distribuției și a arhitecturii

Mai multe comenzi din acest ghid diferă între familiile Debian și RHEL. Pentru a verifica pe care dintre ele vă aflați, rulați:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` sau `ID=debian` — folosiți comenzile `apt`.
- `ID=rhel`, `rocky`, `almalinux` sau `fedora` — folosiți comenzile `dnf`.
- `x86_64` sau `aarch64` — arhitectura pachetului de instalare de care aveți nevoie.

---

## Pregătirea înainte de instalare {: #pre-installation-setup }

Înainte de a instala digna, asigurați-vă că sunt pregătite două cerințe preliminare esențiale:

1. **Serverul PostgreSQL** – pentru stocarea metricilor calculate și a datelor de performanță
2. **Web serverul** – pentru găzduirea digna Dashboard

Dacă aceste componente nu sunt deja configurate, urmați secțiunile de mai jos pentru a le instala și configura.

### Reîmprospătarea indexului de pachete

Actualizați listele de pachete înainte de a instala ceva:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Notă"

    În tot acest ghid, prima comandă dintr-o pereche este pentru **familia Debian**, iar a doua pentru **familia RHEL**. Rulați doar comanda care corespunde sistemului dumneavoastră.

---

## Configurarea serverului PostgreSQL {: #postgresql-server-setup }

### Dacă aveți deja PostgreSQL

Dacă PostgreSQL este deja instalat și rulează pe mașina locală sau dacă folosiți un server PostgreSQL gestionat, la distanță, puteți trece direct la [secțiunea următoare](#web-server-configuration).

### Instalarea PostgreSQL

#### Pasul 1: Instalați pachetul serverului

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Sfat"

    Pachetele distribuției pot rămâne în urma versiunii curente PostgreSQL. Dacă aveți nevoie de o anumită versiune mai nouă, folosiți în schimb [repository-ul oficial PostgreSQL apt sau yum](https://www.postgresql.org/download/linux/).

#### Pasul 2: Inițializați clusterul de baze de date

Pe **familia Debian**, pachetul creează și pornește automat un cluster — treceți la pasul următor.

Pe **familia RHEL**, clusterul trebuie creat explicit:

```bash
sudo postgresql-setup --initdb
```

#### Pasul 3: Porniți și activați serviciul

```bash
sudo systemctl enable --now postgresql
```

Aceasta pornește imediat PostgreSQL și îl configurează să pornească din nou automat la pornirea sistemului.

#### Pasul 4: Verificați instalarea

```bash
psql --version
sudo systemctl status postgresql
```

Ar trebui să vedeți versiunea PostgreSQL și un serviciu `active (running)`.

#### Pasul 5: Conectați-vă la server

Un pachet PostgreSQL pentru Linux creează un cont de sistem `postgres` care deține clusterul. Conectați-vă prin intermediul acestuia:

```bash
sudo -u postgres psql
```

!!! note "Notă — aici Linux diferă de Windows"

    Programul de instalare pentru Windows vă cere să setați o parolă pentru superutilizatorul `postgres` în timpul instalării. Pachetele Linux nu fac acest lucru. În schimb, conexiunile locale sunt autentificate prin **peer authentication**: utilizatorul de sistem de operare `postgres` are voie să se conecteze ca utilizatorul de bază de date `postgres` fără parolă.

    De aceea comanda de mai sus folosește `sudo -u postgres`. Backend-ul digna se conectează prin TCP cu nume de utilizator și parolă, așa că veți crea un utilizator digna explicit în [Instalarea inițială](#initial-installation).

#### Pasul 6: Confirmați portul

Portul implicit PostgreSQL este `5432`. Pentru a confirma portul pe care ascultă serverul:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Notați valoarea — veți avea nevoie de ea la configurarea backend-ului digna.

#### Pasul 7: Activați autentificarea prin parolă pentru utilizatorul digna

digna se conectează la PostgreSQL prin TCP ca `digna_user`, ceea ce necesită autentificare prin parolă, nu peer authentication. Verificați că fișierul `pg_hba.conf` permite acest lucru.

Găsiți fișierul:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Deschideți-l într-un editor și confirmați că liniile TCP locale folosesc `scram-sha-256` (sau `md5` pe serverele mai vechi), nu `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Reîncărcați PostgreSQL după orice modificare:

```bash
sudo systemctl reload postgresql
```

!!! warning "Important"

    Dacă digna raportează `FATAL: Ident authentication failed for user "digna_user"`, această setare este cauza.

#### Pasul 8: Dacă PostgreSQL rulează pe o altă mașină

Pentru a accepta conexiuni de la o altă gazdă, setați `listen_addresses` în `postgresql.conf` și adăugați o linie `host` corespunzătoare pentru rețeaua dumneavoastră în `pg_hba.conf`:

```
listen_addresses = '*'
```

Apoi deschideți portul în firewall și reporniți serviciul:

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

## Configurarea web serverului {: #web-server-configuration }

digna necesită un web server pentru a găzdui dashboard-ul. Alegeți una dintre următoarele opțiuni:

- [nginx](#nginx-setup) — ușor și recomandat
- [Apache httpd](#apache-setup) — alternativă larg răspândită

Trebuie să instalați și să configurați **doar unul** dintre aceste servere.

Ambele secțiuni configurează două lucruri de care depinde dashboard-ul:

- **O rută de rezervă pentru aplicația single-page**, astfel încât reîmprospătarea unui URL al dashboard-ului să nu returneze 404
- **Un tip MIME pentru `.md`**, astfel încât fișierele Markdown să fie servite corect

### Configurarea nginx {: #nginx-setup }

#### Prezentare generală

nginx este un web server ușor și performant, foarte potrivit pentru servirea dashboard-ului static digna.

#### Instalare

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Pornirea nginx

```bash
sudo systemctl enable --now nginx
```

#### Verificați instalarea

1. Deschideți browserul
2. Accesați `http://localhost`
3. Ar trebui să vedeți pagina de bun venit nginx

#### Deschiderea firewall-ului

Dacă serverul este accesat de pe alte mașini, permiteți traficul HTTP:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Configurarea unui site pentru dashboard

Pe ambele familii de distribuții, nginx include fiecare fișier din directorul său `conf.d`. Creați acolo un fișier de configurare dedicat pentru digna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Lipiți următorul conținut, înlocuind `/opt/digna/dashboard` cu calea reală către folderul `dashboard` extras:

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

!!! warning "Important"

    Fără directiva `try_files`, reîncărcarea oricărei pagini a dashboard-ului în afară de URL-ul rădăcină returnează 404. Acesta este echivalentul nginx al modulului URL Rewrite cerut de IIS pe Windows.

#### Dezactivați site-ul implicit

Un singur bloc server poate fi `default_server` pentru un port. Pe **familia Debian**, eliminați site-ul implicit din pachet, pentru a nu intra în conflict:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

Pe **familia RHEL**, comentați sau ștergeți blocul `server { ... }` din `/etc/nginx/nginx.conf`.

#### Aplicați configurația

Testați configurația pentru erori de sintaxă, apoi reîncărcați nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Configurarea Apache httpd {: #apache-setup }

#### Prezentare generală

Apache httpd este disponibil în repository-urile implicite ale fiecărei distribuții acceptate. Pachetul se numește `apache2` pe familia Debian și `httpd` pe familia RHEL.

#### Instalare

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Pornirea Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Verificați instalarea

1. Deschideți browserul
2. Accesați `http://localhost`
3. Ar trebui să vedeți pagina Apache implicită a distribuției

#### Obligatoriu: activați mod_rewrite

Dashboard-ul necesită rescrierea URL-urilor.

Pe **familia Debian**, activați modulul și reporniți:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

Pe **familia RHEL**, `mod_rewrite` este încărcat implicit. Confirmați acest lucru:

```bash
httpd -M | grep rewrite
```

#### Obligatoriu: permiteți suprascrierile .htaccess

Deschideți fișierul de configurare pentru document root:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Găsiți blocul `<Directory>` care acoperă document root (`/var/www/html` pe ambele familii) și modificați:

```apache
AllowOverride None
```

în:

```apache
AllowOverride All
```

#### Obligatoriu: tipul MIME pentru fișierele Markdown

În același fișier, adăugați linia următoare, astfel încât fișierele Markdown să fie servite corect:

```apache
AddType text/markdown .md
```

!!! warning "Important"

    Fără această setare, fișierele `.md` s-ar putea să nu fie servite corect.

#### Aplicați configurația

Verificați configurația pentru erori de sintaxă, apoi reporniți Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Instalarea inițială {: #initial-installation }

### Pasul 1: Configurați repository-ul digna

Repository-ul digna stochează toate metricile calculate de digna. Acesta funcționează ca bază de date centrală pentru datele analitice și de performanță.

#### Creați schema repository-ului și utilizatorul

Deschideți clientul PostgreSQL (psql, pgAdmin sau similar) și executați următoarele comenzi SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Înlocuiți următorii substituenți:**

- `<digna_repo_schema>` — numele dorit pentru schemă (de ex. `dignarepo`)
- `<digna_repo_user>` — numele de utilizator dorit (de ex. `digna_user`)
- `<digna_repo_password>` — o parolă sigură pentru acest utilizator

**Exemplu:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Pentru a le rula din shell într-un singur pas:

```bash
sudo -u postgres psql
```

Apoi lipiți instrucțiunile la promptul `postgres=#` și tastați `\q` pentru a ieși.

!!! tip "Practică recomandată"

    Folosiți parole puternice și complexe pentru utilizatorii bazei de date. Evitați credențialele ușor de ghicit.

---

### Pasul 2: Extrageți pachetul de instalare digna

1. Găsiți fișierul ZIP de instalare digna care v-a fost furnizat
2. Extrageți-l în locația de instalare dorită — de exemplu `/opt/digna`
3. După extragere, ar trebui să vedeți următoarele elemente:
   - `dashboard/` — interfața web a dashboard-ului
   - `digna` — executabilul principal (backend + CLI combinate)

!!! info "Fișierele de configurare și de licență nu se află în pachet"

    Nici `config.toml`, nici `dashboard/dashboard_config.toml` nu sunt livrate cu instalarea — le
    creați pe amândouă dumneavoastră, în [Configurarea backend-ului](#backend-configuration) și
    [Configurarea dashboard-ului](#dashboard-configuration). Nici `license.toml` nu este livrat;
    digna îl furnizează separat, așa cum descrie Pasul 3.

Pentru extragerea din shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Notă"

    Dacă `unzip` nu este instalat, adăugați-l cu `sudo apt install -y unzip` sau `sudo dnf install -y unzip`.

#### Faceți executabilul rulabil

În funcție de modul în care a fost transferată arhiva, bitul de execuție s-ar putea să nu se păstreze la extragere. Setați-l explicit:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Creați un cont de serviciu

Pentru implementările de producție se recomandă rularea backend-ului sub un utilizator dedicat, fără privilegii:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Notă"

    Pe familia RHEL, calea echivalentă a shell-ului este `/sbin/nologin`.

### Pasul 3: Instalați fișierul de licență

!!! warning "Important"

    Fișierul de licență **nu** este inclus în pachetul de instalare și va fi furnizat separat de digna.

1. Găsiți fișierul `license.toml` care v-a fost furnizat
2. Copiați-l în directorul rădăcină al instalării digna (unde se află `config.toml` și executabilul `digna`)

**De ce este important:**
Fișierul de licență conține informațiile dumneavoastră de client, data de expirare a licenței și semnătura digitală. **Nu modificați acest fișier** — orice modificare îl invalidează.

**Structura directorului după configurare:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Configurarea backend-ului {: #backend-configuration }

### Pasul 1: Creați și editați fișierul de configurare

Fișierul `config_template.toml` este furnizat în directorul de instalare digna. Trebuie doar să-l redenumiți în `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Locație:** `/opt/digna/config.toml`

Deschideți `config.toml` într-un editor de text și configurați fiecare secțiune de mai jos.

#### Secțiunea [app]

Această secțiune configurează setările aplicației backend digna:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametru | Valoare | Observații |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | URL-ul frontend-ului | Dacă dashboard-ul se află pe alt server, includeți URL-ul acestuia |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Necesar pentru CORS cu credențiale |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Permite toate metodele HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Permite toate antetele |

!!! note "Notă"

    Dacă serviți dashboard-ul din nginx sau Apache pe portul HTTP implicit, originea care trebuie permisă este `http://localhost` — sau URL-ul public al serverului, atunci când dashboard-ul este accesat de pe alte mașini.

#### Secțiunea [repo]

Această secțiune configurează conexiunea la baza de date PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parametru | Valoare | Observații |
|---|---|---|
| `digna_REPO_HOST` | `localhost` sau IP | Numele de gazdă/IP-ul serverului PostgreSQL |
| `digna_REPO_PORT` | `5432` (implicit) | Portul PostgreSQL |
| `digna_REPO_DB` | `postgres` | Numele bazei de date |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema creată anterior |
| `digna_REPO_USER` | `digna_user` | Utilizatorul creat la configurarea PostgreSQL |
| `digna_REPO_PASSWORD` | Parola dumneavoastră | Parola setată la crearea schemei |

!!! tip "Practică recomandată"

    `config.toml` conține o parolă a bazei de date în text simplu. Restricționați-i permisiunile, astfel încât doar contul de serviciu să-l poată citi:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### Secțiunea [base]

Această secțiune conține setările de securitate și pentru cookie-uri:

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

| Parametru | Valoare | Observații |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Trebuie să corespundă domeniului frontend-ului |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (producție) | Folosiți `true` pentru conexiuni HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Întotdeauna activat, pentru securitate |
| `digna_COOKIE_SAME_SITE` | `lax` | Previne atacurile CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 de ore) | Durata sesiunii, în secunde |
| `digna_MAX_WORKERS` | Numărul de nuclee CPU - 1 | Numărul de sarcini de inspecție paralele |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Întârzierea maximă, în secunde, pe care planificatorul o poate adăuga înainte de a porni o sarcină scadentă |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Ora din zi (format de 24 de ore `HH:MM`) la care începe curățarea zilnică |

!!! tip "Sfat"

    Pentru a afla numărul de nuclee CPU disponibile pe server, rulați `nproc`.

#### Secțiunea [encryption]

Această secțiune conține cheia folosită pentru a cripta valorile sensibile stocate în repository. Este **obligatorie** — `config check` raportează secțiunea `[encryption]` ca FAILED dacă lipsește cheia.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametru | Valoare | Observații |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Cheie codificată Base64 | Criptează valorile sensibile stocate în repository-ul digna |

!!! warning "Protejați config.toml"

    Această cheie este o valoare fixă, identică în toate instalările digna, și tocmai ea decriptează
    valorile sensibile din repository-ul dumneavoastră. Restricționați `config.toml` la contul care
    rulează digna, țineți fișierul în afara controlului versiunilor și a unităților partajate și
    excludeți-l din orice copie de siguranță păstrată mai puțin sigur decât repository-ul însuși.

#### Secțiunea [logging]

Această secțiune configurează comportamentul de logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametru | Valoare | Observații |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` sau `DEBUG` | `INFO` pentru producție, `DEBUG` pentru depanare |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Numărul de copii zilnice ale logurilor păstrate |

---

### Pasul 2: Validați configurația

Înainte de a inițializa repository-ul, verificați dacă `config.toml` este complet și corect alcătuit. În directorul de instalare digna, rulați:

```bash
./digna config check
```

Fiecare secțiune este validată separat, astfel încât o singură greșeală nu ascunde starea celorlalte:

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

Corectați tot ce este raportat ca FAILED și rulați comanda din nou înainte de a continua. Lista completă a opțiunilor se află în [referința CLI](../../../cli/Command_Line_Interface_202606.md).

### Pasul 3: Inițializați repository-ul

1. Deschideți un terminal
2. Accesați directorul de instalare digna (unde se află `config.toml` și executabilul `digna`)
3. Rulați testul de conexiune:

```bash
cd /opt/digna
./digna repo check
```

Ar trebui să vedeți o confirmare că conexiunea este stabilită (repository-ul în sine nu a fost încă inițializat).

!!! note "Notă"

    Pe Linux, directorul curent nu se află în PATH, așa că executabilul este apelat ca `./digna`, nu ca `digna`. Pentru a folosi peste tot forma scurtă, adăugați o legătură simbolică:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Pasul 4: Instalați schema repository-ului

În același director, rulați:

```bash
./digna repo install
```

Această comandă instalează tabelele și schema necesare în baza de date PostgreSQL.

### Pasul 5: Creați un utilizator administrator

Utilizatorul administrator este creat direct în schema repository-ului, astfel încât serverul nu trebuie să ruleze încă. În directorul de instalare digna, rulați:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Exemplu:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Aceasta creează un utilizator cu adresa de e-mail `admin@example.com` și privilegii administrative complete.

!!! tip "Sfat"

    Puneți parola între ghilimele simple. `bash` și `zsh` tratează în mod special caractere precum `!`, `$` și `*`, iar o parolă fără ghilimele care le conține nu va fi transmisă așa cum a fost tastată.

!!! tip "Practică recomandată"

    Folosiți o parolă puternică, cu o combinație de majuscule, minuscule, cifre și caractere speciale.

### Pasul 6: Porniți serverul digna

În directorul de instalare digna, porniți serverul cu:

```bash
./digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — numele de gazdă/IP-ul serverului
- `--port` — portul serverului

Ar trebui să vedeți mesajele de pornire care confirmă că serverul rulează:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Sfat"

    Dacă dashboard-ul este servit de pe o altă mașină decât backend-ul, deschideți și portul API în firewall:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Serverul ocupă terminalul"

    `serve` rulează în prim-plan și continuă până când îl opriți cu ++ctrl+c++. Lăsați-l să ruleze cât timp finalizați configurarea; pentru a-l porni automat la pornirea sistemului, consultați [Rularea digna ca serviciu systemd](#running-digna-as-a-systemd-service).

---

## Configurarea dashboard-ului {: #dashboard-configuration }

### Pasul 1: Implementați dashboard-ul pe web server

Dashboard-ul digna își citește propria configurație din `dashboard/dashboard_config.toml`. Acest fișier nu este livrat cu instalarea — îl creați în directorul `dashboard/`, alături de fișierele dashboard-ului.

Conținutul său este descris în [Single Sign-On](../../../sso/overview.md), unde este de altfel și nevoie de fișier: acesta conține opțiunile de autentificare oferite de dashboard și, pentru implementările cu mai multe instanțe, conexiunea la backend.

Alegeți web serverul și urmați pașii de implementare corespunzători.

#### Implementarea pe nginx

Dacă ați urmat secțiunea [Configurarea nginx](#nginx-setup), blocul server indică deja folderul `dashboard` și nu este necesară nicio copiere.

1. **Confirmați calea**
   - Deschideți `/etc/nginx/conf.d/digna.conf`
   - Verificați că `root` indică folderul `dashboard` extras

2. **Asigurați-vă că folderul poate fi citit**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Reîncărcați nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Testați instalarea**
   - Deschideți browserul
   - Accesați `http://localhost` (sau URL-ul configurat)
   - Ar trebui să vedeți pagina de autentificare a dashboard-ului digna

#### Implementarea pe Apache httpd

1. **Copiați dashboard-ul în document root**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Adăugați regulile de rescriere**

   Creați un fișier `.htaccess` în folderul implementat, astfel încât rutele dashboard-ului să reziste la reîmprospătarea browserului:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Lipiți următorul conținut:

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

3. **Reporniți Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Accesați dashboard-ul**
   - Deschideți browserul
   - Accesați `http://localhost/digna`
   - Ar trebui să vedeți pagina de autentificare a dashboard-ului digna

### Pasul 2: SELinux (doar familia RHEL)

Pe RHEL, Rocky, AlmaLinux și Fedora, SELinux este implicit în modul enforcing și va împiedica web serverul să citească fișiere din afara locațiilor așteptate. Verificați dacă este activ:

```bash
getenforce
```

Dacă rezultatul este `Enforcing` și serviți dashboard-ul din `/opt/digna/dashboard`, etichetați directorul astfel încât web serverul să-l poată citi:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Notă"

    Dacă `semanage` nu este găsit, instalați-l cu `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Important"

    Un dashboard care returnează **403 Forbidden** pe un server RHEL proaspăt configurat este aproape întotdeauna o problemă de etichetare SELinux, nu una de permisiuni ale fișierelor. Confirmați cu `sudo ausearch -m avc -ts recent`.

---

## Rularea digna ca serviciu systemd {: #running-digna-as-a-systemd-service }

### De ce să rulați digna ca serviciu?

Rularea backend-ului digna ca serviciu systemd asigură că acesta:

- Pornește automat la pornirea mașinii
- Rulează în fundal, fără o fereastră de terminal deschisă
- Repornește automat dacă se blochează
- Poate fi gestionat prin `systemctl`, managerul de servicii standard din Linux

### Fișierele de gestionare a serviciului

Toate fișierele necesare se află în directorul de instalare digna, în: `bin/`

Sunt disponibile următoarele scripturi shell:

- `install_service.sh` — înregistrează digna în systemd
- `uninstall_service.sh` — anulează înregistrarea serviciului
- `start_service.sh` — pornește serviciul înregistrat
- `stop_service.sh` — oprește serviciul aflat în execuție

!!! warning "Sunt necesare privilegii root"

    Toate scripturile trebuie executate cu `sudo`, deoarece înregistrarea unui serviciu care pornește la pornirea sistemului scrie un fișier unit în `/etc/systemd/system`.

### Facerea scripturilor executabile

Este posibil ca extragerea să nu păstreze bitul de execuție. Înainte de prima utilizare:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Instalarea serviciului

1. **Deschideți un terminal**

2. **Accesați folderul bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Rulați scriptul de instalare**
   ```bash
   sudo ./install_service.sh
   ```

Serverul digna este acum înregistrat în systemd, cu **pornire automată** activată. Serviciul nu pornește imediat — consultați secțiunea următoare pentru a-l porni.

### Pornirea și oprirea serviciului

#### Pentru a porni serviciul

1. Deschideți un terminal
2. Accesați `/opt/digna/bin`
3. Rulați:
   ```bash
   sudo ./start_service.sh
   ```

#### Pentru a opri serviciul

1. Deschideți un terminal
2. Accesați `/opt/digna/bin`
3. Rulați:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Sfat"

    Opriți întotdeauna serviciul înainte de a actualiza fișierele aplicației.

### Gestionarea serviciului cu systemctl

După înregistrare, serviciul poate fi controlat și cu comenzile systemd standard, din orice director:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Verificarea serviciului

Pentru a confirma că serviciul este înregistrat și rulează:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` înseamnă că serviciul pornește la pornirea sistemului; `active` înseamnă că rulează în acest moment.

### Vizualizarea logurilor serviciului

systemd captează tot ce scrie backend-ul în consolă. Pentru a citi aceste mesaje:

```bash
sudo journalctl -u digna -n 100
```

Pentru a urmări logul în timp real în timp ce reproduceți o problemă:

```bash
sudo journalctl -u digna -f
```

!!! tip "Sfat"

    Aceasta este cea mai rapidă metodă de a diagnostica un serviciu care pornește și se oprește imediat. O eroare de conexiune la repository sau un `license.toml` lipsă sunt raportate aici.

### Mutarea serviciului într-un director nou

Fișierul unit stochează calea absolută către executabil, așa că mutarea instalării necesită reînregistrarea serviciului:

1. **Dezinstalați serviciul curent**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Mutați fișierele aplicației**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Reinstalați serviciul**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Porniți serviciul**
   ```bash
   sudo ./start_service.sh
   ```

### Dezinstalarea serviciului

1. **Opriți serviciul aflat în execuție**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Dezinstalați serviciul**
   ```bash
   sudo ./uninstall_service.sh
   ```

Serverul digna nu mai este acum înregistrat în systemd.

---

## Actualizarea la o versiune nouă {: #upgrading-to-a-new-release }

### Înainte de actualizare

**Verificați mai întâi toate conexiunile la baze de date**

Începând cu Release 2026.06, digna accesează fiecare tehnologie sursă prin **ODBC**. Versiunile anterioare
ofereau alegerea între un driver specific fiecărei tehnologii și ODBC, selectată prin comutatorul **Use ODBC**.
Echipa digna a decis să se bazeze exclusiv pe ODBC, deoarece o singură interfață standard vă oferă
mai mult decât un set de drivere făcute la comandă:

- **Autentificare** — autentificarea face parte din ODBC, așa că o conexiune poate folosi tot ce acceptă
  driverul său: parole, token-uri și PAT-uri, Kerberos și Active Directory, MFA și autentificare unică din browser,
  identități în cloud, certificate de client și TLS. Metodele noi vin odată cu o actualizare a driverului,
  fără a aștepta o versiune digna.
- **Drivere întreținute de producătorii bazelor de date** — driverul propriu al producătorului urmărește noile versiuni
  de server și corecțiile de securitate, iar dumneavoastră îl puteți actualiza după propriul calendar, independent de digna.
- **Un singur mod de a configura totul** — fiecare tehnologie este o listă de proprietăți cheie/valoare, cu
  aceeași interfață, aceeași criptare a valorilor sensibile și aceeași depanare,
  în locul unui set diferit de câmpuri pentru fiecare sursă.
- **Reglare și acoperire** — opțiunile driverului, precum timpii de expirare, setările TLS, proxy-urile și dimensiunile
  de citire, sunt disponibile pentru fiecare sursă, iar orice tehnologie cu un driver ODBC conform poate fi
  conectată, inclusiv cele pentru care digna nu publică un ghid dedicat.

În practică, aceasta înseamnă că comutatorul **Use ODBC** și câmpurile separate pentru gazdă, port, bază de date, utilizator și
parolă nu mai există. **Fiecare conexiune care nu folosește deja ODBC trebuie trecută
pe ODBC** — nu există conversie automată, așa că planificați acest lucru înainte de actualizare:

1. Parcurgeți fiecare conexiune la baze de date definită în instalarea dumneavoastră și notați-le pe cele care nu
   folosesc încă ODBC — fiecare dintre ele va trebui reconfigurată.
2. Instalați driverul ODBC corespunzător pe gazda digna — conexiunile sunt deschise de pe serverul
   care rulează backend-ul digna, nu din browser. Consultați
   [Instalarea driverului ODBC pe gazda digna](../../../databases/overview.md#install-the-driver).
3. Pregătiți proprietățile ODBC pentru fiecare conexiune afectată.
   [Ghidurile pe tehnologii](../../../databases/overview.md#technology-guides) prezintă, pentru fiecare sursă,
   un set de proprietăți verificat.

După actualizare, treceți fiecare conexiune afectată pe ODBC și testați-o din dashboard —
consultați [Crearea unei conexiuni la baza de date](../../../databases/overview.md#create-a-database-connection)
și [Testarea unei conexiuni](../../../databases/overview.md#testing-a-connection).

!!! warning "Conexiuni Databricks Legacy"

    Conectorul Databricks Legacy a fost eliminat în această versiune. Migrați aceste conexiuni
    către conectorul [Databricks](../../../databases/databricks_connector_guide.md).

**Crearea unei copii de siguranță a repository-ului digna este obligatorie**

Înainte de a actualiza digna, faceți o copie de siguranță a repository-ului (PostgreSQL) pentru a vă proteja împotriva pierderii de date.
O copie de siguranță vă permite recuperarea dacă actualizarea întâmpină probleme neașteptate.

Pentru a crea o copie de siguranță din shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Procesul de actualizare

#### Pasul 1: Opriți serviciul digna

Dacă digna rulează ca serviciu systemd, opriți-l mai întâi:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Dacă digna rulează în prim-plan, apăsați `Ctrl + C` în fereastra sa de terminal.

#### Pasul 2: Faceți o copie de siguranță a instalării curente

În directorul de instalare digna, redenumiți folderele instalării curente, astfel încât noua versiune să poată fi implementată alături de ele:

```bash
cd /opt/digna
sudo mv dignabackend dignabackend_old
```
```bash
sudo mv dignacli dignacli_old
```
```bash
sudo mv dashboard dashboard_old
```

!!! info "dignabackend și dignacli nu mai sunt folosite"

    Începând cu Release 2026.06, `dignabackend` și `dignacli` sunt înlocuite de executabilul unic `digna`, care reunește backend-ul și CLI-ul. Păstrați `dignabackend_old` și `dignacli_old` doar până când ați verificat actualizarea — apoi puteți șterge ambele foldere. Păstrați `dashboard_old` până când v-ați restaurat din el fișierele de configurare (consultați Pasul 4).

#### Pasul 3: Extrageți și implementați noua versiune

1. Extrageți noul fișier ZIP de instalare digna
2. Copiați noul executabil `digna` și folderul `dashboard` în directorul de instalare
3. Restabiliți bitul de execuție și proprietarul (contul de serviciu):

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Important"

    Nici `config.toml`, nici `dashboard/dashboard_config.toml` nu sunt incluse vreodată în
    ZIP-ul de instalare — echipa digna nu livrează niciodată aceste fișiere. Configurația existentă
    rămâne, prin urmare, neatinsă de actualizare, iar copiile din folderele `*_old` redenumite sunt
    singurele pe care le aveți.

#### Pasul 4: Restaurați fișierele de configurare

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

!!! warning "Release 2026.06 modifică config.toml"

    Trei setări sunt noi și obligatorii, iar trei nu mai sunt folosite. Un `config.toml` preluat dintr-o versiune anterioară nu conține setările noi, iar digna nu va porni cât timp acestea lipsesc. Adăugați următoarele în `config.toml` existent:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Adăugați cele două chei `[base]` în secțiunea `[base]` existentă și adăugați `[encryption]` ca secțiune nouă. Apoi eliminați setările care nu mai sunt folosite: **`digna_FERNET_KEY`** din `[base]`, precum și **`digna_APP_HOST`** și **`digna_APP_PORT`** din `[app]` — serverul își preia acum adresa și portul din `digna serve`.

    Ce face fiecare setare este descris în [Configurarea backend-ului](#backend-configuration).

!!! warning "Autentificare unică: formatul [oidc_clients] s-a schimbat"

    Release 2026.06 înlocuiește matricea de tabele cu câte un tabel pentru fiecare furnizor, denumit după
    cheia furnizorului. `DIGNA_OIDC_KEY` dispare — cheia face acum parte din antetul secțiunii.

    Înainte:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    După:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Repetați secțiunea pentru fiecare furnizor și păstrați fiecare cheie identică cu `key` din
    `dashboard_config.toml`. `digna config check` raportează `oidc_clients` ca FAILED cât timp
    forma veche este încă prezentă. Sunt afectate doar instalările care folosesc autentificarea unică.

#### Pasul 5: Reîncărcați web serverul

Dashboard-ul este un set de fișiere statice, așa că web serverul — și browserul — pot servi în continuare
versiunea anterioară. Reîncărcați sau reporniți web serverul care găzduiește folderul `dashboard`,
apoi reîncărcați pagina forțat (++ctrl+f5++).

#### Pasul 6: Validați configurația

Confirmați că `config.toml` actualizat este complet înainte de a atinge repository-ul:

```bash
./digna config check
```

Fiecare secțiune trebuie să raporteze OK. Corectați tot ce este raportat ca FAILED și rulați comanda din nou înainte de a continua.

#### Pasul 7: Înlocuiți fișierul de licență

Fiecare versiune este licențiată separat. Copiați fișierul `license.toml` furnizat de echipa digna pentru
această versiune în directorul de instalare, înlocuindu-l pe cel vechi:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Nu păstrați licența anterioară"

    Un `license.toml` emis pentru o versiune anterioară nu o acoperă pe aceasta, iar fiecare comandă
    care verifică licența — `user`, `inspection`, `repo` — se oprește înainte de a atinge
    repository-ul atunci când verificarea eșuează. Verificați-o înainte de a merge mai departe:

    ```bash
    ./digna license check
    ```

#### Pasul 8: Actualizați schema repository-ului

Accesați directorul de instalare digna și rulați:

```bash
cd /opt/digna
./digna repo upgrade
```

Aceasta actualizează schema PostgreSQL la cea mai recentă versiune, păstrând toate datele existente.

#### Pasul 9: Reporniți serviciile

Dacă rulați ca serviciu systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Dacă rulați manual, reporniți serverul:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Dacă folosiți nginx sau Apache, reîncărcați web serverul respectiv:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

Pe familia RHEL, reaplicați etichetarea SELinux dacă directorul `dashboard` a fost înlocuit:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Pasul 10: Verificați actualizarea

1. Accesați dashboard-ul digna
2. Verificați că interfața se încarcă corect
3. Verificați logurile serverului pentru eventuale erori
4. Treceți pe ODBC fiecare conexiune care nu îl folosea încă, apoi testați toate conexiunile
   — consultați [Testarea unei conexiuni](../../../databases/overview.md#testing-a-connection):

```bash
sudo journalctl -u digna -n 100
```

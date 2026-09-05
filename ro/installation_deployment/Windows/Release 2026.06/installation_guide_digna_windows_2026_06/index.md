# Windows Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** August 30, 2026


---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Setup](#pre-installation-setup)
4. [PostgreSQL Server Setup](#postgresql-server-setup)
5. [Web Server Configuration](#web-server-configuration)
6. [Initial Installation](#initial-installation)
7. [Backend Configuration](#backend-configuration)
8. [Dashboard Configuration](#dashboard-configuration)
9. [Running digna as a Windows Service](#running-digna-as-a-windows-service)
10. [Upgrading to a New Release](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### Despre digna

digna este o platformă completă, bazată pe AI, concepută pentru a optimiza gestionarea calității datelor în diverse medii de date, cum ar fi data warehouses, data lakes și lakehouses. Construită pentru scalabilitate și adaptabilitate, digna abordează provocările moderne ale datelor prin automatizare, monitorizare în timp real și detectare de anomalii.

digna este alcătuită din două componente principale:

- **dignabackend**: motorul principal al aplicației, responsabil cu procesarea datelor și executarea verificărilor de calitate.
- **dignadashboard**: interfață web găzduită pe un web server, care oferă o modalitate prietenoasă de a interacționa cu platforma digna și de a vizualiza metricile de calitate a datelor.

### Noutăți în Release 2026.06

Această versiune aduce capabilități de observabilitate a datelor direct în cod, permițând dezvoltatorilor să monitorizeze calitatea datelor la sursă. Vezi [release notes](http://docs.digna.ai/changelog/Release_202606/) pentru detalii complete.

---

## System Requirements {: #system-requirements }

Înainte de a începe instalarea, asigură-te că sistemul tău îndeplinește următoarele cerințe minime:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server sau Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB spațiu disponibil |
| **Database** | PostgreSQL Server 12 sau versiune superioară |
| **Web Server** | IIS, Apache Tomcat, sau echivalent |

### Opțiuni de instalare a bazei de date

**Dacă PostgreSQL este deja instalat:**
Poți adăuga o bază de date nouă pentru digna pe serverul PostgreSQL existent.

**Dacă instalezi PostgreSQL pe aceeași mașină cu digna:**

!!! info "Specificații recomandate"

    - **Memory**: 32 GB RAM (în loc de 16 GB)
    - **Disk Space**: 50 GB spațiu disponibil (în loc de 10 GB)

    Aceste specificații mai mari acomodează rularea simultană a digna și a bazei de date PostgreSQL.

---

## Pre-Installation Setup {: #pre-installation-setup }

Înainte de instalarea digna, asigură-te că două prerechizite importante sunt pregătite:

1. **PostgreSQL Server** – pentru stocarea metricilor calculate și a datelor de performanță
2. **Web Server** – pentru găzduirea digna Dashboard

Dacă aceste componente nu sunt deja configurate, urmează secțiunile de mai jos pentru a le instala și configura.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### Dacă ai deja PostgreSQL

Dacă PostgreSQL este deja instalat și rulează pe mașina locală sau folosești un PostgreSQL gestionat remote, poți sări la [secțiunea următoare](#web-server-configuration).

### Instalarea PostgreSQL

Urmează pașii de mai jos pentru a instala PostgreSQL pe Windows:

#### Pasul 1: Descarcă PostgreSQL

1. Accesează pagina [PostgreSQL Downloads](https://www.postgresql.org/download/)
2. Selectează **Windows**
3. Descarcă ultimul installer

#### Pasul 2: Rulează installer-ul

1. Dublu-click pe fișierul installer descărcat
2. Urmează indicațiile din wizard-ul de instalare

#### Pasul 3: Alege directorul de instalare

Selectează directorul unde va fi instalat PostgreSQL. Locația implicită este de obicei adecvată.

#### Pasul 4: Selectează componentele

Pentru o configurație standard, păstrează opțiunile implicite selectate.

#### Pasul 5: Setează parola superuser-ului PostgreSQL

Introdu și confirmă o parolă pentru superuser-ul PostgreSQL (`postgres`). **Păstrează această parolă în siguranță** — îți va fi necesară mai târziu.

#### Pasul 6: Configurează numărul portului

Portul implicit PostgreSQL este `5432`. Poți folosi valoarea implicită sau specifica un alt port dacă este necesar.

!!! tip "Sfat"

    Dacă portul 5432 este deja utilizat, alege un port alternativ și notează-l pentru configurările ulterioare.

#### Pasul 7: Alege locale

Selectează locale-ul pentru baza ta de date. Opțiunea implicită este de obicei potrivită pentru majoritatea instalărilor.

#### Pasul 8: Finalizează instalarea

Apasă **Next** prin pașii rămași, apoi **Finish**.

#### Pasul 9: Verifică instalarea

Deschide Command Prompt și verifică că PostgreSQL este instalat:

```bash
psql --version
```

Ar trebui să vezi versiunea PostgreSQL dacă instalarea a fost reușită.

---

## Web Server Configuration {: #web-server-configuration }

digna necesită un web server pentru a găzdui dashboard-ul. Alege una dintre următoarele opțiuni:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Trebuie să instalezi și să configurezi **doar unul** dintre aceste servere.

### IIS Setup {: #iis-setup }

#### Prezentare generală

Internet Information Services (IIS) este web server-ul Microsoft pentru găzduirea site-urilor web și a aplicațiilor web.

#### Activarea IIS

1. **Deschide Control Panel**
   - Apasă `Win + R`
   - Tastează `control` și apasă Enter

2. **Navighează la Windows Features**
   - Click pe **Programs**
   - Selectează **Turn Windows features on or off**

3. **Activează Internet Information Services**
   - Derulează și găsește **Internet Information Services (IIS)**
   - Bifează caseta pentru a-l activa
   - Click pe **+** pentru a extinde și verifică că sunt selectate următoarele subcomponente:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Click OK** pentru a aplica modificările

5. **Verifică instalarea IIS**
   - Deschide browser-ul
   - Navighează la `http://localhost`
   - Ar trebui să vezi pagina de bun venit IIS

#### Obligatoriu: Modulul URL Rewrite

IIS necesită componenta URL Rewrite. Descarcă și instaleaz-o de pe [pagina oficială Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Obligatoriu: MIME Type pentru fișiere Markdown

Pentru a te asigura că fișierele Markdown (`.md`) sunt servite corect de IIS:

1. Deschide **IIS Manager** (apasă `Win + R`, tastează `inetmgr`, apasă Enter)
2. Navighează la **Your Site > MIME Types**
3. Click **Add...**
4. Configurează:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Important"

    Fără această setare, fișierele `.md` s-ar putea să nu fie servite corect.

---

### Apache Tomcat Setup {: #apache-tomcat-setup }

#### Prezentare generală

Apache Tomcat este un container Java servlet open-source și un web server.

#### Instalare

1. **Descarcă Apache Tomcat**
   - Vizitează [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Descarcă distribuția ZIP pentru Windows

2. **Extrage arhiva**
   - Extrage fișierul ZIP într-un director de pe sistemul tău
   - Exemplu: `C:\Program Files\Apache Tomcat`

3. **Verifică că Tomcat rulează**
   - Deschide browser-ul
   - Navighează la `http://localhost:8080`
   - Ar trebui să vezi pagina de bun venit Apache Tomcat

!!! tip "Sfat"

    Apache Tomcat pornește de obicei automat după instalare. Dacă nu pornește, navighează în folderul `bin` și rulează `startup.bat`.

---

## Initial Installation {: #initial-installation }

### Pasul 1: Configurează Repository-ul digna

Repository-ul digna stochează toate metricile calculate de digna. Acesta acționează ca baza de date centrală pentru date analitice și de performanță.

#### Creează schema repository și utilizatorul

Deschide clientul PostgreSQL (pgAdmin, psql sau similar) și execută următoarele comenzi SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Înlocuiește următoarele placeholders:**

- `<digna_repo_schema>` — Numele schema dorit (ex.: `dignarepo`)
- `<digna_repo_user>` — Numele de utilizator dorit (ex.: `digna_user`)
- `<digna_repo_password>` — O parolă securizată pentru acest utilizator

**Exemplu:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Practică recomandată"

    Folosește parole puternice și complexe pentru utilizatorii bazei de date. Evită credențiale ușor de ghicit.

---

### Pasul 2: Extrage pachetul de instalare digna

1. Găsește fișierul ZIP de instalare digna furnizat
2. Extrage-l în locația de instalare dorită
3. După extragere, ar trebui să vezi următoarele elemente:
   - `dashboard/` — interfața web dashboard
   - `digna` — executabilul principal (backend + CLI combinate)
   - `config.toml` — fișierul de configurare
   - `license.toml` — fișierul de licență (copiază al tău aici)

### Pasul 3: Instalează fișierul de licență

!!! warning "Important"

    Fișierul de licență **nu** este inclus în pachetul de instalare și va fi furnizat separat de digna.

1. Găsește fișierul `license.toml` furnizat
2. Copiază-l în directorul rădăcină al instalării digna (unde se află `config.toml` și executabilul `digna`)

**De ce este important:**
Fișierul de licență conține informațiile clientului, data de expirare a licenței și semnătura digitală. **Nu modifica acest fișier** — orice modificare îl va invalida.

**Structura directorului după configurare:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend Configuration {: #backend-configuration }

### Pasul 1: Creează și editează fișierul de configurare

Fișierul `config_template.toml` este furnizat în directorul de instalare digna. Tot ce trebuie să faci este să-l redenumești în `config.toml`.

**Locație:** `digna_installation/config.toml`

Deschide `config.toml` într-un editor de text și configurează fiecare secțiune de mai jos.

#### Secțiunea [app]

Această secțiune configurează setările aplicației backend digna:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` sau adresă IP | Hostname sau IP unde este găzduit dignabackend |
| `digna_APP_PORT` | `8082` (implicit) | Port pentru endpoint-urile REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL-ul frontend-ului | Dacă dashboard-ul este pe un server diferit, include URL-ul acestuia |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Necesare pentru CORS cu credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Permite toate metodele HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Permite toate headerele |

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

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` sau IP | Hostname/IP server PostgreSQL |
| `digna_REPO_PORT` | `5432` (implicit) | Port PostgreSQL |
| `digna_REPO_DB` | `postgres` | Numele bazei de date |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema creată anterior |
| `digna_REPO_USER` | `digna_user` | Utilizator creat în setup-ul PostgreSQL |
| `digna_REPO_PASSWORD` | Parola ta | Parola setată la crearea schema/utilizatorului |

#### Secțiunea [base]

Această secțiune conține setări de securitate și cookie-uri:

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

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | Cheie de criptare | Folosită pentru a cripta token-urile și cookie-urile (implicit este furnizat) |
| `digna_COOKIE_DOMAIN` | `localhost` | Potrivește cu domeniul frontend-ului |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (producție) | Folosește `true` pentru conexiuni HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Activat întotdeauna pentru securitate |
| `digna_COOKIE_SAME_SITE` | `lax` | Previne atacurile CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ore) | Timeout pentru sesiune în secunde |
| `digna_MAX_WORKERS` | Numărul de nuclee CPU - 1 | Numărul de task-uri paralele de inspecție |

#### Secțiunea [logging]

Această secțiune configurează comportamentul de logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` sau `DEBUG` | `INFO` pentru producție, `DEBUG` pentru depanare |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Numărul de backup-uri zilnice de log păstrate |

---

### Pasul 3: Inițializează Repository-ul

1. Deschide Command Prompt
2. Navighează la directorul de instalare digna (unde se află `config.toml` și executabilul `digna`)
3. Rulează testul de conexiune:

```bash
digna repo check
```

Ar trebui să vezi o confirmare că conexiunea este stabilită (repository-ul încă nu a fost inițializat).

### Pasul 4: Instalează schema repository-ului

În același director, rulează:

```bash
digna repo install
```

Această comandă instalează tabelele și schema necesare în baza ta PostgreSQL.

### Pasul 5: Pornește serverul digna

În directorul de instalare digna, pornește serverul cu:

```bash
digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — hostname/IP server
- `--port` — port server

Ar trebui să vezi mesaje de startup care confirmă că serverul rulează:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Pasul 6: Creează un utilizator admin

1. Deschide o fereastră **nouă** Command Prompt
2. Navighează la directorul de instalare digna
3. Rulează următoarea comandă pentru a crea un utilizator admin:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Exemplu:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Aceasta creează un utilizator cu privilegii administrative complete.

!!! tip "Practică recomandată"

    Folosește o parolă puternică cu un mix de majuscule, minuscule, cifre și caractere speciale.

---

## Dashboard Configuration {: #dashboard-configuration }

### Pasul 1: Deploy dashboard-ului pe web server

Dashboard-ul digna are propriul fișier `config.toml` localizat în directorul `dashboard/`. Această configurație este deja furnizată și nu necesită modificări în timpul configurării inițiale. Trebuie să-l modifici doar dacă dorești să personalizezi conexiunea către backend.

Dacă trebuie să modifici configurația dashboard-ului (ex.: pentru deploy multi-instanta), consultă documentația dashboard-ului.

Alege web server-ul tău și urmează pașii de deploy corespunzători.

#### Deploy pe IIS

1. **Deschide IIS Manager**
   - Apasă `Win + R`, tastează `inetmgr`, apasă Enter

2. **Creează un site nou**
   - În panoul din stânga, click dreapta pe **Sites**
   - Selectează **Add Website...**

3. **Configurează site-ul**
   - **Site Name**: Introdu un nume (ex.: "dignaDashboard")
   - **Physical Path**: Click Browse și selectează folderul `dashboard`
   - **Binding**: Setează adresa IP și portul (implicit port 80 pentru HTTP, 443 pentru HTTPS)

4. **Pornește site-ul**
   - Click **OK** pentru a crea site-ul
   - Click dreapta pe site-ul nou și selectează **Start**

5. **Testează instalarea**
   - Deschide browser-ul
   - Navighează la `http://localhost` (sau URL-ul configurat)
   - Ar trebui să vezi pagina de login a dashboard-ului digna

#### Deploy pe Apache Tomcat

1. **Copie dashboard în Tomcat**
   - Copiază folderul `dashboard` în directorul `webapps` al Tomcat
   - Redenumește-l dacă este necesar (ex.: în `digna`)
   - Exemplu: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verifică deploy-ul**
   - Reîmprospătează sau reîncarcă pagina de management Tomcat (http://localhost:8080)
   - Ar trebui să vezi "digna" (sau numele ales) listat în aplicațiile deploy-ate

3. **Accesează dashboard-ul**
   - Deschide browser-ul
   - Navighează la `http://localhost:8080/digna`
   - Ar trebui să vezi pagina de login a dashboard-ului digna

---

## Running digna as a Windows Service {: #running-digna-as-a-windows-service }

### De ce să folosești un serviciu Windows?

Rularea backend-ului digna ca serviciu Windows asigură:
- Pornire automată la boot-ul serverului
- Rulează în background fără un Command Prompt deschis
- Repornire automată în caz de crash
- Poate fi gestionat prin Services din Windows

### Fișiere de management al serviciului

Toate fișierele necesare sunt localizate în directorul de instalare digna, sub: `bin/`

Următoarele fișiere batch sunt disponibile:
- `install_service.bat` — înregistrează digna ca serviciu Windows
- `uninstall_service.bat` — dezînregistrează serviciul
- `start_service.bat` — pornește serviciul
- `stop_service.bat` — oprește serviciul

!!! warning "Administrator necesar"

    Toate fișierele batch trebuie executate cu privilegii de Administrator.

### Instalarea serviciului

1. **Deschide Command Prompt ca Administrator**
   - Click dreapta pe Command Prompt
   - Selectează "Run as Administrator"

2. **Navighează la folderul bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Rulează scriptul de instalare**
   ```bash
   install_service.bat
   ```

Serverul digna este acum înregistrat ca serviciu Windows cu pornire **automatică** activată. Serviciul nu pornește imediat — vezi secțiunea următoare pentru a-l porni.

### Pornirea și oprirea serviciului

#### Pentru a porni serviciul

1. Deschide Command Prompt ca Administrator
2. Navighează la `digna\bin`
3. Rulează:
   ```bash
   start_service.bat
   ```

#### Pentru a opri serviciul

1. Deschide Command Prompt ca Administrator
2. Navighează la `digna\bin`
3. Rulează:
   ```bash
   stop_service.bat
   ```

!!! tip "Sfat"

    Oprește întotdeauna serviciul înainte de a actualiza fișierele aplicației.

### Mutarea serviciului într-un nou director

Dacă trebuie să muți instalarea digna:

1. **Dezinstalează serviciul curent**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Mută fișierele aplicației**
   - Mută întregul folder de instalare digna în noua locație

3. **Reinstalează serviciul**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Pornește serviciul**
   ```bash
   start_service.bat
   ```

### Dezinstalarea serviciului

1. **Oprește serviciul**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Dezinstalează serviciul**
   ```bash
   uninstall_service.bat
   ```

Serverul digna este acum dezînregistrat ca serviciu Windows.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Înainte de upgrade

**Crearea unui backup al digna Repository este obligatorie**

Înainte de a face upgrade la digna, fă backup la repository-ul tău (PostgreSQL) pentru a te proteja împotriva pierderii de date.
Un backup îți permite recuperarea dacă upgrade-ul întâmpină probleme neașteptate.

### Procesul de upgrade

#### Pasul 1: Oprește serviciul digna

Dacă digna rulează ca serviciu Windows, oprește-l mai întâi:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Pasul 2: Fă backup instalației curente a backend-ului

În directorul tău de instalare digna:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Pasul 3: Extrage și deploy noua versiune

1. Extrage noul fișier ZIP de instalare digna
2. Copiază noul executabil `digna` și folderul `dashboard` în directorul tău de instalare

!!! warning "Important"

    Fișierul `config.toml` **nu** este niciodată inclus în ZIP-ul de instalare. Configurația ta existentă rămâne în siguranță.

### Pasul 4: Restaurează fișierele de configurație

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Pasul 5: Upgrade schema repository-ului

Navighează la directorul de instalare digna și rulează:

```bash
digna repo upgrade
```

Aceasta actualizează schema PostgreSQL la versiunea cea mai recentă, păstrând toate datele existente.

### Pasul 6: Repornirea serviciilor

Dacă rulezi ca serviciu Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Dacă rulezi manual, repornește serverul:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Dacă folosești IIS sau Tomcat, repornește web server-ul corespunzător.

#### Pasul 7: Verifică upgrade-ul

1. Accesează dashboard-ul digna
2. Verifică că interfața se încarcă corect
3. Verifică log-urile serverului pentru eventuale erori
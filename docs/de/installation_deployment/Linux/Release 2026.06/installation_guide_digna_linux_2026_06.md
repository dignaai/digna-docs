---
title: Linux Installationsanleitung – digna Release 2026.06 | digna Dokumentation
description: Schritt-für-Schritt-Anleitung zur Installation von digna Release 2026.06 unter Linux — Systemanforderungen, PostgreSQL-Einrichtung, nginx- oder Apache-Konfiguration, Backend- und Dashboard-Konfiguration, Ausführen von digna als systemd-Dienst und Upgrade auf eine neue Version.
keywords: digna linux installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql linux, nginx linux, digna systemd service, digna upgrade guide
image: /assets/logo_square.png
---

# Linux Installationsanleitung für digna Release 2026.06

**Release:** 2026.06

**Zuletzt aktualisiert:** 5. September 2026


---

## Inhaltsverzeichnis

1. [Einführung](#introduction)
2. [Systemanforderungen](#system-requirements)
3. [Vorbereitungen vor der Installation](#pre-installation-setup)
4. [PostgreSQL-Server Einrichtung](#postgresql-server-setup)
5. [Webserver-Konfiguration](#web-server-configuration)
6. [Erstinstallation](#initial-installation)
7. [Backend-Konfiguration](#backend-configuration)
8. [Dashboard-Konfiguration](#dashboard-configuration)
9. [digna als systemd-Dienst betreiben](#running-digna-as-a-systemd-service)
10. [Upgrade auf eine neue Version](#upgrading-to-a-new-release)

---

## Einführung {: #introduction }

### Über digna

digna ist eine umfassende, KI-gestützte Plattform zur Optimierung des Datenqualitätsmanagements in unterschiedlichen Datenumgebungen wie Data Warehouses, Data Lakes und Lakehouses. digna wurde hochskalierbar und anpassungsfähig entwickelt und adressiert moderne Datenherausforderungen durch Automatisierung, Echtzeit-Überwachung und Anomalieerkennung.

digna besteht aus zwei Hauptkomponenten:

- **dignabackend**: Die Kern-Engine der Anwendung, verantwortlich für die Datenverarbeitung und Durchführung von Qualitätsprüfungen.
- **dignadashboard**: Eine webbasierte Oberfläche, die auf einem Webserver gehostet wird und eine benutzerfreundliche Möglichkeit bietet, mit der digna-Plattform zu interagieren und Datenqualitätsmetriken zu visualisieren.

### Neu in Release 2026.06

Dieses Release bringt Data-Observability-Funktionen direkt in Ihren Code und ermöglicht Entwicklern, die Datenqualität an der Quelle zu überwachen. Details finden Sie in den [Release Notes](http://docs.digna.ai/changelog/Release_202606/).

### Suchen Sie nach Windows oder macOS?

Diese Anleitung behandelt Linux. Für andere Plattformen siehe die [Windows Installationsanleitung](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) oder die [macOS Installationsanleitung](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

### Für welche Distribution ist diese Anleitung geschrieben?

Die Anweisungen sind für die zwei gebräuchlichsten Serverfamilien formuliert. Wo sie abweichen, werden beide Befehle angegeben:

- **Debian-Familie** — Debian, Ubuntu. Paketmanager: `apt`.
- **RHEL-Familie** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Paketmanager: `dnf`.

Jede moderne Distribution mit `systemd` funktioniert; nur Paketnamen und einige Konfigurationspfade ändern sich.

---

## Systemanforderungen {: #system-requirements }

Bevor Sie mit der Installation beginnen, vergewissern Sie sich, dass Ihr System die folgenden Mindestanforderungen erfüllt:

| Anforderung | Spezifikation |
|---|---|
| **Betriebssystem** | Ubuntu 22.04 LTS oder neuer, Debian 12 oder neuer, RHEL 9 / Rocky 9 / AlmaLinux 9 oder neuer |
| **Architektur** | x86_64 (amd64) oder arm64 |
| **Init-System** | systemd |
| **Arbeitsspeicher (Minimale Einrichtung)** | 16 GB RAM |
| **Festplattenspeicher** | 10 GB verfügbarer Speicher |
| **Datenbank** | PostgreSQL Server 12 oder höher |
| **Webserver** | nginx, Apache httpd oder äquivalent |

### Optionen zur Datenbankinstallation

**Wenn PostgreSQL bereits installiert ist:**
Sie können auf Ihrem vorhandenen PostgreSQL-Server eine neue Datenbank für digna anlegen.

**Wenn PostgreSQL auf derselben Maschine wie digna installiert werden soll:**

!!! info "Empfohlene Spezifikationen"

    - **Arbeitsspeicher**: 32 GB RAM (anstatt 16 GB)
    - **Festplattenspeicher**: 50 GB verfügbarer Speicher (anstatt 10 GB)

    Diese höheren Spezifikationen berücksichtigen, dass sowohl digna als auch die PostgreSQL-Datenbank gleichzeitig laufen.

### Überprüfung von Distribution und Architektur

Mehrere Befehle in dieser Anleitung unterscheiden sich zwischen der Debian- und der RHEL-Familie. Zur Kontrolle, welche Sie verwenden, führen Sie aus:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` oder `ID=debian` — verwenden Sie die `apt`-Befehle.
- `ID=rhel`, `rocky`, `almalinux` oder `fedora` — verwenden Sie die `dnf`-Befehle.
- `x86_64` oder `aarch64` — die Architektur des Installationspakets, das Sie benötigen.

---

## Vorbereitungen vor der Installation {: #pre-installation-setup }

Bevor Sie digna installieren, stellen Sie sicher, dass zwei Voraussetzungen erfüllt sind:

1. **PostgreSQL-Server** – zur Speicherung berechneter Metriken und Leistungsdaten
2. **Webserver** – zum Hosten des digna Dashboards

Wenn diese Komponenten noch nicht eingerichtet sind, folgen Sie den untenstehenden Abschnitten, um sie zu installieren und zu konfigurieren.

### Paketindex aktualisieren

Aktualisieren Sie Ihre Paketlisten, bevor Sie etwas installieren:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Hinweis"

    In dieser Anleitung ist der erste Befehl in einem Paar für die **Debian-Familie** und der zweite für die **RHEL-Familie** gedacht. Führen Sie nur denjenigen aus, der zu Ihrem System passt.

---

## PostgreSQL-Server Einrichtung {: #postgresql-server-setup }

### Falls PostgreSQL bereits vorhanden ist

Wenn PostgreSQL bereits lokal installiert und gestartet ist oder Sie einen verwalteten Remote-PostgreSQL-Server verwenden, können Sie zum [nächsten Abschnitt](#web-server-configuration) springen.

### PostgreSQL installieren

#### Schritt 1: Serverpaket installieren

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Tipp"

    Distribution-Pakete können hinter der aktuellen PostgreSQL-Version zurückbleiben. Wenn Sie eine spezifischere, neuere Version benötigen, verwenden Sie alternativ das offizielle [PostgreSQL apt- oder yum-Repository](https://www.postgresql.org/download/linux/).

#### Schritt 2: Datenbank-Cluster initialisieren

Bei der **Debian-Familie** erstellt und startet das Paket den Cluster automatisch — springen Sie zum nächsten Schritt.

Bei der **RHEL-Familie** muss der Cluster explizit erstellt werden:

```bash
sudo postgresql-setup --initdb
```

#### Schritt 3: Dienst starten und aktivieren

```bash
sudo systemctl enable --now postgresql
```

Dies startet PostgreSQL sofort und konfiguriert es so, dass es beim Booten automatisch erneut startet.

#### Schritt 4: Installation überprüfen

```bash
psql --version
sudo systemctl status postgresql
```

Sie sollten die PostgreSQL-Version sowie einen `active (running)` Dienst sehen.

#### Schritt 5: Verbindung zum Server herstellen

Ein Linux-PostgreSQL-Paket legt ein Systemkonto `postgres` an, dem der Cluster gehört. Melden Sie sich darüber an:

```bash
sudo -u postgres psql
```

!!! note "Hinweis — Linux unterscheidet sich hier von Windows"

    Der Windows-Installer fordert Sie während der Installation auf, ein Passwort für den Superuser `postgres` zu setzen. Linux-Pakete tun dies nicht. Stattdessen erfolgt die Authentifizierung lokaler Verbindungen über **peer authentication**: Der Betriebssystembenutzer `postgres` darf ohne Passwort als Datenbankbenutzer `postgres` verbinden.

    Daher verwendet der obenstehende Befehl `sudo -u postgres`. Das digna Backend verbindet sich über TCP mit Benutzername und Passwort, daher erstellen Sie in der [Erstinstallation](#initial-installation) explizit einen digna-Benutzer.

#### Schritt 6: Port bestätigen

Der Standardport von PostgreSQL ist `5432`. Um zu bestätigen, auf welchem Port Ihr Server lauscht:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Notieren Sie den Wert — Sie benötigen ihn bei der Konfiguration des digna-Backends.

#### Schritt 7: Passwortauthentifizierung für den digna-Benutzer aktivieren

digna verbindet sich per TCP als `digna_user`, was Passwortauthentifizierung erfordert statt Peer-Authentifizierung. Prüfen Sie, ob Ihre `pg_hba.conf` dies erlaubt.

Datei lokalisieren:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Öffnen Sie sie in einem Editor und bestätigen Sie, dass die lokalen TCP-Zeilen `scram-sha-256` (oder `md5` bei älteren Servern) statt `ident` verwenden:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Starten Sie PostgreSQL nach jeder Änderung neu:

```bash
sudo systemctl reload postgresql
```

!!! warning "Wichtig"

    Falls digna meldet `FATAL: Ident authentication failed for user "digna_user"`, ist diese Einstellung die Ursache.

#### Schritt 8: Wenn PostgreSQL auf einem anderen Rechner läuft

Um Verbindungen von einem anderen Host zu akzeptieren, setzen Sie `listen_addresses` in `postgresql.conf` und fügen Sie eine passende `host`-Zeile für Ihr Netzwerk in `pg_hba.conf` hinzu:

```
listen_addresses = '*'
```

Öffnen Sie dann die Portfreigabe in der Firewall und starten Sie den Dienst neu:

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

## Webserver-Konfiguration {: #web-server-configuration }

digna benötigt einen Webserver zum Hosten des Dashboards. Wählen Sie eine der folgenden Optionen:

- [nginx](#nginx-setup) — leichtgewichtig und empfohlen
- [Apache httpd](#apache-setup) — weit verbreitete Alternative

Sie müssen nur einen dieser Server installieren und konfigurieren.

Beide Abschnitte konfigurieren zwei Dinge, von denen das Dashboard abhängt:

- **Fallback für Single-Page-Application**, damit das Neuladen einer Dashboard-URL kein 404 zurückgibt
- **MIME-Typ für `.md`**, damit Markdown-Dateien korrekt ausgeliefert werden

### nginx Einrichtung {: #nginx-setup }

#### Überblick

nginx ist ein leichtgewichtiger, leistungsfähiger Webserver, der sich gut zum Ausliefern des statischen digna-Dashboards eignet.

#### Installation

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginx starten

```bash
sudo systemctl enable --now nginx
```

#### Installation verifizieren

1. Öffnen Sie Ihren Browser
2. Navigieren Sie zu `http://localhost`
3. Sie sollten die nginx-Willkommensseite sehen

#### Firewall öffnen

Wenn der Server von anderen Maschinen aus erreichbar ist, erlauben Sie HTTP-Verkehr:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Site für das Dashboard konfigurieren

nginx lädt alle Dateien in seinem `conf.d`-Verzeichnis in beiden Distributionen ein. Erstellen Sie dort eine eigene Konfigurationsdatei für digna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Fügen Sie Folgendes ein und ersetzen Sie `/opt/digna/dashboard` durch den tatsächlichen Pfad zu Ihrem entpackten `dashboard`-Ordner:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
    index  index.html;

    # Markdown-Dateien mit dem korrekten MIME-Typ ausliefern.
    types {
        text/markdown  md;
    }

    # Single-Page-Application-Fallback: unbekannte Pfade liefern index.html
    # statt eines 404, damit Dashboard-Routen beim Browser-Refresh erhalten bleiben.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Wichtig"

    Ohne die `try_files`-Direktive führt das Neuladen einer beliebigen Dashboard-Seite außer der Root-URL zu einem 404. Dies ist das nginx-Äquivalent zum URL-Rewrite-Modul, das unter IIS auf Windows erforderlich ist.

#### Standardseite deaktivieren

Nur ein Server-Block darf `default_server` für einen Port sein. In der **Debian-Familie** entfernen Sie die mitgelieferte Default-Site, damit sie nicht in Konflikt gerät:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

In der **RHEL-Familie** kommentieren Sie den `server { ... }`-Block in `/etc/nginx/nginx.conf` aus oder löschen ihn.

#### Konfiguration anwenden

Prüfen Sie die Konfiguration auf Syntaxfehler und laden Sie nginx neu:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd Einrichtung {: #apache-setup }

#### Überblick

Apache httpd ist in den Standard-Repositories jeder unterstützten Distribution verfügbar. Das Paket heißt `apache2` in der Debian-Familie und `httpd` in der RHEL-Familie.

#### Installation

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apache starten

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Installation verifizieren

1. Öffnen Sie Ihren Browser
2. Navigieren Sie zu `http://localhost`
3. Sie sollten die standardmäßige Apache-Seite Ihrer Distribution sehen

#### Erforderlich: mod_rewrite aktivieren

Das Dashboard benötigt URL-Rewriting.

In der **Debian-Familie** aktivieren Sie das Modul und starten neu:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

In der **RHEL-Familie** ist `mod_rewrite` standardmäßig geladen. Prüfen Sie es:

```bash
httpd -M | grep rewrite
```

#### Erforderlich: .htaccess-Overrides erlauben

Öffnen Sie die Konfigurationsdatei für Ihre Document-Root:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Finden Sie den `<Directory>`-Block, der Ihre Document-Root abdeckt (`/var/www/html` bei beiden Familien) und ändern Sie:

```apache
AllowOverride None
```

zu:

```apache
AllowOverride All
```

#### Erforderlich: MIME-Typ für Markdown-Dateien

Fügen Sie in derselben Datei die folgende Zeile hinzu, damit Markdown-Dateien korrekt ausgeliefert werden:

```apache
AddType text/markdown .md
```

!!! warning "Wichtig"

    Ohne diese Einstellung werden `.md`-Dateien möglicherweise nicht korrekt ausgeliefert.

#### Konfiguration anwenden

Prüfen Sie die Konfiguration auf Syntaxfehler und starten Sie Apache neu:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Erstinstallation {: #initial-installation }

### Schritt 1: Repository für digna einrichten

Das digna-Repository speichert alle von digna berechneten Metriken. Es fungiert als zentrale Datenbank für Analyse- und Leistungsdaten.

#### Schema und Benutzer für das Repository anlegen

Öffnen Sie Ihren PostgreSQL-Client (psql, pgAdmin oder ähnliches) und führen Sie die folgenden SQL-Anweisungen aus:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Ersetzen Sie die folgenden Platzhalter:**

- `<digna_repo_schema>` — gewünschter Schema-Name (z. B. `dignarepo`)
- `<digna_repo_user>` — gewünschter Benutzername (z. B. `digna_user`)
- `<digna_repo_password>` — ein sicheres Passwort für diesen Benutzer

**Beispiel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Um diese Befehle aus der Shell in einem Schritt auszuführen:

```bash
sudo -u postgres psql
```

Dann fügen Sie die Statements an der Eingabeaufforderung `postgres=#` ein und tippen `\q`, um zu beenden.

!!! tip "Best Practice"

    Verwenden Sie starke, komplexe Passwörter für Datenbankbenutzer. Vermeiden Sie leicht zu erratende Zugangsdaten.

---

### Schritt 2: digna-Installationspaket entpacken

1. Lokalisieren Sie die Ihnen bereitgestellte digna-Installations-ZIP-Datei
2. Entpacken Sie sie an Ihren gewünschten Installationsort — z. B. `/opt/digna`
3. Nach dem Entpacken sollten folgende Elemente vorhanden sein:
   - `dashboard/` — Web-Dashboard-Oberfläche
   - `digna` — Haupt-Executable (Backend + CLI kombiniert)
   - `config.toml` — Konfigurationsdatei
   - `license.toml` — Lizenzdatei (kopieren Sie Ihre hierhin)

Um aus der Shell zu entpacken:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Hinweis"

    Falls `unzip` nicht installiert ist, installieren Sie es mit `sudo apt install -y unzip` oder `sudo dnf install -y unzip`.

#### Executable ausführbar machen

Je nach Übertragungsmethode bleibt das Ausführungsbit eventuell nicht erhalten. Setzen Sie es explizit:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Service-Account anlegen

Es wird empfohlen, das Backend als dedizierten, unprivilegierten Benutzer im Produktivbetrieb auszuführen:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Hinweis"

    In der RHEL-Familie lautet der äquivalente Shell-Pfad `/sbin/nologin`.

### Schritt 3: Lizenzdatei installieren

!!! warning "Wichtig"

    Die Lizenzdatei ist **nicht** im Installationspaket enthalten und wird separat von digna bereitgestellt.

1. Lokalisieren Sie die Ihnen bereitgestellte `license.toml`
2. Kopieren Sie sie in das Root-Installationsverzeichnis von digna (dort, wo `config.toml` und die `digna`-Executable liegen)

**Warum das wichtig ist:**
Die Lizenzdatei enthält Ihre Kundeninformationen, Ablaufdatum der Lizenz und die digitale Signatur. **Ändern Sie diese Datei nicht** — jegliche Modifikation macht sie ungültig.

**Verzeichnisstruktur nach der Einrichtung:**

```
/opt/digna/
├── config.toml         (Konfigurationsdatei)
├── license.toml        (IHRE LIZENZDATEI - hierher kopieren)
├── digna               (Haupt-Executable)
├── bin/                (Skripte zur Dienstverwaltung)
└── dashboard/          (Web-Oberfläche)
    └── (Dashboard-Dateien)
```

---

## Backend-Konfiguration {: #backend-configuration }

### Schritt 1: Konfigurationsdatei anlegen und bearbeiten

Die Datei `config_template.toml` ist in Ihrem digna-Installationsverzeichnis vorhanden. Benennen Sie sie einfach in `config.toml` um.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Pfad:** `/opt/digna/config.toml`

Öffnen Sie `config.toml` in einem Texteditor und konfigurieren Sie die folgenden Abschnitte.

#### [app] Abschnitt

Dieser Abschnitt konfiguriert die Anwendungen des digna-Backends:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `digna_APP_HOST` | `localhost` oder IP-Adresse | Hostname oder IP, auf dem dignabackend gehostet wird |
| `digna_APP_PORT` | `8082` (Standard) | Port für die REST-API-Endpunkte |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Falls das Dashboard auf einem anderen Server läuft, fügen Sie dessen URL hinzu |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Erforderlich für CORS mit Credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Erlaubt alle HTTP-Methoden |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Erlaubt alle Header |

!!! note "Hinweis"

    Wenn Sie das Dashboard per nginx oder Apache auf dem Standard-HTTP-Port ausliefern, ist die Origin, die Sie erlauben sollten, `http://localhost` — oder die öffentliche URL des Servers, wenn das Dashboard von anderen Maschinen erreicht wird.

#### [repo] Abschnitt

Dieser Abschnitt konfiguriert die Verbindung zur PostgreSQL-Datenbank:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `digna_REPO_HOST` | `localhost` oder IP | PostgreSQL-Server Hostname/IP |
| `digna_REPO_PORT` | `5432` (Standard) | PostgreSQL-Port |
| `digna_REPO_DB` | `postgres` | Datenbankname |
| `digna_REPO_SCHEMA` | `dignarepo` | Früher erstelltes Schema |
| `digna_REPO_USER` | `digna_user` | In PostgreSQL angelegter Benutzer |
| `digna_REPO_PASSWORD` | Ihr Passwort | Beim Anlegen des Schemas gesetztes Passwort |

!!! tip "Best Practice"

    `config.toml` enthält ein Datenbankpasswort im Klartext. Beschränken Sie die Berechtigungen so, dass nur das Service-Konto lesend darauf zugreifen kann:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] Abschnitt

Dieser Abschnitt enthält Sicherheits- und Cookie-Einstellungen:

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

| Parameter | Wert | Hinweise |
|---|---|---|
| `digna_FERNET_KEY` | Verschlüsselungs-Schlüssel | Wird zum Verschlüsseln von Tokens und Cookies verwendet (Standard wird bereitgestellt) |
| `digna_COOKIE_DOMAIN` | `localhost` | Passen Sie dies an Ihre Frontend-Domain an |
| `digna_COOKIE_SECURE` | `false` (lokal) / `true` (Produktiv) | Setzen Sie `true` für HTTPS-Verbindungen |
| `digna_COOKIE_HTTPONLY` | `true` | Aus Sicherheitsgründen stets aktiviert |
| `digna_COOKIE_SAME_SITE` | `lax` | Verhindert CSRF-Angriffe |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 Stunden) | Session-Timeout in Sekunden |
| `digna_MAX_WORKERS` | Anzahl der CPU-Kerne - 1 | Anzahl paralleler Inspektionsaufgaben |

!!! tip "Tipp"

    Um die Anzahl der verfügbaren CPU-Kerne auf Ihrem Server zu ermitteln, führen Sie `nproc` aus.

#### [logging] Abschnitt

Dieser Abschnitt konfiguriert das Logging-Verhalten:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` oder `DEBUG` | `INFO` für den Produktivbetrieb, `DEBUG` zur Fehlerbehebung |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Anzahl der täglichen Log-Backups, die aufbewahrt werden sollen |

---

### Schritt 2: Repository initialisieren

1. Öffnen Sie ein Terminal
2. Wechseln Sie in Ihr digna-Installationsverzeichnis (dort, wo `config.toml` und die `digna`-Executable liegen)
3. Führen Sie den Verbindungs-Test aus:

```bash
cd /opt/digna
./digna repo check
```

Sie sollten eine Bestätigung sehen, dass die Verbindung hergestellt wurde (das Repository selbst ist noch nicht initialisiert).

!!! note "Hinweis"

    Unter Linux ist das aktuelle Verzeichnis nicht in Ihrem PATH, daher wird die Executable als `./digna` und nicht als `digna` aufgerufen. Um die kurze Form überall zu verwenden, legen Sie einen symbolischen Link an:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Schritt 3: Repository-Schema installieren

Führen Sie im selben Verzeichnis aus:

```bash
./digna repo install
```

Dieser Befehl legt die benötigten Tabellen und das Schema in Ihrer PostgreSQL-Datenbank an.

### Schritt 4: digna-Server starten

Starten Sie im digna-Installationsverzeichnis den Server mit:

```bash
./digna serve --address <host> --port <port>
```

**Parameter:**
- `--address` — Server-Hostname/IP
- `--port` — Server-Port

Sie sollten Startmeldungen sehen, die bestätigen, dass der Server läuft:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Tipp"

    Wenn das Dashboard von einer anderen Maschine als dem Backend gehostet wird, öffnen Sie auch den API-Port in der Firewall:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Schritt 5: Admin-Benutzer anlegen

1. Öffnen Sie ein **neues** Terminalfenster
2. Wechseln Sie in Ihr digna-Installationsverzeichnis
3. Führen Sie folgenden Befehl aus, um einen Admin-Benutzer anzulegen:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Beispiel:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Dies legt einen Benutzer mit dem Benutzernamen `admin` und vollen administrativen Rechten an.

!!! tip "Tipp"

    Setzen Sie das Passwort in einfache Anführungszeichen. `bash` und `zsh` behandeln Zeichen wie `!`, `$` und `*` speziell; ein ungequoted Passwort mit diesen Zeichen wird nicht wie eingegeben übergeben.

!!! tip "Best Practice"

    Verwenden Sie ein starkes Passwort mit einer Mischung aus Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen.

---

## Dashboard-Konfiguration {: #dashboard-configuration }

### Schritt 1: Dashboard auf dem Webserver bereitstellen

Das digna-Dashboard hat eine eigene `config.toml` im `dashboard/`-Verzeichnis. Diese Konfiguration ist bereits vorhanden und muss während der Erstinstallation nicht geändert werden. Sie müssen sie nur anpassen, falls Sie die Backend-Verbindung modifizieren möchten.

Wenn Sie die Dashboard-Konfiguration (z. B. für Multi-Instance-Deployments) anpassen müssen, konsultieren Sie die Dokumentation des Dashboards.

Wählen Sie Ihren Webserver und folgen Sie den entsprechenden Deployment-Schritten.

#### Deployment mit nginx

Falls Sie dem Abschnitt [nginx Setup](#nginx-setup) gefolgt sind, verweist der Server-Block bereits auf Ihren `dashboard`-Ordner und es ist kein Kopieren erforderlich.

1. **Pfad bestätigen**
   - Öffnen Sie `/etc/nginx/conf.d/digna.conf`
   - Vergewissern Sie sich, dass `root` auf Ihren entpackten `dashboard`-Ordner zeigt

2. **Stellen Sie sicher, dass der Ordner lesbar ist**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **nginx neu laden**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Installation testen**
   - Öffnen Sie Ihren Browser
   - Navigieren Sie zu `http://localhost` (oder Ihrer konfigurierten URL)
   - Sie sollten die Login-Seite des digna-Dashboards sehen

#### Deployment mit Apache httpd

1. **Dashboard in das Document Root kopieren**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Rewrite-Regeln hinzufügen**

   Erstellen Sie eine `.htaccess`-Datei im bereitgestellten Ordner, damit Dashboard-Routen beim Browser-Refresh erhalten bleiben:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Fügen Sie Folgendes ein:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Bestehende Dateien und Verzeichnisse unverändert ausliefern.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Alles andere fällt auf den Single-Page-Application-Einstiegspunkt zurück.
   RewriteRule ^ index.html [L]
   ```

3. **Apache neu starten**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Auf das Dashboard zugreifen**
   - Öffnen Sie Ihren Browser
   - Navigieren Sie zu `http://localhost/digna`
   - Sie sollten die Login-Seite des digna-Dashboards sehen

### Schritt 2: SELinux (nur RHEL-Familie)

Unter RHEL, Rocky, AlmaLinux und Fedora ist SELinux standardmäßig im Enforcing-Modus aktiv und blockiert den Webserver eventuell beim Lesen von Dateien außerhalb der erwarteten Pfade. Prüfen Sie den Status:

```bash
getenforce
```

Ergibt die Abfrage `Enforcing` und Sie bedienen das Dashboard aus `/opt/digna/dashboard`, labeln Sie das Verzeichnis so, dass der Webserver darauf zugreifen darf:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Hinweis"

    Falls `semanage` nicht gefunden wird, installieren Sie es mit `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Wichtig"

    Ein Dashboard, das auf einem frisch konfigurierten RHEL-Server **403 Forbidden** zurückgibt, liegt fast immer an einem SELinux-Labeling-Problem und selten an Dateiberechtigungen. Prüfen Sie mit `sudo ausearch -m avc -ts recent`.

---

## digna als systemd-Dienst betreiben {: #running-digna-as-a-systemd-service }

### Warum digna als Dienst betreiben?

Das Ausführen des digna-Backends als systemd-Dienst stellt sicher, dass es:

- beim Hochfahren des Rechners automatisch startet
- im Hintergrund läuft, ohne ein offenes Terminalfenster
- bei Absturz automatisch neugestartet wird
- über `systemctl` verwaltet werden kann, dem Standard-Service-Manager unter Linux

### Service-Management-Dateien

Alle benötigten Dateien befinden sich im digna-Installationsverzeichnis unter: `bin/`

Folgende Shell-Skripte sind verfügbar:

- `install_service.sh` — registriert digna bei systemd
- `uninstall_service.sh` — entfernt die Registrierung des Dienstes
- `start_service.sh` — startet den registrierten Dienst
- `stop_service.sh` — stoppt den laufenden Dienst

!!! warning "Root-Rechte erforderlich"

    Alle Skripte müssen mit `sudo` ausgeführt werden, da das Registrieren eines Dienstes, der beim Booten startet, eine Unit-Datei in `/etc/systemd/system` schreibt.

### Skripte ausführbar machen

Beim Entpacken kann das Ausführungsbit verloren gehen. Vor der ersten Nutzung:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Dienst installieren

1. **Terminal öffnen**

2. **Ins bin-Verzeichnis wechseln**
   ```bash
   cd /opt/digna/bin
   ```

3. **Installationsskript ausführen**
   ```bash
   sudo ./install_service.sh
   ```

Der digna-Server ist nun bei systemd mit aktivierter automatischer Startoption registriert. Der Dienst startet nicht automatisch sofort — siehe den nächsten Abschnitt zum Starten.

### Dienst starten und stoppen

#### Dienst starten

1. Terminal öffnen
2. In `/opt/digna/bin` wechseln
3. Ausführen:
   ```bash
   sudo ./start_service.sh
   ```

#### Dienst stoppen

1. Terminal öffnen
2. In `/opt/digna/bin` wechseln
3. Ausführen:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tipp"

    Stoppen Sie den Dienst immer, bevor Sie Anwendungsdateien aktualisieren.

### Verwaltung des Dienstes mit systemctl

Nach der Registrierung kann der Dienst auch mit den Standard-systemd-Befehlen aus jedem Verzeichnis gesteuert werden:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Dienst verifizieren

Um zu bestätigen, dass der Dienst registriert ist und läuft:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` bedeutet, dass der Dienst beim Booten startet; `active` bedeutet, dass er derzeit läuft.

### Service-Logs anzeigen

systemd erfasst alles, was das Backend auf die Konsole schreibt. Zum Lesen:

```bash
sudo journalctl -u digna -n 100
```

Um das Log live zu verfolgen, während Sie ein Problem reproduzieren:

```bash
sudo journalctl -u digna -f
```

!!! tip "Tipp"

    Dies ist der schnellste Weg, ein Problem zu diagnostizieren, bei dem der Dienst sofort nach dem Start wieder stoppt. Eine fehlende Repository-Verbindung oder eine fehlende `license.toml` wird hier gemeldet.

### Installation an einen neuen Pfad verschieben

Die Unit-Datei speichert den absoluten Pfad zur Executable, daher erfordert eine Verlagerung der Installation eine Neu-Registrierung des Dienstes:

1. **Aktuellen Dienst deinstallieren**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Anwendungsdateien verschieben**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Dienst neu installieren**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Dienst starten**
   ```bash
   sudo ./start_service.sh
   ```

### Dienst deinstallieren

1. **Laufenden Dienst stoppen**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Dienst deinstallieren**
   ```bash
   sudo ./uninstall_service.sh
   ```

Der digna-Server ist nun von systemd abgemeldet.

---

## Upgrade auf eine neue Version {: #upgrading-to-a-new-release }

### Bevor Sie ein Upgrade durchführen

**Ein Backup des digna-Repositorys ist verpflichtend**

Erstellen Sie vor einem Upgrade von digna ein Backup Ihres Repositorys (PostgreSQL), um Datenverlust zu vermeiden.
Ein Backup stellt sicher, dass Sie im Falle unerwarteter Probleme bei einem Upgrade wiederherstellen können.

Um ein Backup aus der Shell zu erstellen:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Upgrade-Ablauf

#### Schritt 1: digna-Dienst stoppen

Wenn digna als systemd-Dienst läuft, stoppen Sie ihn zuerst:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Falls digna im Vordergrund läuft, drücken Sie in dessen Terminalfenster `Ctrl + C`.

#### Schritt 2: Aktuelle Backend-Installation sichern

Im digna-Installationsverzeichnis:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Schritt 3: Neue Version entpacken und bereitstellen

1. Entpacken Sie die neue digna-Installations-ZIP-Datei
2. Kopieren Sie die neue `digna`-Executable und den `dashboard`-Ordner in Ihr Installationsverzeichnis
3. Stellen Sie das Executable-Bit und den Besitz durch das Service-Konto wieder her:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Wichtig"

    Die `config.toml`-Datei ist **niemals** in der Installations-ZIP enthalten. Ihre bestehende Konfiguration bleibt erhalten.

### Schritt 4: Konfigurationsdateien wiederherstellen

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Schritt 5: Repository-Schema upgraden

Wechseln Sie in Ihr digna-Installationsverzeichnis und führen Sie aus:

```bash
cd /opt/digna
./digna repo upgrade
```

Dies aktualisiert das PostgreSQL-Schema auf die neueste Version und bewahrt alle vorhandenen Daten.

### Schritt 6: Dienste neu starten

Wenn digna als systemd-Dienst läuft:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Wenn Sie es manuell betreiben, starten Sie den Server neu:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Wenn Sie nginx oder Apache verwenden, laden Sie den jeweiligen Webserver neu:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

Auf der RHEL-Familie wenden Sie die SELinux-Labels erneut an, falls das `dashboard`-Verzeichnis ersetzt wurde:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Schritt 7: Upgrade verifizieren

1. Rufen Sie das digna-Dashboard auf
2. Prüfen Sie, ob die Oberfläche korrekt geladen wird
3. Überprüfen Sie die Server-Logs auf Fehler:

```bash
sudo journalctl -u digna -n 100
```
---
title: macOS Installationsanleitung – digna Release 2026.06 | digna Dokumentation
description: Schritt-für-Schritt-Anleitung zur Installation von digna Release 2026.06 auf macOS — Systemanforderungen, Homebrew- und PostgreSQL-Einrichtung, nginx- oder Apache-Konfiguration, Backend- und Dashboard-Konfiguration, Ausführung von digna als Hintergrunddienst und Upgrade auf eine neue Version.
keywords: digna macOS Installation, digna macOS Deployment-Anleitung, digna Backend-Einrichtung, digna Dashboard-Installation, postgresql homebrew, nginx macOS, digna launchd Dienst, digna Upgrade-Anleitung
image: /assets/logo_square.png
---

# macOS Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** September 5, 2026


---

## Inhaltsverzeichnis

1. [Einführung](#introduction)
2. [Systemanforderungen](#system-requirements)
3. [Vorbereitungen vor der Installation](#pre-installation-setup)
4. [PostgreSQL-Server einrichten](#postgresql-server-setup)
5. [Webserver-Konfiguration](#web-server-configuration)
6. [Erstinstallation](#initial-installation)
7. [Backend-Konfiguration](#backend-configuration)
8. [Dashboard-Konfiguration](#dashboard-configuration)
9. [digna als Hintergrunddienst ausführen](#running-digna-as-a-background-service)
10. [Upgrade auf eine neue Version](#upgrading-to-a-new-release)

---

## Einführung {: #introduction }

### Über digna

digna ist eine umfassende, KI-gestützte Plattform zur Optimierung des Datenqualitätsmanagements in unterschiedlichen Datenumgebungen wie Warehouses, Lakes und Lakehouses. Entwickelt für hohe Skalierbarkeit und Anpassungsfähigkeit, adressiert digna moderne Datenherausforderungen durch Automatisierung, Echtzeit-Überwachung und Anomalieerkennung.

digna besteht aus zwei Hauptkomponenten:

- **dignabackend**: Die Kern-Engine der Anwendung, verantwortlich für Datenverarbeitung und Qualitätstests.
- **dignadashboard**: Eine webbasierte Oberfläche, die auf einem Webserver gehostet wird und eine benutzerfreundliche Interaktion mit der digna-Plattform sowie Visualisierung der Datenqualitätskennzahlen bietet.

### Neuigkeiten in Release 2026.06

Dieses Release integriert Data Observability-Funktionen direkt in Ihren Code und ermöglicht Entwicklern, die Datenqualität bereits an der Quelle zu überwachen. Details finden Sie in den [Release-Notizen](http://docs.digna.ai/changelog/Release_202606/).

### Suchen Sie Anleitungen für Windows oder Linux?

Dieses Handbuch behandelt macOS. Für andere Plattformen siehe die [Windows-Installationsanleitung](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) oder die [Linux-Installationsanleitung](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Systemanforderungen {: #system-requirements }

Bevor Sie mit der Installation beginnen, stellen Sie sicher, dass Ihr System die folgenden Mindestanforderungen erfüllt:

| Anforderung | Spezifikation |
|---|---|
| **Betriebssystem** | macOS 13 (Ventura) oder neuer |
| **Architektur** | Apple Silicon (arm64) oder Intel (x86_64) |
| **Arbeitsspeicher (Minimalinstallation)** | 16 GB RAM |
| **Festplattenspeicher** | 10 GB verfügbarer Speicher |
| **Datenbank** | PostgreSQL Server 12 oder neuer |
| **Webserver** | nginx, Apache httpd oder Ähnliches |
| **Command Line Tools** | Xcode Command Line Tools (erforderlich für Homebrew) |

### Optionen zur Datenbankinstallation

**Falls PostgreSQL bereits installiert ist:**
Sie können Ihrer bestehenden PostgreSQL-Instanz eine neue Datenbank für digna hinzufügen.

**Falls Sie PostgreSQL auf derselben Maschine wie digna installieren:**

!!! info "Empfohlene Spezifikationen"

    - **Arbeitsspeicher**: 32 GB RAM (statt 16 GB)
    - **Festplattenspeicher**: 50 GB verfügbarer Speicher (statt 10 GB)

    Diese höheren Ressourcenangaben berücksichtigen, dass sowohl digna als auch die PostgreSQL-Datenbank gleichzeitig laufen.

### Überprüfen Sie Ihre Architektur

Einige Pfade in dieser Anleitung unterscheiden zwischen Apple Silicon und Intel-Macs. Um Ihre Architektur zu prüfen, öffnen Sie das **Terminal** und führen Sie aus:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew installiert sich nach `/opt/homebrew`.
- `x86_64` — Intel. Homebrew installiert sich nach `/usr/local`.

!!! tip "Tipp"

    Anstatt einen Pfad fest zu kodieren, verwendet diese Anleitung `$(brew --prefix)`, das sich auf beiden Architekturen korrekt auflöst. Sie können die Befehle unverändert kopieren.

---

## Vorbereitungen vor der Installation {: #pre-installation-setup }

Bevor Sie digna installieren, stellen Sie sicher, dass drei zentralen Voraussetzungen erfüllt sind:

1. **Homebrew** – der Paketmanager, mit dem die untenstehenden Komponenten installiert werden
2. **PostgreSQL-Server** – zur Speicherung berechneter Metriken und Leistungsdaten
3. **Webserver** – zum Hosten des digna Dashboards

Falls diese Komponenten noch nicht eingerichtet sind, folgen Sie den nachfolgenden Abschnitten, um sie zu installieren und zu konfigurieren.

### Homebrew installieren

Homebrew ist der Standard-Paketmanager für macOS und wird in dieser Anleitung verwendet, um PostgreSQL und nginx zu installieren.

#### Schritt 1: Prüfen, ob Homebrew bereits installiert ist

Öffnen Sie das **Terminal** (Cmd + Leertaste, tippen Sie `Terminal`, Enter) und führen Sie aus:

```bash
brew --version
```

Wenn eine Versionsnummer angezeigt wird, springen Sie zum Abschnitt [PostgreSQL-Server einrichten](#postgresql-server-setup).

#### Schritt 2: Homebrew installieren

Falls der Befehl nicht gefunden wurde, installieren Sie Homebrew, indem Sie den Anweisungen auf der [offiziellen Homebrew-Seite](https://brew.sh) folgen. Der Installer installiert auch die Xcode Command Line Tools, falls diese noch nicht vorhanden sind.

#### Schritt 3: Homebrew zu Ihrem PATH hinzufügen

Auf Apple Silicon gibt der Installer zwei Befehle aus, um Homebrew zur Shell-Umgebung hinzuzufügen. Führen Sie diese wie angegeben aus und prüfen Sie anschließend:

```bash
brew --prefix
```

Dies sollte auf Apple Silicon `/opt/homebrew` oder auf Intel `/usr/local` ausgeben.

---

## PostgreSQL-Server einrichten {: #postgresql-server-setup }

### Falls Sie PostgreSQL bereits installiert haben

Wenn PostgreSQL bereits lokal läuft oder Sie eine verwaltete Remote-PostgreSQL-Instanz verwenden, können Sie zum [nächsten Abschnitt](#web-server-configuration) springen.

### Installationsoptionen

macOS bietet zwei unkomplizierte Wege, PostgreSQL zu installieren. Wählen Sie **einen**:

- [Homebrew](#postgresql-homebrew) — Installation per Kommandozeile, empfohlen für Server-Deployments
- [Postgres.app](#postgresql-app) — grafische Installation, bequem für lokale Evaluierung

### PostgreSQL mit Homebrew installieren {: #postgresql-homebrew }

#### Schritt 1: Das PostgreSQL-Formula installieren

```bash
brew install postgresql@16
```

#### Schritt 2: PostgreSQL zu Ihrem PATH hinzufügen

Versionierte PostgreSQL-Formeln sind *keg-only*, das heißt, Homebrew verlinkt ihre Befehle nicht automatisch in Ihren PATH. Fügen Sie sie selbst hinzu:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Hinweis"

    Dies geht davon aus, dass die Standard-Shell `zsh` von macOS verwendet wird. Wenn Sie `bash` nutzen, fügen Sie dieselbe Zeile stattdessen zu `~/.bash_profile` hinzu.

#### Schritt 3: Den PostgreSQL-Dienst starten

```bash
brew services start postgresql@16
```

Dies startet PostgreSQL sofort und konfiguriert es so, dass es beim Einloggen automatisch wieder startet.

#### Schritt 4: Installation überprüfen

```bash
psql --version
```

Sie sollten die PostgreSQL-Version sehen, wenn die Installation erfolgreich war.

#### Schritt 5: Mit dem Server verbinden

```bash
psql postgres
```

!!! warning "Wichtig — macOS unterscheidet sich hier von Windows"

    Der Windows-Installer fordert Sie auf, einen `postgres` Superuser mit Passwort anzulegen. Homebrew macht das nicht. Stattdessen wird ein Superuser mit dem Namen Ihres **macOS-Benutzerkontos** ohne Passwort angelegt, der nur lokal erreichbar ist.

    Das bedeutet, dass auf einer frischen Homebrew-Installation keine `postgres`-Rolle existiert. Verwenden Sie Ihren eigenen Kontonamen, wenn Sie Superuser-Rechte benötigen, und erstellen Sie einen expliziten digna-Benutzer wie in [Erstinstallation](#initial-installation) beschrieben.

#### Schritt 6: Den Port bestätigen

Der Standardport von PostgreSQL ist `5432`. Um den Port zu bestätigen, auf dem Ihr Server lauscht:

```bash
psql postgres -c "SHOW port;"
```

Notieren Sie sich den Wert — Sie benötigen ihn bei der Konfiguration des digna-Backends.

### PostgreSQL mit Postgres.app installieren {: #postgresql-app }

Wenn Sie eine grafische Installation bevorzugen:

1. Laden Sie [Postgres.app](https://postgresapp.com) herunter und ziehen Sie es in Ihren **Applications**-Ordner
2. Öffnen Sie die App und klicken Sie auf **Initialize**, um einen neuen Server zu erstellen
3. Folgen Sie den Anweisungen der App, um die Kommandozeilentools zu Ihrem PATH hinzuzufügen
4. Überprüfen Sie die Installation:

```bash
psql --version
```

Postgres.app legt ebenfalls einen Superuser mit dem Namen Ihres macOS-Benutzerkontos an.

---

## Webserver-Konfiguration {: #web-server-configuration }

digna benötigt einen Webserver, um das Dashboard zu hosten. Wählen Sie eine der folgenden Optionen:

- [nginx](#nginx-setup) — per Homebrew installiert, empfohlen
- [Apache httpd](#apache-setup) — in macOS enthalten

Sie müssen nur einen dieser Server installieren und konfigurieren.

Beide Abschnitte konfigurieren zwei Dinge, die das Dashboard benötigt:

- **Fallback für Single-Page-Applications**, damit das Aktualisieren einer Dashboard-URL kein 404 zurückgibt
- **Ein `.md` MIME-Typ**, damit Markdown-Dateien korrekt ausgeliefert werden

### nginx einrichten {: #nginx-setup }

#### Überblick

nginx ist ein leichtgewichtiger, leistungsfähiger Webserver, der sich gut eignet, um das statische digna-Dashboard zu servieren.

#### Installation

```bash
brew install nginx
```

#### nginx starten

```bash
brew services start nginx
```

#### Installation überprüfen

1. Öffnen Sie Ihren Browser
2. Rufen Sie `http://localhost:8080` auf
3. Sie sollten die nginx-Willkommensseite sehen

!!! note "Hinweis — Standardport ist 8080, nicht 80"

    Homebrew konfiguriert nginx so, dass es auf Port `8080` lauscht, damit es ohne Administratorrechte laufen kann. Auf macOS erfordert das Binden an Port `80` oder andere Ports unter 1024 Root-Rechte.

    Um das Dashboard auf Port 80 zu bedienen, ändern Sie `listen 8080;` zu `listen 80;` in der untenstehenden Konfiguration und starten Sie nginx stattdessen mit `sudo brew services start nginx`.

#### Eine Site für das Dashboard konfigurieren

Die Homebrew-nginx-Konfiguration inkludiert alle Dateien im `servers`-Verzeichnis. Erstellen Sie dort eine dedizierte Konfigurationsdatei für digna:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Fügen Sie das Folgende ein und ersetzen Sie `/path/to/digna/dashboard` durch den tatsächlichen Pfad zu Ihrem entpackten `dashboard`-Ordner:

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

!!! warning "Wichtig"

    Ohne die `try_files`-Direktive liefert das Neuladen jeder Dashboard-Seite außer der Root-URL ein 404. Dies ist das nginx-Äquivalent des URL-Rewrite-Moduls, das unter Windows bei IIS benötigt wird.

#### Die Konfiguration anwenden

Prüfen Sie die Konfiguration auf Syntaxfehler und laden Sie nginx neu:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd einrichten {: #apache-setup }

#### Überblick

macOS enthält Apache httpd, daher ist keine Installation erforderlich. Er ist standardmäßig deaktiviert.

#### Apache starten

```bash
sudo apachectl start
```

#### Installation überprüfen

1. Öffnen Sie Ihren Browser
2. Rufen Sie `http://localhost` auf
3. Sie sollten die Meldung "It works!" sehen

#### Erforderlich: mod_rewrite aktivieren

Das Dashboard benötigt URL-Rewriting. Öffnen Sie die Apache-Konfiguration:

```bash
sudo nano /etc/apache2/httpd.conf
```

Finden Sie folgende Zeile und entfernen Sie das vorangestellte `#`, um sie zu aktivieren:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Erforderlich: .htaccess-Overrides erlauben

Ändern Sie in derselben Datei den `<Directory "/Library/WebServer/Documents">`-Block von:

```apache
AllowOverride None
```

zu:

```apache
AllowOverride All
```

#### Erforderlich: MIME-Typ für Markdown-Dateien

Fügen Sie ebenfalls in `httpd.conf` die folgende Zeile hinzu, damit Markdown-Dateien korrekt ausgeliefert werden:

```apache
AddType text/markdown .md
```

!!! warning "Wichtig"

    Ohne diese Einstellung können `.md`-Dateien möglicherweise nicht korrekt geliefert werden.

#### Die Konfiguration anwenden

Überprüfen Sie die Konfiguration auf Syntaxfehler und starten Sie Apache neu:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Erstinstallation {: #initial-installation }

### Schritt 1: Repository für digna einrichten

Das digna-Repository speichert alle von digna berechneten Metriken. Es fungiert als zentrale Datenbank für Analyse- und Leistungsdaten.

#### Schema und Benutzer anlegen

Öffnen Sie Ihren PostgreSQL-Client (psql, pgAdmin oder ähnliches) und führen Sie die folgenden SQL-Befehle aus:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Ersetzen Sie die folgenden Platzhalter:**

- `<digna_repo_schema>` — Gewünschter Schema-Name (z. B. `dignarepo`)
- `<digna_repo_user>` — Gewünschter Benutzername (z. B. `digna_user`)
- `<digna_repo_password>` — Ein sicheres Passwort für diesen Benutzer

**Beispiel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Um diese Befehle im Terminal in einem Schritt auszuführen:

```bash
psql postgres
```

Fügen Sie dann die Statements am `postgres=#` Prompt ein und geben Sie `\q` zum Beenden ein.

!!! tip "Beste Praxis"

    Verwenden Sie starke, komplexe Passwörter für Datenbankbenutzer. Vermeiden Sie leicht zu erratende Zugangsdaten.

---

### Schritt 2: Das digna-Installationspaket entpacken

1. Lokalisieren Sie die Ihnen bereitgestellte digna-Installations-ZIP-Datei
2. Entpacken Sie sie an Ihren gewünschten Installationsort — z. B. `/opt/digna` oder `~/digna`
3. Nach dem Entpacken sollten Sie folgende Elemente sehen:
   - `dashboard/` — Web-Dashboard-Oberfläche
   - `digna` — Haupt-Executable (Backend + CLI kombiniert)
   - `config.toml` — Konfigurationsdatei
   - `license.toml` — Lizenzdatei (kopieren Sie Ihre hierhin)

Um im Terminal zu entpacken:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Die ausführbare Datei ausführbar machen

Je nachdem, wie das Archiv übertragen wurde, geht das Ausführbarkeitsbit beim Entpacken möglicherweise verloren. Setzen Sie es explizit:

```bash
cd /opt/digna
chmod +x digna
```

#### Falls macOS die Anwendung blockiert

Per Browser oder Mail-Client heruntergeladene Dateien werden mit einem Quarantäne-Attribut versehen. Wenn macOS meldet, dass die App *"cannot be opened because the developer cannot be verified"*, entfernen Sie das Attribut aus dem Installationsverzeichnis:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativ öffnen Sie **Systemeinstellungen → Datenschutz & Sicherheit**, suchen das blockierte Element unten auf der Seite und klicken auf **Dennoch öffnen** / **Open Anyway**.

!!! note "Hinweis"

    Dieser Schritt ist nur notwendig, wenn macOS die ausführbare Datei tatsächlich blockiert. Über SSH übertragene Pakete oder Dateien aus internen Dateifreigaben sind in der Regel nicht quarantänisiert.

### Schritt 3: Die Lizenzdatei installieren

!!! warning "Wichtig"

    Die Lizenzdatei ist **nicht** im Installationspaket enthalten und wird separat von digna bereitgestellt.

1. Lokalisieren Sie die Ihnen bereitgestellte `license.toml`
2. Kopieren Sie sie in das Root-Installationsverzeichnis von digna (dort, wo `config.toml` und die `digna`-Executable liegen)

**Warum das wichtig ist:**
Die Lizenzdatei enthält Ihre Kundendaten, das Ablaufdatum der Lizenz und die digitale Signatur. **Ändern Sie diese Datei nicht** — jede Änderung macht sie ungültig.

**Verzeichnisstruktur nach der Einrichtung:**

```
/opt/digna/
├── config.toml         (Konfigurationsdatei)
├── license.toml        (IHRE LIZENZDATEI - hierher kopieren)
├── digna               (Haupt-Executable)
├── bin/                (Skripte zur Service-Verwaltung)
└── dashboard/          (Weboberfläche)
    └── (Dashboard-Dateien)
```

---

## Backend-Konfiguration {: #backend-configuration }

### Schritt 1: Konfigurationsdatei anlegen und bearbeiten

Die Datei `config_template.toml` liegt in Ihrem digna-Installationsverzeichnis. Sie müssen sie lediglich in `config.toml` umbenennen.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Pfad:** `/opt/digna/config.toml`

Öffnen Sie `config.toml` in einem Texteditor und konfigurieren Sie die nachstehenden Abschnitte.

#### [app] Abschnitt

Dieser Abschnitt konfiguriert die Einstellungen der digna-Backend-Anwendung:

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
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Falls Dashboard auf anderem Server, dessen URL hier eintragen |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Erforderlich für CORS mit Credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Erlaubt alle HTTP-Methoden |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Erlaubt alle Header |

!!! note "Hinweis"

    Wenn Sie das Dashboard mit Homebrews nginx auf dem Standardport betreiben, ist die Origin, die erlaubt werden muss, `http://localhost:8080`.

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
| `digna_REPO_SCHEMA` | `dignarepo` | Vorhin erstelltes Schema |
| `digna_REPO_USER` | `digna_user` | In PostgreSQL angelegter Benutzer |
| `digna_REPO_PASSWORD` | Ihr Passwort | Passwort, das bei der Schema-Erstellung gesetzt wurde |

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
| `digna_FERNET_KEY` | Verschlüsselungsschlüssel | Wird zur Verschlüsselung von Tokens und Cookies verwendet (Standard wird geliefert) |
| `digna_COOKIE_DOMAIN` | `localhost` | Entspricht Ihrer Frontend-Domain |
| `digna_COOKIE_SECURE` | `false` (lokal) / `true` (Produktion) | `true` bei HTTPS-Verbindungen verwenden |
| `digna_COOKIE_HTTPONLY` | `true` | Aus Sicherheitsgründen immer aktivieren |
| `digna_COOKIE_SAME_SITE` | `lax` | Verhindert CSRF-Angriffe |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 Stunden) | Sitzungsdauer in Sekunden |
| `digna_MAX_WORKERS` | Anzahl CPU-Kerne - 1 | Anzahl paralleler Inspektionsaufgaben |

!!! tip "Tipp"

    Um die Anzahl der CPU-Kerne auf Ihrem Mac zu ermitteln, führen Sie `sysctl -n hw.ncpu` aus.

#### [logging] Abschnitt

Dieser Abschnitt konfiguriert das Logging-Verhalten:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` oder `DEBUG` | `INFO` für Produktion, `DEBUG` zum Debuggen |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Anzahl täglicher Log-Backups, die aufbewahrt werden |

---

### Schritt 2: Das Repository initialisieren

1. Öffnen Sie das **Terminal**
2. Wechseln Sie in Ihr digna-Installationsverzeichnis (dort, wo `config.toml` und die `digna`-Executable liegen)
3. Führen Sie den Verbindungstest aus:

```bash
cd /opt/digna
./digna repo check
```

Sie sollten eine Bestätigung sehen, dass die Verbindung hergestellt wurde (das Repository selbst wurde noch nicht initialisiert).

!!! note "Hinweis"

    Unter macOS sind Befehle im aktuellen Verzeichnis nicht im PATH, daher wird die ausführbare Datei als `./digna` aufgerufen statt `digna`. Um die kürzere Form überall verwenden zu können, fügen Sie das Installationsverzeichnis zu Ihrem PATH hinzu:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Schritt 3: Das Repository-Schema installieren

Führen Sie im selben Verzeichnis aus:

```bash
./digna repo install
```

Dieser Befehl legt die benötigten Tabellen und das Schema in Ihrer PostgreSQL-Datenbank an.

### Schritt 4: Den digna-Server starten

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

    Beim ersten Start fragt macOS möglicherweise, ob die Anwendung eingehende Netzwerkverbindungen akzeptieren darf. Klicken Sie auf **Allow**, sonst kann das Dashboard nicht auf das Backend zugreifen.

### Schritt 5: Einen Admin-Benutzer anlegen

1. Öffnen Sie ein **neues** Terminalfenster
2. Wechseln Sie in Ihr digna-Installationsverzeichnis
3. Führen Sie folgenden Befehl aus, um einen Admin-Benutzer zu erstellen:

```bash
./digna user add <username> "<vollständiger_name>" <password> --su
```

**Beispiel:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Dies erstellt einen Benutzer mit dem Benutzernamen `admin` und vollständigen administrativen Rechten.

!!! tip "Tipp"

    Setzen Sie das Passwort in einfache Anführungszeichen. `zsh` behandelt Zeichen wie `!`, `$` und `*` speziell, und ein nicht-quoted Passwort mit solchen Zeichen wird nicht korrekt übergeben.

!!! tip "Beste Praxis"

    Verwenden Sie ein starkes Passwort mit einer Mischung aus Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen.

---

## Dashboard-Konfiguration {: #dashboard-configuration }

### Schritt 1: Dashboard auf dem Webserver bereitstellen

Das digna-Dashboard hat seine eigene, separate `config.toml`-Datei im `dashboard/`-Verzeichnis. Diese Konfiguration wird bereits mitgeliefert und erfordert während der Erstinstallation keine Änderungen. Sie müssen sie nur anpassen, falls die Backend-Verbindung modifiziert werden soll.

Wenn Sie die Dashboard-Konfiguration (z. B. für Multi-Instance-Deployments) anpassen müssen, konsultieren Sie die Dokumentation des Dashboards.

Wählen Sie Ihren Webserver und folgen Sie den entsprechenden Bereitstellungsschritten.

#### Bereitstellung auf nginx

Wenn Sie der Anleitung im Abschnitt [nginx Setup](#nginx-setup) gefolgt sind, zeigt der Server-Block bereits auf Ihren `dashboard`-Ordner und es ist kein Kopieren erforderlich.

1. **Pfad bestätigen**
   - Öffnen Sie `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Vergewissern Sie sich, dass `root` auf Ihren entpackten `dashboard`-Ordner zeigt

2. **Sicherstellen, dass der Ordner lesbar ist**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **nginx neu laden**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Installation testen**
   - Öffnen Sie Ihren Browser
   - Rufen Sie `http://localhost:8080` (oder Ihre konfigurierte URL) auf
   - Sie sollten die Anmeldeseite des digna-Dashboards sehen

#### Bereitstellung auf Apache httpd

1. **Dashboard in das Document Root kopieren**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Rewrite-Regeln hinzufügen**

   Erstellen Sie eine `.htaccess`-Datei im bereitgestellten Ordner, damit Dashboard-Routen beim Browser-Refresh erhalten bleiben:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Fügen Sie Folgendes ein:

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

3. **Apache neu starten**
   ```bash
   sudo apachectl restart
   ```

4. **Dashboard aufrufen**
   - Öffnen Sie Ihren Browser
   - Rufen Sie `http://localhost/digna` auf
   - Sie sollten die Anmeldeseite des digna-Dashboards sehen

---

## digna als Hintergrunddienst ausführen {: #running-digna-as-a-background-service }

### Warum digna als Dienst ausführen?

Das Ausführen des digna-Backends als Hintergrunddienst stellt sicher, dass es:

- Beim Systemstart automatisch gestartet wird
- Im Hintergrund läuft, ohne ein offenes Terminalfenster zu benötigen
- Bei Abstürzen automatisch neu startet
- Über `launchctl`, den Dienstemanager von macOS, verwaltet werden kann

### Dateien zur Dienstverwaltung

Alle benötigten Dateien befinden sich im digna-Installationsverzeichnis unter: `bin/`

Die folgenden Shell-Skripte sind vorhanden:

- `install_service.sh` — registriert digna bei launchd
- `uninstall_service.sh` — entfernt die Registrierung
- `start_service.sh` — startet den registrierten Dienst
- `stop_service.sh` — stoppt den laufenden Dienst

!!! warning "Administrator erforderlich"

    Alle Skripte müssen mit `sudo` ausgeführt werden, da das Registrieren eines Dienstes beim Booten in `/Library/LaunchDaemons` schreibt.

### Ausführbarkeitsrechte für die Skripte setzen

Beim Entpacken kann das Ausführbarkeitsbit verloren gehen. Vor der ersten Verwendung:

```bash
cd /opt/digna/bin
chmod +x *.sh
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

Der digna-Server ist jetzt bei launchd mit **automatischem Start** registriert. Der Dienst startet nicht sofort — siehe den nächsten Abschnitt, um ihn zu starten.

### Dienst starten und stoppen

#### Dienst starten

1. Terminal öffnen
2. Ins Verzeichnis `/opt/digna/bin` wechseln
3. Ausführen:
   ```bash
   sudo ./start_service.sh
   ```

#### Dienst stoppen

1. Terminal öffnen
2. Ins Verzeichnis `/opt/digna/bin` wechseln
3. Ausführen:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tipp"

    Stoppen Sie den Dienst stets vor dem Aktualisieren der Anwendungsdateien.

### Dienst verifizieren

Um zu bestätigen, dass der Dienst registriert und läuft:

```bash
sudo launchctl list | grep digna
```

Eine Zeile, die mit einer Prozess-ID beginnt, zeigt an, dass der Dienst läuft. Ein `-` in der ersten Spalte bedeutet, dass er registriert, aber gestoppt ist.

### Dienst in ein neues Verzeichnis verschieben

launchd speichert den absoluten Pfad zur ausführbaren Datei, daher erfordert ein Verschieben der Installation eine Neu-Registrierung des Dienstes:

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

Der digna-Server ist nun bei launchd abgemeldet.

---

## Upgrade auf eine neue Version {: #upgrading-to-a-new-release }

### Vor dem Upgrade

**Das Erstellen eines Backups des digna-Repositorys ist verpflichtend**

Bevor Sie digna aktualisieren, sichern Sie unbedingt Ihr Repository (PostgreSQL), um Datenverlust vorzubeugen.
Ein Backup ermöglicht die Wiederherstellung, falls das Upgrade unerwartete Probleme verursacht.

Um ein Backup im Terminal zu erstellen:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Upgrade-Prozess

#### Schritt 1: den digna-Dienst stoppen

Wenn digna als Hintergrunddienst läuft, stoppen Sie ihn zuerst:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Wenn digna im Vordergrund läuft, drücken Sie in dessen Terminalfenster `Ctrl + C`.

#### Schritt 2: Aktuelle Backend-Installation sichern

In Ihrem digna-Installationsverzeichnis:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Schritt 3: Neue Version entpacken und bereitstellen

1. Entpacken Sie das neue digna-Installations-ZIP-Archiv
2. Kopieren Sie die neue `digna`-Executable und den `dashboard`-Ordner in Ihr Installationsverzeichnis
3. Stellen Sie das Ausführbarkeitsbit wieder her und löschen Sie ggf. das Quarantäne-Attribut:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Wichtig"

    Die `config.toml` wird **niemals** im Installations-ZIP enthalten sein. Ihre bestehende Konfiguration bleibt erhalten.

### Schritt 4: Ihre Konfigurationsdateien wiederherstellen

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Schritt 5: Repository-Schema aktualisieren

Wechseln Sie in Ihr digna-Installationsverzeichnis und führen Sie aus:

```bash
cd /opt/digna
./digna repo upgrade
```

Dies aktualisiert das PostgreSQL-Schema auf die neueste Version und bewahrt dabei alle vorhandenen Daten.

### Schritt 6: Dienste neu starten

Falls der Dienst als Hintergrunddienst läuft:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Falls Sie manuell starten, starten Sie den Server neu:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Wenn Sie nginx oder Apache nutzen, starten Sie den jeweiligen Webserver neu:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Schritt 7: Upgrade verifizieren

1. Rufen Sie das digna-Dashboard auf
2. Vergewissern Sie sich, dass die Oberfläche korrekt geladen wird
3. Prüfen Sie die Server-Logs auf etwaige Fehler
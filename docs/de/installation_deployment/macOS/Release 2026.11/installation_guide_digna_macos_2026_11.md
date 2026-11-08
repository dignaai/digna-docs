---
title: macOS Installationsanleitung – digna Release 2026.11 | digna Dokumentation
description: Schritt-für-Schritt-Anleitung zur Installation von digna Release 2026.11 auf macOS — Systemanforderungen, Homebrew- und PostgreSQL-Einrichtung, nginx- oder Apache-Konfiguration, Backend- und Dashboard-Konfiguration, Ausführung von digna als Hintergrunddienst und Upgrade von Release 2026.06.
keywords: digna macOS Installation, digna macOS Deployment-Anleitung, digna Backend-Einrichtung, digna Dashboard-Installation, postgresql homebrew, nginx macOS, digna launchd Dienst, digna Upgrade-Anleitung
image: /assets/logo_square.png
---

# macOS Installationsanleitung für digna Release 2026.11

**Release:** 2026.11

**Zuletzt aktualisiert:** 7. November 2026


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

- **digna**: Der Kern der Anwendung, zuständig für die Verarbeitung von Daten und die Durchführung von Qualitätsprüfungen. Er vereint Backend und Kommandozeilenschnittstelle in einer einzigen ausführbaren Datei und ersetzt damit die früher getrennten Programme `dignabackend` und `dignacli`.
- **dignadashboard**: Eine webbasierte Oberfläche, die auf einem Webserver gehostet wird und eine benutzerfreundliche Interaktion mit der digna-Plattform sowie Visualisierung der Datenqualitätskennzahlen bietet.

### Neuigkeiten in Release 2026.11

Dieses Release ergänzt digna Data Reconciliation, digna Agentic mit dem digna MCP Server und die digna Engine, die Daten innerhalb von digna profilieren und die referenzielle Integrität zwischen unterschiedlichen Datenbanktechnologien prüfen kann. Details finden Sie in den [Release Notes](../../../changelog/Release_202611.md).

Für die Installation bringt das Release einen neuen Mechanismus für Repository-Migrationen, einen optionalen Abschnitt `[duckdb]` in der `config.toml` für die digna Engine und eine neue Lizenzdatei. Der [Abschnitt zum Upgrade](#upgrading-to-a-new-release) behandelt jeden dieser Punkte.

### Suchen Sie Anleitungen für Windows oder Linux?

Dieses Handbuch behandelt macOS. Für andere Plattformen siehe die [Windows-Installationsanleitung](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) oder die [Linux-Installationsanleitung](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Datenbankverbindungen, die die digna Engine als Profiling-Ort verwenden, werden auf dem
    digna-Host selbst profiliert. Planen Sie dafür zusätzlichen Arbeitsspeicher und
    Festplattenplatz ein, siehe den [Abschnitt \[duckdb\]](#duckdb-section).
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

!!! info "Konfigurations- und Lizenzdateien sind nicht im Paket enthalten"

    Weder `config.toml` noch `dashboard/dashboard_config.toml` wird mit der Installation
    ausgeliefert — Sie legen beide selbst an, unter [Backend-Konfiguration](#backend-configuration) und
    [Dashboard-Konfiguration](#dashboard-configuration). Auch `license.toml` ist nicht enthalten;
    digna stellt sie separat bereit, wie in Schritt 3 beschrieben.

Um im Terminal zu entpacken:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
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

Dieser Abschnitt konfiguriert Cross-Origin Resource Sharing (CORS) zwischen Dashboard und Backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard-URLs | Die URLs, unter denen das Dashboard ausgeliefert wird. Browser-Anfragen von jeder anderen Origin werden abgelehnt |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Erforderlich, damit der Browser das Session-Cookie mit jeder Anfrage sendet |

!!! note "Hinweis"

    Wenn Sie das Dashboard mit Homebrews nginx auf dem Standardport betreiben, ist die Origin, die erlaubt werden muss, `http://localhost:8080`.

!!! info "Der Abschnitt [app] ist optional"

    Ab Release 2026.11 können beide Schlüssel und der gesamte Abschnitt `[app]` entfallen. Das ist
    die richtige Einrichtung, wenn ein Reverse Proxy Dashboard und Backend unter einer Origin
    ausliefert: Der Browser stellt dann keine Cross-Origin-Anfragen, und standardmäßig ist keine
    erlaubt.

#### [repo] Abschnitt

Dieser Abschnitt konfiguriert die Verbindung zur PostgreSQL-Datenbank:

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

| Parameter | Wert | Hinweise |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` oder IP | PostgreSQL-Server Hostname/IP |
| `DIGNA_REPO_PORT` | `5432` (Standard) | PostgreSQL-Port |
| `DIGNA_REPO_DB` | `postgres` | Datenbankname |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Vorhin erstelltes Schema |
| `DIGNA_REPO_USER` | `digna_user` | In PostgreSQL angelegter Benutzer |
| `DIGNA_REPO_PASSWORD` | Ihr Passwort | Passwort, das bei der Schema-Erstellung gesetzt wurde |
| `DIGNA_REPO_SSLMODE` | `prefer` (Standard) | Optional. SSL-Modus für PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` oder `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (Standard) | Optional. Anzahl der Verbindungen, die digna zum Repository offen hält |

#### [base] Abschnitt

Dieser Abschnitt enthält Sicherheits-, Cookie- und Inspektionseinstellungen:

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

| Parameter | Wert | Hinweise |
|---|---|---|
| `DIGNA_FERNET_KEY` | Oben gezeigter Wert | Schlüssel der Verschlüsselung früherer Releases. Er muss vorhanden sein; behalten Sie den gezeigten Wert bei |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host, unter dem das Dashboard erreicht wird. `""` setzt keine Domain; das ist richtig hinter einem Proxy, der Dashboard und Backend unter einer Origin ausliefert |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Muss `true` sein, sobald digna über HTTPS ausgeliefert wird |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Hält das Session-Cookie von Skripten fern |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 Stunden) | Sitzungsdauer in Sekunden |
| `DIGNA_MAX_WORKERS` | Anzahl CPU-Kerne - 1 | Anzahl der Inspektionen, die gleichzeitig laufen dürfen |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Erforderlich. Wird für die Links in Benachrichtigungen verwendet und muss daher eine URL sein, die die Empfänger öffnen können |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (Standard) | Optional. Sekunden, die eine einzelne Abfrage gegen eine Quelldatenbank laufen darf, bevor sie abgebrochen wird; `0` deaktiviert das Timeout |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (Standard) | Optional. Sekunden, die auf eine Verbindung zu einer Quelldatenbank gewartet wird; `0` wartet unbegrenzt |

!!! tip "Tipp"

    Um die Anzahl der CPU-Kerne auf Ihrem Mac zu ermitteln, führen Sie `sysctl -n hw.ncpu` aus.

#### [encryption] Abschnitt

Dieser Abschnitt enthält den Schlüssel, mit dem sensible Werte im Repository verschlüsselt werden. Er ist **erforderlich** — `config check` meldet den Abschnitt `[encryption]` als FAILED, wenn der Schlüssel fehlt.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-kodierter Schlüssel | Verschlüsselt sensible Werte, die im digna-Repository gespeichert sind |

!!! warning "config.toml schützen"

    Dieser Schlüssel ist ein fester Wert, der in allen digna-Installationen identisch ist, und er entschlüsselt die sensiblen Werte in Ihrem Repository. Beschränken Sie den Zugriff auf `config.toml` auf das Konto, unter dem digna läuft, halten Sie die Datei aus der Versionsverwaltung und von freigegebenen Laufwerken fern und schließen Sie sie von jedem Backup aus, das weniger sicher aufbewahrt wird als das Repository selbst.

#### [logging] Abschnitt

Dieser Abschnitt konfiguriert das Logging-Verhalten:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` oder `DEBUG` | `INFO` für Produktion, `DEBUG` zum Debuggen. `TRACE`, `WARN` und `ERROR` werden ebenfalls akzeptiert |
| `DIGNA_LOGGING_DIR` | `logs` (Standard) | Optional. Verzeichnis für die rotierenden Log-Dateien, relativ zum Arbeitsverzeichnis |
| `DIGNA_LOGGING_MAX_FILES` | `30` (Standard) | Optional. Anzahl der rotierten Log-Dateien, die aufbewahrt werden |

#### [duckdb] Abschnitt (optional) {: #duckdb-section }

Neu in Release 2026.11. Dieser Abschnitt legt die Ressourcen der **digna Engine** fest, die für
Datenbankverbindungen mit dem Profiling-Ort **digna Engine** Daten innerhalb von digna profiliert
und Prüfungen der referenziellen Integrität zwischen Datenquellen auf unterschiedlichen
Datenbankverbindungen ausführt. Siehe
[Profiling-Ort](../../../platform/profiling/profiling_location.md).

Der Abschnitt ist optional. Ohne ihn gelten die unten genannten Standardwerte.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (Standard) | Arbeitsspeicher in MB, den ein einzelner Lauf der digna Engine belegen darf. Bis zu `DIGNA_MAX_WORKERS` Läufe können gleichzeitig aktiv sein |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standard: das temporäre Verzeichnis des Systems (`$TMPDIR` des Kontos, unter dem digna läuft) | Verzeichnis für temporäre Dateien, wenn die Daten nicht in den Arbeitsspeicher passen |

!!! tip "Dimensionierung der digna Engine"

    Planen Sie auf dem digna-Host bis zu `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB`
    Arbeitsspeicher zusätzlich zu dem ein, was digna selbst belegt, sowie genug freien
    Festplattenplatz im temporären Verzeichnis, um den größten inspizierten Tag der Datenquellen
    aufzunehmen, die die digna Engine verwenden. Lassen Sie `DIGNA_DUCKDB_TEMP_DIRECTORY` auf einen
    Datenträger mit so viel Platz zeigen, der für das Konto beschreibbar ist, unter dem digna läuft:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Sie benötigen diesen Abschnitt nur, wenn mindestens eine Datenbankverbindung die digna Engine
    verwendet oder eine Prüfung der referenziellen Integrität Datenquellen auf unterschiedlichen
    Verbindungen vergleicht.

---

### Schritt 2: Konfiguration prüfen

Prüfen Sie vor der Initialisierung des Repositories, ob `config.toml` vollständig und korrekt aufgebaut ist. Führen Sie in Ihrem digna-Installationsverzeichnis aus:

```bash
./digna config check
```

Jeder Abschnitt wird einzeln geprüft, sodass ein einzelner Fehler den Zustand der übrigen nicht verdeckt:

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

Beheben Sie alles, was als FAILED gemeldet wird, und führen Sie den Befehl erneut aus, bevor Sie fortfahren. Eine WARNING unter **Unknown keys** listet Schlüssel in der `config.toml` auf, die digna nicht liest; sie haben keine Wirkung, entfernen Sie sie also oder korrigieren Sie ihre Schreibweise. Die vollständige Liste der Optionen finden Sie in der [CLI-Referenz](../../../cli/Command_Line_Interface_202611.md).

### Schritt 3: Das Repository initialisieren

1. Öffnen Sie das **Terminal**
2. Wechseln Sie in Ihr digna-Installationsverzeichnis (dort, wo `config.toml` und die `digna`-Executable liegen)
3. Führen Sie den Verbindungstest aus:

```bash
cd /opt/digna
./digna repo check
```

Bei einem neuen Schema stellt der Befehl die Verbindung her und meldet dann, dass noch kein Repository installiert ist:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

An dieser Stelle ist das das erwartete Ergebnis: Es bestätigt, dass digna PostgreSQL und das Schema erreicht. Ein Verbindungs- oder Authentifizierungsfehler weist dagegen auf den Abschnitt `[repo]` oder auf die PostgreSQL-Einrichtung hin.

!!! note "Hinweis"

    Unter macOS sind Befehle im aktuellen Verzeichnis nicht im PATH, daher wird die ausführbare Datei als `./digna` aufgerufen statt `digna`. Um die kürzere Form überall verwenden zu können, fügen Sie das Installationsverzeichnis zu Ihrem PATH hinzu:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Schritt 4: Das Repository-Schema installieren

Führen Sie im selben Verzeichnis aus:

```bash
./digna repo upgrade
```

Dieser Befehl legt die benötigten Tabellen im Repository-Schema an und endet mit:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installiert und aktualisiert"

    Ab Release 2026.11 installiert `repo upgrade` ein neues Repository und aktualisiert ein
    bestehendes. `repo install` funktioniert weiterhin als anderer Name für denselben Befehl.

### Schritt 5: Einen Admin-Benutzer anlegen

1. Öffnen Sie ein **neues** Terminalfenster
2. Wechseln Sie in Ihr digna-Installationsverzeichnis
3. Führen Sie folgenden Befehl aus, um einen Admin-Benutzer zu erstellen:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Beispiel:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Dies legt einen Benutzer mit der E-Mail-Adresse `admin@example.com` und vollen administrativen Rechten an.

!!! tip "Tipp"

    Setzen Sie das Passwort in einfache Anführungszeichen. `zsh` behandelt Zeichen wie `!`, `$` und `*` speziell, und ein nicht-quoted Passwort mit solchen Zeichen wird nicht korrekt übergeben.

!!! tip "Beste Praxis"

    Verwenden Sie ein starkes Passwort mit einer Mischung aus Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen.

---

### Schritt 6: Den digna-Server starten

Starten Sie im digna-Installationsverzeichnis den Server mit:

```bash
./digna serve --address <host> --port <port>
```

**Parameter:**
- `--address` — Server-Hostname/IP (Standard `127.0.0.1`)
- `--port` — Server-Port (Standard `8000`)

Sobald der Server läuft, gibt er die Adresse aus, auf der er lauscht:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tipp"

    Beim ersten Start fragt macOS möglicherweise, ob die Anwendung eingehende Netzwerkverbindungen akzeptieren darf. Klicken Sie auf **Allow**, sonst kann das Dashboard nicht auf das Backend zugreifen.


!!! note "Der Server belegt das Terminal"

    `serve` läuft im Vordergrund und bleibt aktiv, bis Sie es mit ++ctrl+c++ beenden. Lassen Sie es laufen, während Sie die Einrichtung abschließen — wie Sie den Server stattdessen automatisch beim Systemstart starten, steht unter [digna als Hintergrunddienst ausführen](#running-digna-as-a-background-service).

## Dashboard-Konfiguration {: #dashboard-configuration }

### Schritt 1: Dashboard auf dem Webserver bereitstellen

Das digna-Dashboard liest seine eigene Konfiguration aus `dashboard/dashboard_config.toml`. Diese Datei wird nicht mit der Installation ausgeliefert — Sie legen sie im `dashboard/`-Verzeichnis neben den Dashboard-Dateien an.

Ihr Inhalt ist unter [Single Sign-on](../../../sso/overview.md) beschrieben, wo die Datei auch benötigt wird: Sie enthält die Anmeldeoptionen, die das Dashboard anbietet, und bei Multi-Instance-Deployments die Backend-Verbindung.

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

Dieser Abschnitt aktualisiert eine Installation von Release 2026.06 auf Release 2026.11.

!!! warning "Upgrade von einem Release vor 2026.06"

    Führen Sie zuerst die Upgrade-Schritte von Release 2026.06 aus: [Upgrade auf eine neue Version](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release). Fahren Sie danach mit den folgenden Schritten fort.

### Bevor Sie ein Upgrade durchführen

**Ein Backup des digna-Repositorys ist verpflichtend**

Erstellen Sie vor einem Upgrade von digna ein Backup Ihres Repositorys (PostgreSQL), um Datenverlust zu vermeiden.
Ein Backup stellt sicher, dass Sie im Falle unerwarteter Probleme bei einem Upgrade wiederherstellen können.

Um ein Backup im Terminal zu erstellen:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Lizenzdatei für Release 2026.11 anfordern**

Release 2026.11 benötigt eine neue `license.toml`. Fordern Sie sie vor dem Start beim digna-Team an
und halten Sie sie für [Schritt 7](#step-7-replace-the-license-file) bereit.

### Upgrade-Ablauf

#### Schritt 1: digna-Dienst stoppen {: #step-1-stop-the-digna-service }

Wenn digna als Hintergrunddienst läuft, stoppen Sie ihn zuerst:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Falls digna im Vordergrund läuft, drücken Sie in dessen Terminal-Fenster ++ctrl+c++.

#### Schritt 2: Aktuelle Installation sichern {: #step-2-backup-current-installation }

Benennen Sie in Ihrem digna-Installationsverzeichnis die ausführbare Datei und den Dashboard-Ordner
Ihrer aktuellen Installation um, damit das neue Release daneben bereitgestellt werden kann:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Behalten Sie `digna_old`, bis Sie das Upgrade überprüft haben, und `dashboard_old`, bis Sie Ihre
Konfigurationsdateien daraus wiederhergestellt haben (siehe Schritt 4). Danach können Sie beide löschen.

#### Schritt 3: Neue Version entpacken und bereitstellen {: #step-3-extract-and-deploy-new-version }

1. Entpacken Sie die neue digna-Installations-ZIP-Datei
2. Kopieren Sie die neue `digna`-Executable und den `dashboard`-Ordner in Ihr Installationsverzeichnis
3. Stellen Sie das Executable-Bit wieder her und entfernen Sie bei Bedarf das Quarantäne-Attribut:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Wichtig"

    Weder `config.toml` noch `dashboard/dashboard_config.toml` ist jemals in der
    Installations-ZIP enthalten — das digna-Team liefert keine der beiden Dateien aus. Ihre
    bestehende Konfiguration bleibt vom Upgrade daher unberührt, und die Kopien in den
    umbenannten `*_old`-Ordnern sind die einzigen, die Sie haben.

#### Schritt 4: Konfigurationsdateien wiederherstellen {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 erfordert keine Änderung an der `config.toml`: Eine Datei, die mit Release 2026.06
funktioniert, funktioniert weiterhin. Zwei Änderungen sind optional:

- Ergänzen Sie einen [Abschnitt `[duckdb]`](#duckdb-section), wenn Datenbankverbindungen die digna
  Engine verwenden sollen und deren Standardwerte nicht zu Ihrem Host passen.
- Lassen Sie den Abschnitt `[app]` weg, wenn ein Reverse Proxy Dashboard und Backend unter einer
  Origin ausliefert.

!!! warning "Einstellungen, die digna nicht liest"

    Frühere Versionen dieser Anleitung zeigten einige Einstellungen, die digna nicht liest. Sie
    haben keine Wirkung, und `config check` listet sie in Schritt 6 unter **Unknown keys** auf.
    Entfernen oder korrigieren Sie sie:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` und
      `digna_LOGGING_BACKUP_COUNT` gibt es nicht. Entfernen Sie sie.
    - Bei Einstellungsnamen wird zwischen Groß- und Kleinschreibung unterschieden. digna liest
      `DIGNA_REPO_HOST`, nicht `digna_REPO_HOST`. Schreiben Sie jeden Namen in Großbuchstaben, wie
      in der [Backend-Konfiguration](#backend-configuration).

!!! warning "Single Sign-on: [[oidc_clients]] beibehalten"

    digna liest Single-Sign-on-Anbieter als Liste von `[[oidc_clients]]`-Einträgen, jeder mit
    einem eigenen `DIGNA_OIDC_KEY`. Wenn Sie Ihre Anbieter auf `[oidc_clients.<key>]`-Abschnitte
    umgestellt haben, wie es eine frühere Version dieser Anleitung zeigte, stellen Sie sie zurück.
    `config check` meldet `OIDC config(s)` als FAILED, solange diese Form vorhanden ist:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Wiederholen Sie den Eintrag für jeden Anbieter und halten Sie jeden `DIGNA_OIDC_KEY`
    deckungsgleich mit dem `key` in der `dashboard_config.toml`. Betroffen sind nur
    Installationen, die Single Sign-on verwenden.

#### Schritt 5: Webserver neu laden {: #step-5-reload-the-web-server }

Das Dashboard besteht aus statischen Dateien, daher liefern Ihr Webserver — und der Browser —
möglicherweise noch die vorherige Version aus. Laden Sie den Webserver, der den `dashboard`-Ordner
bereitstellt, neu oder starten Sie ihn neu, und laden Sie die Seite anschließend mit einem
Hard Refresh neu (++cmd+shift+r++).

#### Schritt 6: Konfiguration prüfen {: #step-6-validate-the-configuration }

Stellen Sie sicher, dass die `config.toml` vollständig ist, bevor Sie das Repository anfassen:

```bash
./digna config check
```

Jeder Abschnitt muss OK melden. Beheben Sie alles, was als FAILED gemeldet wird, entfernen Sie die
unter **Unknown keys** aufgeführten Schlüssel und führen Sie den Befehl erneut aus, bevor Sie fortfahren.

#### Schritt 7: Lizenzdatei ersetzen {: #step-7-replace-the-license-file }

Eine für ein früheres Release ausgestellte Lizenzdatei funktioniert mit Release 2026.11 nicht.
Kopieren Sie die `license.toml`, die das digna-Team für Release 2026.11 bereitgestellt hat, in das
Installationsverzeichnis und ersetzen Sie damit die alte:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Behalten Sie die bisherige Lizenz nicht"

    Mit der bisherigen Lizenz schlägt jeder Befehl fehl, der die Lizenz prüft — `serve`, `user`,
    `inspection`, `repo` —, sodass digna nicht startet und kein Upgrade des Repositorys möglich ist.
    Prüfen Sie die neue Lizenz, bevor Sie fortfahren:

    ```bash
    ./digna license check
    ```

#### Schritt 8: Repository-Schema upgraden {: #step-8-upgrade-the-repository-schema }

Führen Sie in Ihrem digna-Installationsverzeichnis aus:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 verwaltet das Repository-Schema mit versionierten Migrationen. Das erste Upgrade
von einem früheren Release bringt das Schema auf die letzte Version des bisherigen Verfahrens,
hält diesen Stand als Ausgangspunkt fest und wendet dann die Migrationen von Release 2026.11 an.
Es endet mit:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Alle vorhandenen Daten bleiben erhalten. Um den Zustand des Repositorys jederzeit zu sehen, führen
Sie `./digna repo check` aus: Der Befehl listet die zuletzt angewendete Migration und alle noch
ausstehenden auf.

!!! warning "digna startet nicht auf einem veralteten Repository"

    Ab Release 2026.11 verweigert der Server den Start, solange das Repository ein Upgrade
    benötigt, und meldet das, zum Beispiel:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Führen Sie `repo upgrade` aus, bevor Sie den Server oder den Dienst starten.

#### Schritt 9: Dienste neu starten {: #step-9-restart-services }

Wenn digna als Hintergrunddienst läuft:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Wenn Sie es manuell betreiben, starten Sie den Server neu:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Wenn Sie nginx oder Apache verwenden, starten Sie den jeweiligen Webserver neu:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Schritt 10: Upgrade verifizieren {: #step-10-verify-the-upgrade }

1. Prüfen Sie das Release der neuen ausführbaren Datei:

    ```bash
    ./digna version
    ```

    Die erste Zeile muss `Release: 2026.11` lauten.

2. Rufen Sie das digna-Dashboard auf und prüfen Sie, ob die Oberfläche korrekt geladen wird.
3. Prüfen Sie die Ausgabe des Servers und die Dateien im Verzeichnis `logs` auf Fehler.
4. Testen Sie Ihre Datenbankverbindungen — siehe
   [Verbindung testen](../../../databases/overview.md#testing-a-connection).

Für den Einstieg in die neuen Module siehe [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[KI-Agenten verbinden](../../../platform/agentic/connect_ai_agent.md) für den digna MCP Server und
[Profiling-Ort](../../../platform/profiling/profiling_location.md) für die digna Engine.

---
title: Windows-Installationsanleitung – digna Release 2026.06 | digna Dokumentation
description: Schritt-für-Schritt-Anleitung zur Installation von digna Release 2026.06 unter Windows — Systemanforderungen, PostgreSQL-Einrichtung, Webserver-Konfiguration, Backend- und Dashboard-Konfiguration, Ausführen von digna als Windows-Dienst und Upgrade auf eine neue Version.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Windows-Installationsanleitung für digna Release 2026.06

**Release:** 2026.06

**Zuletzt aktualisiert:** 30. August 2026


---

## Inhaltsverzeichnis

1. [Einführung](#introduction)
2. [Systemanforderungen](#system-requirements)
3. [Vorbereitende Schritte](#pre-installation-setup)
4. [PostgreSQL-Server einrichten](#postgresql-server-setup)
5. [Webserver-Konfiguration](#web-server-configuration)
6. [Erstinstallation](#initial-installation)
7. [Backend-Konfiguration](#backend-configuration)
8. [Dashboard-Konfiguration](#dashboard-configuration)
9. [digna als Windows-Dienst ausführen](#running-digna-as-a-windows-service)
10. [Auf eine neue Version aktualisieren](#upgrading-to-a-new-release)

---

## Einführung {: #introduction }

### Über digna

digna ist eine umfassende, KI-gestützte Plattform zur Optimierung des Datenqualitätsmanagements in verschiedenen Datenumgebungen wie Data Warehouses, Data Lakes und Lakehouses. digna ist hoch skalierbar und anpassungsfähig und adressiert moderne Datenherausforderungen durch Automatisierung, Echtzeitüberwachung und Anomalieerkennung.

digna besteht aus zwei Hauptkomponenten:

- **dignabackend**: Die Kern-Engine der Anwendung, verantwortlich für die Datenverarbeitung und Qualitätsprüfungen.
- **dignadashboard**: Eine webbasierte Oberfläche, gehostet auf einem Webserver, die eine benutzerfreundliche Interaktion mit der digna-Plattform und Visualisierung der Datenqualitätskennzahlen bietet.

### Was ist neu in Release 2026.06

Dieses Release bringt Data Observability-Funktionen direkt in Ihren Code und ermöglicht Entwicklern, die Datenqualität an der Quelle zu überwachen. Details finden Sie in den [Release Notes](http://docs.digna.ai/changelog/Release_202606/).

---

## Systemanforderungen {: #system-requirements }

Bevor Sie mit der Installation beginnen, stellen Sie sicher, dass Ihr System die folgenden Mindestanforderungen erfüllt:

| Anforderung | Spezifikation |
|---|---|
| **Betriebssystem** | Windows Server oder Windows 10/11 |
| **Arbeitsspeicher (Minimal)** | 16 GB RAM |
| **Festplattenspeicher** | 10 GB verfügbarer Speicher |
| **Datenbank** | PostgreSQL Server 12 oder höher |
| **Webserver** | IIS, Apache Tomcat oder vergleichbar |

### Optionen zur Datenbankinstallation

**Falls PostgreSQL bereits installiert ist:**
Sie können Ihrer bestehenden PostgreSQL-Instanz eine neue Datenbank für digna hinzufügen.

**Falls PostgreSQL auf derselben Maschine wie digna installiert werden soll:**

> **Empfohlene Spezifikationen**
>
> - **Arbeitsspeicher**: 32 GB RAM (statt 16 GB)
> - **Festplattenspeicher**: 50 GB verfügbarer Speicher (statt 10 GB)
>
> Diese höheren Spezifikationen berücksichtigen sowohl digna als auch die gleichzeitig laufende PostgreSQL-Datenbank.

---

## Vorbereitende Schritte {: #pre-installation-setup }

Bevor Sie digna installieren, stellen Sie sicher, dass zwei wichtige Voraussetzungen erfüllt sind:

1. **PostgreSQL-Server** – zum Speichern berechneter Metriken und Leistungsdaten
2. **Webserver** – zum Hosten des digna Dashboards

Falls diese Komponenten noch nicht eingerichtet sind, folgen Sie den nachstehenden Abschnitten, um sie zu installieren und zu konfigurieren.

---

## PostgreSQL-Server einrichten {: #postgresql-server-setup }

### Falls PostgreSQL bereits vorhanden ist

Wenn PostgreSQL bereits lokal installiert ist oder Sie einen verwalteten entfernten PostgreSQL-Server verwenden, können Sie zum [nächsten Abschnitt](#web-server-configuration) springen.

### PostgreSQL installieren

Folgen Sie diesen Schritten, um PostgreSQL unter Windows zu installieren:

#### Schritt 1: PostgreSQL herunterladen

1. Besuchen Sie die [PostgreSQL-Downloadseite](https://www.postgresql.org/download/)
2. Wählen Sie **Windows**
3. Laden Sie das neueste Installationsprogramm herunter

#### Schritt 2: Installer ausführen

1. Doppelklicken Sie auf die heruntergeladene Installationsdatei
2. Folgen Sie den Anweisungen im Setup-Assistenten

#### Schritt 3: Installationsverzeichnis auswählen

Wählen Sie das Verzeichnis, in dem PostgreSQL installiert werden soll. Der Standardpfad ist in der Regel geeignet.

#### Schritt 4: Komponenten auswählen

Für eine Standardinstallation lassen Sie die voreingestellten Komponenten ausgewählt.

#### Schritt 5: Passwort für PostgreSQL-Superuser setzen

Geben Sie ein Passwort für den PostgreSQL-Superuser (`postgres`) ein und bestätigen Sie es. **Speichern Sie dieses Passwort sicher** — Sie benötigen es später.

#### Schritt 6: Portnummer konfigurieren

Der Standardport von PostgreSQL ist `5432`. Sie können den Standard verwenden oder bei Bedarf einen anderen Port angeben.

> **Tipp**
>
> Wenn Port 5432 bereits belegt ist, wählen Sie einen alternativen Port und merken Sie ihn für spätere Konfigurationen.

#### Schritt 7: Gebietsschema (Locale) auswählen

Wählen Sie das Gebietsschema für Ihre Datenbank. Die Voreinstellung ist in den meisten Fällen passend.

#### Schritt 8: Installation abschließen

Klicken Sie auf **Next** durch die verbleibenden Schritte und anschließend auf **Finish**.

#### Schritt 9: Installation verifizieren

Öffnen Sie die Eingabeaufforderung und prüfen Sie, ob PostgreSQL installiert ist:

```bash
psql --version
```

Sie sollten die PostgreSQL-Version sehen, wenn die Installation erfolgreich war.

---

## Webserver-Konfiguration {: #web-server-configuration }

digna benötigt einen Webserver zum Hosten des Dashboards. Wählen Sie eine der folgenden Optionen:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Sie müssen nur einen dieser Server installieren und konfigurieren.

### IIS-Setup {: #iis-setup }

#### Überblick

Internet Information Services (IIS) ist Microsofts Webserver zum Hosten von Websites und Webanwendungen.

#### IIS aktivieren

1. **Systemsteuerung öffnen**
   - Drücken Sie `Win + R`
   - Geben Sie `control` ein und drücken Sie Enter

2. **Zu Windows-Funktionen navigieren**
   - Klicken Sie auf **Programme**
   - Wählen Sie **Windows-Funktionen aktivieren oder deaktivieren**

3. **Internet Information Services aktivieren**
   - Scrollen Sie herunter und finden Sie **Internet Information Services (IIS)**
   - Aktivieren Sie das Kontrollkästchen
   - Klicken Sie das **+** an, um zu prüfen, dass folgende Unterkomponenten ausgewählt sind:
     - **Webverwaltungstools**
     - **World Wide Web-Dienste**

4. **Klicken Sie auf OK**, um die Änderungen anzuwenden

5. **IIS-Installation überprüfen**
   - Öffnen Sie Ihren Browser
   - Navigieren Sie zu `http://localhost`
   - Sie sollten die IIS-Willkommensseite sehen

#### Erforderlich: URL Rewrite Module

IIS benötigt die URL Rewrite-Komponente. Laden Sie sie von der [offiziellen Microsoft-Seite](https://www.iis.net/downloads/microsoft/url-rewrite) herunter und installieren Sie sie.

#### Erforderlich: MIME-Typ für Markdown-Dateien

Damit Markdown-Dateien (`.md`) korrekt von IIS ausgeliefert werden, gehen Sie wie folgt vor:

1. Öffnen Sie den **IIS Manager** (drücken Sie `Win + R`, geben Sie `inetmgr` ein und drücken Sie Enter)
2. Navigieren Sie zu **Ihre Website > MIME-Typen**
3. Klicken Sie auf **Hinzufügen...**
4. Konfigurieren Sie:
   - **Dateinamenerweiterung**: `.md`
   - **MIME-Typ**: `text/markdown`

> **Wichtig**
>
> Ohne diese Einstellung werden `.md`-Dateien möglicherweise nicht korrekt ausgeliefert.

---

### Apache Tomcat-Setup {: #apache-tomcat-setup }

#### Überblick

Apache Tomcat ist ein Open-Source Java Servlet-Container und Webserver.

#### Installation

1. **Apache Tomcat herunterladen**
   - Besuchen Sie [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Laden Sie die ZIP-Distribution für Windows herunter

2. **Archiv entpacken**
   - Entpacken Sie die ZIP-Datei in ein Verzeichnis auf Ihrem System
   - Beispiel: `C:\Program Files\Apache Tomcat`

3. **Tomcat läuft prüfen**
   - Öffnen Sie Ihren Browser
   - Navigieren Sie zu `http://localhost:8080`
   - Sie sollten die Apache Tomcat-Willkommensseite sehen

> **Tipp**
>
> Apache Tomcat startet normalerweise nach der Installation automatisch. Falls nicht, wechseln Sie in den `bin`-Ordner und führen Sie `startup.bat` aus.

---

## Erstinstallation {: #initial-installation }

### Schritt 1: Repository für digna einrichten

Das digna-Repository speichert alle von digna berechneten Metriken. Es fungiert als zentrale Datenquelle für Analyse- und Leistungsdaten.

#### Schema und Benutzer für das Repository anlegen

Öffnen Sie Ihren PostgreSQL-Client (pgAdmin, psql oder ähnliches) und führen Sie folgende SQL-Befehle aus:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Ersetzen Sie die Platzhalter:**

- `<digna_repo_schema>` — gewünschter Schema-Name (z. B. `dignarepo`)
- `<digna_repo_user>` — gewünschter Benutzername (z. B. `digna_user`)
- `<digna_repo_password>` — sicheres Passwort für diesen Benutzer

**Beispiel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **Best Practice**
>
> Verwenden Sie starke, komplexe Passwörter für Datenbankbenutzer. Vermeiden Sie leicht zu erratende Anmeldedaten.

---

### Schritt 2: digna-Installationspaket entpacken

1. Suchen Sie die Ihnen bereitgestellte digna-Installations-ZIP-Datei
2. Entpacken Sie sie an den gewünschten Installationsort
3. Nach dem Entpacken sollten folgende Elemente sichtbar sein:
   - `dashboard/` — Web-Dashboard-Oberfläche
   - `digna` — Hauptprogramm (Backend + CLI kombiniert)
   - `config.toml` — Konfigurationsdatei
   - `license.toml` — Lizenzdatei (kopieren Sie Ihre Lizenz hierhin)

### Schritt 3: Lizenzdatei installieren

> **Wichtig**
>
> Die Lizenzdatei ist **nicht** im Installationspaket enthalten und wird separat von digna bereitgestellt.

1. Suchen Sie die Ihnen bereitgestellte `license.toml`
2. Kopieren Sie sie in das Stammverzeichnis der digna-Installation (dort, wo `config.toml` und die `digna`-Executable liegen)

**Warum das wichtig ist:**
Die Lizenzdatei enthält Ihre Kundendaten, das Ablaufdatum der Lizenz und die digitale Signatur. **Verändern Sie diese Datei nicht** — jede Änderung macht sie ungültig.

**Verzeichnisstruktur nach dem Setup:**

```
digna_installation/
├── config.toml         (Konfigurationsdatei)
├── license.toml        (IHRE LIZENZDATEI - hierher kopieren)
├── digna               (Haupt-Executable)
└── dashboard/          (Web-Oberfläche)
    └── (Dashboard-Dateien)
```

---

## Backend-Konfiguration {: #backend-configuration }

### Schritt 1: Konfigurationsdatei erstellen und bearbeiten

Die Datei `config_template.toml` liegt in Ihrem digna-Installationsverzeichnis. Benennen Sie sie einfach in `config.toml` um.

**Pfad:** `digna_installation/config.toml`

Öffnen Sie `config.toml` in einem Texteditor und konfigurieren Sie die folgenden Abschnitte.

#### [app] Abschnitt

Dieser Abschnitt konfiguriert die Anwendungseinstellungen des digna-Backends:

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
| `digna_APP_HOST` | `localhost` oder IP-Adresse | Hostname oder IP, auf dem dignabackend läuft |
| `digna_APP_PORT` | `8082` (Standard) | Port für die REST-API-Endpunkte |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Wenn das Dashboard auf einem anderen Server liegt, fügen Sie dessen URL hinzu |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Erforderlich für CORS mit Anmeldeinformationen |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Erlaubt alle HTTP-Methoden |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Erlaubt alle Header |

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
| `digna_REPO_USER` | `digna_user` | In der PostgreSQL-Einrichtung erstellter Benutzer |
| `digna_REPO_PASSWORD` | Ihr Passwort | Bei der Schema-Erstellung gesetztes Passwort |

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
| `digna_FERNET_KEY` | Verschlüsselungsschlüssel | Wird zur Verschlüsselung von Tokens und Cookies verwendet (Standardwert vorhanden) |
| `digna_COOKIE_DOMAIN` | `localhost` | Sollte Ihrer Frontend-Domain entsprechen |
| `digna_COOKIE_SECURE` | `false` (lokal) / `true` (Produktiv) | Verwenden Sie `true` für HTTPS-Verbindungen |
| `digna_COOKIE_HTTPONLY` | `true` | Immer für Sicherheit aktiviert |
| `digna_COOKIE_SAME_SITE` | `lax` | Verhindert CSRF-Angriffe |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 Stunden) | Session-Timeout in Sekunden |
| `digna_MAX_WORKERS` | Anzahl CPU-Kerne - 1 | Anzahl paralleler Inspektionsaufgaben |

#### [logging] Abschnitt

Dieser Abschnitt konfiguriert das Logging-Verhalten:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` oder `DEBUG` | `INFO` für Produktion, `DEBUG` für Fehlerbehebung |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Anzahl täglicher Log-Backups, die aufbewahrt werden |

---

### Schritt 3: Repository-Verbindung testen

1. Öffnen Sie die Eingabeaufforderung
2. Wechseln Sie in Ihr digna-Installationsverzeichnis (dort, wo `config.toml` und die `digna`-Executable liegen)
3. Führen Sie den Verbindungstest aus:

```bash
digna repo check
```

Sie sollten eine Bestätigung sehen, dass die Verbindung hergestellt wurde (das Repository selbst wurde noch nicht installiert).

### Schritt 4: Repository-Schema installieren

Führen Sie im selben Verzeichnis aus:

```bash
digna repo install
```

Dieser Befehl installiert die notwendigen Tabellen und das Schema in Ihrer PostgreSQL-Datenbank.

### Schritt 5: digna-Server starten

Starten Sie im digna-Installationsverzeichnis den Server mit:

```bash
digna serve --address <host> --port <port>
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

### Schritt 6: Admin-Benutzer anlegen

1. Öffnen Sie ein **neues** Eingabeaufforderungsfenster
2. Wechseln Sie in Ihr digna-Installationsverzeichnis
3. Führen Sie den folgenden Befehl aus, um einen Admin-Benutzer anzulegen:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Beispiel:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Dies erstellt einen Benutzer mit vollständigen Administratorrechten.

> **Best Practice**
>
> Verwenden Sie ein starkes Passwort mit einer Mischung aus Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen.

---

## Dashboard-Konfiguration {: #dashboard-configuration }

### Schritt 1: Dashboard auf dem Webserver bereitstellen

Das digna-Dashboard verfügt über eine eigene `config.toml` im `dashboard/`-Verzeichnis. Diese Konfiguration ist bereits enthalten und erfordert bei der Erstinstallation normalerweise keine Änderungen. Sie müssen sie nur anpassen, wenn Sie die Backend-Verbindung anpassen möchten.

Bei Bedarf an Dashboard-Anpassungen (z. B. bei Multi-Instance-Deployments) konsultieren Sie die Dashboard-Dokumentation.

Wählen Sie Ihren Webserver und folgen Sie den entsprechenden Bereitstellungsschritten.

#### Bereitstellung auf IIS

1. **IIS Manager öffnen**
   - Drücken Sie `Win + R`, geben Sie `inetmgr` ein und drücken Sie Enter

2. **Neue Website erstellen**
   - Klicken Sie im linken Bereich mit der rechten Maustaste auf **Sites**
   - Wählen Sie **Website hinzufügen...**

3. **Website konfigurieren**
   - **Site-Name**: Geben Sie einen Namen ein (z. B. "dignaDashboard")
   - **Physischer Pfad**: Klicken Sie auf Durchsuchen und wählen Sie Ihren `dashboard`-Ordner
   - **Bindung**: Legen Sie IP-Adresse und Port fest (Standardport 80 für HTTP, 443 für HTTPS)

4. **Website starten**
   - Klicken Sie auf **OK**, um die Site zu erstellen
   - Klicken Sie mit der rechten Maustaste auf die neue Site und wählen Sie **Starten**

5. **Installation testen**
   - Öffnen Sie Ihren Browser
   - Navigieren Sie zu `http://localhost` (oder Ihrer konfigurierten URL)
   - Sie sollten die Anmeldeseite des digna-Dashboards sehen

#### Bereitstellung auf Apache Tomcat

1. **Dashboard nach Tomcat kopieren**
   - Kopieren Sie den `dashboard`-Ordner in das `webapps`-Verzeichnis von Tomcat
   - Benennen Sie ihn bei Bedarf um (z. B. in `digna`)
   - Beispiel: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Bereitstellung prüfen**
   - Aktualisieren oder laden Sie die Tomcat-Management-Seite neu (http://localhost:8080)
   - Sie sollten "digna" (oder den gewählten Namen) in der Liste der deployten Anwendungen sehen

3. **Dashboard aufrufen**
   - Öffnen Sie Ihren Browser
   - Navigieren Sie zu `http://localhost:8080/digna`
   - Sie sollten die Anmeldeseite des digna-Dashboards sehen

---

## digna als Windows-Dienst ausführen {: #running-digna-as-a-windows-service }

### Warum als Windows-Dienst?

Das Ausführen des digna-Backends als Windows-Dienst stellt sicher, dass es:
- Beim Systemstart automatisch gestartet wird
- Im Hintergrund läuft, ohne ein offenes Eingabeaufforderungsfenster
- Bei Abstürzen automatisch neu gestartet werden kann
- Über die Windows-Diensteverwaltung gesteuert werden kann

### Dateien zur Dienstverwaltung

Alle notwendigen Dateien befinden sich im digna-Installationsverzeichnis unter: `bin/`

Folgende Batch-Dateien sind vorhanden:
- `install_service.bat` — registriert digna als Windows-Dienst
- `uninstall_service.bat` — entfernt die Dienstregistrierung
- `start_service.bat` — startet den Dienst
- `stop_service.bat` — stoppt den Dienst

> **Administratorrechte erforderlich**
>
> Alle Batch-Dateien müssen mit Administratorrechten ausgeführt werden.

### Dienst installieren

1. **Eingabeaufforderung als Administrator öffnen**
   - Rechtsklicken Sie auf die Eingabeaufforderung
   - Wählen Sie "Als Administrator ausführen"

2. **In den bin-Ordner wechseln**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Installationsskript ausführen**
   ```bash
   install_service.bat
   ```

Der digna-Server ist nun als Windows-Dienst mit **automatischem Start** registriert. Der Dienst startet nicht sofort — siehe nächsten Abschnitt zum Starten.

### Dienst starten und stoppen

#### Dienst starten

1. Öffnen Sie die Eingabeaufforderung als Administrator
2. Wechseln Sie zu `digna\bin`
3. Führen Sie aus:
   ```bash
   start_service.bat
   ```

#### Dienst stoppen

1. Öffnen Sie die Eingabeaufforderung als Administrator
2. Wechseln Sie zu `digna\bin`
3. Führen Sie aus:
   ```bash
   stop_service.bat
   ```

> **Tipp**
>
> Stoppen Sie den Dienst immer, bevor Sie Anwendungsdateien aktualisieren.

### Dienst in ein neues Verzeichnis verschieben

Wenn Sie die digna-Installation verschieben müssen:

1. **Aktuellen Dienst deinstallieren**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Anwendungsdateien verschieben**
   - Verschieben Sie den gesamten digna-Installationsordner in den neuen Pfad

3. **Dienst neu installieren**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Dienst starten**
   ```bash
   start_service.bat
   ```

### Dienst deinstallieren

1. **Laufenden Dienst stoppen**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Dienst deinstallieren**
   ```bash
   uninstall_service.bat
   ```

Der digna-Server ist nun als Windows-Dienst abgemeldet.

---

## Auf eine neue Version aktualisieren {: #upgrading-to-a-new-release }

### Vor dem Upgrade

**Ein Backup des digna-Repositories ist verpflichtend**

Erstellen Sie vor dem Upgrade Ihres digna-Repositories (PostgreSQL) ein Backup, um Datenverlust zu vermeiden. Ein Backup stellt sicher, dass Sie im Fehlerfall wiederherstellen können.

### Upgrade-Prozess

#### Schritt 1: digna-Dienst stoppen

Falls digna als Windows-Dienst läuft, stoppen Sie ihn zuerst:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Schritt 2: Aktuelle Backend-Installation sichern

In Ihrem digna-Installationsverzeichnis:

```bash
# Ordner mit dignabackend umbenennen
ren dignabackend dignabackend_old
```
```bash
# Dashboard umbenennen
ren dashboard dashboard_old
```

#### Schritt 3: Neue Version entpacken und bereitstellen

1. Entpacken Sie das neue digna-Installations-ZIP
2. Kopieren Sie die neue `digna`-Executable und den `dashboard`-Ordner in Ihr Installationsverzeichnis


> **Wichtig**
>
> Die `config.toml` ist **niemals** im Installations-ZIP enthalten. Ihre bestehende Konfiguration bleibt erhalten.

### Schritt 4: Konfigurationsdateien wiederherstellen

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Schritt 5: Repository-Schema aktualisieren

Wechseln Sie in Ihr digna-Installationsverzeichnis und führen Sie aus:

```bash
digna repo upgrade
```

Dies aktualisiert das PostgreSQL-Schema auf die neueste Version und erhält alle vorhandenen Daten.

### Schritt 6: Dienste neu starten

Falls digna als Windows-Dienst läuft:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Falls Sie den Server manuell starten:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Wenn Sie IIS oder Tomcat verwenden, starten Sie den jeweiligen Webserver neu.

#### Schritt 7: Upgrade überprüfen

1. Rufen Sie das digna-Dashboard auf
2. Prüfen Sie, ob die Oberfläche korrekt lädt
3. Überprüfen Sie die Server-Logs auf etwaige Fehler

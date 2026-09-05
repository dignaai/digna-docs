---
title: Windows-Installationsanleitung – digna Release 2026.06 | digna Documentation
description: Schritt-für-Schritt-Anleitung zur Installation von digna Release 2026.06 auf Windows — Systemanforderungen, PostgreSQL-Einrichtung, Webserver-Konfiguration, Backend- und Dashboard-Konfiguration, Ausführen von digna als Windows-Dienst und Upgrade auf eine neue Version.
keywords: digna Windows-Installation, digna Bereitstellungsanleitung, digna Backend-Setup, digna Dashboard-Installation, PostgreSQL Einrichtung, digna Windows-Dienst, digna Upgrade-Anleitung
image: /assets/logo_square.png
---

# Windows Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** August 30, 2026


---

## Table of Contents

1. [Einführung](#introduction)
2. [Systemanforderungen](#system-requirements)
3. [Vorbereitung vor der Installation](#pre-installation-setup)
4. [PostgreSQL-Server Einrichtung](#postgresql-server-setup)
5. [Webserver-Konfiguration](#web-server-configuration)
6. [Erstinstallation](#initial-installation)
7. [Backend-Konfiguration](#backend-configuration)
8. [Dashboard-Konfiguration](#dashboard-configuration)
9. [Ausführen von digna als Windows-Dienst](#running-digna-as-a-windows-service)
10. [Upgrade auf eine neue Version](#upgrading-to-a-new-release)

---

## Einführung {: #introduction }

### Über digna

digna ist eine umfassende, KI-gestützte Plattform zur Optimierung des Datenqualitätsmanagements in verschiedenen Datenumgebungen wie Data Warehouses, Data Lakes und Lakehouses. Entwickelt für hohe Skalierbarkeit und Anpassungsfähigkeit, adressiert digna moderne Datenherausforderungen durch Automatisierung, Echtzeit-Überwachung und Anomalieerkennung.

digna besteht aus zwei Hauptkomponenten:

- **dignabackend**: Die Kern-Engine der Anwendung, verantwortlich für die Datenverarbeitung und die Durchführung von Qualitätsprüfungen.
- **dignadashboard**: Eine webbasierte Benutzeroberfläche, die auf einem Webserver gehostet wird und eine benutzerfreundliche Möglichkeit bietet, mit der digna-Plattform zu interagieren und Metriken zur Datenqualität zu visualisieren.

### Neu in Release 2026.06

Dieses Release bringt Data-Observability-Funktionen direkt in Ihren Code, sodass Entwickler die Datenqualität an der Quelle überwachen können. Siehe die [Release Notes](http://docs.digna.ai/changelog/Release_202606/) für vollständige Details.

### Suchen Sie macOS oder Linux?

Dieses Handbuch behandelt Windows. Für andere Plattformen siehe die [macOS Installationsanleitung](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) oder die [Linux Installationsanleitung](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Systemanforderungen {: #system-requirements }

Bevor Sie mit der Installation beginnen, stellen Sie sicher, dass Ihr System die folgenden Mindestanforderungen erfüllt:

| Anforderung | Spezifikation |
|---|---|
| **Betriebssystem** | Windows Server oder Windows 10/11 |
| **Arbeitsspeicher (Minimal)** | 16 GB RAM |
| **Festplattenspeicher** | 10 GB verfügbarer Speicher |
| **Datenbank** | PostgreSQL Server 12 oder höher |
| **Webserver** | IIS, Apache Tomcat oder gleichwertig |

### Optionen zur Datenbankinstallation

**Wenn PostgreSQL bereits installiert ist:**
Sie können Ihrer vorhandenen PostgreSQL-Instanz eine neue Datenbank für digna hinzufügen.

**Wenn PostgreSQL auf demselben Rechner wie digna installiert werden soll:**

!!! info "Empfohlene Spezifikationen"

    - **Arbeitsspeicher**: 32 GB RAM (anstatt 16 GB)
    - **Festplattenspeicher**: 50 GB verfügbarer Speicher (anstatt 10 GB)

    Diese höheren Spezifikationen berücksichtigen, dass sowohl digna als auch die PostgreSQL-Datenbank gleichzeitig ausgeführt werden.

---

## Vorbereitung vor der Installation {: #pre-installation-setup }

Bevor Sie digna installieren, stellen Sie sicher, dass zwei wichtige Voraussetzungen erfüllt sind:

1. **PostgreSQL-Server** – zur Speicherung berechneter Metriken und Leistungsdaten
2. **Webserver** – zum Hosten des digna Dashboards

Wenn diese Komponenten noch nicht eingerichtet sind, folgen Sie den untenstehenden Abschnitten, um sie zu installieren und zu konfigurieren.

---

## PostgreSQL-Server Einrichtung {: #postgresql-server-setup }

### Wenn PostgreSQL bereits vorhanden ist

Wenn PostgreSQL bereits lokal installiert und ausgeführt wird oder wenn Sie einen verwalteten entfernten PostgreSQL-Server verwenden, können Sie zum [nächsten Abschnitt](#web-server-configuration) springen.

### Installation von PostgreSQL

Führen Sie die folgenden Schritte aus, um PostgreSQL unter Windows zu installieren:

#### Schritt 1: PostgreSQL herunterladen

1. Besuchen Sie die [PostgreSQL Downloads Seite](https://www.postgresql.org/download/)
2. Wählen Sie **Windows**
3. Laden Sie das neueste Installationsprogramm herunter

#### Schritt 2: Das Installationsprogramm ausführen

1. Doppelklicken Sie auf die heruntergeladene Installationsdatei
2. Folgen Sie den Anweisungen im Setup-Assistenten

#### Schritt 3: Installationsverzeichnis wählen

Wählen Sie das Verzeichnis, in dem PostgreSQL installiert werden soll. Der Standardpfad ist in der Regel passend.

#### Schritt 4: Komponenten auswählen

Für eine Standardinstallation belassen Sie die voreingestellten Komponenten.

#### Schritt 5: Passwort für PostgreSQL Superuser festlegen

Geben Sie ein Passwort für den PostgreSQL-Superuser (`postgres`) ein und bestätigen Sie es. **Speichern Sie dieses Passwort sicher** — Sie benötigen es später.

#### Schritt 6: Portnummer konfigurieren

Der Standardport von PostgreSQL ist `5432`. Sie können den Standard verwenden oder bei Bedarf einen anderen Port angeben.

!!! tip "Tipp"

    Wenn Port 5432 bereits verwendet wird, wählen Sie einen alternativen Port und notieren Sie ihn für die spätere Konfiguration.

#### Schritt 7: Gebietsschema wählen

Wählen Sie das Gebietsschema (Locale) für Ihre Datenbank. Der Standard ist in den meisten Fällen geeignet.

#### Schritt 8: Installation abschließen

Klicken Sie sich durch die verbleibenden Schritte mit **Next** (Weiter) und klicken Sie abschließend auf **Finish** (Fertigstellen).

#### Schritt 9: Installation überprüfen

Öffnen Sie die Eingabeaufforderung und überprüfen Sie, ob PostgreSQL installiert wurde:

```bash
psql --version
```

Sie sollten die PostgreSQL-Version sehen, wenn die Installation erfolgreich war.

---

## Webserver-Konfiguration {: #web-server-configuration }

digna benötigt einen Webserver zum Hosten des Dashboards. Wählen Sie eine der folgenden Optionen:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Sie müssen **nur einen** dieser Server installieren und konfigurieren.

### IIS Einrichtung {: #iis-setup }

#### Überblick

Internet Information Services (IIS) ist der Webserver von Microsoft zum Hosten von Websites und Webanwendungen.

#### IIS aktivieren

1. **Systemsteuerung öffnen**
   - Drücken Sie `Win + R`
   - Geben Sie `control` ein und drücken Sie Enter

2. **Zu Windows-Funktionen navigieren**
   - Klicken Sie auf **Programme**
   - Wählen Sie **Windows-Funktionen ein- oder ausschalten**

3. **Internet Information Services aktivieren**
   - Scrollen Sie nach unten und finden Sie **Internet Information Services (IIS)**
   - Aktivieren Sie das Kontrollkästchen
   - Klicken Sie auf das **+**, um sicherzustellen, dass folgende Unterkomponenten ausgewählt sind:
     - **Webverwaltungstools**
     - **World Wide Web-Dienste**

4. **Klicken Sie auf OK**, um die Änderungen anzuwenden

5. **IIS-Installation überprüfen**
   - Öffnen Sie Ihren Browser
   - Navigieren Sie zu `http://localhost`
   - Sie sollten die IIS-Willkommensseite sehen

#### Erforderlich: URL Rewrite Modul

IIS benötigt die URL Rewrite-Komponente. Laden Sie sie von der [offiziellen Microsoft-Seite](https://www.iis.net/downloads/microsoft/url-rewrite) herunter und installieren Sie sie.

#### Erforderlich: MIME-Typ für Markdown-Dateien

Damit Markdown-Dateien (`.md`) korrekt von IIS ausgeliefert werden, gehen Sie wie folgt vor:

1. Öffnen Sie den **IIS-Manager** (drücken Sie `Win + R`, geben Sie `inetmgr` ein und drücken Sie Enter)
2. Navigieren Sie zu **Ihre Website > MIME-Typen**
3. Klicken Sie auf **Hinzufügen...**
4. Konfigurieren Sie:
   - **Dateinamenerweiterung**: `.md`
   - **MIME-Typ**: `text/markdown`

!!! warning "Wichtig"

    Ohne diese Einstellung werden `.md`-Dateien möglicherweise nicht korrekt ausgeliefert.

---

### Apache Tomcat Einrichtung {: #apache-tomcat-setup }

#### Überblick

Apache Tomcat ist ein Open-Source Java-Servlet-Container und Webserver.

#### Installation

1. **Apache Tomcat herunterladen**
   - Besuchen Sie [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Laden Sie die Windows ZIP-Distribution herunter

2. **Archiv entpacken**
   - Entpacken Sie die ZIP-Datei in ein Verzeichnis auf Ihrem System
   - Beispiel: `C:\Program Files\Apache Tomcat`

3. **Tomcat prüfen**
   - Öffnen Sie Ihren Browser
   - Navigieren Sie zu `http://localhost:8080`
   - Sie sollten die Apache Tomcat Willkommensseite sehen

!!! tip "Tipp"

    Apache Tomcat startet in der Regel nach der Installation automatisch. Falls nicht, wechseln Sie in den `bin`-Ordner und führen `startup.bat` aus.

---

## Erstinstallation {: #initial-installation }

### Schritt 1: Das digna-Repository einrichten

Das digna-Repository speichert alle von digna berechneten Metriken. Es dient als zentrale Datenbank für analytische und Leistungsdaten.

#### Schema und Benutzer für das Repository erstellen

Öffnen Sie Ihren PostgreSQL-Client (pgAdmin, psql oder ähnlich) und führen Sie die folgenden SQL-Befehle aus:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Ersetzen Sie die folgenden Platzhalter:**

- `<digna_repo_schema>` — Ihr gewünschter Schema-Name (z. B. `dignarepo`)
- `<digna_repo_user>` — Ihr gewünschter Benutzername (z. B. `digna_user`)
- `<digna_repo_password>` — Ein sicheres Passwort für diesen Benutzer

**Beispiel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Beste Praxis"

    Verwenden Sie starke, komplexe Passwörter für Datenbankbenutzer. Vermeiden Sie leicht zu erratende Zugangsdaten.

---

### Schritt 2: Das digna-Installationspaket entpacken

1. Lokalisieren Sie die Ihnen bereitgestellte digna-Installations-ZIP-Datei
2. Entpacken Sie sie an Ihren gewünschten Installationsort
3. Nach dem Entpacken sollten folgende Elemente vorhanden sein:
   - `dashboard/` — Web-Dashboard-Oberfläche
   - `digna` — Hauptausführbare Datei (Backend + CLI kombiniert)
   - `config.toml` — Konfigurationsdatei
   - `license.toml` — Lizenzdatei (kopieren Sie Ihre hierher)

### Schritt 3: Lizenzdatei installieren

!!! warning "Wichtig"

    Die Lizenzdatei ist **nicht** im Installationspaket enthalten und wird separat von digna bereitgestellt.

1. Lokalisieren Sie die Ihnen bereitgestellte `license.toml`
2. Kopieren Sie sie in das Stammverzeichnis der digna-Installation (dort, wo `config.toml` und die ausführbare Datei `digna` liegen)

**Warum das wichtig ist:**
Die Lizenzdatei enthält Ihre Kundeninformationen, das Ablaufdatum der Lizenz und die digitale Signatur. **Ändern Sie diese Datei nicht** — jede Modifikation macht sie ungültig.

**Verzeichnisstruktur nach der Einrichtung:**

```
digna_installation/
├── config.toml         (Konfigurationsdatei)
├── license.toml        (IHRE LIZENZDATEI - hier einfügen)
├── digna               (Hauptausführbare Datei)
└── dashboard/          (Weboberfläche)
    └── (Dashboard-Dateien)
```

---

## Backend-Konfiguration {: #backend-configuration }

### Schritt 1: Konfigurationsdatei erstellen und bearbeiten

Die Datei `config_template.toml` ist in Ihrem digna-Installationsverzeichnis enthalten. Benennen Sie sie einfach in `config.toml` um.

**Ort:** `digna_installation/config.toml`

Öffnen Sie `config.toml` in einem Texteditor und konfigurieren Sie die untenstehenden Abschnitte.

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
| `digna_APP_PORT` | `8082` (Standard) | Port für REST-API-Endpunkte |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Falls das Dashboard auf einem anderen Server liegt, fügen Sie dessen URL hinzu |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Erforderlich für CORS mit Credentials |
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
| `digna_REPO_PASSWORD` | Ihr Passwort | Während der Schema-Erstellung gesetztes Passwort |

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
| `digna_FERNET_KEY` | Verschlüsselungsschlüssel | Wird zur Verschlüsselung von Tokens und Cookies verwendet (Standardvorgabe vorhanden) |
| `digna_COOKIE_DOMAIN` | `localhost` | Entspricht Ihrer Frontend-Domain |
| `digna_COOKIE_SECURE` | `false` (lokal) / `true` (Produktion) | Verwenden Sie `true` bei HTTPS-Verbindungen |
| `digna_COOKIE_HTTPONLY` | `true` | Immer aus Sicherheitsgründen aktiviert |
| `digna_COOKIE_SAME_SITE` | `lax` | Verhindert CSRF-Angriffe |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 Stunden) | Session-Timeout in Sekunden |
| `digna_MAX_WORKERS` | Anzahl der CPU-Kerne - 1 | Anzahl paralleler Inspektionsaufgaben |

#### [logging] Abschnitt

Dieser Abschnitt konfiguriert das Logging-Verhalten:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` oder `DEBUG` | `INFO` für Produktion, `DEBUG` zur Fehlerbehebung |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Anzahl der täglichen Log-Backups, die aufbewahrt werden |

---

### Schritt 3: Repository testen

1. Öffnen Sie die Eingabeaufforderung
2. Navigieren Sie in Ihr digna-Installationsverzeichnis (dort, wo `config.toml` und die ausführbare Datei `digna` liegen)
3. Führen Sie den Verbindungstest aus:

```bash
digna repo check
```

Sie sollten eine Bestätigung sehen, dass die Verbindung hergestellt wurde (das Repository selbst wurde noch nicht initialisiert).

### Schritt 4: Repository-Schema installieren

Führen Sie im selben Verzeichnis aus:

```bash
digna repo install
```

Dieser Befehl legt die notwendigen Tabellen und das Schema in Ihrer PostgreSQL-Datenbank an.

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

### Schritt 6: Einen Admin-Benutzer anlegen

1. Öffnen Sie ein **neues** Eingabeaufforderungsfenster
2. Navigieren Sie in Ihr digna-Installationsverzeichnis
3. Führen Sie den folgenden Befehl aus, um einen Admin-Benutzer zu erstellen:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Beispiel:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Dies erstellt einen Benutzer mit vollständigen Administratorrechten.

!!! tip "Beste Praxis"

    Verwenden Sie ein starkes Passwort mit einer Mischung aus Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen.

---

## Dashboard-Konfiguration {: #dashboard-configuration }

### Schritt 1: Dashboard auf dem Webserver bereitstellen

Das digna-Dashboard hat eine eigene `config.toml`-Datei im Verzeichnis `dashboard/`. Diese Konfiguration ist bereits vorhanden und erfordert für die Erstinstallation normalerweise keine Änderungen. Sie müssen sie nur anpassen, wenn Sie die Backend-Verbindung individuell konfigurieren möchten.

Wenn Sie die Dashboard-Konfiguration ändern müssen (z. B. bei Multi-Instance-Deployments), konsultieren Sie die Dokumentation des Dashboards.

Wählen Sie Ihren Webserver und folgen Sie den entsprechenden Bereitstellungsschritten.

#### Bereitstellung auf IIS

1. **IIS-Manager öffnen**
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
   - Sie sollten die Login-Seite des digna-Dashboards sehen

#### Bereitstellung auf Apache Tomcat

1. **Dashboard nach Tomcat kopieren**
   - Kopieren Sie den `dashboard`-Ordner in Ihr Tomcat-`webapps`-Verzeichnis
   - Benennen Sie ihn bei Bedarf um (z. B. in `digna`)
   - Beispiel: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Bereitstellung überprüfen**
   - Aktualisieren oder laden Sie die Tomcat-Verwaltungsseite neu (http://localhost:8080)
   - Sie sollten "digna" (oder Ihren gewählten Namen) in der Liste der bereitgestellten Anwendungen sehen

3. **Dashboard aufrufen**
   - Öffnen Sie Ihren Browser
   - Navigieren Sie zu `http://localhost:8080/digna`
   - Sie sollten die Login-Seite des digna-Dashboards sehen

---

## Ausführen von digna als Windows-Dienst {: #running-digna-as-a-windows-service }

### Warum einen Windows-Dienst verwenden?

Das Ausführen des digna-Backends als Windows-Dienst stellt sicher, dass es:
- Beim Systemstart automatisch gestartet wird
- Im Hintergrund ohne offenes Eingabeaufforderungsfenster läuft
- Bei Absturz automatisch neu gestartet werden kann
- Über die Windows-Diensteverwaltung gesteuert werden kann

### Service-verwaltende Dateien

Alle erforderlichen Dateien befinden sich im digna-Installationsverzeichnis unter: `bin/`

Die folgenden Batch-Dateien sind verfügbar:
- `install_service.bat` — Registriert digna als Windows-Dienst
- `uninstall_service.bat` — Deinstalliert den Dienst
- `start_service.bat` — Startet den Dienst
- `stop_service.bat` — Stoppt den Dienst

!!! warning "Administratorrechte erforderlich"

    Alle Batch-Dateien müssen mit Administratorrechten ausgeführt werden.

### Dienst installieren

1. **Eingabeaufforderung als Administrator öffnen**
   - Rechtsklicken Sie auf die Eingabeaufforderung
   - Wählen Sie "Als Administrator ausführen"

2. **Zum bin-Ordner wechseln**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Installationsskript ausführen**
   ```bash
   install_service.bat
   ```

Der digna-Server ist nun als Windows-Dienst mit aktivierter **automatischer** Startart registriert. Der Dienst startet nicht automatisch sofort — siehe nächsten Abschnitt zum Starten.

### Dienst starten und stoppen

#### Dienst starten

1. Öffnen Sie die Eingabeaufforderung als Administrator
2. Wechseln Sie in `digna\bin`
3. Führen Sie aus:
   ```bash
   start_service.bat
   ```

#### Dienst stoppen

1. Öffnen Sie die Eingabeaufforderung als Administrator
2. Wechseln Sie in `digna\bin`
3. Führen Sie aus:
   ```bash
   stop_service.bat
   ```

!!! tip "Tipp"

    Stoppen Sie den Dienst immer vor dem Aktualisieren von Anwendungsdateien.

### Dienst in ein neues Verzeichnis verschieben

Wenn Sie die digna-Installation verschieben müssen:

1. **Aktuellen Dienst deinstallieren**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Anwendungsdateien verschieben**
   - Verschieben Sie den gesamten digna-Installationsordner an den neuen Speicherort

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

## Upgrade auf eine neue Version {: #upgrading-to-a-new-release }

### Bevor Sie upgraden

**Ein Backup des digna-Repositories ist obligatorisch**

Erstellen Sie vor dem Upgrade ein Backup Ihres Repositories (PostgreSQL), um Datenverlust zu vermeiden. Ein Backup stellt sicher, dass Sie im Fall unerwarteter Probleme während des Upgrades wiederherstellen können.

### Upgrade-Prozess

#### Schritt 1: digna-Service stoppen

Wenn digna als Windows-Dienst ausgeführt wird, stoppen Sie ihn zuerst:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Schritt 2: Aktuelle Backend-Installation sichern

In Ihrem digna-Installationsverzeichnis:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Schritt 3: Neue Version entpacken und bereitstellen

1. Entpacken Sie die neue digna-Installations-ZIP-Datei
2. Kopieren Sie die neue ausführbare Datei `digna` und den `dashboard`-Ordner in Ihr Installationsverzeichnis


!!! warning "Wichtig"

    Die `config.toml`-Datei ist **niemals** in der Installations-ZIP enthalten. Ihre bestehende Konfiguration bleibt erhalten.

### Schritt 4: Konfigurationsdateien wiederherstellen

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Schritt 5: Repository-Schema upgraden

Wechseln Sie in Ihr digna-Installationsverzeichnis und führen Sie aus:

```bash
digna repo upgrade
```

Dies aktualisiert das PostgreSQL-Schema auf die neueste Version und erhält alle vorhandenen Daten.

### Schritt 6: Dienste neu starten

Wenn Sie als Windows-Dienst ausführen:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Wenn Sie manuell ausführen, starten Sie den Server neu:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Wenn Sie IIS oder Tomcat verwenden, starten Sie den jeweiligen Webserver neu.

#### Schritt 7: Upgrade überprüfen

1. Rufen Sie das digna-Dashboard auf
2. Prüfen Sie, ob die Oberfläche korrekt geladen wird
3. Überprüfen Sie die Server-Logs auf Fehler
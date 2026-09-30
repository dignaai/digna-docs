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

- **digna**: Der Kern der Anwendung, zuständig für die Verarbeitung von Daten und die Durchführung von Qualitätsprüfungen. Er vereint Backend und Kommandozeilenschnittstelle in einer einzigen ausführbaren Datei und ersetzt damit die früher getrennten Programme `dignabackend` und `dignacli`.
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

!!! info "Konfigurations- und Lizenzdateien sind nicht im Paket enthalten"

    Weder `config.toml` noch `dashboard/dashboard_config.toml` wird mit der Installation
    ausgeliefert — Sie legen beide selbst an, unter [Backend-Konfiguration](#backend-configuration) und
    [Dashboard-Konfiguration](#dashboard-configuration). Auch `license.toml` ist nicht enthalten;
    digna stellt sie separat bereit, wie in Schritt 3 beschrieben.

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
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Wert | Hinweise |
|---|---|---|
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

| Parameter | Wert | Hinweise |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Entspricht Ihrer Frontend-Domain |
| `digna_COOKIE_SECURE` | `false` (lokal) / `true` (Produktion) | Verwenden Sie `true` bei HTTPS-Verbindungen |
| `digna_COOKIE_HTTPONLY` | `true` | Immer aus Sicherheitsgründen aktiviert |
| `digna_COOKIE_SAME_SITE` | `lax` | Verhindert CSRF-Angriffe |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 Stunden) | Session-Timeout in Sekunden |
| `digna_MAX_WORKERS` | Anzahl der CPU-Kerne - 1 | Anzahl paralleler Inspektionsaufgaben |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Maximale Verzögerung in Sekunden, die der Scheduler vor dem Start eines fälligen Jobs hinzufügen darf |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Uhrzeit (24-Stunden-Format `HH:MM`), zu der die tägliche Bereinigung startet |

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` oder `DEBUG` | `INFO` für Produktion, `DEBUG` zur Fehlerbehebung |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Anzahl der täglichen Log-Backups, die aufbewahrt werden |

---

### Schritt 2: Konfiguration prüfen

Prüfen Sie vor der Initialisierung des Repositories, ob `config.toml` vollständig und korrekt aufgebaut ist. Führen Sie in Ihrem digna-Installationsverzeichnis aus:

```bash
digna config check
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

Overall: OK
```

Beheben Sie alles, was als FAILED gemeldet wird, und führen Sie den Befehl erneut aus, bevor Sie fortfahren. Die vollständige Liste der Optionen finden Sie in der [CLI-Referenz](../../../cli/Command_Line_Interface_202606.md).

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

### Schritt 5: Einen Admin-Benutzer anlegen

1. Öffnen Sie ein **neues** Eingabeaufforderungsfenster
2. Navigieren Sie in Ihr digna-Installationsverzeichnis
3. Führen Sie den folgenden Befehl aus, um einen Admin-Benutzer zu erstellen:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Beispiel:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Dies erstellt einen Benutzer mit vollständigen Administratorrechten.

!!! tip "Beste Praxis"

    Verwenden Sie ein starkes Passwort mit einer Mischung aus Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen.

---

### Schritt 6: digna-Server starten

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

!!! note "Der Server belegt das Terminal"

    `serve` läuft im Vordergrund und bleibt aktiv, bis Sie es mit ++ctrl+c++ beenden. Lassen Sie es laufen, während Sie die Einrichtung abschließen — wie Sie den Server stattdessen automatisch beim Systemstart starten, steht unter [digna als Windows-Dienst ausführen](#running-digna-as-a-windows-service).


## Dashboard-Konfiguration {: #dashboard-configuration }

### Schritt 1: Dashboard auf dem Webserver bereitstellen

Das digna-Dashboard liest seine eigene Konfiguration aus `dashboard/dashboard_config.toml`. Diese Datei wird nicht mit der Installation ausgeliefert — Sie legen sie im `dashboard/`-Verzeichnis neben den Dashboard-Dateien an.

Ihr Inhalt ist unter [Single Sign-on](../../../sso/overview.md) beschrieben, wo die Datei auch benötigt wird: Sie enthält die Anmeldeoptionen, die das Dashboard anbietet, und bei Multi-Instance-Deployments die Backend-Verbindung.

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

### Die `windows`-Befehle

Der Dienst wird von der ausführbaren Datei `digna` selbst verwaltet, über die Unterbefehle
`digna windows`. Es gibt keine Batch-Dateien auszuführen.

| Befehl | Zweck |
|---|---|
| `digna windows install` | Registriert digna als Windows-Dienst |
| `digna windows start` | Startet den registrierten Dienst |
| `digna windows stop` | Stoppt den laufenden Dienst |
| `digna windows uninstall` | Hebt die Registrierung des Dienstes auf |

!!! warning "Administratorrechte erforderlich"

    Alle vier Befehle müssen in einer als Administrator geöffneten Eingabeaufforderung ausgeführt werden.

Jeder Befehl akzeptiert `--name`, um einen Dienst anzusprechen, der unter einem vom Standard
abweichenden Namen registriert ist. Die vollständige Liste der Optionen finden Sie in der
[CLI-Referenz](../../../cli/Command_Line_Interface_202606.md).

### Dienst installieren

1. **Eingabeaufforderung als Administrator öffnen**
   - Rechtsklicken Sie auf die Eingabeaufforderung
   - Wählen Sie "Als Administrator ausführen"

2. **Zu Ihrem digna-Installationsverzeichnis wechseln**
   ```bash
   cd C:\path\to\digna
   ```

3. **Dienst registrieren**
   ```bash
   digna windows install
   ```

!!! important "Geben Sie Adresse und Port an, sofern die Standardwerte nicht passen"

    `install` hinterlegt Adresse und Port in der Dienstregistrierung, und der Dienst bindet sich
    genau an die hinterlegten Werte. Die Standardwerte sind `127.0.0.1` und `8000`, die nur
    Verbindungen vom Rechner selbst annehmen. Ein Dashboard auf einem anderen Host kann diese
    Adresse nicht erreichen. Geben Sie daher die Adresse an, auf der das Backend lauschen soll:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Diese Werte werden nicht aus der `config.toml` gelesen. Um sie später zu ändern, deinstallieren
    Sie den Dienst und installieren Sie ihn mit den neuen Werten erneut.

Der Dienst wird mit **automatischer** Startart registriert und startet daher mit Windows. Er startet
nicht sofort — siehe nächsten Abschnitt.

#### Installationsoptionen

| Option | Standard | Zweck |
|---|---|---|
| `--name` | `digna` | Name, unter dem der Dienst registriert wird |
| `--display-name` | `digna` | In services.msc angezeigter Name |
| `--description` | `digna data quality backend` | In services.msc angezeigte Beschreibung |
| `--address` | `127.0.0.1` | Adresse, an die der Dienst seine API bindet |
| `--port` | `8000` | Port, an den der Dienst seine API bindet |
| `--working-dir` | das Verzeichnis der ausführbaren Datei `digna` | Verzeichnis mit `config.toml` und `license.toml`, das der Dienst zu seinem Arbeitsverzeichnis macht |
| `--start-type` | `auto` | `auto` startet mit Windows, `manual` startet nur auf Anforderung, `disabled` registriert den Dienst, verweigert aber seinen Start |
| `--account` | `LocalSystem` | Konto, unter dem der Dienst läuft, z. B. `DOMAIN\user` oder `.\user` |
| `--password` | | Passwort von `--account` |

!!! tip "Ausführen unter einem Domänenkonto"

    `LocalSystem` hat keine Netzwerkidentität, daher schlagen die Windows-Authentifizierung gegenüber
    SQL Server und jeder Zugriff auf eine Netzwerkfreigabe fehl. Installieren Sie mit `--account` und
    `--password`, wenn der Dienst Ressourcen als bestimmter Benutzer erreichen muss.

### Dienst starten und stoppen

#### Dienst starten

```bash
digna windows start
```

#### Dienst stoppen

```bash
digna windows stop
```

!!! tip "Tipp"

    Stoppen Sie den Dienst immer vor dem Aktualisieren von Anwendungsdateien.

### Dienst in ein neues Verzeichnis verschieben

Wenn Sie die digna-Installation verschieben müssen:

1. **Aktuellen Dienst stoppen und abmelden**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Anwendungsdateien verschieben**
   - Verschieben Sie den gesamten digna-Installationsordner an den neuen Speicherort

3. **Dienst vom neuen Speicherort aus erneut registrieren**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Wiederholen Sie alle Werte für `--address`, `--port` oder `--account`, die Sie beim ersten Mal
   verwendet haben — die vorherige Registrierung ist entfernt.

4. **Dienst starten**
   ```bash
   digna windows start
   ```

### Dienst deinstallieren

1. **Laufenden Dienst stoppen**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Dienst abmelden**
   ```bash
   digna windows uninstall
   ```

Der digna-Server ist nun als Windows-Dienst abgemeldet.

---

## Upgrade auf eine neue Version {: #upgrading-to-a-new-release }

### Bevor Sie upgraden

**Prüfen Sie zuerst alle Datenbankverbindungen**

Ab Release 2026.06 erreicht digna jede Quelltechnologie über **ODBC**. Frühere Releases boten die
Wahl zwischen einem technologiespezifischen Treiber und ODBC, ausgewählt über den Schalter
**Use ODBC**. Das digna-Team hat sich entschieden, allein auf ODBC zu setzen, weil eine einzige,
standardisierte Schnittstelle mehr bietet als eine Reihe maßgeschneiderter Treiber:

- **Authentifizierung** — die Authentifizierung ist Teil von ODBC, sodass eine Verbindung alles
  nutzen kann, was ihr Treiber unterstützt: Passwörter, Tokens und PATs, Kerberos und Active
  Directory, MFA und browserbasiertes Single Sign-on, Cloud-Identitäten, Client-Zertifikate und
  TLS. Neue Verfahren kommen mit einem Treiber-Update, statt auf ein digna-Release zu warten.
- **Von den Datenbankherstellern gepflegte Treiber** — der herstellereigene Treiber folgt neuen
  Serverversionen und Sicherheitsupdates, und Sie können ihn unabhängig von digna nach Ihrem
  eigenen Zeitplan aktualisieren.
- **Eine einheitliche Konfiguration** — jede Technologie ist eine Liste von Schlüssel-Wert-Paaren,
  mit derselben Oberfläche, derselben Verschlüsselung sensibler Werte und derselben Fehlersuche,
  statt unterschiedlicher Felder je Quelle.
- **Feinabstimmung und Reichweite** — Treiberoptionen wie Timeouts, TLS-Einstellungen, Proxys und
  Fetch-Größen stehen für jede Quelle zur Verfügung, und jede Technologie mit einem konformen
  ODBC-Treiber lässt sich anbinden, auch solche, für die digna keine eigene Anleitung
  veröffentlicht.

In der Praxis bedeutet das: Den Schalter **Use ODBC** und die separaten Felder für Host, Port,
Datenbank, Benutzer und Passwort gibt es nicht mehr. **Jede Verbindung, die nicht bereits ODBC
verwendet, muss auf ODBC umgestellt werden** — eine automatische Umwandlung gibt es nicht, planen
Sie dies also vor dem Upgrade ein:

1. Sehen Sie jede in Ihrer Installation definierte Datenbankverbindung durch und notieren Sie die,
   die noch kein ODBC verwenden — jede davon muss neu konfiguriert werden.
2. Installieren Sie den passenden ODBC-Treiber auf dem digna-Host — Verbindungen werden von dem
   Server geöffnet, auf dem das digna-Backend läuft, nicht vom Browser aus. Siehe
   [ODBC-Treiber auf dem digna-Host installieren](../../../databases/overview.md#install-the-driver).
3. Halten Sie die ODBC-Eigenschaften für jede betroffene Verbindung bereit. Die
   [Technologie-Anleitungen](../../../databases/overview.md#technology-guides) führen je Quelle
   einen erprobten Satz von Eigenschaften auf.

Stellen Sie nach dem Upgrade jede betroffene Verbindung auf ODBC um und testen Sie sie im
Dashboard — siehe
[Datenbankverbindung anlegen](../../../databases/overview.md#create-a-database-connection) und
[Verbindung testen](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks-Legacy-Verbindungen"

    Der Databricks-Legacy-Connector wurde in diesem Release entfernt. Stellen Sie diese
    Verbindungen auf den [Databricks](../../../databases/databricks_connector_guide.md)-Connector um.

**Ein Backup des digna-Repositories ist obligatorisch**

Erstellen Sie vor dem Upgrade ein Backup Ihres Repositories (PostgreSQL), um Datenverlust zu vermeiden. Ein Backup stellt sicher, dass Sie im Fall unerwarteter Probleme während des Upgrades wiederherstellen können.

### Upgrade-Prozess

#### Schritt 1: Alten Dienst stoppen und abmelden

Wenn digna als Windows-Dienst ausgeführt wird, stoppen Sie ihn mit den **Batch-Dateien Ihrer
aktuellen Installation** — die Befehle `digna windows` gehören zum neuen Release und sind noch
nicht verfügbar:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

Melden Sie den Dienst anschließend ab, ebenfalls mit der alten Batch-Datei. Die Registrierung
verweist auf die alte ausführbare Datei und deren Skripte, die beide durch dieses Upgrade ersetzt
werden, und kann daher nicht wiederverwendet werden:

```bash
uninstall_service.bat
```

!!! warning "Melden Sie den Dienst ab, bevor Sie etwas umbenennen"

    `uninstall_service.bat` liegt im `bin`-Ordner, den Sie gleich umbenennen, und ist das Einzige,
    das die von ihr angelegte Registrierung entfernen kann. Führen Sie sie aus, solange die alte
    Installation noch vorhanden ist. Wurde der Ordner bereits umbenannt, benennen Sie ihn zurück,
    melden Sie den Dienst ab und fahren Sie dann fort.

    Notieren Sie sich das Konto, unter dem der Dienst lief, sowie die Adresse und den Port, auf dem
    er erreichbar war — Sie benötigen diese Angaben in Schritt 9.

#### Schritt 2: Aktuelle Installation sichern

Benennen Sie in Ihrem digna-Installationsverzeichnis die Ordner Ihrer aktuellen Installation um, damit das neue Release daneben bereitgestellt werden kann:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend und dignacli werden nicht mehr verwendet"

    Ab Release 2026.06 werden `dignabackend` und `dignacli` durch die einzelne ausführbare Datei `digna` ersetzt, die Backend und CLI vereint. Behalten Sie `dignabackend_old` und `dignacli_old` nur so lange, bis Sie das Upgrade überprüft haben — danach können Sie beide Ordner löschen. Behalten Sie `dashboard_old`, bis Sie Ihre Konfigurationsdateien daraus wiederhergestellt haben (siehe Schritt 4). Auch der `bin`-Ordner entfällt: Seine Batch-Dateien steuerten den alten Dienst, und 2026.06 liefert sie nicht mehr aus. Sobald der Dienst in Schritt 1 abgemeldet wurde, stiften sie nur noch Verwirrung.

#### Schritt 3: Neue Version entpacken und bereitstellen

1. Entpacken Sie die neue digna-Installations-ZIP-Datei
2. Kopieren Sie die neue ausführbare Datei `digna` und den `dashboard`-Ordner in Ihr Installationsverzeichnis


!!! warning "Wichtig"

    Weder `config.toml` noch `dashboard/dashboard_config.toml` ist jemals in der
    Installations-ZIP enthalten — das digna-Team liefert keine der beiden Dateien aus. Ihre
    bestehende Konfiguration bleibt vom Upgrade daher unberührt, und die Kopien in den
    umbenannten `*_old`-Ordnern sind die einzigen, die Sie haben.

#### Schritt 4: Konfigurationsdateien wiederherstellen

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "Release 2026.06 ändert die config.toml"

    Drei Einstellungen sind neu und erforderlich, drei werden nicht mehr verwendet. Eine aus einem früheren Release übernommene `config.toml` enthält die neuen Einstellungen nicht, und digna startet nicht, solange sie fehlen. Ergänzen Sie Ihre bestehende `config.toml` um Folgendes:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Fügen Sie die beiden `[base]`-Schlüssel in Ihren vorhandenen Abschnitt `[base]` ein und ergänzen Sie `[encryption]` als neuen Abschnitt. Entfernen Sie anschließend die nicht mehr verwendeten Einstellungen: **`digna_FERNET_KEY`** aus `[base]` sowie **`digna_APP_HOST`** und **`digna_APP_PORT`** aus `[app]` — Adresse und Port bezieht der Server jetzt von `digna serve`.

    Was die einzelnen Einstellungen bewirken, steht unter [Backend-Konfiguration](#backend-configuration).

!!! warning "Single Sign-on: das Format von [oidc_clients] hat sich geändert"

    Release 2026.06 ersetzt das Array von Tabellen durch je eine Tabelle pro Anbieter, benannt nach dem Anbieterschlüssel. `DIGNA_OIDC_KEY` entfällt — der Schlüssel ist jetzt Teil der Abschnittsüberschrift.

    Vorher:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Nachher:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Wiederholen Sie den Abschnitt für jeden Anbieter und halten Sie jeden Schlüssel deckungsgleich mit dem `key` in der `dashboard_config.toml`. `digna config check` meldet `oidc_clients` als FAILED, solange die alte Form noch vorhanden ist. Betroffen sind nur Installationen, die Single Sign-on verwenden.

#### Schritt 5: Webserver neu laden

Das Dashboard besteht aus statischen Dateien, daher liefern Ihr Webserver — und der Browser —
möglicherweise noch die vorherige Version aus. Laden Sie den Webserver, der den `dashboard`-Ordner
bereitstellt, neu oder starten Sie ihn neu, und laden Sie die Seite anschließend mit einem
Hard Refresh neu (++ctrl+f5++).

#### Schritt 6: Konfiguration prüfen

Stellen Sie sicher, dass die aktualisierte `config.toml` vollständig ist, bevor Sie das Repository anfassen:

```bash
digna config check
```

Jeder Abschnitt muss OK melden. Beheben Sie alles, was als FAILED gemeldet wird, und führen Sie den Befehl erneut aus, bevor Sie fortfahren.

#### Schritt 7: Lizenzdatei ersetzen

Jedes Release wird separat lizenziert. Kopieren Sie die `license.toml`, die das digna-Team für
dieses Release bereitgestellt hat, in das Installationsverzeichnis und ersetzen Sie damit die alte:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Behalten Sie die bisherige Lizenz nicht"

    Eine `license.toml`, die für ein früheres Release ausgestellt wurde, deckt dieses Release
    nicht ab, und jeder Befehl, der die Lizenz prüft — `user`, `inspection`, `repo` — bricht ab,
    bevor er das Repository verändert, wenn die Prüfung fehlschlägt. Prüfen Sie die Lizenz,
    bevor Sie fortfahren:

    ```bash
    digna license check
    ```

#### Schritt 8: Repository-Schema upgraden

Wechseln Sie in Ihr digna-Installationsverzeichnis und führen Sie aus:

```bash
digna repo upgrade
```

Dies aktualisiert das PostgreSQL-Schema auf die neueste Version und erhält alle vorhandenen Daten.

#### Schritt 9: Dienst registrieren und starten

Die alte Registrierung wurde in Schritt 1 entfernt, daher wird der Dienst erneut registriert —
diesmal mit der ausführbaren Datei `digna`, die ohne Batch-Dateien auskommt:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Geben Sie für `--address` und `--port` die Werte an, auf denen der alte Dienst erreichbar war,
sofern Sie nicht die neuen Standardwerte `127.0.0.1` und `8000` möchten; sie werden in der
Registrierung hinterlegt und nicht mehr aus der `config.toml` gelesen. Ergänzen Sie `--account`
und `--password`, wenn der alte Dienst unter einem Domänenkonto lief. Die vollständige Liste der
Optionen finden Sie unter
[Ausführen von digna als Windows-Dienst](#running-digna-as-a-windows-service).

Wenn Sie manuell ausführen, starten Sie den Server neu:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Wenn Sie IIS oder Tomcat verwenden, starten Sie den jeweiligen Webserver neu.

#### Schritt 10: Upgrade überprüfen

1. Rufen Sie das digna-Dashboard auf
2. Prüfen Sie, ob die Oberfläche korrekt geladen wird
3. Überprüfen Sie die Server-Logs auf Fehler
4. Stellen Sie jede Verbindung, die noch kein ODBC verwendet hat, auf ODBC um und testen Sie anschließend alle Verbindungen — siehe [Verbindung testen](../../../databases/overview.md#testing-a-connection)
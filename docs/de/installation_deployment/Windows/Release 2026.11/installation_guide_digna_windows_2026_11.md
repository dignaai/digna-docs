---
title: Windows-Installationsanleitung – digna Release 2026.11 | digna Documentation
description: Schritt-für-Schritt-Anleitung zur Installation von digna Release 2026.11 auf Windows — Systemanforderungen, PostgreSQL-Einrichtung, Webserver-Konfiguration, Backend- und Dashboard-Konfiguration, Ausführen von digna als Windows-Dienst und Upgrade von Release 2026.06.
keywords: digna Windows-Installation, digna Bereitstellungsanleitung, digna Backend-Setup, digna Dashboard-Installation, PostgreSQL Einrichtung, digna Windows-Dienst, digna Upgrade-Anleitung
image: /assets/logo_square.png
---

# Windows-Installationsanleitung für digna Release 2026.11

**Release:** 2026.11

**Zuletzt aktualisiert:** 7. November 2026


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

### Neu in Release 2026.11

Dieses Release ergänzt digna Data Reconciliation, digna Agentic mit dem digna MCP Server und die digna Engine, die Daten innerhalb von digna profilieren und die referenzielle Integrität zwischen unterschiedlichen Datenbanktechnologien prüfen kann. Details finden Sie in den [Release Notes](../../../changelog/Release_202611.md).

Für die Installation bringt das Release einen neuen Mechanismus für Repository-Migrationen, einen optionalen Abschnitt `[duckdb]` in der `config.toml` für die digna Engine und eine neue Lizenzdatei. Der [Abschnitt zum Upgrade](#upgrading-to-a-new-release) behandelt jeden dieser Punkte.

### Suchen Sie macOS oder Linux?

Dieses Handbuch behandelt Windows. Für andere Plattformen siehe die [macOS Installationsanleitung](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) oder die [Linux Installationsanleitung](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Datenbankverbindungen, die die digna Engine als Profiling-Ort verwenden, werden auf dem
    digna-Host selbst profiliert. Planen Sie dafür zusätzlichen Arbeitsspeicher und
    Festplattenplatz ein, siehe den [Abschnitt \[duckdb\]](#duckdb-section).

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
| `DIGNA_REPO_USER` | `digna_user` | In der PostgreSQL-Einrichtung erstellter Benutzer |
| `DIGNA_REPO_PASSWORD` | Ihr Passwort | Während der Schema-Erstellung gesetztes Passwort |
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
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 Stunden) | Session-Timeout in Sekunden |
| `DIGNA_MAX_WORKERS` | Anzahl der CPU-Kerne - 1 | Anzahl der Inspektionen, die gleichzeitig laufen dürfen |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Erforderlich. Wird für die Links in Benachrichtigungen verwendet und muss daher eine URL sein, die die Empfänger öffnen können |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (Standard) | Optional. Sekunden, die eine einzelne Abfrage gegen eine Quelldatenbank laufen darf, bevor sie abgebrochen wird; `0` deaktiviert das Timeout |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (Standard) | Optional. Sekunden, die auf eine Verbindung zu einer Quelldatenbank gewartet wird; `0` wartet unbegrenzt |

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
| `DIGNA_LOGGING_MODE` | `INFO` oder `DEBUG` | `INFO` für Produktion, `DEBUG` zur Fehlerbehebung. `TRACE`, `WARN` und `ERROR` werden ebenfalls akzeptiert |
| `DIGNA_LOGGING_DIR` | `logs` (Standard) | Optional. Verzeichnis für die rotierenden Log-Dateien, relativ zum Arbeitsverzeichnis |
| `DIGNA_LOGGING_MAX_FILES` | `30` (Standard) | Optional. Anzahl der rotierten Log-Dateien, die aufbewahrt werden |

!!! warning "Log-Verzeichnis beim Betrieb als Dienst beibehalten"

    Ein Windows-Dienst hat keine Konsole, daher sind die Log-Dateien die einzige Aufzeichnung
    dessen, was der Dienst tut. Setzen Sie `DIGNA_LOGGING_DIR` nicht auf einen leeren String,
    denn das schaltet die Log-Dateien ab.

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
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parameter | Wert | Hinweise |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (Standard) | Arbeitsspeicher in MB, den ein einzelner Lauf der digna Engine belegen darf. Bis zu `DIGNA_MAX_WORKERS` Läufe können gleichzeitig aktiv sein |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standard: das temporäre Verzeichnis des Kontos, unter dem digna läuft (`%TEMP%`) | Verzeichnis für temporäre Dateien, wenn die Daten nicht in den Arbeitsspeicher passen |

!!! tip "Dimensionierung der digna Engine"

    Planen Sie auf dem digna-Host bis zu `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB`
    Arbeitsspeicher zusätzlich zu dem ein, was digna selbst belegt, sowie genug freien
    Festplattenplatz im temporären Verzeichnis, um den größten inspizierten Tag der Datenquellen
    aufzunehmen, die die digna Engine verwenden. Lassen Sie `DIGNA_DUCKDB_TEMP_DIRECTORY` auf einen
    Datenträger mit so viel Platz zeigen, der für das Konto beschreibbar ist, unter dem digna läuft:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Sie benötigen diesen Abschnitt nur, wenn mindestens eine Datenbankverbindung die digna Engine
    verwendet oder eine Prüfung der referenziellen Integrität Datenquellen auf unterschiedlichen
    Verbindungen vergleicht.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Beheben Sie alles, was als FAILED gemeldet wird, und führen Sie den Befehl erneut aus, bevor Sie fortfahren. Eine WARNING unter **Unknown keys** listet Schlüssel in der `config.toml` auf, die digna nicht liest; sie haben keine Wirkung, entfernen Sie sie also oder korrigieren Sie ihre Schreibweise. Die vollständige Liste der Optionen finden Sie in der [CLI-Referenz](../../../cli/Command_Line_Interface_202611.md).

### Schritt 3: Repository testen

1. Öffnen Sie die Eingabeaufforderung
2. Navigieren Sie in Ihr digna-Installationsverzeichnis (dort, wo `config.toml` und die ausführbare Datei `digna` liegen)
3. Führen Sie den Verbindungstest aus:

```bash
digna repo check
```

Bei einem neuen Schema stellt der Befehl die Verbindung her und meldet dann, dass noch kein Repository installiert ist:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

An dieser Stelle ist das das erwartete Ergebnis: Es bestätigt, dass digna PostgreSQL und das Schema erreicht. Ein Verbindungs- oder Authentifizierungsfehler weist dagegen auf den Abschnitt `[repo]` oder auf die PostgreSQL-Einrichtung hin.

### Schritt 4: Repository-Schema installieren

Führen Sie im selben Verzeichnis aus:

```bash
digna repo upgrade
```

Dieser Befehl legt die benötigten Tabellen im Repository-Schema an und endet mit:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installiert und aktualisiert"

    Ab Release 2026.11 installiert `repo upgrade` ein neues Repository und aktualisiert ein
    bestehendes. `repo install` funktioniert weiterhin als anderer Name für denselben Befehl.

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
- `--address` — Server-Hostname/IP (Standard `127.0.0.1`)
- `--port` — Server-Port (Standard `8000`)

Sobald der Server läuft, gibt er die Adresse aus, auf der er lauscht:

```text
Server running on http://127.0.0.1:8082
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
[CLI-Referenz](../../../cli/Command_Line_Interface_202611.md).

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

Dieser Abschnitt aktualisiert eine Installation von Release 2026.06 auf Release 2026.11.

!!! warning "Upgrade von einem Release vor 2026.06"

    Führen Sie zuerst die Upgrade-Schritte von Release 2026.06 aus: [Upgrade auf eine neue Version](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). Fahren Sie danach mit den folgenden Schritten fort.

### Bevor Sie ein Upgrade durchführen

**Ein Backup des digna-Repositorys ist verpflichtend**

Erstellen Sie vor einem Upgrade von digna ein Backup Ihres Repositorys (PostgreSQL), um Datenverlust zu vermeiden.
Ein Backup stellt sicher, dass Sie im Falle unerwarteter Probleme bei einem Upgrade wiederherstellen können.

**Lizenzdatei für Release 2026.11 anfordern**

Release 2026.11 benötigt eine neue `license.toml`. Fordern Sie sie vor dem Start beim digna-Team an
und halten Sie sie für [Schritt 7](#step-7-replace-the-license-file) bereit.

### Upgrade-Ablauf

#### Schritt 1: digna-Dienst stoppen {: #step-1-stop-the-digna-service }

Öffnen Sie eine Eingabeaufforderung als Administrator und stoppen Sie den Dienst mit der
`digna`-Executable Ihrer aktuellen Installation:

```bash
cd C:\path\to\digna
digna windows stop
```

Der Dienst bleibt registriert. Die neue ausführbare Datei tritt im selben Verzeichnis an die Stelle
der alten, sodass die Registrierung weiterhin auf die richtige Datei zeigt.

Falls digna im Vordergrund läuft, drücken Sie in dessen Eingabeaufforderungsfenster ++ctrl+c++.

#### Schritt 2: Aktuelle Installation sichern {: #step-2-backup-current-installation }

Benennen Sie in Ihrem digna-Installationsverzeichnis die ausführbare Datei und den Dashboard-Ordner
Ihrer aktuellen Installation um, damit das neue Release daneben bereitgestellt werden kann:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Behalten Sie `digna_old.exe`, bis Sie das Upgrade überprüft haben, und `dashboard_old`, bis Sie Ihre
Konfigurationsdateien daraus wiederhergestellt haben (siehe Schritt 4). Danach können Sie beide löschen.

#### Schritt 3: Neue Version entpacken und bereitstellen {: #step-3-extract-and-deploy-new-version }

1. Entpacken Sie die neue digna-Installations-ZIP-Datei
2. Kopieren Sie die neue `digna`-Executable und den `dashboard`-Ordner in Ihr Installationsverzeichnis

!!! warning "Wichtig"

    Weder `config.toml` noch `dashboard/dashboard_config.toml` ist jemals in der
    Installations-ZIP enthalten — das digna-Team liefert keine der beiden Dateien aus. Ihre
    bestehende Konfiguration bleibt vom Upgrade daher unberührt, und die Kopien in den
    umbenannten `*_old`-Ordnern sind die einzigen, die Sie haben.

#### Schritt 4: Konfigurationsdateien wiederherstellen {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
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
Hard Refresh neu (++ctrl+f5++).

#### Schritt 6: Konfiguration prüfen {: #step-6-validate-the-configuration }

Stellen Sie sicher, dass die `config.toml` vollständig ist, bevor Sie das Repository anfassen:

```bash
digna config check
```

Jeder Abschnitt muss OK melden. Beheben Sie alles, was als FAILED gemeldet wird, entfernen Sie die
unter **Unknown keys** aufgeführten Schlüssel und führen Sie den Befehl erneut aus, bevor Sie fortfahren.

#### Schritt 7: Lizenzdatei ersetzen {: #step-7-replace-the-license-file }

Eine für ein früheres Release ausgestellte Lizenzdatei funktioniert mit Release 2026.11 nicht.
Kopieren Sie die `license.toml`, die das digna-Team für Release 2026.11 bereitgestellt hat, in das
Installationsverzeichnis und ersetzen Sie damit die alte:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Behalten Sie die bisherige Lizenz nicht"

    Mit der bisherigen Lizenz schlägt jeder Befehl fehl, der die Lizenz prüft — `serve`, `user`,
    `inspection`, `repo` —, sodass digna nicht startet und kein Upgrade des Repositorys möglich ist.
    Prüfen Sie die neue Lizenz, bevor Sie fortfahren:

    ```bash
    digna license check
    ```

#### Schritt 8: Repository-Schema upgraden {: #step-8-upgrade-the-repository-schema }

Führen Sie in Ihrem digna-Installationsverzeichnis aus:

```bash
digna repo upgrade
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
Sie `digna repo check` aus: Der Befehl listet die zuletzt angewendete Migration und alle noch
ausstehenden auf.

!!! warning "digna startet nicht auf einem veralteten Repository"

    Ab Release 2026.11 verweigert der Server den Start, solange das Repository ein Upgrade
    benötigt, und meldet das, zum Beispiel:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Führen Sie `repo upgrade` aus, bevor Sie den Server oder den Dienst starten.

#### Schritt 9: Dienste neu starten {: #step-9-restart-services }

Wenn digna als Windows-Dienst läuft, starten Sie ihn erneut:

```bash
cd C:\path\to\digna
digna windows start
```

Wenn Sie es manuell betreiben, starten Sie den Server neu:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Wenn Sie IIS oder Tomcat verwenden, starten Sie den jeweiligen Webserver neu.

#### Schritt 10: Upgrade verifizieren {: #step-10-verify-the-upgrade }

1. Prüfen Sie das Release der neuen ausführbaren Datei:

    ```bash
    digna version
    ```

    Die erste Zeile muss `Release: 2026.11` lauten.

2. Rufen Sie das digna-Dashboard auf und prüfen Sie, ob die Oberfläche korrekt geladen wird.
3. Prüfen Sie die Dateien im Verzeichnis `logs` der Installation auf Fehler.
4. Testen Sie Ihre Datenbankverbindungen — siehe
   [Verbindung testen](../../../databases/overview.md#testing-a-connection).

Für den Einstieg in die neuen Module siehe [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[KI-Agenten verbinden](../../../platform/agentic/connect_ai_agent.md) für den digna MCP Server und
[Profiling-Ort](../../../platform/profiling/profiling_location.md) für die digna Engine.

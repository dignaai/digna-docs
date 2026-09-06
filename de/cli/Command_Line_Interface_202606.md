# digna CLI-Referenz 2026.06
**2026-09-05**

Diese Seite dokumentiert den vollständigen Satz an Befehlen, die im ***digna*** CLI Release **2026.06** verfügbar sind, einschließlich Anwendungsbeispielen und Optionen.

Die ausführbare Datei heißt `digna`.

---

## CLI-Grundlagen

---

### Überblick & Syntax

Das CLI des Releases **2026.06** verwendet eine strukturierte, kategoriebasierte Befehlshierarchie:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` und `serve` sind Einzelbefehle ohne Unterbefehl:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Globale Optionen

Die folgenden globalen Optionen gelten für alle Befehle:

- `--help`, `-h`: Zeigt Hilfeinformationen zum CLI oder zu einer bestimmten Befehlskategorie bzw. einem Unterbefehl an.
- `--stacktrace`: Zeigt im Fehlerfall die vollständige Fehlerkette an statt nur der obersten Meldung.

`--stacktrace` ist im strengen Sinne eine globale Option: Sie muss **vor** der Befehlskategorie angegeben werden, nicht danach.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Es gibt kein `--version`-Flag. Verwenden Sie stattdessen den Befehl [`version`](#version).

### Voraussetzungen

Die meisten Befehle benötigen eine lesbare, gültige `config.toml`; einige erfordern zusätzlich eine gültige Lizenz.
Die folgende Tabelle hält fest, was jede Befehlskategorie lädt, bevor sie überhaupt etwas tut:

| Befehlskategorie | Benötigt `config.toml` | Benötigt eine gültige Lizenz |
|---|---|---|
| `version` | nein | nein |
| `config check` | nein (sie ist genau das, worüber der Befehl berichtet) | nein |
| `license check` | nein | sie *ist* die Prüfung |
| `crypt` | ja | nein |
| `serve` | ja | nein |
| `project` | ja | nein |
| `user` | ja | ja |
| `inspection` | ja | ja |
| `repo` | ja | ja |

Wo eine Lizenz erforderlich ist, werden sowohl ihre Signatur als auch ihr Ablaufdatum geprüft, und der Befehl bricht ab, bevor er das Repository berührt, wenn eines von beidem fehlschlägt.

### Exit-Codes

- `0`: Der Befehl war erfolgreich.
- `1`: Der Befehl ist fehlgeschlagen. Die Fehlermeldung wird nach stderr geschrieben, mit dem Präfix `Error: `.

### help

Die Option `--help` liefert Informationen zu verfügbaren Befehlskategorien, Unterbefehlen und Optionen:

1. **Allgemeine Hilfe anzeigen:**
   ```bash
   digna --help
   ```

2. **Hilfe zu bestimmten Kategorien und Befehlen abrufen:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Die Ausgabe umfasst:**
   - **Befehlsbeschreibung:** Zusammenfassung des Befehlszwecks.
   - **Syntax:** Erforderliche und optionale Argumente.
   - **Optionen:** Flags und Parameter, die für den Befehl spezifisch sind.

### version

Der Befehl `version` gibt das installierte ***digna***-Release aus. Er liest keine Konfiguration und validiert keine Lizenz, sodass er auch auf einer Installation funktioniert, deren `config.toml` oder Lizenz fehlt oder ungültig ist.

Die Release-Version ist unabhängig von der Version des Repository-Schemas, die von [`repo check`](#repo-check) gemeldet wird.

#### Befehlsverwendung
```bash
digna version
```

#### Beispielausgabe
```text
2026.06
```

---

## Konfigurationsverwaltung

---

### config check

Der Befehl `config check` validiert die Konfigurationsdatei (`config.toml`) und prüft, ob alle obligatorischen Abschnitte und Einstellungen vorhanden und korrekt formatiert sind. Jeder Abschnitt wird für sich validiert, sodass ein defekter `[app]`-Abschnitt den Zustand von `[repo]` nicht verdeckt.

Gemeldet werden die folgenden Abschnitte:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — optional; ein fehlender Schlüssel besteht die Prüfung, eine vorhandene, aber fehlerhafte Liste nicht

Der Befehl lädt die Anwendungskonfiguration bewusst nicht so, wie die anderen Befehle es tun, damit er eine `config.toml` diagnostizieren kann, die ***digna*** überhaupt am Starten hindern würde.

#### Befehlsverwendung
```bash
digna config check [OPTIONS]
```

#### Optionen
- `--configpath`, `-c`: Pfad zur Konfigurationsdatei oder zu einem Verzeichnis, das `config.toml` enthält (Standard: `./config.toml`).
- `--json`: Gibt den Validierungsbericht als JSON aus. Hat Vorrang vor `--quiet`.
- `--quiet`, `-q`: Unterdrückt den Bericht und verlässt sich ausschließlich auf den Exit-Code.

#### Beispiel
```bash
digna config check
```

Eine bestimmte Konfigurationsdatei validieren und die Ausgabe als JSON formatieren:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Beispielausgabe
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

Eine fehlende Datei oder ein TOML-Syntaxfehler lässt nichts übrig, was abschnittsweise validiert werden könnte, und wird unabhängig von `--quiet` oder `--json` als einzelner Fehler statt als Bericht gemeldet.

---

## Repository-Verwaltung

---

### repo check

Der Befehl `repo check` testet die Datenbankverbindung und überprüft Installation und Version des Repositorys. Er schlägt fehl, wenn das konfigurierte Schema nicht existiert oder wenn es zwar existiert, aber kein ***digna***-Repository enthält.

Die gemeldete Version ist die Version des Repository-Schemas, die getrennt vom ***digna***-Release versioniert wird, das [`version`](#version) ausgibt.

#### Befehlsverwendung
```bash
digna repo check
```

#### Beispielausgabe
```text
Repo version 3.0.0 installed
```

### repo install

Der Befehl `repo install` installiert ein neues ***digna***-Repository in das in `config.toml` konfigurierte Schema und legt dabei alle erforderlichen Sequenzen, Tabellen, Indizes, Constraints und Initialdatensätze an.

Das Schema selbst wird von diesem Befehl **nicht** erstellt — es muss vorher vorhanden sein. Der Befehl weigert sich außerdem zu laufen, wenn in diesem Schema bereits ein Repository installiert ist, und verweist auf [`repo upgrade`](#repo-upgrade), falls die installierte Version eine ältere ist.

#### Befehlsverwendung
```bash
digna repo install
```

#### Beispielausgabe
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Der Befehl `repo upgrade` wendet Datenbankschema-Migrationen an, um ein bestehendes Repository auf die vom installierten Release erwartete Version zu bringen. Upgrades werden entlang eines festen Upgrade-Pfads jeweils um einen Versionsschritt angewendet, und jeder abgeschlossene Schritt wird im Repository festgehalten.

Ist das Repository bereits auf der erwarteten Version, meldet der Befehl, dass kein Upgrade nötig ist, und nimmt keine Änderungen vor.

#### Befehlsverwendung
```bash
digna repo upgrade
```

#### Beispielausgabe
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Verschlüsselungsverwaltung

---

### crypt gen-key

Der Befehl `crypt gen-key` erzeugt einen neuen AES-GCM-Verschlüsselungsschlüssel zur Verwendung als Verschlüsselungsschlüssel in `config.toml`. Eine ladbare `config.toml` muss bereits vorhanden sein, auch wenn der erzeugte Schlüssel nicht von ihr abhängt.

#### Befehlsverwendung
```bash
digna crypt gen-key
```

#### Beispielausgabe
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Der Befehl `crypt encrypt` verschlüsselt eine Zeichenkette (etwa ein Datenbankkennwort) mit dem in `config.toml` konfigurierten AES-GCM-Schlüssel und gibt den Geheimtext aus.

#### Befehlsverwendung
```bash
digna crypt encrypt <VALUE>
```

#### Argumente
- **VALUE**: Die zu verschlüsselnde Klartext-Zeichenkette (erforderlich).

#### Beispiel
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Der Befehl `crypt decrypt` entschlüsselt eine AES-GCM-verschlüsselte Zeichenkette mit dem in `config.toml` konfigurierten Schlüssel und gibt den Klartext aus.

#### Befehlsverwendung
```bash
digna crypt decrypt <VALUE>
```

#### Argumente
- **VALUE**: Die zu entschlüsselnde verschlüsselte Zeichenkette (erforderlich).

#### Beispiel
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Benutzerverwaltung

---

### user add

Der Befehl `user add` legt ein neues Benutzerkonto im ***digna***-Repository an. Der Befehl schlägt fehl, wenn bereits ein Benutzer mit der angegebenen E-Mail-Adresse existiert.

#### Befehlsverwendung
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumente
- **EMAIL**: Die E-Mail-Adresse des Benutzers (erforderlich).
- **PASSWORD**: Das initiale Kennwort des Benutzers (erforderlich).
- **DISPLAY_NAME**: Der vollständige Anzeigename des Benutzers (erforderlich).

#### Optionen
- `--admin`, `-a`: Legt den Benutzer mit Administratorrechten (Superuser) an.

#### Beispiel
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

So legen Sie ein Administratorkonto an:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Beispielausgabe
```text
User created with ID: 42
```

### user list

Der Befehl `user list` listet alle registrierten Benutzer in Tabellenform mit ID, E-Mail, Anzeigename und Administrator-Flag auf.

#### Befehlsverwendung
```bash
digna user list
```

#### Beispielausgabe
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Der Befehl `user modify` aktualisiert den Anzeigenamen und die Administratorrechte eines bestehenden Benutzerkontos, das über die E-Mail-Adresse identifiziert wird.

Sowohl der Anzeigename als auch das Administrator-Flag werden immer geschrieben. `--admin` ist ein Schalter, kein Wert: **Wird die Option weggelassen, werden die Administratorrechte entzogen**, geben Sie sie also immer dann an, wenn der Benutzer sie behalten oder erhalten soll.

#### Befehlsverwendung
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumente
- **EMAIL**: Die E-Mail-Adresse des zu ändernden Benutzers (erforderlich).
- **DISPLAY_NAME**: Der aktualisierte Anzeigename (erforderlich).

#### Optionen
- `--admin`, `-a`: Gewährt Administratorrechte. Weglassen, um sie zu entziehen.
- `--valid-until`, `-v`: Wird aus Kompatibilitätsgründen akzeptiert, aber **derzeit nicht angewendet**. Die Übergabe gibt eine Warnung aus und ändert nichts.

#### Beispiel
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Beispielausgabe
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Der Befehl `user modify-pwd` aktualisiert das Kennwort eines bestehenden Benutzerkontos.

#### Befehlsverwendung
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumente
- **EMAIL**: Die E-Mail-Adresse des Benutzers, dessen Kennwort aktualisiert werden soll (erforderlich).
- **PASSWORD**: Das neue Kennwort (erforderlich).

#### Beispiel
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Der Befehl `user delete` entfernt ein Benutzerkonto aus dem System.

#### Befehlsverwendung
```bash
digna user delete <EMAIL>
```

#### Argumente
- **EMAIL**: Die E-Mail-Adresse des zu löschenden Benutzers (erforderlich).

#### Beispiel
```bash
digna user delete jdoe@example.com
```

---

## Projekt- & Datenquellenverwaltung

---

### project list

Der Befehl `project list` listet alle im Repository verfügbaren Projekte mit ihrer ID, ihrem Namen und ihrer Beschreibung auf.

#### Befehlsverwendung
```bash
digna project list
```

#### Beispielausgabe
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Der Befehl `project list-ds` listet alle einem bestimmten Projekt zugeordneten Datenquellen mit ihrer ID, ihrem Namen, ihrer Art, ihrem Schema und ihrem Tabellennamen auf.

#### Befehlsverwendung
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, dessen Datenquellen aufgelistet werden sollen (erforderlich). Der Name muss exakt übereinstimmen.

#### Beispiel
```bash
digna project list-ds ProjectA
```

#### Beispielausgabe
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Der Befehl `project export-ds` exportiert Datenquellen eines Projekts in ein JSON-Dokument.

Wird weder `--table-name` noch `--table-id` angegeben, werden alle Datenquellen des Projekts exportiert.

#### Befehlsverwendung
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, aus dem Datenquellen exportiert werden sollen (erforderlich).

#### Optionen
- `--table-name`, `-n`: Namen der zu exportierenden Datenquellen. Mehrere Namen können durch Leerzeichen getrennt angegeben werden.
- `--table-id`, `-i`: IDs der zu exportierenden Datenquellen. Mehrere IDs können durch Leerzeichen getrennt angegeben werden.
- `--exportfile`, `-f`: Pfad, unter dem die exportierten Datenquellen gespeichert werden (Standard: `data_sources_export.json`).

#### Beispiel
So exportieren Sie alle Datenquellen aus `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

So exportieren Sie bestimmte Tabellen:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Beispielausgabe
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Der Befehl `project import-ds` importiert Datenquellen aus einer Exportdatei in ein Zielprojekt und meldet pro Objekt, was angelegt, aktualisiert oder übersprungen wurde.

#### Befehlsverwendung
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumente
- **PROJECT_NAME**: Name des Zielprojekts, in das importiert wird (erforderlich).
- **EXPORT_FILE**: Pfad zur JSON-Exportdatei (erforderlich).

#### Optionen
- `--output-file`, `-o`: Datei, in die der Importbericht geschrieben wird. Ohne diese Option geht der Bericht nach stdout.
- `--output-format`, `-f`: Format des Importberichts — `table`, `json` oder `csv` (Standard: `table`).

#### Beispiel
```bash
digna project import-ds ProjectB my_export.json
```

So erfassen Sie einen maschinenlesbaren Bericht:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Der Bericht umfasst vier Objektebenen — Datenquelle, Datensatzdefinition, Attribut und Validierungsregel — jeweils mit ihrer Importaktion, dem Ergebnis, der resultierenden Objekt-ID und etwaigen Zusatzinformationen.

### project plan-import-ds

Der Befehl `project plan-import-ds` zeigt eine Vorschau des Datenquellen-Imports in ein Zielprojekt und stellt dar, welche Objekte angelegt, aktualisiert oder übersprungen würden, ohne etwas zu verändern. Er nimmt dieselbe Exportdatei und dieselben Berichtsoptionen entgegen wie [`project import-ds`](#project-import-ds) und ergänzt eine Schrittnummer pro geplantem Objekt.

#### Befehlsverwendung
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumente
- **PROJECT_NAME**: Name des Zielprojekts (erforderlich).
- **EXPORT_FILE**: Pfad zur Exportdatei (erforderlich).

#### Optionen
- `--output-file`, `-o`: Datei, in die der Importplan geschrieben wird. Ohne diese Option geht der Plan nach stdout.
- `--output-format`, `-f`: Format des Importplans — `table`, `json` oder `csv` (Standard: `table`).

#### Beispiel
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Inspektionsverwaltung

---

### inspection run

Der Befehl `inspection run` erstellt eine Inspektionsanforderung für ein Projekt und einen Datumsbereich und wartet anschließend — je nach den angegebenen Optionen — entweder darauf, kehrt sofort zurück oder führt sie im eigenen Prozess aus.

Die drei Ausführungsmodi sind:

- **Standard (kein Flag)**: Die Anforderung wird für das Backend in die Warteschlange gestellt, und das CLI fragt sie alle zwei Sekunden ab und gibt den Aufgabenfortschritt aus, bis die Inspektion einen Endzustand erreicht. Ein laufendes `digna serve` ist erforderlich, sonst nimmt niemand die Anforderung auf.
- **`--async-mode`**: Die Anforderung wird in die Warteschlange gestellt und ihre ID sofort ausgegeben. Verwenden Sie [`inspection status`](#inspection-status), um sie zu verfolgen.
- **`--bypass-backend`**: Die Inspektion wird vom CLI-Prozess selbst ausgeführt und nicht in die Warteschlange gestellt, sodass kein laufender Server erforderlich ist.

`--async-mode` und `--bypass-backend` schließen einander aus.

In jedem Modus endet der Befehl mit einem Exit-Code ungleich null, wenn die Inspektion nicht erfolgreich abgeschlossen wurde.

#### Befehlsverwendung
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Zielprojekts (erforderlich). Der Name muss exakt übereinstimmen.
- **START_DATE**: Startdatum des Datumsbereichs im Format `YYYY-MM-DD` (erforderlich).
- **END_DATE**: Enddatum des Datumsbereichs im Format `YYYY-MM-DD` (erforderlich).

#### Optionen
- `--table-name`: Beschränkt die Inspektion auf eine einzelne Datenquelle des Projekts, angegeben über ihren Datenquellennamen. Ohne diese Option werden alle Datenquellen des Projekts inspiziert.
- `--async-mode`: Stellt die Inspektion in die Warteschlange und gibt die Anforderungs-ID aus, statt auf sie zu warten. Kann nicht mit `--bypass-backend` kombiniert werden.
- `--bypass-backend`: Führt die Inspektion direkt im CLI-Prozess aus, statt sie für das Backend in die Warteschlange zu stellen. Kann nicht mit `--async-mode` kombiniert werden.

#### Beispiel
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

So reichen Sie eine asynchrone Inspektion ein:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

So inspizieren Sie eine einzelne Datenquelle:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Beispielausgabe
Standardmodus:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asynchroner Modus:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Der Befehl `inspection status` fragt Zustand und Aufgabenfortschritt einer Inspektionsanforderung anhand ihrer Anforderungs-ID ab.

#### Befehlsverwendung
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumente
- **INSPECTION_REQUEST_ID**: Die numerische ID der Inspektionsanforderung (erforderlich).

#### Beispiel
```bash
digna inspection status 1024
```

#### Beispielausgabe
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Der Befehl `inspection abort` fordert den Abbruch laufender oder ausstehender Inspektionsanforderungen an. Er zeichnet für jede betroffene Anforderung ein Stopp-Ereignis auf; das Backend handelt daraufhin, ein Abbruch ist also eine Aufforderung zum Anhalten und kein sofortiges Beenden.

#### Befehlsverwendung
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumente
- **INSPECTION_REQUEST_ID**: Die ID der abzubrechenden Inspektionsanforderung. Erforderlich, sofern nicht `--killall` angegeben wird.

#### Optionen
- `--killall`: Bricht alle derzeit laufenden und ausstehenden Inspektionsanforderungen ab. Hat Vorrang vor einer gleichzeitig angegebenen Anforderungs-ID.

#### Beispiel
So brechen Sie eine bestimmte Anforderung ab:
```bash
digna inspection abort 1024
```

So brechen Sie alle aktiven und wartenden Inspektionen ab:
```bash
digna inspection abort --killall
```

#### Beispielausgabe
`--killall` meldet, was es getan hat; der Abbruch einer einzelnen Anforderung erzeugt keine Ausgabe und meldet den Erfolg über seinen Exit-Code.
```text
All running and pending inspections have been aborted.
```

---

## Lizenzverwaltung

---

### license check

Der Befehl `license check` validiert `license.toml`, überprüft die Signatur gegen den mit der Installation ausgelieferten öffentlichen Schlüssel und stellt sicher, dass die Lizenz nicht abgelaufen ist. Er liest keine Anwendungskonfiguration und funktioniert daher auch, bevor `config.toml` eingerichtet ist.

#### Befehlsverwendung
```bash
digna license check
```

#### Beispielausgabe
```text
License is valid
```

Eine ungültige Signatur und eine abgelaufene Lizenz werden als unterschiedliche Fehler gemeldet, beide mit Exit-Code 1.

---

## Server- & Hintergrunddienste

---

### serve

Der Befehl `serve` startet den ***digna***-REST-API-Server zusammen mit dem Hintergrund-Inspektionsplaner und dem Inspektionsmanager. Beim Start lässt er außerdem jede Inspektion fehlschlagen, die das Repository noch als laufend führt, da aus einem früheren Prozess nichts überlebt haben kann.

Der Befehl läuft im Vordergrund, bis er beendet wird.

#### Befehlsverwendung
```bash
digna serve [OPTIONS]
```

#### Optionen
- `--address`: Netzwerkadresse, an die der API-Server gebunden wird (Standard: `127.0.0.1`).
- `--port`: Portnummer, auf der gelauscht wird (Standard: `8000`).

#### Beispiel
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Beispielausgabe
```text
Server running on http://0.0.0.0:8000
```
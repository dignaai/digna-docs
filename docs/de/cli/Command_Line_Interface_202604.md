---
title: digna CLI Referenz 2026.04 – Befehle & Beispiele | digna Dokumentation
description: Vollständige Referenz für die digna CLI-Version 2026.04
image: /assets/logo_square.png
---

# digna CLI Referenz 2026.04
**2026-04-08**

Diese Seite dokumentiert die vollständige Menge der in der ***digna*** CLI-Version **2026.04** verfügbaren Befehle, einschließlich Anwendungsbeispiele und Optionen.

---

## CLI-Grundlagen

---

### Hilfe (`--help`)
Die Option `--help` liefert Informationen über verfügbare Befehle und deren Verwendung. Es gibt zwei Hauptmöglichkeiten, diese Option zu verwenden:

1. **Allgemeine Hilfe anzeigen:**
   
    Verwenden Sie `--help` unmittelbar nach dem Stichwort ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Hilfe für spezifische Befehle anzeigen:**  
  
    Für detaillierte Informationen zu einem bestimmten Befehl hängen Sie `--help` an diesen Befehl an.
    Beispielsweise, um Hilfe für den Befehl `add-user` zu erhalten, führen Sie aus:
     ```bash
     dignacli add-user --help
     ```

     ### Ausgabe:
      
     - **Befehlsbeschreibung:** Bietet eine detaillierte Beschreibung der Funktion des Befehls.  
     - **Syntax:** Zeigt die genaue Syntax, einschließlich erforderlicher und optionaler Argumente.  
     - **Optionen:** Listet alle befehlspezifischen Optionen mit ihren Erklärungen auf.  
     - **Beispiele:** Liefert Beispiele zur effektiven Ausführung des Befehls.

### Konfiguration prüfen (`check-config`)
Der Befehl `check-config` ist ein Hilfsprogramm innerhalb des ***digna*** CLI-Tools, das dazu dient, die Konfiguration von ***digna*** zu testen. Dieser Befehl stellt sicher, dass die ***digna***-Komponenten die benötigten Konfigurationselemente in der `config.toml` finden können.

#### Optionen

- `--configpath`, `-cp`: Datei oder Verzeichnis, das die Konfiguration enthält. Falls weggelassen, wird `../config.toml` verwendet.
      
#### Befehlsverwendung
```bash
dignacli check-config
```

Nach erfolgreicher Ausführung gibt der Befehl eine Bestätigung über die Vollständigkeit der Konfiguration aus.  
  
Wenn die Konfiguration unvollständig zu sein scheint, werden die fehlenden Konfigurationselemente aufgelistet.

  
### Repository-Verbindung prüfen (`check-repo-connection`)
Der Befehl `check-repo-connection` ist ein Hilfsprogramm innerhalb des ***digna*** CLI-Tools, das die Konnektivität und den Zugriff auf ein angegebenes ***digna***-Repository testet. Dieser Befehl stellt sicher, dass das CLI mit dem Repository interagieren kann.
      
#### Befehlsverwendung
```bash
dignacli check-repo-connection
```

Nach erfolgreicher Ausführung gibt der Befehl eine Bestätigung der Verbindung aus, zusammen mit Details zum Repository: Repository-Version, Host, Datenbank und Schema.  
  
Wenn die Verbindung zum Repository nicht erfolgreich ist, prüfen Sie die `config.toml`-Datei auf korrekte Konfigurationseinstellungen.


### Version (`--version`)

Um die installierte Version von *dignacli* zu prüfen, verwenden Sie die Option `--version`.  
  
#### Befehlsverwendung
```bash
dignacli --version
```
  
#### Beispielausgabe
```bash
dignacli version 2026.04
```

### Protokollierungsoptionen
  
Standardmäßig ist die Konsolenausgabe der ***digna***-Befehle minimalistisch gehalten. Die meisten Befehle bieten die Möglichkeit, zusätzliche Informationen bereitzustellen, mithilfe der folgenden Optionen:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ und „debug“ legen das Detaillierungslevel fest, während der Schalter „logfile“ erlaubt, die Ausgabe in eine Datei umzuleiten, anstatt sie im Konsolenfenster anzuzeigen.

## Benutzerverwaltung

### Benutzer hinzufügen (`add-user`)
  
Der Befehl `add-user` in der ***digna*** CLI wird verwendet, um einen neuen Benutzer im ***digna***-System anzulegen.
  
#### Befehlsverwendung
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumente

- **USER_NAME**: Der Benutzername für den neuen Benutzer (erforderlich).
- **USER_FULL_NAME**: Der vollständige Name des neuen Benutzers (erforderlich).
- **USER_PASSWORD**: Das Passwort für den neuen Benutzer (erforderlich).

#### Optionen

- `--is_superuser`, `-su`: Kennzeichnet den neuen Benutzer als Administrator.
- `--valid_until`, `-vu`: Setzt ein Ablaufdatum für das Benutzerkonto im Format `YYYY-MM-DD HH:MI:SS`. Wenn nicht gesetzt, hat das Konto kein Ablaufdatum.

#### Beispiel

Um einen neuen Benutzer mit dem Benutzernamen `jdoe`, dem vollständigen Namen `John Doe` und dem Passwort `password123` hinzuzufügen:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Um einen neuen Benutzer hinzuzufügen und ein Ablaufdatum für das Konto festzulegen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Benutzer löschen (`delete-user`)
  
Der Befehl `delete-user` in der ***digna*** CLI wird verwendet, um einen bestehenden Benutzer aus dem ***digna***-System zu entfernen.
  
#### Befehlsverwendung
```bash
dignacli delete-user USER_NAME
```
  
#### Argumente
- **USER_NAME**: Der Benutzername des zu löschenden Benutzers (erforderlich). Dies ist das einzige vom Befehl benötigte Argument.

#### Beispiel
```bash
dignacli delete-user jdoe
```
  
Die Ausführung dieses Befehls entfernt den Benutzer `jdoe` aus dem ***digna***-System, entzieht dessen Zugriff und löscht die zugehörigen Daten und Berechtigungen aus dem Repository.

### Benutzer ändern (`modify-user`)

Der Befehl `modify-user` in der ***digna*** CLI wird verwendet, um die Angaben eines bestehenden Benutzers im ***digna***-System zu aktualisieren.

#### Befehlsverwendung
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumente
  
- **USER_NAME**: Der Benutzername des zu ändernden Benutzers (erforderlich).
- **USER_FULL_NAME**: Der neue vollständige Name des Benutzers (erforderlich).
  
#### Optionen  
  
- `--is_superuser`, `-su`: Setzt den Benutzer als Superuser und gewährt erhöhte Rechte. Dieser Flag erfordert keinen Wert.  
- `--valid_until`, `-vu`: Setzt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS. Wenn nicht angegeben, bleibt das Konto unbegrenzt gültig.  
  
#### Beispiel
  
Um den vollständigen Namen des Benutzers `jdoe` in „Johnathan Doe“ zu ändern und den Benutzer als Superuser zu setzen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Benutzerpasswort ändern (`modify-user-pwd`)
  
Der Befehl `modify-user-pwd` in der ***digna*** CLI wird verwendet, um das Passwort eines bestehenden Benutzers im ***digna***-System zu ändern.
  
#### Befehlsverwendung
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumente
  
- **USER_NAME**: Der Benutzername des Benutzers, dessen Passwort geändert werden soll (erforderlich).
- **USER_PWD**: Das neue Passwort für den Benutzer (erforderlich).
  
#### Beispiel
  
Um das Passwort des Benutzers `jdoe` in `newpassword123` zu ändern:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Benutzer auflisten (`list-users`)

Der Befehl `list-users` in der ***digna*** CLI zeigt eine Liste aller im ***digna***-System registrierten Benutzer an.

#### Befehlsverwendung

```bash
dignacli list-users
```

Die Ausführung dieses Befehls in der ***digna*** CLI verbindet sich mit dem ***digna***-Repository und listet alle Benutzer auf, einschließlich ihrer ID, ihres Benutzernamens, vollständigen Namens, Superuser-Status und Ablaufzeitstempeln.

## Repository-Verwaltung

### Repository aktualisieren (`upgrade-repo`)
  
Der Befehl `upgrade-repo` in der ***digna*** CLI wird verwendet, um das ***digna***-Repository zu aktualisieren oder zu initialisieren. Dieser Befehl ist essentiell, um Updates anzuwenden oder die Repository-Infrastruktur zum ersten Mal einzurichten.
  
#### Befehlsverwendung

```bash
dignacli upgrade-repo [options]
```
  
#### Optionen
  
- `--simulation-mode`, `-s`: Wenn aktiviert, führt dieser Modus den Befehl im Simulationsmodus aus, der die SQL-Anweisungen ausgibt, die ausgeführt würden, ohne sie tatsächlich auszuführen. Dies ist nützlich, um Änderungen zu überprüfen, ohne das Repository zu verändern.  

  
#### Beispiel
  
Um das ***digna***-Repository zu aktualisieren, können Sie den Befehl ohne Optionen ausführen:
  
```bash
dignacli upgrade-repo
```  
Um das Upgrade im Simulationsmodus auszuführen (um die SQL-Anweisungen zu sehen, ohne sie anzuwenden):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dieser Befehl ist wichtig für die Wartung des ***digna***-Systems und stellt sicher, dass das Datenbankschema und andere Repository-Komponenten mit der neuesten Softwareversion übereinstimmen.

### Passwort verschlüsseln (`encrypt`)
  
Der Befehl `encrypt` in der ***digna*** CLI wird verwendet, um ein Passwort zu verschlüsseln.
  
#### Befehlsverwendung
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumente
- **PASSWORD**: Das zu verschlüsselnde Passwort (erforderlich).
  
#### Beispiel
  
Um ein Passwort zu verschlüsseln, müssen Sie das Passwort als Argument angeben.   
Beispielsweise, um das Passwort `mypassword123` zu verschlüsseln, verwenden Sie:
```bash
dignacli encrypt mypassword123
```
Dieser Befehl gibt die verschlüsselte Version des angegebenen Passworts aus, die dann in sicheren Kontexten verwendet werden kann. Wenn das Passwort-Argument nicht angegeben wird, zeigt das CLI einen Fehler an, der auf das fehlende Argument hinweist.

### Schlüssel generieren (`generate-key`)
  
Der Befehl `generate-key` wird verwendet, um einen Fernet-Schlüssel zu erzeugen, der für die Sicherung von Passwörtern im ***digna***-Repository erforderlich ist.
  
#### Befehlsverwendung
```bash
dignacli generate-key
```
  
## Datenverwaltung

### Aufräumen (`clean-up`)

Der Befehl `clean-up` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Ampelsystemdaten für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu entfernen. Dieser Befehl ist wichtig für das Daten-Lifecycle-Management und hilft, eine organisierte und effiziente Datenumgebung zu erhalten, indem veraltete oder unnötige Daten gelöscht werden.

#### Befehlsverwendung

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, aus dem Daten entfernt werden sollen (erforderlich). Die Verwendung des Schlüsselworts `all-projects` in diesem Argument weist ***digna*** an, über alle vorhandenen Projekte zu iterieren und diesen Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Datenlöschung. Akzeptierte Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Datenlöschung, im selben Format wie FROM_DATE (erforderlich).
  
#### Optionen
  
- `--table-name`, `-tn`: Beschränkt die Aufräumaktion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filter zur Beschränkung des Aufräumens auf Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--timing`, `-tm`: Zeigt die Dauer des Aufräumprozesses nach Abschluss an.
- `--help`: Zeigt Hilfeinformationen für den `clean-up`-Befehl an und beendet das Programm.
  
#### Beispiel
  
Um Daten aus dem Projekt `ProjectA` zwischen dem 1. Januar 2023 und dem 30. Juni 2023 zu entfernen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Um Daten nur aus einer bestimmten Tabelle namens `Table1` zu entfernen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dieser Befehl hilft bei der Verwaltung des Datenspeichers und stellt sicher, dass das Repository nur relevante Informationen enthält.

### Orphan-Objekte entfernen (`remove-orphans`)
  
Der Befehl `remove-orphans` in der ***digna*** CLI wird für Aufräumarbeiten im ***digna***-Repository verwendet.  
Wenn ein Benutzer Projekte oder Datenquellen löscht, bleiben Profile und Vorhersagen im Repository zurück. Mit diesem Befehl werden solche verwaisten Zeilen aus dem Repository entfernt.
  
#### Befehlsverwendung
  
```bash
dignacli list-projects
```

### Projekte auflisten (`list-projects`)
  
Der Befehl `list-projects` in der ***digna*** CLI zeigt eine Liste aller verfügbaren Projekte im ***digna***-System an.
  
#### Befehlsverwendung
  
```bash
dignacli list-projects
```

Dieser Befehl ist besonders nützlich für Administratoren und Benutzer, die mehrere Projekte verwalten, und bietet einen schnellen Überblick über die im ***digna***-Repository verfügbaren Projekte.

### Datenquellen auflisten (`list-ds`)

Der Befehl `list-ds` in der ***digna*** CLI dient dazu, eine Liste aller verfügbaren Datenquellen innerhalb eines angegebenen Projekts anzuzeigen. Dieser Befehl ist nützlich, um die im ***digna***-System für Analyse und Verwaltung verfügbaren Datenbestände zu verstehen.

#### Befehlsverwendung
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, für das die Datenquellen aufgelistet werden (erforderlich).
  
#### Beispiel
  
Um alle Datenquellen im Projekt mit dem Namen `ProjectA` aufzulisten:
  
```bash
dignacli list-ds ProjectA
```
  
Dieser Befehl verschafft den Benutzern einen Überblick über die in einem Projekt verfügbaren Datenquellen und hilft ihnen dabei, die Datenlandschaft effizienter zu navigieren und zu verwalten.


### Inspektion durchführen (`inspect`)

Der Befehl `inspect` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Ampelsystemdaten für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erzeugen. Dieser Befehl hilft, Daten über einen definierten Zeitraum zu analysieren und zu überwachen. Nach Abschluss der Inspektion wird der Wert des berechneten Ampelsystems zurückgegeben:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Befehlsverwendung

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das Daten inspiziert werden sollen (erforderlich). Die Verwendung des Schlüsselworts `all-projects` in diesem Argument weist ***digna*** an, über alle vorhandenen Projekte zu iterieren und diesen Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Dateninspektion. Akzeptierte Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Dateninspektion, im selben Format wie FROM_DATE (erforderlich).
  
#### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert, um nur Tabellen zu inspizieren, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--enable_notification`, `-en`: Aktiviert das Senden von Benachrichtigungen im Falle von Alerts.
- `--bypass-backend`, `-bb`: Backend umgehen und die Inspektion direkt aus dem CLI heraus ausführen (nur zu Testzwecken!).

  
#### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 zu inspizieren:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Um nur eine bestimmte Tabelle zu inspizieren und die Neuberechnung von Vorhersagen zu erzwingen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dieser Befehl ist nützlich, um aktualisierte Profile und Vorhersagen zu erzeugen, die Datenintegrität zu überwachen und Alert-Systeme innerhalb eines bestimmten Projektzeitraums zu verwalten.

### Asynchrone Inspektion starten (`inspect-async`)

Der Befehl `inspect-async` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Ampelsystemdaten für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erzeugen. Dieser Befehl hilft, Daten über einen definierten Zeitraum zu analysieren und zu überwachen. Im Gegensatz zum synchronen `inspect`-Befehl wartet dieser Befehl nicht auf den Abschluss der Inspektion.
Stattdessen gibt er die Request-ID für die eingereichte Inspektions-Anfrage zurück. Um den Fortschritt des Inspektionsprozesses abzufragen, verwenden Sie den Befehl `inspect-status`.

#### Befehlsverwendung

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das Daten inspiziert werden sollen (erforderlich). Die Verwendung des Schlüsselworts `all-projects` in diesem Argument weist ***digna*** an, über alle vorhandenen Projekte zu iterieren und diesen Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Dateninspektion. Akzeptierte Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Dateninspektion, im selben Format wie FROM_DATE (erforderlich).
  
#### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert, um nur Tabellen zu inspizieren, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--enable_notification`, `-en`: Aktiviert das Senden von Benachrichtigungen im Falle von Alerts.

  
#### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 asynchron zu inspizieren:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### Inspektionsstatus abfragen (`inspect-status`)

Der Befehl `inspect-status` in der ***digna*** CLI wird verwendet, um den Fortschritt einer asynchronen Inspektion anhand der Request-ID zu prüfen.

#### Befehlsverwendung

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumente
  
- **REQUEST_ID**: Die von `inspect-async` zurückgegebene Request-ID.
  
#### Beispiel
  
Um den Fortschritt einer Inspektion mit der Request-ID 12345 zu prüfen:
  
```bash
dignacli inspect-status 12345
```

### Inspektion abbrechen (`inspect-cancel`)

Der Befehl `inspect-cancel` in der ***digna*** CLI wird verwendet, um Inspektionen anhand der Request-ID abzubrechen, oder er kann verwendet werden, um alle aktuellen Anfragen abzubrechen.

#### Befehlsverwendung

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumente
  
- **REQUEST_ID**: Die von `inspect-async` zurückgegebene Request-ID.
  
#### Beispiel
  
Um die Inspektion mit der Request-ID 12345 abzubrechen:
  
```bash
dignacli inspect-cancel 12345
```

Um alle aktuell laufenden oder wartenden Anfragen abzubrechen:
  
```bash
dignacli inspect-cancel --killall
```

  
### Datenquellen exportieren (`export-ds`)

Der Befehl `export-ds` in der ***digna*** CLI wird verwendet, um einen Export von Datenquellen aus dem ***digna***-Repository zu erstellen. Standardmäßig werden alle Datenquellen eines angegebenen Projekts exportiert.

#### Befehlsverwendung
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, aus dem die Datenquellen exportiert werden.

#### Optionen

- `--table_name`, `-tn`: Exportiert eine bestimmte Datenquelle aus einem Projekt.
- `--exportfile`, `-ef`: Gibt den Dateinamen für den Export an.
    
#### Beispiel
  
Um alle Datenquellen aus dem Projekt `ProjectA` zu exportieren:
  
```bash
dignacli export-ds ProjectA
```
  
Dieser Befehl exportiert alle Datenquellen aus `ProjectA` als JSON-Dokument, das in ein anderes Projekt oder ***digna***-Repository importiert werden kann.


### Datenquellen importieren (`import-ds`)

Der Befehl `import-ds` in der ***digna*** CLI wird verwendet, um Datenquellen in ein Zielprojekt zu importieren und einen Importbericht zu erstellen.

#### Befehlsverwendung
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, in das die Datenquellen importiert werden sollen.
- **EXPORT_FILE**: Der Dateiname des zu importierenden Datenquellen-Exports.

#### Optionen

- `--output-file`, `-o`: Datei zum Speichern des Importberichts (falls nicht angegeben, wird der Bericht tabellarisch im Terminal ausgegeben).
- `--output-format`, `-f`: Format zum Speichern des Importberichts (json, csv).
    
#### Beispiel
  
Um alle Datenquellen aus der Exportdatei `my_export.json` in `ProjectB` zu importieren:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Nach dem Import zeigt dieser Befehl auch einen Bericht über importierte und übersprungene Objekte an. Es werden nur neue Datenquellen in `ProjectB` importiert. Um herauszufinden, welche Objekte importiert und welche übersprungen würden, können Sie den Befehl `plan-import-ds` verwenden.

### Import-Plan anzeigen (`plan-import-ds`)

Der Befehl `plan-import-ds` in der ***digna*** CLI wird verwendet, um den Import von Datenquellen in ein Zielprojekt zu analysieren und einen Importbericht zu erstellen (Plan).

#### Befehlsverwendung
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, in das die Datenquellen analysiert importiert würden.
- **EXPORT_FILE**: Der Dateiname des Datenquellen-Exports, der vor dem Import analysiert werden soll.

#### Optionen

- `--output-file`, `-o`: Datei zum Speichern des Importberichts (falls nicht angegeben, wird der Bericht tabellarisch im Terminal ausgegeben).
- `--output-format`, `-f`: Format zum Speichern des Importberichts (json, csv).
    
#### Beispiel
  
Um zu prüfen, welche Datenquellen aus der Exportdatei `my_export.json` importiert und welche übersprungen würden, wenn sie in `ProjectB` importiert werden:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Dieser Befehl zeigt lediglich einen Importplan der zu importierenden und zu überspringenden Objekte an.
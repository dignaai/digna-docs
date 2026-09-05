# digna CLI Referenz 2025.04
**2025-04-01**

Diese Seite dokumentiert die vollständige Menge der in der ***digna*** CLI-Version **2025.04** verfügbaren Befehle, einschließlich Anwendungsbeispielen und Optionen.

---

## CLI Grundlagen

---

## Verwendung der Option `help`

Die Option `--help` liefert Informationen über verfügbare Befehle und deren Verwendung. Es gibt zwei Hauptarten, diese Option zu verwenden:

1. **Allgemeine Hilfe anzeigen:**
   
    Verwenden Sie --help unmittelbar nach dem Befehl ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Hilfe für bestimmte Befehle erhalten:**  
  
    Für detaillierte Informationen zu einem bestimmten Befehl fügen Sie `--help` an diesen Befehl an.
    Zum Beispiel, um Hilfe zum Befehl `add-user` zu erhalten, führen Sie aus:
     ```bash
     dignacli add-user --help
     ```

     ### Ausgabe:
      
     - **Befehlsbeschreibung:** Liefert eine detaillierte Beschreibung dessen, was der Befehl tut.  
     - **Syntax:** Zeigt die genaue Syntax, einschließlich erforderlicher und optionaler Argumente.  
     - **Optionen:** Listet alle optionsspezifischen Optionen mit ihren Erläuterungen auf.  
     - **Beispiele:** Bietet Beispiele dafür, wie der Befehl effektiv ausgeführt wird.

  
## Verwendung des Befehls `check-repo-connection`

Der Befehl check-repo-connection ist ein Hilfswerkzeug innerhalb des ***digna*** CLI-Tools, das dazu dient, die Konnektivität und den Zugriff auf ein angegebenes ***digna*** Repository zu testen. Dieser Befehl stellt sicher, dass die CLI mit dem Repository interagieren kann.
      
#### Befehlsverwendung
```bash
dignacli check-repo-connection
```

Bei erfolgreicher Ausführung gibt der Befehl eine Bestätigung der Verbindung sowie Details zum Repository aus: Repository-Version, Host, Datenbank und Schema.  
  
Wenn die Repository-Verbindung nicht erfolgreich ist, überprüfen Sie die Datei config.toml auf korrekte Konfigurationseinstellungen.

## Verwendung des Befehls `version`

Um die installierte Version von *dignacli* zu prüfen, verwenden Sie die Option --version.  
  
#### Befehlsverwendung
```bash
dignacli --version
```
  
#### Beispielausgabe
```bash
dignacli version 2025.04
```

## Verwendung von Logging-Optionen
  
Standardmäßig ist die Konsolenausgabe der ***digna*** Befehle minimalistisch gehalten. Die meisten Befehle bieten die Möglichkeit, zusätzliche Informationen auszugeben, mithilfe der folgenden Optionen:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
„verbose“ und „debug“ legen den Detaillierungsgrad fest, während der Schalter „logfile“ es ermöglicht, die Ausgabe in eine Datei umzuleiten, anstatt sie im Konsolenfenster anzuzeigen.

## Benutzerverwaltung

### Verwendung des Befehls `add-user`
  
Der Befehl add-user in der ***digna*** CLI wird verwendet, um einen neuen Benutzer zum ***digna*** System hinzuzufügen.
  
#### Befehlsverwendung
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumente

- **USER_NAME**: Der Benutzername für den neuen Benutzer (erforderlich).
- **USER_FULL_NAME**: Der vollständige Name des neuen Benutzers (erforderlich).
- **USER_PASSWORD**: Das Passwort für den neuen Benutzer (erforderlich).

#### Optionen

- `--is_superuser`, `-su`: Flag, um den neuen Benutzer als Administrator zu kennzeichnen.
- `--valid_until`, `-vu`: Legt ein Ablaufdatum für das Benutzerkonto im Format `YYYY-MM-DD HH:MI:SS` fest. Wenn nicht gesetzt, hat das Konto kein Ablaufdatum.

#### Beispiel

Um einen neuen Benutzer mit dem Benutzernamen `jdoe`, dem vollständigen Namen `John Doe` und dem Passwort `password123` hinzuzufügen:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Um einen neuen Benutzer hinzuzufügen und ein Ablaufdatum für das Konto festzulegen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Verwendung des Befehls `delete-user`
  
Der Befehl `delete-user` in der ***digna*** CLI wird verwendet, um einen vorhandenen Benutzer aus dem ***digna*** System zu entfernen.
  
#### Befehlsverwendung
```bash
dignacli delete-user USER_NAME
```
  
##### Argumente
- **USER_NAME**: Der Benutzername des zu löschenden Benutzers (erforderlich). Dies ist das einzige vom Befehl benötigte Argument.

#### Beispiel
```bash
dignacli delete-user jdoe
```
  
Bei Ausführung dieses Befehls wird der Benutzer `jdoe` aus dem ***digna*** System entfernt, sein Zugriff wird widerrufen und seine zugehörigen Daten sowie Berechtigungen im Repository werden gelöscht.

### Verwendung des Befehls `modify-user`

Der Befehl `modify-user` in der ***digna*** CLI wird verwendet, um die Details eines vorhandenen Benutzers im ***digna*** System zu aktualisieren.

#### Befehlsverwendung
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumente
  
- **USER_NAME**: Der Benutzername des zu ändernden Benutzers (erforderlich).
- **USER_FULL_NAME**: Der neue vollständige Name des Benutzers (erforderlich).
  
#### Optionen  
  
- `--is_superuser`, `-su`: Setzt den Benutzer als Superuser und gewährt erhöhte Berechtigungen. Dieses Flag benötigt keinen Wert.  
- `--valid_until`, `-vu`: Legt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS fest. Wenn nicht angegeben, bleibt das Konto unbegrenzt gültig.  
  
#### Beispiel
  
Um den vollständigen Namen des Benutzers `jdoe` in „Johnathan Doe“ zu ändern und den Benutzer als Superuser zu setzen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Verwendung des Befehls `modify-user-pwd`
  
Der Befehl `modify-user-pwd` in der ***digna*** CLI wird verwendet, um das Passwort eines vorhandenen Benutzers im ***digna*** System zu ändern.
  
#### Befehlsverwendung
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumente
  
- **USER_NAME**: Der Benutzername des Benutzers, dessen Passwort geändert werden soll (erforderlich).
- **USER_PWD**: Das neue Passwort für den Benutzer (erforderlich).
  
#### Beispiel
  
Um das Passwort für den Benutzer `jdoe` in `newpassword123` zu ändern:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Verwendung des Befehls `list-users`

Der Befehl `list-users` in der ***digna*** CLI zeigt eine Liste aller im ***digna*** System registrierten Benutzer an.

#### Befehlsverwendung

```bash
dignacli list-users
```

Bei Ausführung dieses Befehls verbindet sich die ***digna*** CLI mit dem ***digna*** Repository und listet alle Benutzer auf, wobei deren ID, Benutzername, vollständiger Name, Superuser-Status und Ablaufzeitstempel angezeigt werden.

## Repository-Verwaltung

### Verwendung des Befehls `upgrade-repo`
  
Der Befehl `upgrade-repo` in der ***digna*** CLI dient zum Aktualisieren oder Initialisieren des ***digna*** Repositories. Dieser Befehl ist essenziell, um Updates anzuwenden oder die Repository-Infrastruktur zum ersten Mal einzurichten.
  
#### Befehlsverwendung

```bash
dignacli upgrade-repo [options]
```
  
#### Optionen
  
- `--simulation-mode`, `-s`: Wenn aktiviert, führt dieser Schalter den Befehl im Simulationsmodus aus, druckt die SQL-Anweisungen, die ausgeführt würden, führt sie aber nicht tatsächlich aus. Dies ist nützlich, um Änderungen vorab zu prüfen, ohne das Repository zu verändern.  

  
#### Beispiel
  
Um das ***digna*** Repository zu aktualisieren, können Sie den Befehl ohne Optionen ausführen:
  
```bash
dignacli upgrade-repo
```  
Um das Upgrade im Simulationsmodus auszuführen (um die SQL-Anweisungen ohne Anwendung zu sehen):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dieser Befehl ist wichtig für die Wartung des ***digna*** Systems und stellt sicher, dass das Datenbankschema und andere Repository-Komponenten mit der neuesten Softwareversion übereinstimmen.

### Verwendung des Befehls `encrypt`
  
Der Befehl `encrypt` in der ***digna*** CLI wird verwendet, um ein Passwort zu verschlüsseln.
  
#### Befehlsverwendung
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumente
- **PASSWORD**: Das zu verschlüsselnde Passwort (erforderlich).
  
#### Beispiel
  
Um ein Passwort zu verschlüsseln, müssen Sie das Passwort als Argument angeben.   
Zum Beispiel, um das Passwort `mypassword123` zu verschlüsseln, würden Sie verwenden:
```bash
dignacli encrypt mypassword123
```
Dieser Befehl gibt die verschlüsselte Version des angegebenen Passworts aus, die dann in sicheren Kontexten verwendet werden kann. Wenn das Passwort-Argument nicht angegeben wird, zeigt die CLI einen Fehler an, der auf das fehlende Argument hinweist.

## Verwendung des Befehls `generate-key`
  
Der Befehl `generate-key` wird verwendet, um einen Fernet-Schlüssel zu generieren, der für die Sicherung von Passwörtern im ***digna*** Repository erforderlich ist.
  
#### Befehlsverwendung
```bash
dignacli generate-key
```
  
## Datenverwaltung

## Verwendung des Befehls `clean-up`

Der Befehl `clean-up` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Ampelsystems (Traffic Light System) für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu entfernen. Dieser Befehl ist wichtig für das Datenlebenszyklus-Management und hilft, eine organisierte und effiziente Datenumgebung durch das Löschen veralteter oder unnötiger Daten aufrechtzuerhalten.

#### Befehlsverwendung

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, aus dem Daten entfernt werden sollen (erforderlich). Die Verwendung des Schlüsselworts all-projects in diesem Argument weist ***digna*** an, über alle bestehenden Projekte zu iterieren und diesen Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startuhrzeit für die Datenlöschung. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Enduhrzeit für die Datenlöschung, entsprechend denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen
  
- `--table-name`, `-tn`: Beschränkt die Clean-up-Operation auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert, um das Clean-up auf Tabellen zu beschränken, die die angegebene Teilzeichenfolge im Namen enthalten.
- `--timing`, `-tm`: Zeigt die Dauer des Clean-up-Prozesses nach Abschluss an.
- `--help`: Zeigt Hilfsinformationen für den Clean-up-Befehl an und beendet die Ausführung.
  
#### Beispiel
  
Um Daten aus dem Projekt ProjectA zwischen dem 1. Januar 2023 und dem 30. Juni 2023 zu entfernen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Um Daten nur aus einer bestimmten Tabelle namens `Table1` zu entfernen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dieser Befehl hilft bei der Verwaltung des Datenspeichers und stellt sicher, dass das Repository nur relevante Informationen enthält.

## Verwendung des Befehls `list-projects`
  
Der Befehl `list-projects` in der ***digna*** CLI wird verwendet, um eine Liste aller verfügbaren Projekte im ***digna*** System anzuzeigen.
  
#### Befehlsverwendung
  
```bash
dignacli list-projects
```

Dieser Befehl ist insbesondere für Administratoren und Benutzer, die mehrere Projekte verwalten, nützlich und bietet einen schnellen Überblick über die im ***digna*** Repository verfügbaren Projekte.

## Verwendung des Befehls `list-ds`

Der Befehl `list-ds` in der ***digna*** CLI wird verwendet, um eine Liste aller verfügbaren Datenquellen innerhalb eines angegebenen Projekts anzuzeigen. Dieser Befehl ist nützlich, um die für Analyse und Verwaltung verfügbaren Datenbestände im ***digna*** System zu verstehen.

#### Befehlsverwendung
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, für das die Datenquellen aufgelistet werden sollen (erforderlich).
  
#### Beispiel
  
Um alle Datenquellen im Projekt mit dem Namen `ProjectA` aufzulisten:
  
```bash
dignacli list-ds ProjectA
```
  
Dieser Befehl gibt den Benutzern einen Überblick über die im Projekt verfügbaren Datenquellen und unterstützt sie dabei, die Datenlandschaft effektiver zu navigieren und zu verwalten.


## Verwendung des Befehls `inspect`

Der Befehl `inspect` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Ampelsystems (Traffic Light System) für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erstellen. Dieser Befehl hilft bei der Analyse und Überwachung von Daten über einen definierten Zeitraum.

#### Befehlsverwendung

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das Daten inspiziert werden sollen (erforderlich). Die Verwendung des Schlüsselworts all-projects in diesem Argument weist ***digna*** an, über alle bestehenden Projekte zu iterieren und diesen Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startuhrzeit für die Dateninspektion. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Enduhrzeit für die Dateninspektion, entsprechend denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filter, um nur Tabellen zu inspizieren, die die angegebene Teilzeichenfolge im Namen enthalten.
- `--do-profile`: Löst die Neuerfassung von Profilen aus. Standard ist do-profile.
- `--no-do-profile`: Verhindert die Neuerfassung von Profilen.
- `--do-prediction`: Löst die Neuberechnung von Vorhersagen aus. Standard ist do-prediction.
- `--no-do-prediction`: Verhindert die Neuberechnung von Vorhersagen.
- `--do-alert-status`: Löst die Neuberechnung der Alarmstatus aus. Standard ist do-alert-status.
- `--no-do-alert-status`: Verhindert die Neuberechnung der Alarmstatus.
- `--iterative`: Löst die Inspektion eines Zeitraums in täglichen Iterationen aus. Standard ist iterative.
- `--no-iterative`: Löst die Inspektion des gesamten Zeitraums in einem Durchlauf aus.
- `--enable_notification`, `-en`: Aktiviert das Versenden von Benachrichtigungen im Falle von Alarmen.
- `--timing`, `-tm`: Zeigt die Dauer des Inspektionsprozesses nach Abschluss an.
  
#### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 zu inspizieren:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Um nur eine bestimmte Tabelle zu inspizieren und die Neuberechnung der Vorhersagen zu erzwingen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dieser Befehl ist nützlich, um aktualisierte Profile und Vorhersagen zu erzeugen, die Datenintegrität zu überwachen und Alarmmechanismen innerhalb eines definierten Projektzeitraums zu verwalten.

## Verwendung des Befehls `tls-status`

Der Befehl `tls-status` in der ***digna*** CLI wird verwendet, um den Status des Ampelsystems (Traffic Light System, TLS) für eine bestimmte Tabelle innerhalb eines Projekts an einem angegebenen Datum abzufragen. Das Ampelsystem liefert Einblicke in die Gesundheit und Qualität der Daten und weist auf mögliche Probleme oder Alarme hin, die Aufmerksamkeit erfordern.
  
#### Befehlsverwendung
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das der TLS-Status abgefragt wird (erforderlich).
- **TABLE_NAME**: Die spezifische Tabelle innerhalb des Projekts, für die der TLS-Status benötigt wird (erforderlich).
- **DATE**: Das Datum, für das der TLS-Status abgefragt wird, typischerweise im Format %Y-%m-%d (erforderlich).
  
#### Beispiel
  
Um den TLS-Status für eine Tabelle namens UserData im Projekt ProjectA am 1. Juli 2024 zu prüfen:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Dieser Befehl hilft Benutzern dabei, die Datenqualität zu überwachen und zu pflegen, indem er einen klaren und umsetzbaren Statusbericht auf Basis vordefinierter Kriterien liefert.

## Verwendung des Befehls `inspect-async`

Der Befehl `inspect-async` in der ***digna*** CLI wird verwendet, um das Backend anzuweisen, die Inspektion für eine oder mehrere Datenquellen eines Projekts asynchron durchzuführen. Wenn project_name auf all-projects gesetzt ist, iteriert die Inspektion über alle verfügbaren Projekte und führt die Inspektion durch. Er liefert eine Request-ID zurück, mit der der Fortschritt der Inspektion verfolgt werden kann.

#### Befehlsverwendung

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das Daten inspiziert werden sollen (erforderlich). Die Verwendung des Schlüsselworts all-projects in diesem Argument weist ***digna*** an, über alle bestehenden Projekte zu iterieren und diesen Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startuhrzeit für die Dateninspektion. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Enduhrzeit für die Dateninspektion, entsprechend denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filter, um nur Tabellen zu inspizieren, die die angegebene Teilzeichenfolge im Namen enthalten.

  
#### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 asynchron zu inspizieren:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Verwendung des Befehls `inspect-status`

Der Befehl `inspect-status` in der ***digna*** CLI wird verwendet, um den Fortschritt einer asynchronen Inspektion anhand der Request-ID zu prüfen.

#### Befehlsverwendung

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumente
  
- **REQUEST_ID**: Die vom Befehl `inspect-async` zurückgegebene Request-ID 
  
#### Optionen

- `--report_level`, `-rl`: Setzt das Berichtslevel: 'task' oder 'step' [Standard: task]
  
#### Beispiel
  
Um den Fortschritt einer Inspektion mit der Request-ID 12345 auf detaillierter Schritt-Ebene zu prüfen:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Verwendung des Befehls `export-ds`

Der Befehl `export-ds` in der ***digna*** CLI wird verwendet, um einen Export von Datenquellen aus dem ***digna*** Repository zu erstellen. Standardmäßig werden alle Datenquellen eines angegebenen Projekts exportiert.

#### Befehlsverwendung
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, aus dem die Datenquellen exportiert werden sollen.

#### Optionen

- `--table_name`, `-tn`: Exportiert eine bestimmte Datenquelle aus einem Projekt.
- `--exportfile`, `-ef`: Legt den Dateinamen für den Export fest.
    
#### Beispiel
  
Um alle Datenquellen aus dem Projekt mit dem Namen `ProjectA` zu exportieren:
  
```bash
dignacli export-ds ProjectA
```
  
Dieser Befehl exportiert alle Datenquellen aus `ProjectA` als JSON-Dokument, das in ein anderes Projekt oder ein anderes ***digna*** Repository importiert werden kann.


## Verwendung des Befehls `import-ds`

Der Befehl `import-ds` in der ***digna*** CLI wird verwendet, um Datenquellen in ein Zielprojekt zu importieren und einen Importbericht zu erstellen.

#### Befehlsverwendung
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, in das die Datenquellen importiert werden sollen.
- **EXPORT_FILE**: Der Dateiname des zu importierenden Datenquellen-Exports.

#### Optionen

- `--output-file`, `-o`: Datei, in der der Importbericht gespeichert wird (falls nicht angegeben, wird der Bericht tabellarisch im Terminal ausgegeben).
- `--output-format`, `-f`: Format, in dem der Importbericht gespeichert werden soll (json, csv).
    
#### Beispiel
  
Um alle Datenquellen aus der Exportdatei `my_export.json` in `ProjectB` zu importieren:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Nach dem Import zeigt dieser Befehl auch einen Bericht über importierte und übersprungene Objekte an. Nur neue Datenquellen werden in `ProjectB` importiert. Um herauszufinden, welche Objekte importiert und welche übersprungen würden, können Sie den Befehl `plan-import-ds` verwenden.

## Verwendung des Befehls `plan-import-ds`

Der Befehl `plan-import-ds` in der ***digna*** CLI wird verwendet, um das Importieren von Datenquellen in ein Zielprojekt zu planen und einen Importbericht zu erstellen.

#### Befehlsverwendung
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, in das die Datenquellen importiert werden würden.
- **EXPORT_FILE**: Der Dateiname des zu analysierenden Datenquellen-Exports vor dem Import.

#### Optionen

- `--output-file`, `-o`: Datei, in der der Importbericht gespeichert wird (falls nicht angegeben, wird der Bericht tabellarisch im Terminal ausgegeben).
- `--output-format`, `-f`: Format, in dem der Importbericht gespeichert werden soll (json, csv).
    
#### Beispiel
  
Um zu prüfen, welche Datenquellen aus der Exportdatei `my_export.json` beim Import in `ProjectB` importiert bzw. übersprungen würden:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Dieser Befehl zeigt nur einen Importplan der zu importierenden und zu überspringenden Objekte an.
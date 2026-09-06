# digna CLI-Referenz 2025.04
**2025-04-01**

Auf dieser Seite sind alle Befehle der ***digna*** CLI-Version **2025.04** dokumentiert, einschließlich Anwendungsbeispielen und Optionen.

---

## CLI-Grundlagen

---

## Verwendung der `--help`-Option

Die `--help`-Option liefert Informationen über verfügbare Befehle und deren Verwendung. Es gibt zwei Hauptarten, diese Option zu nutzen:

1. **Allgemeine Hilfe anzeigen:**
   
   Verwenden Sie `--help` unmittelbar nach dem Wort `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Hilfe für einen spezifischen Befehl abrufen:**  
  
   Für detaillierte Informationen zu einem bestimmten Befehl hängen Sie `--help` an diesen Befehl an.
   Zum Beispiel, um Hilfe zum Befehl `add-user` zu erhalten, führen Sie aus:
   ```bash
   dignacli add-user --help
   ```

   ### Ausgabe:
      
   - **Befehlsbeschreibung:** Bietet eine detaillierte Beschreibung der Funktion des Befehls.  
   - **Syntax:** Zeigt die genaue Syntax, inklusive erforderlicher und optionaler Argumente.  
   - **Optionen:** Listet alle spezifischen Optionen des Befehls und deren Erklärungen auf.  
   - **Beispiele:** Gibt Beispiele, wie der Befehl effektiv ausgeführt wird.

  
## Verwendung des `check-repo-connection`-Befehls

Der Befehl `check-repo-connection` ist ein Dienstprogramm innerhalb der ***digna*** CLI, mit dem die Konnektivität und der Zugriff auf ein angegebenes ***digna*** Repository getestet werden. Dieser Befehl stellt sicher, dass die CLI mit dem Repository kommunizieren kann.
      
#### Befehlsverwendung
```bash
dignacli check-repo-connection
```

Bei erfolgreicher Ausführung gibt der Befehl eine Bestätigung der Verbindung sowie Details zum Repository aus: Repository-Version, Host, Datenbank und Schema.  
  
Wenn die Repository-Verbindung nicht erfolgreich ist, prüfen Sie die Datei config.toml auf korrekte Konfigurationseinstellungen.

## Verwendung des `--version`-Befehls

Um die installierte Version von *dignacli* zu prüfen, verwenden Sie die Option `--version`.  
  
#### Befehlsverwendung
```bash
dignacli --version
```
  
#### Beispielausgabe
```bash
dignacli version 2025.04
```

## Verwendung der Logging-Optionen
  
Standardmäßig ist die Konsolenausgabe der ***digna***-Befehle minimal gehalten. Die meisten Befehle bieten jedoch die Möglichkeit, zusätzliche Informationen bereitzustellen. Die folgenden Optionen stehen dafür zur Verfügung:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ und „debug“ legen das Detaillierungsniveau fest, während die Option „logfile“ die Ausgabe in eine Datei umleitet, anstatt sie im Konsolenfenster anzuzeigen.

## Benutzerverwaltung

### Verwendung des `add-user`-Befehls
  
Der Befehl `add-user` in der ***digna*** CLI wird verwendet, um einen neuen Benutzer im ***digna***-System anzulegen.
  
#### Befehlsverwendung
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumente

- **USER_NAME**: Der Benutzername für den neuen Benutzer (erforderlich).
- **USER_FULL_NAME**: Der vollständige Name des neuen Benutzers (erforderlich).
- **USER_PASSWORD**: Das Passwort für den neuen Benutzer (erforderlich).

#### Optionen

- `--is_superuser`, `-su`: Kennzeichnet den neuen Benutzer als Administrator.
- `--valid_until`, `-vu`: Setzt ein Ablaufdatum für das Benutzerkonto im Format `YYYY-MM-DD HH:MI:SS`. Wenn nicht gesetzt, hat das Konto kein Ablaufdatum.

#### Beispiel

Um einen neuen Benutzer mit dem Benutzernamen `jdoe`, vollständigem Namen `John Doe` und Passwort `password123` hinzuzufügen:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Um einen neuen Benutzer hinzuzufügen und ein Ablaufdatum für das Konto zu setzen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Verwendung des `delete-user`-Befehls
  
Der Befehl `delete-user` in der ***digna*** CLI wird verwendet, um einen bestehenden Benutzer aus dem ***digna***-System zu entfernen.
  
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
  
Durch Ausführen dieses Befehls wird der Benutzer `jdoe` aus dem ***digna***-System entfernt; damit werden sein Zugriff sowie die zugehörigen Daten und Berechtigungen im Repository widerrufen bzw. gelöscht.

### Verwendung des `modify-user`-Befehls

Der Befehl `modify-user` in der ***digna*** CLI wird verwendet, um die Daten eines bestehenden Benutzers im ***digna***-System zu aktualisieren.

#### Befehlsverwendung
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumente
  
- **USER_NAME**: Der Benutzername des zu ändernden Benutzers (erforderlich).
- **USER_FULL_NAME**: Der neue vollständige Name des Benutzers (erforderlich).
  
#### Optionen  
  
- `--is_superuser`, `-su`: Setzt den Benutzer als Superuser und gewährt erweiterte Rechte. Dieser Schalter benötigt keinen Wert.  
- `--valid_until`, `-vu`: Setzt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS. Wenn nicht angegeben, bleibt das Konto unbegrenzt gültig.  
  
#### Beispiel
  
Um den vollständigen Namen des Benutzers `jdoe` in „Johnathan Doe“ zu ändern und den Benutzer als Superuser zu setzen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Verwendung des `modify-user-pwd`-Befehls
  
Der Befehl `modify-user-pwd` in der ***digna*** CLI wird verwendet, um das Passwort eines bestehenden Benutzers im ***digna***-System zu ändern.
  
#### Befehlsverwendung
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumente
  
- **USER_NAME**: Der Benutzername des Benutzers, dessen Passwort geändert werden soll (erforderlich).
- **USER_PWD**: Das neue Passwort für den Benutzer (erforderlich).
  
#### Beispiel
  
Um das Passwort des Benutzers `jdoe` auf `newpassword123` zu ändern:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Verwendung des `list-users`-Befehls

Der Befehl `list-users` in der ***digna*** CLI zeigt eine Liste aller im ***digna***-System registrierten Benutzer an.

#### Befehlsverwendung

```bash
dignacli list-users
```

Bei Ausführung verbindet sich dieser Befehl mit dem ***digna***-Repository und listet alle Benutzer auf, einschließlich ihrer ID, des Benutzernamens, des vollständigen Namens, des Superuser-Status und der Ablaufzeitpunkte.

## Repository-Verwaltung

### Verwendung des `upgrade-repo`-Befehls
  
Der Befehl `upgrade-repo` in der ***digna*** CLI wird verwendet, um das ***digna***-Repository zu aktualisieren oder zu initialisieren. Dieser Befehl ist erforderlich, um Updates anzuwenden oder die Repository-Infrastruktur erstmals einzurichten.
  
#### Befehlsverwendung

```bash
dignacli upgrade-repo [options]
```
  
#### Optionen
  
- `--simulation-mode`, `-s`: Führt den Befehl im Simulationsmodus aus. Dabei werden die SQL-Anweisungen angezeigt, die ausgeführt würden, aber nicht tatsächlich ausgeführt. Nützlich, um Änderungen vorzuschauen, ohne das Repository zu verändern.  

  
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

### Verwendung des `encrypt`-Befehls
  
Der Befehl `encrypt` in der ***digna*** CLI wird verwendet, um ein Passwort zu verschlüsseln.
  
#### Befehlsverwendung
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumente
- **PASSWORD**: Das zu verschlüsselnde Passwort (erforderlich).
  
#### Beispiel
  
Um ein Passwort zu verschlüsseln, geben Sie das Passwort als Argument an.   
Beispielsweise, um das Passwort `mypassword123` zu verschlüsseln, verwenden Sie:
```bash
dignacli encrypt mypassword123
```
Dieser Befehl gibt die verschlüsselte Version des angegebenen Passworts aus, die dann in sicheren Kontexten verwendet werden kann. Wird das Passwort-Argument nicht angegeben, meldet die CLI einen Fehler wegen des fehlenden Arguments.

## Verwendung des `generate-key`-Befehls
  
Der Befehl `generate-key` erzeugt einen Fernet-Schlüssel, der zur Sicherung von Passwörtern im ***digna***-Repository benötigt wird.
  
#### Befehlsverwendung
```bash
dignacli generate-key
```
  
## Datenverwaltung

## Verwendung des `clean-up`-Befehls

Der Befehl `clean-up` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Ampelsystems für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu löschen. Dieser Befehl ist wichtig für das Daten-Lifecycle-Management und hilft, eine organisierte und effiziente Datenumgebung zu erhalten, indem veraltete oder unnötige Daten bereinigt werden.

#### Befehlsverwendung

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, aus dem Daten gelöscht werden sollen (erforderlich). Die Verwendung des Schlüsselworts all-projects in diesem Argument weist ***digna*** an, über alle vorhandenen Projekte zu iterieren und den Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Datenlöschung. Zulässige Formate umfassen %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Datenlöschung, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen
  
- `--table-name`, `-tn`: Beschränkt die Clean-up-Operation auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und begrenzt die Bereinigung auf Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--timing`, `-tm`: Zeigt nach Abschluss die Dauer des Clean-up-Prozesses an.
- `--help`: Zeigt Hilfsinformationen zum Clean-up-Befehl an und beendet die Ausführung.
  
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

## Verwendung des `list-projects`-Befehls
  
Der Befehl `list-projects` in der ***digna*** CLI zeigt eine Liste aller verfügbaren Projekte im ***digna***-System an.
  
#### Befehlsverwendung
  
```bash
dignacli list-projects
```

Dieser Befehl ist besonders nützlich für Administratoren und Benutzer, die mehrere Projekte verwalten, da er einen schnellen Überblick über die im ***digna***-Repository verfügbaren Projekte bietet.

## Verwendung des `list-ds`-Befehls

Der Befehl `list-ds` in der ***digna*** CLI zeigt eine Liste aller verfügbaren Datenquellen innerhalb eines angegebenen Projekts an. Dieser Befehl ist nützlich, um die für Analyse und Verwaltung verfügbaren Datenbestände im ***digna***-System zu überblicken.

#### Befehlsverwendung
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, für das die Datenquellen aufgelistet werden sollen (erforderlich).
  
#### Beispiel
  
Um alle Datenquellen im Projekt `ProjectA` aufzulisten:
  
```bash
dignacli list-ds ProjectA
```
  
Dieser Befehl gibt Nutzern einen Überblick über die im Projekt verfügbaren Datenquellen und unterstützt sie dabei, die Datenlandschaft besser zu navigieren und zu verwalten.


## Verwendung des `inspect`-Befehls

Der Befehl `inspect` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Ampelsystems für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erstellen. Dieser Befehl hilft bei der Analyse und Überwachung von Daten über einen definierten Zeitraum.

#### Befehlsverwendung

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das Daten inspiziert werden sollen (erforderlich). Die Verwendung des Schlüsselworts all-projects in diesem Argument weist ***digna*** an, über alle vorhandenen Projekte zu iterieren und den Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Dateninspektion. Zulässige Formate umfassen %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Dateninspektion, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und inspiziert nur Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--do-profile`: Löst die Neuerfassung von Profilen aus. Standard ist do-profile.
- `--no-do-profile`: Verhindert die Neuerfassung von Profilen.
- `--do-prediction`: Löst die Neuberechnung von Vorhersagen aus. Standard ist do-prediction.
- `--no-do-prediction`: Verhindert die Neuberechnung von Vorhersagen.
- `--do-alert-status`: Löst die Neuberechnung von Alarmstatus aus. Standard ist do-alert-status.
- `--no-do-alert-status`: Verhindert die Neuberechnung von Alarmstatus.
- `--iterative`: Löst die Inspektion eines Zeitraums in täglichen Iterationen aus. Standard ist iterative.
- `--no-iterative`: Löst die Inspektion des gesamten Zeitraums in einem Durchlauf aus.
- `--enable_notification`, `-en`: Ermöglicht das Versenden von Benachrichtigungen im Falle von Alerts.
- `--timing`, `-tm`: Zeigt nach Abschluss die Dauer des Inspektionsprozesses an.
  
#### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 zu inspizieren:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Um nur eine bestimmte Tabelle zu inspizieren und die Neuberechnung der Vorhersagen zu erzwingen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dieser Befehl ist nützlich, um aktualisierte Profile und Vorhersagen zu erzeugen, die Datenintegrität zu überwachen und Alarmsysteme innerhalb eines definierten Projektzeitraums zu verwalten.

## Verwendung des `tls-status`-Befehls

Der Befehl `tls-status` in der ***digna*** CLI wird verwendet, um den Status des Ampelsystems (TLS) für eine bestimmte Tabelle innerhalb eines Projekts an einem bestimmten Datum abzufragen. Das Ampelsystem liefert Einblicke in die Gesundheit und Qualität der Daten und zeigt eventuelle Probleme oder Alarme an, die Aufmerksamkeit erfordern.
  
#### Befehlsverwendung
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das der TLS-Status abgefragt wird (erforderlich).
- **TABLE_NAME**: Die konkrete Tabelle innerhalb des Projekts, für die der TLS-Status benötigt wird (erforderlich).
- **DATE**: Das Datum, für das der TLS-Status abgefragt wird, typischerweise im Format %Y-%m-%d (erforderlich).
  
#### Beispiel
  
Um den TLS-Status für eine Tabelle namens UserData im Projekt ProjectA am 1. Juli 2024 zu prüfen:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Dieser Befehl hilft Nutzern, die Datenqualität zu überwachen und zu erhalten, indem er einen klaren und umsetzbaren Statusbericht basierend auf vordefinierten Kriterien liefert.

## Verwendung des `inspect-async`-Befehls

Der Befehl `inspect-async` in der ***digna*** CLI weist das Backend an, die Inspektion für eine oder mehrere Datenquellen eines Projekts asynchron auszuführen. Wenn PROJECT_NAME auf all-projects gesetzt ist, wird die Inspektion über alle verfügbaren Projekte iteriert und ausgeführt. Der Befehl gibt eine Request-ID zurück, mit der der Fortschritt der Inspektion nachverfolgt werden kann.

#### Befehlsverwendung

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das Daten inspiziert werden sollen (erforderlich). Die Verwendung des Schlüsselworts all-projects in diesem Argument weist ***digna*** an, über alle vorhandenen Projekte zu iterieren und den Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Dateninspektion. Zulässige Formate umfassen %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Dateninspektion, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und inspiziert nur Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.

  
#### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 asynchron inspizieren zu lassen:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Verwendung des `inspect-status`-Befehls

Der Befehl `inspect-status` in der ***digna*** CLI wird verwendet, um den Fortschritt einer asynchronen Inspektion anhand der Request-ID zu überprüfen.

#### Befehlsverwendung

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumente
  
- **REQUEST_ID**: Die vom Befehl `inspect-async` zurückgegebene Request-ID 
  
#### Optionen

- `--report_level`, `-rl`: Setzt das Berichtsniveau: 'task' oder 'step' [Standard: task]
  
#### Beispiel
  
Um den Fortschritt einer Inspektion mit der Request-ID 12345 auf detaillierter Schrittebene zu prüfen:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Verwendung des `export-ds`-Befehls

Der Befehl `export-ds` in der ***digna*** CLI wird verwendet, um einen Export von Datenquellen aus dem ***digna***-Repository zu erstellen. Standardmäßig werden alle Datenquellen eines Projekts exportiert.

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
  
Um alle Datenquellen des Projekts `ProjectA` zu exportieren:
  
```bash
dignacli export-ds ProjectA
```
  
Dieser Befehl exportiert alle Datenquellen aus `ProjectA` als JSON-Dokument, das in ein anderes Projekt oder Repository von ***digna*** importiert werden kann.


## Verwendung des `import-ds`-Befehls

Der Befehl `import-ds` in der ***digna*** CLI wird verwendet, um Datenquellen in ein Zielprojekt zu importieren und einen Importbericht zu erstellen.

#### Befehlsverwendung
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, in das die Datenquellen importiert werden sollen.
- **EXPORT_FILE**: Der Dateiname der zu importierenden Datenquellen-Exportdatei.

#### Optionen

- `--output-file`, `-o`: Datei, in der der Importbericht gespeichert wird (wenn nicht angegeben, wird der Bericht tabellarisch im Terminal ausgegeben).
- `--output-format`, `-f`: Format zur Speicherung des Importberichts (json, csv).
    
#### Beispiel
  
Um alle Datenquellen aus der Exportdatei `my_export.json` in `ProjectB` zu importieren:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Nach dem Import zeigt dieser Befehl zudem einen Bericht über importierte und übersprungene Objekte an. Es werden nur neue Datenquellen in `ProjectB` importiert. Um herauszufinden, welche Objekte importiert und welche übersprungen würden, können Sie den Befehl `plan-import-ds` verwenden.

## Verwendung des `plan-import-ds`-Befehls

Der Befehl `plan-import-ds` in der ***digna*** CLI wird verwendet, um einen Importplan für Datenquellen in ein Zielprojekt zu erstellen und einen Bericht zu generieren, ohne tatsächlich zu importieren.

#### Befehlsverwendung
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, in das die Datenquellen importiert werden würden.
- **EXPORT_FILE**: Der Dateiname der zu analysierenden Exportdatei vor dem Import.

#### Optionen

- `--output-file`, `-o`: Datei, in der der Importbericht gespeichert wird (wenn nicht angegeben, wird der Bericht tabellarisch im Terminal ausgegeben).
- `--output-format`, `-f`: Format zur Speicherung des Importberichts (json, csv).
    
#### Beispiel
  
Um zu prüfen, welche Datenquellen aus der Exportdatei `my_export.json` beim Import in `ProjectB` importiert bzw. übersprungen würden:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Dieser Befehl zeigt lediglich einen Importplan der Objekte, die importiert bzw. übersprungen werden würden.
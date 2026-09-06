# digna CLI Referenz 2026.01
**2026-01-15**

Diese Seite dokumentiert die vollständige Menge an Befehlen, die in der ***digna*** CLI Version **2026.01** verfügbar sind, einschließlich Anwendungsbeispielen und Optionen.

---

## CLI-Grundlagen

---

### help
Die Option `--help` liefert Informationen über verfügbare Befehle und deren Verwendung. Es gibt zwei Hauptmöglichkeiten, diese Option zu nutzen:

1. **Allgemeine Hilfe anzeigen:**
   
   Verwenden Sie --help unmittelbar nach dem Schlüsselwort ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Hilfe für spezifische Befehle anfordern:**  
  
   Für detaillierte Informationen zu einem bestimmten Befehl hängen Sie `--help` an diesen Befehl an.
   Zum Beispiel, um Hilfe zum Befehl `add-user` zu erhalten, führen Sie aus:
   ```bash
   dignacli add-user --help
   ```

   ### Ausgabe:
      
   - **Befehlsbeschreibung:** Liefert eine ausführliche Beschreibung dessen, was der Befehl tut.  
   - **Syntax:** Zeigt die genaue Syntax, einschließlich erforderlicher und optionaler Argumente.  
   - **Optionen:** Listet alle spezifischen Optionen des Befehls mit Erklärungen auf.  
   - **Beispiele:** Bietet Beispiele, wie der Befehl effektiv ausgeführt wird.

### check-config

Der Befehl check-config ist ein Hilfswerkzeug innerhalb der ***digna*** CLI, das dazu dient, die Konfiguration von ***digna*** zu testen. Dieser Befehl stellt sicher, dass die ***digna***-Komponenten die benötigten Konfigurationsbestandteile in der config.toml finden können.

#### Optionen

- `--configpath`, `-cp`: Datei oder Verzeichnis, das die Konfiguration enthält. Wird dies weggelassen, wird ../config.toml verwendet.
      
#### Befehlsverwendung
```bash
dignacli check-config
```

Nach erfolgreicher Ausführung gibt der Befehl eine Bestätigung über die Vollständigkeit der Konfiguration aus.  
  
Wenn die Konfiguration unvollständig erscheint, werden die fehlenden Konfigurationselemente aufgelistet.

  
### check-repo-connection

Der Befehl check-repo-connection ist ein Hilfswerkzeug innerhalb der ***digna*** CLI, das entwickelt wurde, um die Konnektivität und den Zugriff auf ein angegebenes ***digna*** Repository zu testen. Dieser Befehl stellt sicher, dass die CLI mit dem Repository interagieren kann.
      
#### Befehlsverwendung
```bash
dignacli check-repo-connection
```

Nach erfolgreicher Ausführung gibt der Befehl eine Bestätigung der Verbindung aus, zusammen mit Details zum Repository: Repository-Version, Host, Datenbank und Schema.  
  
Wenn die Verbindung zum Repository nicht erfolgreich ist, überprüfen Sie die config.toml-Datei auf korrekte Konfigurationseinstellungen.


### version

Um die installierte Version von *dignacli* zu prüfen, verwenden Sie die Option --version.  
  
#### Befehlsverwendung
```bash
dignacli --version
```
  
#### Beispielausgabe
```bash
dignacli version 2026.01
```

### Protokollierungsoptionen
  
Standardmäßig ist die Konsolenausgabe der ***digna*** Befehle minimalistisch gehalten. Die meisten Befehle bieten die Möglichkeit, zusätzliche Informationen bereitzustellen, über die folgenden Optionen:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ und „debug“ legen den Detaillierungsgrad fest, während der Schalter „logfile“ erlaubt, die Ausgabe in eine Datei umzuleiten, anstatt sie im Konsolenfenster anzuzeigen.

## Benutzerverwaltung

### add-user
  
Der Befehl add-user in der ***digna*** CLI wird verwendet, um einen neuen Benutzer zum ***digna*** System hinzuzufügen.
  
#### Befehlsverwendung
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumente

- **USER_NAME**: Der Benutzername für den neuen Benutzer (erforderlich).
- **USER_FULL_NAME**: Der vollständige Name des neuen Benutzers (erforderlich).
- **USER_PASSWORD**: Das Passwort für den neuen Benutzer (erforderlich).

#### Optionen

- `--is_superuser`, `-su`: Flag, um den neuen Benutzer als Administrator (Superuser) zu kennzeichnen.
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

### delete-user
  
Der `delete-user` Befehl in der ***digna*** CLI wird verwendet, um einen bestehenden Benutzer aus dem ***digna*** System zu entfernen.
  
#### Befehlsverwendung
```bash
dignacli delete-user USER_NAME
```
  
#### Argumente
- **USER_NAME**: Der Benutzername des zu löschenden Benutzers (erforderlich). Dies ist das einzige vom Befehl erforderliche Argument.

#### Beispiel
```bash
dignacli delete-user jdoe
```
  
Durch Ausführen dieses Befehls wird der Benutzer `jdoe` aus dem ***digna*** System entfernt, sein Zugriff wird entzogen und die zugehörigen Daten und Berechtigungen im Repository werden gelöscht.

### modify-user

Der `modify-user` Befehl in der ***digna*** CLI wird verwendet, um die Details eines bestehenden Benutzers im ***digna*** System zu aktualisieren.

#### Befehlsverwendung
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumente
  
- **USER_NAME**: Der Benutzername des zu ändernden Benutzers (erforderlich).
- **USER_FULL_NAME**: Der neue vollständige Name des Benutzers (erforderlich).
  
#### Optionen  
  
- `--is_superuser`, `-su`: Setzt den Benutzer als Superuser und gewährt erhöhte Berechtigungen. Dieses Flag benötigt keinen Wert.  
- `--valid_until`, `-vu`: Setzt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS. Wenn nicht angegeben, bleibt das Konto unbegrenzt gültig.  
  
#### Beispiel
  
Um den vollständigen Namen des Benutzers `jdoe` auf „Johnathan Doe“ zu ändern und den Benutzer als Superuser zu setzen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Der `modify-user-pwd` Befehl in der ***digna*** CLI wird verwendet, um das Passwort eines bestehenden Benutzers im ***digna*** System zu ändern.
  
#### Befehlsverwendung
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumente
  
- **USER_NAME**: Der Benutzername des Benutzers, dessen Passwort geändert werden soll (erforderlich).
- **USER_PWD**: Das neue Passwort für den Benutzer (erforderlich).
  
#### Beispiel
  
Um das Passwort des Benutzers `jdoe` auf `newpassword123` zu ändern:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Der `list-users` Befehl in der ***digna*** CLI zeigt eine Liste aller im ***digna*** System registrierten Benutzer an.

#### Befehlsverwendung

```bash
dignacli list-users
```

Wenn Sie diesen Befehl in der ***digna*** CLI ausführen, verbindet er sich mit dem ***digna*** Repository und listet alle Benutzer auf, einschließlich ihrer ID, ihres Benutzernamens, vollständigen Namens, Superuser-Status und Ablaufzeitstempel.

## Repository-Verwaltung

### upgrade-repo
  
Der `upgrade-repo` Befehl in der ***digna*** CLI wird verwendet, um das ***digna*** Repository zu aktualisieren oder zu initialisieren. Dieser Befehl ist entscheidend, um Updates anzuwenden oder die Repository-Infrastruktur erstmals einzurichten.
  
#### Befehlsverwendung

```bash
dignacli upgrade-repo [options]
```
  
#### Optionen
  
- `--simulation-mode`, `-s`: Wenn aktiviert, läuft dieser Befehl im Simulationsmodus und gibt die SQL-Anweisungen aus, die ausgeführt würden, führt diese jedoch nicht tatsächlich aus. Dies ist nützlich, um Änderungen vorab zu überprüfen, ohne das Repository zu verändern.  

  
#### Beispiel
  
Um das ***digna*** Repository zu aktualisieren, können Sie den Befehl ohne Optionen ausführen:
  
```bash
dignacli upgrade-repo
```  
Um das Upgrade im Simulationsmodus auszuführen (um die SQL-Anweisungen zu sehen, ohne sie anzuwenden):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dieser Befehl ist wichtig für die Wartung des ***digna*** Systems und stellt sicher, dass das Datenbankschema und andere Repository-Komponenten mit der neuesten Softwareversion auf dem aktuellen Stand sind.

### encrypt
  
Der `encrypt` Befehl in der ***digna*** CLI wird verwendet, um ein Passwort zu verschlüsseln.
  
#### Befehlsverwendung
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumente
- **PASSWORD**: Das zu verschlüsselnde Passwort (erforderlich).
  
#### Beispiel
  
Um ein Passwort zu verschlüsseln, müssen Sie das Passwort als Argument übergeben.   
Zum Beispiel, um das Passwort `mypassword123` zu verschlüsseln, verwenden Sie:
```bash
dignacli encrypt mypassword123
```
Dieser Befehl gibt die verschlüsselte Version des übergebenen Passworts aus, die anschließend in sicheren Kontexten verwendet werden kann. Wenn das Passwort-Argument nicht angegeben ist, zeigt die CLI einen Fehler wegen des fehlenden Arguments an.

### generate-key
  
Der `generate-key` Befehl wird verwendet, um einen Fernet-Schlüssel zu erzeugen, der für die Sicherung von Passwörtern im ***digna*** Repository erforderlich ist.
  
#### Befehlsverwendung
```bash
dignacli generate-key
```
  
## Datenverwaltung

### clean-up

Der `clean-up` Befehl in der ***digna*** CLI wird verwendet, um Profile, Prognosen und Ampelsystem-Daten für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu entfernen. Dieser Befehl ist wichtig für das Daten-Lifecycle-Management und hilft, eine organisierte und effiziente Datenumgebung zu erhalten, indem veraltete oder unnötige Daten gelöscht werden.

#### Befehlsverwendung

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, aus dem Daten entfernt werden sollen (erforderlich). Wenn hier das Schlüsselwort all-projects verwendet wird, weist das ***digna*** an, über alle vorhandenen Projekte zu iterieren und den Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Datenlöschung. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Datenlöschung, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen
  
- `--table-name`, `-tn`: Beschränkt den clean-up-Vorgang auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und beschränkt die Bereinigung auf Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--timing`, `-tm`: Zeigt die Dauer des Bereinigungsvorgangs nach Abschluss an.
- `--help`: Zeigt Hilfeinformationen für den clean-up Befehl an und beendet das Programm.
  
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

### remove-orphans
  
Der `remove-orphans` Befehl in der ***digna*** CLI dient der Wartung des ***digna*** Repositories.  
Wenn Benutzer Projekte oder Datenquellen löschen, bleiben Profile und Prognosen oftmals im Repository zurück. Mit diesem Befehl werden solche verwaisten Einträge aus dem Repository entfernt.
  
#### Befehlsverwendung
  
```bash
dignacli list-projects
```

### list-projects
  
Der `list-projects` Befehl in der ***digna*** CLI wird verwendet, um eine Liste aller verfügbaren Projekte im ***digna*** System anzuzeigen.
  
#### Befehlsverwendung
  
```bash
dignacli list-projects
```

Dieser Befehl ist besonders nützlich für Administratoren und Benutzer, die mehrere Projekte verwalten, da er einen schnellen Überblick über die im ***digna*** Repository verfügbaren Projekte bietet.

### list-ds

Der `list-ds` Befehl in der ***digna*** CLI zeigt eine Liste aller verfügbaren Datenquellen innerhalb eines angegebenen Projekts an. Dieser Befehl ist nützlich, um die verfügbaren Datenbestände für Analyse und Verwaltung im ***digna*** System zu überblicken.

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
  
Dieser Befehl bietet Benutzern einen Überblick über die in einem Projekt verfügbaren Datenquellen und hilft ihnen, die Datenlandschaft effektiver zu navigieren und zu verwalten.


### inspect

Der `inspect` Befehl in der ***digna*** CLI wird verwendet, um Profile, Prognosen und Ampelsystem-Daten für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erstellen. Dieser Befehl hilft bei der Analyse und Überwachung von Daten über einen definierten Zeitraum. Nach Abschluss der Inspektion wird der Wert des berechneten Ampelsystems zurückgegeben:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Befehlsverwendung

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, das inspiziert werden soll (erforderlich). Wenn hier das Schlüsselwort all-projects verwendet wird, weist das ***digna*** an, über alle vorhandenen Projekte zu iterieren und den Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Dateninspektion. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Dateninspektion, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und inspiziert nur Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--enable_notification`, `-en`: Aktiviert das Versenden von Benachrichtigungen im Falle von Alerts.
- `--bypass-backend`, `-bb`: Backend umgehen und die Inspektion direkt aus der CLI heraus ausführen (nur zu Testzwecken!).

  
#### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 zu inspizieren:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Um nur eine bestimmte Tabelle zu inspizieren und die Vorhersagen neu zu berechnen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dieser Befehl ist nützlich, um aktualisierte Profile und Prognosen zu erzeugen, die Datenintegrität zu überwachen und Alarmmechanismen innerhalb eines definierten Projektzeitraums zu verwalten.

### inspect-async

Der `inspect-async` Befehl in der ***digna*** CLI wird verwendet, um Profile, Prognosen und Ampelsystem-Daten für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erstellen. Dieser Befehl hilft bei der Analyse und Überwachung von Daten über einen definierten Zeitraum. Im Gegensatz zum synchronen `inspect`-Befehl wartet dieser nicht auf die Fertigstellung der Inspektion.
Stattdessen gibt er die Request-ID für die eingereichte Inspektionsanfrage zurück. Um den Fortschritt des Inspektionsprozesses abzufragen, verwenden Sie den Befehl `inspect-status`.

#### Befehlsverwendung

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, das inspiziert werden soll (erforderlich). Wenn hier das Schlüsselwort all-projects verwendet wird, weist das ***digna*** an, über alle vorhandenen Projekte zu iterieren und den Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Dateninspektion. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Dateninspektion, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und inspiziert nur Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--enable_notification`, `-en`: Aktiviert das Versenden von Benachrichtigungen im Falle von Alerts.

  
#### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 asynchron zu inspizieren:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Der `inspect-status` Befehl in der ***digna*** CLI wird verwendet, um den Fortschritt einer asynchronen Inspektion anhand der Request-ID zu prüfen.

#### Befehlsverwendung

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumente
  
- **REQUEST_ID**: Die Request-ID, die vom `inspect-async` Befehl zurückgegeben wurde.
  
#### Beispiel
  
Um den Fortschritt einer Inspektion mit der Request-ID 12345 zu prüfen:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Der `inspect-cancel` Befehl in der ***digna*** CLI wird verwendet, um Inspektionen anhand der Request-ID abzubrechen, oder er kann verwendet werden, um alle laufenden Anfragen zu beenden.

#### Befehlsverwendung

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumente
  
- **REQUEST_ID**: Die Request-ID, die vom `inspect-async` Befehl zurückgegeben wurde.
  
#### Beispiel
  
Um die Inspektion mit der Request-ID 12345 abzubrechen:
  
```bash
dignacli inspect-cancel 12345
```

Um alle aktuell laufenden oder wartenden Anfragen abzubrechen:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Der `export-ds` Befehl in der ***digna*** CLI wird verwendet, um einen Export von Datenquellen aus dem ***digna*** Repository zu erstellen. Standardmäßig werden alle Datenquellen eines angegebenen Projekts exportiert.

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
  
Um alle Datenquellen aus dem Projekt mit dem Namen `ProjectA` zu exportieren:
  
```bash
dignacli export-ds ProjectA
```
  
Dieser Befehl exportiert alle Datenquellen aus `ProjectA` als JSON-Dokument, das in ein anderes Projekt oder ein anderes ***digna*** Repository importiert werden kann.


### import-ds

Der `import-ds` Befehl in der ***digna*** CLI wird verwendet, um Datenquellen in ein Zielprojekt zu importieren und einen Importbericht zu erstellen.

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
  
Nach dem Import zeigt dieser Befehl auch einen Bericht über importierte und übersprungene Objekte an. Es werden nur neue Datenquellen in `ProjectB` importiert. Um herauszufinden, welche Objekte importiert bzw. übersprungen würden, können Sie den Befehl `plan-import-ds` verwenden.

### plan-import-ds

Der `plan-import-ds` Befehl in der ***digna*** CLI wird verwendet, um den Import von Datenquellen in ein Zielprojekt zu planen und einen Importbericht zu erstellen.

#### Befehlsverwendung
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, in das die Datenquellen importiert werden würden.
- **EXPORT_FILE**: Der Dateiname des Datenquellen-Exports, der vor dem Import analysiert werden soll.

#### Optionen

- `--output-file`, `-o`: Datei zum Speichern des Importberichts (falls nicht angegeben, wird der Bericht tabellarisch im Terminal ausgegeben).
- `--output-format`, `-f`: Format zum Speichern des Importberichts (json, csv).
    
#### Beispiel
  
Um zu prüfen, welche Datenquellen aus der Exportdatei `my_export.json` beim Import in `ProjectB` importiert bzw. übersprungen würden:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Dieser Befehl zeigt nur einen Importplan der zu importierenden und zu überspringenden Objekte an.
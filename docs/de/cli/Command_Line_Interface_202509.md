---
title: digna CLI Referenz 2025.09 – Befehle & Beispiele | digna Dokumentation
description: Vollständige Referenz für die digna CLI-Version 2025.09. Lernen Sie, wie Sie Benutzer, Repositories und Daten mit Befehlen wie add-user, check-config, check-repo-connection, inspect, inspect-async und weiteren verwalten.
image: /assets/logo_square.png
---

# digna CLI Referenz 2025.09
**2025-09-29**

Diese Seite dokumentiert die vollständige Menge an Befehlen, die in der ***digna*** CLI-Version **2025.09** verfügbar sind, einschließlich Anwendungsbeispielen und Optionen.

---

## CLI-Grundlagen

---

### help
Die Option `--help` liefert Informationen über verfügbare Befehle und deren Verwendung. Es gibt zwei Hauptmöglichkeiten, diese Option zu verwenden:

1. **Allgemeine Hilfe anzeigen:**
   
    Verwenden Sie --help unmittelbar nach dem Stichwort ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Hilfe für spezifische Befehle erhalten:**  
  
    Für detaillierte Informationen zu einem bestimmten Befehl hängen Sie `--help` an diesen Befehl an.  
    Beispielsweise, um Hilfe für den Befehl `add-user` zu erhalten, führen Sie aus:
     ```bash
     dignacli add-user --help
     ```

     ### Ausgabe:
      
     - **Befehlsbeschreibung:** Bietet eine detaillierte Erklärung, was der Befehl bewirkt.  
     - **Syntax:** Zeigt die genaue Syntax, einschließlich erforderlicher und optionaler Argumente.  
     - **Optionen:** Listet spezifische Optionen des Befehls und deren Erklärungen auf.  
     - **Beispiele:** Liefert Beispiele, wie der Befehl effektiv ausgeführt werden kann.

### check-config

Der Befehl check-config ist ein Dienstprogramm innerhalb des ***digna*** CLI-Tools, das dazu dient, die Konfiguration von ***digna*** zu überprüfen. Dieser Befehl stellt sicher, dass die ***digna***-Komponenten die benötigten Konfigurationselemente in der config.toml finden können.

#### Optionen

- `--configpath`, `-cp`: Datei oder Verzeichnis, das die Konfiguration enthält. Wenn weggelassen, wird ../config.toml verwendet.
      
#### Befehlsverwendung
```bash
dignacli check-config
```

Bei erfolgreicher Ausführung gibt der Befehl eine Bestätigung über die Vollständigkeit der Konfiguration aus.  
  
Wenn die Konfiguration unvollständig erscheint, werden die fehlenden Konfigurationselemente aufgelistet.

  
### check-repo-connection

Der Befehl check-repo-connection ist ein Dienstprogramm innerhalb des ***digna*** CLI-Tools, das die Konnektivität und den Zugriff auf ein angegebenes ***digna*** Repository testet. Dieser Befehl stellt sicher, dass die CLI mit dem Repository interagieren kann.
      
#### Befehlsverwendung
```bash
dignacli check-repo-connection
```

Bei erfolgreicher Ausführung gibt der Befehl eine Bestätigung der Verbindung aus, zusammen mit Details zum Repository: Repository-Version, Host, Datenbank und Schema.  
  
Wenn die Repository-Verbindung nicht erfolgreich ist, prüfen Sie die Datei config.toml auf korrekte Konfigurationseinstellungen.


### version

Um die installierte Version von *dignacli* zu überprüfen, verwenden Sie die Option --version.  
  
#### Befehlsverwendung
```bash
dignacli --version
```
  
#### Beispielausgabe
```bash
dignacli version 2025.09
```

### Logging-Optionen
  
Standardmäßig ist die Konsolenausgabe der ***digna*** Befehle minimalistisch gehalten. Die meisten Befehle bieten die Möglichkeit, zusätzliche Informationen bereitzustellen, mittels der folgenden Optionen:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ und „debug“ legen den Detaillierungsgrad fest, während der „logfile“-Schalter ermöglicht, die Ausgabe in eine Datei umzuleiten, anstatt sie im Konsolenfenster anzuzeigen.

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

- `--is_superuser`, `-su`: Kennzeichnet den neuen Benutzer als Administrator.
- `--valid_until`, `-vu`: Setzt ein Ablaufdatum für das Benutzerkonto im Format `YYYY-MM-DD HH:MI:SS`. Wenn nicht gesetzt, hat das Konto kein Ablaufdatum.

#### Beispiel

Um einen neuen Benutzer mit dem Benutzernamen `jdoe`, dem vollständigen Namen `John Doe` und dem Passwort `password123` hinzuzufügen:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Um einen neuen Benutzer hinzuzufügen und ein Ablaufdatum für das Konto zu setzen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Der Befehl `delete-user` in der ***digna*** CLI wird verwendet, um einen vorhandenen Benutzer aus dem ***digna*** System zu entfernen.
  
#### Befehlsverwendung
```bash
dignacli delete-user USER_NAME
```
  
#### Argumente
- **USER_NAME**: Der Benutzername des zu löschenden Benutzers (erforderlich). Dies ist das einzige erforderliche Argument des Befehls.

#### Beispiel
```bash
dignacli delete-user jdoe
```
  
Durch Ausführen dieses Befehls wird der Benutzer `jdoe` aus dem ***digna*** System entfernt, sein Zugriff wird widerrufen und die zugehörigen Daten und Berechtigungen im Repository werden gelöscht.

### modify-user

Der Befehl `modify-user` in der ***digna*** CLI wird verwendet, um die Details eines vorhandenen Benutzers im ***digna*** System zu aktualisieren.

#### Befehlsverwendung
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumente
  
- **USER_NAME**: Der Benutzername des zu ändernden Benutzers (erforderlich).
- **USER_FULL_NAME**: Der neue vollständige Name für den Benutzer (erforderlich).
  
#### Optionen  
  
- `--is_superuser`, `-su`: Setzt den Benutzer als Superuser und gewährt erhöhte Rechte. Dieser Schalter benötigt keinen Wert.  
- `--valid_until`, `-vu`: Setzt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS. Wenn nicht angegeben, bleibt das Konto unbegrenzt gültig.  
  
#### Beispiel
  
Um den vollständigen Namen des Benutzers `jdoe` zu „Johnathan Doe“ zu ändern und den Benutzer als Superuser zu setzen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Der Befehl `modify-user-pwd` in der ***digna*** CLI wird verwendet, um das Passwort eines vorhandenen Benutzers im ***digna*** System zu ändern.
  
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

Der Befehl `list-users` in der ***digna*** CLI zeigt eine Liste aller im ***digna*** System registrierten Benutzer an.

#### Befehlsverwendung

```bash
dignacli list-users
```

Wenn Sie diesen Befehl in der ***digna*** CLI ausführen, verbindet er sich mit dem ***digna*** Repository und listet alle Benutzer auf, wobei ID, Benutzername, vollständiger Name, Superuser-Status und Ablaufzeitstempel angezeigt werden.

## Repository-Verwaltung

### upgrade-repo
  
Der Befehl `upgrade-repo` in der ***digna*** CLI wird verwendet, um das ***digna*** Repository zu aktualisieren oder zu initialisieren. Dieser Befehl ist essenziell, um Updates anzuwenden oder die Repository-Infrastruktur erstmals einzurichten.
  
#### Befehlsverwendung

```bash
dignacli upgrade-repo [options]
```
  
#### Optionen
  
- `--simulation-mode`, `-s`: Wenn aktiviert, führt dieser Schalter den Befehl im Simulationsmodus aus und zeigt die SQL-Anweisungen an, die ausgeführt würden, ohne sie tatsächlich auszuführen. Dies ist nützlich, um Änderungen vorab zu prüfen, ohne das Repository zu verändern.  

  
#### Beispiel
  
Um das ***digna*** Repository zu aktualisieren, können Sie den Befehl ohne Optionen ausführen:
  
```bash
dignacli upgrade-repo
```  
Um die Aktualisierung im Simulationsmodus auszuführen (um die SQL-Anweisungen zu sehen, ohne sie anzuwenden):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dieser Befehl ist wichtig für die Wartung des ***digna*** Systems und stellt sicher, dass das Datenbankschema und andere Repository-Komponenten mit der neuesten Softwareversion übereinstimmen.

### encrypt
  
Der Befehl `encrypt` in der ***digna*** CLI wird verwendet, um ein Passwort zu verschlüsseln.
  
#### Befehlsverwendung
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumente
- **PASSWORD**: Das zu verschlüsselnde Passwort (erforderlich).
  
#### Beispiel
  
Um ein Passwort zu verschlüsseln, müssen Sie das Passwort als Argument übergeben.   
Beispielsweise, um das Passwort `mypassword123` zu verschlüsseln, verwenden Sie:
```bash
dignacli encrypt mypassword123
```
Dieser Befehl gibt die verschlüsselte Version des übergebenen Passworts aus, die dann in sicheren Kontexten verwendet werden kann. Wenn das Passwort-Argument nicht angegeben wird, zeigt die CLI einen Fehler an, der auf das fehlende Argument hinweist.

### generate-key
  
Der Befehl `generate-key` wird verwendet, um einen Fernet-Schlüssel zu erzeugen, der für die Sicherung von Passwörtern im ***digna*** Repository erforderlich ist.
  
#### Befehlsverwendung
```bash
dignacli generate-key
```
  
## Datenverwaltung

### clean-up

Der Befehl `clean-up` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen (predictions) und Ampelsystemdaten für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu entfernen. Dieser Befehl ist wichtig für das Datenlebenszyklus-Management und hilft, eine organisierte sowie effiziente Datenumgebung zu erhalten, indem veraltete oder unnötige Daten gelöscht werden.

#### Befehlsverwendung

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, aus dem Daten entfernt werden sollen (erforderlich). Wenn das Schlüsselwort all-projects verwendet wird, weist dies ***digna*** an, alle vorhandenen Projekte zu durchlaufen und den Befehl auf jedes anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Datenlöschung. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Datenlöschung, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen
  
- `--table-name`, `-tn`: Beschränkt die Clean-up-Operation auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert die Clean-up-Operation auf Tabellen, deren Namen den angegebenen Teilstring enthalten.
- `--timing`, `-tm`: Zeigt nach Abschluss die benötigte Zeitdauer des Clean-up-Prozesses an.
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
  
Dieser Befehl hilft bei der Verwaltung des Datenvolumens und stellt sicher, dass das Repository nur relevante Informationen enthält.

### remove-orphans
  
Der Befehl `remove-orphans` in der ***digna*** CLI dient der Aufräumarbeit im ***digna*** Repository.  
Wenn ein Benutzer Projekte oder Datenquellen löscht, verbleiben oftmals Profile und Vorhersagen im Repository. Mit diesem Befehl werden solche verwaisten Einträge aus dem Repository entfernt.
  
#### Befehlsverwendung
  
```bash
dignacli list-projects
```

### list-projects
  
Der Befehl `list-projects` in der ***digna*** CLI wird verwendet, um eine Liste aller verfügbaren Projekte im ***digna*** System anzuzeigen.
  
#### Befehlsverwendung
  
```bash
dignacli list-projects
```

Dieser Befehl ist besonders nützlich für Administratoren und Nutzer, die mehrere Projekte verwalten, und bietet einen schnellen Überblick über die im ***digna*** Repository verfügbaren Projekte.

### list-ds

Der Befehl `list-ds` in der ***digna*** CLI zeigt eine Liste aller verfügbaren Datenquellen innerhalb eines angegebenen Projekts an. Dieser Befehl ist hilfreich, um die verfügbaren Datenbestände für Analyse und Verwaltung im ***digna*** System zu verstehen.

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
  
Dieser Befehl gibt den Nutzern einen Überblick über die in einem Projekt verfügbaren Datenquellen und hilft ihnen, die Datenlandschaft effektiver zu navigieren und zu verwalten.


### inspect

Der Befehl `inspect` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen (predictions) und Ampelsystemdaten für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erstellen. Dieser Befehl hilft bei der Analyse und Überwachung von Daten über einen definierten Zeitraum. Nach Abschluss der Inspektion wird der Wert des berechneten Ampelsystems zurückgegeben:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Befehlsverwendung

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, das inspiziert werden soll (erforderlich). Wenn das Schlüsselwort all-projects verwendet wird, weist dies ***digna*** an, alle vorhandenen Projekte zu durchlaufen und den Befehl auf jedes anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit der Dateninspektion. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit der Dateninspektion, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und inspiziert nur Tabellen, deren Namen den angegebenen Teilstring enthalten.
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
Dieser Befehl ist nützlich, um aktualisierte Profile und Vorhersagen zu erstellen, die Datenintegrität zu überwachen und das Alert-System innerhalb eines definierten Projektzeitraums zu verwalten.

### inspect-async

Der Befehl `inspect-async` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen (predictions) und Ampelsystemdaten für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erstellen. Dieser Befehl hilft bei der Analyse und Überwachung von Daten über einen definierten Zeitraum. Im Gegensatz zum synchronen `inspect`-Befehl wartet dieser nicht auf den Abschluss der Inspektion. Stattdessen gibt er die Request-ID für die eingereichte Inspektionsanfrage zurück. Um den Fortschritt der Inspektion abzufragen, verwenden Sie den Befehl `inspect-status`.

#### Befehlsverwendung

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, das inspiziert werden soll (erforderlich). Wenn das Schlüsselwort all-projects verwendet wird, weist dies ***digna*** an, alle vorhandenen Projekte zu durchlaufen und den Befehl auf jedes anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit der Dateninspektion. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit der Dateninspektion, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und inspiziert nur Tabellen, deren Namen den angegebenen Teilstring enthalten.
- `--enable_notification`, `-en`: Aktiviert das Versenden von Benachrichtigungen im Falle von Alerts.

  
#### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 asynchron zu inspizieren:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Der Befehl `inspect-status` in der ***digna*** CLI wird verwendet, um den Fortschritt einer asynchronen Inspektion anhand der Request-ID zu prüfen.

#### Befehlsverwendung

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumente
  
- **REQUEST_ID**: Die Request-ID, die vom Befehl `inspect-async` zurückgegeben wurde 
  
#### Beispiel
  
Um den Fortschritt einer Inspektion mit der Request-ID 12345 zu prüfen:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Der Befehl `inspect-cancel` in der ***digna*** CLI dient dazu, Inspektionen anhand der Request-ID abzubrechen, oder er kann verwendet werden, um alle aktuellen Anfragen abzubrechen.

#### Befehlsverwendung

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumente
  
- **REQUEST_ID**: Die Request-ID, die vom Befehl `inspect-async` zurückgegeben wurde 
  
#### Beispiel
  
Um die Inspektion mit der Request-ID 12345 abzubrechen:
  
```bash
dignacli inspect-cancel 12345
```

Um alle Anfragen abzubrechen, die derzeit laufen oder ausstehen:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Der Befehl `export-ds` in der ***digna*** CLI wird verwendet, um einen Export von Datenquellen aus dem ***digna*** Repository zu erstellen. Standardmäßig werden alle Datenquellen eines Projekts exportiert.

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
  
Dieser Befehl exportiert alle Datenquellen aus `ProjectA` als JSON-Dokument, das in ein anderes Projekt oder Repository importiert werden kann.


### import-ds

Der Befehl `import-ds` in der ***digna*** CLI wird verwendet, um Datenquellen in ein Zielprojekt zu importieren und einen Importbericht zu erstellen.

#### Befehlsverwendung
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, in das die Datenquellen importiert werden.
- **EXPORT_FILE**: Der Dateiname des zu importierenden Datenquellen-Exports.

#### Optionen

- `--output-file`, `-o`: Datei, in der der Importbericht gespeichert werden soll (wenn nicht angegeben, wird der Bericht tabellarisch in der Konsole ausgegeben).
- `--output-format`, `-f`: Format für den Importbericht (json, csv).
    
#### Beispiel
  
Um alle Datenquellen aus der Exportdatei `my_export.json` in `ProjectB` zu importieren:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Nach dem Import zeigt dieser Befehl auch einen Bericht über importierte und übersprungene Objekte an. Es werden nur neue Datenquellen in `ProjectB` importiert. Um herauszufinden, welche Objekte importiert bzw. übersprungen würden, können Sie den Befehl `plan-import-ds` verwenden.

### plan-import-ds

Der Befehl `plan-import-ds` in der ***digna*** CLI wird verwendet, um einen Import von Datenquellen in ein Zielprojekt zu planen und einen Importbericht zu erstellen.

#### Befehlsverwendung
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, in das die Datenquellen importiert werden würden.
- **EXPORT_FILE**: Der Dateiname des Datenquellen-Exports, der vor dem Import analysiert werden soll.

#### Optionen

- `--output-file`, `-o`: Datei, in der der Importbericht gespeichert werden soll (wenn nicht angegeben, wird der Bericht tabellarisch in der Konsole ausgegeben).
- `--output-format`, `-f`: Format für den Importbericht (json, csv).
    
#### Beispiel
  
Um zu prüfen, welche Datenquellen aus der Exportdatei `my_export.json` beim Import in `ProjectB` importiert bzw. übersprungen würden:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Dieser Befehl zeigt nur einen Importplan der zu importierenden und zu überspringenden Objekte an.
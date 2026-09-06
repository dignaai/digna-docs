# digna CLI Referenz 2024.12
**2024-12-09**

Diese Seite dokumentiert die vollständige Menge an Befehlen der ***digna*** CLI-Version **2024.12**, einschließlich Anwendungsbeispielen und Optionen.

---


**2024-12-09**


---

## CLI-Grundlagen

---

## Verwendung der `--help`-Option

Die `--help`-Option liefert Informationen zu verfügbaren Befehlen und ihrer Verwendung. Es gibt zwei Hauptmöglichkeiten, diese Option zu verwenden:

1. **Allgemeine Hilfe anzeigen:**
   
    Verwenden Sie --help unmittelbar nach dem Stichwort ***dignacli***  
   ```bash
   dignacli --help
   ```

3.  **Hilfe für bestimmte Befehle anfordern:**  
  
    Für detaillierte Informationen zu einem bestimmten Befehl hängen Sie `--help` an diesen Befehl an.
    Zum Beispiel, um Hilfe zum Befehl `add-user` zu erhalten, führen Sie aus:
     ```bash
     dignacli add-user --help
     ```

     ### Ausgabe:
      
     - **Befehlsbeschreibung:** Bietet eine ausführliche Beschreibung dessen, was der Befehl bewirkt.  
     - **Syntax:** Zeigt die genaue Syntax, einschließlich erforderlicher und optionaler Argumente.  
     - **Optionen:** Listet alle für den Befehl spezifischen Optionen mit Erklärungen auf.  
     - **Beispiele:** Liefert Beispiele, wie der Befehl effektiv ausgeführt wird.  

  
## Verwendung des Befehls `check-repo-connection`

Der Befehl check-repo-connection ist ein Hilfsprogramm innerhalb des ***digna*** CLI-Tools, das dazu dient, die Konnektivität und den Zugriff auf ein angegebenes ***digna***-Repository zu testen. Dieser Befehl stellt sicher, dass die CLI mit dem Repository interagieren kann.
      
### Befehlsverwendung
```bash
dignacli check-repo-connection
```

Nach erfolgreicher Ausführung gibt der Befehl eine Bestätigung der Verbindung sowie Details zum Repository aus: Repository-Version, Host, Datenbank und Schema.  
  
Wenn die Repository-Verbindung nicht erfolgreich ist, überprüfen Sie die Datei config.toml auf korrekte Konfigurationseinstellungen.

## Verwendung des Befehls `version`

Um die installierte Version von *dignacli* zu prüfen, verwenden Sie die Option --version.  
  
### Befehlsverwendung
```bash
dignacli --version
```
  
### Beispielausgabe
```bash
dignacli version 2024.12
```

## Verwendung von Logging-Optionen
  
Standardmäßig ist die Konsolenausgabe der ***digna***-Befehle minimalistisch gehalten. Die meisten Befehle bieten die Möglichkeit, zusätzliche Informationen bereitzustellen, mittels der folgenden Optionen:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ und „debug“ legen den Detailgrad fest, während der Schalter „logfile“ die Umleitung der Ausgabe in eine Datei anstatt in das Konsolenfenster erlaubt.

# Benutzerverwaltung

## Verwendung des Befehls `add-user`
  
Der add-user-Befehl in der ***digna*** CLI wird verwendet, um einen neuen Benutzer im ***digna***-System hinzuzufügen.
  
### Befehlsverwendung
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumente

- **USER_NAME**: Der Benutzername des neuen Benutzers (erforderlich).
- **USER_FULL_NAME**: Der vollständige Name des neuen Benutzers (erforderlich).
- **USER_PASSWORD**: Das Passwort für den neuen Benutzer (erforderlich).

### Optionen

- `--is_superuser`, `-su`: Kennzeichnet den neuen Benutzer als Administrator.
- `--valid_until`, `-vu`: Setzt ein Ablaufdatum für das Benutzerkonto im Format `YYYY-MM-DD HH:MI:SS`. Wenn nicht gesetzt, hat das Konto kein Ablaufdatum.

### Beispiel

Um einen neuen Benutzer mit dem Benutzernamen `jdoe`, Vollnamen `John Doe` und Passwort `password123` hinzuzufügen:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Um einen neuen Benutzer hinzuzufügen und ein Ablaufdatum für das Konto zu setzen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Verwendung des Befehls `delete-user`
  
Der `delete-user`-Befehl in der ***digna*** CLI wird verwendet, um einen bestehenden Benutzer aus dem ***digna***-System zu entfernen.
  
### Befehlsverwendung
```bash
dignacli delete-user USER_NAME
```
  
### Argumente
- **USER_NAME**: Der Benutzername des zu löschenden Benutzers (erforderlich). Dies ist das einzige Argument, das der Befehl benötigt.

### Beispiel
```bash
dignacli delete-user jdoe
```
  
Durch Ausführen dieses Befehls wird der Benutzer `jdoe` aus dem ***digna***-System entfernt; damit werden sein Zugriff sowie zugehörige Daten und Berechtigungen aus dem Repository gelöscht.

## Verwendung des Befehls `modify-user`

Der `modify-user`-Befehl in der ***digna*** CLI dient dazu, die Angaben eines bestehenden Benutzers im ***digna***-System zu aktualisieren.

### Befehlsverwendung
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumente
  
- **USER_NAME**: Der Benutzername des zu ändernden Benutzers (erforderlich).
- **USER_FULL_NAME**: Der neue vollständige Name des Benutzers (erforderlich).
  
### Optionen  
  
- `--is_superuser`, `-su`: Setzt den Benutzer als Superuser und gewährt erhöhte Berechtigungen. Dieser Schalter benötigt keinen Wert.  
- `--valid_until`, `-vu`: Setzt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS. Wenn nicht angegeben, bleibt das Konto unbegrenzt gültig.  
  
### Beispiel
  
Um den vollständigen Namen des Benutzers `jdoe` in „Johnathan Doe“ zu ändern und den Benutzer als Superuser zu setzen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Verwendung des Befehls `modify-user-pwd`
  
Der `modify-user-pwd`-Befehl in der ***digna*** CLI wird verwendet, um das Passwort eines bestehenden Benutzers im ***digna***-System zu ändern.
  
### Befehlsverwendung
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumente
  
- **USER_NAME**: Der Benutzername des Benutzers, dessen Passwort geändert werden soll (erforderlich).
- **USER_PWD**: Das neue Passwort für den Benutzer (erforderlich).
  
### Beispiel
  
Um das Passwort des Benutzers `jdoe` in `newpassword123` zu ändern:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Verwendung des Befehls `list-users`

Der `list-users`-Befehl in der ***digna*** CLI zeigt eine Liste aller im ***digna***-System registrierten Benutzer an.

### Befehlsverwendung

```bash
dignacli list-users
```

Beim Ausführen dieses Befehls verbindet sich die ***digna*** CLI mit dem ***digna***-Repository und listet alle Benutzer auf, wobei deren ID, Benutzername, vollständiger Name, Superuser-Status und Ablaufzeitstempel angezeigt werden.

# Repository-Verwaltung

### Verwendung des Befehls `upgrade-repo`
  
Der `upgrade-repo`-Befehl in der ***digna*** CLI wird verwendet, um das ***digna***-Repository zu aktualisieren oder zu initialisieren. Dieser Befehl ist essenziell, um Updates anzuwenden oder die Repository-Infrastruktur zum ersten Mal einzurichten.
  
### Befehlsverwendung

```bash
dignacli upgrade-repo [options]
```
  
### Optionen
  
- `--simulation-mode`, `-s`: Wenn aktiviert, führt dieser Schalter den Befehl im Simulationsmodus aus, wobei die SQL-Anweisungen ausgegeben, aber nicht tatsächlich ausgeführt werden. Dies ist nützlich, um Änderungen zu prüfen, ohne tatsächliche Modifikationen am Repository vorzunehmen.  

  
### Beispiel
  
Um das ***digna***-Repository zu aktualisieren, können Sie den Befehl ohne Optionen ausführen:
  
```bash
dignacli upgrade-repo
```  
Um das Upgrade im Simulationsmodus auszuführen (um die SQL-Anweisungen zu sehen, ohne sie anzuwenden):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dieser Befehl ist wichtig für die Wartung des ***digna***-Systems und stellt sicher, dass das Datenbankschema und andere Repository-Komponenten mit der neuesten Software-Version aktuell sind.

## Verwendung des Befehls `encrypt`
  
Der `encrypt`-Befehl in der ***digna*** CLI wird verwendet, um ein Passwort zu verschlüsseln.
  
### Befehlsverwendung
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumente
- **PASSWORD**: Das zu verschlüsselnde Passwort (erforderlich).
  
### Beispiel
  
Um ein Passwort zu verschlüsseln, müssen Sie das Passwort als Argument übergeben.   
Beispielsweise, um das Passwort `mypassword123` zu verschlüsseln, verwenden Sie:
```bash
dignacli encrypt mypassword123
```
Dieser Befehl gibt die verschlüsselte Version des angegebenen Passworts aus, die dann in sicheren Kontexten verwendet werden kann. Wird das Passwort-Argument nicht angegeben, zeigt die CLI einen Fehler an, der auf das fehlende Argument hinweist.

## Verwendung des Befehls `generate-key`
  
Der Befehl `generate-key` wird verwendet, um einen Fernet-Schlüssel zu generieren, der für die Sicherung von Passwörtern im ***digna***-Repository erforderlich ist.
  
### Befehlsverwendung
```bash
dignacli generate-key
```
  
# Datenverwaltung

## Verwendung des Befehls `clean-up`

Der `clean-up`-Befehl in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Ampelsystems (Traffic Light System, TLS) für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu entfernen. Dieser Befehl ist wichtig für das Daten-Lifecycle-Management und hilft dabei, eine organisierte und effiziente Datenumgebung zu erhalten, indem veraltete oder unnötige Daten gelöscht werden.

### Befehlsverwendung

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, aus dem Daten entfernt werden sollen (erforderlich). Die Verwendung des Schlüsselworts all-projects in diesem Argument weist ***digna*** an, über alle vorhandenen Projekte zu iterieren und den Befehl auf jedes anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Datenlöschung. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Datenlöschung, im gleichen Format wie FROM_DATE (erforderlich).
  
### Optionen
  
- `--table-name`, `-tn`: Beschränkt die Clean-up-Operation auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und beschränkt das Clean-up auf Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--timing`, `-tm`: Zeigt nach Abschluss die Dauer des Clean-up-Prozesses an.
- `--help`: Gibt Hilfsinformationen zum clean-up-Befehl aus und beendet das Programm.
  
### Beispiel
  
Um Daten aus dem Projekt ProjectA zwischen dem 1. Januar 2023 und dem 30. Juni 2023 zu entfernen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Um Daten nur aus einer bestimmten Tabelle mit dem Namen `Table1` zu entfernen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dieser Befehl unterstützt die Verwaltung des Datenspeichers und stellt sicher, dass das Repository nur relevante Informationen enthält.

## Verwendung des Befehls `inspect`

Der `inspect`-Befehl in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Ampelsystems (Traffic Light System, TLS) für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erstellen. Dieser Befehl hilft bei der Analyse und Überwachung von Daten über einen definierten Zeitraum.

### Befehlsverwendung

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, dessen Daten inspiziert werden sollen (erforderlich). Die Verwendung des Schlüsselworts all-projects in diesem Argument weist ***digna*** an, über alle vorhandenen Projekte zu iterieren und den Befehl auf jedes anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit der Dateninspektion. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit der Dateninspektion, im gleichen Format wie FROM_DATE (erforderlich).
  
### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und inspiziert nur Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--do-profile`: Veranlasst die Neuerfassung von Profilen. Standard ist do-profile.
- `--no-do-profile`: Verhindert die Neuerfassung von Profilen.
- `--do-prediction`: Veranlasst die Neuberechnung von Vorhersagen. Standard ist do-prediction.
- `--no-do-prediction`: Verhindert die Neuberechnung von Vorhersagen.
- `--do-alert-status`: Veranlasst die Neuberechnung von Alarmstatus. Standard ist do-alert-status.
- `--no-do-alert-status`: Verhindert die Neuberechnung von Alarmstatus.
- `--iterative`: Veranlasst die Inspektion eines Zeitraums in täglichen Iterationen. Standard ist iterative.
- `--no-iterative`: Veranlasst die Inspektion des gesamten Zeitraums in einem Durchlauf.
- `--timing`, `-tm`: Zeigt nach Abschluss die Dauer des Inspektionsprozesses an.
  
### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 zu inspizieren:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Um nur eine bestimmte Tabelle zu inspizieren und die Neuberechnung von Vorhersagen zu erzwingen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dieser Befehl ist nützlich, um aktuelle Profile und Vorhersagen zu erzeugen, die Datenintegrität zu überwachen und das Alarmwesen innerhalb eines festgelegten Projektzeitraums zu verwalten.

## Verwendung des Befehls `tls-status`

Der `tls-status`-Befehl in der ***digna*** CLI wird verwendet, um den Status des Traffic Light Systems (TLS) für eine bestimmte Tabelle innerhalb eines Projekts an einem bestimmten Datum abzufragen. Das Ampelsystem liefert Einblicke in die Datenqualität und -gesundheit und zeigt etwaige Probleme oder Alarme an, die Aufmerksamkeit erfordern.
  
### Befehlsverwendung
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das der TLS-Status abgefragt wird (erforderlich).
- **TABLE_NAME**: Die spezifische Tabelle innerhalb des Projekts, für die der TLS-Status benötigt wird (erforderlich).
- **DATE**: Das Datum, für das der TLS-Status abgefragt wird, üblicherweise im Format %Y-%m-%d (erforderlich).
  
### Beispiel
  
Um den TLS-Status für eine Tabelle namens UserData im Projekt ProjectA am 1. Juli 2024 zu prüfen:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Dieser Befehl hilft Anwendern, die Datenqualität zu überwachen und zu pflegen, indem er einen klaren und umsetzbaren Statusbericht auf Basis vordefinierter Kriterien liefert.

## Verwendung des Befehls `list-projects`
  
Der `list-projects`-Befehl in der ***digna*** CLI zeigt eine Liste aller verfügbaren Projekte im ***digna***-System an.
  
### Befehlsverwendung
  
```bash
dignacli list-projects
```

Dieser Befehl ist besonders nützlich für Administratoren und Benutzer, die mehrere Projekte verwalten, und bietet einen schnellen Überblick über die verfügbaren Projekte im ***digna***-Repository.

## Verwendung des Befehls `list-ds`

Der `list-ds`-Befehl in der ***digna*** CLI wird verwendet, um eine Liste aller verfügbaren Datenquellen innerhalb eines angegebenen Projekts anzuzeigen. Dieser Befehl ist nützlich, um die verfügbaren Datenassets für Analyse und Verwaltung im ***digna***-System zu verstehen.

### Befehlsverwendung
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumente
- **PROJECT_NAME**: Der Name des Projekts, für das die Datenquellen aufgelistet werden (erforderlich).
  
### Beispiel
  
Um alle Datenquellen im Projekt mit dem Namen `ProjectA` aufzulisten:
  
```bash
dignacli list-ds ProjectA
```
  
Dieser Befehl bietet Anwendern einen Überblick über die in einem Projekt verfügbaren Datenquellen und hilft ihnen, die Datenlandschaft effektiver zu navigieren und zu verwalten.
---
title: digna CLI Referenz 2024.11 – Befehle & Beispiele | digna Dokumentation
description: Vollständige Referenz für die digna CLI Version 2024.11. Erfahren Sie, wie Sie Benutzer, Repositories und Daten mit Befehlen wie add-user, check-repo-connection, upgrade-repo, inspect, tls-status und mehr verwalten.
image: /assets/logo_square.png
---

# digna CLI Referenz 2024.11
**2024-11-03**

Diese Seite dokumentiert die vollständige Menge an Befehlen, die in der ***digna*** CLI-Version **2024.11** verfügbar sind, einschließlich Anwendungsbeispielen und Optionen.


---
## CLI-Grundlagen

---

## Verwendung der `--help`-Option

Die Option `--help` liefert Informationen über verfügbare Befehle und deren Verwendung. Es gibt zwei Hauptarten, diese Option zu verwenden:

1. **Allgemeine Hilfe anzeigen:**
   
    Verwenden Sie `--help` direkt nach dem Befehl ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Hilfe für bestimmte Befehle erhalten:**  
  
    Für detaillierte Informationen zu einem bestimmten Befehl hängen Sie `--help` an diesen Befehl an.
    Zum Beispiel, um Hilfe zum Befehl `add-user` zu erhalten, führen Sie aus:
     ```bash
     dignacli add-user --help
     ```

     ### Ausgabe:
      
     - **Befehlsbeschreibung:** Bietet eine detaillierte Erklärung, was der Befehl bewirkt.  
     - **Syntax:** Zeigt die genaue Syntax, einschließlich erforderlicher und optionaler Argumente.  
     - **Optionen:** Listet alle spezifischen Optionen des Befehls mit Erklärungen auf.  
     - **Beispiele:** Stellt Beispiele zur Verfügung, wie der Befehl effektiv ausgeführt wird.

  
## Verwendung des `check-repo-connection`-Befehls

Der Befehl `check-repo-connection` ist ein Hilfsprogramm innerhalb der ***digna*** CLI, das entwickelt wurde, um die Konnektivität und den Zugriff auf ein angegebenes ***digna*** Repository zu testen. Dieser Befehl stellt sicher, dass die CLI mit dem Repository interagieren kann.
      
### Befehlsverwendung
```bash
dignacli check-repo-connection
```

Bei erfolgreicher Ausführung gibt der Befehl eine Bestätigung der Verbindung sowie Details zum Repository aus: Repository-Version, Host, Datenbank und Schema.  
  
Wenn die Repository-Verbindung nicht erfolgreich ist, prüfen Sie die Datei config.toml auf korrekte Konfigurationseinstellungen.

## Verwendung des `--version`-Befehls

Um die installierte Version von *dignacli* zu prüfen, verwenden Sie die Option `--version`.  
  
### Befehlsverwendung
```bash
dignacli --version
```
  
### Beispielausgabe
```bash
dignacli version 2024.11
```

## Verwendung von Logging-Optionen
  
Standardmäßig ist die Konsolenausgabe der ***digna*** Befehle minimalistisch gehalten. Die meisten Befehle bieten die Möglichkeit, zusätzliche Informationen bereitzustellen, mit den folgenden Optionen:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ und „debug“ legen den Detaillierungsgrad fest, während die Option „logfile“ die Ausgabe in eine Datei lenkt, anstatt sie im Konsolenfenster anzuzeigen.

# Benutzerverwaltung

## Verwendung des `add-user`-Befehls
  
Der Befehl `add-user` in der ***digna*** CLI wird verwendet, um einen neuen Benutzer im ***digna*** System anzulegen.
  
### Befehlsverwendung
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumente

- **USER_NAME**: Der Benutzername für den neuen Benutzer (erforderlich).
- **USER_FULL_NAME**: Der vollständige Name des neuen Benutzers (erforderlich).
- **USER_PASSWORD**: Das Passwort für den neuen Benutzer (erforderlich).

### Optionen

- `--is_superuser`, `-su`: Kennzeichnet den neuen Benutzer als Administrator.
- `--valid_until`, `-vu`: Legt ein Ablaufdatum für das Benutzerkonto im Format `YYYY-MM-DD HH:MI:SS` fest. Wenn nicht gesetzt, hat das Konto kein Ablaufdatum.

### Beispiel

Um einen neuen Benutzer mit dem Benutzernamen `jdoe`, dem vollständigen Namen `John Doe` und dem Passwort `password123` hinzuzufügen:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Um einen neuen Benutzer hinzuzufügen und ein Ablaufdatum für das Konto zu setzen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Verwendung des `delete-user`-Befehls
  
Der Befehl `delete-user` in der ***digna*** CLI wird verwendet, um einen bestehenden Benutzer aus dem ***digna*** System zu entfernen.
  
### Befehlsverwendung
```bash
dignacli delete-user USER_NAME
```
  
### Argumente
- **USER_NAME**: Der Benutzername des zu löschenden Benutzers (erforderlich). Dies ist das einzige vom Befehl benötigte Argument.

### Beispiel
```bash
dignacli delete-user jdoe
```
  
Durch Ausführen dieses Befehls wird der Benutzer `jdoe` aus dem ***digna*** System entfernt, sein Zugriff widerrufen und die zugehörigen Daten und Berechtigungen im Repository gelöscht.

## Verwendung des `modify-user`-Befehls

Der Befehl `modify-user` in der ***digna*** CLI dient zum Aktualisieren der Angaben eines bestehenden Benutzers im ***digna*** System.

### Befehlsverwendung
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumente
  
- **USER_NAME**: Der Benutzername des zu ändernden Benutzers (erforderlich).
- **USER_FULL_NAME**: Der neue vollständige Name des Benutzers (erforderlich).
  
### Optionen  
  
- `--is_superuser`, `-su`: Setzt den Benutzer als Superuser und gewährt erhöhte Berechtigungen. Dieses Flag benötigt keinen Wert.  
- `--valid_until`, `-vu`: Legt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS fest. Wenn nicht angegeben, bleibt das Konto unbefristet gültig.  
  
### Beispiel
  
Um den vollständigen Namen des Benutzers `jdoe` in „Johnathan Doe“ zu ändern und den Benutzer als Superuser zu setzen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Verwendung des `modify-user-pwd`-Befehls
  
Der Befehl `modify-user-pwd` in der ***digna*** CLI wird verwendet, um das Passwort eines bestehenden Benutzers im ***digna*** System zu ändern.
  
### Befehlsverwendung
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumente
  
- **USER_NAME**: Der Benutzername des Benutzers, dessen Passwort geändert werden soll (erforderlich).
- **USER_PWD**: Das neue Passwort für den Benutzer (erforderlich).
  
### Beispiel
  
Um das Passwort des Benutzers `jdoe` auf `newpassword123` zu ändern:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Verwendung des `list-users`-Befehls

Der Befehl `list-users` in der ***digna*** CLI zeigt eine Liste aller im ***digna*** System registrierten Benutzer an.

### Befehlsverwendung

```bash
dignacli list-users
```

Beim Ausführen dieses Befehls verbindet sich die ***digna*** CLI mit dem ***digna*** Repository und listet alle Benutzer auf, einschließlich ihrer ID, Benutzernamen, vollständigen Namen, Superuser-Status und Ablaufzeitstempel.

# Repository-Verwaltung

### Verwendung des `upgrade-repo`-Befehls
  
Der Befehl `upgrade-repo` in der ***digna*** CLI wird verwendet, um das ***digna*** Repository zu aktualisieren oder zu initialisieren. Dieser Befehl ist wesentlich, um Updates anzuwenden oder die Repository-Infrastruktur für die erste Verwendung einzurichten.
  
### Befehlsverwendung

```bash
dignacli upgrade-repo [options]
```
  
### Optionen
  
- `--simulation-mode`, `-s`: Führt den Befehl im Simulationsmodus aus. In diesem Modus werden die SQL-Anweisungen, die ausgeführt würden, ausgegeben, aber nicht tatsächlich ausgeführt. Dies ist nützlich, um Änderungen zu prüfen, ohne das Repository zu verändern.  

  
### Beispiel
  
Um das ***digna*** Repository zu aktualisieren, können Sie den Befehl ohne Optionen ausführen:
  
```bash
dignacli upgrade-repo
```  
Um das Upgrade im Simulationsmodus auszuführen (um die SQL-Anweisungen zu sehen, ohne sie anzuwenden):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dieser Befehl ist wichtig, um das ***digna*** System zu warten und sicherzustellen, dass das Datenbankschema und weitere Repository-Komponenten mit der neuesten Softwareversion übereinstimmen.

## Verwendung des `encrypt`-Befehls
  
Der Befehl `encrypt` in der ***digna*** CLI wird verwendet, um ein Passwort zu verschlüsseln.
  
### Befehlsverwendung
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumente
- **PASSWORD**: Das zu verschlüsselnde Passwort (erforderlich).
  
### Beispiel
  
Um ein Passwort zu verschlüsseln, geben Sie das Passwort als Argument an.   
Zum Beispiel, um das Passwort `mypassword123` zu verschlüsseln, verwenden Sie:
```bash
dignacli encrypt mypassword123
```
Dieser Befehl gibt die verschlüsselte Version des angegebenen Passworts aus, die dann in sicheren Kontexten verwendet werden kann. Wenn das Passwort-Argument nicht angegeben ist, zeigt die CLI einen Fehler mit dem fehlenden Argument an.

## Verwendung des `generate-key`-Befehls
  
Der Befehl `generate-key` wird verwendet, um einen Fernet-Schlüssel zu erzeugen, der für die Sicherung von Passwörtern im ***digna*** Repository erforderlich ist.
  
### Befehlsverwendung
```bash
dignacli generate-key
```
  
# Datenverwaltung

## Verwendung des `clean-up`-Befehls

Der Befehl `clean-up` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Traffic Light Systems für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu entfernen. Dieser Befehl ist wichtig für das Data-Lifecycle-Management und hilft dabei, eine organisierte und effiziente Datenumgebung zu erhalten, indem veraltete oder unnötige Daten bereinigt werden.

### Befehlsverwendung

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, aus dem Daten entfernt werden sollen (erforderlich). Die Verwendung des Schlüsselworts `all-projects` in diesem Argument veranlasst ***digna***, über alle vorhandenen Projekte zu iterieren und den Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Datenlöschung. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Datenlöschung, nach denselben Formaten wie FROM_DATE (erforderlich).
  
### Optionen
  
- `--table-name`, `-tn`: Beschränkt den Clean-up auf eine spezifische Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und begrenzt den Clean-up auf Tabellen, die den angegebenen Teilstring im Namen enthalten.
- `--timing`, `-tm`: Zeigt die Dauer des Clean-up-Prozesses nach Abschluss an.
- `--help`: Zeigt Hilfsinformationen für den clean-up-Befehl an und beendet das Programm.
  
### Beispiel
  
Um Daten aus dem Projekt ProjectA zwischen dem 1. Januar 2023 und dem 30. Juni 2023 zu entfernen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Um Daten nur aus einer spezifischen Tabelle namens `Table1` zu entfernen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dieser Befehl hilft bei der Verwaltung des Datenvolumens und stellt sicher, dass das Repository nur relevante Informationen enthält.

## Verwendung des `inspect`-Befehls

Der Befehl `inspect` in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Traffic Light Systems für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erstellen. Dieser Befehl unterstützt bei der Analyse und Überwachung von Daten über einen definierten Zeitraum.

### Befehlsverwendung

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das Daten inspiziert werden sollen (erforderlich). Die Verwendung des Schlüsselworts `all-projects` in diesem Argument veranlasst ***digna***, über alle vorhandenen Projekte zu iterieren und den Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Dateninspektion. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Dateninspektion, nach denselben Formaten wie FROM_DATE (erforderlich).
  
### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und inspiziert nur Tabellen, die den angegebenen Teilstring im Namen enthalten.
- `--do-profile`: Veranlasst die Neuerfassung von Profilen. Standard ist do-profile.
- `--no-do-profile`: Verhindert die Neuerfassung von Profilen.
- `--do-prediction`: Veranlasst die Neuberechnung von Vorhersagen. Standard ist do-prediction.
- `--no-do-prediction`: Verhindert die Neuberechnung von Vorhersagen.
- `--do-alert-status`: Veranlasst die Neuberechnung von Alarmstatus. Standard ist do-alert-status.
- `--no-do-alert-status`: Verhindert die Neuberechnung von Alarmstatus.
- `--timing`, `-tm`: Zeigt die Dauer des Inspektionsprozesses nach Abschluss an.
  
### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 zu inspizieren:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Um nur eine bestimmte Tabelle zu inspizieren und die Neuberechnung von Vorhersagen zu erzwingen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dieser Befehl ist nützlich, um aktualisierte Profile und Vorhersagen zu erzeugen, die Datenintegrität zu überwachen und das Alarmmanagement innerhalb eines bestimmten Projektzeitraums zu steuern.

## Verwendung des `tls-status`-Befehls

Der Befehl `tls-status` in der ***digna*** CLI wird verwendet, um den Status des Traffic Light Systems (TLS) für eine bestimmte Tabelle innerhalb eines Projekts an einem gegebenen Datum abzufragen. Das Traffic Light System liefert Einblicke in die Datenqualität und -gesundheit und weist auf Probleme oder Alarme hin, die Aufmerksamkeit erfordern könnten.
  
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

Dieser Befehl hilft Benutzern, die Datenqualität zu überwachen und zu erhalten, indem er einen klaren und umsetzbaren Statusbericht auf Basis vordefinierter Kriterien liefert.

## Verwendung des `list-projects`-Befehls
  
Der Befehl `list-projects` in der ***digna*** CLI dient dazu, eine Liste aller verfügbaren Projekte im ***digna*** System anzuzeigen.
  
### Befehlsverwendung
  
```bash
dignacli list-projects
```

Dieser Befehl ist besonders nützlich für Administratoren und Benutzer, die mehrere Projekte verwalten, und bietet einen schnellen Überblick über die verfügbaren Projekte im ***digna*** Repository.

## Verwendung des `list-ds`-Befehls

Der Befehl `list-ds` in der ***digna*** CLI zeigt eine Liste aller verfügbaren Datenquellen innerhalb eines angegebenen Projekts an. Dieser Befehl ist hilfreich, um die verfügbaren Datenressourcen für Analyse und Verwaltung im ***digna*** System zu verstehen.

### Befehlsverwendung
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumente
- **PROJECT_NAME**: Der Name des Projekts, für das die Datenquellen aufgelistet werden sollen (erforderlich).
  
### Beispiel
  
Um alle Datenquellen im Projekt `ProjectA` aufzulisten:
  
```bash
dignacli list-ds ProjectA
```
  
Dieser Befehl gibt den Benutzern einen Überblick über die im Projekt verfügbaren Datenquellen und hilft ihnen, die Datenlandschaft effektiver zu navigieren und zu verwalten.
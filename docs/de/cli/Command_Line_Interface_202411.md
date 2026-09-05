---
title: digna CLI Referenz 2024.11 – Befehle & Beispiele | digna Dokumentation
description: Vollständige Referenz für die digna CLI-Version 2024.11. Erfahren Sie, wie Sie Benutzer, Repositories und Daten mit Befehlen wie add-user, check-repo-connection, upgrade-repo, inspect, tls-status und weiteren verwalten.
image: /assets/logo_square.png
---

# digna CLI Referenz 2024.11
**2024-11-03**

Diese Seite dokumentiert das vollständige Befehlsset der ***digna*** CLI-Version **2024.11**, einschließlich Nutzungsbeispielen und Optionen.


---
## CLI-Grundlagen

---

## Verwendung der `--help`-Option

Die `--help`-Option liefert Informationen über verfügbare Befehle und deren Verwendung. Es gibt zwei Hauptvarianten, diese Option zu nutzen:

1. **Allgemeine Hilfe anzeigen:**
   
    Verwenden Sie `--help` direkt nach dem Schlüsselwort `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Hilfe zu einem konkreten Befehl erhalten:**  
  
    Für detaillierte Informationen zu einem bestimmten Befehl hängen Sie `--help` an diesen Befehl an.  
    Zum Beispiel, um Hilfe zum Befehl `add-user` zu erhalten, führen Sie aus:
     ```bash
     dignacli add-user --help
     ```

     ### Ausgabe:
      
     - **Befehlsbeschreibung:** Liefert eine ausführliche Beschreibung der Funktion des Befehls.  
     - **Syntax:** Zeigt die genaue Syntax, einschließlich erforderlicher und optionaler Argumente.  
     - **Optionen:** Listet alle zum Befehl gehörenden Optionen mit Erklärungen auf.  
     - **Beispiele:** Bietet Beispiele zur effektiven Ausführung des Befehls.

  
## Verwendung des `check-repo-connection`-Befehls

Der `check-repo-connection`-Befehl ist ein Dienstprogramm innerhalb des ***digna*** CLI-Tools, das die Konnektivität und den Zugriff auf ein angegebenes ***digna*** Repository prüft. Dieser Befehl stellt sicher, dass die CLI mit dem Repository interagieren kann.
      
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
  
Standardmäßig ist die Konsolenausgabe der ***digna***-Befehle minimal gehalten. Die meisten Befehle bieten jedoch die Möglichkeit, zusätzliche Informationen auszugeben, und unterstützen dazu folgende Optionen:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ und „debug“ legen den Detailgrad fest, während der Schalter „logfile“ die Ausgabe in eine Datei umleitet, anstatt sie im Konsolenfenster darzustellen.

# Benutzerverwaltung

## Verwendung des `add-user`-Befehls
  
Der `add-user`-Befehl in der ***digna*** CLI wird verwendet, um einen neuen Benutzer im ***digna***-System anzulegen.
  
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

Um einen neuen Benutzer mit dem Benutzernamen `jdoe`, dem vollständigen Namen `John Doe` und dem Passwort `password123` hinzuzufügen:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Um einen neuen Benutzer hinzuzufügen und ein Ablaufdatum für das Konto zu setzen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Verwendung des `delete-user`-Befehls
  
Der `delete-user`-Befehl in der ***digna*** CLI wird verwendet, um einen bestehenden Benutzer aus dem ***digna***-System zu entfernen.
  
### Befehlsverwendung
```bash
dignacli delete-user USER_NAME
```
  
### Argumente
- **USER_NAME**: Der Benutzername des zu löschenden Benutzers (erforderlich). Dies ist das einzige erforderliche Argument des Befehls.

### Beispiel
```bash
dignacli delete-user jdoe
```
  
Durch Ausführung dieses Befehls wird der Benutzer `jdoe` aus dem ***digna***-System entfernt, sein Zugang entzogen und seine zugehörigen Daten sowie Berechtigungen im Repository gelöscht.

## Verwendung des `modify-user`-Befehls

Der `modify-user`-Befehl in der ***digna*** CLI wird verwendet, um die Angaben eines bestehenden Benutzers im ***digna***-System zu aktualisieren.

### Befehlsverwendung
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumente
  
- **USER_NAME**: Der Benutzername des zu ändernden Benutzers (erforderlich).
- **USER_FULL_NAME**: Der neue vollständige Name des Benutzers (erforderlich).
  
### Optionen  
  
- `--is_superuser`, `-su`: Setzt den Benutzer als Superuser und gewährt erweiterte Rechte. Dieses Flag benötigt keinen Wert.  
- `--valid_until`, `-vu`: Legt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS fest. Wenn nicht angegeben, bleibt das Konto unbegrenzt gültig.  
  
### Beispiel
  
Um den vollständigen Namen des Benutzers `jdoe` auf „Johnathan Doe“ zu ändern und den Benutzer als Superuser zu setzen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Verwendung des `modify-user-pwd`-Befehls
  
Der `modify-user-pwd`-Befehl in der ***digna*** CLI wird verwendet, um das Passwort eines bestehenden Benutzers im ***digna***-System zu ändern.
  
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

Der `list-users`-Befehl in der ***digna*** CLI zeigt eine Liste aller im ***digna***-System registrierten Benutzer an.

### Befehlsverwendung

```bash
dignacli list-users
```

Bei Ausführung dieses Befehls verbindet sich die ***digna*** CLI mit dem ***digna***-Repository und listet alle Benutzer auf, einschließlich ihrer ID, ihres Benutzernamens, vollständigen Namens, Superuser-Status und Ablaufzeitstempel.

# Repository-Verwaltung

### Verwendung des `upgrade-repo`-Befehls
  
Der `upgrade-repo`-Befehl in der ***digna*** CLI wird verwendet, um das ***digna***-Repository zu aktualisieren oder zu initialisieren. Dieser Befehl ist erforderlich, um Updates anzuwenden oder die Repository-Infrastruktur erstmals einzurichten.
  
### Befehlsverwendung

```bash
dignacli upgrade-repo [options]
```
  
### Optionen
  
- `--simulation-mode`, `-s`: Wenn aktiviert, wird der Befehl im Simulationsmodus ausgeführt; die SQL-Anweisungen, die ausgeführt würden, werden ausgegeben, aber nicht tatsächlich angewendet. Dies ist nützlich, um Änderungen vorab zu prüfen, ohne das Repository zu verändern.  

  
### Beispiel
  
Um das ***digna***-Repository zu aktualisieren, können Sie den Befehl ohne Optionen ausführen:
  
```bash
dignacli upgrade-repo
```  
Um das Upgrade im Simulationsmodus auszuführen (um die SQL-Anweisungen ohne Anwendung zu sehen):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dieser Befehl ist entscheidend für die Pflege des ***digna***-Systems und stellt sicher, dass das Datenbankschema und andere Repository-Komponenten mit der neuesten Softwareversion übereinstimmen.

## Verwendung des `encrypt`-Befehls
  
Der `encrypt`-Befehl in der ***digna*** CLI wird verwendet, um ein Passwort zu verschlüsseln.
  
### Befehlsverwendung
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumente
- **PASSWORD**: Das zu verschlüsselnde Passwort (erforderlich).
  
### Beispiel
  
Um ein Passwort zu verschlüsseln, übergeben Sie das Passwort als Argument.   
Beispielsweise, um das Passwort `mypassword123` zu verschlüsseln, verwenden Sie:
```bash
dignacli encrypt mypassword123
```
Dieser Befehl gibt die verschlüsselte Version des übergebenen Passworts aus, die dann in sicheren Kontexten verwendet werden kann. Wenn das Passwort-Argument nicht angegeben wird, zeigt die CLI einen Fehler wegen des fehlenden Arguments an.

## Verwendung des `generate-key`-Befehls
  
Der `generate-key`-Befehl erzeugt einen Fernet-Schlüssel, der zur Absicherung von Passwörtern im ***digna***-Repository erforderlich ist.
  
### Befehlsverwendung
```bash
dignacli generate-key
```
  
# Datenverwaltung

## Verwendung des `clean-up`-Befehls

Der `clean-up`-Befehl in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Traffic-Light-Systems für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu entfernen. Dieser Befehl ist wichtig für das Datenlebenszyklus-Management und hilft dabei, eine organisierte und effiziente Datenumgebung zu erhalten, indem veraltete oder unnötige Daten gelöscht werden.

### Befehlsverwendung

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, aus dem Daten entfernt werden sollen (erforderlich). Wenn als Wert das Schlüsselwort `all-projects` verwendet wird, weist dies ***digna*** an, alle bestehenden Projekte zu durchlaufen und den Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Datenlöschung. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Datenlöschung, im gleichen Format wie FROM_DATE (erforderlich).
  
### Optionen
  
- `--table-name`, `-tn`: Beschränkt die Clean-up-Operation auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und begrenzt die Clean-up-Operation auf Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--timing`, `-tm`: Zeigt nach Abschluss die Dauer des Clean-up-Vorgangs an.
- `--help`: Zeigt Hilfeinformationen zum Clean-up-Befehl an und beendet die Ausführung.
  
### Beispiel
  
Um Daten aus dem Projekt ProjectA zwischen dem 1. Januar 2023 und dem 30. Juni 2023 zu entfernen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Um Daten nur aus einer bestimmten Tabelle namens `Table1` zu entfernen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dieser Befehl unterstützt bei der Verwaltung des Datenvolumens und stellt sicher, dass das Repository nur relevante Informationen enthält.

## Verwendung des `inspect`-Befehls

Der `inspect`-Befehl in der ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Traffic-Light-Systems für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erstellen. Dieser Befehl hilft bei der Analyse und Überwachung von Daten über einen definierten Zeitraum.

### Befehlsverwendung

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das Daten inspiziert werden sollen (erforderlich). Wenn als Wert das Schlüsselwort `all-projects` verwendet wird, weist dies ***digna*** an, alle bestehenden Projekte zu durchlaufen und den Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Dateninspektion. Zulässige Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Dateninspektion, im gleichen Format wie FROM_DATE (erforderlich).
  
### Optionen

- `--table-name`, `-tn`: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- `--table-filter`, `-tf`: Filtert und inspiziert nur Tabellen, deren Namen die angegebene Teilzeichenfolge enthalten.
- `--do-profile`: Löst die Neuerfassung von Profilen aus. Standard ist do-profile.
- `--no-do-profile`: Verhindert die Neuerfassung von Profilen.
- `--do-prediction`: Löst die Neuberechnung von Vorhersagen aus. Standard ist do-prediction.
- `--no-do-prediction`: Verhindert die Neuberechnung von Vorhersagen.
- `--do-alert-status`: Löst die Neuberechnung von Alert-Status aus. Standard ist do-alert-status.
- `--no-do-alert-status`: Verhindert die Neuberechnung von Alert-Status.
- `--timing`, `-tm`: Zeigt nach Abschluss die Dauer des Inspektionsvorgangs an.
  
### Beispiel
  
Um Daten für das Projekt `ProjectA` vom 1. Januar 2024 bis zum 31. Januar 2024 zu inspizieren:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Um nur eine bestimmte Tabelle zu inspizieren und die Neuberechnung von Vorhersagen zu erzwingen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dieser Befehl ist nützlich, um aktualisierte Profile und Vorhersagen zu erzeugen, die Datenintegrität zu überwachen und Alert-Systeme innerhalb eines definierten Projektzeitraums zu verwalten.

## Verwendung des `tls-status`-Befehls

Der `tls-status`-Befehl in der ***digna*** CLI wird verwendet, um den Status des Traffic Light Systems (TLS) für eine bestimmte Tabelle innerhalb eines Projekts an einem gegebenen Datum abzufragen. Das Traffic Light System liefert Einblicke in die Datenqualität und -gesundheit und signalisiert mögliche Probleme oder Alerts, die Aufmerksamkeit erfordern.
  
### Befehlsverwendung
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das der TLS-Status abgefragt wird (erforderlich).
- **TABLE_NAME**: Die spezifische Tabelle innerhalb des Projekts, für die der TLS-Status benötigt wird (erforderlich).
- **DATE**: Das Datum, für das der TLS-Status abgefragt wird, typischerweise im Format %Y-%m-%d (erforderlich).
  
### Beispiel
  
Um den TLS-Status für eine Tabelle namens UserData im Projekt ProjectA am 1. Juli 2024 zu prüfen:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Dieser Befehl hilft Benutzern, die Datenqualität zu überwachen und auf Basis vordefinierter Kriterien klare und umsetzbare Statusberichte zu erhalten.

## Verwendung des `list-projects`-Befehls
  
Der `list-projects`-Befehl in der ***digna*** CLI zeigt eine Liste aller verfügbaren Projekte im ***digna***-System an.
  
### Befehlsverwendung
  
```bash
dignacli list-projects
```

Dieser Befehl ist besonders nützlich für Administratoren und Benutzer, die mehrere Projekte verwalten, und bietet einen schnellen Überblick über die im ***digna***-Repository verfügbaren Projekte.

## Verwendung des `list-ds`-Befehls

Der `list-ds`-Befehl in der ***digna*** CLI zeigt eine Liste aller verfügbaren Datenquellen innerhalb eines angegebenen Projekts an. Dieser Befehl ist hilfreich, um die im ***digna***-System verfügbaren Datenassets für Analyse und Verwaltung zu verstehen.

### Befehlsverwendung
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumente
- **PROJECT_NAME**: Der Name des Projekts, für das die Datenquellen aufgelistet werden (erforderlich).
  
### Beispiel
  
Um alle Datenquellen im Projekt `ProjectA` aufzulisten:
  
```bash
dignacli list-ds ProjectA
```
  
Dieser Befehl verschafft Benutzern einen Überblick über die in einem Projekt verfügbaren Datenquellen und erleichtert die Navigation und Verwaltung der Datenlandschaft.
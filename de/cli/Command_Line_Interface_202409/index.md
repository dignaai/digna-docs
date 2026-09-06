# digna CLI Referenz 2024.09
**2024-08-24**

---

## CLI-Grundlagen

---

###   help

Die Option --help liefert Informationen über verfügbare Befehle und deren Verwendung. Es gibt zwei Hauptmöglichkeiten, diese Option zu nutzen:

1. **Allgemeine Hilfe anzeigen:**
   
    Verwenden Sie --help unmittelbar nach dem Schlüsselwort ***digna***cl  
   bash
   dignacli --help

3.  **Hilfe für spezifische Befehle erhalten:**  
  
    Für detaillierte Informationen zu einem bestimmten Befehl hängen Sie --help an diesen Befehl an.
    Zum Beispiel, um Hilfe zum Befehl add-user zu erhalten, führen Sie aus:
     bash
     dignacli add-user --help
     

     ### Ausgabe:
      
     - **Befehlsbeschreibung:** Bietet eine ausführliche Beschreibung dessen, was der Befehl macht.  
     - **Syntax:** Zeigt die genaue Syntax, einschließlich erforderlicher und optionaler Argumente.  
     - **Optionen:** Listet alle spezifischen Optionen des Befehls mit ihren Erklärungen auf.  
     - **Beispiele:** Liefert Beispiele, wie der Befehl effektiv ausgeführt wird.

  
###   check-repo-connection

Der Befehl check-repo-connection ist ein Hilfsprogramm im ***digna*** CLI-Tool, das dazu dient, die Konnektivität und den Zugriff auf ein angegebenes ***digna*** Repository zu testen. Dieser Befehl stellt sicher, dass das CLI mit dem Repository interagieren kann.
      
##### Befehlsverwendung
bash
dignacli check-repo-connection


Bei erfolgreicher Ausführung gibt der Befehl eine Bestätigung der Verbindung aus sowie Details zum Repository: Repository-Version, Host, Datenbank und Schema.  
  
Wenn die Verbindung zum Repository nicht erfolgreich ist, prüfen Sie die Datei config.toml auf korrekte Konfigurationseinstellungen.

###   version

Um die installierte Version von *dignacli* zu prüfen, verwenden Sie die Option --version.  
  
#### Befehlsverwendung
bash
dignacli --version

  
#### Beispielausgabe
bash
dignacli version 2024.09


###   Logging-Optionen
  
Standardmäßig ist die Konsolenausgabe der ***digna***-Befehle minimalistisch gehalten. Die meisten Befehle bieten die Möglichkeit, zusätzliche Informationen bereitzustellen, mit den folgenden Optionen:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ und „debug“ definieren das Detaillierungsniveau, während die Option „logfile“ das Weiterleiten der Ausgabe in eine Datei anstelle des Konsolenfensters ermöglicht.

## Benutzerverwaltung

###   add-user
  
Der Befehl add-user im ***digna*** CLI wird verwendet, um einen neuen Benutzer zum ***digna***-System hinzuzufügen.
  
#### Befehlsverwendung
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumente

- **USER_NAME**: Der Benutzername des neuen Benutzers (erforderlich).
- **USER_FULL_NAME**: Der vollständige Name des neuen Benutzers (erforderlich).
- **USER_PASSWORD**: Das Passwort für den neuen Benutzer (erforderlich).

#### Optionen

- --is_superuser, -su: Kennzeichnet den neuen Benutzer als Administrator.
- --valid_until, -vu: Legt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS fest. Wenn nicht gesetzt, hat das Konto kein Ablaufdatum.

#### Beispiel

Um einen neuen Benutzer mit dem Benutzernamen jdoe, dem vollständigen Namen John Doe und dem Passwort password123 hinzuzufügen:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Um einen neuen Benutzer hinzuzufügen und ein Ablaufdatum für das Konto zu setzen:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
Der Befehl delete-user im ***digna*** CLI wird verwendet, um einen bestehenden Benutzer aus dem ***digna***-System zu entfernen.
  
##### Befehlsverwendung
bash
dignacli delete-user USER_NAME

  
#### Argumente
- **USER_NAME**: Der Benutzername des zu löschenden Benutzers (erforderlich). Dies ist das einzige vom Befehl benötigte Argument.

#### Beispiel
bash
dignacli delete-user jdoe

  
Durch Ausführen dieses Befehls wird der Benutzer jdoe aus dem ***digna***-System entfernt, sein Zugriff widerrufen und seine zugehörigen Daten und Berechtigungen aus dem Repository gelöscht.

###   modify-user

Der Befehl modify-user im ***digna*** CLI wird verwendet, um die Details eines bestehenden Benutzers im ***digna***-System zu aktualisieren.

##### Befehlsverwendung
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumente
  
- **USER_NAME**: Der Benutzername des zu ändernden Benutzers (erforderlich).
- **USER_FULL_NAME**: Der neue vollständige Name des Benutzers (erforderlich).
  
#### Optionen  
  
- --is_superuser, -su: Setzt den Benutzer als Superuser und gewährt erhöhte Privilegien. Dieses Flag erfordert keinen Wert.  
- --valid_until, -vu: Legt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS fest. Wenn nicht angegeben, bleibt das Konto unbegrenzt gültig.  
  
#### Beispiel
  
Um den vollständigen Namen des Benutzers jdoe in „Johnathan Doe“ zu ändern und den Benutzer als Superuser zu setzen:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
Der Befehl modify-user-pwd im ***digna*** CLI wird verwendet, um das Passwort eines bestehenden Benutzers im ***digna***-System zu ändern.
  
##### Befehlsverwendung
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumente
  
- **USER_NAME**: Der Benutzername des Benutzers, dessen Passwort geändert werden soll (erforderlich).
- **USER_PWD**: Das neue Passwort für den Benutzer (erforderlich).
  
#### Beispiel
  
Um das Passwort des Benutzers jdoe auf newpassword123 zu ändern:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

Der Befehl list-users im ***digna*** CLI zeigt eine Liste aller im ***digna***-System registrierten Benutzer an.

##### Befehlsverwendung

bash
dignacli list-users


Bei Ausführung dieses Befehls verbindet sich das ***digna*** CLI mit dem ***digna***-Repository und listet alle Benutzer auf, wobei ID, Benutzername, vollständiger Name, Superuser-Status und Ablaufzeitstempel angezeigt werden.

# Repository-Verwaltung

###   upgrade-repo
  
Der Befehl upgrade-repo im ***digna*** CLI wird verwendet, um das ***digna***-Repository zu aktualisieren oder zu initialisieren. Dieser Befehl ist wichtig, um Updates anzuwenden oder die Repository-Infrastruktur zum ersten Mal einzurichten.
  
#### Befehlsverwendung

bash
dignacli upgrade-repo [options]

  
#### Optionen
  
- --simulation-mode, -s: Wenn aktiviert, führt diese Option den Befehl im Simulationsmodus aus, wodurch die SQL-Anweisungen gedruckt werden, die ausgeführt würden, ohne sie tatsächlich auszuführen. Dies ist nützlich, um Änderungen vorab zu prüfen, ohne am Repository Änderungen vorzunehmen.  

  
#### Beispiel
  
Um das ***digna***-Repository zu aktualisieren, können Sie den Befehl ohne Optionen ausführen:
  
bash
dignacli upgrade-repo
  
Um das Upgrade im Simulationsmodus auszuführen (um die SQL-Anweisungen ohne Anwendung zu sehen):
  
bash
dignacli upgrade-repo --simulation-mode

  
Dieser Befehl ist entscheidend für die Wartung des ***digna***-Systems und stellt sicher, dass das Datenbankschema und andere Repository-Komponenten mit der neuesten Version der Software auf dem aktuellen Stand sind.

###   encrypt
  
Der Befehl encrypt im ***digna*** CLI wird verwendet, um ein Passwort zu verschlüsseln.
  
#### Befehlsverwendung
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumente
- **PASSWORD**: Das zu verschlüsselnde Passwort (erforderlich).
  
#### Beispiel
  
Um ein Passwort zu verschlüsseln, müssen Sie das Passwort als Argument übergeben.   
Zum Beispiel, um das Passwort mypassword123 zu verschlüsseln, würden Sie verwenden:
bash
dignacli encrypt mypassword123

Dieser Befehl gibt die verschlüsselte Version des angegebenen Passworts aus, die dann in sicheren Kontexten verwendet werden kann. Wenn das Passwort-Argument nicht angegeben wird, zeigt das CLI einen Fehler an, der auf das fehlende Argument hinweist.

###   generate-key
  
Der Befehl generate-key wird verwendet, um einen Fernet-Schlüssel zu erzeugen, der für die Sicherung von Passwörtern im ***digna***-Repository erforderlich ist.
  
#### Befehlsverwendung
bash
dignacli generate-key

  
## Datenverwaltung

###   clean-up

Der Befehl clean-up im ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Ampelsystems (Traffic Light System) für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu entfernen. Dieser Befehl ist wichtig für das Datenlebenszyklus-Management und hilft, eine organisierte und effiziente Datenumgebung zu erhalten, indem veraltete oder unnötige Daten gelöscht werden.

#### Befehlsverwendung

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, aus dem Daten entfernt werden sollen (erforderlich). Wenn Sie das Schlüsselwort all-projects als Argument verwenden, weist das ***digna*** an, über alle vorhandenen Projekte zu iterieren und diesen Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Datenlöschung. Akzeptierte Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Datenlöschung, mit denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen
  
- --table-name, -tn: Beschränkt den Clean-up-Vorgang auf eine bestimmte Tabelle innerhalb des Projekts.
- --table-filter, -tf: Filtert, um die Bereinigung auf Tabellen zu beschränken, die die angegebene Teilzeichenfolge im Namen enthalten.
- --timing, -tm: Zeigt die Dauer des Clean-up-Prozesses nach Abschluss an.
- --help: Zeigt Hilfsinformationen zum clean-up-Befehl an und beendet das Programm.
  
#### Beispiel
  
Um Daten aus dem Projekt ProjectA zwischen dem 1. Januar 2023 und dem 30. Juni 2023 zu entfernen:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Um Daten nur aus einer bestimmten Tabelle namens Table1 zu entfernen:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Dieser Befehl hilft bei der Verwaltung des Datenbestands und stellt sicher, dass das Repository nur relevante Informationen enthält.

###   inspect

Der Befehl inspect im ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Ampelsystems für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erzeugen. Dieser Befehl unterstützt die Analyse und Überwachung von Daten über einen definierten Zeitraum.

#### Befehlsverwendung

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das Daten inspiziert werden sollen (erforderlich). Wenn Sie das Schlüsselwort all-projects als Argument verwenden, weist das ***digna*** an, über alle vorhandenen Projekte zu iterieren und diesen Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Dateninspektion. Akzeptierte Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Dateninspektion, mit denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen

- --table-name, -tn: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- --table-filter, -tf: Filtert, um nur Tabellen zu inspizieren, die die angegebene Teilzeichenfolge im Namen enthalten.
- --force-profile: Erzwingt die Neuerfassung von Profilen. Standard ist force-profile.
- --no-force-profile: Verhindert die Neuerfassung von Profilen.
- --force-prediction: Erzwingt die Neuberechnung von Vorhersagen. Standard ist force-prediction.
- --no-force-prediction: Verhindert die Neuberechnung von Vorhersagen.
- --force-alert-status: Erzwingt die Neuberechnung von Alert-Status. Standard ist force-alert-status.
- --no-force-alert-status: Verhindert die Neuberechnung von Alert-Status.
- --timing, -tm: Zeigt die Dauer des Inspektionsprozesses nach Abschluss an.
- --alert-notification, -an: Sendet Alarmbenachrichtigungen an abonnierte Kanäle.
  
#### Beispiel
  
Um Daten für das Projekt ProjectA vom 1. Januar 2024 bis zum 31. Januar 2024 zu inspizieren:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Um nur eine bestimmte Tabelle zu inspizieren und die Neuberechnung von Vorhersagen zu erzwingen:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Dieser Befehl ist nützlich, um aktualisierte Profile und Vorhersagen zu erstellen, die Datenintegrität zu überwachen und Alarmsysteme innerhalb eines angegebenen Projektzeitraums zu verwalten.

###   tls-status

Der Befehl tls-status im ***digna*** CLI wird verwendet, um den Status des Ampelsystems (Traffic Light System, TLS) für eine bestimmte Tabelle innerhalb eines Projekts an einem angegebenen Datum abzufragen. Das Ampelsystem liefert Einblicke in die Gesundheit und Qualität der Daten und zeigt etwaige Probleme oder Warnungen an, die Aufmerksamkeit erfordern könnten.
  
#### Befehlsverwendung
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das der TLS-Status abgefragt wird (erforderlich).
- **TABLE_NAME**: Die spezifische Tabelle innerhalb des Projekts, für die der TLS-Status benötigt wird (erforderlich).
- **DATE**: Das Datum, für das der TLS-Status abgefragt wird, typischerweise im Format %Y-%m-%d (erforderlich).
  
#### Beispiel
  
Um den TLS-Status für eine Tabelle namens UserData im Projekt ProjectA am 1. Juli 2024 zu prüfen:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Dieser Befehl hilft Benutzern, die Datenqualität zu überwachen und zu pflegen, indem er einen klaren und umsetzbaren Statusbericht basierend auf vordefinierten Kriterien liefert.

###   list-projects
  
Der Befehl list-projects im ***digna*** CLI zeigt eine Liste aller verfügbaren Projekte im ***digna***-System an.
  
#### Befehlsverwendung
  
bash
dignacli list-projects


Dieser Befehl ist besonders nützlich für Administratoren und Benutzer, die mehrere Projekte verwalten, und bietet eine schnelle Übersicht über die im ***digna***-Repository verfügbaren Projekte.

###   list-ds

Der Befehl list-ds im ***digna*** CLI wird verwendet, um eine Liste aller verfügbaren Datenquellen innerhalb eines angegebenen Projekts anzuzeigen. Dieser Befehl ist nützlich, um die für Analyse und Verwaltung in der ***digna***-Systemumgebung verfügbaren Datenbestände zu verstehen.

#### Befehlsverwendung
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, für das die Datenquellen aufgelistet werden (erforderlich).
  
#### Beispiel
  
Um alle Datenquellen im Projekt mit dem Namen ProjectA aufzulisten:
  
bash
dignacli list-ds ProjectA

  
Dieser Befehl gibt den Benutzern einen Überblick über die im Projekt verfügbaren Datenquellen und hilft ihnen, die Datenlandschaft effektiver zu navigieren und zu verwalten.
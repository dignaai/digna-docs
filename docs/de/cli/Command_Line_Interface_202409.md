---
title: digna CLI Referenz 2024.09 – Befehle & Beispiele | digna Dokumentation
description: Vollständige Referenz für digna CLI Release 2024.09. Erfahren Sie, wie Sie Benutzer, Repositories und Daten mit Befehlen wie add-user, check-repo-connection, upgrade-repo, inspect, tls-status und mehr verwalten.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

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

3.  **Hilfe für bestimmte Befehle abrufen:**  
  
    Für detaillierte Informationen zu einem bestimmten Befehl hängen Sie --help an diesen Befehl an.  
    Zum Beispiel, um Hilfe zum Befehl add-user zu erhalten, führen Sie aus:
     bash
     dignacli add-user --help
     

     ### Ausgabe:
      
     - **Befehlsbeschreibung:** Liefert eine detaillierte Beschreibung dessen, was der Befehl tut.  
     - **Syntax:** Zeigt die exakte Syntax, einschließlich erforderlicher und optionaler Argumente.  
     - **Optionen:** Listet alle dem Befehl spezifischen Optionen mit deren Erklärungen auf.  
     - **Beispiele:** Gibt Beispiele, wie der Befehl effektiv ausgeführt wird.

  
###   check-repo-connection

Der Befehl check-repo-connection ist ein Dienstprogramm im ***digna*** CLI-Tool, das entwickelt wurde, um die Konnektivität und den Zugriff auf ein angegebenes ***digna*** Repository zu testen. Dieser Befehl stellt sicher, dass das CLI mit dem Repository interagieren kann.
      
##### Befehlsverwendung
bash
dignacli check-repo-connection


Nach erfolgreicher Ausführung gibt der Befehl eine Bestätigung der Verbindung aus, zusammen mit Details zum Repository: Repository-Version, Host, Datenbank und Schema.  
  
Wenn die Repository-Verbindung nicht erfolgreich ist, überprüfen Sie die Datei config.toml auf korrekte Konfigurationseinstellungen.

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
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
„verbose“ und „debug“ legen das Detaillierungsniveau fest, während der Schalter „logfile“ die Ausgabe in eine Datei umleitet, anstatt sie in der Konsole anzuzeigen.

## Benutzerverwaltung

###   add-user
  
Der Befehl add-user im ***digna*** CLI wird verwendet, um einen neuen Benutzer im ***digna*** System hinzuzufügen.
  
#### Befehlsverwendung
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumente

- **USER_NAME**: Der Benutzername des neuen Benutzers (erforderlich).
- **USER_FULL_NAME**: Der vollständige Name des neuen Benutzers (erforderlich).
- **USER_PASSWORD**: Das Passwort für den neuen Benutzer (erforderlich).

#### Optionen

- --is_superuser, -su: Kennzeichnet den neuen Benutzer als Administrator.
- --valid_until, -vu: Setzt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS. Wenn nicht gesetzt, hat das Konto kein Ablaufdatum.

#### Beispiel

Um einen neuen Benutzer mit dem Benutzernamen jdoe, dem vollständigen Namen John Doe und dem Passwort password123 hinzuzufügen:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Um einen neuen Benutzer hinzuzufügen und ein Ablaufdatum für das Konto festzulegen:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
Der Befehl delete-user im ***digna*** CLI wird verwendet, um einen vorhandenen Benutzer aus dem ***digna*** System zu entfernen.
  
##### Befehlsverwendung
bash
dignacli delete-user USER_NAME

  
#### Argumente
- **USER_NAME**: Der Benutzername des zu löschenden Benutzers (erforderlich). Dies ist das einzige vom Befehl erforderliche Argument.

#### Beispiel
bash
dignacli delete-user jdoe

  
Durch Ausführen dieses Befehls wird der Benutzer jdoe aus dem ***digna*** System entfernt, sein Zugriff widerrufen und die zugehörigen Daten und Berechtigungen im Repository gelöscht.

###   modify-user

Der Befehl modify-user im ***digna*** CLI wird verwendet, um die Details eines vorhandenen Benutzers im ***digna*** System zu aktualisieren.

##### Befehlsverwendung
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumente
  
- **USER_NAME**: Der Benutzername des zu ändernden Benutzers (erforderlich).
- **USER_FULL_NAME**: Der neue vollständige Name des Benutzers (erforderlich).
  
#### Optionen  
  
- --is_superuser, -su: Setzt den Benutzer als Superuser und gewährt erhöhte Berechtigungen. Dieses Flag benötigt keinen Wert.  
- --valid_until, -vu: Setzt ein Ablaufdatum für das Benutzerkonto im Format YYYY-MM-DD HH:MI:SS. Wenn nicht angegeben, bleibt das Konto unbegrenzt gültig.  
  
#### Beispiel
  
Um den vollständigen Namen des Benutzers jdoe in „Johnathan Doe“ zu ändern und den Benutzer als Superuser festzulegen:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
Der Befehl modify-user-pwd im ***digna*** CLI wird verwendet, um das Passwort eines vorhandenen Benutzers im ***digna*** System zu ändern.
  
##### Befehlsverwendung
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumente
  
- **USER_NAME**: Der Benutzername des Benutzers, dessen Passwort geändert werden soll (erforderlich).
- **USER_PWD**: Das neue Passwort für den Benutzer (erforderlich).
  
#### Beispiel
  
Um das Passwort des Benutzers jdoe in newpassword123 zu ändern:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

Der Befehl list-users im ***digna*** CLI zeigt eine Liste aller im ***digna*** System registrierten Benutzer an.

##### Befehlsverwendung

bash
dignacli list-users


Durch Ausführen dieses Befehls verbindet sich das ***digna*** CLI mit dem ***digna*** Repository und listet alle Benutzer auf, wobei deren ID, Benutzername, vollständiger Name, Superuser-Status und Ablaufzeitstempel angezeigt werden.

# Repository-Verwaltung

###   upgrade-repo
  
Der Befehl upgrade-repo im ***digna*** CLI wird verwendet, um das ***digna*** Repository zu aktualisieren oder zu initialisieren. Dieser Befehl ist wichtig, um Updates anzuwenden oder die Repository-Infrastruktur zum ersten Mal einzurichten.
  
#### Befehlsverwendung

bash
dignacli upgrade-repo [options]

  
#### Optionen
  
- --simulation-mode, -s: Wenn aktiviert, führt diese Option den Befehl im Simulationsmodus aus, wobei die SQL-Anweisungen ausgegeben werden, die ausgeführt würden, jedoch nicht tatsächlich ausgeführt werden. Dies ist nützlich, um Änderungen vorab zu prüfen, ohne das Repository zu verändern.  

  
#### Beispiel
  
Um das ***digna*** Repository zu aktualisieren, können Sie den Befehl ohne Optionen ausführen:
  
bash
dignacli upgrade-repo
  
Um das Upgrade im Simulationsmodus auszuführen (um die SQL-Anweisungen ohne Anwendung zu sehen):
  
bash
dignacli upgrade-repo --simulation-mode

  
Dieser Befehl ist entscheidend für die Wartung des ***digna*** Systems und stellt sicher, dass das Datenbankschema und andere Repository-Komponenten mit der neuesten Softwareversion auf dem aktuellen Stand sind.

###   encrypt
  
Der Befehl encrypt im ***digna*** CLI wird verwendet, um ein Passwort zu verschlüsseln.
  
#### Befehlsverwendung
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumente
- **PASSWORD**: Das zu verschlüsselnde Passwort (erforderlich).
  
#### Beispiel
  
Um ein Passwort zu verschlüsseln, müssen Sie das Passwort als Argument angeben.   
Beispielsweise, um das Passwort mypassword123 zu verschlüsseln, verwenden Sie:
bash
dignacli encrypt mypassword123

Dieser Befehl gibt die verschlüsselte Version des übergebenen Passworts aus, die dann in sicheren Kontexten verwendet werden kann. Wenn das Passwort-Argument nicht angegeben wird, zeigt das CLI einen Fehler an, der auf das fehlende Argument hinweist.

###   generate-key
  
Der Befehl generate-key wird verwendet, um einen Fernet key zu generieren, der für die Sicherung von Passwörtern im ***digna*** Repository erforderlich ist.
  
#### Befehlsverwendung
bash
dignacli generate-key

  
## Datenverwaltung

###   clean-up

Der Befehl clean-up im ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Traffic Light Systems für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu entfernen. Dieser Befehl ist wichtig für das Datenlebenszyklus-Management und hilft, eine organisierte und effiziente Datenumgebung zu erhalten, indem veraltete oder unnötige Daten bereinigt werden.

#### Befehlsverwendung

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, aus dem Daten entfernt werden sollen (erforderlich). Die Verwendung des Schlüsselworts all-projects in diesem Argument weist ***digna*** an, über alle vorhandenen Projekte zu iterieren und diesen Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Datenentfernung. Akzeptierte Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Datenentfernung, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen
  
- --table-name, -tn: Beschränkt die Bereinigung auf eine bestimmte Tabelle innerhalb des Projekts.
- --table-filter, -tf: Filter, um die Bereinigung auf Tabellen zu beschränken, die den angegebenen Teilstring im Namen enthalten.
- --timing, -tm: Zeigt die Dauer des Bereinigungsprozesses nach Abschluss an.
- --help: Zeigt Hilfsinformationen zum clean-up-Befehl an und beendet das Programm.
  
#### Beispiel
  
Um Daten aus dem Projekt ProjectA zwischen dem 1. Januar 2023 und dem 30. Juni 2023 zu entfernen:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Um Daten nur aus einer bestimmten Tabelle mit dem Namen Table1 zu entfernen:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Dieser Befehl hilft beim Management des Datenspeichers und stellt sicher, dass das Repository nur relevante Informationen enthält.

###   inspect

Der Befehl inspect im ***digna*** CLI wird verwendet, um Profile, Vorhersagen und Daten des Traffic Light Systems für eine oder mehrere Datenquellen innerhalb eines angegebenen Projekts zu erstellen. Dieser Befehl unterstützt bei der Analyse und Überwachung von Daten über einen definierten Zeitraum.

#### Befehlsverwendung

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumente
  
- **PROJECT_NAME**: Der Name des Projekts, für das Daten inspiziert werden sollen (erforderlich). Die Verwendung des Schlüsselworts all-projects in diesem Argument weist ***digna*** an, über alle vorhandenen Projekte zu iterieren und diesen Befehl anzuwenden.
- **FROM_DATE**: Das Startdatum und die Startzeit für die Dateninspektion. Akzeptierte Formate sind %Y-%m-%d, %Y-%m-%dT%H:%M:%S oder %Y-%m-%d %H:%M:%S (erforderlich).
- **TO_DATE**: Das Enddatum und die Endzeit für die Dateninspektion, in denselben Formaten wie FROM_DATE (erforderlich).
  
#### Optionen

- --table-name, -tn: Beschränkt die Inspektion auf eine bestimmte Tabelle innerhalb des Projekts.
- --table-filter, -tf: Filter, um nur Tabellen zu inspizieren, die den angegebenen Teilstring im Namen enthalten.
- --force-profile: Erzwingt die Neuerfassung von Profilen. Standard ist force-profile.
- --no-force-profile: Verhindert die Neuerfassung von Profilen.
- --force-prediction: Erzwingt die Neuberechnung von Vorhersagen. Standard ist force-prediction.
- --no-force-prediction: Verhindert die Neuberechnung von Vorhersagen.
- --force-alert-status: Erzwingt die Neuberechnung von Alarmstatus. Standard ist force-alert-status.
- --no-force-alert-status: Verhindert die Neuberechnung von Alarmstatus.
- --timing, -tm: Zeigt die Dauer des Inspektionsprozesses nach Abschluss an.
- --alert-notification, -an: Sendet Alarmbenachrichtigungen an abonnierte Kanäle.
  
#### Beispiel
  
Um Daten für das Projekt ProjectA vom 1. Januar 2024 bis zum 31. Januar 2024 zu inspizieren:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Um nur eine bestimmte Tabelle zu inspizieren und die Neuberechnung von Vorhersagen zu erzwingen:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Dieser Befehl ist nützlich, um aktualisierte Profile und Vorhersagen zu erzeugen, die Datenintegrität zu überwachen und Alarmsysteme innerhalb eines bestimmten Projektzeitraums zu verwalten.

###   tls-status

Der Befehl tls-status im ***digna*** CLI wird verwendet, um den Status des Traffic Light System (TLS) für eine bestimmte Tabelle innerhalb eines Projekts an einem bestimmten Datum abzufragen. Das Traffic Light System bietet Einblicke in die Gesundheit und Qualität der Daten und zeigt eventuelle Probleme oder Alarme, die Aufmerksamkeit erfordern.
  
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


Dieser Befehl hilft Benutzern, die Datenqualität zu überwachen und zu pflegen, indem er einen klaren und handlungsorientierten Statusbericht basierend auf vordefinierten Kriterien liefert.

###   list-projects
  
Der Befehl list-projects im ***digna*** CLI wird verwendet, um eine Liste aller verfügbaren Projekte im ***digna*** System anzuzeigen.
  
#### Befehlsverwendung
  
bash
dignacli list-projects


Dieser Befehl ist besonders nützlich für Administratoren und Benutzer, die mehrere Projekte verwalten, und bietet einen schnellen Überblick über die verfügbaren Projekte im ***digna*** Repository.

###   list-ds

Der Befehl list-ds im ***digna*** CLI wird verwendet, um eine Liste aller verfügbaren Datenquellen innerhalb eines angegebenen Projekts anzuzeigen. Dieser Befehl ist nützlich, um die verfügbaren Datenressourcen für Analyse und Verwaltung im ***digna*** System zu erfassen.

#### Befehlsverwendung
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumente
- **PROJECT_NAME**: Der Name des Projekts, für das die Datenquellen aufgelistet werden (erforderlich).
  
#### Beispiel
  
Um alle Datenquellen im Projekt mit dem Namen ProjectA aufzulisten:
  
bash
dignacli list-ds ProjectA

  
Dieser Befehl gibt Benutzern einen Überblick über die im Projekt verfügbaren Datenquellen und erleichtert die Navigation und Verwaltung der Datenlandschaft.
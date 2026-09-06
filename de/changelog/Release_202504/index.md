# Änderungsprotokoll – Release 2025.04

Mit Release 2025.04 macht digna einen großen Schritt nach vorn, um Datenqualität und Observability einfacher zu verwalten, für Teams transparenter zu machen und Nutzern weltweit zugänglich zu machen.  
Dieses Release kombiniert **leistungsstarke neue Funktionen**, **Verbesserungen der Workflow-Automatisierung** und **Feinheiten in der Benutzererfahrung**.  

---

## Neue Funktionen

### Inspection Hub – Ein neues Steuerzentrum
Das **Inspection Hub** ist jetzt als zentraler Ort verfügbar, um alle Ihre Inspektions-Jobs zu verwalten. Anstatt zwischen verschiedenen Modulen hin- und herzuspringen oder ausschließlich auf die Ausführung über die Kommandozeile angewiesen zu sein, können Sie Ihre Inspektionen jetzt in einer schlanken Oberfläche überwachen und steuern.  

Wesentliche Funktionen umfassen:  
- On-Demand-Inspektionen: Starten Sie neue Jobs sofort, wann immer Sie aktuelle Ergebnisse benötigen.  
- Inspektionsverlauf: Sehen Sie eine Zeitachse der Inspektionen — was ausgeführt wurde, wer sie ausgelöst hat und wann.  
- Statusverfolgung: Jobs sind klar als abgeschlossen, in Bearbeitung oder ausstehend markiert.  
- Invoker-Einblicke: Prüfen Sie schnell, ob eine Inspektion von einem Benutzer, dem Scheduler oder der CLI ausgelöst wurde.  
- Aufräum-Tools: Löschen Sie veraltete oder unnötige Jobs, um Ihren Arbeitsbereich übersichtlich zu halten.  
- Detaillierte Logs: Tauchen Sie in jeden Job ein, um zu sehen, wie lange er gedauert hat, welche Quellen eingeschlossen wurden und wie Schwellenwerte angewendet wurden.  

Das Inspection Hub bietet Teams **End-to-End-Sichtbarkeit und Kontrolle** und macht Inspektionen über große Projekte hinweg leichter handhabbar.  

---

### Mehrsprachige Unterstützung – digna spricht Ihre Sprache
digna ist jetzt bereit für internationale Teams mit der Einführung der **Mehrsprachigkeit**.  

In diesem Release können Sie Ihre **bevorzugte Interface-Sprache** direkt in den Benutzereinstellungen festlegen. Unterstützte Sprachen sind:  
- Englisch (UK, US, CA, AU)  
- Deutsch (DE, AT, CH)  
- Polnisch (PL)  

Das macht digna für mehrsprachige Organisationen leichter nutzbar und verbessert die Akzeptanz in Teams, die in verschiedenen Regionen arbeiten. Weitere Sprachen werden in kommenden Releases hinzugefügt.  

---

### Import & Export von Datenquellen – Konfiguration leicht gemacht
Konsistenz über Umgebungen hinweg ist essenziell in Unternehmensbereitstellungen. Mit 2025.04 führt digna den **Import/Export von Datenquellen** über **dignacli** ein, das Kommandozeilenwerkzeug für fortgeschrittene Anwender.  

Vorteile:  
- Exportieren Sie eine Datenquellenkonfiguration einmal und verwenden Sie sie wieder in Development, Test und Production.  
- Vermeiden Sie manuelle Neukonfigurationen und teure Fehler.  
- Unterstützen Sie automatisierte Workflows und CI/CD-Pipelines mit einfachen CLI-Befehlen (`export-ds` und `import-ds`).  
- Kopieren Sie Datenquellen schnell zwischen Projekten für einfachere Zusammenarbeit.  

Diese Funktion stellt sicher, dass Teams mit Vertrauen bereitstellen können, da Konfigurationen in jeder Umgebung konsistent sind.  

---

### Module Analytics (v1) – Von der Erkennung zum Verständnis
digna begann als Plattform für Anomalieerkennung und Überwachung der Datenqualität. Mit Release 2025.04 entwickelt es sich weiter mit der **ersten Version von Module Analytics**.  

Module Analytics hilft Nutzern dabei, ihre **Daten zu verstehen** statt nur auf Probleme zu reagieren. Mit diesem neuen Modul können Sie:  
- Langfristige Trends in Ihren Datensätzen verfolgen.  
- Volatilität erkennen und überwachen, um Schwankungen zu verstehen.  
- Das Verhalten von Daten über die Zeit erkunden, um tieferen Kontext zu erhalten.  

Zum Beispiel kann digna automatisch hervorheben, dass *„Die Zeilenanzahl seit Jahresbeginn um 15,8 % gestiegen ist.“*  
Keine SQL-Abfragen, keine manuellen Prüfungen — nur **umsetzbare Erkenntnisse auf einen Blick**.  

Dies bildet die Grundlage für dignas Weg hin zu fortgeschrittener Datenanalyse und ermöglicht es Datenteams, von reaktiver zu proaktiver Überwachung zu wechseln.  

---

### Dashboard-Verbesserungen – Eine reibungslosere Benutzererfahrung
Neben den großen Funktionen enthält Release 2025.04 mehrere **Feinheiten am Dashboard**, die darauf abzielen, digna intuitiver und angenehmer zu machen:  
- Schnellere Navigation zwischen Projekten und Inspektionen.  
- Ein klareres Layout für Inspektions-Logs und Job-Einreichungen.  
- Dezente Designanpassungen, die Ihnen helfen, Erkenntnisse schneller zu finden.  

Diese Verbesserungen basieren direkt auf Kundenfeedback und zeigen unser fortlaufendes Engagement, digna **zu einer Plattform für den täglichen Gebrauch** zu machen.  

---

## Allgemeine Verbesserungen
- Performance-Optimierungen für Inspektions-Jobs über große Datensätze.  
- Verbesserte Fehlerbehandlung in dignacli, um klareres Feedback zu geben.  
- Stabilitätsverbesserungen für Projekte mit vielen gleichzeitigen Jobs.  
- UI-Feinheiten für das Filtern von Job-Logs und Projektmanagement.  

---

## Zusammenfassung
Release 2025.04 dreht sich um **Kontrolle, Zugänglichkeit und Erkenntnis**.  

- Das neue **Inspection Hub** bietet Nutzern volle Sichtbarkeit über Inspektions-Jobs.  
- **Mehrsprachige Unterstützung** sorgt dafür, dass digna in globalen Teams nutzbar ist.  
- **Import/Export-Funktionalität** vereinfacht das Konfigurationsmanagement über Umgebungen hinweg.  
- **Module Analytics (v1)** verlagert den Fokus von Erkennung zu Verständnis, mit Trend- und Volatilitätsverfolgung.  
- **Dashboard-Verbesserungen** verfeinern das Gesamtbenutzererlebnis.  

Zusammen machen diese Updates digna leistungsfähiger, benutzerfreundlicher und international einsatzbereit wie nie zuvor.
---
title: digna Release 2025.04 | Inspection Hub, Mehrsprachigkeit, Module Analytics
description: Erfahren Sie, was neu ist in digna Release 2025.04. Diese Version führt den Inspection Hub ein, Mehrsprachigkeit (Englisch, Deutsch, Polnisch), den Import/Export von Datenquellen via dignacli, die erste Version von Module Analytics und ein verbessertes Dashboard-Erlebnis.
keywords: digna Release 2025.04, digna Änderungsprotokoll, digna Inspection Hub, digna Mehrsprachigkeit, digna Module Analytics, digna Import Export, digna CLI, Versionshinweise, Datenbeobachtbarkeit, Überwachung der Datenqualität
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Changelog – Release 2025.04

Mit Release 2025.04 macht digna einen großen Schritt, um Datenqualität und Observability einfacher zu verwalten, für Teams transparenter zu machen und weltweit zugänglich zu gestalten.  
Dieses Release kombiniert **starke neue Funktionen**, **Verbesserungen der Workflow-Automatisierung** und **Optimierungen der Benutzererfahrung**.  

---

## Neue Funktionen

### Inspection Hub – Ein neues Kommandozentrum
Der **Inspection Hub** ist jetzt als zentraler Ort verfügbar, um alle Ihre Inspection-Jobs zu verwalten. Statt zwischen verschiedenen Modulen zu wechseln oder ausschließlich auf die Kommandozeile angewiesen zu sein, können Sie Ihre Inspektionen jetzt von einer schlanken Oberfläche aus überwachen und steuern.  

Wesentliche Funktionen umfassen:  
- On-Demand-Inspektionen: Starten Sie neue Jobs sofort, wenn Sie frische Ergebnisse benötigen.  
- Inspektionshistorie: Sehen Sie eine Timeline der Inspektionen — was ausgeführt wurde, wer sie ausgelöst hat und wann.  
- Status-Tracking: Jobs sind klar als abgeschlossen, in Bearbeitung oder ausstehend gekennzeichnet.  
- Invoker-Insights: Prüfen Sie schnell, ob eine Inspektion von einem Benutzer, Scheduler oder der CLI ausgelöst wurde.  
- Aufräumwerkzeuge: Löschen Sie veraltete oder unnötige Jobs, um Ihren Arbeitsbereich übersichtlich zu halten.  
- Detaillierte Logs: Tauchen Sie in jeden Job ein, um Laufzeiten, eingeschlossene Quellen und angewendete Schwellenwerte zu sehen.  

Der Inspection Hub bietet Teams **End-to-End-Transparenz und Kontrolle** und erleichtert das Management von Inspektionen in großen Projekten.  

---

### Mehrsprachigkeit – digna spricht Ihre Sprache
digna ist jetzt bereit für internationale Teams durch die Einführung der **Mehrsprachigkeit**.  

In diesem Release können Sie Ihre **bevorzugte Schnittstellensprache** direkt in den User Preferences einstellen. Unterstützte Sprachen sind:  
- Englisch (UK, US, CA, AU)  
- Deutsch (DE, AT, CH)  
- Polnisch (PL)  

Das macht digna für mehrsprachige Organisationen einfacher nutzbar und sorgt für eine reibungslosere Einführung in Teams, die in verschiedenen Regionen arbeiten. Weitere Sprachen werden in kommenden Releases ergänzt.  

---

### Import & Export von Datenquellen – Konfiguration einfach gemacht
Konsistenz über Umgebungen hinweg ist in Unternehmensumgebungen entscheidend. Mit 2025.04 führt digna den **Import/Export von Datenquellen** via **dignacli** ein, dem Kommandozeilen-Tool für fortgeschrittene Nutzer.  

Vorteile:  
- Exportieren Sie eine Datenquellenkonfiguration einmal und verwenden Sie sie in Development, Test und Production wieder.  
- Eliminieren Sie manuelle Neukonfigurationen und vermeiden Sie kostspielige Fehler.  
- Unterstützen Sie automatisierte Workflows und CI/CD-Pipelines mit einfachen CLI-Befehlen (`export-ds` und `import-ds`).  
- Kopieren Sie Datenquellen schnell zwischen Projekten für einfachere Zusammenarbeit.  

Diese Funktionalität stellt sicher, dass Teams mit Vertrauen deployen können, da Konfigurationen in jeder Umgebung konsistent sind.  

---

### Module Analytics (v1) – Vom Erkennen zum Verstehen
digna begann als Plattform zur Anomalieerkennung und Überwachung der Datenqualität. Mit Release 2025.04 entwickelt es sich weiter durch die **erste Version von Module Analytics**.  

Module Analytics hilft Nutzern, ihre Daten **zu verstehen** statt nur auf Probleme zu reagieren. Mit diesem neuen Modul können Sie:  
- Langfristige Trends in Ihren Datensätzen verfolgen.  
- Volatilität erkennen und überwachen, um Schwankungen besser zu verstehen.  
- Das Verhalten von Daten über die Zeit explorativ untersuchen, um tieferen Kontext zu gewinnen.  

Beispielsweise kann digna automatisch hervorheben, dass „die Zeilenanzahl seit Jahresbeginn um 15,8 % gestiegen ist.“  
Keine SQL-Abfragen, keine manuellen Prüfungen — nur **handlungsfähige Erkenntnisse auf einen Blick**.  

Dies ist die Grundlage von dignas Weiterentwicklung zu fortgeschrittener Datenanalyse, die Data-Teams ermöglicht, von reaktivem zu proaktivem Monitoring zu wechseln.  

---

### Dashboard-Verbesserungen – Eine flüssigere Benutzererfahrung
Neben den großen Features enthält Release 2025.04 mehrere **Feinabstimmungen am Dashboard**, die digna intuitiver und angenehmer machen:  
- Schnellere Navigation zwischen Projekten und Inspektionen.  
- Ein aufgeräumteres Layout für Inspektionslogs und Job-Submissions.  
- Dezente Designanpassungen, die helfen, Erkenntnisse schneller zu finden.  

Diese Verbesserungen basieren direkt auf Kundenfeedback und zeigen unser fortwährendes Engagement, digna **als Plattform für den täglichen Einsatz** zu gestalten.  

---

## Allgemeine Verbesserungen
- Performance-Optimierungen für Inspektionsjobs über große Datensätze.  
- Verbesserte Fehlerbehandlung in dignacli zur klareren Rückmeldung.  
- Stabilitätsverbesserungen für Projekte mit vielen gleichzeitigen Jobs.  
- UI-Verfeinerungen für Job-Log-Filterung und Projektverwaltung.  

---

## Zusammenfassung
Release 2025.04 steht für **Kontrolle, Zugänglichkeit und Erkenntnis**.  

- Der neue **Inspection Hub** bietet Nutzern volle Sichtbarkeit über Inspektionsjobs.  
- **Mehrsprachigkeit** stellt sicher, dass digna in globalen Teams eingesetzt werden kann.  
- Die **Import/Export-Funktion** vereinfacht das Konfigurationsmanagement über Umgebungen hinweg.  
- **Module Analytics (v1)** verlagert den Fokus vom Erkennen zum Verstehen, mit Trend- und Volatilitätsverfolgung.  
- **Dashboard-Verbesserungen** verfeinern das Gesamterlebnis.  

Gemeinsam machen diese Updates digna leistungsfähiger, benutzerfreundlicher und international einsatzbereiter als je zuvor.
---
title: digna Release 2026.11 | Data Reconciliation (Beta), digna Agentic (Beta) & digna Engine
description: Erfahren Sie, was neu ist in digna Release 2026.11. Diese Version bringt drei große Neuerungen - digna Data Reconciliation (Beta), digna Agentic (Beta) mit dem digna MCP Server sowie die digna Engine, die Prüfungen der referenziellen Integrität zwischen unterschiedlichen Datenbanktechnologien ermöglicht.
keywords: digna Release 2026.11, digna Änderungsprotokoll, digna Data Reconciliation, Datenabgleich, ETL-Validierung, Abgleich von Quelle und Ziel, digna Agentic, digna MCP Server, KI-Agenten Datenqualität, digna Engine, verbindungsübergreifende referenzielle Integrität, Query-Attribute, Datenprofiling, Data Observability
image: /assets/logo_square.png
---

# Änderungsprotokoll – Release 2026.11  

Release 2026.11 steht im Zeichen von drei großen Neuerungen:

- **digna Data Reconciliation (Beta)**: prüft, ob Daten konsistent bleiben, während sie zwischen Systemen übertragen werden  
- **digna Agentic (Beta)**: öffnet digna über den digna MCP Server für KI-Agenten  
- **digna Engine**: profiliert Daten optional innerhalb von digna und ermöglicht Prüfungen der referenziellen Integrität zwischen unterschiedlichen Datenbanktechnologien  

---

## Neue Funktionen  

### digna Data Reconciliation (Beta) – Konsistenz von der Quelle bis zum Ziel  
Daten durchlaufen oft mehrere Systeme, bevor sie in einem Bericht ankommen. digna Data Reconciliation (Beta) vergleicht eine **Ziel**-Datenquelle mit den **Quellen**, aus denen sie erstellt wurde, und alarmiert, sobald diese nicht mehr übereinstimmen.

- Konfiguriert als benannte Regeln auf dem neuen Tab **Data Reconciliation** der Ziel-Datenquelle  
- Jede Datenquelle des Projekts mit eingeschalteter Data Reconciliation kann als Quelle dienen  
- Zu den Anwendungsfällen gehören standardisierte Abstimmungsverfahren und die Validierung der Ergebnisse von ETL-Prozessen  
- Zwei Regeltypen: **Exakt** und **KI**  

**Exakt-Regeln – Abgleich als Datenqualitätsregel**: Sie legen genau fest, was zwischen einer Quelle und einem Ziel übereinstimmen muss, wie bei einer Datenqualitätsregel.

  - Eine Quell-Datenquelle mit einer Ziel-Datenquelle vergleichen  
  - Eine Zielprüfung anhand von Statistik und Attribut mit einer Quellprüfung koppeln, z. B. Zeilenanzahl oder die Summe einer Betragsspalte  
  - Eine Abweichung mit einer Toleranz vom Typ **Absolut** (z. B. ± 10) oder **Relativ** (z. B. ± 0,5 % der Quelle) zulassen  
  - Die Zeitleiste zeigt die Differenz jedes Tages im Verhältnis zur Toleranz  

**KI-Regeln – Abgleich als Data Observability**: digna lernt, wie ein Ziel seinen Quellen folgt – so wie digna Daten in anderen Modulen beobachtet – und alarmiert, wenn diese Beziehung bricht.

  - Prüfungen mehrerer Quell-Datenquellen mit den Prüfungen eines Ziels kombinieren  
  - Die Logik dazwischen (Joins, Filter, Aggregationen) müssen Sie weder kennen noch aufschreiben  
  - Ein Modell lernt aus der Historie, wie das Ziel seinen Quellen am selben Tag folgt  
  - Jede Zielprüfung wird aus den Quellwerten des Tages vorhergesagt, und digna alarmiert, wenn das Ziel das Band der bisherigen Fehler dieser Regel verlässt  
  - Jede Regel hat eigene **Modelleinstellungen**: **Empfindlichkeit**, **Gedächtnis** und **Modellkomplexität**  

Abgleichsprüfungen erscheinen auf dem Dashboard mit einer Zeitleiste pro Regel. Sie fließen in den Gesamtstatus der Inspektion ein und lösen Benachrichtigungen aus.

**Auswirkung:** Deckt beide Seiten des Datenabgleichs ab. Exakt-Regeln setzen bekannte Kontrollen zwischen Quelle und Ziel durch, und KI-Regeln überwachen komplexe Datenflüsse wie ETL-Prozesse. So werden unterwegs verlorene oder veränderte Daten erkannt, ohne handgeschriebenes Abgleichs-SQL.

---

### digna Agentic (Beta) – digna für KI-Agenten  
Die erste Version von digna Agentic (Beta). KI-Agenten können jetzt mit digna arbeiten, Geschäftsfragen zu Ihren Daten beantworten und Ihnen helfen, Ihre Konfiguration zu verbessern.

**digna MCP Server**: Ermöglicht Claude und anderen KI-Agenten, über das Model Context Protocol mit digna zu arbeiten.

  - Projekte, Datenquellen, Regeln, Inspektionszeitpläne und Subscriptions verwalten  
  - Inspektionsstatus bis hinunter zur einzelnen Prüfung lesen, um Alarme zu untersuchen  

**Beschreibungen für Datenquellen und Attribute**: Beschreiben Sie in einfacher Sprache, was eine Datenquelle oder ein Attribut enthält.

  - KI-Agenten nutzen die Beschreibungen, um Ihre Daten zu interpretieren  
  - Stellen Sie Geschäftsfragen zu Ihren Daten, und KI-Agenten beantworten sie auf Basis dessen, was digna überwacht  
  - Kann die aktuelle Konfiguration von digna eine Frage nicht beantworten, schlägt der KI-Agent nach Möglichkeit Änderungen an der Datenquelle und ihren Attributen vor, z. B. ein neues Datenset  

**Auswirkung:** Sie können Geschäftsfragen zu Ihren Daten in einfacher Sprache stellen, und KI-Agenten helfen dabei, digna zu konfigurieren und Datenqualitätsprobleme zu untersuchen.

---

### digna Engine – Profiling dort, wo Sie es wählen  
Standardmäßig profiliert digna Daten dort, wo sie liegen: in der Quelldatenbank. Die digna Engine bietet eine zusätzliche Option: digna exportiert die Daten aus der Quelle und profiliert sie innerhalb der digna Engine.

- Optional, nicht verpflichtend: Das Profiling in der Quelldatenbank bleibt verfügbar  
- Pro Datenbankverbindung als **Profiling-Ort** wählbar: **Quelldatenbank** oder **digna Engine**  
- Für jede unterstützte Quelltechnologie verfügbar  

**Verbindungsübergreifende referenzielle Integrität**: Manche Prüfungen erfordern einen Export der Daten. Die digna Engine erweitert **digna Data Validation** für diese Fälle.

  - **Prüfungen der referenziellen Integrität** zwischen Datenquellen auf **unterschiedlichen Datenbankverbindungen**, auch über verschiedene Datenbanktechnologien hinweg (z. B. Oracle und PostgreSQL)  
  - Funktioniert mit beiden Profiling-Orten: Bei der Quelldatenbank werden nur die Schlüsselspalten in die digna Engine exportiert  
  - Das Dashboard zeigt an, wenn eine Prüfung über zwei Verbindungen läuft  

**Auswirkung:** Sie wählen, wo Daten profiliert werden, und setzen Beziehungen zwischen Systemen durch, die auf unterschiedlichen Datenbanktechnologien laufen.

---

## Profiling-Verbesserungen  

Dieses Release gibt Nutzern außerdem mehr Kontrolle darüber, was und wie profiliert wird.

### Query-Attribute – Benutzerdefinierte Spalten  
- Künstliche Spalten definieren: ein SQL-Ausdruck über eine oder mehrere Spalten der Datenquelle  
- Jedes Query-Attribut hat einen eigenen Namen  
- Wird wie jedes andere Attribut profiliert und geprüft  

### Spaltenkategorie DATE  
- Neue Kategorie **Datum** für Attribute  
- Metriken relativ zum inspizierten Datum  

### Profiling auf Abruf  
- Beliebige Attribute gegen den vollständigen Snapshot eines Datums profilieren, ohne eine Inspektion auszuführen  
- Hilft beim Festlegen des Spaltentyps eines Attributs: **Numerisch**, **Kategorisch**, **Datum** oder **Unspezifiziert**  

---

## Wer profitiert von dieser Version  

- **Data Engineers:** Validierung von ETL-Ergebnissen mit digna Data Reconciliation (Beta)  
- **Finanz-, Risiko- & Controlling-Teams:** Standardisierte Abstimmungsverfahren als Exakt-Regeln in digna Data Reconciliation (Beta)  
- **Data-Quality- & Governance-Teams:** Referenzielle Integrität über Datenbanktechnologien hinweg mit der digna Engine  
- **Fachanwender:** Geschäftsfragen zu Daten, beantwortet von KI-Agenten mit digna Agentic (Beta)  
- **KI- & Automatisierungsteams:** KI-Agenten, die über digna Agentic (Beta) mit digna arbeiten  

---

## CLI-Aktualisierungen  
- Keine Änderungen  

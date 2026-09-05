---
title: digna Data Anomalies | KI-gestützte Observability von Daten
description: digna Data Anomalies ist Teil der digna Data Observability Platform. Es lernt automatisch Muster in Ihren Daten und erkennt Anomalien, um die Datenqualität und Observability in Datenbanken, Data Lakes und Warehouses zu verbessern.
tags:
  - Datenqualität
  - Daten-Observability
  - Qualität von Daten
  - Observability von Daten
  - KI-basierte Überwachung
  - Anomalieerkennung
  - digna
  - digna Plattform
hide:
  - toc                # optional: hide the small top-level TOC if you use inline nav
  - navigation         # optional: hide side navigation for standalone pages
image: /assets/logo_square.png
---


# digna Data Anomalies – KI-basierte Erkennung von Datenqualitätsproblemen

**KI-gestützte Observability für durchgängiges Vertrauen in Daten**

digna Data Anomalies ist Teil der **digna Data Observability Platform** — einer modularen Lösung, die die **Datenqualität** verbessert, indem sie kontinuierlich analysiert, wie sich Datensätze im Zeitverlauf verhalten.

Es lernt automatisch, wie „normal“ Ihre Daten sind, und alarmiert, wenn sich das Verhalten ändert — ohne statische Schwellwerte zu definieren oder eine einzige Regel zu schreiben.  
Das Modul läuft direkt in Ihrer Datenbank, sodass Daten Ihre Umgebung niemals verlassen.

---

## Zweck von digna Data Anomalies

Das **digna Data Anomalies**-Modul bietet kontinuierliche **Observability von Daten**, indem es vordefinierte statistische Metriken berechnet und verfolgt, wie zum Beispiel:

- Datenvolumen und Anzahl der Datensätze  
- Anteile fehlender Werte  
- Wertverteilungen und Histogramme  
- Numerische Bereiche und Mittelwerte  
- Spalteneindeutigkeit und Textlängen  

Diese Metriken werden automatisch für jeden Datensatz erhoben.  
Auf Basis dieser Metriken baut digna Modelle auf, die das typische Verhalten jeder Metrik abbilden — und lernt dabei tägliche, wöchentliche oder saisonale Muster.  
Nach dem Training sagt das Modul erwartete Werte für neue Daten voraus und erkennt Abweichungen, die auf Qualitätsprobleme, Prozessfehler oder Änderungen in vorgelagerten Systemen hindeuten können.

---

## Wichtige Funktionen

- Lernt erwartetes Datenverhalten automatisch mit KI — keine Konfiguration von Schwellenwerten.  
- Erkennt plötzliche Einbrüche, Spitzen oder Drift bei Datenmengen und Verteilungen.  
- Identifiziert vertauschte Spalten oder falsche Zuordnungen zwischen Attributen.  
- Markiert unerwartete Kategorienwerte (z. B. neue Regionen oder Codes).  
- Unterstützt alle Spaltentypen: numerisch, kategorial oder unbestimmt.  
- Arbeitet vollständig in der Kundenumgebung — keine Datenübertragung.  
- Integriert sich mit **digna Data Analytics** für langfristige Trendanalysen.

---

## Funktionsweise

### Schritt 1 – Metrikberechnung
digna berechnet eine Reihe von Profilmetriken für jede Tabelle und Spalte.  
Diese Metriken beschreiben die Struktur und das statistische Verhalten Ihrer Daten und werden zur weiteren Analyse gespeichert.

### Schritt 2 – Modelltraining
Basierend auf historischen Metrikwerten trainiert digna kompakte Machine-Learning-Modelle (Signature-Modelle), die den normalen Bereich jeder Metrik erfassen.

### Schritt 3 – Automatische Schwellenwertbildung
Mittels *conformal inference* berechnet digna adaptive Konfidenzintervalle (Auto-Schwellenwerte), die sich mit Ihren Daten weiterentwickeln.  
Fallen neue Metrikwerte außerhalb des vorhergesagten Bereichs, werden sie als Anomalien markiert.

Diese kontinuierliche Rückkopplung stellt sicher, dass das Monitoring auch dann relevant bleibt, wenn Datenmengen oder Muster natürlicherweise wachsen.

---

## Beispiel-Szenarien

### Unerwarteter Einbruch im Datensatzvolumen
Ein Datensatz enthält typischerweise etwa 500 000 Datensätze pro Tag.  
Wenn eine neue Lieferung nur 50 000 Datensätze umfasst, markiert digna eine Anomalie und zeigt, wie stark der Wert von seinem gelernten Bereich abweicht.

### Erkennung vertauschter Spalten
Die durchschnittliche Stringlänge von `last_name` stimmt plötzlich mit der von `first_name` überein.  
digna erkennt die Abweichung in den Metrikmustern und signalisiert einen möglichen Spaltentausch.

### Unerwartete Kategorie entdeckt
Eine Spalte mit österreichischen Städten enthält plötzlich „Zurich“.  
Auf Basis historischer Verteilungen kennzeichnet digna diesen neuen Wert als unerwartet und alarmiert den Anwender.

---

## Integration mit anderen Modulen

- **digna Data Analytics** — aggregiert Anomaliehistorie und Volatilitätsmetriken, um Langfristtrends sichtbar zu machen.  
- **digna Data Validation** — erzwingt explizite Geschäftsregeln für deterministische Qualitätsprüfungen.  
- **digna Data Timeliness** — überwacht Ankunftszeiten von Daten und korreliert Verzögerungen mit Anomalieereignissen.  
- **digna Data Schema Tracker** — erkennt strukturelle Änderungen, die neue Anomalien erklären könnten.

---

## Typische Anwendungsfälle

- Erkennung fehlender oder doppelter Datenladungen.  
- Identifikation vertauschter oder abgeschnittener Spalten.  
- Erkennung von Verteilungsdrift bei numerischen oder kategorialen Merkmalen.  
- Auffinden unerwarteter Referenzwerte oder Codes.  
- Überwachung kontinuierlicher Ingest-Pipelines auf Unregelmäßigkeiten.  
- Verfolgung der gesamten **Datenqualität und Observability von Daten** über Domänen hinweg.

---

## Vorteile

- Sofortige Erkennung abnormalen Datenverhaltens.  
- Eliminierung manueller Schwellenwertanpassungen.  
- Reduktion des operativen Aufwands in großen Datenumgebungen.  
- Stärkung des Vertrauens in Analyse- und Berichtssysteme.  
- Erhöhung der **Datenqualität** und der durchgängigen **Datenobservability**.

---

## Verwandte digna-Module

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — Trend- und Volatilitätsmetriken.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — regelbasierte Datenverifikation.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — Überwachung von Datenlieferplänen.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — Erkennung von Schemaänderungen.

---

## Zusammenfassung

Das **digna Data Anomalies**-Modul bildet den Kern der KI-getriebenen **Data Observability Platform** von digna.  
Durch kontinuierliches Monitoring wichtiger Metriken, Musterlernen und Identifikation von Abweichungen hilft es Organisationen sicherzustellen, dass die **Datenqualität** vertrauenswürdig, stabil und erklärbar bleibt — ganz ohne manuelle Konfiguration.
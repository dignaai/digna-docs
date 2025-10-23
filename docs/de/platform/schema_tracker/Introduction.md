---
title: Data Schema Tracker – Schema-Evolution überwachen | digna Dokumentation
description: Erfahren Sie, wie digna Data Schema Tracker Spaltenänderungen, Datentypänderungen und schema drift überwacht. Erhalten Sie Warnungen bei absichtlichen und unbeabsichtigten Änderungen, um ETL-Ausfälle und Dashboard-Fehler zu verhindern.
---

# Data Schema Tracker – Schema-Evolution überwachen

## Zweck
Schema-Evolution verfolgen und Warnungen auslösen.

## Technische Funktionen
- Überwacht:
  - Hinzugefügte oder entfernte Spalten
  - Datentypänderungen
- Löst Warnungen bei absichtlichen und unbeabsichtigten Schemaänderungen  
- Verhindert **silent schema drift**, der ETL-Pipelines oder Dashboards unterbrechen kann  

## Beispielanwendungsfälle
- Identifizieren von Datentypänderungen (z. B. `INT` → `VARCHAR`), die nachgelagerte Fehler verursachen können  
- Alarmierung von Data Engineers, bevor Pipelines aufgrund von Schemaabweichungen fehlschlagen  

## Nutzen
Hilft Teams, **schnelllebige, sich entwickelnde Datensätze** unter Kontrolle zu halten.
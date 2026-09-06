# Data Anomalies – Automatisierte Erkennung

---

## Zweck

Das **Data Anomalies**-Modul identifiziert Unregelmäßigkeiten in Ihren Datensätzen automatisch — ganz ohne Regeldefinition.  
Es überwacht kontinuierlich **die Qualität der Datenlieferung** und lernt, wie „normal“ aussieht, um Abweichungen in Echtzeit zu erkennen.

Durch KI-basierte Erkennung erkennt digna stille Datenfehler wie fehlende, duplizierte oder beschädigte Datensätze, die Berichte, ML-Modelle und Dashboards verfälschen können.

---

## Technischer Überblick

### Analysierte Metriken

digna profiliert kontinuierlich die folgenden Aspekte Ihrer Daten:

- **Record volume** – Gesamtanzahl der Zeilen, täglich oder batch-basiert  
- **Missing values** – Erkennung von Null- oder leeren Feldern  
- **Distributions and histograms** – Überwachung von Formänderungen in Daten  
- **Value ranges** – automatische Identifikation von außerhalb liegenden oder extremen Werten  
- **Uniqueness** – Prüfungen auf doppelte Schlüssel oder wiederholte Einträge  

### Intelligente Anomalieerkennung

- Nutzt **historisches Lernen**, um erwartete Grenzen dynamisch zu definieren  
- Erkennt Abweichungen in **Volumen, Wertverteilungen oder logischen Beziehungen**  
- Setzt KI ein, um Schwellenwerte automatisch an Tageszeiten oder saisonale Muster anzupassen  
- Unterscheidet zwischen **statistischen Schwankungen** und echten Anomalien  
- Liefert detaillierte Metriken und Konfidenzwerte pro Dataset und Spalte  

---

## Erkennungsszenarien

Nachfolgend Beispiele für reale Probleme, die vom **Data Anomalies**-Modul automatisch erkannt werden:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | Fehlende Hälfte der täglichen Transaktionen, doppelte Batch-Ladevorgänge oder plötzliche Datenanstiege |
| **Missing or null values** | Datenauszüge abgeschlossen, aber kritische Spalten bleiben leer |
| **Distribution drifts** | Durchschnittlicher Kaufbetrag oder Transaktionsanzahl pro Region ändert sich unerwartet |
| **Column swaps** | Spalten wie *first_name* und *last_name* wurden während des ETL versehentlich vertauscht |
| **Unexpected categorical values** | z. B. erscheint „Zurich“ in der österreichischen Städtegruppe |
| **Sudden uniqueness loss** | Zuvor eindeutige IDs duplizieren sich plötzlich wegen fehlerhafter Upstream-Joins |

---

## Architektur und Ausführung

- **In-database execution:** Die gesamte Anomalieerkennungslogik wird *im Datenbank-Engine* (Teradata, Snowflake, Databricks, PostgreSQL, etc.) ausgeführt  
- **No data movement:** digna liest nur Metriken und überträgt niemals Rohdaten extern  
- **Incremental updates:** Es werden nur neue Datensegmente pro Lauf analysiert, um effizient zu bleiben  
- **Configurable inspection frequency:** Stündlich, täglich oder ausgelöst durch Upstream-Prozesse  
- **Result storage:** Metriken und Anomalie-Flags werden zurück in digna’s Observability-Schema geschrieben zur Visualisierung und Alarmierung  

---

## Vorteile

| Area | Benefit |
|------|----------|
| **Automation** | Eliminierung von hunderten manueller SQL- oder Regeldefinitionen |
| **Precision** | Erkennt Probleme, die statische Schwellenwerte oft übersehen |
| **Scalability** | Überwacht Millionen von Datensätzen pro Tabelle effizient |
| **Integration** | Arbeitet nahtlos mit *digna Data Analytics* für Trendanalysen zusammen |
| **Compliance** | Sichert die kontinuierliche Kontrolle über die **Qualität und Beobachtbarkeit von Daten** |
| **Transparency** | Bietet Konfidenzwerte, Zeitstempel und Begründungscodes für jede Anomalie |

---

## Wie digna „Normal“ lernt

1. **Profiling-Phase:** digna sammelt Metriken aus historischen Datensätzen.  
2. **Lernphase:** KI-Modelle identifizieren wiederkehrende Muster (saisonal, wöchentlich, täglich).  
3. **Monitoring-Phase:** Zukünftige Datensätze werden gegen dynamisch gelernte Schwellenwerte verglichen.  
4. **Alerting-Phase:** Abweichungen außerhalb statistischer Konfidenzgrenzen werden als Anomalien gemeldet.  

Alle Modelle sind erklärbar, deterministisch und für Unternehmensdatenvolumen optimiert.

---

## Beispielanwendungsfälle

- Überwachung der Datenqualität in **Bank-Transaktionssystemen**  
- Erkennung von Ladefehlern in **ETL- oder Data-Warehouse-Jobs**  
- Identifikation abnormaler Kundenaktivitäten in **Telekommunikationsdaten**  
- Überprüfung der Konsistenz klinischer Daten in **Healthcare-Analytics-Pipelines**  
- Vermeidung defekter Dashboards in **BI- und Reporting-Umgebungen**

---

## Häufig gestellte Fragen

**Benötigt Data Anomalies vordefinierte Regeln?**  
Nein — das Modul lernt das Verhalten der Daten automatisch.

**Kann ich bei Bedarf trotzdem spezifische Schwellenwerte definieren?**  
Ja. digna erlaubt die Kombination von KI-basierter und regelbasierter Erkennung (via *Data Validation*).

**Wie werden False Positives minimiert?**  
Das Modul verwendet adaptives Lernen und statistische Konfidenzbewertung, um normale saisonale Variationen zu ignorieren.

**Wo findet die Berechnung statt?**  
Die gesamte Verarbeitung läuft in Ihrer Datenbank — digna extrahiert niemals Rohdaten.

**Ist es für sensible oder regulierte Daten geeignet?**  
Ja. digna läuft vollständig on-premises oder in privater Cloud und entspricht europäischen Compliance-Standards.

---
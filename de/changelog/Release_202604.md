# Änderungsprotokoll – Release 2026.04  

Mit Release 2026.04 erweitert digna seine Fähigkeiten in den Bereichen Analytics und Datenvalidierung erheblich.  
Dieses Release führt erweiterte Zeitreihenanalyse, wiederverwendbare Validierungskomponenten und eine zentrale Standardisierung von Werten ein.

---

## Neue Funktionen  

### Analytics Chart – Zeitreihenanalyse ohne Data-Science-Kenntnisse  
- Neues **Analytics Chart** für interaktive Zeitreihenanalyse  
- Eingebaute analytische Methoden:
    - Lineare, quadratische und kubische Regression  
    - Piecewise-Regression mit konfigurierbaren Breakpoints  
    - Glättungstechniken  
    - Quantilanalyse  
- Automatische Identifikation von Trends, Saisonalitäten und Musteränderungen  
- Residuenanalyse für tiefere Einblicke in Abweichungen  
- Zeitreihen werden automatisch für jeden Datensatz berechnet  

**Auswirkung:** Ermöglicht Benutzern, komplexes Datenverhalten über die Zeit zu verstehen, ohne Data-Science-Expertise oder externe Tools zu benötigen.

---

### Enumerations – Zentrale Definition erlaubter Werte  
- Definieren Sie wiederverwendbare Mengen erlaubter Werte (z. B. Länder, Bundesländer, Statuscodes)  
- Validieren Sie Spaltenwerte gegen vordefinierte Enumerations in **digna Data Validation**  
- Wiederverwendung von Enumerations über Projekte und Datenquellen hinweg  
- Verwenden Sie Enumerations überall via `#ENUM:MY_ENUM#`  
- Alle Prüfungen werden **direkt in der Quelldatenbank** ausgeführt  

**Auswirkung:** Sorgt für konsistente und standardisierte Datenwerte in der gesamten Organisation.

---

### Validation Rule Templates – Wiederverwendbare Logik für Datenqualität  
- Definieren Sie wiederverwendbare Validierungsregeln (z. B. Whitespace-Prüfungen, NOT NULL, Formatprüfungen)  
- Wenden Sie Templates auf mehrere Datensätze an  
- Stellen Sie konsistente Regeln über Projekte hinweg sicher  
- Reduzieren Sie Duplikation und manuelle Konfiguration  
- Alle Prüfungen werden **direkt in der Quelldatenbank** ausgeführt  

**Auswirkung:** Ermöglicht skalierbare und leistungsfähige Datenvalidierung ohne Datenverschiebung.

---

### Relevanzbedingungen auf Statistik-Ebene  
- Definieren Sie Relevanzbedingungen auf **Spaltenebene für jede Statistik**  
- Erweitert das Konzept von Relevanzbedingungen für Anomalien  
- Steuern Sie, wann eine Statistik als relevant betrachtet werden sollte  
- Reduzieren Sie Rauschen, indem nicht-kritische Situationen ausgeschlossen werden  

**Auswirkung:** Verbessert die Signalqualität, indem nur sinnvolle Abweichungen fokussiert werden.

---

## Erweiterte Analyse- und Validierungsfähigkeiten  

Mit diesem Release erweitert digna sowohl das **Datenverständnis** als auch die **Standardisierung der Datenvalidierung**:

- Erweiterte **Zeitreiheninterpretation** ohne Data-Science-Kenntnisse  
- Zentrale Definition erlaubter Werte via Enumerations  
- Wiederverwendbare **Validierungslogik** über Templates  
- Fein granulare Kontrolle über die **Relevanz von Statistiken und Alerts**  

Zusammen ermöglichen diese Funktionen Organisationen nicht nur, Probleme zu erkennen, sondern auch **Datenqualität zu verstehen, zu standardisieren und zu steuern**.

---

## Wer von diesem Release profitiert  

- **Data Engineers:** Wiederverwendbare Validierungslogik und verbesserte Kontrolle über das Monitoring-Verhalten  
- **Data Quality & Governance Teams:** Standardisierte Regeln und konsistente Datenvalidierung über Systeme hinweg  
- **Analytics & BI Teams:** Besseres Verständnis von Trends und Abweichungen  
- **Platform Owners:** Erhöhte Akzeptanz durch vereinfachte Analysen und skalierbare Validierung  

---

## CLI-Aktualisierungen  
- Keine Änderungen  

---
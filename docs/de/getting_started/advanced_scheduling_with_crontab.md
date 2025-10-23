---
title: Erweiterte Zeitplanung mit Crontab
description: Erfahren Sie, wie Sie in digna einen Job mithilfe von crontab expressions für erweiterte Zeitsteuerung planen.
---

# Erweiterte Zeitplanung mit Crontab

Dieser Leitfaden zeigt, wie Sie Jobs in *digna* mit **crontab expressions** planen können.  
Im Gegensatz zu den Standardmustern (täglich, wöchentlich, monatlich) bietet crontab volle Flexibilität zur Definition benutzerdefinierter Zeitpläne.

---

## Interaktive Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Was Sie lernen werden

- Wie Sie den Abschnitt **Scheduling** im Dashboard öffnen  
- Wie Sie einen neuen Job mit einer **crontab expression** erstellen  
- Wie Sie einen Zeitplan einrichten, der nur an **Wochenenden um 10:00** ausgeführt wird  

---

## Beispiel: Wochenend-Zeitplan

Um einen Job so zu planen, dass er jeden **Samstag und Sonntag um 10:00 Uhr** ausgeführt wird, verwenden Sie den folgenden Ausdruck:


- `0` → Minute (zur vollen Stunde)  
- `10` → Stunde (10 Uhr)  
- `*` → jeder Tag des Monats  
- `*` → jeder Monat  
- `sat,sun` → nur samstags und sonntags  

---

## Warum Crontab verwenden?

- Zeitpläne erstellen, die über die Standardmuster (täglich, wöchentlich, monatlich) hinausgehen  
- Genaue Ausführungszeiten definieren (bestimmte Tage, Stunden oder Intervalle)  
- Nützlich für Wochenend-Jobs, Überprüfungen außerhalb der Geschäftszeiten oder häufiges Monitoring  

---
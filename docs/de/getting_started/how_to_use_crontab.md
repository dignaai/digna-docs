---
title: Erweiterte Zeitplanung mit Crontab | digna Dokumentation
description: Erfahren Sie, wie Sie in digna Jobs mit Crontab-Ausdrücken für erweiterte Zeitpläne planen.
image: /assets/logo_square.png
---

# Erweiterte Planung mit Crontab

Dieser Leitfaden zeigt, wie man Jobs in *digna* mithilfe von **Crontab-Ausdrücken** plant.  
Im Gegensatz zu den Standardmustern (täglich, wöchentlich, monatlich) bietet Crontab volle Flexibilität, um benutzerdefinierte Zeitpläne zu definieren.

---

## Interaktive Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Was Sie lernen werden

- Wie Sie den Abschnitt **Scheduling** im Dashboard öffnen  
- Wie Sie einen neuen Job mit einem **Crontab-Ausdruck** erstellen  
- Wie Sie einen Zeitplan einstellen, der nur an **Wochenenden um 10:00** läuft  

---

## Beispiel: Wochenend-Planung

Um einen Job so zu planen, dass er jeden **Samstag und Sonntag um 10:00 Uhr** läuft, verwenden Sie folgenden Ausdruck:


- `0` → Minute (zur vollen Stunde)  
- `10` → Stunde (10 Uhr)  
- `*` → jeder Tag des Monats  
- `*` → jeder Monat  
- `sat,sun` → nur samstags und sonntags  

---

## Warum Crontab verwenden?

- Erstellen Sie Zeitpläne, die über die Standardmuster täglich, wöchentlich oder monatlich hinausgehen  
- Definieren Sie präzise Ausführungszeiten (bestimmte Tage, Stunden oder Intervalle)  
- Nützlich für Wochenend-Jobs, Prüfungen außerhalb der Geschäftszeit oder häufige Überwachungen  

---
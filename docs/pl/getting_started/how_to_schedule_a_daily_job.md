---
title: Jak utworzyć zadanie uruchamiane codziennie
description: Dowiedz się, jak zaplanować codzienne zadanie inspekcji w digna za pomocą dashboardu.
keywords: digna scheduling, automatyzacja jakości danych, zadanie codzienne
---

# Jak zaplanować zadanie uruchamiane codziennie

**Scheduling** pozwala uruchamiać inspekcje automatycznie bez ręcznej interwencji.  
W tym przewodniku dowiesz się, jak utworzyć zadanie, które będzie wykonywane **raz dziennie**, zapewniając ciągły monitoring danych.

---

## Demo interaktywne

Przejdź przez interaktywny samouczek, aby zobaczyć proces w praktyce:  

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/Ra9E19A0QfMpzKqm3Yhu?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a New Data Inspection Job" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Czego się nauczysz

- Jak uzyskać dostęp do sekcji **Scheduling** w dashboardzie digna  
- Jak utworzyć nowe zaplanowane zadanie  
- Jak skonfigurować je tak, by uruchamiało się **codziennie o ustalonej godzinie**  
- Jak wybrać odpowiedni projekt i datasource  
- Jak włączyć zadanie, aby uruchamiało się automatycznie  

---

## Dlaczego zadania codzienne są przydatne

Codzienne planowanie to najczęstsza konfiguracja w środowiskach produkcyjnych. Zapewnia:  

- **Świeżość** — dane są walidowane codziennie.  
- **Spójność** — anomalie są wykrywane wcześnie, zanim rozprzestrzenią się dalej.  
- **Automatyzacja** — brak potrzeby ręcznego wywoływania inspekcji.  

---

## Kolejne kroki

- Przejrzyj [How to use crontab definition](how_to_use_crontab.md), aby poznać bardziej zaawansowane, niestandardowe harmonogramy.  
- Łącz zadania codzienne z **alertingiem**, aby otrzymywać powiadomienia, gdy wykryte zostaną anomalie.
---
title: Zaawansowane planowanie z Crontab | Dokumentacja digna
description: Dowiedz się, jak zaplanować zadanie w digna za pomocą wyrażeń crontab, aby uzyskać bardziej zaawansowane ustawienia czasowe.
---

# Zaawansowane planowanie z Crontab

Ten przewodnik pokazuje, jak planować zadania w *digna* przy użyciu **wyrażeń crontab**.  
W przeciwieństwie do standardowych wzorców (daily, weekly, monthly), crontab daje pełną elastyczność w definiowaniu niestandardowych harmonogramów.

---

## Interactive Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## What You Will Learn

- Jak otworzyć sekcję **Scheduling** w panelu  
- Jak utworzyć nowe zadanie używając **wyrażenia crontab**  
- Jak ustawić harmonogram, który uruchamia się tylko w **weekendy o 10:00**  

---

## Example: Weekend Schedule

Aby zaplanować zadanie, które będzie uruchamiane w każdą **sobotę i niedzielę o 10:00**, użyj następującego wyrażenia:


- `0` → minuta (na pełną godzinę)  
- `10` → godzina (10:00)  
- `*` → każdy dzień miesiąca  
- `*` → każdy miesiąc  
- `sat,sun` → tylko w soboty i niedziele  

---

## Why Use Crontab?

- Tworzenie harmonogramów wykraczających poza standardowe wzorce daily, weekly lub monthly  
- Definiowanie precyzyjnych godzin uruchomienia (konkretne dni, godziny lub interwały)  
- Przydatne dla zadań weekendowych, kontroli poza godzinami pracy lub częstego monitoringu  

---
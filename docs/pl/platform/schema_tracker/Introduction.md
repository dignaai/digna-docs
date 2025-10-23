---
title: Data Schema Tracker – Monitorowanie ewolucji schematu | Dokumentacja digna
description: Dowiedz się, jak digna Data Schema Tracker monitoruje zmiany kolumn, aktualizacje typów danych i dryf schematu. Otrzymuj powiadomienia o zamierzonych i niezamierzonych zmianach, aby zapobiec awariom ETL i błędom w dashboardach.
---

# Data Schema Tracker – Monitorowanie ewolucji schematu

## Cel
Śledź i otrzymuj powiadomienia o ewolucji schematu.

## Cechy techniczne
- Monitoruje:
  - Dodane lub usunięte kolumny
  - Zmiany typów danych
- Wysyła alerty zarówno o zamierzonych, jak i niezamierzonych zmianach schematu  
- Zapobiega **cichemu dryfowi schematu**, który może przerwać pipeline'y ETL lub spowodować błędy na dashboardach  

## Przykłady użycia
- Wykrywanie zmian typów danych (np. `INT` → `VARCHAR`), które mogą powodować błędy w kolejnych etapach przetwarzania  
- Powiadamianie inżynierów danych zanim pipeline'y ulegną awarii z powodu niezgodności schematu  

## Wartość
Pozwala zespołom zachować kontrolę nad **szybko ewoluującymi zbiorami danych**.
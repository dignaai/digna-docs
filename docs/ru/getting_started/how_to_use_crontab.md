---
title: Расширенное планирование с помощью crontab
description: Узнайте, как запланировать задачу в digna с помощью crontab-выражений для гибкого расписания.
image: /assets/logo_square.png
---

# Расширенное планирование с помощью crontab

Это руководство показывает, как планировать задачи в *digna* с помощью **crontab-выражений**.  
В отличие от стандартных шаблонов (ежедневно, еженедельно, ежемесячно), crontab даёт вам полную гибкость для определения пользовательских расписаний.

---

## Интерактивная демонстрация

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Чему вы научитесь

- Как открыть раздел **Scheduling** на панели управления  
- Как создать новую задачу с помощью **crontab-выражения**  
- Как задать расписание, которое выполняется только в **выходные в 10:00**  

---

## Пример: Расписание на выходные

Чтобы запланировать задачу на выполнение каждую **субботу и воскресенье в 10:00**, используйте следующее выражение:


- `0` → минута (ровно в начале часа)  
- `10` → час (10:00)  
- `*` → каждый день месяца  
- `*` → каждый месяц  
- `sat,sun` → только по субботам и воскресеньям  

---

## Зачем использовать crontab?

- Создавайте расписания, выходящие за рамки стандартных шаблонов (ежедневно, еженедельно, ежемесячно)  
- Задавайте точное время запусков (конкретные дни, часы или интервалы)  
- Полезно для задач в выходные, проверок в нерабочее время или частого мониторинга  

---
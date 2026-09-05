# Розширене планування за допомогою crontab

Цей посібник показує, як планувати завдання в *digna* за допомогою **crontab expressions**.  
На відміну від стандартних шаблонів (щодня, щотижня, щомісяця), crontab дає повну гнучкість для визначення власних розкладів.

---

## Інтерактивна демонстрація

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Чому ви це вивчите

- Як відкрити розділ **Scheduling** на дашборді  
- Як створити нове завдання, використовуючи **crontab expression**  
- Як налаштувати розклад, який запускається лише на **вихідних о 10:00**  

---

## Приклад: розклад на вихідні

Щоб запланувати завдання, яке виконуватиметься кожну **суботу та неділю о 10:00 ранку**, використайте такий вираз:


- `0` → хвилина (на початку години)  
- `10` → година (10:00)  
- `*` → кожен день місяця  
- `*` → кожен місяць  
- `sat,sun` → тільки в суботу та неділю  

---

## Навіщо використовувати crontab?

- Створювати розклади, які виходять за рамки стандартних щоденних, щотижневих або щомісячних шаблонів  
- Задавати точний час запуску (конкретні дні, години або інтервали)  
- Корисно для завдань на вихідних, перевірок у неробочий час або частого моніторингу  

---
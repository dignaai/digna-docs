---
title: Підключення бази даних | документація digna
description: Покроковий посібник з підключення бази даних до існуючого проєкту в digna. Дізнайтеся, як налаштувати з'єднання, вказати облікові дані та забезпечити безпечний доступ.
---

# Підключення бази даних

У цьому посібнику наведено мінімальні кроки для додавання підключення до бази даних у ваш проєкт.

## Інтерактивна демонстрація

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="Connect a Database to a Project"
    frameborder="0"
    loading="lazy"
    webkitallowfullscreen
    mozallowfullscreen
    allowfullscreen
    allow="clipboard-write"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;">
  </iframe>
</div>
<!--ARCADE EMBED END-->

---

### Кроки

1. **Відкрийте свій проєкт**  
   У лівій навігації натисніть **Projects** і виберіть потрібний проєкт.

2. **Додати підключення**  
   Перейдіть у **Connections** та натисніть **Add Connection**.

3. **Виберіть тип бази даних**  
   Виберіть базу даних, до якої бажаєте підключитися (наприклад, PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Введіть параметри з'єднання**  
   Надайте **Name**, **Host**, **Port**, **Database/Service**, та **Credentials** (ім'я користувача/пароль або SSO, залежно від випадку).

5. **Перевірити та зберегти**  
   Натисніть **Test**. Якщо перевірка успішна, натисніть **Save**. З'єднання з'явиться в розділі **Connections** для проєкту.
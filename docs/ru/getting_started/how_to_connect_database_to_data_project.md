---
title: Подключение базы данных | digna Documentation
description: Пошаговое руководство по подключению базы данных к существующему проекту в digna. Узнайте, как настроить подключение, указать учетные данные и обеспечить защищенный доступ.
image: /assets/logo_square.png
---

# Подключение базы данных

Это руководство показывает минимальные шаги для добавления подключения к базе данных в ваш проект.

## Интерактивная демонстрация

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

### Шаги

1. **Откройте проект**  
   В левой панели навигации нажмите **Projects** и выберите нужный проект.

2. **Добавьте подключение**  
   Перейдите в **Connections** и нажмите **Add Connection**.

3. **Выберите тип базы данных**  
   Выберите базу данных, к которой хотите подключиться (например, PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Введите данные подключения**  
   Укажите **Name**, **Host**, **Port**, **Database/Service** и **Credentials** (имя пользователя/пароль или SSO, в зависимости от случая).

5. **Проверка и сохранение**  
   Нажмите **Test**. Если тест прошел успешно, нажмите **Save**. Подключение появится в разделе **Connections** для данного проекта.
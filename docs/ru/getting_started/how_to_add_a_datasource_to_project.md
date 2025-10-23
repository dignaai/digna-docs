---
title: Подключение базы данных | документация digna
description: Пошаговое руководство по подключению базы данных к существующему проекту в digna. Узнайте, как выбрать подключение, настроить параметры и обеспечить безопасный доступ.
---

# Добавление источника данных (Table) в проект

Это руководство показывает минимальные шаги для добавления источника данных в ваш проект.

## Interactive Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/jvxy4tXv5xQlRAa1MsLI?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Add a Data Source to a Project" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

### Шаги

1. **Откройте проект**  
   В левой навигации нажмите **Projects** и выберите нужный проект.

2. **Добавьте источник данных**  
   Перейдите в **Datasources** и нажмите **Add Datasource**.

3. **Выберите тип источника данных**  
   Выберите тип базы данных: Таблица (Table) или Представление (View).

4. **Найдите источник данных в списке**  
   Выберите ваш источник данных в списке.

5. **Задайте Snapshot Query**  
   Определите Snapshot Query. Snapshot query определяет, как *digna* будет получать данные за один день.

6. **Предпросмотр**  
   Нажмите **Preview**, чтобы убедиться, что Snapshot Query задан корректно.

7. **Создать источник данных**  
   Если всё настроено правильно, вы можете сохранить конфигурацию.
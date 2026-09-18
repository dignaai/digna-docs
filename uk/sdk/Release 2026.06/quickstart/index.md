# Швидкий старт digna Python SDK 2026.06

На цій сторінці показано мінімальне налаштування та основні сценарії роботи з клієнтом Python SDK ***digna***. Почніть із неї, перш ніж переходити до довідкових сторінок про ресурси, моделі та помилки.

## Створення ключа API

Перш ніж підключатися через SDK, створіть ключ API в інтерфейсі ***digna***:

1. Увійдіть до ***digna*** в інтерфейсі.
2. Відкрийте свій профіль користувача в лівому нижньому куті.
3. У профілі користувача натисніть **API Keys**.
4. Натисніть **Add API Key**.
5. Вкажіть змістовну назву та встановіть дату завершення дії. Ключ API можна будь-коли відкликати або видалити.
6. Скопіюйте показаний ключ API до буфера обміну. Ключ відображається лише під час створення.

Використовуйте ключ API як токен SDK. Доречні способи передати його застосунку:

- Змінна середовища, наприклад `DIGNA_API_KEY`, для локальної розробки та автоматизації.
- Сховище секретів вашого CI/CD, наприклад секрети GitHub Actions, змінні CI/CD у GitLab або секретні змінні Azure DevOps.
- Менеджер секретів під час виконання, наприклад секрети Kubernetes, секрети Docker, HashiCorp Vault або сховище секретів хмарного провайдера.

Не вписуйте ключі API безпосередньо у вихідний код, записники, історію командної оболонки чи файли конфігурації, що потрапляють до системи контролю версій.

## Підключення

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Використовуйте `DignaClient` як контекстний менеджер, щоб базовий
пул з'єднань закривався автоматично:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Перегляд списку проєктів

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Створення джерела даних

```python
from digna_sdk.models import (
    DataSourceModules,
    DataSourceObject,
    StableDataSourceKind,
    StableDataSourceQueryMode,
)

data_source = client.data_sources.create(
    project_id=1,
    db_connection_id=10,
    name="orders_table",
    kind=StableDataSourceKind.TABLE,
    query_mode=StableDataSourceQueryMode.SINGLE,
    object=DataSourceObject(catalog_name="prod", schema_name="public", table_name="orders"),
    modules=DataSourceModules(
        data_analytics=True,
        data_anomaly=True,
        data_validation=True,
        schema_tracker=False,
        timeliness=False,
    ),
)
```

## Надсилання запиту на перевірку й очікування його завершення

```python
import datetime
from digna_sdk import DignaInspectionRequestFailed
from digna_sdk.models import StableInspectionRequestMode

request = client.inspection_requests.submit(
    project_id=1,
    data_source_ids=[data_source.id],
    start_date=datetime.date(2026, 1, 1),
    end_date=datetime.date(2026, 1, 31),
    mode=StableInspectionRequestMode.DAILY,
)

try:
    client.inspection_requests.wait_until_finished(request.id, poll_interval=2.0, timeout=300.0)
except DignaInspectionRequestFailed as exc:
    print(f"Inspection failed: {exc.status.value}")

# Once finished, retrieve the resulting statuses.
statuses = client.inspection_statuses.for_data_sources(
    data_source_id=data_source.id,
    start_date=datetime.date(2026, 1, 1),
    end_date=datetime.date(2026, 1, 31),
)
```

Повний перебіг надсилання → опитування → отримання наведено у файлі `examples/inspection_flow.py` у репозиторії.

## Обробка помилок

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
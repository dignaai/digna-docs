# Быстрый старт digna Python SDK 2026.06

На этой странице показаны минимальная настройка и основные сценарии работы с клиентом Python SDK ***digna***. Начните с неё, прежде чем переходить к справочным страницам о ресурсах, моделях и ошибках.

## Создание ключа API

Прежде чем подключаться с помощью SDK, создайте ключ API в интерфейсе ***digna***:

1. Войдите в ***digna*** в интерфейсе.
2. Откройте свой профиль пользователя в левом нижнем углу.
3. В профиле пользователя нажмите **API Keys**.
4. Нажмите **Add API Key**.
5. Укажите понятное имя и задайте срок действия. Ключ API можно отозвать или удалить в любой момент.
6. Скопируйте показанный ключ API в буфер обмена. Ключ отображается только при создании.

Используйте ключ API как токен SDK. Подходящие способы передать его приложению:

- Переменная окружения, например `DIGNA_API_KEY`, для локальной разработки и автоматизации.
- Хранилище секретов вашей CI/CD, например секреты GitHub Actions, переменные CI/CD в GitLab или секретные переменные Azure DevOps.
- Менеджер секретов во время выполнения, например секреты Kubernetes, секреты Docker, HashiCorp Vault или хранилище секретов облачного провайдера.

Не записывайте ключи API напрямую в исходный код, блокноты, историю командной оболочки или файлы конфигурации, попадающие в систему контроля версий.

## Подключение

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Используйте `DignaClient` как контекстный менеджер, чтобы базовый
пул соединений закрывался автоматически:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Список проектов

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Создание источника данных

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

## Отправка запроса на проверку и ожидание её завершения

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

Полный порядок действий отправка → опрос → получение результатов приведён в файле `examples/inspection_flow.py` в репозитории.

## Обработка ошибок

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
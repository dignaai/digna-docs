---
title: digna Python SDK Hızlı Başlangıç 2026.06 | digna Belgeleri
description: digna Python SDK 2026.06 sürümü için hızlı başlangıç kılavuzu
image: /assets/logo_square.png
---

# digna Python SDK Hızlı Başlangıç 2026.06

Bu sayfa, ***digna*** Python SDK'sı için en temel kurulumu ve başlıca istemci iş akışlarını gösterir. Kaynak, model ve hata başvuru sayfalarına geçmeden önce başlangıç noktası olarak kullanın.

## API Anahtarı Oluşturma

SDK ile bağlanmadan önce ***digna*** arayüzünde bir API anahtarı oluşturun:

1. Arayüzde ***digna*** oturumunuzu açın.
2. Sol alt köşedeki kullanıcı profilinizi açın.
3. Kullanıcı profilinde **API Keys** bağlantısına tıklayın.
4. **Add API Key** düğmesine tıklayın.
5. Anlamlı bir ad verin ve bir son kullanma tarihi belirleyin. Bir API anahtarını istediğiniz zaman iptal edebilir veya silebilirsiniz.
6. Görüntülenen API anahtarını panoya kopyalayın. Anahtar yalnızca oluşturulduğu anda gösterilir.

API anahtarını SDK belirteci olarak kullanın. Uygulamanıza iletmenin iyi yolları şunlardır:

- Yerel geliştirme ve otomasyon için bir ortam değişkeni, örneğin `DIGNA_API_KEY`.
- CI/CD gizli bilgi deponuz; örneğin GitHub Actions gizli bilgileri, GitLab CI/CD değişkenleri veya Azure DevOps gizli değişkenleri.
- Çalışma zamanı gizli bilgi yöneticisi; örneğin Kubernetes gizli bilgileri, Docker gizli bilgileri, HashiCorp Vault veya bir bulut sağlayıcısının gizli bilgi deposu.

API anahtarlarını kaynak koda, not defterlerine, kabuk geçmişine veya sürüm denetimine eklenen yapılandırma dosyalarına sabit olarak yazmaktan kaçının.

## Bağlanma

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Alttaki bağlantı havuzunun otomatik olarak kapatılması için `DignaClient` sınıfını
bağlam yöneticisi olarak kullanın:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Projeleri Listeleme

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Veri Kaynağı Oluşturma

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

## İnceleme İsteği Gönderme ve Tamamlanmasını Bekleme

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

Gönderme → yoklama → alma akışının tamamı için depodaki `examples/inspection_flow.py` dosyasına bakın.

## Hataları Ele Alma

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```

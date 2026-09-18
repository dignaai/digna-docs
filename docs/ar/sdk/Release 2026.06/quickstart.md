---
title: البدء السريع مع digna Python SDK 2026.06 | وثائق digna
description: دليل البدء السريع لإصدار digna Python SDK 2026.06
image: /assets/logo_square.png
---

# البدء السريع مع digna Python SDK 2026.06

تعرض هذه الصفحة الحد الأدنى من الإعداد وأهم مسارات العمل مع عميل حزمة تطوير Python الخاصة بـ ***digna***. استخدمها نقطة انطلاق قبل الانتقال إلى صفحات مرجع الموارد والنماذج والأخطاء.

## إنشاء مفتاح واجهة برمجة

أنشئ مفتاح واجهة برمجة في واجهة ***digna*** قبل الاتصال عبر الحزمة:

1. سجّل الدخول إلى ***digna*** من الواجهة.
2. افتح ملفك الشخصي في الزاوية السفلية اليسرى.
3. في الملف الشخصي، انقر على **API Keys**.
4. انقر على **Add API Key**.
5. أدخل اسمًا واضحًا وحدِّد تاريخ انتهاء الصلاحية. يمكنك إبطال مفتاح واجهة البرمجة أو حذفه في أي وقت.
6. انسخ مفتاح واجهة البرمجة المعروض إلى الحافظة. لا يُعرض المفتاح إلا عند إنشائه.

استخدم مفتاح واجهة البرمجة كرمز مميّز للحزمة. ومن الطرق الجيدة لتمريره إلى تطبيقك:

- متغيّر بيئة، مثل `DIGNA_API_KEY`، للتطوير المحلي والأتمتة.
- مخزن الأسرار في سلسلة CI/CD لديك، مثل أسرار GitHub Actions أو متغيّرات CI/CD في GitLab أو المتغيّرات السرية في Azure DevOps.
- مدير أسرار أثناء التشغيل، مثل أسرار Kubernetes أو أسرار Docker أو HashiCorp Vault أو مخزن أسرار مزوّد خدمة سحابية.

تجنّب كتابة مفاتيح واجهة البرمجة مباشرة في الشيفرة المصدرية أو الدفاتر أو سجل الطرفية أو ملفات الإعداد المضافة إلى نظام إدارة الإصدارات.

## الاتصال

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

استخدم `DignaClient` كمدير سياق حتى يُغلق تجمّع الاتصالات
الأساسي تلقائيًا:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## سرد المشاريع

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## إنشاء مصدر بيانات

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

## إرسال طلب فحص وانتظار انتهائه

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

للاطلاع على المسار الكامل من الإرسال إلى الاستعلام ثم جلب النتائج، راجع الملف `examples/inspection_flow.py` في المستودع.

## معالجة الأخطاء

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```

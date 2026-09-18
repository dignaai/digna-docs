# digna Python SDK त्वरित शुरुआत 2026.06

यह पृष्ठ ***digna*** Python SDK के लिए न्यूनतम सेटअप और मुख्य क्लाइंट कार्यप्रवाह दिखाता है। संसाधन, मॉडल और त्रुटि संदर्भ पृष्ठों पर जाने से पहले इसे प्रारंभिक बिंदु के रूप में उपयोग करें।

## API कुंजी बनाना

SDK से कनेक्ट करने से पहले ***digna*** फ्रंटएंड में एक API कुंजी बनाएँ:

1. फ्रंटएंड में ***digna*** में लॉग इन करें।
2. निचले-बाएँ कोने में अपनी उपयोगकर्ता प्रोफ़ाइल खोलें।
3. उपयोगकर्ता प्रोफ़ाइल में **API Keys** पर क्लिक करें।
4. **Add API Key** पर क्लिक करें।
5. एक सार्थक नाम दें और समाप्ति तिथि निर्धारित करें। आप API कुंजी को किसी भी समय रद्द या हटा सकते हैं।
6. दिखाई गई API कुंजी को क्लिपबोर्ड में कॉपी करें। कुंजी केवल बनाते समय ही दिखाई जाती है।

API कुंजी को SDK टोकन के रूप में उपयोग करें। इसे अपने अनुप्रयोग तक पहुँचाने के अच्छे तरीके:

- स्थानीय विकास और स्वचालन के लिए एक परिवेश चर, उदाहरण के लिए `DIGNA_API_KEY`।
- आपका CI/CD सीक्रेट स्टोर, जैसे GitHub Actions सीक्रेट, GitLab CI/CD चर या Azure DevOps के गुप्त चर।
- रनटाइम सीक्रेट प्रबंधक, जैसे Kubernetes सीक्रेट, Docker सीक्रेट, HashiCorp Vault या किसी क्लाउड प्रदाता का सीक्रेट स्टोर।

API कुंजियों को स्रोत कोड, नोटबुक, शेल इतिहास या संस्करण नियंत्रण में जोड़ी गई कॉन्फ़िगरेशन फ़ाइलों में हार्ड-कोड करने से बचें।

## कनेक्ट करना

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

`DignaClient` को कॉन्टेक्स्ट मैनेजर के रूप में उपयोग करें, ताकि अंतर्निहित
कनेक्शन पूल स्वतः बंद हो जाए:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## परियोजनाओं की सूची

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## डेटा स्रोत बनाना

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

## निरीक्षण अनुरोध भेजना और उसके पूरा होने की प्रतीक्षा करना

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

भेजने → पोल करने → परिणाम प्राप्त करने के पूरे प्रवाह के लिए रिपॉज़िटरी में `examples/inspection_flow.py` देखें।

## त्रुटियों का प्रबंधन

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
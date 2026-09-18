---
title: Γρήγορη εκκίνηση digna Python SDK 2026.06 | Τεκμηρίωση digna
description: Οδηγός γρήγορης εκκίνησης για την έκδοση digna Python SDK 2026.06
image: /assets/logo_square.png
---

# Γρήγορη εκκίνηση digna Python SDK 2026.06

Αυτή η σελίδα δείχνει την ελάχιστη ρύθμιση και τις βασικές ροές εργασίας του client για το Python SDK του ***digna***. Χρησιμοποιήστε την ως αφετηρία πριν προχωρήσετε στις σελίδες αναφοράς για πόρους, μοντέλα και σφάλματα.

## Δημιουργία κλειδιού API

Δημιουργήστε ένα κλειδί API στο περιβάλλον του ***digna*** πριν συνδεθείτε με το SDK:

1. Συνδεθείτε στο ***digna*** από το περιβάλλον χρήσης.
2. Ανοίξτε το προφίλ χρήστη σας στην κάτω αριστερή γωνία.
3. Στο προφίλ χρήστη, κάντε κλικ στο **API Keys**.
4. Κάντε κλικ στο **Add API Key**.
5. Δώστε ένα σαφές όνομα και ορίστε ημερομηνία λήξης. Μπορείτε να ανακαλέσετε ή να διαγράψετε ένα κλειδί API οποτεδήποτε.
6. Αντιγράψτε το κλειδί API που εμφανίζεται στο πρόχειρο. Το κλειδί εμφανίζεται μόνο κατά τη δημιουργία του.

Χρησιμοποιήστε το κλειδί API ως token του SDK. Καλοί τρόποι για να το δώσετε στην εφαρμογή σας:

- Μια μεταβλητή περιβάλλοντος, για παράδειγμα `DIGNA_API_KEY`, για τοπική ανάπτυξη και αυτοματοποίηση.
- Ο χώρος αποθήκευσης μυστικών του CI/CD σας, όπως τα secrets του GitHub Actions, οι μεταβλητές CI/CD του GitLab ή οι μυστικές μεταβλητές του Azure DevOps.
- Ένας διαχειριστής μυστικών κατά την εκτέλεση, όπως τα secrets του Kubernetes, τα secrets του Docker, το HashiCorp Vault ή ο χώρος αποθήκευσης μυστικών ενός παρόχου cloud.

Αποφύγετε να γράφετε κλειδιά API απευθείας στον πηγαίο κώδικα, σε notebooks, στο ιστορικό του κελύφους ή σε αρχεία ρυθμίσεων που καταχωρίζονται στο σύστημα ελέγχου εκδόσεων.

## Σύνδεση

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Χρησιμοποιήστε το `DignaClient` ως context manager, ώστε το υποκείμενο
connection pool να κλείνει αυτόματα:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Προβολή έργων

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Δημιουργία πηγής δεδομένων

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

## Υποβολή αιτήματος ελέγχου και αναμονή έως την ολοκλήρωσή του

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

Για την πλήρη ροή υποβολή → ερώτημα → ανάκτηση, δείτε το `examples/inspection_flow.py` στο αποθετήριο.

## Διαχείριση σφαλμάτων

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```

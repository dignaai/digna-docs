---
title: Démarrage rapide du SDK Python digna 2026.06 | Documentation digna
description: Guide de démarrage rapide du SDK Python digna version 2026.06
image: /assets/logo_square.png
---

# Démarrage rapide du SDK Python digna 2026.06

Cette page présente la configuration minimale et les principaux flux de travail du client pour le SDK Python ***digna***. Utilisez-la comme point de départ avant de passer aux pages de référence des ressources, des modèles et des erreurs.

## Créer une clé d'API

Créez une clé d'API dans l'interface ***digna*** avant de vous connecter avec le SDK :

1. Connectez-vous à ***digna*** dans l'interface.
2. Ouvrez votre profil utilisateur en bas à gauche.
3. Dans le profil utilisateur, cliquez sur **API Keys**.
4. Cliquez sur **Add API Key**.
5. Donnez un nom explicite et définissez une date d'expiration. Vous pouvez révoquer ou supprimer une clé d'API à tout moment.
6. Copiez la clé d'API affichée dans le presse-papiers. La clé n'est affichée qu'au moment de sa création.

Utilisez la clé d'API comme jeton du SDK. Voici de bonnes façons de la fournir à votre application :

- Une variable d'environnement, par exemple `DIGNA_API_KEY`, pour le développement local et l'automatisation.
- Le coffre à secrets de votre CI/CD, comme les secrets GitHub Actions, les variables CI/CD GitLab ou les variables secrètes Azure DevOps.
- Un gestionnaire de secrets à l'exécution, comme les secrets Kubernetes, les secrets Docker, HashiCorp Vault ou le coffre à secrets d'un fournisseur cloud.

Évitez de coder en dur les clés d'API dans le code source, les notebooks, l'historique du shell ou les fichiers de configuration versionnés.

## Se connecter

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Utilisez `DignaClient` comme gestionnaire de contexte pour que le pool de connexions
sous-jacent soit fermé automatiquement :

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Lister les projets

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Créer une source de données

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

## Soumettre une demande d'inspection et attendre sa fin

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

Consultez `examples/inspection_flow.py` dans le dépôt pour le flux complet soumission → interrogation → récupération.

## Gérer les erreurs

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```

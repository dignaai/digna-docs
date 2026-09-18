# digna Python SDK クイックスタート 2026.06

このページでは、***digna*** Python SDK の最小限のセットアップと主要なクライアント操作を示します。リソース、モデル、エラーの各リファレンスページに進む前の出発点として利用してください。

## API キーの作成

SDK で接続する前に、***digna*** のフロントエンドで API キーを作成します。

1. フロントエンドで ***digna*** にログインします。
2. 左下のユーザープロファイルを開きます。
3. ユーザープロファイルで **API Keys** をクリックします。
4. **Add API Key** をクリックします。
5. わかりやすい名前を付け、有効期限を設定します。API キーはいつでも失効または削除できます。
6. 表示された API キーをクリップボードにコピーします。キーが表示されるのは作成時のみです。

API キーは SDK のトークンとして使用します。アプリケーションへ渡す適切な方法は次のとおりです。

- ローカル開発や自動化では、環境変数（例: `DIGNA_API_KEY`）を使用する。
- GitHub Actions のシークレット、GitLab の CI/CD 変数、Azure DevOps のシークレット変数など、CI/CD のシークレットストアを使用する。
- Kubernetes シークレット、Docker シークレット、HashiCorp Vault、クラウドプロバイダーのシークレットストアなど、実行時のシークレットマネージャーを使用する。

API キーをソースコード、ノートブック、シェル履歴、バージョン管理に登録する設定ファイルにハードコードしないでください。

## 接続

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

`DignaClient` をコンテキストマネージャーとして使用すると、内部の
コネクションプールが自動的に閉じられます。

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## プロジェクトの一覧表示

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## データソースの作成

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

## 検査リクエストの送信と完了の待機

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

送信 → ポーリング → 取得という一連の流れの全体は、リポジトリの `examples/inspection_flow.py` を参照してください。

## エラーの処理

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
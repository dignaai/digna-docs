# digna Python SDK 빠른 시작 2026.06

이 페이지에서는 ***digna*** Python SDK의 최소 설정과 주요 클라이언트 작업 흐름을 소개합니다. 리소스, 모델, 오류 참조 페이지로 넘어가기 전 출발점으로 활용하세요.

## API 키 만들기

SDK로 연결하기 전에 ***digna*** 프런트엔드에서 API 키를 만듭니다.

1. 프런트엔드에서 ***digna***에 로그인합니다.
2. 왼쪽 아래에서 사용자 프로필을 엽니다.
3. 사용자 프로필에서 **API Keys**를 클릭합니다.
4. **Add API Key**를 클릭합니다.
5. 의미 있는 이름을 지정하고 만료 날짜를 설정합니다. API 키는 언제든지 취소하거나 삭제할 수 있습니다.
6. 표시된 API 키를 클립보드에 복사합니다. 키는 생성할 때만 표시됩니다.

API 키를 SDK 토큰으로 사용합니다. 애플리케이션에 전달하는 좋은 방법은 다음과 같습니다.

- 로컬 개발과 자동화에는 환경 변수(예: `DIGNA_API_KEY`)를 사용합니다.
- GitHub Actions 시크릿, GitLab CI/CD 변수, Azure DevOps 비밀 변수 등 CI/CD 비밀 저장소를 사용합니다.
- Kubernetes 시크릿, Docker 시크릿, HashiCorp Vault, 클라우드 공급자의 비밀 저장소 등 런타임 비밀 관리자를 사용합니다.

API 키를 소스 코드, 노트북, 셸 기록, 버전 관리에 커밋되는 구성 파일에 하드코딩하지 마세요.

## 연결

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

`DignaClient`를 컨텍스트 관리자로 사용하면 내부 연결 풀이
자동으로 닫힙니다.

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## 프로젝트 목록 조회

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## 데이터 소스 만들기

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

## 검사 요청 제출 후 완료 대기

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

제출 → 폴링 → 조회로 이어지는 전체 흐름은 저장소의 `examples/inspection_flow.py`를 참고하세요.

## 오류 처리

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
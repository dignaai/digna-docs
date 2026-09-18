# digna Python SDK 참조 2026.06

이 섹션에서는 ***digna***의 Python SDK를 설명합니다. 여러 페이지로 구성된 참조 문서이므로, 먼저 이 개요로 클라이언트를 파악한 다음 빠른 시작, 리소스, 모델, 오류, 자동 생성 API 문서 페이지로 이어서 살펴보세요.

SDK는 `digna-sdk` 패키지로 배포되며 ***digna*** REST API를 위한 안정적인 버전 관리 클라이언트를 제공합니다.

---

## SDK 기본 사항

---

### 개요

SDK는 리소스 중심의 클라이언트 설계를 따릅니다. 각 API 영역은 최상위 `DignaClient`에서 독립된 클라이언트로 제공되며, 요청과 응답 모델에 타입이 지정되어 있고 오류 처리 방식도 일관됩니다.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### 핵심 기능

- **타입이 지정된 모델** — 모든 요청과 응답이 pydantic으로 검증되므로 네트워크 호출 전에 편집기와 타입 검사기가 실수를 잡아냅니다.
- **리소스 중심 구조** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests`, `client.inspection_statuses`는 각각 간단한 `list` / `get` / `create` / `update` / `delete` 메서드를 제공합니다.
- **명확한 오류** — API 오류는 조용히 `None`을 반환하는 대신 `DignaAPIError`(또는 `DignaAuthenticationError`, `DignaAuthorizationError`, `DignaNotFoundError` 같은 더 구체적인 하위 클래스)를 발생시킵니다.

### 설치

```bash
pip install digna-sdk
```

---

## 참조 페이지

이 릴리스는 다음 페이지로 구성되어 있습니다.

- [빠른 시작](quickstart.md) — 연결하고 첫 호출을 실행합니다.
- [리소스](resources.md) — 사용할 수 있는 리소스 클라이언트의 전체 목록입니다.
- [모델](models.md) — 입력과 출력에 사용되는 pydantic 모델입니다.
- [오류](errors.md) — 예외 계층 구조입니다.
- [API 참조](reference.md) — 자동 생성된 참조 문서입니다.
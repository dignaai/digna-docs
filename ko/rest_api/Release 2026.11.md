# digna REST API 2026.11

*digna* REST API를 사용하면 자체 도구와 파이프라인이 HTTP와 JSON으로 *digna*와 연동할 수 있습니다.
프로젝트와 검사 결과를 읽고, 데이터 소스·데이터 세트·속성을 관리하고, 예를 들어 데이터 적재가 끝날 때
검사를 시작할 수 있습니다. [Python SDK](../../sdk/Release%202026.11/index.md)도
같은 API를 사용합니다.

이 페이지에서는 모든 요청에 공통되는 내용을 다룹니다. 리소스 페이지에는 각 엔드포인트의 매개변수,
요청 본문, 응답, 스키마가 정리되어 있습니다.

| 리소스 | 엔드포인트 |
|---|---|
| [Projects](projects.md) | 프로젝트 읽기 |
| [DB Connections](db_connections.md) | 데이터베이스 연결 읽기 |
| [Data Sources](data_sources.md) | 데이터 소스 생성, 읽기, 업데이트, 삭제 |
| [Data Sets](data_sets.md) | 데이터 세트 생성, 읽기, 업데이트, 삭제 |
| [Attributes](attributes.md) | 속성 생성, 읽기, 업데이트, 삭제 |
| [Check Definitions](check_definitions.md) | 검사 정의 읽기 |
| [Inspection Requests](inspection_requests.md) | 검사 시작 및 진행 상황 추적 |
| [Inspection Statuses](inspection_statuses.md) | 프로젝트, 데이터 소스, 데이터 세트별 검사 결과 읽기 |

---

## 기본 URL {: #base-url }

이 API는 *digna* 백엔드의 일부입니다. 모든 경로는 백엔드 주소 뒤에 `/v1`로 시작합니다.

```text
https://digna.example.com/v1/projects
```

백엔드 주소는 대시보드가 사용하는 주소와 같으며, `dashboard/dashboard_config.toml`의 `[api]` 섹션에 있는
`baseUrl`입니다. 모든 요청에 API 키가 담기므로, 호출하는 쪽과 *digna*가 같은 머신에 있지 않다면
항상 HTTPS를 사용하세요.

---

## 인증 {: #authentication }

모든 요청은 *digna* 사용자의 API 키를 `Authorization` 헤더에 담아 보냅니다.

```text
Authorization: Bearer <api key>
```

키를 만들려면 대시보드 왼쪽 아래에서 사용자 프로필을 열고 **API Keys**, 이어서 **Add API Key**를 클릭한 뒤
키를 복사합니다. 키는 한 번만 표시됩니다. 같은 키를 [digna MCP Server](../../ai_agents/overview.md)에서도
사용할 수 있습니다.

요청은 키 소유 사용자의 권한으로 실행됩니다. 생성, 변경, 삭제에는 해당 프로젝트의 editor 역할이 필요하며,
그렇지 않으면 요청이 `403`과 메시지 `You don't have permission to edit this project`로 거부됩니다.

!!! tip "자동화에는 전용 사용자를 사용하세요"

    통합마다 *digna* 사용자를 만들고 필요한 프로젝트와 역할만 부여한 다음, 만료일이 있는 키를
    만드세요. 그러면 키를 삭제하는 것만으로 한 통합의 접근 권한을 취소할 수 있으며, 다른 사람에게는
    영향을 주지 않습니다.

---

## 요청 보내기 {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

응답은 JSON입니다. 목록은 JSON 배열로 반환됩니다. 요청 본문도 JSON이며 `Content-Type: application/json`과
함께 보냅니다.

---

## 한도와 필터 {: #limits-and-filters }

목록 엔드포인트는 최대 `limit`개의 항목을 반환합니다. 기본값은 200개이고 최대 5000개까지 가능합니다. 이 범위를
벗어난 값은 `400`으로 거부됩니다. 오프셋이나 페이지 토큰이 없으므로, 대신 목록의 필터로 범위를 좁히세요.
예를 들어 `project_id`, `data_source_id`, 또는 검사 상태의 경우 `start_date`와 `end_date`를 사용합니다.

60초보다 오래 걸리는 요청은 `408 Request Timeout`으로 취소됩니다.

---

## 오류 {: #errors }

오류 응답에는 코드와 메시지가 담긴 JSON 본문이 있습니다.

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| 상태 | 코드 | 의미 |
|---|---|---|
| `400` | `BAD_REQUEST` | 요청이 잘못되었습니다. 예: 범위를 벗어난 `limit` |
| `401` | `NOT_AUTHENTICATED` | API 키가 없거나, 형식이 잘못되었거나, 알 수 없거나, 만료되었습니다 |
| `403` | `NOT_AUTHORIZED` | 키의 사용자에게 이 요청에 필요한 역할이 없습니다 |
| `403` | `INVALID_LICENSE` | *digna* 라이선스가 만료되었습니다 |
| `404` | `NOT_FOUND` | 프로젝트, 데이터 소스 또는 기타 항목이 존재하지 않습니다 |
| `500` | `INTERNAL_ERROR` | *digna*에서 예기치 않은 오류가 발생했습니다. 자세한 내용은 백엔드 로그에 있습니다 |

`401`의 `message`는 키에 어떤 문제가 있는지 알려 줍니다.

| 메시지 | 원인 |
|---|---|
| `Missing Authorization header` | `Authorization` 헤더를 보내지 않았습니다 |
| `Invalid Authorization header format` | 값이 `Bearer `로 시작하지 않습니다 |
| `Invalid API key` | 키가 잘못되었거나 삭제되었습니다 |
| `API key expired` | 키가 만료되었습니다. 새 키를 만드세요 |

---

## 검사 실행 {: #running-an-inspection }

일반적인 통합은 데이터 적재가 끝나면 검사를 시작하고, 검사가 끝날 때까지 기다린 다음 결과를 읽습니다.

1. [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request)로 **검사를 시작합니다**.
   응답에는 요청의 `id`가 들어 있습니다.
2. [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request)로 **진행 상황을 추적합니다**.
   `status`는 `PENDING`에서 `RUNNING`을 거쳐 `COMPLETED`로 바뀌거나, `FAILED`, `ABORTED` 또는
   `CANCELLED`로 끝납니다. 값이 더 이상 바뀌지 않을 때까지 몇 초마다 다시 조회하세요.
3. 검사한 날짜에 대해 [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)로 **결과를 읽습니다**.
   각 항목에는 전체 `status`로 `0`(OK), `1`(경고), `2`(심각) 또는 `-1`(상태 없음)이 있고,
   모듈별 상태와 함께 통과, 불확실, 실패한 검사 수가 포함됩니다.

```bash
curl -X POST https://digna.example.com/v1/inspection-requests \
  -H "Authorization: Bearer $DIGNA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "project_id": 1,
    "include_all_data_sources": true,
    "data_source_ids": [],
    "start_date": "2026-11-06",
    "end_date": "2026-11-06",
    "mode": "DAILY",
    "weekly_mode_weekdays": [],
    "monthly_mode_days": [],
    "use_notification": true
  }'
```

---

## OpenAPI 문서 {: #openapi-document }

모든 *digna* 설치는 이 API를 OpenAPI 3.1 문서로 설명하며, 이를 대상으로 요청을 시험해 볼 수 있는 대화형
Swagger UI를 제공합니다.

| 항목 | 주소 |
|---|---|
| OpenAPI 문서 | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Release 2026.11의 문서는 여기에서도 받을 수 있습니다: [openapi.json](openapi.json). 이 문서로 다른 언어의
클라이언트를 생성할 수 있습니다.

!!! note "/v1 엔드포인트만 다룹니다"

    대시보드는 그 밖의 내부 엔드포인트를 통해서도 백엔드와 통신합니다. 이 엔드포인트들은 이 API에
    속하지 않으며 어느 릴리스에서든 바뀔 수 있으므로, 통합은 `/v1` 엔드포인트만을 기반으로 구축하세요.
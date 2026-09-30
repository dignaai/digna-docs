# Databricks용 소스 커넥터

이 가이드는 **DSN 없는(DSN-less)** 연결 문자열을 사용하여 **ODBC**로 Databricks에 연결하도록
*digna*를 구성하는 방법을 설명합니다.

설정 중 *digna* 측 부분은 모든 기술에서 동일합니다. 연결을 만드는 위치, 속성 값을 암호화하는 방법,
연결을 테스트하는 방법, 프로파일링 모드의 의미가 여기에 해당하며
[데이터베이스 연결 개요](overview.md)에 설명되어 있습니다. 이 페이지에서는 Databricks에만 해당하는
내용을 다룹니다.

!!! note "Unity Catalog 필요"

    *digna*는 `system.information_schema.catalogs`에서 사용 가능한 카탈로그를 읽으므로,
    워크스페이스에서 Unity Catalog가 활성화되어 있어야 합니다. 이전 *digna* 릴리스에서는 Unity
    Catalog가 없는 워크스페이스를 위해 별도의 "Databricks Legacy" 기술을 제공했지만, 이제는 더 이상
    제공되지 않습니다.

---

## 1. ODBC 드라이버 설치 {: #1-install-the-odbc-driver }

[Databricks 설치 가이드](https://docs.databricks.com/aws/en/integrations/odbc/)에 따라
*digna* 백엔드가 실행되는 머신에 **Databricks ODBC Driver**를 설치합니다.

버전에 따라 드라이버는 **Simba Spark ODBC Driver** 또는 **Databricks ODBC Driver**라는 이름으로
등록됩니다. [digna 호스트에 ODBC 드라이버 설치](overview.md#install-the-driver)에 설명된 대로
호스트에서 등록된 정확한 이름을 확인합니다.

---

## 2. 연결 세부 정보 수집 {: #2-gather-the-connection-details }

모든 값은 *digna*가 사용할 SQL 웨어하우스(또는 클러스터)에서 가져옵니다. Databricks 워크스페이스에서
해당 웨어하우스를 열고 **Connection details**로 이동합니다:

| Databricks 필드 | 사용처 |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, 일반적으로 `443` |
| **HTTP path** | `HTTPPath` |

인증을 위해 **개인 액세스 토큰(personal access token)**을 만듭니다.
[Databricks 개인 액세스 토큰 인증](https://docs.databricks.com/aws/en/dev-tools/auth/pat)을
참조하세요. 토큰은 사용자 또는 서비스 주체에 속하며, 해당 주체에는 소스 데이터에 대한 `USE CATALOG`,
`USE SCHEMA`, `SELECT` 권한이 필요합니다.

---

## 3. ODBC 속성 {: #3-odbc-properties }

!!! important "사양이 아닌 예시"

    아래 속성 세트는 정상 동작이 확인된 조합 중 하나입니다. 이 속성들은 Databricks/Simba 드라이버에
    속하므로 이름, 기본값, 허용되는 값이 드라이버 버전마다(드라이버는 여러 차례 이름이 바뀌고 인증
    옵션이 확장되었습니다) 그리고 플랫폼마다 다릅니다. 이를 출발점으로 삼고, 설치한 드라이버 버전의
    문서를 확인하세요.

**Add DB Connection** 화면에서 다음 속성을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | *digna* 호스트에 등록된 드라이버 이름과 일치해야 합니다 |
| `Host` | `<workspace>.cloud.databricks.com` | 웨어하우스의 서버 호스트 이름, 예: `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | 웨어하우스 또는 클러스터의 HTTP 경로 |
| `SSL` | `1` | Databricks 엔드포인트는 TLS 전용입니다 |
| `ThriftTransport` | `2` | HTTP 전송으로, SQL 엔드포인트가 사용하는 방식입니다 |
| `AuthMech` | `3` | 토큰 인증 |
| `UID` | `token` | 사용자 이름이 아니라 문자 그대로 `token`입니다 |
| `PWD` | `dapi…` | 개인 액세스 토큰입니다. **Encrypted**를 선택합니다 |
| `UseNativeQuery` | `1` | *digna*의 SQL을 변경 없이 그대로 전달합니다 — 아래 참조 |

결과 연결 문자열은 다음과 같습니다:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "`UseNativeQuery=1`을 유지하세요"

    드라이버 기본값인 `UseNativeQuery=0`에서는 드라이버가 들어오는 SQL을 이식 가능한 ODBC 구문이라고
    판단하는 형태로 다시 씁니다. *digna*는 이미 Databricks SQL을 생성하므로, 이 재작성 과정에서
    백틱 인용과 날짜 리터럴이 바뀔 수 있고, 그 결과 원래대로라면 유효한 문장에서 프로파일링이 실패합니다.

### 토큰 대신 OAuth 사용

OAuth 머신 간(M2M) 인증을 사용하는 서비스 주체의 경우 `AuthMech`, `UID`, `PWD`를 다음으로
바꿉니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | 클라이언트 자격 증명 |
| `Auth_Client_ID` | `<application id>` | 서비스 주체 |
| `Auth_Client_Secret` | `<client secret>` | **Encrypted**를 선택합니다 |

---

## 4. *digna* 구성 {: #4-digna-configuration }

**Add DB Connection** 화면에서 다음을 입력합니다:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Databricks 관련 참고 사항 {: #5-notes-on-databricks }

- ***digna*가 연결할 때 웨어하우스가 실행 중이거나 시작 가능한 상태여야 합니다.** 중지 상태에서
  재개되는 웨어하우스는 연결 시간 제한보다 오래 걸릴 수 있습니다. 유휴 기간 후 첫 시도에서 테스트가
  실패하면 다시 시도하세요.
- **카탈로그는 워크스페이스에서 가져옵니다.** 대부분의 기술과 달리, 하나의 Databricks 연결로 주체가
  볼 수 있는 모든 카탈로그에 접근할 수 있으므로 하나의 연결로 여러 카탈로그에 걸친 소스를 처리할 수
  있습니다.
- **프로파일링 모드.** *Permanent*는 소스 카탈로그 내의 **Work Schema**에 작업 테이블을 만들므로
  주체에게 그곳에 대한 `CREATE TABLE` 권한이 필요합니다. *Session*은 `CREATE TEMPORARY TABLE`을
  사용하며 **Work Schema**를 건드리지 않습니다. *Standard*는 읽기 권한만 필요합니다.
- **서버리스 웨어하우스도 동일하게 동작합니다.** `HTTPPath`만 다릅니다.

---

## 6. 드라이버 확인(선택 사항) {: #6-verifying-the-driver-optional }

DSN 없는 연결에는 ODBC 데이터 소스를 구성할 필요가 없지만, 드라이버 자체의 대화 상자를 사용하면
*digna*에 값을 입력하기 전에 드라이버, 웨어하우스, 토큰이 동작하는지 간편하게 확인할 수 있습니다.

#### 1단계
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### 2단계
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### 3단계
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### 4단계
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### 5단계 – 연결 테스트

**TEST** 버튼을 클릭합니다. 연결에 성공하면 다음과 같이 표시됩니다:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

여기에 입력한 호스트, HTTP 경로, 토큰이 바로 [섹션 3](#3-odbc-properties)의 속성에 들어가는
값입니다.
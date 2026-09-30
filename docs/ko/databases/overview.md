---
title: 데이터베이스 연결 개요 – DSN 없는 ODBC 설정 | digna 문서
description: digna에서 데이터베이스 연결이 작동하는 방식. 모든 소스 기술은 ODBC 속성으로 구성된 DSN 없는 연결 문자열을 통해 ODBC로 연결됩니다. digna 호스트의 드라이버 설치, Add DB Connection 화면, 속성 암호화, 연결 테스트, 문제 해결 및 기술별 가이드 링크를 다룹니다.
image: /assets/logo_square.png
keywords:
  - digna 데이터베이스 연결
  - dsn-less odbc
  - odbc 연결 문자열
  - odbc 드라이버 설정
  - unixodbc
  - odbc 속성
  - 데이터 소스 구성
lang: ko
robots: index, follow
og_title: digna 데이터베이스 연결 – DSN 없는 ODBC 설정
og_description: DSN 없이 ODBC로 digna 소스 연결을 구성합니다. 드라이버 설치, ODBC 속성, 암호화, 테스트 및 문제 해결.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# 데이터베이스 연결 개요

---

## 목차

1. [연결 작동 방식](#how-connections-work)
2. [기술별 가이드](#technology-guides)
3. [사전 요구 사항: digna 호스트에 ODBC 드라이버 설치](#install-the-driver)
4. [데이터베이스 연결 만들기](#create-a-database-connection)
5. [ODBC 속성](#odbc-properties)
6. [속성 값 암호화](#encrypting-property-values)
7. [연결 테스트](#testing-a-connection)
8. [연결이 보는 데이터베이스](#which-database-the-connection-sees)
9. [프로파일링 모드와 Work Schema](#profiling-mode-and-work-schema)
10. [DSN 사용하기](#using-a-dsn-instead)
11. [문제 해결](#troubleshooting)

---

## 연결 작동 방식 {: #how-connections-work }

*digna*는 모든 소스 기술에 **ODBC**로 연결합니다. 연결은 키/값 쌍으로 입력하는 ODBC 속성의
목록입니다. *digna*가 연결을 열면 이 쌍들을 입력한 순서대로 `;`로 구분된 `Key=Value` 형태의 연결
문자열로 합친 다음, *digna* 호스트의 ODBC 드라이버 관리자에 전달합니다.

속성을 직접 입력하기 때문에 설정이 **DSN 없는(DSN-less)** 방식이 됩니다. 연결에 드라이버가 필요로
하는 모든 정보가 들어 있으므로 호스트에 ODBC 데이터 소스(DSN)를 등록할 필요가 없습니다. 연결 정의가
전적으로 *digna* 안에 있고 *digna*와 함께 이동하므로, 이것이 *digna*를 구성하는 권장 방법입니다.

### 왜 ODBC인가 {: #why-odbc }

이전 릴리스에서는 **Use ODBC** 스위치로 기술별 드라이버와 ODBC 중 하나를 선택할 수 있었습니다.
Release 2026.06부터 *digna*는 ODBC만을 기반으로 합니다. 하나의 표준 인터페이스는 개별 맞춤 드라이버
모음보다 더 많은 것을 제공합니다:

- **인증** — 인증은 ODBC의 일부이므로, 연결은 드라이버가 지원하는 모든 방식을 사용할 수 있습니다.
  비밀번호, 토큰과 PAT, Kerberos와 Active Directory, MFA와 브라우저 기반 싱글 사인온, 클라우드 ID,
  클라이언트 인증서와 TLS 등이 해당됩니다. 새로운 방식은 *digna* 릴리스를 기다릴 필요 없이 드라이버
  업데이트와 함께 제공됩니다.
- **데이터베이스 공급업체가 유지 관리하는 드라이버** — 공급업체의 자체 드라이버는 새로운 서버 버전과
  보안 수정 사항을 따라가며, *digna*와 무관하게 원하는 일정에 맞춰 업데이트할 수 있습니다.
- **모든 것을 구성하는 단일 방식** — 소스마다 다른 필드 세트 대신, 모든 기술이 동일한 인터페이스,
  민감한 값의 동일한 암호화, 동일한 문제 해결 방식을 갖춘 키/값 속성 목록으로 구성됩니다.
- **튜닝과 적용 범위** — 시간 제한, TLS 설정, 프록시, 페치 크기 같은 드라이버 수준 옵션을 모든
  소스에서 사용할 수 있으며, *digna*가 전용 가이드를 제공하지 않는 기술을 포함해 호환 ODBC 드라이버가
  있는 모든 기술을 연결할 수 있습니다.

!!! note "인터페이스에서 달라진 점"

    **Use ODBC** 스위치와 별도의 호스트, 포트, 데이터베이스, 사용자, 비밀번호 필드는 더 이상 존재하지
    않습니다. 아직 ODBC를 사용하지 않는 연결은 다시 동작하려면 ODBC 속성을 입력해야 합니다.
    [데이터베이스 연결 만들기](#create-a-database-connection)를 참조하세요.

---

## 기술별 가이드 {: #technology-guides }

속성 이름은 드라이버마다 다르며, 각 기술에는 다른 기술에 없는 세부 사항이 한두 가지씩 있습니다.
아래 가이드에서 그 부분을 다루고, 이 페이지에서는 모든 기술에 공통인 *digna* 측 설정을 다룹니다.

!!! important "가이드의 속성 세트는 예시입니다"

    각 가이드는 정상 동작이 확인된 조합 하나, 즉 *digna*가 테스트한 조합을 보여 줍니다. 이는 사양이
    아니라 출발점입니다. 속성은 ODBC 드라이버에 속하므로, 어떤 속성이 있고 이름이 무엇이며 어떤 값을
    허용하는지는 드라이버 버전과 공급업체, Windows·Linux·macOS 간에 다르고, 인증 방식, TLS, 게이트웨이,
    포트 등 소스 서버의 구성에 따라서도 달라집니다. 값 한두 개는 조정해야 할 수 있으며, 설치한 드라이버
    버전의 문서를 기준으로 삼으세요.

| 기술 | 가이드 | 알아 둘 점 |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | 서버리스 풀은 호스트 이름에 `-ondemand`가 필요하며 *Standard* 프로파일링만 지원합니다 |
| **Databricks** | [Databricks](databricks_connector_guide.md) | 토큰 인증: `UID=token`, `PWD`에 PAT |
| **Apache Hive** | [Hive](hive_connector_guide.md) | 카탈로그는 쿼리가 아니라 드라이버에서 가져옵니다 |
| **Netezza** | [Netezza](netezza_connector_guide.md) | 드라이버 이름을 중괄호로 감쌉니다: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ`에는 전체 연결 디스크립터 또는 `tnsnames.ora` 별칭을 사용합니다 |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode`는 서버의 요구 사항과 일치해야 합니다 |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | 프로그래매틱 액세스 토큰이 테스트된 인증 방식입니다 |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE`가 *digna*가 볼 수 있는 스키마를 결정합니다 |
| **Teradata** | [Teradata](teradata_connector_guide.md) | 호스트는 `DBCNAME`에 입력하며, 데이터베이스가 스키마 역할을 합니다 |

---

## 사전 요구 사항: digna 호스트에 ODBC 드라이버 설치 {: #install-the-driver }

*digna*는 브라우저가 아니라 **digna 백엔드가 실행되는 서버**에서 소스 연결을 엽니다. 따라서 ODBC
드라이버는 해당 머신에 설치되어야 하며, 드라이버 이름이 로컬 드라이버 관리자에 등록되어 있어야
합니다.

=== "Windows"

    공급업체의 64비트 드라이버를 설치한 다음 **ODBC Data Source Administrator (64-bit)**를 열고
    **Drivers** 탭으로 전환합니다. 여기에 나열된 이름이 바로 `Driver` 속성에 사용할 수 있는
    값입니다.

=== "Linux"

    **unixODBC**와 공급업체의 드라이버를 설치한 다음, 등록된 드라이버 이름을 나열합니다:

    ```bash
    odbcinst -q -d
    ```

    대괄호 안에 출력되는 이름이 `Driver` 속성에 사용할 수 있는 값입니다. 이 이름은
    `/etc/odbcinst.ini`(또는 `odbcinst -j`가 알려 주는 파일)에서 가져옵니다.

=== "macOS"

    **unixODBC**(예: `brew install unixodbc`)와 공급업체의 드라이버를 설치한 다음, 등록된 드라이버
    이름을 나열합니다:

    ```bash
    odbcinst -q -d
    ```

!!! warning "드라이버 이름은 한 글자도 틀림없이 일치해야 합니다"

    `Driver`는 변경 없이 드라이버 관리자에 전달됩니다. 드라이버 관리자에게 `Simba Spark ODBC Driver`와
    `Simba Spark ODBC Driver 64`는 서로 다른 드라이버이며, 등록되지 않은 이름을 사용하면 DSN을 사용하지
    않는데도 *data source name not found* 오류가 발생합니다.

등록된 이름 대신 일반적인 드라이버 관리자는 모두 드라이버 라이브러리의 전체 경로도 허용합니다. 예:
`Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. 드라이버가 설치되었지만 등록되지 않은
경우에 유용합니다.

---

## 데이터베이스 연결 만들기 {: #create-a-database-connection }

**Admin Panel**을 열고 **Database Connections** 탭으로 이동한 다음 **Add DB Connection**을
클릭합니다. 화면에서는 다섯 가지를 입력합니다:

| 필드 | 설명 |
|---|---|
| **Name** | 연결의 이름입니다. 다른 화면에서 연결을 참조할 때 사용됩니다. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake 또는 Hive. *digna*가 생성하는 SQL 방언을 선택하므로, 드라이버가 아니라 소스와 일치해야 합니다. Azure Synapse Analytics는 **SQL Server** 연결입니다. |
| **ODBC Properties** | [ODBC 속성](#odbc-properties)에 설명된 키/값 쌍. |
| **Profiling Mode** | *Standard*, *Permanent* 또는 *Session* — [프로파일링 모드와 Work Schema](#profiling-mode-and-work-schema)를 참조하세요. |
| **Work Schema** | *Permanent* 프로파일링의 작업 테이블을 보관하는 스키마. |

연결은 중앙에서 관리된 후 하나 이상의 프로젝트에 할당되므로, 같은 연결을 여러 프로젝트에서 사용할
수 있습니다.

---

## ODBC 속성 {: #odbc-properties }

속성마다 **Add Property**를 클릭하고 **Key**, **Value**를 입력하며, 비밀 값의 경우 **Encrypted**
체크박스를 선택합니다. 각 기술 가이드에는 해당 기술의 예시 속성 세트가 나와 있으며, 이를 사용 중인
드라이버 버전과 서버에 맞게 조정합니다. [위의 참고 사항](#technology-guides)을 참조하세요.

드라이버와 관계없이 속성 세트는 다음 네 가지를 포함합니다:

- **`Driver`** — [위에서](#install-the-driver) 설명한 등록된 드라이버 이름.
- **서버 주소** — 키는 드라이버마다 다릅니다: `SERVER`, `HOST`, `DBCNAME`, `Server`, 또는
  Oracle의 경우 `DBQ` 연결 디스크립터.
- **자격 증명** — 보통 `UID`와 `PWD`입니다. Snowflake는 `UID`와 `token`을 사용하고, Databricks는
  문자 그대로의 사용자 `token`과 `PWD`의 개인 액세스 토큰을 사용합니다.
- **작업할 데이터베이스 또는 카탈로그** (기술에 해당 개념이 있는 경우) —
  [연결이 보는 데이터베이스](#which-database-the-connection-sees)를 참조하세요.

연결 풀링, 소켓 시간 제한, Kerberos 설정, 프록시 설정 등 드라이버 문서에 나온 다른 항목도 같은
방식으로 추가할 수 있습니다. *digna*는 속성을 해석하지 않고 그대로 전달하기만 합니다.

!!! warning "값은 이스케이프되지 않습니다 — 세미콜론이 있으면 중괄호로 감싸세요"

    속성은 `;`로 연결되므로, 값 자체에 `;`가 포함되어 있으면 연결 문자열이 엉뚱한 위치에서
    나뉩니다. 이런 값은 중괄호로 감쌉니다: `PWD={p@ss;word}`. `=`나 앞쪽 공백이 있는 값에도 마찬가지로
    적용됩니다. 일부 드라이버 이름을 `{NetezzaSQL}`이나 `{SnowflakeDSIIDriver}`처럼 관례적으로
    중괄호로 감싸 쓰는 것도 이 때문입니다.

---

## 속성 값 암호화 {: #encrypting-property-values }

`PWD`, `token`, 클라이언트 시크릿 등 비밀 값을 담은 모든 속성에 **Encrypted**를 선택합니다. 그러면
값은 *digna* 리포지토리에 저장되기 전에 암호화되고, 화면에서는 마스킹되며, 연결 문자열을 조합할
때만 복호화됩니다.

!!! tip "팁"

    암호화된 값은 UI나 API를 통해 다시 읽을 수 없으며, 교체만 할 수 있습니다. 비밀 값은 별도로
    자체 비밀번호 관리자에도 보관하세요.

드라이버 이름, 호스트, 포트, 데이터베이스처럼 비밀이 아닌 속성은 암호화하지 않는 것이 좋습니다.
그래야 나중에 연결을 관리하는 사람이 읽을 수 있습니다.

---

## 연결 테스트 {: #testing-a-connection }

저장하기 **전에** *Add DB Connection* 대화 상자에서 **Test**를 클릭합니다. 테스트는 현재 양식에
입력된 값으로 실제 연결을 수행하므로, 잘못된 드라이버 이름, 거부된 비밀번호, 연결할 수 없는 호스트
등 검사 시 발생할 문제를 정확히 보고합니다. 아무것도 저장되지 않으며, 테스트 연결은 성공 여부와
관계없이 롤백됩니다.

이미 있는 연결의 경우 **Database Connections** 탭에서 해당 행에 마우스를 올리고 **plug** 아이콘을
클릭하면 다시 테스트할 수 있습니다. 비밀번호 교체나 방화벽 변경 후 소스에 연결할 수 있는지 가장
빠르게 확인하는 방법입니다.

---

## 연결이 보는 데이터베이스 {: #which-database-the-connection-sees }

데이터 소스를 추가하면 *digna*는 연결이 접근할 수 있는 카탈로그, 스키마, 테이블을 제공합니다. 그
범위는 기술에 따라 다릅니다:

| 기술 | 제공되는 카탈로그 |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | 연결의 **현재** 데이터베이스만 |
| **Teradata**, **Netezza**, **Databricks** | 사용자가 볼 수 있는 모든 데이터베이스 또는 카탈로그 |
| **Hive**, **Impala** | 드라이버가 보고하는 항목 |

!!! important "하나의 연결, 하나의 데이터베이스"

    PostgreSQL, SQL Server, Oracle, Snowflake의 경우 속성은 소스 스키마가 있는 데이터베이스를 가리켜야
    합니다(`DATABASE=…`, `Database=…`, 또는 Oracle `DBQ` 안의 서비스 이름). 다른 데이터베이스의
    테이블은 해당 연결로 접근할 수 없으므로, 그 데이터베이스용 두 번째 연결을 추가하세요.

---

## 프로파일링 모드와 Work Schema {: #profiling-mode-and-work-schema }

프로파일링 모드는 *digna*가 데이터를 처리하고 메트릭을 계산하는 방식을 결정합니다:

- **Standard:** 데이터를 복사하지 않고 소스 테이블에서 직접 메트릭을 계산합니다.
- **Permanent:** 검사 대상일의 데이터를 영구 테이블로 복사하고, 복사된 데이터에서 메트릭을
  계산합니다.
- **Session:** 데이터를 세션 테이블 또는 임시 테이블로 복사하고, 이 임시 데이터에서 메트릭을
  계산합니다.

모드에 따라 연결 사용자에게 필요한 권한이 달라집니다:

| 모드 | 쓰기 대상 | 연결 사용자에게 필요한 권한 |
|---|---|---|
| **Standard** | 없음 | 소스 테이블 읽기 |
| **Permanent** | **Work Schema**에 데이터 소스당 테이블 하나 | **Work Schema**에서 테이블 생성 및 삭제 |
| **Session** | 세션이 끝나면 데이터베이스가 삭제하는 임시 테이블 | 임시 테이블 생성 — **Work Schema**는 사용되지 않습니다 |

*Standard*는 읽기만 하므로, *digna*에 읽기 전용 액세스가 부여된 경우 선택할 모드입니다.
**Work Schema**는 *Permanent*에서만 사용되지만, 나중에 모드를 변경해도 연결이 계속 동작하도록
입력해 두는 것이 좋습니다.

---

## DSN 사용하기 {: #using-a-dsn-instead }

DSN도 여전히 사용할 수 있습니다. `DSN`은 또 하나의 속성일 뿐입니다:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN은 *digna* 호스트에서 *digna* 백엔드를 실행하는 것과 같은 사용자 계정에 대해 등록되어야 하며,
*digna*가 서비스로 실행되는 경우에는 **System DSN**으로 등록되어야 합니다. DSN에 구성된 모든 항목은
속성으로 추가하여 재정의할 수도 있습니다.

DSN 없는 방식이 문서화된 기본값인 이유는 이러한 호스트 측 상태를 피할 수 있기 때문입니다. 연결이
*digna* 안에서 완전히 기술되므로, 새 *digna* 호스트에는 드라이버만 설치하면 되고 별도로 구성할
것이 없습니다.

---

## 문제 해결 {: #troubleshooting }

### Data source name not found / no default driver specified

**증상:**
- DSN 없는 설정인데도 **Test** 버튼이 *data source name not found*를 언급하는 오류를 보고합니다

**원인 및 해결 방법:**
1. `Driver` 값이 등록된 드라이버 이름과 일치하지 않습니다 — *ODBC Data Source Administrator (64-bit)*의
   **Drivers** 탭 또는 `odbcinst -q -d`의 결과와 비교하세요
2. 드라이버가 사용자의 워크스테이션에는 설치되어 있지만 *digna* 호스트에는 설치되어 있지 않습니다
3. *digna*는 64비트인데 드라이버가 32비트입니다 — 64비트 드라이버를 설치하세요
4. `Driver` 속성이 아예 없고, `DSN`도 지정되지 않았습니다
5. Linux와 macOS에서 드라이버가 설치되었지만 등록되지 않았습니다 — 대신 드라이버 라이브러리의 전체
   경로를 지정하거나 `odbcinst.ini`에 등록하세요

---

### 연결 테스트 시간 초과

**증상:**
- **Test**가 멈춘 후 약 30초 뒤에 실패합니다

**원인 및 해결 방법:**
1. *digna* 호스트에서 호스트 또는 포트에 연결할 수 없습니다 — 방화벽과, 클라우드 소스의 경우 IP
   허용 목록을 확인하세요
2. 호스트 이름은 맞지만 포트가 다른 서비스에 속해 있습니다
3. 소스가 연결을 수락하는 데 기본값인 30초보다 오래 걸립니다 — `config.toml`의 `[base]` 섹션에서
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC`를 늘리고(`0`은 무기한 대기) 백엔드를 다시 시작하세요
4. 서버리스 엔드포인트가 유휴 상태에서 재개되는 중입니다 — 다시 시도하고, 이런 일이 자주 발생하면
   위와 같이 로그인 시간 제한을 늘리세요

---

### 자격 증명이 올바른데도 인증 실패

**증상:**
- 드라이버가 잘못된 자격 증명이라고 보고하지만, 같은 사용자로 다른 SQL 클라이언트에서는 동작합니다

**원인 및 해결 방법:**
1. 비밀번호에 `;`가 포함되어 있습니다 — 값을 중괄호로 감싸세요: `{p@ss;word}`
2. 값에 뒤쪽 공백이 함께 복사되었습니다
3. 드라이버가 특정 인증 메커니즘을 요구합니다 — 예를 들어 Hive와 Databricks 드라이버의 `AuthMech`,
   Snowflake의 `authenticator`
4. 값을 암호화하여 저장한 후 편집했습니다 — 암호화된 값은 다시 읽을 수 없으므로 비밀 값을 처음부터
   다시 입력하세요
5. 토큰이 만료되었습니다 — 개인 액세스 토큰과 프로그래매틱 액세스 토큰은 만료일과 함께 발급됩니다

---

### 데이터 소스 화면에 예상한 데이터베이스나 스키마가 표시되지 않음

**증상:**
- 데이터 소스를 추가할 때 카탈로그, 스키마 또는 테이블이 누락되어 있습니다

**원인 및 해결 방법:**
1. 연결이 다른 데이터베이스를 가리키고 있습니다 —
   [연결이 보는 데이터베이스](#which-database-the-connection-sees)를 참조하세요
2. 연결 사용자에게 스키마 또는 데이터 딕셔너리에 대한 읽기 권한이 없습니다
3. **Technology**가 소스와 일치하지 않아 *digna*가 잘못된 데이터 딕셔너리를 조회합니다
4. Snowflake의 경우 사용자에게 기본 웨어하우스가 할당되어 있지 않고 `Warehouse` 속성도 지정되지 않아
   메타데이터 쿼리를 실행할 수 없습니다

---

### 연결 테스트는 성공하지만 프로파일링이 실패함

**증상:**
- **Test**는 통과하지만 작업 테이블을 만들 때 검사가 실패합니다

**원인 및 해결 방법:**
1. *Permanent* 프로파일링이 선택되어 있는데 연결 사용자가 **Work Schema**에 테이블을 만들 수
   없습니다 — 권한을 부여하거나 *Session* 또는 *Standard*로 전환하세요
2. *Permanent* 프로파일링이 선택되어 있는데 **Work Schema**가 비어 있거나 존재하지 않는 스키마를
   지정하고 있습니다
3. *Session* 프로파일링이 선택되어 있는데 연결 사용자가 임시 테이블을 만들 수 없습니다
4. 오래 실행되는 프로파일링 쿼리가 쿼리 시간 제한에 걸립니다 — `config.toml`의 `[base]` 섹션에서
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC`를 늘리세요(기본값 3600초, `0`은 시간 제한 해제)

---

## 모범 사례

**권장 사항:**

- 연결을 구성하기 전에 *digna* 호스트에 드라이버를 설치하고 등록하세요
- 모든 비밀번호와 토큰에 **Encrypted**를 선택하세요
- 저장하기 전에 **Test**를 클릭하고, 비밀번호를 교체한 후 다시 테스트하세요
- 연결 이름은 소스와 환경에 따라 지정하세요. 예: `sales_dwh_prod`
- *digna*에 전용 데이터베이스 사용자를 제공하고, *Standard* 프로파일링으로 충분한 경우 읽기 전용으로
  설정하세요
- 소스 데이터베이스마다 연결을 하나씩 두고, 기존 연결을 바꾸기보다는 두 번째 연결을 추가하세요

**금지 사항:**

- 비밀 값을 암호화하지 않고 저장하거나, 하나의 데이터베이스 사용자를 *digna*와 다른 도구가 공유하지
  마세요
- 64비트 *digna* 설치에 32비트 드라이버를 사용하지 마세요
- *digna*가 서비스로 실행될 때 User DSN에 의존하지 마세요 — 표시되지 않습니다
- `;`가 포함된 값을 중괄호 없이 속성에 넣지 마세요
- **Work Schema**가 소스 데이터를 보관하는 스키마를 가리키게 하지 마세요

---

## 지원

데이터베이스 연결에 도움이 필요하신가요?

- **이메일:** support@digna.ai
- **문서:** https://docs.digna.ai
- **웹사이트:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**

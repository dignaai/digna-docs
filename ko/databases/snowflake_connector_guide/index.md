# Snowflake용 소스 커넥터

이 가이드는 **DSN 없는(DSN-less)** 연결 문자열을 사용하여 **ODBC**로 Snowflake에 연결하도록
*digna*를 구성하는 방법을 설명합니다.

설정 중 *digna* 측 부분은 모든 기술에서 동일합니다. 연결을 만드는 위치, 속성 값을 암호화하는 방법,
연결을 테스트하는 방법, 프로파일링 모드의 의미가 여기에 해당하며
[데이터베이스 연결 개요](overview.md)에 설명되어 있습니다. 이 페이지에서는 Snowflake에만 해당하는
내용을 다룹니다.

---

## 1. ODBC 드라이버 설치 {: #1-install-the-odbc-driver }

[Snowflake 설치 가이드](https://docs.snowflake.com/en/developer-guide/odbc/odbc)에 따라
*digna* 백엔드가 실행되는 머신에 **Snowflake ODBC Driver**를 설치합니다.

드라이버는 **SnowflakeDSIIDriver**라는 이름으로 등록됩니다.
[digna 호스트에 ODBC 드라이버 설치](overview.md#install-the-driver)에 설명된 대로 호스트에서
등록된 정확한 이름을 확인합니다.

---

## 2. ODBC 속성 {: #2-odbc-properties }

Snowflake에는 **프로그래매틱 액세스 토큰(PAT)**으로 연결합니다. 이는 *digna*가 검증된 인증
방식이며, 비밀번호만으로 로그인하는 것이 차단된 계정에서 Snowflake가 요구하는 방식입니다.

!!! important "사양이 아닌 예시"

    아래 속성 세트는 정상 동작이 확인된 조합 중 하나입니다. 이 속성들은 Snowflake ODBC 드라이버에
    속하므로 이름, 기본값, 허용되는 값이 드라이버 버전과 플랫폼마다 다르며, 계정에서 어떤 인증 옵션을
    허용하는지는 계정의 보안 정책에 따라 결정됩니다. 이를 출발점으로 삼고, 설치한 드라이버 버전의
    문서를 확인하세요.

| 키 | 예시 값 | 참고 |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | *digna* 호스트에 등록된 드라이버 이름과 일치해야 합니다 |
| `Server` | `<account>.snowflakecomputing.com` | 계정 식별자와 접미사, 예: `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | 토큰이 속한 Snowflake 사용자 |
| `Database` | `TEST` | 소스 스키마가 있는 데이터베이스입니다. 이 연결로 프로파일링할 수 있는 유일한 데이터베이스입니다 |
| `Schema` | `PUBLIC` | 세션의 기본 스키마 |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | 토큰 인증을 선택합니다 |
| `token` | `<programmatic access token>` | **Encrypted**를 선택합니다 |

결과 연결 문자열은 다음과 같습니다:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### 웨어하우스와 역할

쿼리를 실행하려면 웨어하우스가 필요합니다. *digna* 사용자에게 기본 웨어하우스와 기본 역할이 있으면
세션이 이를 사용하므로 별도로 구성할 필요가 없습니다. 그렇지 않으면 다음을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | 프로파일링 쿼리를 실행하는 웨어하우스 |
| `Role` | `DIGNA_READER` | 세션이 권한을 사용하는 역할 |

!!! tip "digna 전용 웨어하우스를 제공하세요"

    자동 일시 중단되는 별도의 작은 웨어하우스를 사용하면 프로파일링 비용을 파악하기 쉽고, *digna*가
    대화형 사용자와 컴퓨팅 자원을 두고 경쟁하지 않습니다.

### 비밀번호 인증

계정에서 아직 허용하는 경우 토큰 대신 비밀번호를 사용할 수 있습니다. `authenticator`와 `token`을
제거하고 다음을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `PWD` | `<password>` | **Encrypted**를 선택합니다 |

---

## 3. *digna* 구성 {: #3-digna-configuration }

**Add DB Connection** 화면에서 다음을 입력합니다:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Snowflake 관련 참고 사항 {: #4-notes-on-snowflake }

- **토큰은 만료됩니다.** 프로그래매틱 액세스 토큰은 유효 기간을 두고 발급되며, 만료되는 날
  프로파일링이 중단됩니다. 토큰을 만들 때 만료일을 기록해 두고, 새 토큰을 `token` 속성에 다시
  입력하세요. 암호화된 값은 교체할 수는 있지만 다시 읽을 수는 없습니다.
- **하나의 연결은 하나의 데이터베이스만 봅니다.** Snowflake는 현재 데이터베이스만 카탈로그로
  보고하므로, *digna*는 `Database`에 지정된 데이터베이스의 스키마를 제공합니다. 다른 데이터베이스에
  있는 소스 테이블에는 별도의 연결이 필요합니다.
- **식별자는 대문자입니다.** 따옴표로 묶어 생성하지 않은 한 식별자는 대문자입니다. *digna*는
  Snowflake가 보고하는 이름을 그대로 사용합니다.
- **프로파일링 모드.** *Permanent*는 **Work Schema**에 작업 테이블을 만들므로 역할에 그곳에 대한
  `CREATE TABLE` 권한이 필요합니다. *Session*은 `CREATE TEMPORARY TABLE`을 사용하며
  **Work Schema**를 건드리지 않습니다. *Standard*는 읽기 권한만 필요하며, 쓰기 권한은 전혀 필요하지
  않습니다.

---

## 5. 드라이버 확인(선택 사항) {: #5-verifying-the-driver-optional }

DSN 없는 연결에는 ODBC 데이터 소스를 구성할 필요가 없지만, 드라이버 자체의 대화 상자를 사용하면
*digna*에 값을 입력하기 전에 드라이버, 계정 URL, 자격 증명이 동작하는지 간편하게 확인할 수
있습니다.

#### 1단계
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

참고:

- **Server** 값은 Snowflake 계정 식별자 뒤에 `.snowflakecomputing.com`을 붙인 것입니다.
- 여기에 입력하는 **Database**, **Schema**, **Warehouse**는 [섹션 2](#2-odbc-properties)의
  `Database`, `Schema`, `Warehouse` 속성에 해당합니다.

#### 2단계 – 연결 테스트

**TEST** 버튼을 클릭합니다. 연결에 성공하면 다음과 같이 표시됩니다:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)
# PostgreSQL용 소스 커넥터

이 가이드는 **DSN 없는(DSN-less)** 연결 문자열을 사용하여 **ODBC**로 PostgreSQL에 연결하도록
*digna*를 구성하는 방법을 설명합니다.

설정 중 *digna* 측 부분은 모든 기술에서 동일합니다. 연결을 만드는 위치, 속성 값을 암호화하는 방법,
연결을 테스트하는 방법, 프로파일링 모드의 의미가 여기에 해당하며
[데이터베이스 연결 개요](overview.md)에 설명되어 있습니다. 이 페이지에서는 PostgreSQL에만 해당하는
내용을 다룹니다.

---

## 1. ODBC 드라이버 설치 {: #1-install-the-odbc-driver }

공급업체의 공식 설치 가이드에 따라 *digna* 백엔드가 실행되는 머신에 PostgreSQL ODBC 드라이버
(**psqlODBC**)를 설치합니다.

드라이버는 플랫폼과 패키지에 따라 다른 이름으로 등록됩니다. 일반적으로 Windows에서는
**PostgreSQL Unicode(x64)**, Linux에서는 **PostgreSQL ODBC Driver(UNICODE)**입니다.
[digna 호스트에 ODBC 드라이버 설치](overview.md#install-the-driver)에 설명된 대로 호스트에서
정확한 이름을 확인하고, 아래 `DRIVER` 속성에 그 이름을 사용합니다.

---

## 2. ODBC 속성 {: #2-odbc-properties }

!!! important "사양이 아닌 예시"

    아래 속성 세트는 정상 동작이 확인된 조합 중 하나입니다. 이 속성들은 psqlODBC 드라이버에 속하므로
    이름, 기본값, 허용되는 값이 드라이버 버전과 플랫폼마다 다르며, 서버가 요구하는 사항(특히 SSL)도
    다를 수 있습니다. 이를 출발점으로 삼고, 설치한 드라이버 버전의 문서를 확인하세요.

**Add DB Connection** 화면에서 다음 속성을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | *digna* 호스트에 등록된 드라이버 이름과 일치해야 합니다 |
| `SERVER` | `db.example.com` | 서버 이름 또는 IP 주소 |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | 소스 스키마가 있는 데이터베이스입니다. 이 연결로 프로파일링할 수 있는 유일한 데이터베이스입니다 |
| `UID` | `digna_source_user` | 데이터베이스 사용자 |
| `PWD` | `<password>` | **Encrypted**를 선택합니다 |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` 또는 `verify-full` — 서버가 허용하는 값이어야 합니다 |

결과 연결 문자열은 다음과 같습니다:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

그 밖의 psqlODBC 옵션도 추가 속성으로 넣을 수 있습니다. 예를 들어 읽기 전용 세션에는
`ReadOnly=1`을, 연결 시 `SET` 문을 실행하려면 `ConnSettings`를 사용합니다.

---

## 3. *digna* 구성 {: #3-digna-configuration }

**Add DB Connection** 화면에서 다음을 입력합니다:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. PostgreSQL 관련 참고 사항 {: #4-notes-on-postgresql }

- **`SSLMode`는 서버와 일치해야 합니다.** `hostssl`로 구성된 서버는 `SSLMode=disable`을
  거부하며, `verify-ca` 또는 `verify-full`을 사용하려면 *digna* 호스트의 드라이버가 루트 인증서에
  접근할 수 있어야 합니다. 드라이버를 테스트할 때 특정 모드를 선택해야 했다면 여기서도 같은 모드를
  사용하세요.
- **하나의 연결은 하나의 데이터베이스만 봅니다.** PostgreSQL은 현재 데이터베이스만 카탈로그로
  보고하므로, *digna*는 `DATABASE`에 지정된 데이터베이스의 스키마를 제공합니다. 다른 데이터베이스에
  있는 소스 테이블에는 별도의 연결이 필요합니다.
- **프로파일링 모드.** *Permanent*는 **Work Schema**에 작업 테이블을 만들므로 사용자에게 해당
  스키마에 대한 `CREATE` 권한이 필요합니다. *Session*은 `CREATE TEMPORARY TABLE`을 사용하며
  **Work Schema**를 건드리지 않습니다. *Standard*는 읽기 권한만 필요합니다.

---

## 5. 드라이버 확인(선택 사항) {: #5-verifying-the-driver-optional }

DSN 없는 연결에는 ODBC 데이터 소스를 구성할 필요가 없지만, 드라이버 자체의 대화 상자를 사용하면
*digna*에 값을 입력하기 전에 드라이버가 동작하는지, 서버가 자격 증명과 SSL 모드를 허용하는지
간편하게 확인할 수 있습니다.

#### 1단계
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### 2단계 – 연결 테스트

**Test Connection** 버튼을 클릭합니다.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

여기에 입력한 값이 바로 [섹션 2](#2-odbc-properties)의 속성에 들어가는 값입니다.
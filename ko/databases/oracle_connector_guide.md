# Oracle용 소스 커넥터

이 가이드는 **DSN 없는(DSN-less)** 연결 문자열을 사용하여 **ODBC**로 Oracle Database에
연결하도록 *digna*를 구성하는 방법을 설명합니다.

설정 중 *digna* 측 부분은 모든 기술에서 동일합니다. 연결을 만드는 위치, 속성 값을 암호화하는 방법,
연결을 테스트하는 방법, 프로파일링 모드의 의미가 여기에 해당하며
[데이터베이스 연결 개요](overview.md)에 설명되어 있습니다. 이 페이지에서는 Oracle에만 해당하는
내용을 다룹니다.

---

## 1. ODBC 드라이버 설치 {: #1-install-the-odbc-driver }

Oracle ODBC 드라이버는 **Oracle Client**에 포함되어 있습니다(Instant Client "ODBC" 패키지로
충분합니다). 공급업체의 공식 설치 가이드에 따라 *digna* 백엔드가 실행되는 머신에 설치합니다.

드라이버는 **Oracle in `<OracleHomeName>`** 형식의 이름으로 등록됩니다. 예:
`Oracle in OraDB21Home1` 또는 `Oracle in instantclient_21_13`. 홈 이름은 설치마다 다르므로
[digna 호스트에 ODBC 드라이버 설치](overview.md#install-the-driver)에 설명된 대로 호스트에서
정확한 이름을 확인합니다.

---

## 2. ODBC 속성 {: #2-odbc-properties }

!!! important "사양이 아닌 예시"

    아래 속성 세트는 정상 동작이 확인된 조합 중 하나입니다. 이 속성들은 Oracle ODBC 드라이버에
    속하므로 이름, 기본값, 허용되는 값이 클라이언트 버전마다 다르며, 특히 드라이버 이름은 호스트의
    Oracle 홈에 따라 달라집니다. 이를 출발점으로 삼고, 설치한 클라이언트 버전의 문서를 확인하세요.

**Add DB Connection** 화면에서 다음 속성을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | *digna* 호스트에 등록된 드라이버 이름과 일치해야 합니다 |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | 연결할 데이터베이스 — 아래 참조 |
| `UID` | `DIGNA_SOURCE_USER` | 데이터베이스 사용자 |
| `PWD` | `<password>` | **Encrypted**를 선택합니다 |

결과 연결 문자열은 다음과 같습니다:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### `DBQ` 값

`DBQ`는 세 가지 형식을 허용합니다. *digna* 입장에서는 모두 동일하며, *digna* 호스트에서 무엇을
구성해야 하는지만 다릅니다:

| 형식 | 예시 | 필요 사항 |
|---|---|---|
| **전체 연결 디스크립터** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | 없음 — 모든 정보가 속성 안에 있습니다. 권장 |
| **TNS 별칭** | `DIGNA_SOURCE` | *digna* 호스트에 있는 Oracle Client의 `tnsnames.ora`에 별칭이 있어야 합니다 |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Easy Connect를 지원하는 Oracle Client(12c 이상) |

!!! tip "전체 디스크립터를 권장합니다"

    TNS 별칭을 사용하면 연결 정의의 절반이 *digna* 호스트의 파일로 옮겨지는데, 호스트를 다시 구축하거나
    *digna*를 이전할 때 이를 잊기 쉽습니다. 전체 디스크립터를 사용하면 연결이 자체적으로 완결되며,
    이것이 바로 DSN 없는 설정의 목적입니다.

디스크립터의 괄호는 연결 문자열 안에서 문제가 되지 않지만, 비밀번호에 `;`가 포함되어 있다면
중괄호로 감싸세요: `PWD={p@ss;word}`.

---

## 3. *digna* 구성 {: #3-digna-configuration }

**Add DB Connection** 화면에서 다음을 입력합니다:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Oracle 관련 참고 사항 {: #4-notes-on-oracle }

- **스키마는 사용자입니다.** *digna*는 Oracle 사용자를 스키마로 나열하므로, 소스 스키마는 테이블의
  소유자(위의 예에서는 `DIGNA_SOURCE_USER`)입니다. 연결 사용자에게는 직접 또는 롤을 통해 해당
  테이블에 대한 `SELECT` 권한이 필요합니다.
- **하나의 연결은 하나의 데이터베이스만 봅니다.** *digna*가 제공하는 카탈로그는 연결이 붙어 있는
  데이터베이스이므로, `DBQ`가 어떤 서비스, 즉 어떤 데이터베이스를 프로파일링할지 결정합니다.
- **따옴표로 묶인 식별자는 대소문자를 구분합니다.** *digna*는 데이터 딕셔너리에서 읽은 이름, 즉
  Oracle이 저장한 이름(따옴표 없이 만든 객체는 대문자)을 따옴표로 묶어 사용합니다.
- **프로파일링 모드.** *Permanent*는 **Work Schema**에 작업 테이블을 만들므로 사용자에게 그곳에
  대한 `CREATE TABLE` 권한과 테이블스페이스 할당량이 필요합니다. *Session*은 프라이빗 임시 테이블
  (`ORA$PTT_…`, Oracle 18c 이상)을 사용하며 **Work Schema**를 건드리지 않습니다. *Standard*는
  읽기 권한만 필요합니다.

---

## 5. 드라이버 확인(선택 사항) {: #5-verifying-the-driver-optional }

DSN 없는 연결에는 ODBC 데이터 소스를 구성할 필요가 없지만, 드라이버 자체의 대화 상자를 사용하면
*digna*에 값을 입력하기 전에 Oracle Client, 서비스 이름, 자격 증명이 동작하는지 간편하게 확인할
수 있습니다.

#### 1단계
![Step 1](images/oracle/create_odbc_data_source_step1.png)

여기에 표시되는 **TNS Service Name**은 Oracle Client 설치의 `tnsnames.ora`에서 가져옵니다.
별칭과 함께 호스트, 포트, 서비스 이름이 정의되는 곳이 바로 이 파일입니다. *digna*에서는 이 별칭을
`DBQ`로 사용하거나, 대신 전체 디스크립터를 사용할 수 있습니다.

#### 2단계 – 연결 테스트

**Test Connection** 버튼을 클릭합니다.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

비밀번호를 입력하고 **OK** 버튼을 클릭합니다.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

성공 메시지가 표시되면 드라이버와 자격 증명이 정상 동작하는 것입니다.
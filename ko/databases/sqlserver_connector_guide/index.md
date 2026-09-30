# MS SQL Server용 소스 커넥터

이 가이드는 **DSN 없는(DSN-less)** 연결 문자열을 사용하여 **ODBC**로 Microsoft SQL Server에
연결하도록 *digna*를 구성하는 방법을 설명합니다.

설정 중 *digna* 측 부분은 모든 기술에서 동일합니다. 연결을 만드는 위치, 속성 값을 암호화하는 방법,
연결을 테스트하는 방법, 프로파일링 모드의 의미가 여기에 해당하며
[데이터베이스 연결 개요](overview.md)에 설명되어 있습니다. 이 페이지에서는 SQL Server에만 해당하는
내용을 다룹니다.

!!! note "Azure Synapse Analytics"

    Synapse도 SQL Server 연결로 구성하지만, 호스트 이름이 다르고 몇 가지 추가로 고려할 사항이
    있습니다. [Azure Synapse](azure_synapse_connector_guide.md)를 참조하세요.

---

## 1. ODBC 드라이버 설치 {: #1-install-the-odbc-driver }

[Microsoft 설치 가이드](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)에
따라 *digna* 백엔드가 실행되는 머신에 **ODBC Driver 18 for SQL Server**를 설치합니다.

Windows에 **SQL Server**라는 이름으로 기본 제공되는 드라이버도 동작하지만, 오래전에 대체된
드라이버로 최신 TLS 설정과 Azure 인증을 모두 지원하지 않습니다. 현재 드라이버를 설치할 수 없는
경우에만 사용하세요.

[digna 호스트에 ODBC 드라이버 설치](overview.md#install-the-driver)에 설명된 대로 호스트에서
등록된 정확한 드라이버 이름을 확인합니다.

---

## 2. ODBC 속성 {: #2-odbc-properties }

!!! important "사양이 아닌 예시"

    아래 속성 세트는 정상 동작이 확인된 조합 중 하나입니다. 이 속성들은 Microsoft ODBC 드라이버에
    속하므로 이름, 기본값, 허용되는 값이 드라이버 버전마다(예를 들어 Driver 18은 Driver 17과 달리
    기본적으로 암호화합니다) 그리고 플랫폼마다 다릅니다. 이를 출발점으로 삼고, 설치한 드라이버 버전의
    문서를 확인하세요.

**Add DB Connection** 화면에서 다음 속성을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | *digna* 호스트에 등록된 드라이버 이름과 일치해야 합니다 |
| `SERVER` | `sql.example.com` | 서버 이름 또는 IP 주소입니다. 명명된 인스턴스: `host\instance`, 기본값이 아닌 포트: `host,1433` |
| `PORT` | `1433` | 포트가 이미 `SERVER`에 포함되어 있으면 생략합니다 |
| `DATABASE` | `digna_source_db` | 소스 스키마가 있는 데이터베이스입니다. 이 연결로 프로파일링할 수 있는 유일한 데이터베이스입니다 |
| `UID` | `digna_source_user` | 데이터베이스 사용자 |
| `PWD` | `<password>` | **Encrypted**를 선택합니다 |

결과 연결 문자열은 다음과 같습니다:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### ODBC Driver 18의 암호화

Driver 18은 기본적으로 연결을 암호화하고 서버 인증서를 검증합니다. *digna* 호스트가 신뢰하지 않는
인증서(일반적으로 자체 서명 인증서)를 사용하는 서버에 연결하면 인증서 체인 오류로 연결이 실패합니다.
다음을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `Encrypt` | `yes` | Driver 18의 기본값입니다. 서버가 TLS를 지원하지 않는 경우에만 `no`로 설정합니다 |
| `TrustServerCertificate` | `yes` | 인증서 검증을 건너뜁니다. 테스트 환경에서는 편리하지만, 프로덕션에서는 인증서를 설치하는 것이 좋습니다 |

### Windows 인증

SQL 로그인 대신 *digna* 서비스를 실행하는 계정으로 연결하려면 `UID`와 `PWD`를 제거하고 다음을
추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `Trusted_Connection` | `yes` | *digna* 서비스 계정에 데이터베이스 권한이 필요합니다 |

---

## 3. *digna* 구성 {: #3-digna-configuration }

**Add DB Connection** 화면에서 다음을 입력합니다:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. MS SQL Server 관련 참고 사항 {: #4-notes-on-ms-sql-server }

- **하나의 연결은 하나의 데이터베이스만 봅니다.** SQL Server는 현재 데이터베이스만 카탈로그로
  보고하므로, *digna*는 `DATABASE`에 지정된 데이터베이스의 스키마를 제공합니다. 다른 데이터베이스에
  있는 소스 테이블에는 별도의 연결이 필요합니다.
- **프로파일링 모드.** *Permanent*는 **Work Schema**에 작업 테이블을 만들므로 사용자에게 그곳에
  대한 `CREATE TABLE` 권한이 필요합니다. *Session*은 `tempdb`의 로컬 임시 테이블(`#wt_…`)을
  사용하며 **Work Schema**를 건드리지 않습니다. *Standard*는 읽기 권한만 필요합니다.
- **`SERVER`에 인스턴스와 포트가 포함됩니다.** 명명된 인스턴스를 `host\instance`로 지정하면 SQL
  Server Browser 서비스에 접근할 수 있어야 합니다. `host,port`를 사용하면 이를 피할 수 있습니다.

---

## 5. 드라이버 확인(선택 사항) {: #5-verifying-the-driver-optional }

DSN 없는 연결에는 ODBC 데이터 소스를 구성할 필요가 없지만, 드라이버 자체의 마법사를 사용하면
*digna*에 값을 입력하기 전에 드라이버가 동작하는지, 서버가 자격 증명을 허용하는지 간편하게 확인할
수 있습니다.

#### 1단계
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

**Next >** 버튼을 클릭합니다.

#### 2단계
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

인증 방식(예: 사용자 이름과 비밀번호)을 선택하고
필요한 정보를 입력합니다.

**Next >** 버튼을 클릭합니다.

#### 3단계
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

ANSI 호환 설정을 선택한 다음 **Next >** 버튼을 클릭합니다.

#### 4단계
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

기본 설정을 그대로 두거나 필요에 따라 로깅 옵션을 선택한 후
**Finish** 버튼을 클릭합니다. 

#### 5단계
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

이제 **Test datasource** 버튼을 클릭합니다.

#### 6단계
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

성공 화면이 표시되면 드라이버와 자격 증명이 정상 동작하는 것입니다. 입력한 값이 바로
[섹션 2](#2-odbc-properties)의 속성에 들어가는 값입니다.
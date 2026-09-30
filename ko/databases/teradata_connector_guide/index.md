# Teradata용 소스 커넥터

이 가이드는 **DSN 없는(DSN-less)** 연결 문자열을 사용하여 **ODBC**로 Teradata에 연결하도록
*digna*를 구성하는 방법을 설명합니다.

설정 중 *digna* 측 부분은 모든 기술에서 동일합니다. 연결을 만드는 위치, 속성 값을 암호화하는 방법,
연결을 테스트하는 방법, 프로파일링 모드의 의미가 여기에 해당하며
[데이터베이스 연결 개요](overview.md)에 설명되어 있습니다. 이 페이지에서는 Teradata에만 해당하는
내용을 다룹니다.

---

## 1. ODBC 드라이버 설치 {: #1-install-the-odbc-driver }

공급업체의 공식 설치 가이드에 따라 *digna* 백엔드가 실행되는 머신에 **ODBC Driver for Teradata**를
설치합니다.

드라이버는 이름에 버전이 포함된 형태로 등록됩니다. 예: **Teradata Database ODBC Driver 20.00**.
[digna 호스트에 ODBC 드라이버 설치](overview.md#install-the-driver)에 설명된 대로 호스트에서
등록된 정확한 이름을 확인합니다.

---

## 2. ODBC 속성 {: #2-odbc-properties }

!!! important "사양이 아닌 예시"

    아래 속성 세트는 정상 동작이 확인된 조합 중 하나입니다. 이 속성들은 Teradata ODBC 드라이버에
    속하므로 이름, 기본값, 허용되는 값이 드라이버 버전마다(버전은 드라이버 이름 자체에 포함됩니다)
    그리고 플랫폼마다 다릅니다. 이를 출발점으로 삼고, 설치한 드라이버 버전의 문서를 확인하세요.

**Add DB Connection** 화면에서 다음 속성을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | *digna* 호스트에 등록된 드라이버 이름과 일치해야 합니다 |
| `DBCNAME` | `teradata.example.com` | 서버 이름 또는 IP 주소입니다. 호스트 속성에 대한 Teradata 고유의 이름입니다 |
| `UID` | `digna_source_user` | 데이터베이스 사용자 |
| `PWD` | `<password>` | **Encrypted**를 선택합니다 |

결과 연결 문자열은 다음과 같습니다:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

유용한 추가 속성:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `MechanismName` | `TD2` | 로그온 메커니즘입니다. `TD2`가 Teradata 기본값이며, 디렉터리 인증에는 `LDAP`을 사용합니다 |
| `DefaultDatabase` | `dad` | 세션이 시작되는 데이터베이스 |
| `CharacterSet` | `UTF8` | 기본 세션 문자 집합이 비 ASCII 데이터를 손상시킬 경우 설정합니다 |

---

## 3. *digna* 구성 {: #3-digna-configuration }

**Add DB Connection** 화면에서 다음을 입력합니다:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Teradata 관련 참고 사항 {: #4-notes-on-teradata }

- **Teradata 데이터베이스는 스키마가 아니라 카탈로그입니다.** *digna*는 사용자가 볼 수 있는
  데이터베이스(`DBC.DatabasesV` 기준)를 카탈로그로 나열하며, 스키마 수준은 적용되지 않습니다. 데이터
  소스를 추가할 때 데이터베이스를 카탈로그로 선택하면 스키마는 *해당 없음*으로 표시됩니다.
- **하나의 연결로 허용된 모든 데이터베이스에 접근할 수 있으므로**, 연결이 하나의 데이터베이스에
  고정되는 기술과 달리 하나의 연결로 여러 데이터베이스에 걸친 소스를 처리할 수 있습니다.
- **Work Schema는 데이터베이스입니다.** *Permanent* 프로파일링의 경우 작업 테이블을 보관할 Teradata
  데이터베이스를 지정하고, 사용자에게 그 안에서의 `CREATE TABLE` 권한과 `PERM` 공간 할당을 부여합니다.
  perm 공간이 0인 데이터베이스에는 테이블을 만들 수 없습니다.
- **프로파일링 모드.** *Permanent*는 **Work Schema**에 테이블을 만듭니다. *Session*은 `VOLATILE`
  테이블을 사용하며, 이 테이블은 `SPOOL` 공간이 필요하지만 perm 공간이나 **Work Schema**에 대한
  권한은 필요하지 않습니다. *Standard*는 읽기 권한만 필요합니다.

---

## 5. 드라이버 확인(선택 사항) {: #5-verifying-the-driver-optional }

DSN 없는 연결에는 ODBC 데이터 소스를 구성할 필요가 없지만, 드라이버 자체의 대화 상자를 사용하면
*digna*에 값을 입력하기 전에 드라이버와 자격 증명이 동작하는지 간편하게 확인할 수 있습니다.

#### 1단계
![Step 1](images/teradata/create_odbc_data_source_step1.png)

여기의 **Name or IP address** 필드는 [섹션 2](#2-odbc-properties)의 `DBCNAME` 속성에
해당합니다.

**Test** 버튼을 클릭합니다.

#### 2단계
![Step 2](images/teradata/create_odbc_data_source_step2.png)

사용자 이름과 비밀번호를 입력한 다음 **OK** 버튼을 클릭합니다. 성공 화면이 표시되면 드라이버와
자격 증명이 정상 동작하는 것입니다.
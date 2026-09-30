# Hive용 소스 커넥터

이 가이드는 **DSN 없는(DSN-less)** 연결 문자열을 사용하여 **ODBC**로 Apache Hive에 연결하도록
*digna*를 구성하는 방법을 설명합니다.

설정 중 *digna* 측 부분은 모든 기술에서 동일합니다. 연결을 만드는 위치, 속성 값을 암호화하는 방법,
연결을 테스트하는 방법, 프로파일링 모드의 의미가 여기에 해당하며
[데이터베이스 연결 개요](overview.md)에 설명되어 있습니다. 이 페이지에서는 Hive에만 해당하는 내용을
다룹니다.

---

## 1. ODBC 드라이버 설치 {: #1-install-the-odbc-driver }

공급업체의 공식 설치 가이드에 따라 *digna* 백엔드가 실행되는 머신에
**Cloudera ODBC Driver for Apache Hive**를 설치합니다.

[digna 호스트에 ODBC 드라이버 설치](overview.md#install-the-driver)에 설명된 대로 호스트에서
등록된 정확한 드라이버 이름을 확인합니다.

---

## 2. ODBC 속성 {: #2-odbc-properties }

!!! important "사양이 아닌 예시"

    아래 속성 세트는 정상 동작이 확인된 조합 중 하나입니다. 이 속성들은 Cloudera Hive 드라이버에
    속하므로 이름, 기본값, 허용되는 값이 드라이버 버전과 플랫폼마다 다르며, HiveServer2가 무엇을
    허용하는지는 인증 메커니즘, 전송 모드, TLS, 게이트웨이 등 클러스터의 보안 구성에 전적으로 달려
    있습니다. 이를 출발점으로 삼고, 설치한 드라이버 버전의 문서를 확인하세요.

**Add DB Connection** 화면에서 다음 속성을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | *digna* 호스트에 등록된 드라이버 이름과 일치해야 합니다 |
| `HOST` | `hive.example.com` | HiveServer2 호스트 이름 또는 IP 주소 |
| `PORT` | `10000` | HiveServer2 포트, HTTP 전송의 경우 `10001` |

결과 연결 문자열은 다음과 같습니다:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### 인증

보안이 설정되지 않은 HiveServer2는 위의 세 가지 속성만으로 연결을 허용합니다. 인증이 활성화된
경우 다음을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `AuthMech` | `3` | `0` 인증 없음, `2` 사용자 이름만, `3` 사용자 이름과 비밀번호, `1` Kerberos |
| `UID` | `digna_source_user` | `AuthMech` `2` 및 `3`에서 필수 |
| `PWD` | `<password>` | `AuthMech` `3`에서 필수입니다. **Encrypted**를 선택합니다 |

Kerberos(`AuthMech=1`)의 경우 *digna* 호스트에 유효한 티켓 또는 keytab이 추가로 필요하며,
드라이버 문서에 설명된 `KrbHostFQDN`, `KrbServiceName`, `KrbRealm` 속성도 필요합니다.

### 전송 및 TLS

| 키 | 예시 값 | 참고 |
|---|---|---|
| `ThriftTransport` | `2` | `0` 바이너리(기본값, 포트 10000), `1` SASL, `2` HTTP(포트 10001, Knox 게이트웨이가 요구하는 방식) |
| `HTTPPath` | `cliservice` | `ThriftTransport=2`와 함께 사용 |
| `SSL` | `1` | HiveServer2가 TLS로 보호되는 경우 |
| `Schema` | `dignadata` | 세션이 시작되는 Hive 데이터베이스입니다. 선택 사항 — *digna*는 쿼리를 정규화된 이름으로 작성합니다 |

---

## 3. *digna* 구성 {: #3-digna-configuration }

**Add DB Connection** 화면에서 다음을 입력합니다:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Hive 관련 참고 사항 {: #4-notes-on-hive }

- **카탈로그는 드라이버에서 가져옵니다.** Hive에는 자체 카탈로그가 없으므로 *digna*는 드라이버가
  보고하는 값(일반적으로 `HIVE`라는 단일 항목)을 사용하고, 그 아래에 Hive 데이터베이스를 스키마로
  나열합니다.
- **Work Schema는 Hive 데이터베이스입니다.** *Permanent* 프로파일링을 하려면 사용자에게 그 안에서
  테이블을 만들고 삭제할 권한이 필요하며, 기반 스토리지 위치에 쓰기가 가능해야 합니다.
- **프로파일링 모드.** *Permanent*는 **Work Schema**에 작업 테이블을 만듭니다. *Session*은
  `CREATE TEMPORARY TABLE`을 사용하므로 임시 테이블을 지원하는 HiveServer2가 필요하며,
  **Work Schema**를 건드리지 않습니다. *Standard*는 읽기 권한만 필요하며, *digna*에 쓰기 권한이
  전혀 없는 클러스터에서 선택해야 하는 모드입니다.
- **프로파일링은 스캔이 아니라 일련의 쿼리입니다.** 모든 통계는 HiveServer2가 계산하므로, *digna*
  사용자가 작업을 제출하는 큐에는 검사 기간 동안 충분한 용량이 있어야 합니다.

---

## 5. 드라이버 확인(선택 사항) {: #5-verifying-the-driver-optional }

DSN 없는 연결에는 ODBC 데이터 소스를 구성할 필요가 없지만, 드라이버 자체의 대화 상자를 사용하면
*digna*에 값을 입력하기 전에 드라이버, 전송 모드, 자격 증명이 동작하는지 간편하게 확인할 수
있습니다.

#### 1단계
![Step 1](images/hive/create_odbc_data_source_step1.png)

여기의 **Host**, **Port**, **Database**, **Mechanism**, **Thrift Transport** 필드는
[섹션 2](#2-odbc-properties)의 `HOST`, `PORT`, `Schema`, `AuthMech`, `ThriftTransport`
속성에 해당합니다.

#### 2단계 – 연결 테스트

비밀번호를 입력하고 **Test** 버튼을 클릭합니다.

![Step 2](images/hive/create_odbc_data_source_step2.png)

테스트에 성공하면 **OK** 버튼을 클릭합니다.
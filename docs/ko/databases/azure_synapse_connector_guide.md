---
title: Azure Synapse 커넥터 – 데이터베이스 통합 | digna 문서
description: DSN 없는 연결 문자열을 사용해 ODBC로 Azure Synapse Analytics에 연결하도록 digna를 구성합니다. 서버리스 및 전용 SQL 풀을 지원하며, 필수 ODBC 속성과 digna 측 연결 설정을 다룹니다.
image: /assets/logo_square.png
---


# Azure Synapse Analytics용 소스 커넥터

이 가이드는 **DSN 없는(DSN-less)** 연결 문자열을 사용하여 **ODBC**로 Azure Synapse Analytics에
연결하도록 *digna*를 구성하는 방법을 설명합니다. 서버리스 SQL 풀과 전용 SQL 풀이 모두 지원됩니다.

설정 중 *digna* 측 부분은 모든 기술에서 동일합니다. 연결을 만드는 위치, 속성 값을 암호화하는 방법,
연결을 테스트하는 방법, 프로파일링 모드의 의미가 여기에 해당하며
[데이터베이스 연결 개요](overview.md)에 설명되어 있습니다. 이 페이지에서는 Azure Synapse에만
해당하는 내용을 다룹니다.

!!! note "Technology"

    Synapse는 SQL Server 방언을 사용하므로 연결은 **Technology: SQL Server**로 만듭니다.
    온프레미스 서버의 경우 [MS SQL Server](sqlserver_connector_guide.md)를 참조하세요.

---

## 1. ODBC 드라이버 설치 {: #1-install-the-odbc-driver }

[Microsoft 설치 가이드](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)에
따라 *digna* 백엔드가 실행되는 머신에 **ODBC Driver 18 for SQL Server**를 설치하고,
[digna 호스트에 ODBC 드라이버 설치](overview.md#install-the-driver)에 설명된 대로 호스트에서
등록된 정확한 드라이버 이름을 확인합니다.

---

## 2. ODBC 속성 {: #2-odbc-properties }

!!! important "사양이 아닌 예시"

    아래 속성 세트는 정상 동작이 확인된 조합 중 하나입니다. 이 속성들은 Microsoft ODBC 드라이버에
    속하므로 이름, 기본값, 허용되는 값이 드라이버 버전과 플랫폼마다 다르며, 워크스페이스가 요구하는
    사항은 풀 유형, 인증 방식, 방화벽 등 워크스페이스 구성에 따라 달라집니다. 이를 출발점으로 삼고,
    설치한 드라이버 버전의 문서를 확인하세요.

**Add DB Connection** 화면에서 다음 속성을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | *digna* 호스트에 등록된 드라이버 이름과 일치해야 합니다 |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | 워크스페이스 이름과 엔드포인트 접미사 — 아래 참조 |
| `DATABASE` | `dignadata` | 소스 스키마가 있는 데이터베이스입니다. 이 연결로 프로파일링할 수 있는 유일한 데이터베이스입니다 |
| `UID` | `sqladminuser` | SQL 로그인 |
| `PWD` | `<password>` | **Encrypted**를 선택합니다 |

결과 연결 문자열은 다음과 같습니다:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### `SERVER` 값

Synapse 워크스페이스 이름에 엔드포인트 접미사를 붙입니다:

| 풀 | `SERVER` |
|---|---|
| **서버리스 SQL 풀** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **전용 SQL 풀** | `<workspace>.sql.azuresynapse.net` |

!!! warning "`-ondemand` 부분은 놓치기 쉽습니다"

    이 부분이 없으면 이름이 전용 엔드포인트로 확인되어, 연결이 실패하거나 의도와 다른 풀에 조용히
    연결됩니다. 두 엔드포인트는 모두 Azure Portal의 워크스페이스 개요 페이지에 표시됩니다.

### 방화벽

Synapse 워크스페이스 방화벽은 *digna* 호스트의 아웃바운드 주소를 허용해야 합니다. 연결을 테스트하기
전에 워크스페이스의 **Networking**에서 이 주소를 추가하세요. 차단된 주소는 인증 오류가 아니라 연결
시간 초과로 나타납니다.

### Microsoft Entra ID 인증

SQL 로그인 대신 드라이버가 Entra ID로 인증할 수도 있습니다. `UID`/`PWD`를 워크스페이스가 요구하는
인증 방식으로 바꿉니다. 예:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | 이 경우 `UID`에는 애플리케이션(클라이언트) ID, `PWD`에는 클라이언트 시크릿을 입력합니다 |
| `Authentication` | `ActiveDirectoryMSI` | *digna* 호스트의 관리 ID를 사용하며 자격 증명이 필요 없습니다 |

---

## 3. *digna* 구성 {: #3-digna-configuration }

**Add DB Connection** 화면에서 다음을 입력합니다:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Azure Synapse 관련 참고 사항 {: #4-notes-on-azure-synapse }

- **서버리스 풀은 *Standard* 프로파일링만 지원합니다.** 서버리스 SQL 풀은 데이터베이스에 테이블을
  만들 수 없으므로 *Permanent*와 *Session* 프로파일링 모두 실행할 수 없습니다. *Standard*는 소스에서
  직접 메트릭을 계산하며, 서버리스는 처리된 데이터량에 따라 과금되므로 비용 면에서도 더 저렴합니다.
- **하나의 연결은 하나의 데이터베이스만 봅니다.** Synapse는 SQL Server와 마찬가지로 현재
  데이터베이스만 카탈로그로 보고하므로, *digna*는 `DATABASE`에 지정된 데이터베이스의 스키마를
  제공합니다.
- **암호화는 기본적으로 켜져 있습니다.** Driver 18에서는 암호화가 기본값이고 Synapse 엔드포인트는
  유효한 공인 인증서를 제공하므로 `Encrypt`나 `TrustServerCertificate` 속성이 필요 없습니다.
- **서버리스 엔드포인트는 첫 연결 시 유휴 상태에서 재개될 수 있습니다.** 한동안 사용하지 않은 풀에서
  연결 테스트가 시간 초과되면 다시 시도하세요.

---

## 5. 드라이버 확인(선택 사항) {: #5-verifying-the-driver-optional }

DSN 없는 연결에는 ODBC 데이터 소스를 구성할 필요가 없지만, 드라이버 자체의 마법사를 사용하면
*digna*에 값을 입력하기 전에 드라이버가 동작하는지, 워크스페이스가 자격 증명을 허용하는지 간편하게
확인할 수 있습니다.

#### 1단계
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

"Server" 필드를 입력합니다.
Synapse 워크스페이스 이름에 ".sql.azuresynapse.net"을 붙여 사용합니다.  
**주의:** 서버리스 SQL 풀로 연결하려면 위 스크린샷처럼 반드시
"-ondemand"를 포함하세요.

**Next >** 버튼을 클릭합니다.

#### 2단계
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

인증 방식(예: 사용자 이름과 비밀번호)을 선택하고
필요한 정보를 입력합니다.

**Next >** 버튼을 클릭합니다.

#### 3단계
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

ANSI 호환 설정을 선택한 다음 **Next >** 버튼을 클릭합니다.

#### 4단계
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

기본 설정을 그대로 두거나 필요에 따라 옵션을 선택한 후
**Finish** 버튼을 클릭합니다. 

#### 5단계
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

이제 **Test datasource** 버튼을 클릭합니다.

#### 6단계
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

성공 화면이 표시되면 드라이버, 엔드포인트, 자격 증명이 정상 동작하는 것입니다. 입력한 값이 바로
[섹션 2](#2-odbc-properties)의 속성에 들어가는 값입니다.

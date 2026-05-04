---
title: Azure Synapse 커넥터 – 데이터베이스 통합 | digna 문서
description: 네이티브 Python 드라이버 또는 ODBC 드라이버를 사용하여 digna가 Azure Synapse Analytics에 연결하도록 구성하는 방법입니다. 서버리스 및 전용 SQL 풀을 모두 지원합니다.
image: /assets/logo_square.png
canonical_url: https://docs.digna.ai/databases/azure_synapse_connector_guide/
---


# Azure Synapse Analytics용 소스 커넥터

이 가이드는 *digna*를 네이티브 Python 커넥터 또는 ODBC 드라이버를 사용하여 Azure Synapse Analytics에 연결하도록 구성하는 방법을 설명합니다.
서버리스 및 전용 SQL 풀을 모두 지원합니다.

It refers to the screen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** 비밀번호 기반 인증만 지원

> ⚠️ 다른 인증 방법을 사용하려면 ODBC 드라이버를 사용하세요.

### *digna* Configuration (Native Driver)

다음 정보를 **"Create a Database Connection"** 화면에 입력하세요:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC 드라이버는 더 다양한 인증 및 연결 옵션을 지원할 수 있습니다. 이 섹션은 **ODBC Driver 18 for SQL Server** 드라이버를 사용한 비밀번호 기반 인증에 중점을 둡니다.

### 1. ODBC 드라이버 설치

공식 공급업체 설치 가이드를 따라 **ODBC Driver 18 for SQL Server**(또는 유사한 드라이버)를 설치하세요.

### 2. ODBC 데이터 소스 구성

비밀번호 기반 인증을 사용하여 새 ODBC 데이터 소스를 구성하려면 다음 단계를 따르세요:

#### Step 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

"Server" 필드를 입력하세요.
Synapse 워크스페이스 이름을 사용하고 ".sql.azuresynapse.net"을 덧붙이세요.  
**주의**: 서버리스 SQL 풀을 사용하여 연결하려면 아래 스크린샷과 같이 "-ondemand"를 포함해야 합니다.

**Next >** 버튼을 클릭하세요.

#### Step 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

인증 방법(예: 사용자 이름 및 비밀번호)을 선택하고 필요한 정보를 입력하세요.

**Next >** 버튼을 클릭하세요.

#### Step 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

ANSI 호환 설정을 선택한 후 **Next >** 버튼을 클릭하세요.

#### Step 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

기본 설정을 그대로 두거나 필요에 따라 옵션을 선택한 뒤 **Finish** 버튼을 클릭하세요.

#### Step 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

이제 **Test datasource** 버튼을 클릭하세요.

#### Step 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

성공 화면이 표시되면 ODBC가 올바르게 구성된 것입니다.

---

이제 **DSN(Data Source Name)** 또는 DSN-less 설정을 사용하여 *digna*가 ODBC 연결을 사용하도록 구성할 수 있습니다.

---

### A. DSN 기반 구성

#### *digna* Configuration

**"Create a Database Connection"** 화면에 다음을 입력하세요:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN`은 ODBC 드라이버 구성에서 정의한 이름과 일치해야 합니다.

---

### B. DSN-less 구성

#### *digna* Configuration

**"Create a Database Connection"** 화면에 다음을 입력하세요:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**참고** (SERVER 속성 관련):  
Synapse 워크스페이스 이름을 사용하고 ".sql.azuresynapse.net"을 덧붙이세요. 서버리스 SQL 풀로 연결하려면 아래 스크린샷과 같이 "-ondemand"를 포함해야 합니다.
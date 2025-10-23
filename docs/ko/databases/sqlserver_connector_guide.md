---
title: MS SQL Server Connector – Database Integration | digna Documentation
description: pymssql Python 드라이버 또는 SQL Server ODBC 드라이버를 사용해 digna가 Microsoft SQL Server에 연결하도록 구성하는 방법입니다. DSN 기반 또는 DSN-less 설정으로 암호 기반 인증을 지원합니다.
image: /assets/logo_square.png
---


# Source Connector for MS SQL Server

이 가이드는 *digna*를 네이티브 Python 커넥터 또는 ODBC 드라이버를 사용해 SQL Server에 연결하도록 구성하는 방법을 설명합니다.

이 문서는 **"Create a Database Connection"** 화면을 참조합니다.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**지원 인증 방식:** 암호 기반 인증만

> ⚠️ 다른 인증 방법을 사용하려면 ODBC 드라이버를 사용하세요.

### *digna* 구성 (네이티브 드라이버)

**"Create a Database Connection"** 화면에 다음 정보를 입력하세요:

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC 드라이버는 더 다양한 인증 및 연결 옵션을 지원할 수 있습니다. 이 섹션은 드라이버 **SQL Server**를 사용한 암호 기반 인증에 중점을 둡니다.

### 1. ODBC 드라이버 설치

공급업체의 공식 설치 안내를 따라 **SQL Server**(또는 유사 드라이버)를 설치하세요.

### 2. ODBC 데이터 소스 구성

암호 기반 인증을 사용하여 새 ODBC 데이터 소스를 구성하려면 다음 단계를 따르세요:

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

**Next >** 버튼을 클릭하세요.

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

인증 방법(예: 사용자 이름과 암호)을 선택하고 필요한 정보를 입력하세요.

**Next >** 버튼을 클릭하세요.

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

ANSI 호환 설정을 선택한 다음 **Next >** 버튼을 클릭하세요.

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

기본 설정을 그대로 두거나 필요에 따라 로깅 옵션을 선택한 후 **Finish** 버튼을 클릭하세요.

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

이제 **Test datasource** 버튼을 클릭하세요.

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

성공 화면이 나타나면 ODBC가 정상적으로 구성된 것입니다.

---

이제 **DSN (Data Source Name)** 기반 또는 **DSN-less** 설정으로 *digna*가 ODBC 연결을 사용하도록 구성할 수 있습니다.

---

### A. DSN-Based Configuration

#### *digna* 구성

**"Create a Database Connection"** 화면에 다음을 입력하세요:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

> 🔹 `DSN`은 ODBC 드라이버 구성에서 정의한 이름과 일치해야 합니다.

---

### B. DSN-less Configuration

#### *digna* 구성

**"Create a Database Connection"** 화면에 다음을 입력하세요:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```
---
title: Oracle 커넥터 – 데이터베이스 통합 | digna Documentation
description: python-oracledb 드라이버 또는 Oracle ODBC 드라이버를 사용하여 digna가 Oracle에 연결하도록 구성하는 방법입니다. DSN 또는 DSN-less 설정으로 비밀번호 기반 인증을 지원합니다.
image: /assets/logo_square.png
---


# Oracle용 소스 커넥터

이 가이드는 *digna*가 네이티브 Python 커넥터 또는 ODBC 드라이버를 사용하여 Oracle DB에 연결하도록 구성하는 방법을 설명합니다.

본 문서는 화면 **"데이터베이스 연결 생성"**을 참조합니다.

![Create a database connection](images/data_source_config_input_mask.png)

---

## 네이티브 Python 드라이버

**라이브러리:** `python-oracledb`  
**지원되는 인증:** 비밀번호 기반 인증만 지원

> ⚠️ 다른 인증 방식이 필요한 경우 ODBC 드라이버를 사용하세요.

### *digna* 구성 (네이티브 드라이버)

**"데이터베이스 연결 생성"** 화면에 다음 정보를 제공합니다:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC 드라이버

ODBC 드라이버는 더 넓은 범위의 인증 및 연결 옵션을 지원할 수 있습니다. 이 섹션은 드라이버 **Oracle in OraDB21Home1**을 사용한 비밀번호 기반 인증에 중점을 둡니다.

### 1. ODBC 드라이버 설치

공급업체의 공식 설치 가이드를 따라 **Oracle in OraDB21Home1**(또는 유사한 드라이버)을 설치합니다.

### 2. ODBC 데이터 소스 구성

비밀번호 기반 인증을 사용하여 새 ODBC 데이터 소스를 구성하려면 다음 단계를 따르세요:

#### Step 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

참고:
TNS Service Name은 Oracle 클라이언트 설치의 tnsnames.ora 파일에 구성되어야 합니다. 여기에서 연결 디스크립터(host, port, service name)를 제공합니다.

#### Step 2 – 연결 테스트

**Test Connection** 버튼을 클릭합니다.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

비밀번호를 입력하고 **OK** 버튼을 클릭합니다.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

이제 *digna*를 ODBC 연결을 사용하도록 구성할 수 있습니다. **DSN(Data Source Name)** 기반 또는 **DSN-less** 설정 중 선택하세요.

---

### A. DSN 기반 구성

#### *digna* 구성

**"데이터베이스 연결 생성"** 화면에 다음을 입력합니다:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 `DSN`은 ODBC 드라이버 구성에서 정의된 이름과 일치해야 합니다.

---

### B. DSN-less 구성

#### *digna* 구성

**"데이터베이스 연결 생성"** 화면에 다음을 입력합니다:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```
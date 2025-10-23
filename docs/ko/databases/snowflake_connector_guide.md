---
title: Snowflake 커넥터 – 데이터베이스 통합 | digna 문서
description: Python 커넥터 또는 Snowflake ODBC 드라이버를 사용하여 digna를 Snowflake에 연결하도록 구성하는 방법입니다. DSN 또는 DSN-less 설정을 사용한 암호 기반 인증을 지원합니다.
image: /assets/logo_square.png
---


# Snowflake용 소스 커넥터

이 가이드는 네이티브 Python 커넥터 또는 ODBC 드라이버 중 하나를 사용해 *digna*를 Snowflake에 연결하도록 구성하는 방법을 설명합니다.

화면 **"Create a Database Connection"** 을 참조합니다.

![Create a database connection](images/data_source_config_input_mask.png)

---

## 네이티브 Python 드라이버

**라이브러리:** `snowflake-connector-python`  
**지원되는 인증:** 암호 기반 인증만

> ⚠️ 다른 인증 방법을 사용하려면 ODBC 드라이버를 사용하세요.

### *digna* 구성(네이티브 드라이버)

**"Create a Database Connection"** 화면에 다음 정보를 제공하세요:

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
User Name:       User name and warehouse in the format "user<@>warehouse"
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC 드라이버

ODBC 드라이버는 더 다양한 인증 및 연결 옵션을 지원할 수 있습니다. 이 섹션은 **SnowflakeDSIIDriver**를 사용한 암호 기반 인증에 중점을 둡니다.

### 1. ODBC 드라이버 설치

공급업체의 공식 설치 가이드를 따라 **SnowflakeDSIIDriver**를 설치하세요.

### 2. ODBC 데이터 소스 구성

암호 기반 인증을 사용하여 새 ODBC 데이터 소스를 구성하려면 다음 단계를 따르세요:

#### 단계 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

참고:
- Database, Schema 및 Warehouse 값을 제공하지 않으면 *digna* 데이터 소스 구성 중에 ODBC 속성으로 제공해야 합니다.
- "Server"의 값은 여러분의 snowflake 계정 이름 뒤에 ".snowflakecomputing.com"을 붙인 형태입니다.

#### 단계 2 – 연결 테스트

**TEST** 버튼을 클릭하세요. 연결이 성공하면 다음과 같이 표시됩니다:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

이제 **DSN (Data Source Name)** 또는 **DSN-less** 설정 중 하나로 ODBC 연결을 사용하도록 *digna*를 구성할 수 있습니다.

---

### A. DSN 기반 구성

#### *digna* 구성

**"Create a Database Connection"** 화면에 다음을 제공하세요:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> 🔹 `DSN`은 ODBC 드라이버 구성에 정의된 이름과 일치해야 합니다.

---

### B. DSN-less 구성

#### *digna* 구성

**"Create a Database Connection"** 화면에 다음을 제공하세요:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```
---
title: Apache Hive 커넥터 – 데이터베이스 통합 | digna 문서
description: 네이티브 PyHive 드라이버 또는 Cloudera ODBC 드라이버를 사용해 digna를 Apache Hive에 연결하도록 구성하는 방법입니다. 비밀번호 기반 인증과 DSN 또는 DSN-less 설정을 지원합니다.
image: /assets/logo_square.png
---


# Hive용 소스 커넥터

이 가이드는 네이티브 Python 커넥터 또는 ODBC 드라이버 중 하나를 사용하여 *digna*를 Hive에 연결하도록 구성하는 방법을 설명합니다.

화면 **"데이터베이스 연결 생성"** 을 참조합니다.

![데이터베이스 연결 생성](images/data_source_config_input_mask.png)

---

## 네이티브 Python 드라이버

**라이브러리:** `PyHive`  
**지원되는 인증:** 비밀번호 기반 인증만 지원

> 다른 인증 방법을 사용하려면 ODBC 드라이버를 사용하세요.

### *digna* 구성 (네이티브 드라이버)

화면 **"데이터베이스 연결 생성"** 에 다음 정보를 입력하세요:

```
Technology:      Apache Hive
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 10000
Database Name:   Schema that contains the source data
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC 드라이버

ODBC 드라이버는 더 다양한 인증 및 연결 옵션을 지원할 수 있습니다. 이 섹션은 **Cloudera ODBC Driver for Apache Hive** 드라이버를 사용한 비밀번호 기반 인증에 중점을 둡니다.

### 1. ODBC 드라이버 설치

공식 벤더 설치 가이드를 따라 **Cloudera ODBC Driver for Apache Hive**(또는 유사 드라이버)를 설치하세요.

### 2. ODBC 데이터 소스 구성

비밀번호 기반 인증을 사용하여 새 ODBC 데이터 소스를 구성하려면 다음 단계를 따르세요:

#### 1단계
![1단계](images/hive/create_odbc_data_source_step1.png)


#### 2단계 – 연결 테스트

비밀번호를 입력하고 **Test** 버튼을 클릭하세요.

![2단계](images/hive/create_odbc_data_source_step2.png)

테스트가 성공하면 **OK** 버튼을 클릭하세요.

---

이제 **DSN(Data Source Name)** 기반 또는 **DSN-less** 설정으로 *digna*가 ODBC 연결을 사용하도록 구성할 수 있습니다.

---

### A. DSN 기반 구성

#### *digna* 구성

화면 **"데이터베이스 연결 생성"** 에 다음을 입력하세요:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN`은 ODBC 드라이버 구성에 정의된 이름과 일치해야 합니다.

---

### B. DSN-less 구성

#### *digna* 구성

화면 **"데이터베이스 연결 생성"** 에 다음을 입력하세요:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 10000"
name: "Schema",     value: "Schema that contains the source data"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```
---
title: Databricks Connector with Unity Catalog – Database Integration | digna Documentation
description: digna를 Unity Catalog가 있는 Databricks에 네이티브 Python 커넥터 또는 ODBC 드라이버를 사용해 연결하도록 구성합니다. 토큰 기반 인증과 유연한 연결 방식을 지원합니다.
image: /assets/logo_square.png
---

# Databricks용 소스 커넥터 - Unity Catalog와 함께

이 가이드는 *digna*를 Databricks에 연결하는 방법을 설명합니다. 연결 방식으로는 네이티브 Python 커넥터 또는 ODBC 드라이버를 사용할 수 있습니다.

다음은 **"Create a Database Connection"** 화면을 참조합니다.

![데이터베이스 연결 만들기](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**지원되는 인증 방법:** Personal Access Token (PAT)만 지원

> 다른 인증 방법이 필요하면 ODBC 드라이버를 사용하세요.

### Personal Access Token (PAT)

개인 액세스 토큰으로 인증하려면 공식 Databricks 문서를 참조하세요:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* 구성 (네이티브 드라이버)

**"Create a Database Connection"** 화면에서 다음 정보를 제공합니다:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC 드라이버는 더 다양한 인증 및 연결 옵션을 지원합니다. 이 섹션은 **Simba Spark ODBC Driver**를 사용한 토큰 기반 인증에 중점을 둡니다.

### 1. ODBC 드라이버 설치

공급업체의 공식 설치 가이드를 따라 **Simba Spark ODBC Driver**를 설치하세요.

### 2. ODBC 데이터 소스 구성

Personal Access Token을 사용하여 새 ODBC 데이터 소스를 구성하려면 다음 단계를 따르세요:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – 연결 테스트

**TEST** 버튼을 클릭합니다. 성공적인 연결은 다음과 같이 표시됩니다:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

이제 *digna*를 ODBC 연결로 구성할 수 있습니다. **DSN (Data Source Name)** 기반 또는 **DSN-less** 설정 둘 다 지원됩니다.

---

### A. DSN 기반 구성

#### *digna* 구성

**"Create a Database Connection"** 화면에서 다음을 입력하세요:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN`은 ODBC 드라이버 구성에서 정의한 이름과 일치해야 합니다.

---

### B. DSN-less 구성

#### *digna* 구성

**"Create a Database Connection"** 화면에서 다음을 입력하세요:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC 속성

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
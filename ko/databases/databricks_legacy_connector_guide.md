# Unity Catalog 없이 Databricks용 소스 커넥터

이 가이드는 *digna*를 네이티브 Python 커넥터 또는 ODBC 드라이버 중 하나를 사용해 Databricks에 연결하도록 구성하는 방법을 설명합니다.

화면 **"Create a Database Connection"** 을 참조합니다.

![Create a database connection](images/data_source_config_input_mask.png)

---

## 네이티브 Python 드라이버

**라이브러리:** `databricks-sql-connector`  
**지원 인증 방식:** Personal Access Token (PAT) 만 지원

> 다른 인증 방식이 필요한 경우 ODBC 드라이버를 사용하세요.

### Personal Access Token (PAT)

Personal Access Token으로 인증하려면 Databricks 공식 문서를 참조하세요:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* 구성 (네이티브 드라이버)

**"Create a Database Connection"** 화면에 다음 정보를 입력하세요:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC 드라이버

ODBC 드라이버는 더 넓은 범위의 인증 및 연결 옵션을 지원합니다. 이 섹션은 **Simba Spark ODBC Driver**를 사용한 토큰 기반 인증에 중점을 둡니다.

### 1. ODBC 드라이버 설치

공급사의 공식 설치 가이드를 따라 **Simba Spark ODBC Driver**를 설치하세요.

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

**TEST** 버튼을 클릭하세요. 연결 성공 예시는 다음과 같습니다:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

이제 **DSN(Data Source Name)** 방식 또는 **DSN-less** 방식으로 *digna*가 ODBC 연결을 사용하도록 구성할 수 있습니다.

---

### A. DSN 기반 구성

#### *digna* 구성

**"Create a Database Connection"** 화면에 다음을 입력하세요:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
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

**"Create a Database Connection"** 화면에 다음을 입력하세요:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
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
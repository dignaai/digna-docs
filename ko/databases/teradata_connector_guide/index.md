# Source Connector for Teradata

이 가이드는 네이티브 Python 커넥터 또는 ODBC 드라이버 중 하나를 사용하여 *digna*를 Teradata에 연결하도록 구성하는 방법을 설명합니다.

이는 **"Create a Database Connection"** 화면을 참조합니다.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `teradatasql`  
**Supported Authentication:** Password-based authentication only

> 다른 인증 방법을 사용하려면 ODBC 드라이버를 사용하십시오.

### *digna* Configuration (Native Driver)

다음 정보를 **"Create a Database Connection"** 화면에 제공합니다:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC 드라이버는 더 광범위한 인증 및 연결 옵션을 지원할 수 있습니다. 이 섹션은 **Teradata Database ODBC Driver 20.00** 드라이버를 사용한 비밀번호 기반 인증에 중점을 둡니다.

### 1. Install the ODBC Driver

공식 벤더 설치 가이드를 따라 **Teradata Database ODBC Driver 20.00**(또는 유사 버전)을 설치하십시오.

### 2. Configure the ODBC Data Source

비밀번호 기반 인증을 사용하여 새 ODBC 데이터 소스를 구성하려면 다음 단계를 따르십시오:

#### Step 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

**Test** 버튼을 클릭합니다.

#### Step 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

사용자 이름과 비밀번호를 입력합니다.

**OK** 버튼을 클릭합니다. 성공 화면이 표시되면 ODBC가 제대로 구성된 것입니다.

---

이제 **DSN (Data Source Name)** 기반 또는 **DSN-less** 설정 중 하나로 ODBC 연결을 사용하도록 *digna*를 구성할 수 있습니다.

---

### A. DSN-Based Configuration

#### *digna* Configuration

**"Create a Database Connection"** 화면에 다음을 입력합니다:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN`은 ODBC 드라이버 구성에 정의된 이름과 일치해야 합니다.

---

### B. DSN-less Configuration

#### *digna* Configuration

**"Create a Database Connection"** 화면에 다음을 입력합니다:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
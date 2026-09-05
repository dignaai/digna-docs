# PostgreSQL용 소스 커넥터

이 가이드는 네이티브 Python 커넥터 또는 ODBC 드라이버 중 하나를 사용하여 *digna*를 Postgres에 연결하도록 구성하는 방법을 설명합니다.

화면 **"Create a Database Connection"** 을 참조합니다.

![Create a database connection](images/data_source_config_input_mask.png)

---

## 네이티브 Python 드라이버

**라이브러리:** `psycopg`  
**지원 인증:** 암호 기반 인증만 지원

> 다른 인증 방법을 사용해야 하는 경우 ODBC 드라이버를 사용하세요.

### *digna* 구성 (네이티브 드라이버)

**"Create a Database Connection"** 화면에 다음 정보를 제공하세요:

```
기술:            Postgres
호스트 주소:     서버 이름 또는 IP 주소
호스트 포트:     포트 번호, 예: 5432
데이터베이스 이름: 데이터베이스 이름
스키마 이름:     소스 데이터를 포함하는 스키마
사용자 이름:     데이터베이스 사용자 이름
사용자 비밀번호: 사용자 비밀번호
ODBC 사용:       사용 안 함(기본값)
```

---

## ODBC 드라이버

ODBC 드라이버는 더 폭넓은 인증 및 연결 옵션을 지원할 수 있습니다. 이 섹션은 **PostgreSQL Unicode(x64)** 드라이버를 사용한 암호 기반 인증에 중점을 둡니다.

### 1. ODBC 드라이버 설치

공급업체의 공식 설치 가이드를 따라 **PostgreSQL Unicode(x64)**(또는 유사한 드라이버)를 설치하세요.

### 2. ODBC 데이터 소스 구성

암호 기반 인증을 사용하여 새 ODBC 데이터 소스를 구성하려면 다음 단계를 따르세요:

#### Step 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

참고: 데이터베이스 설정에서 특정 "SSLMode"를 선택해야 하는 경우, DSN-less 구성을 정의할 때에도 동일한 설정을 사용해야 합니다.

#### Step 2 – 연결 테스트

**Test Connection** 버튼을 클릭하세요.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

이제 **DSN(Data Source Name)** 기반 또는 **DSN-less** 설정으로 *digna*가 ODBC 연결을 사용하도록 구성할 수 있습니다.

---

### A. DSN 기반 구성

#### *digna* 구성

**"Create a Database Connection"** 화면에 다음을 입력하세요:

```
기술:            PostgreSQL
데이터베이스 이름: 소스 스키마를 포함하는 데이터베이스
스키마 이름:     소스 데이터를 포함하는 스키마
ODBC 사용:       사용
```

#### ODBC 속성

```
name: "DSN",    value: "PostgreSQL35W"
```

> `DSN`은 ODBC 드라이버 구성에 정의된 이름과 일치해야 합니다.

---

### B. DSN-less 구성

#### *digna* 구성

**"Create a Database Connection"** 화면에 다음을 입력하세요:

```
기술:            PostgreSQL
데이터베이스 이름: 소스 데이터를 포함하는 스키마(스키마 이름과 동일)
스키마 이름:     소스 데이터를 포함하는 스키마
ODBC 사용:       사용
```

#### ODBC 속성

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user"
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```
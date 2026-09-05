---
title: Windows 설치 가이드 – digna Release 2026.06 | digna 문서
description: Windows에 digna Release 2026.06을 설치하는 단계별 가이드 — 시스템 요구사항, PostgreSQL 설정, 웹 서버 구성, 백엔드 및 대시보드 구성, Windows 서비스로 digna 실행, 새 릴리스로 업그레이드
keywords: digna windows 설치, digna 배포 가이드, digna 백엔드 설정, digna 대시보드 설치, postgresql 설정, digna windows 서비스, digna 업그레이드 가이드
image: /assets/logo_square.png
---

# digna Release 2026.06용 Windows 설치 가이드

**Release:** 2026.06

**최종 수정일:** 2026년 8월 30일


---

## 목차

1. [소개](#introduction)
2. [시스템 요구사항](#system-requirements)
3. [사전 설치 준비](#pre-installation-setup)
4. [PostgreSQL 서버 설정](#postgresql-server-setup)
5. [웹 서버 구성](#web-server-configuration)
6. [초기 설치](#initial-installation)
7. [백엔드 구성](#backend-configuration)
8. [대시보드 구성](#dashboard-configuration)
9. [digna를 Windows 서비스로 실행하기](#running-digna-as-a-windows-service)
10. [새 릴리스로 업그레이드하기](#upgrading-to-a-new-release)

---

## 소개 {: #introduction }

### digna에 관하여

digna는 데이터 웨어하우스, 데이터 레이크, 레이크하우스 등 다양한 데이터 환경 전반의 데이터 품질 관리를 최적화하도록 설계된 포괄적인 AI 기반 플랫폼입니다. 고도로 확장 가능하고 적응력이 뛰어나며 자동화, 실시간 모니터링 및 이상 탐지를 통해 현대 데이터 과제를 해결합니다.

digna는 두 가지 주요 구성요소로 이루어져 있습니다:

- **dignabackend**: 데이터 처리 및 품질 검사를 수행하는 애플리케이션의 핵심 엔진입니다.
- **dignadashboard**: 웹 서버에 호스팅되는 웹 기반 인터페이스로, digna 플랫폼과 상호작용하고 데이터 품질 지표를 시각화할 수 있는 사용자 친화적인 방법을 제공합니다.

### 릴리스 2026.06의 주요 변경사항

이번 릴리스는 데이터 관찰 가능성(data observability)을 코드에 직접 통합하여 개발자가 소스에서 데이터 품질을 모니터링할 수 있도록 합니다. 전체 내용은 [릴리스 노트](http://docs.digna.ai/changelog/Release_202606/)를 참조하세요.

---

## 시스템 요구사항 {: #system-requirements }

설치를 시작하기 전에 시스템이 다음 최소 요구사항을 충족하는지 확인하십시오:

| Requirement | Specification |
|---|---|
| **운영 체제** | Windows Server 또는 Windows 10/11 |
| **메모리 (최소 구성)** | 16 GB RAM |
| **디스크 공간** | 10 GB 사용 가능한 저장공간 |
| **데이터베이스** | PostgreSQL Server 12 이상 |
| **웹 서버** | IIS, Apache Tomcat 또는 동등 제품 |

### 데이터베이스 설치 옵션

**PostgreSQL이 이미 설치되어 있는 경우:**
기존 PostgreSQL 서버에 digna용 새 데이터베이스를 추가할 수 있습니다.

**digna와 동일한 머신에 PostgreSQL을 설치하는 경우:**

!!! info "권장 사양"

    - **메모리**: 32 GB RAM (16 GB 대신)
    - **디스크 공간**: 50 GB 사용 가능한 저장공간 (10 GB 대신)

    이 높은 사양은 digna와 PostgreSQL 데이터베이스가 동시에 실행될 때를 대비한 것입니다.

---

## 사전 설치 준비 {: #pre-installation-setup }

digna를 설치하기 전에 다음 두 가지 중요한 전제 조건이 준비되어 있어야 합니다:

1. **PostgreSQL 서버** – 계산된 메트릭과 성능 데이터를 저장하기 위함
2. **웹 서버** – digna 대시보드를 호스팅하기 위함

이 구성 요소들이 아직 설정되지 않았다면, 아래 섹션을 따라 설치 및 구성을 진행하세요.

---

## PostgreSQL 서버 설정 {: #postgresql-server-setup }

### PostgreSQL이 이미 설치되어 있는 경우

PostgreSQL이 로컬 머신에서 이미 실행 중이거나 관리형 원격 PostgreSQL 서버를 사용 중이라면 [다음 섹션](#web-server-configuration)으로 건너뛰세요.

### PostgreSQL 설치

Windows에 PostgreSQL을 설치하려면 다음 단계를 따르세요:

#### 1단계: PostgreSQL 다운로드

1. [PostgreSQL 다운로드 페이지](https://www.postgresql.org/download/)를 방문합니다.
2. **Windows**를 선택합니다.
3. 최신 설치관리자를 다운로드합니다.

#### 2단계: 설치관리자 실행

1. 다운로드한 설치관리자 파일을 더블클릭합니다.
2. 설치 마법사의 지시에 따라 진행합니다.

#### 3단계: 설치 디렉터리 선택

PostgreSQL을 설치할 디렉터리를 선택합니다. 기본 위치를 사용해도 무방합니다.

#### 4단계: 구성요소 선택

표준 설치의 경우 기본 구성요소 선택을 유지합니다.

#### 5단계: PostgreSQL 슈퍼유저 암호 설정

PostgreSQL 슈퍼유저(`postgres`)의 암호를 입력하고 확인합니다. **이 암호를 안전하게 보관하세요** — 이후에 필요합니다.

#### 6단계: 포트 번호 구성

기본 PostgreSQL 포트는 `5432`입니다. 기본값을 사용하거나 필요한 경우 다른 포트를 지정할 수 있습니다.

!!! tip "팁"

    포트 5432가 이미 사용 중인 경우 대체 포트를 선택하고 이후 구성에 참고하세요.

#### 7단계: 로케일 선택

데이터베이스의 로케일을 선택합니다. 기본값이 대부분의 설치에 적합합니다.

#### 8단계: 설치 완료

나머지 단계를 **다음(Next)**으로 진행한 후 **끝(Finish)**을 클릭합니다.

#### 9단계: 설치 확인

명령 프롬프트를 열고 PostgreSQL이 설치되었는지 확인합니다:

```bash
psql --version
```

설치가 성공하면 PostgreSQL 버전이 표시됩니다.

---

## 웹 서버 구성 {: #web-server-configuration }

digna는 대시보드를 호스팅하기 위해 웹 서버가 필요합니다. 다음 옵션 중 하나를 선택하세요:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

이 중 **하나**의 서버만 설치하고 구성하면 됩니다.

### IIS 설정 {: #iis-setup }

#### 개요

Internet Information Services(IIS)는 웹사이트 및 웹 애플리케이션을 호스팅하기 위한 Microsoft의 웹 서버입니다.

#### IIS 활성화

1. **제어판 열기**
   - `Win + R`을 누릅니다.
   - `control`을 입력하고 Enter 키를 누릅니다.

2. **Windows 기능으로 이동**
   - **프로그램**을 클릭합니다.
   - **Windows 기능 켜기/끄기**를 선택합니다.

3. **Internet Information Services 활성화**
   - 항목 목록에서 **Internet Information Services (IIS)**를 찾습니다.
   - 체크박스를 선택하여 활성화합니다.
   - **+**를 클릭하여 하위 구성요소가 다음과 같이 선택되었는지 확인합니다:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **확인(OK)**을 클릭하여 변경 사항을 적용합니다.

5. **IIS 설치 확인**
   - 브라우저를 열고
   - `http://localhost`로 이동합니다.
   - IIS 환영 페이지가 표시되어야 합니다.

#### 필수: URL Rewrite 모듈

IIS는 URL Rewrite 구성요소가 필요합니다. [공식 Microsoft 페이지](https://www.iis.net/downloads/microsoft/url-rewrite)에서 다운로드하여 설치하세요.

#### 필수: Markdown 파일용 MIME 타입

IIS에서 Markdown 파일(`.md`)이 올바르게 서빙되도록 하려면:

1. **IIS 관리자**를 엽니다 (`Win + R`, `inetmgr` 입력, Enter)
2. **사이트 > MIME Types**로 이동합니다.
3. **추가(Add...)**를 클릭합니다.
4. 구성:
   - **파일 이름 확장자(File name extension)**: `.md`
   - **MIME 타입(MIME type)**: `text/markdown`

!!! warning "중요"

    이 설정이 없으면 `.md` 파일이 제대로 서빙되지 않을 수 있습니다.

---

### Apache Tomcat 설정 {: #apache-tomcat-setup }

#### 개요

Apache Tomcat은 오픈소스 Java 서블릿 컨테이너이자 웹 서버입니다.

#### 설치

1. **Apache Tomcat 다운로드**
   - [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)를 방문합니다.
   - Windows ZIP 배포판을 다운로드합니다.

2. **압축 해제**
   - ZIP 파일을 시스템의 디렉터리에 압축 해제합니다.
   - 예: `C:\Program Files\Apache Tomcat`

3. **Tomcat 실행 확인**
   - 브라우저를 열고
   - `http://localhost:8080`로 이동합니다.
   - Apache Tomcat 환영 페이지가 표시되어야 합니다.

!!! tip "팁"

    Apache Tomcat은 일반적으로 설치 후 자동으로 시작됩니다. 시작되지 않는 경우 `bin` 폴더로 이동하여 `startup.bat`를 실행하세요.

---

## 초기 설치 {: #initial-installation }

### 1단계: digna 저장소 설정

digna 저장소는 digna가 계산한 모든 메트릭을 저장합니다. 분석 및 성능 데이터의 중앙 데이터베이스 역할을 합니다.

#### 저장소 스키마 및 사용자 생성

PostgreSQL 클라이언트(pgAdmin, psql 등)를 열고 다음 SQL 명령을 실행하세요:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**아래 플레이스홀더를 바꾸세요:**

- `<digna_repo_schema>` — 원하는 스키마 이름 (예: `dignarepo`)
- `<digna_repo_user>` — 원하는 사용자명 (예: `digna_user`)
- `<digna_repo_password>` — 이 사용자에 대한 안전한 암호

**예시:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "권장사항"

    데이터베이스 사용자에 대해 강력하고 복잡한 암호를 사용하세요. 쉽게 추측 가능한 자격증명은 피하십시오.

---

### 2단계: digna 설치 패키지 압축 해제

1. 제공된 digna 설치 ZIP 파일을 찾습니다.
2. 원하는 설치 위치에 압축을 풉니다.
3. 압축 해제 후 다음 항목들이 보여야 합니다:
   - `dashboard/` — 웹 대시보드 인터페이스
   - `digna` — 메인 실행 파일(백엔드 + CLI 결합)
   - `config.toml` — 구성 파일
   - `license.toml` — 라이선스 파일(제공받은 파일을 여기에 복사)

### 3단계: 라이선스 파일 설치

!!! warning "중요"

    라이선스 파일은 설치 패키지에 **포함되어 있지 않으며** digna에서 별도로 제공됩니다.

1. 제공받은 `license.toml` 파일을 찾습니다.
2. `config.toml` 및 `digna` 실행 파일이 있는 digna 설치 루트 디렉터리에 복사합니다.

**중요 이유:**
라이선스 파일에는 고객 정보, 라이선스 만료일 및 디지털 서명이 포함되어 있습니다. **이 파일을 수정하지 마십시오** — 변경 시 라이선스가 무효화됩니다.

**설정 후 디렉터리 구조 예시:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## 백엔드 구성 {: #backend-configuration }

### 1단계: 구성 파일 생성 및 편집

`config_template.toml` 파일이 digna 설치 디렉터리에 제공됩니다. 파일 이름을 `config.toml`로 변경하면됩니다.

**위치:** `digna_installation/config.toml`

텍스트 편집기에서 `config.toml`을 열고 아래 각 섹션을 구성하세요.

#### [app] 섹션

이 섹션은 digna 백엔드 애플리케이션 설정을 구성합니다:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` 또는 IP 주소 | dignabackend가 호스팅되는 호스트명 또는 IP |
| `digna_APP_PORT` | `8082` (기본값) | REST API 엔드포인트용 포트 |
| `digna_APP_CORS_ALLOW_ORIGINS` | 프론트엔드 URL | 대시보드가 다른 서버에 있는 경우 해당 URL 포함 |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | 자격증명 있는 CORS에 필요 |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | 모든 HTTP 메서드 허용 |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | 모든 헤더 허용 |

#### [repo] 섹션

이 섹션은 PostgreSQL 데이터베이스 연결을 구성합니다:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` 또는 IP | PostgreSQL 서버 호스트명/IP |
| `digna_REPO_PORT` | `5432` (기본값) | PostgreSQL 포트 |
| `digna_REPO_DB` | `postgres` | 데이터베이스 이름 |
| `digna_REPO_SCHEMA` | `dignarepo` | 앞서 생성한 스키마 |
| `digna_REPO_USER` | `digna_user` | PostgreSQL 설정에서 생성한 사용자 |
| `digna_REPO_PASSWORD` | 사용자 암호 | 스키마 생성 시 설정한 암호 |

#### [base] 섹션

이 섹션은 보안 및 쿠키 설정을 포함합니다:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | 암호화 키 | 토큰 및 쿠키 암호화에 사용됨 (기본 키 제공) |
| `digna_COOKIE_DOMAIN` | `localhost` | 프론트엔드 도메인과 일치시킵니다 |
| `digna_COOKIE_SECURE` | `false` (로컬) / `true` (프로덕션) | HTTPS 연결인 경우 `true`로 설정 |
| `digna_COOKIE_HTTPONLY` | `true` | 보안을 위해 항상 활성화 |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF 공격 방지에 도움 |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24시간) | 세션 타임아웃(초) |
| `digna_MAX_WORKERS` | CPU 코어 수 - 1 | 병렬 검사 작업 수 |

#### [logging] 섹션

이 섹션은 로깅 동작을 구성합니다:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` 또는 `DEBUG` | 운영환경은 `INFO`, 문제해결 시 `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | 보관할 일별 로그 백업 수 |

---

### 3단계: 저장소 연결 테스트

1. 명령 프롬프트를 엽니다.
2. `config.toml`과 `digna` 실행 파일이 있는 digna 설치 디렉터리로 이동합니다.
3. 연결 테스트를 실행합니다:

```bash
digna repo check
```

연결이 설정되었다는 확인 메시지가 표시되어야 합니다(아직 저장소 자체는 초기화되지 않았습니다).

### 4단계: 저장소 스키마 설치

같은 디렉터리에서 다음을 실행합니다:

```bash
digna repo install
```

이 명령은 PostgreSQL 데이터베이스에 필요한 테이블과 스키마를 설치합니다.

### 5단계: digna 서버 시작

digna 설치 디렉터리에서 서버를 시작합니다:

```bash
digna serve --address <host> --port <port>
```

**매개변수:**
- `--address` — 서버 호스트명/IP
- `--port` — 서버 포트

서버가 실행 중임을 확인하는 시작 메시지가 표시됩니다:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### 6단계: 관리자 사용자 생성

1. **새로운** 명령 프롬프트 창을 엽니다.
2. digna 설치 디렉터리로 이동합니다.
3. 다음 명령을 실행하여 관리자 사용자를 생성합니다:

```bash
digna user add <username> "<full_name>" <password> --su
```

**예시:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

이 명령은 전체 관리 권한을 가진 사용자를 만듭니다.

!!! tip "권장사항"

    대문자, 소문자, 숫자 및 특수문자를 혼합한 강력한 암호를 사용하세요.

---

## 대시보드 구성 {: #dashboard-configuration }

### 1단계: 대시보드를 웹 서버에 배포

digna 대시보드에는 별도의 `config.toml` 파일이 `dashboard/` 디렉터리에 있습니다. 이 구성은 이미 제공되어 있으며 초기 설정 시 변경할 필요가 없습니다. 백엔드 연결을 맞춤화해야 하는 경우에만 구성 파일을 편집하세요.

대시보드 구성이 필요한 경우(예: 다중 인스턴스 배포)에는 대시보드 문서를 참조하세요.

웹 서버를 선택한 후 해당 배포 절차를 따르세요.

#### IIS에 배포

1. **IIS 관리자 열기**
   - `Win + R`을 누르고 `inetmgr`을 입력한 후 Enter

2. **새 웹사이트 생성**
   - 왼쪽 패널에서 **Sites**를 우클릭
   - **Add Website...** 선택

3. **웹사이트 구성**
   - **Site Name**: 이름 입력(예: "dignaDashboard")
   - **Physical Path**: Browse를 클릭하고 `dashboard` 폴더 선택
   - **Binding**: IP 주소와 포트 설정(HTTP 기본 포트 80, HTTPS 443)

4. **웹사이트 시작**
   - **OK**를 클릭하여 사이트 생성
   - 새 사이트를 우클릭하고 **Start** 선택

5. **설치 테스트**
   - 브라우저를 열고
   - `http://localhost`(또는 구성한 URL)로 이동
   - digna 대시보드 로그인 페이지가 표시되어야 합니다.

#### Apache Tomcat에 배포

1. **대시보드를 Tomcat에 복사**
   - `dashboard` 폴더를 Tomcat의 `webapps` 디렉터리에 복사
   - 필요 시 이름 변경(예: `digna`)
   - 예: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **배포 확인**
   - Tomcat 관리 페이지를 새로고침하거나 다시 로드합니다 (`http://localhost:8080`)
   - 배포된 애플리케이션 목록에 "digna"(또는 설정한 이름)가 표시됩니다.

3. **대시보드 접근**
   - 브라우저를 열고
   - `http://localhost:8080/digna`로 이동
   - digna 대시보드 로그인 페이지가 표시되어야 합니다.

---

## digna를 Windows 서비스로 실행하기 {: #running-digna-as-a-windows-service }

### Windows 서비스를 사용하는 이유

digna 백엔드를 Windows 서비스로 실행하면 다음과 같은 이점이 있습니다:
- 서버 부팅 시 자동으로 시작
- 명령 프롬프트 없이 백그라운드에서 실행
- 충돌 시 자동 재시작
- Windows 서비스 관리자를 통해 관리 가능

### 서비스 관리 파일

필요한 모든 파일은 digna 설치 디렉터리의 `bin/` 아래에 있습니다.

다음 배치 파일이 제공됩니다:
- `install_service.bat` — digna를 Windows 서비스로 등록
- `uninstall_service.bat` — 서비스 등록 해제
- `start_service.bat` — 서비스를 시작
- `stop_service.bat` — 서비스를 중지

!!! warning "관리자 권한 필요"

    모든 배치 파일은 관리자 권한으로 실행해야 합니다.

### 서비스 설치

1. **관리자 권한으로 명령 프롬프트 열기**
   - 명령 프롬프트 아이콘을 우클릭
   - "관리자 권한으로 실행(Run as Administrator)" 선택

2. **bin 폴더로 이동**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **설치 스크립트 실행**
   ```bash
   install_service.bat
   ```

이제 digna 서버가 **자동 시작**으로 Windows 서비스에 등록됩니다. 서비스는 즉시 시작되지 않습니다 — 다음 섹션을 참조하여 시작하세요.

### 서비스 시작 및 중지

#### 서비스를 시작하려면

1. 관리자 권한으로 명령 프롬프트를 엽니다.
2. `digna\bin`으로 이동합니다.
3. 실행:
   ```bash
   start_service.bat
   ```

#### 서비스를 중지하려면

1. 관리자 권한으로 명령 프롬프트를 엽니다.
2. `digna\bin`으로 이동합니다.
3. 실행:
   ```bash
   stop_service.bat
   ```

!!! tip "팁"

    애플리케이션 파일을 업데이트하기 전에 항상 서비스를 중지하세요.

### 서비스를 새 디렉터리로 이동하기

digna 설치를 다른 위치로 옮겨야 할 경우:

1. **현재 서비스 제거**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **애플리케이션 파일 이동**
   - 전체 digna 설치 폴더를 새 위치로 이동합니다.

3. **서비스 재설치**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **서비스 시작**
   ```bash
   start_service.bat
   ```

### 서비스 제거

1. **실행 중인 서비스 중지**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **서비스 등록 해제**
   ```bash
   uninstall_service.bat
   ```

이제 digna 서버가 Windows 서비스에서 등록 해제됩니다.

---

## 새 릴리스로 업그레이드하기 {: #upgrading-to-a-new-release }

### 업그레이드 전에

**digna 저장소 백업은 필수입니다**

digna를 업그레이드하기 전에 저장소(PostgreSQL)를 백업하여 데이터 손실에 대비하세요. 백업은 업그레이드 중 예기치 않은 문제가 발생할 경우 복구를 보장합니다.

### 업그레이드 절차

#### 1단계: digna 서비스 중지

digna가 Windows 서비스로 실행 중인 경우 먼저 중지합니다:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### 2단계: 현재 백엔드 설치 백업

digna 설치 디렉터리에서:

```bash
# dignabackend 폴더 이름 변경
ren dignabackend dignabackend_old
```
```bash
# dashboard 이름 변경
ren dashboard dashboard_old
```

#### 3단계: 새 버전 압축 해제 및 배포

1. 새 digna 설치 ZIP 파일의 압축을 풉니다.
2. 새 `digna` 실행 파일과 `dashboard` 폴더를 설치 디렉터리에 복사합니다.

!!! warning "중요"

    `config.toml` 파일은 설치 ZIP에 **절대** 포함되지 않습니다. 기존 구성은 안전하게 유지됩니다.

### 4단계: 구성 파일 복원

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

### 5단계: 저장소 스키마 업그레이드

digna 설치 디렉터리로 이동하여 다음을 실행합니다:

```bash
digna repo upgrade
```

이 명령은 기존 데이터를 보존하면서 PostgreSQL 스키마를 최신 버전으로 업데이트합니다.

### 6단계: 서비스 재시작

Windows 서비스로 실행 중이었다면:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

수동으로 실행하던 경우 서버를 재시작합니다:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

IIS 또는 Tomcat을 사용하는 경우 해당 웹 서버를 재시작하세요.

#### 7단계: 업그레이드 확인

1. digna 대시보드에 접속합니다.
2. 인터페이스가 올바르게 로드되는지 확인합니다.
3. 서버 로그에서 오류가 없는지 확인합니다.

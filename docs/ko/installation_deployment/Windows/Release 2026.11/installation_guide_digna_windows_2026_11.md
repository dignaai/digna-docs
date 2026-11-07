---
title: Windows 설치 안내 – digna 릴리스 2026.11 | digna 문서
description: Windows에 digna 릴리스 2026.11을 설치하는 단계별 안내 — 시스템 요구사항, PostgreSQL 설정, 웹 서버 구성, 백엔드 및 대시보드 설정, Windows 서비스로서의 digna 실행 및 릴리스 2026.06에서 업그레이드하는 방법.
keywords: digna 윈도우 설치, digna 배포 안내, digna 백엔드 설정, digna 대시보드 설치, postgresql 설정, digna 윈도우 서비스, digna 업그레이드 안내
image: /assets/logo_square.png
---

# digna 릴리스 2026.11용 Windows 설치 안내

**릴리스:** 2026.11

**최종 업데이트:** 2026년 11월 7일


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

### digna에 대하여

digna는 데이터 웨어하우스, 데이터 레이크, 레이크하우스 등 다양한 데이터 환경에서 데이터 품질 관리를 최적화하도록 설계된 종합 AI 기반 플랫폼입니다. 높은 확장성과 적응성을 목표로 하며, 자동화, 실시간 모니터링 및 이상 감지를 통해 현대적인 데이터 문제를 해결합니다.

digna는 두 가지 주요 구성요소로 이루어져 있습니다:

- **digna**: 애플리케이션의 핵심으로, 데이터 처리와 품질 검사 수행을 담당합니다. 백엔드와 명령줄 인터페이스를 단일 실행 파일로 통합하여 이전 릴리스의 별도 프로그램인 `dignabackend`와 `dignacli`를 대체합니다.
- **dignadashboard**: 웹 서버에서 호스팅되는 웹 기반 인터페이스로, 사용자 친화적인 방식으로 digna 플랫폼과 데이터 품질 지표를 시각화합니다.

### 릴리스 2026.11의 주요 변경 사항

이번 릴리스는 digna Data Reconciliation, digna MCP Server를 포함한 digna Agentic, 그리고 digna Engine을 추가합니다. digna Engine은 digna 내부에서 데이터를 프로파일링하고 서로 다른 데이터베이스 기술 간의 참조 무결성을 검사할 수 있습니다. 자세한 내용은 [릴리스 노트](../../../changelog/Release_202611.md)를 참조하세요.

설치 측면에서 이번 릴리스는 새로운 저장소 마이그레이션 메커니즘, digna Engine을 위한 `config.toml`의 선택적 `[duckdb]` 섹션, 그리고 새 라이선스 파일을 도입합니다. 각각은 [업그레이드 섹션](#upgrading-to-a-new-release)에서 다룹니다.

### macOS 또는 Linux용 안내서를 찾으시나요?

이 안내서는 Windows를 다룹니다. 다른 플랫폼은 [macOS 설치 안내](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) 또는 [Linux 설치 안내](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md)를 참조하십시오.

---

## 시스템 요구사항 {: #system-requirements }

설치를 시작하기 전에 시스템이 다음 최소 요구사항을 충족하는지 확인하세요:

| 요구사항 | 사양 |
|---|---|
| **운영체제** | Windows Server 또는 Windows 10/11 |
| **메모리 (최소 구성)** | 16 GB RAM |
| **디스크 공간** | 10 GB 사용 가능 저장공간 |
| **데이터베이스** | PostgreSQL Server 12 이상 |
| **웹 서버** | IIS, Apache Tomcat 또는 동등한 서버 |

!!! info "digna Engine"

    프로파일링 위치로 digna Engine을 사용하는 데이터베이스 연결은 digna 호스트 자체에서 프로파일링됩니다.
    이를 위한 추가 메모리와 디스크 공간을 계획하세요. 참조:
    [\[duckdb\] 섹션](#duckdb-section).

### 데이터베이스 설치 옵션

**이미 PostgreSQL이 설치되어 있는 경우:**
기존 PostgreSQL 서버에 digna용 새 데이터베이스를 추가할 수 있습니다.

**digna와 동일한 머신에 PostgreSQL을 설치하는 경우:**

!!! info "권장 사양"

    - **메모리**: 32 GB RAM (기본 16 GB 대신)
    - **디스크 공간**: 50 GB 사용 가능 저장공간 (기본 10 GB 대신)

    이 사양 증가는 digna와 PostgreSQL 데이터베이스가 동시에 실행될 때를 고려한 권장사항입니다.

---

## 사전 설치 준비 {: #pre-installation-setup }

digna를 설치하기 전에 다음 두 가지 핵심 전제 조건이 준비되어 있는지 확인하세요:

1. **PostgreSQL 서버** – 계산된 메트릭 및 성능 데이터를 저장하기 위함
2. **웹 서버** – digna Dashboard를 호스팅하기 위함

이 구성요소들이 아직 설정되어 있지 않다면, 아래 섹션을 따라 설치 및 구성을 진행하세요.

---

## PostgreSQL 서버 설정 {: #postgresql-server-setup }

### 이미 PostgreSQL이 설치되어 있는 경우

PostgreSQL이 로컬 머신에 이미 설치되어 실행 중이거나 관리형 원격 PostgreSQL 서버를 사용하는 경우, [다음 섹션](#web-server-configuration)으로 건너뛰어도 됩니다.

### PostgreSQL 설치

Windows에 PostgreSQL을 설치하려면 다음 단계를 따르세요:

#### 1단계: PostgreSQL 다운로드

1. [PostgreSQL Downloads 페이지](https://www.postgresql.org/download/)로 이동
2. **Windows** 선택
3. 최신 설치 프로그램 다운로드

#### 2단계: 설치 프로그램 실행

1. 다운로드한 설치 프로그램 파일을 더블클릭
2. 설치 마법사의 안내를 따름

#### 3단계: 설치 디렉터리 선택

PostgreSQL이 설치될 디렉터리를 선택합니다. 기본 위치가 일반적으로 적합합니다.

#### 4단계: 구성요소 선택

표준 설정의 경우 기본 구성요소 옵션을 유지합니다.

#### 5단계: PostgreSQL 슈퍼유저 암호 설정

PostgreSQL 슈퍼유저(`postgres`)의 암호를 입력하고 확인합니다. **이 암호를 안전하게 보관**하세요 — 나중에 필요합니다.

#### 6단계: 포트 번호 구성

기본 PostgreSQL 포트는 `5432`입니다. 필요에 따라 기본값을 사용하거나 다른 포트를 지정할 수 있습니다.

!!! tip "팁"

    포트 5432가 이미 사용 중인 경우, 다른 포트를 선택하고 추후 구성 시 해당 포트를 기록해 두세요.

#### 7단계: 로케일 선택

데이터베이스의 로케일을 선택합니다. 기본값은 대부분의 설치에 적합합니다.

#### 8단계: 설치 완료

나머지 단계에서 **다음**을 클릭한 후 **마침**을 클릭합니다.

#### 9단계: 설치 확인

명령 프롬프트를 열고 PostgreSQL이 설치되었는지 확인합니다:

```bash
psql --version
```

설치가 성공적이면 PostgreSQL 버전이 표시됩니다.

---

## 웹 서버 구성 {: #web-server-configuration }

digna는 대시보드를 호스팅하기 위해 웹 서버가 필요합니다. 다음 옵션 중 하나를 선택하세요:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

이 중 하나의 서버만 설치 및 구성하면 됩니다.

### IIS 설정 {: #iis-setup }

#### 개요

Internet Information Services(IIS)는 웹사이트와 웹 애플리케이션을 호스팅하기 위한 Microsoft의 웹 서버입니다.

#### IIS 활성화

1. **제어판 열기**
   - `Win + R` 누름
   - `control` 입력 후 Enter

2. **Windows 기능으로 이동**
   - **프로그램** 클릭
   - **Windows 기능 켜기/끄기** 선택

3. **Internet Information Services 활성화**
   - 아래로 스크롤하여 **Internet Information Services (IIS)** 찾기
   - 체크박스를 체크하여 활성화
   - **+**를 클릭하여 아래 하위 구성요소가 선택되었는지 확인:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **확인(OK)** 클릭하여 변경 사항 적용

5. **IIS 설치 확인**
   - 브라우저 열기
   - `http://localhost`로 이동
   - IIS 환영 페이지가 표시되어야 함

#### 필수: URL Rewrite 모듈

IIS에는 URL Rewrite 구성요소가 필요합니다. [공식 Microsoft 페이지](https://www.iis.net/downloads/microsoft/url-rewrite)에서 다운로드하여 설치하세요.

#### 필수: Markdown 파일용 MIME 타입

IIS가 Markdown 파일(`.md`)을 올바르게 제공하려면:

1. **IIS 관리자** 열기 (`Win + R`, `inetmgr` 입력 후 Enter)
2. **사이트 > MIME Types**로 이동
3. **추가(Add...)** 클릭
4. 구성:
   - **파일 이름 확장자**: `.md`
   - **MIME 타입**: `text/markdown`

!!! warning "중요"

    이 설정이 없으면 `.md` 파일이 올바르게 서빙되지 않을 수 있습니다.

---

### Apache Tomcat 설정 {: #apache-tomcat-setup }

#### 개요

Apache Tomcat은 오픈소스 Java 서블릿 컨테이너이자 웹 서버입니다.

#### 설치

1. **Apache Tomcat 다운로드**
   - [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi) 방문
   - Windows ZIP 배포판 다운로드

2. **압축 해제**
   - ZIP 파일을 시스템의 디렉터리에 압축 해제
   - 예: `C:\Program Files\Apache Tomcat`

3. **Tomcat 실행 확인**
   - 브라우저 열기
   - `http://localhost:8080`로 이동
   - Apache Tomcat 환영 페이지가 표시되어야 함

!!! tip "팁"

    Apache Tomcat은 일반적으로 설치 후 자동으로 시작됩니다. 시작되지 않으면 `bin` 폴더로 이동하여 `startup.bat`을 실행하세요.

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

**다음 플레이스홀더를 교체하세요:**

- `<digna_repo_schema>` — 원하는 스키마 이름(예: `dignarepo`)
- `<digna_repo_user>` — 원하는 사용자 이름(예: `digna_user`)
- `<digna_repo_password>` — 이 사용자에 대한 안전한 비밀번호

**예시:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "권장사항"

    데이터베이스 사용자에는 강력하고 복잡한 암호를 사용하세요. 쉽게 추측 가능한 자격증명은 피하십시오.

---

### 2단계: digna 설치 패키지 압축 해제

1. 제공받은 digna 설치 ZIP 파일을 찾습니다
2. 원하는 설치 위치로 압축을 풉니다
3. 압축 해제 후 다음 항목들이 표시되어야 합니다:
   - `dashboard/` — 웹 대시보드 인터페이스
   - `digna` — 메인 실행 파일(백엔드 + CLI 포함)

!!! info "구성 파일과 라이선스 파일은 패키지에 포함되어 있지 않습니다"

    `config.toml`과 `dashboard/dashboard_config.toml`은 모두 설치 패키지에 포함되어 있지 않습니다.
    두 파일은 [백엔드 구성](#backend-configuration) 및
    [대시보드 구성](#dashboard-configuration)에서 직접 생성합니다. `license.toml`도 포함되어 있지 않으며,
    3단계에서 설명하는 것처럼 digna가 별도로 제공합니다.

### 3단계: 라이선스 파일 설치

!!! warning "중요"

    라이선스 파일은 설치 패키지에 포함되어 있지 않으며 digna에서 별도로 제공됩니다.

1. 제공받은 `license.toml` 파일을 찾습니다
2. `config.toml` 및 `digna` 실행 파일이 있는 digna 설치 루트 디렉터리에 복사합니다

**이유:**
라이선스 파일은 고객 정보, 라이선스 만료일 및 디지털 서명을 포함합니다. **이 파일을 수정하지 마세요** — 변경 시 라이선스가 무효화됩니다.

**설정 후 디렉터리 구조:**

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

`config_template.toml` 파일이 digna 설치 디렉터리에 제공됩니다. 이 파일의 이름을 `config.toml`로 변경하면 됩니다.

**위치:** `digna_installation/config.toml`

텍스트 편집기로 `config.toml`을 열고 아래 각 섹션을 구성하세요.

#### [app] 섹션

이 섹션은 대시보드와 백엔드 간의 교차 출처 리소스 공유(CORS)를 구성합니다:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| 매개변수 | 값 | 비고 |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | 대시보드 URL | 대시보드가 제공되는 URL. 그 밖의 오리진에서 오는 브라우저 요청은 거부됩니다 |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | 필수. 브라우저가 요청마다 세션 쿠키를 함께 보내도록 하는 데 필요합니다 |

!!! info "[app] 섹션은 선택 사항입니다"

    릴리스 2026.11부터는 두 키와 `[app]` 섹션 전체를 생략할 수 있습니다. 리버스 프록시가 대시보드와 백엔드를
    하나의 오리진으로 제공하는 경우에 적합한 구성입니다. 이 경우 브라우저는 교차 출처 요청을 보내지 않으며,
    기본적으로 어떤 교차 출처 요청도 허용되지 않습니다.

#### [repo] 섹션

이 섹션은 PostgreSQL 데이터베이스 연결을 구성합니다:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| 매개변수 | 값 | 비고 |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` 또는 IP | PostgreSQL 서버 호스트명/IP |
| `DIGNA_REPO_PORT` | `5432` (기본) | PostgreSQL 포트 |
| `DIGNA_REPO_DB` | `postgres` | 데이터베이스 이름 |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | 앞서 생성한 스키마 |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL 설정에서 생성한 사용자 |
| `DIGNA_REPO_PASSWORD` | 비밀번호 | 스키마 생성 시 설정한 비밀번호 |
| `DIGNA_REPO_SSLMODE` | `prefer` (기본) | 선택 사항. PostgreSQL SSL 모드: `disable`, `allow`, `prefer`, `require`, `verify-ca` 또는 `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (기본) | 선택 사항. digna가 리포지터리에 열어 두는 연결 수 |

#### [base] 섹션

이 섹션은 보안, 쿠키 및 검사 설정을 포함합니다:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| 매개변수 | 값 | 비고 |
|---|---|---|
| `DIGNA_FERNET_KEY` | 위에 표시된 값 | 이전 릴리스에서 사용하던 암호화 방식의 키. 반드시 있어야 하므로 위에 표시된 값을 그대로 유지하십시오 |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | 대시보드에 접속하는 호스트. `""`로 설정하면 도메인을 지정하지 않으며, 대시보드와 백엔드를 하나의 오리진으로 제공하는 프록시 뒤에서는 이것이 올바른 설정입니다 |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | digna를 HTTPS로 제공하는 경우 반드시 `true`여야 합니다 |
| `DIGNA_COOKIE_HTTPONLY` | `true` | 스크립트가 세션 쿠키에 접근하지 못하도록 합니다 |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24시간) | 세션 타임아웃(초) |
| `DIGNA_MAX_WORKERS` | CPU 코어 수 - 1 | 동시에 실행할 수 있는 검사 수 |
| `DIGNA_FRONTEND_BASEURL` | 대시보드 URL | 필수. 알림 메시지의 링크에 사용되므로 수신자가 열 수 있는 URL이어야 합니다 |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (기본) | 선택 사항. 소스 데이터베이스에 대한 단일 쿼리가 중단되기 전까지 실행될 수 있는 시간(초). `0`이면 타임아웃이 비활성화됩니다 |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (기본) | 선택 사항. 소스 데이터베이스 연결을 기다리는 시간(초). `0`이면 무기한 기다립니다 |

#### [encryption] 섹션

이 섹션에는 리포지터리에 저장된 민감한 값을 암호화하는 데 사용되는 키가 들어 있습니다. **필수**입니다 — 키가 없으면 `config check`는 `[encryption]` 섹션을 FAILED로 보고합니다.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| 매개변수 | 값 | 메모 |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64로 인코딩된 키 | digna 리포지터리에 저장된 민감한 값을 암호화합니다 |

!!! warning "config.toml 보호"

    이 키는 고정된 값으로 모든 digna 설치에서 동일하며, 리포지터리의 민감한 값을 복호화하는 것이 바로 이 키입니다. `config.toml` 접근을 digna를 실행하는 계정으로 제한하고, 버전 관리와 공유 드라이브에서 제외하며, 리포지터리 자체보다 덜 안전하게 보관되는 백업에서는 반드시 빼십시오.

#### [logging] 섹션

이 섹션은 로깅 동작을 구성합니다:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| 매개변수 | 값 | 비고 |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` 또는 `DEBUG` | 프로덕션에는 `INFO`, 문제 해결 시 `DEBUG`. `TRACE`, `WARN`, `ERROR`도 사용할 수 있습니다 |
| `DIGNA_LOGGING_DIR` | `logs` (기본) | 선택 사항. 순환되는 로그 파일을 저장할 디렉터리(작업 디렉터리 기준 상대 경로) |
| `DIGNA_LOGGING_MAX_FILES` | `30` (기본) | 선택 사항. 보관할 순환 로그 파일 수 |

!!! warning "서비스로 실행할 때는 로그 디렉터리를 유지하십시오"

    Windows 서비스에는 콘솔이 없으므로 로그 파일이 서비스의 동작을 보여 주는 유일한 기록입니다.
    `DIGNA_LOGGING_DIR`를 빈 문자열로 설정하지 마십시오. 빈 문자열은 로그 파일을 끕니다.

#### [duckdb] 섹션 (선택 사항) {: #duckdb-section }

릴리스 2026.11의 새 기능입니다. 이 섹션은 **digna Engine**의 리소스를 설정합니다. digna Engine은 프로파일링
위치가 **digna Engine**인 데이터베이스 연결에 대해 digna 내부에서 데이터를 프로파일링하고, 서로 다른 데이터베이스
연결에 있는 데이터 소스 간의 참조 무결성 검사를 실행합니다. 참조:
[프로파일링 위치](../../../platform/profiling/profiling_location.md).

이 섹션은 선택 사항입니다. 이 섹션이 없으면 아래의 기본값이 적용됩니다.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| 매개변수 | 값 | 비고 |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (기본) | digna Engine 실행 한 번이 사용할 수 있는 메모리(MB). 최대 `DIGNA_MAX_WORKERS`개의 실행이 동시에 활성화될 수 있습니다 |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | 기본값: digna를 실행하는 계정의 임시 디렉터리(`%TEMP%`) | 데이터가 메모리에 들어가지 않을 때 임시 파일을 저장할 디렉터리 |

!!! tip "digna Engine 용량 산정"

    digna 자체가 사용하는 메모리 외에, digna 호스트에 최대 `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB`의
    메모리를 추가로 계획하십시오. 또한 임시 디렉터리에는 digna Engine을 사용하는 데이터 소스 중 가장 큰 검사 날짜의
    데이터를 담을 수 있을 만큼의 여유 디스크 공간이 필요합니다. `DIGNA_DUCKDB_TEMP_DIRECTORY`가 그만한 공간이 있고
    digna를 실행하는 계정이 쓸 수 있는 디스크를 가리키도록 설정하십시오:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    이 섹션은 하나 이상의 데이터베이스 연결이 digna Engine을 사용하거나, 참조 무결성 검사가 서로 다른 연결에 있는
    데이터 소스를 비교하는 경우에만 필요합니다.

---

### 2단계: 구성 검증

리포지터리를 초기화하기 전에 `config.toml`이 완전하고 올바르게 구성되었는지 확인하십시오. digna 설치 디렉터리에서 다음을 실행합니다:

```bash
digna config check
```

각 섹션은 개별적으로 검증되므로 하나의 오류가 나머지 상태를 가리지 않습니다:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

FAILED로 보고된 모든 항목을 수정한 뒤, 계속하기 전에 명령을 다시 실행하십시오. **Unknown keys** 아래의 WARNING은 `config.toml`에 있지만 digna가 읽지 않는 키를 나열합니다. 이 키들은 아무 효과가 없으므로 제거하거나 철자를 바로잡으십시오. 전체 옵션 목록은 [CLI 참조](../../../cli/Command_Line_Interface_202611.md)에 있습니다.

### 3단계: 저장소 연결 테스트

1. 명령 프롬프트 열기
2. `config.toml` 및 `digna` 실행 파일이 있는 digna 설치 디렉터리로 이동
3. 연결 테스트 실행:

```bash
digna repo check
```

새 스키마에서는 명령이 연결한 다음, 아직 저장소가 설치되지 않았다고 보고합니다:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

이 시점에서는 이것이 예상된 결과이며, digna가 PostgreSQL과 스키마에 도달할 수 있음을 확인해 줍니다. 대신 연결 오류나 인증 오류가 나타나면 `[repo]` 섹션 또는 PostgreSQL 설정을 확인하세요.

### 4단계: 저장소 스키마 설치

동일한 디렉터리에서 다음을 실행하세요:

```bash
digna repo upgrade
```

이 명령은 저장소 스키마에 필요한 테이블을 설치하고 다음 메시지로 완료됩니다:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade는 설치와 업그레이드를 모두 수행합니다"

    릴리스 2026.11부터 `repo upgrade`는 새 저장소를 설치하고 기존 저장소를 업그레이드합니다.
    `repo install`도 같은 명령의 다른 이름으로 계속 사용할 수 있습니다.

### 5단계: 관리자 사용자 생성

관리자 사용자는 저장소 스키마에 직접 생성되므로 아직 서버를 실행할 필요가 없습니다. digna 설치 디렉터리에서 다음을 실행하세요:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**예시:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

이렇게 하면 전체 관리자 권한을 가진 사용자가 생성됩니다.

!!! tip "권장사항"

    대문자, 소문자, 숫자 및 특수문자가 조합된 강력한 비밀번호를 사용하세요.

### 6단계: digna 서버 시작

digna 설치 디렉터리에서 서버를 시작합니다:

```bash
digna serve --address <host> --port <port>
```

**매개변수:**
- `--address` — 서버 호스트명/IP (기본값 `127.0.0.1`)
- `--port` — 서버 포트 (기본값 `8000`)

서버가 시작되면 수신 대기 중인 주소를 출력합니다:

```text
Server running on http://127.0.0.1:8082
```

!!! note "서버가 터미널을 점유합니다"

    `serve`는 포그라운드에서 실행되며 ++ctrl+c++로 중지할 때까지 계속 동작합니다. 설정을 마칠 때까지 실행 상태로 두십시오. 대신 부팅 시 자동으로 시작하려면 다음을 참조하십시오: [digna를 Windows 서비스로 실행](#running-digna-as-a-windows-service).

---

## 대시보드 구성 {: #dashboard-configuration }

### 1단계: 대시보드를 웹 서버에 배포

digna 대시보드는 자체 구성을 `dashboard/dashboard_config.toml`에서 읽습니다. 이 파일은 설치 패키지에 포함되어 있지 않으므로, 대시보드 파일과 함께 `dashboard/` 디렉터리에 직접 생성해야 합니다.

파일의 내용은 [Single Sign-On](../../../sso/overview.md)에서 설명하며, 이 파일이 필요한 곳도 바로 그곳입니다. 이 파일에는 대시보드가 제공하는 로그인 옵션과, 다중 인스턴스 배포의 경우 백엔드 연결 정보가 담깁니다.

대시보드를 배포할 웹 서버를 선택하고 해당 배포 절차를 따르세요.

#### IIS에 배포

1. **IIS 관리자 열기**
   - `Win + R` 누름, `inetmgr` 입력 후 Enter

2. **새 웹사이트 생성**
   - 왼쪽 패널에서 **사이트(Sites)** 우클릭
   - **웹 사이트 추가(Add Website...)** 선택

3. **웹사이트 구성**
   - **사이트 이름**: 이름 입력(예: "dignaDashboard")
   - **물리적 경로(Physical Path)**: Browse를 클릭하고 `dashboard` 폴더 선택
   - **바인딩(Binding)**: IP 주소 및 포트 설정(기본 HTTP 포트 80, HTTPS는 443)

4. **웹사이트 시작**
   - **확인(OK)** 클릭하여 사이트 생성
   - 새로 생성된 사이트 우클릭 후 **시작(Start)** 선택

5. **설치 테스트**
   - 브라우저 열기
   - `http://localhost`(또는 구성한 URL)로 이동
   - digna 대시보드 로그인 페이지가 표시되어야 함

#### Apache Tomcat에 배포

1. **대시보드를 Tomcat에 복사**
   - `dashboard` 폴더를 Tomcat의 `webapps` 디렉터리에 복사
   - 필요 시 이름 변경(예: `digna`)
   - 예: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **배포 확인**
   - Tomcat 관리 페이지( http://localhost:8080 )를 새로고침하거나 다시 로드
   - 배포된 애플리케이션 목록에 "digna"(또는 선택한 이름)가 표시되어야 함

3. **대시보드 접근**
   - 브라우저 열기
   - `http://localhost:8080/digna`로 이동
   - digna 대시보드 로그인 페이지가 표시되어야 함

---

## digna를 Windows 서비스로 실행하기 {: #running-digna-as-a-windows-service }

### Windows 서비스를 사용하는 이유

digna 백엔드를 Windows 서비스로 실행하면 다음과 같은 이점이 있습니다:
- 서버 부팅 시 자동으로 시작됨
- 열린 명령 프롬프트 없이 백그라운드에서 실행됨
- 충돌 시 자동으로 재시작 가능
- Windows 서비스 관리 도구를 통해 관리 가능

### `windows` 명령

서비스는 `digna` 실행 파일 자체가 `digna windows` 하위 명령을 통해 관리합니다.
실행할 배치 파일은 없습니다.

| 명령 | 용도 |
|---|---|
| `digna windows install` | digna를 Windows 서비스로 등록 |
| `digna windows start` | 등록된 서비스를 시작 |
| `digna windows stop` | 실행 중인 서비스를 중지 |
| `digna windows uninstall` | 서비스 등록 해제 |

!!! warning "관리자 권한 필요"

    네 가지 명령은 모두 관리자 권한으로 연 명령 프롬프트에서 실행해야 합니다.

모든 명령은 `--name`을 받으므로 기본값이 아닌 이름으로 등록된 서비스도 지정할 수 있습니다. 전체
옵션 목록은 [CLI 참조](../../../cli/Command_Line_Interface_202611.md)에 있습니다.

### 서비스 설치

1. **관리자 권한으로 명령 프롬프트 열기**
   - 명령 프롬프트 오른쪽 클릭
   - "관리자 권한으로 실행(Run as Administrator)" 선택

2. **digna 설치 디렉터리로 이동**
   ```bash
   cd C:\path\to\digna
   ```

3. **서비스 등록**
   ```bash
   digna windows install
   ```

!!! important "기본값이 적합하지 않다면 주소와 포트를 지정하십시오"

    `install`은 주소와 포트를 서비스 등록 정보에 기록하며, 서비스는 기록된 값에 정확히 바인딩합니다.
    기본값은 `127.0.0.1`과 `8000`으로, 해당 머신 자체에서 오는 연결만 허용합니다. 다른 호스트에 있는
    대시보드는 여기에 접근할 수 없으므로, 백엔드가 수신 대기할 주소를 지정하십시오:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    이 값은 `config.toml`에서 읽지 않습니다. 나중에 변경하려면 서비스를 제거한 후 새 값으로
    다시 설치하십시오.

서비스는 **자동 시작**으로 등록되므로 Windows와 함께 시작됩니다. 서비스는 즉시 시작되지
않습니다 — 다음 섹션을 참조하세요.

#### 설치 옵션

| 옵션 | 기본값 | 용도 |
|---|---|---|
| `--name` | `digna` | 서비스를 등록할 이름 |
| `--display-name` | `digna` | services.msc에 표시되는 이름 |
| `--description` | `digna data quality backend` | services.msc에 표시되는 설명 |
| `--address` | `127.0.0.1` | 서비스가 API를 바인딩할 주소 |
| `--port` | `8000` | 서비스가 API를 바인딩할 포트 |
| `--working-dir` | `digna` 실행 파일이 있는 디렉터리 | `config.toml`과 `license.toml`이 있는 디렉터리로, 서비스는 이를 작업 디렉터리로 사용합니다 |
| `--start-type` | `auto` | `auto`는 Windows와 함께 시작, `manual`은 요청할 때만 시작, `disabled`는 서비스를 등록하지만 시작을 거부합니다 |
| `--account` | `LocalSystem` | 서비스를 실행할 계정, 예: `DOMAIN\user` 또는 `.\user` |
| `--password` | | `--account`의 암호 |

!!! tip "도메인 계정으로 실행하기"

    `LocalSystem`에는 네트워크 ID가 없으므로 SQL Server에 대한 Windows 인증과 네트워크 공유에 대한
    모든 접근이 실패합니다. 서비스가 특정 사용자로 리소스에 접근해야 하는 경우 `--account`와
    `--password`를 지정하여 설치하십시오.

### 서비스 시작 및 중지

#### 서비스를 시작하려면

```bash
digna windows start
```

#### 서비스를 중지하려면

```bash
digna windows stop
```

!!! tip "팁"

    애플리케이션 파일을 업데이트하기 전에 항상 서비스를 중지하세요.

### 서비스를 새 디렉터리로 이동하기

digna 설치 위치를 이동해야 하는 경우:

1. **현재 서비스 중지 및 등록 해제**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **애플리케이션 파일 이동**
   - 전체 digna 설치 폴더를 새 위치로 이동

3. **새 위치에서 서비스 다시 등록**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   처음에 사용한 `--address`, `--port` 또는 `--account` 값을 다시 지정하십시오 — 이전
   등록 정보는 삭제되었습니다.

4. **서비스 시작**
   ```bash
   digna windows start
   ```

### 서비스 제거

1. **실행 중인 서비스 중지**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **서비스 등록 해제**
   ```bash
   digna windows uninstall
   ```

이제 digna 서버는 Windows 서비스에서 등록 해제됩니다.

---

## 새 릴리스로 업그레이드하기 {: #upgrading-to-a-new-release }

이 섹션에서는 릴리스 2026.06 설치를 릴리스 2026.11로 업그레이드합니다. 설치가 그보다 오래된 경우 먼저
[릴리스 2026.06 이전 릴리스에서 업그레이드](#upgrading-from-a-release-before-2026-06)를 읽으십시오.

### 업그레이드 전에

**digna 저장소 백업 생성은 필수입니다**

digna를 업그레이드하기 전에 저장소(PostgreSQL)를 백업하여 데이터 손실에 대비하십시오.
백업이 있으면 업그레이드 중 예기치 않은 문제가 발생해도 복구할 수 있습니다.

**릴리스 2026.11용 라이선스 파일 요청**

릴리스 2026.11에는 새 `license.toml`이 필요합니다. 시작하기 전에 digna 팀에 요청하고,
[7단계](#step-7-replace-the-license-file)에서 사용할 수 있도록 준비해 두십시오.

### 릴리스 2026.06 이전 릴리스에서 업그레이드 {: #upgrading-from-a-release-before-2026-06 }

릴리스 2026.06에서는 세 가지 변경 사항이 도입되었으며, 이전 설치를 2026.11로 바로 업그레이드할 때에도
여전히 적용됩니다:

- **ODBC 전용.** digna는 모든 소스 기술에 ODBC로 접근합니다. 아직 ODBC를 사용하지 않는 모든 데이터베이스 연결은
  업그레이드 후 ODBC로 변경해야 하며, 자동 변환은 없습니다. 미리 digna 호스트에 ODBC 드라이버를 설치하고(참조:
  [digna 호스트에 ODBC 드라이버 설치](../../../databases/overview.md#install-the-driver)),
  [기술별 안내서](../../../databases/overview.md#technology-guides)를 참고해 각 연결의 속성을 준비해 두십시오.
  Databricks Legacy 커넥터는 더 이상 존재하지 않습니다. 해당 연결은
  [Databricks](../../../databases/databricks_connector_guide.md) 커넥터로 이전하십시오.
- **단일 실행 파일.** `dignabackend`와 `dignacli`는 백엔드와 CLI를 통합한 단일 실행 파일 `digna`로
  대체되었습니다.
- **config.toml.** `[encryption]` 섹션이 필수이며, `DIGNA_APP_HOST`와 `DIGNA_APP_PORT`는 더 이상 읽지 않습니다.
  서버는 주소와 포트를 `digna serve`에서 받습니다. 사용 중인 파일을 [백엔드 구성](#backend-configuration)과
  비교하십시오.

아래 단계에서는 이전 설치에서 다른 작업이 필요한 부분을 알려 줍니다. 8단계의 저장소 업그레이드는 이전 어느 릴리스의
저장소든 바로 2026.11로 업그레이드합니다.

### 업그레이드 절차

#### 1단계: digna 서비스 중지 {: #step-1-stop-the-digna-service }

관리자 권한으로 명령 프롬프트를 열고 현재 설치의 `digna` 실행 파일로 서비스를 중지하십시오:

```bash
cd C:\path\to\digna
digna windows stop
```

서비스 등록은 그대로 유지됩니다. 새 실행 파일이 같은 디렉터리에서 이전 실행 파일을 대체하므로 등록은 계속
올바른 파일을 가리킵니다.

digna가 포그라운드에서 실행 중이면 해당 명령 프롬프트 창에서 ++ctrl+c++를 누르십시오.

!!! warning "릴리스 2026.06 이전 릴리스에서 업그레이드하는 경우"

    릴리스 2026.06 이전에는 서비스가 배치 파일로 등록되었습니다. 2단계에서 이름을 변경하기 **전에** 현재 설치의
    배치 파일로 서비스를 중지하고 등록을 해제하십시오:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    서비스가 실행되던 계정과 서비스가 사용하던 주소 및 포트를 기록해 두십시오. 9단계에서 서비스를 다시
    등록합니다.

#### 2단계: 현재 설치 백업 {: #step-2-backup-current-installation }

digna 설치 디렉터리에서 현재 설치의 실행 파일과 대시보드 폴더 이름을 변경하여, 새 릴리스를 나란히 배포할 수
있도록 하십시오:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

`digna_old.exe`는 업그레이드를 확인할 때까지, `dashboard_old`는 거기에서 구성 파일을 복원할 때까지 보관하십시오
(4단계 참조). 그 후에는 둘 다 삭제해도 됩니다.

!!! info "릴리스 2026.06 이전 릴리스에서 업그레이드하는 경우"

    실행 파일 대신 `dignabackend`와 `dignacli` 폴더의 이름을 변경하십시오:
    `ren dignabackend dignabackend_old` 및 `ren dignacli dignacli_old`. 릴리스 2026.11은 두 폴더도, 배치 파일이 들어 있는 `bin` 폴더도 사용하지 않습니다.

#### 3단계: 새 버전 압축 해제 및 배포 {: #step-3-extract-and-deploy-new-version }

1. 새 digna 설치 ZIP 파일을 압축 해제합니다.
2. 새 `digna` 실행 파일과 `dashboard` 폴더를 설치 디렉터리에 복사합니다.

!!! warning "중요"

    `config.toml`과 `dashboard/dashboard_config.toml`은 모두 설치 ZIP에 절대 포함되지 않습니다.
    digna 팀은 두 파일 중 어느 것도 제공하지 않습니다. 따라서 기존 구성은 업그레이드의 영향을 받지 않으며,
    이름이 변경된 `*_old` 폴더에 있는 사본이 유일한 사본입니다.

#### 4단계: 구성 파일 복원 {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

릴리스 2026.11에서는 `config.toml`을 변경할 필요가 없습니다. 릴리스 2026.06에서 동작하는 파일은 계속 동작합니다.
다음 두 가지 변경은 선택 사항입니다:

- 데이터베이스 연결에서 digna Engine을 사용하고 그 기본값이 호스트에 맞지 않는 경우
  [`[duckdb]` 섹션](#duckdb-section)을 추가합니다.
- 리버스 프록시가 대시보드와 백엔드를 하나의 오리진으로 제공하는 경우 `[app]` 섹션을 생략합니다.

!!! warning "digna가 읽지 않는 설정"

    이 가이드의 이전 버전에는 digna가 읽지 않는 일부 설정이 나와 있었습니다. 이 설정들은 아무 효과가 없으며,
    6단계에서 `config check`가 **Unknown keys** 아래에 나열합니다. 제거하거나 수정하십시오:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` 및
      `digna_LOGGING_BACKUP_COUNT`는 존재하지 않습니다. 제거하십시오.
    - 설정 이름은 대소문자를 구분합니다. digna는 `digna_REPO_HOST`가 아니라 `DIGNA_REPO_HOST`를 읽습니다.
      [백엔드 구성](#backend-configuration)에서처럼 모든 이름을 대문자로 작성하십시오.

!!! warning "Single Sign-On: [[oidc_clients]]를 유지하십시오"

    digna는 Single Sign-On 공급자를 `[[oidc_clients]]` 항목의 목록으로 읽으며, 각 항목에는 고유한
    `DIGNA_OIDC_KEY`가 있습니다. 이 가이드의 이전 버전에 따라 공급자를 `[oidc_clients.<key>]` 섹션으로 변경했다면
    다시 원래대로 되돌리십시오. 그 형식이 남아 있는 동안 `config check`는 `OIDC config(s)`를 FAILED로 보고합니다:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    공급자마다 이 항목을 반복하고, 각 `DIGNA_OIDC_KEY`를 `dashboard_config.toml`의 `key`와 동일하게 유지하십시오.
    Single Sign-On을 사용하는 설치에만 해당됩니다.

#### 5단계: 웹 서버 다시 로드 {: #step-5-reload-the-web-server }

대시보드는 정적 파일의 집합이므로, 웹 서버와 브라우저가 여전히 이전 버전을 제공하고 있을 수 있습니다.
`dashboard` 폴더를 호스팅하는 웹 서버를 다시 로드하거나 재시작한 다음, 강력 새로 고침(++ctrl+f5++)으로 페이지를 다시 로드하십시오.

#### 6단계: 구성 검증 {: #step-6-validate-the-configuration }

리포지터리를 건드리기 전에 `config.toml`이 완전한지 확인하십시오:

```bash
digna config check
```

모든 섹션이 OK로 보고되어야 합니다. FAILED로 보고된 항목을 모두 수정하고 **Unknown keys** 아래에 나열된 키를
제거한 다음, 계속하기 전에 명령을 다시 실행하십시오.

#### 7단계: 라이선스 파일 교체 {: #step-7-replace-the-license-file }

라이선스 파일은 보통 한 릴리스에서 다음 릴리스로 그대로 이어집니다. 릴리스 2026.11은 예외입니다. 이 릴리스는
라이선스가 필요한 두 모듈, digna Data Reconciliation과 digna Agentic을 추가하며, 2026.11 이전에 발급된
라이선스에는 이 모듈들이 포함되어 있지 않습니다. digna 팀이 릴리스 2026.11용으로 제공한 `license.toml`을
설치 디렉터리에 복사하여 기존 파일을 교체하십시오:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "이전 라이선스를 유지하지 마십시오"

    이전 라이선스로도 digna는 시작되지만, digna Data Reconciliation과 digna MCP Server는 비활성화된 상태로 남습니다.
    라이선스를 확인하는 모든 명령(`user`, `inspection`, `repo`)은 확인에 실패하면 리포지터리를 건드리기 전에
    중단됩니다. 다음 단계로 넘어가기 전에 새 라이선스를 확인하십시오:

    ```bash
    digna license check
    ```

#### 8단계: 저장소 스키마 업그레이드 {: #step-8-upgrade-the-repository-schema }

digna 설치 디렉터리에서 다음을 실행하십시오:

```bash
digna repo upgrade
```

릴리스 2026.11은 버전이 지정된 마이그레이션으로 저장소 스키마를 관리합니다. 이전 릴리스에서 처음 업그레이드할 때는
스키마를 이전 방식의 마지막 버전으로 올리고, 이를 시작점으로 기록한 다음, 릴리스 2026.11의 마이그레이션을
적용합니다. 다음 메시지로 완료됩니다:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

기존 데이터는 모두 보존됩니다. 언제든지 `digna repo check`를 실행하면 저장소 상태를 확인할 수 있으며,
마지막으로 적용된 마이그레이션과 대기 중인 마이그레이션이 나열됩니다.

!!! warning "저장소가 최신이 아니면 digna가 시작되지 않습니다"

    릴리스 2026.11부터는 저장소 업그레이드가 필요한 동안 서버가 시작을 거부하고 그 사실을 알려 줍니다. 예:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    서버나 서비스를 시작하기 전에 `repo upgrade`를 실행하십시오.

#### 9단계: 서비스 재시작 {: #step-9-restart-services }

digna가 Windows 서비스로 실행되는 경우 다시 시작하십시오:

```bash
cd C:\path\to\digna
digna windows start
```

릴리스 2026.06 이전 릴리스에서 업그레이드하면서 1단계에서 서비스 등록을 해제했다면, 먼저 `digna` 실행 파일로
서비스를 다시 등록하십시오:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

기본값인 `127.0.0.1`과 `8000`을 사용하려는 경우가 아니라면 `--address`와 `--port`에 이전 서비스가 사용하던 값을
지정하십시오. 이전 서비스가 도메인 계정으로 실행되었다면 `--account`와 `--password`를 추가하십시오. 전체 옵션
목록은 [digna를 Windows 서비스로 실행하기](#running-digna-as-a-windows-service)를 참조하십시오.

수동으로 실행 중인 경우 서버를 재시작하십시오:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

IIS 또는 Tomcat을 사용하는 경우 해당 웹 서버를 재시작하십시오.

#### 10단계: 업그레이드 확인 {: #step-10-verify-the-upgrade }

1. 새 실행 파일의 릴리스를 확인합니다:

    ```bash
    digna version
    ```

    첫 번째 줄이 `Release: 2026.11`이어야 합니다.

2. digna 대시보드에 접속하여 인터페이스가 올바르게 로드되는지 확인합니다.
3. 설치 디렉터리의 `logs` 디렉터리에 있는 파일에 오류가 있는지 확인합니다.
4. 데이터베이스 연결을 테스트합니다. 참조:
   [연결 테스트](../../../databases/overview.md#testing-a-connection). 릴리스 2026.06 이전 릴리스에서
   업그레이드한 경우 먼저 아직 ODBC를 사용하지 않던 모든 연결을 ODBC로 전환하십시오.

새 모듈을 시작하려면 [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
digna MCP Server에 대해서는 [AI 에이전트 연결](../../../platform/agentic/connect_ai_agent.md),
digna Engine에 대해서는 [프로파일링 위치](../../../platform/profiling/profiling_location.md)를 참조하십시오.

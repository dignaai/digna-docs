# macOS용 digna 설치 안내 Release 2026.06

**릴리스:** 2026.06

**최종 업데이트:** 2026년 9월 5일


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
9. [digna를 백그라운드 서비스로 실행하기](#running-digna-as-a-background-service)
10. [새 릴리스로 업그레이드하기](#upgrading-to-a-new-release)

---

## 소개 {: #introduction }

### digna에 관하여

digna는 데이터 웨어하우스, 데이터 레이크, 레이크하우스 등 다양한 데이터 환경에서 데이터 품질 관리를 최적화하도록 설계된 AI 기반 플랫폼입니다. 자동화, 실시간 모니터링 및 이상 탐지를 통해 현대 데이터 문제를 해결할 수 있도록 높은 확장성과 적응성을 갖추고 있습니다.

digna는 두 가지 주요 구성 요소로 이루어져 있습니다:

- **dignabackend**: 데이터 처리 및 품질 검사를 담당하는 핵심 엔진입니다.
- **dignadashboard**: 웹 서버에 호스팅되는 웹 기반 인터페이스로, digna 플랫폼과 상호작용하고 데이터 품질 지표를 시각화하는 사용자 친화적 수단을 제공합니다.

### Release 2026.06의 변경 사항

이번 릴리스는 데이터 관찰 가능성(data observability) 기능을 코드 안으로 직접 제공하여 개발자가 소스에서 데이터 품질을 모니터링할 수 있게 합니다. 전체 내용은 [릴리스 노트](http://docs.digna.ai/changelog/Release_202606/)를 참조하세요.

### Windows 또는 Linux용 안내를 찾고 계신가요?

이 가이드는 macOS를 다룹니다. 다른 플랫폼은 [Windows 설치 안내](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) 또는 [Linux 설치 안내](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md)를 참조하세요.

---

## 시스템 요구사항 {: #system-requirements }

설치를 시작하기 전에 시스템이 다음 최소 요구사항을 충족하는지 확인하세요:

| 요구사항 | 사양 |
|---|---|
| **운영체제** | macOS 13 (Ventura) 이상 |
| **아키텍처** | Apple Silicon (arm64) 또는 Intel (x86_64) |
| **메모리 (최소 구성)** | 16 GB RAM |
| **디스크 공간** | 10 GB 사용 가능 저장소 |
| **데이터베이스** | PostgreSQL Server 12 이상 |
| **웹 서버** | nginx, Apache httpd 또는 동등한 서버 |
| **명령줄 도구** | Xcode Command Line Tools (Homebrew에서 필요) |

### 데이터베이스 설치 옵션

**PostgreSQL가 이미 설치되어 있는 경우:**
기존 PostgreSQL 서버에 digna용 새 데이터베이스를 추가할 수 있습니다.

**digna와 동일한 머신에 PostgreSQL을 설치하는 경우:**

!!! info "권장 사양"

    - **메모리**: 32 GB RAM (16 GB 대신)
    - **디스크 공간**: 50 GB 사용 가능 저장소 (10 GB 대신)

    이 권장 사양은 digna와 PostgreSQL 데이터베이스가 동시에 실행될 때를 고려한 것입니다.

### 아키텍처 확인 방법

이 가이드의 여러 경로는 Apple Silicon과 Intel Mac 간에 다릅니다. 어느 쪽인지 확인하려면 **터미널**을 열고 다음을 실행하세요:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew는 `/opt/homebrew`에 설치됩니다.
- `x86_64` — Intel. Homebrew는 `/usr/local`에 설치됩니다.

!!! tip "팁"

    어느 경로든 하드코딩하기보다는, 이 가이드에서는 `$(brew --prefix)`를 사용합니다. 이 명령은 두 아키텍처 모두에서 올바른 위치로 확장되므로 명령을 그대로 복사해서 사용할 수 있습니다.

---

## 사전 설치 준비 {: #pre-installation-setup }

digna를 설치하기 전에 다음 세 가지 주요 필수 요소가 준비되어 있는지 확인하세요:

1. **Homebrew** – 아래 구성 요소를 설치하는 데 사용되는 패키지 관리자
2. **PostgreSQL 서버** – 계산된 메트릭 및 성능 데이터를 저장하기 위한 데이터베이스
3. **웹 서버** – digna 대시보드를 호스팅하기 위한 서버

이들 구성 요소가 아직 설정되어 있지 않다면, 아래 섹션을 따라 설치 및 구성하세요.

### Homebrew 설치

Homebrew는 macOS의 표준 패키지 관리자이며 이 가이드 전반에서 PostgreSQL과 nginx를 설치하는 데 사용됩니다.

#### 1단계: Homebrew가 이미 설치되어 있는지 확인

**터미널**을 열고(유틸리티에서 또는 `Cmd + Space` 후 Terminal 입력) 다음을 실행하세요:

```bash
brew --version
```

버전 번호가 반환되면 [PostgreSQL 서버 설정](#postgresql-server-setup) 섹션으로 건너뛰세요.

#### 2단계: Homebrew 설치

명령을 찾을 수 없는 경우, [공식 Homebrew 사이트](https://brew.sh)의 지침에 따라 Homebrew를 설치하세요. 설치 프로그램은 Xcode Command Line Tools가 없는 경우 이를 함께 설치합니다.

#### 3단계: Homebrew를 PATH에 추가

Apple Silicon에서는 설치 프로그램이 Homebrew를 셸 환경에 추가하기 위한 두 명령을 출력합니다. 지시에 따라 해당 명령을 실행한 후 다음을 확인하세요:

```bash
brew --prefix
```

Apple Silicon에서는 `/opt/homebrew`를, Intel에서는 `/usr/local`을 출력해야 합니다.

---

## PostgreSQL 서버 설정 {: #postgresql-server-setup }

### 이미 PostgreSQL이 있는 경우

PostgreSQL이 로컬 머신에서 이미 실행 중이거나 관리형 원격 PostgreSQL 서버를 사용하는 경우, [다음 섹션](#web-server-configuration)으로 건너뛰세요.

### 설치 옵션

macOS에서는 PostgreSQL을 설치하는 두 가지 간단한 방법이 있습니다. 하나만 선택하세요:

- [Homebrew](#postgresql-homebrew) — 명령줄 설치, 서버 배포에 권장
- [Postgres.app](#postgresql-app) — 그래픽 설치, 로컬 평가에 편리

### Homebrew로 PostgreSQL 설치 {: #postgresql-homebrew }

#### 1단계: PostgreSQL 포뮬러 설치

```bash
brew install postgresql@16
```

#### 2단계: PostgreSQL을 PATH에 추가

버전 지정 포뮬러는 *keg-only*이므로 Homebrew가 자동으로 명령을 PATH에 연결하지 않습니다. 직접 추가하세요:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "참고"

    macOS의 기본 셸인 `zsh`를 가정한 예입니다. `bash`를 사용하는 경우 동일한 줄을 `~/.bash_profile`에 추가하세요.

#### 3단계: PostgreSQL 서비스 시작

```bash
brew services start postgresql@16
```

이 명령은 PostgreSQL을 즉시 시작하고 로그인할 때 자동으로 다시 시작되도록 구성합니다.

#### 4단계: 설치 확인

```bash
psql --version
```

설치가 성공했다면 PostgreSQL 버전이 표시됩니다.

#### 5단계: 서버에 연결

```bash
psql postgres
```

!!! warning "중요 — macOS는 이 부분에서 Windows와 다릅니다"

    Windows 설치 관리자는 `postgres` 슈퍼유저와 비밀번호를 생성하도록 안내합니다. Homebrew는 그렇지 않습니다. 대신 macOS 계정 이름으로 된 슈퍼유저를 생성하며 비밀번호가 없고 로컬 머신에서만 접근할 수 있습니다.

    따라서 초기 Homebrew 설치에는 `postgres` 역할이 없습니다. 슈퍼유저가 필요할 때는 자신의 계정 이름을 사용하고, [초기 설치](#initial-installation)에 설명된 대로 명시적인 digna 사용자를 생성하세요.

#### 6단계: 포트 확인

기본 PostgreSQL 포트는 `5432`입니다. 서버가 어느 포트를 수신하는지 확인하려면:

```bash
psql postgres -c "SHOW port;"
```

이 값을 기록해 두세요 — digna 백엔드를 구성할 때 필요합니다.

### Postgres.app로 PostgreSQL 설치 {: #postgresql-app }

그래픽 설치를 선호하는 경우:

1. [Postgres.app](https://postgresapp.com)을 다운로드하여 **Applications** 폴더로 드래그합니다.
2. 앱을 열고 **Initialize**를 클릭하여 새 서버를 만듭니다.
3. 앱의 지침에 따라 명령줄 도구를 PATH에 추가합니다.
4. 설치 확인:

```bash
psql --version
```

Postgres.app은 macOS 계정 이름으로 된 슈퍼유저도 생성합니다.

---

## 웹 서버 구성 {: #web-server-configuration }

digna는 대시보드를 호스팅하기 위해 웹 서버가 필요합니다. 다음 옵션 중 하나를 선택하세요:

- [nginx](#nginx-setup) — Homebrew로 설치, 권장
- [Apache httpd](#apache-setup) — macOS에 포함

이 중 하나만 설치하고 구성하면 됩니다.

두 섹션 모두 대시보드가 의존하는 두 가지를 구성합니다:

- **단일 페이지 애플리케이션(fallback)** — 대시보드 URL을 새로고침해도 404가 반환되지 않도록 함
- **`.md` MIME 타입** — Markdown 파일이 올바르게 제공되도록 함

### nginx 설정 {: #nginx-setup }

#### 개요

nginx는 정적 digna 대시보드를 제공하는 데 적합한 가볍고 고성능의 웹 서버입니다.

#### 설치

```bash
brew install nginx
```

#### nginx 시작

```bash
brew services start nginx
```

#### 설치 확인

1. 브라우저를 엽니다.
2. `http://localhost:8080`로 이동합니다.
3. nginx 환영 페이지가 표시되어야 합니다.

!!! note "참고 — 기본 포트는 8080이며 80이 아닙니다"

    Homebrew는 관리자 권한 없이 실행할 수 있도록 nginx를 포트 `8080`으로 설정합니다. macOS에서 포트 `80` 또는 1024 미만의 다른 포트에 바인딩하려면 루트 권한이 필요합니다.

    대시보드를 포트 80에서 제공하려면 아래 구성에서 `listen 8080;`을 `listen 80;`으로 변경하고 대신 `sudo brew services start nginx`로 시작하세요.

#### 대시보드용 사이트 구성

Homebrew의 nginx 구성은 `servers` 디렉터리의 모든 파일을 포함합니다. digna용 전용 구성 파일을 생성하세요:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

다음 내용을 붙여넣고 `/path/to/digna/dashboard`를 압축을 푼 `dashboard` 폴더의 실제 경로로 바꾸세요:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "중요"

    `try_files` 지시어가 없으면 루트 URL이 아닌 대시보드 페이지를 새로고침할 때 404가 반환됩니다. 이는 Windows의 IIS에서 요구되는 URL Rewrite 모듈과 동등한 nginx 설정입니다.

#### 구성 적용

구성 문법 오류가 없는지 테스트한 다음 nginx를 다시 로드하세요:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd 설정 {: #apache-setup }

#### 개요

macOS에는 Apache httpd가 포함되어 있어 별도 설치가 필요 없습니다. 기본적으로 비활성화되어 있습니다.

#### Apache 시작

```bash
sudo apachectl start
```

#### 설치 확인

1. 브라우저를 엽니다.
2. `http://localhost`로 이동합니다.
3. "It works!" 메시지가 표시되어야 합니다.

#### 필수: mod_rewrite 활성화

대시보드는 URL 재작성 기능이 필요합니다. Apache 구성 파일을 엽니다:

```bash
sudo nano /etc/apache2/httpd.conf
```

다음 줄을 찾아 앞의 `#`를 제거하여 주석을 해제하세요:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### 필수: .htaccess 재정의 허용

같은 파일에서 `<Directory "/Library/WebServer/Documents">` 블록을 찾아 다음을 변경하세요:

```apache
AllowOverride None
```

다음으로:

```apache
AllowOverride All
```

#### 필수: Markdown 파일용 MIME 타입

여전히 `httpd.conf`에서 Markdown 파일이 올바르게 제공되도록 다음 줄을 추가하세요:

```apache
AddType text/markdown .md
```

!!! warning "중요"

    이 설정이 없으면 `.md` 파일이 제대로 제공되지 않을 수 있습니다.

#### 구성 적용

구성 문법 오류를 검사한 다음 Apache를 다시 시작하세요:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## 초기 설치 {: #initial-installation }

### 1단계: digna 리포지토리 설정

digna 리포지토리는 digna가 계산한 모든 메트릭을 저장합니다. 분석 및 성능 데이터의 중앙 데이터베이스 역할을 합니다.

#### 리포지토리 스키마 및 사용자 생성

PostgreSQL 클라이언트(psql, pgAdmin 등)를 열고 다음 SQL 명령을 실행하세요:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**다음 플레이스홀더를 교체하세요:**

- `<digna_repo_schema>` — 원하는 스키마 이름(예: `dignarepo`)
- `<digna_repo_user>` — 원하는 사용자 이름(예: `digna_user`)
- `<digna_repo_password>` — 이 사용자의 안전한 비밀번호

**예시:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

터미널에서 한 번에 실행하려면:

```bash
psql postgres
```

그런 다음 `postgres=#` 프롬프트에 위 명령들을 붙여넣고 `\q`를 입력하여 종료하세요.

!!! tip "권장 사항"

    데이터베이스 사용자에는 강력하고 복잡한 비밀번호를 사용하세요. 쉽게 추측 가능한 자격증명은 피하세요.

---

### 2단계: digna 설치 패키지 압축 해제

1. 제공된 digna 설치 ZIP 파일을 찾습니다.
2. 예를 들어 `/opt/digna` 또는 `~/digna`와 같은 원하는 설치 위치에 압축을 풉니다.
3. 압축을 풀면 다음 항목이 보여야 합니다:
   - `dashboard/` — 웹 대시보드 인터페이스
   - `digna` — 메인 실행 파일(백엔드 + CLI 통합)
   - `config.toml` — 구성 파일
   - `license.toml` — 라이선스 파일(별도로 복사)

터미널에서 압축을 풀려면:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### 실행 파일에 실행 권한 부여

아카이브 전송 방법에 따라 실행 비트가 유지되지 않을 수 있습니다. 명시적으로 설정하세요:

```bash
cd /opt/digna
chmod +x digna
```

#### macOS가 애플리케이션을 차단하는 경우

브라우저나 메일 클라이언트를 통해 다운로드된 파일에는 격리(quarantine) 속성이 추가됩니다. macOS에서 앱을 *"개발자를 확인할 수 없어 열 수 없습니다"*라고 보고하면 설치 디렉터리에서 해당 속성을 제거하세요:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

또는 **시스템 설정 → 개인정보 및 보안**을 열어 페이지 하단 근처에서 차단된 항목을 찾아 **열기 허용(Open Anyway)** 을 클릭하세요.

!!! note "참고"

    이 단계는 macOS가 실제로 실행 파일을 차단할 때만 필요합니다. SSH로 전송되었거나 내부 파일 공유로 전달된 패키지는 일반적으로 격리되지 않습니다.

### 3단계: 라이선스 파일 설치

!!! warning "중요"

    라이선스 파일은 설치 패키지에 포함되어 있지 않으며 digna에서 별도로 제공합니다.

1. 제공된 `license.toml` 파일을 찾습니다.
2. `config.toml` 및 `digna` 실행 파일이 있는 digna 설치 루트 디렉터리에 복사합니다.

**이유:**
라이선스 파일에는 고객 정보, 라이선스 만료일 및 디지털 서명이 포함되어 있습니다. **이 파일을 수정하지 마세요** — 변경하면 무효화됩니다.

**설치 후 디렉터리 구조 예시:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## 백엔드 구성 {: #backend-configuration }

### 1단계: 구성 파일 생성 및 편집

`config_template.toml` 파일이 digna 설치 디렉터리에 제공됩니다. 이를 `config.toml`로 이름만 변경하면 됩니다.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**위치:** `/opt/digna/config.toml`

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

| 매개변수 | 값 | 설명 |
|---|---|---|
| `digna_APP_HOST` | `localhost` 또는 IP 주소 | dignabackend가 호스팅되는 호스트명 또는 IP |
| `digna_APP_PORT` | `8082` (기본) | REST API 엔드포인트 포트 |
| `digna_APP_CORS_ALLOW_ORIGINS` | 프론트엔드 URL | 대시보드가 다른 서버에 있다면 해당 URL 포함 |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | 자격증명 있는 CORS에 필요 |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | 모든 HTTP 메서드를 허용 |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | 모든 헤더를 허용 |

!!! note "참고"

    Homebrew의 nginx 기본 포트에서 대시보드를 제공하는 경우 허용할 origin은 `http://localhost:8080`입니다.

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

| 매개변수 | 값 | 설명 |
|---|---|---|
| `digna_REPO_HOST` | `localhost` 또는 IP | PostgreSQL 서버 호스트명/IP |
| `digna_REPO_PORT` | `5432` (기본) | PostgreSQL 포트 |
| `digna_REPO_DB` | `postgres` | 데이터베이스 이름 |
| `digna_REPO_SCHEMA` | `dignarepo` | 이전에 생성한 스키마 |
| `digna_REPO_USER` | `digna_user` | PostgreSQL 설정에서 생성한 사용자 |
| `digna_REPO_PASSWORD` | 비밀번호 | 스키마 생성 시 설정한 비밀번호 |

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

| 매개변수 | 값 | 설명 |
|---|---|---|
| `digna_FERNET_KEY` | 암호화 키 | 토큰과 쿠키 암호화에 사용 (기본값 제공) |
| `digna_COOKIE_DOMAIN` | `localhost` | 프론트엔드 도메인과 일치시킴 |
| `digna_COOKIE_SECURE` | `false` (로컬) / `true` (프로덕션) | HTTPS 연결에서는 `true` 사용 |
| `digna_COOKIE_HTTPONLY` | `true` | 보안을 위해 항상 활성화 |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF 공격 방지 목적 |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24시간) | 세션 만료 시간(초) |
| `digna_MAX_WORKERS` | CPU 코어 수 - 1 | 병렬 검사 작업 수 |

!!! tip "팁"

    Mac에서 사용 가능한 CPU 코어 수를 확인하려면 `sysctl -n hw.ncpu`를 실행하세요.

#### [logging] 섹션

이 섹션은 로깅 동작을 구성합니다:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| 매개변수 | 값 | 설명 |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` 또는 `DEBUG` | 운영 환경은 `INFO`, 문제 해결 시 `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | 보관할 일별 로그 백업 수 |

---

### 2단계: 리포지토리 초기화

1. **터미널**을 엽니다.
2. digna 설치 디렉터리(예: `config.toml`과 `digna` 실행 파일이 있는 위치)로 이동합니다.
3. 연결 테스트를 실행하세요:

```bash
cd /opt/digna
./digna repo check
```

연결이 설정되었다는 확인 메시지가 표시되어야 합니다(리포지토리 자체는 아직 초기화되지 않았습니다).

!!! note "참고"

    macOS에서는 현재 디렉터리의 명령이 PATH에 포함되지 않으므로 실행 파일을 `digna`가 아닌 `./digna`로 호출합니다. 모든 곳에서 짧은 형태를 사용하려면 설치 디렉터리를 PATH에 추가하세요:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### 3단계: 리포지토리 스키마 설치

같은 디렉터리에서 다음을 실행하세요:

```bash
./digna repo install
```

이 명령은 PostgreSQL 데이터베이스에 필요한 테이블과 스키마를 설치합니다.

### 4단계: digna 서버 시작

digna 설치 디렉터리에서 서버를 시작하세요:

```bash
./digna serve --address <host> --port <port>
```

**매개변수:**
- `--address` — 서버 호스트명/IP
- `--port` — 서버 포트

다음과 같은 시작 메시지가 표시되어 서버가 실행 중임을 확인할 수 있습니다:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "팁"

    서버를 처음 시작할 때 macOS가 애플리케이션의 수신 네트워크 연결 허용을 묻는 경우 **허용(Allow)** 을 클릭하세요. 허용하지 않으면 대시보드가 백엔드에 접근할 수 없습니다.

### 5단계: 관리자 사용자 생성

1. **새로운** 터미널 창을 엽니다.
2. digna 설치 디렉터리로 이동합니다.
3. 관리자 사용자를 생성하려면 다음 명령을 실행하세요:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**예시:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

이 명령은 `admin`이라는 사용자 이름과 전체 관리자 권한을 가진 계정을 생성합니다.

!!! tip "팁"

    비밀번호를 작은따옴표로 묶어 사용하세요. `zsh`는 `!`, `$`, `*` 같은 문자를 특별하게 처리하므로 따옴표로 묶지 않으면 의도한 대로 전달되지 않을 수 있습니다.

!!! tip "권장 사항"

    대소문자, 숫자 및 특수 문자를 혼합한 강력한 비밀번호를 사용하세요.

---

## 대시보드 구성 {: #dashboard-configuration }

### 1단계: 대시보드를 웹 서버에 배포

digna 대시보드에는 별도의 `config.toml` 파일이 `dashboard/` 디렉터리에 있습니다. 초기 설정에서는 이 구성 파일이 이미 제공되어 있으며 변경이 필요하지 않습니다. 백엔드 연결을 사용자화해야 하는 경우에만 수정하면 됩니다.

대시보드 구성이 필요하거나(예: 다중 인스턴스 배포) 수정해야 하는 경우에는 대시보드 문서를 참조하세요.

웹 서버를 선택한 다음 해당 배포 단계를 따르세요.

#### nginx에 배포

[nginx 설정](#nginx-setup) 섹션을 따랐다면 서버 블록이 이미 `dashboard` 폴더를 가리키므로 복사할 필요가 없습니다.

1. **경로 확인**
   - `$(brew --prefix)/etc/nginx/servers/digna.conf` 파일을 엽니다.
   - `root`가 압축을 푼 `dashboard` 폴더를 가리키는지 확인합니다.

2. **폴더가 읽기 가능하도록 설정**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **nginx 재로드**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **설치 테스트**
   - 브라우저를 엽니다.
   - `http://localhost:8080`(또는 구성한 URL)로 이동합니다.
   - digna 대시보드 로그인 페이지가 표시되어야 합니다.

#### Apache httpd에 배포

1. **대시보드를 문서 루트로 복사**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **재작성 규칙 추가**

   대시보드 경로가 새로고침 시 유지되도록 배포된 폴더 안에 `.htaccess` 파일을 만듭니다:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   다음 내용을 붙여넣으세요:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Apache 재시작**
   ```bash
   sudo apachectl restart
   ```

4. **대시보드 접속**
   - 브라우저를 엽니다.
   - `http://localhost/digna`로 이동합니다.
   - digna 대시보드 로그인 페이지가 표시되어야 합니다.

---

## digna를 백그라운드 서비스로 실행하기 {: #running-digna-as-a-background-service }

### 왜 digna를 서비스로 실행해야 하나요?

digna 백엔드를 백그라운드 서비스로 실행하면 다음과 같은 이점이 있습니다:

- 머신 부팅 시 자동으로 시작됩니다.
- 열린 터미널 창 없이 백그라운드에서 실행됩니다.
- 충돌 시 자동으로 재시작됩니다.
- macOS의 서비스 관리자 `launchctl`을 통해 관리할 수 있습니다.

### 서비스 관리 파일

필요한 모든 파일은 digna 설치 디렉터리의 `bin/` 아래에 있습니다.

다음 셸 스크립트들이 제공됩니다:

- `install_service.sh` — digna를 launchd에 등록
- `uninstall_service.sh` — 서비스 등록 해제
- `start_service.sh` — 등록된 서비스 시작
- `stop_service.sh` — 실행 중인 서비스 중지

!!! warning "관리자 권한 필요"

    부팅 시 시작되도록 서비스를 등록하려면 `/Library/LaunchDaemons`에 기록해야 하므로 모든 스크립트는 `sudo`로 실행해야 합니다.

### 스크립트에 실행 권한 부여

추출 과정에서 실행 비트가 유지되지 않을 수 있습니다. 처음 사용하기 전에:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### 서비스 설치

1. **터미널을 엽니다.**

2. **bin 폴더로 이동**
   ```bash
   cd /opt/digna/bin
   ```

3. **설치 스크립트 실행**
   ```bash
   sudo ./install_service.sh
   ```

이제 digna 서버가 자동 시작이 활성화된 상태로 launchd에 등록됩니다. 서비스는 즉시 시작되지 않으니, 다음 섹션을 참조하여 시작하세요.

### 서비스 시작 및 중지

#### 서비스를 시작하려면

1. 터미널을 엽니다.
2. `/opt/digna/bin`으로 이동합니다.
3. 다음을 실행하세요:
   ```bash
   sudo ./start_service.sh
   ```

#### 서비스를 중지하려면

1. 터미널을 엽니다.
2. `/opt/digna/bin`으로 이동합니다.
3. 다음을 실행하세요:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "팁"

    애플리케이션 파일을 업데이트하기 전에 항상 서비스를 중지하세요.

### 서비스 확인

서비스가 등록되고 실행 중인지 확인하려면:

```bash
sudo launchctl list | grep digna
```

프로세스 ID로 시작하는 줄이 있으면 서비스가 실행 중입니다. 첫 번째 열에 `-`가 있으면 등록은 되어 있으나 중지된 상태입니다.

### 설치 위치를 변경하는 경우

launchd는 실행 파일의 절대 경로를 저장하므로 설치 위치를 옮기면 서비스를 다시 등록해야 합니다:

1. **현재 서비스 제거**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **애플리케이션 파일 이동**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **서비스 재설치**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **서비스 시작**
   ```bash
   sudo ./start_service.sh
   ```

### 서비스 제거

1. **실행 중인 서비스 중지**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **서비스 등록 해제**
   ```bash
   sudo ./uninstall_service.sh
   ```

이제 digna 서버가 launchd에서 등록 해제되었습니다.

---

## 새 릴리스로 업그레이드하기 {: #upgrading-to-a-new-release }

### 업그레이드 전에

**digna 리포지토리 백업은 필수입니다**

업그레이드하기 전에 데이터 손실을 방지하기 위해 리포지토리(PostgreSQL)를 백업하세요. 백업은 업그레이드 중 문제가 발생할 경우 복구할 수 있게 해줍니다.

터미널에서 백업을 생성하려면:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### 업그레이드 절차

#### 1단계: digna 서비스 중지

digna가 백그라운드 서비스로 실행 중이면 먼저 중지하세요:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

포그라운드에서 실행 중이면 해당 터미널 창에서 `Ctrl + C`를 누르세요.

#### 2단계: 현재 백엔드 설치 백업

digna 설치 디렉터리에서:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### 3단계: 새 버전 압축 해제 및 배포

1. 새 digna 설치 ZIP 파일의 압축을 풉니다.
2. 새 `digna` 실행 파일과 `dashboard` 폴더를 설치 디렉터리에 복사합니다.
3. 실행 비트를 복원하고 필요한 경우 격리 속성을 제거합니다:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "중요"

    `config.toml` 파일은 설치 ZIP에 **절대 포함되지 않습니다**. 기존 구성은 안전하게 유지됩니다.

### 4단계: 구성 파일 복원

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### 5단계: 리포지토리 스키마 업그레이드

digna 설치 디렉터리로 이동하여 다음을 실행하세요:

```bash
cd /opt/digna
./digna repo upgrade
```

이 명령은 기존 데이터를 보존하면서 PostgreSQL 스키마를 최신 버전으로 업데이트합니다.

### 6단계: 서비스 재시작

백그라운드 서비스로 실행 중이었다면:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

수동으로 실행하는 경우 서버를 다시 시작하세요:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

nginx 또는 Apache를 사용하는 경우 해당 웹 서버도 재시작하세요:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### 7단계: 업그레이드 확인

1. digna 대시보드에 접속합니다.
2. 인터페이스가 정상적으로 로드되는지 확인합니다.
3. 서버 로그에서 오류가 있는지 확인합니다.
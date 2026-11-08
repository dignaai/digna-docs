---
title: Linux 설치 가이드 – digna 릴리스 2026.11 | digna 문서
description: Linux에 digna 릴리스 2026.11을 설치하는 단계별 가이드 — 시스템 요구사항, PostgreSQL 설정, nginx 또는 Apache 구성, 백엔드 및 대시보드 구성, digna를 systemd 서비스로 실행하는 방법, 릴리스 2026.06에서 업그레이드하는 방법
keywords: digna 리눅스 설치, digna 배포 가이드, digna 백엔드 설정, digna 대시보드 설치, postgresql 리눅스, nginx 리눅스, digna systemd 서비스, digna 업그레이드 가이드
image: /assets/logo_square.png
---

# digna 릴리스 2026.11용 Linux 설치 가이드

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
9. [digna를 systemd 서비스로 실행하기](#running-digna-as-a-systemd-service)
10. [새 릴리스로 업그레이드하기](#upgrading-to-a-new-release)

---

## 소개 {: #introduction }

### digna 소개

digna는 데이터 웨어하우스, 데이터 레이크, 레이크하우스 등 다양한 데이터 환경 전반에서 데이터 품질 관리를 최적화하도록 설계된 종합적인 AI 기반 플랫폼입니다. 높은 확장성 및 적응성을 갖추었으며 자동화, 실시간 모니터링 및 이상값 탐지를 통해 현대 데이터 과제를 해결합니다.

digna는 두 가지 주요 구성요소로 이루어져 있습니다:

- **digna**: 애플리케이션의 핵심으로, 데이터 처리와 품질 검사 수행을 담당합니다. 백엔드와 명령줄 인터페이스를 단일 실행 파일로 통합하여 이전 릴리스의 별도 프로그램인 `dignabackend`와 `dignacli`를 대체합니다.
- **dignadashboard**: 웹 서버에 호스팅되는 웹 기반 인터페이스로, digna 플랫폼과 상호작용하고 데이터 품질 지표를 시각화하는 사용자 친화적인 방법을 제공합니다.

### 릴리스 2026.11의 새로운 기능

이번 릴리스는 digna Data Reconciliation, digna MCP Server를 포함한 digna Agentic, 그리고 digna Engine을 추가합니다. digna Engine은 digna 내부에서 데이터를 프로파일링하고 서로 다른 데이터베이스 기술 간의 참조 무결성을 검사할 수 있습니다. 자세한 내용은 [릴리스 노트](../../../changelog/Release_202611.md)를 참조하십시오.

설치 측면에서 이번 릴리스는 새로운 저장소 마이그레이션 메커니즘, digna Engine을 위한 `config.toml`의 선택적 `[duckdb]` 섹션, 그리고 새 라이선스 파일을 도입합니다. 각각은 [업그레이드 섹션](#upgrading-to-a-new-release)에서 다룹니다.

### Windows나 macOS용 가이드를 찾고 계신가요?

이 가이드는 Linux를 다룹니다. 다른 플랫폼은 [Windows 설치 가이드](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) 또는 [macOS 설치 가이드](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md)를 참조하십시오.

### 이 가이드는 어떤 배포판을 다루나요?

지침은 가장 일반적인 두 서버 계열을 기준으로 작성되었습니다. 두 계열이 다를 때는 두 가지 명령을 모두 제시합니다:

- **Debian 계열** — Debian, Ubuntu. 패키지 관리자: `apt`.
- **RHEL 계열** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. 패키지 관리자: `dnf`.

`systemd`를 사용하는 현대적인 배포판이면 모두 동작합니다. 변경되는 것은 패키지 이름과 일부 구성 경로뿐입니다.

---

## 시스템 요구사항 {: #system-requirements }

설치를 시작하기 전에 시스템이 다음 최소 요구사항을 충족하는지 확인하십시오:

| 요구사항 | 사양 |
|---|---|
| **운영체제** | Ubuntu 22.04 LTS 이상, Debian 12 이상, RHEL 9 / Rocky 9 / AlmaLinux 9 이상 |
| **아키텍처** | x86_64 (amd64) 또는 arm64 |
| **초기화 시스템** | systemd |
| **메모리 (최소 구성)** | 16 GB RAM |
| **디스크 용량** | 10 GB 사용 가능 저장소 |
| **데이터베이스** | PostgreSQL 서버 12 이상 |
| **웹 서버** | nginx, Apache httpd 또는 동등한 서버 |

!!! info "digna Engine"

    프로파일링 위치로 digna Engine을 사용하는 데이터베이스 연결은 digna 호스트 자체에서 프로파일링됩니다.
    이를 위한 추가 메모리와 디스크 공간을 계획하십시오. 참조:
    [\[duckdb\] 섹션](#duckdb-section).

### 데이터베이스 설치 옵션

**PostgreSQL이 이미 설치된 경우:**
기존 PostgreSQL 서버에 digna용 새 데이터베이스를 추가하면 됩니다.

**digna와 같은 머신에 PostgreSQL을 설치하는 경우:**

!!! info "권장 사양"

    - **메모리**: 32 GB RAM (기본 16 GB 대신)
    - **디스크 공간**: 50 GB 사용 가능 저장소 (기본 10 GB 대신)

    이 더 높은 사양은 digna와 PostgreSQL 데이터베이스가 동시에 실행되는 상황을 수용합니다.

### 배포판 및 아키텍처 확인

이 가이드의 여러 명령은 Debian과 RHEL 계열 간에 다릅니다. 자신의 시스템이 어느 계열인지 확인하려면 다음을 실행하십시오:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` 또는 `ID=debian` — `apt` 명령을 사용하십시오.
- `ID=rhel`, `rocky`, `almalinux` 또는 `fedora` — `dnf` 명령을 사용하십시오.
- `x86_64` 또는 `aarch64` — 설치 패키지에 맞는 아키텍처입니다.

---

## 사전 설치 준비 {: #pre-installation-setup }

digna를 설치하기 전에 두 가지 주요 전제 조건이 준비되어 있는지 확인하십시오:

1. **PostgreSQL 서버** – 계산된 지표와 성능 데이터를 저장하기 위함
2. **웹 서버** – digna Dashboard를 호스팅하기 위함

이 구성 요소들이 아직 설정되지 않았다면 아래 섹션을 따라 설치하고 구성하십시오.

### 패키지 인덱스 갱신

설치하기 전에 패키지 목록을 업데이트하십시오:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "참고"

    이 가이드 전반에서 한 쌍의 첫 번째 명령은 **Debian 계열**용이고 두 번째는 **RHEL 계열**용입니다. 시스템에 맞는 것만 실행하십시오.

---

## PostgreSQL 서버 설정 {: #postgresql-server-setup }

### PostgreSQL이 이미 있는 경우

PostgreSQL이 로컬 머신에 이미 설치되어 실행 중이거나 관리되는 원격 PostgreSQL 서버를 사용 중이라면, [다음 섹션](#web-server-configuration)으로 건너뛸 수 있습니다.

### PostgreSQL 설치

#### 1단계: 서버 패키지 설치

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "팁"

    배포판 패키지는 최신 PostgreSQL 릴리스보다 뒤처질 수 있습니다. 특정 최신 버전이 필요하면 공식 [PostgreSQL apt 또는 yum 저장소](https://www.postgresql.org/download/linux/)를 사용하십시오.

#### 2단계: 데이터베이스 클러스터 초기화

**Debian 계열**에서는 패키지가 자동으로 클러스터를 생성하고 시작합니다 — 다음 단계로 건너뛰십시오.

**RHEL 계열**에서는 클러스터를 명시적으로 생성해야 합니다:

```bash
sudo postgresql-setup --initdb
```

#### 3단계: 서비스 시작 및 활성화

```bash
sudo systemctl enable --now postgresql
```

이 명령은 PostgreSQL을 즉시 시작하고 부팅 시 자동으로 다시 시작되도록 구성합니다.

#### 4단계: 설치 확인

```bash
psql --version
sudo systemctl status postgresql
```

PostgreSQL 버전과 `active (running)` 상태를 확인할 수 있어야 합니다.

#### 5단계: 서버에 접속

Linux PostgreSQL 패키지는 클러스터를 소유한 `postgres` 시스템 계정을 생성합니다. 해당 계정으로 접속하십시오:

```bash
sudo -u postgres psql
```

!!! note "참고 — 여기서 Linux는 Windows와 다릅니다"

    Windows 설치 관리자는 설치 중에 `postgres` 슈퍼유저의 비밀번호 설정을 요청합니다. Linux 패키지는 그렇지 않습니다. 대신 로컬 연결은 **peer authentication**으로 인증됩니다: 운영체제의 `postgres` 사용자가 비밀번호 없이 `postgres` 데이터베이스 사용자로 연결할 수 있습니다.

    그래서 위 명령은 `sudo -u postgres`를 사용합니다. digna 백엔드는 사용자 이름과 비밀번호로 TCP를 통해 연결하므로, [초기 설치](#initial-installation)에서 명시적인 digna 사용자를 생성할 것입니다.

#### 6단계: 포트 확인

기본 PostgreSQL 포트는 `5432`입니다. 서버가 어떤 포트를 리스닝하는지 확인하려면:

```bash
sudo -u postgres psql -c "SHOW port;"
```

값을 기록해 두십시오 — digna 백엔드를 구성할 때 필요합니다.

#### 7단계: digna 사용자를 위한 비밀번호 인증 활성화

digna는 TCP로 `digna_user` 계정으로 PostgreSQL에 연결하므로 peer 인증이 아닌 비밀번호 인증이 필요합니다. `pg_hba.conf`가 이를 허용하는지 확인하십시오.

파일 위치 확인:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

편집기로 열어 로컬 TCP 라인이 `ident` 대신 `scram-sha-256`(또는 오래된 서버에서는 `md5`)을 사용하도록 확인하십시오:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

변경 후 PostgreSQL을 다시 로드하십시오:

```bash
sudo systemctl reload postgresql
```

!!! warning "경고"

    digna가 `FATAL: Ident authentication failed for user "digna_user"`를 보고하면, 이 설정이 원인입니다.

#### 8단계: PostgreSQL이 다른 머신에서 실행되는 경우

다른 호스트의 연결을 허용하려면 `postgresql.conf`에서 `listen_addresses`를 설정하고 `pg_hba.conf`에 해당 네트워크에 맞는 `host` 라인을 추가하십시오:

```
listen_addresses = '*'
```

그런 다음 방화벽에서 포트를 열고 서비스를 재시작하십시오:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## 웹 서버 구성 {: #web-server-configuration }

digna는 대시보드를 호스팅하기 위해 웹 서버가 필요합니다. 다음 옵션 중 하나를 선택하십시오:

- [nginx](#nginx-setup) — 경량이며 권장
- [Apache httpd](#apache-setup) — 널리 배포된 대안

이 서버들 중 하나만 설치하고 구성하면 됩니다.

두 섹션 모두 대시보드가 의존하는 두 가지를 구성합니다:

- **단일 페이지 애플리케이션 폴백** — 대시보드 URL을 새로고침해도 404가 발생하지 않도록 함
- **`.md` MIME 타입** — 마크다운 파일을 올바르게 제공하기 위함

### nginx 설정 {: #nginx-setup }

#### 개요

nginx는 정적 digna 대시보드를 제공하기에 적합한 경량 고성능 웹 서버입니다.

#### 설치

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginx 시작

```bash
sudo systemctl enable --now nginx
```

#### 설치 확인

1. 브라우저를 엽니다.
2. `http://localhost`로 접속합니다.
3. nginx 환영 페이지가 표시되어야 합니다.

#### 방화벽 열기

서버가 다른 머신에서 접근된다면 HTTP 트래픽을 허용하십시오:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### 대시보드용 사이트 구성

nginx는 두 배포판 계열 모두에서 `conf.d` 디렉토리의 모든 파일을 포함합니다. digna 전용 구성 파일을 생성하십시오:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

다음 내용을 붙여넣고 `/opt/digna/dashboard`를 추출한 실제 `dashboard` 폴더 경로로 바꾸십시오:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

    `try_files` 지시어가 없으면 루트 URL이 아닌 다른 대시보드 페이지를 새로고침할 때 404가 발생합니다. 이는 Windows의 IIS에서 필요한 URL Rewrite 모듈에 해당하는 nginx 설정입니다.

#### 기본 사이트 비활성화

포트의 `default_server`가 될 수 있는 서버 블록은 하나뿐입니다. **Debian 계열**에서는 패키지로 제공된 기본 페이지를 제거하여 충돌을 방지하십시오:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

**RHEL 계열**에서는 `/etc/nginx/nginx.conf` 내부의 `server { ... }` 블록을 주석 처리하거나 삭제하십시오.

#### 구성 적용

구문 오류가 있는지 구성 테스트를 실행한 후 nginx를 다시 로드하십시오:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd 설정 {: #apache-setup }

#### 개요

Apache httpd는 지원되는 모든 배포판의 기본 저장소에서 사용할 수 있습니다. 패키지 이름은 Debian 계열에서는 `apache2`이고 RHEL 계열에서는 `httpd`입니다.

#### 설치

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apache 시작

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### 설치 확인

1. 브라우저를 엽니다.
2. `http://localhost`로 접속합니다.
3. 배포판의 기본 Apache 페이지가 표시되어야 합니다.

#### 필수: mod_rewrite 활성화

대시보드는 URL 재작성(rewrite)을 필요로 합니다.

**Debian 계열**에서는 모듈을 활성화하고 재시작하십시오:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

**RHEL 계열**에서는 `mod_rewrite`가 기본으로 로드됩니다. 확인하려면:

```bash
httpd -M | grep rewrite
```

#### 필수: .htaccess 재정의 허용

문서 루트에 대한 구성 파일을 엽니다:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

문서 루트(`/var/www/html` — 두 계열 모두 해당)를 포함하는 `<Directory>` 블록을 찾아 다음을 변경하십시오:

```apache
AllowOverride None
```

다음과 같이 변경:

```apache
AllowOverride All
```

#### 필수: 마크다운 파일용 MIME 타입

같은 파일에 마크다운 파일이 제대로 제공되도록 다음 줄을 추가하십시오:

```apache
AddType text/markdown .md
```

!!! warning "중요"

    이 설정이 없으면 `.md` 파일이 제대로 제공되지 않을 수 있습니다.

#### 구성 적용

구문 오류를 검사한 후 Apache를 재시작하십시오:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## 초기 설치 {: #initial-installation }

### 1단계: digna 저장소 설정

digna 저장소는 digna가 계산한 모든 지표를 저장합니다. 분석 및 성능 데이터의 중앙 데이터베이스 역할을 합니다.

#### 저장소 스키마 및 사용자 생성

PostgreSQL 클라이언트(psql, pgAdmin 등)를 열고 다음 SQL 명령을 실행하십시오:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**다음 플레이스홀더를 교체하십시오:**

- `<digna_repo_schema>` — 원하는 스키마 이름(예: `dignarepo`)
- `<digna_repo_user>` — 원하는 사용자 이름(예: `digna_user`)
- `<digna_repo_password>` — 이 사용자의 안전한 비밀번호

**예시:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

쉘에서 한 번에 실행하려면:

```bash
sudo -u postgres psql
```

그런 다음 `postgres=#` 프롬프트에 위 명령들을 붙여넣고 `\q`로 종료하십시오.

!!! tip "권장 사항"

    데이터베이스 사용자에는 강력하고 복잡한 비밀번호를 사용하십시오. 쉽게 추측할 수 있는 자격증명은 피하십시오.

---

### 2단계: digna 설치 패키지 압축 해제

1. 제공된 digna 설치 ZIP 파일을 찾습니다.
2. 원하는 설치 위치(예: `/opt/digna`)에 압축을 풉니다.
3. 압축을 풀면 다음 항목들이 보여야 합니다:
   - `dashboard/` — 웹 대시보드 인터페이스
   - `digna` — 메인 실행 파일(백엔드 + CLI 결합)

!!! info "구성 파일과 라이선스 파일은 패키지에 포함되어 있지 않습니다"

    `config.toml`과 `dashboard/dashboard_config.toml`은 모두 설치 패키지에 포함되어 있지 않습니다.
    두 파일은 [백엔드 구성](#backend-configuration) 및
    [대시보드 구성](#dashboard-configuration)에서 직접 생성합니다. `license.toml`도 포함되어 있지 않으며,
    3단계에서 설명하는 것처럼 digna가 별도로 제공합니다.

셸에서 압축을 풀려면:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "참고"

    `unzip`이 설치되지 않은 경우 `sudo apt install -y unzip` 또는 `sudo dnf install -y unzip`로 추가하십시오.

#### 실행 파일에 실행 권한 부여

아카이브 전송 방식에 따라 실행 권한 비트가 유지되지 않을 수 있습니다. 명시적으로 설정하십시오:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### 서비스 계정 생성

백엔드를 전용 비권한 사용자로 실행하는 것이 프로덕션 배포에 권장됩니다:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "참고"

    RHEL 계열에서는 동등한 쉘 경로가 `/sbin/nologin`입니다.

### 3단계: 라이선스 파일 설치

!!! warning "중요"

    라이선스 파일은 설치 패키지에 포함되어 있지 않으며 digna에서 별도로 제공됩니다.

1. 제공된 `license.toml` 파일을 찾으십시오.
2. 이를 digna 설치 루트 디렉터리( `config.toml`과 `digna` 실행 파일이 있는 곳)로 복사하십시오.

**이유:**
라이선스 파일에는 고객 정보, 라이선스 만료일 및 디지털 서명이 포함되어 있습니다. **이 파일을 수정하지 마십시오** — 변경하면 무효화됩니다.

**설정 후 디렉터리 구조 예시:**

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
sudo mv config_template.toml config.toml
```

**위치:** `/opt/digna/config.toml`

텍스트 편집기로 `config.toml`을 열고 아래 각 섹션을 구성하십시오.

#### [app] 섹션

이 섹션은 대시보드와 백엔드 간의 교차 출처 리소스 공유(CORS)를 구성합니다:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| 매개변수 | 값 | 메모 |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | 대시보드 URL | 대시보드가 제공되는 URL. 그 밖의 오리진에서 오는 브라우저 요청은 거부됩니다 |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | 필수. 브라우저가 요청마다 세션 쿠키를 함께 보내도록 하는 데 필요합니다 |

!!! note "참고"

    대시보드를 기본 HTTP 포트에서 nginx 또는 Apache로 제공하는 경우 허용할 오리진은 `http://localhost`입니다 — 또는 대시보드에 다른 머신에서 접근하는 경우 서버의 공개 URL을 사용하십시오.

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

| 매개변수 | 값 | 메모 |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` 또는 IP | PostgreSQL 서버 호스트명/IP |
| `DIGNA_REPO_PORT` | `5432` (기본) | PostgreSQL 포트 |
| `DIGNA_REPO_DB` | `postgres` | 데이터베이스 이름 |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | 앞서 생성한 스키마 |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL에서 생성한 사용자 |
| `DIGNA_REPO_PASSWORD` | 비밀번호 | 스키마 생성 시 설정한 비밀번호 |
| `DIGNA_REPO_SSLMODE` | `prefer` (기본) | 선택 사항. PostgreSQL SSL 모드: `disable`, `allow`, `prefer`, `require`, `verify-ca` 또는 `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (기본) | 선택 사항. digna가 리포지터리에 열어 두는 연결 수 |

!!! tip "권장 사항"

    `config.toml`에는 평문으로 데이터베이스 비밀번호가 포함됩니다. 서비스 계정만 읽을 수 있도록 권한을 제한하십시오:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] 섹션

이 섹션에는 보안, 쿠키 및 검사 설정이 포함됩니다:

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

| 매개변수 | 값 | 메모 |
|---|---|---|
| `DIGNA_FERNET_KEY` | 위에 표시된 값 | 이전 릴리스에서 사용하던 암호화 방식의 키. 반드시 있어야 하므로 위에 표시된 값을 그대로 유지하십시오 |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | 대시보드에 접속하는 호스트. `""`로 설정하면 도메인을 지정하지 않으며, 대시보드와 백엔드를 하나의 오리진으로 제공하는 프록시 뒤에서는 이것이 올바른 설정입니다 |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | digna를 HTTPS로 제공하는 경우 반드시 `true`여야 합니다 |
| `DIGNA_COOKIE_HTTPONLY` | `true` | 스크립트가 세션 쿠키에 접근하지 못하도록 합니다 |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24시간) | 세션 만료 시간(초) |
| `DIGNA_MAX_WORKERS` | CPU 코어 수 - 1 | 동시에 실행할 수 있는 검사 수 |
| `DIGNA_FRONTEND_BASEURL` | 대시보드 URL | 필수. 알림 메시지의 링크에 사용되므로 수신자가 열 수 있는 URL이어야 합니다 |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (기본) | 선택 사항. 소스 데이터베이스에 대한 단일 쿼리가 중단되기 전까지 실행될 수 있는 시간(초). `0`이면 타임아웃이 비활성화됩니다 |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (기본) | 선택 사항. 소스 데이터베이스 연결을 기다리는 시간(초). `0`이면 무기한 기다립니다 |

!!! tip "팁"

    서버에서 사용 가능한 CPU 코어 수를 확인하려면 `nproc`를 실행하십시오.

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

| 매개변수 | 값 | 메모 |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` 또는 `DEBUG` | 프로덕션은 `INFO`, 문제 해결 시 `DEBUG`. `TRACE`, `WARN`, `ERROR`도 사용할 수 있습니다 |
| `DIGNA_LOGGING_DIR` | `logs` (기본) | 선택 사항. 순환되는 로그 파일을 저장할 디렉터리(작업 디렉터리 기준 상대 경로) |
| `DIGNA_LOGGING_MAX_FILES` | `30` (기본) | 선택 사항. 보관할 순환 로그 파일 수 |

#### [duckdb] 섹션 (선택 사항) {: #duckdb-section }

릴리스 2026.11의 새 기능입니다. 이 섹션은 **digna Engine**의 리소스를 설정합니다. digna Engine은 프로파일링
위치가 **digna Engine**인 데이터베이스 연결에 대해 digna 내부에서 데이터를 프로파일링하고, 서로 다른 데이터베이스
연결에 있는 데이터 소스 간의 참조 무결성 검사를 실행합니다. 참조:
[프로파일링 위치](../../../platform/profiling/profiling_location.md).

이 섹션은 선택 사항입니다. 이 섹션이 없으면 아래의 기본값이 적용됩니다.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| 매개변수 | 값 | 메모 |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (기본) | digna Engine 실행 한 번이 사용할 수 있는 메모리(MB). 최대 `DIGNA_MAX_WORKERS`개의 실행이 동시에 활성화될 수 있습니다 |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | 기본값: 시스템 임시 디렉터리(`$TMPDIR`, 설정되지 않은 경우 `/tmp`) | 데이터가 메모리에 들어가지 않을 때 임시 파일을 저장할 디렉터리 |

!!! tip "digna Engine 용량 산정"

    digna 자체가 사용하는 메모리 외에, digna 호스트에 최대 `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB`의
    메모리를 추가로 계획하십시오. 또한 임시 디렉터리에는 digna Engine을 사용하는 데이터 소스 중 가장 큰 검사 날짜의
    데이터를 담을 수 있을 만큼의 여유 디스크 공간이 필요합니다. `DIGNA_DUCKDB_TEMP_DIRECTORY`가 그만한 공간이 있고
    digna를 실행하는 계정이 쓸 수 있는 디스크를 가리키도록 설정하십시오:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
    ```

    이 섹션은 하나 이상의 데이터베이스 연결이 digna Engine을 사용하거나, 참조 무결성 검사가 서로 다른 연결에 있는
    데이터 소스를 비교하는 경우에만 필요합니다.

---

### 2단계: 구성 검증

리포지터리를 초기화하기 전에 `config.toml`이 완전하고 올바르게 구성되었는지 확인하십시오. digna 설치 디렉터리에서 다음을 실행합니다:

```bash
./digna config check
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

### 3단계: 저장소 초기화

1. 터미널을 엽니다.
2. digna 설치 디렉터리( `config.toml` 및 `digna` 실행 파일이 있는 곳)로 이동합니다.
3. 연결 테스트를 실행하십시오:

```bash
cd /opt/digna
./digna repo check
```

새 스키마에서는 명령이 연결한 다음, 아직 저장소가 설치되지 않았다고 보고합니다:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

이 시점에서는 이것이 예상된 결과이며, digna가 PostgreSQL과 스키마에 도달할 수 있음을 확인해 줍니다. 대신 연결 오류나 인증 오류가 나타나면 `[repo]` 섹션 또는 PostgreSQL 설정을 확인하십시오.

!!! note "참고"

    Linux에서는 현재 디렉터리가 PATH에 포함되어 있지 않으므로 실행 파일을 `./digna`로 호출합니다. 항상 짧은 명령어로 사용하려면 심볼릭 링크를 추가하십시오:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### 4단계: 저장소 스키마 설치

같은 디렉터리에서 다음을 실행하십시오:

```bash
./digna repo upgrade
```

이 명령은 저장소 스키마에 필요한 테이블을 설치하고 다음 메시지로 완료됩니다:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade는 설치와 업그레이드를 모두 수행합니다"

    릴리스 2026.11부터 `repo upgrade`는 새 저장소를 설치하고 기존 저장소를 업그레이드합니다.
    `repo install`도 같은 명령의 다른 이름으로 계속 사용할 수 있습니다.

### 5단계: 관리자 사용자 생성

관리자 사용자는 저장소 스키마에 직접 생성되므로 아직 서버를 실행할 필요가 없습니다. digna 설치 디렉터리에서 다음을 실행하십시오:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**예시:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

이렇게 하면 이메일 주소가 `admin@example.com`이고 전체 관리자 권한을 가진 사용자가 생성됩니다.

!!! tip "팁"

    비밀번호는 작은따옴표로 감싸십시오. `bash`와 `zsh`는 `!`, `$`, `*` 같은 문자를 특별하게 취급하므로 인용하지 않으면 원래 문자열대로 전달되지 않습니다.

!!! tip "권장 사항"

    대문자, 소문자, 숫자 및 특수 문자를 섞어 강력한 비밀번호를 사용하십시오.

### 6단계: digna 서버 시작

digna 설치 디렉터리에서 서버를 시작합니다:

```bash
./digna serve --address <host> --port <port>
```

**매개변수:**
- `--address` — 서버 호스트명/IP (기본값 `127.0.0.1`)
- `--port` — 서버 포트 (기본값 `8000`)

서버가 시작되면 수신 대기 중인 주소를 출력합니다:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "팁"

    대시보드가 백엔드와 다른 머신에서 제공되는 경우 API 포트도 방화벽에서 열어야 합니다:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "서버가 터미널을 점유합니다"

    `serve`는 포그라운드에서 실행되며 ++ctrl+c++로 중지할 때까지 계속 동작합니다. 설정을 마칠 때까지 실행 상태로 두십시오. 대신 부팅 시 자동으로 시작하려면 다음을 참조하십시오: [digna를 systemd 서비스로 실행](#running-digna-as-a-systemd-service).

---

## 대시보드 구성 {: #dashboard-configuration }

### 1단계: 대시보드를 웹 서버에 배포

digna 대시보드는 자체 구성을 `dashboard/dashboard_config.toml`에서 읽습니다. 이 파일은 설치 패키지에 포함되어 있지 않으므로, 대시보드 파일과 함께 `dashboard/` 디렉터리에 직접 생성해야 합니다.

파일의 내용은 [Single Sign-On](../../../sso/overview.md)에서 설명하며, 이 파일이 필요한 곳도 바로 그곳입니다. 이 파일에는 대시보드가 제공하는 로그인 옵션과, 다중 인스턴스 배포의 경우 백엔드 연결 정보가 담깁니다.

웹 서버를 선택하고 해당 배포 단계를 따르십시오.

#### nginx에 배포

[nginx 설정](#nginx-setup)을 따른 경우 서버 블록이 이미 `dashboard` 폴더를 가리키므로 복사가 필요 없습니다.

1. **경로 확인**
   - `/etc/nginx/conf.d/digna.conf`를 엽니다.
   - `root`가 추출된 `dashboard` 폴더를 가리키는지 확인합니다.

2. **폴더가 읽기 가능하도록 설정**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **nginx 다시 로드**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **설치 테스트**
   - 브라우저를 엽니다.
   - `http://localhost`(또는 구성한 URL)로 이동합니다.
   - digna 대시보드 로그인 페이지가 표시되어야 합니다.

#### Apache httpd에 배포

1. **대시보드를 문서 루트로 복사**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **리라이트 규칙 추가**

   대시보드 경로가 브라우저 새로고침 시 유지되도록 배포된 폴더 안에 `.htaccess` 파일을 생성합니다:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   다음을 붙여넣으십시오:

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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **대시보드 접속**
   - 브라우저를 엽니다.
   - `http://localhost/digna`로 이동합니다.
   - digna 대시보드 로그인 페이지가 표시되어야 합니다.

### 2단계: SELinux (RHEL 계열 전용)

RHEL, Rocky, AlmaLinux 및 Fedora에서는 기본적으로 SELinux가 활성화되어 웹 서버가 예상 위치 외부의 파일을 읽지 못하도록 차단할 수 있습니다. SELinux가 활성화되어 있는지 확인하십시오:

```bash
getenforce
```

결과가 `Enforcing`이고 `/opt/digna/dashboard`에서 대시보드를 제공하는 경우, 웹 서버가 해당 디렉터리를 읽을 수 있도록 라벨을 지정하십시오:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "참고"

    `semanage`가 없다면 `sudo dnf install -y policycoreutils-python-utils`로 설치하십시오.

!!! warning "중요"

    새로 구성된 RHEL 서버에서 대시보드가 **403 Forbidden**을 반환하는 경우, 파일 권한 문제보다는 거의 항상 SELinux 라벨링 문제입니다. `sudo ausearch -m avc -ts recent`로 확인하십시오.

---

## digna를 systemd 서비스로 실행하기 {: #running-digna-as-a-systemd-service }

### 왜 digna를 서비스로 실행해야 하나요?

digna 백엔드를 systemd 서비스로 실행하면 다음과 같은 장점이 있습니다:

- 머신 부팅 시 자동으로 시작됩니다.
- 열린 터미널 창 없이 백그라운드에서 실행됩니다.
- 충돌 시 자동으로 재시작됩니다.
- 표준 Linux 서비스 관리자 `systemctl`로 관리할 수 있습니다.

### 서비스 관리 파일

필요한 모든 파일은 digna 설치 디렉터리의 `bin/` 아래에 있습니다.

사용 가능한 셸 스크립트는 다음과 같습니다:

- `install_service.sh` — digna를 systemd에 등록합니다.
- `uninstall_service.sh` — 서비스를 등록 취소합니다.
- `start_service.sh` — 등록된 서비스를 시작합니다.
- `stop_service.sh` — 실행 중인 서비스를 중지합니다.

!!! warning "관리자 권한 필요"

    모든 스크립트는 부팅 시 시작하도록 단위 파일을 `/etc/systemd/system`에 작성하므로 `sudo`로 실행해야 합니다.

### 스크립트에 실행 권한 부여

압축 해제 시 실행 권한이 보존되지 않을 수 있습니다. 처음 사용 전에 다음을 실행하십시오:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
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

이제 digna 서버가 systemd에 자동 시작으로 등록됩니다. 서비스는 즉시 시작되지 않습니다 — 다음 섹션을 참조하여 시작하십시오.

### 서비스 시작 및 중지

#### 서비스를 시작하려면

1. 터미널을 엽니다.
2. `/opt/digna/bin`로 이동합니다.
3. 다음을 실행합니다:
   ```bash
   sudo ./start_service.sh
   ```

#### 서비스를 중지하려면

1. 터미널을 엽니다.
2. `/opt/digna/bin`로 이동합니다.
3. 다음을 실행합니다:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "팁"

    애플리케이션 파일을 업데이트하기 전에 항상 서비스를 중지하십시오.

### systemctl로 서비스 관리

등록된 후에는 어느 디렉터리에서나 표준 systemd 명령으로 서비스를 제어할 수 있습니다:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### 서비스 확인

서비스가 등록되어 실행 중인지 확인하려면:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled`이면 부팅 시 시작되며; `active`이면 현재 실행 중임을 의미합니다.

### 서비스 로그 보기

systemd는 백엔드가 콘솔에 출력하는 모든 내용을 캡처합니다. 로그를 확인하려면:

```bash
sudo journalctl -u digna -n 100
```

문제를 재현하면서 실시간으로 로그를 따라가려면:

```bash
sudo journalctl -u digna -f
```

!!! tip "팁"

    서비스가 즉시 시작 후 중지되는 경우 진단하는 가장 빠른 방법입니다. 저장소 연결 실패나 누락된 `license.toml`은 여기에서 보고됩니다.

### 서비스를 새 디렉터리로 이동

유닛 파일은 실행 파일의 절대 경로를 저장하므로 설치를 이동하면 서비스를 재등록해야 합니다:

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

이제 digna 서버가 systemd에서 등록 해제됩니다.

---

## 새 릴리스로 업그레이드하기 {: #upgrading-to-a-new-release }

이 섹션에서는 릴리스 2026.06 설치를 릴리스 2026.11로 업그레이드합니다.

!!! warning "2026.06 이전 릴리스에서 업그레이드"

    먼저 릴리스 2026.06의 업그레이드 단계를 수행하십시오: [새 릴리스로 업그레이드하기](../Release%202026.06/installation_guide_digna_linux_2026_06.md#upgrading-to-a-new-release). 그런 다음 아래 단계를 계속 진행하십시오.

### 업그레이드 전에

**digna 저장소 백업 생성은 필수입니다**

digna를 업그레이드하기 전에 저장소(PostgreSQL)를 백업하여 데이터 손실에 대비하십시오.
백업이 있으면 업그레이드 중 예기치 않은 문제가 발생해도 복구할 수 있습니다.

쉘에서 백업을 생성하려면:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**릴리스 2026.11용 라이선스 파일 요청**

릴리스 2026.11에는 새 `license.toml`이 필요합니다. 시작하기 전에 digna 팀에 요청하고,
[7단계](#step-7-replace-the-license-file)에서 사용할 수 있도록 준비해 두십시오.

### 업그레이드 절차

#### 1단계: digna 서비스 중지 {: #step-1-stop-the-digna-service }

digna가 systemd 서비스로 실행 중이면 먼저 중지하십시오:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

digna가 포그라운드에서 실행 중이면 해당 터미널 창에서 ++ctrl+c++를 누르십시오.

#### 2단계: 현재 설치 백업 {: #step-2-backup-current-installation }

digna 설치 디렉터리에서 현재 설치의 실행 파일과 대시보드 폴더 이름을 변경하여, 새 릴리스를 나란히 배포할 수
있도록 하십시오:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

`digna_old`는 업그레이드를 확인할 때까지, `dashboard_old`는 거기에서 구성 파일을 복원할 때까지 보관하십시오
(4단계 참조). 그 후에는 둘 다 삭제해도 됩니다.

#### 3단계: 새 버전 압축 해제 및 배포 {: #step-3-extract-and-deploy-new-version }

1. 새 digna 설치 ZIP 파일을 압축 해제합니다.
2. 새 `digna` 실행 파일과 `dashboard` 폴더를 설치 디렉터리에 복사합니다.
3. 실행 권한 비트와 서비스 계정 소유권을 복원합니다:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "중요"

    `config.toml`과 `dashboard/dashboard_config.toml`은 모두 설치 ZIP에 절대 포함되지 않습니다.
    digna 팀은 두 파일 중 어느 것도 제공하지 않습니다. 따라서 기존 구성은 업그레이드의 영향을 받지 않으며,
    이름이 변경된 `*_old` 폴더에 있는 사본이 유일한 사본입니다.

#### 4단계: 구성 파일 복원 {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
./digna config check
```

모든 섹션이 OK로 보고되어야 합니다. FAILED로 보고된 항목을 모두 수정하고 **Unknown keys** 아래에 나열된 키를
제거한 다음, 계속하기 전에 명령을 다시 실행하십시오.

#### 7단계: 라이선스 파일 교체 {: #step-7-replace-the-license-file }

이전 릴리스용으로 발급된 라이선스 파일은 릴리스 2026.11에서 작동하지 않습니다. digna 팀이 릴리스 2026.11용으로
제공한 `license.toml`을 설치 디렉터리에 복사하여 기존 파일을 교체하십시오:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "이전 라이선스를 유지하지 마십시오"

    이전 라이선스로는 라이선스를 확인하는 모든 명령(`serve`, `user`, `inspection`, `repo`)이 실패하므로
    digna가 시작되지 않고 리포지터리도 업그레이드할 수 없습니다. 다음 단계로 넘어가기 전에 새 라이선스를 확인하십시오:

    ```bash
    ./digna license check
    ```

#### 8단계: 저장소 스키마 업그레이드 {: #step-8-upgrade-the-repository-schema }

digna 설치 디렉터리에서 다음을 실행하십시오:

```bash
cd /opt/digna
./digna repo upgrade
```

릴리스 2026.11은 버전이 지정된 마이그레이션으로 저장소 스키마를 관리합니다. 이전 릴리스에서 처음 업그레이드할 때는
스키마를 이전 방식의 마지막 버전으로 올리고, 이를 시작점으로 기록한 다음, 릴리스 2026.11의 마이그레이션을
적용합니다. 다음 메시지로 완료됩니다:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

기존 데이터는 모두 보존됩니다. 언제든지 `./digna repo check`를 실행하면 저장소 상태를 확인할 수 있으며,
마지막으로 적용된 마이그레이션과 대기 중인 마이그레이션이 나열됩니다.

!!! warning "저장소가 최신이 아니면 digna가 시작되지 않습니다"

    릴리스 2026.11부터는 저장소 업그레이드가 필요한 동안 서버가 시작을 거부하고 그 사실을 알려 줍니다. 예:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    서버나 서비스를 시작하기 전에 `repo upgrade`를 실행하십시오.

#### 9단계: 서비스 재시작 {: #step-9-restart-services }

systemd 서비스로 실행 중인 경우:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

수동으로 실행 중인 경우 서버를 재시작하십시오:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

nginx 또는 Apache를 사용하는 경우 해당 웹 서버를 다시 로드하십시오:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

RHEL 계열에서 `dashboard` 디렉터리를 교체했다면 SELinux 레이블을 다시 적용하십시오:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### 10단계: 업그레이드 확인 {: #step-10-verify-the-upgrade }

1. 새 실행 파일의 릴리스를 확인합니다:

    ```bash
    ./digna version
    ```

    첫 번째 줄이 `Release: 2026.11`이어야 합니다.

2. digna 대시보드에 접속하여 인터페이스가 올바르게 로드되는지 확인합니다.
3. 서버 로그에 오류가 있는지 확인합니다:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. 데이터베이스 연결을 테스트합니다. 참조:
   [연결 테스트](../../../databases/overview.md#testing-a-connection).

새 모듈을 시작하려면 [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
digna MCP Server에 대해서는 [AI 에이전트 연결](../../../platform/agentic/connect_ai_agent.md),
digna Engine에 대해서는 [프로파일링 위치](../../../platform/profiling/profiling_location.md)를 참조하십시오.

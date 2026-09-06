# Single Sign-On Overview

---

## Table of Contents

1. [Introduction and Overview](#introduction-and-overview)
2. [Provider Guides](#provider-guides)
3. [Configuration Steps](#configuration-steps)
4. [Dashboard Configuration](#dashboard-configuration)
5. [Backend Configuration](#backend-configuration)
6. [Testing Login](#testing-login)
7. [Troubleshooting](#troubleshooting)
8. [Supported Providers](#supported-providers)

---

## 소개 및 개요 {: #introduction-and-overview }

이 가이드는 **OpenID Connect (OIDC)**를 사용하여 digna 플랫폼과 Single Sign-On(SSO)을 통합하는 단계별 지침을 제공합니다.

### SSO란?

Single Sign-On은 사용자가 외부 아이덴티티 제공자를 통해 기업 자격증명으로 digna에 안전하게 로그인할 수 있도록 합니다. 사용자는 별도의 digna 비밀번호를 관리하는 대신 사내 자격증명으로 인증할 수 있습니다.

### 동작 원리

digna의 SSO는 OIDC 프로토콜로 구현됩니다. 여러 아이덴티티 제공자를 병렬로 구성할 수 있으며, 이를 위해 두 가지 주요 구성 파일을 조정합니다:

- **`dashboard_config.toml`** — 프런트엔드 로그인 인터페이스 제어
- **`config.toml`** — 백엔드 OIDC 연결 구성

### 지원되는 제공자 {: #supported-providers-overview }

이 가이드의 예시는 **Microsoft**와 **Google**을 사용하지만, **OIDC를 준수하는 모든 제공자**는 동일한 구조로 통합할 수 있습니다.

---

## 제공자 가이드 {: #provider-guides }

모든 제공자는 동일한 네 가지 값(클라이언트 ID, 클라이언트 시크릿, 리디렉션 URI, 디스커버리 URL)을 필요로 하지만, 각 제공자는 관리자 콘솔에서 이를 배치하는 위치가 다르며 몇몇은 다른 제공자와 다른 고유한 단계를 요구합니다. 아래 가이드는 그 절반(제공자 측 설정)을 다루고; 이 페이지는 digna 측 설정을 다룹니다(모두 동일).

| Provider | Guide | Worth knowing |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | 자체 호스팅; 토큰 서비스를 직접 제어하는 유일한 제공자 |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | 디스커버리 URL이 테넌트별이며, 커스텀 도메인은 URL을 변경함 |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | 동의 화면은 비-테스트 사용자가 로그인하기 전에 게시되어야 함 |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | 자체 호스팅; 디스커버리 URL이 realm(영역)별 |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | 테넌트 ID가 디스커버리 URL에 나타나며, 시크릿은 만료됨 |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | 인증 서버 선택이 디스커버리 URL을 변경함 |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | OIDC 앱 유형은 생성 시 선택해야 하며 변경 불가 |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | 환경 ID가 디스커버리 URL에 나타남 |

다른 모든 OIDC 준수 제공자는 동일하게 작동합니다 — [Other OIDC Providers](#supported-providers)를 참조하세요.

---

## 구성 단계 {: #configuration-steps }

SSO 구성에는 두 파일의 업데이트가 필요합니다. 이 섹션은 각 파일을 구성하는 방법을 설명합니다.

### 구성 파일 개요

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | 프런트엔드 로그인 인터페이스 |
| **config.toml** | `/config.toml` | 백엔드 OIDC 연결 |

두 파일 모두 SSO가 제대로 작동하려면 구성되어야 합니다.

---

## 대시보드 구성 {: #dashboard-configuration }

### 파일 위치

```
dashboard/dashboard_config.toml
```

### 단계 1: OIDC 제공자 추가

지원하려는 각 아이덴티티 제공자에 대해 `[[login.oidc]]` 배열 아래에 항목을 추가합니다.

**Microsoft와 Google 예시:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### 단계 2: 로그인 옵션 구성

비밀번호 기반 로그인을 허용할지 지정합니다:

```toml
[login]
usePassword = true
```

### 구성 매개변수

#### `[[login.oidc]]` 섹션

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | OIDC 연결의 고유 식별자 (config.toml의 key와 일치해야 함) |
| `label` | string | Yes | 로그인 버튼에 표시되는 텍스트 (예: "Login with Microsoft") |

#### `[login]` 섹션

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | SSO 외에 비밀번호 기반 로그인을 허용할지 여부 |

### usePassword 이해하기

**`usePassword = true`인 경우:**
- 로그인 화면에 SSO 버튼(예: "Login with Microsoft")이 표시됩니다
- 로그인 화면에 사용자 이름 및 비밀번호 필드도 표시됩니다
- 사용자는 둘 중 한 방법으로 인증할 수 있습니다
- 일부 사용자는 SSO를 사용하고 일부는 비밀번호를 사용하는 하이브리드 설정을 허용합니다

**`usePassword = false`(또는 생략)인 경우:**
- 로그인 화면에는 SSO 버튼만 표시됩니다
- 사용자 이름/비밀번호 필드는 없습니다
- OIDC 인증만 사용 가능합니다

!!! tip "팁"

    Password 기반 로그인은 `digna user add` 명령으로 비밀번호가 설정된 사용자 또는 대시보드를 통해 생성된 사용자에게만 제공됩니다.

### 전체 예시

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## 백엔드 구성 {: #backend-configuration }

### 파일 위치

```
/config.toml
```

(루트 digna 설치 디렉터리)

### 단계 1: OIDC 제공자 섹션 추가

각 제공자는 전용 `[oidc.<key>]` 섹션을 가져야 합니다. key는 `dashboard_config.toml`에 정의된 `key`와 일치해야 합니다.

### Microsoft 구성

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google 구성

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### 구성 매개변수

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | 아이덴티티 제공자에서 발급한 클라이언트 ID | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | 아이덴티티 제공자에서 발급한 클라이언트 시크릿 | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | 인증 후 콜백 URL | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC 구성 엔드포인트 | `https://login.microsoftonline.com/...` |

!!! warning "중요"

    플레이스홀더 값(`<client_id>`, `<client_secret>`, `<tenant_id>`)을 아이덴티티 제공자 개발자 포털의 실제 자격증명으로 교체하세요.

### 리디렉션 URI

리디렉션 URI는 아이덴티티 제공자 구성에 등록된 값과 동일해야 합니다:

```
http://localhost:5173/oidc/callback
```

digna가 다른 도메인에서 호스팅되는 경우 적절히 업데이트하세요:
- 로컬: `http://localhost:5173/oidc/callback`
- 운영 환경: `https://digna.yourdomain.com/oidc/callback`

### 전체 예시

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## 로그인 테스트 {: #testing-login }

구성을 완료한 후 SSO가 정상 작동하는지 확인합니다.

### 테스트 전 체크리스트

테스트 전에 다음을 확인하세요:

- [ ] `dashboard_config.toml`에 OIDC 제공자가 업데이트되었는가
- [ ] `config.toml`에 OIDC 자격증명이 업데이트되었는가
- [ ] 두 파일이 저장되었는가
- [ ] 자격증명이 올바른가 (클라이언트 ID, 클라이언트 시크릿)
- [ ] 리디렉션 URI가 배포 URL과 일치하는가
- [ ] 아이덴티티 제공자 애플리케이션에 리디렉션 URI가 구성되어 있는가

### 테스트 단계

#### 단계 1: 서비스 재시작

변경사항을 적용하려면 digna 백엔드 및 웹 서버를 재시작합니다.

**Windows에서 서비스로 실행 중인 경우:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Linux 또는 macOS에서 서비스로 실행 중인 경우:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**수동으로 실행 중인 경우:**
```bash
digna serve --address localhost --port 8082
```

**웹 서버도 재시작하세요** — Windows의 경우 IIS 또는 Tomcat, Linux/macOS의 경우 nginx 또는 Apache 등.

#### 단계 2: 대시보드 열기

브라우저에서 digna 대시보드를 엽니다:

```
http://localhost:5173
```

(또는 구성한 대시보드 URL)

#### 단계 3: 로그인 버튼 확인

구성된 각 제공자에 대한 로그인 버튼이 표시되는지 확인합니다:

- "Login with Microsoft" 버튼이 보여야 함
- "Login with Google" 버튼이 보여야 함
- (usePassword = true인 경우) 사용자 이름/비밀번호 필드가 보여야 함

버튼이 나타나지 않으면:
- `dashboard_config.toml`이 저장되었는지 확인
- 대시보드 서비스가 재시작되었는지 확인
- 브라우저 콘솔(F12)에서 오류 확인

#### 단계 4: SSO 로그인 테스트

SSO 버튼(예: "Login with Microsoft")을 클릭합니다:

1. 아이덴티티 제공자의 로그인 화면으로 리디렉션되어야 합니다
2. 사내 자격증명으로 로그인합니다
3. digna로 리디렉션되어야 합니다
4. digna에 로그인되어 있어야 합니다

#### 단계 5: 사용자 생성 확인

SSO 로그인 성공 후:

- 사용자가 digna에 자동으로 생성되어야 합니다
- 사용자가 로그인되어야 합니다
- 사용자 프로필에 아이덴티티 제공자 관련 정보가 표시되어야 합니다
- digna 대시보드를 볼 수 있어야 합니다

#### 단계 6: 비밀번호 로그인 테스트 (활성화된 경우)

`usePassword = true`인 경우:

1. digna에서 로그아웃합니다
2. 로그인 페이지에서 사용자 이름과 비밀번호를 입력합니다
3. 비밀번호 자격증명으로 로그인할 수 있어야 합니다

---

## 문제 해결 {: #troubleshooting }

### 로그인 버튼이 표시되지 않음

**증상:**
- 로그인 페이지에 OIDC 로그인 버튼이 보이지 않음
- (usePassword = true인 경우) 비밀번호 필드만 보임

**원인 및 해결책:**
1. `dashboard_config.toml`이 `dashboard/` 디렉터리에 있는지 확인
2. `[[login.oidc]]` 섹션이 올바른 문법으로 존재하는지 검증
3. 대시보드 서비스를 재시작
4. 브라우저 캐시 삭제 (Ctrl+Shift+Delete 또는 Cmd+Shift+Delete)
5. 브라우저 콘솔(F12 → Console 탭)에서 오류 확인

---

### 리디렉션 URI 불일치 오류

**증상:**
- SSO 버튼 클릭 후 "redirect_uri mismatch" 관련 오류 발생
- "The redirect URI is not registered" 오류

**원인 및 해결책:**
1. `config.toml`의 `DIGNA_OIDC_REDIRECT_URI`가 올바른지 확인
2. 아이덴티티 제공자 설정에 리디렉션 URI가 등록되어 있는지 확인
3. 프로토콜, 도메인, 경로까지 정확히 동일한지 확인
4. 리디렉션 URI에 오타가 없는지 확인
5. HTTPS 사용 시 인증서가 유효한지 확인

---

### 잘못된 클라이언트 자격증명 오류

**증상:**
- "Invalid client ID or secret" 오류
- 자격증명 오류로 인증 실패

**원인 및 해결책:**
1. `DIGNA_OIDC_CLIENT_ID` 및 `DIGNA_OIDC_CLIENT_SECRET`이 올바른지 확인
2. 앞뒤 공백이나 특수문자가 포함되어 있지 않은지 확인
3. 자격증명이 만료되었거나 취소되지 않았는지 확인
4. 구성 업데이트 후 백엔드 서비스를 재시작
5. 아이덴티티 제공자 콘솔에서 자격증명이 활성 상태인지 확인

---

### 로그인 중 멈춤 또는 시간 초과

**증상:**
- SSO 버튼 클릭 시 아무 동작이 없음
- 몇 초 후 타임아웃
- 브라우저에서 "Failed to connect" 등의 표시

**원인 및 해결책:**
1. digna 백엔드가 실행 중인지 확인: `digna repo check`
2. 아이덴티티 제공자로의 네트워크 연결 상태 확인
3. `DIGNA_OIDC_CONFIGURATION_URL`에 접근 가능한지 확인
4. 방화벽 규칙이 아웃바운드 HTTPS 연결을 허용하는지 확인
5. 백엔드와 대시보드가 서로 통신 가능한지 확인

---

### 사용자가 자동으로 생성되지 않음

**증상:**
- SSO 로그인은 성공하지만 digna에 사용자가 생성되지 않음
- SSO 로그인 후 권한 오류 발생

**원인 및 해결책:**
1. OIDC 구성이 올바른지 확인
2. 사용자 권한이 적절히 설정되어 있는지 확인
3. digna 로그에서 오류 메시지 검토
4. 백엔드 서비스 재시작
5. 문제가 지속되면 support@digna.ai로 문의

---

## 지원되는 제공자 {: #supported-providers }

### 테스트 및 지원됨

다음 OIDC 제공자는 테스트되어 작동이 확인된 목록입니다:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### 기타 OIDC 제공자

OpenID Connect를 지원하는 모든 제공자는 통합할 수 있습니다. 필요한 정보:

- 클라이언트 ID
- 클라이언트 시크릿
- OpenID 구성 URL (일반적으로 `/.well-known/openid-configuration`)
- 지원되는 스코프(일반적으로 `openid profile email`)

특정 제공자 통합에 도움이 필요하면 support@digna.ai로 문의하세요.

---

## 모범 사례

**해야 할 것(DO):**
- 운영 환경에서는 HTTPS 사용 (HTTP 사용 금지)
- 클라이언트 시크릿을 안전하게 저장 (가능하면 환경 변수 사용)
- 시크릿 주기적 회전
- 먼저 비운영 환경에서 테스트
- 구성된 제공자 문서화
- 이상 활동을 모니터링하기 위해 로그인 로그 확인
- 아이덴티티 제공자 구성과 digna 구성을 동기화 상태로 유지

**하지 말아야 할 것(DON'T):**
- 클라이언트 시크릿을 버전 관리에 저장하지 말 것
- 운영 환경에서 HTTP 리디렉션 URI 사용하지 말 것
- 동일한 키로 여러 제공자를 구성하지 말 것
- 운영 환경에 기본/테스트 자격증명을 남기지 말 것
- 시크릿이 포함된 구성 파일을 공개하지 말 것
- 개발 및 운영 자격증명을 혼용하지 말 것

---

## 지원

SSO 구성에 도움이 필요하신가요?

- **이메일:** support@digna.ai
- **문서:** https://docs.digna.ai
- **웹사이트:** https://www.digna.ai

---

**최종 업데이트:** 2026년 8월 30일  
**릴리스:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
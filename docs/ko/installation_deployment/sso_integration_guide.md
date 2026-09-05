---
title: Single Sign-On (SSO) 통합 가이드 | digna Documentation
description: OpenID Connect (OIDC)를 사용하여 digna에 Single Sign-On (SSO)을 구성하는 단계별 가이드입니다. 대시보드 및 백엔드 구성, 테스트, 문제 해결 및 Microsoft Entra ID, Google Workspace, Okta를 포함한 지원되는 IdP를 다룹니다.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc integration
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integration
  - enterprise authentication
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) 통합 가이드
og_description: OpenID Connect를 사용하여 digna에 Single Sign-On을 구성하세요. Microsoft Entra ID, Google Workspace, Okta 및 기타 OIDC 호환 IdP의 단계별 설정을 제공합니다.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On Integration Guide

---

## 목차

1. [소개 및 개요](#introduction-and-overview)
2. [구성 단계](#configuration-steps)
3. [대시보드 구성](#dashboard-configuration)
4. [백엔드 구성](#backend-configuration)
5. [로그인 테스트](#testing-login)
6. [문제 해결](#troubleshooting)
7. [지원되는 공급자](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

이 가이드는 **OpenID Connect (OIDC)**를 사용하여 digna 플랫폼에 Single Sign-On(SSO)을 통합하는 단계별 지침을 제공합니다.

### SSO란?

Single Sign-On은 외부 아이덴티티 제공자(IdP)를 통해 기업 자격증명으로 digna에 안전하게 로그인할 수 있게 합니다. 사용자는 별도의 digna 비밀번호를 관리하지 않고도 기업 자격증명으로 인증할 수 있습니다.

### 작동 방식

digna의 SSO는 OIDC 프로토콜을 사용해 구현됩니다. 여러 아이덴티티 제공자를 병렬로 구성하려면 두 가지 핵심 구성 파일을 조정하면 됩니다:

- **`dashboard_config.toml`** — 프런트엔드 로그인 인터페이스 제어
- **`config.toml`** — 백엔드 OIDC 연결 구성

### 지원되는 공급자 {: #supported-providers-overview }

이 가이드의 예시는 **Microsoft**와 **Google**을 사용하지만, **OIDC 규격을 준수하는 모든 공급자**는 동일한 구조를 따라 통합할 수 있습니다.

일반적인 OIDC 공급자 예:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- 기타 OIDC 준수 아이덴티티 제공자

---

## Configuration Steps {: #configuration-steps }

SSO 구성은 두 파일의 업데이트를 필요로 합니다. 이 섹션에서는 각 파일을 구성하는 방법을 설명합니다.

### 구성 파일 개요

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | 프런트엔드 로그인 인터페이스 |
| **config.toml** | `/config.toml` | 백엔드 OIDC 연결 |

SSO가 제대로 작동하려면 두 파일 모두 구성되어야 합니다.

---

## Dashboard Configuration {: #dashboard-configuration }

### 파일 위치

```
dashboard/dashboard_config.toml
```

### 1단계: OIDC 공급자 추가

지원하려는 각 아이덴티티 제공자에 대해 `[[login.oidc]]` 배열 아래에 항목을 추가합니다.

**Microsoft 및 Google 예시:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### 2단계: 로그인 옵션 구성

비밀번호 기반 로그인을 허용할지 여부를 지정합니다:

```toml
[login]
usePassword = true
```

### 구성 매개변수

#### `[[login.oidc]]` 섹션

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | OIDC 연결의 고유 식별자(config.toml의 키와 일치해야 함) |
| `label` | string | Yes | 로그인 버튼에 표시될 텍스트(예: "Login with Microsoft") |

#### `[login]` 섹션

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | SSO 외에 비밀번호 기반 로그인을 허용할지 여부 |

### usePassword 이해하기

**`usePassword = true`인 경우:**
- 로그인 화면에 SSO 버튼(예: "Login with Microsoft")이 표시됩니다.
- 로그인 화면에 사용자 이름 및 비밀번호 필드도 표시됩니다.
- 사용자는 두 방법 중 하나로 인증할 수 있습니다.
- 일부 사용자는 SSO를 사용하고 다른 사용자는 비밀번호를 사용하는 하이브리드 설정을 허용합니다.

**`usePassword = false`(또는 생략)인 경우:**
- 로그인 화면에 SSO 버튼만 표시됩니다.
- 사용자 이름/비밀번호 필드가 없습니다.
- OIDC 인증만 사용할 수 있습니다.

!!! tip "팁"

    비밀번호 기반 로그인은 `digna user add` 명령어 또는 대시보드를 통해 비밀번호로 생성된 사용자에게만 제공됩니다.

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

## Backend Configuration {: #backend-configuration }

### 파일 위치

```
/config.toml
```

(루트 digna 설치 디렉터리)

### 1단계: OIDC 공급자 섹션 추가

각 공급자에 대해 `[oidc.<key>]` 섹션을 추가해야 합니다. 여기서 key는 `dashboard_config.toml`에 정의된 `key`와 일치해야 합니다.

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
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | 아이덴티티 제공자에서 발급된 클라이언트 ID | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | 아이덴티티 제공자에서 발급된 클라이언트 시크릿 | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | 인증 후 콜백 URL | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC 구성 엔드포인트 | `https://login.microsoftonline.com/...` |

!!! warning "중요"

    플레이스홀더 값(`<client_id>`, `<client_secret>`, `<tenant_id>`)을 아이덴티티 제공자 개발자 포털에서 발급받은 실제 자격 증명으로 바꾸세요.

### Redirect URI

리디렉션 URI는 아이덴티티 제공자 구성에 등록된 값과 동일해야 합니다:

```
http://localhost:5173/oidc/callback
```

digna가 다른 도메인에 호스팅된 경우 다음과 같이 적절히 업데이트하세요:
- 로컬: `http://localhost:5173/oidc/callback`
- 프로덕션: `https://digna.yourdomain.com/oidc/callback`

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

## Testing Login {: #testing-login }

구성을 완료한 후 SSO가 정상 작동하는지 확인하세요.

### 테스트 전 체크리스트

테스트 전에 다음을 확인하세요:

- [ ] `dashboard_config.toml`에 OIDC 공급자가 추가되었는지
- [ ] `config.toml`에 OIDC 자격 증명이 추가되었는지
- [ ] 두 파일이 저장되었는지
- [ ] 자격 증명(client ID, client secret)이 정확한지
- [ ] 리디렉션 URI가 배포 URL과 일치하는지
- [ ] 아이덴티티 제공자 앱에 리디렉션 URI가 구성되어 있는지

### 테스트 단계

#### 1단계: 서비스 재시작

변경 사항을 적용하려면 digna 백엔드와 웹 서버를 재시작하세요.

**Windows 서비스로 실행 중인 경우:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**수동으로 실행하는 경우:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**IIS 또는 Tomcat을 사용하는 경우:**
웹 서버 서비스를 재시작하세요.

#### 2단계: 대시보드 열기

브라우저에서 digna 대시보드를 엽니다:

```
http://localhost:5173
```

(또는 구성한 대시보드 URL)

#### 3단계: 로그인 버튼 확인

구성한 각 공급자에 대한 로그인 버튼이 표시되는지 확인합니다:

- "Login with Microsoft" 버튼이 보여야 함
- "Login with Google" 버튼이 보여야 함
- (`usePassword = true`인 경우) 사용자명/비밀번호 필드가 보여야 함

버튼이 보이지 않는 경우:
- `dashboard_config.toml`이 저장되었는지 확인
- 대시보드 서비스가 재시작되었는지 확인
- 브라우저 콘솔(F12)에서 오류 확인

#### 4단계: SSO 로그인 테스트

SSO 버튼(예: "Login with Microsoft")을 클릭합니다:

1. 아이덴티티 제공자의 로그인 페이지로 리디렉션되어야 합니다.
2. 기업 자격증명으로 로그인합니다.
3. digna로 리디렉션되어야 합니다.
4. digna에 로그인되어야 합니다.

#### 5단계: 사용자 생성 확인

SSO 로그인 성공 후:

- 사용자가 digna에 자동으로 생성되어야 함
- 사용자가 로그인되어야 함
- 사용자 프로필에 아이덴티티 제공자 정보가 표시되어야 함
- digna 대시보드를 볼 수 있어야 함

#### 6단계: 비밀번호 로그인 테스트(활성화된 경우)

`usePassword = true`인 경우:

1. digna에서 로그아웃합니다.
2. 로그인 페이지에서 사용자명과 비밀번호를 입력합니다.
3. 비밀번호 자격증명으로 로그인이 되어야 합니다.

---

## Troubleshooting {: #troubleshooting }

### 로그인 버튼이 나타나지 않음

**증상:**
- 로그인 페이지에 OIDC 로그인 버튼이 보이지 않음
- 비밀번호 필드만 보임(만약 usePassword = true인 경우)

**원인 및 해결책:**
1. `dashboard_config.toml`이 `dashboard/` 디렉터리에 있는지 확인
2. `[[login.oidc]]` 섹션이 올바른 문법으로 존재하는지 확인
3. 대시보드 서비스를 재시작
4. 브라우저 캐시 지우기(Ctrl+Shift+Delete 또는 Cmd+Shift+Delete)
5. 브라우저 콘솔(F12 → Console 탭)에서 오류 확인

---

### Redirect URI 불일치 오류

**증상:**
- SSO 버튼 클릭 후 "redirect_uri mismatch" 관련 오류 발생
- "The redirect URI is not registered" 오류

**원인 및 해결책:**
1. `config.toml`의 `DIGNA_OIDC_REDIRECT_URI`가 올바른지 확인
2. 아이덴티티 제공자 설정에 리디렉션 URI가 등록되어 있는지 확인
3. 프로토콜, 도메인, 경로까지 동일한지 확인
4. 리디렉션 URI에 오타가 없는지 확인
5. HTTPS 사용 시 인증서가 유효한지 확인

---

### 클라이언트 자격 증명 오류(Invalid Client Credentials)

**증상:**
- "Invalid client ID or secret" 오류
- 자격 증명 오류로 인증 실패

**원인 및 해결책:**
1. `DIGNA_OIDC_CLIENT_ID` 및 `DIGNA_OIDC_CLIENT_SECRET`이 정확한지 확인
2. 추가 공백이나 특수문자가 섞여 있지 않은지 확인
3. 자격 증명이 만료되거나 취소되지 않았는지 확인
4. 구성 업데이트 후 백엔드 서비스를 재시작
5. 아이덴티티 제공자 콘솔에서 자격 증명이 활성 상태인지 확인

---

### 로그인 지연 또는 타임아웃

**증상:**
- SSO 버튼 클릭 시 아무 동작이 없음
- 몇 초 후 타임아웃 발생
- 브라우저에 "Failed to connect" 등의 메시지 표시

**원인 및 해결책:**
1. digna 백엔드가 실행 중인지 확인: `digna repo check`
2. 아이덴티티 제공자로의 네트워크 연결 확인
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
2. 사용자 권한 설정이 올바른지 확인
3. digna 로그에서 오류 메시지 검토
4. 백엔드 서비스 재시작
5. 문제가 지속되면 support@digna.ai로 문의

---

## Supported Providers {: #supported-providers }

### 테스트 및 지원됨

다음 OIDC 공급자는 테스트되었으며 작동하는 것으로 확인되었습니다:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### 기타 OIDC 공급자

OpenID Connect를 지원하는 모든 공급자를 통합할 수 있습니다. 필요한 정보:

- Client ID
- Client secret
- OpenID 구성 URL(일반적으로 `/.well-known/openid-configuration`)
- 지원되는 스코프(일반적으로 `openid profile email`)

특정 공급자 통합에 도움이 필요하면 support@digna.ai로 문의하세요.

---

## Best Practices

**권장 사항:**
- 프로덕션에서는 HTTPS 사용(HTTP 사용 금지)
- 클라이언트 시크릿을 안전하게 보관(가능하면 환경 변수 사용)
- 주기적으로 시크릿 교체(rotate) 수행
- 먼저 비프로덕션 환경에서 테스트
- 구성된 공급자를 문서화
- 로그인 로그를 모니터링하여 이상 활동 감지
- 아이덴티티 제공자 구성과 digna 구성을 동기화 상태로 유지

**금지 사항:**
- 클라이언트 시크릿을 버전 관리에 저장하지 마세요
- 프로덕션에서 HTTP 리디렉션 URI 사용 금지
- 동일한 키로 여러 공급자 구성 금지
- 프로덕션에 기본/테스트 자격 증명 남겨두지 않기
- 시크릿이 포함된 구성 파일 노출 금지
- 개발 및 프로덕션 자격 증명을 혼용하지 마세요

---

## Support

SSO 구성에 도움이 필요하신가요?

- **이메일:** support@digna.ai
- **문서:** https://docs.digna.ai
- **웹사이트:** https://www.digna.ai

---

**마지막 업데이트:** August 30, 2026  
**릴리스:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**

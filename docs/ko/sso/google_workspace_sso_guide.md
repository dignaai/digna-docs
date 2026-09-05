---
title: Google Workspace SSO – Single Sign-On 통합 | digna 문서
description: OpenID Connect를 사용하여 Google Workspace와 digna의 Single Sign-On을 구성하는 방법 — OAuth 동의 화면, OAuth 클라이언트 ID, 승인된 리디렉트 URI 및 대응하는 digna 구성.
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, oauth consent screen, openid connect, enterprise authentication
---

# Google Workspace로 SSO 설정하기

Google의 아이덴티티 플랫폼은 OIDC 규격을 준수하며 모든 고객에 대해 단일의 잘 알려진 디스커버리 URL을 사용하므로, 조직별로 필요한 값은 클라이언트 ID와 시크릿뿐입니다.

이 가이드는 **Google 쪽**을 다룹니다: OAuth 클라이언트 생성과 digna가 필요로 하는 값 수집 방법입니다. digna 쪽 — `dashboard_config.toml`, 테스트 및 문제해결 — 은 모든 공급자에서 동일하며 [Single Sign-On Overview](overview.md)에 설명되어 있습니다.

---

## 시작 전에

| 요구 사항 | 비고 |
|---|---|
| **Google Cloud 프로젝트** | Workspace 도메인과 같은 조직에 속한 아무 프로젝트 |
| **역할** | 프로젝트의 Editor 또는 Owner |
| **digna 리디렉트 URI** | 로그인 후 사용자가 돌아올 URL, 예: `https://digna.yourdomain.com/oidc/callback` |

---

## 1단계: OAuth 동의 화면 구성

Google은 동의 화면이 존재할 때까지 자격 증명을 발급하지 않습니다.

1. [Google Cloud Console](https://console.cloud.google.com)을 열고 프로젝트를 선택합니다.
2. **APIs & Services → OAuth consent screen**으로 이동합니다.
3. 사용자 유형을 선택합니다:
   - **Internal** — Workspace 도메인의 계정만 로그인할 수 있습니다. 권장합니다.
   - **External** — 모든 Google 계정이 로그인 시도를 할 수 있습니다.
4. 앱 이름, 사용자 지원 이메일 및 개발자 연락 이메일을 입력합니다.
5. **Scopes** 단계에서 `openid`, `.../auth/userinfo.email` 및 `.../auth/userinfo.profile`을 추가합니다.
6. 저장합니다.

!!! warning "외부 앱은 게시되어야 합니다"

    **External** 동의 화면은 *Testing* 상태로 시작하며, 이 상태에서는 테스트 사용자 목록에 명시적으로 추가된 계정만 로그인을 완료할 수 있습니다. 다른 모든 사용자에게는 "digna has not completed the Google verification process" 메시지가 표시됩니다. **Publishing status**에서 앱을 **In production**으로 전환하거나 **Internal**을 사용하세요 — Internal은 이러한 제한이 없으며 Workspace 전용 배포에는 올바른 선택입니다.

---

## 2단계: OAuth 클라이언트 생성

1. **APIs & Services → Credentials**로 이동합니다.
2. **Create Credentials → OAuth client ID**를 클릭합니다.
3. **Application type**을 **Web application**으로 설정합니다.
4. 이름을 지정합니다 (예: `digna`).
5. **Authorized redirect URIs**에서 **Add URI**를 클릭하고 다음을 입력합니다:

```
https://digna.yourdomain.com/oidc/callback
```

6. **Create**를 클릭합니다.

!!! note "승인된 JavaScript 출처는 필요하지 않습니다"

    digna는 인가 코드를 브라우저가 아닌 백엔드에서 교환하므로 **Authorized JavaScript origins** 필드는 비워둘 수 있습니다. 리디렉트 URI만 중요합니다.

---

## 3단계: 자격 증명 수집

생성 후 표시되는 대화창에는 다음이 보입니다:

- **Client ID** — `.apps.googleusercontent.com`로 끝남 → `DIGNA_OIDC_CLIENT_ID`가 됩니다
- **Client secret** → `DIGNA_OIDC_CLIENT_SECRET`가 됩니다

두 값 모두 대부분의 다른 제공자와 달리 이후에도 자격 증명 상세 페이지에서 다시 조회할 수 있습니다.

---

## 4단계: 디스커버리 URL

Google은 모든 고객에 대해 하나의 디스커버리 URL을 사용합니다 — 치환할 내용이 없습니다:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## 5단계: digna 구성

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Google로 로그인"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<3단계에서 복사한 클라이언트 시크릿>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

두 파일의 `key`는 일치해야 합니다 — 여기서는 `google`입니다.

---

## 6단계: 테스트

백엔드와 웹 서버를 재시작한 다음 대시보드를 엽니다. 전체 체크리스트는 [Testing Login](overview.md#testing-login)을 참조하세요.

---

## Google Workspace 문제해결

### Error 400: redirect_uri_mismatch

`DIGNA_OIDC_REDIRECT_URI`에 설정된 URI가 **Authorized redirect URIs** 목록에 없거나, 끝에 슬래시가 있거나 스킴이 다른 등 사소한 차이가 있는 경우 발생합니다. Google의 오류 페이지는 수신한 URI를 보여줍니다 — 등록된 URI와 문자 단위로 비교하세요.

### 이 앱이 차단됨 / 검증을 완료하지 않았음

동의 화면이 **External**이고 아직 *Testing* 상태입니다. 게시하거나 앱을 **Internal**로 전환하세요.

### 액세스 차단: 권한 오류

로그인 시도하는 계정이 Workspace 도메인 외부에 있고 동의 화면이 **Internal**인 경우 발생합니다. Internal 앱은 조직 내 계정만 허용하는 것이 의도된 동작입니다.

### 변경 사항 적용에 몇 분 소요

Google은 자격 증명 및 동의 화면 변경을 비동기적으로 전파합니다. 새로 추가한 리디렉트 URI가 적용되기까지 몇 분 걸릴 수 있으므로 변경이 무시된 것처럼 보이면 조사하기 전에 잠시 기다렸다가 재시도하세요.

---

## 참고 링크

- [Single Sign-On Overview](overview.md) — 구성 참조, 테스트 및 일반적인 문제해결
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
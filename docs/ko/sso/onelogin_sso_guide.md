---
title: OneLogin SSO – Single Sign-On 통합 | digna 문서
description: OpenID Connect를 사용해 OneLogin으로 digna의 Single Sign-On을 구성합니다 — OIDC 앱 생성, 리디렉션 URI, 클라이언트 자격증명, 토큰 엔드포인트 인증 및 대응하는 digna 설정을 다룹니다.
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, 토큰 엔드포인트 인증, 엔터프라이즈 인증
---

# OneLogin으로 SSO 설정

OneLogin은 OIDC 규격을 준수합니다. 특징적인 점은 애플리케이션 생성 시 카탈로그에서 커넥터 유형을 선택하면 이후에 변경할 수 없다는 것입니다.

이 가이드는 **OneLogin 측**을 다룹니다: 애플리케이션 생성과 digna에 필요한 값 수집. digna 측 — `dashboard_config.toml`, 테스트 및 문제 해결 — 은 모든 공급자에 대해 동일하며 [Single Sign-On Overview](overview.md)에 설명되어 있습니다.

---

## 시작하기 전에

| 요구사항 | 비고 |
|---|---|
| **OneLogin 역할** | 애플리케이션을 추가할 수 있는 계정 소유자 또는 관리자 |
| **서브도메인** | 예: `yourcompany.onelogin.com` |
| **digna 리디렉션 URI** | 로그인 후 사용자가 돌아올 URL, 예: `https://digna.yourdomain.com/oidc/callback` |

---

## 1단계: OIDC 애플리케이션 생성

1. OneLogin 관리자 포털에 로그인합니다.
2. **Applications → Applications**로 이동합니다.
3. **Add App**을 클릭합니다.
4. `OpenId Connect`를 검색하고 **OpenId Connect (OIDC)** 커넥터를 선택합니다.
5. **Display Name**을 `digna`로 설정합니다.
6. **Save**를 클릭합니다.

!!! warning "커넥터 유형은 생성 시 고정됩니다"

    OneLogin은 SAML과 OIDC에 대해 별도의 카탈로그 항목을 가지고 있으며, 애플리케이션을 한 프로토콜에서 다른 프로토콜로 변환할 수 없습니다. 실수로 SAML 커넥터를 선택했다면 앱을 삭제하고 다시 추가하세요 — 프로토콜을 전환하는 설정은 없습니다.

---

## 2단계: 리디렉션 URI 구성

1. **Configuration** 탭을 엽니다.
2. **Redirect URI's**에 digna 콜백 URL을 입력합니다:

```
https://digna.yourdomain.com/oidc/callback
```

3. 선택적으로 **Post Logout Redirect URIs**에 대시보드 URL을 설정합니다.
4. **Save**를 클릭합니다.

!!! note "URI는 한 줄에 하나씩"

    쉼표로 구분된 목록을 기대하는 공급자와 달리 OneLogin의 **Redirect URI's** 필드는 한 줄에 하나의 URI를 받습니다.

---

## 3단계: 애플리케이션 유형과 인증 방식 설정

1. **SSO** 탭을 엽니다.
2. **Application Type**이 *Web*인지 확인합니다.
3. **Token Endpoint → Authentication Method**를 *POST* (`client_secret_post`) 또는 *Basic* (`client_secret_basic`)으로 설정합니다.

!!! warning "*None*을 선택하지 마십시오"

    인증 방식을 *None*으로 설정하면 애플리케이션이 시크릿 없는 퍼블릭 클라이언트가 되어 digna의 백엔드 토큰 교환이 거부됩니다. POST 또는 Basic 중 하나를 사용하세요.

---

## 4단계: 자격증명 수집

계속해서 **SSO** 탭에서:

- **Client ID** → `DIGNA_OIDC_CLIENT_ID`가 됩니다.
- **Client Secret** → `DIGNA_OIDC_CLIENT_SECRET`가 됩니다 (**Show client secret** 클릭).

페이지에는 또한 **Issuer URL**이 표시되며, 다음 단계의 디스커버리 URL을 확인하는 데 사용됩니다.

---

## 5단계: 사용자 할당

1. **Access** 탭을 엽니다.
2. digna를 사용할 수 있는 역할 또는 그룹을 추가합니다.
3. **Save**를 클릭합니다.

!!! note "할당되지 않은 사용자는 로그인 후 거부됩니다"

    대부분의 공급자와 마찬가지로 OneLogin은 먼저 사용자를 인증하고 그 다음 권한을 확인합니다. 할당되지 않은 사용자는 로그인에는 성공하지만 이후 거부되어 digna 오류처럼 보일 수 있습니다.

---

## 6단계: 디스커버리 URL 구성

OneLogin 서브도메인을 대체합니다:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

예를 들면:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2는 API 버전입니다"

    OneLogin의 현재 OIDC 구현은 `/oidc/2/`에 위치합니다. 이전 문서에서는 버전 없이 `/oidc/`가 나와 있는데 이는 사용 중단된 첫 번째 버전을 가리킵니다. 확실하지 않으면 SSO 탭에 표시된 **Issuer URL**과 비교하세요 — 디스커버리 URL은 Issuer 뒤에 `/.well-known/openid-configuration`를 붙인 것입니다.

---

## 7단계: digna 구성

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "OneLogin으로 로그인"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<4단계에서 복사한 클라이언트 시크릿>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

두 파일의 `key`는 일치해야 합니다 — 여기서는 `onelogin`입니다.

---

## 8단계: 테스트

백엔드와 웹 서버를 재시작한 뒤 대시보드를 엽니다. 전체 체크리스트는 [Testing Login](overview.md#testing-login)을 참고하세요.

---

## OneLogin 문제 해결

### redirect_uri did not match

콜백 URL이 **Configuration → Redirect URI's**에 없거나 항목들이 쉼표로 구분되어 줄바꿈으로 입력되지 않았습니다.

### invalid_client at the Token Step

**Token Endpoint → Authentication Method**가 *None*으로 설정되어 있거나 `config.toml`의 클라이언트 시크릿이 오래되었습니다. **SSO** 탭에서 시크릿을 표시하여 비교하세요.

### 애플리케이션이 사용자에게 표시되지 않음

**Access** 탭에서 어떤 역할이나 그룹에도 접근 권한이 부여되지 않았습니다.

### 디스커버리 URL에서 404 발생

서브도메인이 잘못되었거나 URL에 `/oidc/2/`가 빠졌습니다. SSO 탭에 표시된 **Issuer URL**과 비교하세요.

---

## 관련 문서

- [Single Sign-On Overview](overview.md) — 구성 참조, 테스트 및 일반적인 문제 해결
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)
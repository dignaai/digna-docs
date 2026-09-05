---
title: Okta SSO – Single Sign-On 통합 | digna 문서
description: OpenID Connect를 사용해 Okta로 digna의 Single Sign-On을 구성합니다 — 앱 통합, 로그인 리디렉션 URI, 클라이언트 자격 증명, 인증 서버 선택 및 그에 맞는 digna 설정을 다룹니다.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, 앱 통합, 인증 서버, openid connect, 기업 인증
---

# Okta로 SSO 설정

Okta는 OIDC를 준수하지만, 첫 통합에서 많은 이들이 헷갈리는 한 가지가 있습니다. Okta 조직은 여러 인증 서버(authorization server)를 노출하며, 각 서버는 고유한 discovery URL을 가집니다.

이 가이드는 **Okta 쪽** — 앱 통합 생성과 digna가 필요로 하는 값 수집 — 을 다룹니다. digna 쪽( `dashboard_config.toml`, 테스트와 문제해결)은 공급자에 상관없이 동일하며 [Single Sign-On Overview](overview.md)에 설명되어 있습니다.

---

## 시작하기 전에

| 요구사항 | 비고 |
|---|---|
| **Okta role** | Super Administrator, 또는 앱 통합을 생성할 수 있는 관리자 역할 |
| **Okta domain** | 예: `yourcompany.okta.com`, 또는 구성된 커스텀 도메인 |
| **digna redirect URI** | 로그인 후 사용자가 돌아올 URL, 예: `https://digna.yourdomain.com/oidc/callback` |

---

## 단계 1: 앱 통합 생성

1. Okta Admin Console에 로그인합니다.
2. **Applications → Applications**로 이동합니다.
3. **Create App Integration**를 클릭합니다.
4. 다음을 선택합니다:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. **Next**를 클릭합니다.

!!! warning "애플리케이션 유형은 변경할 수 없습니다"

    *Single-Page Application* 대신 *Web Application*을 선택하지 않으면 비밀 키가 없는 퍼블릭 클라이언트가 생성되고, digna의 백엔드 코드 교환 단계에서 `invalid_client` 오류가 발생합니다. 유형은 생성 시 고정되므로 잘못 선택했다면 앱을 삭제하고 다시 만들어야 합니다.

---

## 단계 2: 통합 구성

1. **App integration name**: `digna`
2. **Grant type**: *Authorization Code*가 선택된 상태로 둡니다.
3. **Sign-in redirect URIs**: digna 콜백 URL을 입력합니다:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: 선택 사항입니다.
5. **Assignments**에서 누가 이 통합을 사용할지 선택합니다 — 특정 그룹을 지정하는 것이 *Allow everyone in your organization to access*보다 안전합니다.
6. **Save**를 클릭합니다.

!!! note "할당이 필요합니다"

    Okta는 사용자를 인증한 후 해당 사용자가 애플리케이션에 할당되었는지를 확인합니다. 할당되지 않은 사용자는 Okta 로그인 페이지에서 정상적으로 로그인하더라도 리디렉션 시 거부됩니다. 본인에게는 로그인이 되지만 동료에게는 되지 않는다면, 가장 먼저 확인할 것은 할당 여부입니다.

---

## 단계 3: 자격 증명 수집

애플리케이션의 **General** 탭에서 **Client Credentials** 항목을 확인합니다:

- **Client ID** → `DIGNA_OIDC_CLIENT_ID`가 됩니다.
- **Client secret** → `DIGNA_OIDC_CLIENT_SECRET`가 됩니다(눈 아이콘을 클릭해 표시).

---

## 단계 4: 인증 서버 선택

이 단계에서 discovery URL이 결정됩니다. **Security → API**로 이동하여 조직의 인증 서버들을 확인합니다.

**Org authorization server** — Okta 조직 자체를 위한 토큰을 발급합니다:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — Okta가 생성하는 `default`를 포함한 커스텀 서버:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

내장 서버의 경우 `<auth_server_id>`는 문자 그대로 `default`입니다:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "어떤 것을 선택해야 하나요?"

    조직이 API 접근 정책을 위해 이미 커스텀 인증 서버를 표준으로 사용 중이 아니라면 **org** 인증 서버를 사용하세요. Okta Developer 계정은 기본적으로 `default`를 사용하며, 많은 기업 조직에서는 이를 비활성화합니다. 두 URL을 브라우저에서 열어보고 JSON을 반환하는 쪽이 사용 가능한 서버입니다.

---

## 단계 5: digna 구성

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Okta로 로그인"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<3단계에서 복사한 클라이언트 시크릿>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

두 파일의 `key`는 반드시 일치해야 합니다 — 여기서는 `okta`입니다.

---

## 단계 6: 테스트

백엔드와 웹 서버를 재시작한 다음 대시보드를 엽니다. 전체 체크리스트는 [Testing Login](overview.md#testing-login)을 참조하세요.

---

## Okta 문제해결

### 리디렉션 URI가 등록되어 있지 않습니다

Okta는 문제를 일으키는 URI를 오류 메시지에 표시합니다. 이를 **General → Sign-in redirect URIs**와 비교해보세요; Okta는 후행 슬래시 포함 전체 문자열을 정확히 일치시킵니다.

### 사용자가 클라이언트 애플리케이션에 할당되어 있지 않습니다

계정이 애플리케이션의 할당 목록에 없습니다. **Assignments**에서 사용자나 그들의 그룹을 추가하세요.

### 400 Bad Request: Invalid Authorization Server

디스커버리 URL의 `<auth_server_id>`가 존재하지 않을 때 발생합니다. 보통 `default`가 제거된 조직에서 발생합니다. 실제로 사용 가능한 서버는 **Security → API**에서 확인하세요.

### 토큰 단계에서 invalid_client

통합이 Single-Page Application으로 생성되어 클라이언트 시크릿이 없습니다. Web Application으로 다시 생성하세요.

---

## 참고

- [Single Sign-On Overview](overview.md) — 구성 참조, 테스트 및 일반적인 문제해결
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
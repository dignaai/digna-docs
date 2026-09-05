---
title: Keycloak SSO – Single Sign-On 통합 | digna 문서
description: OpenID Connect를 사용하여 Keycloak으로 digna의 Single Sign-On을 구성합니다 — realm 및 클라이언트 설정, 클라이언트 인증, 유효한 리디렉트 URI, 클라이언트 시크릿 및 해당 digna 구성.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, confidential client, openid connect, self-hosted identity provider
---

# Keycloak로 SSO 설정

Keycloak은 자체 호스팅되는, 완전한 OIDC 호환 아이덴티티 공급자입니다. 직접 운영하므로 디스커버리 URL은 공급업체 도메인이 아니라 본인의 호스트 이름과 realm에서 만들어집니다.

이 가이드는 **Keycloak 쪽**을 다룹니다: 클라이언트 생성과 digna가 필요로 하는 값 수집. digna 쪽 — `dashboard_config.toml`, 테스트 및 문제해결 — 은 모든 공급자에서 동일하며 [Single Sign-On 개요](overview.md)에 설명되어 있습니다.

---

## 시작 전에

| 요구사항 | 설명 |
|---|---|
| **Keycloak 버전** | 여기에서 사용하는 URL 경로는 17 이상 — 4단계의 주의사항 참조 |
| **Keycloak 역할** | 대상 realm의 `realm-admin`, 또는 서버 관리자 |
| **Realm** | digna 사용자가 속한 realm, 반드시 `master`일 필요는 없음 |
| **digna 리디렉트 URI** | 로그인 후 사용자가 돌아올 URL, 예: `https://digna.yourdomain.com/oidc/callback` |

---

## 단계 1: Realm 선택

1. Keycloak 관리자 콘솔을 엽니다.
2. 좌상단의 realm 선택기에서 사용자가 속한 realm으로 전환합니다.

!!! warning "master Realm을 사용하지 마십시오"

    `master` realm은 Keycloak 자체 관리를 위한 용도입니다. 애플리케이션 클라이언트는 별도의 realm에 있어야 하며; digna를 `master`에 두면 그 사용자가 Keycloak 관리 콘솔에 접근할 수 있는 경로가 생깁니다.

---

## 단계 2: 클라이언트 생성

1. **Clients**로 이동하여 **Create client**를 클릭합니다.
2. 구성:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — 이 값은 `DIGNA_OIDC_CLIENT_ID`가 됩니다
3. **Next**를 클릭합니다.
4. **Capability config** 단계에서 **Client authentication**을 **On**으로 전환합니다.
5. **Standard flow**는 활성화된 상태로 두세요; 다른 플로우는 필요하지 않습니다.
6. **Next**를 클릭합니다.

!!! warning "Client authentication을 켜야 합니다"

    **Client authentication**이 꺼져 있으면 Keycloak은 자격증명이 전혀 없는 *public* 클라이언트를 생성합니다 — 4단계의 **Credentials** 탭이 존재하지 않습니다. digna는 confidential 클라이언트가 필요합니다. 잘못 설정했더라도 생성 후 이 토글을 변경할 수 있습니다.

---

## 단계 3: 리디렉트 URI 설정

**Login settings** 단계(또는 이후 **Settings** 탭)에서:

1. **Valid redirect URIs**: digna 콜백 URL을 입력합니다:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: 비워두거나 리디렉트 URIs를 반영하도록 `+`로 설정합니다.
3. **Save**를 클릭합니다.

!!! tip "와일드카드 사용을 피하세요"

    Keycloak은 `https://digna.yourdomain.com/*` 같은 패턴을 허용합니다. 와일드카드는 해당 호스트의 모든 경로가 인가 코드를 받을 수 있게 하므로, 정확한 콜백 URL을 사용하는 것이 좋습니다.

---

## 단계 4: 클라이언트 시크릿 수집

1. **Credentials** 탭을 엽니다.
2. **Client Authenticator**가 *Client Id and Secret*인지 확인합니다.
3. **Client secret**을 복사 → 이 값이 `DIGNA_OIDC_CLIENT_SECRET`가 됩니다.

시크릿은 여기서 계속해서 조회할 수 있으며 **Regenerate**로 재생성할 수 있습니다.

---

## 단계 5: 디스커버리 URL 구성

Keycloak 호스트와 realm 이름을 대입하세요:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

예시:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 및 이전 버전은 /auth를 포함합니다"

    Keycloak 17 이전에는 모든 엔드포인트가 `/auth` 접두사 아래에 있었습니다:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    `KC_HTTP_RELATIVE_PATH=/auth`를 설정한 배포판은 현재 버전에서도 이전 레이아웃을 유지합니다. `/auth`가 없는 URL이 404를 반환하면 `/auth`를 포함한 URL을 시도해 보세요.

계속하기 전에 브라우저에서 해당 URL을 열어 보세요. JSON 문서가 표시되면 호스트와 realm이 올바른 것입니다.

---

## 단계 6: digna 구성

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Keycloak로 로그인"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

두 파일의 `key`는 반드시 일치해야 합니다 — 여기서는 `keycloak`. 이 값이 Keycloak의 **Client ID**와 같을 필요는 없지만, 동일하게 하면 관리하기 쉽습니다.

---

## 단계 7: 테스트

백엔드와 웹 서버를 재시작한 다음 대시보드를 엽니다. 전체 체크리스트는 [Single Sign-On 개요](overview.md#testing-login)를 참조하세요.

---

## Keycloak 문제해결

### 잘못된 매개변수: redirect_uri

콜백 URL이 **Valid redirect URIs**에 포함되어 있지 않습니다. Keycloak은 수신한 URI를 서버 로그에 기록하므로, 정확한 불일치를 확인하려면 로그가 가장 빠릅니다.

### Credentials 탭이 없음

클라이언트가 public입니다. **Settings → Capability config**에서 **Client authentication**을 켜세요.

### 디스커버리 URL의 404

realm 이름이 틀렸거나 배포가 `/auth` 접두사를 사용하고 있을 수 있습니다. 관리자 콘솔에서 realm 목록을 확인하고 두 가지 URL 형태를 모두 시도해 보세요.

### unauthorized_client 또는 invalid_client

**Standard flow**가 **Capability config**에서 비활성화되었거나, Keycloak에서 시크릿을 재생성했지만 `config.toml`을 업데이트하지 않은 경우입니다.

### 백엔드에서의 인증서 오류

사설 또는 자체 서명된 인증서 뒤에 있는 자체 호스팅 Keycloak은 digna의 디스커버리 URL에 대한 아웃바운드 HTTPS 호출에 실패합니다. digna 백엔드를 실행하는 머신의 신뢰 저장소에 발급 CA를 설치하세요.

---

## 참고

- [Single Sign-On 개요](overview.md) — 구성 참조, 테스트 및 일반적인 문제해결
- [Keycloak: 애플리케이션 보안](https://www.keycloak.org/docs/latest/securing_apps/)
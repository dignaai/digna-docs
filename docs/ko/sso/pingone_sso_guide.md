---
title: PingOne SSO – Single Sign-On 통합 | digna 문서
description: OpenID Connect를 사용하여 PingOne으로 digna의 Single Sign-On을 구성합니다 — OIDC 웹 앱 설정, 리디렉트 URI, 클라이언트 자격 증명, 환경 ID, 지역 도메인 및 대응하는 digna 구성.
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, 환경 ID, OpenID Connect, 엔터프라이즈 인증
---

# PingOne으로 SSO 설정

PingOne은 OIDC를 준수합니다. 특히 주의해야 할 값이 두 가지 있습니다: 모든 엔드포인트 URL에 나타나는 **Environment ID(환경 ID)**와 북미, 유럽, 캐나다, 아시아태평양, 호주 테넌트마다 다른 **지역 도메인**입니다.

이 가이드는 **PingOne 측 작업**을 다룹니다: 애플리케이션 생성과 digna가 필요로 하는 값 수집. digna 측 설정 — `dashboard_config.toml`, 테스트 및 문제 해결 — 은 모든 공급자에서 동일하며 [Single Sign-On Overview](overview.md)에 설명되어 있습니다.

---

## 시작하기 전

| 요구사항 | 비고 |
|---|---|
| **PingOne 역할** | 대상 환경의 Environment Admin 또는 Identity Data Admin |
| **환경** | digna 사용자가 속한 PingOne 환경 |
| **digna 리디렉트 URI** | 로그인 후 사용자가 돌아올 URL, 예: `https://digna.yourdomain.com/oidc/callback` |

---

## 단계 1: 애플리케이션 생성

1. PingOne 관리자 콘솔에 로그인하고 환경을 선택합니다  
2. **Applications → Applications**로 이동합니다  
3. **+** 버튼을 클릭합니다  
4. **Application Name**에 `digna`를 입력합니다  
5. **OIDC Web App**을 선택합니다  
6. **Save**를 클릭합니다

!!! warning "OIDC Web App를 선택하세요, Single-Page App이 아닙니다"

    *Single-Page App*과 *Native App*은 시크릿을 보관할 수 없는 퍼블릭 클라이언트를 만듭니다. digna는 백엔드에서 인가 코드를 교환하므로 기밀을 보관할 수 있는 **OIDC Web App** 유형이 필요합니다.

---

## 단계 2: 리디렉트 URI 구성

1. 애플리케이션의 **Configuration** 탭을 엽니다  
2. 연필 아이콘을 클릭하여 편집합니다  
3. **Response Type**이 *Code*이고 **Grant Type**이 *Authorization Code*인지 확인합니다  
4. **Redirect URIs**에 digna 콜백 URL을 입력합니다:

```
https://digna.yourdomain.com/oidc/callback
```

5. **Token Endpoint Authentication Method**를 *Client Secret Post* 또는 *Client Secret Basic*으로 설정합니다  
6. **Save**를 클릭합니다

---

## 단계 3: 애플리케이션 활성화

애플리케이션의 행 또는 상세 패널에서 토글을 **enabled**로 전환합니다.

!!! warning "새 애플리케이션은 기본적으로 비활성화됩니다"

    PingOne은 애플리케이션을 비활성화된 상태로 생성합니다. 비활성화된 애플리케이션은 인가 단계에서 토글을 언급하지 않는 오류를 발생시키므로, 다른 디버깅을 시작하기 전에 이 항목을 확인하는 것이 좋습니다.

---

## 단계 4: 스코프 부여

1. **Resources** 탭을 엽니다  
2. `openid`가 부여되어 있는지 확인하고 **OpenID Connect** 리소스에서 `profile` 및 `email`을 추가합니다  
3. **Save**를 클릭합니다

---

## 단계 5: 사용자 할당

1. **Access** 탭을 엽니다  
2. digna를 사용할 수 있는 집단 또는 그룹을 추가합니다  
3. **Save**를 클릭합니다

---

## 단계 6: 자격 증명 및 환경 ID 수집

**Configuration** 탭에서 **General**을 확장합니다:

- **Client ID** → `DIGNA_OIDC_CLIENT_ID`가 됩니다  
- **Client Secret** → `DIGNA_OIDC_CLIENT_SECRET`가 됩니다 (눈 아이콘을 클릭)  
- **Environment ID** → discovery URL에 들어갑니다

같은 탭에 이미 만들어져 있는 **OIDC Discovery Endpoint**가 나열되어 있으며, 이를 직접 복사하면 수동으로 조합할 필요가 없습니다.

---

## 단계 7: Discovery URL 구성

환경 ID와 해당 지역의 도메인을 대체하여 사용합니다:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| 지역 | 도메인 |
|---|---|
| 북미 | `auth.pingone.com` |
| 유럽 | `auth.pingone.eu` |
| 캐나다 | `auth.pingone.ca` |
| 아시아-태평양 | `auth.pingone.asia` |
| 호주 | `auth.pingone.com.au` |

유럽 환경의 예:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "직접 입력하지 말고 복사하세요"

    지역 도메인이 PingOne 통합에서 가장 흔한 실수입니다. 잘못된 지역을 사용하면 유용한 메시지 대신 404가 발생하므로, 6단계의 **OIDC Discovery Endpoint** 값을 사용해 복사하세요.

---

## 단계 8: digna 구성

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

두 파일의 `key`가 일치해야 합니다 — 여기서는 `pingone`.

---

## 단계 9: 테스트

백엔드와 웹 서버를 재시작한 다음 대시보드를 엽니다. 전체 체크리스트는 [Single Sign-On Overview](overview.md#testing-login)를 참조하세요.

---

## PingOne 문제 해결

### Discovery URL에서 404 발생

지역 도메인 또는 Environment ID가 잘못되었습니다. 애플리케이션의 Configuration 탭에 표시된 **OIDC Discovery Endpoint**와 비교하세요.

### NOT_FOUND 또는 애플리케이션 비활성화 오류

3단계의 애플리케이션 토글이 여전히 꺼져 있습니다.

### Redirect URI 불일치

PingOne은 전체 문자열을 비교합니다. **Configuration → Redirect URIs**에서 끝에 슬래시가 있거나 스킴(https/http) 차이가 없는지 확인하세요.

### 로그인은 성공하지만 이메일 클레임이 digna에 도달하지 않음

**Resources** 탭에서 `email` 및 `profile` 스코프가 부여되지 않았습니다.

### 사용자가 애플리케이션을 볼 수 없음

**Access** 탭에서 해당 집단 또는 그룹에 접근 권한이 부여되지 않았습니다.

---

## 참고

- [Single Sign-On Overview](overview.md) — 구성 참고, 테스트 및 일반 문제 해결  
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)
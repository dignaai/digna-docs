# Auth0로 SSO 설정

Auth0는 OIDC 규격을 준수하며 테넌트별 discovery 엔드포인트를 제공합니다. 가장 중요한 것은 discovery URL에 들어가는 테넌트 도메인으로, 커스텀 도메인을 활성화하면 변경됩니다.

이 가이드는 **Auth0 측**을 다룹니다: 애플리케이션 생성 및 digna가 필요로 하는 값 수집. digna 측 설정 — `dashboard_config.toml`, 테스트 및 문제해결 — 은 모든 공급자에 대해 동일하며 [Single Sign-On Overview](overview.md)에 설명되어 있습니다.

---

## 시작하기 전에

| 요구 사항 | 비고 |
|---|---|
| **Auth0 역할** | 테넌트의 Admin |
| **테넌트 도메인** | 예: `yourcompany.eu.auth0.com` — 리전 세그먼트가 중요합니다 |
| **digna 리다이렉트 URI** | 로그인 후 사용자가 돌아오는 URL, 예: `https://digna.yourdomain.com/oidc/callback` |

---

## 1단계: 애플리케이션 생성

1. [Auth0 Dashboard](https://manage.auth0.com)에 로그인합니다.
2. **Applications → Applications**로 이동합니다.
3. **Create Application**을 클릭합니다.
4. 이름을 `digna`로 하고 **Regular Web Applications**을 선택합니다.
5. **Create**를 클릭합니다.

!!! warning "Regular Web Applications 선택"

    *Single Page Application* 및 *Native*는 시크릿이 없는 공개 클라이언트를 생성합니다. digna는 백엔드에서 코드 교환을 수행하므로 비밀을 가진 confidential client가 필요하며, 따라서 **Regular Web Applications**이 올바른 유형입니다. 일부 공급자와 달리 Auth0는 이후 **Settings → Application Type**에서 유형을 변경할 수 있습니다.

---

## 2단계: 콜백 URL 추가

애플리케이션의 **Settings** 탭에서:

1. **Allowed Callback URLs**를 찾습니다.
2. digna 콜백 URL을 입력합니다:

```
https://digna.yourdomain.com/oidc/callback
```

3. 선택적으로 **Allowed Logout URLs**를 대시보드 URL로 설정합니다.
4. 페이지 하단으로 스크롤해 **Save Changes**를 클릭합니다.

!!! note "쉼표로 구분, 줄바꿈으로 구분하지 않음"

    Auth0는 이 필드에서 여러 콜백 URL을 쉼표로 구분해 받습니다. 줄바꿈만으로 구분된 목록은 하나의 잘못된 URL로 해석되어 아무것도 일치시키지 않습니다.

---

## 3단계: 자격 증명 수집

여전히 **Settings**의 **Basic Information** 패널에서:

- **Domain** → discovery URL에 들어갑니다
- **Client ID** → `DIGNA_OIDC_CLIENT_ID`가 됩니다
- **Client Secret** → `DIGNA_OIDC_CLIENT_SECRET`가 됩니다 (클릭하여 표시)

---

## 4단계: Grant Type 확인

1. **Settings → Advanced Settings → Grant Types**로 이동합니다.
2. **Authorization Code**가 체크되어 있는지 확인합니다.

Regular Web Applications의 경우 기본적으로 활성화되어 있습니다. 체크가 해제되어 있으면 digna의 로그인이 `unauthorized_client`로 실패합니다.

---

## 5단계: Discovery URL 구성

3단계에서 얻은 **Domain**을 대체합니다:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

예:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "커스텀 도메인은 Issuer를 변경합니다"

    테넌트가 `login.yourcompany.com`과 같은 커스텀 도메인을 사용하는 경우 discovery URL에 해당 도메인을 사용하세요. 둘을 섞어서 — discovery URL에는 표준 도메인, 브라우저에는 커스텀 도메인 — 사용하면 issuer 불일치가 발생해 로그인은 성공했더라도 토큰이 거부됩니다.

---

## 6단계: digna 구성

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

두 파일의 `key`는 일치해야 합니다 — 여기서는 `auth0`.

---

## 7단계: 테스트

백엔드와 웹 서버를 재시작한 다음 대시보드를 엽니다. 전체 체크리스트는 [Testing Login](overview.md#testing-login)을 참조하세요.

---

## Auth0 문제해결

### 콜백 URL 불일치

Auth0의 오류 페이지에 수신된 URL이 표시됩니다. 해당 URL을 **Allowed Callback URLs**에 추가하고 항목이 쉼표로 구분되어 있는지 확인하세요.

### unauthorized_client

**Advanced Settings → Grant Types**에서 **Authorization Code**가 활성화되어 있지 않거나 애플리케이션 유형이 Regular Web Applications이 아닙니다.

### 성공적인 로그인 후 액세스 거부

테넌트의 Rule, Action 또는 Post-Login 트리거가 사용자를 거부하고 있습니다. **Actions → Flows → Login**을 확인하고 정확한 이유를 보여주는 **Monitoring → Logs**의 테넌트 로그를 확인하세요.

### Issuer 불일치

Discovery URL과 브라우저로 리디렉션된 도메인이 다릅니다 — 보통 표준 테넌트 도메인과 커스텀 도메인을 혼용한 경우입니다. 하나로 통일해서 사용하세요.

---

## 참고

- [Single Sign-On Overview](overview.md) — 구성 참조, 테스트 및 일반 문제해결
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
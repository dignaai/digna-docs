# Microsoft Entra ID로 SSO 설정

Microsoft Entra ID(이전 Azure Active Directory)는 완전한 OIDC 호환 공급자이므로 digna는 표준 discovery 엔드포인트를 통해 통합됩니다.

이 가이드는 **Entra ID 측**을 다룹니다: 애플리케이션 등록과 digna가 필요로 하는 네 가지 값을 수집하는 방법입니다. digna 측 — `dashboard_config.toml`, 테스트 및 문제해결 — 은 모든 공급자에 대해 동일하며 [싱글 사인온 개요](overview.md)에 설명되어 있습니다.

---

## 시작하기 전에

| 요구 사항 | 비고 |
|---|---|
| **Entra ID 역할** | Application Administrator, Cloud Application Administrator, 또는 Global Administrator |
| **digna 리디렉트 URI** | 로그인 후 사용자가 돌아올 URL, 예: `https://digna.yourdomain.com/oidc/callback` |
| **테넌트** | 사용자가 로그인하는 디렉터리 |

---

## 1단계: 애플리케이션 등록

1. [Microsoft Entra 관리 센터](https://entra.microsoft.com)에 로그인합니다.
2. **Identity → Applications → App registrations**로 이동합니다.
3. **New registration**을 클릭합니다.
4. 구성:
   - **Name**: `digna` (동의 화면에 사용자에게 표시됨)
   - **Supported account types**: 단일 테넌트 배포의 경우 *Accounts in this organizational directory only*
5. **Redirect URI**에서 플랫폼 **Web**을 선택하고 digna 콜백 URL을 입력합니다:

```
https://digna.yourdomain.com/oidc/callback
```

6. **Register**를 클릭합니다.

!!! warning "중요"

    플랫폼은 **Web**이어야 하며 *Single-page application*이 아닙니다. digna는 백엔드에서 클라이언트 시크릿을 사용해 인증 코드를 교환하므로 SPA 플랫폼 유형은 이를 허용하지 않습니다.

---

## 2단계: 클라이언트 및 테넌트 ID 수집

애플리케이션의 **Overview** 페이지에서 다음을 복사합니다:

- **Application (client) ID** → `DIGNA_OIDC_CLIENT_ID`가 됩니다
- **Directory (tenant) ID** → discovery URL에 사용됩니다

---

## 3단계: 클라이언트 시크릿 생성

1. **Certificates & secrets → Client secrets**로 이동합니다.
2. **New client secret**를 클릭합니다.
3. 설명을 입력하고 만료 기간을 선택합니다.
4. **Add**를 클릭합니다.
5. 즉시 **Value** 열을 복사합니다.

!!! warning "Value를 복사하세요, Secret ID를 복사하지 마세요"

    **Value**는 이 페이지에서 한 번만 표시되며 이후에는 조회할 수 없습니다. 옆에 표시되는 **Secret ID**는 비슷하게 보이지만 실제 시크릿이 아닙니다 — 그것을 사용하면 로그인 시 `invalid_client` 오류가 발생합니다. 복사하기 전에 페이지를 벗어났다면 해당 시크릿을 삭제하고 새로 만드세요.

!!! tip "팁"

    Entra ID는 시크릿 수명을 최대 24개월로 제한하므로 모든 SSO 통합에는 만료일이 있습니다. 만료된 시크릿은 로그인 페이지에 경고 없이 모든 사용자의 SSO를 중단시키므로, 눈에 띄는 곳에 만료일을 기록해 두세요.

---

## 4단계: API 권한 확인

1. **API permissions**로 이동합니다.
2. **Microsoft Graph → User.Read**(delegated)가 있는지 확인합니다 — 기본으로 추가됩니다.

digna가 요청하는 `openid`, `profile`, `email` 스코프는 표준 OIDC 집합의 일부이므로 별도의 권한 부여가 필요 없습니다. 테넌트가 모든 애플리케이션에 대해 관리자 동의를 요구하면 **Grant admin consent for &lt;tenant&gt;**를 클릭하세요.

---

## 5단계: Discovery URL 작성

2단계에서 얻은 **Directory (tenant) ID**를 대체합니다:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "v2.0 엔드포인트 사용"

    `/v2.0/` 세그먼트는 중요합니다. `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration`의 v1.0 엔드포인트는 오래된 형식의 토큰을 발급하며 digna가 기대하는 표준 OIDC 클레임을 반환하지 않습니다.

계속하기 전에 브라우저에서 URL을 열어 보세요. JSON 문서가 표시되면 테넌트 ID가 올바른 것입니다.

---

## 6단계: digna 구성

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

두 파일의 `key`는 일치해야 합니다 — 여기서는 `microsoft`입니다.

---

## 7단계: 테스트

백엔드와 웹 서버를 재시작한 다음 대시보드를 엽니다. 전체 점검 목록은 [로그인 테스트](overview.md#testing-login)를 참조하세요.

---

## Entra ID 문제해결

### AADSTS50011: Redirect URI 불일치

`DIGNA_OIDC_REDIRECT_URI`에 있는 URI가 1단계에서 등록한 것과 다릅니다. Entra ID는 전체 문자열을 비교하므로 슬래시 유무, `http`와 `https`, 포트 차이 모두 불일치로 간주됩니다. **Authentication → Web → Redirect URIs**를 확인하세요.

### AADSTS7000215: 잘못된 클라이언트 시크릿

**Secret ID**를 복사했거나 시크릿이 만료되었습니다. 새 시크릿을 생성하고 Value 열을 복사하세요.

### AADSTS650057: Invalid Resource

애플리케이션 등록이 삭제되었거나 discovery URL의 테넌트와 다른 테넌트에 속해 있습니다. Overview 페이지에서 Directory (tenant) ID를 확인하세요.

### 사용자는 로그인되지만 아무 일도 발생하지 않음

테넌트가 관리자 동의를 요구하는데 동의가 부여되지 않았다면 리다이렉트가 사용 가능한 토큰 없이 돌아옵니다. **API permissions**에서 관리자 동의를 부여하세요.

---

## 관련 문서

- [싱글 사인온 개요](overview.md) — 구성 참조, 테스트 및 일반 문제해결
- [Microsoft: OAuth 2.0 권한 부여 코드 흐름](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
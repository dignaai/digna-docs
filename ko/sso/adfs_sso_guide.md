# AD FS로 SSO 설정

Active Directory Federation Services는 온프레미스 옵션입니다: 자체 서버가 토큰을 발급하며 discovery URL은 자체 호스트 이름입니다. AD FS는 **Windows Server 2016**부터 OpenID Connect를 지원합니다.

이 가이드는 **AD FS 쪽**을 다룹니다: 애플리케이션 그룹을 생성하고 digna가 필요로 하는 값을 수집하는 방법입니다. digna 쪽 — `dashboard_config.toml`, 테스트 및 문제해결 — 은 모든 프로바이더에 대해 동일하며 [Single Sign-On 개요](overview.md)에 설명되어 있습니다.

---

## 시작하기 전에

| Requirement | Notes |
|---|---|
| **AD FS version** | Windows Server 2016 이상 — 이전 버전은 OIDC를 지원하지 않음 |
| **Access** | AD FS 서버의 로컬 관리자 권한 |
| **Federation service name** | 예: `adfs.yourdomain.com` |
| **digna redirect URI** | 로그인 후 사용자가 돌아갈 URL, 예: `https://digna.yourdomain.com/oidc/callback` |

---

## 1단계: 애플리케이션 그룹 생성

1. AD FS 서버에서 **AD FS Management**를 엽니다.
2. **Application Groups**를 우클릭하고 **Add Application Group**을 선택합니다.
3. 이름에 `digna`를 입력합니다.
4. 버전에 따라 **Standalone applications** 또는 **Client-Server applications** 아래에서 **Server application accessing a web API**를 선택합니다.
5. **Next**를 클릭합니다.

---

## 2단계: 서버 애플리케이션 구성

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS가 GUID를 생성합니다. 이를 복사하세요 — 이 값이 `DIGNA_OIDC_CLIENT_ID`가 됩니다.
3. **Redirect URI**: digna 콜백 URL을 입력하고 **Add**를 클릭합니다:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Next**를 클릭합니다.

!!! warning "추가(Add) 버튼을 클릭하세요 — Next만 누르지 마세요"

    Redirect URI 필드에는 자체 **Add** 버튼이 있습니다. URI를 입력하고 **Next**만 누르면 해당 URI가 버려지며 마법자가 경고를 하지 않습니다. 계속하기 전에 필드 아래 목록에 URI가 표시되는지 확인하세요.

---

## 3단계: 공유 비밀 생성

1. **Generate a shared secret**에 체크합니다.
2. 생성된 시크릿을 복사합니다 → 이것이 `DIGNA_OIDC_CLIENT_SECRET`가 됩니다.
3. **Next**를 클릭합니다.

!!! warning "시크릿은 한 번만 표시됩니다"

    AD FS는 이 마법자 페이지에서만 공유 비밀을 표시하며 다시 볼 수 없습니다. 분실한 경우 애플리케이션 그룹 속성에서 나중에 재설정하세요.

---

## 4단계: Web API 구성

1. **Identifier**: 2단계에서 사용한 동일한 클라이언트 식별자를 입력하고 **Add**를 클릭합니다.
2. **Next**를 클릭합니다.
3. **Access Control Policy**를 선택합니다 — *Permit everyone*이 시작하기에 가장 간단합니다; 실사용 환경에서는 그룹으로 제한하세요.
4. **Next**를 클릭합니다.

---

## 5단계: 허용된 스코프 부여

**Configure Application Permissions** 단계에서 다음을 체크하세요:

- `openid`
- `profile`
- `email`

그런 다음 **Next**를 클릭하고 마법자를 완료합니다.

!!! warning "openid가 기본으로 선택되어 있지 않습니다"

    일부 버전의 AD FS는 `user_impersonation`만 기본 선택합니다. `openid`가 없으면 토큰 엔드포인트는 ID 토큰 대신 OAuth 액세스 토큰을 반환하므로 digna는 사용자를 식별할 수 없습니다.

---

## 6단계: Discovery 엔드포인트 확인

페더레이션 서비스 이름을 대체하세요:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

예:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

브라우저에서 열어보세요. JSON 문서가 OIDC가 활성화되어 있고 호스트 이름이 올바른지 확인해 줍니다.

!!! note "백엔드는 인증서 신뢰 필요"

    내부 인증 기관을 사용하는 경우가 AD FS에서 흔합니다. digna 백엔드를 실행하는 머신이 이 URL에 대해 자체적으로 아웃바운드 HTTPS 호출을 하므로, 발급 CA는 해당 머신의 신뢰 저장소에 있어야 합니다 — 로그인하는 사람들의 브라우저에만 있는 것으로는 충분하지 않습니다.

---

## 7단계: digna 구성

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Active Directory로 로그인"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

두 파일의 `key`는 일치해야 합니다 — 여기서는 `adfs`입니다.

---

## 8단계: 테스트

백엔드와 웹 서버를 재시작한 다음 대시보드를 엽니다. 전체 체크리스트는 [로그인 테스트](overview.md#testing-login)를 참조하세요.

---

## AD FS 문제해결

### MSIS9611: The Client Is Not Allowed to Access the Resource

4단계에서 웹 API 식별자가 클라이언트 식별자와 일치하지 않거나 5단계에서 스코프가 부여되지 않았습니다. 둘 다 애플리케이션 그룹 속성에서 편집할 수 있습니다.

### MSIS9602: Invalid redirect_uri

URI를 입력했지만 **Add** 버튼으로 추가하지 않았거나 `DIGNA_OIDC_REDIRECT_URI`와 다릅니다. **Application Groups → digna → digna backend → Properties**를 확인하세요.

### ID 토큰이 반환되지 않음

애플리케이션 권한에 `openid` 스코프가 없습니다.

### 백엔드가 Discovery URL에 접근하지 못함

백엔드 호스트의 DNS가 페더레이션 서비스 이름을 해석하지 못하거나 AD FS 인증서가 신뢰되지 않습니다. digna 서버 자체에서 `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration`로 테스트하세요.

### 확인할 이벤트

AD FS 서버는 Event Viewer의 **Applications and Services Logs → AD FS → Admin**에 실패 로그를 기록하며, 브라우저에 표시되는 것보다 더 구체적인 이유가 있는 경우가 많습니다.

---

## 참고

- [Single Sign-On 개요](overview.md) — 구성 참조, 테스트 및 일반 문제해결
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
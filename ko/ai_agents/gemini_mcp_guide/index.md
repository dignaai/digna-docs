# Gemini를 digna에 연결

이 가이드는 Google의 Gemini 도구를 **digna MCP Server**에 연결하는 방법을 설명합니다.
[AI 에이전트 개요](overview.md)에 설명된 대로 *digna* 설치의 MCP 엔드포인트와 API 키가 필요합니다.

예시에서는 엔드포인트로 `https://digna.example.com/mcp`를 사용합니다. 사용자의 엔드포인트로 바꾸세요.

## 도구 선택 {: #choose-your-tool }

| 도구 | 대상 | 구성 |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE 및 앱 | Google의 에이전트 도구. 2026년 6월부터 개인 Google 계정에서는 Antigravity CLI가 Gemini CLI를 대체했습니다 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard 및 Enterprise 라이선스, 유료 Gemini API 키 | `settings.json` 또는 `gemini mcp add` |
| Gemini Enterprise 앱 | — | 지원되지 않습니다. 이 앱의 사용자 지정 MCP 커넥터는 OAuth 또는 Google Cloud 서비스 계정으로 로그인하지만, digna MCP Server는 API 키로 인증합니다 |

이 도구들은 모두 자신이 실행되는 컴퓨터에서 연결하므로, 그 컴퓨터가 엔드포인트에 접근할 수 있다면 회사
네트워크 내부의 *digna*와도 작동합니다.

---

## Antigravity {: #antigravity }

Antigravity는 CLI, IDE, 앱이 함께 사용하는 `mcp_config.json`에서 MCP 서버를 읽습니다.

### 1. mcp_config.json 열기 {: #1-open-mcp-config-json }

| 범위 | 파일 |
|---|---|
| 모든 프로젝트 | `~/.gemini/config/mcp_config.json` |
| 하나의 작업 공간 | 작업 공간의 `.agents/mcp_config.json` |

사용 중인 파일을 여는 방법:

- **CLI**: `/mcp`를 입력하고 ++enter++를 눌러 MCP 관리자를 엽니다.
- **IDE**: 에이전트 사이드 패널에서 **…** 메뉴를 열고 **MCP Servers**를 선택한 다음 **Manage MCP Servers**,
  **View raw config**를 차례로 선택합니다.
- **앱**: **Customizations** > **Installed** > **MCP Servers**로 이동하여 **Copy Config File Path**를
  사용합니다.

### 2. digna 서버 추가 {: #2-add-the-digna-server }

`digna` 항목을 추가합니다. 파일에 이미 `mcpServers` 섹션이 있다면 그 안에 추가하세요:

```json
{
  "mcpServers": {
    "digna": {
      "serverUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

Antigravity는 원격 서버에 streamable HTTP로만 연결하며, digna MCP Server도 이 방식을 사용합니다.
엔드포인트는 `serverUrl`로 작성하세요. Gemini CLI의 `httpUrl` 키는 지원되지 않습니다.

### 3. 연결 확인 {: #3-verify-the-connection }

CLI에서 `/mcp`를 입력하면 MCP 관리자에 `digna` 서버의 상태와 도구가 표시되며, 구성을 다시 불러오거나 연결
로그를 볼 수도 있습니다. IDE에서는 서버가 **Manage MCP Servers** 아래에 표시됩니다.

!!! warning "파일 보호"

    `mcp_config.json`에는 API 키가 평문으로 저장됩니다. 작업 공간의 `.agents/mcp_config.json`은 버전 관리에서
    제외하고, 전역 파일은 본인 계정만 읽을 수 있도록 하세요.

---

## Gemini CLI {: #gemini-cli }

### 1. 서버 추가 {: #1-add-the-server }

API 키를 환경 변수에 넣은 다음 서버를 추가합니다:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

명령을 실행할 때 셸이 `$DIGNA_API_KEY`를 채워 넣으므로, Gemini CLI는 키를 자체 설정에 저장합니다.
`--scope user`를 지정하지 않으면 서버는 현재 프로젝트에만 추가됩니다.

### 2. 또는 settings.json 편집 {: #2-or-edit-settings-json }

위 명령은 `settings.json`에 기록합니다. 파일을 직접 편집하려면:

| 범위 | 파일 |
|---|---|
| 모든 프로젝트 | `~/.gemini/settings.json` |
| 하나의 프로젝트 | 프로젝트의 `.gemini/settings.json` |

```json
{
  "mcpServers": {
    "digna": {
      "httpUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

streamable HTTP용 키인 `httpUrl`을 사용하세요. 비슷한 `url` 키는 이전 SSE 전송 방식을 선택하는데, digna MCP
Server는 이를 제공하지 않습니다. 서버 이름에는 밑줄을 사용하지 마세요.

!!! tip "trust는 꺼 두세요"

    서버에 `"trust": true`가 설정되어 있지 않으면 Gemini CLI는 도구를 호출할 때마다 확인을 요청합니다.
    *digna*에 대해서는 `trust`를 꺼 두어, 에이전트가 구성에 가하는 모든 변경을 직접 확인하세요.

### 3. 연결 확인 {: #3-verify-the-connection-gemini-cli }

셸에서 다음을 실행합니다:

```bash
gemini mcp list
```

`digna` 서버가 연결됨으로 표시되어야 합니다. Gemini CLI 세션 안에서는 `/mcp`를 실행하면 서버와 그 도구를 볼
수 있습니다.

---

## Gemini 문제 해결 {: #troubleshooting-gemini }

### 서버가 연결 끊김으로 표시됨

- 엔드포인트가 `/mcp`로 끝나고 사용자의 컴퓨터에서 접근 가능한지 확인하세요.
- 키 이름을 확인하세요. Antigravity에서는 `serverUrl`, Gemini CLI에서는 `httpUrl`입니다.
- `401`은 키가 거부되었다는 뜻입니다. [401 Unauthorized](overview.md#troubleshooting)를 참조하세요.

### 내 계정에서 Gemini CLI가 더 이상 시작되지 않음

2026년 6월부터 개인 Google 계정은 Gemini CLI 대신 Antigravity CLI를 사용합니다. [Antigravity](#antigravity)에
설명된 대로 `digna` 항목을 `mcp_config.json`으로 옮기고, `httpUrl`을 `serverUrl`로 바꾸세요.

---

## 함께 보기 {: #see-also }

- [AI 에이전트 개요](overview.md): 엔드포인트, API 키, 보안 및 일반적인 문제 해결
- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop 또는 사용자 지정 커넥터 연결
- [digna Agentic](../platform/agentic/Introduction.md): AI 에이전트가 *digna*로 할 수 있는 일
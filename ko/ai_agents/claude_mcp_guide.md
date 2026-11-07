# Claude를 digna에 연결

이 가이드는 Claude를 **digna MCP Server**에 연결하는 방법을 설명합니다. [AI 에이전트 개요](overview.md)에
설명된 대로 *digna* 설치의 MCP 엔드포인트와 API 키가 필요합니다.

예시에서는 엔드포인트로 `https://digna.example.com/mcp`를 사용합니다. 사용자의 엔드포인트로 바꾸세요.

## 연결 방법 선택 {: #choose-how-to-connect }

| Claude 제품 | 연결 위치 | 네트워크 내부의 *digna*와 사용 가능 |
|---|---|---|
| [Claude Code](#claude-code) | 사용자의 컴퓨터 | 예 |
| [로컬 브리지를 사용하는 Claude Desktop](#claude-desktop-with-a-local-bridge) | 사용자의 컴퓨터 | 예 |
| claude.ai, Claude Desktop, Claude 모바일의 [사용자 지정 커넥터](#custom-connector) | Anthropic의 클라우드 | 아니요. 엔드포인트가 인터넷에서 접근 가능해야 합니다 |

회사 네트워크 내부에서 실행되는 *digna* 설치에는 Claude Code 또는 로컬 브리지를 사용하는 Claude Desktop을
사용하세요.

---

## Claude Code {: #claude-code }

### 1. 서버 추가 {: #1-add-the-server }

API 키를 환경 변수에 넣은 다음 서버를 추가합니다:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

명령을 실행할 때 셸이 `$DIGNA_API_KEY`를 채워 넣으므로, Claude Code는 키를 자체 구성에 저장합니다.

`--scope`는 서버를 사용할 수 있는 범위를 정합니다:

| 범위 | 사용 가능 대상 |
|---|---|
| `local` (기본값) | 사용자 본인, 현재 프로젝트에서만 |
| `user` | 사용자 본인, 모든 프로젝트에서 |
| `project` | 프로젝트의 `.mcp.json` 파일을 통해 프로젝트에서 작업하는 모든 사람 |

### 2. 팀과 서버 공유(선택 사항) {: #2-share-the-server-with-your-team }

프로젝트의 모든 사람에게 같은 서버를 제공하려면 프로젝트 루트에 `.mcp.json` 파일을 추가합니다. 파일에 키를
쓰지 마세요. Claude Code가 각 사용자의 환경에서 `${DIGNA_API_KEY}`를 채워 넣습니다:

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${DIGNA_API_KEY}"
      }
    }
  }
}
```

각 사용자는 `DIGNA_API_KEY`를 자신의 키로 설정합니다. Claude Code는 이 파일을 처음 발견하면 그 안의 서버를
사용할지 묻습니다.

### 3. 연결 확인 {: #3-verify-the-connection }

셸에서 다음을 실행합니다:

```bash
claude mcp list
```

`digna` 서버에 `✔ Connected`가 표시되어야 합니다. Claude Code 세션 안에서는 `/mcp`를 실행하면 서버와 그
도구를 볼 수 있습니다.

---

## 로컬 브리지를 사용하는 Claude Desktop {: #claude-desktop-with-a-local-bridge }

Claude Desktop의 구성 파일은 사용자의 컴퓨터에서 로컬 MCP 서버를 시작합니다. 오픈 소스 패키지인
[`mcp-remote`](https://github.com/geelen/mcp-remote)라는 작은 브리지가 그곳에서 실행되며, 모든 요청을 API
키와 함께 *digna* 엔드포인트로 전달합니다. 브리지가 사용자의 컴퓨터에서 실행되므로 회사 네트워크 내부의
*digna*와도 작동합니다.

!!! note "커뮤니티 패키지"

    `mcp-remote`는 Anthropic이나 digna가 아니라 오픈 소스 커뮤니티가 관리합니다. 사용하기 전에 조직에서
    허용하는지 확인하세요.

### 1. Node.js 설치 {: #1-install-nodejs }

브리지에는 [Node.js](https://nodejs.org) 18 이상이 필요합니다. Claude Desktop은 시스템에 설치된 Node.js
버전을 사용합니다. 다음 명령으로 확인하세요:

```bash
node --version
```

### 2. 구성 파일 편집 {: #2-edit-the-configuration-file }

`claude_desktop_config.json`을 엽니다:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

`digna` 서버를 추가합니다. 파일에 이미 `mcpServers` 섹션이 있다면 그 안에 `digna` 항목을 추가하세요:

```json
{
  "mcpServers": {
    "digna": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://digna.example.com/mcp",
        "--transport",
        "http-only",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer <api key>"
      }
    }
  }
}
```

!!! warning "헤더를 표시된 그대로 유지하세요"

    `Authorization:${AUTH_HEADER}`는 공백 없이 쓰고, `Bearer <api key>`는 `env`에 넣으세요. Windows용
    Claude Desktop은 `args` 안의 공백을 이스케이프하지 않으므로, 그곳에 공백이 있으면 헤더가 깨집니다.

### 3. Claude Desktop 다시 시작 {: #3-restart-claude-desktop }

Claude Desktop을 완전히 종료한 다음 다시 시작합니다. 새 채팅에서 **+**를 클릭하고 **Connectors**를 엽니다.
`digna`가 목록에 있고 켜져 있어야 합니다.

---

## 사용자 지정 커넥터 {: #custom-connector }

사용자 지정 커넥터를 사용하면 로컬 설정 없이 claude.ai, Claude Desktop, Claude 모바일 앱에서 *digna*를
사용할 수 있습니다. Anthropic의 클라우드가 엔드포인트에 연결하므로, 다음 조건을 만족할 때만 작동합니다:

- *digna* 엔드포인트가 인터넷에서 HTTPS로 접근 가능해야 합니다
- Claude 조직의 **Add custom connector** 대화 상자에 **Request headers** 옵션이 있어야 합니다. Anthropic은
  이 옵션을 일부 조직에만 베타로 제공합니다

!!! warning "네트워크 내부의 digna에는 사용할 수 없음"

    사설 네트워크 내부의 서버에 접근하는 Claude의 MCP 터널은 MCP 서버에 OAuth를 요구합니다. digna MCP
    Server는 API 키로 인증하므로 터널을 사용할 수 없습니다. 대신 [Claude Code](#claude-code) 또는
    [로컬 브리지를 사용하는 Claude Desktop](#claude-desktop-with-a-local-bridge)을 사용하세요.

### 1. 커넥터 설정 열기 {: #1-open-the-connector-settings }

- **Free, Pro, Max, Ultra 플랜**: **Customize > Connectors**로 이동하여 **Add custom connector**를
  클릭합니다.
- **Team, Enterprise 플랜**: Owner가 **Organization settings > Connectors**로 이동하여 **Add**를 클릭한 다음
  **Custom**을 클릭하고, 유형을 묻는 경우 **Web**을 선택합니다.

### 2. 커넥터 정보 입력 {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: 헤더 이름으로 `authorization`을 선택하고, 값으로 `Bearer`라는 단어와 공백을 포함하여
   `Bearer <api key>`를 입력한 뒤 **Required**로 표시합니다.
4. **Add**를 클릭합니다.

!!! warning "모든 사람이 키를 공유합니다"

    커넥터를 사용하는 모든 구성원은 같은 API 키로, 즉 같은 *digna* 사용자로 작업합니다. 커넥터 전용 *digna*
    사용자를 만들고, 모든 사람에게 허용되는 프로젝트와 역할(예: reader 역할)만 부여하세요.

Team 및 Enterprise 플랜에서는 이후 구성원이 **Customize > Connectors**에서 연결하며, 이 커넥터에는
**Custom** 레이블이 붙습니다.

Claude에서는 기존 커넥터의 헤더를 변경할 수 없습니다. 새 키를 사용하려면 커넥터를 제거한 뒤 다시 추가하세요.

---

## Claude 문제 해결 {: #troubleshooting-claude }

### claude mcp list에 Failed to connect가 표시됨

`claude mcp get digna`를 실행하여 원인을 확인하세요. `401`은 키가 거부되었다는 뜻입니다.
[401 Unauthorized](overview.md#troubleshooting)를 참조하세요. Claude Code는 키를 복사할 때 자주 함께 들어가는
키 앞뒤의 공백이나 줄바꿈에 대해서도 경고합니다.

### Claude Desktop에 digna가 표시되지 않음

- Node.js 18 이상이 설치되어 있는지 확인하세요: `node --version`.
- `claude_desktop_config.json`이 유효한 JSON인지 확인하세요. 쉼표 하나만 빠져도 파일의 모든 서버가 로드되지
  않습니다.
- 창만 닫지 말고 Claude Desktop을 완전히 종료한 다음 다시 시작하세요.

### 사용자 지정 커넥터가 서버에 접근할 수 없음

Anthropic의 클라우드가 엔드포인트에 접근할 수 없습니다. 엔드포인트가 유효한 인증서와 함께 인터넷에서 HTTPS로
접근 가능한지 확인하거나, 대신 [Claude Code](#claude-code)를 통해 연결하세요.

---

## 함께 보기 {: #see-also }

- [AI 에이전트 개요](overview.md): 엔드포인트, API 키, 보안 및 일반적인 문제 해결
- [Gemini](gemini_mcp_guide.md): Antigravity 또는 Gemini CLI 연결
- [digna Agentic](../platform/agentic/Introduction.md): AI 에이전트가 *digna*로 할 수 있는 일
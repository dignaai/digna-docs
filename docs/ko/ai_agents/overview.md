---
title: AI 에이전트 – MCP 통합 개요 | digna 문서
description: digna MCP Server를 통해 Claude, Gemini 및 기타 AI 에이전트를 digna에 연결합니다. MCP 엔드포인트를 찾고, API 키를 만들고, 라이선스와 네트워크 요구사항을 확인한 뒤 사용하는 AI 클라이언트에 맞는 가이드를 선택하세요.
image: /assets/logo_square.png
keywords: digna MCP server, Model Context Protocol, AI 에이전트 연결, Claude MCP, Gemini MCP, Antigravity MCP, digna API 키, digna Agentic
---

# AI 에이전트를 digna에 연결

**digna MCP Server**를 사용하면 AI 에이전트가 Claude, Gemini 및 여러 AI 도구가 지원하는 개방형 표준인
[Model Context Protocol](https://modelcontextprotocol.io)(MCP)을 통해 *digna*와 함께 작업할 수 있습니다.
*digna*에 연결된 에이전트는 데이터에 관한 질문에 답하고, 알림을 조사하고, *digna* 구성을 도울 수 있습니다.
에이전트가 할 수 있는 일은 [digna Agentic](../platform/agentic/Introduction.md)을 참조하세요.

이 페이지는 모든 AI 클라이언트에 공통인 *digna* 쪽 설정을 다룹니다. 각 클라이언트 가이드는 그 값을 어디에
입력하는지 보여 줍니다:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop 및 사용자 지정 커넥터
- [Gemini](gemini_mcp_guide.md): Antigravity 및 Gemini CLI

!!! info "베타"

    digna Agentic과 그에 포함된 digna MCP Server는
    [Release 2026.11](../changelog/Release_202611.md)에서 베타 버전으로 제공됩니다.

---

## 시작하기 전에 {: #before-you-start }

필요한 항목:

- *digna* Release 2026.11 이상
- **digna Agentic**이 포함된 라이선스. 이 라이선스가 없으면 MCP 서버는 모든 요청을 거부합니다
- *digna* 사용자 계정. 에이전트는 각 프로젝트에서 이 사용자의 권한으로 작업합니다.
  [Permissions](../platform/agentic/how_it_works.md#permissions)를 참조하세요
- **streamable HTTP**로 원격 MCP 서버에 연결하고 `Authorization` 헤더를 보낼 수 있는 AI 클라이언트

---

## 1. MCP 엔드포인트 찾기 {: #1-find-the-mcp-endpoint }

MCP 서버는 *digna* 백엔드의 일부이므로 별도로 설치하거나 시작할 것이 없습니다. 엔드포인트는 백엔드 주소
뒤에 `/mcp`를 붙인 것입니다:

```text
https://digna.example.com/mcp
```

예를 들어 `digna serve --address 0.0.0.0 --port 8082`로 백엔드를 호스트와 포트에서 직접 실행하는 경우,
엔드포인트는 그 주소에 `/mcp`를 붙인 것입니다:

```text
http://digna-host:8082/mcp
```

백엔드 앞에 리버스 프록시가 있다면, 프록시는 `/mcp`를 `Authorization` 헤더와 함께 백엔드로 전달해야
합니다.

!!! warning "네트워크에서는 HTTPS 사용"

    모든 요청에는 API 키가 포함됩니다. AI 클라이언트와 *digna*가 같은 컴퓨터에 있지 않다면 항상 HTTPS를
    사용하세요.

### 연결이 시작되는 위치 {: #where-the-connection-comes-from }

대부분의 AI 클라이언트는 자신이 실행되는 컴퓨터에서 연결합니다. Claude Code, 로컬 브리지를 사용하는
Claude Desktop, Antigravity, Gemini CLI가 여기에 해당합니다. 이 경우 *digna*는 해당 컴퓨터에서만 접근할
수 있으면 됩니다. 예를 들어 회사 네트워크 내부에서 접근할 수 있으면 충분합니다.

Claude의 **사용자 지정 커넥터**는 다릅니다. Anthropic의 클라우드가 엔드포인트에 연결합니다. 따라서
엔드포인트가 인터넷에서 HTTPS로 접근 가능할 때만 작동합니다. 네트워크 내부에서만 접근할 수 있는 *digna*
설치에는 사용자의 컴퓨터에서 실행되는 클라이언트를 사용하세요.

---

## 2. API 키 만들기 {: #2-create-an-api-key }

AI 클라이언트는 *digna* 사용자의 API 키로 인증합니다.

1. *digna*에 로그인합니다.
2. 왼쪽 아래에서 사용자 프로필을 엽니다.
3. **API Keys**를 클릭한 다음 **Add API Key**를 클릭합니다.
4. 키의 용도를 알 수 있는 이름(예: *Claude Code – Marcin*)을 입력하고 만료 시점을 선택합니다.
5. 키를 복사합니다. 키는 한 번만 표시됩니다.

MCP 서버로 보내는 모든 요청은 다음 헤더에 키를 담아 보냅니다:

```text
Authorization: Bearer <api key>
```

`Bearer`라는 단어와 그 뒤의 공백도 헤더 값의 일부입니다.

---

## 3. AI 클라이언트 연결 {: #3-connect-your-ai-client }

| AI 클라이언트 | 연결 위치 | 가이드 |
|---|---|---|
| Claude Code | 사용자의 컴퓨터 | [Claude](claude_mcp_guide.md#claude-code) |
| 로컬 브리지를 사용하는 Claude Desktop | 사용자의 컴퓨터 | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude 사용자 지정 커넥터(claude.ai, Claude Desktop, Claude 모바일) | Anthropic의 클라우드 | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE 및 앱 | 사용자의 컴퓨터 | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | 사용자의 컴퓨터 | [Gemini](gemini_mcp_guide.md#gemini-cli) |

사용자 지정 헤더와 함께 streamable HTTP로 원격 서버를 지원하는 다른 MCP 클라이언트도 사용할 수 있습니다.
대부분은 아래와 같은 구성을 읽습니다. 정확한 파일 이름과 키 이름은 사용하는 클라이언트의 문서를
확인하세요:

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

---

## 4. 사용해 보기 {: #4-try-it }

*digna*만 답할 수 있는 질문을 에이전트에게 해 보세요:

- *"내 digna 프로젝트 목록을 보여 줘."*
- *"프로젝트 X에서 오늘 녹색이 아닌 데이터 소스는 무엇이야?"*
- *"데이터 소스 Y에서 가장 최근에 실패한 검사를 설명해 줘."*

에이전트가 프로젝트 목록을 보여 주면 연결이 정상적으로 작동하는 것입니다.

---

## 보안 {: #security }

- **사람과 클라이언트마다 키 하나.** 그러면 다른 사람에게 영향을 주지 않고 **Delete API Key**로 키 하나만
  취소할 수 있습니다.
- **사용자를 신중하게 선택하세요.** 에이전트는 키 소유 사용자가 할 수 있는 모든 작업을 할 수 있습니다.
  데이터 조사만 할 때는 프로젝트에서 reader 역할을 가진 사용자를 사용하세요.
- **키를 공유 파일에 두지 마세요.** 키가 들어 있는 구성 파일은 커밋하지 마세요. 클라이언트가 지원한다면
  환경 변수에서 키를 읽도록 하세요.
- **만료를 설정하세요.** 이전 키가 만료되기 전에 새 키를 만들고 클라이언트를 업데이트하세요.
- **도구 호출을 검토하세요.** 적어도 구성을 변경하는 호출에 대해서는 클라이언트의 도구 호출 확인 기능을
  켜 두세요.

---

## 문제 해결 {: #troubleshooting }

### 401 Unauthorized

응답에 원인이 표시됩니다:

| 메시지 | 원인 |
|---|---|
| `Missing or malformed Authorization header` | 헤더가 전송되지 않았거나 값이 `Bearer `로 시작하지 않습니다 |
| `Invalid API key` | 키가 잘못되었거나 삭제되었습니다 |
| `API key expired` | 키가 만료되었습니다. 새 키를 만드세요 |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

*digna* 라이선스에 digna Agentic 항목이 없거나 해당 항목이 만료되었습니다. digna 팀에 digna Agentic이
포함된 라이선스를 요청하고, 운영 체제별 설치 가이드에 설명된 대로 설치하세요.

### 모든 요청이 잘못된 라이선스 오류로 실패함

*digna* 라이선스 자체가 만료되었습니다. 새 라이선스가 설치될 때까지 MCP 서버는 대시보드와 함께 응답을
멈춥니다.

### 에이전트가 읽기는 되지만 구성을 변경할 수 없음

API 키의 사용자가 해당 프로젝트에서 editor 역할을 가지고 있지 않습니다. editor 역할을 가진 사용자의 키를
사용하거나 프로젝트 관리자에게 역할 변경을 요청하세요.

### 클라이언트가 전혀 연결되지 않음

연결하는 컴퓨터가 엔드포인트에 접근할 수 없습니다. 해당 컴퓨터에서 엔드포인트 주소를 열어 보고 방화벽,
프록시, 인증서를 확인하세요. Claude 사용자 지정 커넥터의 경우 그 컴퓨터는 Anthropic의 클라우드에
있습니다. [연결이 시작되는 위치](#where-the-connection-comes-from)를 참조하세요.

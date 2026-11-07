# AI エージェントを digna に接続する

**digna MCP Server** を使うと、AI エージェントが [Model Context Protocol](https://modelcontextprotocol.io)
(MCP) を通じて *digna* を操作できます。MCP は Claude、Gemini をはじめ多くの AI ツールがサポートする
オープン標準です。*digna* に接続したエージェントは、データに関する質問に答えたり、アラートを調査したり、
*digna* の設定を手伝ったりできます。エージェントにできることについては
[digna Agentic](../platform/agentic/Introduction.md) を参照してください。

このページでは、すべての AI クライアントで共通の *digna* 側の設定を説明します。各クライアントのガイドでは、
その設定をどこに入力するかを説明します。

- [Claude](claude_mcp_guide.md): Claude Code、Claude Desktop、カスタムコネクタ
- [Gemini](gemini_mcp_guide.md): Antigravity と Gemini CLI

!!! info "ベータ版"

    digna Agentic と、それに含まれる digna MCP Server は、
    [Release 2026.11](../changelog/Release_202611.md) でベータ版として提供されています。

---

## はじめる前に {: #before-you-start }

必要なもの:

- *digna* Release 2026.11 以降
- **digna Agentic** を含むライセンス。これがない場合、MCP サーバーはすべてのリクエストを拒否します
- *digna* のユーザーアカウント。エージェントは各プロジェクトでそのユーザーの権限で動作します。
  [権限](../platform/agentic/how_it_works.md#permissions) を参照してください
- **streamable HTTP** でリモート MCP サーバーに接続でき、`Authorization` ヘッダーを送信できる
  AI クライアント

---

## 1. MCP エンドポイントを確認する {: #1-find-the-mcp-endpoint }

MCP サーバーは *digna* バックエンドの一部なので、追加でインストールや起動を行う必要はありません。
エンドポイントは、バックエンドのアドレスの後ろに `/mcp` を付けたものです。

```text
https://digna.example.com/mcp
```

たとえば `digna serve --address 0.0.0.0 --port 8082` のように、バックエンドがホストとポートで直接
動作している場合、エンドポイントはそのアドレスに `/mcp` を付けたものです。

```text
http://digna-host:8082/mcp
```

バックエンドの前段にリバースプロキシがある場合は、`/mcp` を `Authorization` ヘッダーとともに
バックエンドへ転送する必要があります。

!!! warning "ネットワーク上では HTTPS を使用する"

    すべてのリクエストには API キーが含まれます。AI クライアントと *digna* が同じマシン上にない場合は、
    必ず HTTPS を使用してください。

### 接続元について {: #where-the-connection-comes-from }

ほとんどの AI クライアントは、それが動作しているマシンから接続します。Claude Code、ローカルブリッジを
使う Claude Desktop、Antigravity、Gemini CLI がこれに当たります。これらの場合、*digna* はそのマシンから
到達できれば十分で、たとえば社内ネットワーク内にあっても構いません。

Claude の **カスタムコネクタ** は異なります。エンドポイントに接続するのは Anthropic のクラウドです。
そのため、エンドポイントにインターネットから HTTPS で到達できる場合にのみ動作します。社内ネットワーク内
からしか到達できない *digna* のインストール環境では、お使いのマシン上で動作するクライアントを使用して
ください。

---

## 2. API キーを作成する {: #2-create-an-api-key }

AI クライアントは、*digna* ユーザーの API キーで認証します。

1. *digna* にログインします。
2. 左下のユーザープロファイルを開きます。
3. **API Keys** をクリックし、続いて **Add API Key** をクリックします。
4. キーの用途がわかる名前 (例: *Claude Code – Marcin*) を入力し、有効期限を選択します。
5. キーをコピーします。キーが表示されるのは一度だけです。

MCP サーバーへのすべてのリクエストは、次のヘッダーでキーを送信します。

```text
Authorization: Bearer <api key>
```

`Bearer` という語とその後のスペースも、ヘッダー値の一部です。

---

## 3. AI クライアントを接続する {: #3-connect-your-ai-client }

| AI クライアント | 接続元 | ガイド |
|---|---|---|
| Claude Code | お使いのマシン | [Claude](claude_mcp_guide.md#claude-code) |
| ローカルブリッジを使う Claude Desktop | お使いのマシン | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude のカスタムコネクタ (claude.ai、Claude Desktop、Claude mobile) | Anthropic のクラウド | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI、IDE、アプリ | お使いのマシン | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | お使いのマシン | [Gemini](gemini_mcp_guide.md#gemini-cli) |

その他の MCP クライアントも、カスタムヘッダー付きの streamable HTTP によるリモートサーバーをサポート
していれば動作します。多くのクライアントは次のような設定を読み込みます。正確なファイル名とキー名は、
お使いのクライアントのドキュメントで確認してください。

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

## 4. 試してみる {: #4-try-it }

*digna* でなければ答えられない質問をエージェントにしてみましょう。

- *「digna のプロジェクトを一覧表示して。」*
- *「プロジェクト X のデータソースのうち、今日グリーンでないものはどれ?」*
- *「データソース Y の直近の失敗したチェックについて説明して。」*

エージェントがプロジェクトを一覧表示すれば、接続は成功しています。

---

## セキュリティ {: #security }

- **1 人・1 クライアントにつき 1 つのキー。** そうすれば、**Delete API Key** で 1 つのキーだけを
  失効させても、他の人には影響しません。
- **ユーザーは慎重に選ぶ。** エージェントは、キーのユーザーができることをすべて実行できます。データの
  調査だけが目的なら、プロジェクトで閲覧者ロールを持つユーザーを使用してください。
- **キーを共有ファイルに入れない。** キーを含む設定ファイルをコミットしないでください。クライアントが
  対応している場合は、環境変数からキーを読み込んでください。
- **有効期限を設定する。** 古いキーの有効期限が切れる前に新しいキーを作成し、クライアントを更新して
  ください。
- **ツール呼び出しを確認する。** 少なくとも設定を変更する呼び出しについては、クライアントのツール
  呼び出し確認を有効のままにしてください。

---

## トラブルシューティング {: #troubleshooting }

### 401 Unauthorized

レスポンスに理由が示されます。

| メッセージ | 原因 |
|---|---|
| `Missing or malformed Authorization header` | ヘッダーが送信されていないか、値が `Bearer ` で始まっていません |
| `Invalid API key` | キーが間違っているか、削除されています |
| `API key expired` | キーの有効期限が切れています。新しいキーを作成してください |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

*digna* のライセンスに digna Agentic のエントリがないか、そのエントリの有効期限が切れています。
digna チームに digna Agentic を含むライセンスを依頼し、お使いのオペレーティングシステム向けの
インストールガイドに従ってインストールしてください。

### すべてのリクエストが無効なライセンスのエラーで失敗する

*digna* のライセンス自体の有効期限が切れています。新しいライセンスがインストールされるまで、MCP サーバーは
ダッシュボードとともに応答を停止します。

### エージェントが設定を読み取れるが変更できない

API キーのユーザーが、そのプロジェクトで編集者ロールを持っていません。編集者ロールを持つユーザーのキーを
使用するか、プロジェクト管理者にロールの変更を依頼してください。

### クライアントがまったく接続できない

接続するマシンからエンドポイントに到達できません。そのマシンからエンドポイントのアドレスを開き、
ファイアウォール、プロキシ、証明書を確認してください。Claude のカスタムコネクタの場合、そのマシンは
Anthropic のクラウド上にあります。[接続元について](#where-the-connection-comes-from) を参照してください。
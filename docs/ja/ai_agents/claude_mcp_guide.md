---
title: Claude – MCP で Claude を digna に接続する | digna ドキュメント
description: digna MCP Server を通じて Claude を digna に接続します — コマンドラインまたは共有の .mcp.json による Claude Code、ローカルブリッジを使う Claude Desktop、claude.ai のカスタムコネクタを、Authorization ヘッダーの API キーで設定します。
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai カスタムコネクタ, digna MCP server, mcp-remote, Authorization Bearer, digna API キー
---

# Claude を digna に接続する

このガイドでは、Claude を **digna MCP Server** に接続します。[AI エージェントの概要](overview.md) で
説明しているとおり、*digna* インストール環境の MCP エンドポイントと API キーが必要です。

例ではエンドポイントとして `https://digna.example.com/mcp` を使用しています。実際のエンドポイントに
置き換えてください。

## 接続方法を選ぶ {: #choose-how-to-connect }

| Claude 製品 | 接続元 | 社内ネットワーク内の *digna* で動作するか |
|---|---|---|
| [Claude Code](#claude-code) | お使いのマシン | はい |
| [ローカルブリッジを使う Claude Desktop](#claude-desktop-with-a-local-bridge) | お使いのマシン | はい |
| claude.ai、Claude Desktop、Claude mobile の [カスタムコネクタ](#custom-connector) | Anthropic のクラウド | いいえ。エンドポイントにインターネットから到達できる必要があります |

社内ネットワーク内で動作する *digna* のインストール環境では、Claude Code またはローカルブリッジを使う
Claude Desktop を使用してください。

---

## Claude Code {: #claude-code }

### 1. サーバーを追加する {: #1-add-the-server }

API キーを環境変数に設定してから、サーバーを追加します。

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

コマンドの実行時にシェルが `$DIGNA_API_KEY` を展開するため、Claude Code はキーを自身の設定に保存します。

`--scope` は、サーバーを利用できる範囲を決めます。

| スコープ | 利用できる範囲 |
|---|---|
| `local` (デフォルト) | 自分のみ、現在のプロジェクトのみ |
| `user` | 自分のみ、すべてのプロジェクト |
| `project` | プロジェクト内の `.mcp.json` ファイルを通じて、そのプロジェクトで作業する全員 |

### 2. サーバーをチームと共有する (任意) {: #2-share-the-server-with-your-team }

プロジェクトの全員に同じサーバーを提供するには、プロジェクトのルートに `.mcp.json` ファイルを追加します。
キーはファイルに書き込まないでください。Claude Code は各自の環境から `${DIGNA_API_KEY}` を展開します。

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

各自が `DIGNA_API_KEY` に自分のキーを設定します。Claude Code はこのファイルを初めて検出したときに、
その中のサーバーを使用するかどうかを確認します。

### 3. 接続を確認する {: #3-verify-the-connection }

シェルから次を実行します。

```bash
claude mcp list
```

`digna` サーバーに `✔ Connected` と表示される必要があります。Claude Code のセッション内では、`/mcp` を
実行するとサーバーとそのツールを確認できます。

---

## ローカルブリッジを使う Claude Desktop {: #claude-desktop-with-a-local-bridge }

Claude Desktop の設定ファイルは、お使いのマシン上でローカル MCP サーバーを起動します。小さなブリッジである
オープンソースの [`mcp-remote`](https://github.com/geelen/mcp-remote) パッケージがそこで動作し、すべての
リクエストを API キーとともに *digna* のエンドポイントへ転送します。ブリッジはお使いのマシン上で動作する
ため、社内ネットワーク内の *digna* でも使用できます。

!!! note "コミュニティのパッケージ"

    `mcp-remote` は Anthropic や digna ではなく、オープンソースコミュニティによって保守されています。
    使用する前に、組織で利用が許可されているか確認してください。

### 1. Node.js をインストールする {: #1-install-nodejs }

ブリッジには [Node.js](https://nodejs.org) 18 以降が必要です。Claude Desktop はシステムにインストール
されている Node.js のバージョンを使用します。次のコマンドで確認してください。

```bash
node --version
```

### 2. 設定ファイルを編集する {: #2-edit-the-configuration-file }

`claude_desktop_config.json` を開きます。

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

`digna` サーバーを追加します。ファイルにすでに `mcpServers` セクションがある場合は、そこに `digna` の
エントリを追加します。

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

!!! warning "ヘッダーは示したとおりに記述する"

    `Authorization:${AUTH_HEADER}` はスペースを入れずに記述し、`Bearer <api key>` は `env` に記述します。
    Windows 版 Claude Desktop は `args` 内のスペースをエスケープしないため、そこにスペースがあるとヘッダーが
    壊れます。

### 3. Claude Desktop を再起動する {: #3-restart-claude-desktop }

Claude Desktop を完全に終了してから、再度起動します。新しいチャットで **+** をクリックし、**Connectors** を
開きます。`digna` が一覧に表示され、オンになっている必要があります。

---

## カスタムコネクタ {: #custom-connector }

カスタムコネクタを使うと、ローカルでの設定なしに claude.ai、Claude Desktop、Claude モバイルアプリで
*digna* を利用できます。エンドポイントに接続するのは Anthropic のクラウドなので、次の条件を満たす場合に
のみ動作します。

- *digna* のエンドポイントにインターネットから HTTPS で到達できる
- お使いの Claude 組織の **Add custom connector** ダイアログに **Request headers** オプションがある。
  Anthropic はこれを一部の組織にベータとして提供しています

!!! warning "社内ネットワーク内の digna には使えない"

    プライベートネットワーク内のサーバーに到達する Claude の MCP トンネルでは、MCP サーバー側で OAuth が
    必要です。digna MCP Server は API キーで認証するため、トンネルは使用できません。代わりに
    [Claude Code](#claude-code) または [ローカルブリッジを使う Claude Desktop](#claude-desktop-with-a-local-bridge) を使用してください。

### 1. コネクタの設定を開く {: #1-open-the-connector-settings }

- **Free、Pro、Max、Ultra プラン**: **Customize > Connectors** に移動し、**Add custom connector** を
  クリックします。
- **Team および Enterprise プラン**: Owner が **Organization settings > Connectors** に移動し、**Add**、
  続いて **Custom** をクリックし、種類を尋ねられた場合は **Web** を選択します。

### 2. コネクタの詳細を入力する {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: ヘッダー名として `authorization` を選び、値として `Bearer <api key>` を
   `Bearer` という語とスペースを含めて入力し、**Required** にチェックを入れます。
4. **Add** をクリックします。

!!! warning "全員が同じキーを共有する"

    コネクタを使用するメンバーは全員同じ API キーで、つまり同じ *digna* ユーザーとして作業します。
    コネクタ専用の *digna* ユーザーを作成し、全員に許可してよいプロジェクトとロール (例: 閲覧者ロール)
    だけを付与してください。

Team および Enterprise プランでは、その後メンバーが **Customize > Connectors** で接続します。そこでは
コネクタに **Custom** ラベルが付いています。

Claude では既存のコネクタのヘッダーを変更できません。新しいキーを使うには、コネクタを削除してから
追加し直してください。

---

## Claude のトラブルシューティング {: #troubleshooting-claude }

### claude mcp list に Failed to connect と表示される

`claude mcp get digna` を実行して原因を確認します。`401` はキーが拒否されたことを意味します。
[401 Unauthorized](overview.md#troubleshooting) を参照してください。Claude Code は、キーの先頭や末尾に
あるスペースや改行についても警告します。これらはコピー時によく紛れ込みます。

### Claude Desktop に digna が表示されない

- Node.js 18 以降がインストールされているか確認します: `node --version`。
- `claude_desktop_config.json` が有効な JSON か確認します。カンマが 1 つ欠けているだけで、ファイル内の
  すべてのサーバーが読み込まれなくなります。
- ウィンドウを閉じるだけでなく Claude Desktop を完全に終了し、再度起動します。

### カスタムコネクタがサーバーに到達できない

Anthropic のクラウドからエンドポイントに到達できません。有効な証明書を使った HTTPS でインターネットから
到達できるか確認するか、代わりに [Claude Code](#claude-code) で接続してください。

---

## 関連項目 {: #see-also }

- [AI エージェントの概要](overview.md): エンドポイント、API キー、セキュリティ、一般的なトラブルシューティング
- [Gemini](gemini_mcp_guide.md): Antigravity または Gemini CLI の接続
- [digna Agentic](../platform/agentic/Introduction.md): AI エージェントが *digna* でできること

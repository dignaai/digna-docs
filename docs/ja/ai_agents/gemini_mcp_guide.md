---
title: Gemini – MCP で Antigravity と Gemini CLI を digna に接続する | digna ドキュメント
description: digna MCP Server を通じて Google の Gemini ツールを digna に接続します — mcp_config.json による Antigravity CLI、IDE、アプリと、settings.json または gemini mcp add による Gemini CLI を、Authorization ヘッダーの API キーで設定します。
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, digna API キー
---

# Gemini を digna に接続する

このガイドでは、Google の Gemini ツールを **digna MCP Server** に接続します。
[AI エージェントの概要](overview.md) で説明しているとおり、*digna* インストール環境の MCP エンドポイントと
API キーが必要です。

例ではエンドポイントとして `https://digna.example.com/mcp` を使用しています。実際のエンドポイントに
置き換えてください。

## ツールを選ぶ {: #choose-your-tool }

| ツール | 対象 | 設定 |
|---|---|---|
| [Antigravity](#antigravity) CLI、IDE、アプリ | Google のエージェントツール。2026 年 6 月に、個人の Google アカウント向けには Antigravity CLI が Gemini CLI に取って代わりました | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard および Enterprise ライセンス、有料の Gemini API キー | `settings.json` または `gemini mcp add` |
| Gemini Enterprise アプリ | — | サポートされていません。そのカスタム MCP コネクタは OAuth または Google Cloud サービスアカウントでサインインしますが、digna MCP Server は API キーで認証します |

これらのツールはすべて、それが動作しているマシンから接続します。そのため、そのマシンからエンドポイントに
到達できる限り、社内ネットワーク内の *digna* でも動作します。

---

## Antigravity {: #antigravity }

Antigravity は、CLI、IDE、アプリで共有される `mcp_config.json` から MCP サーバーを読み込みます。

### 1. mcp_config.json を開く {: #1-open-mcp-config-json }

| スコープ | ファイル |
|---|---|
| すべてのプロジェクト | `~/.gemini/config/mcp_config.json` |
| 1 つのワークスペース | ワークスペース内の `.agents/mcp_config.json` |

使用中のファイルを開くには:

- **CLI**: `/mcp` と入力して ++enter++ を押し、MCP マネージャーを開きます。
- **IDE**: エージェントのサイドパネルで **…** メニューを開き、**MCP Servers**、**Manage MCP Servers**、
  **View raw config** の順に選択します。
- **アプリ**: **Customizations** > **Installed** > **MCP Servers** に移動し、**Copy Config File Path** を
  使用します。

### 2. digna サーバーを追加する {: #2-add-the-digna-server }

`digna` のエントリを追加します。ファイルにすでに `mcpServers` セクションがある場合は、そこに追加します。

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

Antigravity はリモートサーバーに streamable HTTP でのみ接続します。digna MCP Server が使用するのも
streamable HTTP です。エンドポイントは `serverUrl` として記述してください。Gemini CLI の `httpUrl` キーは
サポートされていません。

### 3. 接続を確認する {: #3-verify-the-connection }

CLI で `/mcp` と入力します。MCP マネージャーに `digna` サーバーがその状態とツールとともに表示され、
設定の再読み込みや接続ログの表示もできます。IDE では、サーバーは **Manage MCP Servers** に表示されます。

!!! warning "ファイルを保護する"

    `mcp_config.json` には API キーが平文で保存されます。ワークスペースの `.agents/mcp_config.json` は
    バージョン管理に含めず、グローバルファイルは自分のアカウントだけが読み取れるようにしてください。

---

## Gemini CLI {: #gemini-cli }

### 1. サーバーを追加する {: #1-add-the-server }

API キーを環境変数に設定してから、サーバーを追加します。

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

コマンドの実行時にシェルが `$DIGNA_API_KEY` を展開するため、Gemini CLI はキーを自身の設定に保存します。
`--scope user` を指定しない場合、サーバーは現在のプロジェクトにのみ追加されます。

### 2. または settings.json を編集する {: #2-or-edit-settings-json }

上記のコマンドは `settings.json` に書き込みます。ファイルを自分で編集するには:

| スコープ | ファイル |
|---|---|
| すべてのプロジェクト | `~/.gemini/settings.json` |
| 1 つのプロジェクト | プロジェクト内の `.gemini/settings.json` |

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

streamable HTTP 用のキーである `httpUrl` を使用してください。似た名前の `url` キーは古い SSE
トランスポートを選択しますが、digna MCP Server は SSE を提供していません。サーバー名にアンダースコアを
使用しないでください。

!!! tip "trust はオフのままにする"

    サーバーに `"trust": true` が設定されていない限り、Gemini CLI はツール呼び出しのたびに確認を求めます。
    *digna* では `trust` をオフのままにして、エージェントが設定に加える変更をすべて確認できるように
    してください。

### 3. 接続を確認する {: #3-verify-the-connection-gemini-cli }

シェルから次を実行します。

```bash
gemini mcp list
```

`digna` サーバーが接続済みと表示される必要があります。Gemini CLI のセッション内では、`/mcp` を実行すると
サーバーとそのツールを確認できます。

---

## Gemini のトラブルシューティング {: #troubleshooting-gemini }

### サーバーが切断状態と表示される

- エンドポイントが `/mcp` で終わり、お使いのマシンから到達できるか確認します。
- キー名を確認します: Antigravity では `serverUrl`、Gemini CLI では `httpUrl` です。
- `401` はキーが拒否されたことを意味します。[401 Unauthorized](overview.md#troubleshooting) を参照してください。

### 自分のアカウントで Gemini CLI が起動しなくなった

2026 年 6 月以降、個人の Google アカウントでは Gemini CLI の代わりに Antigravity CLI を使用します。
[Antigravity](#antigravity) の説明に従って `digna` のエントリを `mcp_config.json` に移し、`httpUrl` を
`serverUrl` に名前変更してください。

---

## 関連項目 {: #see-also }

- [AI エージェントの概要](overview.md): エンドポイント、API キー、セキュリティ、一般的なトラブルシューティング
- [Claude](claude_mcp_guide.md): Claude Code、Claude Desktop、カスタムコネクタの接続
- [digna Agentic](../platform/agentic/Introduction.md): AI エージェントが *digna* でできること

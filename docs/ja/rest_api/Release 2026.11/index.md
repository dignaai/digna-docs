---
title: REST API の概要 2026.11 | digna ドキュメント
description: digna REST API v1 を使って、プロジェクトとインスペクション結果の読み取り、データソース・データセット・属性の管理、インスペクションの開始を行います。ベース URL、API キー認証、件数の上限、エラー、OpenAPI ドキュメントについて説明します。
image: /assets/logo_square.png
keywords: digna REST API, digna API, digna OpenAPI, digna API キー, インスペクションリクエスト API, データ品質 API, Swagger UI
---

# digna REST API 2026.11

*digna* REST API を使うと、独自のツールやパイプラインから HTTP と JSON で *digna* を操作できます。
プロジェクトとインスペクション結果の読み取り、データソース・データセット・属性の管理、そしてデータロードの
完了時などにインスペクションを開始できます。[Python SDK](../../sdk/Release%202026.11/index.md)
も同じ API を使用しています。

このページでは、すべてのリクエストに共通する事項を説明します。各リソースのページには、エンドポイントごとに
パラメーター、リクエストボディ、レスポンス、スキーマが記載されています。

| リソース | エンドポイント |
|---|---|
| [Projects](projects.md) | プロジェクトの読み取り |
| [DB Connections](db_connections.md) | データベース接続の読み取り |
| [Data Sources](data_sources.md) | データソースの作成、読み取り、更新、削除 |
| [Data Sets](data_sets.md) | データセットの作成、読み取り、更新、削除 |
| [Attributes](attributes.md) | 属性の作成、読み取り、更新、削除 |
| [Check Definitions](check_definitions.md) | チェック定義の読み取り |
| [Inspection Requests](inspection_requests.md) | インスペクションの開始と進行状況の追跡 |
| [Inspection Statuses](inspection_statuses.md) | プロジェクト、データソース、データセットごとのインスペクション結果の読み取り |

---

## ベース URL {: #base-url }

この API は *digna* バックエンドの一部です。すべてのパスは、バックエンドのアドレスに続く `/v1` で始まります。

```text
https://digna.example.com/v1/projects
```

バックエンドのアドレスはダッシュボードが使用するものと同じで、`dashboard/dashboard_config.toml` の
`[api]` セクションにある `baseUrl` です。呼び出し元と *digna* が同じマシン上にない場合は、必ず HTTPS
を使用してください。すべてのリクエストに API キーが含まれるためです。

---

## 認証 {: #authentication }

すべてのリクエストは、*digna* ユーザーの API キーを `Authorization` ヘッダーで送信します。

```text
Authorization: Bearer <api key>
```

キーを作成するには、ダッシュボードの左下にあるユーザープロファイルを開き、**API Keys**、続いて
**Add API Key** をクリックして、キーをコピーします。キーが表示されるのは一度だけです。同じキーは
[digna MCP Server](../../ai_agents/overview.md) でも使用できます。

リクエストは、キーの所有ユーザーの権限で実行されます。作成、変更、削除にはそのプロジェクトでの編集者ロールが
必要です。ロールがない場合、リクエストは `403` とメッセージ
`You don't have permission to edit this project` で拒否されます。

!!! tip "自動化には専用ユーザーを使用する"

    統合ごとに *digna* ユーザーを作成し、必要なプロジェクトとロールだけを付与して、有効期限付きのキーを
    作成します。こうしておけば、キーを削除するだけで 1 つの統合のアクセスを取り消すことができ、
    他のユーザーには影響しません。

---

## リクエストの送信 {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

レスポンスは JSON です。リストは JSON 配列として返されます。リクエストボディも JSON で、
`Content-Type: application/json` を付けて送信します。

---

## 上限とフィルター {: #limits-and-filters }

リスト系のエンドポイントが返す項目は最大 `limit` 件です。既定値は 200 件、上限は 5000 件です。この範囲外の
値は `400` で拒否されます。オフセットやページトークンはないため、代わりにフィルターでリストを絞り込んで
ください。たとえば `project_id`、`data_source_id`、インスペクションステータスでは `start_date` と
`end_date` を使用します。

60 秒を超えるリクエストは `408 Request Timeout` でキャンセルされます。

---

## エラー {: #errors }

エラーレスポンスには、コードとメッセージを含む JSON ボディが付きます。

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| ステータス | コード | 意味 |
|---|---|---|
| `400` | `BAD_REQUEST` | リクエストが無効です (例: `limit` が範囲外) |
| `401` | `NOT_AUTHENTICATED` | API キーがない、形式が正しくない、不明、または期限切れです |
| `403` | `NOT_AUTHORIZED` | キーのユーザーに、このリクエストに必要なロールがありません |
| `403` | `INVALID_LICENSE` | *digna* のライセンスの有効期限が切れています |
| `404` | `NOT_FOUND` | プロジェクト、データソース、またはその他の項目が存在しません |
| `500` | `INTERNAL_ERROR` | *digna* で予期しないエラーが発生しました。詳細はバックエンドのログにあります |

`401` の `message` は、キーの何が問題かを示します。

| メッセージ | 原因 |
|---|---|
| `Missing Authorization header` | `Authorization` ヘッダーが送信されていません |
| `Invalid Authorization header format` | 値が `Bearer ` で始まっていません |
| `Invalid API key` | キーが間違っているか、削除されています |
| `API key expired` | キーの有効期限が切れています。新しいキーを作成してください |

---

## インスペクションの実行 {: #running-an-inspection }

一般的な統合では、データロードの完了時にインスペクションを開始し、その完了を待ってから結果を読み取ります。

1. [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request) で**インスペクションを開始します**。
   レスポンスにはリクエストの `id` が含まれます。
2. [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request) で**進行状況を追跡します**。
   `status` は `PENDING` から `RUNNING` を経て `COMPLETED` に進むか、`FAILED`、`ABORTED`、
   `CANCELLED` のいずれかで終了します。値が変わらなくなるまで、数秒ごとに問い合わせてください。
3. 検査した日付について [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses) で**結果を読み取ります**。
   各項目には全体の `status` として `0` (OK)、`1` (警告)、`2` (重大)、`-1` (ステータスなし) の
   いずれかがあり、さらにモジュールごとのステータスと、合格・不確定・不合格のチェック数が含まれます。

```bash
curl -X POST https://digna.example.com/v1/inspection-requests \
  -H "Authorization: Bearer $DIGNA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "project_id": 1,
    "include_all_data_sources": true,
    "data_source_ids": [],
    "start_date": "2026-11-06",
    "end_date": "2026-11-06",
    "mode": "DAILY",
    "weekly_mode_weekdays": [],
    "monthly_mode_days": [],
    "use_notification": true
  }'
```

---

## OpenAPI ドキュメント {: #openapi-document }

すべての *digna* インストールは、この API を OpenAPI 3.1 ドキュメントで記述しており、それに対して
リクエストを試せる対話型の Swagger UI も提供しています。

| 内容 | アドレス |
|---|---|
| OpenAPI ドキュメント | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Release 2026.11 のドキュメントはこちらからも入手できます: [openapi.json](openapi.json)。これを使って、
他の言語のクライアントを生成できます。

!!! note "対象は /v1 エンドポイントのみ"

    ダッシュボードは、これ以外の内部エンドポイントを通じてもバックエンドと通信します。それらはこの API
    には含まれず、どのリリースでも変更される可能性があるため、統合は `/v1` エンドポイントのみに基づいて
    構築してください。

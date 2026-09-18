---
title: digna Python SDK リファレンス 2026.06 | digna ドキュメント
description: digna Python SDK リリース 2026.06 の完全なリファレンス
image: /assets/logo_square.png
---

# digna Python SDK リファレンス 2026.06

このセクションでは ***digna*** の Python SDK について説明します。複数ページ構成のリファレンスになっており、まずこの概要でクライアントの全体像をつかみ、続いてクイックスタート、リソース、モデル、エラー、自動生成 API ドキュメントの各ページに進んでください。

SDK は `digna-sdk` パッケージとして公開され、***digna*** REST API 用の安定したバージョン管理されたクライアントを提供します。

---

## SDK の基本

---

### 概要

SDK はリソース指向のクライアント設計を採用しています。各 API 領域は最上位の `DignaClient` 上に独立したクライアントとして用意され、型付きのリクエスト／レスポンスモデルと一貫したエラー処理を備えています。

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### 主な機能

- **型付きモデル** — すべてのリクエストとレスポンスは pydantic で検証されるため、ネットワーク呼び出しの前にエディターと型チェッカーが誤りを検出します。
- **リソース指向** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests`、 `client.inspection_statuses` はいずれもシンプルな `list` / `get` / `create` / `update` / `delete` メソッドを提供します。
- **明確なエラー** — API エラーは暗黙的に `None` を返すのではなく、`DignaAPIError`（または `DignaAuthenticationError`、`DignaAuthorizationError`、`DignaNotFoundError` などのより具体的なサブクラス）を送出します。

### インストール

```bash
pip install digna-sdk
```

---

## リファレンスページ

このリリースは次のページで構成されています。

- [クイックスタート](quickstart.md) — 接続して最初の呼び出しを行う。
- [リソース](resources.md) — 利用可能なリソースクライアントの一覧。
- [モデル](models.md) — 入出力に使用される pydantic モデル。
- [エラー](errors.md) — 例外の階層。
- [API リファレンス](reference.md) — 自動生成されたリファレンスドキュメント。

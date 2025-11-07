---
title: Data Validation – ルールベースのチェック（コンプライアンスと監査対応） | digna ドキュメント
description: dignaのData Validationは、閾値、範囲、参照リストを用いた決定論的なルールベースチェックを強制します。金融・医療などの規制業界でのコンプライアンス、監査可能性、報告要件を確保します。
image: /assets/logo_square.png
keywords:
  - data validation
  - ルールベースのデータチェック
  - データ品質
  - データの質
  - data observability
  - 閾値と範囲
  - 参照リスト検証
  - 監査可能性
  - コンプライアンス監視
  - digna data validation
lang: ja
robots: index, follow
og_title: Data Validation – ルールベースのチェック（コンプライアンスと監査対応） | digna ドキュメント
og_description: dignaのData Validationは、閾値、範囲、参照リストを用いた決定論的なルールベースチェックを強制します。規制のある業界向けに設計され、コンプライアンス、透明性、監査可能性を確保します。
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – ルールベースのチェック
<h1 style="display:none;">AI駆動のData Validationモジュール：データ品質と可観測性のためのdigna</h1>

---

## 目的

**Data Validation** モジュールは、正確なルールベースのチェックを通じて**データ品質**を担保します。  
組織が決定論的なビジネスおよび技術的検証ロジックを定義できるようにし、データがコンプライアンス基準、契約上のSLA、および規制要件を満たしていることを保証します。

*データベース内でのルール実行*、*完全な監査トレイル*、および*他のdignaモジュールとの統合*を組み合わせることで、**Data Validation** は複雑なエンタープライズ環境全体で一貫性があり追跡可能な**データ品質と可観測性**を保証します。

---

## 技術概要

### サポートされる検証タイプ

- **等価チェック（Equality Checks）**  
  値が期待される結果と一致することを確認します（例：参照コード、ブールフラグ、カテゴリマッピング）。

- **閾値と範囲（Thresholds & Ranges）**  
  数値指標やKPIを定義済みの上限・下限（静的または動的に算出）に対して検証します。

- **参照リストとルックアップ（Reference Lists & Lookups）**  
  フィールド値が承認されたマスターデータセット内に存在するかを確認します（例：VATコード、ISO国リスト、製品カタログ）。

- **列間整合性（Cross-Column Consistency）**  
  関連性のある整合性を保証します（例：通貨が地域と一致しているか、リスクカテゴリが資産タイプと整合しているか）。

- **NULL処理ルール（Null Handling Rules）**  
  重要な列における予期しないNULLや空値を検出します。

### 実行とログ記録

- **データベース内処理** – すべての検証ルールはお使いのデータベース（Teradata、Snowflake、Databricks、PostgreSQL 等）内で直接実行されます。  
- **データ抽出なし** – digna は生データをお客様の環境外へ転送しません。  
- **完全な追跡可能性** – 各ルール結果はタイムスタンプ、対象データセット、レコード数、および合否結果とともにログ記録されます。  
- **監査**
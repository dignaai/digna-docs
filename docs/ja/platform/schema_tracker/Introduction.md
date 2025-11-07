---
title: Data Schema Tracker – スキーマの進化を監視 | digna Documentation
description: digna Data Schema Tracker がカラムの変更、データ型の更新、スキーマドリフトをどのように監視するかを学びます。ETL の失敗、ダッシュボードの破損、データ可観測性の喪失を防ぐために、意図的・非意図的なスキーマ変更の検出とアラートを行います。
canonical_url: https://docs.digna.ai/platform/data_schema_tracker/
image: /assets/logo_square.png
keywords:
  - データスキーマトラッカー
  - スキーマドリフト検出
  - スキーマ進化の監視
  - メタデータ可観測性
  - データ可観測性
  - データの品質
  - データ構造の監視
  - データベースメタデータ
  - ETL パイプラインの安定性
  - digna data schema tracker
lang: en
robots: index, follow
og_title: Data Schema Tracker – スキーマの進化を監視 | digna Documentation
og_description: digna Data Schema Tracker はスキーマドリフト、データ型の変更、カラムの更新を監視します。予期しない構造変更によって ETL パイプラインやダッシュボードが失敗する前にアラートを受け取れます。
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Monitor Schema Evolution
<h1 style="display:none;">AI駆動のメタデータ可観測性とデータ品質モジュール – digna Data Schema Tracker</h1>

---

## Purpose

The **Data Schema Tracker** はデータベース構造がどのように進化しているかを把握するためのツールです。  
継続的に **テーブルスキーマ、カラム、データ型** を監視し、パイプライン、ETL ジョブ、BI ダッシュボードに影響を与える可能性のある **スキーマドリフト**（意図的・非意図的な構造変更）を検出します。

スキーマの進化を透明化することで、digna は組織が **データ品質への信頼** を維持し、**データシステムの可観測性** を確保し、検知されないスキーマ変更による高額な本番インシデントを回避するのに役立ちます。

---

## Technical Overview

### What It Monitors

- **追加または削除されたカラム** – 新たに導入、リネーム、削除されたカラムを検出します。  
- **データ型の変更** – `INT → VARCHAR` や `DATE → TIMESTAMP` のような変更を特定します。  
- **テーブルおよびビューの変更** – 作成、リネーム、削除を追跡します。  
- **環境間の差異** – 開発（Dev）、テスト（Test）、本番（Production）環境間のスキーマバージョンを比較します。  

### Detection & Alerting

- データプラットフォーム内の **database metadata** または **system catalogs** を直接スキャンします。  
- 各スキーマスナップショットを digna の observability schema に保存されている以前のバージョンと比較します。  
- ダッシュボード上、API 経由、または外部通知チャネル（メール、Slack、Webhook）で **リアルタイムアラート** を生成します。  
- すべてのスキーマバージョンをログとして保存し、**履歴追跡と監査対応** を可能にします。

---

## Architecture and Execution

- **インデータベース実行:** digna は環境内で完全に動作し、ユーザーデータを抽出することなくメタデータビューをクエリします。  
- **軽量なスキャン:** 構造情報のみを参照し、ユーザーデータにはアクセスしません。  
- **集中管理ストレージ:** スキーマメタデータとドリフト記録は可視化と分析のために digna の observability schema に格納されます。  
- **自動化:** digna Core や外部オーケストレーションツールを介したスケジュールまたはイベントベースのスキャンをサポートします。  

---

## Example Use Cases

| Use Case | Description |
|-----------|--------------|
| **ETL Stability Monitoring** | スキーマ不一致によってパイプラインが失敗する前に上流の構造変更を検出します。 |
| **Business Intelligence Reliability** | リネームや欠損したカラムによってダッシュボードが壊れるのを防ぎます。 |
| **Data Warehouse Governance** | コンプライアンスやインパクト分析のためにスキーマ進化の監査可能な履歴を維持します。 |
| **Integration Oversight** | 構造更新後にデータレイクとデータウェアハウスのスキーマが同期されていることを確認します。 |

---

## Benefits

| Area | Benefit |
|------|----------|
| **Data Quality** | 検出されないスキーマドリフトがデータパイプラインを破損または無効化するのを防ぎます。 |
| **Observability** | データエコシステムの全体的な可観測性に構造監視を追加します。 |
| **Compliance** | 監査、トレーサビリティ、変更管理のためにバージョン化されたスキーマ履歴を維持します。 |
| **Prevention** | 構造上の問題が報告や本番エラーに波及する前に検出します。 |

---

## How It Works

1. **Snapshot Collection** – digna が現在のスキーマメタデータをキャプチャします。  
2. **Comparison** – 新しいスナップショットは比較され
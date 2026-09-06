---
title: digna CLI リファレンス 2026.06 – コマンドと例 | digna ドキュメント
description: digna CLI リリース 2026.06 の完全なリファレンス
image: /assets/logo_square.png
---

# digna CLI リファレンス 2026.06
**2026-09-05**

このページでは、***digna*** CLI リリース **2026.06** で利用できるコマンドの全体像を、使用例とオプションを含めて説明します。

実行ファイルの名前は `digna` です。

---

## CLI の基本

---

### 概要と構文

リリース **2026.06** の CLI は、カテゴリに基づく構造化されたコマンド階層を使用します。

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` と `serve` はサブコマンドを持たない単独のコマンドです。

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### グローバルオプション

以下のグローバルオプションはすべてのコマンドに適用されます。

- `--help`、`-h`: CLI 全体、または特定のコマンドカテゴリやサブコマンドのヘルプ情報を表示します。
- `--stacktrace`: 失敗時に、最上位のメッセージだけでなくエラーチェーン全体を表示します。

`--stacktrace` は厳密な意味でのグローバルオプションです。コマンドカテゴリの **前** に指定する必要があり、後ろに置くことはできません。

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

`--version` フラグはありません。代わりに [`version`](#version) コマンドを使用してください。

### 前提条件

ほとんどのコマンドは、読み取り可能で有効な `config.toml` を必要とします。一部のコマンドはさらに有効なライセンスを必要とします。
次の表は、各コマンドカテゴリが処理を始める前に読み込むものを示しています。

| コマンドカテゴリ | `config.toml` が必要 | 有効なライセンスが必要 |
|---|---|---|
| `version` | いいえ | いいえ |
| `config check` | いいえ（コマンドが報告する対象そのものです） | いいえ |
| `license check` | いいえ | それ *自体* が検査です |
| `crypt` | はい | いいえ |
| `serve` | はい | いいえ |
| `project` | はい | いいえ |
| `user` | はい | はい |
| `inspection` | はい | はい |
| `repo` | はい | はい |

ライセンスが必要な場合は、署名と有効期限の両方が検査され、いずれかが失敗するとコマンドはリポジトリに触れる前に中止されます。

### 終了コード

- `0`: コマンドは成功しました。
- `1`: コマンドは失敗しました。エラーメッセージは接頭辞 `Error: ` を付けて stderr に書き出されます。

### help

`--help` オプションは、利用可能なコマンドカテゴリ、サブコマンド、オプションに関する情報を提供します。

1. **全般的なヘルプの表示:**
   ```bash
   digna --help
   ```

2. **特定のカテゴリやコマンドのヘルプの取得:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **出力に含まれる内容:**
   - **コマンドの説明:** コマンドの目的の要約。
   - **構文:** 必須および任意の引数。
   - **オプション:** そのコマンド固有のフラグとパラメーター。

### version

`version` コマンドはインストールされている ***digna*** のリリースを出力します。構成を読み込まず、ライセンスの検証も行わないため、`config.toml` やライセンスが欠落していたり無効であったりするインストールでも動作します。

リリースのバージョンは、[`repo check`](#repo-check) が報告するリポジトリスキーマのバージョンとは独立しています。

#### コマンドの使い方
```bash
digna version
```

#### 出力例
```text
2026.06
```

---

## 構成管理

---

### config check

`config check` コマンドは構成ファイル（`config.toml`）を検証し、必須のセクションと設定がすべて存在し、正しく書式化されていることを確認します。各セクションは個別に検証されるため、壊れた `[app]` セクションが `[repo]` の状態を隠してしまうことはありません。

報告されるセクションは次のとおりです。

- `App config`（`[app]`）
- `Repository config`（`[repo]`）
- `Base config`（`[base]`）
- `Logging config`（`[logging]`）
- `Encryption config`（`[encryption]`）
- `OIDC config(s)`（`oidc_clients`）— 任意。キーが存在しない場合は合格し、存在するが不正な形式のリストは失敗します

このコマンドは他のコマンドのようには意図的にアプリケーション構成を読み込みません。そのため、***digna*** の起動そのものを妨げるような `config.toml` も診断できます。

#### コマンドの使い方
```bash
digna config check [OPTIONS]
```

#### オプション
- `--configpath`、`-c`: 構成ファイルへのパス、または `config.toml` を含むディレクトリへのパス（既定値は `./config.toml`）。
- `--json`: 検証レポートを JSON として出力します。`--quiet` より優先されます。
- `--quiet`、`-q`: レポートを抑制し、終了コードのみに依存します。

#### 例
```bash
digna config check
```

特定の構成ファイルを検証し、出力を JSON 形式にする場合:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### 出力例
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

ファイルが存在しない場合や TOML の構文エラーがある場合は、セクションごとに検証する対象が残らないため、`--quiet` や `--json` の指定にかかわらず、レポートではなく単一のエラーとして報告されます。

---

## リポジトリ管理

---

### repo check

`repo check` コマンドはデータベース接続をテストし、リポジトリのインストール状況とバージョンを確認します。構成されたスキーマが存在しない場合、または存在しても ***digna*** リポジトリが含まれていない場合は失敗します。

報告されるバージョンはリポジトリスキーマのバージョンであり、[`version`](#version) が出力する ***digna*** のリリースとは別に管理されています。

#### コマンドの使い方
```bash
digna repo check
```

#### 出力例
```text
Repo version 3.0.0 installed
```

### repo install

`repo install` コマンドは、`config.toml` で構成されたスキーマに新しい ***digna*** リポジトリをインストールし、必要なシーケンス、テーブル、インデックス、制約、初期レコードをすべて作成します。

スキーマ自体はこのコマンドでは作成 **されません** — 事前に存在している必要があります。また、そのスキーマにリポジトリが既にインストールされている場合、コマンドは実行を拒否し、インストール済みのバージョンが古い場合は [`repo upgrade`](#repo-upgrade) を案内します。

#### コマンドの使い方
```bash
digna repo install
```

#### 出力例
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

`repo upgrade` コマンドはデータベーススキーマのマイグレーションを適用し、既存のリポジトリをインストール済みリリースが想定するバージョンまで引き上げます。アップグレードは決められたアップグレード経路に沿って一度に 1 バージョンずつ適用され、完了した各段階はリポジトリに記録されます。

リポジトリが既に想定どおりのバージョンである場合、コマンドはアップグレードが不要である旨を報告し、変更を行いません。

#### コマンドの使い方
```bash
digna repo upgrade
```

#### 出力例
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## 暗号化管理

---

### crypt gen-key

`crypt gen-key` コマンドは、`config.toml` の暗号化キーとして使用するための新しい AES-GCM 暗号化キーを生成します。生成されるキー自体は `config.toml` に依存しませんが、読み込み可能な `config.toml` が既に存在している必要があります。

#### コマンドの使い方
```bash
digna crypt gen-key
```

#### 出力例
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

`crypt encrypt` コマンドは、`config.toml` で構成された AES-GCM キーを使用して文字列（データベースのパスワードなど）を暗号化し、暗号文を出力します。

#### コマンドの使い方
```bash
digna crypt encrypt <VALUE>
```

#### 引数
- **VALUE**: 暗号化する平文の文字列（必須）。

#### 例
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

`crypt decrypt` コマンドは、`config.toml` で構成されたキーを使用して AES-GCM で暗号化された文字列を復号し、平文を出力します。

#### コマンドの使い方
```bash
digna crypt decrypt <VALUE>
```

#### 引数
- **VALUE**: 復号する暗号文の文字列（必須）。

#### 例
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## ユーザー管理

---

### user add

`user add` コマンドは ***digna*** リポジトリに新しいユーザーアカウントを作成します。指定されたメールアドレスのユーザーが既に存在する場合、コマンドは失敗します。

#### コマンドの使い方
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### 引数
- **EMAIL**: ユーザーのメールアドレス（必須）。
- **PASSWORD**: ユーザーの初期パスワード（必須）。
- **DISPLAY_NAME**: ユーザーの完全な表示名（必須）。

#### オプション
- `--admin`、`-a`: 管理者（スーパーユーザー）権限を持つユーザーとして作成します。

#### 例
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

管理者アカウントを作成する場合:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### 出力例
```text
User created with ID: 42
```

### user list

`user list` コマンドは、登録済みのすべてのユーザーを、ID、メールアドレス、表示名、管理者フラグとともに表形式で一覧表示します。

#### コマンドの使い方
```bash
digna user list
```

#### 出力例
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

`user modify` コマンドは、メールアドレスで識別される既存のユーザーアカウントの表示名と管理者権限を更新します。

表示名と管理者フラグは常に両方とも書き込まれます。`--admin` は値ではなくスイッチです。**省略すると管理者権限が取り消される** ため、ユーザーが権限を維持または取得する必要がある場合は必ず指定してください。

#### コマンドの使い方
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### 引数
- **EMAIL**: 変更対象ユーザーのメールアドレス（必須）。
- **DISPLAY_NAME**: 更新後の表示名（必須）。

#### オプション
- `--admin`、`-a`: 管理者権限を付与します。取り消す場合は省略します。
- `--valid-until`、`-v`: 互換性のために受け付けられますが、**現在は適用されません**。指定すると警告が表示され、何も変更されません。

#### 例
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### 出力例
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

`user modify-pwd` コマンドは、既存のユーザーアカウントのパスワードを更新します。

#### コマンドの使い方
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### 引数
- **EMAIL**: パスワードを更新するユーザーのメールアドレス（必須）。
- **PASSWORD**: 新しいパスワード（必須）。

#### 例
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

`user delete` コマンドは、システムからユーザーアカウントを削除します。

#### コマンドの使い方
```bash
digna user delete <EMAIL>
```

#### 引数
- **EMAIL**: 削除するユーザーのメールアドレス（必須）。

#### 例
```bash
digna user delete jdoe@example.com
```

---

## プロジェクトとデータソースの管理

---

### project list

`project list` コマンドは、リポジトリ内で利用できるすべてのプロジェクトを、ID、名前、説明とともに一覧表示します。

#### コマンドの使い方
```bash
digna project list
```

#### 出力例
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

`project list-ds` コマンドは、指定したプロジェクトに関連付けられたすべてのデータソースを、ID、名前、種類、スキーマ、テーブル名とともに一覧表示します。

#### コマンドの使い方
```bash
digna project list-ds <PROJECT_NAME>
```

#### 引数
- **PROJECT_NAME**: データソースを一覧表示するプロジェクトの名前（必須）。名前は完全に一致している必要があります。

#### 例
```bash
digna project list-ds ProjectA
```

#### 出力例
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

`project export-ds` コマンドは、プロジェクトのデータソースを JSON ドキュメントにエクスポートします。

`--table-name` と `--table-id` のいずれも指定しない場合、プロジェクトのすべてのデータソースがエクスポートされます。

#### コマンドの使い方
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### 引数
- **PROJECT_NAME**: データソースのエクスポート元となるプロジェクトの名前（必須）。

#### オプション
- `--table-name`、`-n`: エクスポートするデータソースの名前。複数の名前をスペース区切りで指定できます。
- `--table-id`、`-i`: エクスポートするデータソースの ID。複数の ID をスペース区切りで指定できます。
- `--exportfile`、`-f`: エクスポートしたデータソースの保存先パス（既定値: `data_sources_export.json`）。

#### 例
`ProjectA` からすべてのデータソースをエクスポートする場合:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

特定のテーブルをエクスポートする場合:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### 出力例
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

`project import-ds` コマンドは、エクスポートファイルから対象プロジェクトへデータソースをインポートし、オブジェクトごとに作成・更新・スキップの結果を報告します。

#### コマンドの使い方
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### 引数
- **PROJECT_NAME**: インポート先となる対象プロジェクトの名前（必須）。
- **EXPORT_FILE**: JSON エクスポートファイルへのパス（必須）。

#### オプション
- `--output-file`、`-o`: インポートレポートの書き出し先ファイル。指定しない場合、レポートは stdout に出力されます。
- `--output-format`、`-f`: インポートレポートの形式 — `table`、`json`、`csv`（既定値: `table`）。

#### 例
```bash
digna project import-ds ProjectB my_export.json
```

機械可読なレポートを取得する場合:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

レポートは 4 つのオブジェクト階層 — データソース、データセット定義、属性、検証ルール — を対象とし、それぞれについてインポート操作、結果、生成されたオブジェクト ID、追加情報を示します。

### project plan-import-ds

`project plan-import-ds` コマンドは、対象プロジェクトへのデータソースのインポートをプレビューし、どのオブジェクトが作成・更新・スキップされるかを、何も変更せずに表示します。[`project import-ds`](#project-import-ds) と同じエクスポートファイルおよび同じレポートオプションを受け付け、計画された各オブジェクトにステップ番号を付与します。

#### コマンドの使い方
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### 引数
- **PROJECT_NAME**: 対象プロジェクトの名前（必須）。
- **EXPORT_FILE**: エクスポートファイルへのパス（必須）。

#### オプション
- `--output-file`、`-o`: インポート計画の書き出し先ファイル。指定しない場合、計画は stdout に出力されます。
- `--output-format`、`-f`: インポート計画の形式 — `table`、`json`、`csv`（既定値: `table`）。

#### 例
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## 検査管理

---

### inspection run

`inspection run` コマンドは、プロジェクトと日付範囲に対する検査リクエストを作成し、その後、指定されたオプションに応じて、完了を待機するか、直ちに制御を返すか、自プロセス内で実行します。

3 つの実行モードは次のとおりです。

- **既定（フラグなし）**: リクエストはバックエンド向けにキューへ入れられ、CLI は 2 秒ごとにポーリングしてタスクの進捗を出力し、検査が最終状態に達するまで続けます。実行中の `digna serve` が必要であり、それがないとリクエストを引き取るものがありません。
- **`--async-mode`**: リクエストはキューへ入れられ、その ID が直ちに出力されます。追跡には [`inspection status`](#inspection-status) を使用してください。
- **`--bypass-backend`**: 検査は CLI プロセス自身によって実行され、キューには入りません。そのため実行中のサーバーは不要です。

`--async-mode` と `--bypass-backend` は同時に指定できません。

いずれのモードでも、検査が正常に完了しなかった場合、コマンドは 0 以外の終了コードで終了します。

#### コマンドの使い方
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### 引数
- **PROJECT_NAME**: 対象プロジェクトの名前（必須）。名前は完全に一致している必要があります。
- **START_DATE**: 日付範囲の開始日。形式は `YYYY-MM-DD`（必須）。
- **END_DATE**: 日付範囲の終了日。形式は `YYYY-MM-DD`（必須）。

#### オプション
- `--table-name`: 検査をプロジェクト内の単一のデータソースに限定します。データソース名で指定します。指定しない場合、プロジェクトのすべてのデータソースが検査されます。
- `--async-mode`: 検査をキューに入れ、完了を待たずにリクエスト ID を出力します。`--bypass-backend` とは併用できません。
- `--bypass-backend`: バックエンド向けにキューへ入れる代わりに、CLI プロセス内で直接検査を実行します。`--async-mode` とは併用できません。

#### 例
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

非同期の検査を送信する場合:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

単一のデータソースを検査する場合:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### 出力例
既定モード:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

非同期モード:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

`inspection status` コマンドは、リクエスト ID を指定して検査リクエストの状態とタスクの進捗を照会します。

#### コマンドの使い方
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### 引数
- **INSPECTION_REQUEST_ID**: 検査リクエストの数値 ID（必須）。

#### 例
```bash
digna inspection status 1024
```

#### 出力例
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

`inspection abort` コマンドは、実行中または保留中の検査リクエストの取り消しを要求します。対象となる各リクエストについて停止イベントを記録し、それに基づいてバックエンドが動作します。したがって中止は即時終了ではなく、停止の要求です。

#### コマンドの使い方
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### 引数
- **INSPECTION_REQUEST_ID**: 中止する検査リクエストの ID。`--killall` を指定しない限り必須です。

#### オプション
- `--killall`: 現在実行中および保留中のすべての検査リクエストを中止します。同時に指定されたリクエスト ID より優先されます。

#### 例
特定のリクエストを中止する場合:
```bash
digna inspection abort 1024
```

実行中およびキュー内のすべての検査を中止する場合:
```bash
digna inspection abort --killall
```

#### 出力例
`--killall` は実行内容を報告します。単一のリクエストの中止は出力を生成せず、終了コードで成功を示します。
```text
All running and pending inspections have been aborted.
```

---

## ライセンス管理

---

### license check

`license check` コマンドは `license.toml` を検証し、インストールに同梱された公開鍵に対して署名を確認するとともに、有効期限が切れていないことを検査します。アプリケーション構成を読み込まないため、`config.toml` の設定前でも動作します。

#### コマンドの使い方
```bash
digna license check
```

#### 出力例
```text
License is valid
```

無効な署名と期限切れのライセンスは、いずれも終了コード 1 で、それぞれ別のエラーとして報告されます。

---

## サーバーとバックグラウンドサービス

---

### serve

`serve` コマンドは、***digna*** の REST API サーバーを、バックグラウンドの検査スケジューラおよび検査マネージャーとともに起動します。起動時には、リポジトリが依然として実行中として記録している検査をすべて失敗として扱います。以前のプロセスから残っているものはあり得ないためです。

コマンドは停止されるまでフォアグラウンドで実行されます。

#### コマンドの使い方
```bash
digna serve [OPTIONS]
```

#### オプション
- `--address`: API サーバーをバインドするネットワークアドレス（既定値: `127.0.0.1`）。
- `--port`: 待ち受けるポート番号（既定値: `8000`）。

#### 例
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### 出力例
```text
Server running on http://0.0.0.0:8000
```

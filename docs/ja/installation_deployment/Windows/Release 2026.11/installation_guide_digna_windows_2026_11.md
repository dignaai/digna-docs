---
title: Windows インストールガイド – digna リリース 2026.11 | digna ドキュメント
description: Windows に digna リリース 2026.11 をインストールするためのステップバイステップガイド — システム要件、PostgreSQL のセットアップ、Web サーバーの構成、バックエンドとダッシュボードの設定、digna を Windows サービスとして実行する方法、リリース 2026.06 からのアップグレード方法を含む
keywords: digna windows インストール, digna デプロイメント ガイド, digna backend セットアップ, digna dashboard インストール, postgresql セットアップ, digna windows サービス, digna アップグレード ガイド
image: /assets/logo_square.png
---

# Windows インストールガイド — digna リリース 2026.11

**リリース:** 2026.11

**最終更新日:** 2026年11月7日


---

## 目次

1. [導入](#introduction)
2. [システム要件](#system-requirements)
3. [事前準備](#pre-installation-setup)
4. [PostgreSQL サーバーのセットアップ](#postgresql-server-setup)
5. [Web サーバーの設定](#web-server-configuration)
6. [初期インストール](#initial-installation)
7. [バックエンドの設定](#backend-configuration)
8. [ダッシュボードの設定](#dashboard-configuration)
9. [digna を Windows サービスとして実行する](#running-digna-as-a-windows-service)
10. [新しいリリースへのアップグレード](#upgrading-to-a-new-release)

---

## 導入 {: #introduction }

### digna について

digna は、ウェアハウス、データレイク、レイクハウスなどさまざまなデータ環境におけるデータ品質管理を最適化するための包括的な AI 駆動プラットフォームです。高いスケーラビリティと適応性を備え、自動化、リアルタイム監視、および異常検知を通じて現代のデータ課題に対処します。

digna は主に次の2つのコンポーネントで構成されています。

- **digna**: アプリケーションの中核であり、データの処理と品質チェックの実行を担います。バックエンドとコマンドラインインターフェイスを単一の実行ファイルに統合し、以前のリリースで別々だった `dignabackend` と `dignacli` を置き換えます。
- **dignadashboard**: Web サーバー上でホストされる Web ベースのインターフェースで、digna プラットフォームと対話しデータ品質メトリクスを可視化するためのユーザーフレンドリーな手段を提供します。

### リリース 2026.11 の新機能

このリリースでは、digna Data Reconciliation、digna MCP Server を備えた digna Agentic、そして digna Engine が追加されました。digna Engine は digna の内部でデータをプロファイリングし、異なるデータベース技術間の参照整合性をチェックできます。詳細は[リリースノート](../../../changelog/Release_202611.md)を参照してください。

インストールに関しては、本リリースで新しいリポジトリのマイグレーション機構、digna Engine 用の `config.toml` のオプションの `[duckdb]` セクション、そして新しいライセンスファイルが導入されます。それぞれについては[アップグレードのセクション](#upgrading-to-a-new-release)で説明します。

### macOS や Linux をお探しですか？

本ガイドは Windows 向けです。他のプラットフォームについては、[macOS インストールガイド](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) や [Linux インストールガイド](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md) を参照してください。

---

## システム要件 {: #system-requirements }

インストールを始める前に、システムが以下の最小要件を満たしていることを確認してください。

| 要件 | 仕様 |
|---|---|
| **オペレーティングシステム** | Windows Server または Windows 10/11 |
| **メモリ（最小構成）** | 16 GB RAM |
| **ディスク容量** | 10 GB の空きストレージ |
| **データベース** | PostgreSQL Server 12 以上 |
| **Web サーバー** | IIS、Apache Tomcat、または同等のもの |

!!! info "digna Engine"

    プロファイリングの場所として digna Engine を使用するデータベース接続は、digna ホスト自体でプロファイリングされます。そのためのメモリとディスク容量を追加で見込んでください。参照: [\[duckdb\] セクション](#duckdb-section)。

### データベースのインストールオプション

**既に PostgreSQL がインストール済みの場合:**
既存の PostgreSQL サーバーに digna 用の新しいデータベースを追加できます。

**digna と同じマシンに PostgreSQL をインストールする場合:**

!!! info "推奨仕様"

    - **メモリ**: 32 GB RAM（16 GB の代わり）
    - **ディスク容量**: 50 GB の空きストレージ（10 GB の代わり）

    これらの高めの仕様は、digna と PostgreSQL データベースの両方を同時に稼働させるために推奨されます。

---

## 事前準備 {: #pre-installation-setup }

digna をインストールする前に、次の2つの重要な前提条件が整っていることを確認してください:

1. **PostgreSQL サーバー** — 計算済みメトリクスとパフォーマンスデータの保存用
2. **Web サーバー** — digna Dashboard のホスティング用

これらのコンポーネントがまだセットアップされていない場合は、以下のセクションに従ってインストールおよび構成してください。

---

## PostgreSQL サーバーのセットアップ {: #postgresql-server-setup }

### 既に PostgreSQL をお持ちの場合

PostgreSQL がローカルで動作しているか、リモートで管理された PostgreSQL サーバーを使用している場合は、[次のセクション](#web-server-configuration)に進んでください。

### PostgreSQL のインストール

Windows に PostgreSQL をインストールする手順は次の通りです。

#### ステップ 1: PostgreSQL をダウンロード

1. [PostgreSQL Downloads page](https://www.postgresql.org/download/) にアクセス
2. **Windows** を選択
3. 最新のインストーラーをダウンロード

#### ステップ 2: インストーラーを実行

1. ダウンロードしたインストーラーをダブルクリック
2. セットアップウィザードの指示に従う

#### ステップ 3: インストール先ディレクトリを選択

PostgreSQL をインストールするディレクトリを選択します。デフォルトの場所で問題ないことが多いです。

#### ステップ 4: コンポーネントの選択

標準的なセットアップでは、デフォルトのコンポーネントオプションのままで問題ありません。

#### ステップ 5: PostgreSQL スーパーユーザーのパスワード設定

PostgreSQL のスーパーユーザー（`postgres`）のパスワードを入力して確認します。**このパスワードは安全な場所に保管してください** — 後で必要になります。

#### ステップ 6: ポート番号の設定

デフォルトの PostgreSQL ポートは `5432` です。必要に応じてデフォルトのままか別のポートを指定できます。

!!! tip "ヒント"

    ポート 5432 が既に使用されている場合は、代替ポートを選択し、後で設定で使用するためにメモしておいてください。

#### ステップ 7: ロケールの選択

データベースのロケールを選択します。ほとんどのインストールではデフォルトで問題ありません。

#### ステップ 8: インストールの完了

残りのステップで **Next** をクリックし、完了したら **Finish** をクリックします。

#### ステップ 9: インストールの確認

コマンドプロンプトを開き、PostgreSQL がインストールされていることを確認します:

```bash
psql --version
```

インストールが成功していれば PostgreSQL のバージョンが表示されます。

---

## Web サーバーの設定 {: #web-server-configuration }

digna はダッシュボードをホストするための Web サーバーを必要とします。次のいずれかを選択してください：

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

これらのうち **いずれか1つ** をインストールして構成すれば十分です。

### IIS のセットアップ {: #iis-setup }

#### 概要

Internet Information Services (IIS) は、Web サイトや Web アプリケーションをホストするための Microsoft の Web サーバーです。

#### IIS の有効化

1. **コントロールパネルを開く**
   - `Win + R` を押す
   - `control` と入力して Enter

2. **Windows の機能に移動**
   - **プログラム** をクリック
   - **Windows の機能の有効化または無効化** を選択

3. **Internet Information Services を有効にする**
   - リストを下にスクロールして **Internet Information Services (IIS)** を見つける
   - チェックボックスをオンにして有効化する
   - **+** をクリックして展開し、次のサブコンポーネントが選択されていることを確認します:
     - **Web Management Tools**
     - **World Wide Web Services**

4. 変更を適用するには **OK** をクリック

5. **IIS インストールの確認**
   - ブラウザを開く
   - `http://localhost` にアクセス
   - IIS のウェルカムページが表示されるはずです

#### 必須: URL Rewrite モジュール

IIS には URL Rewrite コンポーネントが必要です。公式の Microsoft ページからダウンロードしてインストールしてください: [URL Rewrite モジュール](https://www.iis.net/downloads/microsoft/url-rewrite)

#### 必須: Markdown ファイルの MIME タイプ

IIS で Markdown ファイル（`.md`）を正しく配信するための設定:

1. **IIS マネージャー** を開く（`Win + R` を押して `inetmgr` と入力して Enter）
2. **該当サイト > MIME Types** に移動
3. **Add...** をクリック
4. 設定を行う:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "重要"

    この設定がないと、`.md` ファイルが正しく配信されない可能性があります。

---

### Apache Tomcat のセットアップ {: #apache-tomcat-setup }

#### 概要

Apache Tomcat はオープンソースの Java サーブレットコンテナ兼 Web サーバーです。

#### インストール

1. **Apache Tomcat をダウンロード**
   - [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi) を参照
   - Windows 用の ZIP 配布版をダウンロード

2. **アーカイブを展開**
   - ZIP ファイルをシステム上のディレクトリに展開
   - 例: `C:\Program Files\Apache Tomcat`

3. **Tomcat が動作していることを確認**
   - ブラウザを開く
   - `http://localhost:8080` にアクセス
   - Apache Tomcat のウェルカムページが表示されるはずです

!!! tip "ヒント"

    Apache Tomcat は通常インストール後に自動的に起動します。起動していない場合は、`bin` フォルダに移動して `startup.bat` を実行してください。

---

## 初期インストール {: #initial-installation }

### ステップ 1: digna リポジトリのセットアップ

digna リポジトリは digna によって計算されたすべてのメトリクスを保存します。分析およびパフォーマンスデータの中央データベースとして機能します。

#### リポジトリのスキーマとユーザーを作成

PostgreSQL クライアント（pgAdmin、psql など）を開き、次の SQL コマンドを実行してください:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**以下のプレースホルダーを置き換えてください:**

- `<digna_repo_schema>` — 希望するスキーマ名（例: `dignarepo`）
- `<digna_repo_user>` — 希望するユーザー名（例: `digna_user`）
- `<digna_repo_password>` — このユーザーの安全なパスワード

**例:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "ベストプラクティス"

    データベースユーザーには強力で複雑なパスワードを使用してください。簡単に推測できる資格情報は避けてください。

---

### ステップ 2: digna インストールパッケージを展開

1. 提供された digna インストール ZIP ファイルを見つける
2. 希望するインストール先に展開する
3. 展開後、次の項目が存在するはずです:
   - `dashboard/` — Web ダッシュボードインターフェース
   - `digna` — メイン実行ファイル（バックエンド + CLI が統合）

!!! info "設定ファイルとライセンスファイルはパッケージに含まれていません"

    `config.toml` も `dashboard/dashboard_config.toml` もインストールパッケージには含まれていません。どちらも [バックエンドの設定](#backend-configuration) と [ダッシュボードの設定](#dashboard-configuration) でご自身で作成します。`license.toml` も同梱されていません。ステップ 3 で説明するとおり、digna から別途提供されます。

### ステップ 3: ライセンスファイルをインストール

!!! warning "重要"

    ライセンスファイルはインストールパッケージに含まれていません。digna から別途提供されます。

1. 提供された `license.toml` ファイルを見つける
2. `config.toml` と `digna` 実行ファイルがある digna インストールディレクトリのルートにコピーする

**これが重要な理由:**
ライセンスファイルには顧客情報、ライセンスの有効期限、デジタル署名が含まれています。**このファイルを変更しないでください** — 変更すると無効になります。

**セットアップ後のディレクトリ構成:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## バックエンドの設定 {: #backend-configuration }

### ステップ 1: 設定ファイルを作成して編集する

`config_template.toml` ファイルが digna インストールディレクトリに同梱されています。これを `config.toml` にリネームしてください。

**場所:** `digna_installation/config.toml`

`config.toml` をテキストエディタで開き、以下の各セクションを設定します。

#### [app] セクション

このセクションは、ダッシュボードとバックエンド間のクロスオリジンリソース共有（CORS）を構成します:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | ダッシュボードの URL | ダッシュボードの配信元 URL。それ以外のオリジンからのブラウザーリクエストは拒否されます |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | 必須。ブラウザーが各リクエストでセッションクッキーを送信するために必要です |

!!! info "[app] セクションは省略可能です"

    リリース 2026.11 以降、両方のキー、そして `[app]` セクション全体を省略できます。リバースプロキシがダッシュボードとバックエンドを 1 つのオリジンで配信する場合は、これが適切な構成です。その場合、ブラウザーはクロスオリジンリクエストを行わず、デフォルトではいずれも許可されません。

#### [repo] セクション

このセクションは PostgreSQL データベースへの接続を設定します:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` または IP | PostgreSQL サーバーのホスト名/IP |
| `DIGNA_REPO_PORT` | `5432`（デフォルト） | PostgreSQL のポート |
| `DIGNA_REPO_DB` | `postgres` | データベース名 |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | 先に作成したスキーマ |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL セットアップで作成したユーザー |
| `DIGNA_REPO_PASSWORD` | あなたのパスワード | スキーマ作成時に設定したパスワード |
| `DIGNA_REPO_SSLMODE` | `prefer`（デフォルト） | 省略可能。PostgreSQL の SSL モード: `disable`、`allow`、`prefer`、`require`、`verify-ca` または `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16`（デフォルト） | 省略可能。digna がリポジトリに対して開いたままにする接続の数 |

#### [base] セクション

このセクションはセキュリティ、クッキー、検査の設定を含みます:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `DIGNA_FERNET_KEY` | 上記の値 | 以前のリリースで使用されていた暗号化の鍵。必ず指定する必要があるため、上記の値をそのまま使用してください |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | ダッシュボードにアクセスする際のホスト。`""` を指定するとドメインは設定されません。ダッシュボードとバックエンドを 1 つのオリジンで配信するプロキシの背後では、これが適切な設定です |
| `DIGNA_COOKIE_SECURE` | `false`（HTTP） / `true`（HTTPS） | digna を HTTPS で配信する場合は必ず `true` にしてください |
| `DIGNA_COOKIE_HTTPONLY` | `true` | セッションクッキーをスクリプトから参照できないようにします |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400`（24 時間） | セッションの有効期限（秒） |
| `DIGNA_MAX_WORKERS` | CPU コア数 - 1 | 同時に実行できる検査の数 |
| `DIGNA_FRONTEND_BASEURL` | ダッシュボードの URL | 必須。通知メッセージ内のリンクに使用されるため、受信者が開ける URL である必要があります |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600`（デフォルト） | 省略可能。ソースデータベースに対する 1 つのクエリが中止されるまでに実行できる秒数。`0` でタイムアウトを無効にします |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30`（デフォルト） | 省略可能。ソースデータベースへの接続を待機する秒数。`0` の場合は無期限に待機します |

#### [encryption] セクション

このセクションには、リポジトリに保存された機密値を暗号化するための鍵が含まれます。**必須**です。鍵が欠けている場合、`config check` は `[encryption]` セクションを FAILED として報告します。

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| パラメーター | 値 | 注意 |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64 エンコードされた鍵 | digna リポジトリに保存された機密値を暗号化します |

!!! warning "config.toml を保護する"

    この鍵は固定値で、すべての digna インストールで同一であり、リポジトリ内の機密値を復号するのはこの鍵です。`config.toml` へのアクセスを digna を実行するアカウントに限定し、バージョン管理や共有ドライブには置かず、リポジトリ本体より安全性の低い場所に保管されるバックアップからは除外してください。

#### [logging] セクション

このセクションはロギングの動作を設定します:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` または `DEBUG` | 本番では `INFO`、トラブルシューティング時は `DEBUG`。`TRACE`、`WARN`、`ERROR` も指定できます |
| `DIGNA_LOGGING_DIR` | `logs`（デフォルト） | 省略可能。ローテーションされるログファイルのディレクトリ（作業ディレクトリからの相対パス） |
| `DIGNA_LOGGING_MAX_FILES` | `30`（デフォルト） | 省略可能。保持するローテーション済みログファイルの数 |

!!! warning "サービスとして実行する場合はログディレクトリを維持してください"

    Windows サービスにはコンソールがないため、ログファイルがサービスの動作を記録する唯一の手段です。`DIGNA_LOGGING_DIR` を空文字列に設定しないでください。空文字列にするとログファイルが無効になります。

#### [duckdb] セクション（省略可能） {: #duckdb-section }

リリース 2026.11 の新機能です。このセクションでは **digna Engine** のリソースを設定します。digna Engine は、プロファイリングの場所が **digna Engine** であるデータベース接続について digna の内部でデータをプロファイリングし、異なるデータベース接続上のデータソース間で参照整合性チェックを実行します。参照: [プロファイリングの場所](../../../platform/profiling/profiling_location.md)。

このセクションは省略可能です。省略した場合は、以下のデフォルトが適用されます。

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024`（デフォルト） | 1 回の digna Engine の実行が使用できるメモリ（MB）。同時に最大 `DIGNA_MAX_WORKERS` 個の実行がアクティブになります |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | デフォルト: digna を実行するアカウントの一時ディレクトリ（`%TEMP%`） | データがメモリに収まらない場合に一時ファイルを置くディレクトリ |

!!! tip "digna Engine のサイジング"

    digna 自体が使用するメモリに加えて、digna ホストに最大 `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` のメモリを見込んでください。また一時ディレクトリには、digna Engine を使用するデータソースのうち最大の検査対象日のデータを保持できるだけの空きディスク容量が必要です。`DIGNA_DUCKDB_TEMP_DIRECTORY` は、その容量があり、digna を実行するアカウントが書き込めるディスクを指すように設定してください:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    このセクションが必要なのは、少なくとも 1 つのデータベース接続が digna Engine を使用する場合、または参照整合性チェックが異なる接続上のデータソースを比較する場合のみです。

---

### ステップ 2: 構成を検証する

リポジトリを初期化する前に、`config.toml` が完全で正しく構成されていることを確認します。digna のインストールディレクトリで次を実行します:

```bash
digna config check
```

各セクションは個別に検証されるため、1 つの誤りが他のセクションの状態を隠すことはありません:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

FAILED と報告された箇所をすべて修正し、続行する前にコマンドを再実行してください。**Unknown keys** の下に表示される WARNING は、digna が読み取らない `config.toml` 内のキーを示します。これらは効果がないため、削除するかスペルを修正してください。オプションの完全な一覧は [CLI リファレンス](../../../cli/Command_Line_Interface_202611.md)にあります。

### ステップ 3: リポジトリの初期接続確認

1. コマンドプロンプトを開く
2. digna のインストールディレクトリ（`config.toml` と `digna` 実行ファイルがある場所）に移動
3. 接続テストを実行:

```bash
digna repo check
```

新しいスキーマでは、コマンドは接続したうえで、リポジトリがまだインストールされていないことを報告します:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

この時点ではこれが想定どおりの結果で、digna が PostgreSQL とスキーマに到達できることを示しています。代わりに接続エラーや認証エラーが表示される場合は、`[repo]` セクションまたは PostgreSQL のセットアップに原因があります。

### ステップ 4: リポジトリスキーマのインストール

同じディレクトリで次を実行します:

```bash
digna repo upgrade
```

このコマンドはリポジトリスキーマに必要なテーブルをインストールし、最後に次のように表示します:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade はインストールとアップグレードの両方を行います"

    リリース 2026.11 以降、`repo upgrade` は新しいリポジトリのインストールと既存のリポジトリのアップグレードの両方を行います。`repo install` も同じコマンドの別名として引き続き使用できます。

### ステップ 5: 管理者ユーザーを作成

管理者ユーザーはリポジトリスキーマに対して直接作成されるため、この時点でサーバーを起動しておく必要はありません。digna インストールディレクトリで次を実行します:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**例:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

これで完全な管理権限を持つユーザーが作成されます。

!!! tip "ベストプラクティス"

    大文字・小文字・数字・特殊文字を組み合わせた強力なパスワードを使用してください。

### ステップ 6: digna サーバーを起動

digna インストールディレクトリで、サーバーを次のように起動します:

```bash
digna serve --address <host> --port <port>
```

**パラメータ:**
- `--address` — サーバーのホスト名/IP（デフォルト `127.0.0.1`）
- `--port` — サーバーのポート（デフォルト `8000`）

サーバーが起動すると、待ち受けているアドレスが表示されます:

```text
Server running on http://127.0.0.1:8082
```

!!! note "サーバーはターミナルを占有します"

    `serve` はフォアグラウンドで実行され、++ctrl+c++ で停止するまで動作し続けます。セットアップを終えるまで実行したままにしてください。起動時に自動的に開始する方法は次を参照してください: [digna を Windows サービスとして実行する](#running-digna-as-a-windows-service).

---

## ダッシュボードの設定 {: #dashboard-configuration }

### ステップ 1: ダッシュボードを Web サーバーにデプロイ

digna ダッシュボードは独自の設定を `dashboard/dashboard_config.toml` から読み込みます。このファイルはインストールパッケージに含まれていないため、`dashboard/` ディレクトリ内にダッシュボードのファイルと並べて作成します。

その内容は [シングルサインオン](../../../sso/overview.md) で説明しています。このファイルが必要になるのもそこです。このファイルには、ダッシュボードが提供するログイン方法と、マルチインスタンス構成の場合はバックエンドへの接続先が記述されます。

使用する Web サーバーを選択し、該当するデプロイ手順に従ってください。

#### IIS へデプロイする場合

1. **IIS マネージャーを開く**
   - `Win + R` を押して `inetmgr` と入力して Enter

2. **新しいサイトを作成**
   - 左側パネルで **Sites** を右クリック
   - **Add Website...** を選択

3. **サイトを構成**
   - **Site Name**: 名前を入力（例: "dignaDashboard"）
   - **Physical Path**: Browse をクリックして `dashboard` フォルダを選択
   - **Binding**: IP アドレスとポートを設定（HTTP のデフォルトはポート 80、HTTPS は 443）

4. **サイトを開始**
   - **OK** をクリックしてサイトを作成
   - 新しいサイトを右クリックして **Start** を選択

5. **インストールのテスト**
   - ブラウザを開く
   - `http://localhost`（または設定した URL）にアクセス
   - digna ダッシュボードのログインページが表示されるはずです

#### Apache Tomcat へデプロイする場合

1. **ダッシュボードを Tomcat にコピー**
   - `dashboard` フォルダを Tomcat の `webapps` ディレクトリにコピー
   - 必要に応じて名前を変更（例: `digna`）
   - 例: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **デプロイの確認**
   - Tomcat 管理ページ（http://localhost:8080）をリフレッシュまたはリロード
   - 「digna」（または指定した名前）がデプロイ済みアプリケーションとして表示されるはずです

3. **ダッシュボードへアクセス**
   - ブラウザを開く
   - `http://localhost:8080/digna` にアクセス
   - digna ダッシュボードのログインページが表示されるはずです

---

## digna を Windows サービスとして実行する {: #running-digna-as-a-windows-service }

### なぜ Windows サービスを使うのか？

digna バックエンドを Windows サービスとして実行すると、次の利点があります:
- サーバー起動時に自動的に開始される
- 開いたコマンドプロンプトがなくてもバックグラウンドで実行される
- クラッシュ時に自動で再起動される
- Windows サービスから管理できる

### `windows` コマンド

サービスは `digna` 実行ファイル自体が `digna windows` サブコマンドを通じて管理します。実行するバッチファイルはありません。

| コマンド | 用途 |
|---|---|
| `digna windows install` | digna を Windows サービスとして登録する |
| `digna windows start` | 登録済みのサービスを開始する |
| `digna windows stop` | 実行中のサービスを停止する |
| `digna windows uninstall` | サービスの登録を解除する |

!!! warning "管理者権限が必要"

    4 つのコマンドはすべて、管理者として開いたコマンドプロンプトから実行する必要があります。

どのコマンドも `--name` を受け付け、既定以外の名前で登録したサービスを指定できます。オプションの完全な一覧は [CLI リファレンス](../../../cli/Command_Line_Interface_202611.md) にあります。

### サービスのインストール

1. **管理者としてコマンドプロンプトを開く**
   - コマンドプロンプトを右クリック
   - 「管理者として実行」を選択

2. **digna のインストールディレクトリに移動**
   ```bash
   cd C:\path\to\digna
   ```

3. **サービスを登録**
   ```bash
   digna windows install
   ```

!!! important "既定値が適さない場合はアドレスとポートを指定してください"

    `install` はアドレスとポートをサービスの登録情報に記録し、サービスは記録されたとおりの値にバインドします。既定値は `127.0.0.1` と `8000` で、そのマシン自身からの接続しか受け付けません。別のホスト上のダッシュボードからは到達できないため、バックエンドが待ち受けるアドレスを指定してください:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    これらの値は `config.toml` からは読み込まれません。後で変更するには、サービスをアンインストールし、新しい値で再度インストールしてください。

サービスは**自動起動**で登録されるため、Windows とともに起動します。登録直後には開始されません — 次のセクションを参照してください。

#### インストールオプション

| オプション | 既定値 | 用途 |
|---|---|---|
| `--name` | `digna` | サービスを登録する名前 |
| `--display-name` | `digna` | services.msc に表示される名前 |
| `--description` | `digna data quality backend` | services.msc に表示される説明 |
| `--address` | `127.0.0.1` | サービスが API をバインドするアドレス |
| `--port` | `8000` | サービスが API をバインドするポート |
| `--working-dir` | `digna` 実行ファイルのディレクトリ | `config.toml` と `license.toml` を格納するディレクトリ。サービスはこれを作業ディレクトリにします |
| `--start-type` | `auto` | `auto` は Windows とともに起動、`manual` は要求されたときのみ起動、`disabled` はサービスを登録するが起動を拒否します |
| `--account` | `LocalSystem` | 実行に使うアカウント（例: `DOMAIN\user` または `.\user`） |
| `--password` | | `--account` のパスワード |

!!! tip "ドメインアカウントで実行する場合"

    `LocalSystem` にはネットワーク上の ID がないため、SQL Server に対する Windows 認証やネットワーク共有へのアクセスは失敗します。サービスが特定のユーザーとしてリソースにアクセスする必要がある場合は、`--account` と `--password` を指定してインストールしてください。

### サービスの開始と停止

#### サービスを開始するには

```bash
digna windows start
```

#### サービスを停止するには

```bash
digna windows stop
```

!!! tip "ヒント"

    アプリケーションファイルを更新する前には必ずサービスを停止してください。

### サービスを新しいディレクトリに移動する場合

digna のインストールを移動する必要がある場合:

1. **現在のサービスを停止して登録を解除**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **アプリケーションファイルを移動**
   - digna インストールフォルダ全体を新しい場所に移動

3. **新しい場所からサービスを再登録**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   初回に使用した `--address`、`--port`、`--account` の値を再度指定してください — 以前の登録情報は削除されています。

4. **サービスを開始**
   ```bash
   digna windows start
   ```

### サービスのアンインストール

1. **実行中のサービスを停止**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **サービスの登録を解除**
   ```bash
   digna windows uninstall
   ```

これで digna サーバーは Windows サービスとしての登録が解除されます。

---

## 新しいリリースへのアップグレード {: #upgrading-to-a-new-release }

このセクションでは、リリース 2026.06 のインストールをリリース 2026.11 にアップグレードします。それより古いインストールの場合は、先に [リリース 2026.06 より前のリリースからのアップグレード](#upgrading-from-a-release-before-2026-06)をお読みください。

### アップグレード前に

**digna リポジトリのバックアップ作成は必須です**

digna をアップグレードする前にリポジトリ（PostgreSQL）のバックアップを作成し、データ損失に備えてください。バックアップがあれば、アップグレード中に予期しない問題が発生しても復旧できます。

**リリース 2026.11 用のライセンスファイルを依頼する**

リリース 2026.11 には新しい `license.toml` が必要です。作業を始める前に digna チームに依頼し、[ステップ 7](#step-7-replace-the-license-file) で使えるよう準備しておいてください。

### リリース 2026.06 より前のリリースからのアップグレード {: #upgrading-from-a-release-before-2026-06 }

リリース 2026.06 では 3 つの変更が導入されました。古いインストールを 2026.11 に直接アップグレードする場合にも、これらは引き続き適用されます:

- **ODBC のみ。** digna はすべてのソース技術に ODBC 経由で接続します。まだ ODBC を使用していないデータベース接続は、アップグレード後にすべて ODBC に変更する必要があります。自動変換はありません。事前に digna ホストに ODBC ドライバーをインストールし（参照: [digna ホストへの ODBC ドライバーのインストール](../../../databases/overview.md#install-the-driver)）、[技術別ガイド](../../../databases/overview.md#technology-guides) を参考に各接続のプロパティを用意しておいてください。Databricks Legacy コネクタは廃止されました。該当する接続は [Databricks](../../../databases/databricks_connector_guide.md) コネクタへ移行してください。
- **単一の実行ファイル。** `dignabackend` と `dignacli` は、バックエンドと CLI を統合した単一の実行ファイル `digna` に置き換えられました。
- **config.toml。** `[encryption]` セクションが必須となり、`DIGNA_APP_HOST` と `DIGNA_APP_PORT` は読み取られなくなりました。サーバーのアドレスとポートは `digna serve` から渡されます。ご自身のファイルを [バックエンドの設定](#backend-configuration)と比較してください。

以下の手順では、古いインストールで異なる作業が必要な箇所を示します。ステップ 8 のリポジトリのアップグレードにより、以前のどのリリースのリポジトリも直接 2026.11 に更新されます。

### アップグレード手順

#### ステップ 1: digna サービスを停止する {: #step-1-stop-the-digna-service }

管理者としてコマンドプロンプトを開き、現在のインストールの `digna` 実行ファイルでサービスを停止します:

```bash
cd C:\path\to\digna
digna windows stop
```

サービスの登録はそのまま残ります。新しい実行ファイルは同じディレクトリで古い実行ファイルと置き換わるため、登録は引き続き正しいファイルを指します。

digna がフォアグラウンドで動作している場合は、そのコマンドプロンプトウィンドウで ++ctrl+c++ を押してください。

!!! warning "リリース 2026.06 より前のリリースからアップグレードする場合"

    リリース 2026.06 より前のリリースでは、サービスはバッチファイルで登録されていました。ステップ 2 で何かの名前を変更する**前に**、現在のインストールのバッチファイルを使ってサービスを停止し、登録を解除してください:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    サービスを実行していたアカウントと、サービスが待ち受けていたアドレスとポートを控えておいてください。ステップ 9 でサービスを再登録します。

#### ステップ 2: 現在のインストールをバックアップする {: #step-2-backup-current-installation }

digna のインストールディレクトリで、現在のインストールの実行ファイルとダッシュボードフォルダーの名前を変更し、新しいリリースを並べて配置できるようにします:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

`digna_old.exe` はアップグレードを確認するまで、`dashboard_old` はそこから設定ファイルを復元するまで残してください（ステップ 4 を参照）。その後は両方とも削除してかまいません。

!!! info "リリース 2026.06 より前のリリースからアップグレードする場合"

    実行ファイルの代わりに、`dignabackend` と `dignacli` のフォルダー名を変更します:
    `ren dignabackend dignabackend_old` と `ren dignacli dignacli_old`。リリース 2026.11 では、どちらのフォルダーも、バッチファイルの入った `bin` フォルダーも使用されません。

#### ステップ 3: 新バージョンの展開とデプロイ {: #step-3-extract-and-deploy-new-version }

1. 新しい digna インストール ZIP ファイルを展開
2. 新しい `digna` 実行ファイルと `dashboard` フォルダをインストールディレクトリにコピー

!!! warning "重要"

    `config.toml` も `dashboard/dashboard_config.toml` も、インストール ZIP に含まれることは決してありません。digna チームはどちらのファイルも配布しません。そのため既存の設定はアップグレードの影響を受けず、名前を変更した `*_old` フォルダー内のコピーが手元にある唯一の設定になります。

#### ステップ 4: 設定ファイルの復元 {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

リリース 2026.11 では `config.toml` の変更は不要です。リリース 2026.06 で動作するファイルはそのまま動作し続けます。次の 2 つの変更は任意です:

- データベース接続で digna Engine を使用し、そのデフォルトがホストに合わない場合は、[`[duckdb]` セクション](#duckdb-section) を追加します。
- リバースプロキシがダッシュボードとバックエンドを 1 つのオリジンで配信する場合は、`[app]` セクションを省略します。

!!! warning "digna が読み取らない設定"

    本ガイドの以前の版には、digna が読み取らない設定がいくつか記載されていました。これらは効果がなく、ステップ 6 で `config check` が **Unknown keys** の下に一覧表示します。削除するか修正してください:

    - `DIGNA_SCHEDULER_MAX_DELAY`、`DIGNA_CLEANUP_TIME`、`digna_COOKIE_PATH`、`digna_COOKIE_SAME_SITE`、`digna_APP_CORS_ALLOW_METHODS`、`digna_APP_CORS_ALLOW_HEADERS`、`digna_LOGGING_BACKUP_COUNT` は存在しません。削除してください。
    - 設定名は大文字と小文字を区別します。digna が読み取るのは `DIGNA_REPO_HOST` であり、`digna_REPO_HOST` ではありません。[バックエンドの設定](#backend-configuration) と同様に、すべての名前を大文字で記述してください。

!!! warning "シングルサインオン: [[oidc_clients]] を維持してください"

    digna はシングルサインオンのプロバイダーを `[[oidc_clients]]` エントリのリストとして読み取ります。各エントリにはそれぞれ `DIGNA_OIDC_KEY` があります。本ガイドの以前の版に従ってプロバイダーを `[oidc_clients.<key>]` セクションに変更した場合は、元に戻してください。その形式が残っている間、`config check` は `OIDC config(s)` を FAILED と報告します:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    プロバイダーごとにこのエントリを繰り返し、各 `DIGNA_OIDC_KEY` を `dashboard_config.toml` の `key` と一致させてください。影響を受けるのはシングルサインオンを使用しているインストールのみです。

#### ステップ 5: Web サーバーをリロードする {: #step-5-reload-the-web-server }

ダッシュボードは静的ファイルの集まりであるため、Web サーバー（およびブラウザー）が以前のバージョンを配信し続けている可能性があります。`dashboard` フォルダーをホストしている Web サーバーをリロードまたは再起動し、ページをハードリフレッシュ（++ctrl+f5++）で再読み込みしてください。

#### ステップ 6: 構成を検証する {: #step-6-validate-the-configuration }

リポジトリに手を加える前に、`config.toml` が完全であることを確認します:

```bash
digna config check
```

すべてのセクションが OK と報告される必要があります。FAILED と報告された箇所を修正し、**Unknown keys** の下に一覧表示されたキーを削除してから、続行する前にコマンドを再実行してください。

#### ステップ 7: ライセンスファイルを置き換える {: #step-7-replace-the-license-file }

通常、ライセンスファイルはリリースをまたいでそのまま使用できます。リリース 2026.11 は例外です。このリリースでは digna Data Reconciliation と digna Agentic という 2 つのライセンス対象モジュールが追加され、2026.11 より前に発行されたライセンスにはこれらが含まれていません。digna チームがリリース 2026.11 用に提供した `license.toml` をインストールディレクトリにコピーし、古いものを置き換えてください:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "以前のライセンスを使い続けないでください"

    以前のライセンスのままでも digna は起動しますが、digna Data Reconciliation と digna MCP Server は無効のままです。ライセンスを確認するすべてのコマンド（`user`、`inspection`、`repo`）は、確認に失敗するとリポジトリに手を加える前に中止されます。先に進む前に新しいライセンスを確認してください:

    ```bash
    digna license check
    ```

#### ステップ 8: リポジトリスキーマのアップグレード {: #step-8-upgrade-the-repository-schema }

digna のインストールディレクトリで次を実行します:

```bash
digna repo upgrade
```

リリース 2026.11 では、リポジトリスキーマをバージョン管理されたマイグレーションで管理します。以前のリリースからの最初のアップグレードでは、スキーマを従来方式の最終バージョンに更新し、それを起点として記録したうえで、リリース 2026.11 のマイグレーションを適用します。最後に次のように表示されます:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

既存のデータはすべて保持されます。リポジトリの状態はいつでも `digna repo check` で確認できます。最後に適用されたマイグレーションと、保留中のマイグレーションが一覧表示されます。

!!! warning "リポジトリが古いままでは digna は起動しません"

    リリース 2026.11 以降、リポジトリのアップグレードが必要な間はサーバーが起動を拒否し、その旨を表示します。例:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    サーバーまたはサービスを起動する前に `repo upgrade` を実行してください。

#### ステップ 9: サービスの再起動 {: #step-9-restart-services }

digna を Windows サービスとして実行している場合は、再び起動します:

```bash
cd C:\path\to\digna
digna windows start
```

リリース 2026.06 より前のリリースからアップグレードし、ステップ 1 でサービスの登録を解除した場合は、先に `digna` 実行ファイルでサービスを再登録します:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

`--address` と `--port` には、デフォルトの `127.0.0.1` と `8000` を使用する場合を除き、以前のサービスが待ち受けていた値を指定してください。以前のサービスがドメインアカウントで実行されていた場合は、`--account` と `--password` を追加します。オプションの完全な一覧は [digna を Windows サービスとして実行する](#running-digna-as-a-windows-service) を参照してください。

手動で実行している場合はサーバーを再起動します:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

IIS または Tomcat を使用している場合は、それぞれの Web サーバーを再起動してください。

#### ステップ 10: アップグレードの確認 {: #step-10-verify-the-upgrade }

1. 新しい実行ファイルのリリースを確認します:

    ```bash
    digna version
    ```

    1 行目が `Release: 2026.11` となっている必要があります。

2. digna ダッシュボードにアクセスし、インターフェースが正しく読み込まれることを確認します。
3. インストールディレクトリの `logs` ディレクトリ内のファイルにエラーがないか確認します。
4. データベース接続をテストします。参照:
   [接続のテスト](../../../databases/overview.md#testing-a-connection)。リリース 2026.06 より前のリリースからアップグレードした場合は、まだ ODBC を使用していなかった接続をすべて先に ODBC に切り替えてください。

新しいモジュールを使い始めるには、[digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md)、digna MCP Server については [AI エージェントの接続](../../../platform/agentic/connect_ai_agent.md)、digna Engine については [プロファイリングの場所](../../../platform/profiling/profiling_location.md) を参照してください。

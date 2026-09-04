---
title: Windows インストールガイド – digna Release 2026.06 | digna ドキュメント
description: Windows に digna Release 2026.06 をインストールするための手順ガイド — システム要件、PostgreSQL のセットアップ、Web サーバー構成、バックエンドとダッシュボードの設定、Windows サービスとしての起動、リリースのアップグレード手順
keywords: digna windows インストール, digna デプロイガイド, digna バックエンド セットアップ, digna ダッシュボード インストール, postgresql セットアップ, digna windows サービス, digna アップグレード ガイド
image: /assets/logo_square.png
---

# digna Release 2026.06 の Windows インストールガイド

**リリース:** 2026.06

**最終更新日:** 2026年8月30日


---

## 目次

1. [はじめに](#introduction)
2. [システム要件](#system-requirements)
3. [事前準備](#pre-installation-setup)
4. [PostgreSQL サーバーのセットアップ](#postgresql-server-setup)
5. [Web サーバー構成](#web-server-configuration)
6. [初回インストール](#initial-installation)
7. [バックエンド構成](#backend-configuration)
8. [ダッシュボード構成](#dashboard-configuration)
9. [Windows サービスとして digna を実行する](#running-digna-as-a-windows-service)
10. [新しいリリースへのアップグレード](#upgrading-to-a-new-release)

---

## はじめに {: #introduction }

### digna について

digna は、データウェアハウス、データレイク、レイクハウスなどのさまざまなデータ環境におけるデータ品質管理を最適化するための包括的な AI 駆動プラットフォームです。高いスケーラビリティと適応性を備え、自動化、リアルタイム監視、異常検知を通じて現代のデータ課題に対処します。

digna は主に次の2つのコンポーネントで構成されています:

- **dignabackend**: データ処理や品質チェックを担うコアエンジン
- **dignadashboard**: Web サーバー上でホストされる Web ベースのインターフェースで、digna プラットフォームとやり取りし、データ品質指標を可視化します

### Release 2026.06 の新機能

このリリースでは、データ可観測性（data observability）機能をコードの中に直接組み込めるようになり、開発者がソースでデータ品質を監視できるようになります。詳細は[リリースノート](http://docs.digna.ai/changelog/Release_202606/)を参照してください。

---

## システム要件 {: #system-requirements }

インストールを開始する前に、システムが以下の最小要件を満たしていることを確認してください。

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server または Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB の空き領域 |
| **Database** | PostgreSQL Server 12 以上 |
| **Web Server** | IIS、Apache Tomcat、または同等のもの |

### データベースのインストールオプション

**既に PostgreSQL がインストールされている場合:**
既存の PostgreSQL サーバーに digna 用の新しいデータベース／スキーマを追加できます。

**digna と同じマシンに PostgreSQL をインストールする場合:**

> **推奨仕様**
>
> - **メモリ**: 32 GB RAM（16 GB の代わりに推奨）
> - **ディスク容量**: 50 GB の空き領域（10 GB の代わりに推奨）
>
> これらの上位仕様は、digna と PostgreSQL データベースの両方が同時に動作することを想定しています。

---

## 事前準備 {: #pre-installation-setup }

digna をインストールする前に、次の2つの重要な前提条件を用意してください:

1. **PostgreSQL サーバー** — 集計メトリクスやパフォーマンスデータの保存先
2. **Web サーバー** — digna Dashboard をホストするため

これらが未設定の場合は、以下のセクションに従ってインストールおよび構成を行ってください。

---

## PostgreSQL サーバーのセットアップ {: #postgresql-server-setup }

### 既に PostgreSQL をお使いの場合

ローカルで PostgreSQL が稼働している、またはマネージドなリモート PostgreSQL サーバーを使用している場合は、[次のセクション](#web-server-configuration)に進んでください。

### PostgreSQL のインストール

Windows に PostgreSQL をインストールする手順:

#### ステップ 1: PostgreSQL をダウンロード

1. [PostgreSQL ダウンロードページ](https://www.postgresql.org/download/) にアクセス
2. **Windows** を選択
3. 最新のインストーラーをダウンロード

#### ステップ 2: インストーラーを実行

1. ダウンロードしたインストーラーをダブルクリック
2. セットアップウィザードの指示に従う

#### ステップ 3: インストール先の選択

PostgreSQL をインストールするディレクトリを選択します。通常はデフォルトで問題ありません。

#### ステップ 4: コンポーネントの選択

標準的なセットアップでは、デフォルトのコンポーネント設定のままで問題ありません。

#### ステップ 5: PostgreSQL スーパーユーザーのパスワード設定

PostgreSQL のスーパーユーザー（`postgres`）のパスワードを入力して確認します。**このパスワードは安全に保管してください** — 後で必要になります。

#### ステップ 6: ポート番号の設定

PostgreSQL のデフォルトポートは `5432` です。必要に応じてデフォルトのまま、または別のポートを指定してください。

> **ヒント**
>
> もしポート5432が既に使用されている場合は、代替ポートを選択し、後での設定でそのポート番号を記録しておいてください。

#### ステップ 7: ロケールの選択

データベースのロケールを選択します。通常はデフォルトで問題ありません。

#### ステップ 8: インストールの完了

残りの画面で **Next** をクリックし、最後に **Finish** をクリックします。

#### ステップ 9: インストールの確認

コマンドプロンプトを開き、PostgreSQL がインストールされているか確認します:

```bash
psql --version
```

インストールが成功していれば PostgreSQL のバージョンが表示されます。

---

## Web サーバー構成 {: #web-server-configuration }

digna はダッシュボードをホストするために Web サーバーを必要とします。次のいずれかを選択してください:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

これらのうち **いずれか一つ** をインストールして構成すれば十分です。

### IIS のセットアップ {: #iis-setup }

#### 概要

Internet Information Services (IIS) は Microsoft の Web サーバーで、Web サイトや Web アプリケーションをホストします。

#### IIS を有効化する手順

1. **コントロールパネルを開く**
   - `Win + R` を押す
   - `control` と入力して Enter

2. **Windows の機能に移動**
   - **プログラム** をクリック
   - **Windows の機能の有効化または無効化** を選択

3. **Internet Information Services を有効化**
   - リストから **Internet Information Services (IIS)** を見つけ、チェックを入れる
   - `+` をクリックしてサブコンポーネントを展開し、次を選択していることを確認:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **OK をクリック** して変更を適用

5. **IIS のインストール確認**
   - ブラウザを開く
   - `http://localhost` にアクセス
   - IIS のウェルカムページが表示されるはずです

#### 必須: URL Rewrite モジュール

IIS では URL Rewrite コンポーネントが必要です。公式 Microsoft ページからダウンロードしてインストールしてください: https://www.iis.net/downloads/microsoft/url-rewrite

#### 必須: Markdown ファイルの MIME タイプ

IIS で Markdown ファイル（`.md`）を正しく配信するには MIME タイプを追加します:

1. **IIS マネージャー** を開く（`Win + R`、`inetmgr` と入力して Enter）
2. **対象のサイト > MIME Types** に移動
3. **Add...** をクリック
4. 設定:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

> **重要**
>
> この設定がないと `.md` ファイルが正しく配信されない可能性があります。

---

### Apache Tomcat のセットアップ {: #apache-tomcat-setup }

#### 概要

Apache Tomcat はオープンソースの Java サーブレットコンテナ兼 Web サーバーです。

#### インストール手順

1. **Apache Tomcat をダウンロード**
   - [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi) にアクセス
   - Windows 用 ZIP 配布版をダウンロード

2. **アーカイブを展開**
   - ZIP ファイルをシステム上のディレクトリに展開
   - 例: `C:\Program Files\Apache Tomcat`

3. **Tomcat が稼働していることを確認**
   - ブラウザを開く
   - `http://localhost:8080` にアクセス
   - Apache Tomcat のウェルカムページが表示されるはずです

> **ヒント**
>
> 通常、Apache Tomcat はインストール後に自動で起動します。起動していない場合は、`bin` フォルダに移動して `startup.bat` を実行してください。

---

## 初回インストール {: #initial-installation }

### ステップ 1: digna リポジトリをセットアップ

digna リポジトリは digna が計算するすべてのメトリクスを格納します。分析・パフォーマンスデータの中央データベースとして機能します。

#### リポジトリ用スキーマとユーザーの作成

PostgreSQL クライアント（pgAdmin、psql など）を開き、以下の SQL コマンドを実行します:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**以下のプレースホルダーを置き換えてください:**

- `<digna_repo_schema>` — 任意のスキーマ名（例: `dignarepo`）
- `<digna_repo_user>` — 任意のユーザー名（例: `digna_user`）
- `<digna_repo_password>` — このユーザー用の安全なパスワード

**例:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **ベストプラクティス**
>
> データベースユーザーには強固で複雑なパスワードを使用し、推測されやすい認証情報は避けてください。

---

### ステップ 2: digna インストールパッケージを展開

1. 提供された digna インストール ZIP ファイルを見つける
2. 希望のインストール先に展開する
3. 展開後、以下のアイテムが含まれていることを確認してください:
   - `dashboard/` — Web ダッシュボードインターフェース
   - `digna` — メイン実行ファイル（バックエンド＋CLI）
   - `config.toml` — 設定ファイル
   - `license.toml` — ライセンスファイル（別途提供されたものをここにコピー）

### ステップ 3: ライセンスファイルの設置

> **重要**
>
> ライセンスファイルはインストールパッケージに含まれていません。digna から別途提供されます。

1. 提供された `license.toml` ファイルを探す
2. `config.toml` と `digna` 実行ファイルがあるルートの digna インストールディレクトリにコピーします

**理由:**
ライセンスファイルには顧客情報、ライセンスの有効期限、デジタル署名が含まれます。**このファイルを改変しないでください** — 変更すると無効になります。

**セットアップ後のディレクトリ構成例:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## バックエンド構成 {: #backend-configuration }

### ステップ 1: 設定ファイルを作成して編集する

`config_template.toml` ファイルが digna インストールディレクトリに含まれています。これを `config.toml` にリネームして使用します。

**場所:** `digna_installation/config.toml`

`config.toml` をテキストエディタで開き、以下の各セクションを設定してください。

#### [app] セクション

digna バックエンドのアプリケーション設定を構成します:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` または IP アドレス | dignabackend をホストするホスト名または IP |
| `digna_APP_PORT` | `8082` (デフォルト) | REST API エンドポイントのポート |
| `digna_APP_CORS_ALLOW_ORIGINS` | フロントエンドの URL | ダッシュボードが別サーバーにある場合はその URL を含める |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | 認証情報付き CORS に必要 |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | すべての HTTP メソッドを許可 |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | すべてのヘッダーを許可 |

#### [repo] セクション

PostgreSQL データベースへの接続を設定します:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` または IP | PostgreSQL サーバーのホスト名/IP |
| `digna_REPO_PORT` | `5432` (デフォルト) | PostgreSQL のポート |
| `digna_REPO_DB` | `postgres` | データベース名 |
| `digna_REPO_SCHEMA` | `dignarepo` | 先に作成したスキーマ |
| `digna_REPO_USER` | `digna_user` | PostgreSQL で作成したユーザー |
| `digna_REPO_PASSWORD` | あなたのパスワード | スキーマ作成時に設定したパスワード |

#### [base] セクション

セキュリティやクッキー設定を含みます:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | 暗号化キー | トークンやクッキーの暗号化に使用（デフォルトのキーが提供されることがあります） |
| `digna_COOKIE_DOMAIN` | `localhost` | フロントエンドのドメインに合わせて設定 |
| `digna_COOKIE_SECURE` | `false` (ローカル) / `true` (本番) | HTTPS 接続では `true` を使用 |
| `digna_COOKIE_HTTPONLY` | `true` | セキュリティのため常に有効推奨 |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF 対策 |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24時間) | セッションの有効期間（秒） |
| `digna_MAX_WORKERS` | CPU コア数 - 1 | 並列検査タスクの数 |

#### [logging] セクション

ログ動作を設定します:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` または `DEBUG` | 本番は `INFO`、トラブルシューティング時は `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | 保持する日次ログのバックアップ数 |

---

### ステップ 3: リポジトリの接続確認

1. コマンドプロンプトを開く
2. `config.toml` と `digna` 実行ファイルがある digna インストールディレクトリに移動
3. 接続テストを実行:

```bash
digna repo check
```

接続が確立されたことを確認するメッセージが表示されます（リポジトリ自体はまだ初期化されていません）。

### ステップ 4: リポジトリスキーマのインストール

同じディレクトリで次を実行します:

```bash
digna repo install
```

このコマンドで PostgreSQL データベースに必要なテーブルやスキーマがインストールされます。

### ステップ 5: digna サーバーの起動

digna インストールディレクトリでサーバーを起動します:

```bash
digna serve --address <host> --port <port>
```

**パラメーター:**
- `--address` — サーバーのホスト名/IP
- `--port` — サーバーのポート

起動メッセージの例:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### ステップ 6: 管理者ユーザーの作成

1. 新しいコマンドプロンプトウィンドウを開く
2. digna インストールディレクトリに移動
3. 管理者ユーザーを作成するコマンドを実行:

```bash
digna user add <username> "<full_name>" <password> --su
```

**例:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

これでフル管理権限を持つユーザーが作成されます。

> **ベストプラクティス**
>
> 大文字、小文字、数字、特殊文字を組み合わせた強力なパスワードを使用してください。

---

## ダッシュボード構成 {: #dashboard-configuration }

### ステップ 1: ダッシュボードを Web サーバーにデプロイ

digna ダッシュボードには `dashboard/` ディレクトリ内に独自の `config.toml` が含まれています。初期セットアップでは通常変更は不要です。バックエンド接続をカスタマイズする場合のみ編集してください。

ダッシュボード設定の変更（例: マルチインスタンス構成）が必要な場合は、ダッシュボードのドキュメントを参照してください。

使用する Web サーバーを選び、該当するデプロイ手順に従ってください。

#### IIS へのデプロイ

1. **IIS マネージャーを開く**
   - `Win + R`、`inetmgr` と入力して Enter

2. **新しいサイトを作成**
   - 左ペインで **Sites** を右クリック
   - **Add Website...** を選択

3. **ウェブサイトを設定**
   - **Site Name**: 任意の名前（例: "dignaDashboard"）
   - **Physical Path**: Browse をクリックして `dashboard` フォルダを選択
   - **Binding**: IP アドレスとポートを設定（HTTP のデフォルトはポート 80、HTTPS は 443）

4. **サイトを起動**
   - **OK** をクリックしてサイトを作成
   - 新しく作成したサイトを右クリックし **Start** を選択

5. **インストールのテスト**
   - ブラウザを開く
   - `http://localhost` （または設定した URL）にアクセス
   - digna ダッシュボードのログインページが表示されるはずです

#### Apache Tomcat へのデプロイ

1. **ダッシュボードを Tomcat にコピー**
   - `dashboard` フォルダを Tomcat の `webapps` ディレクトリにコピー
   - 必要に応じて名前を変更（例: `digna`）
   - 例: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **デプロイの確認**
   - Tomcat 管理ページ（http://localhost:8080）を更新またはリロード
   - デプロイ済みアプリケーションに "digna"（または設定した名前）が表示されるはずです

3. **ダッシュボードへアクセス**
   - ブラウザを開く
   - `http://localhost:8080/digna` にアクセス
   - digna ダッシュボードのログインページが表示されるはずです

---

## Windows サービスとして digna を実行する {: #running-digna-as-a-windows-service }

### なぜ Windows サービスを使うのか

digna バックエンドを Windows サービスとして実行すると次の利点があります:
- サーバー起動時に自動的に開始
- コマンドプロンプトを開かずにバックグラウンドで動作
- クラッシュ時に自動的に再起動可能
- Windows サービスから管理可能

### サービス管理ファイル

必要なファイルはすべて digna インストールディレクトリの `bin/` にあります。

利用可能なバッチファイル:
- `install_service.bat` — digna を Windows サービスとして登録
- `uninstall_service.bat` — サービスの登録解除
- `start_service.bat` — サービスの起動
- `stop_service.bat` — サービスの停止

> **管理者権限が必要**
>
> これらのバッチファイルはすべて管理者権限で実行する必要があります。

### サービスのインストール手順

1. **管理者としてコマンドプロンプトを開く**
   - コマンドプロンプトを右クリック
   - 「管理者として実行」を選択

2. **bin フォルダに移動**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **インストールスクリプトを実行**
   ```bash
   install_service.bat
   ```

これで digna サーバーが自動起動設定の Windows サービスとして登録されます。サービスは直ちに起動しないため、次のセクションで起動手順を確認してください。

### サービスの起動と停止

#### サービスを起動するには

1. 管理者としてコマンドプロンプトを開く
2. `digna\bin` に移動
3. 次を実行:
   ```bash
   start_service.bat
   ```

#### サービスを停止するには

1. 管理者としてコマンドプロンプトを開く
2. `digna\bin` に移動
3. 次を実行:
   ```bash
   stop_service.bat
   ```

> **ヒント**
>
> アプリケーションファイルを更新する前は、常にサービスを停止してください。

### サービスを新しいディレクトリに移動する

digna を別の場所に移動する必要がある場合:

1. **現在のサービスをアンインストール**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **アプリケーションファイルを移動**
   - digna のインストールフォルダ全体を新しい場所に移動します

3. **サービスを再インストール**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **サービスを起動**
   ```bash
   start_service.bat
   ```

### サービスのアンインストール

1. **実行中のサービスを停止**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **サービスをアンインストール**
   ```bash
   uninstall_service.bat
   ```

これで digna サーバーは Windows サービスから登録解除されます。

---

## 新しいリリースへのアップグレード {: #upgrading-to-a-new-release }

### アップグレード前の準備

**digna リポジトリのバックアップは必須です**

アップグレード前にリポジトリ（PostgreSQL）のバックアップを必ず作成し、データ損失に備えてください。バックアップがあれば、アップグレードで予期せぬ問題が発生した場合に復旧できます。

### アップグレード手順

#### ステップ 1: digna サービスを停止

digna を Windows サービスとして実行している場合は、先に停止します:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### ステップ 2: 現在のバックエンドのバックアップ

digna インストールディレクトリで:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### ステップ 3: 新バージョンの展開とデプロイ

1. 新しい digna インストール ZIP ファイルを展開
2. 新しい `digna` 実行ファイル、`dashboard` フォルダをインストールディレクトリにコピー

> **重要**
>
> `config.toml` ファイルはインストール ZIP に含まれていません。既存の設定はそのまま保持されます。

### ステップ 4: 設定ファイルの復元

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

### ステップ 5: リポジトリスキーマのアップグレード

digna インストールディレクトリに移動し、次を実行:

```bash
digna repo upgrade
```

このコマンドは PostgreSQL スキーマを最新バージョンに更新し、既存データを保持します。

### ステップ 6: サービスの再起動

Windows サービスとして運用している場合:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

手動実行している場合はサーバーを再起動:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

IIS や Tomcat を使用している場合は、それぞれの Web サーバーを再起動してください。

#### ステップ 7: アップグレードの検証

1. digna ダッシュボードにアクセス
2. インターフェースが正しく読み込まれることを確認
3. サーバーログにエラーがないか確認してください

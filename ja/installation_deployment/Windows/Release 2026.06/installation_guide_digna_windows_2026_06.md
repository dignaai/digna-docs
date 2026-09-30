# Windows インストールガイド — digna リリース 2026.06

**リリース:** 2026.06

**最終更新日:** 2026年8月30日


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

### リリース 2026.06 の新機能

このリリースでは、データオブザーバビリティ機能をコードに直接組み込めるようになり、開発者がソースでデータ品質を監視できるようになりました。完全な詳細は[リリースノート](http://docs.digna.ai/changelog/Release_202606/)を参照してください。

### macOS や Linux をお探しですか？

本ガイドは Windows 向けです。他のプラットフォームについては、[macOS インストールガイド](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) や [Linux インストールガイド](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md) を参照してください。

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

このセクションは digna バックエンドアプリケーションの設定を行います:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | フロントエンドの URL | ダッシュボードが別サーバーにある場合はその URL を含める |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | クレデンシャル付き CORS のために必要 |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | すべての HTTP メソッドを許可 |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | すべてのヘッダーを許可 |

#### [repo] セクション

このセクションは PostgreSQL データベースへの接続を設定します:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `digna_REPO_HOST` | `localhost` または IP | PostgreSQL サーバーのホスト名/IP |
| `digna_REPO_PORT` | `5432`（デフォルト） | PostgreSQL のポート |
| `digna_REPO_DB` | `postgres` | データベース名 |
| `digna_REPO_SCHEMA` | `dignarepo` | 先に作成したスキーマ |
| `digna_REPO_USER` | `digna_user` | PostgreSQL セットアップで作成したユーザー |
| `digna_REPO_PASSWORD` | あなたのパスワード | スキーマ作成時に設定したパスワード |

#### [base] セクション

このセクションはセキュリティとクッキーの設定を含みます:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | フロントエンドのドメインに合わせて設定 |
| `digna_COOKIE_SECURE` | `false`（ローカル） / `true`（本番） | HTTPS 接続では `true` を使用 |
| `digna_COOKIE_HTTPONLY` | `true` | セキュリティのため常に有効推奨 |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF 攻撃を防止 |
| `digna_TOKEN_EXPIRES_IN` | `86400`（24 時間） | セッションの有効期限（秒） |
| `digna_MAX_WORKERS` | CPU コア数 - 1 | 並列検査タスクの数 |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | スケジューラーが実行予定のジョブを開始する前に追加できる最大の遅延（秒） |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | 日次クリーンアップが開始される時刻（24 時間表記 `HH:MM`） |

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` または `DEBUG` | 本番では `INFO`、トラブルシューティング時は `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | 保持する日次ログバックアップの数 |

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

Overall: OK
```

FAILED と報告された箇所をすべて修正し、続行する前にコマンドを再実行してください。オプションの完全な一覧は [CLI リファレンス](../../../cli/Command_Line_Interface_202606.md)にあります。

### ステップ 3: リポジトリの初期接続確認

1. コマンドプロンプトを開く
2. digna のインストールディレクトリ（`config.toml` と `digna` 実行ファイルがある場所）に移動
3. 接続テストを実行:

```bash
digna repo check
```

接続が確立されたという確認メッセージが表示されます（リポジトリ自体はまだ初期化されていません）。

### ステップ 4: リポジトリスキーマのインストール

同じディレクトリで次を実行します:

```bash
digna repo install
```

このコマンドは、PostgreSQL データベースに必要なテーブルとスキーマをインストールします。

### ステップ 5: 管理者ユーザーを作成

1. 新しいコマンドプロンプトウィンドウを開く
2. digna インストールディレクトリに移動
3. 管理者ユーザーを作成するコマンドを実行:

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

---

### ステップ 6: digna サーバーを起動

digna インストールディレクトリで、サーバーを次のように起動します:

```bash
digna serve --address <host> --port <port>
```

**パラメータ:**
- `--address` — サーバーのホスト名/IP
- `--port` — サーバーのポート

サーバーが起動していることを示すメッセージが表示されます:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "サーバーはターミナルを占有します"

    `serve` はフォアグラウンドで実行され、++ctrl+c++ で停止するまで動作し続けます。セットアップを終えるまで実行したままにしてください。起動時に自動的に開始する方法は次を参照してください: [digna を Windows サービスとして実行する](#running-digna-as-a-windows-service).

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

どのコマンドも `--name` を受け付け、既定以外の名前で登録したサービスを指定できます。オプションの完全な一覧は [CLI リファレンス](../../../cli/Command_Line_Interface_202606.md) にあります。

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

### アップグレード前に

**最初にすべてのデータベース接続を確認する**

リリース 2026.06 から、digna はすべてのソース技術に **ODBC** 経由で接続します。以前のリリースでは、技術ごとの専用ドライバーと ODBC を **Use ODBC** スイッチで選択できました。digna チームは ODBC のみを基盤とすることを決めました。単一の標準インターフェイスは、個別に作り込まれたドライバー群よりも多くをもたらすからです:

- **認証** — 認証は ODBC の一部であるため、接続はドライバーが対応するあらゆる方式を利用できます。パスワード、トークンと PAT、Kerberos と Active Directory、MFA とブラウザーベースのシングルサインオン、クラウド ID、クライアント証明書、TLS などです。新しい方式は digna のリリースを待つのではなく、ドライバーの更新とともに利用できるようになります。
- **データベースベンダーが保守するドライバー** — ベンダー自身のドライバーが新しいサーバーバージョンとセキュリティ修正に追随し、digna とは独立に、ご自身の都合に合わせて更新できます。
- **すべてを同じ方法で構成できる** — どの技術もキーと値のプロパティの一覧であり、同じインターフェイス、同じ機密値の暗号化、同じトラブルシューティングを使います。ソースごとに異なる入力欄が並ぶことはありません。
- **調整と適用範囲** — タイムアウト、TLS 設定、プロキシ、フェッチサイズといったドライバーレベルのオプションがすべてのソースで利用でき、準拠した ODBC ドライバーがある技術であれば、digna が個別のガイドを公開していないものも含めて接続できます。

実際には、**Use ODBC** スイッチと、ホスト・ポート・データベース・ユーザー・パスワードの個別の入力欄はなくなりました。**すでに ODBC を使っていない接続はすべて ODBC へ移行する必要があります**。自動変換はありませんので、アップグレード前に計画してください:

1. インストールに定義されている各データベース接続を確認し、まだ ODBC を使っていないものを書き出してください。いずれも再構成が必要です。
2. 対応する ODBC ドライバーを digna ホストにインストールします。接続はブラウザーからではなく、digna バックエンドを実行しているサーバーから開かれます。参照: [digna ホストへの ODBC ドライバーのインストール](../../../databases/overview.md#install-the-driver)。
3. 影響を受ける各接続の ODBC プロパティを用意してください。 [技術別ガイド](../../../databases/overview.md#technology-guides)には、ソースごとに実績のあるプロパティ一式が記載されています。

アップグレード後、影響を受けた各接続を ODBC に切り替え、ダッシュボードからテストしてください。参照: [データベース接続の作成](../../../databases/overview.md#create-a-database-connection) および [接続のテスト](../../../databases/overview.md#testing-a-connection)。

!!! warning "Databricks Legacy 接続"

    Databricks Legacy コネクタは本リリースで削除されました。該当する接続は [Databricks](../../../databases/databricks_connector_guide.md) コネクタへ移行してください。

**digna リポジトリのバックアップ作成は必須です**

アップグレードの前に、リポジトリ（PostgreSQL）を必ずバックアップしてください。バックアップは、アップグレード中に予期しない問題が発生した場合の復旧に必要です。

### アップグレード手順

#### ステップ 1: 古いサービスを停止して登録を解除する

digna を Windows サービスとして実行している場合は、**現在のインストールのバッチファイル**で停止します。`digna windows` コマンドは新しいリリースに含まれるもので、この時点ではまだ使用できません:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

続いて、同じく古いバッチファイルでサービスの登録を解除します。登録情報は古い実行ファイルとそのスクリプトを指しており、どちらもこのアップグレードで置き換えられるため、再利用できません:

```bash
uninstall_service.bat
```

!!! warning "名前を変更する前に登録を解除してください"

    `uninstall_service.bat` はこれから名前を変更する `bin` フォルダーにあり、自身が作成した登録情報を削除できるのはこのファイルだけです。古いインストールがまだそのままの状態で実行してください。すでにフォルダー名を変更してしまった場合は、元の名前に戻して登録を解除してから続行してください。

    サービスの実行アカウントと、サービスが使用していたアドレスとポートを控えておいてください — ステップ 9 で必要になります。

#### ステップ 2: 現在のインストールをバックアップする

digna のインストールディレクトリで、新しいリリースを並べて配置できるよう、現在のインストールのフォルダー名を変更します:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend と dignacli は使用されなくなりました"

    リリース 2026.06 から、`dignabackend` と `dignacli` は、バックエンドと CLI を統合した単一の実行ファイル `digna` に置き換えられます。`dignabackend_old` と `dignacli_old` はアップグレードを確認するまで残し、その後は両方とも削除してかまいません。`dashboard_old` は、そこから構成ファイルを復元するまで残してください（手順 4 を参照）。`bin` フォルダーも不要になります。そのバッチファイルは古いサービスを操作するためのもので、2026.06 には同梱されていません。ステップ 1 でサービスの登録を解除した後は、誤解を招くだけです。

#### ステップ 3: 新バージョンを展開してデプロイ

1. 新しい digna インストール ZIP ファイルを展開
2. 新しい `digna` 実行ファイルと `dashboard` フォルダをインストールディレクトリにコピー

!!! warning "重要"

    `config.toml` も `dashboard/dashboard_config.toml` も、インストール ZIP に含まれることは**決して**ありません。digna チームはどちらのファイルも配布しません。そのため既存の設定はアップグレードの影響を受けず、名前を変更した `*_old` フォルダー内のコピーが手元にある唯一の設定になります。

#### ステップ 4: 設定ファイルの復元

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

!!! warning "リリース 2026.06 で config.toml が変わります"

    3 つの設定が新たに必須となり、3 つは使用されなくなりました。以前のリリースから引き継いだ `config.toml` には新しい設定が含まれておらず、それらが欠けている限り digna は起動しません。既存の `config.toml` に次を追加してください:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    2 つの `[base]` キーを既存の `[base]` セクションに追加し、`[encryption]` を新しいセクションとして追加します。そのうえで、使用されなくなった設定を削除してください。`[base]` から **`digna_FERNET_KEY`**、`[app]` から **`digna_APP_HOST`** と **`digna_APP_PORT`** です。サーバーのアドレスとポートは `digna serve` から渡すようになりました。

    各設定の役割については次を参照してください: [バックエンド構成](#backend-configuration).

!!! warning "シングルサインオン: [oidc_clients] の形式が変わりました"

    リリース 2026.06 では、テーブルの配列が、プロバイダーごとに 1 つのテーブルへ置き換わりました。テーブル名はプロバイダーのキーになります。`DIGNA_OIDC_KEY` は廃止され、キーはセクション見出しの一部になりました。

    変更前:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    変更後:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    プロバイダーごとにこのセクションを繰り返し、各キーを `dashboard_config.toml` の `key` と一致させてください。古い形式が残っている間、`digna config check` は `oidc_clients` を FAILED と報告します。影響を受けるのはシングルサインオンを使用しているインストールのみです。

#### ステップ 5: Web サーバーをリロードする

ダッシュボードは静的ファイルの集まりであるため、Web サーバー（およびブラウザー）が以前のバージョンを配信し続けている可能性があります。`dashboard` フォルダーをホストしている Web サーバーをリロードまたは再起動し、ページをハードリフレッシュ（++ctrl+f5++）で再読み込みしてください。

#### ステップ 6: 構成を検証する

リポジトリに手を加える前に、更新した `config.toml` が完全であることを確認します:

```bash
digna config check
```

すべてのセクションが OK と報告される必要があります。FAILED と報告された箇所を修正し、続行する前にコマンドを再実行してください。

#### ステップ 7: ライセンスファイルを置き換える

ライセンスはリリースごとに個別に発行されます。digna チームがこのリリース用に提供した `license.toml` をインストールディレクトリにコピーし、古いものを置き換えます:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "以前のライセンスを使い続けないでください"

    以前のリリース向けに発行された `license.toml` はこのリリースには適用されません。ライセンスを確認するすべてのコマンド（`user`、`inspection`、`repo`）は、確認に失敗するとリポジトリに手を加える前に中止されます。先に進む前にライセンスを確認してください:

    ```bash
    digna license check
    ```

#### ステップ 8: リポジトリスキーマのアップグレード

digna インストールディレクトリに移動して次を実行:

```bash
digna repo upgrade
```

これにより、既存データを保持しつつ PostgreSQL スキーマが最新バージョンに更新されます。

#### ステップ 9: サービスを登録して開始する

古い登録情報はステップ 1 で削除されたため、サービスを再度登録します。今回はバッチファイルを持たない `digna` 実行ファイルを使います:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

新しい既定値の `127.0.0.1` と `8000` を使う場合を除き、`--address` と `--port` には古いサービスが使用していた値を指定してください。これらは登録情報に記録され、`config.toml` からは読み込まれなくなりました。古いサービスがドメインアカウントで実行されていた場合は、`--account` と `--password` を追加してください。オプションの完全な一覧は
[digna を Windows サービスとして実行する](#running-digna-as-a-windows-service) を参照してください。

手動で実行している場合は、サーバーを再起動します:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

IIS や Tomcat を使用している場合は、それぞれの Web サーバーを再起動してください。

#### ステップ 10: アップグレードの確認

1. digna ダッシュボードにアクセス
2. インターフェースが正しく読み込まれることを確認
3. サーバーログにエラーがないか確認してください
4. まだ ODBC を使っていなかった接続をすべて ODBC に切り替え、そのうえですべての接続をテストします。参照: [接続のテスト](../../../databases/overview.md#testing-a-connection)
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

- **dignabackend**: データ処理と品質チェックを行うアプリケーションのコアエンジン。
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
   - `config.toml` — 設定ファイル
   - `license.toml` — ライセンスファイル（別途自分のファイルをここにコピー）

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
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `digna_APP_HOST` | `localhost` または IP アドレス | dignabackend がホストされるホスト名または IP |
| `digna_APP_PORT` | `8082`（デフォルト） | REST API エンドポイント用のポート |
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
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `digna_FERNET_KEY` | 暗号化キー | トークンやクッキーの暗号化に使用（デフォルトが提供されることがあります） |
| `digna_COOKIE_DOMAIN` | `localhost` | フロントエンドのドメインに合わせて設定 |
| `digna_COOKIE_SECURE` | `false`（ローカル） / `true`（本番） | HTTPS 接続では `true` を使用 |
| `digna_COOKIE_HTTPONLY` | `true` | セキュリティのため常に有効推奨 |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF 攻撃を防止 |
| `digna_TOKEN_EXPIRES_IN` | `86400`（24 時間） | セッションの有効期限（秒） |
| `digna_MAX_WORKERS` | CPU コア数 - 1 | 並列検査タスクの数 |

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

### ステップ 5: digna サーバーを起動

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

### ステップ 6: 管理者ユーザーを作成

1. 新しいコマンドプロンプトウィンドウを開く
2. digna インストールディレクトリに移動
3. 管理者ユーザーを作成するコマンドを実行:

```bash
digna user add <username> "<full_name>" <password> --su
```

**例:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

これで完全な管理権限を持つユーザーが作成されます。

!!! tip "ベストプラクティス"

    大文字・小文字・数字・特殊文字を組み合わせた強力なパスワードを使用してください。

---

## ダッシュボードの設定 {: #dashboard-configuration }

### ステップ 1: ダッシュボードを Web サーバーにデプロイ

digna ダッシュボードには `dashboard/` ディレクトリ内に独自の `config.toml` ファイルがあります。この設定ファイルは既に提供されており、初期セットアップ時に変更する必要はありません。バックエンド接続をカスタマイズする場合のみ設定を変更してください。

ダッシュボードの設定を変更する必要がある場合（例えばマルチインスタンス構成など）は、ダッシュボードのドキュメントを参照してください。

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

### サービス管理用ファイル

必要なファイルはすべて digna インストールディレクトリの下の `bin/` にあります。

利用可能なバッチファイル:
- `install_service.bat` — digna を Windows サービスとして登録する
- `uninstall_service.bat` — サービスの登録を解除する
- `start_service.bat` — サービスを開始する
- `stop_service.bat` — サービスを停止する

!!! warning "管理者権限が必要"

    すべてのバッチファイルは管理者権限で実行する必要があります。

### サービスのインストール

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

digna サーバーは自動起動設定で Windows サービスとして登録されます。サービスは即時に開始されません — 次のセクションを参照して起動してください。

### サービスの開始と停止

#### サービスを開始するには

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

!!! tip "ヒント"

    アプリケーションファイルを更新する前には必ずサービスを停止してください。

### サービスを新しいディレクトリに移動する場合

digna のインストールを移動する必要がある場合:

1. **現在のサービスをアンインストール**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **アプリケーションファイルを移動**
   - digna インストールフォルダ全体を新しい場所に移動

3. **サービスを再インストール**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **サービスを開始**
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

これで digna サーバーは Windows サービスとしての登録が解除されます。

---

## 新しいリリースへのアップグレード {: #upgrading-to-a-new-release }

### アップグレード前に

**digna リポジトリのバックアップ作成は必須です**

アップグレードの前に、リポジトリ（PostgreSQL）を必ずバックアップしてください。バックアップは、アップグレード中に予期しない問題が発生した場合の復旧に必要です。

### アップグレード手順

#### ステップ 1: digna サービスを停止

digna を Windows サービスとして実行している場合は、まず停止します:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### ステップ 2: 現在のバックエンドをバックアップ（名前変更）

digna インストールディレクトリで:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### ステップ 3: 新バージョンを展開してデプロイ

1. 新しい digna インストール ZIP ファイルを展開
2. 新しい `digna` 実行ファイルと `dashboard` フォルダをインストールディレクトリにコピー

!!! warning "重要"

    `config.toml` ファイルはインストール ZIP に**決して**含まれていません。既存の設定は保持されます。

### ステップ 4: 設定ファイルの復元

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

### ステップ 5: リポジトリスキーマのアップグレード

digna インストールディレクトリに移動して次を実行:

```bash
digna repo upgrade
```

これにより、既存データを保持しつつ PostgreSQL スキーマが最新バージョンに更新されます。

### ステップ 6: サービスの再起動

Windows サービスとして実行している場合:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

手動で実行している場合は、サーバーを再起動します:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

IIS や Tomcat を使用している場合は、それぞれの Web サーバーを再起動してください。

#### ステップ 7: アップグレードの確認

1. digna ダッシュボードにアクセス
2. インターフェースが正しく読み込まれることを確認
3. サーバーログにエラーがないか確認してください
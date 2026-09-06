# macOS インストールガイド（digna Release 2026.06）

**リリース:** 2026.06

**最終更新日:** 2026年9月5日


---

## 目次

1. [導入](#introduction)
2. [システム要件](#system-requirements)
3. [事前準備](#pre-installation-setup)
4. [PostgreSQL サーバーのセットアップ](#postgresql-server-setup)
5. [Web サーバーの設定](#web-server-configuration)
6. [初期インストール](#initial-installation)
7. [バックエンド構成](#backend-configuration)
8. [ダッシュボード構成](#dashboard-configuration)
9. [digna をバックグラウンドサービスとして実行する](#running-digna-as-a-background-service)
10. [新しいリリースへのアップグレード](#upgrading-to-a-new-release)

---

## 導入 {: #introduction }

### digna について

digna は、データウェアハウス、データレイク、レイクハウスなどさまざまなデータ環境でのデータ品質管理を最適化するために設計された包括的な AI 駆動プラットフォームです。高いスケーラビリティと適応性を備え、自動化、リアルタイム監視、異常検知を通じて現代のデータ課題に対応します。

digna は主に二つのコンポーネントで構成されています:

- **dignabackend**: データ処理と品質チェックを担当するアプリケーションのコアエンジン
- **dignadashboard**: Web サーバー上でホストされるウェブベースのインターフェースで、digna プラットフォームと対話し、データ品質指標を可視化するためのユーザーフレンドリーな画面を提供します

### Release 2026.06 の新機能

このリリースでは、データ可観測性（data observability）機能をコード内に直接取り込むことで、開発者がソースでデータ品質を監視できるようになりました。完全な詳細は [release notes](http://docs.digna.ai/changelog/Release_202606/) を参照してください。

### Windows や Linux をお探しですか？

本ガイドは macOS 向けです。他のプラットフォームについては、[Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) または [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md) を参照してください。

---

## システム要件 {: #system-requirements }

インストールを開始する前に、システムが以下の最小要件を満たしていることを確認してください。

| 要件 | 仕様 |
|---|---|
| **オペレーティングシステム** | macOS 13 (Ventura) 以降 |
| **アーキテクチャ** | Apple Silicon (arm64) または Intel (x86_64) |
| **メモリ（最小構成）** | 16 GB RAM |
| **ディスク容量** | 10 GB の空きストレージ |
| **データベース** | PostgreSQL Server 12 以上 |
| **Web サーバー** | nginx、Apache httpd、または同等 |
| **コマンドラインツール** | Xcode Command Line Tools（Homebrew が必要とするため） |

### データベースのインストールオプション

**PostgreSQL が既にインストールされている場合:**
既存の PostgreSQL サーバーに digna 用の新しいデータベース（スキーマ）を追加できます。

**digna と同じマシンに PostgreSQL をインストールする場合:**

!!! info "推奨仕様"

    - **メモリ**: 32 GB RAM（16 GB の代わりに推奨）
    - **ディスク容量**: 50 GB の空きストレージ（10 GB の代わりに推奨）

    これらの高い仕様は、digna と PostgreSQL データベースの両方を同時に稼働させることを想定しています。

### アーキテクチャの確認

このガイドのいくつかのパスは Apple Silicon と Intel の Mac で異なります。どちらのマシンかを確認するには、**Terminal** を開いて次を実行してください:

```bash
uname -m
```

- `arm64` — Apple Silicon。Homebrew は `/opt/homebrew` にインストールされます。
- `x86_64` — Intel。Homebrew は `/usr/local` にインストールされます。

!!! tip "ヒント"

    どちらかのパスをハードコーディングする代わりに、このガイドでは `$(brew --prefix)` を使用します。これは両方のアーキテクチャで正しい場所に展開されます。コマンドはそのままコピーして使えます。

---

## 事前準備 {: #pre-installation-setup }

digna をインストールする前に、次の 3 つの主要な前提条件が整っていることを確認してください:

1. **Homebrew** – 本ガイドで以下のコンポーネントをインストールするためのパッケージマネージャ
2. **PostgreSQL Server** – 計算されたメトリクスやパフォーマンスデータを格納するため
3. **Web サーバー** – digna ダッシュボードをホストするため

これらのコンポーネントがまだセットアップされていない場合は、以下のセクションに従ってインストールおよび構成してください。

### Homebrew のインストール

Homebrew は macOS の標準パッケージマネージャで、本ガイド全体で PostgreSQL や nginx をインストールするために使用します。

#### ステップ 1: Homebrew が既にインストールされているか確認する

**Terminal** を開き（`Cmd + Space` を押して `Terminal` を入力し、Enter）、次を実行します:

```bash
brew --version
```

バージョン番号が返ってきたら、[PostgreSQL サーバーのセットアップ](#postgresql-server-setup) セクションへ進んでください。

#### ステップ 2: Homebrew をインストールする

コマンドが見つからない場合は、[公式 Homebrew サイト](https://brew.sh) の指示に従って Homebrew をインストールしてください。インストーラーは Xcode Command Line Tools をまだインストールしていない場合、それもインストールします。

#### ステップ 3: Homebrew を PATH に追加する

Apple Silicon では、インストーラーがシェル環境に Homebrew を追加するための 2 つのコマンドを表示します。指示に従ってそれらを実行し、次で確認してください:

```bash
brew --prefix
```

Apple Silicon では `/opt/homebrew`、Intel では `/usr/local` が表示されるはずです。

---

## PostgreSQL サーバーのセットアップ {: #postgresql-server-setup }

### 既に PostgreSQL をお使いの場合

ローカルマシンで PostgreSQL が既にインストールおよび稼働している、または管理されたリモート PostgreSQL サーバーを使用している場合は、[次のセクション](#web-server-configuration)へ進んでください。

### インストールの選択肢

macOS では PostgreSQL のインストール方法が二通りあります。どちらか一方を選んでください:

- [Homebrew](#postgresql-homebrew) — コマンドラインでのインストール、サーバー展開に推奨
- [Postgres.app](#postgresql-app) — GUI ベースのインストール、ローカル評価に便利

### Homebrew で PostgreSQL をインストールする {: #postgresql-homebrew }

#### ステップ 1: PostgreSQL フォーミュラをインストール

```bash
brew install postgresql@16
```

#### ステップ 2: PostgreSQL を PATH に追加

バージョン付きの PostgreSQL フォーミュラは *keg-only* であり、Homebrew は自動的にコマンドを PATH にリンクしません。自分で追加してください:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "注意"

    これは macOS のデフォルトの `zsh` シェルを想定しています。`bash` を使用している場合は、同じ行を `~/.bash_profile` に追加してください。

#### ステップ 3: PostgreSQL サービスを起動

```bash
brew services start postgresql@16
```

これにより PostgreSQL が直ちに起動し、ログイン時に自動で再起動するように設定されます。

#### ステップ 4: インストールを確認

```bash
psql --version
```

インストールが成功していれば PostgreSQL のバージョンが表示されます。

#### ステップ 5: サーバーに接続

```bash
psql postgres
```

!!! warning "重要 — macOS はここで Windows と異なります"

    Windows のインストーラーは `postgres` というスーパーユーザーとパスワードを作成するよう促します。Homebrew はそれを行いません。代わりに、macOS のアカウント名と同じ名前のスーパーユーザーを作成し、パスワードは設定されずローカルマシンからのみアクセス可能です。

    つまり、新規の Homebrew インストールには `postgres` ロールが存在しません。スーパーユーザーが必要な場合は自分のアカウント名を使用し、[Initial Installation](#initial-installation) に記載されているように明示的に digna 用ユーザーを作成してください。

#### ステップ 6: ポートの確認

デフォルトの PostgreSQL ポートは `5432` です。サーバーがどのポートで待ち受けているか確認するには:

```bash
psql postgres -c "SHOW port;"
```

この値をメモしておいてください — digna バックエンドの設定時に必要になります。

### Postgres.app を使って PostgreSQL をインストールする {: #postgresql-app }

GUI によるインストールを好む場合:

1. [Postgres.app](https://postgresapp.com) をダウンロードして **Applications** フォルダにドラッグします
2. アプリを開き **Initialize** をクリックして新しいサーバーを作成します
3. アプリの指示に従い、コマンドラインツールを PATH に追加します
4. インストールを確認します:

```bash
psql --version
```

Postgres.app も macOS のアカウント名を持つスーパーユーザーを作成します。

---

## Web サーバーの設定 {: #web-server-configuration }

digna はダッシュボードをホストするために Web サーバーを必要とします。次のいずれかを選択してください:

- [nginx](#nginx-setup) — Homebrew 経由でインストール、推奨
- [Apache httpd](#apache-setup) — macOS に同梱

いずれか一方のサーバーだけをインストールして構成すれば十分です。

両方のセクションではダッシュボードが依存する以下の 2 点を設定します:

- **シングルページアプリケーション（SPA）フォールバック** — ダッシュボードの URL を更新しても 404 にならないようにする
- **`.md` の MIME タイプ** — Markdown ファイルを正しく配信する

### nginx のセットアップ {: #nginx-setup }

#### 概要

nginx は軽量で高性能の Web サーバーで、静的な digna ダッシュボードの配信に適しています。

#### インストール

```bash
brew install nginx
```

#### nginx の起動

```bash
brew services start nginx
```

#### インストール確認

1. ブラウザを開く
2. `http://localhost:8080` にアクセス
3. nginx のウェルカムページが表示されるはずです

!!! note "注意 — デフォルトポートは 8080（80 ではない）"

    Homebrew は nginx を管理者権限なしで実行できるようにポート `8080` をリッスンするように設定します。macOS でポート `80` や 1024 未満のポートをバインドするには root 権限が必要です。

    ダッシュボードをポート 80 で提供するには、以下の設定で `listen 8080;` を `listen 80;` に変更し、`sudo brew services start nginx` で起動してください。

#### ダッシュボード用サイトの設定

Homebrew の nginx 設定は `servers` ディレクトリ内のすべてのファイルを読み込みます。そこに digna 用の専用設定ファイルを作成してください:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

以下を貼り付け、`/path/to/digna/dashboard` を展開した `dashboard` フォルダへの実際のパスに置き換えてください:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "重要"

    `try_files` ディレクティブがないと、ルート URL 以外のダッシュボードページをリロードすると 404 が返されます。これは Windows の IIS で必要な URL Rewrite モジュールに相当します。

#### 設定の適用

構文エラーがないかテストしてから nginx をリロードします:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd のセットアップ {: #apache-setup }

#### 概要

macOS には Apache httpd が同梱されていますので、インストールは不要です。デフォルトでは無効になっています。

#### Apache の起動

```bash
sudo apachectl start
```

#### インストール確認

1. ブラウザを開く
2. `http://localhost` にアクセス
3. "It works!" というメッセージが表示されるはずです

#### 必須: mod_rewrite を有効にする

ダッシュボードは URL の書き換えを必要とします。Apache 設定を開いてください:

```bash
sudo nano /etc/apache2/httpd.conf
```

以下の行を探して、先頭の `#` を削除してコメント解除します:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### 必須: .htaccess のオーバーライドを許可する

同じファイル内の `<Directory "/Library/WebServer/Documents">` ブロックを見つけ、次を変更してください:

```apache
AllowOverride None
```

から:

```apache
AllowOverride All
```

#### 必須: Markdown ファイルの MIME タイプ

同じ `httpd.conf` に次の行を追加して、Markdown ファイルが正しく配信されるようにします:

```apache
AddType text/markdown .md
```

!!! warning "重要"

    この設定がないと `.md` ファイルが正しく配信されない場合があります。

#### 設定の適用

構成の文法チェックを行い、Apache を再起動します:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## 初期インストール {: #initial-installation }

### ステップ 1: digna リポジトリのセットアップ

digna リポジトリは、digna によって計算されるすべてのメトリクスを格納します。分析データやパフォーマンスデータの中央データベースとして機能します。

#### リポジトリ用スキーマとユーザーの作成

PostgreSQL クライアント（psql、pgAdmin など）を開き、以下の SQL コマンドを実行してください:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**以下のプレースホルダを置き換えてください:**

- `<digna_repo_schema>` — 希望するスキーマ名（例: `dignarepo`）
- `<digna_repo_user>` — 希望するユーザー名（例: `digna_user`）
- `<digna_repo_password>` — このユーザー用の安全なパスワード

**例:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Terminal から一度に実行するには:

```bash
psql postgres
```

その後 `postgres=#` プロンプトに上記のステートメントを貼り付け、終了するには `\q` を入力してください。

!!! tip "ベストプラクティス"

    データベースユーザーには強力で複雑なパスワードを使用してください。推測されやすい認証情報は避けてください。

---

### ステップ 2: digna インストールパッケージの展開

1. 提供された digna インストール ZIP ファイルを見つけます
2. 希望するインストール場所（例: `/opt/digna` または `~/digna`）に展開します
3. 展開後、以下のアイテムがあるはずです:
   - `dashboard/` — Web ダッシュボードインターフェース
   - `digna` — メイン実行ファイル（バックエンド + CLI 統合）
   - `config.toml` — 設定ファイル
   - `license.toml` — ライセンスファイル（別途提供されたものをここにコピー）

Terminal から展開するには:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### 実行可能ファイルに実行権を付与する

アーカイブの転送方法によっては、実行ビットが失われることがあります。明示的に設定してください:

```bash
cd /opt/digna
chmod +x digna
```

#### macOS がアプリケーションをブロックする場合

ブラウザやメールクライアント経由でダウンロードされたファイルには検疫属性が付けられます。macOS が「開発元を確認できないため開けません」と報告する場合は、インストールディレクトリから属性を削除してください:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

または、**System Settings → Privacy & Security** を開き、ページ下部にあるブロックされた項目を見つけて **Open Anyway** をクリックしてください。

!!! note "注意"

    この手順は、macOS が実際に実行ファイルをブロックした場合にのみ必要です。SSH で転送されたパッケージや内部ファイル共有からのファイルは通常検疫されません。

### ステップ 3: ライセンスファイルのインストール

!!! warning "重要"

    ライセンスファイルはインストールパッケージに含まれておらず、digna から別途提供されます。

1. 提供された `license.toml` ファイルを見つけます
2. それを digna インストールのルートディレクトリ（`config.toml` と `digna` 実行ファイルがある場所）にコピーします

**理由:**
ライセンスファイルには顧客情報、ライセンス有効期限、デジタル署名が含まれます。**ファイルを変更しないでください** — 変更すると無効になります。

**セットアップ後のディレクトリ構成:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## バックエンド構成 {: #backend-configuration }

### ステップ 1: 設定ファイルの作成と編集

`config_template.toml` ファイルが digna インストールディレクトリに同梱されています。これを `config.toml` にリネームしてください。

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**場所:** `/opt/digna/config.toml`

テキストエディタで `config.toml` を開き、以下の各セクションを設定してください。

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
| `digna_APP_PORT` | `8082`（デフォルト） | REST API エンドポイントのポート |
| `digna_APP_CORS_ALLOW_ORIGINS` | フロントエンドの URL | ダッシュボードが別サーバーにある場合、その URL を含めてください |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | 認証情報付きの CORS に必要 |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | すべての HTTP メソッドを許可 |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | すべてのヘッダーを許可 |

!!! note "注意"

    Homebrew の nginx をデフォルトポートで提供している場合、許可すべきオリジンは `http://localhost:8080` です。

#### [repo] セクション

このセクションは PostgreSQL データベースへの接続を構成します:

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
| `digna_REPO_USER` | `digna_user` | PostgreSQL で作成したユーザー |
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
| `digna_FERNET_KEY` | 暗号化キー | トークンやクッキーの暗号化に使用（デフォルトが提供されます） |
| `digna_COOKIE_DOMAIN` | `localhost` | フロントエンドのドメインに合わせてください |
| `digna_COOKIE_SECURE` | `false`（ローカル） / `true`（本番） | HTTPS では `true` を使用 |
| `digna_COOKIE_HTTPONLY` | `true` | セキュリティのため常に有効にしてください |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF 攻撃を防ぐ設定 |
| `digna_TOKEN_EXPIRES_IN` | `86400`（24 時間） | セッションの有効期限（秒） |
| `digna_MAX_WORKERS` | CPU コア数 - 1 | 並列検査タスクの数 |

!!! tip "ヒント"

    Mac 上の CPU コア数を調べるには `sysctl -n hw.ncpu` を実行してください。

#### [logging] セクション

このセクションはログの動作を設定します:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` または `DEBUG` | 本番では `INFO`、トラブルシューティング時は `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | 保持する日次ログのバックアップ数 |

---

### ステップ 2: リポジトリの初期化

1. **Terminal** を開く
2. digna インストールディレクトリ（`config.toml` と `digna` 実行ファイルがある場所）に移動する
3. 接続テストを実行:

```bash
cd /opt/digna
./digna repo check
```

接続が確立されたことを示す確認メッセージが表示されるはずです（リポジトリ自体はまだ初期化されていません）。

!!! note "注意"

    macOS ではカレントディレクトリのコマンドが PATH に含まれないため、実行ファイルは `digna` ではなく `./digna` として呼び出します。短い形式で使いたい場合は、インストールディレクトリを PATH に追加してください:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### ステップ 3: リポジトリスキーマのインストール

同じディレクトリで次を実行します:

```bash
./digna repo install
```

このコマンドは PostgreSQL データベースに必要なテーブルとスキーマをインストールします。

### ステップ 4: digna サーバーの起動

digna インストールディレクトリでサーバーを起動します:

```bash
./digna serve --address <host> --port <port>
```

**パラメータ:**
- `--address` — サーバーのホスト名/IP
- `--port` — サーバーのポート

起動に成功すると次のようなメッセージが表示されます:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "ヒント"

    サーバーを最初に起動すると、macOS が外部からのネットワーク接続を受け入れるかどうかを尋ねることがあります。ダッシュボードがバックエンドに接続できるように **Allow** をクリックしてください。

### ステップ 5: 管理者ユーザーの作成

1. 新しい Terminal ウィンドウを開く
2. digna インストールディレクトリに移動
3. 管理者ユーザーを作成するために次のコマンドを実行:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**例:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

これにより、ユーザー名 `admin` で完全な管理権限を持つユーザーが作成されます。

!!! tip "ヒント"

    パスワードはシングルクォートで囲んでください。`zsh` は `!`、`$`、`*` などの文字を特殊扱いするため、クォートしないと意図したとおりに渡されないことがあります。

!!! tip "ベストプラクティス"

    大文字小文字、数字、特殊文字を組み合わせた強力なパスワードを使用してください。

---

## ダッシュボード構成 {: #dashboard-configuration }

### ステップ 1: ダッシュボードを Web サーバーにデプロイする

digna ダッシュボードには `dashboard/` ディレクトリ内に独自の `config.toml` ファイルがあります。この設定は初期セットアップ時に同梱されており、変更は通常不要です。バックエンド接続をカスタマイズする必要がある場合にのみ編集してください。

ダッシュボードの構成を変更する必要がある場合（例: マルチインスタンス構成）、ダッシュボードのドキュメントを参照してください。

使用する Web サーバーを選び、対応するデプロイ手順に従ってください。

#### nginx にデプロイする場合

[nginx セットアップ](#nginx-setup) に従った場合、サーバーブロックは既に `dashboard` フォルダを指しており、コピーは不要です。

1. **パスを確認する**
   - `$(brew --prefix)/etc/nginx/servers/digna.conf` を開く
   - `root` が展開した `dashboard` フォルダを指していることを確認する

2. **フォルダが読み取り可能であることを確認する**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **nginx をリロード**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **インストールのテスト**
   - ブラウザを開く
   - `http://localhost:8080`（または設定した URL）にアクセス
   - digna ダッシュボードのログインページが表示されるはずです

#### Apache httpd にデプロイする場合

1. **ダッシュボードをドキュメントルートにコピーする**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **リライトルールを追加する**

   配備先フォルダ内に `.htaccess` ファイルを作成して、ブラウザのリロード時にルート以外のルートが維持されるようにします:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   以下を貼り付けてください:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Apache を再起動**
   ```bash
   sudo apachectl restart
   ```

4. **ダッシュボードにアクセス**
   - ブラウザを開く
   - `http://localhost/digna` にアクセス
   - digna ダッシュボードのログインページが表示されるはずです

---

## digna をバックグラウンドサービスとして実行する {: #running-digna-as-a-background-service }

### サービスとして実行する理由

digna バックエンドをバックグラウンドサービスとして実行することで、以下が可能になります:

- マシン起動時に自動で開始する
- ターミナルウィンドウを開かずにバックグラウンドで実行される
- クラッシュした場合に自動で再起動される
- macOS のサービス管理ツール `launchctl` を使って管理できる

### サービス管理ファイル

必要なファイルはすべて digna インストールディレクトリの `bin/` にあります。

利用可能なシェルスクリプトは以下です:

- `install_service.sh` — digna を launchd に登録
- `uninstall_service.sh` — サービスの登録を解除
- `start_service.sh` — 登録済みサービスを起動
- `stop_service.sh` — 実行中のサービスを停止

!!! warning "管理者権限が必要"

    これらのスクリプトはすべて `sudo` で実行する必要があります。ブート時に開始するサービスを登録するには `/Library/LaunchDaemons` に書き込む必要があるためです。

### スクリプトに実行権を付与する

抽出時に実行ビットが保持されない場合があります。初回使用前に:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### サービスのインストール

1. **Terminal を開く**

2. **bin フォルダに移動**
   ```bash
   cd /opt/digna/bin
   ```

3. **インストールスクリプトを実行**
   ```bash
   sudo ./install_service.sh
   ```

これで digna サーバーは launchd に自動起動有効で登録されます。サービスはすぐには開始されません — 次のセクションで起動方法を説明します。

### サービスの起動と停止

#### サービスを開始するには

1. Terminal を開く
2. `/opt/digna/bin` に移動
3. 実行:
   ```bash
   sudo ./start_service.sh
   ```

#### サービスを停止するには

1. Terminal を開く
2. `/opt/digna/bin` に移動
3. 実行:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "ヒント"

    アプリケーションファイルを更新する前に必ずサービスを停止してください。

### サービスの確認

サービスが登録されて稼働しているか確認するには:

```bash
sudo launchctl list | grep digna
```

先頭にプロセス ID がある行はサービスが実行中であることを示します。先頭が `-` の場合は登録済みだが停止中です。

### インストール先ディレクトリを移動する場合

launchd は実行ファイルの絶対パスを保存するため、インストール先を移動する場合はサービスの再登録が必要です:

1. **現在のサービスをアンインストール**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **アプリケーションファイルを移動**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **サービスを再インストール**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **サービスを開始**
   ```bash
   sudo ./start_service.sh
   ```

### サービスのアンインストール

1. **実行中のサービスを停止**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **サービスをアンインストール**
   ```bash
   sudo ./uninstall_service.sh
   ```

これで digna サーバーは launchd から登録解除されます。

---

## 新しいリリースへのアップグレード {: #upgrading-to-a-new-release }

### アップグレード前に

**digna リポジトリのバックアップ作成は必須です**

アップグレード前にリポジトリ（PostgreSQL）のバックアップを取り、データ損失に備えてください。バックアップがあれば、アップグレード中に想定外の問題が発生しても復旧できます。

Terminal からバックアップを作成するには:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### アップグレード手順

#### ステップ 1: digna サービスを停止する

digna がバックグラウンドサービスとして動作している場合、まずそれを停止します:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

digna をフォアグラウンドで実行している場合は、そのターミナルウィンドウで `Ctrl + C` を押します。

#### ステップ 2: 現在のバックエンドをバックアップする

digna インストールディレクトリで:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### ステップ 3: 新バージョンを展開してデプロイする

1. 新しい digna インストール ZIP ファイルを展開
2. 新しい `digna` 実行ファイルと `dashboard` フォルダをインストールディレクトリにコピー
3. 実行ビットを復元し、必要なら検疫属性を削除:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "重要"

    `config.toml` ファイルはインストール ZIP に含まれていません。既存の設定は安全に保持されます。

### ステップ 4: 設定ファイルを復元する

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### ステップ 5: リポジトリスキーマをアップグレードする

digna インストールディレクトリに移動して次を実行:

```bash
cd /opt/digna
./digna repo upgrade
```

これにより PostgreSQL スキーマが最新バージョンに更新され、既存のデータは保持されます。

### ステップ 6: サービスを再起動する

バックグラウンドサービスとして実行している場合:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

手動で実行している場合はサーバーを再起動します:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

nginx や Apache を使用している場合は、それぞれの Web サーバーも再起動してください:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### ステップ 7: アップグレードの確認

1. digna ダッシュボードにアクセスする
2. インターフェースが正しく読み込まれることを確認する
3. サーバーログにエラーがないか確認する
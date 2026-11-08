# macOS インストールガイド（digna Release 2026.11）

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
7. [バックエンド構成](#backend-configuration)
8. [ダッシュボード構成](#dashboard-configuration)
9. [digna をバックグラウンドサービスとして実行する](#running-digna-as-a-background-service)
10. [新しいリリースへのアップグレード](#upgrading-to-a-new-release)

---

## 導入 {: #introduction }

### digna について

digna は、データウェアハウス、データレイク、レイクハウスなどさまざまなデータ環境でのデータ品質管理を最適化するために設計された包括的な AI 駆動プラットフォームです。高いスケーラビリティと適応性を備え、自動化、リアルタイム監視、異常検知を通じて現代のデータ課題に対応します。

digna は主に二つのコンポーネントで構成されています:

- **digna**: アプリケーションの中核であり、データの処理と品質チェックの実行を担います。バックエンドとコマンドラインインターフェイスを単一の実行ファイルに統合し、以前のリリースで別々だった `dignabackend` と `dignacli` を置き換えます。
- **dignadashboard**: Web サーバー上でホストされるウェブベースのインターフェースで、digna プラットフォームと対話し、データ品質指標を可視化するためのユーザーフレンドリーな画面を提供します

### Release 2026.11 の新機能

このリリースでは、digna Data Reconciliation、digna MCP Server を備えた digna Agentic、そして digna Engine が追加されました。digna Engine は digna の内部でデータをプロファイリングし、異なるデータベース技術間の参照整合性をチェックできます。詳細は[リリースノート](../../../changelog/Release_202611.md)を参照してください。

インストールに関しては、本リリースで新しいリポジトリのマイグレーション機構、digna Engine 用の `config.toml` のオプションの `[duckdb]` セクション、そして新しいライセンスファイルが導入されます。それぞれについては[アップグレードのセクション](#upgrading-to-a-new-release)で説明します。

### Windows や Linux をお探しですか？

本ガイドは macOS 向けです。他のプラットフォームについては、[Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) または [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md) を参照してください。

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

!!! info "digna Engine"

    プロファイリングの場所として digna Engine を使用するデータベース接続は、digna ホスト自体でプロファイリングされます。そのためのメモリとディスク容量を追加で見込んでください。参照: [\[duckdb\] セクション](#duckdb-section)。

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

!!! info "設定ファイルとライセンスファイルはパッケージに含まれていません"

    `config.toml` も `dashboard/dashboard_config.toml` もインストールパッケージには含まれていません。どちらも [バックエンド構成](#backend-configuration) と [ダッシュボード構成](#dashboard-configuration) でご自身で作成します。`license.toml` も同梱されていません。ステップ 3 で説明するとおり、digna から別途提供されます。

Terminal から展開するには:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
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

!!! note "注意"

    Homebrew の nginx をデフォルトポートで提供している場合、許可すべきオリジンは `http://localhost:8080` です。

!!! info "[app] セクションは省略可能です"

    リリース 2026.11 以降、両方のキー、そして `[app]` セクション全体を省略できます。リバースプロキシがダッシュボードとバックエンドを 1 つのオリジンで配信する場合は、これが適切な構成です。その場合、ブラウザーはクロスオリジンリクエストを行わず、デフォルトではいずれも許可されません。

#### [repo] セクション

このセクションは PostgreSQL データベースへの接続を構成します:

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
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL で作成したユーザー |
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

!!! tip "ヒント"

    Mac 上の CPU コア数を調べるには `sysctl -n hw.ncpu` を実行してください。

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

このセクションはログの動作を設定します:

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

#### [duckdb] セクション（省略可能） {: #duckdb-section }

リリース 2026.11 の新機能です。このセクションでは **digna Engine** のリソースを設定します。digna Engine は、プロファイリングの場所が **digna Engine** であるデータベース接続について digna の内部でデータをプロファイリングし、異なるデータベース接続上のデータソース間で参照整合性チェックを実行します。参照: [プロファイリングの場所](../../../platform/profiling/profiling_location.md)。

このセクションは省略可能です。省略した場合は、以下のデフォルトが適用されます。

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| パラメータ | 値 | 備考 |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024`（デフォルト） | 1 回の digna Engine の実行が使用できるメモリ（MB）。同時に最大 `DIGNA_MAX_WORKERS` 個の実行がアクティブになります |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | デフォルト: システムの一時ディレクトリ（digna を実行するアカウントの `$TMPDIR`） | データがメモリに収まらない場合に一時ファイルを置くディレクトリ |

!!! tip "digna Engine のサイジング"

    digna 自体が使用するメモリに加えて、digna ホストに最大 `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` のメモリを見込んでください。また一時ディレクトリには、digna Engine を使用するデータソースのうち最大の検査対象日のデータを保持できるだけの空きディスク容量が必要です。`DIGNA_DUCKDB_TEMP_DIRECTORY` は、その容量があり、digna を実行するアカウントが書き込めるディスクを指すように設定してください:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    このセクションが必要なのは、少なくとも 1 つのデータベース接続が digna Engine を使用する場合、または参照整合性チェックが異なる接続上のデータソースを比較する場合のみです。

---

### ステップ 2: 構成を検証する

リポジトリを初期化する前に、`config.toml` が完全で正しく構成されていることを確認します。digna のインストールディレクトリで次を実行します:

```bash
./digna config check
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

### ステップ 3: リポジトリの初期化

1. **Terminal** を開く
2. digna インストールディレクトリ（`config.toml` と `digna` 実行ファイルがある場所）に移動する
3. 接続テストを実行:

```bash
cd /opt/digna
./digna repo check
```

新しいスキーマでは、コマンドは接続したうえで、リポジトリがまだインストールされていないことを報告します:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

この時点ではこれが想定どおりの結果で、digna が PostgreSQL とスキーマに到達できることを示しています。代わりに接続エラーや認証エラーが表示される場合は、`[repo]` セクションまたは PostgreSQL のセットアップに原因があります。

!!! note "注意"

    macOS ではカレントディレクトリのコマンドが PATH に含まれないため、実行ファイルは `digna` ではなく `./digna` として呼び出します。短い形式で使いたい場合は、インストールディレクトリを PATH に追加してください:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### ステップ 4: リポジトリスキーマのインストール

同じディレクトリで次を実行します:

```bash
./digna repo upgrade
```

このコマンドはリポジトリスキーマに必要なテーブルをインストールし、最後に次のように表示します:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade はインストールとアップグレードの両方を行います"

    リリース 2026.11 以降、`repo upgrade` は新しいリポジトリのインストールと既存のリポジトリのアップグレードの両方を行います。`repo install` も同じコマンドの別名として引き続き使用できます。

### ステップ 5: 管理者ユーザーの作成

管理者ユーザーはリポジトリスキーマに対して直接作成されるため、この時点でサーバーを起動しておく必要はありません。digna インストールディレクトリで次を実行します:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**例:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

これにより、メールアドレス `admin@example.com` の管理者権限を持つユーザーが作成されます。

!!! tip "ヒント"

    パスワードはシングルクォートで囲んでください。`zsh` は `!`、`$`、`*` などの文字を特殊扱いするため、クォートしないと意図したとおりに渡されないことがあります。

!!! tip "ベストプラクティス"

    大文字小文字、数字、特殊文字を組み合わせた強力なパスワードを使用してください。

### ステップ 6: digna サーバーの起動

digna インストールディレクトリでサーバーを起動します:

```bash
./digna serve --address <host> --port <port>
```

**パラメータ:**
- `--address` — サーバーのホスト名/IP（デフォルト `127.0.0.1`）
- `--port` — サーバーのポート（デフォルト `8000`）

サーバーが起動すると、待ち受けているアドレスが表示されます:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "ヒント"

    サーバーを最初に起動すると、macOS が外部からのネットワーク接続を受け入れるかどうかを尋ねることがあります。ダッシュボードがバックエンドに接続できるように **Allow** をクリックしてください。

!!! note "サーバーはターミナルを占有します"

    `serve` はフォアグラウンドで実行され、++ctrl+c++ で停止するまで動作し続けます。セットアップを終えるまで実行したままにしてください。起動時に自動的に開始する方法は次を参照してください: [digna をバックグラウンドサービスとして実行する](#running-digna-as-a-background-service).

---

## ダッシュボード構成 {: #dashboard-configuration }

### ステップ 1: ダッシュボードを Web サーバーにデプロイする

digna ダッシュボードは独自の設定を `dashboard/dashboard_config.toml` から読み込みます。このファイルはインストールパッケージに含まれていないため、`dashboard/` ディレクトリ内にダッシュボードのファイルと並べて作成します。

その内容は [シングルサインオン](../../../sso/overview.md) で説明しています。このファイルが必要になるのもそこです。このファイルには、ダッシュボードが提供するログイン方法と、マルチインスタンス構成の場合はバックエンドへの接続先が記述されます。

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

このセクションでは、リリース 2026.06 のインストールをリリース 2026.11 にアップグレードします。

!!! warning "2026.06 より前のリリースからのアップグレード"

    まずリリース 2026.06 のアップグレード手順を実行してください： [新しいリリースへのアップグレード](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release)。その後、以下の手順に進んでください。

### アップグレード前に

**digna リポジトリのバックアップ作成は必須です**

digna をアップグレードする前にリポジトリ（PostgreSQL）のバックアップを作成し、データ損失に備えてください。バックアップがあれば、アップグレード中に予期しない問題が発生しても復旧できます。

Terminal からバックアップを作成するには:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**リリース 2026.11 用のライセンスファイルを依頼する**

リリース 2026.11 には新しい `license.toml` が必要です。作業を始める前に digna チームに依頼し、[ステップ 7](#step-7-replace-the-license-file) で使えるよう準備しておいてください。

### アップグレード手順

#### ステップ 1: digna サービスを停止する {: #step-1-stop-the-digna-service }

digna がバックグラウンドサービスとして動作している場合、まず停止します:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

digna がフォアグラウンドで動作している場合は、その Terminal ウィンドウで ++ctrl+c++ を押してください。

#### ステップ 2: 現在のインストールをバックアップする {: #step-2-backup-current-installation }

digna のインストールディレクトリで、現在のインストールの実行ファイルとダッシュボードフォルダーの名前を変更し、新しいリリースを並べて配置できるようにします:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

`digna_old` はアップグレードを確認するまで、`dashboard_old` はそこから設定ファイルを復元するまで残してください（ステップ 4 を参照）。その後は両方とも削除してかまいません。

#### ステップ 3: 新バージョンの展開とデプロイ {: #step-3-extract-and-deploy-new-version }

1. 新しい digna インストール ZIP ファイルを展開
2. 新しい `digna` 実行ファイルと `dashboard` フォルダをインストールディレクトリにコピー
3. 実行ビットを復元し、必要に応じて検疫属性を削除:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "重要"

    `config.toml` も `dashboard/dashboard_config.toml` も、インストール ZIP に含まれることは決してありません。digna チームはどちらのファイルも配布しません。そのため既存の設定はアップグレードの影響を受けず、名前を変更した `*_old` フォルダー内のコピーが手元にある唯一の設定になります。

#### ステップ 4: 設定ファイルの復元 {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

リリース 2026.11 では `config.toml` の変更は不要です。リリース 2026.06 で動作するファイルはそのまま動作し続けます。次の 2 つの変更は任意です:

- データベース接続で digna Engine を使用し、そのデフォルトがホストに合わない場合は、[`[duckdb]` セクション](#duckdb-section) を追加します。
- リバースプロキシがダッシュボードとバックエンドを 1 つのオリジンで配信する場合は、`[app]` セクションを省略します。

!!! warning "digna が読み取らない設定"

    本ガイドの以前の版には、digna が読み取らない設定がいくつか記載されていました。これらは効果がなく、ステップ 6 で `config check` が **Unknown keys** の下に一覧表示します。削除するか修正してください:

    - `DIGNA_SCHEDULER_MAX_DELAY`、`DIGNA_CLEANUP_TIME`、`digna_COOKIE_PATH`、`digna_COOKIE_SAME_SITE`、`digna_APP_CORS_ALLOW_METHODS`、`digna_APP_CORS_ALLOW_HEADERS`、`digna_LOGGING_BACKUP_COUNT` は存在しません。削除してください。
    - 設定名は大文字と小文字を区別します。digna が読み取るのは `DIGNA_REPO_HOST` であり、`digna_REPO_HOST` ではありません。[バックエンド構成](#backend-configuration) と同様に、すべての名前を大文字で記述してください。

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

ダッシュボードは静的ファイルの集まりであるため、Web サーバー（およびブラウザー）が以前のバージョンを配信し続けている可能性があります。`dashboard` フォルダーをホストしている Web サーバーをリロードまたは再起動し、ページをハードリフレッシュ（++cmd+shift+r++）で再読み込みしてください。

#### ステップ 6: 構成を検証する {: #step-6-validate-the-configuration }

リポジトリに手を加える前に、`config.toml` が完全であることを確認します:

```bash
./digna config check
```

すべてのセクションが OK と報告される必要があります。FAILED と報告された箇所を修正し、**Unknown keys** の下に一覧表示されたキーを削除してから、続行する前にコマンドを再実行してください。

#### ステップ 7: ライセンスファイルを置き換える {: #step-7-replace-the-license-file }

通常、ライセンスファイルはリリースをまたいでそのまま使用できます。リリース 2026.11 は例外です。このリリースでは digna Data Reconciliation と digna Agentic という 2 つのライセンス対象モジュールが追加され、2026.11 より前に発行されたライセンスにはこれらが含まれていません。digna チームがリリース 2026.11 用に提供した `license.toml` をインストールディレクトリにコピーし、古いものを置き換えてください:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "以前のライセンスを使い続けないでください"

    以前のライセンスのままでも digna は起動しますが、digna Data Reconciliation と digna MCP Server は無効のままです。ライセンスを確認するすべてのコマンド（`user`、`inspection`、`repo`）は、確認に失敗するとリポジトリに手を加える前に中止されます。先に進む前に新しいライセンスを確認してください:

    ```bash
    ./digna license check
    ```

#### ステップ 8: リポジトリスキーマのアップグレード {: #step-8-upgrade-the-repository-schema }

digna のインストールディレクトリで次を実行します:

```bash
cd /opt/digna
./digna repo upgrade
```

リリース 2026.11 では、リポジトリスキーマをバージョン管理されたマイグレーションで管理します。以前のリリースからの最初のアップグレードでは、スキーマを従来方式の最終バージョンに更新し、それを起点として記録したうえで、リリース 2026.11 のマイグレーションを適用します。最後に次のように表示されます:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

既存のデータはすべて保持されます。リポジトリの状態はいつでも `./digna repo check` で確認できます。最後に適用されたマイグレーションと、保留中のマイグレーションが一覧表示されます。

!!! warning "リポジトリが古いままでは digna は起動しません"

    リリース 2026.11 以降、リポジトリのアップグレードが必要な間はサーバーが起動を拒否し、その旨を表示します。例:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    サーバーまたはサービスを起動する前に `repo upgrade` を実行してください。

#### ステップ 9: サービスの再起動 {: #step-9-restart-services }

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

nginx または Apache を使用している場合は、それぞれの Web サーバーを再起動してください:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### ステップ 10: アップグレードの確認 {: #step-10-verify-the-upgrade }

1. 新しい実行ファイルのリリースを確認します:

    ```bash
    ./digna version
    ```

    1 行目が `Release: 2026.11` となっている必要があります。

2. digna ダッシュボードにアクセスし、インターフェースが正しく読み込まれることを確認します。
3. サーバーの出力と `logs` ディレクトリ内のファイルにエラーがないか確認します。
4. データベース接続をテストします。参照:
   [接続のテスト](../../../databases/overview.md#testing-a-connection)。リリース 2026.06 より前のリリースからアップグレードした場合は、まだ ODBC を使用していなかった接続をすべて先に ODBC に切り替えてください。

新しいモジュールを使い始めるには、[digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md)、digna MCP Server については [AI エージェントの接続](../../../platform/agentic/connect_ai_agent.md)、digna Engine については [プロファイリングの場所](../../../platform/profiling/profiling_location.md) を参照してください。
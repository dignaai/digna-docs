# digna リリース 2026.11 の Linux インストールガイド

**リリース:** 2026.11

**最終更新:** 2026年11月7日


---

## 目次

1. [はじめに](#introduction)
2. [システム要件](#system-requirements)
3. [事前準備](#pre-installation-setup)
4. [PostgreSQL サーバーのセットアップ](#postgresql-server-setup)
5. [Web サーバーの構成](#web-server-configuration)
6. [初回インストール](#initial-installation)
7. [バックエンドの設定](#backend-configuration)
8. [ダッシュボードの設定](#dashboard-configuration)
9. [digna を systemd サービスとして実行する](#running-digna-as-a-systemd-service)
10. [新しいリリースへのアップグレード](#upgrading-to-a-new-release)

---

## はじめに {: #introduction }

### digna について

digna は、ウェアハウス、データレイク、レイクハウスなど様々なデータ環境におけるデータ品質管理を最適化するために設計された包括的な AI 駆動プラットフォームです。高いスケーラビリティと適応性を備え、自動化、リアルタイム監視、および異常検知を通じて現代のデータ課題に対処します。

digna は主に次の2つのコンポーネントで構成されています:

- **digna**: アプリケーションの中核であり、データの処理と品質チェックの実行を担います。バックエンドとコマンドラインインターフェイスを単一の実行ファイルに統合し、以前のリリースで別々だった `dignabackend` と `dignacli` を置き換えます。
- **dignadashboard**: Web サーバー上でホストされる、digna プラットフォームとやり取りしデータ品質指標を可視化するための Web ベースのインターフェース

### リリース 2026.11 の新機能

このリリースでは、digna Data Reconciliation、digna MCP Server を備えた digna Agentic、そして digna Engine が追加されました。digna Engine は digna の内部でデータをプロファイリングし、異なるデータベース技術間の参照整合性をチェックできます。詳細は[リリースノート](../../../changelog/Release_202611.md)を参照してください。

インストールに関しては、本リリースで新しいリポジトリのマイグレーション機構、digna Engine 用の `config.toml` のオプションの `[duckdb]` セクション、そして新しいライセンスファイルが導入されます。それぞれについては[アップグレードのセクション](#upgrading-to-a-new-release)で説明します。

### Windows や macOS をお探しですか？

本ガイドは Linux 向けです。他のプラットフォームについては、[Windows インストールガイド](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) または [macOS インストールガイド](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) を参照してください。

### 本ガイドはどのディストリビューション向けですか？

手順は、最も一般的なサーバーファミリ 2 種に対して書かれています。両者で差がある場合は両方のコマンドを記載しています:

- **Debian 系** — Debian、Ubuntu。パッケージマネージャ: `apt`
- **RHEL 系** — Red Hat Enterprise Linux、Rocky Linux、AlmaLinux、Fedora。パッケージマネージャ: `dnf`

`systemd` を採用している現代的なディストリビューションであれば動作します。変更されるのはパッケージ名と一部の設定パスだけです。

---

## システム要件 {: #system-requirements }

インストールを開始する前に、システムが次の最小要件を満たしていることを確認してください:

| 要件 | 仕様 |
|---|---|
| **オペレーティングシステム** | Ubuntu 22.04 LTS 以降、Debian 12 以降、RHEL 9 / Rocky 9 / AlmaLinux 9 以降 |
| **アーキテクチャ** | x86_64 (amd64) または arm64 |
| **Init システム** | systemd |
| **メモリ（最小構成）** | 16 GB RAM |
| **ディスク容量** | 10 GB の空きストレージ |
| **データベース** | PostgreSQL Server 12 以降 |
| **Web サーバー** | nginx、Apache httpd、または同等のもの |

!!! info "digna Engine"

    プロファイリングの場所として digna Engine を使用するデータベース接続は、digna ホスト自体でプロファイリングされます。そのためのメモリとディスク容量を追加で見込んでください。参照: [\[duckdb\] セクション](#duckdb-section)。

### データベースのインストール オプション

**PostgreSQL が既にインストールされている場合:**
既存の PostgreSQL サーバーに対して digna 用の新しいデータベースを追加できます。

**digna と同じマシンに PostgreSQL をインストールする場合:**

!!! info "推奨仕様"

    - **メモリ**: 32 GB RAM（16 GB の代わりに）
    - **ディスク容量**: 50 GB の空きストレージ（10 GB の代わりに）

    これらの高めの仕様は、digna と PostgreSQL データベースが同一マシン上で同時に動作することを想定したものです。

### ディストリビューションとアーキテクチャの確認

本ガイドのいくつかのコマンドは Debian 系と RHEL 系で異なります。どちらを使用しているかを確認するには、次を実行してください:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` または `ID=debian` — `apt` コマンドを使用
- `ID=rhel`、`rocky`、`almalinux` または `fedora` — `dnf` コマンドを使用
- `x86_64` または `aarch64` — 必要なインストールパッケージのアーキテクチャ

---

## 事前準備 {: #pre-installation-setup }

digna をインストールする前に、次の 2 つの主要な前提条件が整っていることを確認してください:

1. **PostgreSQL サーバー** – 計算されたメトリクスやパフォーマンスデータを格納するため
2. **Web サーバー** – digna Dashboard をホストするため

これらのコンポーネントがまだセットアップされていない場合は、以下のセクションに従ってインストールと構成を行ってください。

### パッケージインデックスの更新

何かをインストールする前にパッケージリストを更新してください:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "注意"

    本ガイド全体で、2 行並んだコマンドの最初の行は **Debian 系**、2 行目は **RHEL 系** 向けです。ご自身の環境に合う方だけを実行してください。

---

## PostgreSQL サーバーのセットアップ {: #postgresql-server-setup }

### 既に PostgreSQL をお持ちの場合

PostgreSQL がローカルで既にインストール済みで稼働している場合、またはマネージドなリモート PostgreSQL サーバーを使用している場合は、[次のセクション](#web-server-configuration)に進んでください。

### PostgreSQL のインストール

#### ステップ 1: サーバーパッケージのインストール

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "ヒント"

    ディストリビューションのパッケージは最新の PostgreSQL リリースに追従していないことがあります。特定の新しいバージョンが必要な場合は、公式の [PostgreSQL apt または yum リポジトリ](https://www.postgresql.org/download/linux/) を使用してください。

#### ステップ 2: データベースクラスタの初期化

**Debian 系**では、パッケージが自動的にクラスタを作成して起動します — 次のステップへ進んでください。

**RHEL 系**では、クラスタを明示的に作成する必要があります:

```bash
sudo postgresql-setup --initdb
```

#### ステップ 3: サービスの起動と有効化

```bash
sudo systemctl enable --now postgresql
```

これにより PostgreSQL が直ちに起動し、ブート時に自動的に再起動するよう設定されます。

#### ステップ 4: インストールの確認

```bash
psql --version
sudo systemctl status postgresql
```

PostgreSQL のバージョンと `active (running)` のサービスが表示されるはずです。

#### ステップ 5: サーバーへの接続

Linux の PostgreSQL パッケージは、クラスタを所有する `postgres` システムアカウントを作成します。次のようにして接続します:

```bash
sudo -u postgres psql
```

!!! note "注意 — ここは Windows と異なります"

    Windows のインストーラーはセットアップ中に `postgres` スーパーユーザーのパスワードを設定するよう促します。Linux パッケージではそうではありません。代わりに、ローカル接続は **peer authentication** で認証されます: `postgres` OS ユーザーはパスワードなしで `postgres` データベースユーザーとして接続できます。

    これが上記コマンドに `sudo -u postgres` を使う理由です。digna バックエンドは TCP 経由でユーザー名とパスワードで接続するため、[初回インストール](#initial-installation) で明示的な digna ユーザーを作成します。

#### ステップ 6: ポートの確認

デフォルトの PostgreSQL ポートは `5432` です。サーバーがどのポートで待ち受けているか確認するには:

```bash
sudo -u postgres psql -c "SHOW port;"
```

値を控えておいてください — digna バックエンドの設定時に必要です。

#### ステップ 7: digna ユーザーのためのパスワード認証を有効にする

digna は `digna_user` として TCP 経由で PostgreSQL に接続します。これは peer 認証ではなくパスワード認証が必要です。`pg_hba.conf` がそれを許可しているか確認してください。

ファイルの場所を確認するには:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

エディタで開き、ローカル TCP 行が `ident` ではなく `scram-sha-256`（古いサーバーでは `md5`）を使用していることを確認します:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

変更を行ったら PostgreSQL をリロードしてください:

```bash
sudo systemctl reload postgresql
```

!!! warning "重要"

    digna が `FATAL: Ident authentication failed for user "digna_user"` を報告する場合、この設定が原因です。

#### ステップ 8: PostgreSQL が別マシンで動作している場合

異なるホストからの接続を受け入れるには、`postgresql.conf` の `listen_addresses` を設定し、`pg_hba.conf` にネットワークに一致する `host` 行を追加します:

```
listen_addresses = '*'
```

その後ファイアウォールでポートを開け、サービスを再起動します:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Web サーバーの構成 {: #web-server-configuration }

digna はダッシュボードをホストするために Web サーバーを必要とします。次のオプションのいずれかを選択してください:

- [nginx](#nginx-setup) — 軽量で推奨
- [Apache httpd](#apache-setup) — 広く採用されている代替

これらのうち **いずれか一つ** をインストールして構成すれば十分です。

両セクションともダッシュボードが依存する次の 2 つを構成します:

- **シングルページアプリケーションのフォールバック** — ダッシュボードの URL をリロードしても 404 が返らないようにする
- **`.md` の MIME タイプ** — Markdown ファイルを正しく配信するため

### nginx のセットアップ {: #nginx-setup }

#### 概要

nginx は静的な digna ダッシュボードの配信に適した軽量で高性能な Web サーバーです。

#### インストール

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginx の起動

```bash
sudo systemctl enable --now nginx
```

#### インストールの確認

1. ブラウザを開く
2. `http://localhost` にアクセス
3. nginx のウェルカムページが表示されるはずです

#### ファイアウォールの開放

サーバーが他のマシンから到達される場合、HTTP トラフィックを許可します:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### ダッシュボード用のサイトを構成する

nginx は両ディストリビューションファミリで `conf.d` ディレクトリ内のすべてのファイルを読み込みます。digna 用の専用設定ファイルを作成してください:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

抽出した `dashboard` フォルダの実際のパスにある `/opt/digna/dashboard` を置き換えながら、以下を貼り付けてください:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

    `try_files` ディレクティブがないと、ルート URL 以外のダッシュボードページをリロードすると 404 が返されます。これは Windows の IIS で必要な URL Rewrite モジュールに相当する nginx の設定です。

#### デフォルトサイトを無効化する

同じポートで `default_server` であるサーバーブロックは 1 つだけにできます。**Debian 系**では、パッケージ付属のデフォルトを削除して競合を避けてください:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

**RHEL 系**では、`/etc/nginx/nginx.conf` 内の `server { ... }` ブロックをコメントアウトするか削除してください。

#### 設定を反映する

構文エラーがないかテストし、nginx をリロードします:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd のセットアップ {: #apache-setup }

#### 概要

Apache httpd はサポートされるすべてのディストリビューションのデフォルトリポジトリで利用可能です。パッケージ名は Debian 系では `apache2`、RHEL 系では `httpd` です。

#### インストール

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apache の起動

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### インストールの確認

1. ブラウザを開く
2. `http://localhost` にアクセス
3. ディストリビューションのデフォルトの Apache ページが表示されるはずです

#### 必須: mod_rewrite を有効にする

ダッシュボードは URL 書き換えを必要とします。

**Debian 系**ではモジュールを有効化して再起動します:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

**RHEL 系**では `mod_rewrite` はデフォルトで読み込まれています。確認するには:

```bash
httpd -M | grep rewrite
```

#### 必須: .htaccess の許可を有効にする

ドキュメントルートの設定ファイルを開きます:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

ドキュメントルートをカバーする `<Directory>` ブロック（両ファミリとも `/var/www/html`）を見つけ、次のように変更します:

```apache
AllowOverride None
```

を:

```apache
AllowOverride All
```

#### 必須: Markdown ファイルの MIME タイプ

同じファイルに次の行を追加して、Markdown ファイルが正しく配信されるようにします:

```apache
AddType text/markdown .md
```

!!! warning "重要"

    この設定がないと、`.md` ファイルが正しく配信されない可能性があります。

#### 設定を反映する

構成の構文をチェックし、Apache を再起動します:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## 初回インストール {: #initial-installation }

### ステップ 1: digna リポジトリのセットアップ

digna リポジトリは、digna が計算するすべてのメトリクスを格納します。分析およびパフォーマンスデータの中央データベースとして機能します。

#### リポジトリ用のスキーマとユーザーを作成する

PostgreSQL クライアント（psql、pgAdmin など）を開き、以下の SQL コマンドを実行してください:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**以下のプレースホルダーを置き換えてください:**

- `<digna_repo_schema>` — 希望するスキーマ名（例: `dignarepo`）
- `<digna_repo_user>` — 希望するユーザー名（例: `digna_user`）
- `<digna_repo_password>` — このユーザーのための安全なパスワード

**例:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

シェルから一度に実行するには:

```bash
sudo -u postgres psql
```

その後 `postgres=#` プロンプトに文を貼り付け、終了するには `\q` と入力してください。

!!! tip "ベストプラクティス"

    データベースユーザーには強力で複雑なパスワードを使用してください。簡単に推測される認証情報は避けてください。

---

### ステップ 2: digna インストールパッケージを展開する

1. 提供された digna インストール ZIP ファイルを見つけます
2. 希望するインストール先（例: `/opt/digna`）に展開します
3. 展開後、次の項目が存在するはずです:
   - `dashboard/` — Web ダッシュボードインターフェース
   - `digna` — メイン実行ファイル（バックエンド + CLI 統合）

!!! info "設定ファイルとライセンスファイルはパッケージに含まれていません"

    `config.toml` も `dashboard/dashboard_config.toml` もインストールパッケージには含まれていません。どちらも [バックエンドの設定](#backend-configuration) と [ダッシュボードの設定](#dashboard-configuration) でご自身で作成します。`license.toml` も同梱されていません。ステップ 3 で説明するとおり、digna から別途提供されます。

シェルから展開するには:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "注意"

    `unzip` がインストールされていない場合は、`sudo apt install -y unzip` または `sudo dnf install -y unzip` で追加してください。

#### 実行ファイルに実行権を付与する

アーカイブの転送方法によっては実行ビットが失われることがあります。明示的に設定してください:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### サービスアカウントを作成する

本番環境では、バックエンドを専用の特権のないユーザーで実行することを推奨します:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "注意"

    RHEL 系では同等のシェルパスは `/sbin/nologin` です。

### ステップ 3: ライセンスファイルのインストール

!!! warning "重要"

    ライセンスファイルはインストールパッケージに含まれておらず、digna から別途提供されます。

1. 提供された `license.toml` ファイルを見つけます
2. それを digna のインストールルートディレクトリ（`config.toml` と `digna` 実行ファイルがある場所）にコピーします

**なぜ重要か:**
ライセンスファイルには顧客情報、ライセンスの有効期限、デジタル署名が含まれています。**このファイルを変更しないでください** — 変更すると無効になります。

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

## バックエンドの設定 {: #backend-configuration }

### ステップ 1: 設定ファイルを作成・編集する

`config_template.toml` ファイルが digna インストールディレクトリに含まれています。これを `config.toml` にリネームするだけです。

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
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

| パラメーター | 値 | 注意 |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | ダッシュボードの URL | ダッシュボードの配信元 URL。それ以外のオリジンからのブラウザーリクエストは拒否されます |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | 必須。ブラウザーが各リクエストでセッションクッキーを送信するために必要です |

!!! note "注意"

    ダッシュボードをデフォルトの HTTP ポートで nginx や Apache から提供している場合、許可するオリジンは `http://localhost` です — またはダッシュボードが他のマシンから到達される場合はサーバーの公開 URL を指定してください。

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

| パラメーター | 値 | 注意 |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` または IP | PostgreSQL サーバーのホスト名/IP |
| `DIGNA_REPO_PORT` | `5432` (デフォルト) | PostgreSQL のポート |
| `DIGNA_REPO_DB` | `postgres` | データベース名 |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | 先に作成したスキーマ |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL セットアップで作成したユーザー |
| `DIGNA_REPO_PASSWORD` | ご自身のパスワード | スキーマ作成時に設定したパスワード |
| `DIGNA_REPO_SSLMODE` | `prefer` (デフォルト) | 省略可能。PostgreSQL の SSL モード: `disable`、`allow`、`prefer`、`require`、`verify-ca` または `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (デフォルト) | 省略可能。digna がリポジトリに対して開いたままにする接続の数 |

!!! tip "ベストプラクティス"

    `config.toml` はプレーンテキストでデータベースパスワードを含みます。サービスアカウントのみが読めるように権限を制限してください:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] セクション

このセクションにはセキュリティ、クッキー、検査の設定が含まれます:

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

| パラメーター | 値 | 注意 |
|---|---|---|
| `DIGNA_FERNET_KEY` | 上記の値 | 以前のリリースで使用されていた暗号化の鍵。必ず指定する必要があるため、上記の値をそのまま使用してください |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | ダッシュボードにアクセスする際のホスト。`""` を指定するとドメインは設定されません。ダッシュボードとバックエンドを 1 つのオリジンで配信するプロキシの背後では、これが適切な設定です |
| `DIGNA_COOKIE_SECURE` | `false`（HTTP） / `true`（HTTPS） | digna を HTTPS で配信する場合は必ず `true` にしてください |
| `DIGNA_COOKIE_HTTPONLY` | `true` | セッションクッキーをスクリプトから参照できないようにします |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400`（24 時間） | セッションのタイムアウト（秒） |
| `DIGNA_MAX_WORKERS` | CPU コア数 - 1 | 同時に実行できる検査の数 |
| `DIGNA_FRONTEND_BASEURL` | ダッシュボードの URL | 必須。通知メッセージ内のリンクに使用されるため、受信者が開ける URL である必要があります |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (デフォルト) | 省略可能。ソースデータベースに対する 1 つのクエリが中止されるまでに実行できる秒数。`0` でタイムアウトを無効にします |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (デフォルト) | 省略可能。ソースデータベースへの接続を待機する秒数。`0` の場合は無期限に待機します |

!!! tip "ヒント"

    サーバー上の CPU コア数を確認するには `nproc` を実行してください。

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

このセクションはログ動作を設定します:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| パラメーター | 値 | 注意 |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` または `DEBUG` | 本番は `INFO`、トラブルシューティング時は `DEBUG`。`TRACE`、`WARN`、`ERROR` も指定できます |
| `DIGNA_LOGGING_DIR` | `logs` (デフォルト) | 省略可能。ローテーションされるログファイルのディレクトリ（作業ディレクトリからの相対パス） |
| `DIGNA_LOGGING_MAX_FILES` | `30` (デフォルト) | 省略可能。保持するローテーション済みログファイルの数 |

#### [duckdb] セクション（省略可能） {: #duckdb-section }

リリース 2026.11 の新機能です。このセクションでは **digna Engine** のリソースを設定します。digna Engine は、プロファイリングの場所が **digna Engine** であるデータベース接続について digna の内部でデータをプロファイリングし、異なるデータベース接続上のデータソース間で参照整合性チェックを実行します。参照:
[プロファイリングの場所](../../../platform/profiling/profiling_location.md)。

このセクションは省略可能です。省略した場合は、以下のデフォルトが適用されます。

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| パラメーター | 値 | 注意 |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (デフォルト) | 1 回の digna Engine の実行が使用できるメモリ（MB）。同時に最大 `DIGNA_MAX_WORKERS` 個の実行がアクティブになります |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | デフォルト: システムの一時ディレクトリ（`$TMPDIR`、未設定の場合は `/tmp`） | データがメモリに収まらない場合に一時ファイルを置くディレクトリ |

!!! tip "digna Engine のサイジング"

    digna 自体が使用するメモリに加えて、digna ホストに最大 `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` のメモリを見込んでください。また一時ディレクトリには、digna Engine を使用するデータソースのうち最大の検査対象日のデータを保持できるだけの空きディスク容量が必要です。`DIGNA_DUCKDB_TEMP_DIRECTORY` は、その容量があり、digna を実行するアカウントが書き込めるディスクを指すように設定してください:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
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

1. ターミナルを開く
2. digna のインストールディレクトリ（`config.toml` と `digna` 実行ファイルがある場所）に移動
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

    Linux ではカレントディレクトリは PATH に含まれていないため、実行ファイルは `./digna` として呼び出します。どこでも短い形式を使いたい場合は、シンボリックリンクを追加してください:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
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

管理者ユーザーはリポジトリスキーマに対して直接作成されるため、この時点でサーバーを起動しておく必要はありません。digna のインストールディレクトリで次を実行します:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**例:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

これにより、メールアドレス `admin@example.com` の管理者権限を持つユーザーが作成されます。

!!! tip "ヒント"

    パスワードはシングルクォートで囲んでください。`bash` や `zsh` は `!`、`$`、`*` などの文字を特別扱いするため、引用符なしだと正しく渡らないことがあります。

!!! tip "ベストプラクティス"

    大文字・小文字・数字・特殊文字を混ぜた強力なパスワードを使用してください。

### ステップ 6: digna サーバーの起動

digna インストールディレクトリでサーバーを起動します:

```bash
./digna serve --address <host> --port <port>
```

**パラメーター:**
- `--address` — サーバーのホスト名/IP（デフォルト `127.0.0.1`）
- `--port` — サーバーのポート（デフォルト `8000`）

サーバーが起動すると、待ち受けているアドレスが表示されます:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "ヒント"

    ダッシュボードがバックエンドと別マシンで提供されている場合、API ポートもファイアウォールで開放してください:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "サーバーはターミナルを占有します"

    `serve` はフォアグラウンドで実行され、++ctrl+c++ で停止するまで動作し続けます。セットアップを終えるまで実行したままにしてください。起動時に自動的に開始する方法は次を参照してください: [digna を systemd サービスとして実行する](#running-digna-as-a-systemd-service).

---

## ダッシュボードの設定 {: #dashboard-configuration }

### ステップ 1: ダッシュボードを Web サーバーにデプロイする

digna ダッシュボードは独自の設定を `dashboard/dashboard_config.toml` から読み込みます。このファイルはインストールパッケージに含まれていないため、`dashboard/` ディレクトリ内にダッシュボードのファイルと並べて作成します。

その内容は [シングルサインオン](../../../sso/overview.md) で説明しています。このファイルが必要になるのもそこです。このファイルには、ダッシュボードが提供するログイン方法と、マルチインスタンス構成の場合はバックエンドへの接続先が記述されます。

利用する Web サーバーを選び、該当するデプロイ手順に従ってください。

#### nginx にデプロイする場合

[nginx のセットアップ](#nginx-setup) に従った場合、サーバーブロックはすでに `dashboard` フォルダを指しているのでコピーは不要です。

1. **パスを確認**
   - `/etc/nginx/conf.d/digna.conf` を開く
   - `root` が展開した `dashboard` フォルダを指しているか確認

2. **フォルダが読み取り可能であることを確認**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **nginx をリロード**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **インストールのテスト**
   - ブラウザを開く
   - `http://localhost`（または設定した URL）にアクセス
   - digna ダッシュボードのログインページが表示されるはずです

#### Apache httpd にデプロイする場合

1. **ダッシュボードをドキュメントルートにコピー**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **リライトルールの追加**

   ブラウザリロード時にダッシュボードのルートが生きるよう、デプロイ先フォルダに `.htaccess` ファイルを作成します:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **ダッシュボードにアクセス**
   - ブラウザを開く
   - `http://localhost/digna` にアクセス
   - digna ダッシュボードのログインページが表示されるはずです

### ステップ 2: SELinux (RHEL 系のみ)

RHEL、Rocky、AlmaLinux、Fedora では SELinux がデフォルトで enforcing になっており、Web サーバーが想定外の場所にあるファイルを読めないようブロックすることがあります。以下でアクティブか確認してください:

```bash
getenforce
```

結果が `Enforcing` で、ダッシュボードを `/opt/digna/dashboard` から配信している場合、Web サーバーが読み取れるようディレクトリにラベルを付けてください:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "注意"

    `semanage` が見つからない場合は、`sudo dnf install -y policycoreutils-python-utils` でインストールしてください。

!!! warning "重要"

    新規に構成した RHEL サーバーでダッシュボードが **403 Forbidden** を返す場合、多くはファイル権限の問題ではなく SELinux のラベリング問題です。`sudo ausearch -m avc -ts recent` で確認してください。

---

## digna を systemd サービスとして実行する {: #running-digna-as-a-systemd-service }

### なぜ digna をサービスとして実行するのか？

digna バックエンドを systemd サービスとして実行すると次のメリットがあります:

- マシン起動時に自動で開始される
- ターミナルを開いておく必要なくバックグラウンドで実行される
- 障害発生時に自動で再起動される
- 標準の Linux サービス管理ツールである `systemctl` で管理できる

### サービス管理ファイル

必要なファイルはすべて digna インストールディレクトリの `bin/` にあります。

利用可能なシェルスクリプトは次の通りです:

- `install_service.sh` — digna を systemd に登録
- `uninstall_service.sh` — サービスを登録解除
- `start_service.sh` — 登録済みサービスを起動
- `stop_service.sh` — 実行中のサービスを停止

!!! warning "ルート権限が必要"

    サービスは起動時に読み込まれるユニットファイルを `/etc/systemd/system` に書き込むため、すべてのスクリプトは `sudo` で実行する必要があります。

### スクリプトに実行権を付与する

展開によって実行ビットが保持されないことがあります。初回使用前に:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### サービスのインストール

1. **ターミナルを開く**

2. **bin フォルダに移動**
   ```bash
   cd /opt/digna/bin
   ```

3. **インストールスクリプトを実行**
   ```bash
   sudo ./install_service.sh
   ```

digna サーバーは systemd に登録され、自動起動が有効になります。サービスは直ちに開始されません — 起動方法は次のセクションを参照してください。

### サービスの起動と停止

#### サービスを開始するには

1. ターミナルを開く
2. `/opt/digna/bin` に移動
3. 次を実行:
   ```bash
   sudo ./start_service.sh
   ```

#### サービスを停止するには

1. ターミナルを開く
2. `/opt/digna/bin` に移動
3. 次を実行:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "ヒント"

    アプリケーションファイルを更新する前は、必ずサービスを停止してください。

### systemctl でのサービス管理

登録後は、任意のディレクトリから標準の systemd コマンドでサービスを管理できます:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### サービスの確認

サービスが登録され、実行中であることを確認するには:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` はブート時に開始されることを意味し、`active` は現在実行中であることを意味します。

### サービスログの表示

systemd はバックエンドがコンソールに出力する内容をすべてキャプチャします。ログを読むには:

```bash
sudo journalctl -u digna -n 100
```

問題を再現しながらログをリアルタイムで追うには:

```bash
sudo journalctl -u digna -f
```

!!! tip "ヒント"

    サービスが起動してすぐ停止する問題を診断する最速の方法はこれです。リポジトリ接続失敗や `license.toml` の欠如はここに記録されます。

### インストール先を移動する場合

ユニットファイルには実行ファイルへの絶対パスが格納されるため、インストールを移動するにはサービスを再登録する必要があります:

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

これで digna サーバーは systemd から登録解除されます。

---

## 新しいリリースへのアップグレード {: #upgrading-to-a-new-release }

このセクションでは、リリース 2026.06 のインストールをリリース 2026.11 にアップグレードします。それより古いインストールの場合は、先に [リリース 2026.06 より前のリリースからのアップグレード](#upgrading-from-a-release-before-2026-06)をお読みください。

### アップグレード前に

**digna リポジトリのバックアップ作成は必須です**

digna をアップグレードする前にリポジトリ（PostgreSQL）のバックアップを作成し、データ損失に備えてください。バックアップがあれば、アップグレード中に予期しない問題が発生しても復旧できます。

シェルからバックアップを作成するには:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

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

digna が systemd サービスとして動作している場合、まず停止します:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

digna がフォアグラウンドで動作している場合は、そのターミナルウィンドウで ++ctrl+c++ を押してください。

#### ステップ 2: 現在のインストールをバックアップする {: #step-2-backup-current-installation }

digna のインストールディレクトリで、現在のインストールの実行ファイルとダッシュボードフォルダーの名前を変更し、新しいリリースを並べて配置できるようにします:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

`digna_old` はアップグレードを確認するまで、`dashboard_old` はそこから設定ファイルを復元するまで残してください（ステップ 4 を参照）。その後は両方とも削除してかまいません。

!!! info "リリース 2026.06 より前のリリースからアップグレードする場合"

    実行ファイルの代わりに、`dignabackend` と `dignacli` のフォルダー名を変更します:
    `sudo mv dignabackend dignabackend_old` と `sudo mv dignacli dignacli_old`。どちらもリリース 2026.11 では使用されません。

#### ステップ 3: 新バージョンの展開とデプロイ {: #step-3-extract-and-deploy-new-version }

1. 新しい digna インストール ZIP ファイルを展開
2. 新しい `digna` 実行ファイルと `dashboard` フォルダをインストールディレクトリにコピー
3. 実行ビットとサービスアカウントの所有権を復元:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "重要"

    `config.toml` も `dashboard/dashboard_config.toml` も、インストール ZIP に含まれることは決してありません。digna チームはどちらのファイルも配布しません。そのため既存の設定はアップグレードの影響を受けず、名前を変更した `*_old` フォルダー内のコピーが手元にある唯一の設定になります。

#### ステップ 4: 設定ファイルの復元 {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
./digna config check
```

すべてのセクションが OK と報告される必要があります。FAILED と報告された箇所を修正し、**Unknown keys** の下に一覧表示されたキーを削除してから、続行する前にコマンドを再実行してください。

#### ステップ 7: ライセンスファイルを置き換える {: #step-7-replace-the-license-file }

通常、ライセンスファイルはリリースをまたいでそのまま使用できます。リリース 2026.11 は例外です。このリリースでは digna Data Reconciliation と digna Agentic という 2 つのライセンス対象モジュールが追加され、2026.11 より前に発行されたライセンスにはこれらが含まれていません。digna チームがリリース 2026.11 用に提供した `license.toml` をインストールディレクトリにコピーし、古いものを置き換えてください:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
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

systemd サービスとして実行している場合:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

手動で実行している場合はサーバーを再起動します:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

nginx または Apache を使用している場合は、それぞれの Web サーバーをリロードしてください:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

RHEL 系で `dashboard` ディレクトリを置き換えた場合は、SELinux のラベリングを再適用してください:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### ステップ 10: アップグレードの確認 {: #step-10-verify-the-upgrade }

1. 新しい実行ファイルのリリースを確認します:

    ```bash
    ./digna version
    ```

    1 行目が `Release: 2026.11` となっている必要があります。

2. digna ダッシュボードにアクセスし、インターフェースが正しく読み込まれることを確認します。
3. サーバーログにエラーがないか確認します:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. データベース接続をテストします。参照:
   [接続のテスト](../../../databases/overview.md#testing-a-connection)。リリース 2026.06 より前のリリースからアップグレードした場合は、まだ ODBC を使用していなかった接続をすべて先に ODBC に切り替えてください。

新しいモジュールを使い始めるには、[digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md)、digna MCP Server については [AI エージェントの接続](../../../platform/agentic/connect_ai_agent.md)、digna Engine については [プロファイリングの場所](../../../platform/profiling/profiling_location.md) を参照してください。
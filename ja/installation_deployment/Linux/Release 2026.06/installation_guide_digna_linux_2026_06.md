# digna リリース 2026.06 の Linux インストールガイド

**リリース:** 2026.06

**最終更新:** 2026年9月5日


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

- **dignabackend**: データ処理と品質チェックを担当するアプリケーションのコアエンジン
- **dignadashboard**: Web サーバー上でホストされる、digna プラットフォームとやり取りしデータ品質指標を可視化するための Web ベースのインターフェース

### リリース 2026.06 の新機能

このリリースでは、データオブザーバビリティ機能をコードの中に直接取り込み、開発者がデータ品質をソースで監視できるようになりました。詳細は [release notes](http://docs.digna.ai/changelog/Release_202606/) を参照してください。

### Windows や macOS をお探しですか？

本ガイドは Linux 向けです。他のプラットフォームについては、[Windows インストールガイド](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) または [macOS インストールガイド](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) を参照してください。

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
   - `config.toml` — 設定ファイル
   - `license.toml` — ライセンスファイル（提供されたものをここにコピー）

シェルから展開するには:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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

このセクションは digna バックエンドのアプリ設定を構成します:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| パラメーター | 値 | 注意 |
|---|---|---|
| `digna_APP_HOST` | `localhost` または IP アドレス | dignabackend がホストされるホスト名または IP |
| `digna_APP_PORT` | `8082` (デフォルト) | REST API エンドポイントのポート |
| `digna_APP_CORS_ALLOW_ORIGINS` | フロントエンドの URL | ダッシュボードが別サーバーの場合、その URL を含める |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | 認証付き CORS に必要 |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | すべての HTTP メソッドを許可 |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | すべてのヘッダを許可 |

!!! note "注意"

    ダッシュボードをデフォルトの HTTP ポートで nginx や Apache から提供している場合、許可するオリジンは `http://localhost` です — またはダッシュボードが他のマシンから到達される場合はサーバーの公開 URL を指定してください。

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

| パラメーター | 値 | 注意 |
|---|---|---|
| `digna_REPO_HOST` | `localhost` または IP | PostgreSQL サーバーのホスト名/IP |
| `digna_REPO_PORT` | `5432` (デフォルト) | PostgreSQL のポート |
| `digna_REPO_DB` | `postgres` | データベース名 |
| `digna_REPO_SCHEMA` | `dignarepo` | 先に作成したスキーマ |
| `digna_REPO_USER` | `digna_user` | PostgreSQL セットアップで作成したユーザー |
| `digna_REPO_PASSWORD` | ご自身のパスワード | スキーマ作成時に設定したパスワード |

!!! tip "ベストプラクティス"

    `config.toml` はプレーンテキストでデータベースパスワードを含みます。サービスアカウントのみが読めるように権限を制限してください:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] セクション

このセクションにはセキュリティとクッキーの設定が含まれます:

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

| パラメーター | 値 | 注意 |
|---|---|---|
| `digna_FERNET_KEY` | 暗号化キー | トークンやクッキーの暗号化に使用（デフォルトが提供される） |
| `digna_COOKIE_DOMAIN` | `localhost` | フロントエンドのドメインに合わせる |
| `digna_COOKIE_SECURE` | `false`（ローカル） / `true`（本番） | HTTPS 接続では `true` を使用 |
| `digna_COOKIE_HTTPONLY` | `true` | セキュリティのため常に有効推奨 |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF 攻撃を防止 |
| `digna_TOKEN_EXPIRES_IN` | `86400`（24 時間） | セッションのタイムアウト（秒） |
| `digna_MAX_WORKERS` | CPU コア数 - 1 | 同時並列検査タスクの数 |

!!! tip "ヒント"

    サーバー上の CPU コア数を確認するには `nproc` を実行してください。

#### [logging] セクション

このセクションはログ動作を設定します:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| パラメーター | 値 | 注意 |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` または `DEBUG` | 本番は `INFO`、トラブルシューティング時は `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | 保持する日次ログバックアップの数 |

---

### ステップ 2: リポジトリの初期化

1. ターミナルを開く
2. digna のインストールディレクトリ（`config.toml` と `digna` 実行ファイルがある場所）に移動
3. 接続テストを実行:

```bash
cd /opt/digna
./digna repo check
```

接続が確立されたことを確認するメッセージが表示されるはずです（リポジトリ自体はまだ初期化されていません）。

!!! note "注意"

    Linux ではカレントディレクトリは PATH に含まれていないため、実行ファイルは `./digna` として呼び出します。どこでも短い形式を使いたい場合は、シンボリックリンクを追加してください:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
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

**パラメーター:**
- `--address` — サーバーのホスト名/IP
- `--port` — サーバーのポート

次のような起動メッセージが表示され、サーバーが実行中であることを確認できます:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "ヒント"

    ダッシュボードがバックエンドと別マシンで提供されている場合、API ポートもファイアウォールで開放してください:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### ステップ 5: 管理者ユーザーの作成

1. 新しいターミナルウィンドウを開く
2. digna のインストールディレクトリに移動
3. 次のコマンドで管理者ユーザーを作成します:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**例:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

これによりユーザー名 `admin` の管理者権限を持つアカウントが作成されます。

!!! tip "ヒント"

    パスワードはシングルクォートで囲んでください。`bash` や `zsh` は `!`、`$`、`*` などの文字を特別扱いするため、引用符なしだと正しく渡らないことがあります。

!!! tip "ベストプラクティス"

    大文字・小文字・数字・特殊文字を混ぜた強力なパスワードを使用してください。

---

## ダッシュボードの設定 {: #dashboard-configuration }

### ステップ 1: ダッシュボードを Web サーバーにデプロイする

digna ダッシュボードには `dashboard/` ディレクトリ内に別の `config.toml` ファイルがあり、この構成は既に提供されています。初期セットアップでは変更は不要です。バックエンド接続をカスタマイズする必要がある場合にのみ編集してください。

ダッシュボード構成を変更する必要がある（例: マルチインスタンス展開）場合は、ダッシュボードのドキュメントを参照してください。

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

### アップグレード前に

**digna リポジトリのバックアップ作成は必須です**

アップグレード前にリポジトリ（PostgreSQL）のバックアップを作成し、データ損失に備えてください。バックアップがあれば、アップグレード中に問題が発生しても復旧できます。

シェルからバックアップを作成するには:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### アップグレード手順

#### ステップ 1: digna サービスを停止する

digna が systemd サービスとして動作している場合、まず停止します:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

digna がフォアグラウンドで動作している場合は、そのターミナルで `Ctrl + C` を押してください。

#### ステップ 2: 現行バックエンドのバックアップ

digna インストールディレクトリで:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### ステップ 3: 新バージョンの展開とデプロイ

1. 新しい digna インストール ZIP ファイルを展開
2. 新しい `digna` 実行ファイルと `dashboard` フォルダをインストールディレクトリにコピー
3. 実行ビットとサービスアカウントの所有権を復元:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "重要"

    `config.toml` ファイルはインストール ZIP に **決して** 含まれません。既存の設定は安全に保持されます。

### ステップ 4: 設定ファイルの復元

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### ステップ 5: リポジトリスキーマのアップグレード

digna インストールディレクトリに移動して次を実行します:

```bash
cd /opt/digna
./digna repo upgrade
```

これにより既存のデータを保持したまま PostgreSQL スキーマが最新バージョンに更新されます。

### ステップ 6: サービスの再起動

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

nginx または Apache を使用している場合は、それぞれをリロードしてください:

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

#### ステップ 7: アップグレードの確認

1. digna ダッシュボードにアクセス
2. インターフェースが正しく読み込まれることを確認
3. サーバーログにエラーがないか確認:

```bash
sudo journalctl -u digna -n 100
```
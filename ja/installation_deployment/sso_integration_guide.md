# シングルサインオン統合ガイド

---

## 目次

1. [導入と概要](#introduction-and-overview)
2. [設定手順](#configuration-steps)
3. [ダッシュボードの設定](#dashboard-configuration)
4. [バックエンドの設定](#backend-configuration)
5. [ログインのテスト](#testing-login)
6. [トラブルシューティング](#troubleshooting)
7. [サポートされているプロバイダ](#supported-providers)

---

## 導入と概要 {: #introduction-and-overview }

このガイドは、**OpenID Connect (OIDC)** を使用して digna プラットフォームにシングルサインオン（SSO）を統合するためのステップバイステップの手順を提供します。

### SSO とは？

シングルサインオンは、ユーザーが外部のアイデンティティプロバイダを介して企業の資格情報で安全に digna にログインできるようにする仕組みです。ユーザーは個別の digna パスワードを管理する代わりに、企業の認証情報で認証できます。

### 動作概要

digna の SSO は OIDC プロトコルを使用して実装されています。複数のアイデンティティプロバイダを並列に設定するには、2 つの主要な設定ファイルを調整します。

- **`dashboard_config.toml`** — フロントエンドのログインインターフェースを制御
- **`config.toml`** — バックエンドの OIDC 接続を設定

### サポートプロバイダ {: #supported-providers-overview }

このガイドの例では **Microsoft** と **Google** を使用していますが、同じ構成に従えば **任意の OIDC 準拠プロバイダ** を統合できます。

一般的な OIDC プロバイダ:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- その他の OIDC 準拠アイデンティティプロバイダ

---

## 設定手順 {: #configuration-steps }

SSO の設定には 2 つのファイルの更新が必要です。本節ではそれぞれの設定方法を説明します。

### 設定ファイルの概要

| ファイル | 場所 | 目的 |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | フロントエンドのログインインターフェース |
| **config.toml** | `/config.toml` | バックエンドの OIDC 接続 |

両方のファイルを適切に設定する必要があります。

---

## ダッシュボードの設定 {: #dashboard-configuration }

### ファイルの場所

```
dashboard/dashboard_config.toml
```

### ステップ 1: OIDC プロバイダを追加

サポートしたい各アイデンティティプロバイダについて、`[[login.oidc]]` 配列の下にエントリを追加します。

**Microsoft と Google の例:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### ステップ 2: ログインオプションの設定

パスワードベースのログインを許可するかどうかを指定します:

```toml
[login]
usePassword = true
```

### 設定パラメータ

#### `[[login.oidc]]` セクション

| パラメータ | 型 | 必須か | 説明 |
|---|---:|---|---|
| `key` | string | はい | OIDC 接続の一意識別子（config.toml のキーと一致する必要があります） |
| `label` | string | はい | ログインボタンに表示されるテキスト（例: "Login with Microsoft"） |

#### `[login]` セクション

| パラメータ | 型 | デフォルト | 説明 |
|---|---:|---|---|
| `usePassword` | boolean | false | SSO に加えてパスワードベースのログインを許可するか |

### usePassword の挙動

**`usePassword = true` の場合:**
- ログイン画面に SSO ボタン（例: "Login with Microsoft"）が表示される
- 同時にユーザー名とパスワードの入力欄が表示される
- ユーザーはどちらの方法でも認証できる
- 一部のユーザーが SSO を使い、他のユーザーがパスワードを使うハイブリッド構成を許可する

**`usePassword = false`（または省略）の場合:**
- ログイン画面には SSO ボタンのみ表示される
- ユーザー名/パスワード入力欄は表示されない
- OIDC 認証のみが使用可能

!!! tip "ヒント"

    パスワードベースのログインは、`digna user add` コマンドやダッシュボードを使ってパスワードで作成されたユーザーのみ利用できます。

### 完全な例

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## バックエンドの設定 {: #backend-configuration }

### ファイルの場所

```
/config.toml
```

(ルートの digna インストールディレクトリ)

### ステップ 1: OIDC プロバイダセクションを追加

各プロバイダは専用の `[oidc.<key>]` セクションを持つ必要があります。key は `dashboard_config.toml` の `key` と一致させてください。

### Microsoft 設定

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google 設定

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### 設定パラメータ

| パラメータ | 型 | 必須か | 説明 | 例 |
|---|---:|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | はい | アイデンティティプロバイダから取得するクライアント ID | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | はい | アイデンティティプロバイダから取得するクライアントシークレット | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | はい | 認証後のコールバック URL | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | はい | OIDC の構成エンドポイント | `https://login.microsoftonline.com/...` |

!!! warning "重要"

    プレースホルダ（`<client_id>`, `<client_secret>`, `<tenant_id>`）は、アイデンティティプロバイダの開発者ポータルから取得した実際の値に置き換えてください。

### リダイレクト URI

リダイレクト URI はアイデンティティプロバイダ側の設定と同一である必要があります:

```
http://localhost:5173/oidc/callback
```

digna を別ドメインでホストしている場合は適宜更新してください:
- ローカル: `http://localhost:5173/oidc/callback`
- 本番: `https://digna.yourdomain.com/oidc/callback`

### 完全な例

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## ログインのテスト {: #testing-login }

設定完了後、SSO が正しく動作するかを確認します。

### テスト前チェックリスト

テスト前に以下を確認してください:

- [ ] `dashboard_config.toml` に OIDC プロバイダが追加されている
- [ ] `config.toml` に OIDC 資格情報が追加されている
- [ ] 両ファイルが保存されている
- [ ] 資格情報が正しい（クライアント ID、クライアントシークレット）
- [ ] リダイレクト URI がデプロイ先の URL と一致している
- [ ] アイデンティティプロバイダのアプリケーションにリダイレクト URI が設定されている

### テスト手順

#### ステップ 1: サービスの再起動

変更を適用するために digna のバックエンドと Web サーバーを再起動します。

**Windows サービスとして実行している場合:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**手動で実行している場合:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**IIS や Tomcat を使用している場合:**
Web サーバーサービスを再起動してください。

#### ステップ 2: ダッシュボードを開く

ブラウザで digna ダッシュボードを開きます:

```
http://localhost:5173
```

（または設定したダッシュボードの URL）

#### ステップ 3: ログインボタンを確認

設定した各プロバイダのログインボタンが表示されていることを確認します:

- "Login with Microsoft" ボタンが表示される
- "Login with Google" ボタンが表示される
- （`usePassword = true` の場合）ユーザー名/パスワード欄が表示される

ボタンが表示されない場合:
- `dashboard_config.toml` が保存されているか確認
- ダッシュボードサービスが再起動されているか確認
- ブラウザコンソール（F12）でエラーを確認

#### ステップ 4: SSO ログインをテスト

SSO ボタン（例: "Login with Microsoft"）をクリックします:

1. アイデンティティプロバイダのログインページにリダイレクトされるはずです
2. 企業の認証情報でログインします
3. digna にリダイレクトされるはずです
4. digna にログインできていることを確認します

#### ステップ 5: ユーザー作成の確認

SSO ログイン成功後:

- ユーザーが自動的に digna に作成されるはずです
- ユーザーがログイン状態になるはずです
- ユーザープロファイルにアイデンティティプロバイダの情報が表示されるはずです
- digna ダッシュボードが表示されるはずです

#### ステップ 6: パスワードログインのテスト（有効な場合）

`usePassword = true` の場合:

1. digna からログアウト
2. ログインページでユーザー名とパスワードを入力
3. パスワード認証でログインできることを確認

---

## トラブルシューティング {: #troubleshooting }

### ログインボタンが表示されない

**症状:**
- ログインページに OIDC ログインボタンが表示されない
- （`usePassword = true` の場合）パスワード欄のみ表示される

**原因と対処法:**
1. `dashboard_config.toml` が `dashboard/` ディレクトリにあるか確認
2. `[[login.oidc]]` セクションが正しい構文で存在するか確認
3. ダッシュボードサービスを再起動
4. ブラウザキャッシュをクリア（Ctrl+Shift+Delete または Cmd+Shift+Delete）
5. ブラウザコンソール（F12 → Console タブ）でエラーを確認

---

### リダイレクト URI 不一致エラー

**症状:**
- SSO ボタンをクリック後に "redirect_uri mismatch" のようなエラー
- "The redirect URI is not registered" エラー

**原因と対処法:**
1. `config.toml` の `DIGNA_OIDC_REDIRECT_URI` が正しいか確認
2. アイデンティティプロバイダの設定にリダイレクト URI が登録されているか確認
3. プロトコル、ドメイン、パスが完全に一致しているか確認
4. リダイレクト URI のタイプミスがないか確認
5. HTTPS を使用している場合は証明書が有効か確認

---

### 無効なクライアント資格情報エラー

**症状:**
- "Invalid client ID or secret" エラー
- 認証が資格情報エラーで失敗する

**原因と対処法:**
1. `DIGNA_OIDC_CLIENT_ID` と `DIGNA_OIDC_CLIENT_SECRET` が正しいか確認
2. 余分なスペースや特殊文字が含まれていないか確認
3. 資格情報が期限切れや取り消しされていないか確認
4. 設定更新後にバックエンドサービスを再起動
5. アイデンティティプロバイダのコンソールで資格情報が有効か確認

---

### ログインがハングする、タイムアウトする

**症状:**
- SSO ボタンをクリックしても何も起きない
- 数秒後にタイムアウトする
- ブラウザが "Failed to connect" のように表示する

**原因と対処法:**
1. digna バックエンドが実行中か確認: `digna repo check`
2. アイデンティティプロバイダへのネットワーク接続を確認
3. `DIGNA_OIDC_CONFIGURATION_URL` にアクセスできることを確認
4. ファイアウォールでアウトバウンド HTTPS 接続が許可されているか確認
5. バックエンドとダッシュボードが相互に到達可能か確認

---

### ユーザーが自動作成されない

**症状:**
- SSO ログインは成功するが digna にユーザーが作成されない
- SSO ログイン後に権限エラーが発生する

**原因と対処法:**
1. OIDC の設定が正しいか確認
2. ユーザー権限の設定を確認
3. digna のログを確認してエラーメッセージを確認
4. バックエンドサービスを再起動
5. 問題が続く場合は support@digna.ai に連絡

---

## サポートされているプロバイダ {: #supported-providers }

### テスト済み & サポート

以下の OIDC プロバイダはテスト済みで動作が確認されています:

| プロバイダ | 構成 URL | セットアップガイド |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### その他の OIDC プロバイダ

OpenID Connect をサポートする任意のプロバイダを統合できます。必要な情報:

- クライアント ID
- クライアントシークレット
- OpenID 構成 URL（通常は `/.well-known/openid-configuration`）
- サポートされるスコープ（通常は `openid profile email`）

特定のプロバイダの統合でサポートが必要な場合は support@digna.ai にご連絡ください。

---

## ベストプラクティス

推奨:
- 本番環境では HTTPS を使用する（HTTP は使用しない）
- クライアントシークレットは安全に保管する（可能な限り環境変数を使用）
- 定期的にシークレットをローテーションする
- まずは非本番環境でテストする
- 設定したプロバイダを文書化する
- ログインログを監視して異常な活動を検出する
- アイデンティティプロバイダの設定を digna 設定と同期させておく

非推奨:
- クライアントシークレットをバージョン管理に保存する
- 本番で HTTP リダイレクト URI を使用する
- 同じキーで複数のプロバイダを設定する
- 本番環境にデフォルト/テスト用資格情報を残す
- シークレットを含む設定ファイルを公開する
- 開発用と本番用の資格情報を混同する

---

## サポート

SSO 設定でサポートが必要ですか？

- Email: support@digna.ai
- ドキュメント: https://docs.digna.ai
- ウェブサイト: https://www.digna.ai

---

**最終更新日:** 2026年8月30日  
**リリース:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
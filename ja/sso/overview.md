# シングルサインオンの概要

---

## 目次

1. [導入と概要](#introduction-and-overview)
2. [プロバイダーガイド](#provider-guides)
3. [設定手順](#configuration-steps)
4. [ダッシュボード設定](#dashboard-configuration)
5. [バックエンド設定](#backend-configuration)
6. [ログインのテスト](#testing-login)
7. [トラブルシューティング](#troubleshooting)
8. [サポートされているプロバイダー](#supported-providers)

---

## 導入と概要 {: #introduction-and-overview }

このガイドは、**OpenID Connect (OIDC)** を使用して digna プラットフォームにシングルサインオン (SSO) を統合するための手順を段階的に説明します。

### SSO とは？

シングルサインオンにより、外部のアイデンティティプロバイダーを使って企業の資格情報で安全に digna にログインできます。ユーザーは digna 用の別パスワードを管理する代わりに、企業の認証情報で認証できます。

### 動作の仕組み

digna の SSO は OIDC プロトコルを使って実装されています。複数のアイデンティティプロバイダーを並行して設定するには、次の 2 つの主要な設定ファイルを調整します。

- **`dashboard_config.toml`** — フロントエンドのログインインターフェースを制御
- **`config.toml`** — バックエンドの OIDC 接続を設定

### 対応プロバイダー {: #supported-providers-overview }

このガイドの例では **Microsoft** と **Google** を使用していますが、**OIDC 準拠のプロバイダーであればどれでも**同じ構成で統合できます。

---

## プロバイダーガイド {: #provider-guides }

すべてのプロバイダーは共通してクライアント ID、クライアントシークレット、リダイレクト URI、ディスカバリー URL の 4 つの値が必要ですが、それらが管理コンソール上のどこにあるかはプロバイダーごとに異なり、いくつかは他のプロバイダーにはない特有の手順があります。以下のガイドはプロバイダー側の作業をカバーし、このページはすべてのプロバイダーで共通の digna 側の設定を説明します。

| Provider | Guide | Worth knowing |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | Self-hosted; the only provider here where you control the token service |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | Discovery URL is per-tenant, and custom domains change it |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | Consent screen must be published before non-test users can log in |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | Self-hosted; discovery URL is per-realm |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID appears in the discovery URL; secrets expire |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | Authorization server choice changes the discovery URL |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | The OIDC app type must be chosen at creation and cannot be changed |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | Environment ID appears in the discovery URL |

その他の OIDC 準拠プロバイダーも同様に統合可能です — 詳しくは [Other OIDC Providers](#supported-providers) を参照してください。

---

## 設定手順 {: #configuration-steps }

SSO の設定には 2 つのファイルの更新が必要です。本セクションではそれぞれの設定方法を説明します。

### 設定ファイルの概要

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | フロントエンドのログインインターフェース |
| **config.toml** | `/config.toml` | バックエンドの OIDC 接続 |

SSO を正しく機能させるには両方のファイルを設定する必要があります。

---

## ダッシュボード設定 {: #dashboard-configuration }

### ファイルの場所

```
dashboard/dashboard_config.toml
```

### ステップ 1: OIDC プロバイダーの追加

サポートしたい各アイデンティティプロバイダーのために `[[login.oidc]]` 配列の下にエントリを追加します。

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

### 設定パラメーター

#### `[[login.oidc]]` セクション

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | OIDC 接続の一意な識別子（config.toml の key と一致する必要があります） |
| `label` | string | Yes | ログインボタンに表示されるテキスト（例: "Login with Microsoft"） |

#### `[login]` セクション

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | SSO に加えてパスワードベースのログインを許可するかどうか |

### usePassword の理解

**`usePassword = true` の場合:**
- ログイン画面に SSO ボタン（例: "Login with Microsoft"）が表示されます
- ログイン画面にユーザー名とパスワードのフィールドも表示されます
- ユーザーはどちらの方法でも認証できます
- 一部のユーザーは SSO、別のユーザーはパスワードを使うハイブリッド構成が可能です

**`usePassword = false`（または省略）の場合:**
- ログイン画面には SSO ボタンのみ表示されます
- ユーザー名/パスワードのフィールドは表示されません
- OIDC による認証のみが利用可能です

!!! tip "ヒント"

    パスワードベースのログインは、`digna user add` コマンドまたはダッシュボードを使ってパスワードで作成されたユーザーでのみ利用可能です。

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

## バックエンド設定 {: #backend-configuration }

### ファイルの場所

```
/config.toml
```

(Root digna installation directory)

### ステップ 1: OIDC プロバイダーセクションの追加

各プロバイダーごとに専用の `[oidc.<key>]` セクションを作成します。key は `dashboard_config.toml` で定義した `key` と一致する必要があります。

### Microsoft の設定

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google の設定

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### 設定パラメーター

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | アイデンティティプロバイダーからのクライアント ID | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | アイデンティティプロバイダーからのクライアントシークレット | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | 認証後のコールバック URL | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC の設定エンドポイント | `https://login.microsoftonline.com/...` |

!!! warning "重要"

    プレースホルダー (`<client_id>`, `<client_secret>`, `<tenant_id>`) を実際のアイデンティティプロバイダーの開発者ポータルから取得した値に置き換えてください。

### リダイレクト URI

リダイレクト URI はアイデンティティプロバイダーの設定と同一である必要があります:

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

設定を完了したら、SSO が正しく動作するか確認します。

### テスト前チェックリスト

テスト前に確認してください:

- [ ] `dashboard_config.toml` に OIDC プロバイダーが追加されている
- [ ] `config.toml` に OIDC の資格情報が追加されている
- [ ] 両ファイルが保存されている
- [ ] 資格情報（クライアント ID、クライアントシークレット）が正しい
- [ ] リダイレクト URI がデプロイ先の URL と一致している
- [ ] アイデンティティプロバイダーのアプリケーションにリダイレクト URI が登録されている

### テスト手順

#### ステップ 1: サービスの再起動

変更を適用するために digna のバックエンドと web サーバーを再起動します。

**Windows でサービスとして実行している場合:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Linux または macOS でサービスとして実行している場合:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**手動で実行している場合:**
```bash
digna serve --address localhost --port 8082
```

**ウェブサーバーも再起動してください** — Windows の場合は IIS や Tomcat、Linux/macOS の場合は nginx や Apache など。

#### ステップ 2: ダッシュボードを開く

ブラウザで digna ダッシュボードを開きます:

```
http://localhost:5173
```

（または設定したダッシュボード URL）

#### ステップ 3: ログインボタンの確認

設定した各プロバイダーのログインボタンが表示されていることを確認します:

- "Login with Microsoft" ボタンが表示されるはず
- "Login with Google" ボタンが表示されるはず
- (もし usePassword = true の場合) ユーザー名/パスワードのフィールドが表示されるはず

ボタンが表示されない場合:
- `dashboard_config.toml` が保存されたか確認
- ダッシュボードサービスを再起動したか確認
- ブラウザのコンソール（F12）でエラーを確認

#### ステップ 4: SSO ログインのテスト

SSO ボタンのひとつ（例: "Login with Microsoft"）をクリックします:

1. アイデンティティプロバイダーのログインページにリダイレクトされるはずです
2. 企業の認証情報でログインしてください
3. digna にリダイレクトされるはずです
4. digna にログインできるはずです

#### ステップ 5: ユーザー作成の確認

SSO ログインが成功した後:

- digna にユーザーが自動作成されるはずです
- ユーザーはログイン状態になるはずです
- ユーザープロファイルにアイデンティティプロバイダーの情報が表示されるはずです
- digna ダッシュボードが表示されるはずです

#### ステップ 6: パスワードログインのテスト（有効な場合）

`usePassword = true` の場合:

1. digna からログアウトする
2. ログインページでユーザー名とパスワードを入力する
3. パスワードでログインできるはずです

---

## トラブルシューティング {: #troubleshooting }

### ログインボタンが表示されない

**症状:**
- ログインページに OIDC ログインボタンが表示されない
- (usePassword = true の場合) パスワード欄のみ表示される

**原因と解決策:**
1. `dashboard_config.toml` が `dashboard/` ディレクトリにあるか確認
2. `[[login.oidc]]` セクションが正しい構文で存在するか確認
3. ダッシュボードサービスを再起動
4. ブラウザキャッシュをクリア（Ctrl+Shift+Delete または Cmd+Shift+Delete）
5. ブラウザのコンソール（F12 → Console タブ）でエラーを確認

---

### リダイレクト URI の不一致エラー

**症状:**
- SSO ボタンをクリックした後で "redirect_uri mismatch" エラーが出る
- "The redirect URI is not registered" エラーが出る

**原因と解決策:**
1. `config.toml` の `DIGNA_OIDC_REDIRECT_URI` が正しいか確認
2. アイデンティティプロバイダーの設定でリダイレクト URI が登録されているか確認
3. 両方が完全に同一の URL（プロトコル、ドメイン、パスを含む）を使用しているか確認
4. リダイレクト URI にタイプミスがないか確認
5. HTTPS を使っている場合は証明書が有効か確認

---

### クライアント資格情報が無効エラー

**症状:**
- "Invalid client ID or secret" エラーが出る
- 認証が資格情報エラーで失敗する

**原因と解決策:**
1. `DIGNA_OIDC_CLIENT_ID` と `DIGNA_OIDC_CLIENT_SECRET` が正しいか確認
2. 余計な空白や特殊文字が入っていないか確認
3. 資格情報が期限切れまたは取り消されていないか確認
4. 設定を更新した後にバックエンドサービスを再起動
5. アイデンティティプロバイダーのコンソールで資格情報が有効か確認

---

### ログインがハングする、タイムアウトする

**症状:**
- SSO ボタンをクリックしても何も起こらない
- 数秒後にタイムアウトする
- ブラウザに "Failed to connect" のような表示が出る

**原因と解決策:**
1. digna バックエンドが実行中か確認: `digna repo check`
2. アイデンティティプロバイダーへのネットワーク接続を確認
3. `DIGNA_OIDC_CONFIGURATION_URL` にアクセスできるか確認
4. ファイアウォールでアウトバウンド HTTPS 接続が許可されているか確認
5. バックエンドとダッシュボードが互いに到達可能か確認

---

### ユーザーが自動作成されない

**症状:**
- SSO ログインは成功するが digna にユーザーが作成されない
- SSO ログイン後に権限エラーが発生する

**原因と解決策:**
1. OIDC 設定が正しいか確認
2. ユーザーの権限設定が正しいか確認
3. digna ログを確認してエラーメッセージを参照
4. バックエンドサービスを再起動
5. 問題が解決しない場合は support@digna.ai に連絡

---

## サポートされているプロバイダー {: #supported-providers }

### テスト済み & サポート対象

以下の OIDC プロバイダーはテストされ、動作が確認されています:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### その他の OIDC プロバイダー

OpenID Connect をサポートするプロバイダーであれば統合可能です。必要な情報:

- クライアント ID
- クライアントシークレット
- OpenID 設定 URL（通常 `/.well-known/openid-configuration` にあります）
- サポートされるスコープ（通常 `openid profile email`）

特定のプロバイダーの統合で支援が必要な場合は support@digna.ai にお問い合わせください。

---

## ベストプラクティス

**やるべきこと:**
- 本番環境では HTTPS を使用する（HTTP は使わない）
- クライアントシークレットは安全に保管する（可能なら環境変数を使用）
- シークレットは定期的にローテーションする
- まずは非本番環境でテストする
- どのプロバイダーが設定されているかを文書化する
- ログインログを監視して異常なアクティビティを検出する
- アイデンティティプロバイダーの設定と digna の設定を同期させる

**やってはいけないこと:**
- クライアントシークレットをバージョン管理に保存する
- 本番で HTTP のリダイレクト URI を使う
- 同じ key を使って複数のプロバイダーを設定する
- 本番環境にデフォルト/テスト用の資格情報を残す
- シークレットを含む設定ファイルを公開する
- 開発用と本番用の資格情報を混在させる

---

## サポート

SSO 設定で助けが必要ですか？

- **Email:** support@digna.ai
- **Documentation:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**最終更新日:** 2026年8月30日  
**リリース:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
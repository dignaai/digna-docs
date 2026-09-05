---
title: Google Workspace SSO — シングルサインオン統合 | digna ドキュメント
description: OpenID Connect を使って Google Workspace で digna のシングルサインオンを設定する方法 — OAuth 同意画面、OAuth クライアント ID、承認済みリダイレクト URI と対応する digna の設定
image: /assets/logo_square.png
keywords: digna sso, Google Workspace SSO, Google OIDC, OAuth 同意画面, OpenID Connect, エンタープライズ認証
---

# Google Workspace で SSO を設定する

Google の識別プラットフォームは OIDC 準拠で、全ての顧客に対して単一の well-known discovery URL を使用するため、組織ごとに異なるのはクライアント ID とシークレットだけです。

このガイドは **Google 側** — OAuth クライアントの作成と digna が必要とする値の収集 — を扱います。digna 側（`dashboard_config.toml`、テスト、トラブルシューティング）はプロバイダに関係なく同じで、[Single Sign-On Overview](overview.md) に記載されています。

---

## 開始前の確認

| 要件 | メモ |
|---|---|
| **Google Cloud プロジェクト** | Workspace ドメインと同じ組織内の任意のプロジェクト |
| **ロール** | プロジェクト上の Editor または Owner |
| **digna のリダイレクト URI** | ログイン後にユーザーが戻る URL（例: `https://digna.yourdomain.com/oidc/callback`） |

---

## ステップ 1: OAuth 同意画面の設定

Google は同意画面が存在するまで資格情報を発行しません。

1. [Google Cloud Console](https://console.cloud.google.com) を開き、プロジェクトを選択します
2. **APIs & Services → OAuth consent screen** に移動します
3. ユーザータイプを選択します:
   - **Internal** — Workspace ドメイン内のアカウントのみがログインできます。推奨設定です。
   - **External** — 任意の Google アカウントがログインを試みることができます。
4. アプリ名、ユーザーサポートメール、開発者連絡先メールを入力します
5. **Scopes** のステップで、`openid`、`.../auth/userinfo.email`、`.../auth/userinfo.profile` を追加します
6. 保存します

!!! warning "外部アプリは公開する必要があります"

    **External** の同意画面は *Testing* ステータスで開始され、その場合はテストユーザーリストに明示的に追加されたアカウントのみがログインを完了できます。それ以外のユーザーには「digna は Google の検証プロセスを完了していません」と表示されます。**Publishing status** でアプリを **In production** に切り替すか、Workspace 専用の配備であれば制限のない **Internal** を使用してください。

---

## ステップ 2: OAuth クライアントの作成

1. **APIs & Services → Credentials** に移動します
2. **Create Credentials → OAuth client ID** をクリックします
3. **Application type** を **Web application** に設定します
4. 名前を付けます（例: `digna`）
5. **Authorized redirect URIs** の下で **Add URI** をクリックし、以下を入力します:

```
https://digna.yourdomain.com/oidc/callback
```

6. **Create** をクリックします

!!! note "承認された JavaScript オリジンは不要です"

    digna はブラウザではなくバックエンドで認可コードを交換するため、**Authorized JavaScript origins** フィールドは空のままで問題ありません。重要なのはリダイレクト URI だけです。

---

## ステップ 3: 資格情報の取得

作成後に表示されるダイアログには次が表示されます:

- **Client ID** — `.apps.googleusercontent.com` で終わる → `DIGNA_OIDC_CLIENT_ID` になります
- **Client secret** → `DIGNA_OIDC_CLIENT_SECRET` になります

どちらも他の多くのプロバイダとは異なり、後から資格情報の詳細ページで再取得できます。

---

## ステップ 4: ディスカバリー URL

Google は全顧客に対して単一のディスカバリー URL を使用します — 置換する値はありません:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## ステップ 5: digna の設定

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

両方のファイルで `key` が一致している必要があります — ここでは `google` です。

---

## ステップ 6: テスト

バックエンドとウェブサーバを再起動し、ダッシュボードを開きます。チェックリストの完全版は [Testing Login](overview.md#testing-login) を参照してください。

---

## Google Workspace のトラブルシューティング

### Error 400: redirect_uri_mismatch

`DIGNA_OIDC_REDIRECT_URI` に設定した URI が **Authorized redirect URIs** リストに含まれていないか、末尾のスラッシュやスキームが異なっています。Google のエラーページには受け取った URI が表示されるので、登録済みの URI と 1 文字ずつ比較してください。

### This App Is Blocked / Has Not Completed Verification

同意画面が **External** かつまだ *Testing* の状態です。公開するか、アプリを **Internal** に切り替えてください。

### Access Blocked: Authorization Error

ログインを試みているアカウントが Workspace ドメイン外で、同意画面が **Internal** に設定されています。Internal アプリは組織内のアカウントのみを受け入れる意図された挙動です。

### 変更の反映に数分かかる

Google は資格情報と同意画面の変更を非同期で伝播します。新しく追加したリダイレクト URI が有効になるまで数分かかる場合があります。変更が無視されたように見える場合は、調査を開始する前に少し待ってから再試行してください。

---

## 参照

- [Single Sign-On Overview](overview.md) — 設定リファレンス、テスト、一般的なトラブルシューティング
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
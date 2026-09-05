---
title: Microsoft Entra ID SSO – シングルサインオン統合 | digna ドキュメント
description: digna を Microsoft Entra ID (旧 Azure AD) の OpenID Connect でシングルサインオンに設定する方法 — アプリ登録、リダイレクト URI、クライアントシークレット、テナント ID と digna の対応設定。
image: /assets/logo_square.png
keywords: digna sso, Microsoft Entra ID, Azure AD SSO, OIDC 統合, アプリ登録, エンタープライズ認証
---

# Microsoft Entra ID で SSO を設定する

Microsoft Entra ID（旧 Azure Active Directory）は完全に OIDC に準拠したプロバイダーで、digna は標準のディスカバリーエンドポイントを通じて統合できます。

このガイドは **Entra ID 側**（アプリの登録と digna に必要な 4 つの値の取得）を扱います。digna 側（`dashboard_config.toml`、テストおよびトラブルシューティング）はプロバイダーに依らず共通で、[Single Sign-On Overview](overview.md) に記載されています。

---

## はじめる前に

| 要件 | 補足 |
|---|---|
| **Entra ID ロール** | Application Administrator、Cloud Application Administrator、または Global Administrator |
| **digna リダイレクト URI** | ログイン後にユーザーが戻る URL、例: `https://digna.yourdomain.com/oidc/callback` |
| **テナント** | ユーザーがサインインするディレクトリ |

---

## ステップ 1: アプリケーションを登録する

1. [Microsoft Entra 管理センター](https://entra.microsoft.com) にサインインします
2. **Identity → Applications → App registrations** に移動します
3. **New registration** をクリックします
4. 設定:
   - **Name**: `digna`（同意画面でユーザーに表示されます）
   - **Supported account types**: *Accounts in this organizational directory only*（シングルテナント構成の場合）
5. **Redirect URI** の下でプラットフォーム **Web** を選び、digna のコールバック URL を入力します:

```
https://digna.yourdomain.com/oidc/callback
```

6. **Register** をクリックします

!!! warning "重要"

    プラットフォームは **Web** でなければなりません。*Single-page application* ではありません。digna はバックエンドでクライアントシークレットを使って認可コードを交換するため、SPA プラットフォームタイプでは許可されません。

---

## ステップ 2: クライアント ID とテナント ID を取得する

アプリケーションの **Overview** ページで、次をコピーします:

- **Application (client) ID** → `DIGNA_OIDC_CLIENT_ID` になります
- **Directory (tenant) ID** → ディスカバリー URL に入れます

---

## ステップ 3: クライアント シークレットを作成する

1. **Certificates & secrets → Client secrets** に移動します
2. **New client secret** をクリックします
3. 説明を入力し、有効期限を選択します
4. **Add** をクリックします
5. **Value** 列をすぐにコピーします

!!! warning "Value をコピーしてください、Secret ID ではありません"

    **Value** はこのページで一度だけ表示され、後から取得できません。隣の **Secret ID** は似て見えますがシークレットではありません — それを使用するとログイン時に `invalid_client` エラーになります。ページを離れる前にコピーし忘れた場合は、シークレットを削除して新しく作成してください。

!!! tip "ヒント"

    Entra ID はシークレットの有効期間を最大 24 か月に制限するため、すべての SSO 統合には有効期限があります。どこか目に付く場所に記録しておいてください — シークレットが期限切れになると、ログインページに警告なしで全ユーザーの SSO が一斉に停止します。

---

## ステップ 4: API 権限を確認する

1. **API permissions** に移動します
2. **Microsoft Graph → User.Read**（委任済み）が存在することを確認します — これはデフォルトで追加されます

digna が要求する `openid`、`profile`、`email` のスコープは標準の OIDC セットの一部であり、別途付与は不要です。テナントがすべてのアプリに管理者同意を要求する場合は、**Grant admin consent for &lt;tenant&gt;** をクリックしてください。

---

## ステップ 5: ディスカバリー URL を作成する

ステップ 2 で取得した **Directory (tenant) ID** を置き換えます:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "v2.0 エンドポイントを使う"

    `/v2.0/` セグメントは重要です。`https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` の v1.0 エンドポイントは古い形式でトークンを発行し、digna が期待する標準の OIDC クレームを返しません。

続行する前にブラウザで URL を開いてください。JSON ドキュメントが表示されればテナント ID が正しいことが確認できます。

---

## ステップ 6: digna を設定する

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

両ファイルの `key` は一致している必要があります — ここでは `microsoft` です。

---

## ステップ 7: テスト

バックエンドとウェブサーバーを再起動し、ダッシュボードを開きます。チェックリストの全項目は [Testing Login](overview.md#testing-login) を参照してください。

---

## Entra ID のトラブルシューティング

### AADSTS50011: Redirect URI の不一致

`DIGNA_OIDC_REDIRECT_URI` に設定した URI がステップ 1 で登録したものと異なります。Entra ID は文字列全体を比較するため、末尾のスラッシュ、`http` と `https`、異なるポートなども不一致と見なされます。**Authentication → Web → Redirect URIs** を確認してください。

### AADSTS7000215: 無効なクライアント シークレット

**Secret ID** をコピーしてしまったか、シークレットが期限切れになっています。新しいシークレットを作成し、Value 列をコピーしてください。

### AADSTS650057: 無効なリソース

アプリ登録が削除されているか、ディスカバリー URL にあるテナントと異なるテナントに属しています。Overview ページで Directory (tenant) ID を確認してください。

### ユーザーはログインするが何も起きない

テナントが管理者の同意を必要としていて同意が付与されていない場合、リダイレクトは有効なトークンを伴わずに戻ってきます。**API permissions** で管理者同意を付与してください。

---

## 関連項目

- [Single Sign-On Overview](overview.md) — 設定リファレンス、テストおよび一般的なトラブルシューティング
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
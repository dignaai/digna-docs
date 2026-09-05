---
title: OneLogin SSO – シングルサインオン統合 | digna ドキュメント
description: OpenID Connect を使って OneLogin で digna のシングルサインオンを構成します — OIDC アプリの作成、リダイレクトURI、クライアント資格情報、トークンエンドポイント認証、および対応する digna の設定。
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, OpenID Connect, トークンエンドポイント認証, 企業向け認証
---

# OneLoginでSSOを設定する

OneLoginはOIDC準拠です。特徴的なのは、アプリ作成時にカタログからコネクタータイプを選択し、後から変更できない点です。

このガイドは**OneLogin側**（アプリの作成とdignaが必要とする値の収集）を扱います。digna側 — `dashboard_config.toml`、テストおよびトラブルシューティング — はプロバイダーに依存せず共通で、[Single Sign-On Overview](overview.md) に記載されています。

---

## はじめる前に

| 要件 | 補足 |
|---|---|
| **OneLogin のロール** | アカウント所有者またはアプリの追加が許可された管理者 |
| **サブドメイン** | 例: `yourcompany.onelogin.com` |
| **digna のリダイレクトURI** | ログイン後にユーザーが戻るURL。例: `https://digna.yourdomain.com/oidc/callback` |

---

## ステップ 1: OIDC アプリケーションを作成する

1. OneLogin 管理ポータルにサインインします
2. **Applications → Applications** に移動します
3. **Add App** をクリックします
4. `OpenId Connect` を検索し、**OpenId Connect (OIDC)** コネクタを選択します
5. **Display Name** を `digna` に設定します
6. **Save** をクリックします

!!! warning "コネクタータイプは作成時に固定されます"

    OneLogin では SAML と OIDC 用に別々のカタログエントリがあり、アプリを一方から他方へ変換することはできません。誤って SAML コネクタを選んだ場合は、アプリを削除して再作成してください — プロトコルを切り替える設定はありません。

---

## ステップ 2: リダイレクトURIを設定する

1. **Configuration** タブを開きます
2. **Redirect URI's** にあなたの digna コールバックURLを入力します:

```
https://digna.yourdomain.com/oidc/callback
```

3. 必要に応じて **Post Logout Redirect URIs** にダッシュボードのURLを設定します
4. **Save** をクリックします

!!! note "URIは1行ごとに記述します"

    カンマ区切りのリストを想定するプロバイダーとは異なり、OneLogin の **Redirect URI's** フィールドは1行につき1つのURIを受け取ります。

---

## ステップ 3: アプリケーションタイプと認証方法を設定する

1. **SSO** タブを開きます
2. **Application Type** が *Web* になっていることを確認します
3. **Token Endpoint → Authentication Method** を *POST* (`client_secret_post`) か *Basic* (`client_secret_basic`) に設定します

!!! warning "None を選ばないでください"

    認証方法を *None* に設定するとアプリがシークレットなしのパブリッククライアントになり、digna のバックエンドでのコード交換が拒否されます。POST か Basic のいずれかを使用してください。

---

## ステップ 4: 資格情報を取得する

引き続き **SSO** タブ上で:

- **Client ID** → `DIGNA_OIDC_CLIENT_ID` になります
- **Client Secret** → `DIGNA_OIDC_CLIENT_SECRET` になります（**Show client secret** をクリック）

ページには **Issuer URL** も表示されており、次のステップで使用するディスカバリーURLを確認できます。

---

## ステップ 5: ユーザーを割り当てる

1. **Access** タブを開きます
2. digna を使用できるロールやグループを追加します
3. **Save** をクリックします

!!! note "割り当てられていないユーザーはログイン後に拒否されます"

    ほとんどのプロバイダーと同様に、OneLogin は先にユーザーを認証し、次に権限を確認します。割り当てられていないユーザーはサインイン自体には成功しますが、その後拒否されるため、digna のエラーのように見えることがあります。

---

## ステップ 6: ディスカバリーURLを作る

OneLogin のサブドメインを差し替えます:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

例:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 は API バージョンです"

    OneLogin の現在の OIDC 実装は `/oidc/2/` の下にあります。古いドキュメントではバージョンなしの `/oidc/` が示されており、これは廃止された最初のバージョンを指します。疑わしい場合は SSO タブに表示されている **Issuer URL** と比較してください — ディスカバリーURLは Issuer に `/.well-known/openid-configuration` を付けたものです。

---

## ステップ 7: digna を設定する

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

両ファイルの `key` は一致している必要があります — ここでは `onelogin` です。

---

## ステップ 8: テスト

バックエンドとウェブサーバーを再起動し、ダッシュボードを開きます。完全なチェックリストは [Single Sign-On Overview](overview.md#testing-login) を参照してください。

---

## OneLogin のトラブルシューティング

### redirect_uri did not match

コールバックURLが **Configuration → Redirect URI's** に無い、またはエントリがカンマで区切られていて改行になっていません。

### invalid_client at the Token Step

**Token Endpoint → Authentication Method** が *None* に設定されているか、`config.toml` のクライアントシークレットが古くなっています。**SSO** タブでシークレットを表示して比較してください。

### アプリがユーザーに表示されない

**Access** タブでどのロールやグループにもアクセス権が付与されていません。

### ディスカバリーURLで404になる

サブドメインが間違っているか、URL に `/oidc/2/` が抜けています。SSO タブに表示されている **Issuer URL** と比較してください。

---

## 関連項目

- [Single Sign-On Overview](overview.md) — 設定リファレンス、テストおよび一般的なトラブルシューティング
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)
---
title: AD FS SSO – シングルサインオン統合 | digna ドキュメント
description: Active Directory Federation Services を使用した OpenID Connect による digna のシングルサインオンを設定します — アプリケーショングループ、サーバーアプリケーション、共有シークレット、許可されたスコープ、および対応する digna 設定。
image: /assets/logo_square.png
keywords: digna sso, adfs sso, Active Directory Federation Services, adfs oidc, アプリケーショングループ, OpenID Connect, オンプレミスのアイデンティティプロバイダー
---

# AD FS で SSO を設定する

Active Directory Federation Services はオンプレミスの選択肢です: 自分のサーバーがトークンを発行し、discovery URL は自分のホスト名になります。AD FS は **Windows Server 2016** 以降で OpenID Connect をサポートします。

このガイドは **AD FS 側** を扱います: アプリケーショングループの作成と digna が必要とする値の収集方法です。digna 側 — `dashboard_config.toml`、テストとトラブルシューティング — はプロバイダーに依存せず共通であり、[Single Sign-On Overview](overview.md) に記載されています。

---

## 開始前に

| 要件 | 備考 |
|---|---|
| **AD FS のバージョン** | Windows Server 2016 以降 — それ以前のバージョンは OIDC をサポートしていません |
| **アクセス権** | AD FS サーバーのローカル管理者 |
| **フェデレーションサービス名** | 例: `adfs.yourdomain.com` |
| **digna リダイレクト URI** | ログイン後にユーザーが戻る URL、例: `https://digna.yourdomain.com/oidc/callback` |

---

## ステップ 1: アプリケーショングループを作成する

1. AD FS サーバーで **AD FS Management** を開きます
2. **Application Groups** を右クリックし **Add Application Group** を選択します
3. 名前に `digna` を入力します
4. バージョンによって **Standalone applications** または **Client-Server applications** の下で、**Server application accessing a web API** を選択します
5. **Next** をクリックします

---

## ステップ 2: サーバーアプリケーションを設定する

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS が GUID を生成します。これをコピーしてください — これが `DIGNA_OIDC_CLIENT_ID` になります
3. **Redirect URI**: digna のコールバック URL を入力して **Add** をクリックします:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Next** をクリックします

!!! warning "「Add」をクリックしてください（Next だけでは不十分）"

    リダイレクト URI のフィールドには独立した **Add** ボタンがあります。URI を入力して **Next** を押すだけだと、Add を押さない限りその URI は破棄され、ウィザードは警告を出しません。続行する前にフィールド下のリストに URI が表示されていることを確認してください。

---

## ステップ 3: 共有シークレットを生成する

1. **Generate a shared secret** にチェックを入れます
2. 生成されたシークレットをコピー → これが `DIGNA_OIDC_CLIENT_SECRET` になります
3. **Next** をクリックします

!!! warning "シークレットは一度だけ表示されます"

    AD FS はこのウィザードのページでのみ共有シークレットを表示し、再表示することはできません。紛失した場合は、後でアプリケーショングループのプロパティからリセットしてください。

---

## ステップ 4: Web API を設定する

1. **Identifier**: ステップ 2 のクライアント識別子と同じ値を入力して **Add** をクリックします
2. **Next** をクリックします
3. **Access Control Policy** を選択します — 試験運用では *Permit everyone* が最も簡単です。本番ではグループに制限してください
4. **Next** をクリックします

---

## ステップ 5: 許可するスコープを付与する

**Configure Application Permissions** のステップで、以下にチェックを入れます:

- `openid`
- `profile`
- `email`

その後 **Next** をクリックしてウィザードを完了させます。

!!! warning "openid はデフォルトで選択されていないことがある"

    一部のバージョンでは AD FS が `user_impersonation` のみを事前選択します。`openid` がないとトークンエンドポイントは ID トークンではなく OAuth のアクセストークンを返し、digna はユーザーを識別できません。

---

## ステップ 6: ディスカバリーエンドポイントを確認する

フェデレーションサービス名を置き換えます:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

例:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

ブラウザで開いてください。JSON ドキュメントが表示され、OIDC が有効でホスト名が正しいことを確認できます。

!!! note "バックエンドは証明書を信頼している必要があります"

    AD FS では社内の認証局がよく使われます。digna バックエンドを動かしているマシンはこの URL に対して自身でアウトバウンドの HTTPS 呼び出しを行うため、証明書を発行した CA はそのマシンの信頼ストアに登録されている必要があります — ログインするユーザーのブラウザにだけ入っていれば良い、というわけではありません。

---

## ステップ 7: digna を設定する

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Active Directory でログイン"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

両ファイルの `key` は一致している必要があります — ここでは `adfs` です。

---

## ステップ 8: テスト

バックエンドとウェブサーバーを再起動し、ダッシュボードを開きます。チェックリストの完全版は [Testing Login](overview.md#testing-login) を参照してください。

---

## AD FS のトラブルシューティング

### MSIS9611: The Client Is Not Allowed to Access the Resource

ステップ 4 の Web API 識別子がクライアント識別子と一致していないか、ステップ 5 のスコープが付与されていません。どちらもアプリケーショングループのプロパティから編集可能です。

### MSIS9602: Invalid redirect_uri

URI を入力したが **Add** ボタンで追加していない、あるいは `DIGNA_OIDC_REDIRECT_URI` と異なっています。**Application Groups → digna → digna backend → Properties** を確認してください。

### ID トークンが返されない

アプリケーションの権限に `openid` スコープが含まれていません。

### バックエンドがディスカバリー URL に到達できない

バックエンドホスト上の DNS がフェデレーションサービス名を解決できないか、AD FS の証明書がそのホストで信頼されていません。digna サーバー自身から次を実行してテストしてください: `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration`

### 確認すべきイベント

AD FS サーバーは Event Viewer の **Applications and Services Logs → AD FS → Admin** に失敗を記録します。ブラウザに表示されるより具体的な理由が記録されていることが多いです。

---

## 関連項目

- [Single Sign-On Overview](overview.md) — 設定リファレンス、テスト、および一般的なトラブルシューティング
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
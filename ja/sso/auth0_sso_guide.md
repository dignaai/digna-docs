# Auth0 で SSO を設定する

Auth0 は OIDC 準拠で、テナントごとにディスカバリーエンドポイントを公開します。最も重要なのはテナントドメインで、ディスカバリー URL に現れ、カスタムドメインを有効にすると変わります。

このガイドは **Auth0 側** を扱います: アプリケーションの作成と digna が必要とする値の収集です。digna 側 — `dashboard_config.toml`、テストとトラブルシューティング — はプロバイダに依らず同じで、[シングルサインオンの概要](overview.md) に記載されています。

---

## はじめる前に

| Requirement | Notes |
|---|---|
| **Auth0 role** | テナントの管理者 |
| **Tenant domain** | 例: `yourcompany.eu.auth0.com` — リージョンのセグメントが重要です |
| **digna redirect URI** | ログイン後にユーザーが戻る URL、例: `https://digna.yourdomain.com/oidc/callback` |

---

## ステップ 1: アプリケーションの作成

1. [Auth0 ダッシュボード](https://manage.auth0.com) にサインインします
2. **Applications → Applications** に移動します
3. **Create Application** をクリックします
4. 名前を `digna` とし、**Regular Web Applications** を選択します
5. **Create** をクリックします

!!! warning "Regular Web Applications を選択する"

    *Single Page Application* や *Native* はシークレットのないパブリッククライアントを作成します。digna はバックエンドでコード交換を行い、機密クライアントが必要なので **Regular Web Applications** が正しいタイプです。Auth0 は一部のプロバイダとは異なり、後から **Settings → Application Type** でタイプを変更することができます。

---

## ステップ 2: コールバック URL を追加する

アプリケーションの **Settings** タブで:

1. **Allowed Callback URLs** を見つけます
2. digna のコールバック URL を入力します:

```
https://digna.yourdomain.com/oidc/callback
```

3. 必要に応じて **Allowed Logout URLs** をダッシュボードの URL に設定します
4. 画面下部までスクロールして **Save Changes** をクリックします

!!! note "カンマ区切り、改行区切りではない"

    Auth0 はこのフィールドで複数のコールバック URL をカンマで区切って受け付けます。改行のみで区切られたリストは一つの不正な URL として解釈され、何にもマッチしません。

---

## ステップ 3: クレデンシャルの取得

同じく **Settings** の **Basic Information** パネルで:

- **Domain** → ディスカバリー URL に使います
- **Client ID** → `DIGNA_OIDC_CLIENT_ID` になります
- **Client Secret** → `DIGNA_OIDC_CLIENT_SECRET` になります（クリックして表示）

---

## ステップ 4: Grant Type を確認する

1. **Settings → Advanced Settings → Grant Types** に移動します
2. **Authorization Code** にチェックが入っていることを確認します

Regular Web Applications ではデフォルトで有効です。外れていると digna のログインが `unauthorized_client` で失敗します。

---

## ステップ 5: ディスカバリー URL を作成する

ステップ 3 の **Domain** を差し替えます:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

例:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "カスタムドメインは Issuer を変えます"

    テナントが `login.yourcompany.com` のようなカスタムドメインを使っている場合は、ディスカバリー URL にそのドメインを使ってください。ディスカバリー URL に正規のドメインを使い、ブラウザ側でカスタムドメインを使うなど混在させると issuer の不一致が発生し、ログインは成功してもトークンが拒否されます。

---

## ステップ 6: digna の設定

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

両方のファイルの `key` は一致している必要があります — ここでは `auth0` です。

---

## ステップ 7: テスト

バックエンドとウェブサーバを再起動し、ダッシュボードを開いてください。完全なチェックリストは [ログインのテスト](overview.md#testing-login) を参照してください。

---

## Auth0 のトラブルシューティング

### コールバック URL の不一致

Auth0 のエラーページには受け取った URL が表示されます。**Allowed Callback URLs** にその URL を追加し、エントリがカンマ区切りになっていることを確認してください。

### unauthorized_client

**Advanced Settings → Grant Types** で **Authorization Code** が有効になっていない、またはアプリケーションタイプが Regular Web Applications ではないことが原因です。

### ログインは成功しているのにアクセス拒否される

テナント内の Rule、Action、または Post-Login トリガがユーザーを拒否している可能性があります。**Actions → Flows → Login** と **Monitoring → Logs** のテナントログを確認してください。ログには拒否の具体的な理由が表示されます。

### Issuer の不一致

ディスカバリー URL とブラウザに送られたドメインが異なっています — 通常は正規のテナントドメインとカスタムドメインの混在です。一貫して同じドメインを使用してください。

---

## 関連資料

- [シングルサインオンの概要](overview.md) — 設定リファレンス、テスト、一般的なトラブルシューティング
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
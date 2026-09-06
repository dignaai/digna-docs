# OktaでSSOを設定する

Okta は OIDC 準拠ですが、初めて統合する多くの人がつまずく点がひとつあります: Okta 組織には複数の認可サーバーが公開されており、それぞれ固有の discovery URL を持ちます。

このガイドは **Okta 側** を扱います: アプリ統合を作成し、digna が必要とする値を収集する手順です。digna 側 — `dashboard_config.toml`、テストとトラブルシューティング — はプロバイダに依存せず共通であり、[Single Sign-On Overview](overview.md) に記載されています。

---

## はじめる前に

| Requirement | Notes |
|---|---|
| **Okta role** | Super Administrator、またはアプリ統合を作成できる管理者ロール |
| **Okta domain** | 例: `yourcompany.okta.com`、またはカスタムドメインを設定している場合はそのドメイン |
| **digna redirect URI** | ログイン後にユーザーが戻る URL。例: `https://digna.yourdomain.com/oidc/callback` |

---

## ステップ 1: アプリ統合を作成する

1. Okta 管理コンソールにサインインします
2. **Applications → Applications** に移動します
3. **Create App Integration** をクリックします
4. 次を選択します:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. **Next** をクリックします

!!! warning "アプリケーションの種類は変更できません"

    *Single-Page Application* を選んでしまうとシークレットのないパブリッククライアントが作成され、digna のバックエンドによるコード交換は `invalid_client` エラーで失敗します。種類は作成時に固定されるため、誤って選択した場合はアプリを削除してやり直す必要があります。

---

## ステップ 2: 統合を構成する

1. **App integration name**: `digna`
2. **Grant type**: *Authorization Code* を選んだままにします
3. **Sign-in redirect URIs**: あなたの digna コールバック URL を入力します:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: 任意
5. **Assignments** の下で、誰が統合を使用できるかを選びます — 組織全員に許可するより特定のグループに限定する方が安全です
6. **Save** をクリックします

!!! note "割り当てが必要です"

    Okta はユーザーを認証した後、アプリへの割り当てがあるかを確認します。割り当てされていないユーザーは Okta のログインページで正常にサインインできても、リダイレクト後に拒否されます。自分ではログインできるが同僚ができない場合は、まず割り当てを確認してください。

---

## ステップ 3: 資格情報を収集する

アプリの **General** タブで、**Client Credentials** の下:

- **Client ID** → `DIGNA_OIDC_CLIENT_ID` になります
- **Client secret** → `DIGNA_OIDC_CLIENT_SECRET` になります（目のアイコンをクリックして表示）

---

## ステップ 4: 認可サーバーを選択する

ここで discovery URL が決まります。**Security → API** に移動して、組織内の認可サーバーを確認してください。

**Org authorization server** — Okta 組織自体のトークンを発行するサーバー:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — Okta が作成する `default` を含むカスタムサーバー:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

組み込みサーバーの場合、`<auth_server_id>` は文字通り `default` です:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "どちらを使うべき？"

    組織が API アクセスポリシーのために既にカスタム認可サーバーを標準採用していない限り、**org** 認可サーバーを使用してください。Okta Developer アカウントはデフォルトで `default` を使用しますが、多くの企業組織では無効化されています。両方の URL をブラウザで開き、エラーではなく JSON を返す方が利用可能なサーバーです。

---

## ステップ 5: digna を設定する

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

両ファイルの `key` は一致している必要があります — ここでは `okta` です。

---

## ステップ 6: テスト

バックエンドとウェブサーバーを再起動し、ダッシュボードを開いてください。完全なチェックリストは [Testing Login](overview.md#testing-login) を参照してください。

---

## Okta のトラブルシューティング

### リダイレクト URI が登録されていない

Okta はエラー内に問題のある URI を表示します。**General → Sign-in redirect URIs** と比較してください; Okta は末尾のスラッシュを含めて完全文字列で一致を確認します。

### ユーザーがクライアントアプリケーションに割り当てられていない

アカウントがアプリの割り当てリストに含まれていません。**Assignments** でユーザーまたはそのグループを追加してください。

### 400 Bad Request: Invalid Authorization Server

discovery URL の `<auth_server_id>` が存在しません。多くの場合、`default` が削除されている組織で発生します。実際に利用可能なサーバーは **Security → API** で確認してください。

### invalid_client（トークン取得時）

統合が Single-Page Application として作成されておりクライアントシークレットがありません。Web Application として再作成してください。

---

## 関連情報

- [シングルサインオンの概要](overview.md) — 設定リファレンス、テスト、一般的なトラブルシューティング
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
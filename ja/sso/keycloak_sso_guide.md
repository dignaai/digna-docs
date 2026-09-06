# KeycloakでSSOを設定する

Keycloakはセルフホスト型で、完全にOIDC準拠のアイデンティティプロバイダーです。自分で運用するため、discovery URLはベンダードメインではなく自分のホスト名とrealmから構築されます。

このガイドは**Keycloak側**（クライアントの作成とdignaが必要とする値の収集）を扱います。digna側 — `dashboard_config.toml`、テストとトラブルシューティング — はプロバイダーに依存せず共通であり、[Single Sign-On Overview](overview.md) に記載されています。

---

## はじめる前に

| 要件 | 説明 |
|---|---|
| **Keycloak のバージョン** | ここで使うURLパスは17以降 — 手順4の注記を参照 |
| **Keycloak の権限** | 対象realmでの `realm-admin` 、またはサーバー管理者 |
| **Realm** | dignaユーザーが所属するrealm（必ずしも `master` ではない） |
| **dignaのリダイレクトURI** | ログイン後にユーザーが戻るURL、例: `https://digna.yourdomain.com/oidc/callback` |

---

## ステップ1: Realmを選択する

1. Keycloak管理コンソールを開く  
2. 左上のrealmセレクタで、ユーザーが所属するrealmに切り替える

!!! warning "master リームを使用しないでください"

    `master` リームはKeycloak自体の管理用です。アプリケーションクライアントは専用のrealmに置くべきで、dignaを `master` に置くとそのユーザーがKeycloak管理コンソールに入る経路を得てしまいます。

---

## ステップ2: クライアントを作成する

1. **Clients** に移動して **Create client** をクリック  
2. 設定:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — これは `DIGNA_OIDC_CLIENT_ID` になります
3. **Next** をクリック
4. **Capability config** ステップで **Client authentication** を **On** にする
5. **Standard flow** は有効のままにする；他のフローは不要です
6. **Next** をクリック

!!! warning "Client authentication をオンにする必要があります"

    **Client authentication** をオフにすると、Keycloakは認証情報を全く持たない *public* クライアントを作成します — この場合、手順4の **Credentials** タブは存在しません。dignaはconfidentialクライアントを必要とします。間違えた場合でもこのトグルは作成後に変更できます。

---

## ステップ3: リダイレクトURIを設定する

**Login settings** ステップ（または後で **Settings** タブ）で:

1. **Valid redirect URIs**: dignaのコールバックURLを入力:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: 空のままにするか、リダイレクトURIをミラーするために `+` を設定する  
3. **Save** をクリック

!!! tip "ワイルドカードは避ける"

    Keycloakは `https://digna.yourdomain.com/*` のようなパターンを受け入れます。ワイルドカードを許すと、そのホスト上の任意のパスが認可コードを受け取れるようになるため、正確なコールバックURLを指定することを推奨します。

---

## ステップ4: クライアントシークレットを取得する

1. **Credentials** タブを開く  
2. **Client Authenticator** が *Client Id and Secret* になっていることを確認  
3. **Client secret** をコピー → これが `DIGNA_OIDC_CLIENT_SECRET` になります

シークレットはここで引き続き取得可能で、**Regenerate** で再生成できます。

---

## ステップ5: Discovery URL を作成する

Keycloakのホストとrealm名を差し替えてください:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

例:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16以前は /auth を含みます"

    Keycloak 17より前は、すべてのエンドポイントが `/auth` プレフィックスの下にありました:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    `KC_HTTP_RELATIVE_PATH=/auth` を設定する配布版は現行バージョンでも旧レイアウトを維持します。もし `/auth` なしのURLが404を返す場合は、`/auth` を付けたURLも試してください。

続行する前にブラウザでそのURLを開いてください。JSONドキュメントが表示されればホストとrealmが正しいことを確認できます。

---

## ステップ6: digna を設定する

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

両ファイルの `key` は一致している必要があります — ここでは `keycloak`。これはKeycloakの**Client ID**と一致している必要はありませんが、同じにしておくと分かりやすいです。

---

## ステップ7: テスト

バックエンドとウェブサーバーを再起動して、ダッシュボードを開いてください。完全なチェックリストは [Testing Login](overview.md#testing-login) を参照してください。

---

## Keycloakのトラブルシューティング

### Invalid parameter: redirect_uri

コールバックURLが **Valid redirect URIs** に含まれていません。Keycloakのサーバーログには受け取ったURIが記録されているので、正確な不一致を確認する最速の方法です。

### Credentialsタブが見当たらない

クライアントがpublicになっています。**Settings → Capability config** で **Client authentication** をオンにしてください。

### Discovery URLで404が返る

realm名が間違っているか、デプロイが `/auth` プレフィックスを使っています。管理コンソールのrealm一覧を確認し、両方のURL形式を試してください。

### unauthorized_client または invalid_client

**Capability config** で **Standard flow** が無効になっているか、Keycloakでシークレットが再生成されて `config.toml` を更新していない可能性があります。

### バックエンドからの証明書エラー

プライベートまたは自己署名証明書を使うセルフホストのKeycloakは、dignaのバックエンドの外向きHTTPS呼び出しで失敗します。dignaバックエンドを実行しているマシンのトラストストアに発行元CAをインストールしてください。

---

## 関連項目

- [Single Sign-On Overview](overview.md) — 設定リファレンス、テスト、一般的なトラブルシューティング  
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)
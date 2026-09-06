# PingOneでSSOを設定する

PingOneはOIDC準拠です。注意が必要な値が2つあります：すべてのエンドポイントURLに現れる**Environment ID**と、北米・欧州・カナダ・アジア太平洋・オーストラリアのテナントで異なる**地域ドメイン**です。

このガイドは**PingOne側**（アプリケーションの作成とdignaが必要とする値の収集）を扱います。digna側の設定 — `dashboard_config.toml`、テストとトラブルシューティング — はプロバイダに関係なく同じで、[Single Sign-On Overview](overview.md)に記載されています。

---

## 開始前に

| 要件 | 補足 |
|---|---|
| **PingOneの役割** | 対象環境でのEnvironment AdminまたはIdentity Data Admin |
| **環境** | dignaユーザーが所属するPingOne環境 |
| **dignaのリダイレクトURI** | ログイン後にユーザーが戻るURL、例： `https://digna.yourdomain.com/oidc/callback` |

---

## ステップ1: アプリケーションを作成する

1. PingOneの管理コンソールにサインインし、環境を選択します
2. **Applications → Applications** に移動します
3. **+** ボタンをクリックします
4. **Application Name** に `digna` と入力します
5. **OIDC Web App** を選択します
6. **Save** をクリックします

!!! warning "Single-Page AppではなくOIDC Web Appを選択する"

    *Single-Page App* と *Native App* はシークレットを保持できないパブリッククライアントを作成します。dignaはバックエンドで認可コードを交換するため、機密クライアントである **OIDC Web App** タイプが必要です。

---

## ステップ2: リダイレクトURIを設定する

1. アプリケーションの **Configuration** タブを開きます
2. 鉛筆アイコンをクリックして編集します
3. **Response Type** が *Code*、**Grant Type** が *Authorization Code* になっていることを確認します
4. **Redirect URIs** にdignaのコールバックURLを入力します：

```
https://digna.yourdomain.com/oidc/callback
```

5. **Token Endpoint Authentication Method** を *Client Secret Post* または *Client Secret Basic* に設定します
6. **Save** をクリックします

---

## ステップ3: アプリケーションを有効にする

アプリケーションの行または詳細パネルで、トグルを **enabled** に切り替えます。

!!! warning "新しいアプリケーションは初めは無効になっています"

    PingOneはアプリケーションを無効な状態で作成します。無効なアプリケーションは認可ステップでトグルについて言及しないエラーを発生させるため、他のデバッグを始める前にこの点を確認する価値があります。

---

## ステップ4: スコープを付与する

1. **Resources** タブを開きます
2. `openid` が付与されていることを確認し、**OpenID Connect** リソースから `profile` と `email` を追加します
3. **Save** をクリックします

---

## ステップ5: ユーザーを割り当てる

1. **Access** タブを開きます
2. dignaを使用できるユーザーが属するポピュレーションまたはグループを追加します
3. **Save** をクリックします

---

## ステップ6: 認証情報とEnvironment IDを取得する

**Configuration** タブで **General** を展開します：

- **Client ID** → `DIGNA_OIDC_CLIENT_ID` になります
- **Client Secret** → `DIGNA_OIDC_CLIENT_SECRET` になります（目のアイコンをクリック）
- **Environment ID** → ディスカバリURLに使用します

同じタブに準備済みの **OIDC Discovery Endpoint** が表示されており、自分で組み立てる代わりに直接コピーできます。

---

## ステップ7: Discovery URLを作成する

環境IDと地域のドメインを置き換えます：

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| リージョン | ドメイン |
|---|---|
| 北米 | `auth.pingone.com` |
| ヨーロッパ | `auth.pingone.eu` |
| カナダ | `auth.pingone.ca` |
| アジア太平洋 | `auth.pingone.asia` |
| オーストラリア | `auth.pingone.com.au` |

ヨーロッパ環境の例：

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "入力するよりコピーする"

    地域ドメインはPingOne統合で最も多いミスであり、誤ったリージョンだと有益なメッセージではなく404が返ります。ステップ6で表示される **OIDC Discovery Endpoint** の値を使用してください。

---

## ステップ8: dignaを設定する

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

両ファイルの `key` は一致している必要があります — この例では `pingone`。

---

## ステップ9: テスト

バックエンドとウェブサーバを再起動し、ダッシュボードを開きます。チェックリスト全体は [ログインのテスト](overview.md#testing-login) を参照してください。

---

## PingOneのトラブルシューティング

### Discovery URLで404エラー

地域ドメインまたはEnvironment IDが間違っています。アプリケーションのConfigurationタブに表示される **OIDC Discovery Endpoint** と比較してください。

### NOT_FOUND またはアプリケーションが無効

ステップ3のアプリケーショントグルがオフのままです。

### リダイレクトURIの不一致

PingOneは完全な文字列を照合します。末尾のスラッシュやスキームの違いがないか **Configuration → Redirect URIs** を確認してください。

### ログインは成功するが、メールクレームがdignaに届かない

**Resources** タブで `email` と `profile` スコープが付与されていません。

### ユーザーがアプリケーションを表示できない

**Access** タブでポピュレーションまたはグループにアクセスが付与されていません。

---

## 関連情報

- [シングルサインオン概要](overview.md) — 設定リファレンス、テスト、一般的なトラブルシューティング
- [PingOne: OIDC アプリケーション設定](https://docs.pingidentity.com/pingone/)
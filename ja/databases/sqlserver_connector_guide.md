# MS SQL Server 用ソースコネクター

このガイドでは、**DSN レス** の接続文字列を使用して、**ODBC** 経由で Microsoft SQL Server に接続するよう *digna* を
設定する方法を説明します。

セットアップの *digna* 側（接続を作成する場所、プロパティ値の暗号化方法、接続のテスト方法、プロファイリングモードの意味）は
すべてのテクノロジーで共通であり、[データベース接続の概要](overview.md) で説明しています。このページでは SQL Server
固有の内容を扱います。

!!! note "Azure Synapse Analytics"

    Synapse も SQL Server 接続として設定しますが、ホスト名が異なり、追加の考慮事項がいくつかあります。
    [Azure Synapse](azure_synapse_connector_guide.md) を参照してください。

---

## 1. ODBC ドライバーをインストールする {: #1-install-the-odbc-driver }

[Microsoft のインストールガイド](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server) に従って、
*digna* バックエンドを実行するマシンに **ODBC Driver 18 for SQL Server** をインストールします。

Windows に **SQL Server** という名前だけで同梱されているドライバーも動作しますが、とうの昔に後継に置き換えられており、
最新の TLS 設定にも Azure 認証にも対応していません。最新のドライバーをインストールできない場合にのみ使用してください。

[digna ホストに ODBC ドライバーをインストールする](overview.md#install-the-driver) の説明に従って、ホスト上で登録されている
正確なドライバー名を確認してください。

---

## 2. ODBC プロパティ {: #2-odbc-properties }

!!! important "これは例であり、仕様ではありません"

    以下のセットは、動作が確認されている組み合わせの 1 つです。プロパティは Microsoft の ODBC ドライバーに属するため、
    その名前、既定値、受け付ける値はドライバーのバージョン（例えば Driver 18 は既定で暗号化しますが、Driver 17 は
    そうではありませんでした）やプラットフォームによって異なります。これを出発点として使用し、インストールした
    ドライバーバージョンのドキュメントを確認してください。

**Add DB Connection** 画面で次のプロパティを追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | *digna* ホストに登録されているドライバー名と一致している必要があります |
| `SERVER` | `sql.example.com` | サーバー名または IP アドレス。名前付きインスタンスは `host\instance`、既定以外のポートは `host,1433` |
| `PORT` | `1433` | ポートがすでに `SERVER` に含まれている場合は省略します |
| `DATABASE` | `digna_source_db` | ソーススキーマを保持するデータベース。この接続でプロファイリングできる唯一のデータベースです |
| `UID` | `digna_source_user` | データベースユーザー |
| `PWD` | `<password>` | **Encrypted** をオンにします |

生成される接続文字列は次のようになります。

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### ODBC Driver 18 での暗号化

Driver 18 は既定で接続を暗号化し、サーバー証明書を検証します。*digna* ホストが信頼していない証明書（一般的には自己署名
証明書）を持つサーバーに対しては、証明書チェーンのエラーで接続に失敗します。次を追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `Encrypt` | `yes` | Driver 18 の既定値。サーバーが TLS に対応できない場合にのみ `no` に設定します |
| `TrustServerCertificate` | `yes` | 証明書の検証をスキップします。テスト環境では便利ですが、本番環境では証明書をインストールすることをお勧めします |

### Windows 認証

SQL ログインの代わりに *digna* サービスを実行するアカウントとして接続するには、`UID` と `PWD` を削除し、次を追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `Trusted_Connection` | `yes` | *digna* のサービスアカウントにデータベースの権限が必要です |

---

## 3. *digna* の設定 {: #3-digna-configuration }

**Add DB Connection** 画面で、次の内容を入力します。

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. MS SQL Server に関する注意事項 {: #4-notes-on-ms-sql-server }

- **1 つの接続から見えるのは 1 つのデータベースです。** SQL Server は現在のデータベースのみをカタログとして報告するため、
  *digna* は `DATABASE` で指定したデータベースのスキーマを提示します。別のデータベースにあるソーステーブルには、専用の
  接続が必要です。
- **プロファイリングモード。** *Permanent* は **Work Schema** にワークテーブルを作成するため、ユーザーにはそこでの
  `CREATE TABLE` 権限が必要です。*Session* は `tempdb` 内のローカル一時テーブル（`#wt_…`）を使用し、**Work Schema** には
  触れません。*Standard* に必要なのは読み取りアクセスのみです。
- **`SERVER` にはインスタンスとポートを含めます。** 名前付きインスタンスで `host\instance` を使う場合は、SQL Server
  Browser サービスに到達できる必要があります。`host,port` を使えばそれを回避できます。

---

## 5. ドライバーの動作確認（任意） {: #5-verifying-the-driver-optional }

DSN レス接続では ODBC データソースの設定は必要ありませんが、ドライバー自体のウィザードを使うと、*digna* に入力する前に、
ドライバーが動作し、サーバーが認証情報を受け付けることを手軽に確認できます。

#### ステップ 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

**Next >** ボタンをクリックします。

#### ステップ 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

認証方式（例: ユーザー名とパスワード）を選択し、
必要な情報を入力します。

**Next >** ボタンをクリックします。

#### ステップ 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

ANSI 準拠の設定を選択し、**Next >** ボタンをクリックします。

#### ステップ 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

既定の設定のままにするか、必要に応じてログのオプションを選択し、
**Finish** ボタンをクリックします。

#### ステップ 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

次に **Test datasource** ボタンをクリックします。

#### ステップ 6
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

成功画面が表示されれば、ドライバーと認証情報が動作していることが確認できます。ここで入力した値は、
[セクション 2](#2-odbc-properties) のプロパティに指定する値そのものです。
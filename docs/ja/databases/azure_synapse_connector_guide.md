---
title: Azure Synapse コネクター – データベース統合 | digna ドキュメント
description: DSN レスの接続文字列を使い、ODBC 経由で Azure Synapse Analytics に接続するよう digna を設定します。サーバーレス SQL プールと専用 SQL プールに対応し、必要な ODBC プロパティと digna 側の接続設定を説明します。
image: /assets/logo_square.png
---


# Azure Synapse Analytics 用ソースコネクター

このガイドでは、**DSN レス** の接続文字列を使用して、**ODBC** 経由で Azure Synapse Analytics に接続するよう *digna* を
設定する方法を説明します。サーバーレス SQL プールと専用 SQL プールの両方に対応しています。

セットアップの *digna* 側（接続を作成する場所、プロパティ値の暗号化方法、接続のテスト方法、プロファイリングモードの意味）は
すべてのテクノロジーで共通であり、[データベース接続の概要](overview.md) で説明しています。このページでは Azure Synapse
固有の内容を扱います。

!!! note "Technology"

    Synapse は SQL Server の方言を使用するため、接続は **Technology: SQL Server** で作成します。
    オンプレミスのサーバーについては [MS SQL Server](sqlserver_connector_guide.md) を参照してください。

---

## 1. ODBC ドライバーをインストールする {: #1-install-the-odbc-driver }

[Microsoft のインストールガイド](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server) に従って、
*digna* バックエンドを実行するマシンに **ODBC Driver 18 for SQL Server** をインストールし、
[digna ホストに ODBC ドライバーをインストールする](overview.md#install-the-driver) の説明に従って、ホスト上で登録されている
正確なドライバー名を確認します。

---

## 2. ODBC プロパティ {: #2-odbc-properties }

!!! important "これは例であり、仕様ではありません"

    以下のセットは、動作が確認されている組み合わせの 1 つです。プロパティは Microsoft の ODBC ドライバーに属するため、
    その名前、既定値、受け付ける値はドライバーのバージョンやプラットフォームによって異なり、ワークスペースが何を要求するかは
    その構成（プールの種類、認証方式、ファイアウォール）に依存します。これを出発点として使用し、インストールした
    ドライバーバージョンのドキュメントを確認してください。

**Add DB Connection** 画面で次のプロパティを追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | *digna* ホストに登録されているドライバー名と一致している必要があります |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | ワークスペース名とエンドポイントのサフィックス — 下記を参照 |
| `DATABASE` | `dignadata` | ソーススキーマを保持するデータベース。この接続でプロファイリングできる唯一のデータベースです |
| `UID` | `sqladminuser` | SQL ログイン |
| `PWD` | `<password>` | **Encrypted** をオンにします |

生成される接続文字列は次のようになります。

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### `SERVER` の値

Synapse ワークスペースの名前に、エンドポイントのサフィックスを付加します。

| プール | `SERVER` |
|---|---|
| **サーバーレス SQL プール** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **専用 SQL プール** | `<workspace>.sql.azuresynapse.net` |

!!! warning "`-ondemand` の部分は見落としやすい点です"

    これがないと、名前は専用エンドポイントに解決され、接続が失敗するか、意図したものとは別のプールに気付かないうちに
    接続されます。両方のエンドポイントは、Azure portal のワークスペースの概要ページに表示されています。

### ファイアウォール

Synapse ワークスペースのファイアウォールで、*digna* ホストの送信元アドレスを許可する必要があります。接続をテストする前に、
ワークスペースの **Networking** でアドレスを追加してください。ブロックされたアドレスは、認証エラーではなく接続タイムアウトと
して現れます。

### Microsoft Entra ID 認証

SQL ログインの代わりに、ドライバーは Entra ID に対して認証することもできます。`UID`/`PWD` を、ワークスペースが想定する
認証方式に置き換えます。例:

| キー | 値の例 | 備考 |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | この場合 `UID` にはアプリケーション (クライアント) ID、`PWD` にはクライアントシークレットを指定します |
| `Authentication` | `ActiveDirectoryMSI` | *digna* ホストのマネージド ID。認証情報は不要です |

---

## 3. *digna* の設定 {: #3-digna-configuration }

**Add DB Connection** 画面で、次の内容を入力します。

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Azure Synapse に関する注意事項 {: #4-notes-on-azure-synapse }

- **サーバーレスプールは *Standard* プロファイリングのみをサポートします。** サーバーレス SQL プールはデータベースに
  テーブルを作成できないため、*Permanent* と *Session* のどちらのプロファイリングも実行できません。*Standard* はソース上で
  直接メトリクスを計算します。サーバーレスは処理したデータ量に応じて課金されるため、これはより安価な選択肢でもあります。
- **1 つの接続から見えるのは 1 つのデータベースです。** Synapse は SQL Server と同様に、現在のデータベースのみを
  カタログとして報告するため、*digna* は `DATABASE` で指定したデータベースのスキーマを提示します。
- Driver 18 では **暗号化が既定で有効** になっており、Synapse のエンドポイントは有効な公開証明書を提示するため、
  `Encrypt` や `TrustServerCertificate` プロパティは不要です。
- **サーバーレスエンドポイントは、最初の接続時にアイドル状態から再開する場合があります。** しばらく使用されていなかった
  プールで接続テストがタイムアウトした場合は、再試行してください。

---

## 5. ドライバーの動作確認（任意） {: #5-verifying-the-driver-optional }

DSN レス接続では ODBC データソースの設定は必要ありませんが、ドライバー自体のウィザードを使うと、*digna* に入力する前に、
ドライバーが動作し、ワークスペースが認証情報を受け付けることを手軽に確認できます。

#### ステップ 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

「Server」フィールドに入力します。
Synapse ワークスペースの名前を使用し、「.sql.azuresynapse.net」を付け加えます。  
**注意**: サーバーレス SQL プールを使用して接続する場合は、上のスクリーンショットのように必ず
「-ondemand」を含めてください。

**Next >** ボタンをクリックします。

#### ステップ 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

認証方式（例: ユーザー名とパスワード）を選択し、
必要な情報を入力します。

**Next >** ボタンをクリックします。

#### ステップ 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

ANSI 準拠の設定を選択し、**Next >** ボタンをクリックします。

#### ステップ 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

既定の設定のままにするか、必要に応じてオプションを選択し、
**Finish** ボタンをクリックします。

#### ステップ 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

次に **Test datasource** ボタンをクリックします。

#### ステップ 6
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

成功画面が表示されれば、ドライバー、エンドポイント、認証情報が動作していることが確認できます。ここで入力した値は、
[セクション 2](#2-odbc-properties) のプロパティに指定する値そのものです。

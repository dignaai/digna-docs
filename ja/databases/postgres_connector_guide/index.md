# PostgreSQL 用ソースコネクター

このガイドでは、**DSN レス** の接続文字列を使用して、**ODBC** 経由で PostgreSQL に接続するよう *digna* を設定する方法を
説明します。

セットアップの *digna* 側（接続を作成する場所、プロパティ値の暗号化方法、接続のテスト方法、プロファイリングモードの意味）は
すべてのテクノロジーで共通であり、[データベース接続の概要](overview.md) で説明しています。このページでは PostgreSQL
固有の内容を扱います。

---

## 1. ODBC ドライバーをインストールする {: #1-install-the-odbc-driver }

ベンダーの公式インストールガイドに従って、*digna* バックエンドを実行するマシンに PostgreSQL ODBC ドライバー
(**psqlODBC**) をインストールします。

ドライバーが登録される名前はプラットフォームやパッケージによって異なり、一般的には Windows では
**PostgreSQL Unicode(x64)**、Linux では **PostgreSQL ODBC Driver(UNICODE)** です。
[digna ホストに ODBC ドライバーをインストールする](overview.md#install-the-driver) の説明に従ってホスト上で正確な名前を
確認し、その名前を以下の `DRIVER` プロパティに使用してください。

---

## 2. ODBC プロパティ {: #2-odbc-properties }

!!! important "これは例であり、仕様ではありません"

    以下のセットは、動作が確認されている組み合わせの 1 つです。プロパティは psqlODBC ドライバーに属するため、
    その名前、既定値、受け付ける値はドライバーのバージョンやプラットフォームによって異なり、サーバーが要求する内容
    （特に SSL）も異なる場合があります。これを出発点として使用し、インストールしたドライバーバージョンのドキュメントを
    確認してください。

**Add DB Connection** 画面で次のプロパティを追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | *digna* ホストに登録されているドライバー名と一致している必要があります |
| `SERVER` | `db.example.com` | サーバー名または IP アドレス |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | ソーススキーマを保持するデータベース。この接続でプロファイリングできる唯一のデータベースです |
| `UID` | `digna_source_user` | データベースユーザー |
| `PWD` | `<password>` | **Encrypted** をオンにします |
| `SSLMode` | `prefer` | `disable`、`allow`、`prefer`、`require`、`verify-ca`、`verify-full` のいずれか — サーバーが受け付けるものである必要があります |

生成される接続文字列は次のようになります。

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

その他の psqlODBC オプションも、追加のプロパティとして指定できます。例えば、読み取り専用セッションにする `ReadOnly=1`、
接続時に `SET` ステートメントを実行する `ConnSettings` などです。

---

## 3. *digna* の設定 {: #3-digna-configuration }

**Add DB Connection** 画面で、次の内容を入力します。

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. PostgreSQL に関する注意事項 {: #4-notes-on-postgresql }

- **`SSLMode` はサーバーと一致している必要があります。** `hostssl` で構成されたサーバーは `SSLMode=disable` を拒否し、
  `verify-ca` または `verify-full` では、さらに *digna* ホスト上のドライバーからルート証明書を利用できる必要があります。
  ドライバーのテスト時に特定のモードを選択する必要があった場合は、ここでも同じモードを使用してください。
- **1 つの接続から見えるのは 1 つのデータベースです。** PostgreSQL は現在のデータベースのみをカタログとして報告するため、
  *digna* は `DATABASE` で指定したデータベースのスキーマを提示します。別のデータベースにあるソーステーブルには、専用の
  接続が必要です。
- **プロファイリングモード。** *Permanent* は **Work Schema** にワークテーブルを作成するため、ユーザーにはそのスキーマに
  対する `CREATE` 権限が必要です。*Session* は `CREATE TEMPORARY TABLE` を使用し、**Work Schema** には触れません。
  *Standard* に必要なのは読み取りアクセスのみです。

---

## 5. ドライバーの動作確認（任意） {: #5-verifying-the-driver-optional }

DSN レス接続では ODBC データソースの設定は必要ありませんが、ドライバー自体のダイアログを使うと、*digna* に入力する前に、
ドライバーが動作し、サーバーが認証情報と SSL モードを受け付けることを手軽に確認できます。

#### ステップ 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### ステップ 2 – 接続をテストする

**Test Connection** ボタンをクリックします。

![Step 2](images/postgres/create_odbc_data_source_step2.png)

ここで入力した値は、[セクション 2](#2-odbc-properties) のプロパティに指定する値そのものです。
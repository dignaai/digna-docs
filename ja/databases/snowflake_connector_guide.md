# Snowflake 用ソースコネクター

このガイドでは、**DSN レス** の接続文字列を使用して、**ODBC** 経由で Snowflake に接続するよう *digna* を設定する方法を
説明します。

セットアップの *digna* 側（接続を作成する場所、プロパティ値の暗号化方法、接続のテスト方法、プロファイリングモードの意味）は
すべてのテクノロジーで共通であり、[データベース接続の概要](overview.md) で説明しています。このページでは Snowflake
固有の内容を扱います。

---

## 1. ODBC ドライバーをインストールする {: #1-install-the-odbc-driver }

[Snowflake のインストールガイド](https://docs.snowflake.com/en/developer-guide/odbc/odbc) に従って、*digna* バックエンドを
実行するマシンに **Snowflake ODBC Driver** をインストールします。

ドライバーは **SnowflakeDSIIDriver** として登録されます。
[digna ホストに ODBC ドライバーをインストールする](overview.md#install-the-driver) の説明に従って、ホスト上で登録されている
正確な名前を確認してください。

---

## 2. ODBC プロパティ {: #2-odbc-properties }

Snowflake には **プログラムによるアクセストークン (PAT)** を使って接続します。これは *digna* が検証済みの認証方式であり、
パスワードのみのサインインがブロックされているアカウントで Snowflake が要求する方式でもあります。

!!! important "これは例であり、仕様ではありません"

    以下のセットは、動作が確認されている組み合わせの 1 つです。プロパティは Snowflake ODBC ドライバーに属するため、
    その名前、既定値、受け付ける値はドライバーのバージョンやプラットフォームによって異なり、アカウントでどの認証
    オプションが許可されるかはアカウントのセキュリティポリシーによって決まります。これを出発点として使用し、
    インストールしたドライバーバージョンのドキュメントを確認してください。

| キー | 値の例 | 備考 |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | *digna* ホストに登録されているドライバー名と一致している必要があります |
| `Server` | `<account>.snowflakecomputing.com` | アカウント識別子とサフィックス。例: `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | トークンが属する Snowflake ユーザー |
| `Database` | `TEST` | ソーススキーマを保持するデータベース。この接続でプロファイリングできる唯一のデータベースです |
| `Schema` | `PUBLIC` | セッションの既定スキーマ |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | トークン認証を選択します |
| `token` | `<programmatic access token>` | **Encrypted** をオンにします |

生成される接続文字列は次のようになります。

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### ウェアハウスとロール

クエリにはウェアハウスが必要です。*digna* ユーザーに既定のウェアハウスと既定のロールがある場合、セッションはそれらを
使用するため、何も設定する必要はありません。それ以外の場合は、次を追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | プロファイリングクエリを実行するウェアハウス |
| `Role` | `DIGNA_READER` | セッションが権限を使用するロール |

!!! tip "digna 専用のウェアハウスを用意してください"

    小規模で自動サスペンドする専用のウェアハウスを用意すると、プロファイリングのコストを把握しやすくなり、*digna* が
    対話的なユーザーとコンピュートリソースを奪い合うことを防げます。

### パスワード認証

アカウントでまだ許可されている場合は、トークンの代わりにパスワードを使用できます。`authenticator` と `token` を削除し、
次を追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `PWD` | `<password>` | **Encrypted** をオンにします |

---

## 3. *digna* の設定 {: #3-digna-configuration }

**Add DB Connection** 画面で、次の内容を入力します。

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Snowflake に関する注意事項 {: #4-notes-on-snowflake }

- **トークンには有効期限があります。** プログラムによるアクセストークンは有効期間付きで発行され、期限が切れた日に
  プロファイリングは停止します。作成時に有効期限を控えておき、新しいトークンを `token` プロパティに入力し直して
  ください。暗号化された値は置き換えることはできますが、読み戻すことはできません。
- **1 つの接続から見えるのは 1 つのデータベースです。** Snowflake は現在のデータベースのみをカタログとして報告するため、
  *digna* は `Database` で指定したデータベースのスキーマを提示します。別のデータベースにあるソーステーブルには、専用の
  接続が必要です。
- **識別子は大文字です**（引用符付きで作成された場合を除く）。*digna* は Snowflake が報告するとおりの名前を使用します。
- **プロファイリングモード。** *Permanent* は **Work Schema** にワークテーブルを作成するため、ロールにはそこでの
  `CREATE TABLE` 権限が必要です。*Session* は `CREATE TEMPORARY TABLE` を使用し、**Work Schema** には触れません。
  *Standard* に必要なのは読み取りアクセスのみで、書き込み権限は一切不要です。

---

## 5. ドライバーの動作確認（任意） {: #5-verifying-the-driver-optional }

DSN レス接続では ODBC データソースの設定は必要ありませんが、ドライバー自体のダイアログを使うと、*digna* に入力する前に、
ドライバー、アカウント URL、認証情報が動作することを手軽に確認できます。

#### ステップ 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

注意事項:

- **Server** の値は、Snowflake のアカウント識別子の後に `.snowflakecomputing.com` を続けたものです。
- ここで入力する **Database**、**Schema**、**Warehouse** は、[セクション 2](#2-odbc-properties) の `Database`、
  `Schema`、`Warehouse` プロパティに対応します。

#### ステップ 2 – 接続をテストする

**TEST** ボタンをクリックします。接続に成功すると、次のように表示されます。

![Step 2](images/snowflake/create_odbc_data_source_step2.png)
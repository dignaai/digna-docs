---
title: Databricks コネクター – データベース統合 | digna ドキュメント
description: DSN レスの接続文字列を使い、ODBC 経由で Unity Catalog 対応の Databricks に接続するよう digna を設定します。Databricks ODBC ドライバー、個人用アクセストークン、HTTP パス、および digna 側の接続設定を説明します。
image: /assets/logo_square.png
---

# Databricks 用ソースコネクター

このガイドでは、**DSN レス** の接続文字列を使用して、**ODBC** 経由で Databricks に接続するよう *digna* を設定する方法を
説明します。

セットアップの *digna* 側（接続を作成する場所、プロパティ値の暗号化方法、接続のテスト方法、プロファイリングモードの意味）は
すべてのテクノロジーで共通であり、[データベース接続の概要](overview.md) で説明しています。このページでは Databricks
固有の内容を扱います。

!!! note "Unity Catalog が必要です"

    *digna* は利用可能なカタログを `system.information_schema.catalogs` から読み取るため、ワークスペースで
    Unity Catalog が有効になっている必要があります。以前の *digna* リリースでは、Unity Catalog のないワークスペース向けに
    別のテクノロジー「Databricks Legacy」が用意されていましたが、現在は利用できません。

---

## 1. ODBC ドライバーをインストールする {: #1-install-the-odbc-driver }

[Databricks のインストールガイド](https://docs.databricks.com/aws/en/integrations/odbc/) に従って、*digna* バックエンドを
実行するマシンに **Databricks ODBC Driver** をインストールします。

バージョンによって、ドライバーは **Simba Spark ODBC Driver** または **Databricks ODBC Driver** として登録されます。
[digna ホストに ODBC ドライバーをインストールする](overview.md#install-the-driver) の説明に従って、ホスト上で登録されている
正確な名前を確認してください。

---

## 2. 接続情報を収集する {: #2-gather-the-connection-details }

すべての値は、*digna* に使用させたい SQL ウェアハウス（またはクラスター）から取得します。Databricks ワークスペースで
それを開き、**Connection details** に移動します。

| Databricks のフィールド | 用途 |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`、通常は `443` |
| **HTTP path** | `HTTPPath` |

認証には **個人用アクセストークン** を作成します。
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat) を参照してください。
トークンはユーザーまたはサービスプリンシパルに属し、そのプリンシパルにはソースデータに対する `USE CATALOG`、
`USE SCHEMA`、`SELECT` 権限が必要です。

---

## 3. ODBC プロパティ {: #3-odbc-properties }

!!! important "これは例であり、仕様ではありません"

    以下のセットは、動作が確認されている組み合わせの 1 つです。プロパティは Databricks/Simba ドライバーに属するため、
    その名前、既定値、受け付ける値はドライバーのバージョン（ドライバーは何度か名称変更され、認証オプションも拡張されて
    きました）やプラットフォームによって異なります。これを出発点として使用し、インストールしたドライバーバージョンの
    ドキュメントを確認してください。

**Add DB Connection** 画面で次のプロパティを追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | *digna* ホストに登録されているドライバー名と一致している必要があります |
| `Host` | `<workspace>.cloud.databricks.com` | ウェアハウスのサーバーホスト名。例: `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | ウェアハウスまたはクラスターの HTTP パス |
| `SSL` | `1` | Databricks のエンドポイントは TLS 専用です |
| `ThriftTransport` | `2` | HTTP トランスポート。SQL エンドポイントが使用する方式です |
| `AuthMech` | `3` | トークン認証 |
| `UID` | `token` | ユーザー名ではなく、文字どおりの単語 `token` |
| `PWD` | `dapi…` | 個人用アクセストークン。**Encrypted** をオンにします |
| `UseNativeQuery` | `1` | *digna* の SQL を変更せずにそのまま渡します — 下記を参照 |

生成される接続文字列は次のようになります。

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "`UseNativeQuery=1` を維持してください"

    ドライバーの既定値である `UseNativeQuery=0` では、ドライバーは受け取った SQL を、移植性のある ODBC 構文と
    みなす形に書き換えます。*digna* はすでに Databricks SQL を生成しているため、この書き換えによってバッククォートの
    引用符や日付リテラルが変わる可能性があり、記述どおりであれば有効なステートメントでプロファイリングが失敗します。

### トークンの代わりに OAuth を使用する

OAuth のマシン間 (M2M) 認証を使用するサービスプリンシパルの場合は、`AuthMech`、`UID`、`PWD` を次のものに置き換えます。

| キー | 値の例 | 備考 |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | クライアント資格情報 |
| `Auth_Client_ID` | `<application id>` | サービスプリンシパル |
| `Auth_Client_Secret` | `<client secret>` | **Encrypted** をオンにします |

---

## 4. *digna* の設定 {: #4-digna-configuration }

**Add DB Connection** 画面で、次の内容を入力します。

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Databricks に関する注意事項 {: #5-notes-on-databricks }

- *digna* が接続するとき、**ウェアハウスが実行中であるか、起動可能である必要があります。** 停止状態から再開する
  ウェアハウスは、接続タイムアウトより長くかかることがあります。アイドル期間の後の最初の試行でテストが失敗した場合は、
  再試行してください。
- **カタログはワークスペースから取得されます。** ほとんどのテクノロジーとは異なり、1 つの Databricks 接続から
  プリンシパルが参照を許可されているすべてのカタログに到達できるため、1 つの接続で複数のカタログにまたがるソースを
  扱えます。
- **プロファイリングモード。** *Permanent* はソースのカタログ内の **Work Schema** にワークテーブルを作成するため、
  プリンシパルにはそこでの `CREATE TABLE` 権限が必要です。*Session* は `CREATE TEMPORARY TABLE` を使用し、
  **Work Schema** には触れません。*Standard* に必要なのは読み取りアクセスのみです。
- **サーバーレスウェアハウスも** 同じように動作します。異なるのは `HTTPPath` だけです。

---

## 6. ドライバーの動作確認（任意） {: #6-verifying-the-driver-optional }

DSN レス接続では ODBC データソースの設定は必要ありませんが、ドライバー自体のダイアログを使うと、*digna* に入力する前に、
ドライバー、ウェアハウス、トークンが動作することを手軽に確認できます。

#### ステップ 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### ステップ 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### ステップ 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### ステップ 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### ステップ 5 – 接続をテストする

**TEST** ボタンをクリックします。接続に成功すると、次のように表示されます。

![Step 5](images/databricks/create_odbc_data_source_step5.png)

ここで入力したホスト、HTTP パス、トークンは、[セクション 3](#3-odbc-properties) のプロパティに指定する値そのものです。

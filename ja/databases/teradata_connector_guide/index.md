# Teradata 用ソースコネクター

このガイドでは、**DSN レス** の接続文字列を使用して、**ODBC** 経由で Teradata に接続するよう *digna* を設定する方法を
説明します。

セットアップの *digna* 側（接続を作成する場所、プロパティ値の暗号化方法、接続のテスト方法、プロファイリングモードの意味）は
すべてのテクノロジーで共通であり、[データベース接続の概要](overview.md) で説明しています。このページでは Teradata 固有の
内容を扱います。

---

## 1. ODBC ドライバーをインストールする {: #1-install-the-odbc-driver }

ベンダーの公式インストールガイドに従って、*digna* バックエンドを実行するマシンに **ODBC Driver for Teradata** を
インストールします。

ドライバーは名前にバージョンを含めて登録されます。例: **Teradata Database ODBC Driver 20.00**。
[digna ホストに ODBC ドライバーをインストールする](overview.md#install-the-driver) の説明に従って、ホスト上で登録されている
正確な名前を確認してください。

---

## 2. ODBC プロパティ {: #2-odbc-properties }

!!! important "これは例であり、仕様ではありません"

    以下のセットは、動作が確認されている組み合わせの 1 つです。プロパティは Teradata ODBC ドライバーに属するため、
    その名前、既定値、受け付ける値はドライバーのバージョン（バージョンはドライバー名自体の一部です）やプラットフォームに
    よって異なります。これを出発点として使用し、インストールしたドライバーバージョンのドキュメントを確認してください。

**Add DB Connection** 画面で次のプロパティを追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | *digna* ホストに登録されているドライバー名と一致している必要があります |
| `DBCNAME` | `teradata.example.com` | サーバー名または IP アドレス。ホストプロパティに対する Teradata 独自の名称です |
| `UID` | `digna_source_user` | データベースユーザー |
| `PWD` | `<password>` | **Encrypted** をオンにします |

生成される接続文字列は次のようになります。

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

便利な追加プロパティ:

| キー | 値の例 | 備考 |
|---|---|---|
| `MechanismName` | `TD2` | ログオンメカニズム。`TD2` が Teradata の既定値です。ディレクトリ認証には `LDAP` を使用します |
| `DefaultDatabase` | `dad` | セッションが開始されるデータベース |
| `CharacterSet` | `UTF8` | 既定のセッション文字セットでは ASCII 以外のデータが文字化けする場合に設定します |

---

## 3. *digna* の設定 {: #3-digna-configuration }

**Add DB Connection** 画面で、次の内容を入力します。

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Teradata に関する注意事項 {: #4-notes-on-teradata }

- **Teradata のデータベースはスキーマではなくカタログです。** *digna* はユーザーが参照できるデータベース
  （`DBC.DatabasesV` から）をカタログとして一覧表示し、スキーマのレベルは適用されません。データソースを追加するときは、
  データベースをカタログとして選択します。スキーマは *not applicable* として表示されます。
- **1 つの接続から、許可されているすべてのデータベースに到達できます。** そのため、接続が 1 つのデータベースに固定される
  テクノロジーとは異なり、1 つの接続で複数のデータベースにまたがるソースを扱えます。
- **Work Schema はデータベースです。** *Permanent* プロファイリングでは、ワークテーブルを保持する Teradata データベースを
  指定し、ユーザーにそのデータベースでの `CREATE TABLE` 権限と `PERM` スペースの割り当てを付与してください。PERM
  スペースがゼロのデータベースにはテーブルを格納できません。
- **プロファイリングモード。** *Permanent* は **Work Schema** にテーブルを作成します。*Session* は `VOLATILE` テーブルを
  使用するため、`SPOOL` スペースが必要ですが、PERM スペースや **Work Schema** での権限は不要です。*Standard* に必要なのは
  読み取りアクセスのみです。

---

## 5. ドライバーの動作確認（任意） {: #5-verifying-the-driver-optional }

DSN レス接続では ODBC データソースの設定は必要ありませんが、ドライバー自体のダイアログを使うと、*digna* に入力する前に、
ドライバーと認証情報が動作することを手軽に確認できます。

#### ステップ 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

ここでの **Name or IP address** フィールドは、[セクション 2](#2-odbc-properties) の `DBCNAME` プロパティです。

**Test** ボタンをクリックします。

#### ステップ 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

ユーザー名とパスワードを入力し、**OK** ボタンをクリックします。成功画面が表示されれば、ドライバーと認証情報が
動作していることが確認できます。
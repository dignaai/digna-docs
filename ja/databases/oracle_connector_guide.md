# Oracle 用ソースコネクター

このガイドでは、**DSN レス** の接続文字列を使用して、**ODBC** 経由で Oracle Database に接続するよう *digna* を設定する
方法を説明します。

セットアップの *digna* 側（接続を作成する場所、プロパティ値の暗号化方法、接続のテスト方法、プロファイリングモードの意味）は
すべてのテクノロジーで共通であり、[データベース接続の概要](overview.md) で説明しています。このページでは Oracle 固有の
内容を扱います。

---

## 1. ODBC ドライバーをインストールする {: #1-install-the-odbc-driver }

Oracle ODBC ドライバーは **Oracle Client** の一部です（Instant Client の「ODBC」パッケージで十分です）。ベンダーの公式
インストールガイドに従って、*digna* バックエンドを実行するマシンにインストールします。

ドライバーは **Oracle in `<OracleHomeName>`** という名前で登録されます。例: `Oracle in OraDB21Home1` や
`Oracle in instantclient_21_13`。ホーム名はインストールごとに異なるため、
[digna ホストに ODBC ドライバーをインストールする](overview.md#install-the-driver) の説明に従って、ホスト上で正確な名前を
確認してください。

---

## 2. ODBC プロパティ {: #2-odbc-properties }

!!! important "これは例であり、仕様ではありません"

    以下のセットは、動作が確認されている組み合わせの 1 つです。プロパティは Oracle ODBC ドライバーに属するため、
    その名前、既定値、受け付ける値はクライアントのバージョンによって異なり、特にドライバー名はホスト上の Oracle ホームに
    依存します。これを出発点として使用し、インストールしたクライアントバージョンのドキュメントを確認してください。

**Add DB Connection** 画面で次のプロパティを追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | *digna* ホストに登録されているドライバー名と一致している必要があります |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | 接続先のデータベース — 下記を参照 |
| `UID` | `DIGNA_SOURCE_USER` | データベースユーザー |
| `PWD` | `<password>` | **Encrypted** をオンにします |

生成される接続文字列は次のようになります。

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### `DBQ` の値

`DBQ` には 3 つの形式を指定できます。*digna* にとってはいずれも同等で、違いは *digna* ホスト上で何を設定する必要が
あるかです。

| 形式 | 例 | 必要なもの |
|---|---|---|
| **完全な接続記述子** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | なし — すべてがプロパティに含まれます。推奨 |
| **TNS エイリアス** | `DIGNA_SOURCE` | エイリアスが *digna* ホスト上の Oracle Client の `tnsnames.ora` に存在している必要があります |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Easy Connect をサポートする Oracle Client（12c 以降） |

!!! tip "完全な接続記述子を推奨します"

    TNS エイリアスを使うと、接続定義の半分が *digna* ホスト上のファイルに移り、ホストを再構築したり *digna* を移行したり
    するときに忘れられがちです。完全な接続記述子を使えば接続は自己完結したものになります。これこそが DSN レス
    セットアップの目的です。

記述子内の括弧は接続文字列内でそのまま使用できますが、パスワードに `;` が含まれる場合は波括弧で囲んでください:
`PWD={p@ss;word}`。

---

## 3. *digna* の設定 {: #3-digna-configuration }

**Add DB Connection** 画面で、次の内容を入力します。

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Oracle に関する注意事項 {: #4-notes-on-oracle }

- **スキーマはユーザーです。** *digna* は Oracle のユーザーをスキーマとして一覧表示するため、ソーススキーマはテーブルの
  所有者（上記の例では `DIGNA_SOURCE_USER`）になります。接続ユーザーには、直接またはロール経由で、それらのテーブルに
  対する `SELECT` 権限が必要です。
- **1 つの接続から見えるのは 1 つのデータベースです。** *digna* が提示するカタログは接続先のデータベースであるため、
  `DBQ` によってどのサービス、つまりどのデータベースがプロファイリングされるかが決まります。
- **識別子は引用符で囲まれると大文字と小文字が区別されます。** *digna* はデータディクショナリから読み取った名前を
  引用符で囲みます。これは Oracle が格納している名前であり、引用符なしで作成されたオブジェクトの場合は大文字です。
- **プロファイリングモード。** *Permanent* は **Work Schema** にワークテーブルを作成するため、ユーザーにはそこでの
  `CREATE TABLE` 権限と表領域のクォータが必要です。*Session* はプライベート一時表（`ORA$PTT_…`、Oracle 18c 以降）を
  使用し、**Work Schema** には触れません。*Standard* に必要なのは読み取りアクセスのみです。

---

## 5. ドライバーの動作確認（任意） {: #5-verifying-the-driver-optional }

DSN レス接続では ODBC データソースの設定は必要ありませんが、ドライバー自体のダイアログを使うと、*digna* に入力する前に、
Oracle Client、サービス名、認証情報が動作することを手軽に確認できます。

#### ステップ 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

ここに表示される **TNS Service Name** は、Oracle Client インストールの `tnsnames.ora` から取得されます。エイリアス、
およびそれに伴うホスト、ポート、サービス名はそこで定義されています。*digna* では、このエイリアスを `DBQ` として使用する
ことも、代わりに完全な接続記述子を使用することもできます。

#### ステップ 2 – 接続をテストする

**Test Connection** ボタンをクリックします。

![Step 2](images/oracle/create_odbc_data_source_step2.png)

パスワードを入力し、**OK** ボタンをクリックします。

![Step 3](images/oracle/create_odbc_data_source_step3.png)

成功メッセージが表示されれば、ドライバーと認証情報が動作していることが確認できます。
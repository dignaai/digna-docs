# Netezza 用ソースコネクター

このガイドでは、**DSN レス** の接続文字列を使用して、**ODBC** 経由で Netezza に接続するよう *digna* を設定する方法を
説明します。

セットアップの *digna* 側（接続を作成する場所、プロパティ値の暗号化方法、接続のテスト方法、プロファイリングモードの意味）は
すべてのテクノロジーで共通であり、[データベース接続の概要](overview.md) で説明しています。このページでは Netezza 固有の
内容を扱います。

---

## 1. ODBC ドライバーをインストールする {: #1-install-the-odbc-driver }

ベンダーの公式インストールガイドに従って、*digna* バックエンドを実行するマシンに **NetezzaSQL** ODBC ドライバー
（IBM Netezza クライアントツールの一部）をインストールします。

[digna ホストに ODBC ドライバーをインストールする](overview.md#install-the-driver) の説明に従って、ホスト上で登録されている
正確なドライバー名を確認してください。

---

## 2. ODBC プロパティ {: #2-odbc-properties }

!!! important "これは例であり、仕様ではありません"

    以下のセットは、動作が確認されている組み合わせの 1 つです。プロパティは NetezzaSQL ドライバーに属するため、
    その名前、既定値、受け付ける値はクライアントのバージョンやプラットフォームによって異なり、TLS で保護された
    アプライアンスにはここに示すもの以上のプロパティが必要です。これを出発点として使用し、インストールした
    クライアントバージョンのドキュメントを確認してください。

**Add DB Connection** 画面で次のプロパティを追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | *digna* ホストに登録されているドライバー名と一致している必要があります。この名前は波括弧で囲んで記述するのが一般的です |
| `SERVER` | `netezza.example.com` | サーバー名または IP アドレス |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | セッションが開始されるデータベース |
| `UID` | `ADMIN` | データベースユーザー |
| `PWD` | `<password>` | **Encrypted** をオンにします |

生成される接続文字列は次のようになります。

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

ドライバーのバージョン、セットアップ、セキュリティ要件によっては、追加のプロパティが必要になる場合があります。例えば、
TLS で保護されたアプライアンスでは `SecurityLevel` と `CaCertFile` です。ドライバーの *Advanced*、*SSL*、*Driver*
ダイアログで提供されるすべてのオプションは、プロパティとして追加できます。

---

## 3. *digna* の設定 {: #3-digna-configuration }

**Add DB Connection** 画面で、次の内容を入力します。

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Netezza に関する注意事項 {: #4-notes-on-netezza }

- **カタログとスキーマの両方が適用されます。** *digna* は、ユーザーが参照できるデータベース（`_V_DATABASE` から）を
  カタログとして、その下にスキーマ（`_V_SCHEMA` から）を一覧表示するため、1 つの接続で複数のデータベースのソースを
  扱えます。`DATABASE` はセッションが開始される場所を決めるだけです。
- **識別子は大文字です**（引用符付きで作成された場合を除く）。そのため、上記の例では `TEST` と `ADMIN` を使用しています。
- **プロファイリングモード。** *Permanent* は **Work Schema** にワークテーブルを作成するため、ユーザーにはそこでの
  `CREATE TABLE` 権限が必要です。*Session* は `CREATE TEMPORARY TABLE` を使用し、**Work Schema** には触れません。
  *Standard* に必要なのは読み取りアクセスのみです。

---

## 5. ドライバーの動作確認（任意） {: #5-verifying-the-driver-optional }

DSN レス接続では ODBC データソースの設定は必要ありませんが、ドライバー自体のダイアログを使うと、*digna* に入力する前に、
ドライバーと認証情報が動作することを手軽に確認できます。

#### ステップ 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

**DSN Options** のフィールドは、[セクション 2](#2-odbc-properties) のプロパティと 1 対 1 で対応しています。Netezza
ドライバー、セットアップ、セキュリティ要件によっては、**Advanced DSN Options**、**SSL DSN Options**、または
**Driver Options** タブにも入力が必要な場合があります。最も単純なセットアップでは **DSN Options** だけで十分です。

**Test Connection** ボタンをクリックします。

#### ステップ 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

成功画面が表示されれば、ドライバーは動作しており、値は正しく設定されています。
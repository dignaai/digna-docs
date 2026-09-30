---
title: Apache Hive コネクター – データベース統合 | digna ドキュメント
description: DSN レスの接続文字列を使い、ODBC 経由で Apache Hive に接続するよう digna を設定します。Cloudera Hive ODBC ドライバー、認証メカニズム、トランスポートモード、および digna 側の接続設定を説明します。
image: /assets/logo_square.png
---


# Hive 用ソースコネクター

このガイドでは、**DSN レス** の接続文字列を使用して、**ODBC** 経由で Apache Hive に接続するよう *digna* を設定する方法を
説明します。

セットアップの *digna* 側（接続を作成する場所、プロパティ値の暗号化方法、接続のテスト方法、プロファイリングモードの意味）は
すべてのテクノロジーで共通であり、[データベース接続の概要](overview.md) で説明しています。このページでは Hive 固有の
内容を扱います。

---

## 1. ODBC ドライバーをインストールする {: #1-install-the-odbc-driver }

ベンダーの公式インストールガイドに従って、*digna* バックエンドを実行するマシンに
**Cloudera ODBC Driver for Apache Hive** をインストールします。

[digna ホストに ODBC ドライバーをインストールする](overview.md#install-the-driver) の説明に従って、ホスト上で登録されている
正確なドライバー名を確認してください。

---

## 2. ODBC プロパティ {: #2-odbc-properties }

!!! important "これは例であり、仕様ではありません"

    以下のセットは、動作が確認されている組み合わせの 1 つです。プロパティは Cloudera Hive ドライバーに属するため、
    その名前、既定値、受け付ける値はドライバーのバージョンやプラットフォームによって異なり、HiveServer2 が何を受け付けるかは
    クラスターのセキュリティ構成（認証メカニズム、トランスポートモード、TLS、ゲートウェイ）に完全に依存します。これを
    出発点として使用し、インストールしたドライバーバージョンのドキュメントを確認してください。

**Add DB Connection** 画面で次のプロパティを追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | *digna* ホストに登録されているドライバー名と一致している必要があります |
| `HOST` | `hive.example.com` | HiveServer2 のホスト名または IP アドレス |
| `PORT` | `10000` | HiveServer2 のポート。HTTP トランスポートの場合は `10001` |

生成される接続文字列は次のようになります。

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### 認証

セキュリティ保護されていない HiveServer2 は、上記の 3 つのプロパティをそのまま受け付けます。認証が有効になっている場合は、
次を追加します。

| キー | 値の例 | 備考 |
|---|---|---|
| `AuthMech` | `3` | `0` 認証なし、`2` ユーザー名のみ、`3` ユーザー名とパスワード、`1` Kerberos |
| `UID` | `digna_source_user` | `AuthMech` が `2` と `3` の場合に必須 |
| `PWD` | `<password>` | `AuthMech` が `3` の場合に必須。**Encrypted** をオンにします |

Kerberos (`AuthMech=1`) の場合、*digna* ホストには有効なチケットまたは keytab に加えて、ドライバーのドキュメントに
記載されている `KrbHostFQDN`、`KrbServiceName`、`KrbRealm` プロパティが必要です。

### トランスポートと TLS

| キー | 値の例 | 備考 |
|---|---|---|
| `ThriftTransport` | `2` | `0` バイナリ（既定、ポート 10000）、`1` SASL、`2` HTTP（ポート 10001、Knox ゲートウェイが想定する方式） |
| `HTTPPath` | `cliservice` | `ThriftTransport=2` の場合 |
| `SSL` | `1` | HiveServer2 が TLS で保護されている場合 |
| `Schema` | `dignadata` | セッションが開始される Hive データベース。任意 — *digna* はクエリを修飾して発行します |

---

## 3. *digna* の設定 {: #3-digna-configuration }

**Add DB Connection** 画面で、次の内容を入力します。

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Hive に関する注意事項 {: #4-notes-on-hive }

- **カタログはドライバーから取得されます。** Hive には独自のカタログがないため、*digna* はドライバーが報告するもの
  （通常は `HIVE` という名前の 1 つのエントリ）を使用し、その下に Hive データベースをスキーマとして一覧表示します。
- **Work Schema は Hive データベースです。** *Permanent* プロファイリングでは、ユーザーにそのデータベース内でテーブルを
  作成・削除する権限が必要であり、基盤となるストレージの場所が書き込み可能である必要があります。
- **プロファイリングモード。** *Permanent* は **Work Schema** にワークテーブルを作成します。*Session* は
  `CREATE TEMPORARY TABLE` を使用するため、一時テーブルをサポートする HiveServer2 が必要で、**Work Schema** には
  触れません。*Standard* に必要なのは読み取りアクセスのみで、*digna* に書き込みアクセスがまったくないクラスターでは
  このモードを選択します。
- **プロファイリングはスキャンではなく、一連のクエリです。** すべての統計は HiveServer2 によって計算されるため、*digna* の
  ユーザーがジョブを投入するキューには、インスペクションの時間帯に十分な容量が必要です。

---

## 5. ドライバーの動作確認（任意） {: #5-verifying-the-driver-optional }

DSN レス接続では ODBC データソースの設定は必要ありませんが、ドライバー自体のダイアログを使うと、*digna* に入力する前に、
ドライバー、トランスポートモード、認証情報が動作することを手軽に確認できます。

#### ステップ 1
![Step 1](images/hive/create_odbc_data_source_step1.png)

ここでの **Host**、**Port**、**Database**、**Mechanism**、**Thrift Transport** フィールドは、
[セクション 2](#2-odbc-properties) の `HOST`、`PORT`、`Schema`、`AuthMech`、`ThriftTransport` プロパティに対応します。

#### ステップ 2 – 接続をテストする

パスワードを入力し、**Test** ボタンをクリックします。

![Step 2](images/hive/create_odbc_data_source_step2.png)

テストが成功したら、**OK** ボタンをクリックします。

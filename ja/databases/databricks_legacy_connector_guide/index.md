# Databricks 用ソースコネクタ - Unity Catalog なし

本ガイドでは、*digna* をネイティブの Python コネクタまたは ODBC ドライバを使用して Databricks に接続するための設定方法について説明します。

このガイドは **"Create a Database Connection"** 画面を参照しています。

![データベース接続の作成](images/data_source_config_input_mask.png)

---

## ネイティブ Python ドライバー

**ライブラリ:** `databricks-sql-connector`  
**サポートされる認証:** Personal Access Token (PAT) のみ

> 他の認証方法を利用する場合は、ODBC ドライバを使用してください。

### パーソナルアクセストークン (PAT)

パーソナルアクセストークンを使用して認証する方法は、公式の Databricks ドキュメントを参照してください。  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* の設定（ネイティブドライバー）

**"Create a Database Connection"** 画面に次の情報を入力してください:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC ドライバー

ODBC ドライバは、より幅広い認証および接続オプションをサポートします。このセクションでは、**Simba Spark ODBC Driver** を使用したトークンベース認証に焦点を当てます。

### 1. ODBC ドライバのインストール

ベンダーの公式インストールガイドに従って **Simba Spark ODBC Driver** をインストールしてください。

### 2. ODBC データソースの設定

パーソナルアクセストークンを使用して新しい ODBC データソースを設定する手順は次の通りです。

#### ステップ 1
![ステップ 1](images/databricks/create_odbc_data_source_step1.png)

#### ステップ 2
![ステップ 2](images/databricks/create_odbc_data_source_step2.png)

#### ステップ 3
![ステップ 3](images/databricks/create_odbc_data_source_step3.png)

#### ステップ 4
![ステップ 4](images/databricks/create_odbc_data_source_step4.png)

#### ステップ 5 – 接続のテスト

**TEST** ボタンをクリックしてください。接続が成功すると次のように表示されます:

![ステップ 5](images/databricks/create_odbc_data_source_step5.png)

---

これで、**DSN (Data Source Name)** を使用する方法、または DSN-less 設定のいずれかで *digna* を ODBC 接続に設定できます。

---

### A. DSN ベースの設定

#### *digna* の設定

**"Create a Database Connection"** 画面に次の情報を入力してください:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` は ODBC ドライバ構成で定義した名前と一致する必要があります。

---

### B. DSN-less の設定

#### *digna* の設定

**"Create a Database Connection"** 画面に次の情報を入力してください:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
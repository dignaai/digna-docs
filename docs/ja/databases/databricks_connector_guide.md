---
title: Databricks Connector with Unity Catalog – Database Integration | digna Documentation
description: digna を Databricks の Unity Catalog に接続する方法。ネイティブ Python コネクタまたは ODBC ドライバを使用したトークン認証と柔軟な接続方法をサポートします。
image: /assets/logo_square.png
---

# Databricks 用ソースコネクタ - Unity Catalog 対応

このガイドでは、*digna* を Databricks に接続する方法を、ネイティブの Python コネクタまたは ODBC ドライバのいずれかを使って説明します。

この手順は **「Create a Database Connection」** 画面を参照しています。

![Create a database connection](images/data_source_config_input_mask.png)

---

## ネイティブ Python ドライバー

**ライブラリ:** `databricks-sql-connector`  
**サポートされる認証:** Personal Access Token (PAT) のみ

> ⚠️ 他の認証方法を使用する場合は、ODBC ドライバを使用してください。

### Personal Access Token (PAT)

Personal Access Token を使った認証方法については、公式の Databricks ドキュメントを参照してください。  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* の設定（ネイティブドライバー）

**「Create a Database Connection」** 画面に次の情報を入力してください:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC ドライバー

ODBC ドライバは、より幅広い認証および接続オプションをサポートします。本節では、**Simba Spark ODBC Driver** を用いたトークンベースの認証に焦点を当てます。

### 1. ODBC ドライバーのインストール

ベンダーの公式インストールガイドに従って、**Simba Spark ODBC Driver** をインストールしてください。

### 2. ODBC データソースの設定

Personal Access Token を使って新しい ODBC データソースを設定する手順は次の通りです。

#### ステップ 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### ステップ 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### ステップ 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### ステップ 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### ステップ 5 – 接続のテスト

**TEST** ボタンをクリックします。接続が成功すると次のように表示されます:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

これで、**DSN（Data Source Name）** を使う方法、または **DSN-less** 設定のいずれかで *digna* に ODBC 接続を使わせることができます。

---

### A. DSN ベースの設定

#### *digna* の設定

**「Create a Database Connection」** 画面に次を入力してください:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 `DSN` は ODBC ドライバ設定で定義した名前と一致する必要があります。

---

### B. DSN-less 設定

#### *digna* の設定

**「Create a Database Connection」** 画面に次を入力してください:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
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
---
title: Snowflake コネクタ – データベース統合 | digna ドキュメント
description: Python コネクタまたは Snowflake ODBC ドライバーを使用して digna を Snowflake に接続する方法を設定します。DSN または DSN-less 構成でのパスワード認証に対応しています。
image: /assets/logo_square.png
---


# Snowflake 用ソースコネクタ

このガイドでは、ネイティブの Python コネクタまたは ODBC ドライバーのいずれかを使用して *digna* を Snowflake に接続する方法を説明します。

これは画面 **"Create a Database Connection"** を参照しています。

![Create a database connection](images/data_source_config_input_mask.png)

---

## ネイティブ Python ドライバー

**ライブラリ:** `snowflake-connector-python`  
**サポートされる認証:** パスワード認証のみ

> 他の認証方法を利用する場合は、ODBC ドライバーを使用してください。

### *digna* の設定（ネイティブドライバー）

**"Create a Database Connection"** 画面で以下の情報を入力してください。

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
User Name:       User name and warehouse in the format "user<@>warehouse"
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC ドライバー

ODBC ドライバーは、より広範な認証および接続オプションをサポートする場合があります。このセクションでは、**SnowflakeDSIIDriver** を使用したパスワード認証に焦点を当てます。

### 1. ODBC ドライバーをインストールする

ベンダーの公式インストールガイドに従って **SnowflakeDSIIDriver** をインストールしてください。

### 2. ODBC データソースの構成

パスワード認証を使用して新しい ODBC データソースを構成する手順は次のとおりです。

#### ステップ 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

注意:
- Database、Schema、Warehouse に値を指定しない場合は、*digna* のデータソース構成時に ODBC プロパティとしてそれらを指定する必要があります。
- "Server" の値は、あなたの Snowflake アカウント名に ".snowflakecomputing.com" を付加したものになります。

#### ステップ 2 – 接続のテスト

**TEST** ボタンをクリックします。接続が成功すると次のように表示されます。

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

これで、**DSN (Data Source Name)** または **DSN-less** 構成のいずれかで ODBC 接続を使用するように *digna* を設定できます。

---

### A. DSN ベースの構成

#### *digna* の設定

**"Create a Database Connection"** 画面で、以下を入力してください。

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> `DSN` は ODBC ドライバー構成で定義した名前と一致する必要があります。

---

### B. DSN-less 構成

#### *digna* の設定

**"Create a Database Connection"** 画面で、以下を入力してください。

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```
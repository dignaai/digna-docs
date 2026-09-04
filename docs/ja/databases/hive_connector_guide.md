---
title: Apache Hive Connector – Database Integration | digna Documentation
description: Configure digna to connect to Apache Hive using the native PyHive driver or the Cloudera ODBC driver. Supports password-based authentication and DSN or DSN-less setups.
image: /assets/logo_square.png
---


# Source Connector for Hive

このガイドでは、ネイティブなPythonコネクタまたはODBCドライバのいずれかを使用して *digna* をHiveに接続する方法を説明します。

画面 **"Create a Database Connection"** を参照しています。

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `PyHive`  
**Supported Authentication:** パスワード認証のみ

> 他の認証方式を使用する場合は、ODBCドライバを使用してください。

### *digna* の設定（ネイティブドライバ）

**"Create a Database Connection"** 画面で以下の情報を入力してください:

```
Technology:      Apache Hive
Host Address:    サーバ名またはIPアドレス
Host Port:       ポート番号（例: 10000）
Database Name:   ソースデータが含まれるスキーマ
Schema Name:     ソースデータが含まれるスキーマ
User Name:       データベースのユーザー名
User Password:   ユーザーのパスワード
Use ODBC:        Disabled（デフォルト）
```

---

## ODBC Driver

ODBCドライバは、より幅広い認証および接続オプションをサポートする場合があります。本節は、ドライバ **Cloudera ODBC Driver for Apache Hive** を使用したパスワード認証に焦点を当てています。

### 1. ODBCドライバのインストール

ベンダーの公式インストールガイドに従い、**Cloudera ODBC Driver for Apache Hive**（または同等のドライバ）をインストールしてください。

### 2. ODBCデータソースの構成

パスワード認証を使用して新しいODBCデータソースを構成する手順は次のとおりです。

#### Step 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Step 2 – 接続のテスト

パスワードを入力し、**Test** ボタンをクリックします。

![Step 2](images/hive/create_odbc_data_source_step2.png)

テストが成功したら、**OK** ボタンをクリックします。

---

これで、**DSN（Data Source Name）** または **DSN-less** の設定で *digna* をODBC接続に使用するように構成できます。

---

### A. DSNベースの構成

#### *digna* の設定

**"Create a Database Connection"** 画面で以下を入力してください:

```
Technology:      Apache Hive
Database Name:   ソースデータが含まれるスキーマ（Schema Nameと同じ）
Schema Name:     ソースデータが含まれるスキーマ
Use ODBC:        Enabled
```

#### ODBCプロパティ

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN` はODBCドライバ設定で定義した名前と一致する必要があります。

---

### B. DSN-less 構成

#### *digna* の設定

**"Create a Database Connection"** 画面で以下を入力してください:

```
Technology:      Apache Hive
Database Name:   ソースデータが含まれるスキーマ（Schema Nameと同じ）
Schema Name:     ソースデータが含まれるスキーマ
Use ODBC:        Enabled
```

#### ODBCプロパティ

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 10000"
name: "Schema",     value: "Schema that contains the source data"
name: "UID",        value: "your hive user"
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```
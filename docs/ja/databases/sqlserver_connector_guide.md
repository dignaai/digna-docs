---
title: MS SQL Server コネクタ – Database Integration | digna ドキュメント
description: pymssql Python ドライバーまたは SQL Server ODBC ドライバーを使用して Microsoft SQL Server に接続するよう digna を構成する方法。DSN ベースおよび DSN-less のパスワード認証をサポートします。
image: /assets/logo_square.png
---


# Source Connector for MS SQL Server

このガイドでは、ネイティブの Python コネクタまたは ODBC ドライバーのいずれかを使用して *digna* を SQL Server に接続する方法について説明します。

画面 **"Create a Database Connection"** を参照しています。

![データベース接続を作成](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**サポートされる認証:** パスワードベースの認証のみ

> ⚠️ 他の認証方法を使用する場合は、ODBC ドライバーを使用してください。

### *digna* の構成（ネイティブドライバー）

**"Create a Database Connection"** 画面に次の情報を入力してください。

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC ドライバーは、より幅広い認証および接続オプションをサポートする場合があります。このセクションでは、ドライバー **SQL Server** を使用したパスワードベースの認証に焦点を当てます。

### 1. ODBC ドライバーのインストール

ベンダーの公式インストールガイドに従って、ドライバー **SQL Server**（または同等）をインストールしてください。

### 2. ODBC データソースの構成

パスワードベースの認証を使用して新しい ODBC データソースを構成する手順は次のとおりです。

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

**Next >** ボタンをクリックしてください。

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

認証方法（例：ユーザー名とパスワード）を選択し、必要な情報を入力してください。

**Next >** ボタンをクリックしてください。

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

ANSI 準拠の設定を選択してから **Next >** ボタンをクリックしてください。

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

必要に応じてデフォルト設定のままにするか、ログオプションを選択して **Finish** ボタンをクリックしてください。

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

次に ** Test datasource ** ボタンをクリックしてください。

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

成功画面が表示されたら、ODBC の設定は正しく行われています。

---

これで、**DSN (Data Source Name)** を使用する方法または **DSN-less** 設定のいずれかで、*digna* に ODBC 接続を使用させるよう構成できます。

---

### A. DSN-Based Configuration

#### *digna* の構成

**"Create a Database Connection"** 画面に次の内容を入力してください。

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` は ODBC ドライバー構成で定義した名前と一致している必要があります。

---

### B. DSN-less Configuration

#### *digna* の構成

**"Create a Database Connection"** 画面に次の内容を入力してください。

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```
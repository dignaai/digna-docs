---
title: Oracle コネクタ – データベース統合 | digna ドキュメント
description: python-oracledb ドライバまたは Oracle ODBC ドライバを使用して digna を Oracle に接続する方法を設定します。DSN または DSN-less 構成によるパスワード認証に対応しています。
image: /assets/logo_square.png
---


# Oracle のソースコネクタ

このガイドは、ネイティブの Python コネクタまたは ODBC ドライバのいずれかを使用して *digna* を Oracle DB に接続する方法について説明します。

これは画面 **"Create a Database Connection"** を参照しています。

![Create a database connection](images/data_source_config_input_mask.png)

---

## ネイティブ Python ドライバ

**Library:** `python-oracledb`  
**Supported Authentication:** Password-based authentication only

> 他の認証方式を使用する場合は、ODBC ドライバを使用してください。

### *digna* の設定（ネイティブドライバ）

**"Create a Database Connection"** 画面に以下の情報を入力してください：

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC ドライバ

ODBC ドライバは、より多くの認証方式や接続オプションをサポートしている場合があります。本節では、ドライバ **Oracle in OraDB21Home1** を使用したパスワード認証に焦点を当てます。

### 1. ODBC ドライバのインストール

ベンダーの公式インストールガイドに従って、**Oracle in OraDB21Home1**（または類似のドライバ）をインストールしてください。

### 2. ODBC データソースの構成

パスワード認証を使用して新しい ODBC データソースを構成する手順は次のとおりです。

#### ステップ 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

注:
TNS Service Name は Oracle クライアントの tnsnames.ora ファイルに設定されている必要があります。ここで接続記述子（ホスト、ポート、サービス名）を指定します。

#### ステップ 2 – 接続のテスト

**Test Connection** ボタンをクリックします。

![Step 2](images/oracle/create_odbc_data_source_step2.png)

パスワードを入力して **OK** ボタンをクリックします。

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

これで、**DSN（Data Source Name）** を使用するか **DSN-less** 構成のいずれかで *digna* を ODBC 接続に設定できます。

---

### A. DSN ベースの構成

#### *digna* の設定

**"Create a Database Connection"** 画面に以下を入力してください：

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN` は ODBC ドライバ構成で定義した名前と一致している必要があります。

---

### B. DSN-less 構成

#### *digna* の設定

**"Create a Database Connection"** 画面に以下を入力してください：

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```
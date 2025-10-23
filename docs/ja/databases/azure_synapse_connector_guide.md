---
title: Azure Synapse コネクタ – データベース統合 | digna ドキュメント
description: ネイティブの Python ドライバーまたは ODBC ドライバーを使用して digna を Azure Synapse Analytics に接続する方法を構成します。サーバーレスおよび専用の SQL プールの両方をサポートします。
image: /assets/logo_square.png
---


# Azure Synapse Analytics 用ソースコネクタ

このガイドでは、ネイティブの Python コネクタまたは ODBC ドライバーのいずれかを使用して *digna* を Azure Synapse Analytics に接続する方法を説明します。サーバーレスおよび専用の SQL プールの両方をサポートしています。

画面「Create a Database Connection」を参照します。

![Create a database connection](images/data_source_config_input_mask.png)

---

## ネイティブ Python ドライバー

**Library:** `pymssql`  
**サポートされる認証:** パスワードベースの認証のみ

> ⚠️ その他の認証方法を使用する場合は、ODBC ドライバーを使用してください。

### *digna* の設定（ネイティブドライバー）

「Create a Database Connection」画面に以下の情報を入力してください:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC ドライバー

ODBC ドライバーは、より広範な認証および接続オプションをサポートする場合があります。本節では、ドライバー「ODBC Driver 18 for SQL Server」を使用したパスワードベースの認証に焦点を当てます。

### 1. ODBC ドライバーのインストール

ベンダーの公式インストールガイドに従って、**ODBC Driver 18 for SQL Server**（または同等のドライバー）をインストールしてください。

### 2. ODBC データソースの設定

パスワードベースの認証を使用して新しい ODBC データソースを構成する手順は次のとおりです。

#### Step 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

「Server」フィールドに入力します。  
Synapse ワークスペースの名前を使用し、「.sql.azuresynapse.net」を付加してください。  
**注意**: サーバーレス SQL プールで接続する場合は、下のスクリーンショットに示すように「-ondemand」を含めることを忘れないでください。

**Next >** ボタンをクリックします。

#### Step 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

認証方法（例：ユーザー名とパスワード）を選択し、必要な情報を入力します。

**Next >** ボタンをクリックします。

#### Step 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

ANSI 準拠の設定を選択してから **Next >** ボタンをクリックします。

#### Step 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

デフォルト設定のままにするか、必要に応じてオプションを選択して **Finish** ボタンをクリックします。

#### Step 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

次に **Test datasource** ボタンをクリックします。

#### Step 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

成功画面が表示されたら、ODBC の構成は正しく行われています。

---

これで *digna* を ODBC 接続で使用するように構成できます。DSN（Data Source Name）を使う方法と DSN レスの設定の両方に対応しています。

---

### A. DSN ベースの構成

#### *digna* の設定

「Create a Database Connection」画面に以下を入力してください:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` は ODBC ドライバー設定で定義した名前と一致している必要があります。

---

### B. DSN-less 構成

#### *digna* の設定

「Create a Database Connection」画面に以下を入力してください:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC プロパティ

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**注**（SERVER プロパティについて）:  
Synapse ワークスペースの名前に「.sql.azuresynapse.net」を付加して使用してください。サーバーレス SQL プールで接続する場合は、下のスクリーンショットに示すように「-ondemand」を含めることを忘れないでください。
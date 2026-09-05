# Source Connector for PostgreSQL

このガイドでは、ネイティブの Python コネクタまたは ODBC ドライバのいずれかを使って *digna* を Postgres に接続する方法について説明します。

画面 **"Create a Database Connection"** を参照してください。

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Supported Authentication:** パスワード認証のみ

> 他の認証方式が必要な場合は、ODBC ドライバを使用してください。

### *digna* Configuration (Native Driver)

画面 **"Create a Database Connection"** に以下の情報を入力してください:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC ドライバは、より幅広い認証および接続オプションをサポートする場合があります。本節では、ドライバ **PostgreSQL Unicode(x64)** を用いたパスワード認証に焦点を当てます。

### 1. Install the ODBC Driver

ベンダーの公式インストールガイドに従って、**PostgreSQL Unicode(x64)**（または同等のもの）をインストールしてください。

### 2. Configure the ODBC Data Source

パスワード認証を使用して新しい ODBC データソースを設定するには、次の手順に従います。

#### Step 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

注意: データベース設定で特定の "SSLMode" を選択する必要がある場合、DSN-less 構成を定義する際にも同じ設定を使用してください。

#### Step 2 – Test the connection

**Test Connection** ボタンをクリックします。

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

これで、**DSN (Data Source Name)** を使うか **DSN-less** 構成のいずれかで、*digna* に ODBC 接続を使用させる設定ができます。

---

### A. DSN-Based Configuration

#### *digna* Configuration

画面 **"Create a Database Connection"** に以下を入力してください:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "PostgreSQL35W"
```

> `DSN` は ODBC ドライバ構成で定義した名前と一致している必要があります。

---

### B. DSN-less Configuration

#### *digna* Configuration

画面 **"Create a Database Connection"** に以下を入力してください:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```
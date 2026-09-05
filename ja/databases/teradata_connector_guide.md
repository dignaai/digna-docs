# Teradata 用ソースコネクタ

このガイドでは、ネイティブの Python コネクタまたは ODBC ドライバーのいずれかを使用して *digna* を Teradata に接続する方法を説明します。

画面 **「Create a Database Connection」** を参照します。

![Create a database connection](images/data_source_config_input_mask.png)

---

## ネイティブ Python ドライバー

**ライブラリ:** `teradatasql`  
**サポートされる認証:** パスワード認証のみ

> 他の認証方法を使用する場合は、ODBC ドライバーを使用してください。

### *digna* の設定（ネイティブドライバー）

**「Create a Database Connection」** 画面に次の情報を入力してください:

```
テクノロジー:    Teradata
ホストアドレス:  サーバー名または IP アドレス
ポート番号:      例: 1025
データベース名:  データベース名
スキーマ名:      データベース名
ユーザー名:      データベースのユーザー名
ユーザーパスワード: ユーザーのパスワード
ODBCを使用:      無効（デフォルト）
```

---

## ODBC ドライバー

ODBC ドライバーは、より広範な認証および接続オプションをサポートする場合があります。本節では、ドライバー **Teradata Database ODBC Driver 20.00** を使用したパスワード認証に焦点を当てます。

### 1. ODBC ドライバーのインストール

ベンダーの公式インストールガイドに従って、**Teradata Database ODBC Driver 20.00**（または同等のバージョン）をインストールしてください。

### 2. ODBC データソースの構成

パスワード認証を使用して新しい ODBC データソースを構成するには、次の手順に従います。

#### ステップ 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

**Test** ボタンをクリックします。

#### ステップ 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

ユーザー名とパスワードを入力します。

**OK** ボタンをクリックします。成功画面が表示されたら、ODBC の設定は正常に完了しています。

---

これで、**DSN（Data Source Name）** または **DSN-less** のいずれかの設定で *digna* を ODBC 接続に使用するように構成できます。

---

### A. DSN ベースの構成

#### *digna* の設定

**「Create a Database Connection」** 画面に次の情報を入力してください:

```
テクノロジー:    Teradata
データベース名:  ソーススキーマを含むデータベース
スキーマ名:      ソースデータを含むスキーマ
ODBCを使用:      有効
```

#### ODBC プロパティ

```
name: "DSN",    value: "*digna*data_teradata"
name: "UID",    value: "your database user"
name: "PWD",    value: "your database password"
```

> `DSN` は ODBC ドライバー設定で定義した名前と一致している必要があります。

---

### B. DSN-less 構成

#### *digna* の設定

**「Create a Database Connection」** 画面に次の情報を入力してください:

```
テクノロジー:    Teradata
データベース名:  ソースデータを含むスキーマ（Schema Name と同じ）
スキーマ名:      ソースデータを含むスキーマ
ODBCを使用:      有効
```

#### ODBC プロパティ

```
name: "DRIVER",   value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",  value: "your server name or IP address"
name: "UID",      value: "your database user"
name: "PWD",      value: "your database password"
```
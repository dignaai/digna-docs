---
title: Netezza コネクタ – データベース統合 | digna ドキュメント
description: NetezzaSQL ODBC ドライバーを使用して digna を Netezza に接続する方法を設定します。DSN ベースまたは DSN-less の構成によるパスワード認証をサポートし、柔軟な接続性を提供します。
image: /assets/logo_square.png
---


# Netezza 用ソースコネクタ

このガイドでは、ODBC ドライバーを使用して *digna* を Netezza に接続する方法を説明します。

画面 **"Create a Database Connection"** を参照します。

![データベース接続を作成](images/data_source_config_input_mask.png)

---

## ODBC ドライバー

ODBC ドライバーは、さまざまな認証および接続オプションをサポートする場合があります。本セクションでは、ドライバー **NetezzaSQL** を使用したパスワード認証に焦点を当てます。

### 1. ODBC ドライバーのインストール

ベンダーの公式インストールガイドに従って、ドライバー **NetezzaSQL**（または同等のドライバー）をインストールしてください。

### 2. ODBC データソースの構成

パスワード認証を使用して新しい ODBC データソースを構成する手順は次のとおりです。

#### ステップ 1
![ステップ 1](images/netezza/create_odbc_data_source_step1.png)

ご使用の Netezza ドライバーやセットアップ、セキュリティ要件によっては、**Advanced DSN Options**、**SSL DSN Options**、または **Driver Options** タブにも情報を入力する必要がある場合があります。最も簡単なセットアップでは、**DSN Options** に情報を入力するだけで十分です。

**Test Connection** ボタンをクリックします。

#### ステップ 2
![ステップ 2](images/netezza/create_odbc_data_source_step2.png)

成功画面が表示されたら、ODBC の設定は正しく行われています。

---

これで、**DSN（Data Source Name）** を使用するか、**DSN-less** 構成のいずれかで *digna* に ODBC 接続を設定できます。

---

### A. DSN ベースの構成

#### *digna* の設定

**"Create a Database Connection"** 画面で、次の項目を入力してください：

```
Technology:      Netezza
Database Name:   ソーススキーマを含むデータベース
Schema Name:     ソースデータを含むスキーマ
Use ODBC:        有効
```

#### ODBC プロパティ

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "データベースのユーザー"
name: "PWD",        value: "データベースのパスワード"
```

> `DSN` は ODBC ドライバー構成で定義した名前と一致する必要があります。

---

### B. DSN-less 構成

#### *digna* の設定

**"Create a Database Connection"** 画面で、次の項目を入力してください：

```
Technology:      Netezza
Database Name:   ソースデータを含むスキーマ（Schema Name と同じ）
Schema Name:     ソースデータを含むスキーマ
Use ODBC:        有効
```

#### ODBC プロパティ

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "サーバー名または IP アドレス"
name: "PORT",       value: "ポート番号（例: 5480）"
name: "DATABASE",   value: "ソースデータスキーマを含むデータベース名"
name: "UID",        value: "データベースのユーザー"
name: "PWD",        value: "データベースのパスワード"
```
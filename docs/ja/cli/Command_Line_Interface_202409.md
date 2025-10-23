---
title: digna CLI リファレンス 2024.09 – コマンドと例 | digna ドキュメント
description: digna CLI リリース 2024.09 の完全リファレンス。add-user、check-repo-connection、upgrade-repo、inspect、tls-status などのコマンドを使ったユーザー、リポジトリ、データの管理方法を解説します。
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI リファレンス 2024.09
**2024-08-24**

---

## CLI 基本

---

### help

--help オプションは利用可能なコマンドとその使い方に関する情報を提供します。主に2つの使い方があります。

1. **一般的なヘルプを表示する場合：**
   
   キーワード ***digna*** の直後に --help を付けて使用します。  
   bash
   dignacli --help

2. **特定のコマンドのヘルプを得る場合：**
   
   特定コマンドの詳細情報を得たいときは、そのコマンドに --help を付けます。  
   例えば、add-user コマンドのヘルプを取得するには次を実行します：  
   bash
   dignacli add-user --help
     

### 出力:
      
- **コマンドの説明:** コマンドが行う処理の詳細な説明。  
- **構文:** 必須およびオプション引数を含む正確な構文。  
- **オプション:** コマンド固有のオプションとその説明の一覧。  
- **例:** コマンドの実行方法の例。

  
### check-repo-connection

check-repo-connection コマンドは、***digna*** CLI ツール内のユーティリティで、指定した ***digna*** リポジトリへの接続性とアクセスをテストするためのコマンドです。CLI がリポジトリとやり取りできることを確認します。
      
##### コマンド使用法
bash
dignacli check-repo-connection


正常に実行されると、接続の確認メッセージとともにリポジトリの詳細（リポジトリバージョン、ホスト、データベース、スキーマなど）が出力されます。  
  
リポジトリ接続が成功しない場合は、config.toml ファイルの設定が正しいか確認してください。

### version

インストール済みの *dignacli* のバージョンを確認するには --version オプションを使用します。  
  
#### コマンド使用法
bash
dignacli --version

  
#### 例の出力
bash
dignacli version 2024.09


### ロギングオプション
  
デフォルトでは、***digna*** コマンドのコンソール出力は最小限に抑えられています。ほとんどのコマンドは追加情報を出力するオプションを提供しており、以下のオプションが利用できます：  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
「verbose」と「debug」は詳細レベルを定義し、"logfile" スイッチは出力をコンソールではなくファイルにストリームすることを可能にします。

## ユーザー管理

### add-user
  
add-user コマンドは、***digna*** CLI で新しいユーザーを ***digna*** システムに追加するために使用します。
  
#### コマンド使用法
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### 引数

- **USER_NAME**: 新しいユーザーのユーザー名（必須）。
- **USER_FULL_NAME**: 新しいユーザーのフルネーム（必須）。
- **USER_PASSWORD**: 新しいユーザーのパスワード（必須）。

#### オプション

- --is_superuser, -su: 新しいユーザーを管理者として指定するフラグ。
- --valid_until, -vu: アカウントの有効期限を YYYY-MM-DD HH:MI:SS 形式で設定します。未設定の場合は有効期限なし。

#### 例

ユーザー名 jdoe、フルネーム John Doe、パスワード password123 の新規ユーザーを追加する場合：

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
アカウントの有効期限を設定してユーザーを追加する場合：
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


### delete-user
  
delete-user コマンドは、***digna*** CLI で既存のユーザーを ***digna*** システムから削除するために使用します。
  
##### コマンド使用法
bash
dignacli delete-user USER_NAME

  
#### 引数
- **USER_NAME**: 削除するユーザーのユーザー名（必須）。このコマンドで必要なのはこの引数のみです。

#### 例
bash
dignacli delete-user jdoe

  
このコマンドを実行すると、ユーザー jdoe は ***digna*** システムから削除され、アクセス権が取り消され、リポジトリから関連するデータと権限が削除されます。

### modify-user

modify-user コマンドは、***digna*** CLI で既存ユーザーの詳細を更新するために使用します。

##### コマンド使用法
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### 引数
  
- **USER_NAME**: 変更対象のユーザー名（必須）。
- **USER_FULL_NAME**: ユーザーの新しいフルネーム（必須）。
  
#### オプション  
  
- --is_superuser, -su: ユーザーをスーパーユーザーに設定し、昇格した権限を付与します。このフラグは値を必要としません。  
- --valid_until, -vu: アカウントの有効期限を YYYY-MM-DD HH:MI:SS 形式で設定します。指定しない場合、アカウントは無期限のままです。  
  
#### 例
  
ユーザー jdoe のフルネームを “Johnathan Doe” に変更し、スーパーユーザーに設定する場合：
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


### modify-user-pwd
  
modify-user-pwd コマンドは、***digna*** CLI で既存ユーザーのパスワードを変更するために使用します。
  
##### コマンド使用法
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### 引数
  
- **USER_NAME**: パスワードを変更するユーザーのユーザー名（必須）。
- **USER_PWD**: 新しいパスワード（必須）。
  
#### 例
  
ユーザー jdoe のパスワードを newpassword123 に変更する場合：
bash
dignacli modify-user-pwd jdoe newpassword123


### list-users

list-users コマンドは、***digna*** CLI で登録されているすべてのユーザーの一覧を表示します。

##### コマンド使用法

bash
dignacli list-users


このコマンドを実行すると、***digna*** リポジトリに接続してすべてのユーザーを一覧表示し、ID、ユーザー名、フルネーム、スーパーユーザーのステータス、有効期限のタイムスタンプを表示します。

# リポジトリ管理

### upgrade-repo
  
upgrade-repo コマンドは、***digna*** CLI で ***digna*** リポジトリをアップグレードまたは初期化するために使用します。このコマンドは更新を適用したり、リポジトリのインフラを初めてセットアップするときに必須です。
  
#### コマンド使用法

bash
dignacli upgrade-repo [options]

  
#### オプション
  
- --simulation-mode, -s: 有効にするとシミュレーションモードで実行され、実行される SQL 文を表示するだけで実際には実行しません。変更をプレビューするのに便利です。  

  
#### 例
  
***digna*** リポジトリをアップグレードするには、オプションなしでコマンドを実行します：
  
bash
dignacli upgrade-repo
  
シミュレーションモードでアップグレードを実行し（SQL 文を確認するのみ）：
  
bash
dignacli upgrade-repo --simulation-mode

  
このコマンドは、データベーススキーマやその他のリポジトリコンポーネントがソフトウェアの最新バージョンと整合していることを保証するため、***digna*** システムの維持に重要です。

### encrypt
  
encrypt コマンドは、***digna*** CLI でパスワードを暗号化するために使用します。
  
#### コマンド使用法
  
bash
dignacli encrypt <PASSWORD>

    
#### 引数
- **PASSWORD**: 暗号化するパスワード（必須）。
  
#### 例
  
パスワードを暗号化するには、パスワードを引数として渡します。  
例えば、mypassword123 を暗号化する場合：
bash
dignacli encrypt mypassword123

このコマンドは、指定したパスワードの暗号化版を出力します。暗号化された値は安全なコンテキストで使用できます。パスワード引数が提供されない場合、CLI は引数が欠落していることを示すエラーを表示します。

### generate-key
  
generate-key コマンドは、Fernet キーを生成するために使用されます。これは ***digna*** リポジトリに保存されるパスワードを保護するために必要です。
  
#### コマンド使用法
bash
dignacli generate-key

  
## データ管理

### clean-up

clean-up コマンドは、***digna*** CLI で指定したプロジェクト内の1つ以上のデータソースに対してプロファイル、予測、およびトラフィックライトシステムのデータを削除するために使用します。このコマンドはデータライフサイクル管理に不可欠で、古いまたは不要なデータをクリアして整理された効率的なデータ環境を維持するのに役立ちます。

#### コマンド使用法

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### 引数
  
- **PROJECT_NAME**: データを削除するプロジェクト名（必須）。この引数に all-projects を指定すると、***digna*** は既存の全プロジェクトを順に処理してコマンドを適用します。
- **FROM_DATE**: データ削除の開始日時。許容される形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: データ削除の終了日時。FROM_DATE と同じ形式を使用します（必須）。
  
#### オプション
  
- --table-name, -tn: クリーンアップをプロジェクト内の特定テーブルに限定します。
- --table-filter, -tf: テーブル名に指定したサブストリングを含むテーブルに限定してクリーンアップします。
- --timing, -tm: 完了後にクリーンアップ処理の所要時間を表示します。
- --help: clean-up コマンドのヘルプ情報を表示して終了します。
  
#### 例
  
ProjectA プロジェクトの 2023年1月1日 から 2023年6月30日 までのデータを削除する場合：
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
特定のテーブル Table1 のみからデータを削除する場合：
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
このコマンドは、データストレージの管理とリポジトリに関連性のある情報だけを保持することに役立ちます。

### inspect

inspect コマンドは、***digna*** CLI で指定したプロジェクト内の1つ以上のデータソースについてプロファイル、予測、およびトラフィックライトシステムのデータを作成するために使用します。このコマンドは、定義した期間内でデータの解析と監視を行うのに役立ちます。

#### コマンド使用法

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### 引数
  
- **PROJECT_NAME**: データを検査するプロジェクト名（必須）。この引数に all-projects を指定すると、***digna*** は既存の全プロジェクトを順に処理してコマンドを適用します。
- **FROM_DATE**: データ検査の開始日時。許容される形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: データ検査の終了日時。FROM_DATE と同じ形式を使用します（必須）。
  
#### オプション

- --table-name, -tn: 検査をプロジェクト内の特定テーブルに限定します。
- --table-filter, -tf: 指定したサブストリングを含むテーブルのみを検査します。
- --force-profile: プロファイルの再収集を強制します。デフォルトは force-profile。
- --no-force-profile: プロファイルの再収集を行わないようにします。
- --force-prediction: 予測の再計算を強制します。デフォルトは force-prediction。
- --no-force-prediction: 予測の再計算を行わないようにします。
- --force-alert-status: アラートステータスの再計算を強制します。デフォルトは force-alert-status。
- --no-force-alert-status: アラートステータスの再計算を行わないようにします。
- --timing, -tm: 完了後に検査処理の所要時間を表示します。
- --alert-notification, -an: サブスクライブされたチャネルへアラート通知を送信します。
  
#### 例
  
ProjectA のデータを 2024年1月1日 から 2024年1月31日 まで検査する場合：
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
特定テーブルのみを検査し、予測の再計算を強制する場合：
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

このコマンドは、更新されたプロファイルや予測の生成、データ整合性の監視、および指定したプロジェクト期間内でのアラートシステムの管理に役立ちます。

### tls-status

tls-status コマンドは、***digna*** CLI で指定したプロジェクト内の特定テーブルに対して、指定日の Traffic Light System (TLS) のステータスを照会するために使用します。Traffic Light System はデータの健全性と品質に関する洞察を提供し、注意が必要な問題やアラートを示します。
  
#### コマンド使用法
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### 引数
  
- **PROJECT_NAME**: TLS ステータスを照会するプロジェクト名（必須）。
- **TABLE_NAME**: TLS ステータスを確認するプロジェクト内の特定テーブル（必須）。
- **DATE**: TLS ステータスを照会する日付。通常 %Y-%m-%d 形式（必須）。
  
#### 例
  
ProjectA の UserData テーブルについて 2024年7月1日の TLS ステータスを確認する場合：

bash
dignacli tls-status ProjectA UserData 2024-07-01


このコマンドは、定義済みの基準に基づいて明確で実行可能なステータスレポートを提供し、ユーザーがデータ品質を監視・維持するのに役立ちます。

### list-projects
  
list-projects コマンドは、***digna*** CLI で利用可能なすべてのプロジェクトの一覧を表示するために使用します。
  
#### コマンド使用法
  
bash
dignacli list-projects


このコマンドは、複数のプロジェクトを管理する管理者やユーザーにとって特に便利で、***digna*** リポジトリ内の利用可能なプロジェクトの概要を素早く把握できます。

### list-ds

list-ds コマンドは、***digna*** CLI で指定したプロジェクト内の利用可能なデータソースの一覧を表示するために使用します。これは、***digna*** システムで分析・管理可能なデータ資産を把握するのに有用です。

#### コマンド使用法
  
bash
dignacli list-ds <PROJECT_NAME>


#### 引数
- **PROJECT_NAME**: データソースを一覧表示するプロジェクト名（必須）。
  
#### 例
  
ProjectA プロジェクト内のすべてのデータソースを一覧表示する場合：
  
bash
dignacli list-ds ProjectA

  
このコマンドは、プロジェクト内で利用可能なデータソースの概要をユーザーに提供し、データの整理や管理をより効果的に行えるようにします。
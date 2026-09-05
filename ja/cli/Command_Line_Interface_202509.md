# digna CLI リファレンス 2025.09
**2025-09-29**

このページでは、***digna*** CLI リリース **2025.09** で利用可能な全コマンドの一覧、使用例、およびオプションをドキュメント化しています。

---

## CLI の基本

---

### help
`--help` オプションは、利用可能なコマンドとその使い方に関する情報を提供します。このオプションの使い方は主に2通りあります。

1. **一般的なヘルプの表示:**
   
   キーワード ***dignacli*** の直後に `--help` を指定します。  
   ```bash
   dignacli --help
   ```

2. **特定コマンドのヘルプを取得する:**

   特定のコマンドについて詳しい情報が必要な場合は、そのコマンドに `--help` を付けます。  
   例えば `add-user` コマンドのヘルプを取得するには次を実行します。  
   ```bash
   dignacli add-user --help
   ```

   ### 出力:

   - **コマンドの説明:** コマンドが実行する内容の詳細説明。  
   - **構文:** 必須引数とオプションを含む正確な構文。  
   - **オプション:** 各コマンド固有のオプションとその説明。  
   - **例:** コマンドの効果的な実行方法の例。

### check-config

`check-config` コマンドは、***digna*** の設定をテストするためのユーティリティです。このコマンドは、***digna*** のコンポーネントが config.toml 内の必要な設定要素を見つけられるかを検証します。

#### オプション

- `--configpath`, `-cp`: 設定ファイルまたは設定ディレクトリのパス。省略した場合は ../config.toml が使用されます。
      
#### コマンドの使用法
```bash
dignacli check-config
```

正常に実行されると、設定の完全性が確認された旨が出力されます。  
  
設定が不完全な場合は、欠落している設定要素が一覧表示されます。

  
### check-repo-connection

`check-repo-connection` コマンドは、指定した ***digna*** リポジトリへの接続性とアクセス権をテストするためのユーティリティです。このコマンドは、CLI がリポジトリとやり取りできるかどうかを確認します。
      
#### コマンドの使用法
```bash
dignacli check-repo-connection
```

正常に実行されると、接続の確認とともにリポジトリの詳細（リポジトリのバージョン、ホスト、データベース、スキーマ）が出力されます。  
  
リポジトリへの接続が成功しない場合は、config.toml ファイルの設定が正しいか確認してください。


### version

インストールされている *dignacli* のバージョンを確認するには `--version` オプションを使用します。  
  
#### コマンドの使用法
```bash
dignacli --version
```
  
#### 例（出力）
```bash
dignacli version 2025.09
```

### ロギングオプション
  
デフォルトでは、***digna*** コマンドのコンソール出力は最小限に抑えられています。多くのコマンドは追加情報を出力するオプションを提供しており、次のオプションで制御できます。  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
「verbose」と「debug」は出力の詳細レベルを定義し、「logfile」は出力をコンソールではなくファイルへリダイレクトするためのスイッチです。

## ユーザー管理

### add-user
  
`add-user` コマンドは、***digna*** システムに新しいユーザーを追加するために使用します。
  
#### コマンドの使用法
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### 引数

- **USER_NAME**: 新規ユーザーのユーザー名（必須）。
- **USER_FULL_NAME**: 新規ユーザーのフルネーム（必須）。
- **USER_PASSWORD**: 新規ユーザーのパスワード（必須）。

#### オプション

- `--is_superuser`, `-su`: 新規ユーザーを管理者（スーパーユーザー）として指定するフラグ。
- `--valid_until`, `-vu`: ユーザーアカウントの有効期限を `YYYY-MM-DD HH:MI:SS` 形式で設定します。指定しない場合は有効期限なしになります。

#### 例

ユーザー名 `jdoe`、フルネーム `John Doe`、パスワード `password123` の新規ユーザーを追加する例:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
アカウント有効期限を設定して新規ユーザーを追加する例:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
`delete-user` コマンドは、既存のユーザーを ***digna*** システムから削除するために使用します。
  
#### コマンドの使用法
```bash
dignacli delete-user USER_NAME
```
  
#### 引数
- **USER_NAME**: 削除するユーザーのユーザー名（必須）。このコマンドで必要な唯一の引数です。

#### 例
```bash
dignacli delete-user jdoe
```
  
このコマンドを実行すると、ユーザー `jdoe` は ***digna*** システムから削除され、アクセス権が取り消され、リポジトリ内の関連データと権限が削除されます。

### modify-user

`modify-user` コマンドは、既存ユーザーの情報を更新するために使用します。

#### コマンドの使用法
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### 引数
  
- **USER_NAME**: 更新対象のユーザー名（必須）。
- **USER_FULL_NAME**: ユーザーの新しいフルネーム（必須）。
  
#### オプション  
  
- `--is_superuser`, `-su`: ユーザーをスーパーユーザーとして設定し、権限を昇格させます。このフラグは値を必要としません。  
- `--valid_until`, `-vu`: アカウントの有効期限を `YYYY-MM-DD HH:MI:SS` 形式で設定します。指定しない場合は無期限のままです。  
  
#### 例
  
ユーザー `jdoe` のフルネームを “Johnathan Doe” に変更し、スーパーユーザーに設定する例:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd` コマンドは、既存ユーザーのパスワードを変更するために使用します。
  
#### コマンドの使用法
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### 引数
  
- **USER_NAME**: パスワードを変更するユーザー名（必須）。
- **USER_PWD**: 新しいパスワード（必須）。
  
#### 例
  
ユーザー `jdoe` のパスワードを `newpassword123` に変更する例:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users` コマンドは、***digna*** システムに登録されているすべてのユーザーを表示します。

#### コマンドの使用法

```bash
dignacli list-users
```

このコマンドを実行すると、***digna*** リポジトリに接続してすべてのユーザーを一覧表示し、ID、ユーザー名、フルネーム、スーパーユーザーかどうか、有効期限のタイムスタンプ等を表示します。

## リポジトリ管理

### upgrade-repo
  
`upgrade-repo` コマンドは、***digna*** リポジトリをアップグレードまたは初期化するために使用します。このコマンドは、更新を適用したり、初めてリポジトリをセットアップする際に必要です。
  
#### コマンドの使用法

```bash
dignacli upgrade-repo [options]
```
  
#### オプション
  
- `--simulation-mode`, `-s`: このオプションを有効にするとシミュレーションモードで実行され、実際には実行されない SQL 文を出力します。リポジトリに変更を加えずに変更内容を確認するのに便利です。  

  
#### 例
  
リポジトリをアップグレードする（オプションなしで実行）:
  
```bash
dignacli upgrade-repo
```  
シミュレーションモードでアップグレードを実行して SQL 文のみを確認する例:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
このコマンドは ***digna*** システムの保守に不可欠であり、データベーススキーマやその他のリポジトリコンポーネントをソフトウェアの最新バージョンに合わせて更新します。

### encrypt
  
`encrypt` コマンドは、パスワードを暗号化するために使用します。
  
#### コマンドの使用法
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### 引数
- **PASSWORD**: 暗号化するパスワード（必須）。
  
#### 例
  
パスワードを暗号化するには、パスワードを引数として渡します。例えば `mypassword123` を暗号化するには次のように実行します:
```bash
dignacli encrypt mypassword123
```
このコマンドは渡されたパスワードの暗号化結果を出力し、リポジトリやその他のセキュアなコンテキストで使用できます。パスワード引数が渡されない場合は、引数不足のエラーが表示されます。

### generate-key
  
`generate-key` コマンドは、Fernet キーを生成するために使用します。このキーは、***digna*** リポジトリに格納されるパスワードの保護に必要です。
  
#### コマンドの使用法
```bash
dignacli generate-key
```
  
## データ管理

### clean-up

`clean-up` コマンドは、指定したプロジェクト内の1つ以上のデータソースに対してプロファイル、予測、およびトラフィックライトシステムのデータを削除するために使用します。このコマンドはデータライフサイクル管理に不可欠で、古くなったデータや不要なデータを削除して環境を整理・最適化するのに役立ちます。

#### コマンドの使用法

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 引数
  
- **PROJECT_NAME**: データを削除するプロジェクト名（必須）。この引数に `all-projects` を指定すると、既存のすべてのプロジェクトに対してこのコマンドを繰り返し実行します。
- **FROM_DATE**: データ削除の開始日時。許容される形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: データ削除の終了日時。FROM_DATE と同様の形式（必須）。
  
#### オプション
  
- `--table-name`, `-tn`: プロジェクト内の特定テーブルに対してクリーンアップを制限します。
- `--table-filter`, `-tf`: 指定した部分文字列をテーブル名に含むテーブルのみを対象にします。
- `--timing`, `-tm`: クリーンアップ処理の所要時間を完了後に表示します。
- `--help`: clean-up コマンドのヘルプ情報を表示して終了します。
  
#### 例
  
ProjectA から 2023-01-01 から 2023-06-30 までのデータを削除する例:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
特定のテーブル `Table1` のみからデータを削除する例:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
このコマンドはストレージ管理に役立ち、リポジトリに関連性のある情報のみを保持することを支援します。

### remove-orphans
  
`remove-orphans` コマンドは、***digna*** リポジトリ内のハウスキーピング用コマンドです。  
ユーザーがプロジェクトやデータソースを削除しても、プロファイルや予測がリポジトリに残ることがあります。このコマンドを使うと、そのような孤立した（オーファン）行をリポジトリから削除できます。
  
#### コマンドの使用法
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects` コマンドは、***digna*** システム内で利用可能なすべてのプロジェクトを一覧表示するために使用します。
  
#### コマンドの使用法
  
```bash
dignacli list-projects
```

このコマンドは複数のプロジェクトを管理する管理者やユーザーにとって有用で、***digna*** リポジトリ内のプロジェクトを素早く確認できます。

### list-ds

`list-ds` コマンドは、指定したプロジェクト内の利用可能なすべてのデータソースを一覧表示するために使用します。このコマンドは、分析や管理の対象となるデータ資産を把握するのに役立ちます。

#### コマンドの使用法
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### 引数
- **PROJECT_NAME**: データソースを一覧表示する対象プロジェクト名（必須）。
  
#### 例
  
ProjectA 内のすべてのデータソースを一覧表示する例:
  
```bash
dignacli list-ds ProjectA
```
  
このコマンドは、プロジェクト内で利用可能なデータソースの概要を提供し、データ管理を効率的に行うのに役立ちます。


### inspect

`inspect` コマンドは、指定したプロジェクト内の1つ以上のデータソースに対してプロファイル、予測、およびトラフィックライトシステムのデータを作成するために使用します。このコマンドは、指定した期間にわたるデータの解析と監視を支援します。検査完了後、計算されたトラフィックライトシステムの値が返されます:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### コマンドの使用法

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 引数
  
- **PROJECT_NAME**: 検査対象のプロジェクト名（必須）。この引数に `all-projects` を指定すると、既存のすべてのプロジェクトに対してこのコマンドを繰り返し実行します。
- **FROM_DATE**: データ検査の開始日時。許容される形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: データ検査の終了日時。FROM_DATE と同様の形式（必須）。
  
#### オプション

- `--table-name`, `-tn`: 検査をプロジェクト内の特定テーブルに限定します。
- `--table-filter`, `-tf`: 指定した部分文字列を含むテーブルのみを検査対象にします。
- `--enable_notification`, `-en`: アラート発生時に通知を送信する機能を有効にします。
- `--bypass-backend`, `-bb`: バックエンドをバイパスして CLI から直接検査を実行します（テスト目的のみ推奨）。

  
#### 例
  
ProjectA の 2024-01-01 から 2024-01-31 までのデータを検査する例:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
特定のテーブルのみ検査し、予測の再計算を強制する例:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
このコマンドは、プロファイルや予測の更新、データ整合性の監視、および指定したプロジェクト期間内のアラート管理に役立ちます。

### inspect-async

`inspect-async` コマンドは、指定したプロジェクト内の1つ以上のデータソースに対してプロファイル、予測、およびトラフィックライトシステムのデータを作成するために使用します。このコマンドは指定期間にわたるデータの解析と監視を支援します。`inspect` コマンドとは異なり、このコマンドは検査の完了を待たずに終了し、送信された検査リクエストのリクエスト ID を返します。検査の進捗を確認するには `inspect-status` コマンドを使用してください。

#### コマンドの使用法

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 引数
  
- **PROJECT_NAME**: 検査対象のプロジェクト名（必須）。この引数に `all-projects` を指定すると、既存のすべてのプロジェクトに対してこのコマンドを繰り返し実行します。
- **FROM_DATE**: データ検査の開始日時。許容される形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: データ検査の終了日時。FROM_DATE と同様の形式（必須）。
  
#### オプション

- `--table-name`, `-tn`: 検査をプロジェクト内の特定テーブルに限定します。
- `--table-filter`, `-tf`: 指定した部分文字列を含むテーブルのみを検査対象にします。
- `--enable_notification`, `-en`: アラート発生時に通知を送信する機能を有効にします。

  
#### 例
  
ProjectA の 2024-01-01 から 2024-01-31 までのデータを非同期で検査する例:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status` コマンドは、非同期検査の進捗をリクエスト ID に基づいて確認するために使用します。

#### コマンドの使用法

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### 引数
  
- **REQUEST_ID**: `inspect-async` コマンドが返すリクエスト ID。
  
#### 例
  
リクエスト ID 12345 の検査進捗を確認する例:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel` コマンドは、リクエスト ID に基づいて検査をキャンセルするか、または全ての現在のリクエストをキャンセルするために使用します。

#### コマンドの使用法

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### 引数
  
- **REQUEST_ID**: `inspect-async` コマンドが返すリクエスト ID。
  
#### 例
  
リクエスト ID 12345 の検査をキャンセルする例:
  
```bash
dignacli inspect-cancel 12345
```

現在実行中または保留中のすべてのリクエストをキャンセルする例:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds` コマンドは、***digna*** リポジトリからデータソースのエクスポートを作成するために使用します。デフォルトでは、指定したプロジェクトのすべてのデータソースがエクスポートされます。

#### コマンドの使用法
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### 引数
- **PROJECT_NAME**: データソースをエクスポートするプロジェクト名。

#### オプション

- `--table_name`, `-tn`: プロジェクト内の特定のデータソースをエクスポートします。
- `--exportfile`, `-ef`: エクスポートファイル名を指定します。
    
#### 例
  
ProjectA のすべてのデータソースをエクスポートする例:
  
```bash
dignacli export-ds ProjectA
```
  
このコマンドは `ProjectA` のすべてのデータソースを JSON ドキュメントとしてエクスポートし、別のプロジェクトや ***digna*** リポジトリへインポートできます。


### import-ds

`import-ds` コマンドは、データソースのエクスポートをターゲットプロジェクトにインポートし、インポートレポートを作成するために使用します。

#### コマンドの使用法
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### 引数
- **PROJECT_NAME**: データソースをインポートする対象プロジェクト名。
- **EXPORT_FILE**: インポートするデータソースのエクスポートファイル名。

#### オプション

- `--output-file`, `-o`: インポートレポートを保存するファイル（指定しない場合はターミナルに表形式で出力）。
- `--output-format`, `-f`: インポートレポートの保存形式（json, csv）。
    
#### 例
  
エクスポートファイル `my_export.json` のデータソースを `ProjectB` にインポートする例:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
インポート後、このコマンドはインポートされたオブジェクトとスキップされたオブジェクトのレポートも表示します。`ProjectB` には新規のデータソースのみがインポートされます。どのオブジェクトがインポートされ、どれがスキップされるかを事前に確認するには `plan-import-ds` コマンドを使用してください。

### plan-import-ds

`plan-import-ds` コマンドは、データソースのエクスポートをターゲットプロジェクトにインポートする前に、その内容を解析してインポート計画（どのオブジェクトがインポートされ、どれがスキップされるか）を表示するために使用します。

#### コマンドの使用法
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### 引数
- **PROJECT_NAME**: エクスポートをインポートする場合の対象プロジェクト名。
- **EXPORT_FILE**: インポート前に解析するエクスポートファイル名。

#### オプション

- `--output-file`, `-o`: インポート計画レポートを保存するファイル（指定しない場合はターミナルに表形式で出力）。
- `--output-format`, `-f`: レポートの保存形式（json, csv）。
    
#### 例
  
エクスポートファイル `my_export.json` を `ProjectB` にインポートした場合にどのデータソースがインポートされ、どれがスキップされるかを確認する例:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
このコマンドは、インポートされるオブジェクトとスキップされるオブジェクトの計画のみを表示します。
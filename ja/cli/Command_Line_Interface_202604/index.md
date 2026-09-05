# digna CLI Reference 2026.04
**2026-04-08**

このページは ***digna*** CLI リリース **2026.04** で利用可能な全コマンドの一覧（使用例とオプションを含む）を記載しています。

---

## CLI Basics

---

### help
`--help` オプションは、利用可能なコマンドとその使用方法に関する情報を提供します。このオプションの主な使い方は次の2通りです。

1. **一般的なヘルプの表示:**
   
    キーワード ***dignacli*** の直後に `--help` を付けて使用します。  
   ```bash
   dignacli --help
   ```

2. **特定のコマンドのヘルプ取得:**  
  
    特定のコマンドの詳細情報を得るには、そのコマンドの後に `--help` を付けます。  
    例えば `add-user` コマンドのヘルプを取得するには次を実行します:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **コマンドの説明:** コマンドが何を行うかの詳細説明。  
     - **構文:** 必須およびオプションの引数を含む正確な構文。  
     - **オプション:** コマンド固有のオプションとその説明の一覧。  
     - **例:** コマンドの効果的な実行方法の例。

### check-config

`check-config` コマンドは、***digna*** CLI 内のユーティリティで、***digna*** の設定をテストするために使用されます。このコマンドは、***digna*** コンポーネントが config.toml 内で必要な設定要素を検出できるかを確認します。

#### Options

- `--configpath`, `-cp`: 設定を含むファイルまたはディレクトリ。省略した場合は ../config.toml が使用されます。
      
#### Command Usage
```bash
dignacli check-config
```

正常に実行されると、設定の完全性に関する確認が出力されます。  
  
設定が不完全な場合は、欠落している設定要素が一覧表示されます。

  
### check-repo-connection

`check-repo-connection` コマンドは、指定した ***digna*** リポジトリへの接続性とアクセスをテストするためのユーティリティです。CLI がリポジトリとやり取りできるかを確認します。
      
#### Command Usage
```bash
dignacli check-repo-connection
```

正常に実行されると、接続の確認とともにリポジトリに関する詳細（リポジトリのバージョン、ホスト、データベース、スキーマ）が出力されます。  
  
リポジトリ接続が成功しない場合は、config.toml ファイルの設定が正しいか確認してください。


### version

インストールされている *dignacli* のバージョンを確認するには `--version` オプションを使用します。  
  
#### Command Usage
```bash
dignacli --version
```
  
#### Example Output
```bash
dignacli version 2026.04
```

### logging options
  
デフォルトでは、***digna*** コマンドのコンソール出力は最小限に設計されています。ほとんどのコマンドは、以下のオプションを使用して追加情報を出力することが可能です。  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
「verbose」と「debug」は詳細レベルを定義し、「logfile」スイッチは出力をコンソールではなくファイルへリダイレクトすることを可能にします。

## User Management

### add-user
  
`add-user` コマンドは、***digna*** システムに新しいユーザーを追加するために使用します。
  
#### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Arguments

- **USER_NAME**: 新規ユーザーのユーザー名（必須）。
- **USER_FULL_NAME**: 新規ユーザーのフルネーム（必須）。
- **USER_PASSWORD**: 新規ユーザーのパスワード（必須）。

#### Options

- `--is_superuser`, `-su`: 新しいユーザーを管理者として指定するフラグ。
- `--valid_until`, `-vu`: アカウントの有効期限を `YYYY-MM-DD HH:MI:SS` 形式で設定します。設定しない場合、アカウントに有効期限はありません。

#### Example

ユーザー名 `jdoe`、フルネーム `John Doe`、パスワード `password123` の新規ユーザーを追加するには:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
アカウントの有効期限を設定してユーザーを追加するには:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
`delete-user` コマンドは、既存のユーザーを ***digna*** システムから削除するために使用します。
  
#### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
#### Arguments
- **USER_NAME**: 削除するユーザーのユーザー名（必須）。この引数のみがコマンドの必須引数です。

#### Example
```bash
dignacli delete-user jdoe
```
  
このコマンドを実行すると、ユーザー `jdoe` が ***digna*** システムから削除され、アクセス権が取り消され、リポジトリから関連するデータと権限が削除されます。

### modify-user

`modify-user` コマンドは、既存ユーザーの情報を更新するために使用します。

#### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Arguments
  
- **USER_NAME**: 更新対象のユーザー名（必須）。
- **USER_FULL_NAME**: ユーザーの新しいフルネーム（必須）。
  
#### Options  
  
- `--is_superuser`, `-su`: ユーザーをスーパーユーザーに設定し、権限を昇格させます。このフラグは値を必要としません。  
- `--valid_until`, `-vu`: アカウントの有効期限を `YYYY-MM-DD HH:MI:SS` 形式で設定します。指定しない場合、アカウントは無期限で有効です。  
  
#### Example
  
ユーザー `jdoe` のフルネームを “Johnathan Doe” に変更し、スーパーユーザーに設定するには:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd` コマンドは、既存ユーザーのパスワードを変更するために使用します。
  
#### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Arguments
  
- **USER_NAME**: パスワードを変更するユーザー名（必須）。
- **USER_PWD**: 新しいパスワード（必須）。
  
#### Example
  
ユーザー `jdoe` のパスワードを `newpassword123` に変更するには:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users` コマンドは、***digna*** システムに登録されている全ユーザーの一覧を表示します。

#### Command Usage

```bash
dignacli list-users
```

このコマンドを実行すると、***digna*** リポジトリに接続して全ユーザーを一覧表示し、ID、ユーザー名、フルネーム、スーパーユーザーかどうか、および有効期限のタイムスタンプを表示します。

## Repository Management

### upgrade-repo
  
`upgrade-repo` コマンドは、***digna*** リポジトリのアップグレードまたは初期化に使用します。これは更新の適用やリポジトリのインフラを初めて設定する際に不可欠なコマンドです。
  
#### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: 有効にするとシミュレーションモードで実行され、実際には SQL を実行せずに実行されるであろう SQL 文を表示します。リポジトリに対する変更を適用せずにプレビューするのに便利です。  

  
#### Example
  
***digna*** リポジトリをアップグレードするにはオプション無しで実行できます:
  
```bash
dignacli upgrade-repo
```  
シミュレーションモードで実行して（SQL 文を確認するだけで適用しない）:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
このコマンドは ***digna*** システムの維持に重要であり、データベーススキーマやその他のリポジトリコンポーネントがソフトウェアの最新バージョンに追従していることを保証します。

### encrypt
  
`encrypt` コマンドは、パスワードを暗号化するために使用します。
  
#### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Arguments
- **PASSWORD**: 暗号化するパスワード（必須）。
  
#### Example
  
パスワードを暗号化するには、パスワードを引数として指定します。  
例えば、パスワード `mypassword123` を暗号化するには次のようにします:
```bash
dignacli encrypt mypassword123
```
このコマンドは指定したパスワードの暗号化されたバージョンを出力し、セキュアなコンテキストで使用できます。パスワード引数が指定されない場合、CLI は引数の欠如を示すエラーを表示します。

### generate-key
  
`generate-key` コマンドは Fernet キーを生成するために使用します。これは ***digna*** リポジトリに保存されるパスワードを保護するために必要です。
  
#### Command Usage
```bash
dignacli generate-key
```
  
## Data Management

### clean-up

`clean-up` コマンドは、指定したプロジェクト内の一つまたは複数のデータソースに対してプロファイル、予測、およびトラフィックライトシステムのデータを削除するために使用します。このコマンドはデータライフサイクル管理に不可欠で、古いまたは不要なデータをクリアして整理された効率的なデータ環境を維持するのに役立ちます。

#### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: データを削除するプロジェクト名（必須）。この引数にキーワード `all-projects` を指定すると、***digna*** は既存のすべてのプロジェクトを順に処理してこのコマンドを適用します。
- **FROM_DATE**: データ削除の開始日時。受け入れ可能な形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: データ削除の終了日時。FROM_DATE と同じ形式を使用（必須）。
  
#### Options
  
- `--table-name`, `-tn`: クリーンアップ操作をプロジェクト内の特定テーブルに限定します。
- `--table-filter`, `-tf`: テーブル名に指定した部分文字列を含むテーブルに対してクリーンアップを行うようフィルタします。
- `--timing`, `-tm`: 完了後にクリーンアップ処理の所要時間を表示します。
- `--help`: clean-up コマンドのヘルプ情報を表示して終了します。
  
#### Example
  
ProjectA プロジェクトから 2023年1月1日 から 2023年6月30日 までのデータを削除するには:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
特定のテーブル `Table1` のデータのみを削除するには:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
このコマンドはデータストレージの管理や、リポジトリに関連性のある情報だけが残るようにするのに役立ちます。

### remove-orphans
  
`remove-orphans` コマンドは、***digna*** リポジトリ内のハウスキーピング用コマンドです。  
ユーザーがプロジェクトやデータソースを削除した際に、プロファイルや予測がリポジトリ内に残ることがあります。このコマンドはそのような孤立した（オーファン）行をリポジトリから削除します。
  
#### Command Usage
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects` コマンドは、***digna*** システム内で利用可能な全プロジェクトの一覧を表示するために使用します。
  
#### Command Usage
  
```bash
dignacli list-projects
```

このコマンドは複数プロジェクトを管理する管理者やユーザーにとって特に有用で、***digna*** リポジトリ内の利用可能なプロジェクトの概要を素早く把握できます。

### list-ds

`list-ds` コマンドは、指定したプロジェクト内で利用可能な全データソースの一覧を表示するために使用します。これは解析や管理のために利用可能なデータ資産を把握するのに役立ちます。

#### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME**: データソースを一覧表示するプロジェクト名（必須）。
  
#### Example
  
ProjectA の全データソースを一覧表示するには:
  
```bash
dignacli list-ds ProjectA
```
  
このコマンドはプロジェクト内で利用可能なデータソースの概要を提供し、データ管理をより効率的に行うのに役立ちます。


### inspect

`inspect` コマンドは、指定したプロジェクト内の一つまたは複数のデータソースに対してプロファイル、予測、およびトラフィックライトシステムのデータを作成するために使用します。このコマンドは定義された期間にわたるデータの解析と監視に役立ちます。検査完了後、計算されたトラフィックライトシステムの値が返されます:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: 検査対象のプロジェクト名（必須）。この引数にキーワード `all-projects` を指定すると、***digna*** は既存のすべてのプロジェクトを順に処理してこのコマンドを適用します。
- **FROM_DATE**: 検査の開始日時。受け入れ可能な形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: 検査の終了日時。FROM_DATE と同じ形式を使用（必須）。
  
#### Options

- `--table-name`, `-tn`: プロジェクト内の特定テーブルに検査を限定します。
- `--table-filter`, `-tf`: テーブル名に指定した部分文字列を含むテーブルのみを検査します。
- `--enable_notification`, `-en`: アラートが発生した場合に通知を送信することを有効にします。
- `--bypass-backend`, `-bb`: バックエンドをバイパスして CLI から直接検査を実行します（テスト目的のみ！）。

  
#### Example
  
ProjectA の 2024年1月1日 から 2024年1月31日 までのデータを検査するには:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
特定のテーブルのみを検査し、予測の再計算を強制するには:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
このコマンドは、更新されたプロファイルと予測を生成し、データの整合性を監視し、指定したプロジェクト期間内でのアラートシステムを管理するのに便利です。

### inspect-async

`inspect-async` コマンドは、指定したプロジェクト内の一つまたは複数のデータソースに対してプロファイル、予測、およびトラフィックライトシステムのデータを作成するために使用します。このコマンドは定義された期間にわたるデータの解析と監視に役立ちます。`inspect-async` は検査の完了を待たずに戻り、送信された検査リクエストの request id を返します。検査プロセスの進行状況を照会するには `inspect-status` コマンドを使用してください。

#### Command Usage

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: 検査対象のプロジェクト名（必須）。この引数にキーワード `all-projects` を指定すると、***digna*** は既存のすべてのプロジェクトを順に処理してこのコマンドを適用します。
- **FROM_DATE**: 検査の開始日時。受け入れ可能な形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: 検査の終了日時。FROM_DATE と同じ形式を使用（必須）。
  
#### Options

- `--table-name`, `-tn`: プロジェクト内の特定テーブルに検査を限定します。
- `--table-filter`, `-tf`: テーブル名に指定した部分文字列を含むテーブルのみを検査します。
- `--enable_notification`, `-en`: アラートが発生した場合に通知を送信することを有効にします。

  
#### Example
  
ProjectA の 2024年1月1日 から 2024年1月31日 までのデータを非同期で検査するには:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  

### inspect-status

`inspect-status` コマンドは、非同期検査の進捗を request ID に基づいて確認するために使用します。

#### Command Usage

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Arguments
  
- **REQUEST_ID**: `inspect-async` コマンドが返すリクエスト ID 
  
#### Example
  
リクエスト ID 12345 の検査進捗を確認するには:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel` コマンドは、リクエスト ID に基づいて検査をキャンセルするため、または現在のすべてのリクエストをキャンセルするために使用します。

#### Command Usage

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Arguments
  
- **REQUEST_ID**: `inspect-async` コマンドが返すリクエスト ID 
  
#### Example
  
リクエスト ID 12345 の検査をキャンセルするには:
  
```bash
dignacli inspect-cancel 12345
```

現在実行中または保留中のすべてのリクエストをキャンセルするには:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds` コマンドは、***digna*** リポジトリからデータソースのエクスポートを作成するために使用します。デフォルトでは、指定したプロジェクトからすべてのデータソースがエクスポートされます。

#### Command Usage
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Arguments
- **PROJECT_NAME**: データソースをエクスポートするプロジェクト名。

#### Options

- `--table_name`, `-tn`: プロジェクトから特定のデータソースをエクスポートします。
- `--exportfile`, `-ef`: エクスポートファイル名を指定します。
    
#### Example
  
ProjectA のすべてのデータソースをエクスポートするには:
  
```bash
dignacli export-ds ProjectA
```
  
このコマンドは `ProjectA` のすべてのデータソースを JSON ドキュメントとしてエクスポートし、別のプロジェクトや ***digna*** リポジトリにインポートすることができます。


### import-ds

`import-ds` コマンドは、データソースをターゲットプロジェクトにインポートし、インポートレポートを作成するために使用します。

#### Command Usage
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: データソースをインポートするプロジェクト名。
- **EXPORT_FILE**: インポートするデータソースのエクスポートファイル名。

#### Options

- `--output-file`, `-o`: インポートレポートを保存するファイル（指定しない場合はターミナルに表形式で出力）。
- `--output-format`, `-f`: インポートレポートの保存形式（json, csv）。
    
#### Example
  
エクスポートファイル `my_export.json` の全データソースを `ProjectB` にインポートするには:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
インポート後、このコマンドはインポートされたオブジェクトとスキップされたオブジェクトのレポートも表示します。`ProjectB` には新規のデータソースのみがインポートされます。どのオブジェクトがインポートされ、どれがスキップされるかを確認するには `plan-import-ds` コマンドを使用できます。

### plan-import-ds

`plan-import-ds` コマンドは、データソースをターゲットプロジェクトにインポートする前に、どのオブジェクトがインポートされ、どれがスキップされるかの計画（プラン）を表示するために使用します。

#### Command Usage
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: データソースをインポートする予定のプロジェクト名。
- **EXPORT_FILE**: インポート前に分析するデータソースのエクスポートファイル名。

#### Options

- `--output-file`, `-o`: インポートレポートを保存するファイル（指定しない場合はターミナルに表形式で出力）。
- `--output-format`, `-f`: インポートレポートの保存形式（json, csv）。
    
#### Example
  
エクスポートファイル `my_export.json` を `ProjectB` にインポートした場合に、どのデータソースがインポートされ、どれがスキップされるかを確認するには:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
このコマンドは、インポートされるオブジェクトとスキップされるオブジェクトのインポートプランのみを表示します。
---
title: digna CLI リファレンス 2025.04 – コマンドと例 | digna ドキュメント
description: digna CLI リリース 2025.04 の完全リファレンス。add-user、check-repo-connection、upgrade-repo、inspect などのコマンドでユーザー、リポジトリ、データを管理する方法を解説します。
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

このページでは、***digna*** CLI リリース **2025.04** で利用可能な全コマンドを、使用例やオプションとともにドキュメント化しています。

---

## CLI 基本

---

## `help` オプションの使い方

`--help` オプションは、利用可能なコマンドとその使い方に関する情報を提供します。主に 2 通りの使い方があります:

1. **一般ヘルプの表示:**
   
   キーワード ***digna*** の直後に --help を指定します。  
   ```bash
   dignacli --help
   ```

2. **特定コマンドのヘルプ取得:**  
  
   特定のコマンドに関する詳細情報を得るには、そのコマンドに `--help` を付けて実行します。  
   例: `add-user` コマンドのヘルプを表示するには次を実行します:
    ```bash
    dignacli add-user --help
    ```

    ### 出力:
      
    - **コマンドの説明:** コマンドが何を行うかの詳細な説明。  
    - **構文:** 必須およびオプションの引数を含む正確な構文。  
    - **オプション:** コマンド固有のオプションとその説明。  
    - **例:** コマンドを効果的に実行するための使用例。

  
## `check-repo-connection` コマンドの使い方

check-repo-connection コマンドは、指定した ***digna*** リポジトリへの接続とアクセスをテストするためのユーティリティです。このコマンドにより、CLI がリポジトリと対話できるかを確認できます。
      
#### コマンド使用法
```bash
dignacli check-repo-connection
```

正常に実行されると、接続が確認された旨とともにリポジトリの詳細（リポジトリのバージョン、ホスト、データベース、スキーマ）が出力されます。  
  
リポジトリ接続が成功しない場合は、設定が正しいかを確認するために config.toml ファイルをチェックしてください。

## `version` コマンドの使い方

インストールされている *dignacli* のバージョンを確認するには、`--version` オプションを使用します。  
  
#### コマンド使用法
```bash
dignacli --version
```
  
#### 出力例
```bash
dignacli version 2025.04
```

## ロギングオプションの使い方
  
デフォルトでは、***digna*** コマンドのコンソール出力は最小限に抑えられています。ほとんどのコマンドは追加情報を出力するオプションを提供しており、次のオプションが利用可能です:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
「verbose」と「debug」は詳細レベルを定義し、「logfile」スイッチは出力をコンソールではなくファイルにリダイレクトするために使用します。

## ユーザー管理

### `add-user` コマンドの使い方
  
add-user コマンドは、***digna*** CLI で新しいユーザーを ***digna*** システムに追加するために使用します。
  
#### コマンド使用法
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### 引数

- **USER_NAME**: 新規ユーザーのユーザー名（必須）。
- **USER_FULL_NAME**: 新規ユーザーのフルネーム（必須）。
- **USER_PASSWORD**: 新規ユーザーのパスワード（必須）。

#### オプション

- `--is_superuser`, `-su`: 新規ユーザーを管理者として指定するフラグ。
- `--valid_until`, `-vu`: ユーザーアカウントの有効期限を `YYYY-MM-DD HH:MI:SS` 形式で設定します。未設定の場合は有効期限なしとなります。

#### 例

ユーザー名 `jdoe`、フルネーム `John Doe`、パスワード `password123` のユーザーを追加するには:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
アカウントの有効期限を設定して新規ユーザーを追加する例:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### `delete-user` コマンドの使い方
  
`delete-user` コマンドは、***digna*** CLI で既存ユーザーを ***digna*** システムから削除するために使用します。
  
#### コマンド使用法
```bash
dignacli delete-user USER_NAME
```
  
##### 引数
- **USER_NAME**: 削除するユーザーのユーザー名（必須）。この引数のみが必要です。

#### 例
```bash
dignacli delete-user jdoe
```
  
このコマンドを実行すると、ユーザー `jdoe` は ***digna*** システムから削除され、アクセス権が取り消され、リポジトリから関連するデータと権限が削除されます。

### `modify-user` コマンドの使い方

`modify-user` コマンドは、***digna*** CLI で既存ユーザーの詳細を更新するために使用します。

#### コマンド使用法
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### 引数
  
- **USER_NAME**: 変更対象のユーザー名（必須）。
- **USER_FULL_NAME**: ユーザーの新しいフルネーム（必須）。
  
#### オプション  
  
- `--is_superuser`, `-su`: ユーザーをスーパーユーザーとして設定し、権限を昇格します。このフラグは値を必要としません。  
- `--valid_until`, `-vu`: ユーザーアカウントの有効期限を YYYY-MM-DD HH:MI:SS 形式で設定します。未指定の場合、アカウントは無期限で有効です。  
  
#### 例
  
ユーザー `jdoe` のフルネームを “Johnathan Doe” に変更し、スーパーユーザーに設定する例:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### `modify-user-pwd` コマンドの使い方
  
`modify-user-pwd` コマンドは、***digna*** CLI で既存ユーザーのパスワードを変更するために使用します。
  
#### コマンド使用法
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### 引数
  
- **USER_NAME**: パスワードを変更するユーザーのユーザー名（必須）。
- **USER_PWD**: 新しいパスワード（必須）。
  
#### 例
  
ユーザー `jdoe` のパスワードを `newpassword123` に変更するには:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### `list-users` コマンドの使い方

`list-users` コマンドは、***digna*** CLI で登録されているすべてのユーザーの一覧を表示します。

#### コマンド使用法

```bash
dignacli list-users
```

このコマンドを実行すると、***digna*** リポジトリに接続して全ユーザーを一覧表示し、ID、ユーザー名、フルネーム、スーパーユーザー判定、有効期限タイムスタンプなどが表示されます。

## リポジトリ管理

### `upgrade-repo` コマンドの使い方
  
`upgrade-repo` コマンドは、***digna*** リポジトリのアップグレードまたは初期化を行うために使用します。このコマンドは、更新を適用したりリポジトリのインフラを初めてセットアップする際に必須です。
  
#### コマンド使用法

```bash
dignacli upgrade-repo [options]
```
  
#### オプション
  
- `--simulation-mode`, `-s`: 有効にするとシミュレーションモードでコマンドを実行し、実行される SQL 文を表示しますが実際には適用しません。変更をプレビューするのに便利です。  

  
#### 例
  
***digna*** リポジトリをアップグレードするには、オプションなしでコマンドを実行します:
  
```bash
dignacli upgrade-repo
```  
シミュレーションモードで実行して、SQL 文を確認するには:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
このコマンドは、データベーススキーマやその他のリポジトリ構成要素がソフトウェアの最新バージョンと整合していることを確保するために重要です。

### `encrypt` コマンドの使い方
  
`encrypt` コマンドは、パスワードを暗号化するために使用します。
  
#### コマンド使用法
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### 引数
- **PASSWORD**: 暗号化するパスワード（必須）。
  
#### 例
  
パスワードを暗号化するには、パスワードを引数として指定します。  
例: `mypassword123` を暗号化するには:
```bash
dignacli encrypt mypassword123
```
このコマンドは、指定したパスワードの暗号化結果を出力します。パスワード引数が指定されない場合は、引数が不足している旨のエラーが表示されます。

## `generate-key` コマンドの使い方
  
`generate-key` コマンドは、Fernet キーを生成するために使用します。これは、***digna*** リポジトリに保存されるパスワードを保護するために必要です。
  
#### コマンド使用法
```bash
dignacli generate-key
```
  
## データ管理

## `clean-up` コマンドの使い方

`clean-up` コマンドは、指定したプロジェクト内の一つまたは複数のデータソースに対して、プロファイル、予測、および Traffic Light System データを削除するために使用します。このコマンドはデータライフサイクル管理に不可欠で、古くなったり不要なデータを削除して整然とした効率的なデータ環境を維持するのに役立ちます。

#### コマンド使用法

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 引数
  
- **PROJECT_NAME**: データを削除するプロジェクト名（必須）。この引数にキーワード all-projects を使用すると、既存プロジェクトすべてに対してこのコマンドを繰り返します。
- **FROM_DATE**: データ削除の開始日時。許容フォーマットは %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: データ削除の終了日時。FROM_DATE と同じフォーマットを使用（必須）。
  
#### オプション
  
- `--table-name`, `-tn`: クリーンアップをプロジェクト内の特定テーブルに限定します。
- `--table-filter`, `-tf`: テーブル名に指定した部分文字列を含むテーブルに限定します。
- `--timing`, `-tm`: 処理完了後にクリーンアップ処理の所要時間を表示します。
- `--help`: clean-up コマンドのヘルプを表示して終了します。
  
#### 例
  
ProjectA プロジェクトの 2023-01-01 から 2023-06-30 の間のデータを削除するには:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
特定のテーブル `Table1` のみからデータを削除するには:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
このコマンドは、データストレージの管理やリポジトリに保存される情報を関連性のあるものだけに保つのに役立ちます。

## `list-projects` コマンドの使い方
  
`list-projects` コマンドは、***digna*** システム内の利用可能なプロジェクトの一覧を表示します。
  
#### コマンド使用法
  
```bash
dignacli list-projects
```

このコマンドは、複数のプロジェクトを管理する管理者やユーザーにとって便利で、***digna*** リポジトリ内の利用可能なプロジェクトの概要を素早く把握できます。

## `list-ds` コマンドの使い方

`list-ds` コマンドは、指定したプロジェクト内の利用可能なすべてのデータソースを表示します。このコマンドは、分析や管理の対象となるデータ資産を把握するのに役立ちます。

#### コマンド使用法
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### 引数
- **PROJECT_NAME**: データソースを一覧表示する対象のプロジェクト名（必須）。
  
#### 例
  
ProjectA プロジェクト内のすべてのデータソースを一覧表示するには:
  
```bash
dignacli list-ds ProjectA
```
  
このコマンドにより、プロジェクト内で利用可能なデータソースの概要が得られ、データの管理や探索が容易になります。


## `inspect` コマンドの使い方

`inspect` コマンドは、指定したプロジェクト内の一つまたは複数のデータソースについて、プロファイル、予測、および Traffic Light System データを作成するために使用します。このコマンドは、定義した期間にわたるデータの解析と監視に役立ちます。

#### コマンド使用法

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 引数
  
- **PROJECT_NAME**: データを検査する対象のプロジェクト名（必須）。この引数にキーワード all-projects を使用すると、既存プロジェクトすべてに対してコマンドを繰り返します。
- **FROM_DATE**: データ検査の開始日時。許容フォーマットは %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: データ検査の終了日時。FROM_DATE と同じフォーマットを使用（必須）。
  
#### オプション

- `--table-name`, `-tn`: 検査をプロジェクト内の特定テーブルに限定します。
- `--table-filter`, `-tf`: 名前に指定した部分文字列を含むテーブルのみを検査します。
- `--do-profile`: プロファイルの再収集を実行します。デフォルトは do-profile です。
- `--no-do-profile`: プロファイルの再収集を行いません。
- `--do-prediction`: 予測の再計算を実行します。デフォルトは do-prediction です。
- `--no-do-prediction`: 予測の再計算を行いません。
- `--do-alert-status`: アラートステータスの再計算を実行します。デフォルトは do-alert-status です。
- `--no-do-alert-status`: アラートステータスの再計算を行いません。
- `--iterative`: 期間を日次イテレーションで検査します。デフォルトは iterative です。
- `--no-iterative`: 期間全体を一度に検査します。
- `--enable_notification`, `-en`: アラート発生時に通知送信を有効にします。
- `--timing`, `-tm`: 検査処理完了後に所要時間を表示します。
  
#### 例
  
ProjectA の 2024-01-01 から 2024-01-31 のデータを検査するには:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
特定のテーブルのみを検査し、予測の再計算を強制する例:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
このコマンドは、更新されたプロファイルと予測の生成、データ整合性の監視、および指定期間内のアラートシステム管理に有用です。

## `tls-status` コマンドの使い方

`tls-status` コマンドは、指定した日付におけるプロジェクト内の特定テーブルについて Traffic Light System (TLS) のステータスを照会するために使用します。Traffic Light System はデータの健全性や品質に関する洞察を提供し、注意が必要な問題やアラートを示します。
  
#### コマンド使用法
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### 引数
  
- **PROJECT_NAME**: TLS ステータスを照会する対象のプロジェクト名（必須）。
- **TABLE_NAME**: TLS ステータスを取得する特定のテーブル名（必須）。
- **DATE**: TLS ステータスを照会する日付。通常は %Y-%m-%d 形式（必須）。
  
#### 例
  
ProjectA プロジェクトの `UserData` テーブルについて、2024-07-01 の TLS ステータスを確認するには:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

このコマンドは、事前定義された基準に基づく明確で実行可能なステータスレポートを提供し、データ品質の監視と維持に役立ちます。

## `inspect-async` コマンドの使い方

`inspect-async` コマンドは、バックエンドに対して非同期に指定プロジェクトの一つまたは複数のデータソースの検査を実行するよう指示します。project_name に all-projects を指定すると、利用可能なすべてのプロジェクトに対して検査を繰り返します。実行後、検査の進捗を追跡するために使用できるリクエスト ID を返します。

#### コマンド使用法

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 引数
  
- **PROJECT_NAME**: データを検査する対象のプロジェクト名（必須）。この引数にキーワード all-projects を使用すると、既存プロジェクトすべてに対してコマンドを繰り返します。
- **FROM_DATE**: データ検査の開始日時。許容フォーマットは %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: データ検査の終了日時。FROM_DATE と同じフォーマットを使用（必須）。
  
#### オプション

- `--table-name`, `-tn`: 検査をプロジェクト内の特定テーブルに限定します。
- `--table-filter`, `-tf`: 名前に指定した部分文字列を含むテーブルのみを検査します。

  
#### 例
  
ProjectA の 2024-01-01 から 2024-01-31 のデータを非同期検査するには:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## `inspect-status` コマンドの使い方

`inspect-status` コマンドは、inspect-async コマンドによって返されたリクエスト ID を基に、非同期検査の進捗を確認するために使用します。

#### コマンド使用法

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### 引数
  
- **REQUEST_ID**: `inspect-async` コマンドが返したリクエスト ID 
  
#### オプション

- `--report_level`, `-rl`: レポートレベルを設定します: 'task' または 'step' [デフォルト: task]
  
#### 例
  
リクエスト ID 12345 の検査進捗を詳細な step レベルで確認するには:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## `export-ds` コマンドの使い方

`export-ds` コマンドは、***digna*** リポジトリからデータソースのエクスポートを作成するために使用します。デフォルトでは、指定したプロジェクトのすべてのデータソースがエクスポートされます。

#### コマンド使用法
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### 引数
- **PROJECT_NAME**: データソースをエクスポートする対象のプロジェクト名。

#### オプション

- `--table_name`, `-tn`: プロジェクト内の特定のデータソースをエクスポートします。
- `--exportfile`, `-ef`: エクスポートファイル名を指定します。
    
#### 例
  
ProjectA のすべてのデータソースをエクスポートするには:
  
```bash
dignacli export-ds ProjectA
```
  
このコマンドは、ProjectA のデータソースを JSON ドキュメントとしてエクスポートし、別のプロジェクトや ***digna*** リポジトリにインポートできます。


## `import-ds` コマンドの使い方

`import-ds` コマンドは、データソースをターゲットプロジェクトにインポートし、インポートレポートを作成するために使用します。

#### コマンド使用法
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### 引数
- **PROJECT_NAME**: データソースをインポートする対象のプロジェクト名。
- **EXPORT_FILE**: インポートするデータソースのエクスポートファイル名。

#### オプション

- `--output-file`, `-o`: インポートレポートを保存するファイル（指定しない場合はターミナルに表形式で表示）。
- `--output-format`, `-f`: インポートレポートの保存形式（json, csv）。
    
#### 例
  
エクスポートファイル `my_export.json` のすべてのデータソースを `ProjectB` にインポートするには:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
インポート後、このコマンドはインポートされたオブジェクトとスキップされたオブジェクトのレポートも表示します。`ProjectB` には新規のデータソースのみがインポートされます。どのオブジェクトがインポートされ、どれがスキップされるかを事前に確認するには、`plan-import-ds` コマンドを使用してください。

## `plan-import-ds` コマンドの使い方

`plan-import-ds` コマンドは、ターゲットプロジェクトにデータソースをインポートする前に、どのオブジェクトがインポートされるかを解析してインポートプランを作成するために使用します。

#### コマンド使用法
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### 引数
- **PROJECT_NAME**: データソースがインポートされる想定のプロジェクト名。
- **EXPORT_FILE**: インポート前に解析するデータソースのエクスポートファイル名。

#### オプション

- `--output-file`, `-o`: インポートプランのレポートを保存するファイル（指定しない場合はターミナルに表形式で表示）。
- `--output-format`, `-f`: インポートプランの保存形式（json, csv）。
    
#### 例
  
エクスポートファイル `my_export.json` を `ProjectB` にインポートした場合に、どのデータソースがインポートされ、どれがスキップされるかを確認するには:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
このコマンドは、インポートされるオブジェクトとスキップされるオブジェクトのインポートプランのみを表示します。
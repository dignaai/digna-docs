# digna CLI Reference 2026.01
**2026-01-15**

このページでは、***digna*** CLI リリース **2026.01** で利用可能な全コマンドを、使用例やオプションを含めて文書化しています。

---

## CLI Basics

---

### help
`--help` オプションは、利用可能なコマンドとその使い方に関する情報を提供します。使い方は主に2通りあります。

1. **一般的なヘルプを表示する:**
   
    キーワード ***digna*** の直後に `--help` を付けて使用します。  
   ```bash
   dignacli --help
   ```

2. **特定のコマンドのヘルプを取得する:**  
  
    特定のコマンドに関する詳細情報を得るには、そのコマンドに `--help` を付けます。  
    例えば、`add-user` コマンドのヘルプを取得するには次のように実行します:
     ```bash
     dignacli add-user --help
     ```

     ### 出力:
      
     - **コマンドの説明:** コマンドが何を行うかの詳細説明。  
     - **構文:** 必須およびオプションの引数を含む正確な構文。  
     - **オプション:** コマンド固有のオプションとその説明。  
     - **例:** コマンドを効果的に実行するための例。

### check-config

`check-config` コマンドは、***digna*** CLI 内のユーティリティで、***digna*** の設定をテストするためのコマンドです。このコマンドは、***digna*** コンポーネントが config.toml 内の必要な設定要素を見つけられるかを確認します。

#### オプション

- `--configpath`, `-cp`: 設定ファイルまたは設定を含むディレクトリ。省略した場合は ../config.toml が使用されます。
      
#### コマンド使用例
```bash
dignacli check-config
```

正常に実行されると、設定の完備性を確認するメッセージが出力されます。  
  
設定が不完全な場合、足りない設定要素が一覧表示されます。

  
### check-repo-connection

`check-repo-connection` コマンドは、指定した ***digna*** リポジトリへの接続性とアクセスをテストするためのユーティリティです。CLI がリポジトリと正常にやり取りできるかを確認します。
      
#### コマンド使用例
```bash
dignacli check-repo-connection
```

正常に実行されると、接続確認とともにリポジトリの詳細（リポジトリのバージョン、ホスト、データベース、スキーマ）が出力されます。  
  
リポジトリ接続が成功しない場合は、config.toml ファイルの設定が正しいか確認してください。


### version

インストールされている *dignacli* のバージョンを確認するには `--version` オプションを使用します。  
  
#### コマンド使用例
```bash
dignacli --version
```
  
#### 例の出力
```bash
dignacli version 2026.01
```

### ロギングオプション
  
既定では、***digna*** コマンドのコンソール出力は最小限に抑えられています。ほとんどのコマンドでは、以下のオプションを使用して追加情報を出力することができます。  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” と “debug” は詳細レベルを定義し、`--logfile` スイッチは出力をコンソールではなくファイルにストリームすることを可能にします。

## ユーザー管理

### add-user
  
`add-user` コマンドは、***digna*** システムに新しいユーザーを追加するためのコマンドです。
  
#### コマンド使用例
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### 引数

- **USER_NAME**: 新しいユーザーのユーザー名（必須）。
- **USER_FULL_NAME**: 新しいユーザーのフルネーム（必須）。
- **USER_PASSWORD**: 新しいユーザーのパスワード（必須）。

#### オプション

- `--is_superuser`, `-su`: 新しいユーザーを管理者として指定するフラグ。
- `--valid_until`, `-vu`: アカウントの有効期限を `YYYY-MM-DD HH:MI:SS` 形式で設定します。未指定の場合は有効期限なしとなります。

#### 例

ユーザー名 `jdoe`、フルネーム `John Doe`、パスワード `password123` で新しいユーザーを追加するには:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
アカウントの有効期限を設定して新しいユーザーを追加する例:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
`delete-user` コマンドは、***digna*** システムから既存のユーザーを削除するためのコマンドです。
  
#### コマンド使用例
```bash
dignacli delete-user USER_NAME
```
  
#### 引数
- **USER_NAME**: 削除するユーザーのユーザー名（必須）。このコマンドで必要となる唯一の引数です。

#### 例
```bash
dignacli delete-user jdoe
```
  
このコマンドを実行すると、ユーザー `jdoe` は ***digna*** システムから削除され、リポジトリ内の関連データや権限が取り消されます。

### modify-user

`modify-user` コマンドは、***digna*** システム内の既存ユーザーの詳細を更新するためのコマンドです。

#### コマンド使用例
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### 引数
  
- **USER_NAME**: 更新対象のユーザー名（必須）。
- **USER_FULL_NAME**: ユーザーの新しいフルネーム（必須）。
  
#### オプション  
  
- `--is_superuser`, `-su`: ユーザーをスーパーユーザーに設定し、昇格した権限を付与します。このフラグは値を必要としません。  
- `--valid_until`, `-vu`: アカウントの有効期限を `YYYY-MM-DD HH:MI:SS` 形式で設定します。指定しない場合、アカウントは無期限で有効です。  
  
#### 例
  
ユーザー `jdoe` のフルネームを “Johnathan Doe” に変更し、スーパーユーザーに設定する例:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd` コマンドは、***digna*** システム内の既存ユーザーのパスワードを変更するためのコマンドです。
  
#### コマンド使用例
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### 引数
  
- **USER_NAME**: パスワードを変更するユーザーのユーザー名（必須）。
- **USER_PWD**: 新しいパスワード（必須）。
  
#### 例
  
ユーザー `jdoe` のパスワードを `newpassword123` に変更するには:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users` コマンドは、***digna*** システムに登録されている全ユーザーの一覧を表示します。

#### コマンド使用例

```bash
dignacli list-users
```

このコマンドを実行すると、***digna*** リポジトリに接続して全ユーザーを一覧表示し、ID、ユーザー名、フルネーム、スーパーユーザーかどうか、および有効期限のタイムスタンプを表示します。

## リポジトリ管理

### upgrade-repo
  
`upgrade-repo` コマンドは、***digna*** リポジトリをアップグレードまたは初期化するためのコマンドです。アップデートの適用やリポジトリの初期セットアップ時に必要になります。
  
#### コマンド使用例

```bash
dignacli upgrade-repo [options]
```
  
#### オプション
  
- `--simulation-mode`, `-s`: 有効にするとシミュレーションモードで実行され、実際には SQL を実行せずに実行されるであろう SQL 文を表示します。変更を適用せずにプレビューしたい場合に便利です。  

  
#### 例
  
***digna*** リポジトリをアップグレードするにはオプションなしで実行できます:
  
```bash
dignacli upgrade-repo
```  
シミュレーションモードでアップグレードを実行して（SQL 文を確認する場合）:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
このコマンドは、データベーススキーマやその他のリポジトリコンポーネントがソフトウェアの最新バージョンと整合していることを保証するために重要です。

### encrypt
  
`encrypt` コマンドは、パスワードを暗号化するためのコマンドです。
  
#### コマンド使用例
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### 引数
- **PASSWORD**: 暗号化するパスワード（必須）。
  
#### 例
  
パスワードを暗号化するには、パスワードを引数として渡します。  
例えば、`mypassword123` を暗号化するには次のように実行します:
```bash
dignacli encrypt mypassword123
```
このコマンドは、渡されたパスワードの暗号化されたバージョンを出力します。パスワード引数が指定されていない場合、CLI は欠落した引数に関するエラーを表示します。

### generate-key
  
`generate-key` コマンドは、Fernet キーを生成するためのコマンドで、***digna*** リポジトリに保存されるパスワードを保護するために必要です。
  
#### コマンド使用例
```bash
dignacli generate-key
```
  
## データ管理

### clean-up

`clean-up` コマンドは、指定したプロジェクト内の1つ以上のデータソースに対してプロファイル、予測、およびトラフィックライトシステムのデータを削除するためのコマンドです。古いまたは不要なデータをクリアしてデータライフサイクルを管理し、整理された効率的なデータ環境を維持するのに役立ちます。

#### コマンド使用例

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 引数
  
- **PROJECT_NAME**: データを削除するプロジェクト名（必須）。この引数に `all-projects` を指定すると、既存のすべてのプロジェクトに対してこのコマンドを適用します。
- **FROM_DATE**: 削除対象の開始日時。許容形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: 削除対象の終了日時（FROM_DATE と同じ形式、必須）。
  
#### オプション
  
- `--table-name`, `-tn`: プロジェクト内の特定のテーブルに対してクリーンアップを限定します。
- `--table-filter`, `-tf`: テーブル名に指定した部分文字列を含むテーブルに限定してクリーンアップします。
- `--timing`, `-tm`: 完了後にクリーンアップ処理の所要時間を表示します。
- `--help`: clean-up コマンドのヘルプ情報を表示して終了します。
  
#### 例
  
ProjectA プロジェクトの 2023-01-01 から 2023-06-30 までのデータを削除する例:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
特定のテーブル `Table1` のデータのみを削除する例:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
このコマンドは、データストレージの管理やリポジトリに関連性のある情報のみを保持するために役立ちます。

### remove-orphans
  
`remove-orphans` コマンドは、***digna*** リポジトリのハウスキーピングのために使用されます。  
ユーザーがプロジェクトやデータソースを削除した場合、プロファイルや予測がリポジトリに残ることがあります。このコマンドは、そのような孤立した行（オーファン）をリポジトリから削除します。
  
#### コマンド使用例
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects` コマンドは、***digna*** システム内の利用可能なプロジェクトの一覧を表示するためのコマンドです。
  
#### コマンド使用例
  
```bash
dignacli list-projects
```

このコマンドは複数のプロジェクトを管理する管理者やユーザーに便利で、***digna*** リポジトリ内の利用可能なプロジェクトの概要を素早く提供します。

### list-ds

`list-ds` コマンドは、指定したプロジェクト内の利用可能なデータソースの一覧を表示するためのコマンドです。分析や管理に利用可能なデータ資産を把握するのに役立ちます。

#### コマンド使用例
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### 引数
- **PROJECT_NAME**: データソースを一覧表示するプロジェクト名（必須）。
  
#### 例
  
ProjectA プロジェクト内の全データソースを一覧表示するには:
  
```bash
dignacli list-ds ProjectA
```
  
このコマンドは、プロジェクト内で利用可能なデータソースの概要を提供し、データ管理を効率化します。


### inspect

`inspect` コマンドは、指定したプロジェクト内の1つ以上のデータソースについて、プロファイル、予測、およびトラフィックライトシステムのデータを作成するためのコマンドです。このコマンドは、定義された期間にわたってデータを分析および監視するのに役立ちます。インスペクション完了後、計算されたトラフィックライトシステムの値を返します:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### コマンド使用例

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 引数
  
- **PROJECT_NAME**: インスペクションを行うプロジェクト名（必須）。この引数に `all-projects` を指定すると、既存のすべてのプロジェクトに対してこのコマンドを適用します。
- **FROM_DATE**: インスペクションの開始日時。許容形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: インスペクションの終了日時（FROM_DATE と同じ形式、必須）。
  
#### オプション

- `--table-name`, `-tn`: インスペクションをプロジェクト内の特定のテーブルに限定します。
- `--table-filter`, `-tf`: 指定した部分文字列を含むテーブルのみをインスペクションします。
- `--enable_notification`, `-en`: アラート発生時に通知を送信することを有効にします。
- `--bypass-backend`, `-bb`: バックエンドをバイパスして CLI から直接インスペクションを実行します（テスト目的のみ使用してください！）。

  
#### 例
  
ProjectA の 2024-01-01 から 2024-01-31 までのデータをインスペクションする例:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
特定のテーブルのみをインスペクションし、予測の再計算を強制する例:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
このコマンドは、プロファイルや予測の更新、データ整合性の監視、および指定されたプロジェクト期間内でのアラートシステム管理に役立ちます。

### inspect-async

`inspect-async` コマンドは、指定したプロジェクト内の1つ以上のデータソースについて、プロファイル、予測、およびトラフィックライトシステムのデータを作成するためのコマンドです。このコマンドは、定義された期間にわたってデータを分析および監視するのに役立ちます。`inspect-async` コマンドはインスペクションの完了を待機しない点が特徴で、代わりに送信されたインスペクション要求のリクエスト ID を返します。インスペクションの進捗を照会するには `inspect-status` コマンドを使用してください。

#### コマンド使用例

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 引数
  
- **PROJECT_NAME**: インスペクションを行うプロジェクト名（必須）。この引数に `all-projects` を指定すると、既存のすべてのプロジェクトに対してこのコマンドを適用します。
- **FROM_DATE**: インスペクションの開始日時。許容形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: インスペクションの終了日時（FROM_DATE と同じ形式、必須）。
  
#### オプション

- `--table-name`, `-tn`: インスペクションをプロジェクト内の特定のテーブルに限定します。
- `--table-filter`, `-tf`: 指定した部分文字列を含むテーブルのみをインスペクションします。
- `--enable_notification`, `-en`: アラート発生時に通知を送信することを有効にします。

  
#### 例
  
ProjectA の 2024-01-01 から 2024-01-31 までのデータを非同期でインスペクションする例:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status` コマンドは、非同期インスペクションの進捗をリクエスト ID に基づいて確認するためのコマンドです。

#### コマンド使用例

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### 引数
  
- **REQUEST_ID**: `inspect-async` コマンドが返したリクエスト ID
  
#### 例
  
リクエスト ID 12345 のインスペクション進捗を確認するには:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel` コマンドは、リクエスト ID に基づいてインスペクションをキャンセルするため、または現在のすべてのリクエストをキャンセルするために使用します。

#### コマンド使用例

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### 引数
  
- **REQUEST_ID**: `inspect-async` コマンドが返したリクエスト ID 
  
#### 例
  
リクエスト ID 12345 のインスペクションをキャンセルするには:
  
```bash
dignacli inspect-cancel 12345
```

現在実行中または保留中のすべてのリクエストをキャンセルするには:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds` コマンドは、***digna*** リポジトリからデータソースのエクスポートを作成するためのコマンドです。デフォルトでは、指定したプロジェクト内のすべてのデータソースがエクスポートされます。

#### コマンド使用例
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### 引数
- **PROJECT_NAME**: データソースをエクスポートするプロジェクト名。

#### オプション

- `--table_name`, `-tn`: プロジェクトから特定のデータソースをエクスポートします。
- `--exportfile`, `-ef`: エクスポートのファイル名を指定します。
    
#### 例
  
ProjectA から全データソースをエクスポートするには:
  
```bash
dignacli export-ds ProjectA
```
  
このコマンドは、ProjectA の全データソースを JSON ドキュメントとしてエクスポートし、別のプロジェクトや ***digna*** リポジトリにインポートできます。


### import-ds

`import-ds` コマンドは、データソースをターゲットプロジェクトにインポートし、インポートレポートを作成するためのコマンドです。

#### コマンド使用例
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### 引数
- **PROJECT_NAME**: データソースをインポートするターゲットプロジェクト名。
- **EXPORT_FILE**: インポートするデータソースのエクスポートファイル名。

#### オプション

- `--output-file`, `-o`: インポートレポートを保存するファイル（指定しない場合はターミナルに表形式で出力）。
- `--output-format`, `-f`: インポートレポートの保存形式（json、csv）。
    
#### 例
  
エクスポートファイル `my_export.json` の内容を `ProjectB` にインポートするには:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
インポート後、このコマンドはインポートされたオブジェクトとスキップされたオブジェクトのレポートも表示します。`ProjectB` には新しいデータソースのみがインポートされます。どのオブジェクトがインポートされ、どれがスキップされるかを事前に確認するには、`plan-import-ds` コマンドを使用してください。

### plan-import-ds

`plan-import-ds` コマンドは、データソースをターゲットプロジェクトにインポートする前に、どのオブジェクトがインポートされるかを解析してインポートレポートを作成するためのコマンドです。

#### コマンド使用例
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### 引数
- **PROJECT_NAME**: データソースがインポートされる予定のターゲットプロジェクト名。
- **EXPORT_FILE**: インポート前に解析するデータソースのエクスポートファイル名。

#### オプション

- `--output-file`, `-o`: インポートレポートを保存するファイル（指定しない場合はターミナルに表形式で出力）。
- `--output-format`, `-f`: インポートレポートの保存形式（json、csv）。
    
#### 例
  
エクスポートファイル `my_export.json` を `ProjectB` にインポートした場合に、どのデータソースがインポートされ、どれがスキップされるかを確認するには:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
このコマンドは、インポートされるオブジェクトとスキップされるオブジェクトの計画のみを表示します。
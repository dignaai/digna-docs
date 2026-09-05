# digna CLI リファレンス 2024.12
**2024-12-09**

このページは、***digna*** CLI リリース **2024.12** で利用可能な全コマンドを、使用例やオプションとともにドキュメント化しています。

---


**2024-12-09**


---

## CLI の基本

---

## `--help` オプションの使い方

`--help` オプションは、利用可能なコマンドとその使い方に関する情報を提供します。主に二つの使い方があります。

1. **一般ヘルプの表示:**
   
   一般的なヘルプを表示するには、`dignacli` の直後に `--help` を付けて実行します。
   ```bash
   dignacli --help
   ```

2. **特定コマンドのヘルプを取得:**
   
   特定のコマンドに関する詳細情報を得るには、そのコマンドに `--help` を付けて実行します。
   例えば、`add-user` コマンドのヘルプを表示するには次のようにします。
   ```bash
   dignacli add-user --help
   ```

   ### 出力内容:
   
   - **コマンドの説明:** コマンドが何を行うかの詳細説明。  
   - **構文:** 必須およびオプション引数を含む正確な構文。  
   - **オプション:** コマンド固有のオプション一覧とその説明。  
   - **例:** コマンドの実行方法の例。

  
## `check-repo-connection` コマンドの使い方

`check-repo-connection` コマンドは、***digna*** CLI のユーティリティで、指定した ***digna*** リポジトリへの接続とアクセスをテストするためのコマンドです。CLI がリポジトリと正常にやり取りできるかを確認します。
      
### コマンド使用法
```bash
dignacli check-repo-connection
```

正常に実行されると、接続確認の出力が表示され、リポジトリに関する詳細（リポジトリのバージョン、ホスト、データベース、スキーマなど）が表示されます。  
  
接続に失敗した場合は、config.toml ファイルの設定が正しいかを確認してください。

## `--version` コマンドの使い方

インストールされている *dignacli* のバージョンを確認するには、`--version` オプションを使用します。  
  
### コマンド使用法
```bash
dignacli --version
```
  
### 例（出力）
```bash
dignacli version 2024.12
```

## ロギングオプションの使用

デフォルトでは、***digna*** コマンドのコンソール出力は最小限に抑えられています。多くのコマンドは追加情報を出力するためのオプションを提供しています。主なオプションは以下の通りです。  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
「verbose」と「debug」は詳細レベルを定義し、「logfile」スイッチは出力をコンソールではなくファイルへリダイレクトするために使用します。

# ユーザー管理

## `add-user` コマンドの使い方
  
`add-user` コマンドは、***digna*** CLI で新しいユーザーを ***digna*** システムに追加するために使用します。
  
### コマンド使用法
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### 引数

- **USER_NAME**: 新規ユーザーのユーザー名（必須）。
- **USER_FULL_NAME**: 新規ユーザーのフルネーム（必須）。
- **USER_PASSWORD**: 新規ユーザーのパスワード（必須）。

### オプション

- `--is_superuser`, `-su`: 新規ユーザーを管理者（スーパーユーザー）として指定するフラグ。
- `--valid_until`, `-vu`: アカウントの有効期限を `YYYY-MM-DD HH:MI:SS` 形式で設定します。未指定の場合は有効期限なし。

### 例

ユーザー名 `jdoe`、フルネーム `John Doe`、パスワード `password123` の新規ユーザーを追加するには:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
アカウントの有効期限を設定してユーザーを追加するには:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` コマンドの使い方
  
`delete-user` コマンドは、***digna*** CLI で既存ユーザーを ***digna*** システムから削除するために使用します。
  
### コマンド使用法
```bash
dignacli delete-user USER_NAME
```
  
### 引数
- **USER_NAME**: 削除するユーザーのユーザー名（必須）。このコマンドが必要とする唯一の引数です。

### 例
```bash
dignacli delete-user jdoe
```
  
このコマンドを実行すると、ユーザー `jdoe` は ***digna*** システムから削除され、リポジトリから関連するデータや権限が取り消されます。

## `modify-user` コマンドの使い方

`modify-user` コマンドは、***digna*** CLI で既存ユーザーの情報を更新するために使用します。

### コマンド使用法
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### 引数
  
- **USER_NAME**: 更新するユーザーのユーザー名（必須）。
- **USER_FULL_NAME**: ユーザーの新しいフルネーム（必須）。
  
### オプション  
  
- `--is_superuser`, `-su`: ユーザーをスーパーユーザーに設定し、権限を昇格させます。このフラグは値を必要としません。  
- `--valid_until`, `-vu`: アカウントの有効期限を `YYYY-MM-DD HH:MI:SS` 形式で設定します。未指定の場合、アカウントは無期限となります。  
  
### 例
  
ユーザー `jdoe` のフルネームを “Johnathan Doe” に変更し、スーパーユーザーに設定するには:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` コマンドの使い方
  
`modify-user-pwd` コマンドは、***digna*** CLI で既存ユーザーのパスワードを変更するために使用します。
  
### コマンド使用法
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### 引数
  
- **USER_NAME**: パスワードを変更するユーザーのユーザー名（必須）。
- **USER_PWD**: 新しいパスワード（必須）。
  
### 例
  
ユーザー `jdoe` のパスワードを `newpassword123` に変更するには:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` コマンドの使い方

`list-users` コマンドは、***digna*** CLI で登録されている全ユーザーの一覧を表示します。

### コマンド使用法

```bash
dignacli list-users
```

このコマンドを実行すると、***digna*** リポジトリに接続して全ユーザーを一覧表示し、ID、ユーザー名、フルネーム、スーパーユーザーの有無、有効期限タイムスタンプなどを表示します。

# リポジトリ管理

### `upgrade-repo` コマンドの使い方
  
`upgrade-repo` コマンドは、***digna*** CLI でリポジトリをアップグレードまたは初期化するために使用します。このコマンドは、アップデートを適用したり、リポジトリのインフラを初めてセットアップする際に必要です。
  
### コマンド使用法

```bash
dignacli upgrade-repo [options]
```
  
### オプション
  
- `--simulation-mode`, `-s`: 有効にするとシミュレーションモードで実行され、実際には実行されない SQL 文が表示されます。変更を適用せずにプレビューするのに便利です。  

  
### 例
  
***digna*** リポジトリをアップグレードするには、オプションなしで実行します：
  
```bash
dignacli upgrade-repo
```  
シミュレーションモードでアップグレードを実行して、実行される SQL 文を確認するには：
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
このコマンドは ***digna*** システムの維持に重要で、データベーススキーマやその他のリポジトリコンポーネントがソフトウェアの最新バージョンと一致していることを確認します。

## `encrypt` コマンドの使い方
  
`encrypt` コマンドは、パスワードを暗号化するために ***digna*** CLI で使用します。
  
### コマンド使用法
  
```bash
dignacli encrypt <PASSWORD>
```
    
### 引数
- **PASSWORD**: 暗号化するパスワード（必須）。
  
### 例
  
パスワードを暗号化するには、パスワードを引数として指定します。  
例えば、`mypassword123` を暗号化するには次のように実行します：
```bash
dignacli encrypt mypassword123
```
このコマンドは指定されたパスワードの暗号化結果を出力し、その後セキュアなコンテキストで使用できます。パスワード引数が指定されていない場合、CLI は引数が欠落している旨のエラーを表示します。

## `generate-key` コマンドの使い方
  
`generate-key` コマンドは、Fernet キーを生成するために使用します。これは ***digna*** リポジトリに格納されるパスワードを保護するために必要です。
  
### コマンド使用法
```bash
dignacli generate-key
```
  
# データ管理

## `clean-up` コマンドの使い方

`clean-up` コマンドは、指定したプロジェクト内の一つ以上のデータソースについて、プロファイル、予測、トラフィックライトシステムのデータを削除するために使用します。このコマンドはデータライフサイクル管理に不可欠で、古くなったデータや不要なデータをクリアしてデータ環境を整理・効率化するのに役立ちます。

### コマンド使用法

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### 引数
  
- **PROJECT_NAME**: データを削除する対象のプロジェクト名（必須）。この引数に `all-projects` を指定すると、全プロジェクトを順次処理します。
- **FROM_DATE**: データ削除の開始日時。許容される形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: データ削除の終了日時。FROM_DATE と同じ形式（必須）。
  
### オプション
  
- `--table-name`, `-tn`: クリーンアップ対象をプロジェクト内の特定テーブルに限定します。
- `--table-filter`, `-tf`: テーブル名に指定したサブストリングを含むものに限定してクリーンアップします。
- `--timing`, `-tm`: 処理完了後にクリーンアップ処理の所要時間を表示します。
- `--help`: clean-up コマンドのヘルプ情報を表示して終了します。
  
### 例
  
ProjectA プロジェクトの 2023 年 1 月 1 日から 2023 年 6 月 30 日までのデータを削除するには:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
特定のテーブル `Table1` のみからデータを削除するには:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
このコマンドは、データストレージの管理やリポジトリに関連する情報を関連性のあるものに保つのに役立ちます。

## `inspect` コマンドの使い方

`inspect` コマンドは、指定したプロジェクト内の一つ以上のデータソースについてプロファイル、予測、トラフィックライトシステムのデータを作成するために使用します。このコマンドは、定義した期間内でのデータ解析と監視を支援します。

### コマンド使用法

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### 引数
  
- **PROJECT_NAME**: 検査対象のプロジェクト名（必須）。`all-projects` キーワードを指定すると、全プロジェクトを順次処理します。
- **FROM_DATE**: 検査の開始日時。許容される形式は %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S（必須）。
- **TO_DATE**: 検査の終了日時。FROM_DATE と同じ形式（必須）。
  
### オプション

- `--table-name`, `-tn`: 検査対象をプロジェクト内の特定テーブルに限定します。
- `--table-filter`, `-tf`: テーブル名に指定したサブストリングを含むもののみを検査します。
- `--do-profile`: プロファイルの再収集を行います。デフォルトは do-profile。
- `--no-do-profile`: プロファイルの再収集を行いません。
- `--do-prediction`: 予測の再計算を行います。デフォルトは do-prediction。
- `--no-do-prediction`: 予測の再計算を行いません。
- `--do-alert-status`: アラートステータスの再計算を行います。デフォルトは do-alert-status。
- `--no-do-alert-status`: アラートステータスの再計算を行いません。
- `--iterative`: 日次の反復で期間を検査します。デフォルトは iterative。
- `--no-iterative`: 期間全体を一度に検査します。
- `--timing`, `-tm`: 処理完了後に検査処理の所要時間を表示します。
  
### 例
  
ProjectA のデータを 2024 年 1 月 1 日から 2024 年 1 月 31 日まで検査するには:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
特定のテーブルのみを検査し、予測の再計算を強制するには:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
このコマンドは、更新されたプロファイルや予測の生成、データの整合性監視、指定期間内のアラートシステム管理に役立ちます。

## `tls-status` コマンドの使い方

`tls-status` コマンドは、指定したプロジェクト内の特定テーブルについて、ある日のトラフィックライトシステム（TLS）のステータスを照会するために使用します。トラフィックライトシステムは、データの健全性や品質に関する洞察を提供し、注意が必要な問題やアラートを示します。
  
### コマンド使用法
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### 引数
  
- **PROJECT_NAME**: TLS ステータスを照会するプロジェクト名（必須）。
- **TABLE_NAME**: TLS ステータスを確認する対象のテーブル名（必須）。
- **DATE**: TLS ステータスを照会する日付（通常は %Y-%m-%d 形式）（必須）。
  
### 例
  
ProjectA のテーブル UserData の 2024 年 7 月 1 日の TLS ステータスを確認するには:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

このコマンドは、定義済みの基準に基づく明確で実行可能なステータスレポートを提供し、データ品質の監視と維持を支援します。

## `list-projects` コマンドの使い方
  
`list-projects` コマンドは、***digna*** CLI で利用可能な全プロジェクトの一覧を表示します。
  
### コマンド使用法
  
```bash
dignacli list-projects
```

このコマンドは多数のプロジェクトを管理する管理者やユーザーにとって便利で、***digna*** リポジトリ内の利用可能なプロジェクトの概要を素早く把握できます。

## `list-ds` コマンドの使い方

`list-ds` コマンドは、指定したプロジェクト内で利用可能な全データソースの一覧を表示するために使用します。このコマンドは、分析や管理のために利用可能なデータ資産を把握するのに役立ちます。

### コマンド使用法
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### 引数
- **PROJECT_NAME**: データソース一覧を表示するプロジェクト名（必須）。
  
### 例
  
ProjectA プロジェクト内の全データソースを一覧表示するには:
  
```bash
dignacli list-ds ProjectA
```
  
このコマンドは、プロジェクト内で利用可能なデータソースの概要を提供し、データランドスケープの把握と管理を容易にします。
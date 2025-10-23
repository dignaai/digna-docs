---
title: digna CLI リファレンス 2024.11 – コマンドと例 | digna ドキュメント
description: digna CLI リリース 2024.11 の完全リファレンス。add-user、check-repo-connection、upgrade-repo、inspect、tls-status などのコマンドを使ってユーザー、リポジトリ、データを管理する方法を解説します。
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

このページは、***digna*** CLI リリース **2024.11** で利用可能なコマンドの全セットを、使用例やオプションとともにドキュメント化しています。


---
## CLI の基本

---

## `help` オプションの使い方

`--help` オプションは、利用可能なコマンドとその使い方に関する情報を提供します。主に2つの使い方があります:

1. **一般的なヘルプの表示:**
   
    キーワード ***digna***cl の直後に --help を付けて使用します。  
   ```bash
   dignacli --help

3.  **特定コマンドのヘルプを取得する:**  
  
    特定のコマンドについて詳しい情報が必要な場合は、そのコマンドの末尾に `--help` を付けます。  
    例として、`add-user` コマンドのヘルプを取得するには次を実行します:
     ```bash
     dignacli add-user --help
     ```

     ### 出力:
      
     - **コマンド説明:** コマンドが何を行うかの詳細な説明。  
     - **構文:** 必須およびオプション引数を含む正確な構文。  
     - **オプション:** コマンド固有のオプションとその説明の一覧。  
     - **例:** コマンドを効果的に実行する方法の例。  


## `check-repo-connection` コマンドの使い方

check-repo-connection コマンドは、指定した ***digna*** リポジトリへの接続性とアクセスをテストするための ***digna*** CLI 内のユーティリティです。このコマンドは CLI がリポジトリと対話できることを確認します。
      
### コマンド使用法
```bash
dignacli check-repo-connection
```

正常に実行されると、接続確認とともにリポジトリの詳細（リポジトリのバージョン、ホスト、データベース、スキーマ）が出力されます。  
  
リポジトリ接続が成功しない場合は、config.toml ファイルの設定が正しいか確認してください。

## ‘version’ コマンドの使い方

インストールされている *dignacli* のバージョンを確認するには、--version オプションを使用します。  
  
### コマンド使用法
```bash
dignacli --version
```
  
### 例の出力
```bash
dignacli version 2024.11
```

## ロギングオプションの使用

デフォルトでは、***digna*** コマンドのコンソール出力は最小限に設計されています。多くのコマンドは追加情報を提供するためのオプションを用意しており、以下のオプションで制御できます:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
「verbose」と「debug」は詳細レベルを定義し、「logfile」スイッチは出力をコンソールではなくファイルにストリームすることを可能にします。

# ユーザー管理

## ‘add-user’ コマンドの使い方
  
add-user コマンドは、***digna*** CLI で新しいユーザーを ***digna*** システムに追加するために使用します。
  
### コマンド使用法
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### 引数

- **USER_NAME**: 新しいユーザーのユーザー名（必須）。
- **USER_FULL_NAME**: 新しいユーザーのフルネーム（必須）。
- **USER_PASSWORD**: 新しいユーザーのパスワード（必須）。

### オプション

- `--is_superuser`, `-su`: 新しいユーザーを管理者として指定するフラグ。
- `--valid_until`, `-vu`: アカウントの有効期限を `YYYY-MM-DD HH:MI:SS` 形式で設定します。設定しない場合、アカウントに有効期限はありません。

### 例

ユーザー名 `jdoe`、フルネーム `John Doe`、パスワード `password123` の新規ユーザーを追加するには:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
アカウントの有効期限を設定して新規ユーザーを追加するには:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` コマンドの使い方
  
`delete-user` コマンドは、既存のユーザーを ***digna*** システムから削除するために使用します。
  
### コマンド使用法
```bash
dignacli delete-user USER_NAME
```
  
### 引数
- **USER_NAME**: 削除するユーザーのユーザー名（必須）。このコマンドで必要なのはこの引数のみです。

### 例
```bash
dignacli delete-user jdoe
```
  
このコマンドを実行すると、ユーザー `jdoe` は ***digna*** システムから削除され、アクセス権が取り消され、リポジトリから関連するデータと権限が削除されます。

## `modify-user` コマンドの使い方

`modify-user` コマンドは、既存のユーザーの詳細を ***digna*** システム内で更新するために使用します。

### コマンド使用法
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### 引数
  
- **USER_NAME**: 変更するユーザーのユーザー名（必須）。
- **USER_FULL_NAME**: ユーザーの新しいフルネーム（必須）。
  
### オプション  
  
- `--is_superuser`, `-su`: ユーザーをスーパーユーザーに設定し、昇格した権限を付与します。このフラグは値を必要としません。  
- `--valid_until`, `-vu`: アカウントの有効期限を YYYY-MM-DD HH:MI:SS 形式で設定します。指定しない場合、アカウントは無期限のままです。  
  
### 例
  
ユーザー `jdoe` のフルネームを “Johnathan Doe” に変更し、スーパーユーザーに設定するには:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` コマンドの使い方
  
`modify-user-pwd` コマンドは、既存ユーザーのパスワードを変更するために使用します。
  
### コマンド使用法
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### 引数
  
- **USER_NAME**: パスワードを変更するユーザーのユーザー名（必須）。
- **USER_PWD**: ユーザーの新しいパスワード（必須）。
  
### 例
  
ユーザー `jdoe` のパスワードを `newpassword123` に変更するには:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` コマンドの使い方

`list-users` コマンドは、***digna*** システムに登録されているすべてのユーザーの一覧を表示します。

### コマンド使用法

```bash
dignacli list-users
```

このコマンドを実行すると、***digna*** リポジトリに接続し、ユーザーの ID、ユーザー名、フルネーム、スーパーユーザー状態、有効期限タイムスタンプなどを表示します。

# リポジトリ管理

### `upgrade-repo` コマンドの使い方
  
`upgrade-repo` コマンドは、***digna*** リポジトリをアップグレードまたは初期化するために使用します。このコマンドは、アップデートを適用したり、初回セットアップでリポジトリのインフラを構築する際に重要です。
  
### コマンド使用法

```bash
dignacli upgrade-repo [options]
```
  
### オプション
  
- `--simulation-mode`, `-s`: 有効にするとシミュレーションモードでコマンドを実行し、実行される SQL 文を表示するだけで実際の実行は行いません。変更をプレビューしたい場合に便利です。  

  
### 例
  
***digna*** リポジトリをアップグレードするには、オプションなしでコマンドを実行します:
  
```bash
dignacli upgrade-repo
```  
シミュレーションモードでアップグレードを実行して（SQL 文のみ確認する）場合:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
このコマンドは、データベーススキーマやその他のリポジトリコンポーネントがソフトウェアの最新バージョンに追従していることを保証するため、***digna*** システムの保守に不可欠です。

## `encrypt` コマンドの使い方
  
`encrypt` コマンドは、パスワードを暗号化するために使用します。
  
### コマンド使用法
  
```bash
dignacli encrypt <PASSWORD>
```
    
### 引数
- **PASSWORD**: 暗号化するパスワード（必須）。
  
### 例
  
パスワードを暗号化するには、パスワードを引数として渡します。   
例えば、`mypassword123` を暗号化するには次のように実行します:
```bash
dignacli encrypt mypassword123
```
このコマンドは、指定したパスワードの暗号化されたバージョンを出力します。暗号化されたパスワードは安全な文脈で使用できます。パスワード引数が指定されていない場合、CLI は引数が不足していることを示すエラーを表示します。

## `generate-key` コマンドの使い方
  
`generate-key` コマンドは、Fernet キーを生成するために使用されます。これは ***digna*** リポジトリに保存されるパスワードのセキュリティ確保に必須です。
  
### コマンド使用法
```bash
dignacli generate-key
```
  
# データ管理

## `clean-up` コマンドの使い方

`clean-up` コマンドは、指定したプロジェクト内の1つ以上のデータソースに対してプロファイル、予測、およびトラフィックライトシステムのデータを削除するために使用されます。このコマンドはデータライフサイクル管理に不可欠で、古いまたは不要なデータをクリアして整理された効率的なデータ環境を維持するのに役立ちます。

### コマンド使用法

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### 引数
  
- **PROJECT_NAME**: データを削除するプロジェクト名（必須）。この引数にキーワード all-projects を使用すると、***digna*** は既存のすべてのプロジェクトを反復してこのコマンドを適用します。
- **FROM_DATE**: 削除の開始日時。許容される形式には %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S が含まれます（必須）。
- **TO_DATE**: 削除の終了日時。FROM_DATE と同じ形式に従います（必須）。
  
### オプション
  
- `--table-name`, `-tn`: クリーンアップ操作をプロジェクト内の特定のテーブルに限定します。
- `--table-filter`, `-tf`: テーブル名に指定した部分文字列を含むテーブルにクリーンアップを制限するフィルタ。
- `--timing`, `-tm`: 完了後にクリーンアップ処理の所要時間を表示します。
- `--help`: clean-up コマンドのヘルプ情報を表示して終了します。
  
### 例
  
プロジェクト ProjectA の 2023年1月1日 から 2023年6月30日 までのデータを削除するには:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
特定のテーブル `Table1` のみからデータを削除するには:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
このコマンドはデータストレージの管理と、リポジトリに関連性のある情報だけが保持されるようにするのに役立ちます。

## `inspect` コマンドの使い方

`inspect` コマンドは、指定したプロジェクト内の1つ以上のデータソースに対してプロファイル、予測、およびトラフィックライトシステムのデータを作成するために使用します。このコマンドは、定義された期間にわたってデータを分析および監視するのに役立ちます。

### コマンド使用法

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### 引数
  
- **PROJECT_NAME**: 検査対象のプロジェクト名（必須）。この引数にキーワード all-projects を使用すると、***digna*** は既存のすべてのプロジェクトを反復してこのコマンドを適用します。
- **FROM_DATE**: 検査の開始日時。許容される形式には %Y-%m-%d、%Y-%m-%dT%H:%M:%S、または %Y-%m-%d %H:%M:%S が含まれます（必須）。
- **TO_DATE**: 検査の終了日時。FROM_DATE と同じ形式に従います（必須）。
  
### オプション

- `--table-name`, `-tn`: 検査をプロジェクト内の特定のテーブルに限定します。
- `--table-filter`, `-tf`: 指定した部分文字列を名前に含むテーブルのみを検査するフィルタ。
- `--do-profile`: プロファイルの再収集をトリガーします。デフォルトは do-profile です。
- `--no-do-profile`: プロファイルの再収集を行わないようにします。
- `--do-prediction`: 予測の再計算をトリガーします。デフォルトは do-prediction です。
- `--no-do-prediction`: 予測の再計算を行わないようにします。
- `--do-alert-status`: アラートステータスの再計算をトリガーします。デフォルトは do-alert-status です。
- `--no-do-alert-status`: アラートステータスの再計算を行わないようにします。
- `--timing`, `-tm`: 完了後に検査処理の所要時間を表示します。
  
### 例
  
プロジェクト `ProjectA` の 2024年1月1日 から 2024年1月31日 までのデータを検査するには:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
特定のテーブルのみを検査し、予測の再計算を強制するには:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
このコマンドは、更新されたプロファイルと予測を生成し、データの整合性を監視し、指定したプロジェクト期間内でアラートシステムを管理するのに有用です。

## `tls-status` コマンドの使い方

`tls-status` コマンドは、指定した日付におけるプロジェクト内の特定テーブルに対するトラフィックライトシステム（TLS）のステータスを照会するために使用します。トラフィックライトシステムは、データの健全性と品質についての洞察を提供し、注意を要する問題やアラートを示します。
  
### コマンド使用法
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### 引数
  
- **PROJECT_NAME**: TLS ステータスを照会するプロジェクト名（必須）。
- **TABLE_NAME**: TLS ステータスが必要なプロジェクト内の特定テーブル（必須）。
- **DATE**: TLS ステータスを照会する日付（通常 %Y-%m-%d 形式）（必須）。
  
### 例
  
プロジェクト ProjectA のテーブル UserData に対して、2024年7月1日の TLS ステータスを確認するには:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

このコマンドは、事前定義された基準に基づく明確で実行可能なステータスレポートを提供することにより、ユーザーがデータ品質を監視および維持するのに役立ちます。

## `list-projects` コマンドの使い方
  
`list-projects` コマンドは、***digna*** システム内の利用可能なすべてのプロジェクトの一覧を表示するために使用します。
  
### コマンド使用法
  
```bash
dignacli list-projects
```

このコマンドは、複数のプロジェクトを管理する管理者やユーザーにとって特に便利で、***digna*** リポジトリ内の利用可能なプロジェクトの概要を素早く確認できます。

## `list-ds` コマンドの使い方

`list-ds` コマンドは、指定したプロジェクト内の利用可能なすべてのデータソースの一覧を表示するために使用します。このコマンドは、***digna*** システムで分析や管理に利用可能なデータ資産を把握するのに役立ちます。

### コマンド使用法
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### 引数
- **PROJECT_NAME**: データソースを一覧表示する対象のプロジェクト名（必須）。
  
### 例
  
プロジェクト `ProjectA` にあるすべてのデータソースを一覧表示するには:
  
```bash
dignacli list-ds ProjectA
```
  
このコマンドは、プロジェクト内で利用可能なデータソースの概要を提供し、データのランドスケープをより効率的にナビゲートおよび管理するのに役立ちます。
---
title: データベースを接続する | digna ドキュメント
description: digna の既存プロジェクトにデータベースを接続する手順ガイド。接続の設定、認証情報の入力、安全なアクセスの有効化方法を学びます。
---

# データベースを接続する

このガイドでは、プロジェクトにデータベース接続を追加するための最小限の手順を示します。

## インタラクティブデモ

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="Connect a Database to a Project"
    frameborder="0"
    loading="lazy"
    webkitallowfullscreen
    mozallowfullscreen
    allowfullscreen
    allow="clipboard-write"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;">
  </iframe>
</div>
<!--ARCADE EMBED END-->

---

### 手順

1. **プロジェクトを開く**  
   左のナビゲーションから **Projects** をクリックし、対象のプロジェクトを選択します。

2. **接続を追加する**  
   **Connections** に移動し、**Add Connection** をクリックします。

3. **データベースの種類を選択する**  
   接続したいデータベース（例: PostgreSQL、MySQL、SQL Server、Oracle、Snowflake、Teradata）を選択します。

4. **接続情報を入力する**  
   **Name**, **Host**, **Port**, **Database/Service**, および **Credentials**（ユーザー名／パスワードまたはSSOなど、該当する方法）を入力します。

5. **テストして保存する**  
   **Test** をクリックします。成功したら **Save** をクリックします。接続はプロジェクトの **Connections** に表示されます。
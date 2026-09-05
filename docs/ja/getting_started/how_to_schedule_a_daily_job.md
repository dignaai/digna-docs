---
title: 毎日実行されるジョブの作成方法
description: digna のダッシュボードを使って毎日実行される検査ジョブをスケジュールする方法を学びます。
keywords: digna スケジューリング, データ品質自動化, 毎日ジョブ
image: /assets/logo_square.png
---

# 毎日実行されるジョブをスケジュールする方法

スケジューリングにより、手動で介入することなく検査を自動実行できます。  
このガイドでは、データが継続的に監視されるように、**1日1回**実行されるジョブを作成する方法を学びます。

---

## インタラクティブデモ

インタラクティブチュートリアルに従って、実際の手順を確認してください：  

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/Ra9E19A0QfMpzKqm3Yhu?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a New Data Inspection Job" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## 学べること

- digna ダッシュボードで **Scheduling** セクションにアクセスする方法  
- 新しいスケジュール済みジョブの作成方法  
- **特定の時刻に毎日**実行されるように設定する方法  
- 正しいプロジェクトとデータソースを選択する方法  
- ジョブを有効化して自動実行させる方法  

---

## 毎日ジョブが有用な理由

本番環境では、毎日スケジューリングが最も一般的な設定です。これにより、以下が保証されます：  

- **Freshness** — 毎日のデータが検証されます。  
- **Consistency** — 異常が下流に伝播する前に早期に検出されます。  
- **Automation** — 手動で検査を起動する必要がありません。  

---

## 次のステップ

- より高度なカスタムスケジュールについては、[crontab 定義の使い方](how_to_use_crontab.md) を参照してください。  
- 毎日ジョブを**alerting**と組み合わせることで、異常が検出されたときに通知を受け取れます。
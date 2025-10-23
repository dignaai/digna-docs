---
title: Crontabを使った高度なスケジューリング
description: crontab 式を使って *digna* で高度なタイミングのジョブをスケジュールする方法を学びます。
---

# Crontabを使った高度なスケジューリング

このガイドでは *digna* で **crontab 式** を使ってジョブをスケジュールする方法を説明します。  
日次・週次・月次といった標準パターンとは異なり、crontab はカスタムスケジュールを柔軟に定義できます。

---

## インタラクティブデモ

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## このガイドで学べること

- ダッシュボードで **Scheduling** セクションを開く方法  
- **crontab 式** を使って新しいジョブを作成する方法  
- **週末の10:00にのみ実行**されるスケジュールを設定する方法  

---

## 例：週末スケジュール

毎週**土曜日と日曜日の午前10時**にジョブを実行するスケジュールを設定するには、次の式を使用します:


- `0` → 分（0分、ちょうど）  
- `10` → 時（午前10時）  
- `*` → 日（毎日）  
- `*` → 月（毎月）  
- `sat,sun` → 土曜と日曜のみ  

---

## Crontabを使う理由

- 日次・週次・月次の標準パターンを超えたスケジュールを作成できる  
- 特定の日、時間、または間隔など、正確な実行時刻を定義できる  
- 週末のジョブ、営業時間外のチェック、または頻繁な監視に便利  

---
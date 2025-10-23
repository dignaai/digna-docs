---
title: Data Anomalies – 自動検出 | digna ドキュメント
description: digna Data Anomalies が手動ルールなしでボリューム低下、欠損値、分布の変化、予期しないパターンを自動検出する仕組みを紹介します。AIによる異常検知でデータ品質を向上させましょう。
---

# Data Anomalies – 自動検出

## Purpose
ルールを記述せずに異常を検出します。

## Technical Features
### Metrics analyzed
- レコード数  
- 欠損値  
- 分布とヒストグラム  
- 値の範囲  
- 一意性  

### Intelligent detection
- **過去データからの学習**を利用して期待される範囲を動的に定義する  
- 実際のデータが期待範囲を外れた場合に異常としてフラグを立てる  

## Detection Scenarios
- **ボリュームの減少/急増** → 例: 日次取引の半数が欠落している  
- **列の入れ替わり** → 名と姓の列が逆になっている  
- **予期しない値** → オーストリアの都市に "Zurich" が表示される  

## Value
通常であれば数百もの手動ルールが必要な判断を自動化します。
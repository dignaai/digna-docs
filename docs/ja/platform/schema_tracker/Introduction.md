---
title: Data Schema Tracker – スキーマの変化を監視 | digna ドキュメント
description: digna Data Schema Trackerがカラムの変更、データ型の更新、スキーマドリフトをどのように監視するかを学びます。意図的・非意図的な変更に対するアラートでETLの失敗やダッシュボードのエラーを防ぎます。
---

# Data Schema Tracker – スキーマの変化を監視

## Purpose
スキーマの変化を追跡してアラートを送信します。

## Technical Features
- 監視対象:
  - 追加または削除されたカラム
  - データ型の変更
- 意図的な変更と意図しない変更の両方に対してアラートを出します  
- ETLパイプラインやダッシュボードを壊す可能性のある**silent schema drift**を防ぎます  

## Example Use Cases
- 下流でエラーを引き起こす可能性のあるデータ型の変更（例: `INT` → `VARCHAR`）を特定する  
- スキーマ不一致によりパイプラインが失敗する前にデータエンジニアに通知する  

## Value
チームが**急速に変化するデータセット**を制御できるようにします。
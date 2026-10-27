---
title: digna Python SDK モデル 2026.11 | digna ドキュメント
description: digna Python SDK リリース 2026.11 のデータモデル
image: /assets/logo_square.png
---

# digna Python SDK モデル 2026.11

このページでは、***digna*** Python SDK が使用する主要なリクエストモデルとレスポンスモデルについて説明します。すべてのペイロードは、`digna_sdk.models` からインポートする [pydantic](https://docs.pydantic.dev/) モデルとして表現されます。

::: digna_sdk.models
    options:
      members:
        - NamedRef
        - DatasetRef
        - StatisticRef
        - InspectionMetric
        - Project
        - DbConnection
        - DataSourceModules
        - DataSourceObject
        - DataSource
        - DataSet
        - AttributeCheckDefinition
        - Attribute
        - CheckDefinition
        - InspectionRequestStatus
        - SubmittedInspectionRequest
        - DatasetInspectionStatus
        - DataSourceInspectionStatus
        - ProjectInspectionStatus

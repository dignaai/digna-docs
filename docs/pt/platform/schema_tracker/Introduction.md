---
title: Data Schema Tracker – Monitorar Evolução do Esquema | digna Documentation
description: Saiba como o Data Schema Tracker da digna monitora alterações de colunas, atualizações de tipos de dados e drift de esquema. Receba alertas para mudanças intencionais e não intencionais para prevenir falhas de ETL e erros em dashboards.
---

# Data Schema Tracker – Monitorar Evolução do Esquema

## Propósito
Rastrear e alertar sobre a evolução do esquema.

## Recursos Técnicos
- Monitora:
  - Colunas adicionadas ou removidas
  - Mudanças de tipo de dados
- Gera alertas para mudanças de esquema tanto intencionais quanto não intencionais  
- Evita a **deriva silenciosa do esquema** que pode quebrar pipelines de ETL ou dashboards  

## Exemplos de Uso
- Identificar mudanças de tipo de dados (por exemplo, `INT` → `VARCHAR`) que podem causar erros em etapas posteriores  
- Alertar engenheiros de dados antes que pipelines falhem devido a incompatibilidades de esquema  

## Valor
Mantém as equipes no controle de **conjuntos de dados dinâmicos e em rápida evolução**.
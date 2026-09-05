---
title: digna Data Anomalies | Observabilidade de Dados com IA
description: O digna Data Anomalies faz parte da digna Data Observability Platform. Ele aprende automaticamente padrões nos seus dados e detecta anomalias para melhorar a qualidade dos dados e a observabilidade em bancos de dados, data lakes e data warehouses.
tags:
  - qualidade de dados
  - observabilidade de dados
  - qualidade dos dados
  - observabilidade dos dados
  - monitoramento orientado por IA
  - detecção de anomalias
  - digna
  - plataforma digna
hide:
  - toc                # optional: hide the small top-level TOC if you use inline nav
  - navigation         # optional: hide side navigation for standalone pages
image: /assets/logo_square.png
---


# digna Data Anomalies – Detecção baseada em IA de problemas de qualidade de dados

**Observabilidade com IA para confiança contínua nos dados**

digna Data Anomalies faz parte da **digna Data Observability Platform** — uma solução modular que melhora a **qualidade dos dados** ao analisar continuamente como os conjuntos de dados se comportam ao longo do tempo.

Ele aprende automaticamente como é o “normal” para seus dados e alerta quando o comportamento muda — sem definir limites estáticos ou escrever uma única regra.  
O módulo é executado diretamente dentro do seu banco de dados, então os dados nunca deixam o seu ambiente.

---

## Objetivo do digna Data Anomalies

O módulo **digna Data Anomalies** fornece **observabilidade de dados** contínua calculando e monitorando métricas estatísticas pré-definidas, tais como:

- Volume de dados e contagem de registros  
- Proporção de valores ausentes  
- Distribuições de valores e histogramas  
- Intervalos numéricos e médias  
- Unicidade de colunas e comprimento de texto  

Essas métricas são coletadas automaticamente para cada conjunto de dados.  
Com base nelas, a digna constrói modelos que representam o comportamento típico de cada métrica — aprendendo padrões diários, semanais ou sazonais.  
Uma vez treinado, o módulo prevê valores esperados para novos dados e detecta desvios que podem indicar problemas de qualidade, falhas de processo ou mudanças a montante.

---

## Principais capacidades

- Aprende automaticamente o comportamento esperado dos dados usando IA — sem configuração de limites.  
- Detecta quedas súbitas, picos ou drift nas distribuições e no volume de dados.  
- Identifica colunas trocadas ou mapeamentos incorretos entre atributos.  
- Destaca valores categóricos inesperados (por exemplo, novas regiões ou códigos).  
- Suporta todos os tipos de coluna: numéricas, categóricas ou não especificadas.  
- Opera inteiramente no ambiente do cliente — sem movimentação de dados.  
- Integra-se com **digna Data Analytics** para análise de tendências de longo prazo.

---

## Como funciona

### Passo 1 – Cálculo de métricas
A digna calcula um conjunto de métricas de perfil para cada tabela e coluna.  
Essas métricas descrevem a estrutura e o comportamento estatístico dos seus dados e são armazenadas para análise posterior.

### Passo 2 – Treinamento do modelo
Com base em valores históricos das métricas, a digna treina modelos compactos de aprendizado de máquina (modelos de assinatura) que capturam a faixa normal de cada métrica.

### Passo 3 – Definição automática de limites
Usando *inferência conformal*, a digna calcula intervalos de confiança adaptativos (limiares automáticos) que evoluem com os seus dados.  
Se novos valores de métricas ficarem fora da faixa prevista, eles são marcados como anomalias.

Esse ciclo contínuo de feedback garante que o monitoramento permaneça relevante mesmo quando os volumes ou padrões de dados crescem naturalmente.

---

## Cenários de exemplo

### Queda inesperada no volume de registros
Um conjunto de dados normalmente contém cerca de 500 000 registros por dia.  
Quando uma nova entrega inclui apenas 50 000 registros, a digna sinaliza uma anomalia e mostra o quanto o valor diverge da faixa aprendida.

### Colunas trocadas detectadas
O comprimento médio da string de `last_name` passa a coincidir repentinamente com o de `first_name`.  
A digna reconhece a mudança nos padrões das métricas e sinaliza uma possível troca de colunas.

### Categoria inesperada detectada
Uma coluna que lista cidades austríacas passa a conter “Zurich”.  
Com base nas distribuições históricas, a digna marca o novo valor como inesperado e alerta o usuário.

---

## Integração com outros módulos

- **digna Data Analytics** — agrega histórico de anomalias e métricas de volatilidade para revelar tendências de longo prazo.  
- **digna Data Validation** — aplica regras de negócio explícitas para verificações determinísticas de qualidade.  
- **digna Data Timeliness** — monitora tempos de chegada dos dados e correlaciona atrasos com ocorrências de anomalias.  
- **digna Data Schema Tracker** — detecta mudanças estruturais que podem explicar novas anomalias.

---

## Casos de uso típicos

- Detectar cargas de dados ausentes ou duplicadas.  
- Identificar colunas trocadas ou truncadas.  
- Detectar drift de distribuição em atributos numéricos ou categóricos.  
- Encontrar valores de referência ou códigos inesperados.  
- Monitorar pipelines de ingestão contínua quanto a irregularidades.  
- Acompanhar a **qualidade e observabilidade dos dados** em vários domínios.

---

## Benefícios

- Detecção imediata de comportamento anômalo dos dados.  
- Elimina a afinação manual de limites.  
- Reduz o esforço operacional em ambientes de dados de grande escala.  
- Constrói confiança em sistemas de análise e relatórios.  
- Reforça a **qualidade dos dados** e a observabilidade de ponta a ponta.

---

## Módulos digna relacionados

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — métricas de tendência e volatilidade.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — verificação de dados baseada em regras.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — monitoramento de cronogramas de entrega de dados.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — detecção de mudanças de esquema.

---

## Resumo

O módulo **digna Data Anomalies** forma o núcleo da **Plataforma de Observabilidade de Dados** da digna orientada por IA.  
Ao monitorar continuamente métricas-chave, aprender padrões e identificar desvios, ele ajuda organizações a garantir que a **qualidade dos dados** permaneça confiável, estável e explicável — sem configuração manual.
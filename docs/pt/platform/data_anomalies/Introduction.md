---
title: Data Anomalies – Detecção Automatizada de Irregularidades em Dados | digna Documentation
description: Saiba como o digna Data Anomalies detecta automaticamente quedas de volume, valores ausentes, deslocamentos de distribuição e padrões inesperados sem necessidade de regras manuais. Melhore a qualidade dos dados e a observabilidade dos pipelines com detecção de anomalias orientada por IA.
image: /assets/logo_square.png
keywords:
  - data anomalies
  - detecção de anomalias por ia
  - monitoramento da qualidade de dados
  - qualidade dos dados
  - observabilidade de dados
  - detecção de dados ausentes
  - monitoramento de volume de dados
  - deslocamento de distribuição
  - confiabilidade de dados
  - digna data anomalies
lang: pt
robots: index, follow
og_title: Data Anomalies – Detecção Automatizada | digna Documentation
og_description: O digna Data Anomalies detecta automaticamente irregularidades no volume, valores e distribuições dos dados sem regras manuais — melhorando a qualidade e a observabilidade dos dados em múltiplas plataformas.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Anomalies – Detecção Automatizada
<h1 style="display:none;">AI-Driven Module for Data Quality and Observability – digna Data Anomalies</h1>

---

## Purpose

O módulo **Data Anomalies** identifica irregularidades nos seus conjuntos de dados automaticamente — sem necessidade de escrever regras.  
Ele monitora continuamente **a qualidade da entrega dos dados**, aprendendo como é o “normal” e detectando desvios em tempo real.

Ao usar detecção baseada em IA, o digna reconhece *erros silenciosos de dados* como registros ausentes, duplicados ou corrompidos que podem distorcer relatórios, modelos de ML e painéis.

---

## Technical Overview

### Metrics analyzed

O digna perfila continuamente os seguintes aspectos dos seus dados:

- **Record volume** – número total de linhas, diário ou por lote  
- **Missing values** – detecção de campos nulos ou vazios  
- **Distributions and histograms** – monitoramento de mudanças na forma dos dados  
- **Value ranges** – identificação automática de valores fora do intervalo ou extremos  
- **Uniqueness** – checagens de chaves duplicadas ou entradas repetidas  

### Intelligent anomaly detection

- Usa **historical learning** para definir dinamicamente limites esperados  
- Detecta desvios em **volume, distribuições de valores ou relacionamentos lógicos**  
- Emprega IA para adaptar limites automaticamente com base em horário ou padrões sazonais  
- Distingue entre **flutuações estatísticas** e anomalias reais  
- Produz métricas detalhadas e pontuações de confiança por conjunto de dados e coluna  

---

## Detection Scenarios

Abaixo estão exemplos de problemas do mundo real capturados automaticamente pelo módulo **Data Anomalies**:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | Falta metade das transações diárias, cargas de lote duplicadas ou picos súbitos de dados |
| **Missing or null values** | Extrações de dados concluídas, mas colunas críticas ficaram vazias |
| **Distribution drifts** | Valor médio de compra ou contagem de transações por região muda inesperadamente |
| **Column swaps** | Colunas como *first_name* e *last_name* trocadas acidentalmente durante o ETL |
| **Unexpected categorical values** | ex.: “Zurich” aparece na lista de cidades da Áustria |
| **Sudden uniqueness loss** | IDs antes únicos começam a se duplicar devido a erros de join a montante |

---

## Architecture and Execution

- **In-database execution:** Toda a lógica de detecção de anomalias é executada *dentro do motor de banco de dados* (Teradata, Snowflake, Databricks, PostgreSQL, etc.)  
- **No data movement:** o digna lê apenas métricas, nunca transfere dados brutos para fora  
- **Incremental updates:** Somente segmentos de dados novos são analisados a cada execução para eficiência  
- **Configurable inspection frequency:** Horária, diária ou acionada por processos a montante  
- **Result storage:** Métricas e flags de anomalia são gravadas de volta no esquema de observabilidade do digna para visualização e alertas  

---

## Benefits

| Area | Benefit |
|------|----------|
| **Automation** | Elimina centenas de definições manuais em SQL ou regras |
| **Precision** | Detecta problemas que limites estáticos frequentemente deixam passar |
| **Scalability** | Monitora milhões de registros por tabela de forma eficiente |
| **Integration** | Funciona perfeitamente com *digna Data Analytics* para análise de tendências |
| **Compliance** | Garante controle contínuo sobre a **qualidade e observabilidade dos dados** |
| **Transparency** | Fornece pontuações de confiança, timestamps e códigos de razão para cada anomalia |

---

## How digna Learns “Normal”

1. **Profiling phase:** o digna coleta métricas de conjuntos de dados históricos.  
2. **Learning phase:** modelos de IA identificam padrões recorrentes (sazonais, semanais, diários).  
3. **Monitoring phase:** conjuntos de dados futuros são comparados contra limites aprendidos dinamicamente.  
4. **Alerting phase:** desvios além das fronteiras de confiança estatística são reportados como anomalias.  

Todos os modelos são explicáveis, determinísticos e otimizados para volumes de dados empresariais.

---

## Example Use Cases

- Monitoramento da qualidade de dados em **sistemas de transações bancárias**  
- Detecção de falhas de carga em **jobs de ETL ou data warehouse**  
- Identificação de atividade anômala de clientes em **registros de telecomunicações**  
- Observação da consistência de dados clínicos em **pipelines de analytics em saúde**  
- Prevenção de painéis quebrados em **BI e ambientes de report**

---

## Frequently Asked Questions

**Does Data Anomalies require predefined rules?**  
Não — o módulo aprende automaticamente a partir do comportamento dos dados.

**Can I still define specific thresholds if needed?**  
Sim. o digna permite combinar detecção baseada em IA com regras (via *Data Validation*).

**How are false positives minimized?**  
O módulo utiliza aprendizado adaptativo e pontuação de confiança estatística para ignorar variações sazonais normais.

**Where does computation happen?**  
Todo o processamento ocorre dentro do seu banco de dados — o digna nunca extrai dados brutos.

**Is it suitable for sensitive or regulated data?**  
Sim. o digna roda totalmente **on-premises ou em nuvem privada** e segue padrões europeus de conformidade.

---
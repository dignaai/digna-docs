# Data Schema Tracker – Monitorar Evolução do Esquema
<h1 style="display:none;">Módulo impulsionado por IA para Observabilidade de Metadados e Qualidade de Dados – digna Data Schema Tracker</h1>

---

## Propósito

O **Data Schema Tracker** mantém você informado sobre como as estruturas do banco de dados evoluem.  
Ele monitora continuamente **schemas de tabelas, colunas e tipos de dados** para detectar **schema drift** — mudanças estruturais intencionais ou não intencionais que podem interromper pipelines, jobs de ETL ou dashboards de BI.

Ao garantir transparência na evolução do esquema, o digna ajuda organizações a manter a **confiança na qualidade dos dados**, sustentar a **observabilidade dos sistemas de dados** e evitar incidentes de produção custosos causados por mudanças de esquema não detectadas.

---

## Visão Técnica

### O que monitora

- **Colunas adicionadas ou removidas** – Detecta colunas recém-introduzidas, renomeadas ou excluídas.  
- **Modificações de tipo de dado** – Identifica alterações como `INT → VARCHAR` ou `DATE → TIMESTAMP`.  
- **Modificações de tabelas e views** – Rastreia criação, renomeação ou remoção de tabelas e views.  
- **Diferenças entre ambientes** – Compara versões de esquema entre ambientes Dev, Test e Production.  

### Detecção e Alertas

- Faz varreduras dos **metadados do banco de dados** ou dos **catálogos do sistema** diretamente na sua plataforma de dados.  
- Compara cada snapshot de esquema com a versão previamente conhecida armazenada no digna observability schema.  
- Gera **alertas em tempo real** no painel, via API ou por canais de notificação externos (e-mail, Slack, webhook).  
- Registra cada versão do esquema para **rastreio histórico e prontidão para auditoria**.

---

## Arquitetura e Execução

- **Execução em Banco de Dados:** o digna é executado inteiramente dentro do seu ambiente, consultando views de metadados sem extrair nenhum dado.  
- **Varredura Leve:** acessa apenas informações estruturais — nunca dados de usuários.  
- **Armazenamento Centralizado:** metadados de esquema e registros de drift são armazenados no digna observability schema para visualização e análise.  
- **Automação:** suporta varreduras agendadas ou baseadas em eventos via digna Core ou ferramentas de orquestração externas.  

---

## Exemplos de Casos de Uso

| Caso de Uso | Descrição |
|-----------|--------------|
| **Monitoramento da Estabilidade de ETL** | Detecta mudanças de estrutura upstream antes que os pipelines falhem devido a incompatibilidades de esquema. |
| **Confiabilidade de Business Intelligence** | Prevê dashboards quebrados causados por colunas renomeadas ou ausentes. |
| **Governança de Data Warehouse** | Mantém um histórico auditável da evolução do esquema para conformidade e análise de impacto. |
| **Supervisão de Integração** | Garante que os schemas do data lake e do data warehouse permaneçam sincronizados após atualizações estruturais. |

---

## Benefícios

| Área | Benefício |
|------|----------|
| **Qualidade dos Dados** | Evita schema drift não detectado que pode corromper ou invalidar pipelines de dados. |
| **Observabilidade** | Adiciona monitoramento estrutural à observabilidade geral dos ecossistemas de dados. |
| **Conformidade** | Mantém histórico versionado de esquema para auditoria, rastreabilidade e controle de mudanças. |
| **Prevenção** | Detecta problemas estruturais antes que se propaguen para relatórios ou erros em produção. |

---

## Como Funciona

1. **Snapshot Collection** – digna captura os metadados do esquema atual.  
2. **Comparison** – o novo snapshot é comparado
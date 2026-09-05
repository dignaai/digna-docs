# Data Timeliness – Monitoramento de Entrega Pontual
<h1 style="display:none;">Módulo Data Timeliness orientado por IA para Qualidade de Dados e Observabilidade – digna</h1>

---

## Objetivo

O módulo **Data Timeliness** garante que **os dados cheguem no prazo** — todas as vezes.  
Ele monitora continuamente cronogramas de entrega e detecta automaticamente quando conjuntos de dados, tabelas ou arquivos estão **atrasados, ausentes ou incompletos**.  

Ao combinar aprendizado de IA com cronogramas definidos pelo usuário, a *digna* permite que organizações previnam erros em etapas posteriores e mantenham rígidas metas de **SLA (Acordo de Nível de Serviço)** tanto para **Qualidade de Dados** quanto para **observabilidade dos pipelines de dados**.

---

## Visão Técnica

### Modos de Monitoramento Duplos
- **Padrões de Chegada Aprendidos por IA**  
  a digna aprende automaticamente o ritmo natural de suas entregas de dados — diárias, horárias ou acionadas por eventos — analisando timestamps históricos e tempos de conclusão.  
  Ela se adapta a mudanças em calendários comerciais, finais de semana ou picos de fim de mês.

- **Cronogramas Definidos pelo Usuário**  
  Usuários podem definir explicitamente horários esperados de entrega (por exemplo, *todo dia útil antes das 7:30 AM*).  
  a digna compara o horário real de chegada com o cronograma planejado e gera alertas quando os dados estão atrasados ou ausentes.

### Mecanismo de Detecção
- Avalia **timestamps de metadados**, **contagens de registros** e **frescura de tabelas**  
- Detecta **jobs de ETL parados**, **extrações falhadas** e **chegadas parciais de arquivos**  
- Integra-se com *Data Anomalies* e *Data Validation* para insights combinados

---

## Cenários de Detecção

| Cenário | Descrição |
|-----------|--------------|
| **Chegada de dados atrasada** | Feed diário de mercado atrasado em duas horas, fazendo com que relatórios percam SLAs |
| **Carga ausente** | Uma tabela ou partição agendada não foi atualizada para a data atual |
| **Atraso por dependência encadeada** | Atraso em job upstream impacta a atualização do pipeline downstream |
| **Mudança de padrão no fim de semana** | Modelo de IA se adapta automaticamente quando não se espera dados aos domingos |

---

## Arquitetura e Execução

- **Execução dentro do banco de dados:** a digna executa checagens de timeliness diretamente no seu banco de dados ou data warehouse.  
- **Acesso leve a metadados:** lê timestamps de jobs, contagens de registros e informações de partições — sem necessidade de extração de dados.  
- **Frequência configurável:** agende o monitoramento por conjunto de dados, schema ou pipeline.  
- **Alertas entre módulos:** resultados podem acionar avisos visuais no *Inspection Hub* ou notificações por e-mail, Slack ou API.  

---

## Exemplos de Uso

- **Feeds de Mercado Financeiro:** detectar atrasos em atualizações de preços ou dados de negociação.  
- **Cargas no Data Warehouse:** monitorar quando jobs ETL noturnos terminam mais tarde do que o esperado.  
- **Compartilhamento de Dados entre Equipes:** garantir que entregas departamentais ocorram antes dos cortes diários.  
- **Relatórios Regulatórios:** confirmar que submissões incluam o snapshot de dados mais recente disponível.  

---

## Benefícios

| Área | Benefício |
|------|----------|
| **Continuidade do Negócio** | Previne interrupções operacionais devido a dados atrasados ou ausentes |
| **Qualidade de Dados** | Melhora a confiabilidade e consistência dos pipelines de dados |
| **Conformidade** | Garante adesão a SLAs e transparência para auditoria |
| **Automação** | IA elimina o rastreamento manual de cronogramas |
| **Integração** | Funciona de forma integrada com *Data Analytics* para visualizar tendências de pontualidade ao longo do tempo |

---

## Como a digna Aprende os Tempos de Entrega Esperados

1. **Análise Histórica:** a digna observa tempos de carga e durações anteriores.  
2. **Modelagem por IA:** aprendizado de máquina cria uma linha de base dinâmica para chegada esperada.  
3. **Monitoramento:** cada nova entrega é comparada à linha de base.  
4. **Alertas:** desvios acionam alertas com métricas contextuais e scores de confiança.  

Essa abordagem de aprendizado contínuo se adapta a processos em evolução enquanto mantém baixos os falsos positivos.

---

## Perguntas Frequentes

**Posso definir meus próprios horários de entrega?**  
Sim. a digna suporta tanto cronogramas fixos definidos pelo usuário quanto padrões aprendidos por IA.

**Ela pode integrar-se ao meu ETL ou ferramenta de orquestração?**  
Sim. a digna integra-se com ferramentas como Airflow, dbt, Informatica ou agendadores personalizados.

**Onde a computação acontece?**  
Todas as análises são executadas dentro do seu banco de dados ou data warehouse na nuvem — nenhum serviço externo é utilizado.

**O que acontece quando os dados estão atrasados?**  
a digna gera alertas no painel, no Inspection Hub e via API/webhooks para notificar as equipes de operações instantaneamente.

---


**digna Data Timeliness** ajuda a garantir **confiança nos dados**, combinando **detecção orientada por IA**, **execução on-premises** e **observabilidade de dados** — tudo dentro do seu ambiente controlado.
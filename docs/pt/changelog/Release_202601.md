---
title: digna Release 2026.01 | Datasources Lógicos, Conexões Globais & Validação Avançada de Dados
description: Saiba o que há de novo no digna Release 2026.01. Esta versão introduz conexões de banco de dados globais, datasources lógicos, condições de relevância de anomalias, exportações CSV e validação avançada de dados incluindo checagens de integridade referencial.
keywords: digna Release 2026.01, digna changelog, digna datasource, digna database connections, digna Data Anomalies, digna Data Validation, referential integrity validation, regras de qualidade de dados, observabilidade de dados, digna CSV export
image: /assets/logo_square.png
---

# Changelog – Release 2026.01  

Com o Release 2026.01, o digna introduz melhorias significativas no modelamento de datasources, na gestão de conexões e na usabilidade das inspeções.  
Esta versão amplia a flexibilidade em todos os módulos e estende significativamente a **cobertura de qualidade e validação de dados**.

---

## Novos Recursos  

### Conexões de Banco de Dados Globais  
- As conexões de banco de dados agora são configuradas em nível **global**.  
- Conexões globais podem ser reutilizadas em **todos os projetos**, simplificando configuração e manutenção.  
- **Impacto:** Reduz o esforço operacional e garante conectividade consistente entre ambientes.

### Múltiplas Conexões de Fonte por Projeto  
- Projetos agora podem referenciar **múltiplas configurações de conexão de fonte**.  
- Permite configurações mais flexíveis para paisagens de dados complexas por projeto.  
- **Impacto:** Suporta arquiteturas empresariais realistas com fontes de dados heterogêneas.

### Datasources Lógicos  
- Datasources agora representam uma **camada lógica** dentro de um projeto.  
- Cada datasource pode ser suportado por:
    - uma **tabela de banco de dados**
    - uma **view de banco de dados**
    - uma **instrução SQL personalizada**  
- Essa separação melhora o reuso, a clareza e o modelamento das inspeções entre os módulos.  
- **Impacto:** Desacopla inspeções e regras de qualidade de dados do armazenamento físico, melhorando manutenção e reuso.

### Condição de Relevância de Anomalia  
- Uma **Condição de Relevância de Anomalia** pode agora ser definida para controlar a avaliação do status de anomalia ao nível do conjunto de dados.  
- As estatísticas são calculadas independentemente de a condição estar definida ou satisfeita.  
- Se a condição **não for satisfeita**, o **digna Data Anomalies** não fornece status de anomalia (verde / amarelo / vermelho).  
- **Exemplo:** Excluir o conjunto de dados da avaliação de anomalia quando a contagem de registros for inferior a 10.  
- **Impacto:** Garante que anomalias sejam avaliadas somente em contextos de negócio relevantes.

### Configuração de Notificações por Módulo  
- As notificações agora podem ser configuradas **por módulo** diretamente no digna.  
- Permite controle independente do comportamento de alertas para **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** e outros módulos.  
- **Impacto:** Habilita estratégias de alerta precisas alinhadas com responsabilidades das equipes e criticidade.

### Exportação de Resultados de Inspeção (CSV)  
- Usuários agora podem **baixar resultados de inspeção como arquivos CSV**.  
- Permite análise offline, relatórios e integração com ferramentas externas.  
- **Impacto:** Simplifica auditorias, geração de relatórios e análises de qualidade de dados a jusante.

---

## Capacidades Estendidas de Validação de Dados  

Com este release, o **digna Data Validation** agora suporta um conjunto abrangente de regras de qualidade de dados:

- **Regras de validação ao nível de linha**  
- **Verificações de unicidade multi-coluna**  
- **Validação de integridade referencial entre datasources**

Juntas, essas verificações possibilitam a aplicação de **regras de qualidade estrutural e relacional** em paisagens de dados complexas.

### Verificações de Unicidade para Múltiplas Colunas
- Introduzidas **Verificações de Unicidade** para um **conjunto configurável de colunas**.  
- Permite validar chaves compostas e restrições de unicidade em nível de negócio.  
- **Impacto:** Detecta entidades de negócio duplicadas que não podem ser identificadas com verificações de coluna única.

### Verificações de Integridade Referencial
- Introduzidas **Verificações de Integridade Referencial** para validar relacionamentos entre datasources.  
- Garante que os **valores de chave estrangeira** em um datasource de origem existam em um datasource alvo referenciado.  
- Ajuda a detectar registros órfãos, relacionamentos quebrados e problemas de consistência de dados precocemente.  
- Projetado para funcionar com **datasources lógicos**, incluindo views e SQL personalizado.  
- **Casos de uso:** integridade de data warehouse, reporte regulatório, consistência de master data e análises confiáveis a jusante.

---

## Quem se Beneficia com Este Release  

- **Engenheiros de Dados:** Modelagem de datasources mais flexível e conexões de banco reutilizáveis  
- **Times de Qualidade de Dados & Governança:** Cobertura de validação expandida incluindo regras de integridade relacional  
- **Times de Analytics & BI:** Entradas mais limpas e resultados de inspeção exportáveis  
- **Responsáveis pela Plataforma:** Menor complexidade de configuração e melhor manutenibilidade operacional

---

## Atualizações da CLI  
- Sem alterações

---
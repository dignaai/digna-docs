---
title: digna Release 2026.06 | Python SDK, Implantação com Docker & Gerenciamento de Validação Aprimorado
description: Saiba o que há de novo na digna Release 2026.06. Esta versão apresenta o novo Python SDK da digna, suporte oficial à implantação via Docker, uma experiência de painel redesenhada e capacidades estendidas de importação/exportação para regras de validação de dados.
keywords: digna Release 2026.06, digna Python SDK, digna suporte Docker, automação de qualidade de dados, perfilamento de dados, importação exportação de regras de validação, painel digna, plataforma de observabilidade de dados, API Python, automação de metadados
image: /assets/logo_square.png
---

# Registro de Alterações – Release 2026.06  

Com a Release 2026.06, a digna dá um grande passo em automação, extensibilidade e usabilidade da plataforma.  
Esta versão apresenta o novo **digna Python SDK**, suporte oficial de **implantação via Docker**, uma experiência de painel renovada e maior portabilidade no gerenciamento de regras de validação.

---

## Novos Recursos  

### digna Python SDK – Automatize Tudo com Python  
- Instale via:
  ```bash
  pip install digna-sdk
  ```
- Gerencie e automatize a digna programaticamente usando Python  
- Crie e configure projetos via código  
- Dispare execuções de inspeções e monitoramento  
- Gerencie conjuntos de dados, regras e configurações programaticamente  
- Faça perfilamento de tabelas e extraia insights de metadados  
- Exporte resultados de perfilamento e qualidade de dados para repositórios e sistemas externos  
- Integre com notebooks, ferramentas de orquestração e pipelines de CI/CD  

**Impacto:** Permite infraestrutura como código completa e automação aprofundada dos fluxos de trabalho de qualidade e observabilidade de dados usando Python.

---

### Suporte Docker – Implantação e Operações Simplificadas  
- Imagem Docker oficial para digna  
- Configuração rápida e consistente entre ambientes  
- Onboarding simplificado para desenvolvimento, testes e produção  
- Integração fácil com Kubernetes e plataformas de contêineres  
- Melhor portabilidade e reprodutibilidade das implantações  

**Impacto:** Facilita a implantação e operação da digna em arquiteturas modernas cloud-native.

---

### QueryMode – Estratégia Flexível de Execução de SQL

Configure a estratégia de execução de consultas: **Single** ou **Combined** mode

**Single Mode**: Cada métrica é calculada com uma consulta SQL dedicada

  - Ideal para fontes de dados grandes onde restrições de memória são uma preocupação
  - Evita exaustão de recursos por consultas combinadas (out of memory, limites de spool)
  - Maior número de consultas, mas menor uso de memória por consulta

**Combined Mode**: Todas as métricas são calculadas dentro de uma única consulta SQL

  - Reduz o número total de consultas e a sobrecarga de rede
  - Otimiza desempenho quando as fontes de dados são gerenciáveis em memória
  - Mais eficiente para execuções frequentes e paralelas

**Impacto:** Oferece controle granular sobre a execução de consultas para equilibrar desempenho, uso de recursos e segurança de memória conforme as características da fonte de dados.


---

### Experiência de Painel Redesenhada  
- UI/UX modernizada e aprimorada  
- Navegação e estrutura mais claras  
- Melhor visibilidade dos resultados de monitoramento e insights de qualidade de dados  
- Maior legibilidade de alertas, estatísticas e painéis  
- Acesso mais rápido às informações operacionais chave  

**Impacto:** Melhora a usabilidade e a produtividade diária de todos os usuários.

---

### Importação & Exportação Estendida para Regras de Validação  
- Funcionalidade de importação/exportação de regras de validação aprimorada  
- Migração mais fácil entre ambientes e projetos  
- Reuso facilitado de conjuntos de regras padronizados  
- Melhor governança e gestão do ciclo de vida das regras  
- Colaboração simplificada entre equipes  

**Impacto:** Possibilita governança de qualidade de dados escalável e consistente em toda a organização.

---

## Aprimoramentos da Plataforma  

- Integração completa do Python SDK para automação  
- Implantação conteinerizada via Docker  
- UX melhorada através do painel redesenhado  
- Maior portabilidade da lógica de validação  

---

## Quem se Beneficia Desta Versão  

- Data Engineers: automação, uso do SDK, integração em pipelines  
- Equipes de Plataforma: implantação simplificada via Docker  
- Equipes de Governança de Dados: gerenciamento reutilizável de regras de validação  
- Equipes de Analytics: melhor usabilidade e visibilidade de insights  

---

## Atualizações da CLI  
- Adicionado suporte de integração ao SDK  
- Fluxos de importação/exportação aprimorados  
- Melhorias gerais de estabilidade e desempenho
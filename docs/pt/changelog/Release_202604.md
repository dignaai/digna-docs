---
title: digna Versão 2026.04 | Analytics Chart, Enumerações & Modelos de Regras de Validação
description: Saiba o que há de novo na digna Versão 2026.04. Esta versão introduz análise avançada de séries temporais com Analytics Chart, componentes reutilizáveis de validação, e padronização centralizada de valores.
keywords: digna Versão 2026.04, changelog digna, digna Data Analytics, análise de séries temporais, regressão, modelos de validação de dados, enumerações, validação de valores permitidos, regras de qualidade de dados, observabilidade de dados
image: /assets/logo_square.png
---

# Registro de alterações – Versão 2026.04  

Com a Versão 2026.04, a digna amplia significativamente suas capacidades em analytics e validação de dados.  
Esta versão introduz análise avançada de séries temporais, componentes reutilizáveis de validação e padronização centralizada de valores.

---

## Novos Recursos  

### Analytics Chart – Análise de Séries Temporais Sem Ciência de Dados  
- Novo **Analytics Chart** para análise interativa de séries temporais  
- Métodos analíticos integrados:
    - Regressão linear, quadrática e cúbica  
    - Regressão piecewise com pontos de quebra configuráveis  
    - Técnicas de suavização  
    - Análise de quantis  
- Identificação automática de tendências, sazonalidade e mudanças de padrão  
- Análise de resíduos para insights mais profundos sobre desvios  
- Séries temporais são calculadas automaticamente para cada conjunto de dados  

**Impacto:** Permite aos usuários compreender comportamentos complexos dos dados ao longo do tempo sem exigir conhecimento em ciência de dados ou ferramentas externas.

---

### Enumerações – Definição Central de Valores Permitidos  
- Defina conjuntos reutilizáveis de valores permitidos (por exemplo, países, estados, códigos de status)  
- Valide valores de colunas contra enumerações predefinidas em **digna Data Validation**  
- Reutilize enumerações entre projetos e fontes de dados  
- Use enumerações em qualquer lugar via `#ENUM:MY_ENUM#`  
- Todas as verificações são executadas **diretamente no banco de dados de origem**  

**Impacto:** Garante valores de dados consistentes e padronizados em toda a organização.

---

### Modelos de Regras de Validação – Lógica de Qualidade de Dados Reutilizável  
- Defina regras de validação reutilizáveis (por exemplo, verificações de espaços em branco, NOT NULL, checagens de formato)  
- Aplique templates em múltiplos conjuntos de dados  
- Garanta lógica de regra consistente entre projetos  
- Reduza duplicação e configuração manual  
- Todas as verificações são executadas **diretamente no banco de dados de origem**  

**Impacto:** Permite validação de dados escalável e de alto desempenho sem movimentação de dados.

---

### Condições de Relevância ao Nível de Estatística  
- Defina condições de relevância no **nível de coluna para cada estatística**  
- Estende o conceito de condições de relevância de anomalias  
- Controle quando uma estatística deve ser considerada relevante  
- Reduza ruído excluindo situações não críticas  

**Impacto:** Melhora a qualidade do sinal ao focar apenas em desvios significativos.

---

## Capacidades Estendidas de Data Analytics & Validação  

Com esta versão, a digna expande tanto o entendimento de dados quanto a padronização da validação:

- Interpretação avançada de **séries temporais** sem necessidade de conhecimento em ciência de dados  
- Definição centralizada de **valores permitidos via enumerações**  
- Lógica de validação reutilizável via **modelos/templates**  
- Controle refinado sobre a **relevância de estatísticas e alertas**  

Juntas, essas capacidades permitem que as organizações não apenas detectem problemas, mas também **compreendam, padronizem e controlem a qualidade dos dados**.

---

## Quem se Beneficia desta Versão  

- **Engenheiros de Dados:** Lógica de validação reutilizável e maior controle sobre o comportamento do monitoramento  
- **Equipes de Qualidade de Dados e Governança:** Regras padronizadas e validação consistente entre sistemas  
- **Equipes de Analytics & BI:** Melhor compreensão de tendências e desvios  
- **Proprietários de Plataforma:** Adoção ampliada por meio de analytics simplificado e validação escalável  

---

## Atualizações da CLI  
- Sem alterações  

---
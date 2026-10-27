# Registro de Alterações – Release 2026.11  

A Release 2026.11 é construída em torno de três grandes novidades:

- **digna Data Reconciliation (Beta)**: verifica se os dados permanecem consistentes à medida que se movem entre sistemas  
- **digna Agentic (Beta)**: abre a digna para agentes de IA por meio do digna MCP Server  
- **digna Engine**: opcionalmente faz o perfilamento dos dados dentro da digna e possibilita verificações de integridade referencial entre diferentes tecnologias de banco de dados  

---

## Novos Recursos  

### digna Data Reconciliation (Beta) – Consistência da Origem ao Destino  
Os dados costumam passar por vários sistemas antes de chegar a um relatório. O digna Data Reconciliation (Beta) compara uma fonte de dados de **destino** com as **origens** a partir das quais ela foi construída e emite um alerta quando elas deixam de corresponder.

- Configurado como regras nomeadas na nova aba **Data Reconciliation** da fonte de dados de destino  
- Qualquer fonte de dados do projeto com o Data Reconciliation ativado pode ser uma origem  
- Os casos de uso incluem procedimentos padrão de reconciliação e a validação dos resultados de processos de ETL  
- Dois tipos de regras: **Exact** e **AI**  

**Regras Exact – Reconciliação como Regra de Qualidade de Dados**: Você define exatamente o que deve corresponder entre uma origem e um destino, como em uma regra de qualidade de dados.

  - Compare uma fonte de dados de origem com uma fonte de dados de destino  
  - Associe uma verificação do destino a uma verificação da origem por estatística e atributo, por exemplo, contagens de linhas ou a soma de uma coluna de valores  
  - Permita uma diferença com uma tolerância **absolute** (por exemplo, ± 10) ou **relative** (por exemplo, ± 0,5 % da origem)  
  - A linha do tempo mostra a diferença de cada dia em relação à tolerância  

**Regras AI – Reconciliação como Observabilidade de Dados**: A digna aprende como um destino acompanha suas origens, da mesma forma que observa os dados em outros módulos, e emite um alerta quando essa relação se rompe.

  - Combine verificações de várias fontes de dados de origem com as verificações de um destino  
  - Não é preciso conhecer nem descrever a lógica entre elas (joins, filtros, agregações)  
  - Um modelo aprende com o histórico como o destino acompanha suas origens no mesmo dia  
  - Cada verificação do destino é prevista a partir dos valores das origens no dia, e a digna emite um alerta quando o destino sai da faixa formada pelos erros passados da própria regra  
  - Cada regra tem suas próprias **Model settings**: **Sensitivity**, **Memory** e **Model Complexity**  

As verificações de reconciliação aparecem no Dashboard com uma linha do tempo por regra. Elas contam para o status geral da inspeção e disparam notificações.

**Impacto:** Cobre os dois lados da reconciliação. As regras Exact garantem controles conhecidos entre origem e destino, e as regras AI monitoram fluxos complexos, como processos de ETL, de modo que dados perdidos ou alterados no caminho sejam detectados sem SQL de reconciliação escrito à mão.

---

### digna Agentic (Beta) – digna para Agentes de IA  
A primeira versão do digna Agentic (Beta). Agentes de IA agora podem trabalhar com a digna, responder a perguntas de negócio sobre seus dados e ajudar a melhorar sua configuração.

**digna MCP Server**: Permite que o Claude e outros agentes de IA trabalhem com a digna por meio do Model Context Protocol.

  - Gerencie projetos, fontes de dados, regras, agendamentos de inspeção e assinaturas  
  - Leia os status de inspeção até o nível de cada verificação, para investigar alertas  

**Descrições em Fontes de Dados e Atributos**: Descreva em linguagem simples o que uma fonte de dados ou um atributo contém.

  - Os agentes de IA usam as descrições para interpretar seus dados  
  - Faça perguntas de negócio sobre seus dados, e os agentes de IA as respondem com base no que a digna monitora  
  - Se a configuração atual da digna não consegue responder a uma pergunta, o agente de IA sugere, quando possível, alterações na fonte de dados e em seus atributos, por exemplo, adicionar um novo conjunto de dados  

**Impacto:** Permite fazer perguntas de negócio sobre seus dados em linguagem simples e permite que agentes de IA ajudem a configurar a digna e a investigar problemas de qualidade de dados.

---

### digna Engine – Perfilamento Onde Você Escolher  
Por padrão, a digna faz o perfilamento dos dados onde eles estão, no banco de dados de origem. O digna Engine adiciona uma opção: a digna exporta os dados da origem e faz o perfilamento dentro do digna Engine.

- Opcional, não obrigatório: o perfilamento no banco de dados de origem continua disponível  
- Selecionado por conexão de banco de dados como seu **local de perfilamento**: **Source Database** ou **digna Engine**  
- Disponível para todas as tecnologias de origem suportadas  

**Integridade Referencial entre Conexões**: Algumas verificações exigem que os dados sejam exportados. O digna Engine estende o **digna Data Validation** para esses casos.

  - **Verificações de Integridade Referencial** entre fontes de dados em **conexões de banco de dados diferentes**, inclusive de tecnologias de banco de dados diferentes (por exemplo, Oracle e PostgreSQL)  
  - Funciona com os dois locais de perfilamento: para o Source Database, apenas as colunas-chave são exportadas para o digna Engine  
  - O painel mostra quando uma verificação é executada entre duas conexões  

**Impacto:** Permite escolher onde os dados são perfilados e garante as relações entre sistemas que rodam em tecnologias de banco de dados diferentes.

---

## Aprimoramentos de Perfilamento  

Esta versão também dá aos usuários mais controle sobre o que é perfilado e como.

### Atributos de Consulta – Colunas Definidas pelo Usuário  
- Defina colunas artificiais: uma expressão SQL sobre uma ou mais colunas da fonte de dados  
- Cada atributo de consulta tem seu próprio nome  
- Perfilado e verificado como qualquer outro atributo  

### Categoria de Coluna DATE  
- Nova categoria **Date** para atributos  
- Métricas relativas à data inspecionada  

### Perfilamento Sob Demanda  
- Faça o perfilamento de qualquer atributo sobre o snapshot completo de uma data, sem executar uma inspeção  
- Ajuda a definir o tipo de coluna do atributo: **Numerical**, **Categorical**, **Date** ou **Unspecified**  

---

## Quem se Beneficia Desta Versão  

- **Data Engineers:** Validação de resultados de ETL com o digna Data Reconciliation (Beta)  
- **Equipes de Finanças, Risco e Controladoria:** Procedimentos padrão de reconciliação como regras exatas no digna Data Reconciliation (Beta)  
- **Equipes de Qualidade e Governança de Dados:** Integridade referencial entre tecnologias de banco de dados com o digna Engine  
- **Usuários de Negócio:** Perguntas de negócio sobre os dados respondidas por agentes de IA com o digna Agentic (Beta)  
- **Equipes de IA e Automação:** Agentes de IA trabalhando com a digna por meio do digna Agentic (Beta)  

---

## Atualizações da CLI  
- Sem alterações  

---
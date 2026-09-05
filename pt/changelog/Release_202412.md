# Registro de alterações – Release 2024.12

A release 2024.12 traz um novo conjunto de recursos e melhorias que tornam o digna mais automatizado, flexível e pronto para o ambiente de negócios.  
Esta versão aprimora agendamento, geração de relatórios, tratamento de consultas e a precisão na detecção de anomalias.  

---

## Novos Recursos

### Agendador embutido
As inspeções não dependem mais apenas da linha de comando ou de chamadas de API.  
Com o **novo digna Scheduler**, as inspeções podem ser executadas automaticamente em horários definidos.  

- Suporta **expressões Cron** para agendamentos recorrentes (diários, semanais ou intervalos personalizados).  
- Oferece controle preciso por meio de **offsets**, **datas de início** e **datas de término**.  
- Permite que as equipes garantam que todas as fontes de dados críticas sejam inspecionadas de forma consistente e sem esforço manual.  

---

### Relatórios em formato PDF
As equipes agora podem compartilhar facilmente os resultados com as partes interessadas por meio de **exportações em PDF**.  

- Gráficos, métricas e resultados de anomalias podem ser exportados em um formato PDF profissional.  
- Relatórios combinam **visualizações** e **dados subjacentes** para atender tanto usuários técnicos quanto de negócio.  
- Elimina a necessidade de ferramentas externas para criação de relatórios.  

---

### Novo tipo de coluna: `CUSTOM`
Para oferecer mais flexibilidade, o digna introduz um novo **tipo de coluna `CUSTOM`**.  

- Usuários podem definir exatamente quais **estatísticas e métricas** são aplicadas a atributos específicos.  
- Perfeito para casos especiais que não se encaixam em categorias padrão como NUMERICAL ou CATEGORICAL.  
- Ajuda a manter as análises focadas e os resultados relevantes ao contexto de negócio.  

---

### Novos espaços reservados em consultas de snapshot
As consultas de snapshot agora são mais simples e menos propensas a erros com **placeholders dinâmicos**.  

- Tokens como `#date+n#` ou `#date-n#` ajustam automaticamente as datas nas consultas.  
- Exemplo:  
  - `#date+1#` → amanhã  
  - `#date-2#` → dois dias atrás  
- Elimina cálculos manuais de datas e garante consistência entre as equipes.  

---

### Otimização de limiares
Os limiares de anomalia agora são mais inteligentes e sensíveis ao contexto.  

- Para métricas como **NULL COUNT**, os limiares inferiores são automaticamente limitados a **0**.  
- Evita limiares inválidos ou sem sentido.  
- Resulta em menos falsos positivos e em uma detecção de anomalias mais confiável.  

---

## Melhorias gerais
- Componentes de **UI** refinados nas telas de configuração de projeto e atributo.  
- Melhor desempenho do **dashboard** para grandes volumes de dados.  
- Logs e mensagens de erro aprimorados para facilitar a solução de problemas.  

---

## Resumo
A release 2024.12 fortalece o digna como uma plataforma para **qualidade de dados, detecção de anomalias e observabilidade**.  
Com automação via agendamento, relatórios compartilháveis em PDF, colunas customizáveis, consultas de snapshot simplificadas e limiares mais inteligentes, o digna se torna ainda mais valioso tanto para usuários técnicos quanto para stakeholders de negócio.
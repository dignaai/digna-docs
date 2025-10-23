---
title: digna Release 2025.04 | Inspection Hub, Suporte multilíngue, Module Analytics
description: Saiba o que há de novo no digna Release 2025.04. Esta versão introduz o Inspection Hub, suporte multilíngue (inglês, alemão, polonês), importação/exportação de fontes de dados via dignacli, a primeira versão do Module Analytics e uma experiência de dashboard aprimorada.
keywords: digna Release 2025.04, digna changelog, digna inspection hub, digna suporte multilíngue, digna module analytics, digna import export, digna CLI, notas de versão, observabilidade de dados, monitoramento de qualidade de dados
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Registro de alterações – Release 2025.04

Com o Release 2025.04, o digna dá um grande passo para tornar a qualidade e a observabilidade de dados mais fáceis de gerenciar, mais transparentes para as equipes e acessíveis a usuários em todo o mundo.  
Esta versão combina **recursos novos e poderosos**, **melhorias na automação de fluxos de trabalho** e **refinamentos na experiência do usuário**.  

---

## Novos Recursos

### Inspection Hub – Um Novo Centro de Comando
O **Inspection Hub** já está disponível como o local central para gerenciar todos os seus jobs de inspeção. Em vez de alternar entre diferentes módulos ou depender apenas da execução via linha de comando, você agora pode monitorar e controlar suas inspeções a partir de uma interface unificada.  

Principais funcionalidades incluem:  
- Inspeções sob demanda: Inicie novos jobs instantaneamente sempre que precisar de resultados atualizados.  
- Histórico de inspeções: Veja uma linha do tempo das inspeções — o que foi executado, quem acionou e quando.  
- Acompanhamento de status: Os jobs são claramente marcados como concluídos, em progresso ou pendentes.  
- Insights do invocador: Verifique rapidamente se uma inspeção foi acionada por um usuário, pelo agendador ou pelo CLI.  
- Ferramentas de limpeza: Exclua jobs desatualizados ou desnecessários para manter seu ambiente organizado.  
- Logs detalhados: Aprofunde-se em cada job para ver quanto tempo levou, quais fontes foram incluídas e como os thresholds foram aplicados.  

O Inspection Hub fornece às equipes **visibilidade e controle de ponta a ponta**, tornando as inspeções mais fáceis de gerenciar em projetos de grande escala.  

---

### Suporte Multilíngue – digna Fala Sua Língua
digna está agora pronto para equipes internacionais com a introdução do **suporte multilíngue**.  

Nesta versão você pode definir seu **idioma de interface preferido** diretamente nas Preferências do Usuário. Os idiomas suportados incluem:  
- Inglês (UK, US, CA, AU)  
- Alemão (DE, AT, CH)  
- Polonês (PL)  

Isso torna o digna mais fácil de usar para organizações multilíngues e garante uma adoção mais suave entre equipes que trabalham em diferentes regiões. Mais idiomas serão adicionados em versões futuras.  

---

### Importação & Exportação de Fontes de Dados – Configuração Simplificada
A consistência entre ambientes é essencial em implantações corporativas. Com o 2025.04, o digna introduz a **importação/exportação de fontes de dados** via **dignacli**, a ferramenta de linha de comando para usuários avançados.  

Benefícios:  
- Exporte a configuração de uma fonte de dados uma vez e reutilize-a em Development, Test e Production.  
- Elimine reconfigurações manuais e evite erros caros.  
- Dê suporte a fluxos de trabalho automatizados e pipelines de CI/CD com comandos simples de CLI (`export-ds` e `import-ds`).  
- Copie rapidamente fontes de dados entre projetos para facilitar a colaboração.  

Essa funcionalidade assegura que as equipes possam implantar com confiança, sabendo que as configurações são consistentes em todos os ambientes.  

---

### Module Analytics (v1) – Da Detecção ao Entendimento
O digna começou como uma plataforma de detecção de anomalias e monitoramento da qualidade de dados. Com o Release 2025.04, ele evolui ainda mais com a **primeira versão do Module Analytics**.  

O Module Analytics ajuda os usuários a **entender seus dados** em vez de apenas reagir a problemas. Com este novo módulo você pode:  
- Acompanhar tendências de longo prazo em seus conjuntos de dados.  
- Detectar e monitorar volatilidade para compreender flutuações.  
- Explorar o comportamento dos dados ao longo do tempo para obter contexto mais profundo.  

Por exemplo, o digna pode destacar automaticamente que *“a contagem de linhas aumentou 15,8% desde o início do ano.”*  
Sem consultas SQL, sem verificações manuais — apenas **insights acionáveis de relance**.  

Isto é a base da jornada do digna rumo à análise avançada de dados, permitindo que as equipes de dados passem de um monitoramento reativo para um monitoramento proativo.  

---

### Melhorias no Dashboard – Uma Experiência de Uso Mais Fluida
Além dos recursos principais, o Release 2025.04 inclui vários **refinamentos no dashboard** projetados para tornar o digna mais intuitivo e agradável:  
- Navegação mais rápida entre projetos e inspeções.  
- Layout mais limpo para logs de inspeção e submissão de jobs.  
- Ajustes sutis de design que ajudam a encontrar insights mais rapidamente.  

Essas melhorias são baseadas diretamente no feedback de clientes e demonstram nosso compromisso contínuo em fazer do digna **uma plataforma construída para o uso diário**.  

---

## Melhorias Gerais
- Otimizações de performance para jobs de inspeção em grandes conjuntos de dados.  
- Tratamento de erros aprimorado no dignacli para fornecer feedback mais claro.  
- Melhorias de estabilidade para projetos com muitos jobs simultâneos.  
- Refinamentos de UI para filtragem de logs de jobs e gerenciamento de projetos.  

---

## Resumo
O Release 2025.04 trata de **controle, acessibilidade e insight**.  

- O novo **Inspection Hub** oferece aos usuários visibilidade completa sobre os jobs de inspeção.  
- O **suporte multilíngue** garante que o digna possa ser usado por equipes globais.  
- A funcionalidade de **importação/exportação** simplifica o gerenciamento de configurações entre ambientes.  
- **Module Analytics (v1)** desloca o foco da detecção para o entendimento, com acompanhamento de tendências e volatilidade.  
- **Melhorias no dashboard** refinam a experiência geral do usuário.  

Juntas, essas atualizações tornam o digna mais poderoso, fácil de usar e pronto para o ambiente internacional como nunca antes.
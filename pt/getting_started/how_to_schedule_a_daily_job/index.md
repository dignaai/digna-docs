# Como agendar um job diário

Scheduling permite executar inspeções automaticamente, sem intervenção manual.  
Neste guia, você aprenderá como criar um job que é executado **uma vez por dia**, garantindo que seus dados sejam monitorados continuamente.

---

## Demonstração interativa

Siga o tutorial interativo para ver o processo em ação:  

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/Ra9E19A0QfMpzKqm3Yhu?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a New Data Inspection Job" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## O que você vai aprender

- Como acessar a seção **Scheduling** no dashboard do digna  
- Como criar um novo job agendado  
- Como configurá-lo para rodar **diariamente em um horário fixo**  
- Como selecionar o projeto e o datasource corretos  
- Como ativar o job para que ele seja executado automaticamente  

---

## Por que jobs diários são úteis

O agendamento diário é a configuração mais comum em ambientes de produção. Ele garante:  

- **Atualidade** — os dados de cada dia são validados.  
- **Consistência** — as anomalias são detectadas cedo, antes de se propagarem a sistemas a jusante.  
- **Automação** — não é necessário disparar inspeções manualmente.  

---

## Próximos passos

- Explore [Como usar definições crontab](how_to_use_crontab.md) para agendamentos personalizados mais avançados.  
- Combine jobs diários com **alerting** para receber notificações quando anomalias forem detectadas.
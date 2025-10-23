---
title: Agendamento Avançado com Crontab
description: Aprenda a agendar um job no digna usando expressões crontab para agendamento avançado.
---

# Agendamento Avançado com Crontab

Este guia mostra como agendar jobs no *digna* usando **expressões crontab**.  
Ao contrário dos padrões pré-definidos (diário, semanal, mensal), o crontab oferece total flexibilidade para definir agendamentos personalizados.

---

## Demonstração Interativa

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## O que você vai aprender

- Como abrir a seção **Scheduling** no dashboard  
- Como criar um novo job usando uma **expressão crontab**  
- Como definir um agendamento que execute somente nos **fins de semana às 10:00**  

---

## Exemplo: Agendamento de Fim de Semana

Para agendar um job para executar todo **sábado e domingo às 10:00**, use a seguinte expressão:


- `0` → minuto (na hora cheia)  
- `10` → hora (10:00)  
- `*` → todo dia do mês  
- `*` → todo mês  
- `sat,sun` → somente aos sábados e domingos  

---

## Por que usar o Crontab?

- Crie agendamentos além dos padrões diários, semanais ou mensais  
- Defina horários de execução precisos (dias específicos, horas ou intervalos)  
- Útil para jobs de fim de semana, verificações fora do horário comercial ou monitoramento frequente  

---
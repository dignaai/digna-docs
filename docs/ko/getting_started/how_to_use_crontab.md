---
title: Crontab을 이용한 고급 스케줄링
description: crontab 표현식을 사용해 digna에서 고급 타이밍으로 작업을 예약하는 방법을 알아보세요.
---

# Advanced Scheduling with Crontab

This guide shows how to schedule jobs in *digna* using **crontab expressions**.  
Unlike the standard patterns (daily, weekly, monthly), crontab gives you full flexibility to define custom schedules.

---

## Interactive Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## What You Will Learn

- 대시보드에서 **Scheduling** 섹션을 여는 방법  
- **crontab 표현식**을 사용해 새 작업을 만드는 방법  
- 오직 **주말 오전 10시에**만 실행되도록 스케줄을 설정하는 방법  

---

## Example: Weekend Schedule

To schedule a job to run every **Saturday and Sunday at 10:00 AM**, use the following expression:


- `0` → 분 (정시)  
- `10` → 시간 (오전 10시)  
- `*` → 월의 모든 날짜  
- `*` → 매월  
- `sat,sun` → 토요일과 일요일에만  

---

## Why Use Crontab?

- 표준 일간, 주간, 월간 패턴을 넘어선 스케줄 생성  
- 정확한 실행 시간 정의(특정 요일, 시간 또는 간격)  
- 주말 작업, 비업무시간 점검, 또는 빈번한 모니터링에 유용  

---
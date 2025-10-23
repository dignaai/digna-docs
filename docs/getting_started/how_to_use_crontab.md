---
title: Advanced Scheduling with Crontab
description: Learn how to schedule a job in digna using crontab expressions for advanced timing.
---

# Advanced Scheduling with Crontab

This guide shows how to schedule jobs in *digna* using **crontab expressions**.  
Unlike the standard patterns (daily, weekly, monthly), crontab gives you full flexibility to define custom schedules.

---

## Interactive Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## What You Will Learn

- How to open the **Scheduling** section in the dashboard  
- How to create a new job using a **crontab expression**  
- How to set a schedule that runs only on **weekends at 10:00**  

---

## Example: Weekend Schedule

To schedule a job to run every **Saturday and Sunday at 10:00 AM**, use the following expression:


- `0` → minute (on the hour)  
- `10` → hour (10 AM)  
- `*` → every day of the month  
- `*` → every month  
- `sat,sun` → only on Saturdays and Sundays  

---

## Why Use Crontab?

- Create schedules beyond standard daily, weekly, or monthly patterns  
- Define precise run times (specific days, hours, or intervals)  
- Useful for weekend jobs, off-hours checks, or frequent monitoring  

---

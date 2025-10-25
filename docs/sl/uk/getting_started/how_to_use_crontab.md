---
title: Napredno razporejanje z uporabo crontab
description: Izvedite, kako razporejati naloge v digna z uporabo crontab expressions za napredno nastavitev časa.
---

# Napredno razporejanje z uporabo crontab

Ta vodnik prikazuje, kako v *digna* razporediti naloge z uporabo **crontab expressions**.  
V nasprotju s standardnimi predlogami (dnevno, tedensko, mesečno) crontab omogoča popolno prilagodljivost pri določanju lastnih urnikov.

---

## Інтерактивна демонстрація

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Zakaj se boste tega naučili

- Kako odpreti razdelek **Scheduling** na nadzorni plošči  
- Kako ustvariti novo nalogo z uporabo **crontab expression**  
- Kako nastaviti urnik, ki se zažene le med **vikendi ob 10:00**  

---

## Primer: urnik za vikende

Da načrtujete nalogo, ki se bo izvajala vsako **soboto in nedeljo ob 10:00 zjutraj**, uporabite naslednji izraz:


- `0` → minuta (na začetku ure)  
- `10` → ura (10:00)  
- `*` → vsak dan v mesecu  
- `*` → vsak mesec  
- `sat,sun` → samo v soboto in nedeljo  

---

## Zakaj uporabljati crontab?

- Ustvarjati urnike, ki presegajo standardne dnevne, tedenske ali mesečne predloge  
- Določiti natančen čas zagona (konkretni dnevi, ure ali intervali)  
- Koristno za naloge ob vikendih, preverjanja izven delovnega časa ali pogosto spremljanje  

---
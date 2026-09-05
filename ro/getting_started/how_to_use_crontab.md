# Planificare Avansată cu Crontab

Acest ghid arată cum să programezi joburi în *digna* folosind **expresii crontab**.  
Spre deosebire de tiparele standard (daily, weekly, monthly), crontab îți oferă flexibilitate completă pentru a defini programări personalizate.

---

## Demo interactiv

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Programează un job de date cu un timp de execuție personalizat" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Ce vei învăța

- Cum să deschizi secțiunea **Scheduling** din dashboard  
- Cum să creezi un job nou folosind o **expresie crontab**  
- Cum să setezi un program care rulează doar în **weekend la 10:00**  

---

## Exemplu: Program pentru weekend

Pentru a programa un job să ruleze în fiecare **sâmbătă și duminică la 10:00**, folosește următoarea expresie:


- `0` → minut (la începutul orei)  
- `10` → oră (10:00)  
- `*` → în fiecare zi a lunii  
- `*` → în fiecare lună  
- `sat,sun` → doar sâmbătă și duminică  

---

## De ce să folosești Crontab?

- Creează programe dincolo de tiparele standard daily, weekly sau monthly  
- Definește ore precise de rulare (zile specifice, ore sau intervale)  
- Util pentru joburi de weekend, verificări în afara orelor de lucru sau monitorizare frecventă  

---
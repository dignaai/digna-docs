# Napredno razporejanje s crontab

Ta vodič prikazuje, kako v *digna* razporediti opravila z uporabo **crontab izrazov**.  
Za razliko od standardnih vzorcev (dnevno, tedensko, mesečno) crontab omogoča popolno prilagodljivost pri opredelitvi lastnih urnikov.

---

## Interactive Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## What You Will Learn

- How to open the **Scheduling** section in the dashboard  
- How to create a new job using a **crontab izraz**  
- How to set a schedule that runs only on **weekends at 10:00**  

---

## Primer: urnik za vikende

Če želite razporediti opravilo, da se izvaja vsako **soboto in nedeljo ob 10:00**, uporabite naslednji izraz:


- `0` → minuta (na polni uri)  
- `10` → ura (10:00)  
- `*` → vsak dan v mesecu  
- `*` → vsak mesec  
- `sat,sun` → samo ob sobotah in nedeljah  

---

## Zakaj uporabiti crontab?

- Ustvarjajte urnike, ki presegajo standardne dnevne, tedenske ali mesečne vzorce  
- Določite natančne čase izvajanja (specifični dnevi, ure ali intervali)  
- Uporabno za opravila ob vikendih, preverjanja izven delovnega časa ali pogosto spremljanje  

---
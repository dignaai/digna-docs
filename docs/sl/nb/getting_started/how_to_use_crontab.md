---
title: Napredno načrtovanje s crontab
description: Naučite se, kako v digna načrtovati opravilo z uporabo crontab-izrazov za napredne urnike.
---

# Napredno načrtovanje s crontab

Ta vodnik prikazuje, kako v *digna* načrtovati opravila z uporabo **crontab-izrazov**.  
Za razliko od privzetih vzorcev (dnevno, tedensko, mesečno) vam crontab nudi popolno prilagodljivost pri opredeljevanju lastnih urnikov.

---

## Interaktivna predstavitev

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## To se boste naučili

- Kako odpreti **Scheduling**-razdelek na nadzorni plošči  
- Kako ustvariti novo opravilo z uporabo **crontab-izraza**  
- Kako nastaviti urnik, ki teče samo **ob koncih tedna ob 10:00**  

---

## Primer: Vikend urnik

Če želite načrtovati opravilo, ki se izvaja vsako **soboto in nedeljo ob 10:00**, uporabite naslednji izraz:


- `0` → minuta (na polno uro)  
- `10` → ura (ob 10:00)  
- `*` → vsak dan v mesecu  
- `*` → vsak mesec  
- `sat,sun` → le ob sobotah in nedeljah  

---

## Zakaj uporabljati crontab?

- Ustvarite urnike, ki presegajo privzete dnevne, tedenske ali mesečne vzorce  
- Določite natančne čase izvajanja (specifični dnevi, ure ali intervali)  
- Uporabno za opravila ob koncu tedna, preverjanja izven delovnega časa ali pogosto spremljanje  

---
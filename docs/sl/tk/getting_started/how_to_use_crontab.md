---
title: Napredno razporejanje s Crontab
description: Naučite se, kako z izrazi crontab v digna načrtovati opravilo za napredna razporejanja.
---

# Napredno razporejanje s crontab

Ta vodnik prikazuje, kako v *digna* z uporabo **crontab izrazov** razporediti opravila.  
V nasprotju s standardnimi vzorci (dnevni, tedenski, mesečni) crontab zagotavlja popolno prilagodljivost pri določanju lastnih razporedov.

---

## Interaktivni demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Kaj se boste naučili

- Kako odpreti razdelek **Razporejanje** na nadzorni plošči  
- Kako ustvariti novo opravilo z uporabo **crontab izraza**  
- Kako nastaviti razpored, ki bo deloval samo **ob koncih tedna ob 10:00**  

---

## Primer: razpored ob koncu tedna

Uporabite naslednji izraz za razporeditev opravila tako, da se bo izvajalo vsak **soboto in nedeljo ob 10:00**:


- `0` → minuta (na začetku ure)  
- `10` → ura (10:00)  
- `*` → vsak dan v mesecu  
- `*` → vsak mesec  
- `sat,sun` → samo sobota in nedelja  

---

## Zakaj uporabljati crontab?

- Ustvarite razporede, ki presegajo standardne vzorce (dnevni, tedenski, mesečni)  
- Opredelite natančne čase izvajanja (določeni dnevi, ure ali intervali)  
- Uporabno za naloge ob koncu tedna, preglede izven delovnega časa ali pogosto spremljanje  

---
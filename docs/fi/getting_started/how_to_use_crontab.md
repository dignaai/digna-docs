---
title: Edistynyt ajastus Crontabilla
description: Opi ajastamaan tehtävä dignassa käyttämällä crontab-ilmaisuja edistyneisiin ajoituksiin.
image: /assets/logo_square.png
---

# Edistynyt ajastus Crontabilla

Tässä oppaassa näytetään, miten ajastetaan tehtäviä *digna*:ssa käyttämällä **crontab-ilmaisuja**.  
Toisin kuin vakiomallit (päivittäin, viikoittain, kuukausittain), crontab antaa täydet mahdollisuudet määritellä räätälöityjä aikatauluja.

---

## Interaktiivinen demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Mitä opit

- Miten avata hallintapaneelin **Scheduling**-osio  
- Miten luoda uusi tehtävä käyttäen **crontab-ilmausta**  
- Miten asettaa aikataulu, joka suoritetaan vain **viikonloppuisin klo 10:00**  

---

## Esimerkki: viikonloppuaikataulu

Ajastaaksesi tehtävän suoritettavaksi joka **lauantai ja sunnuntai klo 10:00**, käytä seuraavaa ilmausta:


- `0` → minuutti (tasalta)  
- `10` → tunti (klo 10)  
- `*` → joka kuukauden päivä  
- `*` → joka kuukausi  
- `sat,sun` → vain lauantaisin ja sunnuntaisin  

---

## Miksi käyttää crontabia?

- Luo aikatauluja tavanomaisten päivittäisten, viikoittaisten tai kuukausittaisten mallien ulkopuolelle  
- Määritä tarkat suoritusajat (tietyt päivät, tunnit tai aikavälit)  
- Hyödyllinen viikonlopputehtäville, työajan ulkopuolisille tarkistuksille tai tiheälle seurannalle  

---
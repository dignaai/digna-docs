---
title: digna Išleidimas 2026.01 | Loginiai duomenų šaltiniai, globalios jungtys ir išplėstinė Data Validation
description: Sužinokite, kas naujo digna Išleidime 2026.01. Ši versija pristato globalias duomenų bazės jungtis, loginius duomenų šaltinius, anomalijų reikšmingumo sąlygas, CSV eksporto galimybę ir išplėstinę Data Validation, įskaitant nuorodų vientisumo patikras.
keywords: digna Išleidimas 2026.01, digna pakeitimų žurnalas, digna duomenų šaltinis, digna duomenų bazės jungtys, digna Data Anomalies, digna Data Validation, nuorodų vientisumo tikrinimas, duomenų kokybės taisyklės, duomenų stebėjimas, digna CSV eksportas
image: /assets/logo_square.png
---

# Keitimų žurnalas – Išleidimas 2026.01  

Su Išleidimu 2026.01 digna pristato esminių patobulinimų duomenų šaltinių modeliavimui, jungčių valdymui ir inspekcijų naudojimo patogumui.  
Šis leidimas didina lankstumą visuose moduliuose ir reikšmingai plečia **duomenų kokybės ir validacijos aprėptį**.

---

## 🚀 Naujos funkcijos  

### Globalios duomenų bazės jungtys  
- Dabar duomenų bazės jungtys konfigūruojamos **globaliu lygiu**.  
- Globalios jungtys gali būti pakartotinai naudojamos **visuose projektuose**, supaprastinant konfigūravimą ir priežiūrą.  
- **Poveikis:** Mažina operacinę naštą ir užtikrina nuoseklų prijungimą skirtingose aplinkose.

### Keli šaltinių jungčių konfigūravimai projekte  
- Projektai dabar gali nurodyti **kelias šaltinio jungčių konfigūracijas**.  
- Leidžia sudėtingesnėms duomenų aplinkoms lankstesnius nustatymus.  
- **Poveikis:** Palaiko realistiškas įmonių architektūras su heterogeniniais duomenų šaltiniais.

### Loginiai duomenų šaltiniai  
- Duomenų šaltiniai dabar atstovauja **loginį sluoksnį** projekte.  
- Kiekvieną duomenų šaltinį gali palaikyti:
    - **duomenų bazės lentelė**
    - **duomenų bazės vaizdas (view)**
    - **vartotojo aprašyta SQL užklausa**  
- Šis atskyrimas gerina pakartotinį panaudojimą, aiškumą ir inspekcijų modeliavimą visuose moduliuose.  
- **Poveikis:** Atskiria inspekcijas ir duomenų kokybės taisykles nuo fizinio saugojimo, gerindamas prižiūrimumą ir pakartotinį panaudojimą.

### Anomalijos reikšmingumo sąlyga  
- Dabar galima apibrėžti **Anomalijos reikšmingumo sąlygą**, kuri kontroliuoja anomalijos būsenos vertinimą duomenų rinkinio lygyje.  
- Statistikos skaičiuojamos nepriklausomai nuo to, ar sąlyga nustatyta arba ar ji tenkinama.  
- Jeigu sąlyga **nėra tenkinama**, **digna Data Anomalies** nepateikia anomalijos būsenos (žalia / geltona / raudona).  
- **Pavyzdys:** Išskirti duomenų rinkinį iš anomalijų vertinimo, kai įrašų skaičius yra mažesnis nei 10.  
- **Poveikis:** Užtikrina, kad anomalijos vertinamos tik reikšminguose verslo kontekstuose.

### Pranešimų konfigūravimas pagal modulį  
- Pranešimus dabar galima konfigūruoti **kiekvienam moduliui atskirai** tiesiog digna aplinkoje.  
- Leidžia nepriklausomai valdyti įspėjimų elgseną moduliams, tokiems kaip **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** ir kitiems.  
- **Poveikis:** Leidžia tiksliai nustatyti įspėjimų strategijas, suderintas su komandos atsakomybėmis ir kritiškumu.

### Inspekcijų rezultatų eksportas (CSV)  
- Vartotojai dabar gali **parsisiųsti inspekcijų rezultatus CSV failais**.  
- Leidžia atlikti neprisijungusią analizę, rengti ataskaitas ir integruoti su išoriniais įrankiais.  
- **Poveikis:** Supaprastina auditus, ataskaitų rengimą ir tolimesnę duomenų kokybės analizę.

---

## 🧪 Išplėstos Data Validation galimybės  

Su šiuo leidimu **digna Data Validation** dabar palaiko išsamų duomenų kokybės taisyklių rinkinį:

- **Eilučių lygio validacijos taisyklės**  
- **Unikalumo patikros keliems stulpeliams**  
- **Nuorodų vientisumo patikros tarp duomenų šaltinių**

Šios patikros kartu leidžia taikyti **struktūrines ir relacines duomenų kokybės taisykles** sudėtingose duomenų aplinkose.

### Unikalumo patikros keliems stulpeliams
- Pridėtos **Unikalumo patikros** konfigūruojamai **stulpelių grupei**.  
- Leidžia tikrinti sudėtinius raktus ir verslo lygmens unikalumo apribojimus.  
- **Poveikis:** Aptinka pasikartojančias verslo entitetų reikšmes, kurių negalima identifikuoti vieno stulpelio patikromis.

### Nuorodų vientisumo patikros
- Pridėtos **Nuorodų vientisumo patikros**, skirtos tikrinti ryšius tarp duomenų šaltinių.  
- Užtikrina, kad **užsieninio rakto reikšmės** šaltinio duomenų rinkinyje egzistuotų nurodytame tikslo duomenų rinkinyje.  
- Padeda anksti aptikti apleistus įrašus, nutrūkusius ryšius ir duomenų nuoseklumo problemas.  
- Sukurta taip, kad veiktų su **loginiais duomenų šaltiniais**, įskaitant vaizdus ir vartotojo aprašytą SQL.  
- **Panaudojimo atvejai:** duomenų sandėlio vientisumas, reglamentavimui skirtos ataskaitos, pagrindinių duomenų nuoseklumas ir patikima tolimesnė analizė.

---

## 🎯 Kam naudingas šis leidimas  

- **Duomenų inžinieriams:** lankstesnis duomenų šaltinių modeliavimas ir pakartotinai naudojamos duomenų bazės jungtys  
- **Duomenų kokybės ir valdymo komandoms:** išplėsta validacijos aprėptis, įskaitant relacinius vientisumo patikrinimus  
- **Analitikų ir BI komandų nariams:** švaresni įvesties duomenys ir eksportuojami inspekcijų rezultatai  
- **Platformos savininkams:** sumažėjo konfigūracijos sudėtingumas ir pagerėjo operacinis prižiūrimumas

---

## 🛠 CLI atnaujinimai  
- Nėra pakeitimų

---
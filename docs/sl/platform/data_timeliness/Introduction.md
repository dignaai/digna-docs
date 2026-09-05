---
title: Data Timeliness – Spremljanje pravočasne dostave | digna Dokumentacija
description: Izvedite, kako digna Data Timeliness zagotavlja, da podatki prispejo pravočasno. Zaznajte zamude ali manjkajoče dostave, spremljajte SLA in zaščitite poslovne procese pred tihimi zamudami. AI-podprta zaznava za izboljšano kakovost podatkov in opaznost podatkovnih tokov.
image: /assets/logo_square.png
keywords:
  - časovna pravočasnost podatkov
  - spremljanje dostave
  - kakovost podatkov
  - kvaliteta podatkov
  - opaznost podatkov
  - zaznavanje zamud podatkov
  - opozarjanje na manjkajoče podatke
  - spremljanje SLA
  - AI analiza dostave
  - digna data timeliness
lang: en
robots: index, follow
og_title: Data Timeliness – Spremljanje pravočasne dostave | digna Dokumentacija
og_description: digna Data Timeliness samodejno zaznava zamujene ali manjkajoče dostave podatkov z uporabo AI. Zaščitite poslovne procese, spremljajte SLA in zagotovite pravočasne, zanesljive podatke v vseh podatkovnih cevovodih.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – Spremljanje pravočasne dostave
<h1 style="display:none;">AI-podprt modul Data Timeliness za kakovost podatkov in opaznost – digna</h1>

---

## Namen

Modul **Data Timeliness** zagotavlja, da **podatki prispejo pravočasno** — vsakič.  
Nenehno spremlja urnike dostave in samodejno zaznava, kdaj so podatkovni nizi, tabele ali datoteke **zamujeni, manjkajoči ali nepopolni**.  

Z združevanjem AI učenja in uporabniško določenih urnikov *digna* omogoča organizacijam preprečevanje napak v nižjih slojih in izpolnjevanje strogih ciljev **SLA (Service Level Agreement)** tako za **kakovost podatkov** kot za **opaznost podatkovnih cevovodov**.

---

## Tehnični pregled

### Dvojni načini spremljanja
- **AI-učeni vzorci prihoda**  
  digna samodejno uči naravni ritem vaših dobav podatkov — dnevno, na uro ali sproženo z dogodki — z analizo zgodovinskih časovnih žigov in časov dokončanja.  
  Prilagaja se spremembam v poslovnih koledarjih, vikendih ali koncih meseca.

- **Uporabniško določeni urniki**  
  Uporabniki lahko izrecno določijo pričakovane čase dostave (npr. *vsak delovni dan pred 7:30*).  
  digna primerja dejanski čas prihoda s načrtovanim urnikom in sproži opozorila, kadar so podatki zamujeni ali manjkajo.

### Mehanizem zaznavanja
- Ocenjuje **časovne žige v metadatah**, **število zapisov** in **svežino tabel**  
- Zaznava **zagozdene ETL opravke**, **neuspešne ekstrakcije** in **delne prihode datotek**  
- Integrira se z *Data Anomalies* in *Data Validation* za kombinirane vpoglede

---

## Scenariji zaznavanja

| Scenario | Opis |
|-----------|--------------|
| **Zamuda pri prihodu podatkov** | Dnevni napajalnik tržnih podatkov zamujal za dve uri, zaradi česar poročila niso izpolnila SLA |
| **Manjkajoči nalaganje** | Načrtovana tabela ali particija ni bila posodobljena za tekoči datum |
| **Zamik v verigi odvisnosti** | Zamuda zgornjega opravka vpliva na osvežitev spodnjega cevovoda |
| **Premik vzorca za vikend** | AI model se samodejno prilagodi, ko se ob nedeljah ne pričakuje podatkov |

---

## Arhitektura in izvajanje

- **Izvajanje v podatkovni zbirki:** digna izvaja preverjanja pravočasnosti neposredno v vaši podatkovni zbirki ali podatkovnem skladišču.  
- **Lahkoten dostop do metadata:** bere časovne žige opravil, števila zapisov in informacije o particijah — brez potrebe po izvleku podatkov.  
- **Konfigurabilna frekvenca:** načrtovanje spremljanja po podatkovnem nizu, shemi ali cevovodu.  
- **Opozorila med moduli:** rezultati lahko sprožijo vizualna opozorila v *Inspection Hub* ali obvestila po elektronski pošti, Slacku ali prek API.

---

## Primeri uporabe

- **Finančni tržni podatki:** zaznava zamude pri posodobitvah cen ali trgovinskih podatkov.  
- **Nalaganje v podatkovno skladišče:** spremljanje, kdaj nočni ETL postopki končajo pozneje kot pričakovano.  
- **Izmenjava podatkov med ekipami:** zagotavljanje, da oddelčne dobave podatkov pridejo pred dnevnim rokom.  
- **Regulatorno poročanje:** potrditev, da predložitve vključujejo najnovejši razpoložljivi posnetek podatkov.

---

## Koristi

| Področje | Korist |
|------|----------|
| **Poslovna kontinuiteta** | Preprečuje operativne prekinitev zaradi zamujenih ali manjkajočih podatkov |
| **Kakovost podatkov** | Izboljšuje zanesljivost in doslednost podatkovnih cevovodov |
| **Skladnost** | Zagotavlja spoštovanje SLA in preglednost za revizije |
| **Avtomatizacija** | AI odpravlja ročno spremljanje urnikov |
| **Integracija** | Deluje brezhibno z *Data Analytics* za vizualizacijo trendov pravočasnosti skozi čas |

---

## Kako digna uči pričakovane čase dostave

1. **Zgodovinska analiza:** digna opazuje prejšnje čase nalaganja in trajanja.  
2. **AI modeliranje:** strojno učenje ustvari dinamično osnovo za pričakovani prihod.  
3. **Spremljanje:** Vsaka nova dostava se primerja z osnovo.  
4. **Opozarjanje:** Odstopanja sprožijo opozorila s kontekstualnimi metričnimi podatki in ocenami zanesljivosti.  

Ta pristop nenehnega učenja se prilagaja razvijajočim se procesom in obenem ohranja nizko število lažnih pozitivnih zaznav.

---

## Pogosto zastavljena vprašanja

**Ali lahko določim svoje čase dostave?**  
Da. digna podpira tako fiksne uporabniške urnike kot AI-učene vzorce.

**Se lahko integrira z mojim ETL ali orkestracijskim orodjem?**  
Da. digna se integrira z orodji, kot so Airflow, dbt, Informatica ali z lastnimi načrtovalniki.

**Kje se izvaja izračun?**  
Vsa analiza teče znotraj vaše podatkovne zbirke ali oblačnega skladišča — brez uporabe zunanje storitve.

**Kaj se zgodi, ko so podatki zamujeni?**  
digna sproži opozorila na nadzorni plošči, v Inspection Hub in preko API/webhookov, da takoj obvesti operativne ekipe.

---


**digna Data Timeliness** pomaga zagotoviti **zaupanje v podatke**, združuje **AI-podprto zaznavanje**, **izvajanje v lastnem okolju** in **opaznost podatkov** — vse v vašem nadzorovanem okolju.
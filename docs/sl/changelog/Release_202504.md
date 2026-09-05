---
title: digna Release 2025.04 | Inspection Hub, večjezičnost, Module Analytics
description: Spoznajte novosti v digna izdaji 2025.04. Ta različica uvaja Inspection Hub, večjezično podporo (angleščina, nemščina, poljščina), uvoz/izvoz virov podatkov preko dignacli, prvo izdajo Module Analytics in izboljšano izkušnjo nadzorne plošče.
keywords: digna Release 2025.04, digna changelog, digna inspection hub, digna multi-language support, digna module analytics, digna import export, digna CLI, release notes, data observability, data quality monitoring
image: /assets/logo_square.png
---

# Zapis sprememb – izdaja 2025.04

Z izdajo 2025.04 digna naredi velik korak naprej pri poenostavljanju upravljanja kakovosti podatkov in opazovanja podatkov, poveča preglednost za ekipe in omogoči dostop uporabnikom po vsem svetu.  
Ta izdaja združuje **močne nove funkcije**, **izboljšave avtomatizacije delovnih tokov** in **prilagoditve uporabniške izkušnje**.  

---

## Nove funkcije

### Inspection Hub – nov ukazni center
**Inspection Hub** je zdaj na voljo kot osrednje mesto za upravljanje vseh vaših inšpekcijskih opravil. Namesto skakanja med različnimi moduli ali zanašanja izključno na izvajanje iz ukazne vrstice, lahko zdaj spremljate in nadzorujete inšpekcije iz enotnega, poenostavljenega vmesnika.  

Ključne zmožnosti vključujejo:  
- Inšpekcije na zahtevo: Zaženite nova opravila takoj, ko potrebujete sveže rezultate.  
- Zgodovina inšpekcij: Oglejte si časovnico inšpekcij — kaj je bilo zagnano, kdo je sprožil in kdaj.  
- Spremljanje statusa: Opravila so jasno označena kot dokončana, v teku ali čakajoča.  
- Vpogledi v sprožitelje: Hitro preverite, ali je inšpekcijo sprožil uporabnik, razporejevalnik ali CLI.  
- Orodja za čiščenje: Izbrišite zastarela ali nepotrebna opravila, da bo vaše delovno okolje urejeno.  
- Podrobni dnevniki: Poglobite se v vsako opravilo in si oglejte, koliko je trajalo, kateri viri so bili vključeni in kako so bile uporabljene meje (thresholds).  

Inspection Hub ekipam zagotavlja **vidnost in nadzor od začetka do konca**, zaradi česar je upravljanje inšpekcij lažje tudi pri velikih projektih.  

---

### Večjezičnost – digna govori vaš jezik
digna je zdaj pripravljena za mednarodne ekipe z uvedbo **večjezične podpore**.  

V tej izdaji lahko v **Uporabniških nastavitvah (User Preferences)** nastavite svoj **želeni jezik vmesnika**. Podprti jeziki vključujejo:  
- Angleščina (UK, US, CA, AU)  
- Nemščina (DE, AT, CH)  
- Poljščina (PL)  

To omogoča lažjo uporabo digne v večjezičnih organizacijah in zagotavlja bolj gladko sprejetje med ekipami v različnih regijah. V prihodnjih izdajah bomo dodali še več jezikov.  

---

### Uvoz in izvoz virov podatkov – poenostavljena konfiguracija
Doslednost med okolji je ključna v podjetniških nameščanjih. Z izdajo 2025.04 digna uvaja **uvoz/izvoz virov podatkov** preko orodja **dignacli**, ukazne vrstice za napredne uporabnike.  

Prednosti:  
- Izvozite konfiguracijo vira podatkov enkrat in jo ponovno uporabite v Razvoju, Testiranju in Produkciji.  
- Odpravite ročne ponastavitve in zmanjšajte drage napake.  
- Podprite avtomatizirane delovne tokove in CI/CD cevi s preprostimi ukazi CLI (`export-ds` in `import-ds`).  
- Hitro kopirajte vire podatkov med projekti za lažje sodelovanje.  

Ta funkcionalnost zagotavlja, da ekipe lahko nameščajo z zaupanjem, saj vedo, da so konfiguracije dosledne v vsakem okolju.  

---

### Module Analytics (v1) – od odkrivanja k razumevanju
digna se je začela kot platforma za odkrivanje anomalij in spremljanje kakovosti podatkov. Z izdajo 2025.04 se še naprej razvija z **prvo različico Module Analytics**.  

Module Analytics pomaga uporabnikom **razumeti njihove podatke**, ne le reagirati na težave. S tem novim modulom lahko:  
- Spremljate dolgoročne trende v vaših nizih podatkov.  
- Odkrijete in spremljate volatilnost za razumevanje nihanj.  
- Raziščete vedenje podatkov skozi čas za globlji kontekst.  

Na primer, digna lahko samodejno izpostavi, da *“število vrstic se je od začetka leta povečalo za 15,8 %.”*  
Brez SQL poizvedb, brez ročnih preverjanj — le **ukrepljivi vpogledi na prvi pogled**.  

To je temelj digne na poti k napredni analitiki podatkov, ki ekipam omogoča premik iz reaktivnega v proaktivno spremljanje.  

---

### Izboljšave nadzorne plošče – bolj tekoča uporabniška izkušnja
Poleg glavnih funkcij izdaja 2025.04 vključuje več **izboljšav nadzorne plošče**, zasnovanih za bolj intuitivno in prijetno uporabo digne:  
- Hitrejša navigacija med projekti in inšpekcijami.  
- Čistejša postavitev za dnevnike inšpekcij ter oddajo opravil.  
- Subtilne oblikovne prilagoditve, ki pomagajo hitreje najti vpoglede.  

Te izboljšave temeljijo neposredno na povratnih informacijah strank in kažejo našo stalno zavezanost k temu, da je digna **platforma za vsakodnevno uporabo**.  

---

## Splošne izboljšave
- Optimizacije zmogljivosti za inšpekcijska opravila na velikih naborih podatkov.  
- Izboljšano ravnanje z napakami v dignacli za jasnejša sporočila.  
- Izboljšave stabilnosti pri projektih z veliko sočasnimi opravili.  
- Prilagoditve uporabniškega vmesnika za filtriranje dnevnikov opravil in upravljanje projektov.  

---

## Povzetek
Izdaja 2025.04 pomeni **nadzor, dostopnost in vpoglede**.  

- Novi **Inspection Hub** uporabnikom daje popoln pregled nad inšpekcijskimi opravili.  
- **Večjezična podpora** zagotavlja, da je digna uporabna za globalne ekipe.  
- Funkcionalnost **uvoza/izvoza** poenostavlja upravljanje konfiguracij med okolji.  
- **Module Analytics (v1)** premika fokus iz odkrivanja k razumevanju z zbiranjem trendov in spremljanjem volatilnosti.  
- **Izboljšave nadzorne plošče** izpopolnjujejo splošno uporabniško izkušnjo.  

Skupaj te posodobitve naredijo digno močnejšo, bolj prijazno do uporabnika in mednarodno pripravljeno kot kdajkoli prej.
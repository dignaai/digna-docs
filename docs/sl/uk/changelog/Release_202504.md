---
title: digna Izdaja 2025.04 | Inspection Hub, večjezičnost, Module Analytics
description: Odkrijte novosti v izdaji digna 2025.04. V tej različici predstavljamo Inspection Hub, podporo več jezikom (angleščina, nemščina, poljščina), uvoz/izvoz virov podatkov prek dignacli, prvo izdajo Module Analytics in izboljšano izkušnjo nadzorne plošče.
keywords: digna Izdaja 2025.04, digna changelog, digna inspection hub, digna večjezičnost, digna module analytics, digna import export, digna CLI, release notes, data observability, spremljanje kakovosti podatkov
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Changelog – Izdaja 2025.04

V izdaji 2025.04 digna naredi velik korak naprej pri poenostavitvi upravljanja kakovosti podatkov in opaznosti za ekipe po vsem svetu.  
Ta izdaja združuje **moč nove funkcionalnosti**, **izboljšave avtomatizacije delovnih tokov** in **izboljšano uporabniško izkušnjo**.  

---

## Novosti

### Inspection Hub – nov upravljalni center
**Inspection Hub** je zdaj na voljo kot osrednje mesto za upravljanje vseh vaših inspekcijskih nalog. Namesto preklapljanja med različnimi moduli ali zanašanja izključno na izvedbo iz ukazne vrstice, lahko zdaj nadzirate in upravljate preglede iz enega urejenega vmesnika.  

Glavne funkcionalnosti vključujejo:  
- Pregledi na zahtevo: zaženite nove naloge takoj, ko potrebujete sveže rezultate.  
- Zgodovina pregledov: oglejte si kronologijo pregledov — kaj je bilo izvedeno, kdo je to sprožil in kdaj.  
- Sledenje stanja: naloge so jasno označene kot zaključene, v teku ali v čakanju.  
- Podatki o iniciatorju: hitro preverite, ali je pregled sprožil uporabnik, razporejevalnik ali CLI.  
- Orodja za čiščenje: izbrišite zastarele ali nepotrebne naloge, da ohranite delovni prostor urejen.  
- Podrobni dnevniki: poglobite se v posamezno nalogo, da vidite trajanje izvajanja, kateri viri so bili vključeni in kako so bili uporabljeni pragovi.  

Inspection Hub ekipam zagotavlja **vidnost in nadzor povsod**, kar poenostavi upravljanje pregledov v velikih projektih.  

---

### Večjezična podpora – digna govori vaš jezik
digna je zdaj pripravljena za mednarodne ekipe z uvedbo **večjezične podpore**.  

V tej izdaji lahko nastavitve želenega jezika vmesnika nastavite neposredno v uporabniških nastavitvah. Podprti jeziki vključujejo:  
- Angleščina (UK, US, CA, AU)  
- Nemščina (DE, AT, CH)  
- Poljščina (PL)  

To naredi digno bolj prijazno za večjezične organizacije in olajša uvajanje v ekipah, ki delajo v različnih regijah. V prihodnjih izdajah bomo dodali še več jezikov.  

---

### Uvoz in izvoz virov podatkov – lažja konfiguracija
Konsistentnost med okolji je ključna v korporativnih nameščanjih. V različici 2025.04 digna uvaja **uvoz/izvoz virov podatkov** prek **dignacli** — orodja ukazne vrstice za zahtevnejše uporabnike.  

Prednosti:  
- Izvozite konfiguracijo vira podatkov enkrat in jo nato ponovno uporabite v Development, Test in Production.  
- Odpravite ročne ponastavitve in se izognite dragim napakam.  
- Podprite avtomatizirane delovne tokove in CI/CD cevi z enostavnimi CLI ukazi (`export-ds` in `import-ds`).  
- Hitro kopirajte vire podatkov med projekti za lažje sodelovanje.  

Ta funkcionalnost zagotavlja, da se ekipe lahko uvajajo z zanesljivostjo, saj vedo, da so konfiguracije enake v vseh okoljih.  

---

### Module Analytics (v1) – od odkrivanja do razumevanja
digna se je začela kot platforma za odkrivanje anomalij in spremljanje kakovosti podatkov. V izdaji 2025.04 napreduje z **prvo različico Module Analytics**.  

Module Analytics pomaga uporabnikom **razumeti svoje podatke**, ne le reagirati na težave. S tem novim modulom lahko:  
- Spremljate dolgoročne trende v vaših podatkovnih zbirkah.  
- Odkrijete in spremljate volatilnost, da razumete nihanja.  
- Raziščete vedenje podatkov skozi čas za globlji kontekst.  

Na primer, digna lahko samodejno poudari, da *"Število vrstic se je od začetka leta povečalo za 15.8%."*  
Brez SQL-poizvedb, brez ročnih preverjanj — le **koristni vpogledi na prvi pogled**.  

To je temelj v potovanju digne proti napredni analitiki podatkov, ki ekipam omogoča prehod iz reaktivnega v proaktivno spremljanje.  

---

### Izboljšave nadzorne plošče – bolj gladka uporabniška izkušnja
Poleg glavnih funkcij izdaja 2025.04 vključuje več **izboljšav nadzorne plošče**, namenjenih temu, da naredijo digno bolj intuitivno in prijetno za uporabo:  
- Hitrejša navigacija med projekti in pregledi.  
- Čistejša postavitev za dnevnike pregledov in pošiljanje nalog.  
- Subtilne oblikovalske prilagoditve, ki pomagajo hitreje najti vpoglede.  

Te izboljšave temeljijo neposredno na povratnih informacijah strank in kažejo našo stalno zavezanost, da digna postane **platforma za vsakodnevno uporabo**.  

---

## Splošne izboljšave
- Optimizacija zmogljivosti za pregledovalna opravila pri velikih podatkovnih zbirkah.  
- Izboljšano upravljanje napak v dignacli za bolj jasne povratne informacije.  
- Povečana stabilnost za projekte z velikim številom sočasnih opravil.  
- UI-izboljšave za filtriranje dnevnikov nalog in upravljanje projektov.  

---

## Povzetek
Izdaja 2025.04 je posvečena temam **nadzora, dostopnosti in vpogledov**.  

- Novi **Inspection Hub** uporabnikom nudi popolno vidnost inspekcijskih nalog.  
- **Večjezična podpora** zagotavlja, da je digna primerna za uporabo v globalnih ekipah.  
- Funkcija **uvoza/izvoza** poenostavlja upravljanje konfiguracij med okolji.  
- **Module Analytics (v1)** premakne fokus od odkrivanja k razumevanju z možnostjo spremljanja trendov in volatilnosti.  
- **Izboljšave nadzorne plošče** izboljšujejo splošno uporabniško izkušnjo.  

Skupaj te posodobitve narekujejo, da je digna močnejša, bolj uporabniku prijazna in bolj pripravljena za mednarodno uporabo kot kdaj koli prej.
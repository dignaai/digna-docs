---
title: digna Release 2025.04 | Inspection Hub, večjezičnost, Module Analytics
description: Odkrijte, kaj je novega v digna Release 2025.04. Ta izdaja uvaja Inspection Hub, večjezično podporo (angleščina, nemščina, poljščina), uvoz/izvoz podatkovnih virov preko dignacli, prvo izdajo Module Analytics in izboljšano izkušnjo nadzorne plošče.
keywords: digna Release 2025.04, digna changelog, digna inspection hub, digna multi-language support, digna module analytics, digna import export, digna CLI, release notes, data observability, data quality monitoring
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Zapis sprememb – Release 2025.04

S izdajo Release 2025.04 digna naredi velik korak k poenostavitvi upravljanja kakovosti podatkov in opazljivosti, večji preglednosti za ekipe ter dostopnosti za uporabnike po vsem svetu.  
Ta izdaja združuje **močne nove funkcije**, **izboljšave avtomatizacije delovnih tokov** in **izpiljene uporabniške izkušnje**.  

---

## Nove funkcije

### Inspection Hub – nov nadzorni center
**Inspection Hub** je zdaj na voljo kot osrednje mesto za upravljanje vseh vaših inspekcijskih opravil. Namesto skakanja med različnimi moduli ali popolnega zanašanja na ukazno vrstico lahko zdaj spremljate in nadzorujete svoje inšpekcije iz enotnega, poenostavljenega vmesnika.  

Glavne zmogljivosti vključujejo:  
- Inšpekcije na zahtevo: Zaženite nova opravila takoj, ko potrebujete sveže rezultate.  
- Zgodovina inšpekcij: Oglejte si časovnico inšpekcij — kaj je bilo izvedeno, kdo je sprožil opravilo in kdaj.  
- Spremljanje stanja: Opravila so jasno označena kot zaključena, v teku ali v čakalnem stanju.  
- Informacije o sprožilcu: Hitro preverite, ali je bila inšpekcija sprožena s strani uporabnika, načrtovalnika ali preko CLI.  
- Orodja za čiščenje: Izbrišite zastala ali nepotrebna opravila, da ohranite delovni prostor urejen.  
- Podrobni dnevni zapisi: Pogledate lahko vsak posamezen posel, koliko časa je trajal, kateri viri so bili vključeni in kako so bile uporabljene pragovne vrednosti.  

Inspection Hub zagotavlja ekipam **vidljivost in nadzor od začetka do konca** ter poenostavlja upravljanje inšpekcij v velikih projektih.  

---

### Večjezična podpora – digna govori vaš jezik
digna je zdaj pripravljena za mednarodne ekipe z uvedbo **večjezične podpore**.  

V tej izdaji lahko v Nastavitvah uporabnika nastavite svoj **želeni jezik vmesnika**. Podprti jeziki vključujejo:  
- Angleščina (UK, US, CA, AU)  
- Nemščina (DE, AT, CH)  
- Poljščina (PL)  

To naredi digna lažjo za uporabo v večjezičnih organizacijah in pomaga zagotoviti bolj gladko prevzemanje v ekipah, ki delujejo v različnih regijah. V prihodnjih izdajah bomo dodali še več jezikov.  

---

### Uvoz in izvoz podatkovnih virov – konfiguracija poenostavljena
Konsistentnost med okolji je ključna v poslovnih namestitvah. Z izdajo 2025.04 digna uvaja **uvoz/izvoz podatkovnih virov** preko orodja **dignacli**, ukazne vrstice za napredne uporabnike.  

Prednosti:  
- Izvozite konfiguracijo podatkovnega vira enkrat in jo znova uporabite v Development, Test in Production.  
- Odpravite ročno ponovno konfiguracijo in se izognite dragim napakam.  
- Podprite avtomatizirane delovne tokove in CI/CD-pipelines z enostavnimi CLI ukazi (`export-ds` in `import-ds`).  
- Hitro kopirajte podatkovne vire med projekti za lažje sodelovanje.  

Ta funkcionalnost omogoča ekipam zanesljivo uvajanje, saj vedo, da so konfiguracije skladne v vseh okoljih.  

---

### Module Analytics (v1) – od zaznavanja k razumevanju
digna se je začela kot platforma za zaznavanje anomalij in spremljanje kakovosti podatkov. Z izdajo 2025.04 napreduje z **prvo različico Module Analytics**.  

Module Analytics pomaga uporabnikom, da **razumejo svoje podatke** namesto, da le reagirajo na težave. Z novim modulom lahko:  
- Spremljate dolgoročne trende v svojih podatkovnih nizih.  
- Odkrijete in spremljate volatilnost, da razumete nihanja.  
- Raziskujete vedenje dotoka podatkov skozi čas za globlji kontekst.  

Na primer, digna lahko samodejno poudari *«Število vrstic se je povečalo za 15,8 % od začetka leta.»*  
Brez SQL-poizvedb, brez ročnih pregledov — le **akcijsko usmerjene vpoglede na prvi pogled**.  

To je temelj dignine poti proti napredni analitiki podatkov in omogoča ekipam za podatke prehod iz reaktivnega v proaktivno spremljanje.  

---

### Izboljšave nadzorne plošče – bolj gladka uporabniška izkušnja
Poleg večjih funkcij vsebuje Release 2025.04 več **izboljšav nadzorne plošče**, zasnovanih za bolj intuitivno in prijetno uporabo digna:  
- Hitrejše prehajanje med projekti in inšpekcijami.  
- Bolj urejena postavitev dnevnikov in predajanja opravkov inšpekcij.  
- Subtilne oblikovne prilagoditve, ki vam pomagajo hitreje najti vpoglede.  

Te izboljšave temeljijo neposredno na povratnih informacijah strank in odražajo našo stalno zavezanost k oblikovanju digna kot **platforme za vsakodnevno uporabo**.  

---

## Splošne izboljšave
- Optimizacije zmogljivosti za inšpekcijska opravila na velikih podatkovnih nizih.  
- Izboljšano ravnanje z napakami v dignacli za jasnejše povratne informacije.  
- Izboljšana stabilnost za projekte z veliko sočasnimi opravili.  
- UI-izboljšave za filtriranje dnevnikov opravil in upravljanje projektov.  

---

## Povzetek
Release 2025.04 je osredotočen na **nadzor, dostopnost in vpoglede**.  

- Novi **Inspection Hub** uporabnikom zagotavlja popolno preglednost inšpekcijskih opravil.  
- **Večjezična podpora** omogoča uporabo digne globalnim ekipam.  
- Funkcija **uvoz/izvoz** poenostavlja upravljanje konfiguracij med okolji.  
- **Module Analytics (v1)** premika poudarek od zaznavanja k razumevanju z sledenjem trendov in volatilnosti.  
- **Izboljšave nadzorne plošče** dodelajo celotno uporabniško izkušnjo.  

Skupaj te posodobitve naredijo digno močnejšo, bolj uporabniku prijazno in bolj pripravljeno za mednarodno uporabo kot kdaj koli prej.
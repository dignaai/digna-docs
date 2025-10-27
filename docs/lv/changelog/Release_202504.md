---
title: digna izlaišana 2025.04 | Inspection Hub, daudzvalodu atbalsts, Module Analytics
description: Uzziniet, kas jauns digna izlaidumā 2025.04. Šī versija ievieš Inspection Hub, daudzvalodu atbalstu (angļu, vācu, poļu), datu avotu importēšanu/eksportēšanu caur dignacli, pirmo Module Analytics laidienu un uzlabotu paneļa pieredzi.
keywords: digna Release 2025.04, digna changelog, digna inspection hub, digna multi-language support, digna module analytics, digna import export, digna CLI, release notes, data observability, data quality monitoring
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Izmaiņu žurnāls – Release 2025.04

Ar izlaidumu 2025.04 digna veic nozīmīgu soli uz priekšu, padarot datu kvalitātes un novērošanas pārvaldību vienkāršāku, caurspīdīgāku komandām un pieejamāku lietotājiem visā pasaulē.  
Šajā laidienā apvienotas **jaudīgas jaunas funkcijas**, **darplūsmu automatizācijas uzlabojumi** un **lietotāja pieredzes pilnveidojumi**.  

---

## Jaunas funkcijas

### Inspection Hub – jauns komandcentrs
Pats **Inspection Hub** tagad pieejams kā centrālā vieta visu jūsu inspekciju darbu pārvaldībai. Tā vietā, lai pārlēktu starp dažādiem moduļiem vai paļautos tikai uz komandrindas palaišanu, tagad varat uzraudzīt un kontrolēt savas inspekcijas no viena vienkāršota interfeisa.  

Galvenās iespējas ietver:  
- Inspekcijas pēc pieprasījuma: Sāciet jaunus darbus uzreiz, kad nepieciešami svaigi rezultāti.  
- Inspekciju vēsture: Redziet laika līniju ar inspekcijām — kas tika palaists, kas to izsauca un kad.  
- Statusa izsekošana: Darbi skaidri atzīmēti kā pabeigti, procesā vai gaidoši.  
- Izsaucēja informācija: Ātri pārbaudiet, vai inspekcija tika palaista no lietotāja, plānotāja vai CLI.  
- Notīrīšanas rīki: Dzēsiet novecojušus vai liekus darbus, lai darba vieta būtu sakārtota.  
- Detalizētas žurnālfailas: Iedziļinieties katrā darbā, lai redzētu, cik ilgi tas ilga, kuri avoti tika iekļauti un kā tika pielietoti sliekšņi.  

Inspection Hub komandām nodrošina **pilnīgu redzamību un kontroli**, padarot inspekciju pārvaldību vienkāršāku liela mēroga projektos.  

---

### Daudzvalodu atbalsts – digna runā jūsu valodā
digna tagad ir gatava starptautiskām komandām ar **daudzvalodu atbalsta** ieviešanu.  

Šajā laidienā varat iestatīt savu **vēlamo lietotāja saskarnes valodu** tieši Lietotāja preferencēs. Atbalstītās valodas ietver:  
- angļu (UK, US, CA, AU)  
- vācu (DE, AT, CH)  
- poļu (PL)  

Tas padara digna lietošanas ērtāku daudzvalodu organizācijām un nodrošina vienmērīgāku ieviešanu komandām, kas strādā dažādās reģionos. Turpmākajos laidienos tiks pievienotas vēl citas valodas.  

---

### Datu avotu importēšana un eksportēšana – konfigurēšana padarīta vienkārša
Saskaņotība starp vidēm ir būtiska uzņēmuma izvietošanai. Ar 2025.04 digna ievieš **datu avotu importēšanu/eksportēšanu** caur **dignacli**, komandrindas rīku uzlabotiem lietotājiem.  

Ieguvumi:  
- Eksportējiet datu avota konfigurāciju vienreiz un izmantojiet to atkārtoti Attīstībā, Testēšanā un Ražošanā.  
- Novērsiet manuālu pārkārtošanu un dārgi maksājošas kļūdas.  
- Atbalstiet automatizētas darplūsmas un CI/CD caur vienkāršām CLI komandām (`export-ds` un `import-ds`).  
- Ātri kopējiet datu avotus starp projektiem vieglākai sadarbībai.  

Šī funkcionalitāte ļauj komandām izvietot ar pārliecību, zinot, ka konfigurācijas ir vienotas katrā vidē.  

---

### Module Analytics (v1) – no atklāšanas uz izpratni
digna sākotnēji bija platforma anomāliju noteikšanai un datu kvalitātes uzraudzībai. Ar izlaidumu 2025.04 tā turpina attīstīties, piedāvājot **Module Analytics pirmo versiju**.  

Module Analytics palīdz lietotājiem **izprast savus datus**, nevis tikai reaģēt uz problēmām. Ar šo jauno moduli varat:  
- Izsekot ilgtermiņa tendences datu kopās.  
- Atklāt un uzraudzīt svārstīgumu, lai saprastu izmaiņu raksturu.  
- Pētīt datu uzvedību laika gaitā, lai iegūtu dziļāku kontekstu.  

Piemēram, digna var automātiski izcelt, ka *“Rindu skaits kopš gada sākuma palielinājies par 15.8%.”*  
Ne SQL vaicājumi, ne manuālas pārbaudes — tikai **rīcībai noderīgi ieskati uzreiz**.  

Tas ir pamats digna ceļam uz attīstītāku datu analītiku, ļaujot datu komandām pāriet no reaktīvas uz proaktīvu uzraudzību.  

---

### Paneļa uzlabojumi – raitāka lietotāja pieredze
Papildus galvenajām funkcijām izlaidums 2025.04 ietver vairākus **paneļa uzlabojumus**, kas paredzēti, lai digna būtu intuitīvāka un patīkamāka lietošanā:  
- Ātrāka navigācija starp projektiem un inspekcijām.  
- Tīrāks izkārtojums inspekciju žurnāliem un darbu iesniegšanām.  
- Smalkas dizaina pielāgošanas, kas palīdz ātrāk atrast ieskatus.  

Šie uzlabojumi balstīti tieši uz klientu atsauksmēm un atspoguļo mūsu pastāvīgo apņemšanos padarīt digna **platformu ikdienas lietošanai**.  

---

## Vispārīgie uzlabojumi
- Veiktspējas optimizācijas inspekciju darbiem lielos datu apjomos.  
- Uzlabota kļūdu apstrāde dignacli, lai nodrošinātu skaidrāku atgriezenisko saiti.  
- Stabilitātes uzlabojumi projektiem ar daudziem vienlaicīgiem darbiem.  
- UI pilnveidojumi darba žurnālu filtrēšanai un projektu pārvaldībai.  

---

## Kopsavilkums
Izlaidums 2025.04 ir par **kontroli, pieejamību un ieskatu**.  

- Jaunais **Inspection Hub** sniedz lietotājiem pilnu pārredzamību pār inspekciju darbiem.  
- **Daudzvalodu atbalsts** nodrošina, ka digna var tikt lietota globālās komandās.  
- **Importēšanas/eksportēšanas funkcionalitāte** vienkāršo konfigurāciju vadību starp vidēm.  
- **Module Analytics (v1)** maina fokusu no atklāšanas uz izpratni, piedāvājot tendenču un svārstīguma izsekošanu.  
- **Paneļa uzlabojumi** pilnveido kopējo lietotāja pieredzi.  

Kopā šie atjauninājumi padara digna jaudīgāku, lietotājam draudzīgāku un starptautiski gatavāku nekā jebkad agrāk.
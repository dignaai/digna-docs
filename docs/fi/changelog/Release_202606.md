---
title: digna Julkaisu 2026.06 | Python SDK, Docker-käyttöönotto ja laajennettu validointihallinta
description: Tutustu, mitä uutta digna Julkaisussa 2026.06. Tämä versio esittelee uuden digna Python SDK:n, virallisen Docker-käyttöönoton tuen, uudistetun kojelaudan ja laajennetut tuonti-/vientimahdollisuudet validointisäännöille.
keywords: digna Julkaisu 2026.06, digna Python SDK, digna Docker-tuki, datan laadun automaatio, dataprofilointi, validointisääntöjen tuonti vienti, digna kojelauta, data observability -alusta, Python API, metadata-automaatio
image: /assets/logo_square.png
---

# Muutosloki – Julkaisu 2026.06  

Julkaisussa 2026.06 digna ottaa merkittävän askeleen eteenpäin automaatiossa, laajennettavuudessa ja alustan käytettävyydessä.  
Tässä julkaisussa esittelemme uuden **digna Python SDK:n**, virallisen **Docker-käyttöönoton tuen**, uudistetun kojelaudan käyttökokemuksen ja parannetun siirrettävyyden validointisääntöjen hallintaan.

---

## 🚀 Uudet ominaisuudet  

### digna Python SDK – Automatisoi kaikki Pythonilla  
- Asenna:
  ```bash
  pip install digna-sdk
  ```
- Hallitse ja automatisoi dignaa ohjelmallisesti Pythonilla  
- Luo ja konfiguroi projekteja koodilla  
- Käynnistä tarkastuksia ja monitoroinnin ajoja  
- Hallitse datasetit, säännöt ja asetukset ohjelmallisesti  
- Profiloi tauluja ja poimi metatiedon oivalluksia  
- Vie profilointi- ja datan laadun tuloksia ulkoisiin arkistoihin ja järjestelmiin  
- Integroi notebookeihin, orkestrointityökaluihin ja CI/CD-putkiin  

**Vaikutus:** Mahdollistaa infrastruktuurin kokonaisvaltaisen määrittelyn koodina ja syvän automaation datan laadun ja observability-työnkuluille Pythonin avulla.

---

### Docker-tuki – Yksinkertaistettu käyttöönotto ja operointi  
- Virallinen Docker-imagetuki dignalle  
- Nopea ja yhtenäinen asennus eri ympäristöihin  
- Helppo käyttöönotto kehitys-, testaus- ja tuotantoympäristöihin  
- Helppo integraatio Kubernetesin ja konttialustojen kanssa  
- Parempi siirrettävyys ja toistettavuus käyttöönotossa  

**Vaikutus:** Tekee dignan käyttöönotosta ja ylläpidosta helpompaa moderneissa cloud-native -arkkitehtuureissa.

---

### QueryMode – Joustava SQL-suoritustapa

Määritä kyselyjen suoritusstrategia: **Single** tai **Combined** -tila

**Single-tila**: Jokainen tilasto lasketaan yhdellä omalla SQL-kyselyllään

  - Ihanteellinen suurille tietolähteille, joissa muistirajoitukset ovat huomionarvoisia
  - Estää yhdistetyn kyselyn resurssien loppumisen (muistin loppuminen, spool-rajoitukset)
  - Suurempi kyselymäärä mutta pienempi muistijalanjälki per kysely

**Combined-tila**: Kaikki tilastot lasketaan yhdessä SQL-kyselyssä

  - Vähentää kokonaiskyselymäärää ja verkon overheadia
  - Optimoi suorituskykyä, kun tietolähteet ovat hallittavissa muistissa
  - Tehokkaampi usein toistuvissa ja rinnakkaisissa ajoissa

**Vaikutus:** Antaa käyttäjille tarkemman hallinnan kyselyjen suorittamisesta, jotta suorituskyky, resurssien käyttö ja muistisuoja voidaan tasapainottaa tietolähteen ominaisuuksien mukaan.

---

### Uudistettu kojelaudan käyttökokemus  
- Modernisoitu ja parannettu UI/UX-suunnittelu  
- Selkeämpi navigointi ja rakenne  
- Parempi näkyvyys monitorointituloksiin ja datan laadun oivalluksiin  
- Parannettu hälytysten, tilastojen ja kojelautojen luettavuus  
- Nopeampi pääsy keskeiseen operatiiviseen informaatioon  

**Vaikutus:** Parantaa käytettävyyttä ja päivittäistä tuottavuutta kaikille käyttäjille.

---

### Laajennettu tuonti ja vienti validointisäännöille  
- Parannettu tuonti-/vienti-toiminnallisuus validointisäännöille  
- Helpompi migraatio ympäristöjen ja projektien välillä  
- Parempi uudelleenkäytettävyys standardoiduille sääntökokoelmille  
- Parempi hallinnointi ja sääntöjen elinkaaren hallinta  
- Yksinkertaistettu tiimien välinen yhteistyö  

**Vaikutus:** Mahdollistaa skaalautuvan ja yhdenmukaisen datan laadun hallinnan koko organisaation laajuudessa.

---

## 🧪 Alustan parannukset  

- Täydellinen Python SDK -integraatio automaatiolle  
- Konttioitu käyttöönotto Dockerin kautta  
- Parannettu käyttökokemus uudistetulla kojelaudalla  
- Laajennettu validointilogiikan siirrettävyys  

---

## 🎯 Kenelle tämä julkaisu hyödyttää  

- Data-insinöörit: automatisointi, SDK:n käyttö, putkistojen integraatio  
- Alustatiimit: yksinkertaistettu käyttöönotto Dockerin avulla  
- Tiedonhallintatiimit: uudelleenkäytettävät validointisääntöjen hallintamallit  
- Analytiikkatiimit: parantunut käytettävyys ja oivallusten näkyvyys  

---

## 🛠 CLI-päivitykset  
- Lisätty SDK-integraation tuki  
- Parannetut tuonti-/vienti-työnkulut  
- Yleisiä vakaus- ja suorituskykyparannuksia
# Muutosloki – Julkaisu 2026.06  

Julkaisussa 2026.06 digna ottaa merkittävän askeleen eteenpäin automaatiossa, laajennettavuudessa ja alustan käytettävyydessä.  
Tässä julkaisussa esittelemme uuden **digna Python SDK:n**, virallisen **Docker-käyttöönoton tuen**, uudistetun kojelaudan käyttökokemuksen ja parannetun siirrettävyyden validointisääntöjen hallintaan.

---

## Katso julkaisun esittely

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — katsaus tähän julkaisuun dignan YouTube-kanavalla.*

---

## Uudet ominaisuudet  

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

### Muokattava ennustemalli

Poikkeamien tunnistuksen taustalla oleva malli on nyt muokattavissa. Seitsemän parametria ohjaa sitä, miten ennuste sovitetaan:

- Break Sensitivity
- Outlier Sensitivity
- Memory
- Ridge Strength
- Gap Tolerance
- Outlier Correction
- Plausible Range Tightness

Oletusarvot sopivat valtaosalle sarjoista, ja jokainen parametri voidaan palauttaa oletusarvoonsa milloin tahansa.

**Vaikutus:** Antaa käyttäjille hallinnan itse ennustemalliin toleranssikaistan nykyisten Sensitivity- ja Memory-asetusten rinnalla. Kysy dignalta ohjeita siitä, milloin parametriin kannattaa tarttua ja miten se asetetaan.

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

## Alustan parannukset  

- Täydellinen Python SDK -integraatio automaatiolle  
- Konttioitu käyttöönotto Dockerin kautta  
- Parannettu käyttökokemus uudistetulla kojelaudalla  
- Laajennettu validointilogiikan siirrettävyys  

---

## Kenelle tämä julkaisu hyödyttää  

- Data-insinöörit: automatisointi, SDK:n käyttö, putkistojen integraatio  
- Alustatiimit: yksinkertaistettu käyttöönotto Dockerin avulla  
- Tiedonhallintatiimit: uudelleenkäytettävät validointisääntöjen hallintamallit  
- Analytiikkatiimit: parantunut käytettävyys ja oivallusten näkyvyys  

---

## CLI-päivitykset  
- Lisätty SDK-integraation tuki  
- Parannetut tuonti-/vienti-työnkulut  
- Yleisiä vakaus- ja suorituskykyparannuksia
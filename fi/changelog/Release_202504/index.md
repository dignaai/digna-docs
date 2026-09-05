# Muutosloki – Julkaisu 2025.04

Julkaisulla 2025.04 digna ottaa merkittävän askeleen eteenpäin tehdäkseen datan laadun ja observabilityn hallinnasta helpompaa, läpinäkyvämpää tiimeille ja saavutettavampaa käyttäjille ympäri maailmaa.  
Tämä julkaisu yhdistää **tehokkaita uusia ominaisuuksia**, **työnkulkujen automaatioparannuksia** ja **käyttökokemuksen hienosäätöjä**.  

---

## Uudet ominaisuudet

### Inspection Hub – uusi komentokeskus
Inspection Hub on nyt saatavilla keskeisenä paikkana hallita kaikkia tarkastusajoja. Sen sijaan, että hyppisit moduulista toiseen tai luottaisit pelkästään komentorivisuorituksiin, voit nyt valvoa ja ohjata tarkastuksia yhdestä virtaviivaisesta käyttöliittymästä.  

Tärkeimmät ominaisuudet:  
- Tarpeen mukaan suoritettavat tarkastukset: Käynnistä uusia töitä heti, kun tarvitset tuoreita tuloksia.  
- Tarkastushistoria: Näe tarkastusten aikajana — mitä ajettiin, kuka käynnisti sen ja milloin.  
- Tilaseuranta: Työt on selkeästi merkitty valmistuneiksi, käynnissä oleviksi tai odottaviksi.  
- Käynnistäjäin tiedot: Tarkista nopeasti, käynnistettiinkö tarkastus käyttäjän, ajastimen vai CLI:n kautta.  
- Siivoustyökalut: Poista vanhentuneita tai tarpeettomia töitä, jotta työtila pysyy siistinä.  
- Yksityiskohtaiset lokit: Syvenny jokaisen työn tietoihin nähdäksesi kuinka kauan se kesti, mitkä lähteet sisällytettiin ja miten kynnysarvoja sovellettiin.  

Inspection Hub antaa tiimeille **end-to-end-näkyvyyden ja ohjauksen**, jolloin tarkastusten hallinta suurissa projekteissa on helpompaa.  

---

### Monikielisyys – digna puhuu kieltäsi
digna on nyt valmis kansainvälisille tiimeille monikielistuen ansiosta.  

Tässä julkaisussa voit asettaa **mieluisan käyttöliitteen kielen** suoraan Käyttäjäasetuksista. Tuetut kielet ovat:  
- Englanti (UK, US, CA, AU)  
- Saksa (DE, AT, CH)  
- Puola (PL)  

Tämä tekee dignasta helpommin käytettävän monikielisissä organisaatioissa ja varmistaa sujuvamman käyttöönoton eri alueilla työskenteleville tiimeille. Lisää kieliä lisätään tulevissa julkaisuissa.  

---

### Datalähteiden tuonti ja vienti – Konfigurointi yksinkertaistuu
Konsistenssi ympäristöjen välillä on olennaista yritystason käyttöönotossa. Versiossa 2025.04 digna tuo käyttöön **datalähteiden tuonnin ja viennin** **dignacli**-työkalun kautta, joka on komentorivityökalu edistyneille käyttäjille.  

Hyödyt:  
- Vie datalähdekokoonpano kerran ja käytä uudelleen Kehitys-, Testi- ja Tuotantoympäristöissä.  
- Poista manuaalinen uudelleenkonfigurointi ja vältä kalliit virheet.  
- Tue automatisoituja työnkulkuja ja CI/CD-putkia yksinkertaisilla CLI-komennoilla (`export-ds` ja `import-ds`).  
- Kopioi datalähteitä nopeasti projektien välillä helpottaaksesi yhteistyötä.  

Tämä toiminnallisuus varmistaa, että tiimit voivat ottaa käyttöön luottavaisin mielin, tietäen että kokoonpanot ovat yhtenäisiä kaikissa ympäristöissä.  

---

### Module Analytics (v1) – Havaitsemisesta ymmärtämiseen
digna alkoi alustana poikkeamien havaitsemiseen ja datan laadun seurantaan. Julkaisulla 2025.04 se kehittyy edelleen ensimmäisellä versiollaan **Module Analytics**-osiosta.  

Module Analytics auttaa käyttäjiä **ymmärtämään dataansa** sen sijaan, että he vain reagoisivat ongelmiin. Tämän uuden moduulin avulla voit:  
- Seurata pitkän aikavälin trendejä tietojoukoissasi.  
- Havaita ja seurata volatiliteettia ymmärtääksesi vaihteluita.  
- Tutkia datan käyttäytymistä ajan myötä syvempää kontekstia varten.  

Esimerkiksi digna voi automaattisesti korostaa, että *“Rivien määrä on kasvanut 15,8 % vuodenvaihteen jälkeen.”*  
Ei SQL-kyselyjä, ei manuaalisia tarkistuksia — vain **toimintakelpoisia näkemyksiä yhdellä silmäyksellä**.  

Tämä on perusta dignan matkalla kohti kehittyneempää data-analytiikkaa, mahdollistaen datatiimien siirtymisen reaktiivisesta valvonnasta proaktiiviseen seurantaan.  

---

### Kojelaudan parannukset – Sujuvampi käyttökokemus
Suurten ominaisuuksien lisäksi julkaisu 2025.04 sisältää useita **kojelautaan liittyviä hienosäätöjä**, jotka tekevät dignasta intuitiivisemman ja miellyttävämmän käyttää:  
- Nopeat siirtymät projektien ja tarkastusten välillä.  
- Selkeämpi asettelu tarkastuslokille ja työn lähettämisille.  
- Hienovaraiset suunnittelumuutokset, jotka auttavat löytämään oivalluksia nopeammin.  

Nämä parannukset perustuvat suoraan asiakaspalautteeseen ja osoittavat jatkuvan sitoutumisemme tehdä dignasta **päivittäiseen käyttöön suunniteltu alusta**.  

---

## Yleiset parannukset
- Suorituskyvyn optimointeja tarkastustöille suurissa tietojoukoissa.  
- Parannettu virheenkäsittely dignacli:ssa selkeämmän palautteen tarjoamiseksi.  
- Vakautusparannuksia projekteille, joissa on monta samanaikaista työtä.  
- Käyttöliittymän hienosäätöjä työn lokien suodatukseen ja projektinhallintaan.  

---

## Yhteenveto
Julkaisu 2025.04 keskittyy **ohjaukseen, saavutettavuuteen ja oivalluksiin**.  

- Uusi **Inspection Hub** antaa käyttäjille täydellisen näkyvyyden tarkastustöihin.  
- **Monikielisyys** varmistaa, että dignaa voidaan käyttää globaalisti eri tiimeissä.  
- **Tuonti/vienti-toiminnallisuus** yksinkertaistaa konfiguraation hallintaa eri ympäristöissä.  
- **Module Analytics (v1)** siirtää painopistettä havaitsemisesta ymmärtämiseen trendi- ja volatiliteettiseurannalla.  
- **Kojelaudan parannukset** viimeistelevät kokonaiskäyttökokemusta.  

Nämä päivitykset yhdessä tekevät dignasta tehokkaamman, käyttäjäystävällisemmän ja kansainvälisesti valmis kuin koskaan ennen.
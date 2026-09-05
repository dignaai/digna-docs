# Muutospäiväkirja – Versio 2024.12

Versio 2024.12 tuo joukon uusia ominaisuuksia ja parannuksia, jotka tekevät dignasta entistä automatisoidumman, joustavamman ja yrityskäyttöön valmiimman.  
Tässä versiossa parannetaan ajoitusta, raportointia, kyselyiden käsittelyä ja poikkeamien tunnistuksen tarkkuutta.  

---

## Uudet ominaisuudet

### Sisäänrakennettu Scheduler
Tarkastukset eivät enää riipu pelkästään komentorivistä tai API-kutsuista.  
Uuden digna Schedulerin avulla tarkastuksia voidaan ajaa automaattisesti määriteltyinä ajankohtina.  

- Tukee **Cron expressions** -lausekkeita toistuville ajoituksille (päivittäin, viikoittain tai mukautetut jaksot).  
- Tarjoaa tarkan hallinnan **offsettien**, **aloituspäivien** ja **lopetuspäivien** avulla.  
- Mahdollistaa tiimien varmistaa, että kaikki kriittiset datalähteet tarkastetaan johdonmukaisesti ilman manuaalista työtä.  

---

### PDF-raportit
Tiimit voivat nyt helposti jakaa tuloksia sidosryhmille **PDF-viennin** avulla.  

- Kaaviot, mittarit ja poikkeamatulokset voidaan viedä ammattimaiseen PDF-muotoon.  
- Raportit yhdistävät **visualisoinnit** ja **taustalla olevan datan**, palvellen sekä teknisiä että liiketoiminnan käyttäjiä.  
- Poistaa tarpeen ulkoisille työkaluilla raporttien luontiin.  

---

### Uusi saraketyyppi: `CUSTOM`
Joustavuuden lisäämiseksi digna esittelee uuden `CUSTOM`-saraketyypin.  

- Käyttäjät voivat määritellä tarkasti, mitä **tilastoja ja mittareita** sovelletaan tiettyihin attribuutteihin.  
- Ihanteellinen erikoistapauksiin, jotka eivät sovi standardikategorioihin kuten NUMERICAL tai CATEGORICAL.  
- Auttaa pitämään analyysit fokusoituina ja tulokset liiketoimintayhteyteen relevantteina.  

---

### Uudet paikkamerkit snapshot-kyselyissä
Snapshot-kyselyt ovat nyt yksinkertaisempia ja vähemmän virhealttiita dynaamisten paikkamerkkien avulla.  

- Tokenit kuten `#date+n#` tai `#date-n#` säätävät päivämääriä kyselyissä automaattisesti.  
- Esimerkki:  
  - `#date+1#` → huomenna  
  - `#date-2#` → kaksi päivää sitten  
- Poistaa manuaaliset päivälaskelmat ja varmistaa johdonmukaisuuden tiimien välillä.  

---

### Kynnysarvojen optimointi
Poikkeamakynnysarvot ovat nyt älykkäämpiä ja kontekstin mukaisia.  

- Mittareille kuten **NULL COUNT** alemmat kynnysarvot rajoitetaan automaattisesti arvoon **0**.  
- Estää virheellisiä tai merkityksettömiä kynnysarvoja.  
- Johtaa vähempiin väärin ilmoitettuihin poikkeamiin ja luotettavampaan poikkeamien tunnistukseen.  

---

## Yleiset parannukset
- Viilatut **UI-komponentit** projektin ja attribuuttien konfigurointinäkymissä.  
- Parannettu **dashboardin suorituskyky** suurilla datamäärillä.  
- Laajennettu **lokitus ja virheilmoitukset** vianmääritystä varten.  

---

## Yhteenveto
Versio 2024.12 vahvistaa dignaa alustana datalaadun, poikkeamien tunnistuksen ja havaittavuuden alueilla.  
Ajastuksen automatisoinnin, jaettavien PDF-raporttien, mukautettavien sarakkeiden, yksinkertaistettujen snapshot-kyselyiden ja älykkäämpien kynnysarvojen myötä digna on entistä arvokkaampi sekä teknisille käyttäjille että liiketoiminnan sidosryhmille.
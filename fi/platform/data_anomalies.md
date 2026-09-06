# digna Data Anomalies – Tekoälypohjainen datalaadun poikkeamien havaitseminen

**Tekoälyn tehostama observoitavuus jatkuvan dataluottamuksen takaamiseksi**

digna Data Anomalies on osa **digna Data Observability Platform**ia — modulaarinen ratkaisu, joka parantaa **datan laatua** analysoimalla jatkuvasti, miten datasetit käyttäytyvät ajan myötä.

Se oppii automaattisesti, miltä “normaali” näyttää datallesi, ja varoittaa muutoksista — ilman staattisten kynnysarvojen määrittelyä tai sääntöjen kirjoittamista.  
Moduuli ajetaan suoraan tietokannassasi, joten data ei koskaan poistu ympäristöstäsi.

---

## digna Data Anomaliesin tarkoitus

**digna Data Anomalies** -moduuli tarjoaa jatkuvaa **datan observoitavuutta** laskemalla ja seuraamalla ennalta määriteltyjä tilastollisia mittareita, kuten:

- Datan määrä ja rivimäärät  
- Puuttuvien arvojen osuudet  
- Arvojen jakaumat ja histogrammit  
- Numeraaliset vaihteluvälit ja keskiarvot  
- Sarake-uniikkius ja tekstin pituus  

Nämä mittarit kerätään automaattisesti jokaista datasettiä varten.  
Niiden avulla digna rakentaa malleja, jotka kuvaavat kunkin mittarin tyypillistä käyttäytymistä — oppien päivittäiset, viikoittaiset tai kausivaihtelut.  
Kun malli on koulutettu, moduuli ennustaa odotettuja arvoja uudelle datalle ja havaitsee poikkeamat, jotka voivat viitata laatupoikkeamiin, prosessivirheisiin tai upstream-muutoksiin.

---

## Keskeiset ominaisuudet

- Oppii odotetun datakäyttäytymisen automaattisesti tekoälyn avulla — ei kynnysarvojen konfigurointia.  
- Havaitsee äkilliset pudotukset, piikit tai driftin datamäärissä ja jakaumissa.  
- Tunnistaa vaihdettuja sarakkeita tai virheellisiä attribuuttimäärittelyjä.  
- Nostaa esiin odottamattomia kategorisia arvoja (esim. uudet alueet tai koodit).  
- Tukee kaikkia saraketyyppejä: numeerinen, kategorinen tai määrittämätön.  
- Toimii kokonaan asiakkaan ympäristössä — ei datan siirtoa.  
- Integroituu **digna Data Analytics** -moduuliin pitkäaikaista trendianalyysiä varten.

---

## Miten se toimii

### Vaihe 1 – Metrien laskenta
digna laskee joukon profilointimittareita jokaiselle taululle ja sarakkeelle.  
Nämä mittarit kuvaavat datasi rakennetta ja tilastollista käyttäytymistä ja tallennetaan jatkoanalyysiä varten.

### Vaihe 2 – Mallin koulutus
Historiallisten mittariarvojen perusteella digna kouluttaa kompaktit koneoppimismallit (signature models), jotka sieppaavat kunkin mittarin normaalin vaihteluvälin.

### Vaihe 3 – Automaattinen raja-arvotus
Käyttäen *conformal inference* -menetelmää digna laskee adaptiiviset luottamusvälit (automaattiset kynnysarvot), jotka kehittyvät datasi mukana.  
Jos uudet mittariarvot jäävät ennustetun alueen ulkopuolelle, ne merkitään poikkeamiksi.

Tämä jatkuva palautesilmukka varmistaa, että monitorointi pysyy merkityksellisenä myös silloin, kun datamäärät tai -kaavat luonnollisesti muuttuvat.

---

## Esimerkkitilanteet

### Odottamaton lasku tietueiden määrässä
Datasetti sisältää tyypillisesti noin 500 000 riviä päivässä.  
Kun uusi toimitus sisältää vain 50 000 riviä, digna merkitsee poikkeaman ja näyttää, kuinka paljon arvo poikkeaa opitusta vaihteluvälistä.

### Sarakevaihto havaittu
Kentän `last_name` keskimääräinen merkkipituus alkaa yhtäkkiä vastata `first_name`-kentän pituutta.  
digna tunnistaa muutoksen mittarimallissa ja antaa varoituksen mahdollisesta sarakevaihdosta.

### Odottamaton kategoria havaittu
Itävallan kaupunkeja listaava sarake sisältää yllättäen arvon “Zurich”.  
Historiallisten jakaumien perusteella digna merkitsee uuden arvon odottamattomaksi ja hälyttää käyttäjän.

---

## Integraatio muihin moduuleihin

- **digna Data Analytics** — kokoaa yhteen poikkeamien historian ja volatiliteettimittarit paljastaakseen pitkäaikaiset trendit.  
- **digna Data Validation** — valvoo eksplisiittisiä liiketoimintasääntöjä deterministisiin laatutarkistuksiin.  
- **digna Data Timeliness** — seuraa datan saapumisaikoja ja korreloi viiveitä poikkeamatapahtumien kanssa.  
- **digna Data Schema Tracker** — havaitsee rakenteelliset muutokset, jotka voivat selittää uusia poikkeamia.

---

## Tyypillisiä käyttötapauksia

- Puuttuvien tai duplikaattisten latausten havaitseminen.  
- Vaihdettujen tai katkenneiden sarakkeiden tunnistaminen.  
- Jakauman driftin havaitseminen numeerisissa tai kategorisissa ominaisuuksissa.  
- Odottamattomien viitearvojen tai koodien löytäminen.  
- Jatkuvien ingestio-putkien valvonta epäsäännöllisyyksien varalta.  
- Koko organisaation laajuinen **datan laadun ja observoitavuuden** seuranta.

---

## Hyödyt

- Poikkeavan datakäyttäytymisen välitön havaitseminen.  
- Manuaalisen kynnysarvojen säätämisen poistaminen.  
- Operatiivisen työn väheneminen suurissa dataympäristöissä.  
- Luottamuksen rakentaminen analytiikka- ja raportointijärjestelmiin.  
- Parantaa **datan laatua** ja end-to-end **datan observoitavuutta**.

---

## Asiaankuuluvat digna-moduulit

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — trendi- ja volatiliteettimittarit.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — sääntöpohjainen datan varmennus.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — datan toimitusaikataulujen seuranta.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — skeeman muutosten havainnointi.

---

## Yhteenveto

**digna Data Anomalies** -moduuli muodostaa ydinosan dignan tekoälyvetoisesta **Data Observability Platform** -ratkaisusta.  
Se seuraa jatkuvasti keskeisiä mittareita, oppii kaavoja ja tunnistaa poikkeamat, mikä auttaa organisaatioita varmistamaan, että **datan laatu** pysyy luotettavana, vakaana ja selitettävänä — ilman manuaalista konfigurointia.
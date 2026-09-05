# Data Validation – sääntöpohjaiset tarkistukset
<h1 style="display:none;">AI:n ohjaama Data Validation -moduuli tietojen laadun ja havaittavuuden varmistukseen – digna</h1>

---

## Tarkoitus

Data Validation -moduuli varmistaa datan laadun tarkkojen, sääntöpohjaisten tarkistusten avulla.  
Se antaa organisaatioille mahdollisuuden määritellä deterministisen liiketoiminta- ja teknisen validointilogiikan, varmistaen, että data täyttää vaatimustenmukaisuuden standardit, sopimusperusteiset SLA:t ja sääntelyvaatimukset.

Yhdistämällä *tietokannassa suoritettavat säännöt*, *täydelliset auditointilokit* ja *integraation muihin digna-moduuleihin*, Data Validation takaa johdonmukaisen ja jäljitettävän **datan laadun ja havaittavuuden** monimutkaisissa yritysympäristöissä.

---

## Tekninen yleiskatsaus

### Tuetut validointityypit

- **Vastaavuustarkistukset**  
  Varmistaa, että arvot vastaavat odotettuja tuloksia (esim. viitekoodit, totuusarvot, kategoriset kartoitukset).

- **Kynnysarvot & arvovälit**  
  Validoi numeerisia mittareita tai KPI:itä määriteltyjä rajoja vastaan — staattisia tai dynaamisesti johdettuja.

- **Viitelistat & haut**  
  Tarkistaa, esiintyykö kentän arvo hyväksytyissä master-dataseteissä (esim. ALV-koodit, ISO-maa-listat, tuoteluettelot).

- **Sarakkeiden välinen yhdenmukaisuus**  
  Varmistaa relaatiollisen oikeellisuuden (esim. valuutta vastaa aluetta, riskiluokka vastaa omaisuustyyppiä).

- **Null-arvojen käsittelysäännöt**  
  Havaitsee odottamattomat null- tai tyhjät arvot kriittisissä sarakkeissa.

### Suoritus ja lokitus

- **Tietokantasuoritus** – Kaikki validointisäännöt suoritetaan suoraan tietokannassasi (Teradata, Snowflake, Databricks, PostgreSQL jne.).  
- **Ei tietojen poistoa** – digna ei koskaan siirrä raakatietoja ympäristösi ulkopuolelle.  
- **Täysi jäljitettävyys** – Jokainen säännön tulos kirjataan aikaleiman, vastuullisen datasetin, rivimäärien sekä hyväksytty/hylätty -tulosten kanssa.  
- **Auditointi**
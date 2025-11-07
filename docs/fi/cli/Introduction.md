## Komentorivikäyttöliittymän (CLI) tarkoitus

The ***digna*** Command Line Interface (CLI) on tehokas työkalu, joka on suunniteltu sujuvoittamaan vuorovaikutusta ***digna***-alustan kanssa. Se tarjoaa tekstipohjaisen käyttöliittymän, jonka avulla käyttäjät voivat suorittaa laajan valikoiman tehtäviä tehokkaasti ilman graafista käyttöliittymää.

### Keskeiset ominaisuudet:

- **Efficiency and Flexibility:** CLI mahdollistaa komentojen nopean suorittamisen, mikä parantaa tuottavuutta.
- **Automation:** Tukee skriptausta toistuvien tehtävien automatisointiin.
- **Remote Access:** Hallitse ***digna***-resursseja mistä tahansa.
- **Consistency and Reliability:** Varmistaa luotettavat toiminnot dokumentoiduilla, versionhallituilla komennoilla.
- **Scalability:** Käsittelee suuria toimintoja yritystason tarpeisiin.
- **Learning and Mastery:** Tarjoaa syvemmän ymmärryksen ***digna***-alustan toiminnallisuudesta.
- **Integration with Other Tools:** Integroituu saumattomasti automaatiotyökaluihin kuten Control-M, UC4, AutomateNOW!

---

## Asennusohjeet Windowsille

Aloittaaksesi noudata alla olevia ohjeita purkaaksesi tarvittavat tiedostot, sijoittaaksesi *dignacli*-kansion ja konfiguroidaksesi yhteytesi ***digna***-repositorioon. Varmista, että sinulla on repositorion tunnukset ja kaikki tarvittavat konfiguraatiotiedot valmiina ennen aloittamista.

1. **Pura ***digna*** CLI:**
   - Hanki `.zip`-tiedosto, joka sisältää ***digna*** CLI:n.
   - Pura tiedosto haluamaasi hakemistoon.

2. **Siirrä `dignacli`-kansio:**
   - Kopioi `dignacli`-kansio haluamaasi asennussijaintiin (esim. `C:\Program Files\***digna***`).

3. **`config.toml`-tiedoston konfigurointi:**
   - Tarkista `dignacli`-kansion sisältä, löytyykö `config.toml`.
   - Nimeä tarvittaessa `config_template.toml` uudelleen `config.toml`-ksi ja konfiguroi se toimitetun dokumentaation mukaisesti.
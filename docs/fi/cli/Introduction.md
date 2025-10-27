## Komentoriviliittymän (CLI) tarkoitus

***digna*** komentoriviliittymä (CLI) on tehokas työkalu, joka on suunniteltu sujuvoittamaan vuorovaikutusta ***digna***-alustan kanssa. Se tarjoaa tekstipohjaisen käyttöliittymän, jonka avulla käyttäjät voivat suorittaa laajan valikoiman tehtäviä tehokkaasti ilman graafista käyttöliittymää.

### Keskeiset ominaisuudet:

- **Tehokkuus ja joustavuus:** CLI mahdollistaa komentojen nopean suorittamisen ja parantaa tuottavuutta.
- **Automaatio:** Tukee skriptausta toistuvien tehtävien automatisoimiseksi.
- **Etäkäyttö:** Hallitse ***digna***-resursseja mistä tahansa.
- **Johdonmukaisuus ja luotettavuus:** Varmistaa luotettavat toiminnot dokumentoiduilla, versionhallituilla komennoilla.
- **Skaalautuvuus:** Soveltuu laajamittaisiin yritystehtäviin.
- **Oppiminen ja hallinta:** Tarjoaa syvemmän ymmärryksen ***digna***-alustan toiminnallisuuksista.
- **Integraatio muiden työkalujen kanssa:** Integroituu saumattomasti automaatiotyökalujen kuten Control-M, UC4 ja AutomateNOW! kanssa.

---

## Asennusohjeet Windowsille

Aloittaaksesi suorita alla olevat vaiheet purkaaksesi tarvittavat tiedostot, sijoittaaksesi *dignacli*‑kansion ja määrittääksesi yhteytesi ***digna***-repositorioon. Varmista, että sinulla on repositorion käyttöoikeustiedot ja kaikki tarvittavat määritystiedot valmiina ennen aloittamista.

1. **Extracting the ***digna*** CLI:**
   - Hanki the `.zip`-tiedosto, joka sisältää ***digna*** CLI:n.
   - Pura tiedosto haluamaasi hakemistoon.

2. **Deploying the `dignacli` Folder:**
   - Kopioi `dignacli`-kansio haluamaasi asennussijaintiin (esim. `C:\Program Files\***digna***`).

3. **Configuring `config.toml`:**
   - Tarkista `dignacli`-kansion sisältä, löytyykö `config.toml`.
   - Nimeä `config_template.toml` tarvittaessa `config.toml`-tiedostoksi ja konfiguroi se toimitetun dokumentaation mukaisesti.
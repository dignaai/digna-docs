---
title: Data Analytics – Trendit, vakaus & pitkän aikavälin näkemykset | digna-dokumentaatio
description: Opi, kuinka digna Data Analytics paljastaa pitkän aikavälin trendejä, volatiliteettia ja datan vakautta KPI:issä. Havaitse muutokset datan laadussa ja havaittavuudessa, löydä piilevät anomaliat ja muunna tilastot käyttökelpoisiksi oivalluksiksi.
canonical_url: https://docs.digna.ai/platform/data_analytics/
image: /assets/logo_square.png
keywords:
  - data-analytiikka
  - datan vakaus
  - datan trendit
  - volatiliteetin havaitseminen
  - data-observability
  - datan laatu
  - datan monitorointi
  - aikasarja-analyysi
  - digna data analytics
  - kpi-vakaus
lang: fi
robots: index, follow
og_title: Data Analytics – Trendit, vakaus & pitkän aikavälin näkemykset | digna-dokumentaatio
og_description: digna Data Analytics havaitsee pitkän aikavälin trendejä, volatiliteettia ja datan vakautta. Tutustu, kuinka seurata KPI:itä, havaita driftit ja muuttaa datatilastot liiketoimintaa ohjaaviksi oivalluksiksi.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Analytics – Trendit ja vakaus
<h1 style="display:none;">AI-ohjattu Data Analytics -moduuli datan laadun ja havaittavuuden (observability) parantamiseen – digna</h1>

---

## Tarkoitus

The **Data Analytics** -moduuli paljastaa **pitkän aikavälin kuvioita, vakautta ja volatiliteettia** dataseteissäsi — muuntaen raakat mittarit merkityksellisiksi oivalluksiksi.  
Se tarjoaa korkeamman tason analytiikkakerroksen *Data Anomalies* -tulosten päälle, mahdollistaen tiimien **muutosten ymmärtämisen ajan kuluessa** sekä sekä **datan laadun** että **dataputkien havaittavuuden** parantamisen.

Tunnistamalla trendikatkoksia, toistuvia kuvioita ja volatiliteetin muutoksia, digna Data Analytics auttaa erottamaan **odotetun kausikäyttäytymisen** ja **todelliset datan laatupoikkeamat**.

---

## Tekninen yleiskatsaus

### Johdetut tilastot
*digna Data Analytics* laskee tilastollisia ominaisuuksia, kuten:

- **Trendi** – mittarin pitkän aikavälin suunta (nouseva, laskeva, vakaa)  
- **Volatiliteetti** – kuinka paljon mittari vaihtelee tietyllä aikavälillä  
- **Sesonkisuus** – toistuvat ajalliset kuviot (päivittäin, viikoittain, kuukausittain)  
- **Muutoskohdat** – tilastollisesti merkitsevät käyttäytymisen muutokset  

### Tuetut mittarit
Moduuli voi analysoida mitä tahansa muiden digna-moduulien tuottamaa metriikkaa, mukaan lukien:

- Tietueiden määrä  
- Puuttuvien arvojen osuus  
- Jakaumatilastot (min, max, keskiarvo, varianssi)  
- KPI-aggregaatit (esim. liikevaihto, transaktiot, korvaushakemukset)  
- Aikataulupoikkeamat tai anomalioiden esiintymistiheydet  

### Aikasarja-analyysi
Data Analytics arvioi **vakautta eri ajanjaksojen välillä** — vertaamalla yhtä viikkoa, kuukautta tai neljännestä toiseen — käyttäen tilastollista luottamustasoa ja visuaalisia mittareita trendin vakaudesta.

---

## Miten se toimii

1. **Syöte** – digna kerää aikasarjamittareita muista moduuleista (esim. anomalioiden määrä).  
2. **Tilastollinen mallinnus** – AI ja tilastofunktiot tunnistavat taustalla olevat trendit ja volatiliteettitasot.  
3. **Ajanjaksojen vertailu** – digna vertailee historiallista ja nykyistä suorituskykyä KPI:ille tai laatuindikaattoreille.  
4. **Oivallusten tuottaminen** – kojelaudat näyttävät havaitut trendit, vakaat jaksot ja muutoskohdat *Inspection Hub*:issa ja analytiikkanäkymissä.  

Tämä mahdollistaa proaktiivisen havaitsemisen *hitaista siirtymistä* tai *asteittaisesta heikentymisestä* datan laadussa ennen kuin ne muuttuvat kriittisiksi.

---

## Esimerkkikäyttötapaukset

| Käyttötapaus | Kuvaus |
|-----------|--------------|
| **KPI-vakauden seuranta** | Seuraa myyntiä, transaktioita tai korvaushakemuksia ajan kuluessa ja havaitse epätavallinen volatiliteetti. |
| **Piilotetun datasiirtymän havaitseminen** | Tarkkaile hitaita muutoksia datan jakaumissa tai puuttuvien arvojen osuuksissa, jotka tavanomaiset säännöt usein ohittavat. |
| **Muutoskohtien analyysi** | Tunnista milloin mittari muuttaa käyttäytymistään (esim. yhtäkkiä lisääntyvät anomalioiden määrät). |
| **Toiminnallinen luotettavuus** | Arvioi jaksoja, joina datan vakaus on korkea vs. matala eri järjestelmissä tai osastoilla. |
| **Liiketoiminnan oivallukset** | Korosta parhaiten suoriutuvia kategorioita tai tuotteita liukuvilla ajanjaksoilla. |

---

## Hyödyt

| Alue | Hyöty |
|------|----------|
| **Näkyvyys** | Tarjoaa pitkän aikavälin näkemyksen datan laadun trendeistä ja kuvioista. |
| **Varhainen varoitus** | Havaitsee hitaita siirtymiä ennen kuin ne laukaisevat anomalioita tai SLA-loukkauksia. |
| **Optimointi** | Auttaa tunnistamaan epävakaita datalähteitä tai järjestelmiä, jotka tarvitsevat prosessien hienosäätöä. |
| **Ristimoduulinen analyysi** | Yhdistää dataa moduuleista Data Anomalies, Data Validation ja Data Timeliness kokonaisvaltaisten oivallusten saamiseksi. |
| **Toimintaan perustuvat oivallukset** | Tukee sekä teknisiä tiimejä että liiketoiminnan käyttäjiä ymmä... |
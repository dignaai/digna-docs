# Muudatused – Väljalase 2025.09

Väljalaskega 2025.09 tutvustab digna uut **moodulitest koosnevat arhitektuuri** ja käivitab **viis spetsialiseeritud moodulit** andmete kvaliteedi ja observeeritavuse jaoks.  
See versioon tugevdab ka autentimist ning parandab teavituste haldamist platvormil.

---

## Uued funktsioonid

### Mooduline ülesehitus
- digna kasutab nüüd **moodulitest koosnevat arhitektuuri**.  
- Kliendid saavad aktiveerida ainult need moodulid, mida nad vajavad, ning lisada uusi, kui nõuded kasvavad.  
- Varasem funktsionaalsus on nüüd osa **digna Data Anomalies**.

### Uued moodulid
- **digna Data Anomalies** – tehisintellektil põhinev anomaaliate tuvastus andmemahtudes, jaotustes ja puuduvates väärtustes.  
- **digna Data Analytics** – aikasarja hindamine vaatlusmõõdikute tuvastamiseks pikaajaliste trendide ja volatiilsuse osas.  
- **digna Data Timeliness** – oodatava andmete saabumise aegade jälgimine, nii tehisintellektil kui reeglitel põhinev.  
- **digna Data Validation** – reeglitel põhinevad kirjetasandi kontrollid, mis tagavad ärireeglite järgimise.  
- **digna Data Schema Tracker** – skeemi muutuste (DDL-i muudatuste) tuvastamine jälgitavates andmebaasides.

### MFA OIDC kaudu
- Tugi **mitmefaktorilisele autentimisele (MFA)** OIDC Single Sign-On kaudu.  
- Tagab ettevõttetasemelise turvalisuse kõigile kasutajate sisselogimistele.

### Moodulipõhised teavitusmeilid
- Teavitused saadetakse nüüd **mooduli kaupa**, mis teeb lihtsamaks alarmide eraldamise Data Anomalies, Data Analytics ja teiste moodulite vahel.

---

## CLI uuendused

- **Uus käsk: `inspect-cancel`** – tühista inspekteerimised päringu ID järgi või lõpetada kõik aktiivsed päringud.  
- **Uus käsk: `check-config`** – valideeri konfiguratsioonifailid enne käivitust.  
- **Uus käsk: `remove-orphans`** – puhasta orvuks jäänud repositooriumi kirjed.  
- **Täiendatud `inspect` käsk** – uus valik `--bypass-backend` (`-bb`) ja standardiseeritud väljumiskoodid (`0 = OK, 1 = INFO, 2 = WARNING`).

## Dokumentatsioon
- Uued juhendid:  
  - Single Sign-On integratsiooni juhend
---
title: digna CLI Reference 2025.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2025.109 Learn how to manage users, repositories, and data with commands such as add-user, check-config, check-repo-connection, inspect, inspect-async, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.09
**2025-09-29**

See lehekülg dokumenteerib kogu käsustiku, mis on saadaval ***digna*** CLI versioonis **2025.09**, kaasa arvatud kasutusnäited ja valikud.

---

## CLI põhialused

---

### help
Valik `--help` annab teavet saadaolevate käskude ja nende kasutuse kohta. Selle valiku kasutamiseks on kaks peamist viisi:

1. **Üldise abi kuvamine:**
   
   Kasuta `--help` kohe pärast sõna ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Abi konkreetse käsu kohta:**  
  
   Täpsema info saamiseks konkreetse käsu kohta lisa sellele `--help`.  
   Näiteks, et saada abi käsuga `add-user`, käivita:
   ```bash
   dignacli add-user --help
   ```

   ### väljund:
      
   - **Käsu kirjeldus:** Annab üksikasjaliku ülevaate, mida käsk teeb.  
   - **Süntaks:** Näitab täpset süntaksit, sh nõutud ja valikulisi argumente.  
   - **Valikud:** Loetleb käsule spetsiifilised valikud koos selgitustega.  
   - **Näited:** Esitab näiteid käsu efektiivseks käivitamiseks.

### check-config

Käsk `check-config` on utiliit ***digna*** CLI tööriistas, mis testib ***digna*** konfiguratsiooni. See käsk kontrollib, kas ***digna*** komponendid leiavad vajalikud konfiguratsioonielemendid failist config.toml.

#### Valikud

- `--configpath`, `-cp`: Fail või kataloog, mis sisaldab konfiguratsiooni. Kui seda ei anta, siis kasutatakse ../config.toml.
      
#### Käsu kasutus
```bash
dignacli check-config
```

Eduka käivituse korral väljastab käsk kinnituse, et konfiguratsioon on täielik.  
  
Kui konfiguratsioon tundub puudulik, loetletakse ära puuduvad konfiguratsioonielemendid.

  
### check-repo-connection

Käsk `check-repo-connection` on utiliit ***digna*** CLI tööriistas, mis testib ühenduvust ja ligipääsu määratud ***digna*** repositooriumile. See käsk kontrollib, kas CLI saab repositooriumiga suhelda.
      
#### Käsu kasutus
```bash
dignacli check-repo-connection
```

Eduka käivituse korral väljastab käsk kinnituse ühenduse kohta ning repositooriumi üksikasjad: Repository version, Host, Database ja Schema.  
  
Kui repositooriumiga ühendus ei õnnestu, kontrolli config.toml faili, et konfiguratsiooniseaded oleksid õiged.


### version

Paigaldatud *dignacli* versiooni kontrollimiseks kasuta valikut `--version`.  
  
#### Käsu kasutus
```bash
dignacli --version
```
  
#### Näide väljundist
```bash
dignacli version 2025.09
```

### logimise valikud
  
Vaiketena on ***digna*** käskude konsooliväljund minimalistlik. Enamik käske võimaldab pakkuda lisainfot, kasutades järgmisi valikuid:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ ja „debug“ määravad detailide taset, samas kui „logfile“ lüliti võimaldab suunata väljundi faili, mitte konsooli aknasse.

## Kasutajate haldus

### add-user
  
Käsk `add-user` ***digna*** CLI-s kasutatakse uue kasutaja lisamiseks ***digna*** süsteemi.
  
#### Käsu kasutus
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumendid

- **USER_NAME**: Uue kasutaja kasutajanimi (nõutud).
- **USER_FULL_NAME**: Uue kasutaja täielik nimi (nõutud).
- **USER_PASSWORD**: Uue kasutaja parool (nõutud).

#### Valikud

- `--is_superuser`, `-su`: Lipp, mis määrab uue kasutaja administraatoriks.
- `--valid_until`, `-vu`: Määrab kasutajakonto aegumiskuupäeva vormingus `YYYY-MM-DD HH:MI:SS`. Kui seda ei määrata, siis kontol pole aegumiskuupäeva.

#### Näide

Uue kasutaja lisamiseks kasutajanimega `jdoe`, täisnimega `John Doe` ja parooliga `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Uue kasutaja lisamiseks ja konto aegumiskuupäeva määramiseks:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Käsk `delete-user` ***digna*** CLI-s kasutatakse olemasoleva kasutaja eemaldamiseks ***digna*** süsteemist.
  
#### Käsu kasutus
```bash
dignacli delete-user USER_NAME
```
  
#### Argumendid
- **USER_NAME**: Eemaldatava kasutaja kasutajanimi (nõutud). See on käsu ainus nõutav argument.

#### Näide
```bash
dignacli delete-user jdoe
```
  
Selle käsu käivitamisel eemaldatakse kasutaja `jdoe` ***digna*** süsteemist, tühistades tema juurdepääsu ja kustutades seotud andmed ning õigused repositooriumist.

### modify-user

Käsk `modify-user` ***digna*** CLI-s kasutatakse olemasoleva kasutaja andmete uuendamiseks ***digna*** süsteemis.

#### Käsu kasutus
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumendid
  
- **USER_NAME**: Muudetava kasutaja kasutajanimi (nõutud).
- **USER_FULL_NAME**: Kasutaja uus täielik nimi (nõutud).
  
#### Valikud  
  
- `--is_superuser`, `-su`: Määrab kasutaja superkasutajaks, andes kõrgendatud õigused. Selle lipu kasutamisel ei ole vaja väärtust.  
- `--valid_until`, `-vu`: Määrab kasutajakonto aegumiskuupäeva vormingus YYYY-MM-DD HH:MI:SS. Kui seda ei anta, jääb konto kehtima piiramatult.  
  
#### Näide
  
Kasutaja `jdoe` täisnime muutmiseks „Johnathan Doe“ ja tema määramiseks superkasutajaks:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Käsk `modify-user-pwd` ***digna*** CLI-s kasutatakse olemasoleva kasutaja parooli muutmiseks ***digna*** süsteemis.
  
#### Käsu kasutus
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumendid
  
- **USER_NAME**: Parooli muudetava kasutaja kasutajanimi (nõutud).
- **USER_PWD**: Kasutaja uus parool (nõutud).
  
#### Näide
  
Parooli muutmiseks kasutajale `jdoe` uueks `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Käsk `list-users` ***digna*** CLI-s kuvab nimekirja kõigist registreeritud kasutajatest ***digna*** süsteemis.

#### Käsu kasutus

```bash
dignacli list-users
```

Käsu käivitamisel ühendub ***digna*** CLI ***digna*** repositooriumiga ja kuvab kõik kasutajad, näidates nende ID-d, kasutajanime, täielikku nime, superkasutaja staatust ja aegumisaegasid.

## Repositooriumi haldus

### upgrade-repo
  
Käsk `upgrade-repo` ***digna*** CLI-s kasutatakse ***digna*** repositooriumi uuendamiseks või initsialiseerimiseks. See käsk on vajalik uuenduste rakendamiseks või repositooriumi esmakordseks ettevalmistamiseks.
  
#### Käsu kasutus

```bash
dignacli upgrade-repo [options]
```
  
#### Valikud
  
- `--simulation-mode`, `-s`: Kui lubatud, töötab käsk simulatsioonirežiimis, mis prindib välja SQL-lauseid, mis oleksid täidetud, kuid ei käivita neid tegelikult. See on kasulik muudatuste eelvaatamiseks ilma repositooriumit muutmata.  

  
#### Näide
  
***digna*** repositooriumi uuendamiseks käivita käsk ilma valikuteta:
  
```bash
dignacli upgrade-repo
```  
Uuenduse käivitamiseks simulatsioonirežiimis (näha SQL-lauseid ilma neid rakendamata):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
See käsk on oluline ***digna*** süsteemi hooldamiseks, tagades, et andmebaasi skeem ja teised repositooriumi komponendid oleksid kooskõlas tarkvara viimase versiooniga.

### encrypt
  
Käsk `encrypt` ***digna*** CLI-s kasutatakse parooli krüpteerimiseks.
  
#### Käsu kasutus
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumendid
- **PASSWORD**: Parool, mida on vaja krüpteerida (nõutud).
  
#### Näide
  
Parooli krüpteerimiseks tuleb parool anda argumendina.  
Näiteks parooli `mypassword123` krüpteerimiseks kasuta:
```bash
dignacli encrypt mypassword123
```
See käsk väljastab antud parooli krüpteeritud versiooni, mida saab seejärel kasutada turvalistes kontekstides. Kui parooli argumenti ei anta, kuvab CLI vea, mis näitab puuduva argumendi.

### generate-key
  
Käsku `generate-key` kasutatakse Fernet-võtme genereerimiseks, mis on vajalik paroolide turvaliseks salvestamiseks ***digna*** repositooriumis.
  
#### Käsu kasutus
```bash
dignacli generate-key
```
  
## Andmete haldus

### clean-up

Käsk `clean-up` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja traffic light system andmete eemaldamiseks ühelt või mitmelt andmeallikalt määratud projekti piires. See käsk on oluline andmete elutsükli haldamiseks, aidates hoida andmekeskkonda korrastatuna ja efektiivsena, kustutades aegunud või mittevajalikke andmeid.

#### Käsu kasutus

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, kust andmeid eemaldatakse (nõutud). Kui selles argumendis kasutatakse märksõna all-projects, käsib see ***digna***l iteratsiooni kõigi olemasolevate projektide üle ja käsk rakendatakse igale projektile.
- **FROM_DATE**: Andmete eemaldamise alguskuupäev ja kellaaeg. Aktsepteeritavad vormingud hõlmavad %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutud).
- **TO_DATE**: Andmete eemaldamise lõppkuupäev ja kellaaeg, järgides samu vorminguid nagu FROM_DATE (nõutud).
  
#### Valikud
  
- `--table-name`, `-tn`: Piirab clean-up toimingu konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, piirates clean-up'i ainult tabelitele, mille nimedes esineb antud alamsõne.
- `--timing`, `-tm`: Kuvab clean-up protsessi kestuse pärast lõpuleviimist.
- `--help`: Kuvab help-i info clean-up käsu kohta ja väljub.
  
#### Näide
  
Andmete eemaldamiseks projektist ProjectA ajavahemikus 1. jaanuar 2023 kuni 30. juuni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Andmete eemaldamiseks ainult konkreetsest tabelist nimega `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
See käsk aitab hallata andmete salvestamist ja tagab, et repositoorium sisaldab ainult asjakohast informatsiooni.

### remove-orphans
  
Käsk `remove-orphans` ***digna*** CLI-s kasutatakse repositooriumi korrastamiseks.  
Kui kasutaja kustutab projekte või andmeallikaid, jäävad profiilid ja ennustused repositooriumisse. Selle käsu abil eemaldatakse sellised orvustatud read repositooriumist.
  
#### Käsu kasutus
  
```bash
dignacli list-projects
```

### list-projects
  
Käsk `list-projects` ***digna*** CLI-s kuvab nimekirja kõigist saadaolevatest projektidest ***digna*** süsteemis.
  
#### Käsu kasutus
  
```bash
dignacli list-projects
```

See käsk on eriti kasulik administraatoritele ja kasutajatele, kes haldavad mitut projekti, pakkudes kiiret ülevaadet repositooriumis olemasolevatest projektidest.

### list-ds

Käsk `list-ds` ***digna*** CLI-s kuvab nimekirja kõigist saadaolevatest andmeallikatest määratud projektis. See käsk on kasulik andmevarade ülevaatamiseks, mis on saadaval analüüsiks ja halduseks ***digna*** süsteemis.

#### Käsu kasutus
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, mille andmeallikad listitakse (nõutud).
  
#### Näide
  
Kõigi andmeallikate listimiseks projektis `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
See käsk annab kasutajatele ülevaate projekti andmeallikatest, aidates neil andmekeskkonda paremini navigeerida ja hallata.


### inspect

Käsk `inspect` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja traffic light system andmete loomiseks ühelt või mitmelt andmeallikalt määratud projektis. See käsk aitab andmeid analüüsida ja jälgida määratud perioodi jooksul. Inspektsiooni lõpetamisel tagastatakse arvutatud traffic light system väärtus:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Käsu kasutus

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid inspekteeritakse (nõutud). Kui selles argumendis kasutatakse märksõna all-projects, käsib see ***digna***l iteratsiooni kõigi olemasolevate projektide üle ja käsk rakendatakse igale projektile.
- **FROM_DATE**: Inspektsiooni alguskuupäev ja kellaaeg. Aktsepteeritavad vormingud hõlmavad %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutud).
- **TO_DATE**: Inspektsiooni lõppkuupäev ja kellaaeg, järgides samu vorminguid nagu FROM_DATE (nõutud).
  
#### Valikud

- `--table-name`, `-tn`: Piirab inspektsiooni konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, inspekteerides ainult tabelid, mille nimedes esineb antud alamsõne.
- `--enable_notification`, `-en`: Lubab teavituste saatmise häirete korral.
- `--bypass-backend`, `-bb`: Mingib backend-i vahele ja käivitab inspektsiooni otse CLI-st (ainult testimiseks!).

  
#### Näide
  
Andmete inspekteerimiseks projektis `ProjectA` ajavahemikus 1. jaanuar 2024 kuni 31. jaanuar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Ainult konkreetse tabeli inspekteerimiseks ja ennustuste sunnitud ümberarvutamiseks:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
See käsk on kasulik värskendatud profiilide ja ennustuste genereerimiseks, andmete terviklikkuse jälgimiseks ja häirete haldamiseks määratud projekti ajavahemikus.

### inspect-async

Käsk `inspect-async` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja traffic light system andmete loomiseks ühelt või mitmelt andmeallikalt määratud projektis. See käsk aitab andmeid analüüsida ja jälgida määratud perioodi jooksul. Erinevalt sünkroonsest `inspect` käsust ei oota see inspektsiooni lõppemist. Selle asemel tagastatakse esitatud inspektsioonipäringu request id. Inspektsiooni protsessi edenemise pärimiseks kasuta käsku `inspect-status`.

#### Käsu kasutus

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid inspekteeritakse (nõutud). Kui selles argumendis kasutatakse märksõna all-projects, käsib see ***digna***l iteratsiooni kõigi olemasolevate projektide üle ja käsk rakendatakse igale projektile.
- **FROM_DATE**: Inspektsiooni alguskuupäev ja kellaaeg. Aktsepteeritavad vormingud hõlmavad %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutud).
- **TO_DATE**: Inspektsiooni lõppkuupäev ja kellaaeg, järgides samu vorminguid nagu FROM_DATE (nõutud).
  
#### Valikud

- `--table-name`, `-tn`: Piirab inspektsiooni konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, inspekteerides ainult tabelid, mille nimedes esineb antud alamsõne.
- `--enable_notification`, `-en`: Lubab teavituste saatmise häirete korral.

  
#### Näide
  
Andmete inspekteerimiseks projektis `ProjectA` ajavahemikus 1. jaanuar 2024 kuni 31. jaanuar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Käsk `inspect-status` ***digna*** CLI-s kasutatakse asünkroonse inspektsiooni edenemise kontrollimiseks, lähtudes request ID-st.

#### Käsu kasutus

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumendid
  
- **REQUEST_ID**: Request id, mille tagastas `inspect-async` käsk.
  
#### Näide
  
Inspektsiooni edenemise kontrollimiseks request ID-ga 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Käsk `inspect-cancel` ***digna*** CLI-s kasutatakse inspektsioonide tühistamiseks request ID alusel või kõigi jooksvate/pending-päringute tühistamiseks.

#### Käsu kasutus

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumendid
  
- **REQUEST_ID**: Request id, mille tagastas `inspect-async` käsk.
  
#### Näide
  
Inspektsiooni tühistamiseks request ID-ga 12345:
  
```bash
dignacli inspect-cancel 12345
```

Kõigi praegu töötavate või järjekorras olevate päringute tühistamiseks:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Käsk `export-ds` ***digna*** CLI-s kasutatakse andmeallikate eksportimiseks ***digna*** repositooriumist. Vaiketäpsusega eksporditakse kõik antud projekti andmeallikad.

#### Käsu kasutus
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kust andmeallikad eksporditakse.

#### Valikud

- `--table_name`, `-tn`: Ekspordib konkreetse andmeallika projektist.
- `--exportfile`, `-ef`: Määrab ekspordi faili nime.
    
#### Näide
  
Kõigi andmeallikate eksportimiseks projektist `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
See käsk ekspordib kõik `ProjectA` andmeallikad JSON-dokumendina, mida saab importida teise projekti või ***digna*** repositooriumisse.


### import-ds

Käsk `import-ds` ***digna*** CLI-s kasutatakse andmeallikate importimiseks sihtprojekti ja import-aruande koostamiseks.

#### Käsu kasutus
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kuhu andmeallikad imporditakse.
- **EXPORT_FILE**: Ekspordi faili nimi, mida imporditakse.

#### Valikud

- `--output-file`, `-o`: Fail, kuhu salvestada import-aruanne (kui pole määratud, prinditakse konsooli tabelina).
- `--output-format`, `-f`: Vorming, milles import-aruanne salvestatakse (json, csv).
    
#### Näide
  
Kõigi andmeallikate importimiseks ekspordifailist `my_export.json` projekti `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Pärast importi kuvab käsk ka aruande imporditud ja vahele jäetud objektide kohta. Ainult uued andmeallikad imporditakse `ProjectB`-sse. Selleks, et teada saada, millised objektid imporditakse ja millised vahele jäetakse, võid kasutada käsku `plan-import-ds`.

### plan-import-ds

Käsk `plan-import-ds` ***digna*** CLI-s kasutatakse andmeallikate importimise plaani koostamiseks sihtprojekti jaoks ja import-aruande loomiseks ilma tegeliku impordita.

#### Käsu kasutus
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kuhu andmeallikad imporditakse (plaanis).
- **EXPORT_FILE**: Ekspordi faili nimi, mida analüüsitakse enne importi.

#### Valikud

- `--output-file`, `-o`: Fail, kuhu salvestada import-aruanne (kui pole määratud, prinditakse konsooli tabelina).
- `--output-format`, `-f`: Vorming, milles import-aruannet salvestatakse (json, csv).
    
#### Näide
  
Selleks, et kontrollida, millised andmeallikad imporditakse ja millised jäetakse vahele ekspordifailist `my_export.json`, kui neid imporditakse projekti `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
See käsk kuvab ainult impordiplaani objektide kohta, mis imporditakse ja mis jäetakse vahele.
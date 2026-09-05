---
title: digna CLI viide 2026.04 – käsud ja näited | digna Dokumentatsioon
description: Täielik viide digna CLI väljaandele 2026.04
image: /assets/logo_square.png
---

# digna CLI viide 2026.04
**2026-04-08**

See leht dokumenteerib kõiki käsklusi, mis on saadaval ***digna*** CLI väljaandes **2026.04**, sealhulgas kasutusnäited ja valikud.

---

## CLI põhialused

---

### help
Valik `--help` annab teavet saadavalolevate käskude ja nende kasutuse kohta. Selle valiku kasutamiseks on kaks peamist moodust:

1. **Üldise abi kuvamine:**
   
    Kasuta --help kohe pärast märksõna ***digna***  
   ```bash
   dignacli --help
   ```

2. **Spetsiifilise käsu abi saamine:**  
  
    Konkreetse käsu kohta täpsema info saamiseks lisa sellele käsule `--help`.
    Näiteks, et saada abi käsuga `add-user`, käivita:
     ```bash
     dignacli add-user --help
     ```

     ### väljund:
      
     - **Käsu kirjeldus:** Pakub üksikasjalikku selgitust, mida käsk teeb.  
     - **Süntaks:** Näitab täpset süntaksit, sealhulgas kohustuslikke ja valikulisi argumente.  
     - **Valikud:** Loetleb käsu spetsiifilised valikud koos selgitustega.  
     - **Näited:** Esitab näiteid käsu tõhusaks käivitamiseks.

### check-config

käsk check-config on utiliit ***digna*** CLI tööriistas, mis on mõeldud ***digna*** konfiguratsiooni testimiseks. See käsk kontrollib, et ***digna*** komponendid suudaksid leida vajalikud konfiguratsiooni elemendid config.toml failist.

#### Valikud

- `--configpath`, `-cp`: Fail või kataloog, mis sisaldab konfiguratsiooni. Kui seda ei määrata, kasutatakse ../config.toml.

#### Käsu kasutus
```bash
dignacli check-config
```

Õnnestunud täitmise korral annab käsk kinnituse konfiguratsiooni täielikkuse kohta.  
  
Kui konfiguratsioon tundub olevat puudulik, loetletakse puuduolevad konfiguratsiooni elemendid.

  
### check-repo-connection

käsk check-repo-connection on utiliit ***digna*** CLI tööriistas, mis testib ühenduvust ja juurdepääsu määratud ***digna*** repositooriumile. See käsk tagab, et CLI saab repositooriumiga suhelda.
      
#### Käsu kasutus
```bash
dignacli check-repo-connection
```

Õnnestunud täitmise korral annab käsk ühenduse kinnituse koos repositooriumi üksikasjadega: Repository version, Host, Database and Schema.  
  
Kui repositooriumiga ühendus ei õnnestu, kontrolli config.toml faili, et konfiguratsiooniseaded oleksid õiged.


### version

Paigaldatud *dignacli* versiooni kontrollimiseks kasuta valikut --version.  
  
#### Käsu kasutus
```bash
dignacli --version
```
  
#### Näiduväljund
```bash
dignacli version 2026.04
```

### logimise valikud
  
Vaikimisi on ***digna*** käskude konsooli väljund minimalistlik. Enamik käske võimaldab täiendava info kuvamist järgmiste valikutega:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ja “debug” määravad detailide taset, samas kui “logfile” lüliti võimaldab väljundi ümber suunata faili asemel konsooli.

## Kasutajate haldus

### add-user
  
käsk add-user ***digna*** CLI-s kasutatakse uue kasutaja lisamiseks ***digna*** süsteemi.
  
#### Käsu kasutus
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumendid

- **USER_NAME**: Uue kasutaja kasutajanimi (kohustuslik).
- **USER_FULL_NAME**: Uue kasutaja täielik nimi (kohustuslik).
- **USER_PASSWORD**: Uue kasutaja parool (kohustuslik).

#### Valikud

- `--is_superuser`, `-su`: Lipp, et määrata uus kasutaja administraatoriks.
- `--valid_until`, `-vu`: Määrab kasutajakonto aegumiskuupäeva vormingus `YYYY-MM-DD HH:MI:SS`. Kui seda ei määrata, ei aeguma konto.

#### Näide

Uue kasutaja lisamiseks kasutajanimega `jdoe`, täieliku nimega `John Doe` ja parooliga `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Uue kasutaja lisamiseks ja konto aegumiskuupäeva seadistamiseks:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
käsk `delete-user` ***digna*** CLI-s kasutatakse olemasoleva kasutaja eemaldamiseks ***digna*** süsteemist.
  
#### Käsu kasutus
```bash
dignacli delete-user USER_NAME
```
  
#### Argumendid
- **USER_NAME**: Kustutatava kasutaja kasutajanimi (kohustuslik). See on käsu ainus nõutud argument.

#### Näide
```bash
dignacli delete-user jdoe
```
  
Selle käsu täitmine eemaldab kasutaja `jdoe` ***digna*** süsteemist, tühistades tema juurdepääsu ja kustutades seotud andmed ning õigused repositooriumist.

### modify-user

käsk `modify-user` ***digna*** CLI-s kasutatakse olemasoleva kasutaja andmete uuendamiseks ***digna*** süsteemis.

#### Käsu kasutus
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumendid
  
- **USER_NAME**: Muudetava kasutaja kasutajanimi (kohustuslik).
- **USER_FULL_NAME**: Kasutaja uus täielik nimi (kohustuslik).
  
#### Valikud  
  
- `--is_superuser`, `-su`: Määrab kasutaja superkasutajaks, andes kõrgendatud privileegid. Sellel lipul ei ole vaja väärtust.  
- `--valid_until`, `-vu`: Määrab kasutajakonto aegumiskuupäeva vormingus YYYY-MM-DD HH:MI:SS. Kui seda ei anta, jääb konto kehtima määramata ajani.  
  
#### Näide
  
Et muuta kasutaja `jdoe` täielik nimi “Johnathan Doe” ja teha temast superkasutaja:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
käsk `modify-user-pwd` ***digna*** CLI-s kasutatakse olemasoleva kasutaja parooli muutmiseks ***digna*** süsteemis.
  
#### Käsu kasutus
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumendid
  
- **USER_NAME**: Parooli muutmisele alluv kasutajanimi (kohustuslik).
- **USER_PWD**: Kasutaja uus parool (kohustuslik).
  
#### Näide
  
Et muuta kasutaja `jdoe` parooliks `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

käsk `list-users` ***digna*** CLI-s kuvab nimekirja kõigist ***digna*** süsteemis registreeritud kasutajatest.

#### Käsu kasutus

```bash
dignacli list-users
```

Selle käsu käivitamisel ühendub ***digna*** CLI ***digna*** repositooriumiga ja loetleb kõik kasutajad, näidates nende ID-d, kasutajanime, täielikku nime, superkasutaja staatust ja aegumistähtaja märgiseid.

## Repositooriumi haldus

### upgrade-repo
  
käsk `upgrade-repo` ***digna*** CLI-s kasutatakse ***digna*** repositooriumi uuendamiseks või initsialiseerimiseks. See käsk on oluline uuenduste rakendamiseks või repositooriumi infrastruktuuri esmakordseks seadistamiseks.
  
#### Käsu kasutus

```bash
dignacli upgrade-repo [options]
```
  
#### Valikud
  
- `--simulation-mode`, `-s`: Kui see on lubatud, töötab käsk simulatsioonirežiimis, mis prindib välja SQL laused, mida täidetaks, kuid ei käivita neid tegelikult. See on kasulik muudatuste eelvaatamiseks ilma repositooriumi muutmata.  

  
#### Näide
  
Et uuendada ***digna*** repositooriumi, võid käivitada käsu ilma valikuteta:
  
```bash
dignacli upgrade-repo
```  
Et käivitada uuendus simulatsioonirežiimis (näha SQL lauseid ilma nende rakendamiseta):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
See käsk on kriitilise tähtsusega ***digna*** süsteemi hooldamisel, tagades, et andmebaasi skeem ja muud repositooriumi komponendid oleksid ajakohased tarkvara viimase versiooniga.

### encrypt
  
käsk `encrypt` ***digna*** CLI-s kasutatakse parooli krüpteerimiseks.
  
#### Käsu kasutus
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumendid
- **PASSWORD**: Parool, mida tuleb krüpteerida (kohustuslik).
  
#### Näide
  
Parooli krüpteerimiseks tuleb see anda argumendina.   
Näiteks, et krüpteerida parool `mypassword123`, kasutage:
```bash
dignacli encrypt mypassword123
```
See käsk väljastab antud parooli krüpteeritud versiooni, mida saab seejärel kasutada turvalistes kontekstides. Kui parooli argumendi ei anta, kuvab CLI vea puuduva argumendi kohta.

### generate-key
  
käsk `generate-key` genereerib Fernet-võtme, mis on vajalik repositooriumis salvestatud paroolide turvamiseks.
  
#### Käsu kasutus
```bash
dignacli generate-key
```
  
## Andmete haldus

### clean-up

käsk `clean-up` ***digna*** CLI-s kasutatakse profilide, ennustuste ja liiklusmärgisüsteemi andmete eemaldamiseks ühelt või mitmelt andmeallikalt määratud projekti piires. See käsk on oluline andmete elutsükli haldamiseks, aidates hoida organiseeritud ja tõhusat andmekeskkonda, kustutades aegunud või mittevajalikke andmeid.

#### Käsu kasutus

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, kust andmeid eemaldatakse (kohustuslik). Kui selle argumendina kasutatakse märksõna all-projects, käsib see ***digna***-l iteratsiooni kõigi olemasolevate projektide üle ja rakendada käsku igale projektile.
- **FROM_DATE**: Andmete eemaldamise alguskuupäev ja -kellaaeg. Aktsepteeritud vormingud: %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (kohustuslik).
- **TO_DATE**: Andmete eemaldamise lõppkuupäev ja -kellaaeg, sama vorminguga nagu FROM_DATE (kohustuslik).
  
#### Valikud
  
- `--table-name`, `-tn`: Piirab clean-up toimingu konkreetsele tabelile projekti sees.
- `--table-filter`, `-tf`: Filtrid, et piirata clean-up ainult tabelitele, mille nimedes on määratud alamsõne.
- `--timing`, `-tm`: Kuvab clean-up protsessi kestuse pärast lõpetamist.
- `--help`: Kuvab clean-up käsu abiinfot ja väljub.
  
#### Näide
  
Andmete eemaldamiseks projektist ProjectA ajavahemikus 1. jaanuar 2023 kuni 30. juuni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Andmete eemaldamiseks ainult konkreetsest tabelist nimega `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
See käsk aitab hallata andmemahtu ja tagada, et repositoorium sisaldab ainult asjakohast teavet.

### remove-orphans
  
käsk `remove-orphans` ***digna*** CLI-s kasutatakse repositooriumi korrastamiseks.  
Kui kasutaja kustutab projekte või andmeallikaid, jäävad profiilid ja ennustused repositooriumisse. Selle käsuga eemaldatakse sellised orvuks jäänud read repositooriumist.
  
#### Käsu kasutus
  
```bash
dignacli list-projects
```

### list-projects
  
käsk `list-projects` ***digna*** CLI-s kuvab kõigi saadavalolevate projektide nimekirja ***digna*** süsteemis.
  
#### Käsu kasutus
  
```bash
dignacli list-projects
```

See käsk on eriti kasulik administraatoritele ja kasutajatele, kes haldavad mitut projekti, pakkudes kiiret ülevaadet saadavalolevatest projektidest ***digna*** repositooriumis.

### list-ds

käsk `list-ds` ***digna*** CLI-s kuvab kõigi saadavalolevate andmeallikate nimekirja määratud projektis. See käsk aitab mõista analüütika ja halduse jaoks olemasolevaid andmevaraüksusi ***digna*** süsteemis.

#### Käsu kasutus
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, mille andmeallikaid loetletakse (kohustuslik).
  
#### Näide
  
Kõigi andmeallikate loetlemiseks projektis nimega `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
See käsk annab kasutajatele ülevaate projekti andmeallikatest, aidates neil andmemaastikku paremini navigeerida ja hallata.


### inspect

käsk `inspect` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja liiklusmärgisüsteemi andmete loomiseks ühelt või mitmelt andmeallikalt määratud projekti piires. See käsk aitab andmeid määratletud perioodi jooksul analüüsida ja jälgida. Pärast inspekteerimise lõppu tagastatakse arvutatud liiklusmärgisüsteemi väärtus:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Käsu kasutus

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid inspekteeritakse (kohustuslik). Kui selle argumendina kasutatakse märksõna all-projects, käsib see ***digna***-l iteratsiooni kõigi olemasolevate projektide üle ja rakendada käsku igale projektile.
- **FROM_DATE**: Inspektsiooni alguskuupäev ja -kellaaeg. Aktsepteeritud vormingud: %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (kohustuslik).
- **TO_DATE**: Inspektsiooni lõppkuupäev ja -kellaaeg, sama vorminguga nagu FROM_DATE (kohustuslik).
  
#### Valikud

- `--table-name`, `-tn`: Piirab inspekteerimise konkreetsele tabelile projekti sees.
- `--table-filter`, `-tf`: Filtrid, et inspekteerida ainult tabeleid, mille nimedes on määratud alamsõne.
- `--enable_notification`, `-en`: Lubab teavituste saatmise häirete korral.
- `--bypass-backend`, `-bb`: Väldi backendit ja käivita inspektsioon otse CLI-st (ainult testimiseks!).

  
#### Näide
  
Andmete inspekteerimiseks projektis `ProjectA` perioodil 1. jaanuar 2024 kuni 31. jaanuar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Ainult konkreetse tabeli inspekteerimiseks ja ennustuste sundarvutuseks:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
See käsk on kasulik uuendatud profiilide ja ennustuste genereerimiseks, andmete terviklikkuse jälgimiseks ning häiresüsteemide haldamiseks määratud projekti ajavahemikus.

### inspect-async

käsk `inspect-async` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja liiklusmärgisüsteemi andmete loomiseks ühelt või mitmelt andmeallikalt määratud projekti piires. See käsk aitab andmeid määratletud perioodi jooksul analüüsida ja jälgida. Erinevalt sünkroonsest `inspect` käsust ei oota see inspektsiooni lõpuleviimist. Selle asemel tagastatakse esitatud inspekteerimisettekandega seotud request id. Inspektsiooni edenemise pärimiseks kasuta käsku `inspect-status`.

#### Käsu kasutus

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid inspekteeritakse (kohustuslik). Kui selle argumendina kasutatakse märksõna all-projects, käsib see ***digna***-l iteratsiooni kõigi olemasolevate projektide üle ja rakendada käsku igale projektile.
- **FROM_DATE**: Inspektsiooni alguskuupäev ja -kellaaeg. Aktsepteeritud vormingud: %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (kohustuslik).
- **TO_DATE**: Inspektsiooni lõppkuupäev ja -kellaaeg, sama vorminguga nagu FROM_DATE (kohustuslik).
  
#### Valikud

- `--table-name`, `-tn`: Piirab inspekteerimise konkreetsele tabelile projekti sees.
- `--table-filter`, `-tf`: Filtrid, et inspekteerida ainult tabeleid, mille nimedes on määratud alamsõne.
- `--enable_notification`, `-en`: Lubab teavituste saatmise häirete korral.

  
#### Näide
  
Andmete inspekteerimiseks projektis `ProjectA` perioodil 1. jaanuar 2024 kuni 31. jaanuar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

käsk `inspect-status` ***digna*** CLI-s kasutatakse asünkroonse inspekteerimise edenemise kontrollimiseks vastavalt request ID-le.

#### Käsu kasutus

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumendid
  
- **REQUEST_ID**: `inspect-async` käsu tagastatud request id
  
#### Näide
  
Inspektsiooni edenemise kontrollimiseks request ID-ga 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

käsk `inspect-cancel` ***digna*** CLI-s kasutatakse inspektsioonide tühistamiseks vastavalt request ID-le või kõigi praegu jooksvate taotluste tühistamiseks.

#### Käsu kasutus

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumendid
  
- **REQUEST_ID**: `inspect-async` käsu tagastatud request id 
  
#### Näide
  
Inspektsiooni tühistamiseks request ID-ga 12345:
  
```bash
dignacli inspect-cancel 12345
```

Kõikide jooksvate või järjekorras olevate taotluste tühistamiseks:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

käsk `export-ds` ***digna*** CLI-s kasutatakse andmeallikate eksportimiseks ***digna*** repositooriumist. Vaikimisi eksporditakse kõik antud projekti andmeallikad.

#### Käsu kasutus
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kust andmeallikad eksporditakse.

#### Valikud

- `--table_name`, `-tn`: Ekspordi kindel andmeallikas projektist.
- `--exportfile`, `-ef`: Määra ekspordi faili nimi.
    
#### Näide
  
Kõigi andmeallikate eksportimiseks projektist `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
See käsk ekspordib `ProjectA` kõik andmeallikad JSON-dokumendina, mida saab importida teise projekti või ***digna*** repositooriumisse.


### import-ds

käsk `import-ds` ***digna*** CLI-s kasutatakse andmeallikate importimiseks sihtprojekti ja loob importaruande.

#### Käsu kasutus
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kuhu andmeallikad imporditakse.
- **EXPORT_FILE**: Ekspordi faili nimi, mida imporditakse.

#### Valikud

- `--output-file`, `-o`: Fail, kuhu salvestada importaruanne (kui ei ole määratud, prinditakse tabelina terminali).
- `--output-format`, `-f`: Vorming, milles importaruanne salvestada (json, csv).
    
#### Näide
  
Kõigi andmeallikate importimiseks ekspordifailist `my_export.json` projekti `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Pärast importi kuvab see käsk ka aruande imporditud ja vahele jäetud objektide kohta. Ainult uued andmeallikad imporditakse `ProjectB`-sse. Selleks, et teada saada, millised objektid imporditaks ja millised jäetaks vahele, võid kasutada käsku `plan-import-ds`.

### plan-import-ds

käsk `plan-import-ds` ***digna*** CLI-s kasutatakse andmeallikate importimise plaani koostamiseks ja importaruande loomiseks enne tegelikku importi.

#### Käsu kasutus
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kuhu andmeallikad imporditaks.
- **EXPORT_FILE**: Ekspordi faili nimi, mida analüüsitakse enne importi.

#### Valikud

- `--output-file`, `-o`: Fail, kuhu salvestada importaruanne (kui ei ole määratud, prinditakse tabelina terminali).
- `--output-format`, `-f`: Vorming, milles importaruanne salvestada (json, csv).
    
#### Näide
  
Et kontrollida, millised andmeallikad imporditakse ja millised jäetaks vahele ekspordifailist `my_export.json` importimisel projekti `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
See käsk kuvab ainult importplaani objektide kohta, mis imporditakse ja mis jäetaks vahele.
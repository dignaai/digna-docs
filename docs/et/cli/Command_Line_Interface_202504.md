---
title: digna CLI Reference 2025.04 – Käsud ja näited | digna Dokumentatsioon
description: Täielik viide digna CLI väljalaske 2025.04 kohta. Õppige, kuidas hallata kasutajaid, reposiitoreid ja andmeid käskudega nagu add-user, check-repo-connection, upgrade-repo, inspect ja teised.
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

See leht dokumenteerib kogu käsustiku, mis on kättesaadav ***digna*** CLI väljalaskes **2025.04**, sealhulgas kasutusnäited ja valikud.

---

## CLI põhitõed

---

## Kasutades `--help` valikut

Valik `--help` kuvab teavet saadaolevate käskude ja nende kasutuse kohta. Selle valiku kasutamiseks on kaks peamist viisi:

1. **Üldise abi kuvamine:**
   
    Kasutage `--help` kohe pärast märksõna ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Abi saamine konkreetse käsu kohta:**  
  
    Konkreetse käsu kohta üksikasjaliku teabe saamiseks lisage sellele käsule `--help`.  
    Näiteks, et saada abi käsuga `add-user`, käivitage:
     ```bash
     dignacli add-user --help
     ```

     ### väljund:
      
     - **Käsu kirjeldus:** Pakub üksikasjaliku selgituse, mida käsk teeb.  
     - **Süntaks:** Näitab täpset süntaksit, sealhulgas kohustuslikke ja valikulisi argumente.  
     - **Valikud:** Loetleb käsule spetsiifilised valikud koos nende selgitustega.  
     - **Näited:** Annavad näiteid, kuidas käsku tõhusalt käivitada.

  
## Kasutades `check-repo-connection` käsku

Käsk `check-repo-connection` on utiliit ***digna*** CLI tööriistas, mis on mõeldud kontrollimaks ühenduvust ja juurdepääsu määratud ***digna*** repositooriumile. See käsk tagab, et CLI saab repositooriumiga suhelda.
      
#### Käsu kasutus
```bash
dignacli check-repo-connection
```

Eduka täitmise korral väljastab käsk ühenduse kinnituse koos repositooriumi detailidega: repositooriumi versioon, host, andmebaas ja skeem.  
  
Kui repositooriumiga ühendamine ei õnnestu, kontrollige config.toml faili, et seadistused oleksid õiged.

## Kasutades `--version` käsku

Paigaldatud *dignacli* versiooni kontrollimiseks kasutage valikut `--version`.  
  
#### Käsu kasutus
```bash
dignacli --version
```
  
#### Näidise väljund
```bash
dignacli version 2025.04
```

## Logimise valikud
  
Vaikimisi on ***digna*** käskude konsooliväljund minimalistlik. Enamik käske võimaldab kuvada täiendavat teavet, kasutades järgmisi valikuid:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
"verbose" ja "debug" määravad detailsuse taseme, samas kui "logfile" lüliti võimaldab suunata väljundi faili, mitte konsooliaknast välja printida.

## Kasutajate haldus

### Kasutades `add-user` käsku
  
Käsk `add-user` ***digna*** CLI-s kasutatakse uue kasutaja lisamiseks ***digna*** süsteemi.
  
#### Käsu kasutus
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumendid

- **USER_NAME**: Uue kasutaja kasutajanimi (nõutav).
- **USER_FULL_NAME**: Uue kasutaja täielik nimi (nõutav).
- **USER_PASSWORD**: Uue kasutaja parool (nõutav).

#### Valikud

- `--is_superuser`, `-su`: Lipuke, mis määrab uue kasutaja administraatoriks.
- `--valid_until`, `-vu`: Seab kasutajakonto aegumiskuupäeva formaadis `YYYY-MM-DD HH:MI:SS`. Kui seda ei määrata, ei aegu konto.

#### Näide

Uue kasutaja lisamiseks kasutajanimega `jdoe`, täieliku nimega `John Doe` ja parooliga `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Uue kasutaja lisamine ja konto aegumiskuupäeva määramine:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Kasutades `delete-user` käsku
  
Käsk `delete-user` ***digna*** CLI-s kasutatakse olemasoleva kasutaja eemaldamiseks ***digna*** süsteemist.
  
#### Käsu kasutus
```bash
dignacli delete-user USER_NAME
```
  
##### Argumendid
- **USER_NAME**: Kustutatava kasutaja kasutajanimi (nõutav). See on käsu ainus nõutav argument.

#### Näide
```bash
dignacli delete-user jdoe
```
  
Selle käsu täitmine eemaldab kasutaja `jdoe` ***digna*** süsteemist, kehtetuks tunnistades tema juurdepääsu ning kustutades seotud andmed ja õigused repositooriumist.

### Kasutades `modify-user` käsku

Käsk `modify-user` ***digna*** CLI-s kasutatakse olemasoleva kasutaja andmete uuendamiseks ***digna*** süsteemis.

#### Käsu kasutus
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumendid
  
- **USER_NAME**: Muudetava kasutaja kasutajanimi (nõutav).
- **USER_FULL_NAME**: Kasutaja uus täielik nimi (nõutav).
  
#### Valikud  
  
- `--is_superuser`, `-su`: Määrab kasutaja superkasutajaks, andes kõrgendatud õigused. See lipp ei vaja väärtust.  
- `--valid_until`, `-vu`: Seab kasutajakonto aegumiskuupäeva formaadis YYYY-MM-DD HH:MI:SS. Kui seda ei anta, jääb konto kehtima piiramatu ajani.  
  
#### Näide
  
Kasutaja `jdoe` täieliku nime muutmiseks `Johnathan Doe` ning kasutaja määramiseks superkasutajaks:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Kasutades `modify-user-pwd` käsku
  
Käsk `modify-user-pwd` ***digna*** CLI-s kasutatakse olemasoleva kasutaja parooli muutmiseks ***digna*** süsteemis.
  
#### Käsu kasutus
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumendid
  
- **USER_NAME**: Kasutajanimi, kelle parooli soovitakse muuta (nõutav).
- **USER_PWD**: Uus parool kasutaja jaoks (nõutav).
  
#### Näide
  
Parooli muutmiseks kasutajale `jdoe` uueks `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Kasutades `list-users` käsku

Käsk `list-users` ***digna*** CLI-s kuvab nimekirja kõigist ***digna*** süsteemi registreeritud kasutajatest.

#### Käsu kasutus

```bash
dignacli list-users
```

Selle käsu käivitamine ***digna*** CLI-s ühendub ***digna*** repositooriumiga ja loetleb kõik kasutajad, kuvades nende ID, kasutajanime, täisnimi, superkasutaja staatuse ja aegumisaegade ajatempleid.

## Repositooriumi haldus

### Kasutades `upgrade-repo` käsku
  
Käsk `upgrade-repo` ***digna*** CLI-s kasutatakse ***digna*** repositooriumi uuendamiseks või initsialiseerimiseks. See käsk on oluline uuenduste rakendamiseks või repositooriumi infrastruktuuri esmakordseks seadistamiseks.
  
#### Käsu kasutus

```bash
dignacli upgrade-repo [options]
```
  
#### Valikud
  
- `--simulation-mode`, `-s`: Kui lubatud, töötab käsk simulatsioonirežiimis, mis prindib SQL-lauseid, mis oleksid täidetud, kuid ei käivita neid tegelikult. See on kasulik muudatuste eelvaatamiseks ilma repositooriumi muutmiseta.  

  
#### Näide
  
***digna*** repositooriumi uuendamiseks võite käivitada käsu ilma valikuteta:
  
```bash
dignacli upgrade-repo
```  
Simulatsioonirežiimis uuenduse käivitamiseks (et näha SQL-lauseid ilma neid rakendamata):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
See käsk on kriitilise tähtsusega ***digna*** süsteemi hooldamisel, tagades, et andmebaasi skeem ja muud repositooriumi komponendid oleksid ajakohased tarkvara uusima versiooniga.

### Kasutades `encrypt` käsku
  
Käsk `encrypt` ***digna*** CLI-s kasutatakse parooli krüpteerimiseks.
  
#### Käsu kasutus
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumendid
- **PASSWORD**: Parool, mida tuleb krüpteerida (nõutav).
  
#### Näide
  
Parooli krüpteerimiseks tuleb parool anda argumendina.  
Näiteks, parooli `mypassword123` krüpteerimiseks kasutage:
```bash
dignacli encrypt mypassword123
```
See käsk väljastab antud parooli krüpteeritud versiooni, mida saab kasutada turvalistes kontekstides. Kui parooli argumenti ei anta, kuvab CLI veateate puuduva argumendi kohta.

## Kasutades `generate-key` käsku
  
Käsku `generate-key` kasutatakse Fernet-võtme genereerimiseks, mis on vajalik ***digna*** repositooriumis salvestatud paroolide turvamiseks.
  
#### Käsu kasutus
```bash
dignacli generate-key
```
  
## Andmete haldus

## Kasutades `clean-up` käsku

Käsk `clean-up` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja Traffic Light System andmete eemaldamiseks ühelt või mitmelt andmeallikalt määratud projektis. See käsk on oluline andmete elutsükli haldamiseks, aidates hoida korraldatud ja tõhusat andmekeskkonda, kustutades aegunud või mittevajalikud andmed.

#### Käsu kasutus

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, kust andmeid eemaldada (nõutav). Kui selle argumendi väärtuseks on märksõna all-projects, käsib see ***digna***-l iteratsiooni kõigi olemasolevate projektide üle ja rakendada käsku.
- **FROM_DATE**: Andmete eemaldamise alguskuupäev ja kellaaeg. Aktsepteeritud formaadid: %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutav).
- **TO_DATE**: Andmete eemaldamise lõppkuupäev ja kellaaeg, sama formaadiga nagu FROM_DATE (nõutav).
  
#### Valikud
  
- `--table-name`, `-tn`: Piirab clean-up operatsiooni konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, et piirata clean-up ainult tabelitega, mille nimedes on antud alamstring.
- `--timing`, `-tm`: Kuvab clean-up protsessi kestuse pärast lõpetamist.
- `--help`: Kuvab clean-up käsu abi ja väljub.
  
#### Näide
  
Andmete eemaldamiseks projektist ProjectA ajavahemikus 1. jaanuar 2023 kuni 30. juuni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Andmete eemaldamiseks ainult konkreetsest tabelist nimega `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
See käsk aitab hallata andmete salvestust ja tagada, et repositoorium sisaldab ainult asjakohast teavet.

## Kasutades `list-projects` käsku
  
Käsk `list-projects` ***digna*** CLI-s kuvab nimekirja kõigist saadaval olevatest projektidest ***digna*** süsteemis.
  
#### Käsu kasutus
  
```bash
dignacli list-projects
```

See käsk on eriti kasulik administraatoritele ja kasutajatele, kes haldavad mitut projekti, pakkudes kiiret ülevaadet saadaval olevatest projektidest ***digna*** repositooriumis.

## Kasutades `list-ds` käsku

Käsk `list-ds` ***digna*** CLI-s kuvab nimekirja kõigist saadaval olevatest andmeallikatest määratud projektis. See käsk on kasulik andmevarade mõistmiseks, mis on analüüsi ja halduse jaoks saadaval ***digna*** süsteemis.

#### Käsu kasutus
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, mille andmeallikad loetletakse (nõutav).
  
#### Näide
  
Kõigi andmeallikate loetlemiseks projektis `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
See käsk annab kasutajatele ülevaate projekti andmeallikatest, aidates neil paremini navigeerida ja hallata andmemaastikku.


## Kasutades `inspect` käsku

Käsk `inspect` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja Traffic Light System andmete loomiseks ühelt või mitmelt andmeallikalt määratud projektis. See käsk aitab andmete analüüsimisel ja jälgimisel määratud perioodi jooksul.

#### Käsu kasutus

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid kontrollitakse (nõutav). Kui selle argumendi väärtuseks on all-projects, käsib see ***digna***-l iteratsiooni kõigi olemasolevate projektide üle ja rakendada käsku.
- **FROM_DATE**: Andmete inspekteerimise alguskuupäev ja kellaaeg. Aktsepteeritud formaadid: %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutav).
- **TO_DATE**: Andmete inspekteerimise lõppkuupäev ja kellaaeg, sama formaadiga nagu FROM_DATE (nõutav).
  
#### Valikud

- `--table-name`, `-tn`: Piirab inspekteerimise konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, et inspekteerida ainult tabeleid, mille nimedes on antud alamstring.
- `--do-profile`: Käivitab profiilide uuesti kogumise. Vaikimisi on do-profile.
- `--no-do-profile`: Takistab profiilide uuesti kogumist.
- `--do-prediction`: Käivitab ennustuste ümberarvutuse. Vaikimisi on do-prediction.
- `--no-do-prediction`: Takistab ennustuste ümberarvutust.
- `--do-alert-status`: Käivitab hoiatusseisundite ümberarvutuse. Vaikimisi on do-alert-status.
- `--no-do-alert-status`: Takistab hoiatusseisundite ümberarvutust.
- `--iterative`: Käivitab perioodi inspekteerimise päevase iteratsiooni kaupa. Vaikimisi on iterative.
- `--no-iterative`: Käivitab kogu perioodi inspekteerimise korraga.
- `--enable_notification`, `-en`: Lubab teavituste saatmise hoiatusjuhtudel.
- `--timing`, `-tm`: Kuvab inspekteerimisprotsessi kestuse pärast lõpetamist.
  
#### Näide
  
Andmete inspekteerimiseks projektis `ProjectA` ajavahemikus 1. jaanuar 2024 kuni 31. jaanuar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Ainult konkreetse tabeli inspekteerimiseks ja ennustuste sunnitud ümberarvutuseks:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
See käsk on kasulik uuendatud profiilide ja ennustuste genereerimiseks, andmete terviklikkuse jälgimiseks ning hoiatussüsteemide haldamiseks määratud projekti ajaraamis.

## Kasutades `tls-status` käsku

Käsk `tls-status` ***digna*** CLI-s kasutatakse Traffic Light System (TLS) staatuse pärimiseks konkreetse tabeli jaoks projektis antud kuupäeval. Traffic Light System annab ülevaate andmete tervisest ja kvaliteedist, märgistades võimalikud probleemid või hoiatused, mis vajavad tähelepanu.
  
#### Käsu kasutus
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille TLS staatust päritakse (nõutav).
- **TABLE_NAME**: Konkreetne tabel projektis, mille TLS-i olekut vaja on (nõutav).
- **DATE**: Kuupäev, mille kohta TLS staatust päritakse, tavaliselt formaat %Y-%m-%d (nõutav).
  
#### Näide
  
TLS staatuse kontrollimiseks tabeli UserData jaoks projektis ProjectA kuupäeval 1. juuli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

See käsk aitab kasutajatel jälgida ja säilitada andmete kvaliteeti, pakkudes selget ja tegutsemisvõimelist olekuraportit vastavalt etteantud kriteeriumitele.

## Kasutades `inspect-async` käsku

Käsk `inspect-async` ***digna*** CLI-s annab tagumise osa süsteemile käsu inspekteerimise asünkroonseks tegemiseks määratud projekti ühe või mitme andmeallika jaoks. Kui project_name on seatud väärtusele all-projects, iteritakse üle kõikide saadaval olevate projektide ja inspekteerimine viiakse läbi igas neist. Käsk tagastab päringu-ID, mida saab kasutada inspekteerimise edenemise jälgimiseks.

#### Käsu kasutus

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid inspekteeritakse (nõutav). Kui kasutatakse märksõna all-projects, iteritakse kõigi olemasolevate projektide üle.
- **FROM_DATE**: Inspekteerimise alguskuupäev ja kellaaeg. Aktsepteeritud formaadid: %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutav).
- **TO_DATE**: Inspekteerimise lõppkuupäev ja kellaaeg, sama formaadiga nagu FROM_DATE (nõutav).
  
#### Valikud

- `--table-name`, `-tn`: Piirab inspekteerimise konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, et inspekteerida ainult tabeleid, mille nimedes on antud alamstring.

  
#### Näide
  
Andmete asünkroonseks inspekteerimiseks projektis `ProjectA` ajavahemikus 1. jaanuar 2024 kuni 31. jaanuar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Kasutades `inspect-status` käsku

Käsk `inspect-status` ***digna*** CLI-s kasutatakse asünkroonse inspekteerimise edenemise kontrollimiseks, kasutades päringu ID-d.

#### Käsu kasutus

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumendid
  
- **REQUEST_ID**: Päringu ID, mille tagastab käsk `inspect-async`. 
  
#### Valikud

- `--report_level`, `-rl`: Määrab raporti taseme: 'task' või 'step' [vaikimisi: task]
  
#### Näide
  
Inspekteerimise edenemise kontrollimiseks päringu ID-ga 12345 detailse step-taseme aruandluse jaoks:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Kasutades `export-ds` käsku

Käsk `export-ds` ***digna*** CLI-s kasutatakse andmeallikate eksportimiseks ***digna*** repositooriumist. Vaikimisi eksporditakse kõik antud projekti andmeallikad.

#### Käsu kasutus
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kust andmeallikad eksporditakse.

#### Valikud

- `--table_name`, `-tn`: Ekspordi konkreetne andmeallikas projektist.
- `--exportfile`, `-ef`: Määrake ekspordi faili nimi.
    
#### Näide
  
Kõigi andmeallikate eksportimiseks projektist `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
See käsk ekspordib kõik `ProjectA` andmeallikad JSON-dokumendina, mida saab importida teise projekti või ***digna*** repositooriumi.

## Kasutades `import-ds` käsku

Käsk `import-ds` ***digna*** CLI-s kasutatakse andmeallikate importimiseks sihtprojekti ja impordi aruande koostamiseks.

#### Käsu kasutus
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kuhu andmeallikad imporditakse.
- **EXPORT_FILE**: Ekspordi failinimi, mida imporditakse.

#### Valikud

- `--output-file`, `-o`: Fail, kuhu salvestada impordi aruanne (kui ei ole määratud, prinditakse terminali tabelina).
- `--output-format`, `-f`: Vorming, milles impordi aruanne salvestada (json, csv).
    
#### Näide
  
Kõigi andmeallikate importimiseks ekspordifailist `my_export.json` projekti `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Pärast importi kuvab see käsk ka aruande imporditud ja vahele jäetud objektide kohta. Ainult uued andmeallikad imporditakse `ProjectB`-sse. Selleks, et teada saada, millised objektid imporditakse ja millised jäetakse vahele, võite kasutada käsku `plan-import-ds`.

## Kasutades `plan-import-ds` käsku

Käsk `plan-import-ds` ***digna*** CLI-s kasutatakse impordi planeerimiseks — analüüsib ekspordifaili ja loob impordi aruande ilma tegeliku impordita.

#### Käsu kasutus
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kuhu andmeallikad oleksid imporditud.
- **EXPORT_FILE**: Ekspordifaili nimi, mida analüüsitakse enne importi.

#### Valikud

- `--output-file`, `-o`: Fail, kuhu salvestada impordi aruanne (kui ei ole määratud, prinditakse terminali tabelina).
- `--output-format`, `-f`: Vorming, milles impordi aruanne salvestada (json, csv).
    
#### Näide
  
Selleks, et kontrollida, millised andmeallikad ekspordifailist `my_export.json` imporditakse ja millised jäetakse vahele importimisel projekti `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
See käsk kuvab ainult impordiplaani objektide kohta, mis imporditakse ja millised jäetakse vahele.
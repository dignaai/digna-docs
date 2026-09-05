# digna CLI viide 2026.01
**2026-01-15**

See leht dokumenteerib kõiki käske, mis on saadaval ***digna*** CLI väljalaskes **2026.01**, sh kasutusnäited ja valikud.

---

## CLI põhitõed

---

### help
Valik `--help` annab teavet saadaolevate käskude ja nende kasutuse kohta. Selle valiku kasutamiseks on kaks peamist viisi:

1. **Üldise abi kuvamine:**
   
    Kasuta --help kohe pärast märksõna ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Abi konkreetse käsu kohta:**  
  
    Konkreetse käsu üksikasjalikumaks informatsiooniks lisa sellele käskudele `--help`.
    Näiteks, et saada abi käsuga `add-user`, käivita:
     ```bash
     dignacli add-user --help
     ```

     ### väljund:
      
     - **Käsu kirjeldus:** Annab üksikasjaliku kirjelduse, mida käsk teeb.  
     - **Süntaks:** Näitab täpset süntaksit, sh nõutud ja valikulised argumendid.  
     - **Valikud:** Loetleb käsule spetsiifilised valikud koos selgitustega.  
     - **Näited:** Pakub näiteid käsu tõhusaks kasutamiseks.

### check-config

Käsk check-config on tööriist ***digna*** CLI tööriistas, mis on mõeldud kontrollimaks ***digna*** konfiguratsiooni. See käsk tagab, et ***digna*** komponendid leiaksid config.toml failist vajalikud konfiguratsioonielemendid.

#### Valikud

- `--configpath`, `-cp`: Fail või kataloog, mis sisaldab konfiguratsiooni. Kui seda ei ole määratud, kasutatakse ../config.toml.

#### Käsu kasutus
```bash
dignacli check-config
```

Edukalt täidetuna väljastab käsk kinnituse konfiguratsiooni täielikkuse kohta.  
  
Kui konfiguratsioon tundub olevat mittetäielik, loetletakse puuduvad konfiguratsioonielemendid.

  
### check-repo-connection

Käsk check-repo-connection on tööriist ***digna*** CLI tööriistas, mis kontrollib ühenduvust ja ligipääsu määratud ***digna*** hoidla (repository) suhtes. See käsk tagab, et CLI saab hoidla kaudu suhelda.
      
#### Käsu kasutus
```bash
dignacli check-repo-connection
```

Edukalt täidetuna väljastab käsk kinnituse ühenduse kohta koos hoidla üksikasjadega: hoidla versioon, host, andmebaas ja skeem.  
  
Kui hoidlaühendus ei õnnestu, kontrolli config.toml faili, kas konfiguratsiooni sätted on õiged.


### version

Paigaldatud *dignacli* versiooni kontrollimiseks kasuta valikut --version.  
  
#### Käsu kasutus
```bash
dignacli --version
```
  
#### Näidiväljund
```bash
dignacli version 2026.01
```

### logimise valikud
  
Vaikimisi on ***digna*** käskude konsooli väljund minimalistlik. Enamik käske võimaldab lisainfot väljastada järgmiste valikute abil:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” ja „debug” määravad detailide taset, samas kui „logfile” lüliti võimaldab suunata väljundi faili, mitte konsooli aknasse.

## Kasutajate haldus

### add-user
  
Käsk add-user ***digna*** CLI-s kasutatakse uue kasutaja lisamiseks ***digna*** süsteemi.
  
#### Käsu kasutus
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumendid

- **USER_NAME**: Uue kasutaja kasutajanimi (nõutud).
- **USER_FULL_NAME**: Uue kasutaja täielik nimi (nõutud).
- **USER_PASSWORD**: Uue kasutaja parool (nõutud).

#### Valikud

- `--is_superuser`, `-su`: Lipuke, et määrata uus kasutaja administraatoriks.
- `--valid_until`, `-vu`: Määrab kasutajakonto aegumiskuupäeva formaadis `YYYY-MM-DD HH:MI:SS`. Kui seda ei määra, ei ole kontol aegumistähtaega.

#### Näide

Uue kasutaja lisamiseks kasutajanimega `jdoe`, täieliku nimega `John Doe` ja parooliga `password123`:

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
- **USER_NAME**: Selle kasutaja kasutajanimi, kes eemaldatakse (nõutud). See on käsu ainus nõutud argument.

#### Näide
```bash
dignacli delete-user jdoe
```
  
Selle käsu täitmine eemaldab kasutaja `jdoe` ***digna*** süsteemist, ärike nende juurdepääs ja kustutatakse nendega seotud andmed ja õigused hoidlast.

### modify-user

Käsk `modify-user` ***digna*** CLI-s kasutatakse olemasoleva kasutaja andmete värskendamiseks ***digna*** süsteemis.

#### Käsu kasutus
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumendid
  
- **USER_NAME**: Muudetava kasutaja kasutajanimi (nõutud).
- **USER_FULL_NAME**: Kasutaja uus täielik nimi (nõutud).
  
#### Valikud  
  
- `--is_superuser`, `-su`: Määrab kasutaja superkasutajaks, andes kõrgendatud õigused. See lipuke ei vaja väärtust.  
- `--valid_until`, `-vu`: Määrab kasutajakonto aegumiskuupäeva formaadis YYYY-MM-DD HH:MI:SS. Kui seda ei anta, jääb konto piiramatult kehtivaks.  
  
#### Näide
  
Kasutaja `jdoe` täieliku nime muutmiseks „Johnathan Doe” ja kasutaja määramiseks superkasutajaks:
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
  
Kasutaja `jdoe` parooli muutmiseks `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Käsk `list-users` ***digna*** CLI-s kuvab nimekirja kõigist registreeritud kasutajatest ***digna*** süsteemis.

#### Käsu kasutus

```bash
dignacli list-users
```

Selle käsu täitmine ühendub ***digna*** hoidla ja loetleb kõik kasutajad, näidates nende ID, kasutajanime, täieliku nime, superkasutaja staatuse ja aegumistähtajad.

## Hoidla haldus

### upgrade-repo
  
Käsk `upgrade-repo` ***digna*** CLI-s kasutatakse ***digna*** hoidla uuendamiseks või initsialiseerimiseks. See käsk on oluline värskenduste rakendamiseks või hoidla infrastruktuuri esmakordseks seadistamiseks.
  
#### Käsu kasutus

```bash
dignacli upgrade-repo [options]
```
  
#### Valikud
  
- `--simulation-mode`, `-s`: Kui lubatud, käivitab käsu simulatsioonirežiimis, mis prindib SQL-laused, mis oleksid täidetud, kuid ei käivita neid tegelikult. See on kasulik muudatuste eelvaatamiseks ilma hoidlat muutmata.  

  
#### Näide
  
***digna*** hoidla uuendamiseks võid käivitada käsu ilma valikuteta:
  
```bash
dignacli upgrade-repo
```  
Uuenduse käivitamiseks simulatsioonirežiimis (et näha SQL-lauset, ilma neid rakendamata):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
See käsk on oluline ***digna*** süsteemi hooldamiseks, tagades, et andmebaasi skeem ja muud hoidla komponendid on kooskõlas tarkvara viimase versiooniga.

### encrypt
  
Käsk `encrypt` ***digna*** CLI-s kasutatakse parooli krüpteerimiseks.
  
#### Käsu kasutus
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumendid
- **PASSWORD**: Parool, mida tuleb krüpteerida (nõutud).
  
#### Näide
  
Parooli krüpteerimiseks tuleb parool anda argumendina.   
Näiteks parooli `mypassword123` krüpteerimiseks kasutage:
```bash
dignacli encrypt mypassword123
```
See käsk väljastab antud parooli krüpteeritud versiooni, mida saab kasutada turvalistes kontekstides. Kui parooli argumenti ei anta, kuvab CLI puuduva argumendi vea.

### generate-key
  
Käsku `generate-key` kasutatakse Fernet-võtme genereerimiseks, mis on vajalik paroolide turvaliseks salvestamiseks ***digna*** hoidlas.
  
#### Käsu kasutus
```bash
dignacli generate-key
```
  
## Andmete haldus

### clean-up

Käsk `clean-up` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja fooride (traffic light system) andmete eemaldamiseks ühelt või mitmelt andmeallikalt määratud projekti piires. See käsk on oluline andmete elutsükli haldamiseks, aidates hoida korrastatud ja tõhusat andmekeskkonda, kustutades aegunud või tarbetud andmed.

#### Käsu kasutus

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, kust andmed eemaldatakse (nõutud). Kui selle argumendina kasutatakse märksõna all-projects, siis **digna** iteriseerib üle kõigi olemasolevate projektide ja rakendab käsku.
- **FROM_DATE**: Andmete eemaldamise alguskuupäev ja aeg. Aktsepteeritavad vormingud on %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutud).
- **TO_DATE**: Andmete eemaldamise lõpukuupäev ja aeg, sama formaadiga nagu FROM_DATE (nõutud).
  
#### Valikud
  
- `--table-name`, `-tn`: Piirab clean-up toimingu konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, piirates clean-upi ainult tabelitele, mille nimedes esineb antud alamstring.
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
  
See käsk aitab hallata andmete salvestust ja tagab, et hoidlas hoitakse ainult asjakohast informatsiooni.

### remove-orphans
  
Käsk `remove-orphans` ***digna*** CLI-s kasutatakse hoidla koristustööde jaoks.  
Kui kasutaja kustutab projekte või andmeallikaid, jäävad profiilid ja ennustused sageli hoidlasse orbudena. Selle käsuga eemaldatakse sellised orvud ridu hoidlast.
  
#### Käsu kasutus
  
```bash
dignacli list-projects
```

### list-projects
  
Käsk `list-projects` ***digna*** CLI-s kasutatakse kõigi saadaval olevate projektide nimekirja kuvamiseks ***digna*** süsteemis.
  
#### Käsu kasutus
  
```bash
dignacli list-projects
```

See käsk on eriti kasulik administraatoritele ja kasutajatele, kes haldavad mitut projekti, pakkudes kiiret ülevaadet saadavalolevatest projektidest ***digna*** hoidlas.

### list-ds

Käsk `list-ds` ***digna*** CLI-s kuvab nimekirja kõigist saadaval olevatest andmeallikatest (data sources) määratud projektis. See käsk on kasulik andmevarade tugevdamiseks ja haldamiseks ***digna*** süsteemis.

#### Käsu kasutus
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, mille andmeallikaid loetletakse (nõutud).
  
#### Näide
  
Kõigi andmeallikate loetlemiseks projektis nimega `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
See käsk annab kasutajatele ülevaate projekti andmeallikatest, aidates neil andmete maastikku paremini navigeerida ja hallata.


### inspect

Käsk `inspect` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja fooride (traffic light system) andmete loomiseks ühelt või mitmelt andmeallikalt määratud projektis. See käsk aitab andmeid analüüsida ja jälgida määratud ajavahemikus. Inspecti lõpuks tagastatakse arvutatud foorisüsteemi väärtus:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Käsu kasutus

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid inspekteeritakse (nõutud). Kui selle argumendina kasutatakse märksõna all-projects, siis **digna** iteriseerib üle kõigi olemasolevate projektide ja rakendab käsku.
- **FROM_DATE**: Inspektsiooni alguskuupäev ja aeg. Aktsepteeritavad vormingud on %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutud).
- **TO_DATE**: Inspektsiooni lõpukuupäev ja aeg, sama formaadiga nagu FROM_DATE (nõutud).
  
#### Valikud

- `--table-name`, `-tn`: Piirab inspekteerimise konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib inspekteerimise ainult tabelitele, mille nimedes esineb antud alamstring.
- `--enable_notification`, `-en`: Lubab teavituste saatmise alertide korral.
- `--bypass-backend`, `-bb`: Väldi backendit ja käivita inspekteerimine otse CLI-st (ainult testimiseks!).

  
#### Näide
  
Andmete inspekteerimiseks projektis `ProjectA` ajavahemikus 1. jaanuar 2024 kuni 31. jaanuar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Ainult konkreetse tabeli inspekteerimiseks ja ennustuste uuesti arvutamise sundimiseks:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
See käsk on kasulik uuendatud profiilide ja ennustuste genereerimiseks, andmete terviklikkuse jälgimiseks ja alert-süsteemide haldamiseks määratud projekti ajavahemikus.

### inspect-async

Käsk `inspect-async` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja fooride andmete loomiseks ühelt või mitmelt andmeallikalt määratud projektis. See käsk aitab andmeid analüüsida ja jälgida määratud ajavahemikus. Erinevalt käsust `inspect`, see ei oota inspekteerimise lõppemist.
Selle asemel tagastab see esitatud inspekteerimispäringu request id. Inspektsiooni edenemise pärimiseks kasuta käsku `inspect-status`.

#### Käsu kasutus

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid inspekteeritakse (nõutud). Kui selle argumendina kasutatakse märksõna all-projects, siis **digna** iteriseerib üle kõigi olemasolevate projektide ja rakendab käsku.
- **FROM_DATE**: Inspektsiooni alguskuupäev ja aeg. Aktsepteeritavad vormingud on %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutud).
- **TO_DATE**: Inspektsiooni lõpukuupäev ja aeg, sama formaadiga nagu FROM_DATE (nõutud).
  
#### Valikud

- `--table-name`, `-tn`: Piirab inspekteerimise konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib inspekteerimise ainult tabelitele, mille nimedes esineb antud alamstring.
- `--enable_notification`, `-en`: Lubab teavituste saatmise alertide korral.

  
#### Näide
  
Andmete inspekteerimiseks projektis `ProjectA` ajavahemikus 1. jaanuar 2024 kuni 31. jaanuar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Käsk `inspect-status` ***digna*** CLI-s kasutatakse asünkroonse inspekteerimise edenemise kontrollimiseks request ID alusel.

#### Käsu kasutus

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumendid
  
- **REQUEST_ID**: `inspect-async` käsu poolt tagastatud request id
  
#### Näide
  
Inspektsiooni edenemise kontrollimiseks request ID-ga 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Käsk `inspect-cancel` ***digna*** CLI-s kasutatakse inspekteerimiste tühistamiseks request ID alusel või kõigi praegu käimas/pending päringute tühistamiseks.

#### Käsu kasutus

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumendid
  
- **REQUEST_ID**: `inspect-async` käsu poolt tagastatud request id 
  
#### Näide
  
Inspektsiooni tühistamiseks request ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Kõigi praegu käimas või ootel olevate päringute tühistamiseks:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Käsk `export-ds` ***digna*** CLI-s kasutatakse andmeallikate eksportimiseks ***digna*** hoidlast. Vaikimisi eksporditakse kõik andmeallikad antud projektist.

#### Käsu kasutus
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kust andmeallikad eksporditakse.

#### Valikud

- `--table_name`, `-tn`: Ekspordi konkreetne andmeallikas projektist.
- `--exportfile`, `-ef`: Määra ekspordi faili nimi.
    
#### Näide
  
Kõikide andmeallikate eksportimiseks projektist nimega `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
See käsk ekspordib `ProjectA` kõik andmeallikad JSON-dokumendina, mida saab importida teise projekti või ***digna*** hoidlasse.


### import-ds

Käsk `import-ds` ***digna*** CLI-s kasutatakse andmeallikate importimiseks sihtprojekti ja importaruande loomiseks.

#### Käsu kasutus
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kuhu andmeallikad imporditakse.
- **EXPORT_FILE**: Ekspordifaili nimi, mida imporditakse.

#### Valikud

- `--output-file`, `-o`: Fail, kuhu salvestada importaruanne (kui ei ole määratud, prinditakse terminali tabeliliselt).
- `--output-format`, `-f`: Vorming, milles salvestada importaruanne (json, csv).
    
#### Näide
  
Kõikide andmeallikate importimiseks ekspordifailist `my_export.json` projekti `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Pärast importi kuvab käsk ka aruande imporditud ja vahele jäetud objektide kohta. Ainult uued andmeallikad imporditakse projekti `ProjectB`. Selleks, et teada saada, milliseid objekte imporditakse ja milliseid jäetakse vahele, võid kasutada käsku `plan-import-ds`

### plan-import-ds

Käsk `plan-import-ds` ***digna*** CLI-s kasutatakse andmeallikate impordi planeerimiseks ja importaruande koostamiseks enne tegelikku importi.

#### Käsu kasutus
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumendid
- **PROJECT_NAME**: Projekti nimi, kuhu andmeallikad imporditaksid.
- **EXPORT_FILE**: Ekspordifaili nimi, mida analüüsitakse enne importi.

#### Valikud

- `--output-file`, `-o`: Fail, kuhu salvestada importaruanne (kui ei ole määratud, prinditakse terminali tabeliliselt).
- `--output-format`, `-f`: Vorming, milles salvestada importaruanne (json, csv).
    
#### Näide
  
Kontrollimaks, millised andmeallikad imporditakse ja millised jäetakse vahele ekspordifailist `my_export.json`, kui imporditakse projekti `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
See käsk kuvab ainult impordiplaani objektidest, mis imporditakse või jäetakse vahele.
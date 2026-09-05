# digna CLI viide 2024.12
**2024-12-09**

See leht dokumenteerib kõiki käske, mis on saadaval ***digna*** CLI väljalaskes **2024.12**, sealhulgas kasutusnäiteid ja valikuid.

---


**2024-12-09**


---

## CLI põhialused

---

## `--help` valiku kasutamine

Valik `--help` annab informatsiooni saadaval olevate käskude ja nende kasutuse kohta. Selle valiku kasutamiseks on kaks peamist viisi:

1. **Üldise abi kuvamine:**
   
   Kasuta `--help` kohe pärast käsku ***digna*** CLI:
   ```bash
   dignacli --help
   ```

2. **Spetsiifilise käsu abi:**
  
   Kui vajad üksikasjalikku infot konkreetse käsu kohta, lisa sellele käsule `--help`.
   Näiteks, et saada abi käsu `add-user` kohta, käivita:
   ```bash
   dignacli add-user --help
   ```

   ### väljund:
      
   - **Käsu kirjeldus:** Annab üksikasjaliku selgituse, mida käsk teeb.  
   - **Süntaks:** Näitab täpset süntaksit, kaasa arvatud kohustuslikud ja valikulised argumendid.  
   - **Valikud:** Loetleb käsule spetsiifilised valikud koos nende selgitustega.  
   - **Näited:** Näitab näiteid, kuidas käsku tõhusalt kasutada.  


## `check-repo-connection` käsu kasutamine

Käsk `check-repo-connection` on tööriist ***digna*** CLI-s, mis on mõeldud antud ***digna*** repositooriumi ühenduvuse ja ligipääsu testimiseks. See käsk kontrollib, kas CLI suudab repositooriumiga suhelda.
      
### Käsu kasutus
```bash
dignacli check-repo-connection
```

Kui käsk õnnestub, väljastatakse kinnitus ühenduse kohta koos andmetega repositooriumi kohta: repositooriumi versioon, host, andmebaas ja skeem.  
  
Kui repositooriumiga ühendus ei õnnestu, kontrolli config.toml faili, et seaded oleksid õiged.

## `--version` käsu kasutamine

Paigaldatud *dignacli* versiooni kontrollimiseks kasuta valikut `--version`.  
  
### Käsu kasutus
```bash
dignacli --version
```
  
### Näide väljundist
```bash
dignacli version 2024.12
```

## Logimise valikute kasutamine
  
Vaikimisi on ***digna*** käskude konsooli väljund minimalistlik. Enamik käskudest võimaldab täiendava info kuvamist järgmiste valikute abil:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” ja „debug” määravad detailide taseme, samas kui „logfile” lüliti võimaldab suunata väljundi faili, mitte konsooli.

# Kasutajate haldus

## `add-user` käsu kasutamine
  
Käsk `add-user` ***digna*** CLI-s kasutatakse uue kasutaja lisamiseks ***digna*** süsteemi.
  
### Käsu kasutus
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumendid

- **USER_NAME**: Uue kasutaja kasutajanimi (nõutav).
- **USER_FULL_NAME**: Uue kasutaja täisnimi (nõutav).
- **USER_PASSWORD**: Uue kasutaja parool (nõutav).

### Valikud

- `--is_superuser`, `-su`: Lipuke, mis määrab uue kasutaja administraatoriks.
- `--valid_until`, `-vu`: Määrab kasutajakonto kehtivusaja lõpu vormingus `YYYY-MM-DD HH:MI:SS`. Kui seda ei määrata, puudub kontol aegumine.

### Näide

Uue kasutaja lisamiseks kasutajanimega `jdoe`, täisnimega `John Doe` ja parooliga `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Uue kasutaja lisamiseks ja konto aegumise määramiseks:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` käsu kasutamine
  
Käsk `delete-user` ***digna*** CLI-s kasutatakse olemasoleva kasutaja eemaldamiseks ***digna*** süsteemist.
  
### Käsu kasutus
```bash
dignacli delete-user USER_NAME
```
  
### Argumendid
- **USER_NAME**: Kustutatava kasutaja kasutajanimi (nõutav). See on käsk, mis nõuab ainsana seda argumenti.

### Näide
```bash
dignacli delete-user jdoe
```
  
Selle käsu täitmisel eemaldatakse kasutaja `jdoe` ***digna*** süsteemist, tühistatakse tema ligipääs ning kustutatakse seotud andmed ja õigused repositooriumist.

## `modify-user` käsu kasutamine

Käsk `modify-user` ***digna*** CLI-s kasutatakse olemasoleva kasutaja andmete uuendamiseks ***digna*** süsteemis.

### Käsu kasutus
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumendid
  
- **USER_NAME**: Muudetava kasutaja kasutajanimi (nõutav).
- **USER_FULL_NAME**: Uus täisnimi kasutajale (nõutav).
  
### Valikud  
  
- `--is_superuser`, `-su`: Seab kasutaja superkasutajaks, andes täiendavaid privileege. See lipuke ei vaja väärtust.  
- `--valid_until`, `-vu`: Määrab kasutajakonto aegumise kuupäeva vormingus YYYY-MM-DD HH:MI:SS. Kui seda ei anta, jääb konto kehtima määramata ajani.  
  
### Näide
  
Kasutaja `jdoe` täisnime muutmiseks „Johnathan Doe” ja kasutaja superkasutajaks määramiseks:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` käsu kasutamine
  
Käsk `modify-user-pwd` ***digna*** CLI-s kasutatakse olemasoleva kasutaja parooli muutmiseks.
  
### Käsu kasutus
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumendid
  
- **USER_NAME**: Parooli muudetava kasutaja kasutajanimi (nõutav).
- **USER_PWD**: Uus parool kasutajale (nõutav).
  
### Näide
  
Kasutaja `jdoe` parooli muutmiseks `newpassword123`-ks:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` käsu kasutamine

Käsk `list-users` ***digna*** CLI-s kuvab nimekirja kõigist süsteemi registreeritud kasutajatest.

### Käsu kasutus

```bash
dignacli list-users
```

Selle käsu käivitamisel ühendub ***digna*** CLI ***digna*** repositooriumiga ja kuvab kõik kasutajad, näidates nende ID-d, kasutajanime, täisnime, superkasutaja staatust ja aegumise timestampe.

# Repositooriumi haldus

### `upgrade-repo` käsu kasutamine
  
Käsk `upgrade-repo` ***digna*** CLI-s kasutatakse ***digna*** repositooriumi uuendamiseks või initsialiseerimiseks. See käsk on oluline tarkvara uuenduste rakendamiseks või repositooriumi infrastruktuuri esmakordseks seadistamiseks.
  
### Käsu kasutus

```bash
dignacli upgrade-repo [options]
```
  
### Valikud
  
- `--simulation-mode`, `-s`: Kui lubatud, siis käivitatakse käsk simulatsioonirežiimis, mis prindib SQL-lauseid, mida täidetakse, kuid ei käivita neid tegelikult. See on kasulik muudatuste eelvaatamiseks ilma repositooriumi muutmiseta.  

  
### Näide
  
***digna*** repositooriumi uuendamiseks käivita käsk ilma valikuteta:
  
```bash
dignacli upgrade-repo
```  
Uuenduse käivitamiseks simulatsioonirežiimis (näha SQL-lauseid ilma neid rakendamast):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
See käsk on oluline ***digna*** süsteemi hooldamiseks, tagades andmebaasi skeemi ja teiste repositooriumi komponentide ajakohasuse tarkvara viimase versiooniga.

## `encrypt` käsu kasutamine
  
Käsk `encrypt` ***digna*** CLI-s kasutatakse parooli krüpteerimiseks.
  
### Käsu kasutus
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumendid
- **PASSWORD**: Parool, mida on vaja krüpteerida (nõutav).
  
### Näide
  
Parooli krüpteerimiseks anna parool argumendina.  
Näiteks, parooli `mypassword123` krüpteerimiseks kasuta:
```bash
dignacli encrypt mypassword123
```
See käsk väljastab antud parooli krüpteeritud versiooni, mida saab seejärel kasutada turvalistes kontekstides. Kui parooli argumendi ei anta, kuvab CLI veateate puuduva argumendi kohta.

## `generate-key` käsu kasutamine
  
Käsk `generate-key` genereerib Fernet võtme, mis on oluline paroolide turvamiseks, mis on salvestatud ***digna*** repositooriumis.
  
### Käsu kasutus
```bash
dignacli generate-key
```
  
# Andmete haldus

## `clean-up` käsu kasutamine

Käsk `clean-up` ***digna*** CLI-s eemaldab profiile, ennustusi ja Traffic Light System andmeid ühelt või mitmelt andmeallikalt määratud projekti piires. See käsk on oluline andmete elutsükli haldamiseks, aidates hoida korrastatud ja tõhusat andmekeskkonda, kustutades aegunud või mittevajalikke andmeid.

### Käsu kasutus

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, kust andmeid eemaldatakse (nõutav). Kui selles argumendis kasutada märksõna `all-projects`, siis käsu puhul iteratsioon toimub üle kõigi olemasolevate projektide.
- **FROM_DATE**: Andmete eemaldamise alguskuupäev ja -kellaaeg. Aktsepteeritud vormingud on %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutav).
- **TO_DATE**: Andmete eemaldamise lõppkuupäev ja -kellaaeg, samas vormingus nagu FROM_DATE (nõutav).
  
### Valikud
  
- `--table-name`, `-tn`: Piirab clean-up operatsiooni konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, limiteerides clean-up ainult tabelitele, mille nimedes on etteantud alamsõne.
- `--timing`, `-tm`: Kuvab clean-up protsessi kestuse pärast lõpetamist.
- `--help`: Kuvab clean-up käsu abi ja väljub.
  
### Näide
  
Andmete eemaldamiseks projektist ProjectA ajavahemikus 1. jaanuar 2023 kuni 30. juuni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Andmete eemaldamiseks ainult konkreetsest tabelist nimega `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
See käsk aitab hallata andmete salvestust ja tagada, et repositoorium sisaldab ainult asjakohast informatsiooni.

## `inspect` käsu kasutamine

Käsk `inspect` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja Traffic Light System andmete genereerimiseks ühelt või mitmelt andmeallikalt määratud projekti piires. See käsk aitab andmete analüüsimisel ja jälgimisel määratud perioodi jooksul.

### Käsu kasutus

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid inspekteeritakse (nõutav). Kui selles argumendis kasutada märksõna `all-projects`, siis käsk iteratsioonib üle kõigi olemasolevate projektide.
- **FROM_DATE**: Inspektsiooni alguskuupäev ja -kellaaeg. Aktsepteeritud vormingud on %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutav).
- **TO_DATE**: Inspektsiooni lõppkuupäev ja -kellaaeg, sama vorming kui FROM_DATE (nõutav).
  
### Valikud

- `--table-name`, `-tn`: Piirab inspektsiooni konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, et inspekteerida ainult tabeleid, mille nimedes on etteantud alamsõne.
- `--do-profile`: Käivitab profiilide kogumise. Vaikeväärtus on do-profile.
- `--no-do-profile`: Takistab profiilide kogumist.
- `--do-prediction`: Käivitab ennustuste ümberarvutuse. Vaikeväärtus on do-prediction.
- `--no-do-prediction`: Takistab ennustuste ümberarvutust.
- `--do-alert-status`: Käivitab häireseisundite ümberarvutuse. Vaikeväärtus on do-alert-status.
- `--no-do-alert-status`: Takistab häireseisundite ümberarvutust.
- `--iterative`: Käivitab perioodi inspektsiooni päevaste iteratsioonidena. Vaikeväärtus on iterative.
- `--no-iterative`: Käivitab kogu perioodi inspektsiooni korraga.
- `--timing`, `-tm`: Kuvab inspektsiooni protsessi kestuse pärast lõpetamist.
  
### Näide
  
Andmete inspekteerimiseks projektis `ProjectA` vahemikus 1. jaanuar 2024 kuni 31. jaanuar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Ainult konkreetse tabeli inspekteerimiseks ja ennustuste sunniviisiliseks ümberarvutamiseks:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
See käsk on kasulik uuendatud profiilide ja ennustuste genereerimiseks, andmete terviklikkuse jälgimiseks ning häiresüsteemide haldamiseks määratud projekti ajavahemikul.

## `tls-status` käsu kasutamine

Käsk `tls-status` ***digna*** CLI-s kasutatakse Traffic Light System (TLS) staatuse pärimiseks konkreetse tabeli kohta projektis antud kuupäeval. Traffic Light System annab ülevaate andmete tervisest ja kvaliteedist, tuues esile võimalikud probleemid või hoiatused, mis võivad vajada tähelepanu.
  
### Käsu kasutus
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille TLS staatust päritakse (nõutav).
- **TABLE_NAME**: Konkreetselt tabel, mille TLS staatust vajatakse (nõutav).
- **DATE**: Kuupäev, mille kohta TLS staatust päritakse, tavaliselt vormingus %Y-%m-%d (nõutav).
  
### Näide
  
TLS staatuse kontrollimiseks tabeli nimega UserData kohta projektis ProjectA kuupäeval 1. juuli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

See käsk aitab kasutajatel andmete kvaliteeti jälgida ja säilitada, pakkudes selget ning rakendatavat staatusaruannet vastavalt eelmääratletud kriteeriumitele.

## `list-projects` käsu kasutamine
  
Käsk `list-projects` ***digna*** CLI-s kuvab nimekirja kõigist saadaval olevatest projektidest ***digna*** süsteemis.
  
### Käsu kasutus
  
```bash
dignacli list-projects
```

See käsk on eriti kasulik administraatoritele ja kasutajatele, kes haldavad mitut projekti, pakkudes kiiret ülevaadet olemasolevatest projektidest ***digna*** repositooriumis.

## `list-ds` käsu kasutamine

Käsk `list-ds` ***digna*** CLI-s kuvab nimekirja kõigist saadaval olevatest andmeallikatest määratud projektis. See käsk on kasulik andmevarade mõistmiseks, mis on saadaval analüüsiks ja halduseks ***digna*** süsteemis.

### Käsu kasutus
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumendid
- **PROJECT_NAME**: Projekti nimi, mille andmeallikaid loetletakse (nõutav).
  
### Näide
  
Kõigi andmeallikate loetlemiseks projektis nimega `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
See käsk annab kasutajatele ülevaate projekti andmeallikatest, aidates neil andmemaastikku paremini navigeerida ja hallata.
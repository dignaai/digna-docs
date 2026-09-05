---
title: digna CLI Reference 2024.11 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.11. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

See leht dokumenteerib kõiki käske, mis on saadaval ***digna*** CLI väljaandes **2024.11**, kaasa arvatud kasutusnäited ja valikud.


---
## CLI põhitõed

---

## `help` valiku kasutamine

Valik `--help` annab teavet saadaolevate käskude ja nende kasutuse kohta. Selle valiku kasutamiseks on kaks peamist viisi:

1. **Üldise abi kuvamine:**
   
    Kasutage `--help` kohe pärast märksõna ***digna***cl  
   ```bash
   dignacli --help
   ```

3.  **Spetsiifilise käsu abi saamine:**  
  
    Konkreetse käsu kohta täpsema info saamiseks lisage sellele käsule `--help`.
    Näiteks, et saada abi käsuga `add-user`, käivitage:
     ```bash
     dignacli add-user --help
     ```

     ### väljund:
      
     - **Käsu kirjeldus:** Pakub üksikasjaliku selgituse, mida antud käsk teeb.  
     - **Süntaks:** Kuvab täpse süntaksi, kaasa arvatud nõutud ja valikulised argumendid.  
     - **Valikud:** Loetleb käsu spetsiifilised valikud koos selgitustega.  
     - **Näited:** Esitab näited käsu tõhusaks kasutamiseks.

  
## `check-repo-connection` käsu kasutamine

käsk check-repo-connection on utiliit ***digna*** CLI tööriistas, mis on loodud testimaks ühenduvust ja juurdepääsu määratud ***digna*** repositooriumile. See käsk kontrollib, kas CLI suudab repositooriumiga suhelda.
      
### Käsu kasutus
```bash
dignacli check-repo-connection
```

Õnnestunud täitmise korral väljastab käsk ühenduse kinnitusinfo koos repositooriumi detailidega: repositooriumi versioon, host, andmebaas ja skeem.  
  
Kui repositooriumiga ühendus ei õnnestu, kontrollige, kas failis config.toml on õiged konfiguratsiooniseaded.

## `version` käsu kasutamine

Paigaldatud *dignacli* versiooni kontrollimiseks kasutage valikut `--version`.  
  
### Käsu kasutus
```bash
dignacli --version
```
  
### Näide väljundist
```bash
dignacli version 2024.11
```

## Logimisvalikute kasutamine
  
Vaikimisi on ***digna*** käskude konsooliväljund minimalistlik. Enamik käske võimaldab kuvada täiendavat teavet järgmiste valikute abil:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” ja „debug” määravad detailitaseme, samas kui valik „logfile” võimaldab suunata väljundi faili konsooliväljundi asemel.

# Kasutajate haldus

## `add-user` käsu kasutamine
  
Käsk add-user ***digna*** CLI-s kasutatakse uue kasutaja lisamiseks ***digna*** süsteemi.
  
### Käsu kasutus
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumendid

- **USER_NAME**: Uue kasutaja kasutajanimi (nõutud).
- **USER_FULL_NAME**: Uue kasutaja täielik nimi (nõutud).
- **USER_PASSWORD**: Uue kasutaja parool (nõutud).

### Valikud

- `--is_superuser`, `-su`: Lipp, mis määrab uue kasutaja administraatoriks.
- `--valid_until`, `-vu`: Seab kasutajakontole aegumiskuupäeva vormingus `YYYY-MM-DD HH:MI:SS`. Kui seda ei määrata, pole kontol aegumistähtaega.

### Näide

Uue kasutaja lisamiseks kasutajanimega `jdoe`, täieliku nimega `John Doe` ja parooliga `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Uue kasutaja lisamiseks ja konto aegumiskuupäeva seadistamiseks:
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
- **USER_NAME**: Kustutatava kasutaja kasutajanimi (nõutud). See on käsu ainus nõutav argument.

### Näide
```bash
dignacli delete-user jdoe
```
  
Selle käsu täitmine eemaldab kasutaja `jdoe` ***digna*** süsteemist, tühistades tema juurdepääsu ja kustutades repositooriumist tema seotud andmed ja õigused.

## `modify-user` käsu kasutamine

Käsk `modify-user` ***digna*** CLI-s kasutatakse olemasoleva kasutaja andmete uuendamiseks ***digna*** süsteemis.

### Käsu kasutus
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumendid
  
- **USER_NAME**: Muudetava kasutaja kasutajanimi (nõutud).
- **USER_FULL_NAME**: Kasutaja uus täielik nimi (nõutud).
  
### Valikud  
  
- `--is_superuser`, `-su`: Seab kasutaja superkasutajaks, andes talle kõrgendatud õigused. Selle lipu jaoks ei ole vaja väärtust.  
- `--valid_until`, `-vu`: Seab kasutajakonto aegumiskuupäeva vormingus YYYY-MM-DD HH:MI:SS. Kui seda ei anta, jääb konto kehtivaks määramata ajani.  
  
### Näide
  
Kasutaja `jdoe` täieliku nime muutmiseks „Johnathan Doe” ja kasutaja superkasutajaks tegemiseks:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` käsu kasutamine
  
Käsk `modify-user-pwd` ***digna*** CLI-s kasutatakse olemasoleva kasutaja parooli muutmiseks ***digna*** süsteemis.
  
### Käsu kasutus
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumendid
  
- **USER_NAME**: Kasutajanimi, kelle parool vahetatakse (nõutud).
- **USER_PWD**: Kasutaja uus parool (nõutud).
  
### Näide
  
Kasutaja `jdoe` parooli muutmiseks uueks `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` käsu kasutamine

Käsk `list-users` ***digna*** CLI-s kuvab nimekirja kõigist ***digna*** süsteemis registreeritud kasutajatest.

### Käsu kasutus

```bash
dignacli list-users
```

Selle käsu käivitamisel ühendub ***digna*** CLI ***digna*** repositooriumiga ja loetleb kõik kasutajad, kuvades nende ID, kasutajanime, täieliku nime, superkasutaja staatuse ja aegumisaegade märgistused.

# Repositooriumi haldus

### `upgrade-repo` käsu kasutamine
  
Käsk `upgrade-repo` ***digna*** CLI-s kasutatakse ***digna*** repositooriumi uuendamiseks või algseadistuse tegemiseks. See käsk on oluline värskenduste rakendamiseks või repositooriumi infrastruktuuri esmakordseks seadistamiseks.
  
### Käsu kasutus

```bash
dignacli upgrade-repo [options]
```
  
### Valikud
  
- `--simulation-mode`, `-s`: Kui lubatud, käivitab käsku simulatsioonirežiimis, mis prindib SQL-laused, mida täidetaks, kuid ei käivita neid tegelikult. See on kasulik muudatuste eelvaatamiseks ilma repositooriumi muutmata.  

  
### Näide
  
***digna*** repositooriumi uuendamiseks võite käivitada käsu ilma valikuteta:
  
```bash
dignacli upgrade-repo
```  
Uuenduse käivitamiseks simulatsioonirežiimis (et näha SQL-lauseid ilma nende rakendamiseta):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
See käsk on oluline ***digna*** süsteemi hooldamiseks, tagades, et andmebaasi skeem ja muud repositooriumi komponendid on tarkvara uusima versiooniga kooskõlas.

## `encrypt` käsu kasutamine
  
Käsk `encrypt` ***digna*** CLI-s kasutatakse parooli krüpteerimiseks.
  
### Käsu kasutus
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumendid
- **PASSWORD**: Krüpteeritav parool (nõutud).
  
### Näide
  
Parooli krüpteerimiseks tuleb parool anda argumendina.  
Näiteks parooli `mypassword123` krüpteerimiseks kasutage:
```bash
dignacli encrypt mypassword123
```
See käsk väljastab antud parooli krüpteeritud versiooni, mida saab seejärel turvalistes kontekstides kasutada. Kui parooli argumendi ei anta, kuvab CLI veateate, mis näitab puuduva argumendi.

## `generate-key` käsu kasutamine
  
Käsku `generate-key` kasutatakse Fernet-võtme genereerimiseks, mis on oluline paroolide turvamiseks, mis on salvestatud ***digna*** repositooriumis.
  
### Käsu kasutus
```bash
dignacli generate-key
```
  
# Andmete haldus

## `clean-up` käsu kasutamine

Käsk `clean-up` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja Traffic Light System andmete eemaldamiseks ühelt või mitmelt andmeallikalt määratud projekti piires. See käsk on oluline andmete elutsükli haldamiseks, aidates hoida korrastatud ja tõhusat andmekeskkonda, kustutades aegunud või mittevajalikke andmeid.

### Käsu kasutus

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, kust andmeid eemaldatakse (nõutud). Selle argumendi väärtusena kasutatav võtmesõna `all-projects` käsib ***digna***-l läbida kõik olemasolevad projektid ja rakendada käsku igale neist.
- **FROM_DATE**: Andmete eemaldamise alguskuupäev ja -aeg. Aktsepteeritud vormingud hõlmavad %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutud).
- **TO_DATE**: Andmete eemaldamise lõppkuupäev ja -aeg, järgides samu vorminguid mis FROM_DATE (nõutud).
  
### Valikud
  
- `--table-name`, `-tn`: Piirab clean-up operatsiooni konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, et piirata clean-up ainult tabelitele, mille nimedes on antud alamsõne.
- `--timing`, `-tm`: Kuvab puhastuse kestuse pärast lõpetamist.
- `--help`: Kuvab clean-up käsu abiinfo ja väljub.
  
### Näide
  
Andmete eemaldamiseks projektist ProjectA perioodil 1. jaanuar 2023 kuni 30. juuni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Andmete eemaldamiseks ainult tabelist nimega `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
See käsk aitab hallata andmete salvestust ja tagada, et repositoorium sisaldab ainult asjakohast infot.

## `inspect` käsu kasutamine

Käsk `inspect` ***digna*** CLI-s kasutatakse profiilide, ennustuste ja Traffic Light System andmete loomiseks ühelt või mitmelt andmeallikalt määratud projekti piires. See käsk aitab andmete analüüsimisel ja jälgimisel määratud ajavahemikus.

### Käsu kasutus

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid inspekteeritakse (nõutud). Selle argumendi väärtusena kasutatav võtmesõna `all-projects` käsib ***digna***-l läbida kõik olemasolevad projektid ja rakendada käsku igale neist.
- **FROM_DATE**: Andmete inspekteerimise alguskuupäev ja -aeg. Aktsepteeritavad vormingud hõlmavad %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutud).
- **TO_DATE**: Andmete inspekteerimise lõppkuupäev ja -aeg, järgides samu vorminguid mis FROM_DATE (nõutud).
  
### Valikud

- `--table-name`, `-tn`: Piirab inspekteerimise konkreetsele tabelile projektis.
- `--table-filter`, `-tf`: Filtreerib, et inspekteerida ainult tabeleid, mille nimedes on antud alamsõne.
- `--do-profile`: Käivitab profiilide uuesti kogumise. Vaikimisi on do-profile lubatud.
- `--no-do-profile`: Takistab profiilide uuesti kogumist.
- `--do-prediction`: Käivitab ennustuste ümberarvutamise. Vaikimisi on do-prediction lubatud.
- `--no-do-prediction`: Takistab ennustuste ümberarvutamist.
- `--do-alert-status`: Käivitab hoiatusstaatuste ümberarvutamise. Vaikimisi on do-alert-status lubatud.
- `--no-do-alert-status`: Takistab hoiatusstaatuste ümberarvutamist.
- `--timing`, `-tm`: Kuvab inspekteerimise kestuse pärast lõpetamist.
  
### Näide
  
Andmete inspekteerimiseks projektis `ProjectA` alates 1. jaanuarist 2024 kuni 31. jaanuarini 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Ainult konkreetse tabeli inspekteerimiseks ja ennustuste sunniviisiliseks ümberarvutamiseks:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
See käsk on kasulik uuendatud profiilide ja ennustuste genereerimiseks, andmete terviklikkuse jälgimiseks ja hoiatussüsteemide haldamiseks määratud projekti ajavahemikus.

## `tls-status` käsu kasutamine

Käsk `tls-status` ***digna*** CLI-s kasutatakse Traffic Light System (TLS) staatuse pärimiseks konkreetse tabeli kohta projektis määratud kuupäeval. Traffic Light System annab ülevaate andmete tervisest ja kvaliteedist, näidates võimalikke probleeme või hoiatusi, mis vajavad tähelepanu.
  
### Käsu kasutus
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille TLS staatust päritakse (nõutud).
- **TABLE_NAME**: Konkreetne tabel projektis, mille TLS staatust küsitakse (nõutud).
- **DATE**: Kuupäev, mille kohta TLS staatust päritakse, tavaliselt vormingus %Y-%m-%d (nõutud).
  
### Näide
  
TLS staatuse kontrollimiseks tabeli UserData kohta projektis ProjectA kuupäeval 1. juuli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

See käsk aitab kasutajatel andmekvaliteeti jälgida ja säilitada, pakkudes selget ja tegutsemisvõimelist olekuaruannet eelmääratletud kriteeriumitele tuginedes.

## `list-projects` käsu kasutamine
  
Käsk `list-projects` ***digna*** CLI-s kuvab nimekirja kõigist saadaval olevatest projektidest ***digna*** süsteemis.
  
### Käsu kasutus
  
```bash
dignacli list-projects
```

See käsk on eriti kasulik administraatoritele ja kasutajatele, kes haldavad mitut projekti, pakkudes kiiret ülevaadet saadaolevatest projektidest ***digna*** repositooriumis.

## `list-ds` käsu kasutamine

Käsk `list-ds` ***digna*** CLI-s kuvab nimekirja kõigist saadaolevatest andmeallikatest määratud projektis. See käsk on kasulik andmevarade mõistmiseks, mis on saadaval analüüsiks ja halduseks ***digna*** süsteemis.

### Käsu kasutus
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumendid
- **PROJECT_NAME**: Projekti nimi, mille andmeallikaid loetletakse (nõutud).
  
### Näide
  
Kõigi andmeallikate loetlemiseks projektis nimega `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
See käsk annab kasutajatele ülevaate projekti andmeallikatest, aidates neil andmemaastikul paremini navigeerida ja hallata.
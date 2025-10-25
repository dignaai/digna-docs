---
title: digna CLI Referenca 2024.11 – Ukazi & Primeri | digna Dokumentacija
description: Popolna referenca za digna CLI različico 2024.11. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi kot so add-user, check-repo-connection, upgrade-repo, inspect, tls-status.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Referenca 2024.11
**2024-11-03**

Ta stran dokumentira vse ukaze, primere uporabe in možnosti, ki so na voljo v različici **2024.11** CLI orodja ***digna***.


---
## Osnove CLI

---

## Uporaba možnosti `help`

Možnost `--help` zagotavlja informacije o razpoložljivih ukazih in njihovi uporabi. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
   Uporabite možnost `--help` takoj za ukazom ***digna***.  
   ```bash
   dignacli --help
   ```

3.  **Pridobivanje pomoči za določen ukaz:**  
  
    Za podrobne informacije o določenem ukazu dodajte `--help` k temu ukazu.  
    Na primer, za pomoč pri ukazu `add-user` zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### izhod:
      
     - **Opis ukaza:** Pojasni, kaj ukaz naredi.  
     - **Sintaksa:** Prikaže popolno sintakso, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Navaja možnosti, specifične za ukaz, skupaj z razlagami.  
     - **Primeri:** Ponudi primere, kako učinkovito zagnati ukaz.

  
## Uporaba ukaza `check-repo-connection`

Ukaz `check-repo-connection` je orodje v CLI orodju ***digna*** za testiranje povezave in dostopa do določenega ***digna*** repozitorija, kot je konfigurirano v CLI. Ta ukaz preveri, ali lahko CLI komunicira z repozitorijem.
      
### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Ob uspešnem izvajanju ukaz potrdi povezavo in izpiše naslednje podrobnosti o repozitoriju: Repository version, Host, Database in Schema.  
  
Če povezava z repozitorijem ni uspešna, preverite datoteko config.toml za pravilne nastavitve.

## Uporaba ukaza `version`

Za preverjanje nameščene različice *dignacli* uporabite možnost `--version`.  
  
### Uporaba ukaza
```bash
dignacli --version
```
  
### Primer izhoda
```bash
dignacli version 2024.11
```

## Uporaba možnosti beleženja (logging)
  
Privzeto je izhod ukazov ***digna*** zasnovan kot minimalen. Večina ukazov omogoča dodatne informacije z uporabo naslednjih možnosti:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
"verbose" in "debug" določata raven podrobnosti, ključ "logfile" pa omogoča preusmeritev izhoda v datoteko namesto v konzolo.

# Upravljanje uporabnikov

## Uporaba ukaza `add-user`
  
Ukaz `add-user` se uporablja za dodajanje novega uporabnika v sistem ***digna*** prek CLI.
  
### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenti

- **USER_NAME**: Uporabniško ime novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

### Možnosti

- `--is_superuser`, `-su`: Zastavica za nastavitev novega uporabnika kot skrbnika.
- `--valid_until`, `-vu`: Določi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni naveden, je račun brez časovne omejitve.

### Primer

Za dodajanje novega uporabnika z uporabniškim imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Za dodajanje novega uporabnika z določenim datumom poteka:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Uporaba ukaza `delete-user`
  
Ukaz `delete-user` se uporablja za odstranitev obstoječega uporabnika iz sistema ***digna*** prek CLI.
  
### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
### Argumenti
- **USER_NAME**: Uporabniško ime uporabnika, ki ga želite izbrisati (obvezno). To je edini zahtevan argument ukaza.

### Primer
```bash
dignacli delete-user jdoe
```
  
Ob izvedbi bo uporabnik `jdoe` odstranjen iz sistema ***digna***; dostop bo preklican in s tem povezani podatki ter pravice v repozitoriju bodo izbrisani.

## Uporaba ukaza `modify-user`

Ukaz `modify-user` se uporablja za posodabljanje informacij obstoječega uporabnika v sistemu ***digna*** prek CLI.

### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, ki ga želite spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuporabnika z višjimi privilegiji. Ta zastavica ne potrebuje dodatne vrednosti.  
- `--valid_until`, `-vu`: Določi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni naveden, bo račun veljal brez časovne omejitve.  
  
### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in njegovo povišanje v superuporabnika:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Uporaba ukaza `modify-user-pwd`
  
Ukaz `modify-user-pwd` se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna*** prek CLI.
  
### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, katerega geslo želite spremeniti (obvezno).
- **USER_PWD**: Novo geslo uporabnika (obvezno).
  
### Primer
  
Za nastavitev gesla uporabnika `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Uporaba ukaza `list-users`

Ukaz `list-users` prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***, prek CLI.

### Uporaba ukaza

```bash
dignacli list-users
```

Zagon tega ukaza se poveže z repozitorijem ***digna*** in izpiše vse uporabnike z ID-jem, uporabniškim imenom, polnim imenom, statusom superuporabnika in časovnimi žigi datuma poteka.

# Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` se uporablja za nadgradnjo ali inicializacijo repozitorija ***digna*** prek CLI. Ta ukaz je potreben za uporabo posodobitev ali za prvo namestitev repozitorija.
  
### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
### Možnosti
  
- `--simulation-mode`, `-s`: Ko je omogočeno, ukaz deluje v simulacijskem načinu; izpiše SQL ukaze, ki bi jih izvedel, vendar jih ne izvede. To je koristno za predogled sprememb pred njihovo izvedbo.  

  
### Primer
  
Repositotij ***digna*** lahko nadgradite brez dodatnih možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (ogled SQL ukazov brez izvedbe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključen za vzdrževanje sistema ***digna***, saj zagotavlja, da je shema baze podatkov in druge komponente repozitorija združljive z najnovejšo različico programske opreme.

## Uporaba ukaza `encrypt`
  
Ukaz `encrypt` šifrira geslo v okviru CLI orodja ***digna***.
  
### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenti
- **PASSWORD**: Geslo, ki ga želite šifrirati (obvezno).
  
### Primer
  
Geslo se šifrira tako, da ga podate kot argument.   
Na primer, za šifriranje gesla `mypassword123`:
```bash
dignacli encrypt mypassword123
```
Ukaz izpiše šifrirano različico podanega gesla; to različico lahko nato uporabite v varnejših kontekstih. Če geslovo ni podano, bo CLI vrnil napako o manjkajočem argumentu.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` ustvari Fernet ključ, ki je potreben za zaščito gesel, shranjenih v repozitoriju ***digna***.
  
### Uporaba ukaza
```bash
dignacli generate-key
```
  
# Upravljanje podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` odstrani profile, napovedi in podatke Trafik Išči (Traffic Light System - TLS) za enega ali več virov podatkov v okviru določenega projekta v CLI orodju ***digna***. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in čiščenje zastarelih ali nepotrebnih podatkov.

### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega bodo podatki odstranjeni (obvezno). Če se kot argument navede ključna beseda all-projects, bo ***digna*** iteriral čez vse obstoječe projekte in uporabil ukaz.  
- **FROM_DATE**: Začetni datum in čas čiščenja podatkov. Sprejeti formati so %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).  
- **TO_DATE**: Končni datum in čas čiščenja podatkov; sprejema iste formate kot FROM_DATE (obvezno).
  
### Možnosti
  
- `--table-name`, `-tn`: Omeji čiščenje na določeno tabelo v projektu.
- `--table-filter`, `-tf`: Uporabi filter za omejitev čiščenja na tabele, katerih imena vsebujejo navedeni podniz.
- `--timing`, `-tm`: Po zaključku prikaže čas trajanja čiščenja.
- `--help`: Prikaže pomoč za ukaz clean-up in izstopi.
  
### Primer
  
Za odstranjevanje podatkov iz projekta ProjectA v obdobju od 1. januarja 2023 do 30. junija 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranjevanje podatkov samo iz določene tabele `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga pri upravljanju porabe prostora za shranjevanje in zagotavlja, da repozitorij vsebuje le relevantne informacije.

## Uporaba ukaza `inspect`

Ukaz `inspect` v CLI orodju ***digna*** ustvari profile, napovedi in podatke Trafik Išči (TLS) za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz pomaga analizirati in spremljati podatke za določeno časovno obdobje.

### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se izvaja inšpekcija (obvezno). Če je kot argument podano all-projects, bo ***digna*** iteriral čez vse obstoječe projekte in uporabil ukaz.
- **FROM_DATE**: Datum in čas začetka inšpekcije. Sprejeti formati so %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Datum in čas konca inšpekcije; sprejema iste formate kot FROM_DATE (obvezno).
  
### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo v projektu.
- `--table-filter`, `-tf`: Uporabi filter za izvajanje inšpekcije le na tabelah, katerih imena vsebujejo navedeni podniz.
- `--do-profile`: Sproži ponovno zbiranje profilov. Privzeto je do-profile vklopljen.
- `--no-do-profile`: Onemogoči ponovno zbiranje profilov.
- `--do-prediction`: Sproži ponovno izračunavanje napovedi. Privzeto je do-prediction vklopljen.
- `--no-do-prediction`: Onemogoči ponovno izračunavanje napovedi.
- `--do-alert-status`: Sproži ponovno izračunavanje stanja opozoril. Privzeto je do-alert-status vklopljen.
- `--no-do-alert-status`: Onemogoči ponovno izračunavanje stanja opozoril.
- `--timing`, `-tm`: Po zaključku prikaže čas trajanja inšpekcije.
  
### Primer
  
Za inšpekcijo podatkov v projektu `ProjectA` med 1. januarjem 2024 in 31. januarjem 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za inšpekcijo samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za ustvarjanje posodobljenih profilov in napovedi, spremljanje integritete podatkov ter upravljanje sistema opozoril znotraj navedenega časovnega intervala projekta.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` v CLI orodju ***digna*** poizveduje stanje Trafik Išči (Traffic Light System - TLS) za določeno tabelo znotraj projekta na določen datum. TLS daje vpoglede v zdravje in kakovost podatkov ter označuje morebitne težave ali opozorila, ki zahtevajo pozornost.
  
### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se preverja stanje TLS (obvezno).
- **TABLE_NAME**: Ime tabele v projektu, za katero se preverja stanje TLS (obvezno).
- **DATE**: Datum, za katerega se preverja stanje TLS, običajno v formatu %Y-%m-%d (obvezno).
  
### Primer
  
Za preverjanje stanja TLS za tabelo `UserData` v projektu `ProjectA` na datum 1. julij 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ta ukaz uporabnikom zagotovi jasen in uporabniku prijazen poročilo o stanju na podlagi vnaprej določenih kriterijev, kar pomaga pri spremljanju in vzdrževanju kakovosti podatkov.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` prikaže seznam vseh razpoložljivih projektov v CLI orodju ***digna***.
  
### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za upravitelje in uporabnike, ki upravljajo več projektov, saj ponuja hiter pregled obstoječih projektov v repozitoriju ***digna***.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` prikaže vse obstoječe vire podatkov znotraj določenega projekta v CLI orodju ***digna***. Pomaga pri razumevanju razpoložljivih podatkovnih sredstev za analizo in upravljanje.

### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se izpisujejo viri podatkov (obvezno).
  
### Primer
  
Za izpis vseh virov podatkov v projektu `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz nudi pregled virov podatkov v projektu in pomaga uporabnikom učinkoviteje pregledovati ter upravljati podatkovno okolje.
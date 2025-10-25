---
title: digna CLI Referenca 2024.12 – Ukazi & Primeri | digna Dokumentacija
description: Popolna referenca za digna CLI različico 2024.12. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-repo-connection, upgrade-repo, inspect in več.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Referenca 2024.12
**2024-12-09**

Ta stran dokumentira vse ukaze, primere uporabe in možnosti, ki so na voljo v digna CLI različici **2024.12**.

---


**2024-12-09**


---

## Osnove CLI

---

## Uporaba možnosti `help`

Možnost `--help` zagotavlja informacije o razpoložljivih ukazih in njihovem načinu uporabe. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite `--help` takoj za ključnim besedo `dignacli`.  
   ```bash
   dignacli --help
   ```

2. **Pridobitev pomoči za določen ukaz:**  
  
    Za podrobne informacije o določenem ukazu dodajte `--help` k temu ukazu.  
    Na primer, za pomoč pri ukazu `add-user` zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### izhod:
      
     - **Opis ukaza:** Podrobno pojasni, kaj ukaz počne.  
     - **Sinteša:** Prikaže polno sintakso z zahtevnimi in izbirnimi argumenti.  
     - **Možnosti:** Našteje možnosti ukaza in njihove opise.  
     - **Primeri:** Prikaže primere, kako ukaz učinkovito zagnati.

  
## Uporaba ukaza `check-repo-connection`

Ukaz `check-repo-connection` je pripomoček v digna CLI za testiranje povezave in dostopa do določenega digna repozitorija. Ta ukaz preveri, ali se CLI lahko poveže z repozitorijem.
      
### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Ob uspešnem zagonu ukaz potrdi povezavo in izpiše informacije o repozitoriju, kot so Repository version, Host, Database in Schema.  
  
Če povezava do repozitorija ni uspešna, preverite konfiguracijo v datoteki config.toml.

## Uporaba ukaza `version`

Za preverjanje nameščene različice *dignacli* uporabite možnost `--version`.  
  
### Uporaba ukaza
```bash
dignacli --version
```
  
### Primer izhoda
```bash
dignacli version 2024.12
```

## Možnosti beleženja (logging)
  
Privzeto so izhodi digna ukazov zasnovani minimalistično. Večina ukazov omogoča prikaz dodatnih informacij z naslednjimi možnostmi:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ in „debug“ določata raven podrobnosti, medtem ko možnost „logfile“ preusmeri izhod v datoteko namesto v konzolo.

# Upravljanje uporabnikov

## Uporaba ukaza `add-user`
  
Ukaz `add-user` se uporablja za dodajanje novega uporabnika v digna sistem preko digna CLI.
  
### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenti

- **USER_NAME**: Uporniško ime novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

### Možnosti

- `--is_superuser`, `-su`: Označi novega uporabnika kot skrbnika.
- `--valid_until`, `-vu`: Določi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni nastavljen, račun nima roka veljavnosti.

### Primer

Za dodajanje uporabnika z uporabniškim imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Za dodajanje novega uporabnika z datumom poteka računa:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Uporaba ukaza `delete-user`
  
Ukaz `delete-user` se uporablja za odstranjevanje obstoječega uporabnika iz digna sistema preko digna CLI.
  
### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
### Argumenti
- **USER_NAME**: Uporniško ime uporabnika, ki ga želite izbrisati (obvezno). To je edini zahtevan argument tega ukaza.

### Primer
```bash
dignacli delete-user jdoe
```
  
Ob zagonu tega ukaza bo uporabnik `jdoe` odstranjen iz digna sistema, dostop bo preklican in ustrezni podatki ter dovoljenja v repozitoriju bodo izbrisani.

## Uporaba ukaza `modify-user`

Ukaz `modify-user` se uporablja za posodabljanje informacij obstoječega uporabnika v digna CLI.

### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, ki ga želite urejati (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuporabnika, kar dodeli povišane privilegije. Ta preklop ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Določi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni podano, račun velja nedoločen čas.  
  
### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in dodelitev super uporabniških pravic:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Uporaba ukaza `modify-user-pwd`
  
Ukaz `modify-user-pwd` se uporablja za spreminjanje gesla obstoječega uporabnika v digna CLI.
  
### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, katerega geslo želite spremeniti (obvezno).
- **USER_PWD**: Novo geslo uporabnika (obvezno).
  
### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Uporaba ukaza `list-users`

Ukaz `list-users` se uporablja za izpis vseh uporabnikov, registriranih v digna sistemu preko digna CLI.

### Uporaba ukaza

```bash
dignacli list-users
```

Zagon tega ukaza se poveže z digna repozitorijem in prikaže vse uporabnike; izpiše ID, uporabniško ime, polno ime, status superuporabnika in časovne žige poteka.

# Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` se uporablja za nadgradnjo ali inicializacijo digna repozitorija preko digna CLI. Ta ukaz je potreben za uporabo posodobitev ali začetno vzpostavitev repozitorija.
  
### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
### Možnosti
  
- `--simulation-mode`, `-s`: Če je omogočeno, ukaz deluje v simulacijskem načinu; izpiše SQL ukaze, ki bi jih izvedel, vendar jih ne izvede. Uporabno za predogled sprememb brez vpliva na repozitorij.  

  
### Primer
  
Za nadgradnjo digna repozitorija lahko ukaz zaženete brez dodatnih možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (prikaz SQL ukazov brez izvajanja):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključen za vzdrževanje digna sistema; zagotavlja, da je shema baze podatkov in druge komponente repozitorija združljive z najnovejšo različico programske opreme.

## Uporaba ukaza `encrypt`
  
Ukaz `encrypt` se uporablja za šifriranje gesla v digna CLI.
  
### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenti
- **PASSWORD**: Geslo, ki ga je treba zašifrirati (obvezno).
  
### Primer
  
Geslo za šifriranje morate posredovati kot argument.   
Na primer, za šifriranje gesla `mypassword123`:
```bash
dignacli encrypt mypassword123
```
Ukaz izpiše šifrirano obliko podanega gesla; ta izhod se lahko nato uporabi v varnih kontekstih. Če ni podanega argumenta gesla, bo CLI prijavil napako o manjkajočem argumentu.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` generira Fernet ključ, potreben za zaščito gesel, shranjenih v digna repozitoriju.
  
### Uporaba ukaza
```bash
dignacli generate-key
```
  
# Upravljanje podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` se uporablja za odstranitev profilov, napovedi in podatkov sistema prometnih luči (TLS) za enega ali več virov podatkov v okviru določenega projekta v digna CLI. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga ohranjati urejeno ter učinkovito podatkovno okolje z odstranjevanjem starih ali nepotrebnih podatkov.

### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega bodo podatki odstranjeni (obvezno). Če je namesto imena projekta podan ključna beseda all-projects, bo digna preletel vse obstoječe projekte in izvedel ukaz zanje.
- **FROM_DATE**: Začetni datum in čas za brisanje podatkov. Sprejeti formati: %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za brisanje podatkov; sprejema iste formate kot FROM_DATE (obvezno).
  
### Možnosti
  
- `--table-name`, `-tn`: Omeji čiščenje na določeno tabelo v projektu.
- `--table-filter`, `-tf`: Uporabi filter za omejitev na tabele, katerih imena vsebujejo podniz.
- `--timing`, `-tm`: Prikaže čas, porabljen za zaključen postopek čiščenja.
- `--help`: Prikaže pomoč za ukaz clean-up in zapusti.
  
### Primer
  
Za odstranitev podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za brisanje podatkov samo iz določene tabele, imenovane `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga pri upravljanju skladiščenja podatkov in zagotavlja, da repozitorij vsebuje le relevantne informacije.

## Uporaba ukaza `inspect`

Ukaz `inspect` se uporablja za generiranje profilov, napovedi in podatkov sistema prometnih luči za enega ali več virov podatkov v okviru določenega projekta v digna CLI. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem časovnem obdobju.

### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, katerega podatke želite pregledati (obvezno). Če je namesto imena projekta uporabljena ključna beseda all-projects, bo digna preletel vse obstoječe projekte in ukaz uporabil za vse.
- **FROM_DATE**: Začetni datum in čas za pregled podatkov. Sprejeti formati: %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za pregled podatkov; sprejema iste formate kot FROM_DATE (obvezno).
  
### Možnosti

- `--table-name`, `-tn`: Omeji pregled na določeno tabelo v projektu.
- `--table-filter`, `-tf`: Uporabi filter in preišče tabele, katerih imena vsebujejo navedeni podniz.
- `--do-profile`: Sproži ponovno zbiranje profilov. Privzeto je do-profile.
- `--no-do-profile`: Onemogoči ponovno zbiranje profilov.
- `--do-prediction`: Sproži ponovno izračunavanje napovedi. Privzeto je do-prediction.
- `--no-do-prediction`: Onemogoči ponovno izračunavanje napovedi.
- `--do-alert-status`: Sproži ponovno izračunavanje stanja opozoril. Privzeto je do-alert-status.
- `--no-do-alert-status`: Onemogoči ponovno izračunavanje stanja opozoril.
- `--iterative`: Sproži pregled navedenega obdobja z dnevnim iteriranjem. Privzeto je iterative.
- `--no-iterative`: Sproži pregled celega obdobja na enkrat.
- `--timing`, `-tm`: Prikaže čas, porabljen za dokončanje pregleda.
  
### Primer
  
Za pregled podatkov projekta `ProjectA` med 1. januarjem 2024 in 31. januarjem 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za pregled samo določene tabele in prisilno ponovno izračunanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za ustvarjanje posodobljenih profilov in napovedi, spremljanje celovitosti podatkov ter upravljanje sistema opozoril za določeno projektno časovno obdobje.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` se uporablja za poizvedbo o stanju sistema prometnih luči (TLS) za določeno tabelo v projektu na določen datum. Sistem prometnih luči zagotavlja informacije o zdravju in kakovosti podatkov ter opozarja na težave ali nepravilnosti, ki zahtevajo pozornost.
  
### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega poizvedujete stanje TLS (obvezno).
- **TABLE_NAME**: Ime tabele v projektu, za katero poizvedujete stanje TLS (obvezno).
- **DATE**: Datum, za katerega poizvedujete stanje TLS, običajno v formatu %Y-%m-%d (obvezno).
  
### Primer
  
Za preverjanje stanja TLS za tabelo `UserData` v projektu `ProjectA` na datum 1. julij 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ta ukaz zagotovi jasen in uporabniku prijazen poročilo o stanju glede na vnaprej določena merila, s čimer pomaga uporabnikom spremljati in vzdrževati kakovost podatkov.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` prikaže seznam vseh razpoložljivih projektov v digna CLI.
  
### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je posebej koristen za skrbnike in uporabnike, ki upravljajo več projektov; omogoča hiter pregled na razpoložljive projekte v digna repozitoriju.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` prikaže vse obstoječe vire podatkov znotraj določenega projekta v digna CLI. Ta ukaz pomaga razumeti, katere podatkovne vire lahko uporabite za analizo in upravljanje.

### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega želite izpisati vire podatkov (obvezno).
  
### Primer
  
Za izpis vseh virov podatkov v projektu `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz daje splošen pregled razpoložljivih virov podatkov v projektu, kar pomaga pri učinkovitejšem upravljanju podatkovnega prostora.
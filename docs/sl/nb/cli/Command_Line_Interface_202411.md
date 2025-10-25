---
title: digna CLI-referenca 2024.11 – Ukazi in primeri | digna-dokumentacija
description: Celovita referenca za izdajo digna CLI 2024.11. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-repo-connection, upgrade-repo, inspect, tls-status in drugi.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI-referenca 2024.11
**2024-11-03**

Ta stran dokumentira celoten nabor ukazov, ki so na voljo v izdaji CLI-ja ***digna*** **2024.11**, vključno z vzorčnimi uporabo in možnostmi.


---
## Osnove CLI

---

## Uporaba možnosti `help`

Možnost `--help` daje informacije o razpoložljivih ukazih in o tem, kako jih uporabiti. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help neposredno za ključnimi besedami ***digna***  
   ```bash
   dignacli --help
   ```

3.  **Pridobitev pomoči za določene ukaze:**  
  
    Za podrobne informacije o določenem ukazu dodajte `--help` za tem ukazom.  
    Na primer, da dobite pomoč za ukaz `add-user`, zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### izhod:
      
     - **Opis ukaza:** Podroben opis, kaj ukaz počne.  
     - **Sinteza:** Prikazuje natančno sintezo, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Navedba morebitnih opcij, specifičnih za ukaz, z razlagami.  
     - **Primeri:** Predstavlja primere učinkovite uporabe ukaza.

  
## Uporaba ukaza `check-repo-connection`

Ukaz check-repo-connection je orodje v CLI-ju ***digna***, namenjeno testiranju povezave in dostopa do navedenega repozitorija ***digna***. Ta ukaz zagotavlja, da lahko CLI komunicira z repozitorijem.
      
### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Ob uspešnem izvajanju bo ukaz potrdil povezavo ter prikazal podrobnosti o repozitoriju: različico repozitorija, gostitelja (Host), bazo podatkov (Database) in shemo (Schema).  
  
Če povezava do repozitorija ne uspe, preverite datoteko config.toml za pravilne nastavitve konfiguracije.

## Uporaba ukaza `version`

Za preverjanje nameščene različice *dignacli* uporabite možnost --version.  
  
### Uporaba ukaza
```bash
dignacli --version
```
  
### Primer izhoda
```bash
dignacli version 2024.11
```

## Uporaba možnosti za beleženje

Privzeto je izpis v konzolo iz ukazov ***digna*** zasnovan minimalistično. Večina ukazov omogoča prikaz dodatnih informacij z uporabo naslednjih možnosti:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” in “debug” določa raven podrobnosti, medtem ko preklop “logfile” omogoča preusmeritev izpisa v datoteko namesto v konzolo.

# Upravljanje uporabnikov

## Uporaba ukaza `add-user`
  
Ukaz add-user v CLI-ju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenti

- **USER_NAME**: Uporniško ime za novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

### Možnosti

- `--is_superuser`, `-su`: Preklop za označitev novega uporabnika kot skrbnika (superuser).
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni nastavljen, račun nima poteka.

### Primer

Za dodajanje novega uporabnika z uporabniškim imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Za dodajanje novega uporabnika in nastavitev datuma poteka računa:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Uporaba ukaza `delete-user`
  
Ukaz `delete-user` v CLI-ju ***digna*** se uporablja za odstranitev obstoječega uporabnika iz sistema ***digna***.
  
### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
### Argumenti
- **USER_NAME**: Uporniško ime uporabnika, ki ga je treba izbrisati (obvezno). To je edini argument, ki ga ukaz zahteva.

### Primer
```bash
dignacli delete-user jdoe
```
  
Ob izvedbi tega ukaza bo uporabnik `jdoe` odstranjen iz sistema ***digna***, z odpoklicem dostopa ter brisanjem povezanih podatkov in pravic v repozitoriju.

## Uporaba ukaza `modify-user`

Ukaz `modify-user` v CLI-ju ***digna*** se uporablja za posodabljanje podatkov obstoječega uporabnika v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, ki ga je treba spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
### Možnosti  
  
- `--is_superuser`, `-su`: Označi uporabnika kot superuser in mu dodeli povišane pravice. Ta preklop ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven za nedoločen čas.  
  
### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in označitev uporabnika kot superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Uporaba ukaza `modify-user-pwd`
  
Ukaz `modify-user-pwd` v CLI-ju ***digna*** se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna***.
  
### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, katerega geslo se spreminja (obvezno).
- **USER_PWD**: Novo geslo za uporabnika (obvezno).
  
### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Uporaba ukaza `list-users`

Ukaz `list-users` v CLI-ju ***digna*** prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

### Uporaba ukaza

```bash
dignacli list-users
```

Zagon tega ukaza v CLI-ju ***digna*** bo povezal z repozitorijem ***digna*** in izpisal vse uporabnike z njihovimi ID-ji, uporabniškimi imeni, polnimi imeni, statusom superuser ter časom poteka.

# Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` v CLI-ju ***digna*** se uporablja za nadgradnjo ali inicializacijo repozitorija ***digna***. Ta ukaz je potreben za uporabo posodobitev ali za izbiro repozitorijske infrastrukture ob prvi namestitvi.
  
### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
### Možnosti
  
- `--simulation-mode`, `-s`: Ko je vklopljeno, ukaz teče v simulacijskem načinu in izpiše SQL stavke, ki bi bili izvedeni, vendar jih ne izvede. To je uporabno za predogled sprememb brez spreminjanja repozitorija.  

  
### Primer
  
Za nadgradnjo repozitorija ***digna*** lahko zaženete ukaz brez možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (za ogled SQL stavkov brez njihove uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je pomemben za vzdrževanje sistema ***digna*** in zagotavljanje, da so shema baze podatkov ter drugi repozitorijski komponenti posodobljeni na najnovejšo različico programske opreme.

## Uporaba ukaza `encrypt`
  
Ukaz `encrypt` v CLI-ju ***digna*** se uporablja za šifriranje gesla.
  
### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenti
- **PASSWORD**: Geslo, ki ga želite šifrirati (obvezno).
  
### Primer
  
Za šifriranje gesla morate geslo posredovati kot argument.   
Na primer, za šifriranje gesla `mypassword123` uporabite:
```bash
dignacli encrypt mypassword123
```
Ta ukaz izpiše šifrirano različico navedenega gesla, ki jo lahko nato uporabite v varnih okoljih. Če argument gesla ni podan, bo CLI prikazal napako, ki označuje manjkajoči argument.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` se uporablja za generiranje Fernet-ključa, ki je potreben za varovanje gesel, shranjenih v repozitoriju ***digna***.
  
### Uporaba ukaza
```bash
dignacli generate-key
```
  
# Obdelava podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` v CLI-ju ***digna*** se uporablja za odstranjevanje profilov, napovedi in podatkov iz Traffic Light System za eno ali več podatkovnih virov znotraj določenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga pri vzdrževanju organiziranega in učinkovitega podatkovnega okolja z odstranjevanjem zastarelih ali nepotrebnih podatkov.

### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega bodo podatki odstranjeni (obvezno). Uporaba ključne besede all-projects v tem argumentu pove sistemu ***digna***, naj iterira skozi vse obstoječe projekte in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas čiščenja podatkov. Dovoljeni formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas čiščenja podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
### Možnosti
  
- `--table-name`, `-tn`: Omeji operacijo clean-up na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtri za omejitev clean-up samo na tabele, katerih imena vsebujejo navedeno podniz.
- `--timing`, `-tm`: Prikaže porabljen čas za postopek clean-up po zaključku.
- `--help`: Prikaže pomoč za ukaz clean-up in izstopi.
  
### Primer
  
Za odstranjevanje podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranjevanje podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga pri upravljanju hrambe podatkov in zagotavlja, da repozitorij vsebuje le relevantne informacije.

## Uporaba ukaza `inspect`

Ukaz `inspect` v CLI-ju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov za Traffic Light System za enega ali več podatkovnih virov znotraj določenega projekta. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem časovnem obdobju.

### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se bodo podatki pregledali (obvezno). Uporaba ključne besede all-projects v tem argumentu pove sistemu ***digna***, naj iterira skozi vse obstoječe projekte in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas za inšpekcijo podatkov. Dovoljeni formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za inšpekcijo podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtriraj inšpekcijo samo na tabele, katerih imena vsebujejo navedeno podniz.
- `--do-profile`: Sproži ponovno zbiranje profilov. Privzeto je do-profile.
- `--no-do-profile`: Onemogoči ponovno zbiranje profilov.
- `--do-prediction`: Sproži ponovno izračunavanje napovedi. Privzeto je do-prediction.
- `--no-do-prediction`: Onemogoči ponovno izračunavanje napovedi.
- `--do-alert-status`: Sproži ponovno izračunavanje statusa opozoril. Privzeto je do-alert-status.
- `--no-do-alert-status`: Onemogoči ponovno izračunavanje statusa opozoril.
- `--timing`, `-tm`: Prikaže trajanje inšpekcijskega postopka po zaključku.
  
### Primer
  
Za inšpekcijo podatkov za projekt `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za inšpekcijo samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje integritete podatkov ter upravljanje sistema opozoril v določenem projektno-časovnem okviru.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` v CLI-ju ***digna*** se uporablja za pridobitev stanja Traffic Light System (TLS) za določeno tabelo v projektu na določen datum. Traffic Light System nudi vpogled v kakovost in zdravje podatkov ter označuje morebitne težave ali opozorila, ki potrebujejo pozornost.
  
### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se zahteva TLS-status (obvezno).
- **TABLE_NAME**: Konkretna tabela v projektu, za katero velja TLS-status (obvezno).
- **DATE**: Datum, za katerega velja TLS-status, navadno v formatu %Y-%m-%d (obvezno).
  
### Primer
  
Za preverjanje TLS-statusa tabele UserData v projektu ProjectA na datum 1. julija 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov z jasnim in izvedljivim poročilom stanja, temelječim na vnaprej določenih kriterijih.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` v CLI-ju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj nudi hiter pregled razpoložljivih projektov v repozitoriju ***digna***.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` v CLI-ju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih podatkovnih virov znotraj določenega projekta. Ta ukaz je uporaben za razumevanje, kateri podatkovni viri so na voljo za analizo in upravljanje v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se bodo izpisali podatkovni viri (obvezno).
  
### Primer
  
Za izpis vseh podatkovnih virov v projektu `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled nad podatkovnimi viri, ki so na voljo v projektu, in jim pomaga učinkoviteje krmariti in upravljati podatkovno okolje.
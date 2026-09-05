---
title: digna CLI Reference 2025.04 – Ukazi in primeri | digna Dokumentacija
description: Popolna referenca za digna CLI izdajo 2025.04. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-repo-connection, upgrade-repo, inspect in drugi.
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Ta stran dokumentira celoten nabor ukazov, ki so na voljo v ***digna*** CLI izdaji **2025.04**, vključno z primeri uporabe in možnostmi.

---

## Osnove CLI

---

## Uporaba možnosti `help`

Možnost `--help` zagotavlja informacije o razpoložljivih ukazih in njihovi uporabi. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help takoj za ključno besedo ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Pridobitev pomoči za določene ukaze:**  
  
    Za podrobne informacije o določenem ukazu pripnite `--help` temu ukazu.
    Na primer, če želite pomoč pri ukazu `add-user`, zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### izhod:
      
     - **Opis ukaza:** Ponuja podroben opis, kaj ukaz počne.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Navaja vse možnosti, specifične za ukaz, skupaj z njihovimi razlagami.  
     - **Primeri:** Pruža primere, kako učinkovito izvesti ukaz.

  
## Uporaba ukaza `check-repo-connection`

Ukaz check-repo-connection je pripomoček znotraj orodja ***digna*** CLI, zasnovan za testiranje povezljivosti in dostopa do določenega ***digna*** repozitorija. Ta ukaz zagotavlja, da lahko CLI komunicira z repozitorijem.
      
#### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Ob uspešni izvedbi ukaz izpiše potrdilo o povezavi skupaj s podrobnostmi o repozitoriju: različica repozitorija, gostitelj, baza podatkov in shema.  
  
Če povezava z repozitorijem ni uspešna, preverite datoteko config.toml za pravilne nastavitve konfiguracije.

## Uporaba ukaza ‘version’

Za preverjanje nameščene različice *dignacli* uporabite možnost --version.  
  
#### Uporaba ukaza
```bash
dignacli --version
```
  
#### Primer izhoda
```bash
dignacli version 2025.04
```

## Uporaba možnosti za beleženje (logging)
  
Privzeto je izpis ukazov ***digna*** v konzoli zasnovan minimalistično. Večina ukazov ponuja možnost podajanja dodatnih informacij z uporabo naslednjih možnosti:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
»verbose« in »debug« določata raven podrobnosti, medtem ko stikalo »logfile« omogoča preusmeritev izpisa v datoteko namesto na konzolo.

## Upravljanje uporabnikov

### Uporaba ukaza ‘add-user’
  
Ukaz add-user v ***digna*** CLI se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumenti

- **USER_NAME**: Uporabniško ime za novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

#### Možnosti

- `--is_superuser`, `-su`: Preklop za označitev novega uporabnika kot skrbnika.
- `--valid_until`, `-vu`: Nastavi datum poteka uporabniškega računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni nastavljen, račun nima datuma poteka.

#### Primer

Za dodajanje novega uporabnika z uporabniškim imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Za dodajanje novega uporabnika in nastavljanje datuma poteka računa:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Uporaba ukaza `delete-user`
  
Ukaz `delete-user` v ***digna*** CLI se uporablja za odstranitev obstoječega uporabnika iz sistema ***digna***.
  
#### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
##### Argumenti
- **USER_NAME**: Uporabniško ime uporabnika, ki bo izbrisan (obvezno). To je edini argument, ki ga ukaz zahteva.

#### Primer
```bash
dignacli delete-user jdoe
```
  
Izvedba tega ukaza bo odstranila uporabnika `jdoe` iz sistema ***digna***, odvzela njihov dostop in izbrisala pripadajoče podatke ter pravice iz repozitorija.

### Uporaba ukaza `modify-user`

Ukaz `modify-user` v ***digna*** CLI se uporablja za posodabljanje podatkov obstoječega uporabnika v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, ki ga želite spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime za uporabnika (obvezno).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuserja, kar podeli povišane privilegije. Ta preklop ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka uporabniškega računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven brez časovne omejitve.  
  
#### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in nastavitev uporabnika kot superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Uporaba ukaza `modify-user-pwd`
  
Ukaz `modify-user-pwd` v ***digna*** CLI se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna***.
  
#### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, za katerega se geslo spreminja (obvezno).
- **USER_PWD**: Novo geslo za uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Uporaba ukaza `list-users`

Ukaz `list-users` v ***digna*** CLI prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

#### Uporaba ukaza

```bash
dignacli list-users
```

Izvedba tega ukaza v ***digna*** CLI se poveže z ***digna*** repozitorijem in izpiše vse uporabnike, prikazano bodo njihova ID, uporabniško ime, polno ime, status superuserja in časovne oznake poteka.

## Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` v ***digna*** CLI se uporablja za nadgradnjo ali inicializacijo ***digna*** repozitorija. Ta ukaz je ključnega pomena za uporabo posodobitev ali nastavitev repozitorijske infrastrukture prvič.
  
#### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Ko je omogočeno, ta možnost zažene ukaz v načinu simulacije, kar izpiše SQL stavke, ki bi jih bilo treba izvesti, vendar jih dejansko ne izvrši. To je uporabno za predogled sprememb brez spreminjanja repozitorija.  

  
#### Primer
  
Za nadgradnjo ***digna*** repozitorija lahko zaženete ukaz brez dodatnih možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (da se prikažejo SQL stavki brez njihove uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključnega pomena za vzdrževanje sistema ***digna*** in zagotavlja, da sta shema baze podatkov in ostale komponente repozitorija posodobljene z najnovejšo različico programske opreme.

### Uporaba ukaza `encrypt`
  
Ukaz `encrypt` v ***digna*** CLI se uporablja za šifriranje gesla.
  
#### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Geslo, ki ga je treba šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla morate geslo podati kot argument.   
Na primer, za šifriranje gesla `mypassword123`, uporabite:
```bash
dignacli encrypt mypassword123
```
Ukaz izpiše šifrirano različico podanega gesla, ki jo je nato mogoče uporabiti v varnih kontekstih. Če argument gesla ni posredovan, bo CLI prikazal napako o manjkajočem argumentu.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` se uporablja za generiranje Fernet ključa, ki je ključnega pomena za varovanje gesel, shranjenih v ***digna*** repozitoriju.
  
#### Uporaba ukaza
```bash
dignacli generate-key
```
  
## Upravljanje podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` v ***digna*** CLI se uporablja za odstranjevanje profilov, napovedi in podatkov sistema prometnih luči za enega ali več podatkovnih virov znotraj določenega projekta. Ta ukaz je bistven za upravljanje življenjskega cikla podatkov in pomaga ohranjati urejeno in učinkovito podatkovno okolje z brisanjem zastarelih ali nepotrebnih podatkov.

#### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega naj se podatki odstranijo (obvezno). Uporaba ključno besedo all-projects v tem argumentu naroči ***digna***, naj iterira prek vseh obstoječih projektov in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas za odstranjevanje podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za odstranjevanje podatkov, v istih formatih kot FROM_DATE (obvezno).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omeji operacijo čiščenja na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtri za omejitev čiščenja na tabele, ki v imenu vsebujejo določeno podniz.
- `--timing`, `-tm`: Po zaključku prikaže čas trajanja postopka čiščenja.
- `--help`: Prikaže pomoč za ukaz clean-up in izstopi.
  
#### Primer
  
Za odstranitev podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranitev podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga pri upravljanju shrambe podatkov in zagotavlja, da repozitorij vsebuje le relevantne informacije.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` v ***digna*** CLI se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj zagotavlja hiter pregled razpoložljivih projektov v ***digna*** repozitoriju.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` v ***digna*** CLI se uporablja za prikaz seznama vseh razpoložljivih podatkovnih virov znotraj določenega projekta. Ta ukaz je koristen za razumevanje podatkovnih virov, razpoložljivih za analizo in upravljanje v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se izpisujejo podatkovni viri (obvezno).
  
#### Primer
  
Za izpis vseh podatkovnih virov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom omogoča pregled podatkovnih virov v projektu in pomaga pri navigaciji ter upravljanju podatkovnega prostora.

## Uporaba ukaza `inspect`

Ukaz `inspect` v ***digna*** CLI se uporablja za ustvarjanje profilov, napovedi in podatkov sistema prometnih luči za enega ali več podatkovnih virov v določenem projektu. Ta ukaz pomaga pri analiziranju in spremljanju podatkov v določenem obdobju.

#### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega naj se podatki pregledajo (obvezno). Uporaba ključno besedo all-projects v tem argumentu naroči ***digna***, naj iterira prek vseh obstoječih projektov in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas za pregled podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za pregled podatkov, v istih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji pregled na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtri za pregled samo tabel, ki v imenu vsebujejo določeno podniz.
- `--do-profile`: Sproži ponovno zbiranje profilov. Privzeto je do-profile.
- `--no-do-profile`: Prepreči ponovno zbiranje profilov.
- `--do-prediction`: Sproži ponovno izračunavanje napovedi. Privzeto je do-prediction.
- `--no-do-prediction`: Prepreči ponovno izračunavanje napovedi.
- `--do-alert-status`: Sproži ponovno izračunavanje statusov opozoril. Privzeto je do-alert-status.
- `--no-do-alert-status`: Prepreči ponovno izračunavanje statusov opozoril.
- `--iterative`: Sproži pregled obdobja z dnevnim iteriranjem. Privzeto je iterative.
- `--no-iterative`: Izvede pregled celotnega obdobja naenkrat.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil v primeru opozoril.
- `--timing`, `-tm`: Prikaže trajanje postopka pregleda po zaključku.
  
#### Primer
  
Za pregled podatkov v projektu `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za pregled samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje integritete podatkov in upravljanje sistemov opozoril znotraj določenega časovnega okvira projekta.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` v ***digna*** CLI se uporablja za poizvedbo o statusu sistema prometnih luči (Traffic Light System, TLS) za določeno tabelo v projektu na določen datum. Sistem prometnih luči nudi vpogled v zdravje in kakovost podatkov ter opozarja na morebitne težave, ki zahtevajo ukrepanje.
  
#### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se preverja TLS status (obvezno).
- **TABLE_NAME**: Določena tabela v projektu, za katero želite TLS status (obvezno).
- **DATE**: Datum, za katerega se preverja TLS status, običajno v formatu %Y-%m-%d (obvezno).
  
#### Primer
  
Za preverjanje TLS statusa za tabelo z imenom UserData v projektu ProjectA dne 1. julija 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov z jasnim in uporabnim poročilom o stanju, temelječim na vnaprej določenih kriterijih.

## Uporaba ukaza `inspect-async`

Ukaz `inspect-async` v ***digna*** CLI se uporablja za navodilo backendu, naj asinhrono izvede pregled za enega ali več podatkovnih virov za določen projekt. Če je project_name nastavljen na all-projects, bo pregled iteriral čez vse razpoložljive projekte in izvedel pregled. Vrne ID zahteve, ki ga je mogoče uporabiti za sledenje napredka pregleda.

#### Uporaba ukaza

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega naj se podatki pregledajo (obvezno). Uporaba ključno besedo all-projects v tem argumentu naroči ***digna***, naj iterira prek vseh obstoječih projektov in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas za pregled podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za pregled podatkov, v istih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji pregled na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtri za pregled samo tabel, ki v imenu vsebujejo določeno podniz.

  
#### Primer
  
Za pregled podatkov v projektu `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Uporaba ukaza `inspect-status`

Ukaz `inspect-status` v ***digna*** CLI se uporablja za preverjanje napredka asinhronega pregleda na podlagi ID zahteve.

#### Uporaba ukaza

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumenti
  
- **REQUEST_ID**: ID zahteve, ki ga vrača ukaz `inspect-async` 
  
#### Možnosti

- `--report_level`, `-rl`: Nastavi raven poročila: 'task' ali 'step' [privzeto: task]
  
#### Primer
  
Za preverjanje napredka pregleda z ID zahteve 12345 na podrobni ravni korakov:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Uporaba ukaza `export-ds`

Ukaz `export-ds` v ***digna*** CLI se uporablja za ustvarjanje izvoza podatkovnih virov iz ***digna*** repozitorija. Privzeto bodo izvaženi vsi podatkovni viri iz določenega projekta.

#### Uporaba ukaza
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, iz katerega bodo podatkovni viri izvoženi.

#### Možnosti

- `--table_name`, `-tn`: Izvozi določen podatkovni vir iz projekta.
- `--exportfile`, `-ef`: Določi ime datoteke za izvoz.
    
#### Primer
  
Za izvoz vseh podatkovnih virov iz projekta z imenom `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ta ukaz izvozi vse podatkovne vire iz `ProjectA` kot JSON dokument, ki ga je mogoče uvoziti v drug projekt ali ***digna*** repozitorij.


## Uporaba ukaza `import-ds`

Ukaz `import-ds` v ***digna*** CLI se uporablja za uvoz podatkovnih virov v ciljni projekt in ustvarjanje poročila o uvozu.

#### Uporaba ukaza
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bodo podatkovni viri uvoženi.
- **EXPORT_FILE**: Ime datoteke izvoza podatkovnih virov, ki se bo uvozila.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni navedeno, se poročilo izpiše v terminalu v tabelarni obliki).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za uvoz vseh podatkovnih virov iz izvoznega fajla `my_export.json` v `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po uvozu bo ta ukaz tudi prikazal poročilo o uvoženih in izpuščenih objektih. V `ProjectB` bodo uvoženi samo novi podatkovni viri. Če želite izvedeti, kateri objekti bi bili uvoženi in kateri izpuščeni, lahko uporabite ukaz `plan-import-ds`

## Uporaba ukaza `plan-import-ds`

Ukaz `plan-import-ds` v ***digna*** CLI se uporablja za načrtovanje uvoza podatkovnih virov v ciljni projekt in ustvarjanje poročila o uvozu (brez dejanskega uvoza).

#### Uporaba ukaza
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bi bili podatkovni viri uvoženi.
- **EXPORT_FILE**: Ime datoteke izvoza podatkovnih virov, ki bo analizirana pred uvozom.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni navedeno, se poročilo izpiše v terminalu v tabelarni obliki).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za preverjanje, kateri podatkovni viri bi bili uvoženi in kateri bi bili izpuščeni iz izvoznega fajla `my_export.json`, če bi jih uvozili v `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ta ukaz bo prikazal le načrt uvoza objektov, ki bodo uvoženi in izpuščeni.
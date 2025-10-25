---
title: digna CLI Referenca 2025.04 – Ukazi in primeri | digna Documentation
description: Popolna referenca za digna CLI različico 2025.04. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-repo-connection, upgrade-repo, inspect in še več.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Referenca 2025.04
**2025-04-01**

Ta stran vsebuje popolno dokumentacijo vseh ukazov, ki so na voljo v CLI orodju ***digna*** različice **2025.04**, z uporabo, možnostmi in primeri.

---

## Osnove CLI

---

## Uporaba možnosti `--help`

Možnost `--help` zagotavlja informacije o razpoložljivih ukazih in njihovem načinu uporabe. Obstajata dva osnovna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite `--help` takoj po ključni besedi `***digna***`.  
   ```bash
   dignacli --help

2. **Dobite pomoč za določen ukaz:**  
  
    Za podrobnejše informacije o določenem ukazu dodajte `--help` k temu ukazu.  
    Na primer, če želite pomoč za ukaz `add-user`, zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### izpis:
      
     - **Opis ukaza:** Pojasni, kaj ukaz naredi.  
     - **Skladnja:** Prikaže polno skladnjo, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Navede možnosti, specifične za ukaz, in njihove opise.  
     - **Primeri:** Poda primere, kako učinkovito zagnati ukaz.

  
## Uporaba ukaza `check-repo-connection`

Ukaz `check-repo-connection` v CLI orodju ***digna*** se uporablja za testiranje povezave in dostopa do okrepljenega ***digna*** repozitorija. Ta ukaz preveri, ali lahko CLI komunicira z repozitorijem.
      
#### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Ob uspešnem izvrševanju ukaz poleg potrditve povezave izpiše tudi informacije o repozitoriju: različico repozitorija, gostitelja (Host), bazo podatkov (Database) in shemo (Schema).  
  
Če povezava z repozitorijem ni uspešna, preverite nastavitve v datoteki config.toml.

## Uporaba ukaza `version`

Če želite preveriti nameščeno različico *dignacli*, uporabite možnost `--version`.  
  
#### Uporaba ukaza
```bash
dignacli --version
```
  
#### Primer izpisa
```bash
dignacli version 2025.04
```

## Uporaba možnosti za beleženje (log)

Privzeto je izpis ukazov ***digna*** na konzoli minimalen. Večina ukazov omogoča izpis dodatnih informacij; na voljo so naslednje možnosti:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
"verbose" in "debug" določata raven podrobnosti; možnost "logfile" pa preusmeri izpis v datoteko namesto na konzolo.

## Upravljanje uporabnikov

### Uporaba ukaza `add-user`
  
Ukaz `add-user` v CLI orodju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumenti

- **USER_NAME**: Uporabniško ime novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

#### Možnosti

- `--is_superuser`, `-su`: Označi novega uporabnika kot skrbnika (superuser).
- `--valid_until`, `-vu`: Določi datum veljavnosti računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni naveden, račun nima datuma poteka.

#### Primer

Za dodajanje uporabnika z uporabniškim imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Za dodajanje novega uporabnika z datuma poteka računa:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Uporaba ukaza `delete-user`
  
Ukaz `delete-user` odstrani obstoječega uporabnika iz sistema ***digna***.
  
#### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
##### Argumenti
- **USER_NAME**: Uporabniško ime uporabnika, ki bo izbrisan (obvezno).

#### Primer
```bash
dignacli delete-user jdoe
```
  
Ta ukaz odstrani uporabnika `jdoe` iz sistema ***digna***; prekine njegovo dostopno pravico in izbriše ustrezne podatke ter dovoljenja iz repozitorija.

### Uporaba ukaza `modify-user`

Ukaz `modify-user` v CLI orodju ***digna*** posodobi informacije obstoječega uporabnika.

#### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, ki ga želite posodobiti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuser; poviša privilegije. Ta preklop ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Določi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven neskončno.  
  
#### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in povišanje v superuserja:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Uporaba ukaza `modify-user-pwd`
  
Ukaz `modify-user-pwd` spremeni geslo obstoječega uporabnika v CLI orodju ***digna***.
  
#### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, katerega geslo se spreminja (obvezno).
- **USER_PWD**: Novo geslo (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Uporaba ukaza `list-users`

Ukaz `list-users` prikaže vse uporabnike, registrirane v sistemu ***digna***.

#### Uporaba ukaza

```bash
dignacli list-users
```

Ta ukaz se poveže z repozitorijem in izpiše seznam uporabnikov z ID-jem, uporabniškim imenom, polnim imenom, stanjem superuserja in žigi poteka.

## Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` v CLI orodju ***digna*** se uporablja za nadgradnjo ali inicializacijo ***digna*** repozitorija. Ta ukaz je potreben za uporabo posodobitev ali vzpostavitev repozitorija prvič.
  
#### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Ko je omogočeno, ukaz deluje v simulacijskem načinu; izpiše SQL stavke, ki bi jih izvedel, vendar jih dejansko ne izvede. Uporabno za predogled sprememb brez njihovega izvajanja.  

  
#### Primer
  
Za nadgradnjo ***digna*** repozitorija brez dodatnih možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (prikaže SQL stavke, ne izvede jih):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključnega pomena za vzdrževanje sistema ***digna***, saj zagotavlja, da so shema baze podatkov in drugi repozitorijski elementi usklajeni z najnovejšo različico programske opreme.

### Uporaba ukaza `encrypt`
  
Ukaz `encrypt` v CLI orodju ***digna*** šifrira geslo.
  
#### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Geslo, ki ga je treba šifrirati (obvezno).
  
#### Primer
  
Geslo morate podati kot argument za njegovo šifriranje.   
Na primer, za šifriranje gesla `mypassword123`:
```bash
dignacli encrypt mypassword123
```
Ukaz izpiše šifrirano obliko podanega gesla; to lahko nato uporabite v varnih kontekstih. Če geselni argument ni podan, bo CLI izpisal napako o manjkajočem argumentu.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` ustvari Fernet ključ; ta ključ je potreben za varno shranjevanje gesel v ***digna*** repozitoriju.
  
#### Uporaba ukaza
```bash
dignacli generate-key
```
  
## Upravljanje podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` v CLI orodju ***digna*** odstrani profile, napovedi (predictions) in podatke sistema za Trafik luči (traffic light system) za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga ohranjati urejeno in učinkovito podatkovno okolje z odstranjevanjem starih ali nepotrebnih podatkov.

#### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega bodo podatki odstranjeni (obvezno). Če je podana ključna beseda all-projects, bo ***digna*** iteriral skozi vse obstoječe projekte in uporabil ukaz za vsak izmed njih.
- **FROM_DATE**: Začetni datum in čas za brisanje podatkov. Sprejeti formati so %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za brisanje podatkov; sprejema iste formate kot FROM_DATE (obvezno).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omeji čiščenje na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Uporabi filter za omejevanje na tabele, katerih imena vsebujejo določeno podniz.
- `--timing`, `-tm`: Po zaključku prikaže trajanje čiščenja.
- `--help`: Prikaže pomoč za ukaz clean-up in izstopi.
  
#### Primer
  
Za odstranitev podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranitev podatkov samo iz tabele `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga upravljati porabo prostora za shranjevanje podatkov in zagotavlja, da v repozitoriju ostanejo samo relevantne informacije.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` prikaže seznam vseh obstoječih projektov v CLI orodju ***digna***.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je posebej uporaben za upravljavce in uporabnike, ki upravljajo več projektov; hitro prikaže pregled projektov, ki so na voljo v repozitoriju.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` prikaže vse razpoložljive podatkovne vire znotraj določenega projekta. Ta ukaz pomaga razumeti, katere podatkovne entitete so na voljo za analizo in upravljanje.

#### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, katerega podatkovni viri bodo izpisani (obvezno).
  
#### Primer
  
Za izpis vseh podatkovnih virov v projektu `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ukaz zagotovi pregled razpoložljivih virov v projektu, kar olajša učinkovitejše upravljanje podatkovnega okolja.


## Uporaba ukaza `inspect`

Ukaz `inspect` v CLI orodju ***digna*** ustvari profile, napovedi in podatke Trafik luči za enega ali več podatkovnih virov znotraj določenega projekta za navedeno obdobje. Ukaz pomaga pri analizi podatkov in spremljanju v določenem časovnem okviru.

#### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, katerega podatke želite pregledati (obvezno). Če je podana vrednost all-projects, bo ***digna*** iteriral skozi vse obstoječe projekte.
- **FROM_DATE**: Začetni datum in čas pregleda. Sprejeti formati: %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas pregleda; sprejema iste formate kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji pregled na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira pregled na tabele, katerih imena vsebujejo določen podniz.
- `--do-profile`: Sproži ponovno zbiranje profilov. Privzeto: do-profile.
- `--no-do-profile`: Onemogoči ponovno zbiranje profilov.
- `--do-prediction`: Sproži ponovno izračunavanje napovedi. Privzeto: do-prediction.
- `--no-do-prediction`: Onemogoči ponovno izračunavanje napovedi.
- `--do-alert-status`: Sproži ponovno izračunavanje stanja opozoril. Privzeto: do-alert-status.
- `--no-do-alert-status`: Onemogoči ponovno izračunavanje stanja opozoril.
- `--iterative`: Sproži pregled navedenega obdobja z dnevnim iteriranjem. Privzeto: iterative.
- `--no-iterative`: Izvede pregled navedenega obdobja naenkrat.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil ob opozorilih.
- `--timing`, `-tm`: Prikaže trajanje pregleda po zaključku.
  
#### Primer
  
Za pregled podatkov v projektu `ProjectA` med 1. januarjem 2024 in 31. januarjem 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za pregled samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za ustvarjanje posodobljenih profilov in napovedi, spremljanje integritete podatkov in upravljanje sistema opozoril v navedenem časovnem obdobju projekta.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` v CLI orodju ***digna*** preveri stanje sistema Trafik luči (TLS) za dano tabelo v projektu na določen datum. Trafik luči predstavljajo stanje zdravja in kakovosti podatkov; opozarjajo na težave, ki zahtevajo pozornost.
  
#### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se preverja TLS stanje (obvezno).
- **TABLE_NAME**: Ime tabele znotraj projekta, katere stanje TLS se preverja (obvezno).
- **DATE**: Datum, za katerega se preverja TLS stanje; običajno v formatu %Y-%m-%d (obvezno).
  
#### Primer
  
Za preverjanje TLS stanja tabele `UserData` v projektu `ProjectA` za datum 1. julij 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ukaz zagotovi jasne in uporabne poročilne podatke o kakovosti podatkov na podlagi vnaprej določenih meril, kar pomaga spremljati stanje kakovosti podatkov.

## Uporaba ukaza `inspect-async`

Ukaz `inspect-async` v CLI orodju ***digna*** zahteva, da backend asinkrono izvede pregled enega ali več podatkovnih virov za določen projekt. Če je parameter project_name nastavljen na all-projects, bo pregled iteriral skozi vse projekte. Ukaz vrne identifikator zahteve (request id), s katerim lahko spremljate napredek pregleda.

#### Uporaba ukaza

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, ki ga želite pregledati (obvezno). Če uporabite all-projects, bo ***digna*** iteriral skozi vse projekte.
- **FROM_DATE**: Začetni datum in čas pregleda. Sprejeti formati: %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas pregleda; sprejema iste formate kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji asinkroni pregled na določeno tabelo v projektu.
- `--table-filter`, `-tf`: Filtrira pregled na tabele, katerih imena vsebujejo določen podniz.

  
#### Primer
  
Za asinkroni pregled podatkov v projektu `ProjectA` med 1. januarjem 2024 in 31. januarjem 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Uporaba ukaza `inspect-status`

Ukaz `inspect-status` preveri napredek asinkronega pregleda, ki je bil sprožen z `inspect-async`, glede na identifikator zahteve (request ID).

#### Uporaba ukaza

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumenti
  
- **REQUEST_ID**: Identifikator zahteve, ki ga je vrnil ukaz `inspect-async`.
  
#### Možnosti

- `--report_level`, `-rl`: Nastavi raven poročila: 'task' ali 'step' [privzeto: task]
  
#### Primer
  
Za preverjanje napredka pregleda z ID-jem 12345 na podrobni ravni korakov (step):
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Uporaba ukaza `export-ds`

Ukaz `export-ds` v CLI orodju ***digna*** ustvari izvoz podatkovnih virov iz repozitorija. Privzeto izvozi vse podatkovne vire v navedenem projektu.

#### Uporaba ukaza
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, iz katerega se bodo izvozi izvedli.

#### Možnosti

- `--table_name`, `-tn`: Izvozi določen podatkovni vir iz projekta.
- `--exportfile`, `-ef`: Določi ime datoteke za izvoz.
    
#### Primer
  
Za izvoz vseh podatkovnih virov iz projekta `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ukaz ustvari JSON dokument, ki vsebuje vse podatkovne vire iz `ProjectA`, kar omogoča prenos v drug projekt ali v drug ***digna*** repozitorij.

## Uporaba ukaza `import-ds`

Ukaz `import-ds` v CLI orodju ***digna*** uvozi podatkovne vire iz izvozne datoteke v ciljni projekt in ustvari poročilo o uvozu.

#### Uporaba ukaza
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bodo podatkovni viri uvoženi.
- **EXPORT_FILE**: Ime izvozne datoteke, ki vsebuje podatkovne vire za uvoz.

#### Možnosti

- `--output-file`, `-o`: Datoteka, v katero bo shranjeno poročilo o uvozu (če ni določeno, se poročilo izpiše v terminalu kot tabela).
- `--output-format`, `-f`: Format poročila o uvozu (json, csv).
    
#### Primer
  
Za uvoz vseh podatkovnih virov iz datoteke `my_export.json` v projekt `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po uvozu ukaz prikaže tudi poročilo o uvoženih in izpuščenih objektih. V projekt `ProjectB` se uvozijo samo novi podatkovni viri. Za ogled, kateri objekti bi bili uvoženi in kateri izpuščeni, uporabite ukaz `plan-import-ds`.

## Uporaba ukaza `plan-import-ds`

Ukaz `plan-import-ds` v CLI orodju ***digna*** analizira, kateri objekti bodo uvoženi in kateri izpuščeni, preden dejansko izvedete uvoz podatkovnih virov v ciljni projekt.

#### Uporaba ukaza
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bi bili podatkovni viri uvoženi.
- **EXPORT_FILE**: Ime izvozne datoteke, ki bo analizirana pred uvozom.

#### Možnosti

- `--output-file`, `-o`: Datoteka, v katero bo shranjeno poročilo o načrtu uvoza (če ni določeno, se poročilo izpiše v terminalu kot tabela).
- `--output-format`, `-f`: Format poročila o načrtu uvoza (json, csv).
    
#### Primer
  
Za pregled, kateri podatkovni viri iz datoteke `my_export.json` bi bili uvoženi ali izpuščeni v projektu `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ta ukaz prikaže le načrt uvoza in izpuščanja objektov, brez dejanskega uvoza.
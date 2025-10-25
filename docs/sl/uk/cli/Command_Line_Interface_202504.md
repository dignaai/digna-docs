---
title: digna CLI Reference 2025.04 – Ukazi in primeri | digna Documentation
description: Celoten priročnik za digna CLI izdajo 2025.04. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-repo-connection, upgrade-repo, inspect in drugimi.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Na tej strani je dokumentiran celoten nabor ukazov, razpoložljivih v CLI orodju ***digna*** za izdajo **2025.04**, vključno s primeri uporabe in možnostmi.

---

## Osnove CLI

---

## Uporaba možnosti `--help`

Možnost `--help` prikaže informacije o razpoložljivih ukazih in njihovi uporabi. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help takoj za ukazom ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Pridobitev pomoči za določene ukaze:**  
  
    Za podrobne informacije o določenem ukazu dodajte `--help` k temu ukazu.  
    Na primer, za pomoč pri ukazu `add-user` izvedite:
     ```bash
     dignacli add-user --help
     ```

     ### Izhod:
      
     - **Opis ukaza:** Nudi podroben opis, kaj ukaz opravi.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Seznam možnosti, specifičnih za ukaz, z njihovimi pojasnili.  
     - **Primeri:** Prikazuje primere, kako učinkovito uporabiti ukaz.

  
## Uporaba ukaza `check-repo-connection`

Ukaz `check-repo-connection` je pripomoček v CLI orodju ***digna***, namenjen preverjanju dostopnosti in povezave z navedenim repozitorijem ***digna***. Ta ukaz zagotavlja, da lahko CLI komunicira z repozitorijem.
      
#### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Če je izvedba uspešna, bo ukaz izpisal potrdilo o povezavi skupaj z informacijami o repozitoriju: različico repozitorija, gostitelja, bazo podatkov in shemo.  
  
Če povezava do repozitorija ne uspe, preverite datoteko config.toml glede pravilnih nastavitev.

## Uporaba ukaza `--version`

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
  
Privzeto je izpis v konzoli ukazov ***digna*** minimalističen. Večina ukazov omogoča izpis dodatnih informacij z naslednjimi možnostmi:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” in “debug” določata stopnjo podrobnosti, medtem ko parameter “logfile” omogoča preusmeritev izpisa v datoteko namesto v konzolo.

## Upravljanje uporabnikov

### Uporaba ukaza `add-user`
  
Ukaz `add-user` v CLI orodju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumenti

- **USER_NAME**: Ime uporabnika za nov račun (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

#### Možnosti

- `--is_superuser`, `-su`: Označi novega uporabnika kot skrbnika (superuser).
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni navedeno, račun nima roka veljavnosti.

#### Primer

Za dodajanje novega uporabnika z uporabniškim imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Za dodajanje novega uporabnika in nastavitev datuma poteka računa:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Uporaba ukaza `delete-user`
  
Ukaz `delete-user` v CLI orodju ***digna*** se uporablja za odstranitev obstoječega uporabnika iz sistema ***digna***.
  
#### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
##### Argumenti
- **USER_NAME**: Ime uporabnika, ki ga je treba izbrisati (obvezno). To je edini zahtevan argument ukaza.

#### Primer
```bash
dignacli delete-user jdoe
```
  
Izvedba tega ukaza bo izbrisala uporabnika `jdoe` iz sistema ***digna***, preklicala njegove pravice in odstranila povezane podatke in pravice iz repozitorija.

### Uporaba ukaza `modify-user`

Ukaz `modify-user` v CLI orodju ***digna*** se uporablja za posodobitev podatkov obstoječega uporabnika v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumenti
  
- **USER_NAME**: Ime uporabnika, ki ga je treba spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuserja, kar mu da povišane privilegije. Ta zastavica ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni navedeno, račun ostane aktiven brez datuma poteka.  
  
#### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in za dodelitev superuser pravic:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Uporaba ukaza `modify-user-pwd`
  
Ukaz `modify-user-pwd` v CLI orodju ***digna*** se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna***.
  
#### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumenti
  
- **USER_NAME**: Ime uporabnika, katerega geslo je treba spremeniti (obvezno).
- **USER_PWD**: Novo geslo za uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Uporaba ukaza `list-users`

Ukaz `list-users` v CLI orodju ***digna*** prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

#### Uporaba ukaza

```bash
dignacli list-users
```

Izvedba tega ukaza v CLI orodju ***digna*** se poveže z repozitorijem ***digna*** in izpiše vse uporabnike, prikazuje njihov ID, uporabniško ime, polno ime, status superuserja ter časovne žige poteka.

## Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` v CLI orodju ***digna*** se uporablja za posodobitev ali inicializacijo repozitorija ***digna***. Ta ukaz je potreben za uporabo posodobitev ali za prvotno nastavitev infrastrukture repozitorija.
  
#### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Če je omogočeno, ukaz teče v simulacijskem načinu in izpiše SQL ukaze, ki bi bili izvedeni, vendar jih dejansko ne izvede. To je koristno za predogled sprememb brez vpliva na repozitorij.  

  
#### Primer
  
Za posodobitev repozitorija ***digna*** lahko zaženete ukaz brez možnosti:
  
```bash
dignacli upgrade-repo
```  
Za izvedbo posodobitve v simulacijskem načinu (da vidite SQL ukaze brez njihove izvedbe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je kritičen za vzdrževanje sistema ***digna***, saj zagotavlja usklajenost sheme baze podatkov in drugih komponent repozitorija z zadnjo različico programske opreme.

### Uporaba ukaza `encrypt`
  
Ukaz `encrypt` v CLI orodju ***digna*** se uporablja za šifriranje gesla.
  
#### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Geslo, ki ga je treba šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla ga je treba posredovati kot argument.   
Na primer, za šifriranje gesla `mypassword123` uporabite:
```bash
dignacli encrypt mypassword123
```
Ta ukaz bo izpisal šifrirano različico podanega gesla, ki jo nato lahko uporabite v varnih kontekstih. Če argument gesla ni naveden, bo CLI izpisal napako o manjkajočem argumentu.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` se uporablja za generiranje Fernet key, ki je potreben za zaščito gesel, shranjenih v repozitoriju ***digna***.
  
#### Uporaba ukaza
```bash
dignacli generate-key
```
  
## Upravljanje podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` v CLI orodju ***digna*** je namenjen brisanju profilov, napovedi in podatkov sistema Traffic Light System za enega ali več virov podatkov znotraj navedenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov, saj pomaga ohranjati urejeno in učinkovito podatkovno okolje z odstranjevanjem zastarelih ali nepotrebnih podatkov.

#### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega je treba izbrisati podatke (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira skozi vse obstoječe projekte in uporabi ukaz.
- **FROM_DATE**: Začetni datum in čas za brisanje podatkov. Dovoljeni formati: %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za brisanje podatkov v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omeji čiščenje na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira čiščenje na tabele, ki vsebujejo dano podniz v svojih imenih.
- `--timing`, `-tm`: Po končanem postopku čiščenja prikaže trajanje procesa.
- `--help`: Prikaže pomoč za ukaz clean-up in izstopi.
  
#### Primer
  
Za brisanje podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za brisanje podatkov le iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga upravljati shranjevanje podatkov in zagotavlja, da v repozitoriju ostanejo samo relevantne informacije.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj hitro prikaže razpoložljive projekte v repozitoriju ***digna***.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih virov podatkov v navedenem projektu. Ta ukaz je koristen za razumevanje razpoložljivih podatkov za analizo in upravljanje v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se naštetejo viri podatkov (obvezno).
  
#### Primer
  
Za navajanje vseh virov podatkov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled virov podatkov, prisotnih v projektu, in jim pomaga bolje upravljati podatkovno okolje.


## Uporaba ukaza `inspect`

Ukaz `inspect` v CLI orodju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema Traffic Light System za enega ali več virov podatkov znotraj navedenega projekta. Ta ukaz pomaga analizirati in spremljati podatke za določeno obdobje.

#### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega je treba izvesti inšpekcijo podatkov (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira skozi vse obstoječe projekte in uporabi ukaz.
- **FROM_DATE**: Začetni datum in čas za inšpekcijo podatkov. Dovoljeni formati: %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za inšpekcijo podatkov v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira inšpekcijo le na tabele, ki vsebujejo določen podniz v svojih imenih.
- `--do-profile`: Zažene zbiranje profilov. Privzeto — do-profile.
- `--no-do-profile`: Onemogoči zbiranje profilov.
- `--do-prediction`: Zažene ponovno izračunavanje napovedi. Privzeto — do-prediction.
- `--no-do-prediction`: Onemogoči ponovno izračunavanje napovedi.
- `--do-alert-status`: Zažene ponovno izračunavanje stanj opozoril. Privzeto — do-alert-status.
- `--no-do-alert-status`: Onemogoči ponovno izračunavanje stanj opozoril.
- `--iterative`: Izvede inšpekcijo obdobja z dnevnimi iteracijami. Privzeto — iterative.
- `--no-iterative`: Izvede inšpekcijo celotnega obdobja naenkrat.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil v primeru opozoril.
- `--timing`, `-tm`: Po končani inšpekciji prikaže trajanje procesa.
  
#### Primer
  
Za inšpekcijo podatkov za projekt `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za inšpekcijo samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje ažurnih profilov in napovedi, spremljanje integritete podatkov in upravljanje sistema obveščanja znotraj navedenega obdobja projekta.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` v CLI orodju ***digna*** se uporablja za poizvedbo stanja Traffic Light System (TLS) za določeno tabelo v projektu na naveden datum. Traffic Light System zagotavlja vpoglede v stanje in kakovost podatkov, označuje težave ali opozorila, ki lahko potrebujejo pozornost.
  
#### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se poizveduje stanje TLS (obvezno).
- **TABLE_NAME**: Določena tabela v projektu, za katero je potreben TLS status (obvezno).
- **DATE**: Datum, za katerega se poizveduje TLS status, običajno v formatu %Y-%m-%d (obvezno).
  
#### Primer
  
Za preverjanje TLS stanja za tabelo z imenom UserData v projektu ProjectA na 1. julij 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov, saj zagotavlja jasna in uporabna poročila o stanju na podlagi vnaprej določenih kriterijev.

## Uporaba ukaza `inspect-async`

Ukaz `inspect-async` v CLI orodju ***digna*** se uporablja za naročilo, da backend izvede inšpekcijo asinhrono za enega ali več virov podatkov znotraj navedenega projekta. Če je project_name nastavljen na all-projects, bo inšpekcija izvedena za vse razpoložljive projekte. Ukaz vrne request id, ki ga lahko uporabite za sledenje napredku inšpekcije.

#### Uporaba ukaza

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se izvaja inšpekcija podatkov (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira skozi vse obstoječe projekte in uporabi ukaz.
- **FROM_DATE**: Začetni datum in čas za inšpekcijo podatkov. Dovoljeni formati: %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za inšpekcijo podatkov v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira inšpekcijo le na tabele, ki vsebujejo določen podniz v svojih imenih.

  
#### Primer
  
Za zagon inšpekcije podatkov za projekt `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Uporaba ukaza `inspect-status`

Ukaz `inspect-status` v CLI orodju ***digna*** se uporablja za preverjanje napredka asinhrone inšpekcije po ID-ju zahteve.

#### Uporaba ukaza

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumenti
  
- **REQUEST_ID**: ID zahteve, ki ga je vrnil ukaz `inspect-async` 
  
#### Možnosti

- `--report_level`, `-rl`: Nastavi raven poročila: 'task' ali 'step' [privzeto: task]
  
#### Primer
  
Za preverjanje napredka inšpekcije z ID-jem zahteve 12345 na podrobni ravni korakov:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Uporaba ukaza `export-ds`

Ukaz `export-ds` v CLI orodju ***digna*** se uporablja za ustvarjanje izvoza virov podatkov iz repozitorija ***digna***. Privzeto se izvozi vse vire podatkov iz navedenega projekta.

#### Uporaba ukaza
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, iz katerega bodo izvoženi viri podatkov.

#### Možnosti

- `--table_name`, `-tn`: Izvozi določen vir podatkov iz projekta.
- `--exportfile`, `-ef`: Določi ime datoteke za izvoz.
    
#### Primer
  
Za izvoz vseh virov podatkov iz projekta z imenom `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ta ukaz izvozi vse vire podatkov iz `ProjectA` kot JSON dokument, ki ga je mogoče uvoziti v drug projekt ali repozitorij ***digna***.


## Uporaba ukaza `import-ds`

Ukaz `import-ds` v CLI orodju ***digna*** se uporablja za uvoz virov podatkov v ciljni projekt in za ustvarjanje poročila o uvozu.

#### Uporaba ukaza
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bodo uvoženi viri podatkov.
- **EXPORT_FILE**: Ime datoteke izvoza virov podatkov za uvoz.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni navedeno, izpiše v terminal v tabelarični obliki).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za uvoz vseh virov podatkov iz izvoznega datoteke `my_export.json` v `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po uvozu bo ta ukaz prikazal tudi poročilo o uvoženih in izpuščenih objektih. V `ProjectB` bodo uvoženi samo novi viri podatkov. Če želite vedeti, kateri objekti bodo uvoženi in kateri izpuščeni, lahko uporabite ukaz `plan-import-ds`.

## Uporaba ukaza `plan-import-ds`

Ukaz `plan-import-ds` v CLI orodju ***digna*** se uporablja za analizo izvoza virov podatkov pred uvozom in ustvari načrt uvoza z ustreznim poročilom.

#### Uporaba ukaza
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega se načrtuje uvoz objektov.
- **EXPORT_FILE**: Ime izvoznega fajla virov podatkov, ki se bo analiziral pred uvozom.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o načrtu uvoza (če ni navedeno, izpiše v terminal v tabelarični obliki).
- `--output-format`, `-f`: Format za shranjevanje poročila o načrtu uvoza (json, csv).
    
#### Primer
  
Za preverjanje, kateri viri podatkov bodo uvoženi in kateri izpuščeni iz izvoznega fajla `my_export.json` pri uvozu v `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ta ukaz bo prikazal samo načrt uvoza objektov, ki bodo uvoženi in izpuščeni.
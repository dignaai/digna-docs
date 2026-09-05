---
title: digna CLI Reference 2026.01 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2026.01 Learn how to manage users, repositories, and data with commands such as add-user, check-config, check-repo-connection, inspect, inspect-async, and more.
image: /assets/logo_square.png
---

# digna CLI Reference 2026.01
**2026-01-15**

Na tej strani je dokumentiran celoten nabor ukazov, ki so na voljo v izdaji ***digna*** CLI **2026.01**, vključno z uporabnimi primeri in možnostmi.

---

## Osnove CLI

---

### help
Možnost `--help` zagotavlja informacije o razpoložljivih ukazih in njihovem načinu uporabe. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite –help takoj za ključnimi besedami ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Pridobitev pomoči za določen ukaz:**  
  
    Za podrobne informacije o določenem ukazu dodajte `--help` temu ukazu.
    Na primer, za pomoč pri ukazu `add-user` zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Opis ukaza:** Ponuja podroben opis funkcionalnosti ukaza.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Našteje možnosti, specifične za ukaz, skupaj z njihovimi pojasnili.  
     - **Primeri:** Ponuja primere, kako učinkovito izvesti ukaz.  

### check-config

Ukaz check-config je orodje v okviru ***digna*** CLI, namenjeno preverjanju konfiguracije ***digna***. Ta ukaz zagotavlja, da komponente ***digna*** najdejo potrebne konfiguracijske elemente v config.toml.

#### Možnosti

- `--configpath`, `-cp`: Datoteka ali imenik, ki vsebuje konfiguracijo. Če ni določeno, bo uporabljen ../config.toml.
      
#### Uporaba ukaza
```bash
dignacli check-config
```

Ob uspešni izvedbi ukaz izpiše potrdilo o popolnosti konfiguracije.  
  
Če se konfiguracija zdi nepopolna, bodo navedeni manjkajoči konfiguracijski elementi.

  
### check-repo-connection

Ukaz check-repo-connection je orodje v okviru ***digna*** CLI, namenjeno preverjanju povezljivosti in dostopa do določenega ***digna*** repozitorija. Ta ukaz zagotavlja, da se CLI lahko poveže in komunicira z repozitorijem.
      
#### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Ob uspešni izvedbi ukaz izpiše potrdilo o povezavi skupaj s podrobnostmi o repozitoriju: različico repozitorija, gostitelja, podatkovno bazo in shemo.  
  
Če povezava z repozitorijem ni uspešna, preverite datoteko config.toml za pravilne nastavitve konfiguracije.


### version

Za preverjanje nameščene različice *dignacli* uporabite možnost --version.  
  
#### Uporaba ukaza
```bash
dignacli --version
```
  
#### Primer izhoda
```bash
dignacli version 2026.01
```

### opcije beleženja (logging options)
  
Privzeto je izhod v konzoli za ukaze ***digna*** zasnovan minimalistično. Večina ukazov ponuja možnost prikaza dodatnih informacij z uporabo naslednjih možnosti:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” in “debug” določata raven podrobnosti, medtem ko stikalo “logfile” omogoča preusmeritev izhoda v datoteko namesto v konzolo.

## Upravljanje uporabnikov

### add-user
  
Ukaz add-user v okviru ***digna*** CLI se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenti

- **USER_NAME**: Uporniško ime za novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

#### Možnosti

- `--is_superuser`, `-su`: Preklop za dodelitev novega uporabnika kot administratorja.
- `--valid_until`, `-vu`: Nastavi datum poteka uporabniškega računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni nastavljen, račun nima datuma poteka.

#### Primer

Za dodajanje novega uporabnika z uporabniškim imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Za dodajanje novega uporabnika in nastavitev datuma poteka računa:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Ukaz `delete-user` v okviru ***digna*** CLI se uporablja za odstranitev obstoječega uporabnika iz sistema ***digna***.
  
#### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenti
- **USER_NAME**: Uporniško ime uporabnika, ki naj bo izbrisan (obvezno). To je edini zahtevan argument ukaza.

#### Primer
```bash
dignacli delete-user jdoe
```
  
Izvedba tega ukaza bo odstranila uporabnika `jdoe` iz sistema ***digna***, preklicala njihov dostop in izbrisala ustrezne podatke ter dovoljenja iz repozitorija.

### modify-user

Ukaz `modify-user` v okviru ***digna*** CLI se uporablja za posodobitev podatkov obstoječega uporabnika v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, ki ga želite spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuserja, s čimer dobi povišane privilegije. Ta preklop ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka uporabniškega računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven nedoločen čas.  
  
#### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in nastavitev uporabnika kot superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Ukaz `modify-user-pwd` v okviru ***digna*** CLI se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna***.
  
#### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, katerega geslo želite spremeniti (obvezno).
- **USER_PWD**: Novo geslo za uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Ukaz `list-users` v okviru ***digna*** CLI prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

#### Uporaba ukaza

```bash
dignacli list-users
```

Izvedba tega ukaza se bo poveza la na ***digna*** repozitorij in izpisala vse uporabnike, prikazujoč njihov ID, uporabniško ime, polno ime, status superuserja in časovne žige poteka.

## Upravljanje repozitorija

### upgrade-repo
  
Ukaz `upgrade-repo` v okviru ***digna*** CLI se uporablja za nadgradnjo ali inicializacijo ***digna*** repozitorija. Ta ukaz je ključen za uporabo posodobitev ali za začetno nastavitev repozitorija.
  
#### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Če je omogočeno, ukaz zažene v načinu simulacije, ki izpiše SQL izjave, ki bi bile izvršene, vendar jih dejansko ne izvede. To je uporabno za predogled sprememb brez kakršnih koli modifikacij repozitorija.  

  
#### Primer
  
Za nadgradnjo ***digna*** repozitorija lahko zaženete ukaz brez možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v načinu simulacije (za ogled SQL izjav brez njihove uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključnega pomena za vzdrževanje sistema ***digna***, saj zagotavlja, da je shema podatkovne baze in drugi repozitorijski elementi posodobljeni z najnovejšo različico programske opreme.

### encrypt
  
Ukaz `encrypt` v okviru ***digna*** CLI se uporablja za šifriranje gesla.
  
#### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Geslo, ki ga je treba šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla morate geslo posredovati kot argument.   
Na primer, za šifriranje gesla `mypassword123` uporabite:
```bash
dignacli encrypt mypassword123
```
Ukaz izpiše šifrirano različico danega gesla, ki jo lahko nato uporabite v varnih kontekstih. Če argument gesla ni podan, bo CLI izpisal napako o manjkajočem argumentu.

### generate-key
  
Ukaz `generate-key` se uporablja za generiranje Fernet ključa, ki je potreben za varno shranjevanje gesel v ***digna*** repozitoriju.
  
#### Uporaba ukaza
```bash
dignacli generate-key
```
  
## Upravljanje podatkov

### clean-up

Ukaz `clean-up` v okviru ***digna*** CLI se uporablja za odstranjevanje profilov, napovedi in podatkov sistema prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz je bistven za upravljanje življenjskega cikla podatkov in pomaga ohranjati urejeno in učinkovito podatkovno okolje z odstranjevanjem zastarelih ali nepotrebnih podatkov.

#### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega se bodo podatki odstranjevali (obvezno). Uporaba ključen besede all-projects v tem argumentu ukaže ***digna***, naj iterira skozi vse obstoječe projekte in izvede ta ukaz.
- **FROM_DATE**: Začetni datum in čas za odstranitev podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za odstranitev podatkov, v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omeji operacijo clean-up na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtri za omejitev čiščenja na tabele, katerih imena vsebujejo določeno podniz.
- `--timing`, `-tm`: Prikaže trajanje časa izvedbe procesa čiščenja po zaključku.
- `--help`: Prikaže pomoč za ukaz clean-up in izstopi.
  
#### Primer
  
Za odstranjevanje podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranjevanje podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga pri upravljanju shranjevanja podatkov in zagotavlja, da repozitorij vsebuje le relevantne informacije.

### remove-orphans
  
Ukaz `remove-orphans` v okviru ***digna*** CLI se uporablja za vzdrževanje v repozitoriju ***digna***.  
Ko uporabnik izbriše projekte ali vire podatkov, profili in napovedi pogosto ostanejo v repozitoriju. S tem ukazom bodo taki osamljeni (orphaned) vnosi odstranjeni iz repozitorija.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

### list-projects
  
Ukaz `list-projects` v okviru ***digna*** CLI se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za administratorje in uporabnike, ki upravljajo več projektov, saj nudi hiter pregled razpoložljivih projektov v ***digna*** repozitoriju.

### list-ds

Ukaz `list-ds` v okviru ***digna*** CLI se uporablja za prikaz seznama vseh razpoložljivih virov podatkov znotraj določenega projekta. Ta ukaz je koristen za razumevanje podatkovnih sredstev, ki so na voljo za analizo in upravljanje v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se navajajo viri podatkov (obvezno).
  
#### Primer
  
Za prikaz vseh virov podatkov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled virov podatkov v projektu in jim pomaga učinkoviteje krmariti ter upravljati podatkovno okolje.


### inspect

Ukaz `inspect` v okviru ***digna*** CLI se uporablja za ustvarjanje profilov, napovedi in podatkov sistema prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz pomaga pri analizi in nadzoru podatkov v določenem obdobju. Po zaključku pregleda se vrne vrednost izračunanega sistema prometnih luči:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, ki ga je treba pregledati (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira skozi vse obstoječe projekte in izvede ta ukaz.
- **FROM_DATE**: Začetni datum in čas za pregled podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za pregled podatkov, v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji pregled na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtri za pregled samo tabel, katerih imena vsebujejo določeno podniz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil v primeru alarmov.
- `--bypass-backend`, `-bb`: Zaobidi backend in zaženi pregled neposredno iz CLI (samo za testne namene!).

  
#### Primer
  
Za pregled podatkov v projektu `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za pregled samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje celovitosti podatkov ter upravljanje sistema opozoril znotraj določenega časovnega okvira projekta.

### inspect-async

Ukaz `inspect-async` v okviru ***digna*** CLI se uporablja za ustvarjanje profilov, napovedi in podatkov sistema prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem obdobju. V nasprotju z ukazom `inspect` ta ne čaka na zaključek pregleda.
Namesto tega vrne ID zahteve za poslan asinkroni zahtevek pregleda. Za poizvedbo poteka pregleda uporabite ukaz `inspect-status`.

#### Uporaba ukaza

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, ki ga je treba pregledati (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira skozi vse obstoječe projekte in izvede ta ukaz.
- **FROM_DATE**: Začetni datum in čas za pregled podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za pregled podatkov, v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji pregled na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtri za pregled samo tabel, katerih imena vsebujejo določeno podniz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil v primeru alarmov.

  
#### Primer
  
Za asinkroni pregled podatkov v projektu `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Ukaz `inspect-status` v okviru ***digna*** CLI se uporablja za preverjanje poteka asinkronega pregleda na podlagi ID zahteve.

#### Uporaba ukaza

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenti
  
- **REQUEST_ID**: ID zahteve, ki ga vrne ukaz `inspect-async` 
  
#### Primer
  
Za preverjanje poteka pregleda z ID zahteve 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Ukaz `inspect-cancel` v okviru ***digna*** CLI se uporablja za preklicovanje pregledov na podlagi ID zahteve ali za preklic vseh trenutnih zahtev.

#### Uporaba ukaza

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenti
  
- **REQUEST_ID**: ID zahteve, ki ga vrne ukaz `inspect-async` 
  
#### Primer
  
Za preklic pregleda z ID zahteve 12345:
  
```bash
dignacli inspect-cancel 12345
```

Za preklic vseh zahtev, ki so trenutno v teku ali čakajo:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Ukaz `export-ds` v okviru ***digna*** CLI se uporablja za ustvarjanje izvoza virov podatkov iz ***digna*** repozitorija. Privzeto bodo izvoženi vsi viri podatkov iz danega projekta.

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
  
Ta ukaz izvozi vse vire podatkov iz `ProjectA` kot JSON dokument, ki ga je mogoče uvoziti v drug projekt ali ***digna*** repozitorij.


### import-ds

Ukaz `import-ds` v okviru ***digna*** CLI se uporablja za uvoz virov podatkov v ciljni projekt in ustvarjanje poročila o uvozu.

#### Uporaba ukaza
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bodo vneseni viri podatkov.
- **EXPORT_FILE**: Ime datoteke izvoza virov podatkov, ki se bo uvozila.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni določeno, se poročilo izpiše v terminal v tabelarni obliki).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za uvoz vseh virov podatkov iz izvozne datoteke `my_export.json` v `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po uvozu bo ta ukaz prikazal tudi poročilo uvoženih in izpuščenih objektov. V `ProjectB` bodo uvoženi le novi viri podatkov. Če želite ugotoviti, kateri objekti bi bili uvoženi in kateri preskočeni, lahko uporabite ukaz `plan-import-ds`

### plan-import-ds

Ukaz `plan-import-ds` v okviru ***digna*** CLI se uporablja za analizo izvoza virov podatkov in pripravo poročila, kateri objekti bi bili uvoženi in kateri preskočeni, brez dejanskega uvoza.

#### Uporaba ukaza
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bi bili viri podatkov uvoženi.
- **EXPORT_FILE**: Ime datoteke izvoza virov podatkov, ki bo analizirana pred uvozom.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni določeno, se poročilo izpiše v terminal v tabelarni obliki).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za preverjanje, kateri viri podatkov bi bili uvoženi in kateri bi bili preskočeni iz izvozne datoteke `my_export.json` pri uvozu v `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ta ukaz bo prikazal samo načrt uvoza objektov, ki bi bili uvoženi in preskočeni.
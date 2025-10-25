---
title: Referenca digna CLI 2025.09 – Ukazi in primeri | digna Dokumentacija
description: Popolna referenca za izdajo digna CLI 2025.09. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-config, check-repo-connection, inspect, inspect-async in več.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# digna CLI Referenca 2025.09
**2025-09-29**

Ta stran dokumentira celoten nabor ukazov, ki so na voljo v izdaji ***digna*** CLI **2025.09**, vključno z vzorčnimi primeri uporabe in možnostmi.

---

## Osnove CLI

---

### help
Možnost `--help` zagotavlja informacije o razpoložljivih ukazih in o tem, kako jih uporabljati. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaži splošno pomoč:**
   
    Uporabite --help takoj po ključni besedi ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Pridobi pomoč za določen ukaz:**  
  
    Za podrobne informacije o določenem ukazu dodajte `--help` za tem ukazom.  
    Na primer, za pomoč pri ukazu `add-user`, zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### Izhod:
      
     - **Opis ukaza:** Podrobno pojasni, kaj ukaz naredi.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z obveznimi in neobveznimi argumenti.  
     - **Možnosti:** Našteje možnosti, specifične za ukaz, skupaj z razlagami.  
     - **Primeri:** Prikazuje primere učinkovite uporabe ukaza.

### check-config

Ukaz check-config je orodje v ***digna*** CLI, namenjeno preverjanju konfiguracije ***digna***. Ta ukaz zagotovi, da komponente ***digna*** najdejo potrebne konfiguracijske elemente v config.toml.

#### Možnosti

- `--configpath`, `-cp`: Datoteka ali imenik, ki vsebuje konfiguracijo. Če je izpuščeno, se uporabi ../config.toml.
      
#### Primer ukaza
```bash
dignacli check-config
```

Ob uspešnem zagonu ukaz potrdi, da je konfiguracija popolna.  
  
Če konfiguracija ni popolna, bodo izpisani manjkajoči konfiguracijski elementi.

  
### check-repo-connection

Ukaz check-repo-connection je orodje v ***digna*** CLI, namenjeno testiranju povezave in dostopa do določenega ***digna*** repozitorija. Ta ukaz zagotavlja, da se CLI lahko poveže z repozitorijem.
      
#### Primer ukaza
```bash
dignacli check-repo-connection
```

Ob uspešnem zagonu ukaz izpiše potrditev o povezavi skupaj s podrobnostmi o repozitoriju: različica repozitorija, gostitelj, baza podatkov in shema.  
  
Če povezava do repozitorija ne uspe, preverite datoteko config.toml za pravilne konfiguracijske nastavitve.


### version

Za preverjanje nameščene različice *dignacli* uporabite možnost --version.  
  
#### Primer ukaza
```bash
dignacli --version
```
  
#### Primer izhoda
```bash
dignacli version 2025.09
```

### možnosti dnevnika (logging)
  
Privzeto so izpisi ukazov ***digna*** na konzolo minimalni. Večina ukazov omogoča dodatne informacije z naslednjimi možnostmi:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” in “debug” določata raven podrobnosti, medtem ko preklop “logfile” omogoča preusmeritev izpisa v datoteko namesto v konzolo.

## Upravljanje uporabnikov

### add-user
  
Ukaz add-user v ***digna*** CLI se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Primer ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenti

- **USER_NAME**: Uporabniško ime novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

#### Možnosti

- `--is_superuser`, `-su`: Zastavica za označitev novega uporabnika kot skrbnika.
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
  
Ukaz `delete-user` v ***digna*** CLI se uporablja za odstranitev obstoječega uporabnika iz sistema ***digna***.
  
#### Primer ukaza
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenti
- **USER_NAME**: Uporabniško ime uporabnika, ki ga želite izbrisati (obvezno). To je edini zahtevan argument ukaza.

#### Primer
```bash
dignacli delete-user jdoe
```
  
Zagon tega ukaza bo odstranil uporabnika `jdoe` iz sistema ***digna***, preklical njegove pravice in izbrisal povezane podatke ter dovoljenja iz repozitorija.

### modify-user

Ukaz `modify-user` v ***digna*** CLI se uporablja za posodobitev podatkov obstoječega uporabnika v sistemu ***digna***.

#### Primer ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, ki ga želite spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Označi uporabnika kot superuporabnika in mu podeli povišane pravice. Ta zastavica ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka uporabniškega računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven za nedoločen čas.  
  
#### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in označitev uporabnika kot superuporabnika:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Ukaz `modify-user-pwd` v ***digna*** CLI se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna***.
  
#### Primer ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, katerega geslo želite spremeniti (obvezno).
- **USER_PWD**: Novo geslo za uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Ukaz `list-users` v ***digna*** CLI prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

#### Primer ukaza

```bash
dignacli list-users
```

Zagon tega ukaza se poveže z ***digna*** repozitorijem in izpiše vse uporabnike, prikazujoč njihove ID-je, uporabniška imena, polna imena, status superuporabnika in datume poteka.

## Upravljanje repozitorija

### upgrade-repo
  
Ukaz `upgrade-repo` v ***digna*** CLI se uporablja za nadgradnjo ali inicializacijo ***digna*** repozitorija. Ta ukaz je ključnega pomena za uporabo posodobitev ali za prvo vzpostavitev infrastrukture repozitorija.
  
#### Primer ukaza

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Če je omogočeno, ukaz teče v simulacijskem načinu, kjer izpiše SQL-poizvedbe, ki bi bile izvedene, vendar jih dejansko ne izvede. To je uporabno za predogled sprememb brez spreminjanja repozitorija.  

  
#### Primer
  
Za nadgradnjo ***digna*** repozitorija lahko zaženete ukaz brez možnosti:
  
```bash
dignacli upgrade-repo
```  
Za izvedbo nadgradnje v simulacijskem načinu (ogled SQL-povedi brez njihove uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je pomemben za vzdrževanje sistema ***digna*** in zagotavljanje, da so sheme baz podatkov in drugi repozitorijski elementi posodobljeni glede na zadnjo različico programske opreme.

### encrypt
  
Ukaz `encrypt` v ***digna*** CLI se uporablja za šifriranje gesla.
  
#### Primer ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Geslo, ki ga želite šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla ga posredujte kot argument.   
Na primer, za šifriranje gesla `mypassword123` uporabite:
```bash
dignacli encrypt mypassword123
```
Ta ukaz vrne šifrirano različico podanega gesla, ki se lahko nato uporabi v varnih kontekstih. Če argument gesla ni podan, bo CLI izpisal napako o manjkajočem argumentu.

### generate-key
  
Ukaz `generate-key` se uporablja za generiranje Fernet-ključa, ki je potreben za zaščito gesel, shranjenih v ***digna*** repozitoriju.
  
#### Primer ukaza
```bash
dignacli generate-key
```
  
## Upravljanje podatkov

### clean-up

Ukaz `clean-up` v ***digna*** CLI se uporablja za odstranjevanje profilov, napovedi in podatkov iz sistema semaforjev za eno ali več podatkovnih virov znotraj določene projekte. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga ohranjati organiziran in učinkovit obseg podatkov z odstranjevanjem zastarelih ali nepotrebnih podatkov.

#### Primer ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega bodo podatki odstranjeni (obvezno). Uporaba ključne besede all-projects v tem argumentu nakaže ***digna***, naj iterira čez vse obstoječe projekte in izvede ukaz.
- **FROM_DATE**: Začetni datum in čas čiščenja podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas čiščenja podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omeji operacijo clean-up na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira in omeji clean-up na tabele, katerih imena vsebujejo podani podniz.
- `--timing`, `-tm`: Prikaže porabljen čas za postopek clean-up po dokončanju.
- `--help`: Prikaže pomoč za ukaz clean-up in zapre.
  
#### Primer
  
Za odstranjevanje podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranitev podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga nadzorovati hranjenje podatkov in zagotavlja, da repozitorij vsebuje le relevantne informacije.

### remove-orphans
  
Ukaz `remove-orphans` v ***digna*** CLI se uporablja za vzdrževanje v ***digna*** repozitoriju.  
Ko uporabnik izbriše projekte ali podatkovne vire, v repozitoriju pogosto ostanejo profili in napovedi brez sorodnih zapisov. Ta ukaz odstrani take sirote (orphan) vrstice iz repozitorija.
  
#### Primer ukaza
  
```bash
dignacli list-projects
```

### list-projects
  
Ukaz `list-projects` v ***digna*** CLI se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
#### Primer ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj hitro prikaže pregled projektov, ki se nahajajo v ***digna*** repozitoriju.

### list-ds

Ukaz `list-ds` v ***digna*** CLI se uporablja za prikaz seznama vseh razpoložljivih podatkovnih virov znotraj določenega projekta. Ta ukaz je uporaben za razumevanje, kateri viri podatkov so na voljo za analizo in upravljanje v sistemu ***digna***.

#### Primer ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se izpišejo podatkovni viri (obvezno).
  
#### Primer
  
Za prikaz vseh podatkovnih virov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled nad podatkovnimi viri, ki so na voljo v projektu, in jim pomaga lažje krmariti in upravljati podatkovno okolje.


### inspect

Ukaz `inspect` v ***digna*** CLI se uporablja za ustvarjanje profilov, napovedi in podatkov za sistem semaforjev za enega ali več podatkovnih virov znotraj določenega projekta. Ta ukaz pomaga analizirati in spremljati podatke za definirano obdobje. Po končani inšpekciji vrne vrednost za izračunan sistem semaforjev:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Primer ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se bodo podatki inšpekcijsko obdelali (obvezno). Uporaba ključne besede all-projects v tem argumentu nakaže ***digna***, naj iterira čez vse obstoječe projekte in izvede ukaz.
- **FROM_DATE**: Začetni datum in čas inšpekcije podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas inšpekcije podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira in inšpektira le tabele, katerih imena vsebujejo podani podniz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil ob dogodkih.
- `--bypass-backend`, `-bb`: Obide backend in zažene inšpekcijo neposredno iz CLI (samo za testne namene!).

  
#### Primer
  
Za inšpekcijo podatkov za projekt `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za inšpekcijo samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je koristen za ustvarjanje posodobljenih profilov in napovedi, spremljanje integritete podatkov in upravljanje sistema obveščanja znotraj določenega projektnega obdobja.

### inspect-async

Ukaz `inspect-async` v ***digna*** CLI se uporablja za ustvarjanje profilov, napovedi in podatkov sistema semaforjev za enega ali več podatkovnih virov znotraj določenega projekta. Ta ukaz pomaga analizirati in spremljati podatke za določeno obdobje. V nasprotju z ukazom `inspect` ta ukaz ne čaka na zaključek inšpekcije. Namesto tega vrne request-id za vloženi zahtevek in za preverjanje napredka inšpekcijskega procesa uporabite ukaz `inspect-status`.

#### Primer ukaza

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se bodo podatki inšpekcijsko obdelali (obvezno). Uporaba ključne besede all-projects v tem argumentu nakaže ***digna***, naj iterira čez vse obstoječe projekte in izvede ukaz.
- **FROM_DATE**: Začetni datum in čas inšpekcije podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas inšpekcije podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira in inšpektira le tabele, katerih imena vsebujejo podani podniz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil ob dogodkih.

  
#### Primer
  
Za zagon asinhrone inšpekcije podatkov za projekt `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Ukaz `inspect-status` v ***digna*** CLI se uporablja za preverjanje napredka asinhrone inšpekcije na podlagi request-id.

#### Primer ukaza

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenti
  
- **REQUEST_ID**: Request-id, ki ga vrne ukaz `inspect-async` 
  
#### Primer
  
Za preverjanje napredka inšpekcije z request-id 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Ukaz `inspect-cancel` v ***digna*** CLI se uporablja za prekinitev inšpekcij na podlagi request-id, lahko pa tudi prekine vse trenutno aktivne zahteve.

#### Primer ukaza

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenti
  
- **REQUEST_ID**: Request-id, ki ga vrne ukaz `inspect-async` 
  
#### Primer
  
Za prekinitev inšpekcije z request-id 12345:
  
```bash
dignacli inspect-cancel 12345
```

Za prekinitev vseh zahtev, ki trenutno tečejo ali so v čakalni vrsti:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Ukaz `export-ds` v ***digna*** CLI se uporablja za izvoz podatkovnih virov iz ***digna*** repozitorija. Privzeto se izvozijo vsi podatkovni viri iz navedenega projekta.

#### Primer ukaza
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, iz katerega bodo podatkovni viri izvoženi.

#### Možnosti

- `--table_name`, `-tn`: Izvozi določen podatkovni vir iz projekta.
- `--exportfile`, `-ef`: Določi ime izhodne datoteke za izvoz.
    
#### Primer
  
Za izvoz vseh podatkovnih virov iz projekta `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ta ukaz izvozi vse podatkovne vire iz `ProjectA` kot JSON-dokument, ki ga je mogoče uvoziti v drug projekt ali ***digna*** repozitorij.

### import-ds

Ukaz `import-ds` v ***digna*** CLI se uporablja za uvoz podatkovnih virov v ciljni projekt in za ustvarjanje uvozne izjave.

#### Primer ukaza
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega se bodo podatkovni viri uvozili.
- **EXPORT_FILE**: Ime datoteke z izvozom podatkovnih virov, ki se bo uvozila.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni določeno, se poročilo izpiše v terminal v obliki tabele).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za uvoz vseh podatkovnih virov iz izvoznega datoteke `my_export.json` v `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po uvozu bo ukaz tudi prikazal poročilo o uvoženih in preskočenih objektih. Uvoženi bodo samo novi podatkovni viri v `ProjectB`. Če želite izvedeti, kateri objekti bi bili uvoženi ali preskočeni, uporabite ukaz `plan-import-ds`.

### plan-import-ds

Ukaz `plan-import-ds` v ***digna*** CLI se uporablja za analizo izvoznega datoteke pred dejanskim uvozom in za izdelavo načrta/poročila uvoza.

#### Primer ukaza
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bi se podatkovni viri morebiti uvozili.
- **EXPORT_FILE**: Ime izvoznega datoteke podatkovnih virov, ki ga je treba analizirati pred uvozom.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni določeno, se poročilo izpiše v terminal v obliki tabele).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za preverjanje, kateri podatkovni viri bi bili uvoženi in kateri preskočeni iz izvoznega datoteke `my_export.json`, če bi bil uvožen v `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ta ukaz bo prikazal le načrt uvoza z objektih, ki bi bili uvoženi ali preskočeni.
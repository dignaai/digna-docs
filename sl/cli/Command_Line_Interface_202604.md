# digna CLI referenca 2026.04
**2026-04-08**

Ta stran dokumentira celoten nabor ukazov, ki so na voljo v CLI orodju ***digna*** izdaje **2026.04**, vključno z primeri uporabe in možnostmi.

---

## Osnove CLI

---

### help
Možnost `--help` zagotavlja informacije o razpoložljivih ukazih in njihovi uporabi. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help takoj za ključnim izrazom ***digna*** CLI  
   ```bash
   dignacli --help
   ```

2. **Pridobitev pomoči za določene ukaze:**  
  
    Za podrobne informacije o določenem ukazu dodajte `--help` temu ukazu.
    Na primer, za pomoč z ukazom `add-user` zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### izhod:
      
     - **Opis ukaza:** Ponuja podroben opis tega, kaj ukaz počne.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Našteje možnosti, specifične za ukaz, skupaj z njihovimi pojasnili.  
     - **Primeri:** Ponuja primere, kako ukaz učinkovito izvesti.

### check-config

Ukaz check-config je pripomoček v CLI orodju ***digna***, namenjen preizkusu konfiguracije ***digna***. Ta ukaz zagotavlja, da komponente ***digna*** najdejo potrebne konfiguracijske elemente v config.toml.

#### Možnosti

- `--configpath`, `-cp`: Datoteka ali imenik, ki vsebuje konfiguracijo. Če ni naveden, bo uporabljen ../config.toml.
      
#### Uporaba ukaza
```bash
dignacli check-config
```

Po uspešni izvedbi ukaz izpiše potrditev popolnosti konfiguracije.  
  
Če se konfiguracija zdi nepopolna, bodo navedeni manjkajoči konfiguracijski elementi.

  
### check-repo-connection

Ukaz check-repo-connection je pripomoček v CLI orodju ***digna***, namenjen preverjanju povezljivosti in dostopa do določene ***digna*** repozitorija. Ta ukaz zagotavlja, da se CLI lahko poveže in komunicira z repozitorijem.
      
#### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Po uspešni izvedbi ukaz izpiše potrditev povezave in podrobnosti o repozitoriju: različica repozitorija, gostitelj (Host), baza podatkov in shema.  
  
Če povezava do repozitorija ni uspešna, preverite datoteko config.toml glede pravilnih nastavitev konfiguracije.


### version

Za preverjanje nameščene različice *dignacli* uporabite možnost --version.  
  
#### Uporaba ukaza
```bash
dignacli --version
```
  
#### Primer izhoda
```bash
dignacli version 2026.04
```

### možnosti beleženja (logging)
  
Privzeto je izpis ukazov ***digna*** v konzoli zasnovan minimalistično. Večina ukazov omogoča pridobitev dodatnih informacij z uporabo naslednjih možnosti:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
"verbose" in "debug" določata raven podrobnosti, medtem ko stikalo "logfile" omogoča preusmeritev izpisa v datoteko namesto v konzolo.

## Upravljanje uporabnikov

### add-user
  
Ukaz add-user v CLI orodju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenti

- **USER_NAME**: Uporniško ime za novega uporabnika (obvezno).
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
  
Ukaz `delete-user` v CLI orodju ***digna*** se uporablja za odstranitev obstoječega uporabnika iz sistema ***digna***.
  
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
  
Izvedba tega ukaza bo odstranila uporabnika `jdoe` iz sistema ***digna***, preklicala njegov dostop in iz repozitorija izbrisala njegove povezane podatke in dovoljenja.

### modify-user

Ukaz `modify-user` v CLI orodju ***digna*** se uporablja za posodobitev podatkov obstoječega uporabnika v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, ki naj bo spremenjen (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuserja, kar podeli povišane privilegije. Ta zastavica ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka uporabniškega računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven nedoločen čas.  
  
#### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in nastavitvijo uporabnika kot superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Ukaz `modify-user-pwd` v CLI orodju ***digna*** se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna***.
  
#### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, katerega geslo je potrebno spremeniti (obvezno).
- **USER_PWD**: Novo geslo za uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla za uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Ukaz `list-users` v CLI orodju ***digna*** prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

#### Uporaba ukaza

```bash
dignacli list-users
```

Izvajanje tega ukaza v CLI orodju ***digna*** bo vzpostavilo povezavo z ***digna*** repozitorijem in izpisalo vse uporabnike, prikazujoč njihovo ID, uporabniško ime, polno ime, status superuserja in časovne žige poteka.

## Upravljanje repozitorija

### upgrade-repo
  
Ukaz `upgrade-repo` v CLI orodju ***digna*** se uporablja za nadgradnjo ali inicializacijo ***digna*** repozitorija. Ta ukaz je bistven za uporabo posodobitev ali prvič postavitev infrastrukture repozitorija.
  
#### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Ko je omogočeno, ukaz zažene v simulacijskem načinu, ki izpiše SQL stavke, ki bi bili izvršeni, vendar jih dejansko ne izvede. To je uporabno za predogled sprememb brez spreminjanja repozitorija.  

  
#### Primer
  
Za nadgradnjo ***digna*** repozitorija lahko zaženete ukaz brez dodatnih možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (za ogled SQL stavkov brez njihove uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključen za vzdrževanje sistema ***digna*** in zagotavljanje, da je shema baze podatkov in druge sestavine repozitorija posodobljene na najnovejšo različico programske opreme.

### encrypt
  
Ukaz `encrypt` v CLI orodju ***digna*** se uporablja za šifriranje gesla.
  
#### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Geslo, ki ga je potrebno šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla morate podati geslo kot argument.   
Na primer, za šifriranje gesla `mypassword123` bi uporabili:
```bash
dignacli encrypt mypassword123
```
Ta ukaz izpiše šifrirano različico podanega gesla, ki se ga lahko nato uporabi v varnih kontekstih. Če argument gesla ni podan, bo CLI izpisal napako, ki kaže na manjkajoči argument.

### generate-key
  
Ukaz `generate-key` se uporablja za generiranje Fernet ključa, ki je bistven za varovanje gesel, shranjenih v ***digna*** repozitoriju.
  
#### Uporaba ukaza
```bash
dignacli generate-key
```
  
## Upravljanje podatkov

### clean-up

Ukaz `clean-up` v CLI orodju ***digna*** se uporablja za odstranjevanje profilov, napovedi in podatkov sistema semaforja za enega ali več podatkovnih virov znotraj določenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga ohranjati organizirano in učinkovito okolje z odstranjevanjem zastarelih ali nepotrebnih podatkov.

#### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega naj se podatki odstranijo (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira čez vse obstoječe projekte in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas za odstranjevanje podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za odstranjevanje podatkov, v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omeji operacijo čiščenja na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filter za omejitev čiščenja na tabele, ki v svojih imenih vsebujejo podan podniz.
- `--timing`, `-tm`: Prikaže trajanje postopka čiščenja po zaključku.
- `--help`: Prikaže pomoč za ukaz clean-up in izstopi.
  
#### Primer
  
Za odstranitev podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranjevanje podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga pri upravljanju prostora za shranjevanje in zagotavlja, da repozitorij vsebuje le relevantne informacije.

### remove-orphans
  
Ukaz `remove-orphans` v CLI orodju ***digna*** se uporablja za vzdrževanje (house-keeping) v ***digna*** repozitoriju.  
Ko uporabnik zbriše projekte ali podatkovne vire, v repozitoriju običajno ostanejo profile in napovedi. S tem ukazom bodo take osirotele vrstice odstranjene iz repozitorija.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

### list-projects
  
Ukaz `list-projects` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj omogoča hitro pregledovanje razpoložljivih projektov v ***digna*** repozitoriju.

### list-ds

Ukaz `list-ds` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih podatkovnih virov v določenem projektu. Ta ukaz je uporaben za razumevanje podatkovnih sredstev, ki so na voljo za analizo in upravljanje v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se izpisujejo podatkovni viri (obvezno).
  
#### Primer
  
Za prikaz vseh podatkovnih virov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled nad podatkovnimi viri v projektu in jim pomaga pri učinkovitejšem upravljanju podatkovnega okolja.


### inspect

Ukaz `inspect` v CLI orodju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema semaforja za enega ali več podatkovnih virov znotraj določenega projekta. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem obdobju. Po zaključku inšpekcije se vrne vrednost izračunanega sistema semaforja:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega naj se podatki pregledajo (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira čez vse obstoječe projekte in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas za inšpekcijo podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za inšpekcijo podatkov, v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filter za inšpekcijo samo tabel, ki v svojih imenih vsebujejo podan podniz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil v primeru opozoril.
- `--bypass-backend`, `-bb`: Zaobide backend in zažene inšpekcijo neposredno iz CLI (samo za namene testiranja!).

  
#### Primer
  
Za pregled podatkov projekta `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za pregled samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje celovitosti podatkov ter upravljanje sistema alarmov znotraj določenega časovnega okvira projekta.

### inspect-async

Ukaz `inspect-async` v CLI orodju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema semaforja za enega ali več podatkovnih virov znotraj določenega projekta. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem obdobju. V nasprotju z ukazom `inspect` ta ne čaka na zaključek inšpekcije.
Namesto tega vrne identifikator zahteve (request id) za oddano zahtevo inšpekcije. Za preverjanje napredka inšpekcijskega procesa uporabite ukaz `inspect-status`.

#### Uporaba ukaza

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega naj se podatki pregledajo (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira čez vse obstoječe projekte in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas za inšpekcijo podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za inšpekcijo podatkov, v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filter za inšpekcijo samo tabel, ki v svojih imenih vsebujejo podan podniz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil v primeru opozoril.

  
#### Primer
  
Za asinhrono inšpekcijo podatkov projekta `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Ukaz `inspect-status` v CLI orodju ***digna*** se uporablja za preverjanje napredka asinhrone inšpekcije na podlagi request ID.

#### Uporaba ukaza

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenti
  
- **REQUEST_ID**: Identifikator zahteve, ki ga vrne ukaz `inspect-async` 
  
#### Primer
  
Za preverjanje napredka inšpekcije z request ID 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Ukaz `inspect-cancel` v CLI orodju ***digna*** se uporablja za preklic inšpekcij na podlagi request ID ali pa za preklic vseh trenutnih zahtev.

#### Uporaba ukaza

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenti
  
- **REQUEST_ID**: Identifikator zahteve, ki ga vrne ukaz `inspect-async` 
  
#### Primer
  
Za preklic inšpekcije z request ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Za preklic vseh zahtev, ki so trenutno v teku ali čakajo:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Ukaz `export-ds` v CLI orodju ***digna*** se uporablja za izvoz podatkovnih virov iz ***digna*** repozitorija. Privzeto bodo izvoženi vsi podatkovni viri iz danega projekta.

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


### import-ds

Ukaz `import-ds` v CLI orodju ***digna*** se uporablja za uvoz podatkovnih virov v ciljni projekt in ustvarjanje poročila o uvozu.

#### Uporaba ukaza
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bodo podatkovni viri uvoženi.
- **EXPORT_FILE**: Ime datoteke izvoza podatkovnih virov, ki se bo uvozila.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni navedeno, se poročilo izpiše v terminalu v tabelarnem formatu).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za uvoz vseh podatkovnih virov iz datoteke izvoza `my_export.json` v `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po uvozu bo ta ukaz prikazal tudi poročilo o uvoženih in preskočenih objektih. V `ProjectB` bodo uvoženi samo novi podatkovni viri. Če želite ugotoviti, kateri objekti bi bili uvoženi in kateri preskočeni, lahko uporabite ukaz `plan-import-ds`.

### plan-import-ds

Ukaz `plan-import-ds` v CLI orodju ***digna*** se uporablja za analizo izvozne datoteke podatkovnih virov in pripravo načrta uvoza v ciljni projekt.

#### Uporaba ukaza
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bi bili podatkovni viri uvoženi.
- **EXPORT_FILE**: Ime datoteke izvoza podatkovnih virov, ki se bo analizirala pred uvozom.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni navedeno, se poročilo izpiše v terminalu v tabelarnem formatu).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za preverjanje, kateri podatkovni viri bi bili uvoženi in kateri preskočeni iz datoteke izvoza `my_export.json`, če bi jih uvozili v `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ta ukaz bo prikazal le načrt uvoza objektov, ki bodo uvoženi in preskočeni.
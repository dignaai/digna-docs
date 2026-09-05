# digna CLI Reference 2025.09
**2025-09-29**

Ta stran dokumentira celoten nabor ukazov, razpoložljivih v CLI orodju ***digna*** izdaje **2025.09**, vključno z primeri uporabe in možnostmi.

---

## Osnove CLI

---

### help
Možnost `--help` zagotavlja informacije o razpoložljivih ukazih in njihovi rabi. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help takoj za ukazom ***dignacli***
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
      
     - **Opis ukaza:** Ponuja podroben opis, kaj ukaz počne.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Nakaže možnosti, specifične za ukaz, skupaj z razlagami.  
     - **Primeri:** Ponuja primere, kako ukaz učinkovito izvesti.

### check-config

Ukaz check-config je pripomoček v CLI orodju ***digna***, namenjen testiranju konfiguracije ***digna***. Ta ukaz preveri, ali lahko komponente ***digna*** najdejo potrebne konfiguracijske elemente v datoteki config.toml.

#### Možnosti

- `--configpath`, `-cp`: Datoteka ali imenik, ki vsebuje konfiguracijo. Če je izpuščeno, bo uporabljen ../config.toml.
      
#### Uporaba ukaza
```bash
dignacli check-config
```

Po uspešni izvedbi bo ukaz izpisal potrditev popolnosti konfiguracije.  
  
Če se zdi, da konfiguracija ni popolna, bodo izpisani manjkajoči konfiguracijski elementi.

  
### check-repo-connection

Ukaz check-repo-connection je pripomoček v CLI orodju ***digna***, namenjen testiranju povezljivosti in dostopa do določene ***digna*** repozitorija. Ta ukaz preveri, ali lahko CLI komunicira z repozitorijem.
      
#### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Po uspešni izvedbi bo ukaz izpisal potrditev povezave, skupaj s podrobnostmi o repozitoriju: različica repozitorija, gostitelj (Host), baza (Database) in shema (Schema).  
  
Če povezava do repozitorija ni uspešna, preverite datoteko config.toml za pravilne konfiguracijske nastavitve.


### version

Za preverjanje nameščene različice *dignacli* uporabite možnost --version.  
  
#### Uporaba ukaza
```bash
dignacli --version
```
  
#### Primer izhoda
```bash
dignacli version 2025.09
```

### možnosti beleženja (logging)
  
Privzeto je izpis v konzoli ukazov ***digna*** zasnovan minimalistično. Večina ukazov omogoča izpis dodatnih informacij z uporabo naslednjih možnosti:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
»verbose« in »debug« določata raven podrobnosti, medtem ko omogoča preklop »logfile« preusmeritev izpisa v datoteko namesto v konzolo.

## Upravljanje uporabnikov

### add-user
  
Ukaz add-user v CLI orodju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenti

- **USER_NAME**: uporabniško ime za novega uporabnika (obvezno).
- **USER_FULL_NAME**: polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: geslo za novega uporabnika (obvezno).

#### Možnosti

- `--is_superuser`, `-su`: Zastavica za označitev novega uporabnika kot skrbnika.
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni nastavljen, račun nima datuma poteka.

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
- **USER_NAME**: uporabniško ime uporabnika, ki naj bo izbrisan (obvezno). To je edini zahtevan argument ukaza.

#### Primer
```bash
dignacli delete-user jdoe
```
  
Izvedba tega ukaza bo odstranila uporabnika `jdoe` iz sistema ***digna***, preklicala njihov dostop in iz repozitorija izbrisala povezane podatke in dovoljenja.

### modify-user

Ukaz `modify-user` v CLI orodju ***digna*** se uporablja za posodobitev podatkov obstoječega uporabnika v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenti
  
- **USER_NAME**: uporabniško ime uporabnika, ki naj bo spremenjen (obvezno).
- **USER_FULL_NAME**: novo polno ime za uporabnika (obvezno).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuserja, s čimer mu dodeli povišane privilegije. Ta zastavica ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni podano, račun ostane veljaven neomejeno.  
  
#### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in za nastavitev uporabnika kot superuser:
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
  
- **USER_NAME**: uporabniško ime uporabnika, katerega geslo naj bo spremenjeno (obvezno).
- **USER_PWD**: novo geslo za uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Ukaz `list-users` v CLI orodju ***digna*** prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

#### Uporaba ukaza

```bash
dignacli list-users
```

Izvedba tega ukaza v CLI orodju ***digna*** se poveže z ***digna*** repozitorijem in izpiše vse uporabnike, prikazujoč njihov ID, uporabniško ime, polno ime, status superuserja in časovne žige poteka.

## Upravljanje repozitorija

### upgrade-repo
  
Ukaz `upgrade-repo` v CLI orodju ***digna*** se uporablja za nadgradnjo ali inicializacijo ***digna*** repozitorija. Ta ukaz je bistven za uporabo posodobitev ali postavitev repozitorijske infrastrukture prvič.
  
#### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Ko je omogočeno, ukaz teče v simulacijskem načinu, ki izpiše SQL stavke, ki bi bili izvršeni, vendar jih dejansko ne izvede. To je uporabno za predogled sprememb, ne da bi spremenili repozitorij.  

  
#### Primer
  
Za nadgradnjo ***digna*** repozitorija lahko zaženete ukaz brez opcij:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (za ogled SQL stavkov brez njihove uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključnega pomena za vzdrževanje sistema ***digna***, saj zagotavlja, da so shema baze in drugi repozitorijski elementi posodobljeni z najnovejšo različico programske opreme.

### encrypt
  
Ukaz `encrypt` v CLI orodju ***digna*** se uporablja za šifriranje gesla.
  
#### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: geslo, ki ga je treba šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla morate geslo podati kot argument.   
Na primer, za šifriranje gesla `mypassword123` bi uporabili:
```bash
dignacli encrypt mypassword123
```
Ukaz izpiše šifrirano različico podanega gesla, ki jo je nato mogoče uporabiti v varnih kontekstih. Če argument gesla ni podan, bo CLI prikazal napako, ki nakaže manjkajoči argument.

### generate-key
  
Ukaz `generate-key` se uporablja za generiranje Fernet ključa, ki je ključnega pomena za zaščito gesel, shranjenih v ***digna*** repozitoriju.
  
#### Uporaba ukaza
```bash
dignacli generate-key
```
  
## Upravljanje podatkov

### clean-up

Ukaz `clean-up` v CLI orodju ***digna*** se uporablja za odstranjevanje profilov, napovedi in podatkov sistema rdeče-žarnice (traffic light system) za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz je bistven za upravljanje življenjskega cikla podatkov in pomaga ohranjati organizirano ter učinkovito okolje s čiščenjem zastarelih ali nepotrebnih podatkov.

#### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: ime projekta, iz katerega je treba odstraniti podatke (obvezno). Uporaba ključne besede all-projects v tem argumentu naroči ***digna***, naj iterira po vseh obstoječih projektih in uporabi ta ukaz na njih.
- **FROM_DATE**: začetni datum in čas za odstranjevanje podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: končni datum in čas za odstranjevanje podatkov, po istih formatih kot FROM_DATE (obvezno).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omeji ukaz clean-up na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filter za omejitev čiščenja na tabele, katerih imena vsebujejo podniz.
- `--timing`, `-tm`: Prikaže čas trajanja postopka čiščenja po zaključku.
- `--help`: Prikaže informacije pomoči za ukaz clean-up in zapusti.
  
#### Primer
  
Za odstranitev podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranitev podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga pri upravljanju prostora za shranjevanje podatkov in zagotavlja, da repozitorij vsebuje le relevantne informacije.

### remove-orphans
  
Ukaz `remove-orphans` v CLI orodju ***digna*** se uporablja za vzdrževalna opravila v ***digna*** repozitoriju.  
Ko uporabnik izbriše projekte ali vire podatkov, v repozitoriju ostanejo profili in napovedi. S tem ukazom bodo taki zapuščeni (orphaned) zapisi odstranjeni iz repozitorija.
  
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

Ta ukaz je posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj hitro prikaže pregled razpoložljivih projektov v ***digna*** repozitoriju.

### list-ds

Ukaz `list-ds` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih virov podatkov znotraj določenega projekta. Ta ukaz je uporaben za razumevanje podatkovnih virov, ki so na voljo za analizo in upravljanje v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: ime projekta, za katerega so viri podatkov izpisani (obvezno).
  
#### Primer
  
Za izpis vseh virov podatkov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled virov podatkov, razpoložljivih v projektu, kar jim pomaga pri lažjem upravljanju podatkovnega okolja.


### inspect

Ukaz `inspect` v CLI orodju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema rdeče-žarnice (traffic light system) za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem obdobju. Po zaključku inšpekcije se vrne vrednost izračunanega stanja sistema rdeče-žarnice:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: ime projekta, za katerega naj bodo podatki pregledani (obvezno). Uporaba ključne besede all-projects v tem argumentu naroči ***digna***, naj iterira po vseh obstoječih projektih in uporabi ta ukaz.
- **FROM_DATE**: začetni datum in čas za pregled podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: končni datum in čas za pregled podatkov, po istih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filter za inšpekcijo samo tabel, katerih imena vsebujejo določen podniz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil v primeru alarmov.
- `--bypass-backend`, `-bb`: Preskoči backend in zažene inšpekcijo neposredno iz CLI (samo za namene testiranja!).

  
#### Primer
  
Za pregled podatkov za projekt `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za pregled samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje integritete podatkov in upravljanje sistema alarmov znotraj določenega časovnega obdobja projekta.

### inspect-async

Ukaz `inspect-async` v CLI orodju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema rdeče-žarnice za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem obdobju. V nasprotju z ukazom `inspect` ta ne čaka na dokončanje inšpekcije.
Namesto tega vrne ID zahteve za oddano inšpekcijsko zahtevo. Za poizvedbo o napredku inšpekcijskega procesa uporabite ukaz `inspect-status`.

#### Uporaba ukaza

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: ime projekta, za katerega naj bodo podatki pregledani (obvezno). Uporaba ključne besede all-projects v tem argumentu naroči ***digna***, naj iterira po vseh obstoječih projektih in uporabi ta ukaz.
- **FROM_DATE**: začetni datum in čas za pregled podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: končni datum in čas za pregled podatkov, po istih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filter za inšpekcijo samo tabel, katerih imena vsebujejo določen podniz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil v primeru alarmov.

  
#### Primer
  
Za asinhrono inšpekcijo podatkov za projekt `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Ukaz `inspect-status` v CLI orodju ***digna*** se uporablja za preverjanje napredka asinhrone inšpekcije na podlagi ID-ja zahteve.

#### Uporaba ukaza

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenti
  
- **REQUEST_ID**: ID zahteve, ki ga vrne ukaz `inspect-async` 
  
#### Primer
  
Za preverjanje napredka inšpekcije z ID-jem zahteve 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Ukaz `inspect-cancel` v CLI orodju ***digna*** se uporablja za preklic inšpekcij na podlagi ID-ja zahteve ali lahko prekliče vse trenutne zahteve.

#### Uporaba ukaza

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenti
  
- **REQUEST_ID**: ID zahteve, ki ga vrne ukaz `inspect-async` 
  
#### Primer
  
Za preklic inšpekcije z ID-jem zahteve 12345:
  
```bash
dignacli inspect-cancel 12345
```

Za preklic vseh zahtev, ki so trenutno v teku ali čakajo:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Ukaz `export-ds` v CLI orodju ***digna*** se uporablja za ustvarjanje izvoza virov podatkov iz ***digna*** repozitorija. Privzeto bodo izvoženi vsi viri podatkov iz podanega projekta.

#### Uporaba ukaza
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenti
- **PROJECT_NAME**: ime projekta, iz katerega bodo izvoženi viri podatkov.

#### Možnosti

- `--table_name`, `-tn`: Izvozi določen vir podatkov iz projekta.
- `--exportfile`, `-ef`: Določi ime datoteke za izvoz.
    
#### Primer
  
Za izvoz vseh virov podatkov iz projekta z imenom `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ta ukaz izvozi vse vire podatkov iz `ProjectA` kot JSON dokument, ki ga je mogoče uvoziti v drug projekt ali v drug ***digna*** repozitorij.


### import-ds

Ukaz `import-ds` v CLI orodju ***digna*** se uporablja za uvoz virov podatkov v ciljni projekt in ustvarjanje poročila o uvozu.

#### Uporaba ukaza
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: ime projekta, v katerega bodo uvoženi viri podatkov.
- **EXPORT_FILE**: ime datoteke izvoza virov podatkov, ki jo je treba uvoziti.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni navedeno, se poročilo izpiše v terminal v tabelarni obliki).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za uvoz vseh virov podatkov iz izvožne datoteke `my_export.json` v `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po uvozu bo ta ukaz prikazal tudi poročilo o uvoženih in preskočenih objektih. V `ProjectB` bodo uvoženi le novi viri podatkov. Če želite izvedeti, kateri objekti bi bili uvoženi in kateri preskočeni, lahko uporabite ukaz `plan-import-ds`.

### plan-import-ds

Ukaz `plan-import-ds` v CLI orodju ***digna*** se uporablja za pripravo načrta uvoza virov podatkov v ciljni projekt in pripravo poročila o tem načrtu.

#### Uporaba ukaza
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: ime projekta, v katerega bi bili viri podatkov uvoženi.
- **EXPORT_FILE**: ime datoteke izvoza virov podatkov, ki jo je treba analizirati pred uvozom.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o načrtu uvoza (če ni navedeno, se poročilo izpiše v terminal v tabelarni obliki).
- `--output-format`, `-f`: Format za shranjevanje poročila (json, csv).
    
#### Primer
  
Za preverjanje, kateri viri podatkov bi bili uvoženi in kateri preskočeni iz izvožne datoteke `my_export.json`, če bi jo uvozili v `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ta ukaz bo prikazal le načrt uvoza objektov, ki bi bili uvoženi in preskočeni.
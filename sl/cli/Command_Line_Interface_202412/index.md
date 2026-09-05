# digna CLI Reference 2024.12
**2024-12-09**

Ta stran dokumentira celoten nabor ukazov, ki so na voljo v CLI orodju ***digna*** različice **2024.12**, vključno z primeri uporabe in opcijami.

---


**2024-12-09**


---

## Osnove CLI

---

## Uporaba opcije `--help`

Opcija `--help` zagotavlja informacije o razpoložljivih ukazih in njihovi uporabi. Obstajata dva glavna načina uporabe te opcije:

1. **Prikaz splošne pomoči:**
   
   Uporabite --help takoj za ključnim besedam ***digna***cl  
   ```bash
   dignacli --help
   ```

3.  **Pridobitev pomoči za določene ukaze:**  
  
    Za podrobne informacije o določenem ukazu priložite `--help` temu ukazu.
    Na primer, za pomoč pri ukazu `add-user` zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Opis ukaza:** Podroben opis, kaj ukaz počne.  
     - **Sintaksa:** Prikazuje natančno sintakso, vključno z obveznimi in izbirnimi argumenti.  
     - **Opcije:** Našteje opcije, specifične za ukaz, skupaj z razlagami.  
     - **Primeri:** Ponuja primere, kako ukaz učinkovito izvesti.

  
## Uporaba ukaza `check-repo-connection`

Ukaz check-repo-connection je orodje znotraj CLI-ja ***digna***, namenjeno testiranju povezljivosti in dostopa do določene ***digna*** repozitorija. Ta ukaz preveri, ali lahko CLI komunicira z repozitorijem.
      
### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Ob uspešni izvedbi ukaz izpiše potrditev o povezavi ter podrobnosti o repozitoriju: različico repozitorija, gostitelja, bazo in shemo.  
  
Če povezava z repozitorijem ni uspešna, preverite datoteko config.toml za pravilne nastavitve konfiguracije.

## Uporaba ukaza `version`

Za preverjanje nameščene različice *dignacli* uporabite možnost --version.  
  
### Uporaba ukaza
```bash
dignacli --version
```
  
### Primer izhoda
```bash
dignacli version 2024.12
```

## Uporaba možnosti za beleženje (logging)
  
Privzeto je izpis v konzolo ukazov ***digna*** zasnovan minimalistično. Večina ukazov omogoča prikaz dodatnih informacij z uporabo naslednjih opcij:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” in “debug” določata stopnjo podrobnosti, medtem ko preklop “logfile” omogoča preusmeritev izpisa v datoteko namesto na konzolo.

# Upravljanje uporabnikov

## Uporaba ukaza `add-user`
  
Ukaz add-user v CLI-ju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenti

- **USER_NAME**: uporabniško ime za novega uporabnika (obvezno).
- **USER_FULL_NAME**: polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: geslo za novega uporabnika (obvezno).

### Opcije

- `--is_superuser`, `-su`: zastavica za dodelitev novega uporabnika kot administratorja.
- `--valid_until`, `-vu`: nastavi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni nastavljen, račun nima datuma poteka.

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
- **USER_NAME**: uporabniško ime uporabnika, ki ga želite izbrisati (obvezno). To je edini zahtevan argument ukaza.

### Primer
```bash
dignacli delete-user jdoe
```
  
Izvedba tega ukaza bo odstranila uporabnika `jdoe` iz sistema ***digna***, odvzela dostop in izbrisala pripadajoče podatke ter dovoljenja v repozitoriju.

## Uporaba ukaza `modify-user`

Ukaz `modify-user` v CLI-ju ***digna*** se uporablja za posodobitev podatkov obstoječega uporabnika v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenti
  
- **USER_NAME**: uporabniško ime uporabnika, ki ga želite spremeniti (obvezno).
- **USER_FULL_NAME**: novo polno ime za uporabnika (obvezno).
  
### Opcije  
  
- `--is_superuser`, `-su`: nastavi uporabnika kot superuserja, s čimer dobi povišane privilegije. Ta zastavica ne zahteva vrednosti.  
- `--valid_until`, `-vu`: nastavi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni podan, račun ostane veljaven neomejeno.  
  
### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in nastavitev uporabnika kot superuser:
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
  
- **USER_NAME**: uporabniško ime uporabnika, katerega geslo želite spremeniti (obvezno).
- **USER_PWD**: novo geslo za uporabnika (obvezno).
  
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

Izvedba tega ukaza v CLI-ju ***digna*** se poveže z repozitorijem ***digna*** in izpiše vse uporabnike, prikazano bodo njihove ID, uporabniško ime, polno ime, status superuserja in časovne žige poteka.

# Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` v CLI-ju ***digna*** se uporablja za nadgradnjo ali inicializacijo repozitorija ***digna***. Ta ukaz je ključen za uporabo posodobitev ali pripravo infrastrukture repozitorija za prvo uporabo.
  
### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
### Opcije
  
- `--simulation-mode`, `-s`: ko je omogočeno, ta možnost zažene ukaz v simulacijskem načinu, ki izpiše SQL poizvedbe, ki bi bile izvedene, vendar jih dejansko ne izvede. To je uporabno za predogled sprememb brez izvajanja le-teh.  

  
### Primer
  
Za nadgradnjo repozitorija ***digna*** lahko zaženete ukaz brez opcij:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (da vidite SQL poizvedbe brez njihovega izvajanja):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključen za vzdrževanje sistema ***digna*** in zagotavlja, da so shema baze podatkov in drugi sestavni deli repozitorija posodobljeni na zadnjo različico programske opreme.

## Uporaba ukaza `encrypt`
  
Ukaz `encrypt` v CLI-ju ***digna*** se uporablja za šifriranje gesla.
  
### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenti
- **PASSWORD**: geslo, ki ga želite šifrirati (obvezno).
  
### Primer
  
Za šifriranje gesla je treba geslo podati kot argument.   
Na primer, za šifriranje gesla `mypassword123` uporabite:
```bash
dignacli encrypt mypassword123
```
Ukaz izpiše šifrirano različico podanega gesla, ki se nato lahko uporabi v varnih kontekstih. Če argument gesla ni podan, bo CLI izpisal napako, ki opozarja na manjkajoči argument.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` se uporablja za generiranje Fernet ključa, ki je potreben za varno shranjevanje gesel v repozitoriju ***digna***.
  
### Uporaba ukaza
```bash
dignacli generate-key
```
  
# Upravljanje podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` v CLI-ju ***digna*** se uporablja za odstranjevanje profilov, napovedi in podatkov sistema prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga ohranjati urejeno ter učinkovito podatkovno okolje z brisanjem zastarelih ali nepotrebnih podatkov.

### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: ime projekta, iz katerega želite odstraniti podatke (obvezno). Uporaba ključne besede all-projects v tem argumentu pomeni, da bo ***digna*** iteriral skozi vse obstoječe projekte in uporabil ta ukaz.
- **FROM_DATE**: začetni datum in čas za odstranjevanje podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: končni datum in čas za odstranjevanje podatkov, v enakih formatih kot FROM_DATE (obvezno).
  
### Opcije
  
- `--table-name`, `-tn`: omeji operacijo čiščenja na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: filter za omejitev čiščenja na tabele, ki v imenu vsebujejo navedeni podniz.
- `--timing`, `-tm`: po zaključku prikaže čas trajanja procesa čiščenja.
- `--help`: prikaže informacije za pomoč pri ukazu clean-up in izstopi.
  
### Primer
  
Za odstranjevanje podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranjevanje podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga pri upravljanju prostora za shranjevanje in zagotavlja, da repozitorij vsebuje samo relevantne informacije.

## Uporaba ukaza `inspect`

Ukaz `inspect` v CLI-ju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz pomaga pri analiziranju in spremljanju podatkov v določenem obdobju.

### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: ime projekta, za katerega želite opraviti inšpekcijo podatkov (obvezno). Uporaba ključne besede all-projects v tem argumentu pomeni, da bo ***digna*** iteriral skozi vse obstoječe projekte in uporabil ta ukaz.
- **FROM_DATE**: začetni datum in čas za inšpekcijo podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: končni datum in čas za inšpekcijo podatkov, v enakih formatih kot FROM_DATE (obvezno).
  
### Opcije

- `--table-name`, `-tn`: omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: filter za inšpekcijo samo tabel, ki v imenu vsebujejo navedeni podniz.
- `--do-profile`: sproži ponovno zbiranje profilov. Privzeto je do-profile.
- `--no-do-profile`: prepreči ponovno zbiranje profilov.
- `--do-prediction`: sproži ponovno izračunavanje napovedi. Privzeto je do-prediction.
- `--no-do-prediction`: prepreči ponovno izračunavanje napovedi.
- `--do-alert-status`: sproži ponovno izračunavanje statusov opozoril. Privzeto je do-alert-status.
- `--no-do-alert-status`: prepreči ponovno izračunavanje statusov opozoril.
- `--iterative`: sproži inšpekcijo obdobja z dnevnim iteriranjem. Privzeto je iterative.
- `--no-iterative`: sproži inšpekcijo celotnega obdobja naenkrat.
- `--timing`, `-tm`: po zaključku prikaže trajanje procesa inšpekcije.
  
### Primer
  
Za inšpekcijo podatkov projekta `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za inšpekcijo samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje integritete podatkov in upravljanje sistema opozoril v okviru določenega časovnega okvira projekta.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` v CLI-ju ***digna*** se uporablja za poizvedbo o stanju Traffic Light System (TLS) za določeno tabelo znotraj projekta na podan datum. Traffic Light System daje vpogled v zdravje in kakovost podatkov ter opozori na morebitne težave ali opozorila, ki zahtevajo pozornost.
  
### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenti
  
- **PROJECT_NAME**: ime projekta, za katerega se poizveduje stanje TLS (obvezno).
- **TABLE_NAME**: določena tabela znotraj projekta, za katero potrebujete stanje TLS (obvezno).
- **DATE**: datum, za katerega se poizveduje stanje TLS, običajno v formatu %Y-%m-%d (obvezno).
  
### Primer
  
Za preverjanje stanja TLS za tabelo z imenom UserData v projektu ProjectA na 1. julij 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov z zagotavljanjem jasnega in uporabnega poročila o stanju na podlagi vnaprej določenih meril.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` v CLI-ju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je posebej koristen za skrbnike in uporabnike, ki upravljajo več projektov, saj hitro prikaže pregled razpoložljivih projektov v repozitoriju ***digna***.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` v CLI-ju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih virov podatkov znotraj določenega projekta. Ta ukaz je uporaben za razumeti podatkovne vire, ki so na voljo za analizo in upravljanje v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenti
- **PROJECT_NAME**: ime projekta, za katerega se navajajo podatkovni viri (obvezno).
  
### Primer
  
Za izpis vseh virov podatkov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled nad viri podatkov, ki so na voljo v projektu, in jim pomaga pri lažjem upravljanju podatkovnega okolja.
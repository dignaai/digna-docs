---
title: Priročnik digna CLI 2025.09 – ukazi in primeri | Dokumentacija digna
description: Popoln priročnik za digna CLI izdajo 2025.09. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-config, check-repo-connection, inspect, inspect-async itd.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# Referenca digna CLI 2025.09
**2025-09-29**

Na tej strani je dokumentiran celoten nabor ukazov, ki so na voljo v CLI ***digna*** izdaje **2025.09**, vključno s primeri uporabe in možnostmi.

---

## Osnove CLI

---

### help
Možnost `--help` poda informacije o razpoložljivih ukazih in njihovi uporabi. Obstajata dva osnovna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite `--help` neposredno za besedo `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Pridobitev pomoči za določene ukaze:**  
  
    Za podrobne informacije o določenem ukazu dodajte `--help` k temu ukazu.  
    Na primer, za pomoč pri ukazu `add-user` izvedite:
     ```bash
     dignacli add-user --help
     ```

     ### izhod:
      
     - **Opis ukaza:** Podroben opis, kaj ukaz naredi.  
     - **Sintaksa:** Prikazuje natančno sintakso, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Seznam možnosti, specifičnih za ukaz, skupaj z njihovimi pojasnili.  
     - **Primeri:** Primeri učinkovite uporabe ukaza.

### check-config

Ukaz check-config je pripomoček v CLI orodju ***digna***, namenjen preverjanju konfiguracije ***digna***. Ta ukaz zagotavlja, da komponente ***digna*** lahko najdejo potrebne konfiguracijske elemente v config.toml.

#### Možnosti

- `--configpath`, `-cp`: Datoteka ali imenik, ki vsebuje konfiguracijo. Če ni navedeno, bo uporabljen ../config.toml.
      
#### Uporaba ukaza
```bash
dignacli check-config
```

Po uspešnem zagonu ukaz izpiše potrdilo o popolnosti konfiguracije.  
  
Če je konfiguracija nepopolna, bo naveden seznam manjkajočih konfiguracijskih elementov.

  
### check-repo-connection

Ukaz check-repo-connection je pripomoček v CLI orodju ***digna***, namenjen preverjanju dostopnosti in povezave z navedenim repozitorijem ***digna***. Ta ukaz preveri, ali lahko CLI komunicira z repozitorijem.
      
#### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Po uspešnem zagonu ukaz izpiše potrdilo o povezavi skupaj s podrobnostmi o repozitoriju: različica repozitorija, gostitelj, baza podatkov in shema.  
  
Če povezava z repozitorijem ni bila vzpostavljena, preverite datoteko config.toml glede pravilnih nastavitev.


### version

Za preverjanje nameščene različice *dignacli* uporabite možnost `--version`.  
  
#### Uporaba ukaza
```bash
dignacli --version
```
  
#### Primer izhoda
```bash
dignacli version 2025.09
```

### parametri beleženja
  
Privzeto je izhod ukazov v konzoli orodij ***digna*** minimalističen. Večina ukazov omogoča izpis dodatnih informacij z uporabo naslednjih možnosti:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
»verbose« in »debug« določata raven podrobnosti, medtem ko preklopnik »logfile« omogoča preusmeritev izhoda v datoteko namesto v konzolo.

## Upravljanje uporabnikov

### add-user
  
Ukaz add-user v CLI ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenti

- **USER_NAME**: Uporniško ime za nov račun (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

#### Možnosti

- `--is_superuser`, `-su`: Preklopnik za dodelitev skrbniških pravic novemu uporabniku.
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni naveden, račun nima datuma poteka.

#### Primer

Da dodate novega uporabnika z imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Da dodate novega uporabnika in nastavite datum poteka računa:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Ukaz `delete-user` v CLI ***digna*** se uporablja za brisanje obstoječega uporabnika iz sistema ***digna***.
  
#### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenti
- **USER_NAME**: Uporniško ime uporabnika, katerega želite izbrisati (obvezno). To je edini argument, potreben za ukaz.

#### Primer
```bash
dignacli delete-user jdoe
```
  
Izvedba tega ukaza bo iz sistema ***digna*** odstranila uporabnika `jdoe`, preklicala njegovo dostopanje in iz repozitorija odstranila povezane podatke in dovoljenja.

### modify-user

Ukaz `modify-user` v CLI ***digna*** se uporablja za posodobitev podatkov obstoječega uporabnika v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, katerega želite spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Dodeli uporabniku status superuporabnika, s čimer pridobi povišane privilegije. Ta preklopnik ne potrebuje vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven brez omejitve.  
  
#### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v »Johnathan Doe« in dodelitev superuporabniškega statusa:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Ukaz `modify-user-pwd` v CLI ***digna*** se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna***.
  
#### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, za katerega želite spremeniti geslo (obvezno).
- **USER_PWD**: Novo geslo za uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Ukaz `list-users` v CLI ***digna*** prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

#### Uporaba ukaza

```bash
dignacli list-users
```

Izvedba tega ukaza se bo v CLI ***digna*** povezala z repozitorijem ***digna*** in izpisala seznam vseh uporabnikov, prikazala njihov ID, uporabniško ime, polno ime, status superuporabnika in časovne oznake poteka.

## Upravljanje repozitorija

### upgrade-repo
  
Ukaz `upgrade-repo` v CLI ***digna*** se uporablja za nadgradnjo ali inicializacijo repozitorija ***digna***. Ta ukaz je potreben za uporabo posodobitev ali prvotno nastavitev repozitorijske infrastrukture.
  
#### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Če je naveden, se ukaz zažene v simulacijskem načinu, ki izpiše SQL ukaze, ki bi bili izvedeni, vendar jih dejansko ne izvede. To je uporabno za ogled sprememb brez posegov v repozitorij.  

  
#### Primer
  
Za nadgradnjo repozitorija ***digna*** lahko izvedete ukaz brez možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (da si ogledate SQL ukaze brez njihove uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je kritičen za vzdrževanje sistema ***digna***, saj zagotavlja aktualnost sheme baze podatkov in drugih komponent repozitorija v skladu z najnovejšo različico programske opreme.

### encrypt
  
Ukaz `encrypt` v CLI ***digna*** se uporablja za šifriranje gesla.
  
#### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Geslo, ki ga je treba šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla ga posredujte kot argument.   
Na primer, za šifriranje gesla `mypassword123` uporabite:
```bash
dignacli encrypt mypassword123
```
Ta ukaz bo izpisal šifrirano različico podanega gesla, ki jo je nato mogoče uporabiti v varnih kontekstih. Če argument gesla ni naveden, bo CLI prikazal napako o manjkajočem argumentu.

### generate-key
  
Ukaz `generate-key` se uporablja za generiranje ključa Fernet, ki je potreben za zaščito gesel, shranjenih v repozitoriju ***digna***.
  
#### Uporaba ukaza
```bash
dignacli generate-key
```
  
## Upravljanje podatkov

### clean-up

Ukaz `clean-up` v CLI ***digna*** se uporablja za brisanje profilov, napovedi in podatkov sistema signalnih indikatorjev (traffic light system) za enega ali več virov podatkov znotraj navedenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga ohranjati organizirano ter učinkovito okolje z odstranjevanjem zastarelih ali nepotrebnih podatkov.

#### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega želite odstraniti podatke (obvezno). Uporaba ključne besede `all-projects` v tem argumentu ukaže ***digna***, naj pregleda vse razpoložljive projekte in izvede ukaz za vsak od njih.
- **FROM_DATE**: Datum in čas začetka brisanja podatkov. Dovoljeni formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Datum in čas zaključka brisanja podatkov v istih formatih kot FROM_DATE (obvezno).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omeji operacijo čiščenja na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filter za omejitev čiščenja na tabele, katerih ime vsebuje navedeni niz.
- `--timing`, `-tm`: Prikaže trajanje izvedbe čiščenja po njegovem zaključku.
- `--help`: Prikaže pomoč za ukaz clean-up in izstopi.
  
#### Primer
  
Za brisanje podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za brisanje podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga upravljati shranjevanje podatkov in zagotavlja, da v repozitoriju ostanejo le relevantne informacije.

### remove-orphans
  
Ukaz `remove-orphans` v CLI ***digna*** se uporablja za čiščenje repozitorija ***digna***.  
Ko uporabnik izbriše projekte ali vire podatkov, se lahko v repozitoriju pojavijo preostali profili in napovedi. S tem ukazom bodo take zapuščene (orphaned) vnose izbrisali iz repozitorija.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

### list-projects
  
Ukaz `list-projects` v CLI ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj ponuja hiter pregled razpoložljivih projektov v repozitoriju ***digna***.

### list-ds

Ukaz `list-ds` v CLI ***digna*** se uporablja za prikaz seznama vseh razpoložljivih virov podatkov v navedenem projektu. Ta ukaz je koristen za razumevanje podatkov, ki so na voljo za analizo in upravljanje v sistemu ***digna***.

#### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se naštejejo viri podatkov (obvezno).
  
#### Primer
  
Za prikaz vseh virov podatkov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled virov podatkov, ki so na voljo v projektu, kar pomaga pri lažjem upravljanju in orientaciji v podatkovnem okolju.


### inspect

Ukaz `inspect` v CLI ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema signalnih indikatorjev (traffic light system) za enega ali več virov podatkov znotraj navedenega projekta. Ta ukaz pomaga analizirati in nadzorovati podatke za določeno obdobje. Po zaključku inšpekcije je vrnjena vrednost izračunanega sistema signalnih indikatorjev:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, katerega podatke želite inšpektirati (obvezno). Uporaba ključne besede `all-projects` v tem argumentu ukaže ***digna***, naj pregleda vse razpoložljive projekte in izvede ukaz za vsak od njih.
- **FROM_DATE**: Datum in čas začetka inšpekcije podatkov. Dovoljeni formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Datum in čas zaključka inšpekcije podatkov v istih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filter za inšpekcijo samo tabel, katerih ime vsebuje navedeni niz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil v primeru alarmov.
- `--bypass-backend`, `-bb`: Prezri backend in zaženi inšpekcijo neposredno iz CLI (samo za testiranje!).

  
#### Primer
  
Za inšpekcijo podatkov projekta `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za inšpekcijo samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje integritete podatkov ter upravljanje sistema obveščanja v navedenem časovnem obdobju projekta.

### inspect-async

Ukaz `inspect-async` v CLI ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema signalnih indikatorjev (traffic light system) za enega ali več virov podatkov znotraj navedenega projekta. Ta ukaz pomaga analizirati in nadzorovati podatke za določeno obdobje. V nasprotju s sinhrono različico ta ukaz ne čaka na dokončanje inšpekcije.
Namesto tega vrne identifikator zahteve za vloženo asinhrono inšpekcijo. Za preverjanje napredka inšpekcije uporabite ukaz `inspect-status`.

#### Uporaba ukaza

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, katerega podatke želite inšpektirati (obvezno). Uporaba ključne besede `all-projects` v tem argumentu ukaže ***digna***, naj pregleda vse razpoložljive projekte in izvede ukaz za vsak od njih.
- **FROM_DATE**: Datum in čas začetka inšpekcije podatkov. Dovoljeni formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Datum in čas zaključka inšpekcije podatkov v istih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filter za inšpekcijo samo tabel, katerih ime vsebuje navedeni niz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestil v primeru alarmov.

  
#### Primer
  
Za asinhrono inšpekcijo podatkov projekta `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Ukaz `inspect-status` v CLI ***digna*** se uporablja za preverjanje napredka asinhrone inšpekcije na podlagi identifikatorja zahteve.

#### Uporaba ukaza

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenti
  
- **REQUEST_ID**: Identifikator zahteve, ki ga je vrnil ukaz `inspect-async`. 
  
#### Primer
  
Za preverjanje napredka inšpekcije z identifikatorjem zahteve 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Ukaz `inspect-cancel` v CLI ***digna*** se uporablja za preklic inšpekcij po identifikatorju zahteve ali za preklic vseh trenutnih zahtev.

#### Uporaba ukaza

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenti
  
- **REQUEST_ID**: Identifikator zahteve, ki ga je vrnil ukaz `inspect-async`. 
  
#### Primer
  
Za preklic inšpekcije z identifikatorjem zahteve 12345:
  
```bash
dignacli inspect-cancel 12345
```

Za preklic vseh zahtev, ki se trenutno izvajajo ali čakajo:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Ukaz `export-ds` v CLI ***digna*** se uporablja za ustvarjanje izvoza virov podatkov iz repozitorija ***digna***. Privzeto se izvažajo vsi viri podatkov iz navedenega projekta.

#### Uporaba ukaza
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, iz katerega bodo izvažani viri podatkov.

#### Možnosti

- `--table_name`, `-tn`: Izvozi določen vir podatkov iz projekta.
- `--exportfile`, `-ef`: Določi ime datoteke za izvoz.
    
#### Primer
  
Za izvoz vseh virov podatkov iz projekta `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ta ukaz izvozi vse vire podatkov iz `ProjectA` v formatu JSON, ki ga je mogoče uvoziti v drug projekt ali repozitorij ***digna***.


### import-ds

Ukaz `import-ds` v CLI ***digna*** se uporablja za uvoz virov podatkov v ciljni projekt in ustvarjanje poročila o uvozu.

#### Uporaba ukaza
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bodo uvoženi viri podatkov.
- **EXPORT_FILE**: Ime izvozne datoteke virov podatkov, ki jo je treba uvoziti.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o uvozu (če ni navedeno, se poročilo izpiše v terminal v tabelarni obliki).
- `--output-format`, `-f`: Format za shranjevanje poročila o uvozu (json, csv).
    
#### Primer
  
Za uvoz vseh virov podatkov iz datoteke izvoza `my_export.json` v `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po uvozu bo ta ukaz prikazal tudi poročilo o uvoženih in izpuščenih objektih. V `ProjectB` bodo uvoženi le novi viri podatkov. Če želite vedeti, kateri objekti bodo uvoženi in kateri izpuščeni, lahko uporabite ukaz `plan-import-ds`.

### plan-import-ds

Ukaz `plan-import-ds` v CLI ***digna*** se uporablja za analizo izvoza virov podatkov pred uvozom in ustvarjanje načrta uvoza.

#### Uporaba ukaza
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega je načrtovan uvoz virov podatkov.
- **EXPORT_FILE**: Ime izvozne datoteke virov podatkov, ki bo analizirana pred uvozom.

#### Možnosti

- `--output-file`, `-o`: Datoteka za shranjevanje poročila o načrtu uvoza (če ni navedeno, se poročilo izpiše v terminal v tabelarni obliki).
- `--output-format`, `-f`: Format za shranjevanje poročila o načrtu uvoza (json, csv).
    
#### Primer
  
Za preverjanje, kateri viri podatkov bodo uvoženi in kateri bodo izpuščeni iz datoteke izvoza `my_export.json` pri uvozu v `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ta ukaz bo le prikazal načrt uvoza objektov, ki bodo uvoženi in izpuščeni.
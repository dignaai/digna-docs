---
title: digna CLI Referenca 2024.12 – Ukazi & Primeri | digna Dokumentacija
description: Celovit referenčni prikaz za izdajo digna CLI 2024.12. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-repo-connection, upgrade-repo, inspect in več.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Referenca 2024.12
**2024-12-09**

Ta stran dokumentira celoten nabor ukazov, na voljo v izdaji CLI-ja ***digna*** **2024.12**, vključno z uporabnimi primeri in možnostmi.

---


**2024-12-09**


---

## Osnove CLI

---

## Uporaba možnosti `help`

Možnost `--help` zagotavlja informacije o razpoložljivih ukazih in njihovem načinu uporabe. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help takoj po ukazu `dignacli`  
   ```bash
   dignacli --help

3.  **Pomoč za posamezen ukaz:**  
  
    Za podrobne informacije o določenem ukazu dodajte `--help` za tem ukazom.
    Na primer, za pomoč pri ukazu `add-user` zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### izhod:
      
     - **Opis ukaza:** Ponuja podroben opis, kaj ukaz naredi.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z zahtevnimi in izbirnimi argumenti.  
     - **Možnosti:** Navedene so morebitne možnosti, specifične za ukaz, skupaj z razlagami.  
     - **Primeri:** Prikazuje primere učinkovite uporabe ukaza.

  
## Uporaba ukaza `check-repo-connection`

Ukaz `check-repo-connection` je orodje v CLI-ju ***digna***, namenjeno testiranju povezave in dostopa do določenega repoziotorija ***digna***. Ta ukaz zagotavlja, da lahko CLI komunicira z repozitorijem.
      
### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Ob uspešni izvedbi bo ukaz potrdil povezavo ter prikazal podrobnosti o repozitoriju: različico repozitorija, gostitelja (Host), bazo podatkov (Database) in shemo (Schema).  
  
Če povezava z repozitorijem ne uspe, preverite datoteko config.toml za pravilne nastavitve konfiguracije.

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
  
Privzeto je izpis v konzolo iz ukazov ***digna*** zasnovan minimalistično. Večina ukazov omogoča dodaten izpis informacij z uporabo naslednjih možnosti:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” in “debug” določata raven podrobnosti, medtem ko možnost “logfile” omogoča preusmeritev izpisa v datoteko namesto na konzolo.

# Upravljanje uporabnikov

## Uporaba ukaza `add-user`
  
Ukaz `add-user` v CLI-ju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenti

- **USER_NAME**: Uporniško ime novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo novega uporabnika (obvezno).

### Možnosti

- `--is_superuser`, `-su`: Zastavica za dodelitev novega uporabnika kot skrbnika.
- `--valid_until`, `-vu`: Nastavi datum poteka uporabniškega računa v obliki `YYYY-MM-DD HH:MI:SS`. Če ni nastavljen, račun nima roka veljavnosti.

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
- **USER_NAME**: Uporniško ime uporabnika, ki naj bo izbrisan (obvezno). To je edini argument, ki ga ukaz zahteva.

### Primer
```bash
dignacli delete-user jdoe
```
  
Izvedba tega ukaza bo odstranila uporabnika `jdoe` iz sistema ***digna***, preklicala njihove pravice in izbrisala povezane podatke ter dovoljenja iz repozitorija.

## Uporaba ukaza `modify-user`

Ukaz `modify-user` v CLI-ju ***digna*** se uporablja za posodobitev podatkov obstoječega uporabnika v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, ki naj bo spremenjen (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuporabnika in mu podeli povišane privilegije. Ta zastavica ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka uporabniškega računa v formatu YYYY-MM-DD HH:MI:SS. Če ni podano, račun ostane veljaven nedoločen čas.  
  
### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in nastavitvijo uporabnika kot superuporabnika:
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
  
- **USER_NAME**: Uporniško ime uporabnika, katerega geslo naj bo spremenjeno (obvezno).
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

Izvedba tega ukaza bo vzpostavila povezavo z repozitorijem ***digna*** in izpisala vse uporabnike, prikazala njihove ID-je, uporabniška imena, polna imena, status superuporabnika in datume poteka.

# Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` v CLI-ju ***digna*** se uporablja za nadgradnjo ali inicializacijo repozitorija ***digna***. Ta ukaz je ključnega pomena za uporabo posodobitev ali nastavitev repozitorijske infrastrukture prvič.
  
### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
### Možnosti
  
- `--simulation-mode`, `-s`: Ko je aktivirano, ta možnost zažene ukaz v simulacijskem načinu, ki izpiše SQL-stavke, ki bi bili izvršeni, vendar jih ne izvede. To je uporabno za predogled sprememb brez dejanskih sprememb v repozitoriju.  

  
### Primer
  
Za nadgradnjo repozitorija ***digna*** lahko zaženete ukaz brez možnosti:
  
```bash
dignacli upgrade-repo
```  
Za izvajanje nadgradnje v simulacijskem načinu (za ogled SQL-stavkov brez njihove uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je pomemben za vzdrževanje sistema ***digna*** in zagotavlja, da so sheme baze podatkov in drugi repozitorijski elementi posodobljeni z najnovejšo različico programske opreme.

## Uporaba ukaza `encrypt`
  
Ukaz `encrypt` v CLI-ju ***digna*** se uporablja za šifriranje gesla.
  
### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenti
- **PASSWORD**: Geslo, ki naj bo šifrirano (obvezno).
  
### Primer
  
Za šifriranje gesla podajte geslo kot argument.   
Na primer, za šifriranje gesla `mypassword123` uporabite:
```bash
dignacli encrypt mypassword123
```
Ta ukaz vrne šifrirano različico podanega gesla, ki jo je mogoče uporabiti v varnih kontekstih. Če argument za geslo ni podan, bo CLI prikazal napako, ki nakaže manjkajoč argument.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` se uporablja za generiranje Fernet-ključa, kar je pomembno za varno shranjevanje gesel v repozitoriju ***digna***.
  
### Uporaba ukaza
```bash
dignacli generate-key
```
  
# Upravljanje podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` v CLI-ju ***digna*** se uporablja za odstranjevanje profilov, napovedi (predictions) in podatkov iz Traffic Light System za eno ali več podatkovnih virov v okviru določenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga ohranjati organizirano ter učinkovito podatkovno okolje z odstranjevanjem zastarelih ali nepotrebnih podatkov.

### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega naj se podatki odstranijo (obvezno). Uporaba ključne besede `all-projects` v tem argumentu ukaže ***digna***, naj iterira čez vse obstoječe projekte in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas čiščenja podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas čiščenja podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
### Možnosti
  
- `--table-name`, `-tn`: Omeji operacijo clean-up na določen tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira in omeji clean-up na tabele, ki vsebujejo navedeni del imena.
- `--timing`, `-tm`: Prikaže čas porabljen za postopek clean-up po zaključku.
- `--help`: Prikaže pomočno informacijo za ukaz clean-up in zapre program.
  
### Primer
  
Za odstranjevanje podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranjevanje podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga upravljati shranjevanje podatkov in zagotavlja, da repozitorij vsebuje le relevantne informacije.

## Uporaba ukaza `inspect`

Ukaz `inspect` v CLI-ju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov za Traffic Light System za eno ali več podatkovnih virov v okviru določenega projekta. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem obdobju.

### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega naj se izvajajo inšpekcije podatkov (obvezno). Uporaba ključne besede `all-projects` v tem argumentu ukaže ***digna***, naj iterira čez vse obstoječe projekte in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas inšpekcije podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas inšpekcije podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira inšpekcijo samo na tabele, ki vsebujejo navedeni del imena.
- `--do-profile`: Sproži ponovni izračun profilov. Privzeto je do-profile.
- `--no-do-profile`: Prepreči ponovni izračun profilov.
- `--do-prediction`: Sproži ponovni izračun napovedi. Privzeto je do-prediction.
- `--no-do-prediction`: Prepreči ponovni izračun napovedi.
- `--do-alert-status`: Sproži ponovni izračun stanja opozoril. Privzeto je do-alert-status.
- `--no-do-alert-status`: Prepreči ponovni izračun stanja opozoril.
- `--iterative`: Sproži inšpekcijo obdobja z uporabo dnevnih iteracij. Privzeto je iterative.
- `--no-iterative`: Izvede inšpekcijo celotnega obdobja naenkrat.
- `--timing`, `-tm`: Prikaže trajanje procesa inšpekcije po zaključku.
  
### Primer
  
Za inšpekcijo podatkov projekta `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za inšpekcijo samo določene tabele in prisilno ponovni izračun napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje integritete podatkov in upravljanje sistema opozoril v okviru določenega projektnega časovnega okvira.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` v CLI-ju ***digna*** se uporablja za preverjanje stanja Traffic Light System (TLS) za določeno tabelo v projektu na določen datum. Traffic Light System zagotavlja vpogled v kakovost in zdravstveno stanje podatkov ter označi morebitne težave ali opozorila, ki zahtevajo pozornost.
  
### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se zahteva TLS-status (obvezno).
- **TABLE_NAME**: Določena tabela znotraj projekta, za katero se zahteva TLS-status (obvezno).
- **DATE**: Datum, za katerega se zahteva TLS-status, običajno v formatu %Y-%m-%d (obvezno).
  
### Primer
  
Za preverjanje TLS-stanja tabele UserData v projektu ProjectA za 1. julij 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov z jasnim in uporabnim poročilom o stanju na podlagi vnaprej določenih meril.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` v CLI-ju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, in nudi hiter pregled razpoložljivih projektov v repozitoriju ***digna***.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` v CLI-ju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih podatkovnih virov v določenem projektu. Ta ukaz je uporaben za pregled podatkovnih virov, ki so na voljo za analizo in upravljanje v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega naj se izpiše seznam podatkovnih virov (obvezno).
  
### Primer
  
Za izpis vseh podatkovnih virov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled nad podatkovnimi viri, ki so na voljo v projektu, in jim pomaga učinkoviteje krmariti ter upravljati podatkovno okolje.
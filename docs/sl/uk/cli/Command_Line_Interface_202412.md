---
title: digna CLI Referenca 2024.12 – Ukazi in primeri | digna Documentation
description: Popolna referenca za digna CLI izdajo 2024.12. Naučite se upravljati uporabnike, repozitorije in podatke s pomočjo ukazov, kot so add-user, check-repo-connection, upgrade-repo, inspect in drugi.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Na tej strani je dokumentiran popoln nabor ukazov, dostopnih v CLI orodju ***digna*** izdaje **2024.12**, vključno s primeri uporabe in parametri.

---


**2024-12-09**


---

## Osnove CLI

---

## Uporaba možnosti `help`

Možnost `--help` zagotavlja informacije o razpoložljivih ukazih in njihovi uporabi. Obstajata dva osnovna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help takoj za ključno besedo ***dignacli***  
   ```bash
   dignacli --help
   ```

3.  **Pridobitev pomoči za konkreten ukaz:**  
  
    Če želite podrobne informacije o določenem ukazu, dodajte `--help` k temu ukazu.
    Na primer, za pomoč pri ukazu `add-user` izvedite:
     ```bash
     dignacli add-user --help
     ```

     ### izhod:
      
     - **Opis ukaza:** Podroben opis, kaj ukaz naredi.  
     - **Sintaksa:** Prikazuje natančno sintakso, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Navedeni so parametri specifični za ukaz z njihovimi pojasnili.  
     - **Primeri:** Prikaz primerov, kako učinkovito izvesti ukaz.

  
## Uporaba ukaza `check-repo-connection`

Ukaz check-repo-connection je pripomoček v CLI orodju ***digna***, namenjen preverjanju povezave in dostopa do navedenega repozitorija ***digna***. Ta ukaz preveri, ali lahko CLI komunicira z repozitorijem.
      
### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Po uspešni izvedbi ukaz izpiše potrdilo o povezavi skupaj s podrobnostmi o repozitoriju: različico repozitorija, gostitelja, bazo podatkov in shemo.  
  
Če povezava z repozitorijem ni uspešna, preverite datoteko config.toml glede pravilnih nastavitev.

## Uporaba ukaza ‘version’

Za preverjanje nameščene različice *dignacli* uporabite možnost --version.  
  
### Uporaba ukaza
```bash
dignacli --version
```
  
### Primer izhoda
```bash
dignacli version 2024.12
```

## Uporaba nastavitev beleženja (logging)
  
Privzeto je izhod ukazov v konzoli orodij ***digna*** minimalističen. Večina ukazov omogoča pridobitev dodatnih informacij z naslednjimi možnostmi:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
»verbose« in »debug« določata stopnjo podrobnosti, medtem ko stikalo »logfile« omogoča preusmeritev izhoda v datoteko namesto v konzolo.

# Upravljanje uporabnikov

## Uporaba ukaza ‘add-user’
  
Ukaz add-user v CLI orodju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenti

- **USER_NAME**: Ime uporabnika za nov račun (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

### Možnosti

- `--is_superuser`, `-su`: Preklop za označitev novega uporabnika kot skrbnika.
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni naveden, račun nima roka veljavnosti.

### Primer

Za dodajanje novega uporabnika z imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Za dodajanje novega uporabnika in nastavitev datuma poteka računa:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Uporaba ukaza `delete-user`
  
Ukaz `delete-user` v CLI orodju ***digna*** se uporablja za brisanje obstoječega uporabnika iz sistema ***digna***.
  
### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
### Argumenti
- **USER_NAME**: Ime uporabnika, ki ga je treba izbrisati (obvezno). To je edini argument, potreben za ukaz.

### Primer
```bash
dignacli delete-user jdoe
```
  
Izvedba tega ukaza bo odstranila uporabnika `jdoe` iz sistema ***digna***, preklicala njegov dostop in izbrisala povezane podatke ter dovoljenja iz repozitorija.

## Uporaba ukaza `modify-user`

Ukaz `modify-user` v CLI orodju ***digna*** se uporablja za posodabljanje podatkov obstoječega uporabnika v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenti
  
- **USER_NAME**: Ime uporabnika, ki ga želite spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuporabnika, kar mu daje povišane privilegije. Ta preklop ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven za nedoločen čas.  
  
### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in nastavitev uporabnika kot superuporabnika:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Uporaba ukaza `modify-user-pwd`
  
Ukaz `modify-user-pwd` v CLI orodju ***digna*** se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna***.
  
### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenti
  
- **USER_NAME**: Ime uporabnika, za katerega želite spremeniti geslo (obvezno).
- **USER_PWD**: Novo geslo za uporabnika (obvezno).
  
### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Uporaba ukaza `list-users`

Ukaz `list-users` v CLI orodju ***digna*** prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

### Uporaba ukaza

```bash
dignacli list-users
```

Izvedba tega ukaza v CLI orodju ***digna*** se poveže na repozitorij ***digna*** in izpiše vse uporabnike, prikazujoč njihove ID-je, uporabniška imena, polna imena, status superuporabnika ter časovne oznake poteka.

# Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` v CLI orodju ***digna*** se uporablja za posodobitev ali inicializacijo repozitorija ***digna***. Ta ukaz je potreben za uporabo posodobitev ali nastavitev infrastrukture repozitorija prvič.
  
### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
### Možnosti
  
- `--simulation-mode`, `-s`: Ko je omogočeno, ta možnost zažene ukaz v simulacijskem načinu, ki izpiše SQL ukaze, ki bi bili izvedeni, vendar jih v resnici ne izvede. To je uporabno za predogled sprememb brez dejanskega spreminjanja repozitorija.  

  
### Primer
  
Za posodobitev repozitorija ***digna*** lahko zaženete ukaz brez možnosti:
  
```bash
dignacli upgrade-repo
```  
Za izvedbo posodobitve v simulacijskem načinu (da si ogledate SQL ukaze brez njihovega uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je pomemben za vzdrževanje sistema ***digna***, saj zagotavlja aktualnost sheme baze podatkov in drugih komponent repozitorija v skladu z najnovejšo različico programske opreme.

## Uporaba ukaza `encrypt`
  
Ukaz `encrypt` v CLI orodju ***digna*** se uporablja za šifriranje gesla.
  
### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenti
- **PASSWORD**: Geslo, ki ga je treba šifrirati (obvezno).
  
### Primer
  
Za šifriranje gesla ga je treba posredovati kot argument.   
Na primer, za šifriranje gesla `mypassword123` uporabite:
```bash
dignacli encrypt mypassword123
```
Ta ukaz izpiše šifrirano različico posredovanega gesla, ki jo lahko nato uporabite v varnih kontekstih. Če argument gesla ni podan, bo CLI prikazal napako o manjkajočem argumentu.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` se uporablja za generiranje Fernet-ključa, ki je potreben za zaščito gesel, shranjenih v repozitoriju ***digna***.
  
### Uporaba ukaza
```bash
dignacli generate-key
```
  
# Upravljanje podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` v CLI orodju ***digna*** se uporablja za brisanje profilov, napovedi in podatkov Traffic Light System za enega ali več virov podatkov v okviru navedenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov, saj pomaga ohranjati urejeno in učinkovito okolje z odstranjevanjem zastarelih ali nepotrebnih podatkov.

### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega želite izbrisati podatke (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira čez vse razpoložljive projekte in izvede ukaz.
- **FROM_DATE**: Datum in čas začetka brisanja podatkov. Dovoljene oblike vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Datum in čas konca brisanja podatkov, v enakih oblikah kot FROM_DATE (obvezno).
  
### Možnosti
  
- `--table-name`, `-tn`: Omeji operacijo čiščenja na določeno tabelo v okviru projekta.
- `--table-filter`, `-tf`: Filter za omejitev čiščenja na tabele, katerih ime vsebuje navedeno podniz.
- `--timing`, `-tm`: Po koncu izpiše trajanje postopka čiščenja.
- `--help`: Prikaže pomoč za ukaz clean-up in izstopi.
  
### Primer
  
Za brisanje podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za brisanje podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga upravljati shranjevanje podatkov in zagotavlja, da v repozitoriju ostanejo le relevantne informacije.

## Uporaba ukaza `inspect`

Ukaz `inspect` v CLI orodju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov Traffic Light System za enega ali več virov podatkov v okviru navedenega projekta. Ta ukaz pomaga analizirati in spremljati podatke za določeno obdobje.

### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega želite izvesti inšpekcijo podatkov (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira čez vse razpoložljive projekte in izvede ukaz.
- **FROM_DATE**: Datum in čas začetka inšpekcije podatkov. Dovoljene oblike vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Datum in čas konca inšpekcije podatkov, v enakih oblikah kot FROM_DATE (obvezno).
  
### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo v okviru projekta.
- `--table-filter`, `-tf`: Filtrira inšpekcijo samo na tabele, katerih ime vsebuje navedeno podniz.
- `--do-profile`: Zažene ponovni zbir profilov. Privzeto — do-profile.
- `--no-do-profile`: Onemogoči ponovni zbir profilov.
- `--do-prediction`: Zažene ponovno izračunavanje napovedi. Privzeto — do-prediction.
- `--no-do-prediction`: Onemogoči ponovno izračunavanje napovedi.
- `--do-alert-status`: Zažene ponovno izračunavanje statusov opozoril. Privzeto — do-alert-status.
- `--no-do-alert-status`: Onemogoči ponovno izračunavanje statusov opozoril.
- `--iterative`: Izvede inšpekcijo obdobja z dnevno iteracijo. Privzeto — iterative.
- `--no-iterative`: Izvede inšpekcijo celotnega obdobja v enem koraku.
- `--timing`, `-tm`: Po koncu prikaže trajanje postopka inšpekcije.
  
### Primer
  
Za inšpekcijo podatkov za projekt `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za inšpekcijo samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje integritete podatkov ter upravljanje sistema opozoril v okviru določenega časovnega obdobja projekta.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` v CLI orodju ***digna*** se uporablja za pridobitev statusa Traffic Light System (TLS) za določeno tabelo v projektu na naveden datum. Traffic Light System daje vpogled v stanje in kakovost podatkov ter opozarja na morebitne težave ali opozorila, ki zahtevajo pozornost.
  
### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se zahteva status TLS (obvezno).
- **TABLE_NAME**: Določena tabela v projektu, za katero je potreben status TLS (obvezno).
- **DATE**: Datum, za katerega se zahteva status TLS, običajno v formatu %Y-%m-%d (obvezno).
  
### Primer
  
Za preverjanje statusa TLS za tabelo UserData v projektu ProjectA na 1. julij 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov z zagotavljanjem jasnega in uporabnega poročila na podlagi vnaprej določenih meril.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej koristen za skrbnike in uporabnike, ki upravljajo več projektov, saj omogoča hiter pregled razpoložljivih projektov v repozitoriju ***digna***.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih virov podatkov v navedenem projektu. Ta ukaz je koristen za razumevanje podatkovnih virov, dostopnih za analizo in upravljanje v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se navajajo viri podatkov (obvezno).
  
### Primer
  
Za izpis vseh virov podatkov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom omogoča pregled virov podatkov, razpoložljivih v projektu, kar olajša navigacijo in upravljanje podatkovnega okolja.
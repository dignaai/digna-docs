---
title: digna CLI Reference 2024.11 – Ukazi in primeri | digna Dokumentacija
description: Celovit priročnik za digna CLI izdajo 2024.11. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-repo-connection, upgrade-repo, inspect, tls-status in drugi.
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Ta stran dokumentira celoten nabor ukazov, razpoložljivih v CLI orodju ***digna*** izdaje **2024.11**, vključno z uporabo in primeri ter možnostmi.


---
## Osnove CLI

---

## Uporaba možnosti `help`

Možnost `--help` prikaže informacije o razpoložljivih ukazih in njihovi uporabi. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite `--help` takoj za ključnim besedami ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Pridobitev pomoči za posamezne ukaze:**  
  
    Za podrobne informacije o določenem ukazu dodajte `--help` za tem ukazom.
    Na primer, za pomoč pri ukazu `add-user` zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### izhod:
      
     - **Opis ukaza:** Podaja podroben opis, kaj ukaz počne.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z obveznimi in neobveznimi argumenti.  
     - **Možnosti:** Seznam možnosti, specifičnih za ukaz, z razlagami.  
     - **Primeri:** Daje primere, kako učinkovito izvesti ukaz.  


## Uporaba ukaza `check-repo-connection`

Ukaz `check-repo-connection` je pripomoček v CLI orodju ***digna***, namenjen testiranju povezljivosti in dostopa do določenega repozitorija ***digna***. Ta ukaz zagotavlja, da CLI lahko komunicira z repozitorijem.
      
### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Ob uspešni izvedbi ukaz izpiše potrdilo o povezavi, skupaj s podrobnostmi o repozitoriju: verzija repozitorija, gostitelj, baza podatkov in shema.  
  
Če povezava z repozitorijem ni uspešna, preverite datoteko config.toml zaradi pravilnih nastavitev konfiguracije.

## Uporaba ukaza `version`

Za preverjanje nameščene različice *dignacli* uporabite možnost `--version`.  
  
### Uporaba ukaza
```bash
dignacli --version
```
  
### Primer izhoda
```bash
dignacli version 2024.11
```

## Uporaba možnosti za beleženje (logging)
  
Privzeto je izpis v konzoli za ukaze ***digna*** zasnovan minimalno. Večina ukazov ponuja možnost podajanja dodatnih informacij z naslednjimi možnostmi:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
”verbose” in ”debug” določata raven podrobnosti, medtem ko možnost ”logfile” omogoča preusmeritev izpisa v datoteko namesto na konzolo.

# Upravljanje uporabnikov

## Uporaba ukaza `add-user`
  
Ukaz `add-user` v CLI orodju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenti

- **USER_NAME**: Uporniško ime novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

### Možnosti

- `--is_superuser`, `-su`: Zastavica za označitev novega uporabnika kot skrbnika.
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni nastavljen, račun nima datuma poteka.

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
  
Ukaz `delete-user` v CLI orodju ***digna*** se uporablja za odstranjevanje obstoječega uporabnika iz sistema ***digna***.
  
### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
### Argumenti
- **USER_NAME**: Uporniško ime uporabnika, ki naj bo izbrisan (obvezno). To je edini argument, ki ga ta ukaz zahteva.

### Primer
```bash
dignacli delete-user jdoe
```
  
Izvajanje tega ukaza bo odstranilo uporabnika `jdoe` iz sistema ***digna***, preklicalo njegov dostop in izbrisalo povezane podatke ter dovoljenja iz repozitorija.

## Uporaba ukaza `modify-user`

Ukaz `modify-user` v CLI orodju ***digna*** se uporablja za posodobitev podatkov obstoječega uporabnika v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, ki ga želite spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuserja, kar mu podeli povišane privilegije. Ta zastavica ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni podan, račun ostane veljaven za nedoločen čas.  
  
### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in nastavitev uporabnika kot superuser:
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
  
- **USER_NAME**: Uporniško ime uporabnika, katerega geslo želite spremeniti (obvezno).
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

Izvedba tega ukaza v CLI orodju ***digna*** se poveže z repozitorijem ***digna*** in izpiše vse uporabnike, prikazano z njihovimi ID-ji, uporabniškimi imeni, polnimi imeni, statusom superuserja in časovnimi žigi poteka.

# Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` v CLI orodju ***digna*** se uporablja za nadgradnjo ali inicializacijo repozitorija ***digna***. Ta ukaz je ključen za uporabo posodobitev ali za prvo nastavitev infrastrukture repozitorija.
  
### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
### Možnosti
  
- `--simulation-mode`, `-s`: Ko je omogočeno, ta možnost zažene ukaz v simulacijskem načinu, ki izpiše SQL stavke, ki bi bili izvršeni, vendar jih dejansko ne izvede. To je uporabno za predogled sprememb brez spreminjanja repozitorija.  

  
### Primer
  
Za nadgradnjo repozitorija ***digna*** lahko zaženete ukaz brez dodatnih možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (ogled SQL stavkov brez njihove uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključnega pomena za vzdrževanje sistema ***digna*** in zagotavlja, da so shema baze podatkov in drugi repozitorijski elementi skladni z najnovejšo različico programske opreme.

## Uporaba ukaza `encrypt`
  
Ukaz `encrypt` v CLI orodju ***digna*** se uporablja za šifriranje gesla.
  
### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenti
- **PASSWORD**: Geslo, ki ga je treba šifrirati (obvezno).
  
### Primer
  
Za šifriranje gesla morate geslo posredovati kot argument.   
Na primer, za šifriranje gesla `mypassword123` uporabite:
```bash
dignacli encrypt mypassword123
```
Ukaz izpiše šifrirano različico podanega gesla, ki jo nato lahko uporabite v varnih kontekstih. Če argument gesla ni podan, bo CLI prikazal napako o manjkajočem argumentu.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` se uporablja za generiranje Fernet ključa, ki je ključnega pomena za varovanje gesel, shranjenih v repozitoriju ***digna***.
  
### Uporaba ukaza
```bash
dignacli generate-key
```
  
# Upravljanje podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` v CLI orodju ***digna*** se uporablja za odstranitev profilov, napovedi in podatkov sistema prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga ohranjati urejeno ter učinkovito okolje podatkov z odstranitvijo zastarelih ali nepotrebnih podatkov.

### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega naj bodo podatki odstranjeni (obvezno). Uporaba ključne besede `all-projects` v tem argumentu pomeni, da bo ***digna*** iteriral čez vse obstoječe projekte in uporabil ta ukaz.
- **FROM_DATE**: Začetni datum in čas za odstranjevanje podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za odstranjevanje podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
### Možnosti
  
- `--table-name`, `-tn`: Omeji operacijo čiščenja na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtri za omejitev čiščenja na tabele, ki vsebujejo navedeni podniz v svojih imenih.
- `--timing`, `-tm`: Prikaže trajanje postopka čiščenja po končani izvedbi.
- `--help`: Prikaže informacije pomoči za ukaz clean-up in izstopi.
  
### Primer
  
Za odstranitev podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranitev podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga pri upravljanju porabe prostora in zagotavlja, da repozitorij vsebuje le relevantne informacije.

## Uporaba ukaza `inspect`

Ukaz `inspect` v CLI orodju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem obdobju.

### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega naj bodo podatki pregledani (obvezno). Uporaba ključne besede `all-projects` v tem argumentu pomeni, da bo ***digna*** iteriral čez vse obstoječe projekte in uporabil ta ukaz.
- **FROM_DATE**: Začetni datum in čas za pregled podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za pregled podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
### Možnosti

- `--table-name`, `-tn`: Omeji pregled na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira pregled samo na tabele, ki vsebujejo navedeni podniz v svojih imenih.
- `--do-profile`: Sproži ponovno zbiranje profilov. Privzeto je do-profile.
- `--no-do-profile`: Onemogoči ponovno zbiranje profilov.
- `--do-prediction`: Sproži ponovno izračunavanje napovedi. Privzeto je do-prediction.
- `--no-do-prediction`: Onemogoči ponovno izračunavanje napovedi.
- `--do-alert-status`: Sproži ponovno izračunavanje stanj opozoril. Privzeto je do-alert-status.
- `--no-do-alert-status`: Onemogoči ponovno izračunavanje stanj opozoril.
- `--timing`, `-tm`: Prikaže trajanje postopka pregleda po končani izvedbi.
  
### Primer
  
Za pregled podatkov projekta `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za pregled samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje integritete podatkov ter upravljanje sistemov opozoril znotraj določenega časovnega okvira projekta.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` v CLI orodju ***digna*** se uporablja za poizvedbo o stanju Sistema prometnih luči (Traffic Light System, TLS) za določeno tabelo v projektu na določen datum. Sistem prometnih luči daje vpogled v zdravje in kakovost podatkov ter opozorila, ki lahko zahtevajo ukrepanje.
  
### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se poizveduje stanje TLS (obvezno).
- **TABLE_NAME**: Določena tabela znotraj projekta, za katero je potreben status TLS (obvezno).
- **DATE**: Datum, za katerega se poizveduje stanje TLS, običajno v formatu %Y-%m-%d (obvezno).
  
### Primer
  
Za preverjanje stanja TLS za tabelo z imenom UserData v projektu ProjectA na dan 1. julija 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov z jasnim in izvedljivim poročilom o stanju glede na vnaprej določena merila.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj nudi hiter pregled razpoložljivih projektov v repozitoriju ***digna***.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih virov podatkov znotraj določenega projekta. Ta ukaz je uporaben za razumevanje podatkovnih virov, razpoložljivih za analizo in upravljanje v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se izpisujejo viri podatkov (obvezno).
  
### Primer
  
Za izpis vseh virov podatkov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled nad viri podatkov, razpoložljivimi v projektu, in jim pomaga pri navigaciji ter upravljanju podatkovnega okolja.
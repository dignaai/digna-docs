---
title: Referenca digna CLI 2024.11 – ukazi in primeri | Dokumentacija digna
description: Popolna referenca za digna CLI izdajo 2024.11. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-repo-connection, upgrade-repo, inspect, tls-status in več.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Ta stran dokumentira celoten nabor ukazov, ki so na voljo v CLI orodju ***digna*** različice **2024.11**, vključno s primeri uporabe in možnostmi.


---
## Osnove CLI

---

## Uporaba opcije `help`

Opcija `--help` zagotavlja informacije o razpoložljivih ukazih in njihovi uporabi. Obstajata dva glavna načina uporabe te opcije:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help takoj po ključni besedi ***digna***  
   ```bash
   dignacli --help
   ```

3.  **Pridobitev pomoči za posamezne ukaze:**  
  
    Za podrobne informacije o posameznem ukazu dodajte `--help` za tem ukazom.
    Na primer, če želite pomoč za ukaz `add-user`, zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### Izhod:
      
     - **Opis ukaza:** Podrobno pojasnjuje, kaj ukaz počne.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z obveznimi in neobveznimi argumenti.  
     - **Možnosti:** Navedene so možnosti, specifične za ukaz, skupaj z razlagami.  
     - **Primeri:** Ponuja primere učinkovite uporabe ukaza.

  
## Uporaba ukaza `check-repo-connection`

Ukaz check-repo-connection je pripomoček v CLI orodju ***digna***, namenjen preverjanju dosegljivosti in povezave z navedenim repozitorijem ***digna***. Ta ukaz zagotavlja, da lahko CLI komunicira z repozitorijem.
      
### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Po uspešnem izvajanju ukaz izpiše potrdilo o povezavi skupaj s podrobnostmi o repozitoriju: različico repozitorija, gostitelja, bazo podatkov in shemo.  
  
Če povezave z repozitorijem ni mogoče vzpostaviti, preverite datoteko config.toml glede pravilnosti nastavitev.

## Uporaba ukaza ‘version’

Za preverjanje nameščene različice *dignacli* uporabite opcijo --version.  
  
### Uporaba ukaza
```bash
dignacli --version
```
  
### Primer izhoda
```bash
dignacli version 2024.11
```

## Uporaba možnosti beleženja (logging)
  
Privzeto je izpis ukazov ***digna*** minimalen. Večina ukazov omogoča izpis dodatnih informacij z naslednjimi možnostmi:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
»verbose« in »debug« določata stopnjo podrobnosti, medtem ko stikalo »logfile« omogoča preusmeritev izpisa v datoteko namesto v konzolo.

# Upravljanje uporabnikov

## Uporaba ukaza ‘add-user’
  
Ukaz add-user v CLI orodju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenti

- **USER_NAME**: Uporniško ime za nov račun (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

### Možnosti

- `--is_superuser`, `-su`: Oznaka, da je novi uporabnik skrbnik.
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni naveden, račun nima datuma poteka.

### Primer

Da dodate novega uporabnika z uporabniškim imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Da dodate novega uporabnika in nastavite datum poteka računa:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Uporaba ukaza `delete-user`
  
Ukaz `delete-user` v CLI orodju ***digna*** se uporablja za izbris obstoječega uporabnika iz sistema ***digna***.
  
### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
### Argumenti
- **USER_NAME**: Uporniško ime uporabnika, ki ga je treba izbrisati (obvezno). To je edini argument, ki ga ukaz zahteva.

### Primer
```bash
dignacli delete-user jdoe
```
  
Izvedba tega ukaza bo izbrisala uporabnika `jdoe` iz sistema ***digna***, razveljavila njegov dostop in odstranila povezane podatke ter pravice iz repozitorija.

## Uporaba ukaza `modify-user`

Ukaz `modify-user` v CLI orodju ***digna*** se uporablja za posodabljanje podatkov obstoječega uporabnika v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, ki ga želite spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
### Možnosti  
  
- `--is_superuser`, `-su`: Oznaka, da je uporabnik superuporabnik, kar mu podeli povišane privilegije. Ta zastavica ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Nastavi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven za nedoločen čas.  
  
### Primer
  
Da spremenite polno ime uporabnika `jdoe` v “Johnathan Doe” in mu dodelite vlogo superuporabnika:
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
  
- **USER_NAME**: Uporniško ime uporabnika, za katerega želite spremeniti geslo (obvezno).
- **USER_PWD**: Novo geslo za uporabnika (obvezno).
  
### Primer
  
Da spremenite geslo uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Uporaba ukaza `list-users`

Ukaz `list-users` v CLI orodju ***digna*** prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

### Uporaba ukaza

```bash
dignacli list-users
```

Izvedba tega ukaza se bo v CLI orodju ***digna*** povezala z repozitorijem ***digna*** in izpisala seznam vseh uporabnikov, prikazala njihove ID-je, uporabniška imena, polna imena, status superuporabnika ter časovne oznake poteka.

# Upravljanje repozitorija

### Uporaba ukaza `upgrade-repo`
  
Ukaz `upgrade-repo` v CLI orodju ***digna*** se uporablja za posodobitev ali inicializacijo repozitorija ***digna***. Ta ukaz je potreben za uporabo posodobitev ali za prvo nastavitev infrastrukture repozitorija.
  
### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
### Možnosti
  
- `--simulation-mode`, `-s`: Če je omogočeno, ta možnost zažene ukaz v simulacijskem načinu, ki izpiše SQL ukaze, ki bi bili izvršeni, vendar jih dejansko ne izvrši. To je koristno za pregled sprememb brez njihovega apliciranja v repozitorij.  

  
### Primer
  
Za posodobitev repozitorija ***digna*** lahko zaženete ukaz brez možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon posodobitve v simulacijskem načinu (da vidite SQL ukaze brez njihove uporabe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključnega pomena za vzdrževanje sistema ***digna***, saj zagotavlja, da sta shema baze podatkov in drugi sestavni deli repozitorija posodobljeni skladno z zadnjo verzijo programske opreme.

## Uporaba ukaza `encrypt`
  
Ukaz `encrypt` v CLI orodju ***digna*** se uporablja za šifriranje gesla.
  
### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenti
- **PASSWORD**: Geslo, ki ga je treba šifrirati (obvezno).
  
### Primer
  
Za šifriranje gesla je potrebno geslo posredovati kot argument.   
Na primer, za šifriranje gesla `mypassword123` uporabite:
```bash
dignacli encrypt mypassword123
```
Ta ukaz bo izpisal šifrirano različico posredovanega gesla, ki jo lahko nato uporabite v varnih kontekstih. Če argument gesla ni podan, bo CLI izpisal napako z opozorilom o manjkajočem argumentu.

## Uporaba ukaza `generate-key`
  
Ukaz `generate-key` se uporablja za generiranje Fernet-ključa, ki je potreben za zaščito gesel, shranjenih v repozitoriju ***digna***.
  
### Uporaba ukaza
```bash
dignacli generate-key
```
  
# Upravljanje podatkov

## Uporaba ukaza `clean-up`

Ukaz `clean-up` v CLI orodju ***digna*** se uporablja za brisanje profilov, napovedi in podatkov sistema semaforjev za enega ali več virov podatkov v navedenem projektu. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga ohranjati urejeno in učinkovito okolje z odstranjevanjem zastarelih ali nepotrebnih podatkov.

### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega želite izbrisati podatke (obvezno). Uporaba ključne besede all-projects v tem argumentu nakaže ***digna***, da naj iterira po vseh obstoječih projektih in uporabi ukaz.
- **FROM_DATE**: Datum in čas začetka brisanja podatkov. Dovoljeni formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Datum in čas konca brisanja podatkov, v istih formatih kot FROM_DATE (obvezno).
  
### Možnosti
  
- `--table-name`, `-tn`: Omeji operacijo čiščenja na določeno tabelo v projektu.
- `--table-filter`, `-tf`: Filter za omejitev čiščenja na tabele, katerih imena vsebujejo dano podniz.
- `--timing`, `-tm`: Prikaže trajanje procesa čiščenja po zaključku.
- `--help`: Prikaže pomoč za ukaz clean-up in zaključi izvajanje.
  
### Primer
  
Za izbris podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za izbris podatkov samo iz določene tabele z imenom `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga pri upravljanju shranjevanja podatkov in zagotavlja, da v repozitoriju ostanejo le relevantne informacije.

## Uporaba ukaza `inspect`

Ukaz `inspect` v CLI orodju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema semaforjev za enega ali več virov podatkov v navedenem projektu. Ta ukaz pomaga analizirati in spremljati podatke za določen časovni razpon.

### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega želite inšpektirati podatke (obvezno). Uporaba ključne besede all-projects v tem argumentu nakaže ***digna***, da naj iterira po vseh obstoječih projektih in uporabi ukaz.
- **FROM_DATE**: Datum in čas začetka inšpekcije podatkov. Dovoljeni formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Datum in čas konca inšpekcije podatkov, v istih formatih kot FROM_DATE (obvezno).
  
### Možnosti

- `--table-name`, `-tn`: Omeji inšpekcijo na določeno tabelo v projektu.
- `--table-filter`, `-tf`: Filtrira inšpekcijo le na tabele, katerih ime vsebuje določeni podniz.
- `--do-profile`: Zažene ponovni zagon zbiranja profilov. Privzeto do-profile.
- `--no-do-profile`: Onemogoči ponovni zagon zbiranja profilov.
- `--do-prediction`: Zažene ponovno izračunavanje napovedi. Privzeto do-prediction.
- `--no-do-prediction`: Onemogoči ponovno izračunavanje napovedi.
- `--do-alert-status`: Zažene ponovno izračunavanje statusov opozoril. Privzeto do-alert-status.
- `--no-do-alert-status`: Onemogoči ponovno izračunavanje statusov opozoril.
- `--timing`, `-tm`: Prikaže trajanje procesa inšpekcije po zaključku.
  
### Primer
  
Za inšpekcijo podatkov za projekt `ProjectA` od 1. januarja 2024 do 31. januarja 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za inšpekcijo samo določene tabele in prisilno ponovni izračun napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, nadzor integritete podatkov ter upravljanje sistema opozoril znotraj navedenega obdobja projekta.

## Uporaba ukaza `tls-status`

Ukaz `tls-status` v CLI orodju ***digna*** se uporablja za poizvedbo o statusu Traffic Light System (TLS) za določeno tabelo v projektu na izbrani datum. Sistem semaforjev ponuja pregled stanja in kakovosti podatkov, ter opozarja na težave ali alarmne stanje, ki potrebujejo pozornost.
  
### Uporaba ukaza
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se zahteva TLS status (obvezno).
- **TABLE_NAME**: Določena tabela v projektu, za katero je potreben TLS status (obvezno).
- **DATE**: Datum, za katerega se zahteva TLS status, običajno v formatu %Y-%m-%d (obvezno).
  
### Primer
  
Za preverjanje TLS statusa za tabelo z imenom UserData v projektu ProjectA na 1. julij 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov, saj nudi jasne in koristne poročila o statusu glede na vnaprej določena merila.

## Uporaba ukaza `list-projects`
  
Ukaz `list-projects` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj hitro prikaže razpoložljive projekte v repozitoriju ***digna***.

## Uporaba ukaza `list-ds`

Ukaz `list-ds` v CLI orodju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih virov podatkov v navedenem projektu. Ta ukaz je koristen za spoznavanje podatkovnih virov, ki so na voljo za analizo in upravljanje v sistemu ***digna***.

### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se naštejejo viri podatkov (obvezno).
  
### Primer
  
Za seznam vseh virov podatkov v projektu z imenom `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz uporabnikom nudi pregled virov podatkov, ki so na voljo v projektu, kar pomaga pri učinkovitejšem orientiranju in upravljanju podatkovnega okolja.
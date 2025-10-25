---
title: digna CLI Referenca 2025.09 – Ukazi in primeri | digna Dokumentacija
description: Celovita referenca za digna CLI različico 2025.09. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi add-user, check-config, check-repo-connection, inspect, inspect-async in drugimi.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# digna CLI Referenca 2025.09
**2025-09-29**

Ta stran dokumentira vse ukaze, primere uporabe in možnosti, ki so na voljo z različico **digna** CLI **2025.09**.

---

## Osnove CLI

---

### help
Možnost `--help` prikaže informacije o razpoložljivih ukazih in uporabi. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Po besedi `***digna***` uporabite `--help`  
   ```bash
   dignacli --help
   ```

2. **Pridobitev pomoči za določen ukaz:**  
  
    Za podrobne informacije o posameznem ukazu dodajte `--help` k temu ukazu.  
    Na primer, če želite pomoč za ukaz `add-user`, zaženite:
     ```bash
     dignacli add-user --help
     ```

     ### izpis:
      
     - **Opis ukaza:** Pojasni, kaj ukaz počne.  
     - **Sintaksa:** Prikaže celotno sintakso vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Našteje možnosti specifične za ukaz in njihove opise.  
     - **Primeri:** Poda primere, kako ukaz učinkovito uporabiti.

### check-config

Ukaz check-config je pripomoček v ***digna*** CLI za testiranje konfiguracije ***digna***. Ta ukaz preveri, ali komponentam ***digna*** v config.toml obstajajo zahtevani konfiguracijski elementi.

#### Možnosti

- `--configpath`, `-cp`: Datoteka ali imenik s konfiguracijo. Če je izpuščeno, bo uporabljena ../config.toml.
      
#### Uporaba ukaza
```bash
dignacli check-config
```

Ob uspešni izvedbi ukaz izpiše potrditev, da je konfiguracija popolna.  
  
Če se zdi, da konfiguracija manjka, bodo izpisani manjkajoči konfiguracijski elementi.

  
### check-repo-connection

Ukaz check-repo-connection je pripomoček v ***digna*** CLI za testiranje povezave in dostopa do navedenega ***digna*** repozitorija. Ta ukaz zagotovi, da lahko CLI komunicira z repozitorijem.
      
#### Uporaba ukaza
```bash
dignacli check-repo-connection
```

Ob uspešni izvedbi ukaz potrdi povezavo in izpiše naslednje informacije o repozitoriju: Repository version, Host, Database in Schema.  
  
Če povezava z repozitorijem ni uspešna, preverite, ali so pravilne konfiguracijske nastavitve v datoteki config.toml.


### version

Uporabite možnost `--version` za preverjanje nameščene različice *dignacli*.  
  
#### Uporaba ukaza
```bash
dignacli --version
```
  
#### Primer izpisa
```bash
dignacli version 2025.09
```

### možnosti beleženja (logging)
  
Privzeto je izpis ukazov ***digna*** na konzoli zasnovan minimalistično. Večina ukazov omogoča dodatne informacije z naslednjimi možnostmi:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
Možnosti “verbose” in “debug” določajo raven podrobnosti, medtem ko možnost “logfile” preusmeri izpis v datoteko namesto na konzolo.

## Upravljanje uporabnikov

### add-user
  
Ukaz add-user doda novega uporabnika v sistem ***digna*** prek ***digna*** CLI.
  
#### Uporaba ukaza
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenti

- **USER_NAME**: Uporabniško ime novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

#### Možnosti

- `--is_superuser`, `-su`: Zastavica za dodelitev uporabnika kot superuser.
- `--valid_until`, `-vu`: Določi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni naveden, račun nima datuma poteka.

#### Primer

Za dodajanje uporabnika z uporabniškim imenom `jdoe`, polnim imenom `John Doe` in geslom `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Za dodajanje uporabnika in določitev datuma poteka računa:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Ukaz `delete-user` odstrani obstoječega uporabnika iz sistema ***digna*** prek ***digna*** CLI.
  
#### Uporaba ukaza
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenti
- **USER_NAME**: Uporabniško ime uporabnika, ki se bo izbrisal (obvezno). To je edini zahtevan argument ukaza.

#### Primer
```bash
dignacli delete-user jdoe
```
  
Ko se ukaz izvede, bo uporabnik `jdoe` odstranjen iz sistema ***digna***; njegov dostop bo preklican, povezani podatki in dovoljenja v repozitoriju pa bodo izbrisani.

### modify-user

Ukaz `modify-user` posodobi podatke obstoječega uporabnika v ***digna*** prek CLI.

#### Uporaba ukaza
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, ki se bo posodobil (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Nastavi uporabnika kot superuser, kar mu daje povišane privilegije. Ta zastavica ne zahteva vrednosti.  
- `--valid_until`, `-vu`: Določi datum poteka računa v formatu `YYYY-MM-DD HH:MI:SS`. Če ni priložen, račun ostane veljaven brez omejitve.  
  
#### Primer
  
Za spremembo polnega imena uporabnika `jdoe` v “Johnathan Doe” in dodelitev superuser pravic:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Ukaz `modify-user-pwd` spremeni geslo obstoječega uporabnika v ***digna*** prek CLI.
  
#### Uporaba ukaza
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, katerega geslo se bo spremenilo (obvezno).
- **USER_PWD**: Novo geslo uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika `jdoe` v `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Ukaz `list-users` prikaže seznam vseh registriranih uporabnikov v sistemu ***digna*** prek CLI.

#### Uporaba ukaza

```bash
dignacli list-users
```

Ko se ukaz izvede, se poveže z ***digna*** repozitorijem in izpiše vse uporabnike skupaj z ID, uporabniškim imenom, polnim imenom, stanjem superuser ter časovnimi žigi poteka.

## Upravljanje repozitorija

### upgrade-repo
  
Ukaz `upgrade-repo` se uporablja v ***digna*** CLI za nadgradnjo ali inicializacijo ***digna*** repozitorija. Ta ukaz je potreben za uporabo posodobitev ali prvo nastavitev repozitorija.
  
#### Uporaba ukaza

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Če je vklopljeno, ukaz teče v simulacijskem načinu; izpiše SQL ukaze, ki bi bili izvedeni, vendar jih dejansko ne izvede. To je koristno za predogled sprememb brez njihove izvedbe.  

  
#### Primer
  
Lahko zaženete nadgradnjo ***digna*** repozitorija brez možnosti:
  
```bash
dignacli upgrade-repo
```  
Za zagon nadgradnje v simulacijskem načinu (ogled SQL ukazov brez izvedbe):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ta ukaz je ključen pri vzdrževanju sistema ***digna*** in zagotavlja, da je shema baze podatkov ter ostale komponente repozitorija skladne z najnovejšo različico programske opreme.

### encrypt
  
Ukaz `encrypt` v ***digna*** CLI šifrira geslo.
  
#### Uporaba ukaza
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Geslo, ki ga je treba šifrirati (obvezno).
  
#### Primer
  
Geslo je treba posredovati kot argument za šifriranje.   
Na primer, za šifriranje gesla `mypassword123`:
```bash
dignacli encrypt mypassword123
```
Ukaz izpiše šifrirano različico posredovanega gesla; ta rezultat je primeren za uporabo v varnejših kontekstih. Če argument gesla ni podan, CLI prikaže napako zaradi manjkajočega argumenta.

### generate-key
  
Ukaz `generate-key` ustvari Fernet ključ; ta ključ je potreben za varno shranjevanje gesel v ***digna*** repozitoriju.
  
#### Uporaba ukaza
```bash
dignacli generate-key
```
  
## Upravljanje podatkov

### clean-up

Ukaz `clean-up` v ***digna*** CLI odstrani profile, napovedi in podatke sistema prometnih lučk (traffic light) za enega ali več virov podatkov v okviru navedenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov; čiščenje starih ali nepotrebnih podatkov pomaga ohranjati urejeno in učinkovito okolje.

#### Uporaba ukaza

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega bodo podatki odstranjeni (obvezno). Če se kot ta argument uporabi ključna beseda all-projects, bo ***digna*** iteriral skozi vse obstoječe projekte in izvedel ukaz za vsakogar.
- **FROM_DATE**: Začetni datum in čas za brisanje podatkov. Sprejemljivi formati so %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za brisanje podatkov; uporablja iste formate kot FROM_DATE (obvezno).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omeji čiščenje na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Filtrira tabele glede na podniz, ki se pojavi v njihovih imenih.
- `--timing`, `-tm`: Prikaz trajanja operacije po zaključenem čiščenju.
- `--help`: Prikaže pomoč za ukaz clean-up in izstopi.
  
#### Primer
  
Za odstranitev podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Za odstranitev podatkov samo iz določene tabele `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ta ukaz pomaga upravljati porabo prostora za shranjevanje in zagotavlja, da repozitorij vsebuje le relevantne informacije.

### remove-orphans
  
Ukaz `remove-orphans` se uporablja za vzdrževalna opravila v ***digna*** CLI.  
Ko uporabniki izbrišejo projekte ali vire podatkov, lahko profili in napovedi ostanejo v repozitoriju kot sirote. Ta ukaz odstrani takšne sirote iz repozitorija.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

### list-projects
  
Ukaz `list-projects` prikaže seznam vseh obstoječih projektov v ***digna*** prek CLI.
  
#### Uporaba ukaza
  
```bash
dignacli list-projects
```

Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov; hitro prikaže povzetek projektov, ki so trenutno v repozitoriju ***digna***.

### list-ds

Ukaz `list-ds` v ***digna*** CLI navaja vse obstoječe vire podatkov v navedenem projektu. Ta ukaz pomaga razumeti razpoložljive podatkovne vire za analizo in upravljanje.

#### Uporaba ukaza
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se navajajo viri podatkov (obvezno).
  
#### Primer
  
Za navajanje vseh virov podatkov v projektu `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ta ukaz ponudi pregled razpoložljivih virov podatkov v projektu, kar olajša njihovo upravljanje in navigacijo.


### inspect

Ukaz `inspect` v ***digna*** CLI ustvari profile, napovedi in podatke sistema prometnih lučk za enega ali več virov podatkov v okviru navedenega projekta. Ta ukaz analizira in spremlja podatke za določeno obdobje. Po zaključku pregleda vrne vrednost sistema prometnih lučk:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Uporaba ukaza

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, čigar podatki bodo pregledani (obvezno). Če se uporabi ključna beseda all-projects, bo ***digna*** iteriral skozi vse obstoječe projekte in izvedel ukaz za vsak.
- **FROM_DATE**: Začetni datum in čas za pregled podatkov. Sprejemljivi formati so %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za pregled podatkov; uporablja iste formate kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji pregled na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Izvede pregled na tabelah, katerih imena vsebujejo naveden podniz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestila v primeru opozorila.
- `--bypass-backend`, `-bb`: Onemogoči backend in izvede pregled neposredno iz CLI (samo za testiranje!).

  
#### Primer
  
Za pregled podatkov v projektu `ProjectA` med 1. januarjem 2024 in 31. januarjem 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Za pregled samo določene tabele in prisilno ponovno izračunanje napovedi:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ta ukaz je koristen za ustvarjanje posodobljenih profilov in napovedi, spremljanje integritete podatkov ter upravljanje sistemov opozarjanja za zadevno časovno okno projekta.

### inspect-async

Ukaz `inspect-async` v ***digna*** CLI ustvari profile, napovedi in podatke sistema prometnih lučk za enega ali več virov podatkov v okviru navedenega projekta. Ta ukaz analizira in spremlja podatke za določeno obdobje. V nasprotju z ukazom `inspect` ta ukaz ne čaka na dokončanje pregleda.  
Namesto tega vrne request id za poslan zahtevek pregleda. Napredek pregleda lahko preverite z ukazom `inspect-status`.

#### Uporaba ukaza

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, čigar podatki bodo pregledani (obvezno). Če se uporabi ključna beseda all-projects, bo ***digna*** iteriral skozi vse obstoječe projekte in izvedel ukaz za vsak.
- **FROM_DATE**: Začetni datum in čas za pregled podatkov. Sprejemljivi formati so %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za pregled podatkov; uporablja iste formate kot FROM_DATE (obvezno).
  
#### Možnosti

- `--table-name`, `-tn`: Omeji pregled na določeno tabelo znotraj projekta.
- `--table-filter`, `-tf`: Izvede pregled na tabelah, katerih imena vsebujejo naveden podniz.
- `--enable_notification`, `-en`: Omogoči pošiljanje obvestila v primeru opozorila.

  
#### Primer
  
Za asinkron pregled podatkov v projektu `ProjectA` med 1. januarjem 2024 in 31. januarjem 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Ukaz `inspect-status` preveri napredek asinhronega pregleda na podlagi request ID v ***digna*** CLI.

#### Uporaba ukaza

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenti
  
- **REQUEST_ID**: Request id, ki ga je vrnil ukaz `inspect-async`.
  
#### Primer
  
Za preverjanje napredka pregleda z request ID 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Ukaz `inspect-cancel` prekliče posamezne ali vse obstoječe zahteve za pregled na podlagi request ID v ***digna*** CLI.

#### Uporaba ukaza

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenti
  
- **REQUEST_ID**: Request id, ki ga je vrnil ukaz `inspect-async`. 
  
#### Primer
  
Za preklic pregleda z request ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Za preklic vseh trenutno tečečih ali čakajočih zahtev:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Ukaz `export-ds` ustvari izvoz virov podatkov v ***digna*** CLI. Privzeto se izvozijo vsi viri podatkov v navedenem projektu.

#### Uporaba ukaza
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, iz katerega bodo viri podatkov izvoženi.

#### Možnosti

- `--table_name`, `-tn`: Izvozi določen vir podatkov iz projekta.
- `--exportfile`, `-ef`: Določi ime datoteke za izvoz.
    
#### Primer
  
Za izvoz vseh virov podatkov iz projekta `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ta ukaz izvozi vse vire podatkov iz `ProjectA` v JSON dokument, ki ga je mogoče uvoziti v drug projekt ali v ***digna*** repozitorij.


### import-ds

Ukaz `import-ds` v ***digna*** CLI uvozi vire podatkov iz izvoznega datoteke v ciljni projekt in ustvari poročilo o uvozu.

#### Uporaba ukaza
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, v katerega bodo viri podatkov uvoženi.
- **EXPORT_FILE**: Ime izvoznega datoteke, ki vsebuje vire podatkov za uvoz.

#### Možnosti

- `--output-file`, `-o`: Datoteka, v katero bo shranjeno poročilo o uvozu (če ni navedeno, se poročilo izpiše kot tabela v terminalu).
- `--output-format`, `-f`: Format poročila o uvozu (json, csv).
    
#### Primer
  
Za uvoz vseh virov podatkov iz datoteke `my_export.json` v `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po uvozu ukaz prikaže poročilo o uvoženih in preskočenih objektih. V `ProjectB` bodo uvoženi le novi viri podatkov. Za pregled, kateri objekti bodo uvoženi in kateri preskočeni, uporabite ukaz `plan-import-ds`.

### plan-import-ds

Ukaz `plan-import-ds` v ***digna*** CLI analizira izvozno datoteko in pripravi načrt, kateri viri podatkov bodo uvoženi v ciljni projekt in kateri bodo preskočeni.

#### Uporaba ukaza
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Ime ciljne projekte, za katerega se analizira uvoz.
- **EXPORT_FILE**: Ime izvoznega datoteke, ki se bo analizirala pred uvozom.

#### Možnosti

- `--output-file`, `-o`: Datoteka, v katero bo shranjeno poročilo načrta uvoza (če ni navedeno, se poročilo izpiše kot tabela v terminalu).
- `--output-format`, `-f`: Format poročila načrta uvoza (json, csv).
    
#### Primer
  
Za preverjanje, kateri viri podatkov iz `my_export.json` bodo uvoženi v `ProjectB` in kateri bodo preskočeni:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ta ukaz prikaže samo načrt uvoza z objekti, ki bodo uvoženi in tistimi, ki bodo preskočeni.
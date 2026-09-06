# digna CLI referencia 2026.06
**2026-09-05**

Ez az oldal a ***digna*** CLI **2026.06** kiadásában elérhető parancsok teljes körét dokumentálja, használati példákkal és beállításokkal együtt.

A futtatható állomány neve `digna`.

---

## A CLI alapjai

---

### Áttekintés és szintaxis

A **2026.06** kiadás CLI-je strukturált, kategóriaalapú parancshierarchiát használ:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

A `version` és a `serve` önálló parancsok, alparancs nélkül:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Globális beállítások

A következő globális beállítások minden parancsra érvényesek:

- `--help`, `-h`: Súgóinformációt jelenít meg a CLI-ről vagy egy adott parancskategóriáról, illetve alparancsról.
- `--stacktrace`: Hiba esetén a teljes hibaláncot jeleníti meg a legfelső szintű üzenet helyett.

A `--stacktrace` szigorú értelemben globális beállítás: a parancskategória **elé** kell írni, nem utána.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Nincs `--version` kapcsoló. Használja helyette a [`version`](#version) parancsot.

### Előfeltételek

A legtöbb parancshoz olvasható, érvényes `config.toml` szükséges; egyeseknek ezen felül érvényes licenc is kell.
Az alábbi táblázat rögzíti, hogy az egyes parancskategóriák mit töltenek be, mielőtt bármit is tennének:

| Parancskategória | Szükséges hozzá a `config.toml` | Szükséges hozzá érvényes licenc |
|---|---|---|
| `version` | nem | nem |
| `config check` | nem (éppen ez az, amiről a parancs jelentést ad) | nem |
| `license check` | nem | ez *maga* az ellenőrzés |
| `crypt` | igen | nem |
| `serve` | igen | nem |
| `project` | igen | nem |
| `user` | igen | igen |
| `inspection` | igen | igen |
| `repo` | igen | igen |

Ahol licenc szükséges, ott az aláírását és a lejárati dátumát egyaránt ellenőrzi a rendszer, és a parancs még azelőtt megszakad, hogy hozzányúlna a tárolóhoz, ha bármelyik ellenőrzés sikertelen.

### Kilépési kódok

- `0`: a parancs sikeres volt.
- `1`: a parancs meghiúsult. A hibaüzenet a stderr kimenetre kerül, `Error: ` előtaggal.

### help

A `--help` beállítás az elérhető parancskategóriákról, alparancsokról és beállításokról nyújt információt:

1. **Általános súgó megjelenítése:**
   ```bash
   digna --help
   ```

2. **Súgó lekérése adott kategóriákhoz és parancsokhoz:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **A kimenet tartalmazza:**
   - **A parancs leírását:** A parancs céljának összefoglalását.
   - **A szintaxist:** A kötelező és opcionális argumentumokat.
   - **A beállításokat:** A parancsra jellemző kapcsolókat és paramétereket.

### version

A `version` parancs kiírja a telepített ***digna*** kiadást. Nem olvas be konfigurációt és nem ellenőriz licencet, így olyan telepítésen is működik, amelynek a `config.toml` fájlja vagy licence hiányzik, illetve érvénytelen.

A kiadás verziója független a tároló sémájának verziójától, amelyet a [`repo check`](#repo-check) jelent.

#### A parancs használata
```bash
digna version
```

#### Példakimenet
```text
2026.06
```

---

## Konfigurációkezelés

---

### config check

A `config check` parancs ellenőrzi a konfigurációs fájlt (`config.toml`), meggyőződve arról, hogy minden kötelező szakasz és beállítás jelen van és megfelelően formázott. Minden szakasz külön kerül ellenőrzésre, így egy hibás `[app]` szakasz nem fedi el a `[repo]` állapotát.

A jelentésben szereplő szakaszok:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — opcionális; a hiányzó kulcs átmegy az ellenőrzésen, a jelen lévő, de hibás formátumú lista viszont megbukik

A parancs szándékosan nem úgy tölti be az alkalmazás konfigurációját, ahogyan a többi parancs, hogy olyan `config.toml` fájlt is diagnosztizálni tudjon, amely a ***digna*** elindulását teljesen megakadályozná.

#### A parancs használata
```bash
digna config check [OPTIONS]
```

#### Beállítások
- `--configpath`, `-c`: A konfigurációs fájl vagy a `config.toml` fájlt tartalmazó könyvtár elérési útja (alapértelmezés: `./config.toml`).
- `--json`: Az ellenőrzési jelentést JSON formátumban adja ki. Elsőbbséget élvez a `--quiet` beállítással szemben.
- `--quiet`, `-q`: Elnyomja a jelentést, és kizárólag a kilépési kódra hagyatkozik.

#### Példa
```bash
digna config check
```

Adott konfigurációs fájl ellenőrzése és a kimenet JSON formátumban:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Példakimenet
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

A hiányzó fájl vagy a TOML szintaktikai hiba nem hagy semmit, amit szakaszonként ellenőrizni lehetne, ezért egyetlen hibaként jelenik meg jelentés helyett, függetlenül a `--quiet` vagy `--json` beállítástól.

---

## Tárolókezelés

---

### repo check

A `repo check` parancs teszteli az adatbázis-kapcsolatot, és ellenőrzi a tároló telepítését és verzióját. Meghiúsul, ha a beállított séma nem létezik, vagy ha létezik ugyan, de nem tartalmaz ***digna*** tárolót.

A jelentett verzió a tároló sémájának verziója, amely a [`version`](#version) által kiírt ***digna*** kiadástól függetlenül van verziózva.

#### A parancs használata
```bash
digna repo check
```

#### Példakimenet
```text
Repo version 3.0.0 installed
```

### repo install

A `repo install` parancs új ***digna*** tárolót telepít a `config.toml` fájlban beállított sémába, létrehozva minden szükséges szekvenciát, táblát, indexet, megszorítást és kezdeti rekordot.

Magát a sémát ez a parancs **nem** hozza létre — annak előzetesen léteznie kell. A parancs továbbá megtagadja a futást, ha az adott sémában már van telepített tároló, és a [`repo upgrade`](#repo-upgrade) parancsra irányít, ha a telepített verzió régebbi.

#### A parancs használata
```bash
digna repo install
```

#### Példakimenet
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

A `repo upgrade` parancs adatbázisséma-migrációkat alkalmaz, hogy a meglévő tárolót a telepített kiadás által elvárt verzióra emelje. A frissítések rögzített frissítési útvonal mentén, egyszerre egy verzióugrással kerülnek alkalmazásra, és minden befejezett ugrás rögzül a tárolóban.

Ha a tároló már az elvárt verzión van, a parancs jelzi, hogy nincs szükség frissítésre, és nem hajt végre változtatást.

#### A parancs használata
```bash
digna repo upgrade
```

#### Példakimenet
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Titkosításkezelés

---

### crypt gen-key

A `crypt gen-key` parancs új AES-GCM titkosítókulcsot állít elő, amelyet a `config.toml` fájlban titkosítókulcsként lehet használni. Betölthető `config.toml` fájlnak már léteznie kell, még akkor is, ha az előállított kulcs nem függ tőle.

#### A parancs használata
```bash
digna crypt gen-key
```

#### Példakimenet
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

A `crypt encrypt` parancs egy karakterláncot (például adatbázisjelszót) titkosít a `config.toml` fájlban beállított AES-GCM kulccsal, és kiírja a titkosított szöveget.

#### A parancs használata
```bash
digna crypt encrypt <VALUE>
```

#### Argumentumok
- **VALUE**: A titkosítandó nyílt szöveges karakterlánc (kötelező).

#### Példa
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

A `crypt decrypt` parancs egy AES-GCM titkosítású karakterláncot fejt vissza a `config.toml` fájlban beállított kulccsal, és kiírja a nyílt szöveget.

#### A parancs használata
```bash
digna crypt decrypt <VALUE>
```

#### Argumentumok
- **VALUE**: A visszafejtendő titkosított karakterlánc (kötelező).

#### Példa
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Felhasználókezelés

---

### user add

A `user add` parancs új felhasználói fiókot hoz létre a ***digna*** tárolóban. A parancs meghiúsul, ha a megadott e-mail-címmel már létezik felhasználó.

#### A parancs használata
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumentumok
- **EMAIL**: A felhasználó e-mail-címe (kötelező).
- **PASSWORD**: A felhasználó kezdeti jelszava (kötelező).
- **DISPLAY_NAME**: A felhasználó teljes megjelenítendő neve (kötelező).

#### Beállítások
- `--admin`, `-a`: A felhasználót rendszergazdai (superuser) jogosultságokkal hozza létre.

#### Példa
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Rendszergazdai fiók létrehozása:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Példakimenet
```text
User created with ID: 42
```

### user list

A `user list` parancs táblázatos formában felsorolja az összes regisztrált felhasználót az azonosítóval, az e-mail-címmel, a megjelenítendő névvel és a rendszergazdai jelzővel.

#### A parancs használata
```bash
digna user list
```

#### Példakimenet
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

A `user modify` parancs egy meglévő, e-mail-cím alapján azonosított felhasználói fiók megjelenítendő nevét és rendszergazdai jogosultságait frissíti.

A megjelenítendő nevet és a rendszergazdai jelzőt a rendszer mindig egyszerre írja. Az `--admin` kapcsoló, nem érték: **elhagyása visszavonja a rendszergazdai jogosultságokat**, ezért adja meg minden olyan esetben, amikor a felhasználónak meg kell tartania vagy meg kell szereznie azokat.

#### A parancs használata
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumentumok
- **EMAIL**: A módosítandó felhasználó e-mail-címe (kötelező).
- **DISPLAY_NAME**: A frissített megjelenítendő név (kötelező).

#### Beállítások
- `--admin`, `-a`: Rendszergazdai jogosultságokat ad. Hagyja el a visszavonásukhoz.
- `--valid-until`, `-v`: Kompatibilitási okokból elfogadott, de **jelenleg nem érvényesül**. Megadása figyelmeztetést ír ki, és semmit sem változtat.

#### Példa
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Példakimenet
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

A `user modify-pwd` parancs egy meglévő felhasználói fiók jelszavát frissíti.

#### A parancs használata
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumentumok
- **EMAIL**: Annak a felhasználónak az e-mail-címe, akinek a jelszavát frissíteni kell (kötelező).
- **PASSWORD**: Az új jelszó (kötelező).

#### Példa
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

A `user delete` parancs eltávolít egy felhasználói fiókot a rendszerből.

#### A parancs használata
```bash
digna user delete <EMAIL>
```

#### Argumentumok
- **EMAIL**: A törlendő felhasználó e-mail-címe (kötelező).

#### Példa
```bash
digna user delete jdoe@example.com
```

---

## Projektek és adatforrások kezelése

---

### project list

A `project list` parancs felsorolja a tárolóban elérhető összes projektet, megjelenítve azonosítójukat, nevüket és leírásukat.

#### A parancs használata
```bash
digna project list
```

#### Példakimenet
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

A `project list-ds` parancs felsorolja az adott projekthez tartozó összes adatforrást, megjelenítve azonosítójukat, nevüket, típusukat, sémájukat és táblanevüket.

#### A parancs használata
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelynek az adatforrásait fel kell sorolni (kötelező). A névnek pontosan egyeznie kell.

#### Példa
```bash
digna project list-ds ProjectA
```

#### Példakimenet
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

A `project export-ds` parancs egy projekt adatforrásait JSON dokumentumba exportálja.

Ha sem a `--table-name`, sem a `--table-id` nincs megadva, a projekt összes adatforrása exportálásra kerül.

#### A parancs használata
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelyből az adatforrásokat exportálni kell (kötelező).

#### Beállítások
- `--table-name`, `-n`: Az exportálandó adatforrások nevei. Több név is megadható szóközzel elválasztva.
- `--table-id`, `-i`: Az exportálandó adatforrások azonosítói. Több azonosító is megadható szóközzel elválasztva.
- `--exportfile`, `-f`: Az az elérési út, ahová az exportált adatforrások mentésre kerülnek (alapértelmezés: `data_sources_export.json`).

#### Példa
A `ProjectA` összes adatforrásának exportálása:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Adott táblák exportálása:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Példakimenet
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

A `project import-ds` parancs adatforrásokat importál egy exportfájlból a célprojektbe, és objektumonként jelenti, mi jött létre, mi frissült és mi maradt ki.

#### A parancs használata
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumentumok
- **PROJECT_NAME**: A célprojekt neve, amelybe az importálás történik (kötelező).
- **EXPORT_FILE**: A JSON exportfájl elérési útja (kötelező).

#### Beállítások
- `--output-file`, `-o`: Az a fájl, amelybe az importjelentés íródik. Nélküle a jelentés a stdout kimenetre kerül.
- `--output-format`, `-f`: Az importjelentés formátuma — `table`, `json` vagy `csv` (alapértelmezés: `table`).

#### Példa
```bash
digna project import-ds ProjectB my_export.json
```

Géppel olvasható jelentés rögzítése:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

A jelentés négy objektumszintet fed le — adatforrás, adathalmaz-definíció, attribútum és érvényesítési szabály —, mindegyiket az importművelettel, az eredménnyel, a létrejött objektum azonosítójával és az esetleges további információkkal együtt.

### project plan-import-ds

A `project plan-import-ds` parancs előnézetet ad az adatforrások célprojektbe történő importálásáról, megmutatva, mely objektumok jönnének létre, frissülnének vagy maradnának ki, anélkül hogy bármit megváltoztatna. Ugyanazt az exportfájlt és ugyanazokat a jelentési beállításokat fogadja el, mint a [`project import-ds`](#project-import-ds), és tervezett objektumonként lépésszámmal egészíti ki.

#### A parancs használata
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumentumok
- **PROJECT_NAME**: A célprojekt neve (kötelező).
- **EXPORT_FILE**: Az exportfájl elérési útja (kötelező).

#### Beállítások
- `--output-file`, `-o`: Az a fájl, amelybe az importterv íródik. Nélküle a terv a stdout kimenetre kerül.
- `--output-format`, `-f`: Az importterv formátuma — `table`, `json` vagy `csv` (alapértelmezés: `table`).

#### Példa
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Ellenőrzések kezelése

---

### inspection run

Az `inspection run` parancs ellenőrzési kérést hoz létre egy projekthez és egy dátumtartományhoz, majd — a megadott beállításoktól függően — vagy megvárja, vagy azonnal visszatér, vagy saját folyamatán belül futtatja le.

A három végrehajtási mód:

- **Alapértelmezett (kapcsoló nélkül)**: a kérés a háttérrendszer várólistájára kerül, a CLI pedig kétmásodpercenként lekérdezi, és kiírja a feladatok haladását, amíg az ellenőrzés végállapotba nem jut. Futó `digna serve` szükséges, különben senki sem veszi fel a kérést.
- **`--async-mode`**: a kérés várólistára kerül, azonosítóját pedig a rendszer azonnal kiírja. A követéséhez használja az [`inspection status`](#inspection-status) parancsot.
- **`--bypass-backend`**: az ellenőrzést maga a CLI folyamat hajtja végre, és nem kerül várólistára, így nincs szükség futó kiszolgálóra.

Az `--async-mode` és a `--bypass-backend` kölcsönösen kizárják egymást.

Minden módban a parancs nem nulla kilépési kóddal zárul, ha az ellenőrzés nem fejeződött be sikeresen.

#### A parancs használata
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumentumok
- **PROJECT_NAME**: A célprojekt neve (kötelező). A névnek pontosan egyeznie kell.
- **START_DATE**: A dátumtartomány kezdődátuma `YYYY-MM-DD` formátumban (kötelező).
- **END_DATE**: A dátumtartomány záródátuma `YYYY-MM-DD` formátumban (kötelező).

#### Beállítások
- `--table-name`: Az ellenőrzést a projekt egyetlen adatforrására korlátozza, amelyet az adatforrás neve határoz meg. Nélküle a projekt összes adatforrása ellenőrzésre kerül.
- `--async-mode`: Várólistára teszi az ellenőrzést, és kiírja a kérés azonosítóját ahelyett, hogy megvárná. Nem kombinálható a `--bypass-backend` beállítással.
- `--bypass-backend`: Az ellenőrzést közvetlenül a CLI folyamatában futtatja ahelyett, hogy a háttérrendszer várólistájára tenné. Nem kombinálható az `--async-mode` beállítással.

#### Példa
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Aszinkron ellenőrzés beküldése:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Egyetlen adatforrás ellenőrzése:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Példakimenet
Alapértelmezett mód:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Aszinkron mód:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Az `inspection status` parancs egy ellenőrzési kérés állapotát és feladathaladását kérdezi le a kérés azonosítója alapján.

#### A parancs használata
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumentumok
- **INSPECTION_REQUEST_ID**: Az ellenőrzési kérés numerikus azonosítója (kötelező).

#### Példa
```bash
digna inspection status 1024
```

#### Példakimenet
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Az `inspection abort` parancs a futó vagy függőben lévő ellenőrzési kérések megszakítását kéri. Minden érintett kéréshez leállítási eseményt rögzít; ez alapján a háttérrendszer jár el, így a megszakítás leállítási kérés, nem pedig azonnali kilövés.

#### A parancs használata
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumentumok
- **INSPECTION_REQUEST_ID**: A megszakítandó ellenőrzési kérés azonosítója. Kötelező, hacsak nincs megadva a `--killall`.

#### Beállítások
- `--killall`: Megszakítja az összes jelenleg futó és függőben lévő ellenőrzési kérést. Elsőbbséget élvez a mellette megadott kérésazonosítóval szemben.

#### Példa
Adott kérés megszakítása:
```bash
digna inspection abort 1024
```

Az összes aktív és várólistán lévő ellenőrzés megszakítása:
```bash
digna inspection abort --killall
```

#### Példakimenet
A `--killall` jelenti, mit tett; egyetlen kérés megszakítása nem ad kimenetet, és a sikerről a kilépési kódjával számol be.
```text
All running and pending inspections have been aborted.
```

---

## Licenckezelés

---

### license check

A `license check` parancs ellenőrzi a `license.toml` fájlt: aláírását a telepítéssel szállított nyilvános kulccsal veti össze, és megvizsgálja, hogy nem járt-e le. Nem olvas alkalmazáskonfigurációt, ezért még a `config.toml` beállítása előtt is működik.

#### A parancs használata
```bash
digna license check
```

#### Példakimenet
```text
License is valid
```

Az érvénytelen aláírás és a lejárt licenc külön hibaként jelenik meg, mindkettő 1-es kilépési kóddal.

---

## Kiszolgáló és háttérszolgáltatások

---

### serve

A `serve` parancs elindítja a ***digna*** REST API kiszolgálót a háttérben futó ellenőrzésütemezővel és ellenőrzéskezelővel együtt. Indításkor sikertelenné nyilvánít minden olyan ellenőrzést is, amelyet a tároló még futóként tart nyilván, mivel egy korábbi folyamatból semmi sem maradhatott fenn.

A parancs előtérben fut, amíg le nem állítják.

#### A parancs használata
```bash
digna serve [OPTIONS]
```

#### Beállítások
- `--address`: Az a hálózati cím, amelyhez az API-kiszolgáló kötődik (alapértelmezés: `127.0.0.1`).
- `--port`: A figyelt port száma (alapértelmezés: `8000`).

#### Példa
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Példakimenet
```text
Server running on http://0.0.0.0:8000
```
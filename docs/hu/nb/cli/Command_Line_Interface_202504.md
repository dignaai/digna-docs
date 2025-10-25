---
title: digna CLI Referencia 2025.04 – Parancsok & Példák | digna Dokumentáció
description: Teljes referencia a digna CLI kiadásához 2025.04. Tanulja meg, hogyan kezelje a felhasználókat, repository-kat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect és továbbiak.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Referencia 2025.04
**2025-04-01**

Ez az oldal dokumentálja a ***digna*** CLI **2025.04** kiadásában elérhető összes parancsot, beleértve használati példákat és opciókat.

---

## CLI Alapok

---

## A `--help` opció használata

A `--help` opció információt ad az elérhető parancsokról és azok használatáról. Két fő módja van ennek az opció használatának:

1. **Általános súgó megjelenítése:**
   
   Használja a --help-et közvetlenül a főparancs után:  
   ```bash
   dignacli --help
   ```

2. **Specifikus parancs súgója:**  
  
   A részletes információkért adja meg a `--help`-et a kívánt parancs után.  
   Például az `add-user` parancs súgójához futtassa:
   ```bash
   dignacli add-user --help
   ```

   ### Kimenet:
      
   - **Parancs leírása:** Részletes magyarázatot ad a parancs működéséről.  
   - **Szin­taxis:** Pontos szintaxist mutat, beleértve a kötelező és választható argumentumokat.  
   - **Opciók:** Felsorolja a parancs-specifikus opciókat és azok magyarázatát.  
   - **Példák:** Mutat példákat a parancs hatékony használatára.

  
## A `check-repo-connection` parancs használata

A `check-repo-connection` parancs a ***digna*** CLI-ben egy eszköz a megadott ***digna*** repository kapcsolódásának és hozzáférésének tesztelésére. Ez a parancs meggyőződik arról, hogy a CLI tud-e kommunikálni a repository-val.
      
#### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres futtatás esetén a parancs megerősíti a kapcsolatot, és részleteket jelenít meg a repository-ról: Repository-verzió, Host, Database és Schema.  
  
Ha a repository-hoz való kapcsolódás sikertelen, ellenőrizze a config.toml fájlt a helyes konfigurációs beállításokért.

## A `--version` parancs használata

Az telepített *dignacli* verzió ellenőrzéséhez használja a --version opciót.  
  
#### Parancs használata
```bash
dignacli --version
```
  
#### Példa kimenet
```bash
dignacli version 2025.04
```

## Naplózási opciók használata
  
Alapértelmezés szerint a ***digna*** parancsok konzol kimenete minimalizált. A legtöbb parancs lehetőséget ad több információ megjelenítésére az alábbi opciók segítségével:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
A “verbose” és a “debug” a részletességi szintet határozza meg, míg a “logfile” kapcsoló lehetővé teszi a kimenet fájlba történő átirányítását a konzol helyett.

## Felhasználókezelés

### Az `add-user` parancs használata
  
Az `add-user` parancs a ***digna*** CLI-ben új felhasználó hozzáadására szolgál a ***digna*** rendszerben.
  
#### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- `--is_superuser`, `-su`: Jelző az új felhasználó adminisztrátorrá tételéhez.
- `--valid_until`, `-vu`: Beállítja a felhasználói fiók lejárati dátumát a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs beállítva, a fióknak nincs lejárati ideje.

#### Példa

Egy új felhasználó hozzáadásához `jdoe` felhasználónévvel, teljes névvel `John Doe` és jelszóval `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Egy új felhasználó hozzáadásához és a fiók lejárati dátumának beállításához:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### A `delete-user` parancs használata
  
A `delete-user` parancs a ***digna*** CLI-ben meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből.
  
#### Parancs használata
```bash
dignacli delete-user USER_NAME
```
  
##### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen szükséges argumentum.

#### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs futtatása eltávolítja a `jdoe` felhasználót a ***digna*** rendszerből, megvonja a hozzáférését, és törli a repository-ban tárolt kapcsolódó adatokat és jogosultságokat.

### A `modify-user` parancs használata

A `modify-user` parancs a ***digna*** CLI-ben meglévő felhasználó adatainak frissítésére szolgál a ***digna*** rendszerben.

#### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Opciók  
  
- `--is_superuser`, `-su`: Beállítja a felhasználót superuserként, és emelt jogosultságokat ad. Ez a kapcsoló érték nélkül használható.  
- `--valid_until`, `-vu`: Beállítja a felhasználói fiók lejárati dátumát YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
#### Példa
  
A `jdoe` felhasználó teljes nevének megváltoztatásához “Johnathan Doe”-ra és superuserré tételéhez:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### A `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben meglévő felhasználó jelszavának megváltoztatására szolgál a ***digna*** rendszerben.
  
#### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumentumok
  
- **USER_NAME**: A jelszót módosítandó felhasználó felhasználóneve (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
#### Példa
  
A `jdoe` felhasználó jelszavának megváltoztatásához `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### A `list-users` parancs használata

A `list-users` parancs a ***digna*** CLI-ben felsorolja az összes regisztrált felhasználót a ***digna*** rendszerben.

#### Parancs használata

```bash
dignacli list-users
```

A parancs futtatásakor a ***digna*** CLI csatlakozik a ***digna*** repository-hoz és felsorolja a felhasználókat, megjelenítve azonosítójukat, felhasználónevüket, teljes nevüket, superuser státuszukat és lejárati idejüket.

## Repository-kezelés

### Az `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ez a parancs lényeges a frissítések alkalmazásához vagy a repository infrastruktúra első telepítéséhez.
  
#### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
#### Opciók
  
- `--simulation-mode`, `-s`: Aktiváláskor a parancs szimulációs módban fut, ami kiírja azokat az SQL parancsokat, amelyeket végrehajtana, de nem hajtja végre azokat. Hasznos a változtatások előzetes megtekintéséhez anélkül, hogy módosítás történne a repository-ban.  

  
#### Példa
  
A ***digna*** repository frissítéséhez futtassa a parancsot opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
A frissítést szimulációs módban megtekintéséhez (hogy lássa az SQL parancsokat anélkül, hogy alkalmazná őket):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs fontos a ***digna*** rendszer karbantartásához, és biztosítja, hogy az adatbázis-séma és egyéb repository-komponensek naprakészek legyenek a szoftver legutóbbi verziójával.

### Az `encrypt` parancs használata
  
Az `encrypt` parancs a ***digna*** CLI-ben egy jelszó titkosítására szolgál.
  
#### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
#### Példa
  
Egy jelszó titkosításához adja meg a jelszót argumentumként.   
Például a `mypassword123` jelszó titkosításához használja:
```bash
dignacli encrypt mypassword123
```
A parancs visszaadja a megadott jelszó titkosított változatát, amelyet aztán biztonságos környezetben lehet használni. Ha a jelszóargumentum hiányzik, a CLI hibát jelez a hiányzó argumentum miatt.

## A `generate-key` parancs használata
  
A `generate-key` parancs Fernet-kulcsot generál, amely szükséges a ***digna*** repository-ban tárolt jelszavak védelméhez.
  
#### Parancs használata
```bash
dignacli generate-key
```
  
## Adatkezelés

## A `clean-up` parancs használata

A `clean-up` parancs a ***digna*** CLI-ben profilok, predikciók és a Traffic Light System adatait törli egy vagy több adatforrásból egy megadott projektben. Ez a parancs fontos az adatok életciklus-kezeléséhez, és segít rendezett, hatékony adatkörnyezet fenntartásában az elavult vagy felesleges adatok eltávolításával.

#### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, ahonnan az adatokat törölni kell (kötelező). Ha ebben az argumentumban az all-projects kulcsszót használja, a ***digna*** végigiterál az összes létező projekten, és alkalmazza a parancsot.
- **FROM_DATE**: Az adattisztítás kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adattisztítás záró dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- `--table-name`, `-tn`: Korlátozza a clean-up műveletet egy meghatározott táblára a projektben.
- `--table-filter`, `-tf`: Szűkíti a clean-up-ot a megadott részstringet tartalmazó tábla-nevekhez.
- `--timing`, `-tm`: A clean-up folyamat időtartamát mutatja a befejezés után.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
#### Példa
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Csak egy `Table1` nevű konkrét táblából történő adatok eltávolításához:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében és biztosítja, hogy a repository csak a releváns információkat tartalmazza.

## A `list-projects` parancs használata
  
A `list-projects` parancs a ***digna*** CLI-ben az összes elérhető projekt listázására szolgál a ***digna*** rendszerben.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos az adminisztrátorok és több projektet kezelő felhasználók számára, mivel gyors áttekintést ad az elérhető projektekről a ***digna*** repository-ban.

## A `list-ds` parancs használata

A `list-ds` parancs a ***digna*** CLI-ben az összes elérhető adatforrás felsorolására szolgál egy adott projektben. Ez a parancs hasznos a projekt elemzési és kezelési erőforrásainak áttekintéséhez.

#### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelyre az adatforrások listázása vonatkozik (kötelező).
  
#### Példa
  
Az összes adatforrás listázása a `ProjectA` projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést ad a projektben elérhető adatforrásokról, és segít a felhasználóknak hatékonyabban navigálni és kezelni az adatokat.

## Az `inspect` parancs használata

Az `inspect` parancs a ***digna*** CLI-ben profilok, predikciók és a Traffic Light System adatok előállítására szolgál egy vagy több adatforrásra egy megadott projekt esetén. Ez a parancs segít az adatok elemzésében és felügyeletében egy meghatározott időszakon belül.

#### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Az ellenőrzendő projekt neve (kötelező). Ha ebben az argumentumban az all-projects kulcsszót használja, a ***digna*** végigiterál az összes létező projekten, és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Korlátozza az ellenőrzést egy meghatározott táblára a projektben.
- `--table-filter`, `-tf`: Csak azokat a táblákat vizsgálja, amelyek neve tartalmazza a megadott részstringet.
- `--do-profile`: Újraindítja a profilok begyűjtését. Alapértelmezett: do-profile.
- `--no-do-profile`: Megakadályozza a profilok újbóli begyűjtését.
- `--do-prediction`: Rekalkulálja a predikciókat. Alapértelmezett: do-prediction.
- `--no-do-prediction`: Megakadályozza a predikciók rekalkulálását.
- `--do-alert-status`: Rekalkulálja az alert státuszt. Alapértelmezett: do-alert-status.
- `--no-do-alert-status`: Megakadályozza az alert státusz rekalkulálását.
- `--iterative`: A periódus napi iterációkkal történő ellenőrzését indítja. Alapértelmezett: iterative.
- `--no-iterative`: Az egész periódus egyszeri futtatását indítja.
- `--enable_notification`, `-en`: Engedélyezi az értesítések küldését alert esetén.
- `--timing`, `-tm`: A vizsgálat időtartamát mutatja a befejezés után.
  
#### Példa
  
Adatok ellenőrzése a `ProjectA` projektben 2024. január 1-jétől 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy adott tábla ellenőrzéséhez és a predikciók erőltetett újraszámításához:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos friss profilok és predikciók generálására, az adatintegritás felügyeletére és az értesítési rendszerek kezelésére egy adott projekt-időkereten belül.

## A `tls-status` parancs használata

A `tls-status` parancs a ***digna*** CLI-ben egy adott tábla Traffic Light System (TLS) státuszának lekérdezésére szolgál egy projekten belül egy megadott dátumra. A Traffic Light System betekintést nyújt az adatok minőségébe és állapotába, és jelzi az esetleges problémákat vagy riasztásokat, amelyek figyelmet igényelhetnek.
  
#### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyre a TLS státusz lekérés vonatkozik (kötelező).
- **TABLE_NAME**: Az a konkrét tábla a projektben, amelyre a TLS státusz vonatkozik (kötelező).
- **DATE**: A dátum, amelyre a TLS státuszt kérdezi le, általában %Y-%m-%d formátumban (kötelező).
  
#### Példa
  
A `ProjectA` projekt `UserData` nevű táblájának TLS státuszának ellenőrzése 2024. július 1-jén:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ez a parancs segít a felhasználóknak az adatok minőségének felügyeletében és karbantartásában az előre definiált kritériumok alapján nyújtott világos, cselekvésre alkalmas státuszjelentéssel.

## Az `inspect-async` parancs használata

Az `inspect-async` parancs a ***digna*** CLI-ben arra szolgál, hogy a backendet aszinkron módon utasítsa egy vagy több adatforrás ellenőrzésének elvégzésére egy adott projekthez. Ha a project_name értéke all-projects, az ellenőrzés végigiterál az összes elérhető projekten és végrehajtja az ellenőrzést. A parancs egy request id-t ad vissza, amely segítségével nyomon követhető az ellenőrzés előrehaladása.

#### Parancs használata

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Az ellenőrizendő projekt neve (kötelező). Ha ebben az argumentumban az all-projects kulcsszót használja, a ***digna*** végigiterál az összes létező projekten, és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Korlátozza az ellenőrzést egy meghatározott táblára a projektben.
- `--table-filter`, `-tf`: Csak azokat a táblákat vizsgálja, amelyek neve tartalmazza a megadott részstringet.

  
#### Példa
  
Aszinkron ellenőrzés indítása a `ProjectA` projektben 2024. január 1-jétől 2024. január 31-ig:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Az `inspect-status` parancs használata

Az `inspect-status` parancs a ***digna*** CLI-ben egy aszinkron ellenőrzés előrehaladásának lekérdezésére szolgál a request ID alapján.

#### Parancs használata

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumentumok
  
- **REQUEST_ID**: Az `inspect-async` parancs által visszaadott request id 
  
#### Opciók

- `--report_level`, `-rl`: Állítsa be a riport szintjét: 'task' vagy 'step' [alapértelmezett: task]
  
#### Példa
  
Egy részletes, lépésenkénti riport lekérése egy 12345 request ID-val rendelkező ellenőrzéshez:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Az `export-ds` parancs használata

Az `export-ds` parancs a ***digna*** CLI-ben adatforrások exportálására szolgál a ***digna*** repository-ból. Alapértelmezés szerint egy adott projekt összes adatforrása exportálásra kerül.

#### Parancs használata
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, ahonnan az adatforrások exportálása történik.

#### Opciók

- `--table_name`, `-tn`: Egy adott adatforrás exportálása egy projekten belül.
- `--exportfile`, `-ef`: Az export fájlnevének megadása.
    
#### Példa
  
Az összes adatforrás exportálása a `ProjectA` projektből:
  
```bash
dignacli export-ds ProjectA
```
  
A parancs az `ProjectA` összes adatforrását egy JSON dokumentumba exportálja, amely importálható egy másik projektbe vagy ***digna*** repository-ba.

## Az `import-ds` parancs használata

Az `import-ds` parancs a ***digna*** CLI-ben adatforrások importálására szolgál egy célnak megfelelő projektbe, és import riport létrehozására.

#### Parancs használata
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelybe az adatforrásokat importálni kívánja.
- **EXPORT_FILE**: Az importálandó export fájl neve.

#### Opciók

- `--output-file`, `-o`: Fájl az importraport mentéséhez (ha nincs megadva, a riport táblázatos formában a terminálra íródik).
- `--output-format`, `-f`: Az importraport mentésének formátuma (json, csv).
    
#### Példa
  
Az összes adatforrás importálása a `my_export.json` export fájlból a `ProjectB`-be:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Az import után a parancs riportot jelenít meg az importált és kihagyott objektumokról. Csak az új adatforrások lesznek importálva `ProjectB`-be. Annak megtekintéséhez, hogy mely objektumok lennének importálva és kihagyva, használja a `plan-import-ds` parancsot.

## A `plan-import-ds` parancs használata

A `plan-import-ds` parancs a ***digna*** CLI-ben egy exportfájl elemzésére és egy terv megjelenítésére szolgál arról, hogy mely adatforrások kerülnének importálásra egy célprojektbe.

#### Parancs használata
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelybe az adatforrások importálása történne.
- **EXPORT_FILE**: Az elemzendő export fájl neve az import előtt.

#### Opciók

- `--output-file`, `-o`: Fájl az importraport mentéséhez (ha nincs megadva, a riport táblázatos formában a terminálra íródik).
- `--output-format`, `-f`: Az importraport mentésének formátuma (json, csv).
    
#### Példa
  
Annak ellenőrzéséhez, hogy az `my_export.json` exportfájlból mely adatforrások kerülnének importálásra és melyek kerülnének kihagyásra, ha azt a `ProjectB`-be importálják:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ez a parancs csak egy importtervet mutat a beimportálandó és kihagyandó objektumokról.
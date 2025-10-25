---
title: digna CLI Reference 2025.04 – Parancsok & Példák | digna Dokumentáció
description: Teljes referencia a digna CLI 2025.04 verziójához. Ismerje meg, hogyan kezelje a felhasználókat, repository-kat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect és még sok más.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Ez az oldal a ***digna*** CLI **2025.04** verziójában elérhető összes parancs teljes dokumentációját tartalmazza, példákkal és opciókkal.

---

## CLI alapok

---

## A `help` opció használata

A `--help` opció információt nyújt az elérhető parancsokról és azok használatáról. Ennek két fő használati módja van:

1. **Általános súgó megtekintése:**
   
   Használja a `--help`-et közvetlenül a `***digna***` kulcsszó után.  
   ```bash
   dignacli --help

2. **Specifikus parancsok súgója:**  
  
   Egy adott parancs részletes leírásához adja hozzá a `--help`-et a parancshoz.  
   Például, ha az `add-user` parancs súgóját szeretné megtekinteni, futtassa:
    ```bash
    dignacli add-user --help
    ```

    ### kimenet:
     
    - **Parancs leírása:** Részletesen ismerteti, mit csinál a parancs.  
    - **Szintaxis:** Megjeleníti a teljes szintaxist, beleértve a kötelező és választható argumentumokat.  
    - **Opciók:** Felsorolja a parancshoz tartozó opciókat és azok magyarázatát.  
    - **Példák:** Példákat ad arra, hogyan kell hatékonyan futtatni a parancsot.

  
## A `check-repo-connection` parancs használata

A `check-repo-connection` parancs a ***digna*** CLI-ben arra szolgál, hogy tesztelje a megadott ***digna*** repository-hoz való kapcsolódást és hozzáférést. Ez a parancs megerősíti, hogy a CLI képes kommunikálni a repository-val.
      
#### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres futtatás esetén a parancs a kapcsolat megerősítése mellett a repository-ról a következő információkat adja vissza: Repository verzió, Host, Database és Schema.  
  
Ha a repository-hoz való csatlakozás nem sikerül, ellenőrizze a config.toml fájlban található beállításokat.

## A `version` parancs használata

A telepített *dignacli* verzió ellenőrzéséhez használja a `--version` opciót.  
  
#### Parancs használata
```bash
dignacli --version
```
  
#### Példa kimenet
```bash
dignacli version 2025.04
```

## Naplózási opciók használata
  
Alapértelmezés szerint a ***digna*** parancsok konzol kimenete minimálisra van tervezve. A legtöbb parancs lehetőséget ad további információk megjelenítésére; a következő opciók érhetők el:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
A „verbose” és a „debug” a részletességi szintet határozza meg; a „logfile” opció pedig lehetővé teszi, hogy a kimenetet a konzol helyett egy fájlba irányítsa.

## Felhasználókezelés

### Az `add-user` parancs használata
  
A ***digna*** CLI-ben az `add-user` parancs új felhasználó hozzáadására szolgál a ***digna*** rendszerhez.
  
#### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- `--is_superuser`, `-su`: Jelző az új felhasználó adminisztrátorrá (superuser) való kinevezéséhez.
- `--valid_until`, `-vu`: A felhasználói fiók érvényességének végét adja meg `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fióknak nincs lejárati ideje.

#### Példa

Új felhasználó hozzáadása, akinek a felhasználóneve `jdoe`, teljes neve `John Doe` és jelszava `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Új felhasználó hozzáadása lejárati dátummal:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### A `delete-user` parancs használata
  
A `delete-user` parancs a ***digna*** CLI-ben egy meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből.
  
#### Parancs használata
```bash
dignacli delete-user USER_NAME
```
  
##### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen argumentum, amelyet a parancs igényel.

#### Példa
```bash
dignacli delete-user jdoe
```
  
Ez a parancs eltávolítja a `jdoe` felhasználót a ***digna*** rendszerből; visszavonja a hozzáférését, és törli a repository-ban található kapcsolódó adatait és engedélyeit.

### A `modify-user` parancs használata

A `modify-user` parancs a ***digna*** CLI-ben egy meglévő felhasználó adatainak frissítésére szolgál.

#### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumentumok
  
- **USER_NAME**: A frissítendő felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Opciók  
  
- `--is_superuser`, `-su`: Beállítja a felhasználót superuserként; emelt jogosultságokat ad. Ez az opció nem igényel értéket.  
- `--valid_until`, `-vu`: A felhasználói fiók lejárati idejét állítja be YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók korlátlanul érvényes.  
  
#### Példa
  
A `jdoe` felhasználó teljes nevének „Johnathan Doe”-ra való módosítása és superuserré tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### A `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben egy meglévő felhasználó jelszavának megváltoztatására szolgál.
  
#### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumentumok
  
- **USER_NAME**: A jelszót módosítandó felhasználó felhasználóneve (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
#### Példa
  
A `jdoe` felhasználó jelszavának `newpassword123`-ra való megváltoztatásához:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### A `list-users` parancs használata

A `list-users` parancs listázza az összes, a ***digna*** rendszerben regisztrált felhasználót a ***digna*** CLI-ben.

#### Parancs használata

```bash
dignacli list-users
```

A parancs repository-hoz csatlakozva listázza az összes felhasználót, megjelenítve az ID-t, felhasználónevet, teljes nevet, superuser státuszt és a lejárati időbélyegeket.

## Repository kezelés

### Az `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ezt a parancsot frissítések alkalmazásához vagy a repository infrastruktúrájának első létrehozásához használják.
  
#### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
#### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut; kiírja a végrehajtandó SQL utasításokat, de nem hajtja végre azokat. Hasznos a változtatások alkalmazása előtti előnézethez.  

  
#### Példa
  
A ***digna*** repository frissítése opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
A frissítést szimulációs módban futtatni (látni az SQL utasításokat, de nem alkalmazni azokat):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kritikus fontosságú a ***digna*** rendszer karbantartásához, biztosítva, hogy az adatbázis séma és a többi repository-elem kompatibilis legyen a szoftver legújabb verziójával.

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
Például a `mypassword123` jelszó titkosításához:
```bash
dignacli encrypt mypassword123
```
Ez a parancs a megadott jelszó titkosított változatát adja vissza kimenetként; később biztonságosabb környezetben használható. Ha nem ad meg jelszó argumentumot, a CLI hibát jelez a hiányzó argumentum miatt.

## A `generate-key` parancs használata
  
A `generate-key` parancs Fernet kulcs generálására szolgál; ez a kulcs szükséges ahhoz, hogy a ***digna*** repository-ban tárolt jelszavak biztonságosan legyenek kezelve.
  
#### Parancs használata
```bash
dignacli generate-key
```
  
## Adatkezelés

## A `clean-up` parancs használata

A `clean-up` parancs a ***digna*** CLI-ben egy adott projekten belül egy vagy több adatforráshoz tartozó profilok, előrejelzések és a forgalmi lámpa rendszer adatait törli. Ez a parancs fontos az adat életciklus-kezelés szempontjából, és segít megtartani az adatkört rendezettnek és hatékonynak az elavult vagy felesleges adatok eltávolításával.

#### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyből az adatokat törölni kívánja (kötelező). Ha az argumentum értéke all-projects, a ***digna*** végigiterál az összes elérhető projekten és alkalmazza a parancsot.
- **FROM_DATE**: A törlés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: A törlés befejezésének dátuma és ideje; ugyanazokat a formátumokat fogadja el, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- `--table-name`, `-tn`: A tisztítást egy adott projekten belüli táblára korlátozza.
- `--table-filter`, `-tf`: Szűrőt alkalmaz azokra a táblákra, amelyek neve tartalmazza a megadott részstringet.
- `--timing`, `-tm`: A művelet befejezése után megjeleníti a tisztítás időtartamát.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
#### Példa
  
Adatok törlése a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Csak a `Table1` nevű táblából adatokat törölni:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében, és biztosítja, hogy a repository csak a szükséges információkat tartalmazza.

## A `list-projects` parancs használata
  
A `list-projects` parancs megjeleníti a rendszerben található összes elérhető projekt listáját a ***digna*** CLI-ben.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára; gyors áttekintést nyújt az aktuálisan létező projektekről a repository-ban.

## A `list-ds` parancs használata

A `list-ds` parancs megjeleníti egy megadott projekten belül található összes adatforrást. Ez a parancs segít megérteni azokat az adatvagyonokat, amelyeket elemzésre és kezelésre lehet használni.

#### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt neve, amelynek adatforrásait listázni kívánja (kötelező).
  
#### Példa
  
A ProjectA projekt összes adatforrásának listázásához:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést ad egy projektben található adatforrások jelenlegi állapotáról, segítve az adatkör hatékonyabb kezelését.


## Az `inspect` parancs használata

Az `inspect` parancs a ***digna*** CLI-ben egy adott projekten belül egy vagy több adatforráshoz profilokat, előrejelzéseket és a forgalmi lámpa rendszerhez tartozó adatokat hoz létre. Ez a parancs segít az adatok adott időszak alatti elemzésében és monitorozásában.

#### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelynek adatait ellenőrizni szeretné (kötelező). Ha az argumentum all-projects, a ***digna*** végigiterál az összes elérhető projekten.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés befejező dátuma és ideje; ugyanazokat a formátumokat fogadja el, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Az ellenőrzést egy adott projekten belüli táblára korlátozza.
- `--table-filter`, `-tf`: Szűrőt alkalmaz azon táblákra, amelyek nevében megadott részstring szerepel.
- `--do-profile`: Újraprofilozás indítása. Alapértelmezett: do-profile.
- `--no-do-profile`: Megakadályozza a profilok újragyűjtését.
- `--do-prediction`: Előrejelzések újraszámításának indítása. Alapértelmezett: do-prediction.
- `--no-do-prediction`: Megakadályozza az előrejelzések újraszámítását.
- `--do-alert-status`: Figyelmeztetési státuszok újraszámításának indítása. Alapértelmezett: do-alert-status.
- `--no-do-alert-status`: Megakadályozza a figyelmeztetési státuszok újraszámítását.
- `--iterative`: Az adott időszak napi iterációkban történő vizsgálatát indítja. Alapértelmezett: iterative.
- `--no-iterative`: Az adott időszak egyszeri feldolgozását biztosítja.
- `--enable_notification`, `-en`: Értesítések engedélyezése figyelmeztetés esetén.
- `--timing`, `-tm`: Az ellenőrzés befejezése után megjeleníti a futási időt.
  
#### Példa
  
A ProjectA projekt 2024. január 1. és 2024. január 31. közötti adatainak ellenőrzéséhez:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy konkrét tábla ellenőrzéséhez és az előrejelzések újraszámításának kényszerítéséhez:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos frissített profilok és előrejelzések létrehozásához, az adatintegritás monitorozásához, valamint a figyelmeztetési rendszerek kezeléséhez a megadott projekt-időszakban.

## A `tls-status` parancs használata

A `tls-status` parancs a ***digna*** CLI-ben egy adott dátumra vonatkozóan lekérdezi egy projekt táblájának Forgalmi Lámpa Rendszer (TLS) státuszát. A Forgalmi Lámpa Rendszer információt ad az adatok egészségéről és minőségéről; jelzi a figyelmet igénylő problémákat vagy riasztásokat.
  
#### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyre a TLS státuszt lekérdezik (kötelező).
- **TABLE_NAME**: A projektben található tábla neve, amelynek TLS státuszát lekérdezik (kötelező).
- **DATE**: Az a dátum, amelyre a TLS státuszt lekérdezik; általában %Y-%m-%d formátumú (kötelező).
  
#### Példa
  
A ProjectA projektben található `UserData` tábla 2024. július 1-jei TLS státuszának ellenőrzéséhez:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ez a parancs a meghatározott kritériumok alapján világos és gyakorlatias állapotjelentést nyújt az adatminőségről, segítve a felhasználókat az adatok nyomon követésében.

## Az `inspect-async` parancs használata

Az `inspect-async` parancs a ***digna*** CLI-ben aszinkron módon kérést küld a backendnek, hogy egy vagy több adatforrás ellenőrzését végezze el egy adott projekten. Ha a project_name all-projects, az ellenőrzés az összes elérhető projekten végigiterál. A parancs egy kérésazonosítót (request id) ad vissza, amellyel az ellenőrzés előrehaladása nyomon követhető.

#### Parancs használata

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Az ellenőrzés alá eső projekt neve (kötelező). Ha az érték all-projects, a ***digna*** az összes projektet feldolgozza.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés befejező dátuma és ideje; ugyanazokat a formátumokat fogadja el, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Az ellenőrzést egy adott projekten belüli táblára korlátozza.
- `--table-filter`, `-tf`: Szűrőt alkalmaz azon táblákra, amelyek nevében a megadott részstring szerepel.

  
#### Példa
  
Aszinkron ellenőrzés kérése a ProjectA projekt 2024. január 1. és 2024. január 31. közötti adataira:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Az `inspect-status` parancs használata

Az `inspect-status` parancs az `inspect-async` által indított aszinkron ellenőrzés előrehaladását ellenőrzi a kérésazonosító (request ID) alapján.

#### Parancs használata

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumentumok
  
- **REQUEST_ID**: Az `inspect-async` parancs által visszaadott kérésazonosító.
  
#### Opciók

- `--report_level`, `-rl`: Beállítja a jelentés szintjét: 'task' vagy 'step' [alapértelmezett: task]
  
#### Példa
  
Egy, 12345 kérésazonosítójú ellenőrzés részletes lépés (step) szintű előrehaladásának lekérdezéséhez:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Az `export-ds` parancs használata

Az `export-ds` parancs a ***digna*** CLI-ben adatforrások exportálásának előállítására szolgál a repository-ból. Alapértelmezés szerint egy megadott projekt összes adatforrása exportálásra kerül.

#### Parancs használata
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelyből az adatforrásokat exportálni kívánja.

#### Opciók

- `--table_name`, `-tn`: Egy adott projektbeli adatforrás exportálására.
- `--exportfile`, `-ef`: Megadja az exportáláshoz használt fájl nevét.
    
#### Példa
  
Az összes adatforrás exportálása a ProjectA projektből:
  
```bash
dignacli export-ds ProjectA
```
  
Ez a parancs JSON dokumentumot hoz létre, amely a ProjectA-ban található összes adatforrást tartalmazza, és másik projekthez vagy ***digna*** repository-hoz importálható.

## Az `import-ds` parancs használata

Az `import-ds` parancs a ***digna*** CLI-ben adatforrások importálására szolgál egy célprojektbe, és importálási jelentést készít.

#### Parancs használata
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelybe az adatforrásokat importálni kívánja.
- **EXPORT_FILE**: Az export fájl neve, amelyből az adatforrásokat importálni kell.

#### Opciók

- `--output-file`, `-o`: Az importálási jelentés mentési fájlja (ha nincs megadva, a jelentés táblázatos formában a terminálra íródik).
- `--output-format`, `-f`: Az importálási jelentés formátuma (json, csv).
    
#### Példa
  
Az `my_export.json` export fájlban található összes adatforrás importálása a ProjectB projektbe:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Az importálás után a parancs jelentést ad az importált és kihagyott objektumokról. Csak az új adatforrások lesznek importálva a ProjectB-be. Az importálandó és kihagyandó objektumok megtekintéséhez használja a `plan-import-ds` parancsot.

## A `plan-import-ds` parancs használata

A `plan-import-ds` parancs a ***digna*** CLI-ben elemzi, hogy egy export fájl tartalma közül mely objektumok lesznek importálva és melyek lesznek kihagyva, mielőtt tényleges importot hajtana végre a célprojektben.

#### Parancs használata
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelybe az adatforrásokat importálni kívánja.
- **EXPORT_FILE**: Az export fájl neve, amelyet az import előtt elemezni kell.

#### Opciók

- `--output-file`, `-o`: A tervezett importálási jelentés mentési fájlja (ha nincs megadva, a jelentés táblázatos formában a terminálra íródik).
- `--output-format`, `-f`: A terv jelentésének formátuma (json, csv).
    
#### Példa
  
Az `my_export.json` export fájl elemzése, hogy mely adatforrások lesznek importálva és melyek lesznek kihagyva a ProjectB-be:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ez a parancs csak egy tervet jelenít meg az importálandó és kihagyandó objektumokról.
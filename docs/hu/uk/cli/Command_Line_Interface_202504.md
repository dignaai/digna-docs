---
title: digna CLI Reference 2025.04 – Parancsok és példák | digna Documentation
description: Teljes kézikönyv a digna CLI 2025.04 kiadásához. Tudja meg, hogyan kezelheti a felhasználókat, repozitóriumokat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect és mások.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Ezen az oldalon dokumentáljuk a digna CLI **2025.04** kiadásában elérhető teljes parancskészletet, beleértve a használati példákat és az opciókat.

---

## CLI alapok

---

## A `--help` opció használata

A `--help` opció információt ad az elérhető parancsokról és azok használatáról. Két fő módja van az opció használatának:

1. **Általános segítség megjelenítése:**
   
   Használja a --help-et közvetlenül a `dignacli` parancs után.  
   ```bash
   dignacli --help
   ```

2. **Segítség konkrét parancshoz:**  
  
   Részletes információkért egy adott parancsról adja hozzá a `--help`-et a parancshoz.
   Például az `add-user` parancs súgójának megszerzéséhez futtassa:
   ```bash
   dignacli add-user --help
   ```

   ### Kimenet:
      
   - **Parancs leírása:** Részletesen ismerteti, mit végez a parancs.  
   - **Szintaxis:** Megjeleníti a pontos szintaxist, beleértve a kötelező és opcionális argumentumokat.  
   - **Opciók:** A parancs-specifikus opciók listája magyarázatokkal.  
   - **Példák:** Mutat példákat a parancs hatékony használatára.

  
## A `check-repo-connection` parancs használata

A `check-repo-connection` parancs a digna CLI eszközben egy segédprogram a megadott digna repozitórium elérhetőségének és kapcsolódásának ellenőrzéséhez. A parancs biztosítja, hogy a CLI képes kommunikálni a repozitóriummal.
      
#### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres futtatás esetén a parancs megerősíti a csatlakozást, és részleteket ad a repozitóriumról: repozitórium verziója, host, adatbázis és séma.  
  
Ha a csatlakozás sikertelen, ellenőrizze a config.toml fájlt a helyes beállításokért.

## A `--version` opció használata

A telepített `dignacli` verzió ellenőrzéséhez használja a `--version` opciót.  
  
#### Parancs használata
```bash
dignacli --version
```
  
#### Példa kimenet
```bash
dignacli version 2025.04
```

## Naplózási opciók használata
  
Alapértelmezés szerint a digna parancsok konzol kimenete minimális. A legtöbb parancs lehetőséget ad további információk kiíratására az alábbi opciók segítségével:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A „verbose” és a „debug” a részletességi szintet határozzák meg, míg a „logfile” kapcsoló lehetővé teszi a kimenet fájlba történő átirányítását a konzol helyett.

## Felhasználók kezelése

### Az `add-user` parancs használata
  
Az `add-user` parancs a digna CLI-ben új felhasználó létrehozására szolgál a digna rendszerben.
  
#### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- `--is_superuser`, `-su`: Jelző az új felhasználó rendszergazdává (szuperfelhasználóvá) jelöléséhez.
- `--valid_until`, `-vu`: A fiók lejárati dátumának beállítása `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fióknak nincs lejárati ideje.

#### Példa

Új felhasználó hozzáadásához `jdoe` felhasználónévvel, `John Doe` teljes névvel és `password123` jelszóval:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
A felhasználó hozzáadása lejárati dátum megadásával:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### A `delete-user` parancs használata
  
A `delete-user` parancs a digna CLI-ben meglévő felhasználó törlésére szolgál a digna rendszerből.
  
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
  
A parancs végrehajtása eltávolítja `jdoe` felhasználót a digna rendszerből, visszavonja hozzáférését, és törli a repozitóriumban tárolt kapcsolódó adatokat és jogosultságokat.

### A `modify-user` parancs használata

A `modify-user` parancs a digna CLI-ben meglévő felhasználó adatainak frissítésére szolgál a digna rendszerben.

#### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Opciók  
  
- `--is_superuser`, `-su`: A felhasználót szuperfelhasználóvá teszi, magasabb jogosultságokat adva. Ez a jelző érték nélkül használatos.  
- `--valid_until`, `-vu`: A fiók lejárati dátumának beállítása `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fiók lejárat nélküli marad.  
  
#### Példa
  
A `jdoe` felhasználó teljes nevének megváltoztatása „Johnathan Doe”-ra és szuperfelhasználóvá tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### A `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs a digna CLI-ben meglévő felhasználó jelszavának megváltoztatására szolgál.
  
#### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumentumok
  
- **USER_NAME**: A felhasználó felhasználóneve, akinek a jelszavát módosítani kell (kötelező).
- **USER_PWD**: Az új jelszó (kötelező).
  
#### Példa
  
A `jdoe` felhasználó jelszavának megváltoztatása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### A `list-users` parancs használata

A `list-users` parancs a digna CLI-ben megjeleníti az összes, a digna rendszerben regisztrált felhasználót.

#### Parancs használata

```bash
dignacli list-users
```

A parancs csatlakozik a digna repozitóriumhoz és felsorolja az összes felhasználót, megjelenítve az ID-t, felhasználónevet, teljes nevet, szuperfelhasználói státuszt és a lejárati időbélyegeket.

## Repozitórium kezelése

### Az `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a digna CLI-ben a repozitórium frissítésére vagy inicializálására szolgál. A parancs szükséges a frissítések alkalmazásához vagy a repozitórium infrastruktúrájának első beállításához.
  
#### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
#### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut, és kiírja azokat az SQL utasításokat, amelyeket végrehajtana, de ténylegesen nem hajtja végre őket. Hasznos a változtatások előzetes megtekintéséhez a repozitórium módosítása nélkül.  

  
#### Példa
  
A repozitórium frissítéséhez futtassa a parancsot opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
Szimulációs módban történő frissítéshez (az SQL utasítások megtekintéséhez alkalmazás nélkül):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kritikus fontosságú a digna rendszer karbantartásához, biztosítva az adatbázis séma és a repozitórium egyéb összetevőinek megfelelését a szoftver legújabb verziójával.

### Az `encrypt` parancs használata
  
Az `encrypt` parancs a digna CLI-ben jelszó titkosítására szolgál.
  
#### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
#### Példa
  
A jelszó titkosításához adja meg argumentumként.   
Például a `mypassword123` titkosításához használja:
```bash
dignacli encrypt mypassword123
```
A parancs kiadja a megadott jelszó titkosított verzióját, amelyet aztán biztonságos környezetben használhat. Ha a jelszó argumentum nincs megadva, a CLI hibát jelez a hiányzó argumentum miatt.

## A `generate-key` parancs használata
  
A `generate-key` parancs Fernet kulcs generálására szolgál, amely szükséges a repozitóriumban tárolt jelszavak védelméhez.
  
#### Parancs használata
```bash
dignacli generate-key
```
  
## Adatkezelés

## A `clean-up` parancs használata

A `clean-up` parancs a digna CLI-ben a Traffic Light System profilok, előrejelzések és rendszeradatok törlésére szolgál egy vagy több adatforrás esetén a megadott projekten belül. Ez a parancs fontos az adattámogatás élettartamának kezeléséhez, segítve a rendezettség és a hatékonyság fenntartását az elavult vagy nem szükséges adatok eltávolításával.

#### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyből törölni kell az adatokat (kötelező). Ha az `all-projects` kulcsszót használja ebben az argumentumban, a digna végigiterál az összes meglévő projekten és alkalmazza a parancsot.
- **FROM_DATE**: A törlés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: A törlés befejező dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- `--table-name`, `-tn`: A törlési művelet korlátozása egy konkrét táblára a projekten belül.
- `--table-filter`, `-tf`: Szűrő a törlés korlátozásához, csak olyan táblákra, amelyek nevében a megadott alstring szerepel.
- `--timing`, `-tm`: A tisztítási folyamat időtartamának megjelenítése a befejezés után.
- `--help`: Megjeleníti a `clean-up` parancs súgóját és kilép.
  
#### Példa
  
Adatok törlése a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Adatok törlése csak egy konkrét, `Table1` nevű táblából:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében, biztosítva, hogy a repozitóriumban csak releváns információk maradjanak.

## A `list-projects` parancs használata
  
A `list-projects` parancs a digna CLI-ben megjeleníti az összes elérhető projekt listáját a digna rendszerben.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára, gyors áttekintést adva az elérhető projektekről a digna repozitóriumban.

## A `list-ds` parancs használata

A `list-ds` parancs a digna CLI-ben megjeleníti az adott projektben elérhető összes adatforrást. Hasznos az elérhető adatok áttekintéséhez, amelyek elemzésre és kezelésre állnak rendelkezésre a digna rendszerben.

#### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentumok
- **PROJECT_NAME**: A projekt neve, amelynek adatforrásai felsorolásra kerülnek (kötelező).
  
#### Példa
  
Az összes adatforrás felsorolása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést nyújt a projektben rendelkezésre álló adatforrásokról, segítve a felhasználókat az adatok térképének jobb kezelésében.

## Az `inspect` parancs használata

Az `inspect` parancs a digna CLI-ben profilok, előrejelzések és a Traffic Light System adatok létrehozására szolgál egy vagy több adatforráshoz a megadott projekten belül. A parancs segít az adatok meghatározott időszak szerinti elemzésében és monitorozásában.

#### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyre az adat-ellenőrzést végre kell hajtani (kötelező). Ha az `all-projects` kulcsszót használja, a digna végigiterál az összes meglévő projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés befejező dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Az ellenőrzés korlátozása egy konkrét táblára a projekten belül.
- `--table-filter`, `-tf`: Az ellenőrzés csak azokra a táblákra korlátozása, amelyek nevében a megadott alstring szerepel.
- `--do-profile`: Profilgyűjtés elindítása. Alapértelmezés szerint — do-profile.
- `--no-do-profile`: Profilgyűjtés leállítása.
- `--do-prediction`: Előrejelzések újraszámolásának indítása. Alapértelmezés szerint — do-prediction.
- `--no-do-prediction`: Előrejelzések újraszámolásának leállítása.
- `--do-alert-status`: Értesítési státuszok újraszámolásának indítása. Alapértelmezés szerint — do-alert-status.
- `--no-do-alert-status`: Értesítési státuszok újraszámolásának leállítása.
- `--iterative`: Az időszak ellenőrzését napi iterációkkal végzi. Alapértelmezés szerint — iterative.
- `--no-iterative`: Az egész időszak egyszerre történő ellenőrzése.
- `--enable_notification`, `-en`: Értesítések küldésének engedélyezése riasztások esetén.
- `--timing`, `-tm`: Az ellenőrzési folyamat időtartamának megjelenítése a befejezés után.
  
#### Példa
  
Adatok ellenőrzése a `ProjectA` projektben 2024. január 1. és 2024. január 31. között:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Egy konkrét tábla ellenőrzése és az előrejelzések kényszerített újraszámolása:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos aktuális profilok és előrejelzések generálására, az adatintegritás monitorozására és az értesítési rendszer kezelésére a megadott projekt időszakában.

## A `tls-status` parancs használata

A `tls-status` parancs a digna CLI-ben a Traffic Light System (TLS) státuszának lekérdezésére szolgál egy konkrét tábla esetén egy adott dátumra. A Traffic Light System betekintést nyújt az adatok állapotába és minőségébe, jelezve olyan problémákat vagy riasztásokat, amelyek figyelmet igényelhetnek.
  
#### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyre a TLS státuszt lekérdezik (kötelező).
- **TABLE_NAME**: A projekt adott táblája, amelyhez a TLS státuszt szeretné lekérdezni (kötelező).
- **DATE**: A dátum, amelyre a TLS státuszt lekérdezik, általában %Y-%m-%d formátumban (kötelező).
  
#### Példa
  
A `UserData` nevű tábla TLS státuszának ellenőrzése a `ProjectA` projektben 2024. július 1-jére:
```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ez a parancs segít a felhasználóknak az adatok minőségének monitorozásában és fenntartásában, világos és gyakorlatias jelentést adva a meghatározott kritériumok alapján.

## Az `inspect-async` parancs használata

Az `inspect-async` parancs a digna CLI-ben arra szolgál, hogy a backendet aszinkron ellenőrzés végrehajtására utasítsa egy vagy több adatforrásra a megadott projekten belül. Ha a `project_name` értéke `all-projects`, az ellenőrzés minden elérhető projektre lefut. A parancs visszaad egy request id-t, amelyet a folyamat nyomon követésére használhat.

#### Parancs használata

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyre az ellenőrzést végzik (kötelező). Ha az `all-projects` kulcsszót használja, a digna végigiterál az összes meglévő projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés befejező dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Az ellenőrzés korlátozása egy konkrét táblára a projekten belül.
- `--table-filter`, `-tf`: Az ellenőrzés csak azokra a táblákra korlátozása, amelyek nevében a megadott alstring szerepel.

  
#### Példa
  
Aszinkron ellenőrzés indítása a `ProjectA` projektben 2024. január 1. és 2024. január 31. között:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Az `inspect-status` parancs használata

Az `inspect-status` parancs a digna CLI-ben az aszinkron ellenőrzés előrehaladásának lekérdezésére szolgál a kérés azonosítója alapján.

#### Parancs használata

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumentumok
  
- **REQUEST_ID**: A kérés azonosítója, amelyet az `inspect-async` parancs adott vissza. 
  
#### Opciók

- `--report_level`, `-rl`: A jelentési szint beállítása: 'task' vagy 'step' [alapértelmezett: task]
  
#### Példa
  
Az aszinkron ellenőrzés előrehaladásának ellenőrzése 12345 azonosítójú kérésre, részletes lépés szintű nézettel:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Az `export-ds` parancs használata

Az `export-ds` parancs a digna CLI-ben adatforrások exportálására szolgál a digna repozitóriumból. Alapértelmezés szerint az adott projekt összes adatforrása exportálásra kerül.

#### Parancs használata
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentumok
- **PROJECT_NAME**: A projekt neve, amelyből az adatforrások exportálásra kerülnek.

#### Opciók

- `--table_name`, `-tn`: Egy konkrét adatforrás exportálása a projekten belül.
- `--exportfile`, `-ef`: Az export fájl nevének megadása.
    
#### Példa
  
Az összes adatforrás exportálása a `ProjectA` projektből:
  
```bash
dignacli export-ds ProjectA
```
  
A parancs exportálja a `ProjectA` összes adatforrását JSON dokumentumként, amely importálható egy másik projektbe vagy digna repozitóriumba.

## Az `import-ds` parancs használata

Az `import-ds` parancs a digna CLI-ben adatforrások importálására szolgál a célprojektbe, és importálási jelentést készít.

#### Parancs használata
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: A célprojekt neve, amelybe az adatforrások importálásra kerülnek.
- **EXPORT_FILE**: Az importálandó export fájl neve.

#### Opciók

- `--output-file`, `-o`: A fájl, amelybe az importálási jelentést menti (ha nincs megadva, a kimenet terminálon táblázatos formátumban jelenik meg).
- `--output-format`, `-f`: Az importálási jelentés mentésének formátuma (json, csv).
    
#### Példa
  
Az import fájlból `my_export.json` származó adatforrások importálása a `ProjectB`-be:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Az import után a parancs megjeleníti az importált és kihagyott objektumok jelentését. Csak az új adatforrások kerülnek importálásra a `ProjectB`-be. Az importálandó és kihagyott objektumok megtekintéséhez használja a `plan-import-ds` parancsot.

## A `plan-import-ds` parancs használata

A `plan-import-ds` parancs a digna CLI-ben az adatforrás-export import előtti elemzésére szolgál, és importtervet készít megfelelő jelentéssel.

#### Parancs használata
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: A célprojekt neve, amelybe az objektumokat importálni tervezik.
- **EXPORT_FILE**: Az export fájl neve, amely az import előtt elemzésre kerül.

#### Opciók

- `--output-file`, `-o`: A fájl, amelybe az importterv jelentését menti (ha nincs megadva, a kimenet terminálon táblázatos formátumban jelenik meg).
- `--output-format`, `-f`: Az importterv jelentésének mentési formátuma (json, csv).
    
#### Példa
  
Annak ellenőrzése, hogy mely adatforrások kerülnek importálásra és melyek lesznek kihagyva a `my_export.json` fájlból a `ProjectB`-be történő importálás esetén:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ez a parancs csak az importtervet mutatja meg azokról az objektumokról, amelyek importálásra vagy kihagyásra kerülnek.
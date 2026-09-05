---
title: digna CLI Reference 2025.04 – Parancsok és példák | digna Dokumentáció
description: Teljes referencia a digna CLI 2025.04 kiadáshoz. Ismerje meg a felhasználók, tárolók és adatok kezelését olyan parancsokkal, mint add-user, check-repo-connection, upgrade-repo, inspect és továbbiak.
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Ez az oldal dokumentálja a ***digna*** CLI **2025.04** kiadásában elérhető összes parancsot, beleértve a használati példákat és opciókat.

---

## CLI alapok

---

## A `--help` opció használata

A `--help` opció információt ad az elérhető parancsokról és azok használatáról. Két fő módja van az opció használatának:

1. **Általános súgó megjelenítése:**
   
   Használja a --help opciót közvetlenül a ***dignacli*** kulcsszó után:  
   ```bash
   dignacli --help
   ```

2. **Súgó lekérése egy adott parancshoz:**  
  
   Részletes információkért egy adott parancsról, fűzze hozzá a `--help` opciót a parancshoz.
   Például az `add-user` parancs súgójának lekéréséhez futtassa:
   ```bash
   dignacli add-user --help
   ```

   ### kimenet:
      
   - **Parancs leírása:** Részletes leírást ad arról, mit csinál a parancs.  
   - **Szintaxis:** Megmutatja a pontos szintaxist, beleértve a kötelező és opcionális argumentumokat.  
   - **Opciók:** Felsorolja a parancsra jellemző opciókat és azok magyarázatát.  
   - **Példák:** Mutat példákat a parancs hatékony végrehajtására.

  
## A `check-repo-connection` parancs használata

A check-repo-connection parancs a ***digna*** CLI eszköz része, és arra szolgál, hogy tesztelje a kapcsolatot és a hozzáférést egy megadott ***digna*** tárolóhoz. A parancs ellenőrzi, hogy a CLI képes-e kommunikálni a tárolóval.
      
#### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres végrehajtás esetén a parancs megerősíti a kapcsolatot, és részleteket ad a tárolóról: Repository verzió, Host, Database és Schema.  
  
Ha a tárolóhoz való kapcsolódás nem sikerül, ellenőrizze a config.toml fájlt a helyes beállításokért.

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
  
Alapértelmezés szerint a ***digna*** parancsok konzol kimenete minimális. A legtöbb parancs lehetőséget nyújt további információk megjelenítésére az alábbi opciók segítségével:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A „verbose” és „debug” az információ részletességi szintjét határozza meg, míg a „logfile” kapcsoló lehetővé teszi a kimenet fájlba irányítását a konzol helyett.

## Felhasználókezelés

### Az `add-user` parancs használata
  
Az add-user parancs a ***digna*** CLI-ben új felhasználó hozzáadására szolgál a ***digna*** rendszerhez.
  
#### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- `--is_superuser`, `-su`: Kapcsoló, amely rendszergazdai jogosultságot ad az új felhasználónak.
- `--valid_until`, `-vu`: Lejárati dátum beállítása a felhasználói fiókra a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fióknak nincs lejárati ideje.

#### Példa

Új felhasználó hozzáadása `jdoe` felhasználónévvel, teljes névvel `John Doe` és jelszóval `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Új felhasználó hozzáadása lejárati dátummal:
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
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen kötelező argumentuma a parancsnak.

#### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs végrehajtásával a `jdoe` felhasználó törlődik a ***digna*** rendszerből, visszavonva hozzáférését és eltávolítva a kapcsolódó adatokat és jogosultságokat a tárolóból.

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
  
- `--is_superuser`, `-su`: Beállítja a felhasználót rendszergazdává, emelt szintű jogosultságokkal. Ez a kapcsoló nem igényel értéket.  
- `--valid_until`, `-vu`: Lejárati dátum beállítása a felhasználói fiókra a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
#### Példa
  
A `jdoe` felhasználó teljes nevének módosítása „Johnathan Doe”-ra és rendszergazdává tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### A `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben meglévő felhasználó jelszavának megváltoztatására szolgál.
  
#### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumentumok
  
- **USER_NAME**: Annak a felhasználónak a felhasználóneve, akinek a jelszavát módosítani kell (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
#### Példa
  
A `jdoe` felhasználó jelszavának megváltoztatása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### A `list-users` parancs használata

A `list-users` parancs a ***digna*** CLI-ben a rendszerbe regisztrált összes felhasználó listázására szolgál.

#### Parancs használata

```bash
dignacli list-users
```

A parancs csatlakozik a ***digna*** tárolóhoz, és felsorolja az összes felhasználót azonosítóval, felhasználónévvel, teljes névvel, rendszergazda státusszal és lejárati időbélyegekkel.

## Tárolókezelés

### Az `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** tároló frissítésére vagy inicializálására szolgál. Ez a parancs létfontosságú a frissítések alkalmazásához vagy a tároló infrastruktúrájának első beállításához.
  
#### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
#### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut; ekkor a végrehajtandó SQL utasításokat kinyomtatja, de nem hajtja végre őket. Hasznos a változtatások előnézetéhez anélkül, hogy módosítás történne a tárolóban.  

  
#### Példa
  
A ***digna*** tároló frissítése opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
A frissítés szimulációs módban történő futtatása (az SQL utasítások megtekintéséhez anélkül, hogy alkalmaznánk őket):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kulcsfontosságú a ***digna*** rendszer karbantartásához, biztosítva, hogy az adatbázis sémája és a tároló egyéb részei naprakészek legyenek a szoftver legújabb verziójával.

### Az `encrypt` parancs használata
  
Az `encrypt` parancs a ***digna*** CLI-ben jelszó titkosítására szolgál.
  
#### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
#### Példa
  
Jelszó titkosításához adja meg a jelszót argumentumként.  
Például a `mypassword123` titkosításához:
```bash
dignacli encrypt mypassword123
```
A parancs visszaadja a megadott jelszó titkosított változatát, amelyet biztonságos helyeken lehet használni. Ha a jelszóargumentum nincs megadva, a CLI hibát jelez a hiányzó argumentum miatt.

## A `generate-key` parancs használata
  
A `generate-key` parancs egy Fernet kulcs generálására szolgál, amely elengedhetetlen a tárolt jelszavak védelméhez a ***digna*** tárolóban.
  
#### Parancs használata
```bash
dignacli generate-key
```
  
## Adatkezelés

## A `clean-up` parancs használata

A `clean-up` parancs a ***digna*** CLI-ben profilok, predikciók és a közlekedési lámpa rendszer (traffic light system) adatainak törlésére szolgál egy vagy több adatforrásból egy megadott projektben. Ez a parancs fontos az adatok életciklus-kezeléséhez, segít rendszerezett és hatékony adatkörnyezet fenntartásában az elavult vagy szükségtelen adatok törlésével.

#### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, ahonnan az adatokat törölni kell (kötelező). Ha az argumentumban az all-projects kulcsszót használja, a ***digna*** minden meglévő projektre lefuttatja a parancsot.
- **FROM_DATE**: Az adateltávolítás kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adateltávolítás záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- `--table-name`, `-tn`: A clean-up műveletet egy adott táblára korlátozza a projekten belül.
- `--table-filter`, `-tf`: Csak azokat a táblákat célozza, amelyek nevében megtalálható a megadott részstring.
- `--timing`, `-tm`: A folyamat befejezése után megjeleníti a clean-up időtartamát.
- `--help`: A clean-up parancs súgóját jeleníti meg és kilép.
  
#### Példa
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. közötti időszakra:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Csak egy adott, `Table1` nevű táblából történő adatok eltávolítása:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében, és biztosítja, hogy a tároló csak a releváns információkat tartalmazza.

## A `list-projects` parancs használata
  
A `list-projects` parancs a ***digna*** CLI-ben az elérhető összes projekt listázására szolgál a ***digna*** rendszerben.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára, gyors áttekintést adva a ***digna*** tárolóban lévő projektekről.

## A `list-ds` parancs használata

A `list-ds` parancs a ***digna*** CLI-ben az adott projektben elérhető adatforrások listázására szolgál. A parancs hasznos az elemzésre és kezelésre rendelkezésre álló adathalmazok áttekintéséhez.

#### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentumok
- **PROJECT_NAME**: A projekt neve, amelyhez az adatforrásokat listázza (kötelező).
  
#### Példa
  
Az összes adatforrás listázása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
A parancs áttekintést nyújt a projektben elérhető adatforrásokról, segítve a felhasználókat az adatok kezelésében és navigálásában.

## Az `inspect` parancs használata

Az `inspect` parancs a ***digna*** CLI-ben profilok, predikciók és a közlekedési lámpa rendszer adatainak létrehozására szolgál egy vagy több adatforráshoz egy megadott projektben. A parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakon belül.

#### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyet ellenőrizni szeretne (kötelező). Ha az argumentumban az all-projects kulcsszót használja, a ***digna*** minden meglévő projektre lefuttatja a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Az ellenőrzést egy adott táblára korlátozza a projekten belül.
- `--table-filter`, `-tf`: Csak azokat a táblákat ellenőrzi, amelyek nevében megtalálható a megadott részstring.
- `--do-profile`: Elindítja a profilok újragyűjtését. Alapértelmezett állapot: do-profile.
- `--no-do-profile`: Megakadályozza a profilok újragyűjtését.
- `--do-prediction`: Elindítja a predikciók újraszámítását. Alapértelmezett állapot: do-prediction.
- `--no-do-prediction`: Megakadályozza a predikciók újraszámítását.
- `--do-alert-status`: Elindítja az riasztási státuszok újraszámítását. Alapértelmezett állapot: do-alert-status.
- `--no-do-alert-status`: Megakadályozza az riasztási státuszok újraszámítását.
- `--iterative`: Napi iterációk szerint végzi az ellenőrzést az időszakon. Alapértelmezett állapot: iterative.
- `--no-iterative`: Az egész időszakot egyben ellenőrzi.
- `--enable_notification`, `-en`: Engedélyezi az értesítések küldését riasztás esetén.
- `--timing`, `-tm`: Az ellenőrzés befejezése után megjeleníti a folyamat időtartamát.
  
#### Példa
  
Adatok ellenőrzése a `ProjectA` projektben 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy adott tábla ellenőrzése és a predikciók újraszámításának kikényszerítése:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos friss profilok és predikciók létrehozásához, az adatintegritás monitorozásához és a riasztási rendszer kezeléséhez egy adott projekten belüli időszakra.

## A `tls-status` parancs használata

A `tls-status` parancs a ***digna*** CLI-ben a Traffic Light System (TLS) státuszának lekérdezésére szolgál egy adott tábla esetén egy projektben egy megadott dátumra. A Traffic Light System betekintést nyújt az adatok egészségébe és minőségébe, jelezve az esetleges problémákat vagy riasztásokat.
  
#### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyhez a TLS státuszt lekérdezi (kötelező).
- **TABLE_NAME**: A projektben lévő adott tábla, amelyhez a TLS státusz szükséges (kötelező).
- **DATE**: A dátum, amelyre a TLS státuszt lekérdezi, általában a %Y-%m-%d formátumban (kötelező).
  
#### Példa
  
A `ProjectA` projekt `UserData` nevű táblájának TLS státuszának ellenőrzése 2024. július 1-jén:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

A parancs segít a felhasználóknak az adatminőség nyomon követésében és fenntartásában az előre meghatározott kritériumok alapján készített egyértelmű és akciózható státuszjelentéssel.

## Az `inspect-async` parancs használata

Az `inspect-async` parancs a ***digna*** CLI-ben arra szolgál, hogy aszinkron módon utasítsa a háttérrendszert egy vagy több adatforrás ellenőrzésére egy adott projekthez. Ha a projekt neve all-projects, az ellenőrzés minden elérhető projekten végigiterál. A parancs egy kérésazonosítót (request id) ad vissza, amellyel nyomon követhető az ellenőrzés állapota.

#### Parancs használata

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyet ellenőrizni szeretne (kötelező). Az all-projects kulcsszó használata esetén a ***digna*** az összes meglévő projekten végrehajtja az ellenőrzést.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Az ellenőrzést egy adott táblára korlátozza a projekten belül.
- `--table-filter`, `-tf`: Csak azokat a táblákat ellenőrzi, amelyek nevében megtalálható a megadott részstring.

  
#### Példa
  
Adatok aszinkron ellenőrzése a `ProjectA` projektben 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Az `inspect-status` parancs használata

Az `inspect-status` parancs a ***digna*** CLI-ben az aszinkron ellenőrzés előrehaladásának lekérdezésére szolgál a kérésazonosító alapján.

#### Parancs használata

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumentumok
  
- **REQUEST_ID**: Az `inspect-async` parancs által visszaadott kérésazonosító.
  
#### Opciók

- `--report_level`, `-rl`: Jelentési szint beállítása: 'task' vagy 'step' [alapértelmezett: task]
  
#### Példa
  
Az ellenőrzés előrehaladásának lekérdezése részletes, lépésenkénti szinten a 12345 kérésazonosító esetén:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Az `export-ds` parancs használata

Az `export-ds` parancs a ***digna*** CLI-ben az adatforrások exportálására szolgál a ***digna*** tárolóból. Alapértelmezés szerint egy adott projekt összes adatforrása exportálásra kerül.

#### Parancs használata
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt, ahonnan az adatforrásokat exportálni fogja.

#### Opciók

- `--table_name`, `-tn`: Egy adott adatforrás exportálása a projekten belül.
- `--exportfile`, `-ef`: Az export fájl nevének megadása.
    
#### Példa
  
Az összes adatforrás exportálása a `ProjectA` projektből:
  
```bash
dignacli export-ds ProjectA
```
  
A parancs JSON dokumentumként exportálja a `ProjectA` adatforrásait, amely importálható egy másik projekthez vagy ***digna*** tárolóhoz.


## Az `import-ds` parancs használata

Az `import-ds` parancs a ***digna*** CLI-ben adatforrások importálására szolgál egy célprojektbe, valamint import riport létrehozására.

#### Parancs használata
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelybe az adatforrásokat importálni fogja.
- **EXPORT_FILE**: Az importálandó adatforrás-export fájl neve.

#### Opciók

- `--output-file`, `-o`: A fájl, ahová az import riportot menti (ha nincs megadva, táblázatos formában a terminálra írja).
- `--output-format`, `-f`: Az import riport mentési formátuma (json, csv).
    
#### Példa
  
Az összes adatforrás importálása a `my_export.json` exportfájlból a `ProjectB` projektbe:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Az import után a parancs jelentést is mutat az importált és kihagyott objektumokról. Csak az új adatforrások lesznek importálva a `ProjectB`-be. Annak megtekintéséhez, hogy mely objektumok lennének importálva és melyek lennének kihagyva, használhatja a `plan-import-ds` parancsot.

## A `plan-import-ds` parancs használata

A `plan-import-ds` parancs a ***digna*** CLI-ben arra szolgál, hogy elemezze egy export fájlt és importtervet készítsen a célprojekt számára (mely objektumok kerülnének importálásra és melyek lennének kihagyva).

#### Parancs használata
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelybe az adatforrások importálásra kerülnének.
- **EXPORT_FILE**: Az export fájl neve, amelyet az import előtt elemezni kell.

#### Opciók

- `--output-file`, `-o`: A fájl, ahová az import riportot menti (ha nincs megadva, táblázatos formában a terminálra írja).
- `--output-format`, `-f`: Az import riport mentési formátuma (json, csv).
    
#### Példa
  
Annak ellenőrzése, hogy mely adatforrások kerülnének importálásra és melyek kerülnének kihagyásra a `my_export.json` fájlból, ha azt a `ProjectB`-be importálnák:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ez a parancs csak egy importtervet mutat a importálandó és kihagyandó objektumokról.
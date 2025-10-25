---
title: digna CLI Reference 2025.09 – Parancsok & Példák | digna Documentation
description: Teljes referencia a digna CLI 2025.109 verziójához. Ismerje meg, hogyan kezelheti a felhasználókat, repókat és adatokat az add-user, check-config, check-repo-connection, inspect, inspect-async és egyéb parancsokkal.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.09
**2025-09-29**

Ez az oldal dokumentálja a ***digna*** CLI **2025.09** kiadásában elérhető összes parancsot, használati példákat és opciókat.

---

## CLI alapok

---

### help
A `--help` opció információt ad az elérhető parancsokról és a használatról. Ezt az opciót két fő módon lehet használni:

1. **Általános segítség megjelenítése:**
   
    Használja a `--help`-et közvetlenül a `***digna***` szóra követően  
   ```bash
   dignacli --help
   ```

2. **Egy adott parancs súgója:**  
  
    Egy adott parancs részletes információjáért adja hozzá a `--help`-et a parancshoz.  
    Például, ha az `add-user` parancs súgóját szeretné látni, futtassa:
     ```bash
     dignacli add-user --help
     ```

     ### kimenet:
      
     - **Parancs leírása:** Részletesen elmagyarázza, mit csinál a parancs.  
     - **Szintaxis:** Megjeleníti a szükséges és opcionális argumentumokkal a teljes szintaxist.  
     - **Opciók:** Felsorolja a parancs-specifikus opciókat és azok leírását.  
     - **Példák:** Mutat példákat a parancs hatékony futtatására.

### check-config

A check-config parancs a ***digna*** CLI-ben segít a ***digna*** konfiguráció tesztelésében. Ez a parancs ellenőrzi, hogy a config.toml fájl tartalmazza-e a szükséges konfigurációs elemeket a ***digna*** komponensek számára.

#### Opciók

- `--configpath`, `-cp`: A konfigurációt tartalmazó fájl vagy könyvtár. Ha kihagyja, a ../config.toml lesz használva.
      
#### Parancs használata
```bash
dignacli check-config
```

Sikeres futtatás esetén a parancs megerősíti, hogy a konfiguráció teljes.  
  
Ha hiányos a konfiguráció, a hiányzó konfigurációs elemek listája megjelenik.

  
### check-repo-connection

A check-repo-connection parancs a ***digna*** CLI-ben egy megadott ***digna*** repóhoz való csatlakozást és hozzáférést teszteli. A parancs biztosítja, hogy a CLI képes legyen kommunikálni a repóval.
      
#### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres futtatás esetén a parancs igazolja a kapcsolatot és a repóról a következő információkat írja ki: Repository version, Host, Database és Schema.  
  
Ha a repóhoz való csatlakozás nem sikerül, ellenőrizze, hogy a helyes beállítások szerepelnek-e a config.toml fájlban.


### version

Az telepített *dignacli* verzió ellenőrzéséhez használja a `--version` opciót.  
  
#### Parancs használata
```bash
dignacli --version
```
  
#### Példa kimenet
```bash
dignacli version 2025.09
```

### naplózási opciók
  
Alapértelmezés szerint a ***digna*** parancsok konzol kimenete minimalista. A legtöbb parancs lehetőséget ad további információk megjelenítésére a következő opciókkal:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A “verbose” és “debug” a részletességi szintet határozza meg, míg a “logfile” opció a kimenetet egy fájlba irányítja a konzol helyett.

## Felhasználókezelés

### add-user
  
Az add-user parancs új felhasználó hozzáadására szolgál a ***digna*** rendszerhez, a ***digna*** CLI-n keresztül.
  
#### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- `--is_superuser`, `-su`: Jelző az új felhasználó superuser (rendszergazda) jogosultságainak megadásához.
- `--valid_until`, `-vu`: A felhasználói fiók lejárati időpontja `YYYY-MM-DD HH:MI:SS` formátumban. Ha nem adja meg, a fióknak nincs lejárati ideje.

#### Példa

Új felhasználó hozzáadása `jdoe` felhasználó névvel, teljes név `John Doe` és jelszó `password123`:
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Felhasználó hozzáadása lejárati idő megadásával:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
A `delete-user` parancs egy meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből a ***digna*** CLI-n keresztül.
  
#### Parancs használata
```bash
dignacli delete-user USER_NAME
```
  
#### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen szükséges argumentum.

#### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs futtatásakor a `jdoe` felhasználó eltávolításra kerül a ***digna*** rendszerből; hozzáférését visszavonják, és a repóban található kapcsolódó adatokat és jogosultságokat törlik.

### modify-user

A `modify-user` parancs egy meglévő felhasználó adatait frissíti a ***digna*** CLI-ben.

#### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentumok
  
- **USER_NAME**: A frissítendő felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Opciók  
  
- `--is_superuser`, `-su`: Beállítja a felhasználót superuser-ré, emelt jogosultságot adva. Ez a jelző nem igényel értéket.  
- `--valid_until`, `-vu`: A felhasználói fiók lejárati idejét adja meg `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes.  
  
#### Példa
  
A `jdoe` felhasználó teljes nevének megváltoztatása “Johnathan Doe”-ra és superuser-é tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
A `modify-user-pwd` parancs egy meglévő felhasználó jelszavának módosítására szolgál a ***digna*** CLI-ben.
  
#### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumentumok
  
- **USER_NAME**: A jelszót módosítandó felhasználó felhasználóneve (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
#### Példa
  
A `jdoe` felhasználó jelszavának megváltoztatása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

A `list-users` parancs listázza az összes, a ***digna*** rendszerben regisztrált felhasználót a ***digna*** CLI-n keresztül.

#### Parancs használata

```bash
dignacli list-users
```

A parancs csatlakozik a ***digna*** repóhoz és felsorolja az összes felhasználót ID, felhasználónév, teljes név, superuser státusz és lejárati időbélyegek szerint.

## Repó kezelés

### upgrade-repo
  
Az `upgrade-repo` parancs a ***digna*** repó frissítésére vagy inicializálására szolgál a ***digna*** CLI-ben. Ez a parancs szükséges a frissítések alkalmazásához vagy a repó infrastruktúrájának első telepítéséhez.
  
#### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
#### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut; kiírja a végrehajtandó SQL utasításokat, de nem futtatja őket. Hasznos a változtatások alkalmazása előtti előnézethez.  

  
#### Példa
  
A ***digna*** repó frissítése opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
A frissítés szimulációs módban futtatása (az SQL utasítások megtekintése, de nem végrehajtása):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kritikus a ***digna*** rendszer karbantartásához, biztosítva, hogy az adatbázis-séma és más repó komponensek kompatibilisek legyenek a szoftver legújabb verziójával.

### encrypt
  
Az `encrypt` parancs egy jelszó titkosítására szolgál a ***digna*** CLI-ben.
  
#### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
#### Példa
  
Adja meg a jelszót argumentumként egy jelszó titkosításához.   
Például a `mypassword123` jelszó titkosításához:
```bash
dignacli encrypt mypassword123
```
A parancs kiírja a megadott jelszó titkosított változatát; ezt a kimenetet biztonságosabb kontextusokban lehet használni. Ha nem ad meg jelszó-argumentumot, a CLI hibaüzenetet ad a hiányzó argumentumról.

### generate-key
  
A `generate-key` parancs Fernet kulcs generálására szolgál; ez a kulcs szükséges a ***digna*** repóban tárolt jelszavak védelméhez.
  
#### Parancs használata
```bash
dignacli generate-key
```
  
## Adatkezelés

### clean-up

A `clean-up` parancs eltávolítja egy vagy több adatforrás profiljait, predikcióit és a “traffic light” (forgalmi lámpa) rendszer adatait egy megadott projekt hatókörében a ***digna*** CLI-ben. Ez a parancs fontos az adatok életciklus-kezeléséhez; régi vagy felesleges adatok törlésével tisztán és hatékonyan tartja az adatkörnyezetet.

#### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelyből az adatokat törölni fogja (kötelező). Ha az argumentumnak az all-projects kulcsszót adja meg, a ***digna*** végigiterál az összes elérhető projekten és alkalmazza a parancsot.
- **FROM_DATE**: A törlés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: A törlés befejező dátuma és ideje; ugyanazokat a formátumokat használja, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- `--table-name`, `-tn`: A törlést korlátozza egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűri a táblákat, amelyek neve egy megadott részstringet tartalmaz.
- `--timing`, `-tm`: A törlési művelet befejezése után megjeleníti az időtartamot.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
#### Példa
  
Adatok törlése a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Csak a `Table1` nevű adott táblából való törlés:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adatok tárolásának kezelésében, biztosítva, hogy a repó csak a releváns információkat tartsa meg.

### remove-orphans
  
A `remove-orphans` parancs karbantartási célokra szolgál a ***digna*** repóban a ***digna*** CLI-n keresztül.  
Amikor egy felhasználó projekteket vagy adatforrásokat töröl, a profilok és predikciók előfordulhat, hogy a repóban “árván” maradnak. Ezzel a paranccsal az ilyen árva sorok eltávolíthatók a repóból.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

### list-projects
  
A `list-projects` parancs felsorolja az összes elérhető projektet a ***digna*** CLI-ben.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára; gyors áttekintést ad a ***digna*** repóban elérhető projektekről.

### list-ds

A `list-ds` parancs a megadott projektben található összes adatforrást felsorolja a ***digna*** CLI-ben. Ez a parancs segít megérteni az elérhető adatvagyonokat az elemzés és kezelés céljából.

#### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt, amelynek adatforrásait listázni szeretné (kötelező).
  
#### Példa
  
Az összes adatforrás kilistázása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs átfogó képet ad egy projektben található adatforrásokról, megkönnyítve az adatok hatékonyabb kezelését és navigációját.


### inspect

Az `inspect` parancs profillokat, predikciókat és a forgalmi lámpa (traffic light) rendszer adatait generálja egy megadott projekt vagy projektek körében a ***digna*** CLI-ben. Ez a parancs segít az adatok elemzésében és monitorozásában a megadott időintervallum alatt. A vizsgálat befejezésekor a számított forgalmi lámpa státuszkódot adja vissza:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelynek adatait ellenőrizni szeretné (kötelező). Ha az argumentum értéke all-projects, a ***digna*** végigmegy az összes projekten és alkalmazza a parancsot.
- **FROM_DATE**: A vizsgálat kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: A vizsgálat záró dátuma és ideje; ugyanazokat a formátumokat használja, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: A vizsgálatot egy adott táblára korlátozza a projektben.
- `--table-filter`, `-tf`: Csak azokat a táblákat vizsgálja, amelyek nevében szerepel a megadott részstring.
- `--enable_notification`, `-en`: Értesítések küldését engedélyezi riasztás esetén.
- `--bypass-backend`, `-bb`: Kihagyja a backend-et és közvetlenül a CLI-ból futtatja a vizsgálatot (csak tesztelésre!).

  
#### Példa
  
Adatok ellenőrzése a `ProjectA` projektben 2024. január 1. és 2024. január 31. között:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy adott tábla ellenőrzése és a predikciók újraszámolásának kényszerítése:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos frissített profilok és predikciók létrehozásához, az adatintegritás figyeléséhez, és a riasztási rendszerek kezeléséhez a megadott projekt és időtartam alatt.

### inspect-async

Az `inspect-async` parancs profilt, predikciókat és a forgalmi lámpa rendszer adatait generálja egy megadott projekt vagy projektek körében a ***digna*** CLI-ben aszinkron módon. Ellentétben az `inspect` paranccsal, ez a parancs nem várja meg a vizsgálat befejezését.  
Ehelyett visszaad egy request id-t a beküldött vizsgálati kérelemhez. A vizsgálat állapotának lekérdezésére használja az `inspect-status` parancsot.

#### Parancs használata

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelynek adatait ellenőrizni szeretné (kötelező). Ha all-projects értéket ad meg, a ***digna*** végigiterál az összes projekten és alkalmazza a parancsot.
- **FROM_DATE**: A vizsgálat kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: A vizsgálat záró dátuma és ideje; ugyanazokat a formátumokat használja, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: A vizsgálatot egy adott táblára korlátozza a projektben.
- `--table-filter`, `-tf`: Csak azokat a táblákat vizsgálja, amelyek nevében szerepel a megadott részstring.
- `--enable_notification`, `-en`: Értesítések küldését engedélyezi riasztás esetén.

  
#### Példa
  
Aszinkron vizsgálat futtatása a `ProjectA` projektben 2024. január 1. és 2024. január 31. között:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Az `inspect-status` parancs aszinkron vizsgálat állapotának lekérdezésére szolgál request ID alapján a ***digna*** CLI-ben.

#### Parancs használata

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentumok
  
- **REQUEST_ID**: Az `inspect-async` parancs által visszaadott request id.
  
#### Példa
  
Egy, 12345 request ID-val rendelkező vizsgálat állapotának lekérdezése:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Az `inspect-cancel` parancs egy adott request ID-hez tartozó vizsgálat vagy az összes aktuális kérés törlésére szolgál a ***digna*** CLI-ben.

#### Parancs használata

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentumok
  
- **REQUEST_ID**: Az `inspect-async` parancs által visszaadott request id. 
  
#### Példa
  
Egy, 12345 request ID-val rendelkező vizsgálat törlése:
  
```bash
dignacli inspect-cancel 12345
```

Az összes jelenleg futó vagy várakozó kérés törlése:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Az `export-ds` parancs az adatforrások exportálására szolgál a ***digna*** CLI-ben. Alapértelmezés szerint a megadott projekt összes adatforrása exportálásra kerül.

#### Parancs használata
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt, amelyből az adatforrások exportálódnak.

#### Opciók

- `--table_name`, `-tn`: Egy adott adatforrást exportál a projektből.
- `--exportfile`, `-ef`: Megadja az export fájl nevét.
    
#### Példa
  
Az összes adatforrás exportálása a `ProjectA` projektből:
  
```bash
dignacli export-ds ProjectA
```
  
A parancs egy JSON dokumentumot hoz létre, amely a `ProjectA` összes adatforrását tartalmazza, és amely áthelyezhető másik projektbe vagy ***digna*** repóba.


### import-ds

Az `import-ds` parancs adatforrások importálására szolgál egy célprojektbe a ***digna*** CLI-ben, és import jelentést készít.

#### Parancs használata
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt, amelybe az adatforrások importálódnak.
- **EXPORT_FILE**: Az importálandó export fájl neve.

#### Opciók

- `--output-file`, `-o`: Az import jelentés mentési fájlja (ha nincs megadva, a jelentés táblázatos formában a terminálra íródik).
- `--output-format`, `-f`: Az import jelentés formátuma (json, csv).
    
#### Példa
  
Az export fájlban (`my_export.json`) található összes adatforrás importálása a `ProjectB` projektbe:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Az import után a parancs megjeleníti az importált és kihagyott objektumok jelentését. Csak az új adatforrások lesznek importálva a `ProjectB`-be. Az importálás előtt megtekintheti, mely objektumok kerülnek importálásra vagy kihagyásra a `plan-import-ds` paranccsal.

### plan-import-ds

A `plan-import-ds` parancs elemzést készít arról, hogy egy export fájl importálása esetén mely adatforrások kerülnének importálásra és melyek kerülnének kihagyásra a célprojektben a ***digna*** CLI-ben.

#### Parancs használata
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Az a célprojekt, amelyre nézve az elemzést végzi (ahová importálni tervez).
- **EXPORT_FILE**: Az importálás előtt elemzendő export fájl neve.

#### Opciók

- `--output-file`, `-o`: Az import terv jelentésének mentési fájlja (ha nincs megadva, a jelentés táblázatos formában a terminálra íródik).
- `--output-format`, `-f`: Az import terv jelentés formátuma (json, csv).
    
#### Példa
  
Ellenőrizze, hogy a `my_export.json` fájl mely adatforrásokat importálná a `ProjectB`-be és melyeket hagyná ki:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ez a parancs csak egy import tervet jelenít meg az importálandó és kihagyandó objektumokról.
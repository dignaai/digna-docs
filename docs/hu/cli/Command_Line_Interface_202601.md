---
title: digna CLI Reference 2026.01 – Parancsok és példák | digna Dokumentáció
description: Teljes referencia a digna CLI kiadásról 2026.01. Ismerje meg a felhasználók, adattárak és adatok kezelését olyan parancsokkal, mint az add-user, check-config, check-repo-connection, inspect, inspect-async és továbbiak.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202601/
image: /assets/logo_square.png
---

# digna CLI Reference 2026.01
**2026-01-15**

Ez az oldal dokumentálja a ***digna*** CLI **2026.01** kiadásában elérhető összes parancsot, beleértve a használati példákat és opciókat.

---

## CLI alapok

---

### help
A `--help` opció információt ad az elérhető parancsokról és azok használatáról. Két fő módja van ennek az opció használatának:

1. **Általános súgó megjelenítése:**
   
    Használja a --help-et közvetlenül a ***dignacli*** parancs után  
   ```bash
   dignacli --help
   ```

2. **Specifikus parancs súgó lekérése:**  
  
    Részletes információkért egy adott parancsról, fűzze hozzá a `--help` opciót a parancshoz.
    Például, ha az `add-user` parancs súgóját szeretné megtekinteni, futtassa:
     ```bash
     dignacli add-user --help
     ```

     ### kimenet:
      
     - **Parancs leírása:** Részletes leírást ad arról, mit csinál a parancs.  
     - **Szintaxis:** Megmutatja a pontos szintaxist, beleértve a kötelező és opcionális argumentumokat.  
     - **Opciók:** Felsorolja az adott parancshoz tartozó opciókat és magyarázatukat.  
     - **Példák:** Bemutat példákat a parancs hatékony végrehajtására.

### check-config

A check-config parancs a ***digna*** CLI eszköztár része, amely a ***digna*** konfigurációjának tesztelésére szolgál. Ez a parancs biztosítja, hogy a ***digna*** komponensek megtalálják a szükséges konfigurációs elemeket a config.toml fájlban.

#### Opciók

- `--configpath`, `-cp`: Fájl vagy könyvtár, amely a konfigurációt tartalmazza. Ha elhagyják, a ../config.toml lesz használva.
      
#### Parancs használata
```bash
dignacli check-config
```

Sikeres végrehajtás esetén a parancs megerősítést ad a konfiguráció teljességéről.  
  
Ha a konfiguráció hiányosnak tűnik, a hiányzó konfigurációs elemek felsorolásra kerülnek.

  
### check-repo-connection

A check-repo-connection parancs a ***digna*** CLI eszköztár része, amely az adott ***digna*** adattárhoz való kapcsolódás és hozzáférés tesztelésére szolgál. Ez a parancs biztosítja, hogy a CLI képes legyen kommunikálni az adattárral.
      
#### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres végrehajtás esetén a parancs megerősíti a kapcsolatot, és részleteket ad az adattárról: Repository version, Host, Database és Schema.  
  
Ha az adattárhoz való kapcsolat nem sikeres, ellenőrizze a config.toml fájlt a helyes konfigurációs beállításokért.


### version

Az telepített *dignacli* verziójának ellenőrzéséhez használja a --version opciót.  
  
#### Parancs használata
```bash
dignacli --version
```
  
#### Példa kimenet
```bash
dignacli version 2026.01
```

### naplózási opciók
  
Alapértelmezés szerint a ***digna*** parancsok konzol kimenete minimalista. A legtöbb parancs lehetőséget kínál további információk megjelenítésére az alábbi opciók használatával:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A „verbose” és a „debug” a részletek szintjét határozza meg, míg a „logfile” kapcsoló lehetővé teszi a kimenet fájlba történő átirányítását a konzol helyett.

## Felhasználókezelés

### add-user
  
Az add-user parancs a ***digna*** CLI-ben új felhasználó hozzáadására szolgál a ***digna*** rendszerhez.
  
#### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- `--is_superuser`, `-su`: Jelölőkapcsoló, amely rendszergazdaként jelöli az új felhasználót.
- `--valid_until`, `-vu`: Lejárati dátumot állít be a felhasználói fiókra a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fióknak nincs lejárati dátuma.

#### Példa

Új felhasználó hozzáadása `jdoe` felhasználónévvel, teljes névvel `John Doe` és jelszóval `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Új felhasználó hozzáadása lejárati dátummal:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
A `delete-user` parancs a ***digna*** CLI-ben egy meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből.
  
#### Parancs használata
```bash
dignacli delete-user USER_NAME
```
  
#### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen kötelező argumentum.

#### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs végrehajtásával a `jdoe` felhasználó eltávolításra kerül a ***digna*** rendszerből, ezzel visszavonva a hozzáférését és törölve a kapcsolódó adatait és jogosultságait az adattárból.

### modify-user

A `modify-user` parancs a ***digna*** CLI-ben egy meglévő felhasználó adatainak frissítésére szolgál a ***digna*** rendszerben.

#### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Opciók  
  
- `--is_superuser`, `-su`: A felhasználót superuserré állítja, emelt szintű jogosultságokat adva. Ez a kapcsoló nem igényel értéket.  
- `--valid_until`, `-vu`: Lejárati dátumot állít be a felhasználói fiókra a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
#### Példa
  
A `jdoe` felhasználó teljes nevének módosítása „Johnathan Doe”-ra és superuserré tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben egy meglévő felhasználó jelszavának megváltoztatására szolgál a ***digna*** rendszerben.
  
#### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumentumok
  
- **USER_NAME**: A felhasználó felhasználóneve, akinek a jelszavát módosítani kell (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
#### Példa
  
A `jdoe` felhasználó jelszavának megváltoztatása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

A `list-users` parancs a ***digna*** CLI-ben felsorolja a ***digna*** rendszerben regisztrált összes felhasználót.

#### Parancs használata

```bash
dignacli list-users
```

A parancs végrehajtásakor a ***digna*** CLI csatlakozik az adattárhoz és listázza az összes felhasználót, megjelenítve az ID-t, felhasználónevet, teljes nevet, superuser státuszt és lejárati időbélyegeket.

## Adatkezelés

### upgrade-repo
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben az adattár frissítésére vagy inicializálására szolgál. Ez a parancs elengedhetetlen a frissítések alkalmazásához vagy az adattár infrastruktúrájának első beállításához.
  
#### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
#### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezett, a parancs szimulációs módban fut, ami kiírja azokat az SQL utasításokat, amelyeket végrehajtana, de nem hajtja végre azokat. Hasznos a változtatások előnézetéhez anélkül, hogy módosítaná az adattárat.  

  
#### Példa
  
Az adattár frissítéséhez futtassa a parancsot opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
A frissítés szimulációs módban történő futtatásához (az SQL utasítások megtekintéséhez anélkül, hogy alkalmazná őket):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kulcsfontosságú a ***digna*** rendszer karbantartásához, biztosítva, hogy az adatbázis sémája és az egyéb adattár komponensek naprakészek legyenek a szoftver legújabb verziójával.

### encrypt
  
Az `encrypt` parancs a ***digna*** CLI-ben jelszó titkosítására szolgál.
  
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
A parancs a megadott jelszó titkosított változatát adja vissza, amely biztonságos kontextusokban használható. Ha a jelszó argumentum nem kerül megadásra, a CLI hibát jelez a hiányzó argumentum miatt.

### generate-key
  
A `generate-key` parancs egy Fernet kulcs generálására szolgál, amely szükséges a jelszavak biztonságos tárolásához a ***digna*** adattárban.
  
#### Parancs használata
```bash
dignacli generate-key
```
  
## Adatkezelés (Data Management)

### clean-up

A `clean-up` parancs a ***digna*** CLI-ben profilok, előrejelzések és a forgalmi lámpa rendszer adatait távolítja el egy vagy több adatforrásból egy adott projektben. Ez a parancs fontos az adatok életciklus-kezeléséhez, segít megőrizni a rendezett és hatékony adatkörnyezetet az elavult vagy felesleges adatok törlésével.

#### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, ahonnan az adatokat törölni kell (kötelező). Az all-projects kulcsszó használata esetén a ***digna*** minden meglévő projekten végighalad és alkalmazza a parancsot.
- **FROM_DATE**: Az adattörlés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adattörlés záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- `--table-name`, `-tn`: Korlátozza a clean-up műveletet egy adott táblára a projekten belül.
- `--table-filter`, `-tf`: Szűrők, amelyekkel a törlést csak a megadott részstringet tartalmazó táblákra lehet korlátozni.
- `--timing`, `-tm`: A clean-up folyamat időtartamának megjelenítése a befejezés után.
- `--help`: Súgó információk megjelenítése a clean-up parancsról, majd kilépés.
  
#### Példa
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Csak egy konkrét `Table1` nevű táblából történő törlés:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében és biztosítja, hogy az adattár csak a releváns információkat tartalmazza.

### remove-orphans
  
A `remove-orphans` parancs a ***digna*** CLI-ben karbantartási műveletekhez használható az adattárban.  
Amikor egy felhasználó projekteket vagy adatforrásokat töröl, a profilok és előrejelzések gyakran az adattárban maradnak. Ezzel a paranccsal az ilyen árva sorok eltávolíthatók az adattárból.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

### list-projects
  
A `list-projects` parancs a ***digna*** CLI-ben az elérhető projektek listázására szolgál a ***digna*** rendszerben.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára, gyors áttekintést nyújtva a ***digna*** adattárban található projektekről.

### list-ds

A `list-ds` parancs a ***digna*** CLI-ben az adott projektben elérhető adatforrások listázására szolgál. Ez a parancs hasznos az elemzésre és kezelésre rendelkezésre álló adatvagyon megismeréséhez a ***digna*** rendszerben.

#### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt neve, amelynek adatforrásait listázni kívánjuk (kötelező).
  
#### Példa
  
Az összes adatforrás listázása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést ad a projektben elérhető adatforrásokról, segítve a felhasználókat az adatkörnyezet hatékonyabb kezelésében.

### inspect

Az `inspect` parancs a ***digna*** CLI-ben profilok, előrejelzések és a forgalmi lámpa rendszer adatainak létrehozására szolgál egy vagy több adatforráshoz egy adott projektben. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakra vonatkozóan. A vizsgálat befejeztével a számított forgalmi lámpa rendszer értékét adja vissza:
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyen az adatokat vizsgálni kell (kötelező). Az all-projects kulcsszó használata esetén a ***digna*** minden meglévő projekten végighalad és alkalmazza a parancsot.
- **FROM_DATE**: Az adatok vizsgálatának kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adatok vizsgálatának záró dátuma és ideje, ugyanezekkel a formátumokkal (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Korlátozza az inspect műveletet egy adott táblára a projekten belül.
- `--table-filter`, `-tf`: Csak azokat a táblákat vizsgálja, amelyek neve a megadott részstringet tartalmazza.
- `--enable_notification`, `-en`: Értesítések küldésének engedélyezése riasztás esetén.
- `--bypass-backend`, `-bb`: Megkerüli a backend-et és közvetlenül a CLI-ből futtatja az inspect-et (csak tesztelési célokra!).

  
#### Példa
  
Adatok vizsgálata a `ProjectA` projektben 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy adott tábla vizsgálata és az előrejelzések újraszámítása kényszerítve:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos friss profilok és előrejelzések generálásához, az adatintegritás monitorozásához és a riasztási rendszer kezeléséhez egy adott projekt időszakában.

### inspect-async

Az `inspect-async` parancs a ***digna*** CLI-ben profilok, előrejelzések és a forgalmi lámpa rendszer adatainak létrehozását indítja el egy vagy több adatforráshoz egy adott projektben. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakra vonatkozóan. Ellentétben az `inspect` paranccsal, ez nem várja meg a vizsgálat befejezését.
Ehelyett visszaadja a beküldött vizsgálati kérés azonosítóját. A vizsgálat előrehaladásának lekérdezéséhez használja az `inspect-status` parancsot.

#### Parancs használata

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyen az adatokat vizsgálni kell (kötelező). Az all-projects kulcsszó használata esetén a ***digna*** minden meglévő projekten végighalad és alkalmazza a parancsot.
- **FROM_DATE**: Az adatok vizsgálatának kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adatok vizsgálatának záró dátuma és ideje, ugyanezekkel a formátumokkal (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Korlátozza az inspect műveletet egy adott táblára a projekten belül.
- `--table-filter`, `-tf`: Csak azokat a táblákat vizsgálja, amelyek neve a megadott részstringet tartalmazza.
- `--enable_notification`, `-en`: Értesítések küldésének engedélyezése riasztás esetén.

  
#### Példa
  
Adatok vizsgálatának aszinkron indítása a `ProjectA` projektben 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Az `inspect-status` parancs a ***digna*** CLI-ben az aszinkron vizsgálat előrehaladásának ellenőrzésére szolgál a kérésazonosító alapján.

#### Parancs használata

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentumok
  
- **REQUEST_ID**: Az `inspect-async` parancs által visszaadott kérésazonosító 
  
#### Példa
  
Egy 12345 kérésazonosítójú vizsgálat előrehaladásának ellenőrzése:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Az `inspect-cancel` parancs a ***digna*** CLI-ben a vizsgálatok megszakítására szolgál kérésazonosító alapján, vagy az összes aktuális kérés megszakítására is használható.

#### Parancs használata

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentumok
  
- **REQUEST_ID**: Az `inspect-async` parancs által visszaadott kérésazonosító 
  
#### Példa
  
Egy 12345 kérésazonosítójú vizsgálat megszakítása:
  
```bash
dignacli inspect-cancel 12345
```

Az összes jelenleg futó vagy függőben lévő kérés megszakítása:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Az `export-ds` parancs a ***digna*** CLI-ben adatforrások exportálására szolgál a ***digna*** adattárból. Alapértelmezés szerint egy adott projekt összes adatforrása exportálásra kerül.

#### Parancs használata
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt neve, amelyből az adatforrások exportálásra kerülnek.

#### Opciók

- `--table_name`, `-tn`: Egy adott adatforrás exportálása a projektből.
- `--exportfile`, `-ef`: Az export fájlnevének megadása.
    
#### Példa
  
Az összes adatforrás exportálása a `ProjectA` nevű projektből:
  
```bash
dignacli export-ds ProjectA
```
  
Ez a parancs a `ProjectA` összes adatforrását JSON dokumentumként exportálja, amely importálható egy másik projektbe vagy ***digna*** adattárba.


### import-ds

Az `import-ds` parancs a ***digna*** CLI-ben adatforrások importálására szolgál egy célprojektbe, és import riportot készít.

#### Parancs használata
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt neve, amelybe az adatforrások importálásra kerülnek.
- **EXPORT_FILE**: Az importálandó adatforrás export fájl neve.

#### Opciók

- `--output-file`, `-o`: A fájl, ahová az import riport mentésre kerül (ha nincs megadva, táblázatos formában a terminálra írja).
- `--output-format`, `-f`: Az import riport mentésének formátuma (json, csv).
    
#### Példa
  
Az összes adatforrás importálása a `my_export.json` export fájlból a `ProjectB`-be:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Az import után a parancs riportot is megjelenít az importált és kihagyott objektumokról. Csak az új adatforrások kerülnek importálásra `ProjectB`-be. Ha szeretné megtudni, mely objektumok kerülnének importálásra vagy kihagyásra, használja a `plan-import-ds` parancsot.

### plan-import-ds

A `plan-import-ds` parancs a ***digna*** CLI-ben az adatforrások importálásának előzetes vizsgálatára szolgál, és import tervet készít az elemzéshez.

#### Parancs használata
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt neve, amelybe az adatforrások importálásra kerülnének.
- **EXPORT_FILE**: Az export fájl neve, amelyet az import előtt elemezni kell.

#### Opciók

- `--output-file`, `-o`: A fájl, ahová az import riport mentésre kerül (ha nincs megadva, táblázatos formában a terminálra írja).
- `--output-format`, `-f`: Az import riport mentésének formátuma (json, csv).
    
#### Példa
  
Annak ellenőrzése, hogy mely adatforrások kerülnének importálásra és melyek lennének kihagyva a `my_export.json` fájlból `ProjectB`-be történő importálás esetén:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ez a parancs csak egy import tervet jelenít meg az importálandó és kihagyandó objektumokról.
---
title: digna CLI Referencia 2025.09 – Parancsok & Példák | digna Dokumentáció
description: Teljes referencia a digna CLI kiadásról 2025.09. Ismerje meg, hogyan kezelhet felhasználókat, repository-kat és adatokat olyan parancsokkal, mint az add-user, check-config, check-repo-connection, inspect, inspect-async és még több.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# digna CLI Referencia 2025.09
**2025-09-29**

Ez az oldal dokumentálja a ***digna*** CLI **2025.09** kiadásában elérhető parancsok teljes készletét, beleértve használati példákat és opciókat.

---

## CLI alapok

---

### help
A `--help` opció információt ad az elérhető parancsokról és azok használatáról. Két fő módja van ennek az opció használatának:

1. **Általános súgó megjelenítése:**
   
    Használja a --help-et közvetlenül a ***dignacli*** kulcsszó után  
   ```bash
   dignacli --help
   ```

2. **Specifikus parancs súgó lekérése:**  
  
    Részletes információkért egy adott parancsról, adja hozzá a `--help`-et a parancs után.  
    Például, ha az `add-user` parancs súgóját szeretné megkapni, futtassa:
     ```bash
     dignacli add-user --help
     ```

     ### Kimenet:
      
     - **Parancsleírás:** Részletes magyarázat arról, mit csinál a parancs.  
     - **Szin­taxis:** Pontos szintaxis megjelenítése, beleértve a kötelező és választható argumentumokat.  
     - **Opciók:** Felsorolja a parancsra jellemző opciókat és azok magyarázatát.  
     - **Példák:** Mutat példákat a parancs hatékony használatára.

### check-config

A check-config parancs a ***digna*** CLI-ben arra szolgál, hogy tesztelje a ***digna*** konfigurációját. Ez a parancs biztosítja, hogy a ***digna*** komponensek megtalálják a szükséges beállításokat a config.toml fájlban.

#### Opciók

- `--configpath`, `-cp`: Az a fájl vagy könyvtár, amely a konfigurációt tartalmazza. Ha elhagyják, a ../config.toml lesz használva.
      
#### Parancspélda
```bash
dignacli check-config
```

Sikeres futtatás esetén a parancs megerősíti, hogy a konfiguráció teljes.  
  
Ha a konfiguráció hiányosnak tűnik, a hiányzó beállítások listája megjelenik.

  
### check-repo-connection

A check-repo-connection parancs a ***digna*** CLI-ben arra szolgál, hogy tesztelje egy megadott ***digna*** repository kapcsolatát és hozzáférését. Ez a parancs ellenőrzi, hogy a CLI képes-e kommunikálni a repository-val.
      
#### Parancspélda
```bash
dignacli check-repo-connection
```

Sikeres futtatás esetén a parancs kiírja a kapcsolódás megerősítését, valamint részleteket a repository-ról: Repository-verzió, Host, Database és Schema.  
  
Ha a repository-hoz való kapcsolódás nem sikerül, ellenőrizze a config.toml fájlt a helyes konfigurációs beállításokért.


### version

A telepített *dignacli* verzió ellenőrzéséhez használja a --version opciót.  
  
#### Parancspélda
```bash
dignacli --version
```
  
#### Példa kimenet
```bash
dignacli version 2025.09
```

### naplózási opciók
  
Alapértelmezésben a ***digna*** parancsok konzol kimenete minimális. A legtöbb parancs lehetőséget ad további információk megjelenítésére az alábbi opciókkal:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A “verbose” és “debug” határozza meg a részletességi szintet, míg a “logfile” kapcsoló lehetővé teszi a kimenet fájlba irányítását a konzol helyett.

## Felhasználókezelés

### add-user
  
Az add-user parancs a ***digna*** CLI-ben új felhasználó hozzáadására szolgál a ***digna*** rendszerhez.
  
#### Parancspélda
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- `--is_superuser`, `-su`: Jelző az új felhasználó adminisztrátorrá tételéhez.
- `--valid_until`, `-vu`: Felhasználói fiók lejárati dátumának beállítása a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fiók nem jár le.

#### Példa

Új felhasználó hozzáadásához `jdoe` felhasználónévvel, `John Doe` teljes névvel és `password123` jelszóval:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Új felhasználó hozzáadása lejárati dátummal:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
A `delete-user` parancs a ***digna*** CLI-ben meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből.
  
#### Parancspélda
```bash
dignacli delete-user USER_NAME
```
  
#### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen szükséges argumentum.

#### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs futtatása eltávolítja a `jdoe` felhasználót a ***digna*** rendszerből, visszavonja hozzáférését és törli a kapcsolódó adatokat és jogosultságokat a repository-ból.

### modify-user

A `modify-user` parancs a ***digna*** CLI-ben meglévő felhasználó adatainak frissítésére szolgál a ***digna*** rendszerben.

#### Parancspélda
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Opciók  
  
- `--is_superuser`, `-su`: A felhasználó superuserként történő megjelölése, emelt jogosultságokkal. Ez a kapcsoló nem igényel értéket.  
- `--valid_until`, `-vu`: Felhasználói fiók lejárati dátumának beállítása a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
#### Példa
  
A `jdoe` felhasználó teljes nevének módosítása „Johnathan Doe”-ra és superuserként való megjelölése:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben meglévő felhasználó jelszavának megváltoztatására szolgál.
  
#### Parancspélda
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumentumok
  
- **USER_NAME**: A jelszót módosítandó felhasználó felhasználóneve (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
#### Példa
  
A `jdoe` felhasználó jelszavának módosítása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

A `list-users` parancs a ***digna*** CLI-ben az összes regisztrált felhasználó listázására szolgál a ***digna*** rendszerben.

#### Parancspélda

```bash
dignacli list-users
```

A parancs futtatásakor a ***digna*** CLI csatlakozik a ***digna*** repository-hoz és felsorolja az összes felhasználót, megjelenítve ID-jukat, felhasználónevüket, teljes nevüket, superuser státuszukat és lejárati időpontjaikat.

## Repository-kezelés

### upgrade-repo
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ez a parancs kulcsfontosságú a frissítések alkalmazásához vagy a repository infrastruktúra elsődleges beállításához.
  
#### Parancspélda

```bash
dignacli upgrade-repo [options]
```
  
#### Opciók
  
- `--simulation-mode`, `-s`: Ha aktiválva van, ez az opció szimulációs módban futtatja a parancsot, és kiírja azokat az SQL utasításokat, amelyek lefutnának, de valójában nem hajtja végre őket. Hasznos a változtatások előnézetéhez anélkül, hogy módosításokat végezne a repository-n.  

  
#### Példa
  
A ***digna*** repository frissítéséhez futtassa a parancsot opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
Az upgrade futtatása szimulációs módban (SQL utasítások megtekintéséhez anélkül, hogy alkalmazná őket):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs fontos a ***digna*** rendszer karbantartásához, és biztosítja, hogy az adatbázis-séma és más repository-komponensek naprakészek legyenek a szoftver legújabb verziójához képest.

### encrypt
  
Az `encrypt` parancs a ***digna*** CLI-ben jelszó titkosítására szolgál.
  
#### Parancspélda
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
#### Példa
  
Egy jelszó titkosításához adja meg a jelszót argumentumként.  
Például az `mypassword123` titkosításához használja:
```bash
dignacli encrypt mypassword123
```
A parancs visszaadja a megadott jelszó titkosított változatát, amelyet ezután biztonságos környezetben lehet használni. Ha a jelszóargumentum nincs megadva, a CLI hibát jelez a hiányzó argumentum miatt.

### generate-key
  
A `generate-key` parancs Fernet-kulcs generálására szolgál, amely alapvető a ***digna*** repository-ban tárolt jelszavak védelméhez.
  
#### Parancspélda
```bash
dignacli generate-key
```
  
## Adatkezelés

### clean-up

A `clean-up` parancs a ***digna*** CLI-ben profilok, előrejelzések és adat eltávolítására szolgál a jelzőrendszerből egy vagy több adatforrás esetén egy adott projekten belül. Ez a parancs fontos az adatok élettartamának kezeléséhez, és segít rendezett, hatékony adatkészlet fenntartásában az elavult vagy nem szükséges adatok eltávolításával.

#### Parancspélda

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, ahonnan az adatokat eltávolítják (kötelező). Az all-projects kulcsszó használata arra utasítja a ***digna***-t, hogy végigiteráljon az összes meglévő projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az adat-tisztítás kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adat-tisztítás záró dátuma és ideje, ugyanazokat a formátumokat fogadva el, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- `--table-name`, `-tn`: Korlátozza a clean-up műveletet egy adott táblára a projekten belül.
- `--table-filter`, `-tf`: Szűrő, amely korlátozza a clean-up-ot olyan táblákra, amelyek neve tartalmazza a megadott alstringet.
- `--timing`, `-tm`: A clean-up folyamat időtartamának megjelenítése a futtatás befejezése után.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
#### Példa
  
Adatok törlése a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Adatok eltávolítása csak a `Table1` nevű konkrét táblából:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében és biztosítja, hogy a repository csak releváns információkat tartson.

### remove-orphans
  
A `remove-orphans` parancs a ***digna*** CLI-ben a repository karbantartására szolgál.  
Amikor egy felhasználó töröl projekteket vagy adatforrásokat, a profilok és előrejelzések gyakran az orphan (szülő nélküli) sorokként maradnak a repository-ban. Ezzel a paranccsal az ilyen szülő nélküli sorok eltávolíthatók a repository-ból.
  
#### Parancspélda
  
```bash
dignacli list-projects
```

### list-projects
  
A `list-projects` parancs a ***digna*** CLI-ben az összes elérhető projekt listázására szolgál a ***digna*** rendszerben.
  
#### Parancspélda
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára, gyors áttekintést adva azokról a projektekről, amelyek megtalálhatók a ***digna*** repository-ban.

### list-ds

A `list-ds` parancs a ***digna*** CLI-ben az összes elérhető adatforrás listázására szolgál egy megadott projekten belül. Ez a parancs hasznos annak megértéséhez, milyen adaterőforrások állnak rendelkezésre elemzésre és kezelésre a ***digna*** rendszerben.

#### Parancspélda
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelynek adatforrásait listázni kell (kötelező).
  
#### Példa
  
Az összes adatforrás listázása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést ad a projektben elérhető adatforrásokról, és segít hatékonyabban navigálni és kezelni az adatok világát.


### inspect

Az `inspect` parancs a ***digna*** CLI-ben profilok, előrejelzések és jelzőrendszer adatok létrehozására szolgál egy vagy több adatforráshoz egy adott projektben. Ez a parancs segít az adatok elemzésében és felügyeletében egy meghatározott időszakon belül. A befejezett ellenőrzés után a parancs visszaadja a számított jelzőrendszer értékét:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Parancspélda

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyre az adatok ellenőrzése történik (kötelező). Az all-projects kulcsszó használata arra utasítja a ***digna***-t, hogy végigmenjen az összes projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és ideje, ugyanolyan formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Korlátozza az ellenőrzést egy adott táblára a projekten belül.
- `--table-filter`, `-tf`: Szűri az ellenőrzést, hogy csak azok a táblák legyenek ellenőrizve, amelyek neve tartalmazza a megadott alstringet.
- `--enable_notification`, `-en`: Engedélyezi az eseményekről történő értesítések küldését.
- `--bypass-backend`, `-bb`: Megkerüli a backendet és közvetlenül a CLI-ből futtatja az ellenőrzést (csak tesztelési célokra!).

  
#### Példa
  
Adatok ellenőrzése a `ProjectA` projektben 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Egy konkrét tábla ellenőrzése és az előrejelzések újraszámításának kényszerítése:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos friss profilok és előrejelzések generálásához, az adatintegritás ellenőrzéséhez és az értesítési rendszerek kezeléséhez egy adott projektidőszakon belül.

### inspect-async

Az `inspect-async` parancs a ***digna*** CLI-ben profilok, előrejelzések és jelzőrendszer adatok létrehozására szolgál egy vagy több adatforráshoz egy adott projektben. Ez a parancs segít az adatok elemzésében és felügyeletében egy meghatározott időszakon belül. Ellentétben az `inspect`-tel, ez a parancs nem várja meg az ellenőrzés befejezését.
Helyette visszaadja a request-id-t az elindított ellenőrzési kérelemhez. Az ellenőrzés állapotának lekérdezéséhez használja az `inspect-status` parancsot.

#### Parancspélda

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyre az adatok ellenőrzése történik (kötelező). Az all-projects kulcsszó használata arra utasítja a ***digna***-t, hogy végigiteráljon az összes projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és ideje, ugyanazokat a formátumokat elfogadva, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Korlátozza az ellenőrzést egy adott táblára a projekten belül.
- `--table-filter`, `-tf`: Szűri az ellenőrzést, hogy csak azok a táblák legyenek ellenőrizve, amelyek neve tartalmazza a megadott alstringet.
- `--enable_notification`, `-en`: Engedélyezi az eseményekről történő értesítések küldését.

  
#### Példa
  
Aszinkron ellenőrzés futtatása a `ProjectA` projekt adataira 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Az `inspect-status` parancs a ***digna*** CLI-ben az aszinkron ellenőrzés előrehaladásának lekérdezésére szolgál a request-id alapján.

#### Parancspélda

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentumok
  
- **REQUEST_ID**: A `inspect-async` parancs által visszaadott request-id 
  
#### Példa
  
Az ellenőrzés előrehaladásának lekérdezése 12345 request-id alapján:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Az `inspect-cancel` parancs a ***digna*** CLI-ben az ellenőrzések törlésére szolgál request-id alapján, vagy használható az összes jelenlegi kérés megszakítására.

#### Parancspélda

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentumok
  
- **REQUEST_ID**: A `inspect-async` parancs által visszaadott request-id 
  
#### Példa
  
Az 12345 request-id-vel rendelkező ellenőrzés megszakítása:
  
```bash
dignacli inspect-cancel 12345
```

Minden jelenleg futó vagy váró kérés megszakítása:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Az `export-ds` parancs a ***digna*** CLI-ben adatforrások exportálására szolgál a ***digna*** repository-ból. Alapértelmezés szerint egy adott projekt összes adatforrása exportálásra kerül.

#### Parancspélda
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelyből az adatforrások exportálásra kerülnek.

#### Opciók

- `--table_name`, `-tn`: Egy adott adatforrás exportálása egy projektről.
- `--exportfile`, `-ef`: Export fájl nevének megadása.
    
#### Példa
  
Az összes adatforrás exportálása a `ProjectA` projektből:
  
```bash
dignacli export-ds ProjectA
```
  
Ez a parancs exportálja a `ProjectA` összes adatforrását egy JSON dokumentumként, amely importálható egy másik projektbe vagy ***digna*** repository-ba.

### import-ds

Az `import-ds` parancs a ***digna*** CLI-ben adatforrások importálására szolgál egy célprojektbe, és létrehoz egy importáltalányt (import declaration).

#### Parancspélda
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt, ahová az adatforrások importálásra kerülnek.
- **EXPORT_FILE**: Az export fájl neve, amelyből az adatforrások importálásra kerülnek.

#### Opciók

- `--output-file`, `-o`: Fájl az importraport mentéséhez (ha nincs megadva, a jelentés táblázatos formában jelenik meg a terminálban).
- `--output-format`, `-f`: Az importraport formátuma (json, csv).
    
#### Példa
  
Az `my_export.json` exportfájl összes adatforrásának importálása a `ProjectB` projektbe:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Az import után a parancs jelentést is megjelenít az importált és kihagyott objektumokról. Csak az új adatforrások kerülnek importálásra `ProjectB`-be. Azoknak az objektumoknak a megtekintéséhez, amelyek importálva vagy kihagyva lettek volna, használhatja a `plan-import-ds` parancsot.

### plan-import-ds

A `plan-import-ds` parancs a ***digna*** CLI-ben egy exportfájl előzetes elemzésére szolgál a tényleges importálás előtt, és létrehoz egy importtervet/riportot.

#### Parancspélda
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelybe az adatforrások esetleg importálásra kerülnének.
- **EXPORT_FILE**: Az export fájl neve, amelyet az import előtt elemezni kell.

#### Opciók

- `--output-file`, `-o`: Fájl az importraport mentéséhez (ha nincs megadva, a jelentés táblázatos formában jelenik meg a terminálban).
- `--output-format`, `-f`: Az importraport formátuma (json, csv).
    
#### Példa
  
Annak ellenőrzése, hogy az `my_export.json` exportfájlból mely adatforrások kerülnének importálásra és melyek kerülnének kihagyásra, ha azt a `ProjectB`-be importálnánk:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ez a parancs csak egy importtervet jelenít meg azokról az objektumokról, amelyek importálásra vagy kihagyásra kerülnének.
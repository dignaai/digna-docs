# digna CLI Reference 2026.04
**2026-04-08**

Ez az oldal dokumentálja a ***digna*** CLI **2026.04** kiadásában elérhető parancsok teljes készletét, beleértve használati példákat és opciókat.

---

## CLI alapok

---

### help
A `--help` opció információt nyújt az elérhető parancsokról és azok használatáról. Két fő módja van ennek az opciónak a használatára:

1. **Általános súgó megjelenítése:**
   
    Használja a `--help` opciót közvetlenül a `dignacli` parancs után  
   ```bash
   dignacli --help
   ```

2. **Súgó egy adott parancshoz:**  
  
    Részletes információkért egy adott parancsról, kapcsolja a `--help` opciót az adott parancs végére.
    Például, ha az `add-user` parancs súgóját szeretné megtekinteni, futtassa:
     ```bash
     dignacli add-user --help
     ```

     ### kimenet:
      
     - **Parancs leírása:** Részletes leírást ad arról, mit csinál a parancs.  
     - **Szintaxis:** Megmutatja a pontos szintaxist, beleértve a kötelező és opcionális argumentumokat.  
     - **Opciók:** Felsorolja a parancshoz tartozó opciókat és azok magyarázatát.  
     - **Példák:** Példákat ad arra, hogyan kell hatékonyan végrehajtani a parancsot.

### check-config

A `check-config` parancs a ***digna*** CLI eszközön belül egy segédprogram, amely a ***digna*** konfigurációját teszteli. Ez a parancs ellenőrzi, hogy a ***digna*** komponensei megtalálják-e a szükséges konfigurációs elemeket a config.toml fájlban.

#### Opciók

- `--configpath`, `-cp`: A konfigurációt tartalmazó fájl vagy könyvtár. Ha nincs megadva, a ../config.toml lesz használva.
      
#### Parancs használata
```bash
dignacli check-config
```

Sikeres végrehajtás esetén a parancs megerősítést ad a konfiguráció teljességéről.  
  
Ha a konfiguráció hiányosnak tűnik, a hiányzó konfigurációs elemek listázásra kerülnek.

  
### check-repo-connection

A `check-repo-connection` parancs a ***digna*** CLI eszközén belül egy segédprogram, amely a megadott ***digna*** repository elérhetőségét és hozzáférését teszteli. Ez a parancs biztosítja, hogy a CLI képes legyen kommunikálni a repository-val.
      
#### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres végrehajtás esetén a parancs megerősítést ad a kapcsolatról, valamint részleteket a repository-ról: Repository verzió, Host, Adatbázis és Sémák.  
  
Ha a repository kapcsolat nem sikeres, ellenőrizze a config.toml fájlt a helyes konfigurációs beállításokért.


### version

A telepített *dignacli* verziójának ellenőrzéséhez használja a `--version` opciót.  
  
#### Parancs használata
```bash
dignacli --version
```
  
#### Példa kimenet
```bash
dignacli version 2026.04
```

### naplózási opciók
  
Alapértelmezésben a ***digna*** parancsok konzol-kimenete minimalista. A legtöbb parancs lehetőséget ad további információk megjelenítésére a következő opciókkal:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A „verbose” és a „debug” a részletességi szintet határozza meg, míg a „logfile” kapcsoló lehetővé teszi a kimenet fájlba történő átirányítását a konzol helyett.

## Felhasználókezelés

### add-user
  
Az `add-user` parancs a ***digna*** CLI-ben új felhasználó hozzáadására szolgál a ***digna*** rendszerhez.
  
#### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- `--is_superuser`, `-su`: Jelző, amellyel az új felhasználót adminisztrátori jogosultságokkal (superuser) látja el.
- `--valid_until`, `-vu`: Lejárati dátumot állít be a felhasználói fiókra a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fióknak nincs lejárati ideje.

#### Példa

Új felhasználó hozzáadásához `jdoe` felhasználónévvel, teljes névvel `John Doe` és jelszóval `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Új felhasználó hozzáadása lejárati dátummal:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
A `delete-user` parancs a ***digna*** CLI-ben meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből.
  
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
  
A parancs végrehajtásával a `jdoe` felhasználó eltávolításra kerül a ***digna*** rendszerből, visszavonva hozzáférését és törölve a kapcsolódó adatokat és jogosultságokat a repository-ból.

### modify-user

A `modify-user` parancs a ***digna*** CLI-ben meglévő felhasználó adatainak frissítésére szolgál a ***digna*** rendszerben.

#### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Opciók  
  
- `--is_superuser`, `-su`: Superuser jogosultságot ad a felhasználónak, amely megnövelt jogosultságokat biztosít. Ez a kapcsoló nem igényel értéket.  
- `--valid_until`, `-vu`: Lejárati dátumot állít be a felhasználói fiókra `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
#### Példa
  
A `jdoe` felhasználó teljes nevének módosítása „Johnathan Doe”-ra és superuser beállítása:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben meglévő felhasználó jelszavának megváltoztatására szolgál.
  
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

A `list-users` parancs a ***digna*** CLI-ben megjeleníti az összes regisztrált felhasználót a ***digna*** rendszerben.

#### Parancs használata

```bash
dignacli list-users
```

A parancs végrehajtásakor a ***digna*** CLI csatlakozik a ***digna*** repository-hoz és felsorolja az összes felhasználót, megjelenítve azok ID-ját, felhasználónevét, teljes nevét, superuser státuszát és lejárati időbélyegeit.

## Repository kezelés

### upgrade-repo
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ez a parancs elengedhetetlen a frissítések alkalmazásához vagy a repository infrastruktúra első beállításához.
  
#### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
#### Opciók
  
- `--simulation-mode`, `-s`: Engedélyezés esetén a parancs szimulációs módban fut, és kiírja azokat az SQL utasításokat, amelyeket végrehajtaná, de ténylegesen nem futtatja azokat. Hasznos a változások előnézetéhez anélkül, hogy módosításokat hajtana végre a repository-n.  

  
#### Példa
  
A ***digna*** repository frissítéséhez a parancs futtatható opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
A frissítés szimulációs módban történő futtatásához (az SQL utasítások megtekintéséhez anélkül, hogy alkalmaznánk őket):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kulcsfontosságú a ***digna*** rendszer karbantartásához, biztosítva, hogy az adatbázis séma és a repository egyéb összetevői naprakészek legyenek a szoftver legfrissebb verziójával.

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
Például a `mypassword123` jelszó titkosításához használja:
```bash
dignacli encrypt mypassword123
```
A parancs a megadott jelszó titkosított változatát adja vissza, amely aztán biztonságos környezetben használható. Ha a jelszó argumentum nincs megadva, a CLI hibát jelez a hiányzó argumentum miatt.

### generate-key
  
A `generate-key` parancs egy Fernet kulcs generálására szolgál, amely elengedhetetlen a ***digna*** repository-ban tárolt jelszavak védelméhez.
  
#### Parancs használata
```bash
dignacli generate-key
```
  
## Adatkezelés

### clean-up

A `clean-up` parancs a ***digna*** CLI-ben profilok, predikciók és a forgalmi lámpa rendszer adatok törlésére szolgál egy vagy több adattforrás esetén egy adott projektben. Ez a parancs fontos az adatok élettartamának kezeléséhez, segít rendezett és hatékony adatkörnyezet fenntartásában az elavult vagy szükségtelen adatok törlésével.

#### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, ahonnan az adatokat törölni kell (kötelező). Ha az `all-projects` kulcsszót használja ebben az argumentumban, a ***digna*** végigiterál az összes létező projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az adateltávolítás kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adateltávolítás záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- `--table-name`, `-tn`: Korlátozza a törlést egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűrő, amely csak azokat a táblákat érinti, amelyek nevében megtalálható a megadott részstring.
- `--timing`, `-tm`: A clean-up folyamat időtartamát jeleníti meg a befejezés után.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
#### Példa
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Adatok eltávolítása csak egy `Table1` nevű táblából:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében és biztosítja, hogy a repository csak a releváns információkat tartalmazza.

### remove-orphans
  
A `remove-orphans` parancs a ***digna*** CLI-ben karbantartási feladatokat végez a ***digna*** repository-ban.  
Amikor egy felhasználó projekteket vagy adattforrásokat töröl, a profilok és predikciók gyakran a repository-ban maradnak. Ezzel a paranccsal az ilyen árva (orphan) sorok eltávolíthatók a repository-ból.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

### list-projects
  
A `list-projects` parancs a ***digna*** CLI-ben az összes elérhető projekt felsorolására szolgál a ***digna*** rendszerben.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára, gyors áttekintést adva a ***digna*** repository-ban található projektekről.

### list-ds

A `list-ds` parancs a ***digna*** CLI-ben az adott projekthez tartozó összes elérhető adattforrást listázza. Ez a parancs hasznos annak felmérésére, milyen adathalmazok állnak rendelkezésre elemzésre és kezelésre a ***digna*** rendszerben.

#### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentumok
- **PROJECT_NAME**: A projekt neve, amelyhez a adattforrások listázása történik (kötelező).
  
#### Példa
  
Az `ProjectA` projekt összes adattforrásának listázásához:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést nyújt a projektben elérhető adattforrásokról, segítve a felhasználókat az adatkörnyezet hatékonyabb kezelésében.


### inspect

Az `inspect` parancs a ***digna*** CLI-ben profilok, predikciók és a forgalmi lámpa rendszer adatainak létrehozására szolgál egy vagy több adattforráshoz egy adott projekten belül. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakon belül. Az ellenőrzés befejezése után a kiszámított forgalmi lámpa rendszer értéke visszaadásra kerül:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyet ellenőrizni kíván (kötelező). Ha az `all-projects` kulcsszót használja ebben az argumentumban, a ***digna*** végigiterál az összes létező projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Korlátozza az ellenőrzést egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűrő, amely csak azokat a táblákat ellenőrzi, amelyek nevében megtalálható a megadott részstring.
- `--enable_notification`, `-en`: Értesítések küldésének engedélyezése riasztások esetén.
- `--bypass-backend`, `-bb`: Megkerüli a backend-et, és közvetlenül a CLI-ből futtatja az ellenőrzést (csak tesztelési célokra!).

  
#### Példa
  
Adatok ellenőrzése a `ProjectA` projektben 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy adott tábla ellenőrzése és a predikciók újraszámításának kikényszerítése:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos friss profilok és predikciók generálásához, az adatintegritás monitorozásához és a riasztási rendszerek kezeléséhez egy adott projekt időszakára vonatkozóan.

### inspect-async

Az `inspect-async` parancs a ***digna*** CLI-ben profilok, predikciók és a forgalmi lámpa rendszer adatainak létrehozására szolgál egy vagy több adattforráshoz egy adott projekten belül. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakon belül. A `inspect-async` parancs esetén a parancs nem várja meg az ellenőrzés befejezését; ehelyett visszaadja a beküldött ellenőrzési kérés azonosítóját (request id). Az ellenőrzés előrehaladásának lekérdezéséhez használja az `inspect-status` parancsot.

#### Parancs használata

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyet ellenőrizni kíván (kötelező). Ha az `all-projects` kulcsszót használja ebben az argumentumban, a ***digna*** végigiterál az összes létező projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Korlátozza az ellenőrzést egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűrő, amely csak azokat a táblákat ellenőrzi, amelyek nevében megtalálható a megadott részstring.
- `--enable_notification`, `-en`: Értesítések küldésének engedélyezése riasztások esetén.

  
#### Példa
  
Adatok ellenőrzése a `ProjectA` projektben 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Az `inspect-status` parancs a ***digna*** CLI-ben egy aszinkron ellenőrzés előrehaladásának lekérdezésére szolgál a request ID alapján.

#### Parancs használata

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentumok
  
- **REQUEST_ID**: Az `inspect-async` parancs által visszaadott kérésazonosító.
  
#### Példa
  
Egy 12345 azonosítójú ellenőrzés előrehaladásának lekérdezéséhez:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Az `inspect-cancel` parancs a ***digna*** CLI-ben ellenőrzések törlésére szolgál request ID alapján, vagy használható az összes aktuális kérés törlésére.

#### Parancs használata

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentumok
  
- **REQUEST_ID**: Az `inspect-async` parancs által visszaadott kérésazonosító.
  
#### Példa
  
Egy 12345 azonosítójú ellenőrzés törléséhez:
  
```bash
dignacli inspect-cancel 12345
```

Az összes jelenleg futó vagy függőben lévő kérés törléséhez:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Az `export-ds` parancs a ***digna*** CLI-ben adattforrások exportálására szolgál a ***digna*** repository-ból. Alapértelmezés szerint egy adott projekt minden adattforrása exportálásra kerül.

#### Parancs használata
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentumok
- **PROJECT_NAME**: A projekt neve, ahonnan az adattforrások exportálása történik.

#### Opciók

- `--table_name`, `-tn`: Egy adott adattforrás exportálása a projektből.
- `--exportfile`, `-ef`: Az export fájl nevének megadása.
    
#### Példa
  
Az `ProjectA` projekt összes adattforrásának exportálásához:
  
```bash
dignacli export-ds ProjectA
```
  
Ez a parancs az `ProjectA` összes adattforrását JSON dokumentumként exportálja, amely importálható egy másik projektbe vagy ***digna*** repository-ba.


### import-ds

Az `import-ds` parancs a ***digna*** CLI-ben adattforrások importálására szolgál egy célprojektbe, és import jelentést készít.

#### Parancs használata
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: A projekt neve, ahová az adattforrások importálása történik.
- **EXPORT_FILE**: Az importálandó adattforrás export fájl neve.

#### Opciók

- `--output-file`, `-o`: Fájl az import jelentés mentéséhez (ha nincs megadva, táblázatos formában a terminálra írja).
- `--output-format`, `-f`: Az import jelentés mentésének formátuma (json, csv).
    
#### Példa
  
Az `my_export.json` export fájlban található összes adattforrás importálása a `ProjectB`-be:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Az import után a parancs jelentést is megjelenít az importált és kihagyott objektumokról. Csak az újszerű adattforrások lesznek importálva a `ProjectB`-be. Annak megállapításához, hogy mely objektumok kerülnének importálásra vagy kihagyásra, használhatja a `plan-import-ds` parancsot.

### plan-import-ds

A `plan-import-ds` parancs a ***digna*** CLI-ben azt vizsgálja meg, hogy egy export fájl importálása esetén mely adattforrások kerülnének importálásra és melyek lennének kihagyva, és import jelentést készít előzetesen.

#### Parancs használata
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: A projekt neve, ahová az adattforrások importálása történne.
- **EXPORT_FILE**: Az importálás előtt elemezendő export fájl neve.

#### Opciók

- `--output-file`, `-o`: Fájl az import jelentés mentéséhez (ha nincs megadva, táblázatos formában a terminálra írja).
- `--output-format`, `-f`: Az import jelentés mentésének formátuma (json, csv).
    
#### Példa
  
Annak ellenőrzéséhez, hogy az `my_export.json` export fájlból mely adattforrások kerülnének importálásra és melyek lennének kihagyva a `ProjectB`-be történő importálás esetén:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ez a parancs csak egy importtervet jelenít meg az importálandó és kihagyandó objektumokról.
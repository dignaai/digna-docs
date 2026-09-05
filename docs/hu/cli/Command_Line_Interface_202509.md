---
title: digna CLI Referencia 2025.09 – Parancsok & Példák | digna dokumentáció
description: Teljes referencia a digna CLI 2025.109 kiadásához. Ismerje meg, hogyan kezelhet felhasználókat, repository-kat és adatokat olyan parancsokkal, mint add-user, check-config, check-repo-connection, inspect, inspect-async és továbbiak.
image: /assets/logo_square.png
---

# digna CLI Referencia 2025.09
**2025-09-29**

Ez az oldal dokumentálja a ***digna*** CLI **2025.09** kiadásában elérhető parancsok teljes készletét, beleértve a használati példákat és opciókat.

---

## CLI alapok

---

### help
A `--help` opció információt ad az elérhető parancsokról és azok használatáról. Két fő módja van ennek az opció használatának:

1. **Általános súgó megjelenítése:**
   
    Használja a --help-et közvetlenül a ***digna*** kulcsszó után:  
   ```bash
   dignacli --help
   ```

2. **Külön parancs súgójának lekérése:**  
  
    Egy adott parancs részletes információiért fűzze hozzá a `--help`-et az adott parancshoz.  
    Például, ha az `add-user` parancs súgóját szeretné, futtassa:
     ```bash
     dignacli add-user --help
     ```

     ### kimenet:
      
     - **Parancs leírása:** Részletesen ismerteti, mit végez a parancs.  
     - **Szintaxis:** Megjeleníti a pontos szintaxist, beleértve a kötelező és választható argumentumokat.  
     - **Opciók:** Felsorolja a parancshoz tartozó opciókat és azok magyarázatát.  
     - **Példák:** Példákat ad a parancs hatékony végrehajtására.

### check-config

A check-config parancs a ***digna*** CLI eszközön belül arra szolgál, hogy tesztelje a ***digna*** konfigurációját. Ez a parancs biztosítja, hogy a ***digna*** komponensek megtalálják a szükséges konfigurációs elemeket a config.toml fájlban.

#### Opciók

- `--configpath`, `-cp`: A konfigurációt tartalmazó fájl vagy könyvtár. Ha elhagyják, a ../config.toml kerül használatra.
      
#### Parancs használata
```bash
dignacli check-config
```

Sikeres végrehajtás esetén a parancs megerősítést ad a konfiguráció teljességéről.  
  
Ha a konfiguráció hiányosnak tűnik, a hiányzó konfigurációs elemek listázásra kerülnek.

  
### check-repo-connection

A check-repo-connection parancs a ***digna*** CLI eszközben a megadott ***digna*** repository elérhetőségének és hozzáférésének tesztelésére szolgál. Ez a parancs biztosítja, hogy a CLI képes együttműködni a repository-val.
      
#### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres végrehajtás esetén a parancs megerősíti a kapcsolatot, és részleteket ad a repository-ról: Repository verzió, Host, Adatbázis és Sémája.  
  
Ha a repository kapcsolata nem sikeres, ellenőrizze a config.toml fájlt a helyes konfigurációs beállításokért.


### version

Az *dignacli* telepített verziójának ellenőrzéséhez használja a --version opciót.  
  
#### Parancs használata
```bash
dignacli --version
```
  
#### Példa kimenet
```bash
dignacli version 2025.09
```

### naplózási opciók
  
Alapértelmezés szerint a ***digna*** parancsok konzol kimenete minimalista. A legtöbb parancs lehetőséget ad további információk megjelenítésére a következő opciók használatával:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A “verbose” és “debug” az információ részletességi szintjét határozzák meg, míg a “logfile” kapcsoló lehetővé teszi a kimenet fájlba történő átirányítását a konzol helyett.

## Felhasználókezelés

### add-user
  
Az add-user parancs a ***digna*** CLI-ben új felhasználó létrehozására szolgál a ***digna*** rendszerben.
  
#### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- `--is_superuser`, `-su`: Jelző, amellyel az új felhasználó adminisztrátorrá tehető.
- `--valid_until`, `-vu`: Beállítja a felhasználói fiók lejárati dátumát a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fióknak nincs lejárati ideje.

#### Példa

Új felhasználó hozzáadása `jdoe` felhasználónévvel, `John Doe` teljes névvel és `password123` jelszóval:

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
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen kötelező argumentuma a parancsnak.

#### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs végrehajtása eltávolítja a `jdoe` felhasználót a ***digna*** rendszerből, visszavonva hozzáférését és törölve a hozzá kapcsolódó adatokat és jogosultságokat a repository-ból.

### modify-user

A `modify-user` parancs a ***digna*** CLI-ben egy meglévő felhasználó adatait frissíti a ***digna*** rendszerben.

#### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Opciók  
  
- `--is_superuser`, `-su`: Szuperfelhasználóvá teszi a felhasználót, magasabb jogosultságokkal. Ez a kapcsoló nem igényel értéket.  
- `--valid_until`, `-vu`: Beállítja a felhasználói fiók lejárati dátumát a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
#### Példa
  
A `jdoe` felhasználó teljes nevének módosítása „Johnathan Doe”-ra és szuperfelhasználóvá tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben egy meglévő felhasználó jelszavának módosítására szolgál a ***digna*** rendszerben.
  
#### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumentumok
  
- **USER_NAME**: Annak a felhasználónak a felhasználóneve, akinek a jelszava módosítandó (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
#### Példa
  
A `jdoe` felhasználó jelszavának megváltoztatása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

A `list-users` parancs a ***digna*** CLI-ben kilistázza az összes, a ***digna*** rendszerben regisztrált felhasználót.

#### Parancs használata

```bash
dignacli list-users
```

A parancs végrehajtása a ***digna*** CLI-ben csatlakozik a ***digna*** repository-hoz és kilistázza az összes felhasználót, megjelenítve azok azonosítóját, felhasználónevét, teljes nevét, szuperfelhasználói státuszát és lejárati időbélyegeit.

## Repository kezelése

### upgrade-repo
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ez a parancs elengedhetetlen a frissítések alkalmazásához vagy a repository infrastruktúra első beállításához.
  
#### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
#### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut, amely kiírja a végrehajtandó SQL utasításokat, de nem hajtja végre azokat. Hasznos a változtatások előnézetéhez anélkül, hogy módosítások történnének a repository-ban.  

  
#### Példa
  
A ***digna*** repository frissítéséhez futtathatja a parancsot opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
A frissítés szimulációs módban történő futtatásához (csak az SQL utasítások megtekintéséhez):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kulcsfontosságú a ***digna*** rendszer karbantartásához, biztosítva, hogy az adatbázis sémája és a repository egyéb összetevői naprakészek legyenek a szoftver legújabb verziójával.

### encrypt
  
Az `encrypt` parancs a ***digna*** CLI-ben jelszó titkosítására szolgál.
  
#### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
#### Példa
  
Jelszó titkosításához adja meg a jelszót argumentumként.  
Például a `mypassword123` jelszó titkosításához:
```bash
dignacli encrypt mypassword123
```
A parancs a megadott jelszó titkosított változatát adja vissza, amelyet biztonságos kontextusokban lehet használni. Ha a jelszó argumentum hiányzik, a CLI hibát jelez a hiányzó argumentum miatt.

### generate-key
  
A `generate-key` parancs egy Fernet kulcs generálására szolgál, amely létfontosságú a ***digna*** repository-ban tárolt jelszavak védelméhez.
  
#### Parancs használata
```bash
dignacli generate-key
```
  
## Adatkezelés

### clean-up

A `clean-up` parancs a ***digna*** CLI-ben profilok, előrejelzések és a forgalmi lámpa-rendszer adatok eltávolítására szolgál egy vagy több adatforrásról egy megadott projektben. Ez a parancs fontos az adatok életciklus-kezeléséhez, segítve a rendezet és hatékony adattár kialakítását az elavult vagy szükségtelen adatok törlésével.

#### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, ahonnan az adatokat törölni kell (kötelező). Az all-projects kulcsszó használata esetén a ***digna*** minden létező projekten végigiterál és alkalmazza a parancsot.
- **FROM_DATE**: Az adatok eltávolításának kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adatok eltávolításának befejező dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- `--table-name`, `-tn`: A clean-up műveletet korlátozza egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűrő, amely csak azokat a táblákat érinti, amelyek nevében a megadott részstring megtalálható.
- `--timing`, `-tm`: A clean-up befejezése után megjeleníti a művelet időtartamát.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
#### Példa
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Adatok eltávolítása csak egy konkrét, `Table1` nevű táblából:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében és biztosítja, hogy a repository csak releváns információkat tartalmazzon.

### remove-orphans
  
A `remove-orphans` parancs a ***digna*** CLI-ben a repository karbantartására szolgál.  
Ha egy felhasználó projekteket vagy adatforrásokat töröl, a profilok és előrejelzések gyakran a repository-ban maradnak. Ezzel a parancssal az ilyen árva (orphan) sorok eltávolításra kerülnek a repository-ból.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

### list-projects
  
A `list-projects` parancs a ***digna*** CLI-ben az összes elérhető projekt listázására szolgál a ***digna*** rendszerben.
  
#### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára, gyors áttekintést adva a ***digna*** repository elérhető projektjeiről.

### list-ds

A `list-ds` parancs a ***digna*** CLI-ben az adott projekt összes elérhető adatforrásának listázására szolgál. Ez a parancs hasznos az elemzésre és kezelésre rendelkezésre álló adatvagyon megismeréséhez a ***digna*** rendszerben.

#### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt, amelyhez tartozó adatforrások listázása történik (kötelező).
  
#### Példa
  
Az összes adatforrás kilistázása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést nyújt a projektben rendelkezésre álló adatforrásokról, segítve a felhasználókat az adatok kezelésében.

### inspect

Az `inspect` parancs a ***digna*** CLI-ben profilok, előrejelzések és a forgalmi lámpa-rendszer adatok létrehozására szolgál egy vagy több adatforráshoz egy megadott projektben. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakon belül. Az ellenőrzés befejezése után a számított forgalmi lámpa-rendszer értéke kerül visszaadásra:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelynek adatait ellenőrizni kell (kötelező). Az all-projects kulcsszó használata esetén a ***digna*** minden meglévő projekten végrehajtja a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés befejező dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Az ellenőrzést korlátozza egy adott táblára a projektben.
- `--table-filter`, `-tf`: Csak azokat a táblákat vizsgálja, amelyek nevében megtalálható a megadott részstring.
- `--enable_notification`, `-en`: Értesítések küldését engedélyezi riasztás esetén.
- `--bypass-backend`, `-bb`: Kikerüli a backend-et és közvetlenül a CLI-ből futtatja az ellenőrzést (csak tesztelési célokra!).

  
#### Példa
  
Adatok ellenőrzése a `ProjectA` projektben 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Egy konkrét tábla ellenőrzése és a jóslatok újraszámításának kikényszerítése:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos a frissített profilok és előrejelzések generálásához, az adatintegritás monitorozásához és a riasztási rendszerek kezeléséhez egy adott projekt időszakán belül.

### inspect-async

Az `inspect-async` parancs a ***digna*** CLI-ben profilok, előrejelzések és a forgalmi lámpa-rendszer adatok létrehozására szolgál egy vagy több adatforráshoz egy megadott projektben. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakon belül. A `inspect-async` parancshoz képest ez a parancs nem várja meg az ellenőrzés befejezését. Ehelyett visszaadja a benyújtott ellenőrzési kérés azonosítóját. Az ellenőrzés folyamatának lekérdezéséhez használja az `inspect-status` parancsot.

#### Parancs használata

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelynek adatait ellenőrizni kell (kötelező). Az all-projects kulcsszó használata esetén a ***digna*** minden meglévő projekten végrehajtja a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés befejező dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók

- `--table-name`, `-tn`: Az ellenőrzést korlátozza egy adott táblára a projektben.
- `--table-filter`, `-tf`: Csak azokat a táblákat vizsgálja, amelyek nevében megtalálható a megadott részstring.
- `--enable_notification`, `-en`: Értesítések küldését engedélyezi riasztás esetén.

  
#### Példa
  
Adatok aszinkron ellenőrzése a `ProjectA` projektben 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Az `inspect-status` parancs a ***digna*** CLI-ben egy aszinkron ellenőrzés előrehaladásának ellenőrzésére szolgál a kérés azonosítója alapján.

#### Parancs használata

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentumok
  
- **REQUEST_ID**: A `inspect-async` parancs által visszaadott kérés azonosítója 
  
#### Példa
  
Egy 12345 azonosítójú ellenőrzés előrehaladásának lekérdezése:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Az `inspect-cancel` parancs a ***digna*** CLI-ben egy ellenőrzés leállítására szolgál a kérés azonosítója alapján, vagy használható az összes aktuális kérés leállítására is.

#### Parancs használata

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentumok
  
- **REQUEST_ID**: A `inspect-async` parancs által visszaadott kérés azonosítója 
  
#### Példa
  
Egy 12345 azonosítójú ellenőrzés leállítása:
  
```bash
dignacli inspect-cancel 12345
```

Az összes jelenleg futó vagy függőben lévő kérés leállítása:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Az `export-ds` parancs a ***digna*** CLI-ben az adatforrások exportálására szolgál a ***digna*** repository-ból. Alapértelmezés szerint egy adott projekt összes adatforrása exportálásra kerül.

#### Parancs használata
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, ahonnan az adatforrások exportálódnak.

#### Opciók

- `--table_name`, `-tn`: Egy adott adatforrás exportálása a projektből.
- `--exportfile`, `-ef`: Megadja az export fájl nevét.
    
#### Példa
  
Az összes adatforrás exportálása a `ProjectA` nevű projektből:
  
```bash
dignacli export-ds ProjectA
```
  
Ez a parancs a `ProjectA` összes adatforrását egy JSON dokumentumba exportálja, amely importálható egy másik projektbe vagy ***digna*** repository-ba.


### import-ds

Az `import-ds` parancs a ***digna*** CLI-ben adatforrások importálására szolgál egy célnprojektbe, és import riportot készít.

#### Parancs használata
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt, ahová az adatforrások importálásra kerülnek.
- **EXPORT_FILE**: Az importálandó adatforrás export fájljának neve.

#### Opciók

- `--output-file`, `-o`: A mentendő import riport fájlja (ha nincs megadva, táblázatos formában a terminálra írja).
- `--output-format`, `-f`: A riport mentésének formátuma (json, csv).
    
#### Példa
  
Az `my_export.json` export fájl összes adatforrásának importálása a `ProjectB` projektbe:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Az import után a parancs jelentést is megjelenít az importált és kihagyott objektumokról. Csak az új adatforrások kerülnek importálásra a `ProjectB`-be. Annak megállapításához, hogy mely objektumok kerülnének importálásra vagy kihagyásra, használhatja a `plan-import-ds` parancsot.

### plan-import-ds

A `plan-import-ds` parancs a ***digna*** CLI-ben az import előzetes elemzésére szolgál: megmutatja, mely adatforrások kerülnének importálásra és melyek lennének kihagyva.

#### Parancs használata
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentumok
- **PROJECT_NAME**: Az a projekt, ahová az adatforrások importálása történne.
- **EXPORT_FILE**: A vizsgálandó export fájl neve az import előtt.

#### Opciók

- `--output-file`, `-o`: A mentendő import terv fájlja (ha nincs megadva, táblázatos formában a terminálra írja).
- `--output-format`, `-f`: A mentés formátuma (json, csv).
    
#### Példa
  
Annak ellenőrzése, hogy az `my_export.json` export fájlból mely adatforrások kerülnének importálásra és melyek lennének kihagyva, ha azokat a `ProjectB`-be importálnánk:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ez a parancs csak az import tervezetét mutatja meg az importálandó és kihagyandó objektumokról.
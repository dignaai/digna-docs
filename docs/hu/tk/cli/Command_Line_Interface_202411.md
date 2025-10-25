---
title: digna CLI Referencia 2024.11 – Parancsok & Példák | digna Dokumentáció
description: teljes digna CLI referencia a 2024.11-es verzióhoz. Ismerje meg, hogyan kezelheti a felhasználókat, repository-kat és adatokat az olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect, tls-status.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Ez az oldal dokumentálja a ***digna*** CLI **2024.11** verziójában elérhető összes parancsot, használati példát és opciót.


---
## CLI alapok

---

## `help` opció használata

A `--help` opció információt ad az elérhető parancsokról és azok használatáról. Ennek az opciónak két fő használati módja van:

1. **Általános segítség megjelenítése:**
   
   Használja a `--help` opciót közvetlenül a ***digna*** parancs után.  
   ```bash
   dignacli --help
   ```

3.  **Segítség egy adott parancshoz:**  
  
    Egy adott parancs részletes leírásáért adja hozzá a `--help` opciót az adott parancshoz.  
    Például az `add-user` parancsról szóló segítség megtekintéséhez futtassa:
     ```bash
     dignacli add-user --help
     ```

     ### kimenet:
      
     - **Parancs leírása:** Részletesen ismerteti, mit csinál a parancs.  
     - **Szin­taxis:** A kötelező és opcionális argumentumokkal együtt mutatja a teljes szintaxist.  
     - **Opciók:** Felsorolja a parancshoz tartozó opciókat és azok leírását.  
     - **Példák:** Mutat példákat arra, hogyan kell hatékonyan futtatni a parancsot.

  
## `check-repo-connection` parancs használata

A check-repo-connection parancs a ***digna*** CLI-ben egy adott ***digna*** repository-hoz való csatlakozást és hozzáférést teszteli. Ez a parancs megerősíti, hogy a CLI képes kommunikálni a repository-val.
      
### Használat
```bash
dignacli check-repo-connection
```

Sikeres futtatás esetén a parancs megerősíti a kapcsolatot és a repository-ról a következő részleteket adja meg: Repository version, Host, Database és Schema.  
  
Ha a repository-hoz való csatlakozás sikertelen, ellenőrizze a config.toml fájl megfelelő beállításait.

## `version` parancs használata

A telepített *dignacli* verzió ellenőrzéséhez használja a `--version` opciót.  
  
### Használat
```bash
dignacli --version
```
  
### Példa kimenet
```bash
dignacli version 2024.11
```

## Naplózási opciók használata
  
Alapértelmezés szerint a ***digna*** parancsok konzolra kiírt üzenetei minimálisak. A legtöbb parancs további információk megadására képes az alábbi opciók használatával:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A „verbose” és „debug” a részletességi szintet határozza meg, míg a „logfile” opció lehetővé teszi a kimenet fájlba irányítását a konzol helyett.

# Felhasználókezelés

## `add-user` parancs használata
  
Az add-user parancs új felhasználó hozzáadására szolgál a ***digna*** rendszerbe a ***digna*** CLI-n keresztül.
  
### Használat
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

### Opciók

- `--is_superuser`, `-su`: Jelző az új felhasználó rendszergazdává jelöléséhez.
- `--valid_until`, `-vu`: A felhasználói fiók lejárati idejét állítja be `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fiók lejárat nélküli lesz.

### Példa

Új felhasználó létrehozása, felhasználónév `jdoe`, teljes név `John Doe`, jelszó `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Új felhasználó hozzáadása lejárati dátummal:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` parancs használata
  
A `delete-user` parancs meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből a CLI-n keresztül.
  
### Használat
```bash
dignacli delete-user USER_NAME
```
  
### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen szükséges argumentum.

### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs futtatásakor a `jdoe` felhasználó eltávolításra kerül a ***digna*** rendszerből; a hozzáférése megszűnik, valamint a repository-val kapcsolatos adatai és jogosultságai törlődnek.

## `modify-user` parancs használata

A `modify-user` parancs meglévő felhasználó adatainak frissítésére szolgál a ***digna*** CLI-ben.

### Használat
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
### Opciók  
  
- `--is_superuser`, `-su`: A felhasználót rendszergazdai jogosultságokkal rendelkező szuperfelhasználóvá alakítja. Ennek a jelzőnek nincs értéke.  
- `--valid_until`, `-vu`: A felhasználói fiók lejárati idejét állítja be `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fiók lejárat nélküli marad.  
  
### Példa
  
A `jdoe` felhasználó teljes nevének `Johnathan Doe`-ra módosítása és szuperfelhasználóvá tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs meglévő felhasználó jelszavának megváltoztatására szolgál a ***digna*** CLI-ben.
  
### Használat
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentumok
  
- **USER_NAME**: A jelszót módosítandó felhasználó felhasználóneve (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
### Példa
  
A `jdoe` felhasználó jelszavának `newpassword123`-ra módosítása:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` parancs használata

A `list-users` parancs kilistázza a ***digna*** rendszerben regisztrált összes felhasználót a ***digna*** CLI-n keresztül.

### Használat

```bash
dignacli list-users
```

A parancs kapcsolódik a ***digna*** repository-hoz és megjeleníti az összes felhasználót azonosító, felhasználónév, teljes név, szuperfelhasználói státusz és lejárati időbélyegek szerint.

# Tárolókezelés

### `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a ***digna*** repository frissítésére vagy inicializálására szolgál a ***digna*** CLI-ben. Ezt a parancsot a frissítések alkalmazásához vagy a repository első beállításához kell használni.
  
### Használat

```bash
dignacli upgrade-repo [options]
```
  
### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut; kiírja a végrehajtandó SQL utasításokat, de nem futtatja azokat. Ez hasznos a változtatások alkalmazása előtti előnézethez.  

  
### Példa
  
A ***digna*** repository frissítése opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
A frissítés szimulációs módban történő futtatása (SQL utasítások megtekintése anélkül, hogy végrehajtaná őket):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kritikus fontosságú a ***digna*** rendszer karbantartásában, mivel gondoskodik arról, hogy az adatbázis sémája és egyéb repository összetevők megfeleljenek a szoftver legújabb verziójának.

## `encrypt` parancs használata
  
Az `encrypt` parancs jelszó titkosítására szolgál a ***digna*** CLI-ben.
  
### Használat
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
### Példa
  
A jelszó titkosításához adja meg azt argumentumként.  
Például a `mypassword123` jelszó titkosításához:
```bash
dignacli encrypt mypassword123
```
A parancs a megadott jelszó titkosított változatát adja vissza; ezt a változatot később biztonságos környezetben lehet használni. Ha nem ad meg jelszó-argumentumot, a CLI hibát jelez a hiányzó argumentum miatt.

## `generate-key` parancs használata
  
A `generate-key` parancs egy Fernet kulcsot hoz létre, amely a ***digna*** repository-ban tárolt jelszavak védelméhez szükséges.
  
### Használat
```bash
dignacli generate-key
```
  
# Adatkezelés

## `clean-up` parancs használata

A `clean-up` parancs egy adott projekt keretében egy vagy több adatforráshoz tartozó profilok, előrejelzések és Forgalmi Lámpa Rendszer (Traffic Light System - TLS) adatok eltávolítására szolgál a ***digna*** CLI-ben. Ez a parancs fontos az adatok életciklus-kezelésében és segít a régi vagy felesleges adatok törlésében.

### Használat

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyből az adatok eltávolításra kerülnek (kötelező). Ha az argumentum értéke `all-projects`, a ***digna*** végigiterál az összes meglévő projekten és alkalmazza a parancsot.
- **FROM_DATE**: A tisztítás kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: A tisztítás záró dátuma és ideje; ugyanazokat a formátumokat követi, mint a FROM_DATE (kötelező).
  
### Opciók
  
- `--table-name`, `-tn`: A tisztítás műveletet korlátozza egy adott tábla nevére a projektben.
- `--table-filter`, `-tf`: Szűrőt alkalmaz a táblákra, csak azokat kezeli, amelyek neve tartalmazza a megadott alláncot.
- `--timing`, `-tm`: A tisztítás befejezése után megjeleníti a művelet időtartamát.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
### Példa
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Csak a `Table1` nevű táblából történő adatok törlése:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás menedzselésében és abban, hogy a repository csak a releváns információkat tartalmazza.

## `inspect` parancs használata

Az `inspect` parancs profilok, előrejelzések és Forgalmi Lámpa Rendszer adatok létrehozására szolgál egy adott projekt egy vagy több adatforrására vonatkozóan a ***digna*** CLI-ben. Ez a parancs hasznos az adatok adott időszak alatti elemzéséhez és monitorozásához.

### Használat

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelyen az ellenőrzést végrehajtják (kötelező). Ha az érték `all-projects`, a ***digna*** az összes meglévő projekten végrehajtja a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és ideje; ugyanazokat a formátumokat követi, mint a FROM_DATE (kötelező).
  
### Opciók

- `--table-name`, `-tn`: Az ellenőrzést egy konkrét tábla nevére korlátozza a projektben.
- `--table-filter`, `-tf`: Szűrőt alkalmaz, hogy csak az adott alláncot tartalmazó táblákon végezze el az ellenőrzést.
- `--do-profile`: Újraindítja a profilok gyűjtését. Alapértelmezett: do-profile.
- `--no-do-profile`: Megakadályozza a profilok újragyűjtését.
- `--do-prediction`: Újraszámolja az előrejelzéseket. Alapértelmezett: do-prediction.
- `--no-do-prediction`: Megakadályozza az előrejelzések újraszámolását.
- `--do-alert-status`: Újraszámolja az figyelmeztetési/riasztási státuszokat. Alapértelmezett: do-alert-status.
- `--no-do-alert-status`: Megakadályozza az riasztási státuszok újraszámolását.
- `--timing`, `-tm`: A művelet befejezése után megmutatja az ellenőrzés időtartamát.
  
### Példa
  
A `ProjectA` projekt 2024. január 1. és 2024. január 31. közötti adatainak ellenőrzése:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy adott tábla ellenőrzése és az előrejelzések újraszámolásának kikényszerítése:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos frissített profilok és előrejelzések létrehozásához, az adatintegritás monitorozásához és a megadott projektidőszakra vonatkozó riasztási rendszerek kezeléséhez.

## `tls-status` parancs használata

A `tls-status` parancs egy adott napon belül egy projekt egy adott táblájának Forgalmi Lámpa Rendszer (TLS) státuszát kérdezi le a ***digna*** CLI-ben. A Forgalmi Lámpa Rendszer betekintést nyújt az adatok egészségébe és minőségébe, valamint kiemeli a figyelmet igénylő problémákat vagy riasztásokat.
  
### Használat
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyre a TLS státuszt lekérdezik (kötelező).
- **TABLE_NAME**: A projektben lévő tábla, melyre a TLS státusz vonatkozik (kötelező).
- **DATE**: A lekérdezett TLS státusz dátuma, általában %Y-%m-%d formátumban (kötelező).
  
### Példa
  
A `ProjectA` projekt `UserData` táblájának 2024. július 1-jei TLS státuszának ellenőrzése:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

A parancs előre definiált kritériumok alapján egy világos és hasznos státuszüzenetet ad, amely segít a felhasználóknak az adatminőség nyomon követésében és fenntartásában.

## `list-projects` parancs használata
  
A `list-projects` parancs kilistázza a ***digna*** CLI-ben elérhető összes projektet.
  
### Használat
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos adminisztrátorok és több projektet kezelő felhasználók számára; gyors áttekintést ad a repository-ban található projektek állapotáról.

## `list-ds` parancs használata

A `list-ds` parancs kilistázza egy adott projektben elérhető összes adatforrást a ***digna*** CLI-ben. Ez a parancs segít megérteni az elemzéshez és kezeléshez rendelkezésre álló adatvagyonokat.

### Használat
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentumok
- **PROJECT_NAME**: Az a projekt, amelynek adatforrásait listázni szeretné (kötelező).
  
### Példa
  
Az összes adatforrás kilistázása a `ProjectA` projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést nyújt egy projekt adatforrásairól, és segíti a felhasználókat az adatkörnyezet hatékonyabb navigálásában és kezelésében.
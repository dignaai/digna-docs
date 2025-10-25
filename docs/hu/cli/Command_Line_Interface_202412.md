---
title: digna CLI Reference 2024.12 – Commands & Examples | digna Documentation
description: Teljes referencia a digna CLI 2024.12 kiadásához. Ismerje meg, hogyan kezelhet felhasználókat, tárolókat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect és továbbiak.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Ez az oldal dokumentálja a ***digna*** CLI **2024.12** kiadásában elérhető teljes parancskészletet, beleértve a használati példákat és opciókat.

---


**2024-12-09**


---

## CLI alapok

---

## A `--help` opció használata

A `--help` opció információt nyújt az elérhető parancsokról és azok használatáról. Ennek az opciónak két fő használati módja van:

1. **Általános súgó megjelenítése:**
   
    Használja a --help-et közvetlenül a ***dignacli*** kulcsszó után  
   ```bash
   dignacli --help
   ```

3.  **Konkrét parancsok súgójának lekérése:**  
  
    Részletes információkért egy adott parancsról, fűzze hozzá a `--help` opciót a parancshoz.
    Például az `add-user` parancs súgójának lekéréséhez futtassa:
     ```bash
     dignacli add-user --help
     ```

     ### kimenet:
      
     - **Parancs leírása:** Részletesen ismerteti, mit végez a parancs.  
     - **Szinaxis:** Megjeleníti a pontos szintaxist, beleértve a kötelező és opcionális argumentumokat.  
     - **Opciók:** Felsorolja a parancshoz tartozó opciókat és magyarázatukat.  
     - **Példák:** Mutat példákat a parancs hatékony végrehajtására.

  
## A `check-repo-connection` parancs használata

A check-repo-connection parancs a ***digna*** CLI eszköz része, amely a megadott ***digna*** tároló elérhetőségét és hozzáférését teszteli. Ez a parancs biztosítja, hogy a CLI képes legyen kommunikálni a tárolóval.
      
### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres végrehajtás esetén a parancs megerősíti a kapcsolatot, és részleteket jelenít meg a tárolóról: Repository version, Host, Database és Schema.  
  
Ha a tárolóhoz való csatlakozás nem sikerül, ellenőrizze a config.toml fájlt a helyes konfigurációs beállításokért.

## A `--version` parancs használata

A telepített *dignacli* verziójának lekérdezéséhez használja a --version opciót.  
  
### Parancs használata
```bash
dignacli --version
```
  
### Példa kimenet
```bash
dignacli version 2024.12
```

## Naplózási opciók használata
  
Alapértelmezés szerint a ***digna*** parancsok konzol kimenete minimalista. A legtöbb parancs lehetőséget ad további információk megadására a következő opciókkal:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A "verbose" és "debug" a részletesség szintjét határozza meg, míg a "logfile" kapcsoló lehetővé teszi a kimenet fájlba irányítását a konzol helyett.

# Felhasználókezelés

## Az `add-user` parancs használata
  
Az add-user parancs a ***digna*** CLI-ben új felhasználó létrehozására szolgál a ***digna*** rendszerben.
  
### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

### Opciók

- `--is_superuser`, `-su`: Jelző, amellyel az új felhasználót adminisztrátorrá jelölik.
- `--valid_until`, `-vu`: Beállítja a felhasználói fiók lejárati dátumát a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs beállítva, a fióknak nincs lejárati dátuma.

### Példa

Új felhasználó hozzáadása `jdoe` felhasználónévvel, `John Doe` teljes névvel és `password123` jelszóval:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Új felhasználó hozzáadása és fióklejárat beállítása:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## A `delete-user` parancs használata
  
A `delete-user` parancs a ***digna*** CLI-ben meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből.
  
### Parancs használata
```bash
dignacli delete-user USER_NAME
```
  
### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen kötelező argumentum.

### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs végrehajtásával a `jdoe` felhasználó eltávolításra kerül a ***digna*** rendszerből, visszavonva hozzáférését és törölve a repositoryban tárolt kapcsolódó adatait és jogosultságait.

## A `modify-user` parancs használata

A `modify-user` parancs a ***digna*** CLI-ben meglévő felhasználó adatainak frissítésére szolgál a ***digna*** rendszerben.

### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új teljes név a felhasználó számára (kötelező).
  
### Opciók  
  
- `--is_superuser`, `-su`: A felhasználót szuperfelhasználóvá teszi, emelt szintű jogosultságokat adva. Ez a zászló nem igényel értéket.  
- `--valid_until`, `-vu`: Beállítja a felhasználói fiók lejárati dátumát a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
### Példa
  
A `jdoe` felhasználó teljes nevének módosítása "Johnathan Doe"-ra, és a felhasználó szuperfelhasználóvá tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## A `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben meglévő felhasználó jelszavának megváltoztatására szolgál a ***digna*** rendszerben.
  
### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentumok
  
- **USER_NAME**: A felhasználó felhasználóneve, akinek a jelszavát meg kell változtatni (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
### Példa
  
A `jdoe` felhasználó jelszavának megváltoztatása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## A `list-users` parancs használata

A `list-users` parancs a ***digna*** CLI-ben felsorolja a rendszerben regisztrált összes felhasználót.

### Parancs használata

```bash
dignacli list-users
```

A parancs végrehajtásakor a ***digna*** CLI csatlakozik a ***digna*** tárolóhoz, és felsorolja az összes felhasználót, megjelenítve az ID-t, felhasználónevet, teljes nevet, szuperfelhasználói státuszt és lejárati időbélyegeket.

# Tárolókezelés

### Az `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** tároló frissítésére vagy inicializálására szolgál. Ez a parancs nélkülözhetetlen a frissítések alkalmazásához vagy a tároló infrastruktúra első alkalommal történő beállításához.
  
### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut, amely kiírja azokat az SQL utasításokat, amelyeket végrehajtana, de valójában nem futtatja őket. Hasznos a változások előnézetéhez anélkül, hogy módosításokat végezne a tárolón.  

  
### Példa
  
A ***digna*** tároló frissítéséhez futtassa a parancsot opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
Szimulációs módban (az SQL utasítások megtekintéséhez a tényleges alkalmazás nélkül):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kulcsfontosságú a ***digna*** rendszer karbantartásához, biztosítva, hogy az adatbázis séma és a tároló egyéb komponensei naprakészek legyenek a szoftver legújabb verziójával.

## Az `encrypt` parancs használata
  
Az `encrypt` parancs a ***digna*** CLI-ben jelszó titkosítására szolgál.
  
### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
### Példa
  
Egy jelszó titkosításához adja meg a jelszót argumentumként.   
Például a `mypassword123` jelszó titkosításához használja:
```bash
dignacli encrypt mypassword123
```
A parancs visszaadja a megadott jelszó titkosított változatát, amely biztonságos környezetben használható. Ha a jelszó argumentum nincs megadva, a CLI hibát jelez a hiányzó argumentum miatt.

## A `generate-key` parancs használata
  
A `generate-key` parancs egy Fernet kulcs generálására szolgál, amely szükséges a tárolt jelszavak védelméhez a ***digna*** tárolóban.
  
### Parancs használata
```bash
dignacli generate-key
```
  
# Adatkezelés

## A `clean-up` parancs használata

A `clean-up` parancs a ***digna*** CLI-ben profilok, előrejelzések és a forgalmi lámpa rendszer adatait távolítja el egy vagy több adatforrásból egy megadott projekt keretében. Ez a parancs fontos az adatok életciklusának kezeléséhez, segít rendezett és hatékony adatkörnyezet fenntartásában az elavult vagy felesleges adatok törlésével.

### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, ahonnan az adatokat törölni kell (kötelező). Az all-projects kulcsszó használata azt utasítja a ***digna***-nak, hogy iteráljon az összes meglévő projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az adatok törlésének kezdő dátuma és időpontja. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adatok törlésének záró dátuma és időpontja, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
### Opciók
  
- `--table-name`, `-tn`: A clean-up műveletet egy adott táblára korlátozza a projektben.
- `--table-filter`, `-tf`: Szűrő, amely a törlést csak azokra a táblákra korlátozza, amelyek nevében a megadott részstring szerepel.
- `--timing`, `-tm`: A clean-up folyamat befejezése után megjeleníti a művelet időtartamát.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
### Példa
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Adatok eltávolítása csak egy konkrét, `Table1` nevű táblából:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében és abban, hogy a tároló csak a releváns információkat tartalmazza.

## Az `inspect` parancs használata

Az `inspect` parancs a ***digna*** CLI-ben profilok, előrejelzések és a forgalmi lámpa rendszer adatok létrehozására szolgál egy vagy több adatforrásban egy megadott projekt keretében. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakon belül.

### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyet ellenőrizni kell (kötelező). Az all-projects kulcsszó használata azt utasítja a ***digna***-nak, hogy iteráljon az összes meglévő projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és időpontja. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és időpontja, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
### Opciók

- `--table-name`, `-tn`: Az ellenőrzést korlátozza egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűrő, amely csak azokat a táblákat ellenőrzi, amelyek nevében a megadott részstring szerepel.
- `--do-profile`: Elindítja a profilok újragyűjtését. Alapértelmezett: do-profile.
- `--no-do-profile`: Megakadályozza a profilok újragyűjtését.
- `--do-prediction`: Elindítja az előrejelzések újraszámítását. Alapértelmezett: do-prediction.
- `--no-do-prediction`: Megakadályozza az előrejelzések újraszámítását.
- `--do-alert-status`: Elindítja az riasztási státuszok újraszámítását. Alapértelmezett: do-alert-status.
- `--no-do-alert-status`: Megakadályozza az riasztási státuszok újraszámítását.
- `--iterative`: Az időszak napi iterációk során történő ellenőrzését indítja. Alapértelmezett: iterative.
- `--no-iterative`: Az egész időszak egyszeri ellenőrzését hajtja végre.
- `--timing`, `-tm`: Az ellenőrzési folyamat befejezése után megjeleníti az időtartamot.
  
### Példa
  
Adatok ellenőrzése a `ProjectA` projekt számára 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy adott tábla ellenőrzése és az előrejelzések újraszámításának kényszerítése:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos a frissített profilok és előrejelzések generálásához, az adatintegritás monitorozásához és a riasztási rendszer kezeléséhez egy meghatározott projektidőszakon belül.

## A `tls-status` parancs használata

A `tls-status` parancs a ***digna*** CLI-ben a Traffic Light System (TLS) állapotának lekérdezésére szolgál egy adott tábla esetén egy projektben egy megadott dátumra. A Traffic Light System betekintést nyújt az adatok egészségébe és minőségébe, jelezve az esetleges problémákat vagy riasztásokat, amelyek figyelmet igényelnek.
  
### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyhez a TLS állapotot lekérdezik (kötelező).
- **TABLE_NAME**: A projektben található konkrét tábla, amelyre a TLS állapot szükséges (kötelező).
- **DATE**: Az a dátum, amelyre a TLS állapotot lekérdezik, általában a %Y-%m-%d formátumban (kötelező).
  
### Példa
  
A TLS állapot ellenőrzése a UserData nevű táblára a ProjectA projektben 2024. július 1-jén:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ez a parancs segít a felhasználóknak az adatok minőségének monitorozásában és karbantartásában, világos és végrehajtható állapotjelentést nyújtva előre definiált kritériumok alapján.

## A `list-projects` parancs használata
  
A `list-projects` parancs a ***digna*** CLI-ben az összes elérhető projekt listázására szolgál a ***digna*** rendszerben.
  
### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos az adminisztrátorok és a több projektet kezelő felhasználók számára, gyors áttekintést adva az elérhető projektekről a ***digna*** tárolóban.

## A `list-ds` parancs használata

A `list-ds` parancs a ***digna*** CLI-ben az adott projekt összes elérhető adatforrását listázza. Ez a parancs hasznos az elemzésre és kezelésre rendelkezésre álló adatvagyon megismeréséhez a ***digna*** rendszerben.

### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentumok
- **PROJECT_NAME**: A projekt neve, amelyhez az adatforrások listázása történik (kötelező).
  
### Példa
  
Az összes adatforrás felsorolása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést nyújt a projektben elérhető adatforrásokról, segítve a felhasználókat az adatstruktúra hatékonyabb navigálásában és kezelésében.
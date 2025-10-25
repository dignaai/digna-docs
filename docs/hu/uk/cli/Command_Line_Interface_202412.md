---
title: digna CLI Referencia 2024.12 – Parancsok és példák | digna Documentation
description: Teljes referencia a digna CLI 2024.12 kiadásához. Tudja meg, hogyan kezelhet felhasználókat, repository-kat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect és mások.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Ezen az oldalon dokumentáltuk a CLI ***digna*** teljes parancskészletét a **2024.12** kiadáshoz, beleértve használati példákat és opciókat.

---


**2024-12-09**


---

## CLI alapok

---

## A `--help` opció használata

A `--help` opció információt ad az elérhető parancsokról és azok használatáról. Két fő módja van ennek az opció használatának:

1. **Általános súgó megjelenítése:**
   
    Használja a --help-et közvetlenül a ***dignacli*** kulcsszó után  
   ```bash
   dignacli --help
   ```

3.  **Súgó lekérése egy konkrét parancshoz:**  
  
    Egy adott parancs részletes információinak lekéréséhez adja hozzá a `--help`-et a parancshoz.
    Például az `add-user` parancs súgójának lekéréséhez futtassa:
     ```bash
     dignacli add-user --help
     ```

     ### kimenet:
      
     - **Parancs leírása:** Részletesen bemutatja, mit végez a parancs.  
     - **Szinaktxis:** Megmutatja a pontos használatot, beleértve a kötelező és opcionális argumentumokat.  
     - **Opciók:** Felsorolja a parancsra vonatkozó opciókat és azok magyarázatát.  
     - **Példák:** Mutat példákat a parancs hatékony használatára.

  
## A `check-repo-connection` parancs használata

A `check-repo-connection` parancs a CLI ***digna*** eszközben arra szolgál, hogy ellenőrizze a megadott digna repository-hoz való csatlakozást és hozzáférést. A parancs meggyőződik arról, hogy a CLI képes kommunikálni a repository-val.
      
### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres végrehajtás esetén a parancs visszaigazolást ad a csatlakozásról, valamint részleteket a repository-ról: repository verzió, host, adatbázis és séma.  
  
Ha a csatlakozás nem sikerül, ellenőrizze a config.toml fájlt a helyes beállításokért.

## A `version` parancs használata

Az telepített *dignacli* verzió ellenőrzéséhez használja a `--version` opciót.  
  
### Parancs használata
```bash
dignacli --version
```
  
### Példa kimenet
```bash
dignacli version 2024.12
```

## Naplózási paraméterek használata
  
Alapértelmezés szerint a ***digna*** parancsok konzolos kimenete tömör. A legtöbb parancs több információt adhat az alábbi opciók segítségével:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A „verbose” és a „debug” a részletességi szintet határozza meg, míg a „logfile” kapcsoló lehetővé teszi a kimenet fájlba irányítását a konzol helyett.

# Felhasználók kezelése

## Az `add-user` parancs használata
  
Az `add-user` parancs a CLI ***digna***-ban új felhasználó hozzáadására szolgál a digna rendszerbe.
  
### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentumok

- **USER_NAME**: Az új fiók felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

### Opciók

- `--is_superuser`, `-su`: Jelző az új felhasználó adminisztrátorrá tételéhez.
- `--valid_until`, `-vu`: A fiók lejárati dátumának beállítása `YYYY-MM-DD HH:MI:SS` formátumban. Ha nem adja meg, a fióknak nincs lejárati ideje.

### Példa

Új felhasználó hozzáadása `jdoe` felhasználónévvel, `John Doe` teljes névvel és `password123` jelszóval:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Új felhasználó hozzáadása lejárati dátummal:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## A `delete-user` parancs használata
  
A `delete-user` parancs a CLI ***digna***-ban meglévő felhasználó törlésére szolgál a digna rendszerből.
  
### Parancs használata
```bash
dignacli delete-user USER_NAME
```
  
### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen szükséges argumentum.

### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs végrehajtásával a `jdoe` felhasználó hozzáférése visszavonásra kerül, és a kapcsolódó adatok és jogosultságok törlődnek a repository-ból.

## A `modify-user` parancs használata

A `modify-user` parancs a CLI ***digna***-ban meglévő felhasználó adatainak frissítésére szolgál a digna rendszerben.

### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
### Opciók  
  
- `--is_superuser`, `-su`: A felhasználót superuserré teszi, magasabb jogosultságokkal. Ez a jelző nem igényel értéket.  
- `--valid_until`, `-vu`: A fiók lejárati dátumának beállítása YYYY-MM-DD HH:MI:SS formátumban. Ha nem adja meg, a fiók határozatlan ideig érvényes marad.  
  
### Példa
  
A `jdoe` felhasználó teljes nevének módosítása „Johnathan Doe”-ra és superuser jelző beállítása:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## A `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs a CLI ***digna***-ban meglévő felhasználó jelszavának megváltoztatására szolgál a digna rendszerben.
  
### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentumok
  
- **USER_NAME**: A felhasználó felhasználóneve, amelyhez a jelszót módosítani kell (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
### Példa
  
A `jdoe` felhasználó jelszavának módosítása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## A `list-users` parancs használata

A `list-users` parancs a CLI ***digna***-ban megjeleníti az összes regisztrált felhasználót a digna rendszerben.

### Parancs használata

```bash
dignacli list-users
```

A parancs csatlakozik a digna repository-hoz és kilistázza az összes felhasználót, megjelenítve az ID-t, felhasználónevet, teljes nevet, superuser státuszt és a lejárati időbélyegeket.

# Repository kezelése

### Az `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a CLI ***digna***-ban a repository frissítésére vagy inicializálására szolgál. Ezt a parancsot akkor kell használni, amikor frissítéseket kell alkalmazni, vagy a repository infrastruktúráját először kell beállítani.
  
### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban futtatja, és kiírja azokat az SQL utasításokat, amelyek végrehajtásra kerülnének, de ténylegesen nem hajtja végre őket. Ez hasznos a módosítások előzetes megtekintéséhez anélkül, hogy változtatná a repository-t.  

  
### Példa
  
A digna repository frissítéséhez futtassa a parancsot opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
Szimulációs módban történő frissítéshez (az SQL utasítások megjelenítéséhez, de alkalmazásuk nélkül):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs fontos a digna rendszer karbantartásához, biztosítva az adatbázis séma és a repository komponenseinek naprakészségét a szoftver legújabb verziójával.

## Az `encrypt` parancs használata
  
Az `encrypt` parancs a CLI ***digna***-ban jelszavak titkosítására szolgál.
  
### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
### Példa
  
Jelszó titkosításához adja meg argumentumként.   
Például a `mypassword123` titkosításához használja:
```bash
dignacli encrypt mypassword123
```
A parancs visszaadja a megadott jelszó titkosított változatát, amelyet aztán biztonságos környezetben használhat. Ha nincs megadva jelszó argumentum, a CLI hibát jelez a hiányzó argumentumról.

## A `generate-key` parancs használata
  
A `generate-key` parancs Fernet-kulcs generálására szolgál, amely a repository-ban tárolt jelszavak védelméhez szükséges.
  
### Parancs használata
```bash
dignacli generate-key
```
  
# Adatkezelés

## A `clean-up` parancs használata

A `clean-up` parancs a CLI ***digna***-ban profilok, előrejelzések és a Traffic Light System adatok törlésére szolgál egy vagy több adatforrásból egy megadott projekt keretében. Ez a parancs fontos az adatok életciklusának kezeléséhez, segít rendben és hatékonyan tartani a környezetet a régi vagy felesleges adatok eltávolításával.

### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, ahonnan törölni szeretné az adatokat (kötelező). Az `all-projects` kulcsszó használata arra utasítja a ***digna***-t, hogy végigiteráljon az összes meglévő projekten és alkalmazza a parancsot.
- **FROM_DATE**: A törlés kezdetének dátuma és időpontja. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: A törlés befejezésének dátuma és időpontja, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
### Opciók
  
- `--table-name`, `-tn`: A törlési művelet korlátozása egy konkrét táblára a projektben.
- `--table-filter`, `-tf`: Szűrő a táblák korlátozásához, amelyek nevében a megadott részstring szerepel.
- `--timing`, `-tm`: A törlési folyamat időtartamának megjelenítése a befejezés után.
- `--help`: Súgó megjelenítése a clean-up parancshoz, majd kilépés.
  
### Példa
  
Adatok törlése a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Csak egy konkrét, `Table1` nevű táblából történő törlés:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében és biztosítja, hogy a repository-ban csak releváns információk maradjanak.

## Az `inspect` parancs használata

Az `inspect` parancs a CLI ***digna***-ban profilok, előrejelzések és a Traffic Light System adatok létrehozására szolgál egy vagy több adatforrás esetén egy adott projektben. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakra vonatkozóan.

### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyre az adatellenőrzést végrehajtja (kötelező). Az `all-projects` kulcsszó használata azt jelenti, hogy a ***digna*** végigiterál az összes elérhető projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés befejezésének dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
### Opciók

- `--table-name`, `-tn`: Az ellenőrzés korlátozása egy konkrét táblára a projektben.
- `--table-filter`, `-tf`: Csak azoknak a tábláknak az ellenőrzése, amelyek nevében a megadott részstring szerepel.
- `--do-profile`: Újraprofil-gyűjtés futtatása. Alapértelmezés szerint — do-profile.
- `--no-do-profile`: Letiltja az újraprofil-gyűjtést.
- `--do-prediction`: Előrejelzések újraszámítása. Alapértelmezés szerint — do-prediction.
- `--no-do-prediction`: Letiltja az előrejelzések újraszámítását.
- `--do-alert-status`: Az alert státuszok újraszámítása. Alapértelmezés szerint — do-alert-status.
- `--no-do-alert-status`: Letiltja az alert státuszok újraszámítását.
- `--iterative`: Az időszak napi iterációkban történő ellenőrzése. Alapértelmezés szerint — iterative.
- `--no-iterative`: Az egész időszak egyetlen futással történő ellenőrzése.
- `--timing`, `-tm`: Az ellenőrzési folyamat időtartamának megjelenítése a befejezés után.
  
### Példa
  
Adatok ellenőrzése a `ProjectA` projekthez 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy konkrét tábla ellenőrzése és az előrejelzések kényszerített újraszámítása:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos frissített profilok és előrejelzések generálásához, az adatintegritás monitorozásához és az alert rendszer kezeléséhez a projekt meghatározott időszakában.

## A `tls-status` parancs használata

A `tls-status` parancs a CLI ***digna***-ban a Traffic Light System (TLS) státuszának lekérésére szolgál egy adott táblához egy projektben megadott dátumra. A Traffic Light System betekintést nyújt az adatok állapotába és minőségébe, jelezve az esetleges problémákat vagy figyelmeztetéseket, amelyekre figyelni kell.
  
### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyhez a TLS státusz kérhető (kötelező).
- **TABLE_NAME**: A projekt adott táblája, amelyhez a TLS státusz szükséges (kötelező).
- **DATE**: A dátum, amelyre a TLS státuszt lekérdezik, általában %Y-%m-%d formátumban (kötelező).
  
### Példa
  
A `UserData` tábla TLS státuszának ellenőrzése a `ProjectA` projektben 2024. július 1-jére:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ez a parancs segíti a felhasználókat az adatok minőségének monitorozásában és fenntartásában, világos és cselekvőképes jelentést adva előre definiált kritériumok alapján.

## A `list-projects` parancs használata
  
A `list-projects` parancs a CLI ***digna***-ban az összes elérhető projekt kilistázására szolgál.
  
### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és olyan felhasználók számára, akik több projektet kezelnek, gyors áttekintést nyújtva a repository-ban elérhető projektekről.

## A `list-ds` parancs használata

A `list-ds` parancs a CLI ***digna***-ban az adott projekt összes elérhető adatforrásának kilistázására szolgál. Ez a parancs hasznos az adatokkal kapcsolatos eszközök megismeréséhez, amelyek elemzésre és kezelésre elérhetők a digna rendszerben.

### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentumok
- **PROJECT_NAME**: A projekt neve, amelyhez az adatforrások listázása történik (kötelező).
  
### Példa
  
Az összes adatforrás kilistázása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést ad a projektben elérhető adatforrásokról, segítve a hatékonyabb navigációt és az adatok kezelését.
---
title: digna CLI Reference 2024.11 – Parancsok & Példák | digna Dokumentáció
description: Teljes referencia a digna CLI kiadás 2024.11-hez. Ismerje meg, hogyan kezelhet felhasználókat, tárolókat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect, tls-status és továbbiak.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Referencia 2024.11
**2024-11-03**

Ez az oldal dokumentálja a CLI ***digna*** **2024.11** verziójában elérhető teljes parancskészletet, beleértve a használati példákat és opciókat.


---
## A CLI alapjai

---

## A `--help` opció használata

A `--help` opció információt nyújt az elérhető parancsokról és azok használatáról. Két fő módja van az opció használatának:

1. **Általános súgó megjelenítése:**
   
   Használja a `--help`-et közvetlenül a `dignacli` parancs után.  
   ```bash
   dignacli --help
   ```

2. **Súgó egy konkrét parancshoz:**
   
   Részletes információkért egy adott parancsról adja hozzá a `--help`-et a parancs után.  
   Például az `add-user` parancs súgójának lekéréséhez futtassa:
   ```bash
   dignacli add-user --help
   ```

   ### Kimenet:
    
   - **Parancs leírása:** Részletesen ismerteti, mit csinál a parancs.  
   - **Szintaxis:** Megmutatja a pontos szintaxist, beleértve a kötelező és opcionális argumentumokat.  
   - **Opciók:** Felsorolja a parancshoz tartozó opciókat és azok magyarázatát.  
   - **Példák:** Hatékony végrehajtási példákat ad.

  
## A `check-repo-connection` parancs használata

A `check-repo-connection` parancs a CLI ***digna*** eszközeiben arra szolgál, hogy ellenőrizze a megadott ***digna*** tároló elérhetőségét és kapcsolatát. A parancs biztosítja, hogy a CLI képes kommunikálni a tárolóval.
      
### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres végrehajtás után a parancs megerősítést ad a kapcsolatról, valamint részleteket a tárolóról: a tároló verzióját, hostját, adatbázisát és sémáját.  
  
Ha a kapcsolat a tárolóval nem sikerül, ellenőrizze a config.toml fájlt a beállítások helyessége szempontjából.

## A `--version` opció használata

A telepített *dignacli* verzió ellenőrzéséhez használja a `--version` opciót.  
  
### Parancs használata
```bash
dignacli --version
```
  
### Példa kimenet
```bash
dignacli version 2024.11
```

## Naplózási opciók használata
  
Alapértelmezés szerint a ***digna*** parancsok konzol-kimenete minimalistán jelenik meg. A legtöbb parancs további információk megjelenítését teszi lehetővé a következő opciókkal:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
A "verbose" és a "debug" a részletezettség szintjét határozza meg, míg a "logfile" kapcsoló lehetővé teszi a kimenet fájlba történő átirányítását a konzol helyett.

# Felhasználókezelés

## Az `add-user` parancs használata
  
Az `add-user` parancs a CLI ***digna*** rendszerében új felhasználó hozzáadására szolgál a ***digna*** rendszerbe.
  
### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentumok

- **USER_NAME**: Az új fiók felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

### Opciók

- `--is_superuser`, `-su`: Jelölő, amely a felhasználót rendszergazdai jogosultságokkal ruházza fel.
- `--valid_until`, `-vu`: Beállítja a fiók lejárati dátumát a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fióknak nincs lejárati dátuma.

### Példa

Új felhasználó hozzáadása `jdoe` felhasználónévvel, `John Doe` teljes névvel és `password123` jelszóval:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Példa lejárati dátummal:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## A `delete-user` parancs használata
  
A `delete-user` parancs a CLI ***digna*** rendszerében meglévő felhasználó törlésére szolgál a ***digna*** rendszerből.
  
### Parancs használata
```bash
dignacli delete-user USER_NAME
```
  
### Argumentumok
- **USER_NAME**: A törlendő felhasználó neve (kötelező). Ez az egyetlen argumentum, amelyet a parancs igényel.

### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs futtatásával a `jdoe` felhasználó hozzáférése visszavonásra kerül, és a vele kapcsolatos adatok és jogosultságok törlődnek a ***digna*** tárolóból.

## A `modify-user` parancs használata

A `modify-user` parancs a CLI ***digna*** rendszerében meglévő felhasználó adatait frissíti a ***digna*** rendszerben.

### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó neve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
### Opciók  
  
- `--is_superuser`, `-su`: A felhasználót szuperfelhasználóvá teszi, magasabb jogosultságokat adva. Ez a kapcsoló érték megadása nélkül használható.  
- `--valid_until`, `-vu`: Beállítja a fiók lejárati dátumát YYYY-MM-DD HH:MI:SS formátumban. Ha nem adja meg, a fiók határozatlan ideig érvényes marad.  
  
### Példa
  
A `jdoe` teljes nevének módosítása `Johnathan Doe`-ra és szuperfelhasználói szerep hozzárendelése:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## A `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs a CLI ***digna*** rendszerében meglévő felhasználó jelszavának megváltoztatására szolgál.
  
### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentumok
  
- **USER_NAME**: A jelszó módosítandó felhasználó neve (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
### Példa
  
A `jdoe` felhasználó jelszavának megváltoztatása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## A `list-users` parancs használata

A `list-users` parancs a CLI ***digna*** rendszerében az összes regisztrált felhasználó listáját jeleníti meg.

### Parancs használata

```bash
dignacli list-users
```

A parancs csatlakozik a ***digna*** tárolóhoz és kilistázza az összes felhasználót, megjelenítve az ID-jukat, felhasználónevüket, teljes nevüket, szuperfelhasználói státuszukat és a lejárati időbélyegeket.

# Tároló (repository) kezelése

### Az `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a CLI ***digna*** rendszerében a tároló frissítésére vagy inicializálására szolgál. A parancs szükséges a frissítések alkalmazásához vagy a tároló infrastruktúrájának első beállításához.
  
### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut, és kiírja azokat az SQL utasításokat, amelyek végrehajtásra kerülnének, de ténylegesen nem hajtja végre őket. Hasznos a változtatások megtekintéséhez anélkül, hogy módosításokat végezne a tárolón.  

  
### Példa
  
A tároló frissítése opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
Szimulációs módban történő futtatás (az SQL utasítások megtekintéséhez anélkül, hogy alkalmazná őket):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kulcsfontosságú a ***digna*** rendszer karbantartásához, biztosítva az adatbázis séma és a tároló egyéb komponenseinek naprakészségét a szoftver legújabb verziójával.

## Az `encrypt` parancs használata
  
Az `encrypt` parancs a CLI ***digna*** rendszerében jelszavak titkosítására szolgál.
  
### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
### Példa
  
Egy jelszó titkosításához adja meg a jelszót argumentumként.  
Például a `mypassword123` titkosításához használja:
```bash
dignacli encrypt mypassword123
```
A parancs kiadja a megadott jelszó titkosított verzióját, amelyet biztonságos környezetben használhat. Ha a jelszó argumentum nincs megadva, a CLI hibaüzenetet ad a hiányzó argumentumról.

## A `generate-key` parancs használata
  
A `generate-key` parancs Fernet-kulcs generálására szolgál, amely szükséges a tárolt jelszavak védelméhez a ***digna*** tárolóban.
  
### Parancs használata
```bash
dignacli generate-key
```
  
# Adatkezelés

## A `clean-up` parancs használata

A `clean-up` parancs a CLI ***digna*** rendszerében profilmetszések, előrejelzések és a Traffic Light System-hez tartozó adatok törlésére szolgál egy vagy több adattforrásra vonatkozóan a megadott projektben. Ez a parancs fontos az adatok életciklus-kezeléséhez, segítve a rendezettség és hatékonyság fenntartását az elavult vagy felesleges adatok eltávolításával.

### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, ahonnan törölni kell az adatokat (kötelező). Az `all-projects` kulcsszó használata arra utasítja a ***digna***-t, hogy iteráljon az összes létező projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az adatok törlésének kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adatok törlésének záró dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
### Opciók
  
- `--table-name`, `-tn`: A törlést korlátozza egy konkrét táblára a projektben.
- `--table-filter`, `-tf`: Szűrő a táblanevek alsubstringje alapján, hogy csak azokat a táblákat törölje, amelyek tartalmazzák a megadott részt.
- `--timing`, `-tm`: A törlési folyamat időtartamának megjelenítése a befejezés után.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
### Példa
  
Adatok törlése a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Csak egy konkrét `Table1` nevű táblából történő törlés:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében, és biztosítja, hogy a tárolóban csak releváns információk maradjanak.

## Az `inspect` parancs használata

Az `inspect` parancs a CLI ***digna*** rendszerében profilok, előrejelzések és a Traffic Light System adatok létrehozására szolgál egy vagy több adattforrásra vonatkozóan a megadott projektben. A parancs segít az adatok elemzésében és monitorozásában a megadott időszakra vonatkozóan.

### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelynek adatait vizsgálni kell (kötelező). Az `all-projects` kulcsszó használata arra utasítja a ***digna***-t, hogy végigmenjen az összes meglévő projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
### Opciók

- `--table-name`, `-tn`: Az ellenőrzést korlátozza egy konkrét táblára a projektben.
- `--table-filter`, `-tf`: Csak azokat a táblákat vizsgálja, amelyek neve tartalmazza a megadott alstringet.
- `--do-profile`: Újraprofilozást indít. Alapértelmezett: do-profile.
- `--no-do-profile`: Megakadályozza az újraprofilozást.
- `--do-prediction`: Előrejelzések újraszámítását indítja. Alapértelmezett: do-prediction.
- `--no-do-prediction`: Megakadályozza az előrejelzések újraszámítását.
- `--do-alert-status`: Az alert státuszok újraszámítását indítja. Alapértelmezett: do-alert-status.
- `--no-do-alert-status`: Megakadályozza az alert státuszok újraszámítását.
- `--timing`, `-tm`: Az ellenőrzési folyamat időtartamának megjelenítése a befejezés után.
  
### Példa
  
Adatok ellenőrzése a `ProjectA` projekthez 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Egy konkrét tábla ellenőrzése és az előrejelzések kényszerített újraszámítása:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos frissített profilok és előrejelzések generálásához, az adatok integritásának ellenőrzéséhez és az alert rendszer kezeléséhez a megadott projektidőszakon belül.

## A `tls-status` parancs használata

A `tls-status` parancs a CLI ***digna*** rendszerében a Traffic Light System (TLS) státuszának lekérdezésére szolgál egy adott tábla esetében egy megadott dátumra vonatkozóan. A Traffic Light System betekintést nyújt az adatok állapotába és minőségébe, jelölve az esetleges problémákat vagy riasztásokat, amelyek figyelmet igényelhetnek.
  
### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyre a TLS státusz vonatkozik (kötelező).
- **TABLE_NAME**: A projektben található konkrét tábla, amelyhez a TLS státuszt lekérdezzük (kötelező).
- **DATE**: A dátum, amelyre a TLS státuszt lekérdezzük, általában %Y-%m-%d formátumban (kötelező).
  
### Példa
  
A `ProjectA` projekt `UserData` nevű táblájának TLS státuszának ellenőrzése 2024. július 1-jére:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ez a parancs segíti a felhasználókat az adatok minőségének monitorozásában és karbantartásában az előre meghatározott kritériumok alapján.

## A `list-projects` parancs használata
  
A `list-projects` parancs a CLI ***digna*** rendszerében az összes elérhető projekt listáját jeleníti meg a ***digna*** rendszerben.
  
### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos adminoknak és olyan felhasználóknak, akik több projektet kezelnek, mivel gyors áttekintést nyújt az elérhető projektekről a ***digna*** tárolóban.

## A `list-ds` parancs használata

A `list-ds` parancs a CLI ***digna*** rendszerében az adott projekt összes elérhető adatforrásának listáját jeleníti meg. A parancs hasznos az adatok elemzésére és kezelésére rendelkezésre álló adathalmazok áttekintéséhez a ***digna*** rendszerben.

### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentumok
- **PROJECT_NAME**: A projekt neve, amelyhez az adatforrások felsorolása tartozik (kötelező).
  
### Példa
  
Az összes adatforrás kilistázása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést ad a projektben elérhető adatforrásokról, segítve a hatékonyabb navigációt és az adatok kezelését.
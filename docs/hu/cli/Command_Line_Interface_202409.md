---
title: digna CLI Reference 2024.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.09. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
image: /assets/logo_square.png
---

# digna CLI Reference 2024.09
**2024-08-24**

---

## CLI Alapok

---

###   help

A --help opció információt nyújt az elérhető parancsokról és azok használatáról. Két fő módja van az opció használatának:

1. **Általános súgó megjelenítése:**
   
    Használja a --help-et közvetlenül a ***digna*** után  
   bash
   dignacli --help

3.  **Súgó egy konkrét parancshoz:**  
  
    Ha egy adott parancs részletes leírását szeretné megkapni, írja a parancs után a --help-et.
    Például, hogy segítséget kapjon az add-user parancshoz, futtassa:
     bash
     dignacli add-user --help
     

     ### output:
      
     - **Command Description:** Részletes leírást ad arról, mit csinál a parancs.  
     - **Syntax:** Megmutatja a pontos szintaxist, beleértve a kötelező és opcionális argumentumokat.  
     - **Options:** Felsorolja a parancshoz tartozó opciókat és azok magyarázatát.  
     - **Examples:** Példákat ad arra, hogyan érdemes a parancsot végrehajtani.

  
###   check-repo-connection

A check-repo-connection parancs a ***digna*** CLI eszközben arra szolgál, hogy tesztelje a kapcsolódást és hozzáférést egy megadott ***digna*** repository-hoz. Ez a parancs ellenőrzi, hogy a CLI képes-e kommunikálni a repository-val.
      
##### Command Usage
bash
dignacli check-repo-connection


Sikeres végrehajtás esetén a parancs megerősíti a kapcsolatot, és részleteket ad a repository-ról: Repository version, Host, Database és Schema.  
  
Ha a repository-hoz való kapcsolat nem sikerül, ellenőrizze a config.toml fájlt a helyes konfigurációs beállításokért.

###   version

A telepített *dignacli* verziójának lekérdezéséhez használja a --version opciót.  
  
#### Command Usage
bash
dignacli --version

  
#### Example Output
bash
dignacli version 2024.09


###   logging options
  
Alapértelmezésben a ***digna*** parancsok konzol kimenete minimalista. A legtöbb parancs lehetőséget ad további információk megjelenítésére a következő opciók használatával:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A “verbose” és a “debug” a részletességi szintet határozza meg, míg a “logfile” kapcsoló lehetővé teszi a kimenet fájlba történő átirányítását a konzol helyett.

## Felhasználókezelés

###   add-user
  
Az add-user parancs a ***digna*** CLI-ben új felhasználó hozzáadására szolgál a ***digna*** rendszerhez.
  
#### Command Usage
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Arguments

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Options

- --is_superuser, -su: Jelző arra, hogy az új felhasználó adminisztrátor legyen.
- --valid_until, -vu: A felhasználói fiók lejárati idejének beállítása a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fióknak nincs lejárati ideje.

#### Example

Új felhasználó hozzáadása jdoe felhasználónévvel, John Doe teljes névvel és password123 jelszóval:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Új felhasználó hozzáadása lejárati dátummal:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
A delete-user parancs a ***digna*** CLI-ben meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből.
  
##### Command Usage
bash
dignacli delete-user USER_NAME

  
#### Arguments
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen kötelező argumentum.

#### Example
bash
dignacli delete-user jdoe

  
A parancs végrehajtásakor a jdoe felhasználó törlődik a ***digna*** rendszerből; ezzel visszavonódik a hozzáférése és törlődnek a repository-ban hozzá kapcsolódó adatok és jogosultságok.

###   modify-user

A modify-user parancs a ***digna*** CLI-ben meglévő felhasználó adatainak frissítésére szolgál a ***digna*** rendszerben.

##### Command Usage
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Arguments
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Options  
  
- --is_superuser, -su: A felhasználó szuperfelhasználóvá tétele, magasabb jogosultságokkal. Ez a jelző nem igényel értéket.  
- --valid_until, -vu: A felhasználói fiók lejárati idejének beállítása a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók érvényes marad korlátlan ideig.  
  
#### Example
  
A jdoe felhasználó teljes nevének módosítása “Johnathan Doe”-ra és a szuperfelhasználóként való beállítása:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
A modify-user-pwd parancs a ***digna*** CLI-ben meglévő felhasználó jelszavának megváltoztatására szolgál a ***digna*** rendszerben.
  
##### Command Usage
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Arguments
  
- **USER_NAME**: A felhasználó felhasználóneve, akinek a jelszavát meg kell változtatni (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
#### Example
  
A jdoe felhasználó jelszavának megváltoztatása newpassword123-re:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

A list-users parancs a ***digna*** CLI-ben az összes regisztrált felhasználót listázza a ***digna*** rendszerben.

##### Command Usage

bash
dignacli list-users


A parancs végrehajtása összekapcsolódik a ***digna*** repository-val és felsorolja az összes felhasználót, megjelenítve az ID-t, felhasználónevet, teljes nevet, szuperfelhasználói státuszt és a lejárati időbélyegeket.

# Repository Kezelés

###   upgrade-repo
  
Az upgrade-repo parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ez a parancs elengedhetetlen a frissítések alkalmazásához vagy a repository infrastruktúrájának első beállításához.
  
#### Command Usage

bash
dignacli upgrade-repo [options]

  
#### Options
  
- --simulation-mode, -s: Ha engedélyezve van, ez az opció szimulációs módban futtatja a parancsot, ami kiírja azokat az SQL utasításokat, amelyek végrehajtásra kerülnének, de ténylegesen nem futtatja azokat. Hasznos a változtatások előnézetéhez anélkül, hogy módosítás történne a repository-ban.  

  
#### Example
  
A ***digna*** repository frissítéséhez futtathatja a parancsot opciók nélkül:
  
bash
dignacli upgrade-repo
  
A frissítés szimulációs módban történő futtatásához (az SQL utasítások megtekintéséhez, alkalmazás nélkül):
  
bash
dignacli upgrade-repo --simulation-mode

  
Ez a parancs kulcsfontosságú a ***digna*** rendszer karbantartásához, biztosítva, hogy az adatbázis sémája és a repository egyéb összetevői naprakészek legyenek a szoftver legújabb verziójával.

###   encrypt
  
Az encrypt parancs a ***digna*** CLI-ben jelszó titkosítására szolgál.
  
#### Command Usage
  
bash
dignacli encrypt <PASSWORD>

    
#### Arguments
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
#### Example
  
Egy jelszó titkosításához adja meg a jelszót argumentumként.  
Például a mypassword123 jelszó titkosításához használja:
bash
dignacli encrypt mypassword123

A parancs a megadott jelszó titkosított változatát adja vissza, amelyet biztonságos környezetben lehet használni. Ha a jelszó argumentum nincs megadva, a CLI hibaüzenetet jelenít meg a hiányzó argumentumról.

###   generate-key
  
A generate-key parancs egy Fernet kulcs generálására szolgál, amely elengedhetetlen a ***digna*** repository-ban tárolt jelszavak védelméhez.
  
#### Command Usage
bash
dignacli generate-key

  
## Adatkezelés

###   clean-up

A clean-up parancs a ***digna*** CLI-ben arra szolgál, hogy eltávolítsa a profilokat, predikciókat és a Traffic Light System adatait egy vagy több adatforrásról egy megadott projektben. Ez a parancs fontos az adatok életciklus-kezeléséhez, segít rendezett és hatékony adatkörnyezet fenntartásában az elavult vagy felesleges adatok törlésével.

#### Command Usage

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Annak a projektnek a neve, ahonnan az adatokat törölni kell (kötelező). Ha az argumentumban az all-projects kulcsszót használja, a ***digna*** végigiterál az összes létező projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az adatok törlésének kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adatok törlésének záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
#### Options
  
- --table-name, -tn: A clean-up művelet korlátozása egy adott tábla szintjére a projektben.
- --table-filter, -tf: Szűrés, amely csak azokat a táblákat érinti, amelyek nevében a megadott részstring szerepel.
- --timing, -tm: A clean-up folyamat időtartamának megjelenítése a befejezés után.
- --help: Súgó megjelenítése a clean-up parancshoz és kilépés.
  
#### Example
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Csak egy meghatározott, Table1 nevű táblából történő adatok eltávolítása:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Ez a parancs segít az adattárolás kezelésében és biztosítja, hogy a repository csak a releváns információkat tartalmazza.

###   inspect

Az inspect parancs a ***digna*** CLI-ben profilok, predikciók és a Traffic Light System adatok létrehozására szolgál egy vagy több adatforráshoz egy megadott projektben. Ez a parancs segít az adatok elemzésében és megfigyelésében egy meghatározott időszakra vonatkozóan.

#### Command Usage

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyen az adatokat ellenőrizni kell (kötelező). Ha az argumentumban az all-projects kulcsszót használja, a ***digna*** végigiterál az összes létező projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az adatellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adatellenőrzés záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
#### Options

- --table-name, -tn: Az ellenőrzés korlátozása egy adott táblára a projektben.
- --table-filter, -tf: Szűrés, hogy csak azok a táblák legyenek ellenőrizve, amelyek nevében a megadott részstring szerepel.
- --force-profile: Kényszeríti a profilok újragyűjtését. Alapértelmezett viselkedés: force-profile.
- --no-force-profile: Megakadályozza a profilok újragyűjtését.
- --force-prediction: Kényszeríti a predikciók újraszámítását. Alapértelmezett viselkedés: force-prediction.
- --no-force-prediction: Megakadályozza a predikciók újraszámítását.
- --force-alert-status: Kényszeríti az alert státuszok újraszámítását. Alapértelmezett viselkedés: force-alert-status.
- --no-force-alert-status: Megakadályozza az alert státuszok újraszámítását.
- --timing, -tm: Az ellenőrzés időtartamának megjelenítése a befejezés után.
- --alert-notification, -an: Értesítések küldése az előfizetett csatornákra.
  
#### Example
  
Adatok ellenőrzése a ProjectA projekt számára 2024. január 1-től 2024. január 31-ig:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Csak egy adott tábla ellenőrzése és a predikciók újraszámításának kényszerítése:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Ez a parancs hasznos a frissített profilok és predikciók generálásához, az adatintegritás nyomon követéséhez és az alert rendszerek kezeléséhez egy adott projekt időkeretén belül.

###   tls-status

A tls-status parancs a ***digna*** CLI-ben arra szolgál, hogy lekérdezze egy adott tábla Traffic Light System (TLS) státuszát egy projektben egy adott dátumra. A Traffic Light System betekintést nyújt az adatok állapotába és minőségébe, jelezve az esetleges problémákat vagy riasztásokat, amelyek figyelmet igényelhetnek.
  
#### Command Usage
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Arguments
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyre vonatkozóan a TLS státuszt lekérdezik (kötelező).
- **TABLE_NAME**: A projektben található konkrét tábla, amelyre a TLS státuszt igénylik (kötelező).
- **DATE**: Az a dátum, amelyre a TLS státuszt lekérdezik, általában %Y-%m-%d formátumban (kötelező).
  
#### Example
  
A ProjectA projekt UserData nevű táblájának TLS státuszának lekérdezése 2024. július 1-jére:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Ez a parancs segít a felhasználóknak az adatok minőségének nyomon követésében és karbantartásában, egyértelmű és akcióképes státuszjelentést biztosítva az előre definiált kritériumok alapján.

###   list-projects
  
A list-projects parancs a ***digna*** CLI-ben az összes elérhető projekt listázására szolgál a ***digna*** rendszerben.
  
#### Command Usage
  
bash
dignacli list-projects


Ez a parancs különösen hasznos az adminisztrátorok és a több projektet kezelő felhasználók számára, gyors áttekintést nyújtva az elérhető projektekről a ***digna*** repository-ban.

###   list-ds

A list-ds parancs a ***digna*** CLI-ben az összes elérhető adatforrás listázására szolgál egy megadott projekten belül. Ez a parancs hasznos az elemzésre és kezelésre rendelkezésre álló adatvagyon megismeréséhez a ***digna*** rendszerben.

#### Command Usage
  
bash
dignacli list-ds <PROJECT_NAME>


#### Arguments
- **PROJECT_NAME**: Annak a projektnek a neve, amelyre vonatkozóan az adatforrásokat listázzák (kötelező).
  
#### Example
  
Az összes adatforrás listázása a ProjectA nevű projektben:
  
bash
dignacli list-ds ProjectA

  
Ez a parancs áttekintést nyújt a projektben elérhető adatforrásokról, segítve a felhasználókat az adatok kezelésében és navigálásában.

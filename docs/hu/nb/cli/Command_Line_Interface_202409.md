---
title: digna CLI referencia 2024.09 – Parancsok & Példák | digna Dokumentáció
description: Teljes referencia a digna CLI 2024.09 kiadáshoz. Ismerje meg, hogyan kezelhet felhasználókat, repository-kat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect, tls-status és még több.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI referencia 2024.09
**2024-08-24**

---

## CLI alapok

---

###   help

A --help opció információt ad az elérhető parancsokról és azok használatáról. Két fő módja van ennek az opciónak a használatára:

1. **Általános súgó megjelenítése:**
   
    Használja a --help-et közvetlenül a ***digna*** kliens után.  
   bash
   dignacli --help

3.  **Súgó lekérése konkrét parancshoz:**  
  
    Részletes információkért egy adott parancsról, adja hozzá a --help-et a parancs után.
    Például, ha az add-user parancs súgóját szeretné megtekinteni, futtassa:
     bash
     dignacli add-user --help
     

     ### output:
      
     - **Parancs leírása:** Részletes leírást ad arról, hogy mit csinál a parancs.  
     - **Szin­taxis:** Pontosan megjeleníti a szintaxist, beleértve a kötelező és választható argumentumokat.  
     - **Opciók:** Felsorolja a parancshoz tartozó opciókat magyarázatokkal.  
     - **Példák:** Mutat példákat a parancs hatékony végrehajtására.

  
###   check-repo-connection

A check-repo-connection parancs a ***digna*** CLI-ben arra szolgál, hogy tesztelje egy megadott ***digna*** repository elérését és kapcsolódását. Ez a parancs biztosítja, hogy a CLI képes kommunikálni a repository-val.
      
##### Command Usage
bash
dignacli check-repo-connection


Sikeres futtatás esetén a parancs megerősíti a kapcsolatot, és részleteket ad a repository-ról: Repository version, Host, Database és Schema.  
  
Ha a repository-hoz való csatlakozás nem sikerül, ellenőrizze a config.toml fájlt a helyes konfigurációs beállításokért.

###   version

A telepített *dignacli* verzió ellenőrzéséhez használja a --version opciót.  
  
#### Command Usage
bash
dignacli --version

  
#### Example Output
bash
dignacli version 2024.09


###   logging options
  
Alapértelmezés szerint a ***digna*** parancsok konzol-kimenete minimális. A legtöbb parancs lehetőséget ad több információ megjelenítésére a következő opciók használatával:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A „verbose” és „debug” a részletességi szintet adják meg, míg a „logfile” kapcsoló lehetővé teszi, hogy a kimenetet fájlba irányítsa a konzol helyett.

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

- --is_superuser, -su: Jelző az új felhasználó admin jogosultságainak megadásához.
- --valid_until, -vu: Beállítja a felhasználói fiók lejárati dátumát az YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fióknak nincs lejárati dátuma.

#### Example

Új felhasználó hozzáadása jdoe felhasználónévvel, teljes névként John Doe és jelszóval password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Új felhasználó hozzáadása és a fiók lejárati dátumának beállítása:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
A delete-user parancs a ***digna*** CLI-ben egy meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből.
  
##### Command Usage
bash
dignacli delete-user USER_NAME

  
#### Arguments
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen szükséges argumentum.

#### Example
bash
dignacli delete-user jdoe

  
A parancs futtatásával a jdoe felhasználó eltávolításra kerül a ***digna*** rendszerből, és hozzáférése, valamint a repository-val kapcsolatos jogosultságai és kapcsolódó adatai megszűnnek.

###   modify-user

A modify-user parancs a ***digna*** CLI-ben meglévő felhasználó adatainak frissítésére szolgál a ***digna*** rendszerben.

##### Command Usage
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Arguments
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Options  
  
- --is_superuser, -su: Superuserré teszi a felhasználót, emelt jogosultságokat adva. Ez a jelző érték megadása nélkül alkalmazható.  
- --valid_until, -vu: Beállítja a felhasználói fiók lejárati dátumát az YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
#### Example
  
A jdoe felhasználó teljes nevének módosítása „Johnathan Doe”-ra és superuser jogosultság adása:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
A modify-user-pwd parancs a ***digna*** CLI-ben egy meglévő felhasználó jelszavának megváltoztatására szolgál a ***digna*** rendszerben.
  
##### Command Usage
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Arguments
  
- **USER_NAME**: A jelszót módosítandó felhasználó felhasználóneve (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
#### Example
  
A jdoe felhasználó jelszavának megváltoztatása newpassword123-ra:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

A list-users parancs a ***digna*** CLI-ben megjeleníti a rendszerben regisztrált összes felhasználó listáját.

##### Command Usage

bash
dignacli list-users


A parancs futtatásakor a ***digna*** CLI csatlakozik a ***digna*** repository-hoz, és megjeleníti az összes felhasználót azok azonosítójával, felhasználónevével, teljes nevével, superuser státuszával és lejárati idejével.

# Repository-kezelés

###   upgrade-repo
  
Az upgrade-repo parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ez a parancs elengedhetetlen a frissítések alkalmazásához vagy a repository infrastruktúra első beállításához.
  
#### Command Usage

bash
dignacli upgrade-repo [options]

  
#### Options
  
- --simulation-mode, -s: Amennyiben ez engedélyezve van, a parancs szimulációs módban fut, és kiírja azokat az SQL utasításokat, amelyeket futtatna, de nem hajtja végre azokat. Hasznos a változtatások előnézetéhez anélkül, hogy tényleges módosításokat végezne a repository-ban.  

  
#### Example
  
A ***digna*** repository frissítéséhez futtassa a parancsot opciók nélkül:
  
bash
dignacli upgrade-repo
  
A frissítés szimulációs módban történő futtatásához (az SQL utasítások megtekintéséhez anélkül, hogy alkalmaznák azokat):
  
bash
dignacli upgrade-repo --simulation-mode

  
Ez a parancs fontos a ***digna*** rendszer karbantartásához, és biztosítja, hogy az adatbázis-séma és a repository komponensei naprakészek legyenek a szoftver legújabb verziójának megfelelően.

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

A parancs visszaadja a megadott jelszó titkosított verzióját, amelyet aztán biztonságos célokra lehet használni. Ha a jelszó argumentum nincs megadva, a CLI hibaüzenetet fog jelezni a hiányzó argumentum miatt.

###   generate-key
  
A generate-key parancs Fernet-kulcs generálására szolgál, amely fontos a repository-ban tárolt jelszavak védelméhez.
  
#### Command Usage
bash
dignacli generate-key

  
## Adatfeldolgozás

###   clean-up

A clean-up parancs a ***digna*** CLI-ben profilok, predikciók és adatok eltávolítására szolgál a forgalmi lámpa rendszerből egy vagy több adatkforráshoz egy adott projekten belül. Ez a parancs fontos az adatok életciklus-kezeléséhez, és segít rendezett, hatékony adathalmazt fenntartani az elavult vagy felesleges adatok törlésével.

#### Command Usage

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Annak a projektnek a neve, ahonnan az adatokat törölni kell (kötelező). Ha az all-projects kulcsszót használja ebben az argumentumban, a ***digna*** az összes meglévő projekten végigiterál és alkalmazza a parancsot.
- **FROM_DATE**: Az adat-tisztítás kezdő dátuma és időpontja. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adat-tisztítás záró dátuma és időpontja, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Options
  
- --table-name, -tn: Korlátozza a clean-up műveletet egy adott táblára a projektben.
- --table-filter, -tf: Szűr a táblákra, és csak azokat érinti, amelyek tartalmazzák a megadott alstringet a nevükben.
- --timing, -tm: A clean-up folyamat futási idejét jeleníti meg a befejezés után.
- --help: Megjeleníti a clean-up parancs súgóját és kilép.
  
#### Example
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Adatok eltávolítása csak egy adott, Table1 nevű táblából:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Ez a parancs segít az adattárolás kezelésében és biztosítja, hogy a repository csak releváns információkat tartalmazzon.

###   inspect

Az inspect parancs a ***digna*** CLI-ben profilok, predikciók és forgalmi lámpa rendszerhez szükséges adatok létrehozására szolgál egy vagy több adatforráshoz egy adott projektben. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakon belül.

#### Command Usage

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelynek adatait vizsgálni kell (kötelező). Ha az all-projects kulcsszót használja ebben az argumentumban, a ***digna*** az összes meglévő projekten végigiterál és alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdő dátuma és időpontja. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záró dátuma és időpontja, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Options

- --table-name, -tn: Korlátozza az ellenőrzést egy adott táblára a projektben.
- --table-filter, -tf: Csak azokat a táblákat vizsgálja, amelyek tartalmazzák a megadott alstringet a nevükben.
- --force-profile: Kényszeríti a profilok újbóli gyűjtését. Alapértelmezett: force-profile.
- --no-force-profile: Megakadályozza a profilok újbóli gyűjtését.
- --force-prediction: Kényszeríti a predikciók újraszámítását. Alapértelmezett: force-prediction.
- --no-force-prediction: Megakadályozza a predikciók újraszámítását.
- --force-alert-status: Kényszeríti az értesítési státusz újraszámítását. Alapértelmezett: force-alert-status.
- --no-force-alert-status: Megakadályozza az értesítési státusz újraszámítását.
- --timing, -tm: Megjeleníti az ellenőrzés időtartamát a befejezés után.
- --alert-notification, -an: Értesítéseket küld a feliratkozott csatornákra.
  
#### Example
  
Adatok ellenőrzése a ProjectA projekt számára 2024. január 1-től 2024. január 31-ig:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Csak egy adott tábla ellenőrzése és a predikciók újraszámolásának kényszerítése:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Ez a parancs hasznos friss profilok és predikciók generálásához, az adatintegritás monitorozásához és az értesítési rendszerek kezeléséhez egy adott projektidőszakon belül.

###   tls-status

A tls-status parancs a ***digna*** CLI-ben arra szolgál, hogy lekérdezze a Forgalmi Lámpa Rendszer (TLS) státuszát egy adott tábla számára egy projekten belül egy adott dátumra. A Forgalmi Lámpa Rendszer betekintést nyújt az adatok minőségébe és állapotába, és jelzi az esetleges problémákat vagy riasztásokat, amelyek figyelmet igényelhetnek.
  
#### Command Usage
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Arguments
  
- **PROJECT_NAME**: A projekt neve, amelyre a TLS státuszt lekérdezik (kötelező).
- **TABLE_NAME**: Az adott tábla a projektben, amelyre a TLS státusz vonatkozik (kötelező).
- **DATE**: Az a dátum, amelyre a TLS státuszt lekérdezik, általában %Y-%m-%d formátumban (kötelező).
  
#### Example
  
A UserData nevű tábla TLS státuszának ellenőrzése a ProjectA projektben 2024. július 1-jén:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Ez a parancs segít a felhasználóknak az adatok minőségének nyomon követésében és fenntartásában azzal, hogy egyértelmű és gyakorlati státusz-jelentést ad előre definiált kritériumok alapján.

###   list-projects
  
A list-projects parancs a ***digna*** CLI-ben az elérhető projektek listázására szolgál a ***digna*** rendszerben.
  
#### Command Usage
  
bash
dignacli list-projects


Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára, és gyors áttekintést nyújt a repository-ban található elérhető projektekről.

###   list-ds

A list-ds parancs a ***digna*** CLI-ben az adott projektben elérhető összes adatforrás listázására szolgál. Ez a parancs hasznos áttekintést ad az elemzésre és kezelésre rendelkezésre álló adaterőforrásokról a ***digna*** rendszerben.

#### Command Usage
  
bash
dignacli list-ds <PROJECT_NAME>


#### Arguments
- **PROJECT_NAME**: A projekt neve, amelyre vonatkozóan az adatforrásokat listázni kell (kötelező).
  
#### Example
  
Az összes adatforrás listázása a ProjectA nevű projektben:
  
bash
dignacli list-ds ProjectA

  
Ez a parancs áttekintést ad a projektben elérhető adatforrásokról, és segít hatékonyabban navigálni és kezelni az adatközpontot.
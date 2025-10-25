---
title: digna CLI Kézikönyv 2024.09 – Parancsok és Példák | digna Dokumentáció
description: Teljes kézikönyv a digna CLI 2024.09 kiadásához. Tudja meg, hogyan kezelhet felhasználókat, tárolókat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect, tls-status és mások.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI Kézikönyv 2024.09
**2024-08-24**

---

## CLI alapok

---

###   help

A --help opció információt ad az elérhető parancsokról és azok használatáról. Két fő módja van ennek az opció használatának:

1. **Általános súgó megjelenítése:**
   
    Használja a --help-et közvetlenül a ***digna*** kulcsszó után  
bash
dignacli --help

2.  **Specifikus parancs súgó megtekintése:**  
  
    A konkrét parancs részletes információjához adja hozzá a parancshoz a --help opciót.
    Például az add-user parancs súgójának megtekintéséhez futtassa:
bash
dignacli add-user --help
     

     ### kimenet:
      
     - **Parancsleírás:** Részletes leírás arról, mit végez a parancs.  
     - **Szintaxis:** Megmutatja a pontos szintaxist, beleértve a kötelező és választható argumentumokat.  
     - **Opciók:** A parancsra jellemző opciók listája magyarázatokkal.  
     - **Példák:** Példák a parancs helyes használatára.

  
###   check-repo-connection

A check-repo-connection parancs a ***digna*** CLI eszközben egy olyan segédprogram, amely a megadott digna tárolóhoz (repository) való csatlakozást és hozzáférést ellenőrzi. A parancs biztosítja, hogy a CLI képes kommunikálni a tárolóval.
      
##### A parancs használata
bash
dignacli check-repo-connection


Sikeres végrehajtás után a parancs megerősítést ad a kapcsolatról, valamint részleteket a tárolóról: tároló verzió, host, adatbázis és séma.  
  
Ha a tárolóhoz való csatlakozás sikertelen, ellenőrizze a config.toml fájlt a beállítások helyessége érdekében.

###   version

A telepített *dignacli* verzió ellenőrzéséhez használja a --version opciót.  
  
#### A parancs használata
bash
dignacli --version

  
#### Példa kimenet
bash
dignacli version 2024.09


###   naplózási beállítások
  
Alapértelmezés szerint a ***digna*** parancsok konzolkimenete minimális. A legtöbb parancs további információt adhat ki az alábbi opciók használatával:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
A „verbose” és „debug” a részletességi szintet határozzák meg, míg a „logfile” opció lehetővé teszi a kimenet fájlba irányítását a konzol helyett.

## Felhasználók kezelése

###   add-user
  
Az add-user parancs a ***digna*** CLI-ben új felhasználó hozzáadására szolgál a ***digna*** rendszerbe.
  
#### A parancs használata
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumentumok

- **USER_NAME**: Az új fiók felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- --is_superuser, -su: Megjelöli az új felhasználót adminisztrátornak.
- --valid_until, -vu: Beállítja a fiók érvényességének végét YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a lejárat nincs beállítva.

#### Példa

Új felhasználó hozzáadása jdoe névvel, teljes névként John Doe és jelszóval password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Új felhasználó hozzáadása és a fiók lejárati idejének megadása:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
A delete-user parancs a ***digna*** CLI-ben meglévő felhasználó törlésére szolgál a ***digna*** rendszerből.
  
##### A parancs használata
bash
dignacli delete-user USER_NAME

  
#### Argumentumok
- **USER_NAME**: A törlendő felhasználó neve (kötelező). Ez az egyetlen szükséges argumentum a parancshoz.

#### Példa
bash
dignacli delete-user jdoe

  
A parancs végrehajtásával a jdoe felhasználó törlődik a ***digna*** rendszerből, visszavonódik a hozzáférése, és eltávolításra kerülnek a tárolóhoz kapcsolódó adatok és jogosultságok.

###   modify-user

A modify-user parancs a ***digna*** CLI-ben meglévő felhasználó adatainak frissítésére szolgál a ***digna*** rendszerben.

##### A parancs használata
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó neve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Opciók  
  
- --is_superuser, -su: Beállítja a felhasználót szuperfelhasználónak, magasabb jogosultságokkal. Ez a jelző érték nélküli kapcsoló.  
- --valid_until, -vu: Beállítja a fiók lejárati dátumát YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
#### Példa
  
A jdoe felhasználó teljes nevének módosítása „Johnathan Doe”-ra és szuperfelhasználóvá tétele:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
A modify-user-pwd parancs a ***digna*** CLI-ben egy meglévő felhasználó jelszavának megváltoztatására szolgál a ***digna*** rendszerben.
  
##### A parancs használata
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumentumok
  
- **USER_NAME**: A jelszót módosítandó felhasználó neve (kötelező).
- **USER_PWD**: Az új jelszó (kötelező).
  
#### Példa
  
A jdoe felhasználó jelszavának megváltoztatása newpassword123-re:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

A list-users parancs a ***digna*** CLI-ben a rendszerben regisztrált összes felhasználó listázására szolgál.

##### A parancs használata

bash
dignacli list-users


A parancs végrehajtásakor a ***digna*** CLI csatlakozik a ***digna*** tárolóhoz, és kilistázza az összes felhasználót, megjelenítve az ID-jüket, felhasználónevüket, teljes nevüket, szuperfelhasználó státuszukat és a lejárati idő bélyegét.

# Tároló (repository) kezelése

###   upgrade-repo
  
Az upgrade-repo parancs a ***digna*** CLI-ben a tároló frissítésére vagy inicializálására szolgál. Ez a parancs szükséges a frissítések alkalmazásához vagy a tároló infrastruktúrájának első beállításához.
  
#### A parancs használata

bash
dignacli upgrade-repo [options]

  
#### Opciók
  
- --simulation-mode, -s: Ha engedélyezve van, a parancs szimulációs módban fut — kiírja azokat az SQL-utasításokat, amelyek végrehajtásra kerülnének, de ténylegesen nem hajtja végre őket. Hasznos a változtatások előzetes megtekintéséhez a tároló módosítása nélkül.  

  
#### Példa
  
A digna tároló frissítéséhez futtassa a parancsot opciók nélkül:
  
bash
dignacli upgrade-repo
  
A frissítés szimulációs módban történő futtatásához (az SQL-utasítások megtekintéséhez alkalmazás nélkül):
  
bash
dignacli upgrade-repo --simulation-mode

  
Ez a parancs fontos a ***digna*** rendszer karbantartásához, biztosítva az adatbázis séma és a tároló egyéb komponenseinek naprakészségét a legújabb szoftververzió szerint.

###   encrypt
  
Az encrypt parancs a ***digna*** CLI-ben egy jelszó titkosítására szolgál.
  
#### A parancs használata
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
#### Példa
  
A jelszó titkosításához adja meg argumentumként.   
Például a mypassword123 jelszó titkosításához használja:
bash
dignacli encrypt mypassword123

A parancs a megadott jelszó titkosított változatát adja vissza, amelyet biztonságos kontextusokban felhasználhat. Ha a jelszó argumentum nem kerül megadásra, a CLI hibát jelez a hiányzó argumentum miatt.

###   generate-key
  
A generate-key parancs Fernet-kulcs generálására szolgál, amely szükséges a tárolóban (***digna***) tárolt jelszavak védelméhez.
  
#### A parancs használata
bash
dignacli generate-key

  
## Adatkezelés

###   clean-up

A clean-up parancs a ***digna*** CLI-ben profilok, előrejelzések és a forgalmi lámpa rendszer (Traffic Light System) adatok törlésére szolgál egy vagy több adatforrás esetén a megadott projektben. Ez a parancs fontos az adatok életciklusának kezeléséhez, segítve a rendezettség és hatékonyság fenntartását az elavult vagy nem szükséges adatok eltávolításával.

#### A parancs használata

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, ahonnan az adatokat törölni kell (kötelező). Az all-projects kulcsszó használata ebben az argumentumban azt utasítja a ***digna***-t, hogy iteráljon az összes elérhető projekten és alkalmazza a parancsot mindegyikre.
- **FROM_DATE**: Az adat törlésének kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adat törlésének befejező dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- --table-name, -tn: A törlést korlátozza egy konkrét táblára a projektben.
- --table-filter, -tf: A táblákat szűri, csak azokat törli, amelyek neve tartalmazza a megadott alstringet.
- --timing, -tm: A törlési folyamat időtartamát mutatja a befejezés után.
- --help: Megjeleníti a clean-up parancs súgóját és kilép.
  
#### Példa
  
Adatok törlése a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Adatok törlése csak egy konkrét Table1 nevű táblából:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Ez a parancs segít az adatok megtartásának kezelésében, biztosítva, hogy a tárolóban csak releváns információk maradjanak.

###   inspect

Az inspect parancs a ***digna*** CLI-ben profilok, előrejelzések és a forgalmi lámpa rendszer (Traffic Light System) adatok létrehozására szolgál egy vagy több adatforráshoz a megadott projektben. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakra vonatkozóan.

#### A parancs használata

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyhez az adatok vizsgálatát el kell végezni (kötelező). Az all-projects kulcsszó használata azt utasítja a ***digna***-t, hogy iteráljon az összes elérhető projekten és alkalmazza a parancsot mindegyikre.
- **FROM_DATE**: Az adatvizsgálat kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adatvizsgálat befejező dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
#### Opciók

- --table-name, -tn: Az inspectet korlátozza egy konkrét táblára a projektben.
- --table-filter, -tf: A táblákat szűri, csak azokat vizsgálja, amelyek neve tartalmazza a megadott alstringet.
- --force-profile: Kényszeríti a profilok újbóli összegyűjtését. Alapértelmezés szerint a force-profile engedélyezve van.
- --no-force-profile: Megakadályozza a profilok újbóli összegyűjtését.
- --force-prediction: Kényszeríti az előrejelzések újbóli számítását. Alapértelmezés szerint a force-prediction engedélyezve van.
- --no-force-prediction: Megakadályozza az előrejelzések újbóli számítását.
- --force-alert-status: Kényszeríti a riasztási állapotok újbóli számítását. Alapértelmezés szerint a force-alert-status engedélyezve van.
- --no-force-alert-status: Megakadályozza a riasztási állapotok újbóli számítását.
- --timing, -tm: Az inspect folyamat időtartamát mutatja a befejezés után.
- --alert-notification, -an: Riasztási értesítéseket küld a feliratkozott csatornákra.
  
#### Példa
  
A ProjectA projekt adatainak vizsgálata 2024. január 1-től 2024. január 31-ig:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Csak egy konkrét tábla vizsgálata és az előrejelzések kényszerített újraszámítása:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Ez a parancs hasznos frissített profilok és előrejelzések generálásához, az adatok integritásának monitorozásához és a riasztási rendszer kezeléséhez a projekt megadott időtartamában.

###   tls-status

A tls-status parancs a ***digna*** CLI-ben a Traffic Light System (TLS) állapotának lekérésére szolgál egy adott tábla esetén egy megadott dátumra. A forgalmi lámpa rendszer áttekintést ad az adatok állapotáról és minőségéről, jelezve a kezelendő problémákat vagy riasztásokat.
  
#### A parancs használata
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyhez a TLS állapotát lekérdezik (kötelező).
- **TABLE_NAME**: A projektben szereplő konkrét tábla, amelynek TLS állapota szükséges (kötelező).
- **DATE**: Az a dátum, amelyre a TLS állapotát lekérdezik, általában %Y-%m-%d formátumban (kötelező).
  
#### Példa
  
A ProjectA projekt UserData táblájának TLS állapotának ellenőrzése 2024. július 1-jére:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Ez a parancs segít a felhasználóknak az adatok nyomon követésében és karbantartásában, érthető és gyakorlatias jelentést adva az állapotról előre definiált kritériumok alapján.

###   list-projects
  
A list-projects parancs a ***digna*** CLI-ben az összes elérhető projekt listázására szolgál a ***digna*** rendszerben.
  
#### A parancs használata
  
bash
dignacli list-projects


Ez a parancs különösen hasznos rendszergazdák és többszörös projektek kezelésével foglalkozó felhasználók számára, gyors áttekintést adva a tárolóban elérhető projektekről.

###   list-ds

A list-ds parancs a ***digna*** CLI-ben az adott projekt összes elérhető adatforrásának listázására szolgál. Ez a parancs hasznos az elemzésre és kezelésre rendelkezésre álló adatok áttekintéséhez a ***digna*** rendszerben.

#### A parancs használata
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelyhez az adatforrások felsorolása szükséges (kötelező).
  
#### Példa
  
Az összes adatforrás felsorolása a ProjectA nevű projektben:
  
bash
dignacli list-ds ProjectA

  
Ez a parancs áttekintést nyújt a projektben elérhető adatforrásokról, segítve a tájékozódást és az adatkörnyezet hatékonyabb kezelését.
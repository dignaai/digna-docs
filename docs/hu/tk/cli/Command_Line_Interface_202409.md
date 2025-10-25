---
title: digna CLI Referencia 2024.09 – Parancsok és Példák | digna Dokumentáció
description: Teljes referencia a digna CLI 2024.09 verzióhoz. Ismerje meg, hogyan kezelje a felhasználókat, repókat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect, tls-status és még sok más.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI Referencia 2024.09
**2024-08-24**

---

## CLI Alapok

---

###   help

--help opció információt nyújt az elérhető parancsokról és azok használatáról. Ennek az opciónak két fő használati módja van:

1. **Általános segítség megtekintése:**
   
    Használja a --help-et közvetlenül a ***digna*** parancs után  
   bash
   dignacli --help

3.  **Egy adott parancs súgója:**  
  
    Ha egy konkrét parancsról szeretne részletes információt, adja hozzá a --help-et ahhoz a parancshoz.  
    Például, ha az add-user parancs súgóját szeretné megtekinteni, futtassa a következőt:
     bash
     dignacli add-user --help
     

     ### kimenet:
      
     - **Parancs leírása:** Részletesen elmagyarázza, mit csinál a parancs.  
     - **Szin­taxis:** Megjeleníti a teljes szintaxist, beleértve a kötelező és opcionális argumentumokat.  
     - **Opciók:** Felsorolja a parancsra vonatkozó opciókat és azok leírását.  
     - **Példák:** Példákat ad arra, hogyan kell hatékonyan futtatni a parancsot.

  
###   check-repo-connection

A check-repo-connection parancs a ***digna*** CLI-ben található segédprogram, amely egy adott ***digna*** repóhoz való csatlakozást és hozzáférést teszteli. Ez a parancs ellenőrzi, hogy a CLI képes-e kommunikálni a repóval.
      
##### Parancs használata
bash
dignacli check-repo-connection


Sikeres végrehajtás esetén a parancs visszaigazolja a kapcsolatot és megjeleníti a repóhoz kapcsolódó információkat: Repository version, Host, Database és Schema.  
  
Ha a repóhoz való csatlakozás nem sikerül, ellenőrizze a config.toml fájl helyes konfigurációs beállításait.

###   version

A telepített *dignacli* verzió ellenőrzéséhez használja a --version opciót.  
  
#### Parancs használata
bash
dignacli --version

  
#### Példa kimenet
bash
dignacli version 2024.09


###   logging options
  
Alapértelmezés szerint a ***digna*** parancsok konzol kimenete minimalista. A legtöbb parancs támogat további információk megjelenítését a következő opciók használatával:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A "verbose" és a "debug" a részletességi szintet határozza meg, míg a "logfile" opció lehetővé teszi, hogy a kimenetet a konzol helyett egy fájlba irányítsa.

## Felhasználókezelés

###   add-user
  
Az add-user parancsot a ***digna*** CLI-ben új felhasználó hozzáadására használják a ***digna*** rendszerhez.
  
#### Parancs használata
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

#### Opciók

- --is_superuser, -su: Jelző az új felhasználó adminisztrátorrá (superuser) tételezéséhez.
- --valid_until, -vu: A felhasználói fiók lejárati dátuma a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fióknak nincs lejárati ideje.

#### Példa

Új felhasználó hozzáadása jdoe felhasználónévvel, John Doe teljes névvel és password123 jelszóval:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Egy felhasználó hozzáadása és a fiók lejárati idejének beállítása:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
A delete-user parancs a ***digna*** CLI-ben meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből.
  
##### Parancs használata
bash
dignacli delete-user USER_NAME

  
#### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen szükséges argumentum.

#### Példa
bash
dignacli delete-user jdoe

  
A parancs futtatása után a jdoe felhasználó eltávolításra kerül a ***digna*** rendszerből, a hozzáférése megszűnik, és a repóban található kapcsolódó adatok és jogosultságok törlődnek.

###   modify-user

A modify-user parancs a ***digna*** CLI-ben egy meglévő felhasználó adatainak frissítésére szolgál.

##### Parancs használata
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumentumok
  
- **USER_NAME**: A felhasználó felhasználóneve, amelynek adatait módosítani kell (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
#### Opciók  
  
- --is_superuser, -su: Beállítja a felhasználót superuserként, emelt jogosultságokat biztosítva. Ennek a jelzőnek nincs értéke.  
- --valid_until, -vu: A felhasználói fiók lejárati dátuma a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes.  
  
#### Példa
  
A jdoe felhasználó teljes nevének "Johnathan Doe"-ra történő módosítása és superuser státusz adása:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
A modify-user-pwd parancs a ***digna*** CLI-ben egy meglévő felhasználó jelszavának megváltoztatására szolgál.
  
##### Parancs használata
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumentumok
  
- **USER_NAME**: A jelszavát módosítandó felhasználó felhasználóneve (kötelező).
- **USER_PWD**: Az új jelszó a felhasználó számára (kötelező).
  
#### Példa
  
A jdoe felhasználó jelszavának newpassword123-ra módosítása:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

A list-users parancs kilistázza a ***digna*** rendszerben regisztrált összes felhasználót a ***digna*** CLI-ben.

##### Parancs használata

bash
dignacli list-users


Ennek a parancsnak a futtatása a ***digna*** CLI-ben csatlakozik a ***digna*** repóhoz, és felsorolja az összes felhasználót, megjelenítve azok ID-ját, felhasználónevét, teljes nevét, superuser státuszát és a lejárati időbélyegeket.

# Repókezelés

###   upgrade-repo
  
Az upgrade-repo parancs a ***digna*** CLI-ben a ***digna*** repó frissítésére vagy inicializálására szolgál. Ezt a parancsot a frissítések alkalmazásához vagy a repó infrastruktúrájának első beállításához használják.
  
#### Parancs használata

bash
dignacli upgrade-repo [options]

  
#### Opciók
  
- --simulation-mode, -s: Ha engedélyezve van, a parancs szimulációs módban fut; kiírja a végrehajtandó SQL utasításokat, de nem futtatja azokat. Ez hasznos a változások előnézetéhez anélkül, hogy módosítás történne a repóban.  

  
#### Példa
  
A ***digna*** repó frissítése opciók nélkül:
  
bash
dignacli upgrade-repo
  
A frissítés szimulációs módban történő futtatása (SQL utasítások alkalmazása nélküli megtekintés):
  
bash
dignacli upgrade-repo --simulation-mode

  
Ez a parancs kritikus fontosságú a ***digna*** rendszer karbantartásában, mert biztosítja az adatbázis sémájának és más repóösszetevőknek a szoftver legújabb verziójával való kompatibilitását és naprakész állapotát.

###   encrypt
  
Az encrypt parancs a ***digna*** CLI-ben egy jelszó titkosítására szolgál.
  
#### Parancs használata
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
#### Példa
  
Egy jelszó titkosításához adja meg a jelszót argumentumként.   
Például a mypassword123 titkosítása:
bash
dignacli encrypt mypassword123

A parancs visszaadja a megadott jelszó titkosított változatát; ezt a kimenetet később biztonságos környezetben felhasználhatja. Ha nem ad meg jelszóargumentumot, a CLI hibaüzenetet jelez a hiányzó argumentumról.

###   generate-key
  
A generate-key parancs egy Fernet kulcsot hoz létre, amely szükséges a repóban tárolt jelszavak biztonságához a ***digna*** rendszerben.
  
#### Parancs használata
bash
dignacli generate-key

  
## Adatkezelés

###   clean-up

A clean-up parancs a ***digna*** CLI-ben egy adott projekt alatt lévő egy vagy több adatforrás profiljainak, előrejelzéseinek és a Forgalmi lámpák rendszerének (TLS) adatait törli. Ez a parancs fontos az adatok életciklus-kezeléséhez, és segít a régi vagy felesleges adatok eltávolításában, így rendezett és hatékony adatkörnyezetet biztosítva.

#### Parancs használata

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelyből az adatokat törölni kell (kötelező). Ha ebben az argumentumban az all-projects kulcsszót használja, a ***digna*** végigiterál az összes elérhető projekten és alkalmazza a parancsot.
- **FROM_DATE**: A törlés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: A törlés befejezésének dátuma és ideje; ugyanazokat a formátumokat használja, mint a FROM_DATE (kötelező).
  
#### Opciók
  
- --table-name, -tn: Korlátozza a tisztítást egy adott táblára a projekten belül.
- --table-filter, -tf: Szűrőt alkalmaz a táblákra, amelyek neve tartalmazza a megadott részstringet.
- --timing, -tm: Megjeleníti az eltávolítási művelet befejeztével eltelt időt.
- --help: Megjeleníti a clean-up parancs súgóját, majd kilép.
  
#### Példa
  
ProjectA projektből az 2023. január 1. és 2023. június 30. közötti adatok eltávolítása:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Csak a Table1 nevű konkrét táblából történő adateltávolításhoz:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Ez a parancs segít az adattárolás kezelésében, és biztosítja, hogy a repó csak a releváns információkat tartalmazza.

###   inspect

Az inspect parancs a ***digna*** CLI-ben egy adott projekt alatt lévő egy vagy több adatforrás profiljainak, előrejelzéseinek és a Forgalmi lámpák rendszerének (TLS) adatainak létrehozására szolgál. Ez a parancs segíti az adatok adott időszak alatti elemzését és monitorozását.

#### Parancs használata

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelynek adatait vizsgálni kell (kötelező). Ha itt az all-projects kulcsszót adja meg, a ***digna*** végigiterál az összes elérhető projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az elemzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az elemzés befejezésének dátuma és ideje; ugyanazokat a formátumokat használja, mint a FROM_DATE (kötelező).
  
#### Opciók

- --table-name, -tn: Korlátozza az elemzést egy adott táblára a projekten belül.
- --table-filter, -tf: Szűrőt alkalmaz olyan táblákra, amelyek neve tartalmazza a megadott részstringet.
- --force-profile: Kényszeríti a profilok újbóli gyűjtését. Alapértelmezés szerint force-profile aktív.
- --no-force-profile: Megakadályozza a profilok újbóli gyűjtését.
- --force-prediction: Kényszeríti a predikciók újbóli kiszámítását. Alapértelmezés szerint force-prediction aktív.
- --no-force-prediction: Megakadályozza a predikciók újbóli kiszámítását.
- --force-alert-status: Kényszeríti a riasztási állapotok újbóli kiszámítását. Alapértelmezés szerint force-alert-status aktív.
- --no-force-alert-status: Megakadályozza a riasztási állapotok újbóli kiszámítását.
- --timing, -tm: Megjeleníti az elemzési művelet befejeztével eltelt időt.
- --alert-notification, -an: Riasztási értesítéseket küld a feliratkozott csatornákra.
  
#### Példa
  
ProjectA projekt 2024. január 1. és 2024. január 31. közötti adatainak vizsgálata:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Csak egy adott tábla vizsgálata és a predikciók újbóli kiszámításának kényszerítése:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Ez a parancs hasznos frissített profilok és predikciók létrehozására, az adatintegritás monitorozására és az adott projekt időszakára vonatkozó riasztási rendszerek kezelésére.

###   tls-status

A tls-status parancs a ***digna*** CLI-ben egy adott projekt alatt lévő tábla egy adott időpontbeli Forgalmi lámpák rendszerére (TLS) vonatkozó állapotának lekérdezésére szolgál. A Forgalmi lámpák rendszere a adat egészségére és minőségére vonatkozó figyelmeztető vagy kiemelendő állapotokat jelzi.
  
#### Parancs használata
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelynek TLS állapotát lekérdezik (kötelező).
- **TABLE_NAME**: A projektben található, TLS állapot lekérdezéséhez szükséges tábla (kötelező).
- **DATE**: Az a dátum, amelyre a TLS állapotot lekérdezik, általában %Y-%m-%d formátumban (kötelező).
  
#### Példa
  
A ProjectA projektben található UserData tábla 2024. július 1-jei TLS állapotának ellenőrzése:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Ez a parancs előre definiált kritériumok alapján világos és gyakorlatias állapotjelentést nyújt, segítve a felhasználókat az adatok minőségének nyomon követésében és fenntartásában.

###   list-projects
  
A list-projects parancs kilistázza az összes elérhető projektet a ***digna*** CLI-ben.
  
#### Parancs használata
  
bash
dignacli list-projects


Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára; gyors áttekintést ad a ***digna*** repóban elérhető projektekről.

###   list-ds

A list-ds parancs kilistázza egy adott projekt alatt található összes elérhető adatforrást a ***digna*** CLI-ben. Ez a parancs hasznos a ***digna*** rendszerben található elemzésre és kezelésre rendelkezésre álló adatvagyon megismeréséhez.

#### Parancs használata
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumentumok
- **PROJECT_NAME**: Az a projekt, amelynek adatforrásait listázni szeretnék (kötelező).
  
#### Példa
  
Az összes adatforrás listázása a ProjectA projektben:
  
bash
dignacli list-ds ProjectA

  
Ez a parancs áttekintést nyújt egy projekt meglévő adatforrásairól, segítve a felhasználókat az adatkörnyezet hatékonyabb kezelésében.
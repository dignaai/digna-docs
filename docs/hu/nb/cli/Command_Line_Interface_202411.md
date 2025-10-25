---
title: digna CLI-referencia 2024.11 – Parancsok és példák | digna-dokumentáció
description: Teljes referencia a digna CLI kiadásához 2024.11. Ismerje meg, hogyan kezelheti a felhasználókat, repókat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect, tls-status és továbbiak.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI-referencia 2024.11
**2024-11-03**

Ez az oldal dokumentálja a ***digna*** CLI **2024.11** kiadásában elérhető parancsok teljes készletét, beleértve használati példákat és opciókat.


---
## CLI alapok

---

## A `--help` opció használata

A `--help` opció információt ad az elérhető parancsokról és azok használatáról. Két fő módja van az opció használatának:

1. **Általános segítség megjelenítése:**
   
    Használja a --help-et közvetlenül a ***digna*** kulcsszó után  
   ```bash
   dignacli --help
   ```

2.  **Segítség egy konkrét parancshoz:**  
  
    Részletes információkért egy adott parancsról adja meg a `--help`-et a parancs után.  
    Például az `add-user` parancs súgójának lekéréséhez futtassa:
     ```bash
     dignacli add-user --help
     ```

     ### Kimenet:
      
     - **Parancs leírása:** Részletesen elmagyarázza, mit csinál a parancs.  
     - **Szintaxis:** Megjeleníti a pontos szintaxist, beleértve a kötelező és választható argumentumokat.  
     - **Opciók:** Felsorolja az adott parancshoz tartozó opciókat és azok magyarázatát.  
     - **Példák:** Mutat példákat a parancs hatékony használatára.

  
## A `check-repo-connection` parancs használata

A check-repo-connection parancs a ***digna*** CLI-ben arra szolgál, hogy tesztelje a csatlakozást és hozzáférést egy megadott ***digna***-repositoryhoz. Ez a parancs biztosítja, hogy a CLI képes legyen kommunikálni a repository-val.
      
### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres futtatás esetén a parancs megerősíti a csatlakozást, és részleteket ad a repository-ról: Repository-verzió, Host, Database és Schema.  
  
Ha a repository-hoz való csatlakozás nem sikerül, ellenőrizze a config.toml fájlt a helyes konfigurációs beállításokért.

## A `--version` parancs használata

Az *dignacli* telepített verziójának lekérdezéséhez használja a --version opciót.  
  
### Parancs használata
```bash
dignacli --version
```
  
### Példa kimenet
```bash
dignacli version 2024.11
```

## Naplózási opciók használata
  
Alapértelmezés szerint a ***digna*** parancsok konzolra írt kimenete minimalista. A legtöbb parancs lehetőséget ad további információk megadására a következő opciók használatával:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
A “verbose” és “debug” a részletességi szintet határozzák meg, míg a “logfile” opció lehetővé teszi a kimenet fájlba való átirányítását a konzol helyett.

# Felhasználókezelés

## Az `add-user` parancs használata
  
Az add-user parancs a ***digna*** CLI-ben új felhasználó hozzáadására szolgál a ***digna*** rendszerhez.
  
### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

### Opciók

- `--is_superuser`, `-su`: Jelző az új felhasználó rendszergazdává (superuser) jelöléséhez.
- `--valid_until`, `-vu`: Lejárati dátum beállítása a felhasználói fiókra a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fiók nem jár le.

### Példa

Új felhasználó hozzáadása `jdoe` felhasználónévvel, teljes névvel `John Doe` és jelszóval `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Új felhasználó hozzáadása és a fiók lejárati dátumának beállítása:
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
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen szükséges argumentum.

### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs futtatásakor a `jdoe` felhasználó eltávolításra kerül a ***digna*** rendszerből, beleértve a hozzáférések visszavonását és a repository-ban található kapcsolódó adatok és jogosultságok törlését.

## A `modify-user` parancs használata

A `modify-user` parancs a ***digna*** CLI-ben meglévő felhasználó adatainak frissítésére szolgál a ***digna*** rendszerben.

### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
### Opciók  
  
- `--is_superuser`, `-su`: A felhasználó superuserré tétele, emelt jogosultságokkal. Ez a jelző nem igényel értéket.  
- `--valid_until`, `-vu`: Lejárati dátum beállítása a felhasználói fiókra a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
### Példa
  
A `jdoe` felhasználó teljes nevének módosítása “Johnathan Doe”-ra és a felhasználó superuserré tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## A `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben meglévő felhasználó jelszavának megváltoztatására szolgál.
  
### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentumok
  
- **USER_NAME**: A felhasználó felhasználóneve, akinek a jelszavát módosítani kell (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
### Példa
  
A `jdoe` felhasználó jelszavának megváltoztatása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## A `list-users` parancs használata

A `list-users` parancs a ***digna*** CLI-ben az összes regisztrált felhasználó listázására szolgál a ***digna*** rendszerben.

### Parancs használata

```bash
dignacli list-users
```

A parancs futtatása a ***digna*** CLI-ben csatlakozik a ***digna*** repository-hoz és felsorolja az összes felhasználót, megadva azok azonosítóját, felhasználónevét, teljes nevét, superuser státuszát és lejárati idejét.

# Repository-kezelés

### Az `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ezt a parancsot akkor kell használni, amikor frissítéseket alkalmazunk vagy a repository infrastruktúráját állítjuk be először.
  
### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut, kiírva azokat az SQL-utasításokat, amelyeket végrehajtana, de ténylegesen nem futtatja azokat. Hasznos a változtatások előzetes megtekintéséhez anélkül, hogy módosítások történnének a repositoryban.  

  
### Példa
  
A ***digna*** repository frissítéséhez futtassa a parancsot opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
Az upgrade futtatása szimulációs módban (az SQL-utasítások megtekintéséhez anélkül, hogy alkalmazná őket):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs fontos a ***digna*** rendszer karbantartásához, és biztosítja, hogy az adatbázisséma és a többi repository-komponens naprakész legyen a szoftver legújabb verziójával.

## Az `encrypt` parancs használata
  
Az `encrypt` parancs a ***digna*** CLI-ben jelszó titkosítására szolgál.
  
### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
### Példa
  
Jelszó titkosításához adja meg a jelszót argumentumként.   
Például a `mypassword123` jelszó titkosításához használja:
```bash
dignacli encrypt mypassword123
```
A parancs kiírja a megadott jelszó titkosított változatát, amelyet később biztonságos környezetben lehet használni. Ha a jelszó-argumentum nincs megadva, a CLI hibát jelez a hiányzó argumentum miatt.

## A `generate-key` parancs használata
  
A `generate-key` parancs Fernet-kulcs generálására szolgál, amely szükséges a repository-ban tárolt jelszavak védelméhez.
  
### Parancs használata
```bash
dignacli generate-key
```
  
# Adatfeldolgozás

## A `clean-up` parancs használata

A `clean-up` parancs a ***digna*** CLI-ben profilok, predikciók és a Traffic Light Systemből származó adatok eltávolítására szolgál egy vagy több adatforrás esetén egy adott projekten belül. Ez a parancs fontos az adatok életciklus-kezeléséhez, és segít rendezett, hatékony adatkörnyezet fenntartásában az elavult vagy felesleges adatok takarításával.

### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, ahonnan az adatokat törölni kell (kötelező). Ha az argumentumban az all-projects kulcsszót használja, a ***digna*** minden létező projektre iterálva alkalmazza a parancsot.
- **FROM_DATE**: A tisztítás kezdődátuma és időpontja. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: A tisztítás záródátuma és időpontja, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
### Opciók
  
- `--table-name`, `-tn`: A clean-up művelet korlátozása egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűrők alkalmazása, hogy csak azok a táblák legyenek érintettek, melyek nevében megtalálható a megadott részstring.
- `--timing`, `-tm`: A clean-up folyamat időtartamának megjelenítése a befejezés után.
- `--help`: A clean-up parancs súgójának megjelenítése, majd kilépés.
  
### Példa
  
Adatok törlése a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Adatok törlése csak egy konkrét, `Table1` nevű táblából:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében, és biztosítja, hogy a repository csak a releváns információkat tartalmazza.

## Az `inspect` parancs használata

Az `inspect` parancs a ***digna*** CLI-ben profilok, predikciók és a Traffic Light System számára szükséges adatok létrehozására szolgál egy vagy több adatforráshoz egy adott projekten belül. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időtartamon belül.

### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyre az adatok ellenőrzése vonatkozik (kötelező). Ha az argumentumban az all-projects kulcsszót használja, a ***digna*** minden létező projektre iterálva alkalmazza a parancsot.
- **FROM_DATE**: Az ellenőrzés kezdődátuma és időpontja. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az ellenőrzés záródátuma és időpontja, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
### Opciók

- `--table-name`, `-tn`: Az ellenőrzés korlátozása egy adott táblára a projektben.
- `--table-filter`, `-tf`: Csak azoknak a tábláknak az ellenőrzése, amelyek nevében megtalálható a megadott részstring.
- `--do-profile`: Profilok újragyűjtésének indítása. Alapértelmezett: do-profile.
- `--no-do-profile`: Megakadályozza a profilok újragyűjtését.
- `--do-prediction`: Predikciók újraszámításának indítása. Alapértelmezett: do-prediction.
- `--no-do-prediction`: Megakadályozza a predikciók újraszámítását.
- `--do-alert-status`: Riasztási státusz újraszámításának indítása. Alapértelmezett: do-alert-status.
- `--no-do-alert-status`: Megakadályozza a riasztási státusz újraszámítását.
- `--timing`, `-tm`: Az ellenőrzési folyamat időtartamának megjelenítése a befejezés után.
  
### Példa
  
Adatok ellenőrzése a `ProjectA` projekt számára 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy adott tábla ellenőrzése és a predikciók kényszerített újraszámítása:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos friss profilok és predikciók létrehozásához, az adatintegritás figyeléséhez, és a riasztórendszerek kezeléséhez egy adott projekt-időszakon belül.

## A `tls-status` parancs használata

A `tls-status` parancs a ***digna*** CLI-ben arra szolgál, hogy lekérdezze a Traffic Light System (TLS) státuszát egy adott tábla esetén egy projektben egy megadott dátumra. A Traffic Light System betekintést nyújt az adatok minőségébe és állapotába, és jelzi az esetleges problémákat vagy riasztásokat, amelyek figyelmet igényelnek.
  
### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyhez a TLS státusz lekérdezés vonatkozik (kötelező).
- **TABLE_NAME**: A projekt azon konkrét táblája, amelyre a TLS státusz vonatkozik (kötelező).
- **DATE**: A dátum, amelyre a TLS státuszt lekérdezzük, jellemzően %Y-%m-%d formátumban (kötelező).
  
### Példa
  
TLS státusz ellenőrzése a `UserData` nevű táblához a `ProjectA` projektben 2024. július 1-jén:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ez a parancs segít a felhasználóknak az adatok minőségének felügyeletében és fenntartásában az előre definiált kritériumok alapján készített világos és cselekvésre ösztönző státuszjelentéssel.

## A `list-projects` parancs használata
  
A `list-projects` parancs a ***digna*** CLI-ben az összes elérhető projekt listázására szolgál a ***digna*** rendszerben.
  
### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára, gyors áttekintést adva az elérhető projektekről a ***digna*** repository-ban.

## A `list-ds` parancs használata

A `list-ds` parancs a ***digna*** CLI-ben az adott projekthez tartozó összes elérhető adatforrás listázására szolgál. Ez a parancs hasznos annak megértéséhez, hogy mely adaterőforrások állnak rendelkezésre elemzésre és kezelésre a ***digna*** rendszerben.

### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentumok
- **PROJECT_NAME**: A projekt neve, amely számára az adatforrásokat listázni kell (kötelező).
  
### Példa
  
Az összes adatforrás listázása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést nyújt a projekthez tartozó adatforrásokról, és segít hatékonyabban navigálni és kezelni az adatlandscape-et.
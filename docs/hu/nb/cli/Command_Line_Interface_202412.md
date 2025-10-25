---
title: digna CLI Reference 2024.12 – Parancsok & Példák | digna Dokumentáció
description: Teljes referencia a digna CLI kiadásához 2024.12. Ismerd meg, hogyan kezelhetsz felhasználókat, repository-kat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect és még sok más.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Ez az oldal dokumentálja a ***digna*** CLI **2024.12** kiadásában elérhető parancsok teljes készletét, beleértve használati példákat és opciókat.

---


**2024-12-09**


---

## CLI-alapok

---

## A `help` opció használata

A `--help` opció információt nyújt az elérhető parancsokról és azok használatáról. Két fő módja van ennek az opció használatának:

1. **Általános súgó megjelenítése:**
   
    Használd a --help-et rögtön a `dignacli` parancs után  
   ```bash
   dignacli --help

3.  **Súgó konkrét parancsokhoz:**  
  
    Részletes információkért egy konkrét parancsról add hozzá a `--help` opciót a parancs után.
    Például az `add-user` parancs súgójának megjelenítéséhez futtasd:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Parancs leírása:** Részletesen ismerteti, mit csinál a parancs.  
     - **Szin­taxis:** Pontos szintaxist mutat, beleértve a kötelező és választható argumentumokat.  
     - **Opciók:** Felsorolja az adott parancshoz tartozó opciókat és magyarázatukat.  
     - **Példák:** Mutat példákat a parancs hatékony futtatására.

  
## A `check-repo-connection` parancs használata

A `check-repo-connection` parancs a ***digna*** CLI-ben arra szolgál, hogy tesztelje a csatlakozást és az elérést egy megadott ***digna*** repository felé. Ez a parancs biztosítja, hogy a CLI kommunikálni tud a repository-val.
      
### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres futtatás esetén a parancs visszaigazolást ad a csatlakozásról, valamint részleteket a repository-ról: Repository-verzió, Host, Database és Schema.  
  
Ha a repository-hoz való csatlakozás nem sikerül, ellenőrizd a config.toml fájlt a helyes konfigurációs beállításokért.

## A `version` parancs használata

Az telepített *dignacli* verzió ellenőrzéséhez használd a --version opciót.  
  
### Parancs használata
```bash
dignacli --version
```
  
### Példa kimenet
```bash
dignacli version 2024.12
```

## Naplózási opciók használata
  
Alapértelmezés szerint a ***digna*** parancsok konzol-kimenete minimalistára van tervezve. A legtöbb parancs lehetőséget ad további információk megjelenítésére az alábbi opciók használatával:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
A “verbose” és a “debug” meghatározza a részletességi szintet, míg a “logfile” kapcsoló lehetővé teszi a kimenet fájlba irányítását a konzol helyett.

# Felhasználókezelés

## Az `add-user` parancs használata
  
Az `add-user` parancs a ***digna*** CLI-ben új felhasználó hozzáadására szolgál a ***digna*** rendszerhez.
  
### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

### Opciók

- `--is_superuser`, `-su`: Jelző az új felhasználó adminisztrátorrá (superuser) tételéhez.
- `--valid_until`, `-vu`: Beállítja a felhasználói fiók lejárati dátumát a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fióknak nincs lejárati ideje.

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
  
A `delete-user` parancs a ***digna*** CLI-ben egy meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből.
  
### Parancs használata
```bash
dignacli delete-user USER_NAME
```
  
### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen argumentum, amit a parancs igényel.

### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs futtatása eltávolítja a `jdoe` felhasználót a ***digna*** rendszerből, visszavonja hozzáférését és törli a kapcsolódó adatokat és jogosultságokat a repository-ból.

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
  
- `--is_superuser`, `-su`: A felhasználót superuserré teszi és emelt jogosultságokat ad. Ez a kapcsoló nem igényel értéket.  
- `--valid_until`, `-vu`: Beállítja a felhasználói fiók lejárati dátumát a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes marad.  
  
### Példa
  
A `jdoe` felhasználó teljes nevének módosítása “Johnathan Doe”-ra és a felhasználó superuserré tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## A `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben egy meglévő felhasználó jelszavának módosítására szolgál a ***digna*** rendszerben.
  
### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentumok
  
- **USER_NAME**: A jelszót módosítandó felhasználó felhasználóneve (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
### Példa
  
A `jdoe` felhasználó jelszavának módosítása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## A `list-users` parancs használata

A `list-users` parancs a ***digna*** CLI-ben az összes regisztrált felhasználó listázására szolgál a ***digna*** rendszerben.

### Parancs használata

```bash
dignacli list-users
```

A parancs futtatásakor a ***digna*** CLI csatlakozik a ***digna*** repository-hoz és kilistázza az összes felhasználót, megjelenítve azok ID-ját, felhasználónevét, teljes nevét, superuser státuszát és lejárati idejét.

# Repository-kezelés

### Az `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ez a parancs elengedhetetlen a frissítések alkalmazásához vagy a repository infrastruktúra első beállításához.
  
### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
### Opciók
  
- `--simulation-mode`, `-s`: Ha aktiválva van, ez az opció szimulációs módban futtatja a parancsot, és kiírja azokat az SQL utasításokat, amelyek futnának, de nem hajtja végre őket. Hasznos a változások előzetes megtekintéséhez anélkül, hogy tényleges módosításokat végeznénk a repository-ban.  

  
### Példa
  
A ***digna*** repository frissítéséhez futtasd a parancsot opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
Az frissítés szimulációs módban történő futtatásához (az SQL utasítások megtekintéséhez, de alkalmazásuk nélkül):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs fontos a ***digna*** rendszer karbantartásához, és biztosítja, hogy az adatbázisséma és egyéb repository-komponensek összhangban legyenek a szoftver legújabb verziójával.

## Az `encrypt` parancs használata
  
Az `encrypt` parancs a ***digna*** CLI-ben egy jelszó titkosítására szolgál.
  
### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
### Példa
  
Egy jelszó titkosításához add meg a jelszót argumentumként.   
Például a `mypassword123` jelszó titkosításához:
```bash
dignacli encrypt mypassword123
```
A parancs visszaadja a megadott jelszó titkosított változatát, amelyet aztán biztonságos környezetben lehet használni. Ha a jelszó-argumentum nincs megadva, a CLI hibát jelez, amely hiányzó argumentumra utal.

## A `generate-key` parancs használata
  
A `generate-key` parancs Fernet-kulcs generálására szolgál, ami fontos a repository-ban tárolt jelszavak védelméhez.
  
### Parancs használata
```bash
dignacli generate-key
```
  
# Adatkezelés

## A `clean-up` parancs használata

A `clean-up` parancs a ***digna*** CLI-ben arra szolgál, hogy eltávolítson profilokat, predikciókat és adatokat a Traffic Light System-ből egy vagy több adatforrásnál egy megadott projekten belül. Ez a parancs fontos az adatok életciklus-kezeléséhez, és segít fenntartani egy rendezett, hatékony adatkörnyezetet az elavult vagy felesleges adatok takarításával.

### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, ahonnan az adatokat törölni kell (kötelező). Az `all-projects` kulcsszó használata ebben az argumentumban utasítja a ***digna***-t, hogy iteráljon az összes létező projekten és alkalmazza a parancsot mindegyikre.
- **FROM_DATE**: Az adat-takarítás kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adat-takarítás záró dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
### Opciók
  
- `--table-name`, `-tn`: Korlátozza a clean-up műveletet egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűrő, amely korlátozza a clean-up-ot azoknál a tábláknál, amelyek neve tartalmazza a megadott részsztringet.
- `--timing`, `-tm`: A clean-up folyamat futási idejének megjelenítése a befejezés után.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
### Példa
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. közötti időszakra:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Adatok eltávolítása csak egy konkrét, `Table1` nevű táblából:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében és biztosítja, hogy a repository csak a releváns információkat tartalmazza.

## Az `inspect` parancs használata

Az `inspect` parancs a ***digna*** CLI-ben profilok, predikciók és adatok létrehozására szolgál a Traffic Light System számára egy vagy több adatforrásnál egy meghatározott projekten belül. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakon belül.

### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyre az adat-inspketció vonatkozik (kötelező). Az `all-projects` kulcsszó használata ebben az argumentumban utasítja a ***digna***-t, hogy iteráljon az összes létező projekten és alkalmazza a parancsot mindegyikre.
- **FROM_DATE**: Az adat-inspketció kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adat-inspketció záró dátuma és ideje, ugyanazokkal a formátumokkal, mint a FROM_DATE (kötelező).
  
### Opciók

- `--table-name`, `-tn`: Korlátozza az inspecktálást egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűrő, amely csak azokat a táblákat inspectálja, amelyek neve tartalmazza a megadott részsztringet.
- `--do-profile`: Újraprofilozás elindítása. Alapértelmezett: do-profile.
- `--no-do-profile`: Megakadályozza a profilok újragyűjtését.
- `--do-prediction`: Predikciók újraszámolásának indítása. Alapértelmezett: do-prediction.
- `--no-do-prediction`: Megakadályozza a predikciók újraszámolását.
- `--do-alert-status`: Figyelési státusz újraszámolásának indítása. Alapértelmezett: do-alert-status.
- `--no-do-alert-status`: Megakadályozza a figyelési státusz újraszámolását.
- `--iterative`: Naponta iterálva inspectálja az időszakot. Alapértelmezett: iterative.
- `--no-iterative`: Az egész időszak egyszerre történő inspectálását indítja.
- `--timing`, `-tm`: Az inspecktálási folyamat időtartamának megjelenítése a befejezés után.
  
### Példa
  
Adatok inspectálása a `ProjectA` projektben 2024. január 1-től 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy konkrét tábla inspectálása és a predikciók újbóli kiszámítása kényszerítve:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos frissített profilok és predikciók generálásához, az adat-integritás monitorozásához és a figyelési rendszerek kezeléséhez egy adott projektidőszakon belül.

## A `tls-status` parancs használata

A `tls-status` parancs a ***digna*** CLI-ben arra szolgál, hogy lekérdezze a Traffic Light System (TLS) státuszát egy adott tábla esetén egy projekten belül egy megadott dátumra. A Traffic Light System betekintést ad az adatok minőségébe és egészségi állapotába, és jelzi az esetleges problémákat vagy figyelmeztetéseket, amelyek figyelmet igényelnek.
  
### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentumok
  
- **PROJECT_NAME**: A projekt neve, amelyre a TLS státusz lekérdezés vonatkozik (kötelező).
- **TABLE_NAME**: A konkrét tábla a projektben, amelyre a TLS státusz vonatkozik (kötelező).
- **DATE**: A dátum, amelyre a TLS státuszt lekérdezik, általában a %Y-%m-%d formátumban (kötelező).
  
### Példa
  
A `UserData` nevű tábla TLS státuszának ellenőrzése a `ProjectA` projektben 2024. július 1-jére:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ez a parancs segít a felhasználóknak az adatok minőségének monitorozásában és fenntartásában az előre definiált kritériumok alapján történő, egyértelmű és teendő-orientált státuszjelentés nyújtásával.

## A `list-projects` parancs használata
  
A `list-projects` parancs a ***digna*** CLI-ben az összes elérhető projekt listázására szolgál a ***digna*** rendszerben.
  
### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos adminisztrátorok és több projektet kezelő felhasználók számára, és gyors áttekintést ad a rendelkezésre álló projektek listájáról a ***digna*** repository-ban.

## A `list-ds` parancs használata

A `list-ds` parancs a ***digna*** CLI-ben az összes elérhető adatforrás listázására szolgál egy megadott projekten belül. Ez a parancs hasznos a rendelkezésre álló adatforrások áttekintéséhez, amelyek elemzésre és kezelésre állnak rendelkezésre a ***digna*** rendszerben.

### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentumok
- **PROJECT_NAME**: A projekt neve, amelyhez tartozó adatforrásokat listázni kell (kötelező).
  
### Példa
  
Az összes adatforrás listázása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést ad a projektben elérhető adatforrásokról, és segít a felhasználóknak hatékonyabban navigálni és kezelni az adatkörnyezetet.
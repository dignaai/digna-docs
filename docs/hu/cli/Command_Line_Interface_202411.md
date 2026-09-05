---
title: digna CLI Reference 2024.11 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.11. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Ez az oldal a ***digna*** CLI **2024.11** kiadásában elérhető parancsok teljes készletét dokumentálja, beleértve használati példákat és opciókat.


---
## CLI Alapok

---

## `help` opció használata

A `--help` opció információt ad a rendelkezésre álló parancsokról és azok használatáról. Két fő módja van ennek az opciónak a használatára:

1. **Általános súgó megjelenítése:**
   
   Használja a `--help`-et közvetlenül a `dignacli` után:
   ```bash
   dignacli --help
   ```

2. **Specifikus parancsok súgója:**
  
   Egy adott parancs részletes leírásához fűzze hozzá a `--help`-et a parancshoz.
   Például az `add-user` parancs súgójának lekéréséhez futtassa:
   ```bash
   dignacli add-user --help
   ```

   ### kimenet:
      
   - **Parancs leírása:** Részletesen ismerteti, mit csinál a parancs.  
   - **Szintaxis:** Megmutatja a pontos szintaxist, beleértve a kötelező és opcionális argumentumokat.  
   - **Opciók:** Felsorolja a parancshoz tartozó opciókat és azok magyarázatát.  
   - **Példák:** Megad példákat a parancs hatékony használatára.

  
## `check-repo-connection` parancs használata

A `check-repo-connection` parancs a ***digna*** CLI eszköz azon segédprogramja, amely a megadott ***digna*** repository elérhetőségét és hozzáférését teszteli. Ez a parancs biztosítja, hogy a CLI képes kommunikálni a repository-val.
      
### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres végrehajtás esetén a parancs megerősíti a kapcsolatot, és részleteket ad a repository-ról: Repository verzió, Host, Adatbázis és Schema.  
  
Ha a repository-hoz való kapcsolódás sikertelen, ellenőrizze a config.toml fájlt a helyes konfigurációs beállításokért.

## `version` parancs használata

A telepített *dignacli* verziójának lekérdezéséhez használja a `--version` opciót.  
  
### Parancs használata
```bash
dignacli --version
```
  
### Példa kimenet
```bash
dignacli version 2024.11
```

## Naplózási opciók használata
  
Alapértelmezés szerint a ***digna*** parancsok konzol kimenete minimalista. A legtöbb parancs lehetőséget kínál további információk megjelenítésére az alábbi opciók használatával:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A „verbose” és a „debug” a részletezettségi szintet határozza meg, míg a „logfile” kapcsoló lehetővé teszi a kimenet fájlba történő átirányítását a konzol helyett.

# Felhasználókezelés

## `add-user` parancs használata
  
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

- `--is_superuser`, `-su`: Jelző, amely adminisztrátori jogosultságot ad az új felhasználónak.
- `--valid_until`, `-vu`: Azonosítja a felhasználói fiók lejárati idejét a `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fiók nem jár le.

### Példa

Egy új felhasználó hozzáadásához `jdoe` felhasználónévvel, teljes névvel `John Doe`, és jelszóval `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Egy új felhasználó hozzáadásához és fióklejárat beállításához:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` parancs használata
  
A `delete-user` parancs a ***digna*** CLI-ben meglévő felhasználó törlésére szolgál a ***digna*** rendszerből.
  
### Parancs használata
```bash
dignacli delete-user USER_NAME
```
  
### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen kötelező argumentuma a parancsnak.

### Példa
```bash
dignacli delete-user jdoe
```
  
A parancs végrehajtásakor a `jdoe` felhasználó hozzáférése megszűnik, és a hozzátartozó adatai és jogosultságai törlődnek a repository-ból.

## `modify-user` parancs használata

A `modify-user` parancs a ***digna*** CLI-ben meglévő felhasználó adatainak frissítésére szolgál a ***digna*** rendszerben.

### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
### Opciók  
  
- `--is_superuser`, `-su`: A felhasználót superuserré (rendszergazdává) teszi, emelt jogosultságokat adva. Ennek a kapcsolónak nincs értéke.  
- `--valid_until`, `-vu`: Beállítja a felhasználói fiók lejárati idejét a YYYY-MM-DD HH:MI:SS formátumban. Ha nincs megadva, a fiók érvényessége határozatlan marad.  
  
### Példa
  
A `jdoe` felhasználó teljes nevének módosítása „Johnathan Doe”-ra és superuserként történő beállítása:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs a ***digna*** CLI-ben meglévő felhasználó jelszavának megváltoztatására szolgál a ***digna*** rendszerben.
  
### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentumok
  
- **USER_NAME**: A felhasználó felhasználóneve, akinek a jelszavát módosítani kell (kötelező).
- **USER_PWD**: Az új jelszó (kötelező).
  
### Példa
  
A `jdoe` felhasználó jelszavának megváltoztatása `newpassword123`-ra:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` parancs használata

A `list-users` parancs a ***digna*** CLI-ben megjeleníti az összes, a ***digna*** rendszerben regisztrált felhasználót.

### Parancs használata

```bash
dignacli list-users
```

A parancs futtatásakor a ***digna*** CLI csatlakozik a ***digna*** repository-hoz, és listázza az összes felhasználót, megjelenítve az ID-t, felhasználónevet, teljes nevet, superuser státuszt és a lejárati időbélyegeket.

# Repository kezelés

### `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ez a parancs elengedhetetlen a frissítések alkalmazásához vagy a repository infrastruktúrájának első beállításához.
  
### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut, ami kiírja azokat az SQL utasításokat, amelyeket végrehajtana, de nem hajtja végre őket. Ez hasznos a módosítások előnézetéhez anélkül, hogy a repository-t megváltoztatná.  

  
### Példa
  
A ***digna*** repository frissítéséhez futtassa a parancsot opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
Ha szimulációs módban szeretné futtatni a frissítést (látni az SQL utasításokat anélkül, hogy alkalmazná őket):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kulcsfontosságú a ***digna*** rendszer karbantartásához, biztosítva, hogy az adatbázis séma és a repository komponensei naprakészek legyenek a szoftver legújabb verziójával.

## `encrypt` parancs használata
  
Az `encrypt` parancs a ***digna*** CLI-ben jelszó titkosítására szolgál.
  
### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
### Példa
  
Egy jelszó titkosításához meg kell adni a jelszót argumentumként.   
Például a `mypassword123` jelszó titkosításához használja:
```bash
dignacli encrypt mypassword123
```
A parancs visszaadja a megadott jelszó titkosított változatát, amelyet aztán biztonságos környezetben használhat. Ha a jelszó argumentum nincs megadva, a CLI hibaüzenetet jelenít meg a hiányzó argumentum miatt.

## `generate-key` parancs használata
  
A `generate-key` parancs Fernet kulcs generálására szolgál, amely szükséges a ***digna*** repository-ban tárolt jelszavak védelméhez.
  
### Parancs használata
```bash
dignacli generate-key
```
  
# Adatkezelés

## `clean-up` parancs használata

A `clean-up` parancs a ***digna*** CLI-ben profilok, predikciók és a Traffic Light System adatok törlésére szolgál egy vagy több adatforrás esetén egy adott projektben. Ez a parancs fontos az adatok életciklus-kezeléséhez, segít fenntartani az áttekinthető és hatékony adatkörnyezetet az elavult vagy felesleges adatok törlésével.

### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyből az adatokat törölni kell (kötelező). Ha az `all-projects` kulcsszót használja, a ***digna*** végigiterál az összes meglévő projekten és alkalmazza rájuk a parancsot.
- **FROM_DATE**: Az adatok törlésének kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adatok törlésének befejező dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
### Opciók
  
- `--table-name`, `-tn`: Korlátozza a clean-up műveletet egy adott táblára a projekten belül.
- `--table-filter`, `-tf`: Szűrő, amely csak azokat a táblákat érinti, amelyek nevében megtalálható a megadott részstring.
- `--timing`, `-tm`: A művelet befejezése után megjeleníti a clean-up időtartamát.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
### Példa
  
Adatok eltávolítása a ProjectA projektből 2023. január 1. és 2023. június 30. között:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Csak egy konkrét `Table1` nevű táblából történő adatok eltávolításához:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás kezelésében, és biztosítja, hogy a repository csak a releváns információkat tartalmazza.

## `inspect` parancs használata

Az `inspect` parancs a ***digna*** CLI-ben profilok, predikciók és a Traffic Light System adatok létrehozására szolgál egy vagy több adatforráshoz egy adott projektben. Ez a parancs segít az adatok elemzésében és monitorozásában egy meghatározott időszakon belül.

### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyben az adatokat vizsgálni kell (kötelező). Ha az `all-projects` kulcsszót használja, a ***digna*** végigiterál az összes meglévő projekten és alkalmazza rájuk a parancsot.
- **FROM_DATE**: Az adatellenőrzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adatellenőrzés befejező dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
### Opciók

- `--table-name`, `-tn`: Korlátozza az inspectet egy adott táblára a projekten belül.
- `--table-filter`, `-tf`: Csak azokat a táblákat vizsgálja, amelyek nevében megtalálható a megadott részstring.
- `--do-profile`: Profilok újragyűjtését indítja el. Alapértelmezett: do-profile.
- `--no-do-profile`: Megakadályozza a profilok újragyűjtését.
- `--do-prediction`: Predikciók újraszámítását indítja el. Alapértelmezett: do-prediction.
- `--no-do-prediction`: Megakadályozza a predikciók újraszámítását.
- `--do-alert-status`: Riasztási státuszok újraszámítását indítja el. Alapértelmezett: do-alert-status.
- `--no-do-alert-status`: Megakadályozza a riasztási státuszok újraszámítását.
- `--timing`, `-tm`: A művelet befejezése után megjeleníti az inspect futásidejét.
  
### Példa
  
Adatok ellenőrzése a `ProjectA` projektben 2024. január 1-jétől 2024. január 31-ig:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy konkrét tábla ellenőrzése és a predikciók újraszámításának kikényszerítése:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos friss profilok és predikciók generálásához, az adatok integritásának monitorozásához és a riasztási rendszerek kezeléséhez egy adott projekt időszakán belül.

## `tls-status` parancs használata

A `tls-status` parancs a ***digna*** CLI-ben a Traffic Light System (TLS) státuszának lekérdezésére szolgál egy adott projekt egy adott táblájára és egy megadott dátumra. A Traffic Light System betekintést ad az adatok egészségébe és minőségébe, jelezve az esetleges problémákat vagy riasztásokat, amelyek figyelmet igényelhetnek.
  
### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentumok
  
- **PROJECT_NAME**: Annak a projektnek a neve, amelyre a TLS státuszt kérdezi (kötelező).
- **TABLE_NAME**: A projekt azon konkrét táblája, amelyre a TLS státuszt kéri (kötelező).
- **DATE**: Az a dátum, amelyre a TLS státuszt lekérdezi, általában a %Y-%m-%d formátumban (kötelező).
  
### Példa
  
A `ProjectA` projekt `UserData` nevű táblájának TLS státuszának lekérdezése 2024. július 1-jén:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ez a parancs segít a felhasználóknak az adatok minőségének monitorozásában és fenntartásában az előre definiált kritériumok alapján adható világos és cselekvésre alkalmas státuszjelentéssel.

## `list-projects` parancs használata
  
A `list-projects` parancs a ***digna*** CLI-ben az összes elérhető projekt listázására szolgál a ***digna*** rendszerben.
  
### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára, gyors áttekintést adva a repository-ban elérhető projektekről.

## `list-ds` parancs használata

A `list-ds` parancs a ***digna*** CLI-ben az egy adott projekthez tartozó összes elérhető adatforrás listázására szolgál. Ez a parancs hasznos az elemzésre és kezelésre rendelkezésre álló adatvagyon megismeréséhez a ***digna*** rendszerben.

### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentumok
- **PROJECT_NAME**: Annak a projektnek a neve, amelyhez az adatforrásokat listázni szeretné (kötelező).
  
### Példa
  
Az összes adatforrás listázása a `ProjectA` nevű projektben:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést nyújt a projektben elérhető adatforrásokról, segítve a felhasználókat az adatkörnyezet hatékonyabb navigálásában és kezelésében.
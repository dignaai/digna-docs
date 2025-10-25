---
title: digna CLI Referencia 2024.12 – Parancsok & Példák | digna Dokumentáció
description: Teljes referencia a digna CLI 2024.12 verziójához. Tanulja meg, hogyan kezelje a felhasználókat, repository-kat és adatokat olyan parancsokkal, mint az add-user, check-repo-connection, upgrade-repo, inspect és még sok más.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Referencia 2024.12
**2024-12-09**

Ez az oldal dokumentálja az összes parancsot, használati példát és opciót, amely a ***digna*** CLI **2024.12** verziójában elérhető.

---


**2024-12-09**


---

## CLI alapok

---

## `help` opció használata

A `--help` opció információt nyújt az elérhető parancsokról és azok használatáról. Ennek két fő használati módja van:

1. **Általános segítség megjelenítése:**
   
    Használja a `--help`-et közvetlenül a `dignacli` parancs után.  
   ```bash
   dignacli --help
   ```

2. **Specifikus parancsokhoz tartozó segítség:**
  
    Részletes információkért egy adott parancsról adja hozzá a `--help`-et az adott parancshoz.  
    Például az `add-user` parancs súgójának megtekintéséhez futtassa:
     ```bash
     dignacli add-user --help
     ```

     ### Kimenet:
      
     - **Parancs leírása:** Részletezi, mit végez a parancs.  
     - **Szinaxis:** Megmutatja a teljes szintaxist, beleértve a kötelező és opcionális argumentumokat.  
     - **Opciók:** Listázza a parancshoz tartozó opciókat és azok magyarázatát.  
     - **Példák:** Mutat példákat a parancs hatékony használatára.

  
## `check-repo-connection` parancs használata

A `check-repo-connection` parancs a ***digna*** CLI-ben egy segédparancs, amely egy adott ***digna*** repository-hoz való kapcsolódást és hozzáférést teszteli. A parancs igazolja, hogy a CLI képes kommunikálni a repository-val.
      
### Parancs használata
```bash
dignacli check-repo-connection
```

Sikeres futtatás esetén a parancs megerősíti a kapcsolatot és kiírja a repository-val kapcsolatos információkat, például Repository version, Host, Database és Schema.  
  
Ha a repository-hoz való csatlakozás nem sikerül, ellenőrizze a config.toml fájl megfelelő konfigurációs beállításait.

## `version` parancs használata

A telepített *dignacli* verziójának ellenőrzéséhez használja a `--version` opciót.  
  
### Parancs használata
```bash
dignacli --version
```
  
### Példa kimenet
```bash
dignacli version 2024.12
```

## Naplózási (logging) opciók használata
  
Alapértelmezés szerint a ***digna*** parancsok konzol-kimenete minimalista. A legtöbb parancs lehetőséget ad további információk megjelenítésére az alábbi opciók használatával:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
A „verbose” és a „debug” a részletességi szintet határozza meg, míg a „logfile” opció a kimenetet konzol helyett fájlba irányítja.

# Felhasználókezelés

## `add-user` parancs használata
  
Az `add-user` parancs új felhasználó hozzáadására szolgál a ***digna*** rendszerhez a ***digna*** CLI-n keresztül.
  
### Parancs használata
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentumok

- **USER_NAME**: Az új felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: Az új felhasználó teljes neve (kötelező).
- **USER_PASSWORD**: Az új felhasználó jelszava (kötelező).

### Opciók

- `--is_superuser`, `-su`: Flag az új felhasználó rendszergazdává (szuperfelhasználóvá) tétele céljából.
- `--valid_until`, `-vu`: Meghatározza a felhasználói fiók lejárati dátumát `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fióknak nincs lejárati ideje.

### Példa

Egy új felhasználó létrehozása jdoe felhasználónévvel, teljes névvel John Doe és jelszóval password123:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Egy felhasználó létrehozása lejárati dátummal:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` parancs használata
  
A `delete-user` parancs meglévő felhasználó eltávolítására szolgál a ***digna*** rendszerből a ***digna*** CLI használatával.
  
### Parancs használata
```bash
dignacli delete-user USER_NAME
```
  
### Argumentumok
- **USER_NAME**: A törlendő felhasználó felhasználóneve (kötelező). Ez az egyetlen argumentum, amelyre a parancsnak szüksége van.

### Példa
```bash
dignacli delete-user jdoe
```
  
Ennek a parancsnak a futtatása eltávolítja a `jdoe` felhasználót a ***digna*** rendszerből, visszavonja a hozzáférését, és törli a repository-ban kapcsolódó engedélyeket és adatokat.

## `modify-user` parancs használata

A `modify-user` parancs meglévő felhasználó adatait frissíti a ***digna*** CLI-ben.

### Parancs használata
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentumok
  
- **USER_NAME**: A módosítandó felhasználó felhasználóneve (kötelező).
- **USER_FULL_NAME**: A felhasználó új teljes neve (kötelező).
  
### Opciók  
  
- `--is_superuser`, `-su`: A felhasználót szuperfelhasználóként állítja be, emelt privilégiumokkal. Ez a flag nem igényel értéket.  
- `--valid_until`, `-vu`: Meghatározza a felhasználói fiók lejárati dátumát `YYYY-MM-DD HH:MI:SS` formátumban. Ha nincs megadva, a fiók határozatlan ideig érvényes.  
  
### Példa
  
A `jdoe` felhasználó teljes nevének `Johnathan Doe`-ra módosítása és szuperfelhasználóvá tétele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` parancs használata
  
A `modify-user-pwd` parancs egy meglévő felhasználó jelszavának megváltoztatására szolgál a ***digna*** CLI-ben.
  
### Parancs használata
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentumok
  
- **USER_NAME**: A jelszót módosítandó felhasználó felhasználóneve (kötelező).
- **USER_PWD**: A felhasználó új jelszava (kötelező).
  
### Példa
  
A `jdoe` felhasználó jelszavának `newpassword123`-ra változtatása:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` parancs használata

A `list-users` parancs a ***digna*** rendszerben regisztrált összes felhasználó felsorolására szolgál a ***digna*** CLI-ben.

### Parancs használata

```bash
dignacli list-users
```

Ezt a parancsot futtatva a CLI csatlakozik a ***digna*** repository-hoz és listázza az összes felhasználót; megjelenítve az ID-t, felhasználónevet, teljes nevet, szuperfelhasználói státuszt és a lejárati időbélyegeket.

# Repository kezelés

### `upgrade-repo` parancs használata
  
Az `upgrade-repo` parancs a ***digna*** CLI-ben a ***digna*** repository frissítésére vagy inicializálására szolgál. Ezt a parancsot a frissítések alkalmazásához vagy a repository infrastruktúra első beállításához kell használni.
  
### Parancs használata

```bash
dignacli upgrade-repo [options]
```
  
### Opciók
  
- `--simulation-mode`, `-s`: Ha engedélyezve van, a parancs szimulációs módban fut; kiírja a végrehajtandó SQL utasításokat, de ténylegesen nem alkalmazza azokat. Hasznos a változtatások végrehajtása előtti előnézethez, anélkül, hogy módosítaná a repository-t.  

  
### Példa
  
A ***digna*** repository frissítése opciók nélkül:
  
```bash
dignacli upgrade-repo
```  
A frissítés szimulációs módban történő futtatása (az SQL utasítások megjelenítése, de nem végrehajtása):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ez a parancs kritikus szerepet játszik a ***digna*** rendszer karbantartásában; biztosítja, hogy az adatbázis sémája és a repository egyéb összetevői kompatibilisek legyenek a szoftver legújabb verziójával.

## `encrypt` parancs használata
  
Az `encrypt` parancs egy jelszó titkosítására szolgál a ***digna*** CLI-ben.
  
### Parancs használata
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentumok
- **PASSWORD**: A titkosítandó jelszó (kötelező).
  
### Példa
  
Egy jelszó titkosításához adja meg a jelszót argumentumként.  
Például a `mypassword123` jelszó titkosításához:
```bash
dignacli encrypt mypassword123
```
A parancs kiadja a megadott jelszó titkosított változatát; ezt a kimenetet később biztonságosabb kontextusokban használhatja. Ha nem ad meg jelszó-argumentumot, a CLI hibát jelez a hiányzó argumentum miatt.

## `generate-key` parancs használata
  
A `generate-key` parancs egy Fernet kulcsot generál, amely a repository-ban tárolt jelszavak védelméhez szükséges a ***digna*** rendszerben.
  
### Parancs használata
```bash
dignacli generate-key
```
  
# Adatkezelés

## `clean-up` parancs használata

A `clean-up` parancs a ***digna*** CLI-ben egy vagy több adatforrás profiljainak, predikcióinak és a Forgalmi Lámpa Rendszer (TLS) adatait törli egy adott projekt keretében. Ez a parancs fontos az adatok életciklus-kezeléséhez, és segít rendszerezett, hatékony adatkörnyezet fenntartásában az elavult vagy felesleges adatok eltávolításával.

### Parancs használata

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelyből az adatokat törölni kell (kötelező). Ha az argumentum értéke all-projects, akkor a ***digna*** végigiterál minden projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az adateltávolítás kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az adateltávolítás záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
### Opciók
  
- `--table-name`, `-tn`: Korlátozza a törlést egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűrőt alkalmaz, hogy csak azok a táblák legyenek érintettek, amelyek neve adott alstringet tartalmaz.
- `--timing`, `-tm`: Megmutatja a törlési művelet befejezéséhez szükséges időt.
- `--help`: Megjeleníti a clean-up parancs súgóját és kilép.
  
### Példa
  
Az adat eltávolítása a ProjectA projektből 2023.01.01 és 2023.06.30 közötti időszakra:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Csak a `Table1` nevű táblából való törléshez:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ez a parancs segít az adattárolás menedzselésében és abban, hogy a repository csak a releváns információkat tartalmazza.

## `inspect` parancs használata

Az `inspect` parancs a ***digna*** CLI-ben profilok, predikciók és a Forgalmi Lámpa Rendszer (TLS) adatainak létrehozására szolgál egy vagy több adatforrásra egy adott projekt keretében. A parancs segít az adatelemzésben és a monitorozásban egy megadott időszakon belül.

### Parancs használata

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelynek adatait elemezni kell (kötelező). Ha az argumentum értéke all-projects, akkor a ***digna*** végigiterál minden projekten és alkalmazza a parancsot.
- **FROM_DATE**: Az elemzés kezdő dátuma és ideje. Elfogadott formátumok: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vagy %Y-%m-%d %H:%M:%S (kötelező).
- **TO_DATE**: Az elemzés záró dátuma és ideje, ugyanazokat a formátumokat követve, mint a FROM_DATE (kötelező).
  
### Opciók

- `--table-name`, `-tn`: Korlátozza az elemzést egy adott táblára a projektben.
- `--table-filter`, `-tf`: Szűrőt alkalmaz azokra a táblákra, amelyek neve adott alstringet tartalmaz.
- `--do-profile`: Újraindítja a profilok gyűjtését. Alapértelmezett: do-profile.
- `--no-do-profile`: Megakadályozza a profilok újragyűjtését.
- `--do-prediction`: Újraszámolja a predikciókat. Alapértelmezett: do-prediction.
- `--no-do-prediction`: Megakadályozza a predikciók újraszámolását.
- `--do-alert-status`: Újraszámolja az riasztási állapotokat. Alapértelmezett: do-alert-status.
- `--no-do-alert-status`: Megakadályozza az riasztási állapotok újraszámolását.
- `--iterative`: A megadott időszakot napi iterációkkal elemzi. Alapértelmezett: iterative.
- `--no-iterative`: Az egész időszak egyszerre történő elemzését kényszeríti.
- `--timing`, `-tm`: Megmutatja az elemzés befejezéséhez szükséges időt.
  
### Példa
  
A `ProjectA` projekt 2024.01.01 és 2024.01.31 közötti adatainak vizsgálata:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Csak egy adott tábla vizsgálata és a predikciók újraszámolásának kikényszerítése:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ez a parancs hasznos friss profilok és predikciók létrehozásához, az adatintegritás monitorozásához, és a megadott projekt-időintervallumon belüli riasztási rendszerek kezeléséhez.

## `tls-status` parancs használata

A `tls-status` parancs a ***digna*** CLI-ben egy projekt adott táblájának egy megadott időpontra vonatkozó Forgalmi Lámpa Rendszer (TLS) állapotát kérdezi le. A Forgalmi Lámpa Rendszer információkat ad az adatok egészségéről és minőségéről, valamint jelzi a potenciális problémákat vagy riasztásokat.
  
### Parancs használata
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentumok
  
- **PROJECT_NAME**: Az a projekt, amelyben a TLS állapotot lekérdezik (kötelező).
- **TABLE_NAME**: A projektben a vizsgálandó tábla neve (kötelező).
- **DATE**: A TLS állapot lekérdezésének dátuma, általában %Y-%m-%d formátumban (kötelező).
  
### Példa
  
A `ProjectA` projekt `UserData` nevű táblájának 2024-07-01 napi TLS állapotának ellenőrzése:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ez a parancs előre definiált kritériumok alapján egy világos és használható állapotjelentést ad, segítve a felhasználókat az adatminőség nyomon követésében és fenntartásában.

## `list-projects` parancs használata
  
A `list-projects` parancs az összes elérhető projekt listáját jeleníti meg a ***digna*** CLI-ben.
  
### Parancs használata
  
```bash
dignacli list-projects
```

Ez a parancs különösen hasznos rendszergazdák és több projektet kezelő felhasználók számára; gyors áttekintést ad a repository-ban lévő meglévő projektekről.

## `list-ds` parancs használata

A `list-ds` parancs egy adott projektben lévő összes elérhető adatforrást listázza a ***digna*** CLI-ben. A parancs segít megérteni, milyen adatvagyonok állnak rendelkezésre elemzésre és kezelésre.

### Parancs használata
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentumok
- **PROJECT_NAME**: Az a projekt, amelynek adatforrásait listázni szeretné (kötelező).
  
### Példa
  
Az `ProjectA` projekt összes adatforrásának listázásához:
  
```bash
dignacli list-ds ProjectA
```
  
Ez a parancs áttekintést nyújt a projektben elérhető adatforrásokról, segítve a hatékonyabb adatkezelést és -tervezést.